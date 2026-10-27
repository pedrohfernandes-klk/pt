"""Tabelas «Encomenda por curso» (27/10/2026): legíveis do telemóvel à projeção.

M2-F09, M6-F08, M8-F10 e M9-F05 têm, num cartão de leitura, a tabela das encomendas por curso dentro de
«Desenvolver a proposta no projeto de turma». Confere-se, no motor real: todas as linhas e células visíveis,
nenhum transbordo horizontal; até 560 px cada linha empilha e cada célula leva o nome da coluna; acima disso,
três colunas que cabem no cartão; letra de pelo menos 14 px; projeção em três tamanhos.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json,sys,threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards

CASOS=[('m2/licao-m2-f09',2),('m6/licao-m6-f08',2),('m8/licao-m8-f10',4),('m9/licao-m9-f05',7)]

def mount(page,card):
    page.evaluate('''card=>{
     document.querySelectorAll('.casca').forEach(e=>e.remove());
     EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Fim.</p>'}],chave:'qa-tabela-encomendas',variar:false});
     document.querySelector('.jogo-alvo').id='baralho';
     document.querySelectorAll('#baralho details').forEach(d=>d.open=true);
    }''',card)

def check(scope,largura,linhas):
    t=scope.locator('#baralho table.quadro.empilha')
    assert t.count()==1
    assert t.locator('tr').count()==linhas+1
    d=t.evaluate('''t=>{const rows=[...t.querySelectorAll('tr')].slice(1),cs=getComputedStyle;
      return {vis:rows.every(r=>[...r.cells].every(c=>c.getBoundingClientRect().width>0&&c.getBoundingClientRect().height>0)),
       bloco:rows.every(r=>cs(r).display==='block'),
       rotulos:rows.every(r=>[...r.cells].slice(1).every(c=>cs(c,'::before').content.length>2)),
       letra:Math.min(...rows.flatMap(r=>[...r.cells].map(c=>parseFloat(cs(c).fontSize)))),
       cabe:t.scrollWidth<=t.parentElement.clientWidth+2,
       pag:document.documentElement.scrollWidth<=innerWidth+2}}''')
    assert d['vis'] and d['cabe'] and d['pag'],d
    # 27/10/2026: as células desta tabela de apoio medem 14,7 px no telemóvel (a leitura mede 16,8) e crescem na
    # projeção (16,6 a 25,8 px); fica registado no relatório, sem mudar o estilo comum das tabelas «quadro».
    assert d['letra']>=14,d
    if largura<=560:assert d['bloco'] and d['rotulos'],d
    else:assert not d['bloco'],d

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True)
            for pasta,i in CASOS:
                card=lesson_cards(ROOT/pasta/'index.html')[i];linhas=json.dumps(card).count('<tr>')-1
                for largura in (320,390,560,600,900,1440):
                    for esquema in ('light','dark'):
                        ctx=b.new_context(viewport={'width':largura,'height':900},color_scheme=esquema,reduced_motion='reduce')
                        p=ctx.new_page();erros=[];p.on('pageerror',lambda e:erros.append(str(e)))
                        p.route('**/fonts.g*/**',lambda r:r.abort())
                        p.goto(host+'/'+pasta+'/',wait_until='networkidle');mount(p,card)
                        check(p,p.evaluate('innerWidth'),linhas)
                        assert not erros,(pasta,largura,esquema,erros);ctx.close()
                print('PASS',pasta,'cartão',i+1,linhas,'linhas, 320 a 1440 px, claro e escuro',flush=True)
                ctx=b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce');p=ctx.new_page()
                p.route('**/fonts.g*/**',lambda r:r.abort())
                def local(route):
                    route.fulfill(response=route.fetch(url=host+route.request.url.split(host+'/pt',1)[1]))
                p.route(host+'/pt/**',local)
                p.goto(host+'/pt/projetar/?pagina=%2Fpt%2F'+pasta.replace('/','%2F')+'%2F',wait_until='networkidle')
                f=p.frame_locator('#lesson-frame');f.locator('#baralho .cartao').wait_for()
                filho=next(x for x in p.frames if '/'+pasta+'/' in x.url);mount(filho,card)
                for tam in ('small','medium','large'):
                    p.locator(f'[data-projection-size="{tam}"]').click();check(f,filho.evaluate('innerWidth'),linhas)
                print('PASS',pasta,'cartão',i+1,'projeção em três tamanhos',flush=True);ctx.close()
            b.close()
    finally:server.shutdown()
if __name__=='__main__':main()
