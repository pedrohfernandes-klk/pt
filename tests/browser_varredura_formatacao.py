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
                assert page.locator('#galeria .tabela').is_visible()
                assert 'não identificado' in page.locator('#galeria .tabela').inner_text()
                assert page.locator('#galeria .tabela').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')<=13.1
                assert page.locator('#galeria figcaption').filter(has_text='Fernando Pessoa, cerca de 1914.').get_by_text('Lição M7-F01').count()==1
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
                for slug,phrase in [('m2/visita-farsa-de-ines-pereira-no-teatro','cena: Farsa'),('m4/visita-frei-luis-de-sousa-no-teatro','palco: Frei')]:
                    page.goto(host+'/'+slug+'/',wait_until='load')
                    assert phrase in page.locator('.migalhas [aria-current]').inner_text(),slug
                # Todas as sessões e fases; responder revela também os retornos formatados.
                sessions=json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))['sessions']
                for session in sessions:
                    for phase in ('aquecer','ler','escrever','corrigir','fechar'):
                        page.goto(host+'/exame/#'+session['id']+'/'+phase,wait_until='networkidle')
                        if phase=='corrigir':page.locator('[data-action="reveal"]').click()
                        for question in page.locator('.question').all():
                            choice=question.locator('button:not([disabled])').first
                            if choice.count():choice.click()
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
