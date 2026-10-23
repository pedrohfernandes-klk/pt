"""Post-performance entry, complete F28/F20 banks, feedback, route and projection."""
from functools import partial
from http.server import ThreadingHTTPServer
import json,threading,re
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page
from browser_m2_complete import respond
from sys import path
path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards

server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/pt'

def finish(page):
 for _ in range(150):
  if page.locator('#baralho .cartao.fim').count():return
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
  respond(page)
 raise AssertionError('M4 route stalled')

try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(host+'/',wait_until='networkidle')
   assert '16 lições' in page.locator('li[data-m="M4"]').inner_text().lower()
   page.goto(host+'/mapa/',wait_until='networkidle')
   assert '16 lições' in page.locator('summary').filter(has_text='M4 —').inner_text().lower()
   page.goto(host+'/m4/',wait_until='networkidle')
   assert page.locator('.cabm .n').inner_text()=='4'
   assert page.locator('.passos > li .n').all_text_contents()==[str(i) for i in range(1,19)]
   steps=page.locator('[data-unidade="2"] .passos > li')
   assert steps.first.get_attribute('id')=='m4-f28'
   assert steps.nth(1).get_attribute('id')=='m4-f07'
   steps.first.get_by_role('link').click()
   # 23/10/2026: espera pelo cartão desenhado (lido logo a seguir ao clique, o #baralho ainda vazio dava falsos erros em máquinas lentas)
   page.wait_for_url('**/licao-m4-f28/');page.locator('#baralho .cartao').wait_for()
   assert 'Já viste' in page.locator('#baralho').inner_text()
   page.locator('.casca [data-seguinte]').click()
   assert 'Raquel Castro' in page.locator('#baralho').inner_text()
   assert 'Almeida Garrett' in page.locator('#baralho').inner_text()
   page.locator('.casca [data-seguinte]').click()
   page.locator('#baralho button[data-j="0"]').press('Enter')
   assert 'não uma transcrição integral' in page.locator('[data-c-folha]').inner_text()
   page.locator('[data-c-folha] [data-seguinte]').click()
   page.locator('summary').filter(has_text='Ajuda: como sustentar').press('Enter')
   assert 'Procura outro detalhe' in page.locator('#baralho').inner_text()
   page.locator('.casca [data-seguinte]').click()
   # The engine rotates adjacent equivalent activities inside a group.
   for _ in range(5):
    if page.locator('#baralho button[data-j="1"]').count():break
    respond(page)
   assert 'interpretação sustentada' in page.locator('#baralho').inner_text()
   page.locator('#baralho button[data-j="1"]').press('Enter')
   assert 'Confrontar' not in page.locator('[data-c-folha]').inner_text()
   assert 'hipótese liga' in page.locator('[data-c-folha]').inner_text()
   page.locator('[data-c-folha] [data-seguinte]').click()
   # Shared engine persists completion, not a half-finished session.
   page.reload(wait_until='networkidle')
   assert ''.join(page.locator('[data-c-num]').inner_text().split())=='1/15'
   assert 'O palco abriu uma pergunta' in page.locator('#baralho').inner_text()
   finish(page)
   assert page.evaluate('!!JSON.parse(localStorage.getItem("licao-m4-f28-a1"))')
   page.reload(wait_until='networkidle')
   assert page.locator('#baralho .cartao.fim').is_visible()
   page.goto(host+'/m4/licao-m4-f07/',wait_until='networkidle')
   page.get_by_role('button',name='Menu',exact=True).click()
   assert page.get_by_role('link',name=re.compile(r'^Lição anterior')).get_attribute('href').endswith('/licao-m4-f28/')
   assert 'passo 10 de 18' in page.locator('[data-c-painel]').inner_text().lower()
   page.goto(host+'/m4/licao-m4-f10/',wait_until='networkidle')
   page.get_by_role('button',name='Menu',exact=True).click()
   assert page.get_by_role('link',name=re.compile(r'^Lição seguinte')).get_attribute('href').endswith('/licao-m4-f28/')
   page.goto(host+'/m4/painel-m4-f28/',wait_until='networkidle')
   assert '20–35 min' in page.locator('main').inner_text()
   assert 'Não classificar a memória' in page.locator('main').inner_text()
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
   page.goto(host+'/m4/licao-m4-f20/',wait_until='networkidle')
   assert 'Já viste' in page.locator('#baralho').inner_text()
   finish(page)
   # Exercise every retained variant in F20, in addition to the normal deck.
   cards=lesson_cards(ROOT/'m4/licao-m4-f20/index.html')
   page.evaluate('''cards=>{
    document.querySelectorAll('.casca').forEach(n=>n.remove());
    EPIJogo.montar({itens:cards,chave:'qa-m4-tpc-f20-banco',variar:false});
    document.querySelector('.jogo-alvo').id='baralho';
   }''',cards)
   finish(page)
   page.goto(host+'/m4/painel-m4-f20/',wait_until='networkidle')
   for i in (4,5,12,15):
    assert page.locator(f'select[data-r-k] option[value="{i}"]').inner_text()==cards[i]['p']
   assert not errors,errors
   ctx.close();print(f'PASS post-TPC F28/F20 normal/full, wrong/correct feedback, keyboard, resume, teacher labels and route {width}',flush=True)
  ctx,page=new_page(browser,1440)
  page.goto(host+'/projetar/?pagina=/pt/m4/licao-m4-f28/',wait_until='networkidle')
  frame=page.frame_locator('#lesson-frame')
  assert '45 minutos' in frame.locator('#baralho').inner_text()
  page.locator('[data-projection-size="large"]').click()
  frame.locator('.casca [data-seguinte]').click()
  assert frame.locator('html').get_attribute('data-projection-size')=='large'
  assert 'Raquel Castro' in frame.locator('#baralho').inner_text()
  assert not frame.locator('html').evaluate('(el)=>el.scrollWidth>innerWidth+3')
  assert page.locator('#page-qr svg').count()==1
  ctx.close();browser.close();print('PASS post-TPC large projection',flush=True)
finally:server.shutdown()
