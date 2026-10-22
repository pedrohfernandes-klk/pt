"""Real renderer: aligned F12 cards, recycled challenge and teacher index."""
from functools import partial
from http.server import ThreadingHTTPServer
import json,threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page
from browser_inferencia_m8_m4 import open_card,close_card

def read(path,marker):
 return json.JSONDecoder().raw_decode((ROOT/path).read_text('utf-8').split(marker,1)[1])[0]

cards=read('m8/licao-m8-f12/index.html','CARTOES=')
pool=read('m8/index.html','var U=')[1]['pool']
reference=next(c for c in pool if 'exemplo inventado' in c.get('p',''))
inference=next(c for c in pool if c.get('o',[''])[0]=='Inferência sustentada')
comparison=next(c for c in pool if c['p']==cards[6]['p'])
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/pt'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);errors=[]
   page.on('pageerror',lambda err:errors.append(str(err)))
   page.goto(host+'/m8/licao-m8-f12/',wait_until='networkidle')
   for lesson,url in [('03','https://ensina.rtp.pt/artigo/jorge-sena-poesia/'),('04','https://ensina.rtp.pt/artigo/as-palavras-de-eugenio-de-andrade/'),('05','https://searanova.publ.pt/2023/08/07/poesia-prece-no-mediterraneo/')]:
    reading=read(f'm8/licao-m8-f{lesson}/index.html','CARTOES=')[3]
    modal=open_card(page,reading,f'qa-source-{lesson}-{width}')
    assert modal.locator(f'a[href="{url}"]').first.is_visible()
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
    close_card(page)
   for name,item in [('habit',cards[8]),('aspect',cards[17]),('reference',reference),('inference',inference),('comparison',comparison)]:
    modal=open_card(page,item,f'qa-f12-{name}-{width}')
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
    if item['t']=='escolha':
     modal.locator(f'button.op[data-j="{item["c"]}"]').press('Enter')
    else:
     for i in range(len(item['pares'])):
      modal.locator(f'.pares .esq [data-e="{i}"]').click()
      modal.locator(f'.pares .dir [data-d="{i}"]').click()
    feedback=modal.locator('.casca-folha')
    assert feedback.is_visible()
    if name=='habit':assert 'não é necessária uma contagem exata' in feedback.inner_text()
    if name=='aspect':assert 'não diz que a pintora parou' in feedback.inner_text()
    if name=='reference':assert 'informação anterior' in feedback.inner_text()
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
    modal.locator('[data-seguinte]').click()
    assert modal.locator('.cartao.fim').is_visible()
    close_card(page)
   page.goto(host+'/m8/painel-m8-f12/',wait_until='networkidle')
   dropdown=page.locator('select[data-r-k]')
   assert dropdown.locator('option[value="10"]').count()==0
   dropdown.select_option('8');assert dropdown.input_value()=='8'
   assert dropdown.locator('option[value="8"]').inner_text()==cards[8]['p']
   assert dropdown.locator('option[value="19"]').inner_text()==cards[19]['p']
   assert not errors,errors
   ctx.close();print(f'PASS F12 focused cards, unit challenge and teacher index {width}',flush=True)
  ctx,page=new_page(browser,1440)
  page.goto(host+'/projetar/?pagina=/pt/m8/licao-m8-f12/',wait_until='networkidle')
  frame=page.frame_locator('#lesson-frame')
  frame.locator('.casca [data-seguinte]').click()
  page.locator('[data-projection-size="large"]').click()
  assert frame.locator('html').get_attribute('data-projection-size')=='large'
  assert 'Li o conto. Ele surpreendeu-me' in frame.locator('#baralho').inner_text()
  assert not frame.locator('html').evaluate('(el)=>el.scrollWidth>innerWidth+3')
  ctx.close();browser.close();print('PASS F12 essential in large projection',flush=True)
finally:server.shutdown()
