from functools import partial
from http.server import ThreadingHTTPServer
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
from browser_m2_complete import respond
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(f'http://127.0.0.1:{server.server_port}/pt/m1/licao-m1-f01/',wait_until='networkidle')
   page.evaluate('''() => {document.querySelectorAll('.casca').forEach(n=>n.remove());window.results=[];window.missed=0;const items=[{t:'ler',html:'<p>Consulta <b class="gt" data-s="uma explicação útil">a palavra</b>.</p><ul class="vida"><li>Uma etapa</li></ul>'},{t:'vf',id:0,g:'unico',p:'Uma voz construída não se confunde automaticamente com o autor.',v:true,f:'A voz pertence ao texto.'},...Array.from({length:12},(_,i)=>({t:'vf',id:i+1,g:'outros',p:'Pergunta '+(i+1),v:false,f:'Retoma a prova no texto.'}))];window.api=EPIJogo.montar({itens:items,chave:'qa-rotacao',evento:e=>{if(e.t==='resp'){results.push(e.x.id);if(!e.ok)missed++}}});document.querySelector('.casca.sobreposta .jogo-alvo').id='baralho';}''')
   gt=page.locator('#baralho .gt');gt.focus();gt.press('Enter');assert gt.get_attribute('aria-expanded')=='true'
   gt.press('Space');assert gt.get_attribute('aria-expanded')=='false'
   life=page.locator('#baralho .vida li');life.focus();life.press('Enter');assert life.get_attribute('aria-expanded')=='true'
   runs=[]
   for attempt in range(2):
    if attempt:page.evaluate('results=[];missed=0;api.reiniciar()')
    for _ in range(50):
     if page.locator('#baralho .cartao.fim').count():break
     respond(page)
    else:raise AssertionError('Attempt did not finish')
    missed=page.evaluate('missed')
    if missed:
     assert 'O que rever' in page.locator('#baralho [data-aprendeste]').inner_text()
     page.locator('#baralho [data-aprendeste]').click()
     assert page.locator('#baralho .aprendeste li').count()==missed
    ids=page.evaluate('results');assert 0 in ids;assert len(ids)==len(set(ids));runs.append(set(ids))
   assert runs[0]!=runs[1]
   assert len(runs[0]|runs[1])==13
   assert page.evaluate('Object.keys(JSON.parse(localStorage.getItem("qa-rotacao")).exposicoes).length')==13
   page.evaluate('''() => {const c=api.casca;c.corpo.innerHTML='';EPIJogo.montar({casca:c,itens:[{t:'completar',frase:'A voz [1] o mundo.',lacunas:[{o:['observa','ignora'],c:0}],f:'A ação é observar.'}],chave:'qa-lacuna',variar:false})}''')
   assert page.locator('.casca.sobreposta select[aria-label="Lacuna 1 de 1"]').count()==1, page.locator('select').evaluate_all('(els)=>els.map(el=>el.outerHTML)')
   page.evaluate('''() => {const c=api.casca;c.corpo.innerHTML='';window.hintPoints=[];EPIJogo.montar({casca:c,itens:[{t:'vf',p:'A primeira afirmação permite observar uma pista.',v:true,f:'A prova sustenta a afirmação.'},{t:'vf',p:'A segunda afirmação permite observar uma pista.',v:true,f:'A prova sustenta a afirmação.'}],pistas:['Procura a prova antes de decidir.'],chave:'qa-ajuda-sem-penalizacao',variar:false,evento:e=>{if(e.t==='resp')hintPoints.push(e.xp)}});c.corpo.querySelector('.jogo-alvo').id='baralho';}''')
   page.locator('#baralho [data-j="1"]').click()
   page.locator('.casca [data-c-folha]:visible [data-seguinte]').click()
   page.locator('.casca [data-pista-ess]').click()
   assert 'menos cinco pontos' not in page.locator('#baralho .pista').inner_text()
   page.locator('#baralho [data-j="1"]').click()
   assert page.evaluate('hintPoints')==[10,20]
   assert not errors,errors
   print('PASS keyboard, repeated completed attempts, coverage and lacuna names',width,flush=True)
   ctx.close()
  ctx,page=new_page(browser,1440)
  page.goto(f'http://127.0.0.1:{server.server_port}/pt/projetar/?pagina=/pt/m1/licao-m1-f01/',wait_until='networkidle')
  frame=page.frame_locator('#lesson-frame')
  frame.locator('.casca [data-seguinte]').wait_for()
  page.locator('[data-projection-size="large"]').click()
  assert frame.locator('html').get_attribute('data-projection-size')=='large'
  frame.locator('.casca [data-seguinte]').click()
  assert frame.locator('script[src*="jogo.js?v=20261021-ux06"]').count()==1
  print('PASS classroom projection: lesson, next card and large text',flush=True)
  ctx.close()
  browser.close()
finally:server.shutdown()
