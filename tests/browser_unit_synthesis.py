from functools import partial
from http.server import ThreadingHTTPServer
import threading,sys,json
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
from browser_task_contract import TASK_MODULES, learning_storage
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
   # 23/10/2026 (plano de melhoria, fase 0): a síntese já não tem caixa de notas nem botão «Copiar para o Teams».
   assert page.locator('[data-fim="1"] textarea, [data-fim="1"] [data-copiar], [data-fim="1"] .sintese-notas').count()==0
   assert page.evaluate('JSON.parse(localStorage.getItem("percurso-M2")).unidades[0].cumprida')
   assert box.locator('[data-sintese-rever]').evaluate('el=>el===document.activeElement')
   page.reload(wait_until='networkidle')
   assert mode in page.evaluate('localStorage.getItem("percurso-sintese-M2-u1")')
   page.locator('[data-fim="1"] > summary').click()
   box.locator('[data-sintese-rever]').click()
   assert not page.evaluate('JSON.parse(localStorage.getItem("percurso-M2")).unidades[0].cumprida')
   # 23/10/2026 (plano de melhoria, fase 0): sem notas no ecrã, confirma-se só que o «Ainda estou a rever» persiste.
   page.reload(wait_until='networkidle')
   assert not page.evaluate('JSON.parse(localStorage.getItem("percurso-sintese-M2-u1")).feita')
   print('PASS synthesis without on-screen writing, completion, focus, reload and undo:',mode,flush=True)
   ctx.close()
  ctx,page=new_page(browser,320)
  page.goto(host+'/m2/',wait_until='networkidle')
  page.evaluate("localStorage.removeItem('percurso-sintese-M2-u1-inicializada'); localStorage.setItem('percurso-v2-M2-u1',JSON.stringify(Array(85).fill('anterior').join(' ')))")
  page.reload(wait_until='networkidle')
  assert page.evaluate('JSON.parse(localStorage.getItem("percurso-sintese-M2-u1")).modo')=='anterior'
  print('PASS prior qualifying synthesis migration',flush=True)
  ctx.close()
  # 26/10: M1/M4/M7 close in the task lesson. Historic notes stay readable,
  # never migrate into a new assessment or become a second synthesis gate.
  for m in sorted(TASK_MODULES):
   ctx,page=new_page(browser,320);errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(host+f'/m{m}/',wait_until='networkidle')
   records={f'percurso-M{m}-u1':'A minha resposta anterior <img src=x>',
            f'percurso-v2-M{m}-u1':' '.join(['anterior']*85),
            f'percurso-sintese-M{m}-u1':json.dumps({'feita':True,'modo':'caderno'}),
            f'desafio-M{m}-u1':json.dumps({'ganho':True,'melhor':8,'total':8}),
            f'licao-m{m}-f01':json.dumps({'lida':True,'melhor':10,'total':12,'xp':100})}
   if m==7:records['percurso-M7-u5']='Registo da antiga etapa cinco'
   page.evaluate('records=>Object.entries(records).forEach(([k,v])=>localStorage.setItem(k,v))',records)
   before=learning_storage(page);page.reload(wait_until='networkidle')
   assert learning_storage(page)==before
   assert page.locator('[data-sintese], [data-sintese-registar], #cartao, #copiar-cartao').count()==0
   assert not page.locator('#arquivo-percurso').is_visible()
   assert page.locator('button[data-desafio]:visible').count()==0
   assert 'lição feita' in page.locator(f'#m{m}-f01 [data-k]').inner_text()
   page.locator('.route-teacher-tools > summary').click()
   page.locator('.route-teacher-tools a[href="?arquivo=1#arquivo-percurso"]').click()
   page.wait_for_url('**/?arquivo=1#arquivo-percurso')
   archive=page.locator('#arquivo-percurso')
   assert archive.is_visible() and '<img src=x>' in archive.inner_text()
   assert archive.locator('img').count()==0
   if m==7:assert 'antiga etapa cinco' in archive.inner_text()
   assert learning_storage(page)==before
   assert not errors,(m,errors)
   print('PASS integrated task synthesis; historic keys read without migration or automatic assessment:',m,flush=True)
   ctx.close()
  plan=json.loads((ROOT/'docs/pedagogia/interpretacoes-abertas-20261020.json').read_text('utf-8'))
  for x in plan['unscored_cards']:
   m=x['module'];lesson=x['lesson'];path=f'{m}/licao-{m}-f{lesson}'
   ctx,page=new_page(browser,320);page.goto(host+'/'+path+'/',wait_until='networkidle')
   card=lesson_cards(ROOT/path/'index.html')[x['index']]
   page.evaluate('card=>EPIJogo.montar({itens:[card],chave:"qa-open",variar:false})',card)
   modal=page.locator('.casca.sobreposta');modal.locator('.cartao details summary').first.click()
   assert modal.locator('.cartao details').first.evaluate('el=>el.open')
   optional=modal.locator('.retoma-partilhada')
   if optional.count():
    optional.locator('summary').focus();optional.locator('summary').press('Enter')
    assert optional.evaluate('el=>el.open')
    assert 'A sós' in optional.inner_text()
   assert modal.locator('[data-j]').count()==0
   print('PASS open interpretation',path,x['index'],flush=True);ctx.close()
  browser.close()
finally: server.shutdown()
