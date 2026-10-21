from pathlib import Path
import sys,json,threading,argparse
from functools import partial
from http.server import ThreadingHTTPServer
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tests'))
from browser_m1_and_inventory import QuietHandler,new_page
from browser_m2_complete import respond
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
out=root.parents[1]/'outputs/pt-transversal-clareza';out.mkdir(exist_ok=True,parents=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(root.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
results=[]
def bank(key):return json.JSONDecoder().raw_decode((root/key[:2]/('licao-'+key)/'index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for key,index in [('m7-f02',15),('m7-f13',18),('m7-f14',16)]:
   for width in [320,1440]:
    ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(host+'/pt/'+key[:2]+'/licao-'+key+'/',wait_until='networkidle')
    page.evaluate("card=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:[card],chave:'qa-transversal-layout',variar:false});document.querySelector('.jogo-alvo').id='baralho'}",bank(key)[index])
    widths=page.locator('#baralho .paralelo .lado').evaluate_all('els=>els.map(e=>e.getBoundingClientRect().width)')
    page.screenshot(path=str(out/(f'{key}-{width}-'+('before' if args.baseline else 'after')+'.png')))
    if not args.baseline:assert min(widths)>=200,(key,width,widths)
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');assert not errors;results.append({'lesson':key,'width':width,'column_widths':widths,'errors':errors});ctx.close()
  if not args.baseline:
   for width in [320,1440]:
    ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));key='m3-f11';page.goto(host+'/pt/m3/licao-m3-f11/',wait_until='networkidle')
    for action in range(150):
     if page.locator('#baralho .cartao.fim').count():break
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');respond(page)
    else:raise AssertionError('Normal attempt stalled')
    page.reload(wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for()
    page.evaluate("cards=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:cards,chave:'qa-transversal-bank',variar:false});document.querySelector('.jogo-alvo').id='baralho'}",bank(key))
    for action in range(150):
     if page.locator('#baralho .cartao.fim').count():break
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');respond(page)
    else:raise AssertionError('Full bank stalled')
    assert not errors;results.append({'lesson':key,'width':width,'normal_and_full_bank':True,'progress_after_reload':True,'errors':errors});ctx.close()
  if not args.baseline:
   for module,unit_number,pool_index in [('m3',1,51),('m3',2,24),('m6',1,11)]:
    text=(root/module/'index.html').read_text('utf-8');units=json.JSONDecoder().raw_decode(text.split('var U=',1)[1])[0];card=next(u for u in units if u['n']==unit_number)['pool'][pool_index]
    ctx,page=new_page(browser,390);page.goto(host+'/pt/'+module+'/',wait_until='networkidle')
    page.evaluate("card=>{EPIJogo.montar({itens:[card],chave:'qa-transversal-index',variar:false});document.querySelector('.jogo-alvo').id='baralho'}",card)
    page.locator('#baralho .ops [data-j="'+str(card['c'])+'"]').click();assert 'Certo' in page.locator('.casca-folha').inner_text();results.append({'challenge':card['_l'],'correct_answer':card['o'][card['c']],'rendered_correct':True});ctx.close()
   ctx,page=new_page(browser,390);page.goto(host+'/pt/m3/licao-m3-f11/',wait_until='networkidle')
   page.evaluate("card=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:[card],chave:'qa-transversal-vf',variar:false});document.querySelector('.jogo-alvo').id='baralho'}",bank('m3-f11')[11])
   page.locator('#baralho .ops [data-j="1"]').click();assert 'deve mandar' in page.locator('.casca-folha').inner_text()
   results.append({'question_assumption_feedback':True});ctx.close()
  if not args.baseline:
   ctx,page=new_page(browser,1440);page.goto(host+'/pt/projetar/?pagina=/pt/m7/licao-m7-f13/',wait_until='networkidle');frame=page.frame_locator('#lesson-frame');frame.locator('#baralho .cartao').wait_for();page.locator('[data-projection-size="large"]').click()
   frame.locator('body').evaluate("(el,card)=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:[card],chave:'qa-transversal-projecao',variar:false});document.querySelector('.jogo-alvo').id='baralho'}",bank('m7-f13')[18])
   assert frame.locator('html').get_attribute('data-projection-size')=='large';assert frame.locator('.paralelo .lado').nth(1).bounding_box()['width']>=200;assert not frame.locator('body').evaluate('()=>document.documentElement.scrollWidth>innerWidth+2');page.screenshot(path=str(out/'projecao-1440.png'));results.append({'projection_large':True,'readable_columns':True});ctx.close()
  browser.close()
finally:server.shutdown()
(out/('baseline.json' if args.baseline else 'qa.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print('PASS baseline' if args.baseline else 'PASS transversal layout and M3 full lesson')
