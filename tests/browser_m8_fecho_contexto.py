"""Focused browser regression for linked support and the two-poem exam task."""
from functools import partial
from http.server import ThreadingHTTPServer
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler, new_page

server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/pt'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);errors=[]
   page.on('pageerror',lambda err:errors.append(str(err)))
   page.goto(host+'/m8/gramatica-aspeto/',wait_until='networkidle')
   page.locator('#seguir').click()
   assert 'sem exigir contagem exata' in page.locator('#palco').inner_text()
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
   page.locator('#seguir').click()
   for row,answer in enumerate((0,1,2,3,1,2)):
    page.locator(f'#palco button[data-v="{row}"][data-j="{answer}"]').click()
   page.locator('#verificar').click()
   assert '6 de 6 certas' in page.locator('body').inner_text()
   page.locator('#seguir').click()
   page.get_by_text('«Ela relia a carta.»',exact=True).click()
   assert 'se a personagem parou ou terminou depois' in page.locator('body').inner_text()
   page.locator('#seguir').click()
   page.get_by_text('Ele abria a janela quando ouviu o carro.',exact=True).click()
   assert 'Não sabemos se parou' in page.locator('body').inner_text()
   page.locator('#seguir').click()
   page.get_by_text('Naquela manhã, abriu a janela várias vezes seguidas.',exact=True).click()
   assert 'sem número exato' in page.locator('body').inner_text()
   page.locator('#seguir').click()
   page.get_by_text('A primeira apresenta um hábito; a segunda, uma repetição num episódio.',exact=True).press('Enter')
   assert 'Não provam, por si sós' in page.locator('body').inner_text()
   page.locator('#seguir').click();page.reload(wait_until='networkidle')
   assert 'O meu cartão' in page.locator('#palco').inner_text()
   page.goto(host+'/exame/#s17/escrever',wait_until='networkidle')
   assert 'Comparei os dois poemas selecionados' in page.locator('#app').inner_text()
   page.goto(host+'/exame/#s17/corrigir',wait_until='networkidle')
   assert page.locator('#correction').is_hidden()
   page.locator('[data-action="reveal"]').click()
   assert 'Não é necessário acrescentar um terceiro autor' in page.locator('#correction').inner_text()
   assert not errors,errors
   ctx.close();print(f'PASS linked support and s17 {width}',flush=True)
  browser.close()
finally:server.shutdown()
