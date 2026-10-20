from functools import partial
from http.server import ThreadingHTTPServer
import threading,json
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}'
data=json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);requests=[];errors=[]
   page.on('request',lambda r: requests.append(r.url));page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(host+'/exame/#s01/aquecer',wait_until='networkidle')
   page.locator('[data-action="another"]').wait_for()
   app=next(u for u in requests if '/exame/app.js?' in u)
   req=next(u for u in requests if '/sessoes.json?' in u)
   assert parse_qs(urlparse(app).query)==parse_qs(urlparse(req).query)
   ids=[q['id'] for q in data['sessions'][0]['warmup']]
   state=page.evaluate('JSON.parse(localStorage.getItem("pt-exame-sessao-s01"))')
   assert len(state['warm'])==2 and len(set(state['warm']))==2
   unseen=state['remaining'][:]
   assert unseen
   page.locator('[data-action="another"]').click()
   state=page.evaluate('JSON.parse(localStorage.getItem("pt-exame-sessao-s01"))')
   assert state['warm'][:len(unseen)]==unseen
   assert len(set(state['warm']))==2
   saved=state['warm']
   page.reload(wait_until='networkidle');page.locator('[data-action="another"]').wait_for()
   assert page.evaluate('JSON.parse(localStorage.getItem("pt-exame-sessao-s01")).warm')==saved
   for _ in range(5):
    page.locator('[data-action="another"]').click()
    state=page.evaluate('JSON.parse(localStorage.getItem("pt-exame-sessao-s01"))')
    assert len(set(state['warm']))==2 and set(state['warm'])<=set(ids)
   assert not errors,errors
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   print('PASS versioned data request; unseen question first; unique pairs; reload; layout',width,flush=True)
   ctx.close()
  browser.close()
finally:server.shutdown()
