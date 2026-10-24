"""Readable paired panels: live lesson, review, projection and all existing examples."""
from functools import partial
from http.server import ThreadingHTTPServer
import sys,threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards

server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/pt'

def readable(scope):
 panels=scope.locator('.paralelo>.lado')
 boxes=panels.evaluate_all('(els)=>els.map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,b:r.bottom}})')
 assert len(boxes)==2,boxes
 assert min(b['w'] for b in boxes)>=215,boxes
 assert .85<=boxes[0]['w']/boxes[1]['w']<=1.18,boxes
 assert boxes[1]['x']>=boxes[0]['x']+boxes[0]['w']-2 or boxes[1]['y']>=boxes[0]['b']-2,boxes
 assert not scope.locator('html').evaluate('(e)=>e.scrollWidth>innerWidth+3')

try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,390,900,1440):
   ctx,page=new_page(browser,width)
   page.goto(host+'/m4/licao-m4-f28/',wait_until='networkidle')
   page.locator('.casca [data-seguinte]').click()
   readable(page)
   page.locator('.casca [data-seguinte]').click()
   page.get_by_role('button',name='Ver os cartões já feitos',exact=True).click()
   page.get_by_role('button',name='Cartão 2',exact=True).click()
   readable(page)
   assert 'A REVER' in page.locator('[data-c-modo]').inner_text().upper()
   ctx.close();print(f'PASS paired panel live/review legibility {width}',flush=True)
  examples=[]
  for path in ROOT.glob('m[1-9]/licao-*/index.html'):
   for card in lesson_cards(path):
    if 'class="paralelo"' in card.get('html',''):examples.append(card)
  # 24/10/2026, aulas claras do M4: as lições do M4 refeitas têm 3 cartões «Em paralelo» (eram 11); o mínimo passa de 71 para 62
  # 24/10/2026, aulas claras do M1: as lições do M1 refeitas têm 3 (eram 7); o mínimo passa de 62 para 59
  assert len(examples)>=59
  for width in (320,900):
   ctx,page=new_page(browser,width)
   page.goto(host+'/m4/licao-m4-f28/',wait_until='networkidle')
   for i,card in enumerate(examples):
    page.evaluate('''({card,i})=>{
     document.querySelectorAll('.casca').forEach(e=>e.remove());
     EPIJogo.montar({itens:[card],chave:'qa-paired-layout-'+i,variar:false});
    }''',dict(card=card,i=i))
    readable(page)
   ctx.close();print(f'PASS all {len(examples)} existing comparisons readable {width}',flush=True)
  ctx,page=new_page(browser,1440)
  page.goto(host+'/projetar/?pagina=/pt/m4/licao-m4-f28/',wait_until='networkidle')
  frame=page.frame_locator('#lesson-frame')
  page.locator('[data-projection-size="large"]').click()
  frame.locator('.casca [data-seguinte]').click()
  readable(frame)
  ctx.close();browser.close();print('PASS paired panels large projection',flush=True)
finally:server.shutdown()
