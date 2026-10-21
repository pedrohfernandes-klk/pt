from functools import partial
from http.server import ThreadingHTTPServer
import json,threading,argparse
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
from browser_m2_complete import respond
parser=argparse.ArgumentParser();parser.add_argument('--module',choices=['m2','m7'],default='m2');parser.add_argument('--lessons',default='08,09');args=parser.parse_args();module=args.module;lessons=args.lessons.split(',');assert lessons and all(n in (['06','08','09','11'] if module=='m2' else ['14','15']) for n in lessons)
OUT=ROOT.parents[1]/('outputs/m7-sonho-memoria' if module=='m7' else 'outputs/m2-desfecho-satira' if '06' in lessons else 'outputs/m2-revisao');OUT.mkdir(parents=True,exist_ok=True)
def bank(n):return json.JSONDecoder().raw_decode((ROOT/f'{module}/licao-{module}-f{n}/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
results=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1280):
   for n in lessons:
    ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(host+f'/pt/{module}/licao-{module}-f{n}/',wait_until='networkidle');assert page.evaluate('!!window.EPITipos.rever')
    def mount(items):page.evaluate('''items=>{document.querySelectorAll('.casca').forEach(n=>n.remove());window.responses=[];window.api=EPIJogo.montar({itens:items,chave:'qa-revision',variar:false,mostrarAnterior:false,evento:e=>{if(e.t==='resp')responses.push(e.ok)}});document.querySelector('.jogo-alvo').id='baralho';}''',items)
    if module=='m7':
     for normal_attempt in range(2):
      if normal_attempt:page.locator('[data-repetir]').click()
      for action in range(180):
       if page.locator('#baralho .cartao.fim').count():break
       respond(page)
      else:raise AssertionError('Normal lesson stalled')
      state=page.evaluate('key=>JSON.parse(localStorage.getItem(key))','licao-'+module+'-f'+n);assert state['lida'] and state['tentativas']>=normal_attempt+1
      page.reload(wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for()
    cards=bank(n);mount(cards)
    for step in range(160):
     if page.locator('#baralho .cartao.fim').count():break
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(n,width,step)
     respond(page)
    else:raise AssertionError('Bank did not finish')
    x=next(c for c in cards if c['t']=='rever')
    for wrong in [i for i in range(len(x['o'])) if i!=x['c']]:
     mount([x]);confirm=page.locator('[data-rever-confirmar]');assert confirm.is_disabled()
     for chosen in [wrong,x['c'],wrong]:
      b=page.locator(f'[data-rever-op="{chosen}"]');b.focus();b.press('Enter');assert b.get_attribute('aria-pressed')=='true';assert x['o'][chosen] in page.locator('[data-rever-prev]').inner_text();assert page.evaluate('responses.length')==0
     page.screenshot(path=str(OUT/f'experimentar-{n}-{width}.png'));summary=page.locator('summary').filter(has_text='Comparar com o rascunho');summary.focus();summary.press('Enter');assert summary.evaluate('e=>e.parentElement.open');assert x['frase'] in summary.evaluate('e=>e.parentElement.innerText');summary.press('Enter');page.evaluate('window.lastConfirm=document.querySelector("[data-rever-confirmar]")');confirm.focus();confirm.press('Enter');assert page.evaluate('responses')==[False];page.evaluate('lastConfirm.click()');assert page.evaluate('responses')==[False]
     assert x['fe'][wrong] in page.locator('.casca-folha').inner_text();respond(page);page.locator('[data-errados]').click();assert page.locator('[data-rever-op]').count()==3
     page.locator(f'[data-rever-op="{x["c"]}"]').click();page.locator('[data-rever-confirmar]').click();assert 'Certo' in page.locator('.casca-folha').inner_text();respond(page);assert page.locator('.cartao.fim').count()==1
    mount([x]);page.locator(f'[data-rever-op="{x["c"]}"]').click();page.locator('[data-rever-confirmar]').click();assert page.evaluate('responses')==[True]
    assert not errors,errors;results.append({'lesson':n,'width':width,'full_bank':len(cards),'all_wrong_feedbacks':True,'preview_reversible':True,'retry_correct':True,'errors':errors});ctx.close();print('PASS revision and full bank',n,width,flush=True)
  # The new format can also render in the existing unit challenge context.
  ctx,page=new_page(browser,1280);page.goto(host+f'/pt/{module}/',wait_until='networkidle');assert page.evaluate('!!window.EPITipos.rever');page.evaluate('''card=>{EPIJogo.montar({itens:[card],chave:'qa-revision-unit',variar:false});}''',next(c for c in bank(lessons[-1]) if c['t']=='rever'));page.locator('[data-rever-op="0"]').click();page.locator('[data-rever-confirmar]').click();assert 'Certo' in page.locator('.casca-folha').inner_text();ctx.close()
  ctx,page=new_page(browser,1440);page.goto(host+f'/pt/projetar/?pagina=/pt/{module}/licao-{module}-f{lessons[0]}/',wait_until='networkidle');frame=page.frame_locator('#lesson-frame');frame.locator('#baralho .cartao').wait_for();page.locator('[data-projection-size="large"]').click()
  card=next(c for c in bank(lessons[0]) if c['t']=='rever');frame.locator('body').evaluate("(el,card)=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:[card],chave:'qa-revision-projection',variar:false});}",card)
  frame.locator('[data-rever-op="0"]').focus();frame.locator('[data-rever-op="0"]').press('Enter');assert card['o'][card['c']] in frame.locator('[data-rever-prev]').inner_text();assert frame.locator('html').get_attribute('data-projection-size')=='large';assert frame.locator('body').evaluate('()=>document.documentElement.scrollWidth<=innerWidth+2');page.screenshot(path=str(OUT/'projecao-1440.png'));ctx.close()
  if module=='m2' and '06' in lessons:
   ctx,page=new_page(browser,390);ctx.add_init_script("if(!localStorage.getItem('licao-m2-f06'))localStorage.setItem('licao-m2-f06',JSON.stringify({lida:true,melhor:12,totalMelhor:12,tentativas:3,xp:125,exposicoes:{11:3,15:2,23:1},ult:'11,15,23'}))")
   page.goto(host+'/pt/m2/licao-m2-f06/',wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for()
   for run in range(2):
    state=page.evaluate("JSON.parse(localStorage.getItem('licao-m2-f06'))");assert state['lida'] and state['melhor']==12 and state['tentativas']==3;assert state['exposicoes']=={'17':3,'10':2,'23':1},state
    if run==0:page.reload(wait_until='networkidle')
   results.append({'legacy_f06':True,'scores_preserved':True,'exposures_mapped_once':True});ctx.close()
  browser.close()
finally:server.shutdown()
(OUT/'qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
