from pathlib import Path
import json,threading
from functools import partial
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page
from browser_m2_complete import respond
OUT=ROOT.parents[1]/'outputs/m8-ironia-contexto';OUT.mkdir(parents=True,exist_ok=True)
cards=json.JSONDecoder().raw_decode((ROOT/'m8/licao-m8-f05/index.html').read_text('utf-8').split('CARTOES=',1)[1])[0]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();results=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in [320,1440]:
   ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/pt/m8/licao-m8-f05/',wait_until='networkidle')
   def finish():
    for _ in range(160):
     if page.locator('#baralho .cartao.fim').count():return
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');respond(page)
    raise AssertionError('Lesson stalled')
   finish();page.reload(wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for()
   def mount(items):page.evaluate("items=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:items,chave:'qa-ironia',variar:false,mostrarAnterior:false});document.querySelector('.jogo-alvo').id='baralho'}",items)
   mount(cards);finish();mount([cards[6]]);assert 'não são versos do poema' in page.locator('#baralho').inner_text();assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');page.screenshot(path=str(OUT/f'modelo-{width}.png'),full_page=True)
   for wrong in [1,2,3]:
    card={**cards[18],'o':[cards[18]['o'][0],cards[18]['o'][wrong]],'c':0}
    mount([card]);button=page.locator('#baralho .ops [data-j="1"]');button.focus();button.press('Enter');assert 'exclamação, sozinha' in page.locator('.casca-folha').inner_text()
   assert not errors;results.append({'width':width,'normal_attempt':True,'full_bank':24,'progress_reload':True,'three_distractors_keyboard':True,'overflow':False,'errors':errors});ctx.close()
  browser.close()
finally:server.shutdown()
(OUT/'qa.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('PASS ironia 320/1440')
