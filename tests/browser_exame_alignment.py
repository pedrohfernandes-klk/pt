from functools import partial
from http.server import ThreadingHTTPServer
import threading,json,re
# 01/11/2026: compara o texto visível, mantendo a conferência integral das frases.
def visivel(s):return re.sub(r"_([^_]+)_",r"\1",s)
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  ctx,page=new_page(browser,390);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for s in json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))['sessions']:
   # 01/11/2026: todas as cinco fases, incluindo títulos e opções do aquecimento.
   for phase in ('aquecer','ler','escrever','corrigir','fechar'):
    page.goto(host+'/exame/#'+s['id']+'/'+phase,wait_until='networkidle')
    page.locator('h1').filter(has_text=s['title']).wait_for()
    if phase=='ler' and s['id']=='s01':assert 'Nom hei [eu] i barqueiro nem remador' in page.locator('#app').inner_text()
    if phase=='escrever':assert visivel(s['writing']['prompt']) in page.locator('#app').inner_text()
    if phase=='corrigir':
     assert page.locator('#correction').is_hidden()
     page.locator('[data-action="reveal"]').click()
     assert page.locator('#correction').is_visible()
     assert visivel(s['correction']['model'])[:50] in page.locator('#correction').inner_text()
    assert not re.search(r'(?<![\w/])_[^_\n]+_(?!\w)',page.locator('#app').inner_text()),(s['id'],phase)
   print('PASS reading, writing and manually revealed correction',s['id'],flush=True)
  assert not errors,errors
  ctx.close();browser.close()
finally:server.shutdown()
