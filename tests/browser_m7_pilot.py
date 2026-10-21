from functools import partial
from http.server import ThreadingHTTPServer
import threading,json
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
from browser_m2_complete import respond
OUT=ROOT.parents[1]/'outputs/m7-piloto';OUT.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)));threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1280):
   for n in ('02','13'):
    ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'http://127.0.0.1:{server.server_port}/pt/m7/licao-m7-f{n}/',wait_until='networkidle')
    cards=json.JSONDecoder().raw_decode((ROOT/f'm7/licao-m7-f{n}/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
    # Full bank, in lesson order: exercise mechanics and reading layout, with no sampling.
    page.evaluate('''items=>{document.querySelectorAll('.casca').forEach(n=>n.remove());window.api=EPIJogo.montar({itens:items,chave:'qa-m7-pilot',variar:false});document.querySelector('.jogo-alvo').id='baralho';}''',cards)
    opened=False
    for step in range(240):
     if page.locator('#baralho .cartao.fim').count():break
     if page.locator('#baralho details summary').count():
      summary=page.locator('#baralho details summary').first;summary.focus();summary.press('Enter');assert summary.evaluate('e=>e.parentElement.open');opened=True
      page.screenshot(path=str(OUT/f'comparacao-{n}-{width}.png'))
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(n,width,step)
     respond(page)
    else:raise AssertionError(('unfinished',n,width))
    if n=='13':assert opened
    assert not errors,errors
    results.append({'lesson':n,'width':width,'full_bank':len(cards),'javascript_errors':errors,'overflow':False});print('PASS full bank',n,width,flush=True)
    ctx.close()
  browser.close()
finally:server.shutdown()
(OUT/'qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
