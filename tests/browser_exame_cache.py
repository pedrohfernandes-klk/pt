from functools import partial
from http.server import ThreadingHTTPServer
import threading,json
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}'
data=json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf-8'))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);requests=[];errors=[]
   page.on('request',lambda r: requests.append(r.url));page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(host+'/exame/#s01/aquecer',wait_until='networkidle')
   page.locator('[data-action="another"]').wait_for()
   app=next(u for u in requests if '/exame/app.js?' in u)
   req=next(u for u in requests if '/sessoes.json?' in u)
   assert parse_qs(urlparse(app).query)==parse_qs(urlparse(req).query)
   # 01/11/2026: o banco completo substitui os pares aleatórios; recomeçar preserva o melhor e as chaves anteriores.
   page.evaluate("localStorage.setItem('pt-exame-sessao-s01',JSON.stringify({warm:['antigo'],remaining:['guardado']}));localStorage.setItem('aquecimento-exame-s01',JSON.stringify({lida:true,melhor:12,totalMelhor:12,tentativas:2,versao:1}))")
   old=page.evaluate("localStorage.getItem('pt-exame-sessao-s01')")
   page.locator('[data-aquecimento]').click()
   page.locator('#baralho .cartao').wait_for()
   assert 'Já feita' in page.locator('#baralho').text_content()
   page.locator('[data-exame-voltar]').first.click()
   page.locator('[data-action="another"]').click()
   page.locator('#baralho .cartao').wait_for()
   assert 'recomecar=1' in page.url
   assert 'Já feita' not in page.locator('#baralho').text_content()
   assert page.evaluate("localStorage.getItem('pt-exame-sessao-s01')")==old
   assert page.evaluate("JSON.parse(localStorage.getItem('aquecimento-exame-s01')).melhor")==12
   page.reload(wait_until='networkidle')
   assert 'Já feita' not in page.locator('#baralho').text_content()
   bank=page.evaluate("JSON.parse(document.getElementById('exame-aquecimento-dados').textContent)")
   assert len([c for c in bank['cartoes'] if c['t']!='ler'])==12
   assert {c.get('legacyId') for c in bank['cartoes'] if c.get('legacyId')}=={q['id'] for q in data['sessions'][0]['warmup']}
   assert not errors,errors
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   print('PASS versioned data request; full bank; restart preserves previous progress; reload; layout',width,flush=True)
   ctx.close()
  browser.close()
finally:server.shutdown()
