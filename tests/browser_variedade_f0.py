"""02/11/2026: ajuda dos vinte aquecimentos e importação real entre lotes."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
import mimetypes
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


def local(route):
    u=urlsplit(route.request.url)
    if u.hostname not in ('f0.test','pedrohfernandes-klk.github.io') or not u.path.startswith('/pt/'):
        route.abort();return
    p=(ROOT/unquote(u.path[4:])).resolve()
    if p.is_dir():p=p/'index.html'
    if p.is_relative_to(ROOT) and p.is_file():route.fulfill(path=str(p),content_type=mimetypes.guess_type(p)[0] or 'application/octet-stream')
    else:route.fulfill(status=404,body='Not found')


def main():
    cases=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        for source in sorted((ROOT/'docs/pedagogia/aquecimentos').glob('*.json')):
            for width,scheme,projection in [(320,'dark',False),(390,'light',False),(1366,'light',True)]:
                ctx=browser.new_context(viewport={'width':width,'height':900},color_scheme=scheme,reduced_motion='reduce')
                page=ctx.new_page();page.route('**/*',local);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(f'https://f0.test/pt/tarefas/{source.stem}/aquecimento/'+('?projetar=1' if projection else ''))
                help=page.get_by_role('button',name='Como se faz',exact=True);help.wait_for()
                before=page.evaluate('JSON.stringify(localStorage)')
                help.focus();page.keyboard.press('Enter')
                modal=page.get_by_role('dialog',name='Como se faz');modal.wait_for()
                assert modal.locator('video source').count()==2
                assert modal.locator('video source').first.get_attribute('src').endswith('/andar-na-licao.mp4')
                assert page.locator('.casca-topo').bounding_box()['width']<=width+1
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                page.keyboard.press('Escape');assert modal.count()==0
                assert page.evaluate('JSON.stringify(localStorage)')==before
                assert not errors,errors
                cases+=1;ctx.close()
        print('PASS',cases,'casos de ajuda: teclado, destino, três larguras e progresso intacto',flush=True)
        # As duas direções são necessárias: a ordem das chaves do ficheiro não pode mudar a compatibilidade.
        cases_import=[
            ('local-novo',['l1'],None,{'4':7},{'3':99},{'4':7}),
            ('recebido-novo',None,['l1'],{'3':99},{'4':7},{'4':7}),
            ('iguais',['l1'],['l1'],{'4':2},{'4':7},{'4':7}),
            ('incomparaveis',['l1'],['l2'],{'3':2},{'4':7},None),
            ('primeira-importacao',None,None,None,{'3':7},{'3':7}),
            ('marca-sem-registo',['l1'],None,None,{'3':7},None),
        ]
        for name,local_lots,incoming_lots,local_exp,incoming_exp,expected in cases_import:
            ctx=browser.new_context(viewport={'width':390,'height':900});page=ctx.new_page();page.route('**/*',local)
            page.goto('https://f0.test/pt/')
            state={'versao':'v','lida':True,'melhor':8,'tentativas':3,'exposicoes':local_exp,'ult':','.join(sorted(local_exp or {}))}
            if local_exp is not None:page.evaluate('(s)=>localStorage.setItem("licao-m4-f01",JSON.stringify(s))',state)
            if local_lots is not None:page.evaluate('(s)=>localStorage.setItem("licao-m4-f01-acrescentos",JSON.stringify(s))',local_lots)
            records={}
            if incoming_lots is not None:records['licao-m4-f01-acrescentos']=json.dumps(incoming_lots)
            records['licao-m4-f01']=json.dumps({'versao':'v','lida':True,'melhor':9,'tentativas':5,'exposicoes':incoming_exp,'ult':','.join(sorted(incoming_exp))})
            payload=json.dumps({'formato':'epi-progresso','versao':1,'registos':records}).encode()
            page.locator('[data-pf-repor]').set_input_files({'name':'progresso.json','mimeType':'application/json','buffer':payload})
            page.wait_for_function('JSON.parse(localStorage.getItem("licao-m4-f01")||"{}").tentativas===5')
            got=page.evaluate('JSON.parse(localStorage.getItem("licao-m4-f01"))')
            assert got.get('exposicoes')==expected,(name,got)
            assert got.get('ult')==(','.join(sorted(expected)) if expected is not None else None),(name,got)
            assert got['melhor']==9 and got['lida'] is True and got['versao']=='v',(name,got)
            print('PASS importação',name,flush=True);ctx.close()
        # Um aparelho novo pode exportar só a marca do lote, sem uma tentativa nessa lição.
        ctx=browser.new_context();page=ctx.new_page();page.route('**/*',local)
        page.goto('https://f0.test/pt/')
        page.evaluate('localStorage.setItem("licao-m4-f01",JSON.stringify({versao:"v",lida:true,melhor:8,tentativas:3,exposicoes:{3:9},ult:"3"}))')
        payload=json.dumps({'formato':'epi-progresso','versao':1,'registos':{'licao-m4-f01-acrescentos':json.dumps(['l1'])}}).encode()
        page.locator('[data-pf-repor]').set_input_files({'name':'so-marca.json','mimeType':'application/json','buffer':payload})
        page.wait_for_function('localStorage.getItem("licao-m4-f01-acrescentos")!==null')
        got=page.evaluate('JSON.parse(localStorage.getItem("licao-m4-f01"))')
        assert got=={'versao':'v','lida':True,'melhor':8,'tentativas':3},got
        print('PASS importação marca recebida sem tentativa, resultados locais preservados',flush=True)
        ctx.close()
        browser.close()


if __name__=='__main__':main()
