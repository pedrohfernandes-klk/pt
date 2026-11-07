"""01/11/2026: apresentação das páginas corrigidas e segurança do itálico do exame."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import re
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass


# 02/11/2026: posição do texto de cada rótulo .verso>b (não da caixa, que pode ser mais estreita do que o texto)
# e do primeiro caráter visível que se lhe segue.
ROTULOS=r"""()=>[...document.querySelectorAll('.casca.sobreposta .verso>b')].map(b=>{
  const w=document.createTreeWalker(b.parentNode,NodeFilter.SHOW_TEXT);let n,txt=null;
  while((n=w.nextNode())){if(b.contains(n))continue;if((b.compareDocumentPosition(n)&Node.DOCUMENT_POSITION_FOLLOWING)&&n.textContent.trim()){txt=n;break}}
  const qr=document.createRange();qr.selectNodeContents(b);const q=qr.getBoundingClientRect();
  if(!txt)return {rot:b.textContent,dir:q.right,ini:null,mesma:false};
  const k=txt.textContent.search(/\S/),r=document.createRange();r.setStart(txt,k);r.setEnd(txt,k+1);
  const c=r.getBoundingClientRect();
  return {rot:b.textContent,dir:q.right,ini:c.left,mesma:Math.abs((c.top+c.bottom)/2-(q.top+q.bottom)/2)<q.height/2}})"""

def main():
    manifest=json.loads((ROOT/'tests/fixtures/varredura-formatacao-edits-20261101.json').read_text('utf-8'))
    pages=[p for p in manifest['files'] if p.endswith('.html')]
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    host=f'http://127.0.0.1:{server.server_port}'
    checked=0
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for width in (390,1366):
                ctx=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
                ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith(host) else r.abort())
                page=ctx.new_page()
                for path in pages:
                    errors=[]
                    def error(e):errors.append(str(e))
                    page.on('pageerror',error)
                    page.goto(host+'/'+path,wait_until='load')
                    page.wait_for_timeout(100)
                    assert page.locator('body').inner_text().strip(),path
                    assert not errors,(path,errors)
                    visible=page.locator('body').inner_text()
                    assert not re.search(r'(?<![\w/])_[^_\n]+_(?!\w)',visible),(path,visible[:200])
                    page.remove_listener('pageerror',error)
                    checked+=1
                # O título vem dos dados, mas apresenta-se como itálico, sem mostrar etiquetas.
                page.goto(host+'/exame/#s08/escrever',wait_until='networkidle')
                assert page.locator('.writing-task i').filter(has_text='Amor de Perdição').count()==1
                assert '_Amor de Perdição_' not in page.locator('.writing-task').inner_text()
                # Os títulos mantêm o itálico quando o docente lança o cartão do painel.
                for slug,book in [('m3/painel-m3-f10','Os Lusíadas'),('m7/painel-m7-f10','Frei Luís de Sousa'),('m9/painel-m9-f07','Os Maias')]:
                    page.goto(host+'/'+slug+'/',wait_until='load')
                    value=page.locator('[data-r-k] option').filter(has_text=book).first.get_attribute('value')
                    page.locator('[data-r-k]').select_option(value)
                    page.locator('[data-relampago]').click()
                    assert page.locator('[data-pedido] i').filter(has_text=book).count()==1,slug
                # Créditos legíveis e sem alargar o ecrã; a data incerta continua declarada.
                page.goto(host+'/m7/mapa-do-modulo-m7/',wait_until='load')
                page.locator('#galeria > summary').click()
                # 01/11/2026: crédito imediatamente visível, tipografia subordinada e ligação conservada.
                # 05/11/2026: decisão 153 (docente: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir»)
                # substitui o crédito imediatamente visível: o «i» vê-se, fechado; aberto, os seis campos veem-se, com a mesma
                # tipografia subordinada (13,1 px ou menos) e a ligação conservada; «Lição M7-F01» continua à vista, fora do «i».
                ii=page.locator('#galeria details.info-i:has(a[href*="File:PessoaChapeu.jpg"])')
                assert ii.count()==1
                assert ii.locator('summary').is_visible()
                assert not ii.evaluate('d=>d.open')
                ii.locator('summary').click()
                credito=ii.locator('.info-i-texto')
                assert credito.is_visible()
                for field in ('Fotógrafo não identificado;','retrato de Fernando Pessoa com chapéu;','cerca de 1914 (data incerta);',
                              'original sem instituição indicada;','domínio público'):
                    assert field in credito.inner_text(),field
                assert credito.locator('a[href*="File:PessoaChapeu.jpg"]').is_visible()
                assert credito.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')<=13.1
                licao=page.locator('#galeria figcaption').filter(has_text='Fernando Pessoa, cerca de 1914.').get_by_text('Lição M7-F01')
                assert licao.count()==1 and licao.is_visible()
                assert licao.evaluate('a=>!a.closest("details.info-i")')
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                # 01/11/2026: as palavras tocáveis mantêm o itálico, sem expor os marcadores.
                page.goto(host+'/m7/licao-m7-f01/',wait_until='load')
                raw=(ROOT/'m7/licao-m7-f01/index.html').read_text('utf-8')
                start=re.search(r'CARTOES\s*=\s*',raw).end()
                card=json.JSONDecoder().raw_decode(raw[start:])[0][16]
                page.evaluate('x=>{window.checkCasca=EPICasca.abrir({semVoltar:true});EPIJogo.montar({casca:checkCasca,itens:[x],chave:"qa-formatacao"})}',card)
                assert page.locator('.casca.sobreposta .pal').count()==8
                assert '_' not in page.locator('.casca.sobreposta').inner_text()
                assert page.locator('.casca.sobreposta .pal i').count()==4
                # 02/11/2026: os rótulos de fala das lições («Fidalgo:», «Sapateiro:») não ficam por cima do verso:
                # o lado direito do rótulo não passa do primeiro caráter do texto que se segue na mesma linha.
                for slug,idx in [('m2/licao-m2-f12',3),('m2/licao-m2-f13',1),('m2/licao-m2-f13',3)]:
                    page.goto(host+'/'+slug+'/',wait_until='load')
                    raw=(ROOT/slug/'index.html').read_text('utf-8')
                    start=re.search(r'CARTOES\s*=\s*',raw).end()
                    card=json.JSONDecoder().raw_decode(raw[start:])[0][idx]
                    page.evaluate('x=>{window.checkCasca=EPICasca.abrir({semVoltar:true});EPIJogo.montar({casca:checkCasca,itens:[x],chave:"qa-rotulos"})}',card)
                    medidas=page.evaluate(ROTULOS)
                    assert len(medidas)>=2,(slug,idx,width)
                    for m in medidas:
                        assert m['ini'] is not None,(slug,idx,width,m)
                        if m['mesma']:assert m['dir']<=m['ini']+1,(slug,idx,width,m)
                for slug,phrase in [('m2/visita-farsa-de-ines-pereira-no-teatro','cena: Farsa'),('m4/visita-frei-luis-de-sousa-no-teatro','palco: Frei')]:
                    page.goto(host+'/'+slug+'/',wait_until='load')
                    assert phrase in page.locator('.migalhas [aria-current]').inner_text(),slug
                # Todas as sessões e fases; responder revela também os retornos formatados.
                sessions=json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))['sessions']
                for session in sessions:
                    for phase in ('aquecer','ler','escrever','corrigir','fechar'):
                        page.goto(host+'/exame/#'+session['id']+'/'+phase,wait_until='networkidle')
                        # 01/11/2026: a rota aguarda IndexedDB; conferir a fase e a sessão antes de tocar.
                        page.wait_for_function('x=>document.body.dataset.fase===x.phase && document.querySelector(".session-heading h1")?.textContent===x.title',arg={'phase':phase,'title':session['title']})
                        if phase=='corrigir':page.locator('[data-action="reveal"]').click()
                        for question in page.locator('.question').all():
                            choice=question.locator('button:not([disabled])').first
                            if choice.count():choice.click()
                            question.locator('.feedback').wait_for(state='visible')
                        assert not re.search(r'(?<![\w/])_[^_\n]+_(?!\w)',page.locator('#app').inner_text()),(session['id'],phase,width)
                # Cópia HTML legível, com os dados de reposição intactos.
                exported=page.evaluate("""async sessions=>{
                  for(const s of sessions) await PTExameDossier.saveEntry({sessionId:s.id,title:s.title,session:s,notes:'',revisedText:'',answers:{},checklist:{},photos:[]});
                  return await (await PTExameDossier.exportHTML()).text();
                }""",sessions)
                export_page=ctx.new_page();export_page.set_content(exported)
                assert not re.search(r'(?<![\w/])_[^_\n]+_(?!\w)',export_page.locator('body').inner_text())
                restored=json.loads(export_page.locator('#pt-exame-dossier-data').text_content())
                assert {x['sessionId']:x['session'] for x in restored['entries']}=={x['id']:x for x in sessions}
                export_page.close()
                ctx.close()
            # O escape precede o itálico: conteúdo semelhante a HTML continua texto inerte.
            ctx=browser.new_context();page=ctx.new_page()
            source=(ROOT/'assets/exame/app.js').read_text('utf-8')
            esc=re.search(r'const e=v=>.*?;\n',source)[0]
            italic=re.search(r'const f=v=>.*?;\n',source)[0]
            result=page.evaluate('() => {'+esc+italic+'return f("_<img src=x onerror=alert(1)>_");}')
            assert '<img' not in result and '&lt;img' in result,result
            ctx.close();browser.close()
        print(f'PASS {checked} aberturas, duas larguras, itálico do exame, créditos e escape de HTML')
    finally:
        server.shutdown()


if __name__=='__main__':main()
