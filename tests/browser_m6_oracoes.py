from pathlib import Path
import json,threading
from functools import partial
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page
from browser_m2_complete import respond
OUT=ROOT.parents[1]/'outputs/m6-oracoes-contexto';OUT.mkdir(parents=True,exist_ok=True)
def bank(key):return json.JSONDecoder().raw_decode((ROOT/'m6'/('licao-'+key)/'index.html').read_text('utf-8').split('CARTOES=',1)[1])[0]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}';results=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for key in ['m6-f04','m6-f09']:
   for width in [320,1440]:
    ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(host+'/pt/m6/licao-'+key+'/',wait_until='networkidle')
    def mount(items):page.evaluate("items=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:items,chave:'qa-oracoes-contexto',variar:false,mostrarAnterior:false});document.querySelector('.jogo-alvo').id='baralho'}",items)
    def finish():
     for action in range(170):
      if page.locator('#baralho .cartao.fim').count():return
      assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');respond(page)
     raise AssertionError('Lesson stalled')
    finish();page.reload(wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for();cards=bank(key);mount(cards);finish()
    if key=='m6-f04':
     mount([cards[4]]);page.screenshot(path=str(OUT/f'modelo-{width}.png'));summary=page.locator('#baralho summary');summary.focus();summary.press('Enter');assert summary.evaluate('e=>e.parentElement.open');assert 'E eu sigo' in page.locator('#baralho').inner_text();summary.press('Enter')
     mount([cards[19]]);page.locator('#baralho .ops [data-j="0"]').focus();page.locator('#baralho .ops [data-j="0"]').press('Enter');assert 'não estabelece' in page.locator('.casca-folha').inner_text()
     mount([cards[12]]);page.locator('#baralho select[data-k="0"]').select_option('0');page.locator('#baralho select[data-k="1"]').select_option(page.locator('#baralho select[data-k="1"] option').evaluate_all("opts=>opts.find(o=>o.value!==''&&o.value!=='0').value"));assert 'antecedente' in page.locator('.casca-folha').inner_text()
    assert not errors;results.append({'lesson':key,'width':width,'normal_attempt':True,'full_bank':len(cards),'progress_after_reload':True,'errors':errors});ctx.close()
  browser.close()
finally:server.shutdown()
(OUT/'qa.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('PASS full lessons, progress, context hint and correction feedback at 320/1440')
