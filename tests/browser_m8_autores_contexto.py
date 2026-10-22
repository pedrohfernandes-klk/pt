"""Three-voice orientation, optional authors, full banks and projection."""
from functools import partial
from http.server import ThreadingHTTPServer
import json,threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page
from browser_m2_complete import respond

cards=json.JSONDecoder().raw_decode((ROOT/'m8/licao-m8-f01/index.html').read_text('utf8').split('CARTOES=',1)[1])[0]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/pt'
def finish(page):
 for _ in range(170):
  if page.locator('#baralho .cartao.fim').count():return
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
  respond(page)
 raise AssertionError('Author lesson stalled')
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(host+'/m8/licao-m8-f01/',wait_until='networkidle')
   assert 'Ângelo' not in page.locator('#baralho').inner_text()
   page.locator('summary').filter(has_text='Adília Lopes').click()
   assert 'Poema de Adília Lopes, lido por Fernando Alvim' in page.locator('#baralho').inner_text()
   assert page.locator('iframe').count()==0
   page.locator('.casca [data-seguinte]').click()
   timeline=page.locator('#baralho .vida')
   assert 'Ângelo' not in timeline.inner_text()
   assert timeline.locator('li').count()==6
   timeline.locator('li').first.press('Enter')
   assert timeline.locator('li').first.get_attribute('aria-expanded')=='true'
   finish(page);page.reload(wait_until='networkidle')
   assert page.locator('#baralho .cartao.fim').is_visible()
   page.evaluate("""cards=>{
    document.querySelectorAll('.casca').forEach(n=>n.remove());
    EPIJogo.montar({itens:cards,chave:'qa-m8-autores-banco',variar:false});
    document.querySelector('.jogo-alvo').id='baralho';
   }""",cards)
   saw_optional=False
   for _ in range(170):
    if page.locator('#baralho .cartao.fim').count():break
    if page.locator('#baralho h3').filter(has_text='Jorge de Sena · olhar e responder').count():
     page.locator('#baralho summary').filter(has_text='Outra geração').press('Enter')
     assert page.locator('#baralho a[href="../../atlas/#figura-angelo-de-lima"]').is_visible()
     assert 'Não integra as três vozes centrais' in page.locator('#baralho').inner_text()
     saw_optional=True
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
    respond(page)
   else:raise AssertionError('Full author bank stalled')
   assert saw_optional
   assert not errors,errors
   page.goto(host+'/m8/painel-m8-f01/',wait_until='networkidle')
   assert page.locator('select[data-r-k] option[value="8"]').inner_text()==cards[8]['p']
   assert 'Ângelo' not in page.locator('select[data-r-k]').inner_text()
   ctx.close();print(f'PASS M8 authors normal/full bank, keyboard, reload and optional context {width}',flush=True)
  ctx,page=new_page(browser,1440)
  page.goto(host+'/projetar/?pagina=/pt/m8/licao-m8-f01/',wait_until='networkidle')
  frame=page.frame_locator('#lesson-frame')
  frame.locator('.casca [data-seguinte]').click()
  page.locator('[data-projection-size="large"]').click()
  assert frame.locator('html').get_attribute('data-projection-size')=='large'
  assert 'Ângelo' not in frame.locator('.vida').inner_text()
  assert not frame.locator('html').evaluate('(el)=>el.scrollWidth>innerWidth+3')
  ctx.close();browser.close();print('PASS M8 authors large projection',flush=True)
finally:server.shutdown()
