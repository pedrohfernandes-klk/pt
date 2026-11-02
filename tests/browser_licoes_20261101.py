"""01/11/2026: percurso integral das novas lições, móvel e projeção, sem dados pessoais."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import mimetypes
import sys
from playwright.sync_api import sync_playwright
from browser_m2_complete import respond

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from licoes_20261101 import LESSONS


def local(route):
    url=urlsplit(route.request.url)
    if url.hostname != 'licoes.test':
        route.abort();return
    path=(ROOT/unquote(url.path.lstrip('/'))).resolve()
    if not path.is_relative_to(ROOT):
        route.fulfill(status=403,body='Forbidden');return
    if path.is_dir():path=path/'index.html'
    if path.is_file():route.fulfill(path=str(path),content_type=mimetypes.guess_type(path)[0] or 'application/octet-stream')
    else:route.fulfill(status=404,body='Not found')


def main():
    cases=activities=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        # 01/11/2026: inclui 320 px em claro e escuro e projeção a 1366 × 768.
        for width,projection,scheme in ((320,False,'light'),(320,False,'dark'),(390,False,'light'),(1366,True,'dark')):
            for item in LESSONS:
                context=browser.new_context(viewport={'width':width,'height':768 if projection else 640 if width==320 else 900},color_scheme=scheme,reduced_motion='reduce')
                page=context.new_page();page.route('**/*',local)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                module=item['id'].split('-')[0]
                url=f'https://licoes.test/{module}/licao-{item["id"]}/'+('?projetar=1' if projection else '')
                page.goto(url,wait_until='networkidle')
                page.locator('#baralho .cartao').wait_for()
                # 01/11/2026: as imagens do Abre carregam inteiras, também na projeção.
                for picture in page.locator('#baralho .documento img').all():
                    assert picture.evaluate('(im)=>im.complete && im.naturalWidth>0'),(item['id'],'image missing')
                    assert picture.evaluate('(im)=>getComputedStyle(im).objectFit')=='contain'
                    bounds=picture.bounding_box()
                    assert bounds and bounds['width']<=width,(item['id'],'image overflow')
                if item['id']=='m9-f14' and width==390:
                    page.screenshot(path=str(ROOT.parent/'licoes-a-abre-piranesi.png'),full_page=True)
                seen=set();feedback=0
                for _ in range(100):
                    if page.locator('#baralho .cartao.fim').count():break
                    assert page.locator('#baralho .cartao').count()==1,(item['id'],'one card')
                    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'),(item['id'],width,'overflow')
                    # 01/11/2026: nenhum par nem texto pode ultrapassar a margem do cartão a 320 px.
                    if width==320:
                        # Medir a disposição final, depois da entrada animada dos pares.
                        page.locator('#baralho .cartao').evaluate('async e=>{await Promise.all(e.getAnimations({subtree:true}).filter(a=>a.effect.getTiming().iterations!==Infinity).map(a=>a.finished.catch(()=>{})))}')
                        outside=page.locator('#baralho .cartao').evaluate("""card=>{
                            const edge=card.getBoundingClientRect().right;
                            return [...card.querySelectorAll('.pares .op,.pares .tx')].filter(e=>e.getBoundingClientRect().right>edge+1 || (e.matches('.tx') && e.scrollWidth>e.clientWidth+1)).map(e=>({text:e.textContent,tag:e.className,right:e.getBoundingClientRect().right,edge,scroll:e.scrollWidth,width:e.clientWidth}));
                        }""")
                        assert not outside,(item['id'],outside)
                    text=page.locator('#baralho .cartao').inner_text()
                    seen.add(page.locator('[data-c-num]').inner_text())
                    result=respond(page)
                    if result=='feedback':feedback+=1
                else:raise AssertionError((item['id'],'did not finish'))
                assert not errors,(item['id'],errors)
                assert len(seen)==len(item['cards']),(item['id'],len(seen),len(item['cards']))
                assert feedback==14,(item['id'],feedback)
                key='licao-'+item['id']+'-a1'
                # 01/11/2026: projeção usa o motor sem gravar conclusão pessoal.
                if projection:
                    assert page.evaluate('(key)=>localStorage.getItem(key)',key) is None
                    assert page.evaluate('localStorage.getItem("epi-ultima")') is None
                else:
                    assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).lida',key)
                page.reload(wait_until='networkidle')
                if projection:
                    assert page.evaluate('(key)=>localStorage.getItem(key)',key) is None
                else:
                    assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).lida',key)
                cases+=1;activities+=feedback
                print(f'PASS {item["id"]} {width} {scheme} projection={projection}: {feedback} atividades, progresso conservado',flush=True)
                context.close()
        browser.close()
    print(f'PASS total: {cases} percursos, {activities} atividades',flush=True)


if __name__=='__main__':main()
