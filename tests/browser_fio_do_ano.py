"""02/11/2026: fio discreto, teclado, temas e continuação na mesma posição."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from urllib.parse import urlsplit,parse_qs
import threading,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from auditoria_20261028 import undo_fio_do_ano
FILES=('1/index.html','m1/index.html','m2/index.html','m3/index.html')

class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        url=urlsplit(self.path);rel=url.path.lstrip('/')
        if rel.endswith('/'):rel+='index.html'
        if rel in FILES and parse_qs(url.query).get('sem-fio')==['1']:
            body=undo_fio_do_ano(rel,(ROOT/rel).read_text('utf-8')).encode('utf-8')
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
        super().do_GET()

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
    count=0
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width,projection in ((320,False),(390,False),(1366,False),(1366,True)):
                for scheme in ('light','dark'):
                    ctx=browser.new_context(viewport={'width':width,'height':900},color_scheme=scheme,reduced_motion='reduce')
                    page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                    page.route('**/*',lambda r:r.continue_() if urlsplit(r.request.url).hostname=='127.0.0.1' else r.abort())
                    query='?projetar=1' if projection else ''
                    for rel in FILES:
                        route=rel.removesuffix('index.html');original=None
                        if rel.startswith('m'):
                            page.goto(host+'/'+route+'?sem-fio=1'+('&projetar=1' if projection else ''),wait_until='networkidle')
                            original=page.locator('[data-module-next]').bounding_box()
                        page.goto(host+'/'+route+query,wait_until='networkidle')
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(rel,width,scheme)
                        if original:
                            current=page.locator('[data-module-next]').bounding_box()
                            for key in ('x','y','width','height'):assert abs(original[key]-current[key])<.5,(rel,key,original,current)
                            if width==320:assert current['y']<600,(rel,current)
                            assert page.locator('.fio-ano-modulo').count()==1
                            assert page.locator('.fio-ano-modulo').evaluate('e=>e.nextElementSibling.classList.contains("unit-index")')
                        else:
                            summary=page.locator('.fio-ano summary');summary.focus()
                            assert summary.evaluate('e=>e===document.activeElement')
                            assert summary.bounding_box()['height']>=44
                            assert summary.evaluate('e=>parseFloat(getComputedStyle(e).outlineWidth)')>=2
                            summary.press('Enter');assert page.locator('.fio-ano details').get_attribute('open') is not None
                            for term in page.locator('.fio-ano dt').all():assert term.is_visible()
                            assert page.locator('.fio-ano dt').count()==4
                            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                            if width==390 and scheme=='light' and not projection:page.screenshot(path=str(ROOT.parent/'fio-do-ano-piloto-390.png'),full_page=True)
                            page.emulate_media(media='print');assert page.locator('.fio-ano-sentido').is_visible();page.emulate_media(media='screen')
                            summary.press('Space');assert page.locator('.fio-ano details').get_attribute('open') is None
                        assert not errors,(rel,errors)
                        count+=1
                    ctx.close();print('PASS',width,scheme,'projeção',projection,flush=True)
            browser.close()
    finally:server.shutdown()
    print(f'PASS {count} páginas/cenários; teclado, temas, projeção e botão na posição original.',flush=True)
if __name__=='__main__':main()
