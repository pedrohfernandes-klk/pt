import sys,json,threading
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tests'))
from browser_m1_and_inventory import QuietHandler,new_page
from browser_m2_complete import respond
from playwright.sync_api import sync_playwright
out=root.parents[1]/'outputs/m6-forma-soneto';out.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(root.parent)));threading.Thread(target=server.serve_forever,daemon=True).start()
cards=json.JSONDecoder().raw_decode((root/'m6/licao-m6-f01/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0];results=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for w in [320,1440]:
  ctx,page=new_page(b,w);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/pt/m6/licao-m6-f01/',wait_until='networkidle')
  for k in range(150):
   if page.locator('#baralho .cartao.fim').count():break
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');respond(page)
  else:raise AssertionError('stalled')
  page.reload(wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for()
  page.evaluate("cards=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:cards,chave:'qa-m6-forma',variar:false});document.querySelector('.jogo-alvo').id='baralho'}",[cards[i] for i in [17,20,21,23]])
  page.screenshot(path=str(out/f'esquema-{w}.png'))
  for k in range(40):
   if page.locator('#baralho .cartao.fim').count():break
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');respond(page)
  else:raise AssertionError('changed cards stalled')
  assert not errors;results.append({'width':w,'normal_attempt_complete':True,'progress_after_reload':True,'changed_cards_complete':True,'errors':errors});ctx.close()
 b.close()
server.shutdown();(out/'qa.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('PASS M6 normal attempt, progress, changed cards at 320/1440')
