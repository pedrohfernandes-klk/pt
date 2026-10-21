"""Six real support steps, reference feedback, resumption and projection."""
from functools import partial
import re
from http.server import ThreadingHTTPServer
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler, new_page

server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/pt'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);errors=[]
   page.on('pageerror',lambda err:errors.append(str(err)))
   page.goto(host+'/m8/licao-m8-f06/',wait_until='networkidle')
   page.get_by_role('button',name='Menu',exact=True).click()
   link=page.get_by_role('link',name=re.compile('Praticar anáfora e catáfora · opcional'))
   assert link.is_visible()
   assert link.get_attribute('href').endswith('/m8/anafora-catafora/')
   page.goto(host+'/m8/anafora-catafora/',wait_until='networkidle')
   page.locator('#seguir').click()
   page.get_by_text('Ajuda: como confirmar a direção?',exact=True).press('Enter')
   assert page.locator('details').get_attribute('open') is not None
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
   page.locator('#seguir').click()
   for row,answer in enumerate((0,1,0,1)):
    page.locator(f'#palco button[data-v="{row}"][data-j="{answer}"]').click()
   page.locator('#verificar').click()
   assert 'ambos aparecem antes' in page.locator('.casca-folha').inner_text()
   page.locator('#seguir').click();page.reload(wait_until='networkidle')
   page.locator('#palco .op[data-j="2"]').press('Enter')
   assert 'para o que ainda vem' in page.locator('.casca-folha').inner_text()
   page.locator('#seguir').click()
   page.locator('#palco button[data-v="0"][data-j="0"]').click()
   page.locator('#palco button[data-v="1"][data-j="1"]').click()
   page.locator('#verificar').click()
   assert '1 de 2' in page.locator('.casca-folha').inner_text()
   assert 'não concorda em género' in page.locator('.casca-folha').inner_text()
   page.locator('#seguir').click()
   for row,answer in enumerate((1,0,1,0)):
    page.locator(f'#palco button[data-v="{row}"][data-j="{answer}"]').click()
   page.locator('#verificar').click()
   assert '4 de 4' in page.locator('.casca-folha').inner_text()
   page.locator('#seguir').click()
   page.locator('#palco .op[data-j="1"]').click()
   assert 'oralmente ou no caderno' in page.locator('.casca-folha').inner_text()
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
   page.locator('#seguir').click();page.reload(wait_until='networkidle')
   assert 'o meu cartão' in page.locator('#palco').inner_text().lower()
   page.get_by_role('button',name='Menu',exact=True).click()
   assert page.get_by_role('link',name=re.compile('Voltar à lição M8-F06')).is_visible()
   assert not errors,errors
   ctx.close();print(f'PASS anaphora six steps, feedback, keyboard and reload {width}',flush=True)
  ctx,page=new_page(browser,1440)
  page.goto(host+'/projetar/?pagina=/pt/m8/anafora-catafora/',wait_until='networkidle')
  frame=page.frame_locator('#lesson-frame')
  frame.locator('#seguir').click()
  page.locator('[data-projection-size="large"]').click()
  assert frame.locator('html').get_attribute('data-projection-size')=='large'
  assert 'Não classifiques pela pontuação' in frame.locator('#palco').inner_text()
  frame.locator('#seguir').click()
  assert frame.get_by_text('Classifica apenas a expressão indicada em cada caso.',exact=True).is_visible()
  assert not frame.locator('html').evaluate('(el)=>el.scrollWidth>innerWidth+2')
  ctx.close();browser.close();print('PASS anaphora large projection',flush=True)
finally:server.shutdown()
