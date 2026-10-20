from functools import partial
from http.server import ThreadingHTTPServer
import threading,sys,json
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for mode in ('oral','caderno'):
   ctx,page=new_page(browser,320)
   page.goto(host+'/m2/',wait_until='networkidle')
   page.evaluate('''() => { for(const id of ['m2-f01','m2-f02','m2-f07','m2-f06']) {localStorage.setItem('licao-'+id,JSON.stringify({lida:true}));localStorage.setItem('licao-'+id+'-a1',JSON.stringify({lida:true}));} for(const id of ['ines-panela','gram-oracoes-farsa','ines-escolher']) localStorage.setItem('epi-pt-'+id,JSON.stringify({fim:true}));localStorage.setItem('desafio-unidade-v2-M2-u1',JSON.stringify({ganho:true,melhor:8,total:8}));}''')
   page.reload(wait_until='networkidle')
   page.locator('[data-fim="1"] > summary').click()
   box=page.locator('[data-sintese="1"]')
   box.locator(f'input[value="{mode}"]').check()
   box.locator('[data-sintese-registar]').click()
   if mode=='oral':
    out=ROOT.parents[1]/'outputs/sintese-interpretacao'
    out.mkdir(parents=True,exist_ok=True)
    box.screenshot(path=str(out/'sintese-oral-320.png'))
   assert page.locator('[data-resp="1"]').input_value()==''
   assert page.evaluate('JSON.parse(localStorage.getItem("percurso-M2")).unidades[0].cumprida')
   assert box.locator('[data-sintese-rever]').evaluate('el=>el===document.activeElement')
   page.reload(wait_until='networkidle')
   assert mode in page.evaluate('localStorage.getItem("percurso-sintese-M2-u1")')
   page.locator('[data-fim="1"] > summary').click()
   box.locator('[data-sintese-rever]').click()
   assert not page.evaluate('JSON.parse(localStorage.getItem("percurso-M2")).unidades[0].cumprida')
   page.locator('[data-fim="1"] .sintese-notas summary').click()
   page.locator('[data-resp="1"]').fill(' '.join(['nota']*85))
   page.reload(wait_until='networkidle')
   assert not page.evaluate('JSON.parse(localStorage.getItem("percurso-sintese-M2-u1")).feita')
   print('PASS empty synthesis, completion, focus, reload, undo and optional notes:',mode,flush=True)
   ctx.close()
  ctx,page=new_page(browser,320)
  page.goto(host+'/m2/',wait_until='networkidle')
  page.evaluate("localStorage.removeItem('percurso-sintese-M2-u1-inicializada'); localStorage.setItem('percurso-v2-M2-u1',JSON.stringify(Array(85).fill('anterior').join(' ')))")
  page.reload(wait_until='networkidle')
  assert page.evaluate('JSON.parse(localStorage.getItem("percurso-sintese-M2-u1")).modo')=='anterior'
  print('PASS prior qualifying synthesis migration',flush=True)
  ctx.close()
  plan=json.loads((ROOT/'docs/pedagogia/interpretacoes-abertas-20261020.json').read_text('utf-8'))
  for x in plan['unscored_cards']:
   m=x['module'];lesson=x['lesson'];path=f'{m}/licao-{m}-f{lesson}'
   ctx,page=new_page(browser,320);page.goto(host+'/'+path+'/',wait_until='networkidle')
   card=lesson_cards(ROOT/path/'index.html')[x['index']]
   page.evaluate('card=>EPIJogo.montar({itens:[card],chave:"qa-open",variar:false})',card)
   modal=page.locator('.casca.sobreposta');modal.locator('.cartao details summary').click()
   assert modal.locator('.cartao details').evaluate('el=>el.open')
   assert modal.locator('[data-j]').count()==0
   print('PASS open interpretation',path,x['index'],flush=True);ctx.close()
  browser.close()
finally: server.shutdown()
