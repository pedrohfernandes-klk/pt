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
  # 01/11/2026: nenhum módulo mantém a síntese separada; todos têm aula de tarefa.
  assert TASK_MODULES == set(range(1,10))
  # 26/10: M1/M4/M7 close in the task lesson. Historic notes stay readable,
  # never migrate into a new assessment or become a second synthesis gate.
  for m in sorted(TASK_MODULES):
   ctx,page=new_page(browser,320);errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(host+f'/m{m}/',wait_until='networkidle')
   # 31/10/2026: a primeira lição do M3 é F02; usa a primeira lição real do percurso.
   first=json.loads(page.locator('#epi-unidades-pedagogicas').text_content())[0]['lessons'][0]
   records={f'percurso-M{m}-u1':'A minha resposta anterior <img src=x>',
            f'percurso-v2-M{m}-u1':' '.join(['anterior']*85),
            f'percurso-sintese-M{m}-u1':json.dumps({'feita':True,'modo':'caderno'}),
            f'desafio-M{m}-u1':json.dumps({'ganho':True,'melhor':8,'total':8}),
            f'licao-{first}':json.dumps({'lida':True,'melhor':10,'total':12,'xp':100})}
   if m==7:records['percurso-M7-u5']='Registo da antiga etapa cinco'
   # 27/10/2026: o M2 tinha quatro etapas antes das unidades; a quarta continua legível no arquivo.
   if m==2:records['percurso-M2-u4']='Registo da antiga etapa quatro'
   page.evaluate('records=>Object.entries(records).forEach(([k,v])=>localStorage.setItem(k,v))',records)
   before=learning_storage(page);page.reload(wait_until='networkidle')
   assert learning_storage(page)==before
   assert page.locator('[data-sintese], [data-sintese-registar], #cartao, #copiar-cartao').count()==0
   assert not page.locator('#arquivo-percurso').is_visible()
   assert page.locator('button[data-desafio]:visible').count()==0
   # 01/11/2026: um registo antigo sem data lê-se «Feita», sem inventar uma data.
   assert page.locator(f'#{first} [data-cz-state-text]').inner_text() == 'Feita'
   assert page.locator(f'#{first} [data-cz-point]').get_attribute('aria-hidden') == 'true'
   # 03/11/2026: no piloto M4 os materiais abrem dentro dos recursos nativos.
   if page.locator('.m4-recursos:not([open])').count():
       page.locator('.m4-recursos > summary').click()
   # 03/11/2026: abrir o mesmo arquivo pelo acesso docente recolhido na boia.
   page.locator('.pt-apoios > summary').click()
   page.locator('.pt-apoios a[href="?arquivo=1#arquivo-percurso"]').click()
   page.wait_for_url('**/?arquivo=1#arquivo-percurso')
   archive=page.locator('#arquivo-percurso')
   assert archive.is_visible() and '<img src=x>' in archive.inner_text()
   assert archive.locator('img').count()==0
   if m==7:assert 'antiga etapa cinco' in archive.inner_text()
   if m==2:assert 'antiga etapa quatro' in archive.inner_text()
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
