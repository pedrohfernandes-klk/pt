from functools import partial
from http.server import ThreadingHTTPServer
import threading,json,re
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
from browser_m2_complete import respond
OUT=ROOT.parents[1]/'outputs/m2-coerencia';OUT.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
results=[]
def at_task_2(page):
 # 28/10/2026: a ligação #desafio-unidade-2 da F09 (congelada) acaba na aula de tarefa da unidade 2, visível e assinalada.
 page.wait_for_url(re.compile(r'/pt/m2/#(desafio|tarefa)-unidade-2$'));page.wait_for_function('location.hash==="#tarefa-unidade-2"')
 task=page.locator('#tarefa-unidade-2');assert task.is_visible() and task.evaluate('e=>e.classList.contains("aqui")')
 assert task.locator('a').first.get_attribute('href').endswith('tarefas/m2-u2/')
 page.wait_for_function('()=>{const r=document.getElementById("tarefa-unidade-2").getBoundingClientRect();return r.top>=0&&r.top<innerHeight&&r.height>0}')
 assert not page.locator('#arquivo-percurso').is_visible()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1280):
   ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   def local(route):route.fulfill(response=route.fetch(url=route.request.url.replace('https://pedrohfernandes-klk.github.io',host)))
   page.route('https://pedrohfernandes-klk.github.io/pt/**',local)
   page.goto(host+'/pt/m2/',wait_until='networkidle')
   ids=page.locator('.unidade[data-u="2"] li[data-passo]').evaluate_all('(els)=>els.map(e=>e.dataset.passo)');assert ids==['m2-f11','m2-f10','m2-f08','m2-f09']
   assert page.locator('button[data-desafio]').count()==2;assert page.locator('.module-opening figure.doc').is_visible()
   for n,expected in [(1,['m2-f01','m2-f02','m2-f07','m2-f06']),(2,ids)]:
    capture=page.evaluate('''n=>{let captured;const original=EPIJogo.montar;EPIJogo.montar=cfg=>{captured=cfg.itens.map(c=>c._l)};document.querySelector('[data-desafio="'+n+'"]').click();EPIJogo.montar=original;return captured;}''',n)
    assert len(capture)==8 and set(capture)==set(expected),(n,capture)
   page.locator('[data-unidade="2"]').screenshot(path=str(OUT/f'unidade-2-{width}.png'))
   # Follow the menu links, so order and destinations are tested as rendered.
   page.goto(host+'/pt/m2/licao-m2-f06/',wait_until='networkidle')
   for target in ['11','10','08','09']:
    page.locator('[data-c-menu]').first.click();link=page.locator('[data-c-painel] a').filter(has_text=re.compile('^Lição seguinte$')).first;assert link.count()==1;link.click();page.wait_for_url(f'**/licao-m2-f{target}/')
   # 28/10/2026 (revisão do PR #124): antes conferia-se só o URL (**/m2/#desafio-unidade-2), mas esse desafio
   # está no arquivo escondido. O índice leva à aula de tarefa da unidade 2, à vista, pelo menu e pelo botão final.
   page.locator('[data-c-menu]').first.click();page.locator('[data-c-painel] a').filter(has_text=re.compile('^Desafio da unidade 2$')).click();at_task_2(page)
   page.goto(host+'/pt/m2/licao-m2-f09/',wait_until='networkidle');page.evaluate("localStorage.setItem('licao-m2-f09',JSON.stringify({lida:true,melhor:6,totalMelhor:8,total:8,tentativas:1}))");page.reload(wait_until='networkidle')
   final=page.locator('[data-c-acoes] a').filter(has_text=re.compile('^Lição seguinte'));assert final.count()==1 and final.get_attribute('href')=='../#desafio-unidade-2';final.click();at_task_2(page)
   # The whole revised F07 bank, including readings and every exercise mechanic.
   page.goto(host+'/pt/m2/licao-m2-f07/',wait_until='networkidle')
   cards=json.JSONDecoder().raw_decode((ROOT/'m2/licao-m2-f07/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
   page.evaluate('''items=>{document.querySelectorAll('.casca').forEach(n=>n.remove());window.api=EPIJogo.montar({itens:items,chave:'qa-m2-f07-full',variar:false});document.querySelector('.jogo-alvo').id='baralho';}''',cards)
   for _ in range(200):
    if page.locator('#baralho .cartao.fim').count():break
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
    if 'O Escudeiro: a promessa e o bastidor' in page.locator('#baralho').inner_text():page.screenshot(path=str(OUT/f'bastidor-{width}.png'))
    if 'uma ordem e a sua finalidade' in page.locator('#baralho').inner_text().casefold():
     summary=page.locator('summary').filter(has_text='Consultar os tipos');summary.focus();summary.press('Enter');assert summary.evaluate('e=>e.parentElement.open');page.screenshot(path=str(OUT/f'exemplo-gramatica-{width}.png'))
    respond(page)
   else:raise AssertionError('F07 did not finish')
   # Existing F10 card: alternative for class or independent work opens by keyboard.
   page.goto(host+'/pt/m2/licao-m2-f10/',wait_until='networkidle')
   cards=json.JSONDecoder().raw_decode((ROOT/'m2/licao-m2-f10/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
   page.evaluate('''item=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:[item],chave:'qa-m2-without-visit',variar:false});}''',cards[2])
   summary=page.locator('summary').filter(has_text='Sem visita ao teatro');summary.focus();summary.press('Enter');assert summary.evaluate('e=>e.parentElement.open')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');page.screenshot(path=str(OUT/f'sem-visita-{width}.png'))
   assert not errors,errors;results.append({'width':width,'navigation':ids,'full_f07_cards':28,'no_visit_keyboard':True,'errors':errors});ctx.close()
   # Start at the real judgement screen in the two corrected legacy activities.
   for name in ['pero-visita','janelas-pregadas']:
    ctx,page=new_page(browser,width);ctx.add_init_script('localStorage.setItem('+json.dumps('epi-pt-'+name)+',JSON.stringify({i:4,r:{},p:{},fim:false,ini:true,sem:17}))')
    page.goto(host+'/pt/m2/'+name+'/',wait_until='networkidle')
    text=page.locator('#palco').inner_text();assert not any(x in text for x in ['Alencar','Cohen','Ega','Carlos'])
    source=(ROOT/f'm2/{name}/index.html').read_text('utf-8');e=json.JSONDecoder().raw_decode(source[re.search(r'var E=(\{"pasta")',source).start(1):])[0]
    for i,case in enumerate(e['passos'][4]['casos']):page.locator(f'#palco [data-v="{i}"][data-j="{1 if case[1] else 0}"]').click()
    page.locator('#verificar').click();assert '4 de 4' in page.locator('.casca').inner_text();assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');results.append({'activity':name,'width':width,'correct_judgements':4});ctx.close()
   print('PASS M2 sequence, full F07, no-visit alternative, corrected judgements',width,flush=True)
  ctx,page=new_page(browser,390);ctx.add_init_script("if(!localStorage.getItem('licao-m2-f07'))localStorage.setItem('licao-m2-f07',JSON.stringify({lida:true,melhor:12,totalMelhor:12,tentativas:3,xp:125,exposicoes:{3:2,8:4,23:1},ult:'23,3,8'}))")
  page.goto(host+'/pt/m2/licao-m2-f07/',wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for()
  for run in range(2):
   state=page.evaluate("JSON.parse(localStorage.getItem('licao-m2-f07'))");assert state['lida'] and state['melhor']==12 and state['tentativas']==3;assert state['exposicoes']=={'6':2,'11':4,'26':1},state
   if run==0:page.reload(wait_until='networkidle')
  results.append({'legacy_f07':True,'scores_preserved':True,'exposures_mapped_once':True});ctx.close()
  ctx,page=new_page(browser,1440);page.route('https://pedrohfernandes-klk.github.io/pt/**',lambda route:route.fulfill(response=route.fetch(url=route.request.url.replace('https://pedrohfernandes-klk.github.io',host))))
  page.goto(host+'/pt/projetar/?pagina=/pt/m2/licao-m2-f07/',wait_until='networkidle');frame=page.frame_locator('#lesson-frame');frame.locator('#baralho .cartao').wait_for();page.locator('[data-projection-size="large"]').click();assert frame.locator('html').get_attribute('data-projection-size')=='large'
  for _ in range(35):
   if 'uma ordem e a sua finalidade' in frame.locator('#baralho').inner_text().casefold():break
   respond(frame)
  else:raise AssertionError('Worked example absent in projection')
  page.screenshot(path=str(OUT/'projecao-1440.png'));results.append({'projection':1440,'large_text':True,'worked_example':True});ctx.close()
  browser.close()
finally:server.shutdown()
(OUT/'qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
