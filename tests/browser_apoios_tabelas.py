"""M7-F15 table: real lesson CSS/engine, all rows, review and projection sizes."""
from functools import partial
from http.server import ThreadingHTTPServer
import sys,threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards

def mount(page,card):
 page.evaluate('''card=>{
  document.querySelectorAll('.casca').forEach(e=>e.remove());
  EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar ao apoio.</p>'}],chave:'qa-apoio-tabela',variar:false});
  document.querySelector('.jogo-alvo').id='baralho';
 }''',card)

def table_check(scope,width):
 table=scope.get_by_role('table',name='Como se formam palavras novas')
 assert table.count()==1
 assert table.locator('thead th[scope="col"]').count()==3
 assert table.locator('tbody tr').count()==7
 assert table.locator('tbody th[scope="row"]').all_text_contents()==['Sigla','Acrónimo','Truncação','Amálgama','Empréstimo','Extensão semântica','Onomatopeia']
 for row in table.locator('tbody tr').all():
  assert row.is_visible()
  assert row.locator('th,td').count()==3
  assert all(row.locator('th,td').evaluate_all('(els)=>els.map(e=>e.clientWidth>0&&getComputedStyle(e).display!=="none")'))
 assert table.locator('tbody th').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')>=16
 if width<=620:
  assert table.locator('caption').evaluate('e=>e.getBoundingClientRect().width')>=table.evaluate('e=>e.getBoundingClientRect().width')-4
  assert table.locator('tbody th').first.evaluate('e=>e.getBoundingClientRect().width')>=table.evaluate('e=>e.getBoundingClientRect().width')-4
 assert not scope.locator('html').evaluate('e=>e.scrollWidth>innerWidth+3')

def main():
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
 card=lesson_cards(ROOT/'m7/licao-m7-f15/index.html')[11]
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(headless=True)
   for width in (320,390,900,1440):
    for scheme in ('light','dark'):
     ctx=browser.new_context(viewport={'width':width,'height':900},color_scheme=scheme,reduced_motion='reduce')
     page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
     page.route('**/fonts.googleapis.com/**',lambda r:r.abort());page.route('**/fonts.gstatic.com/**',lambda r:r.abort())
     page.goto(host+'/m7/licao-m7-f15/',wait_until='networkidle');mount(page,card)
     assert page.evaluate('innerWidth')==width
     table_check(page,width)
     # Last row can be reached by normal keyboard scrolling within the lesson.
     page.locator('.casca-corpo').press('Control+End')
     page.wait_for_function('''()=>{
      const row=document.querySelector('.apoio-tabela tbody tr:last-child'),body=document.querySelector('.casca-corpo');
      return row.getBoundingClientRect().bottom<=body.getBoundingClientRect().bottom+2;
     }''')
     page.emulate_media(media='print')
     assert page.locator('.apoio-tabela').evaluate('e=>getComputedStyle(e).display')=='table'
     assert page.locator('.apoio-tabela thead').evaluate('e=>getComputedStyle(e).clipPath')=='none'
     assert page.locator('.apoio-tabela tbody tr').count()==7
     page.emulate_media(media='screen')
     page.locator('.casca [data-seguinte]').click()
     page.get_by_role('button',name='Ver os cartões já feitos',exact=True).click()
     page.get_by_role('button',name='Cartão 1',exact=True).click();table_check(page,width)
     assert not errors,(width,scheme,errors)
     print('PASS table and review:',width,scheme,flush=True);ctx.close()
   for scheme in ('light','dark'):
    ctx=browser.new_context(viewport={'width':1440,'height':900},color_scheme=scheme,reduced_motion='reduce')
    page=ctx.new_page()
    page.route('**/fonts.googleapis.com/**',lambda r:r.abort());page.route('**/fonts.gstatic.com/**',lambda r:r.abort())
    def local(route):
     response=route.fetch(url=host+route.request.url.split(host+'/pt',1)[1]);route.fulfill(response=response)
    page.route(host+'/pt/**',local)
    page.goto(host+'/pt/projetar/?pagina=%2Fpt%2Fm7%2Flicao-m7-f15%2F',wait_until='networkidle')
    frame=page.frame_locator('#lesson-frame');frame.locator('#baralho .cartao').wait_for()
    child=next(f for f in page.frames if '/m7/licao-m7-f15/' in f.url)
    mount(child,card)
    for size in ('small','medium','large'):
     page.locator(f'[data-projection-size="{size}"]').click()
     assert page.locator(f'[data-projection-size="{size}"]').get_attribute('aria-pressed')=='true'
     table_check(frame,child.evaluate('innerWidth'))
     assert frame.locator('.casca-corpo').evaluate('e=>["auto","scroll"].includes(getComputedStyle(e).overflowY)')
     print('PASS projected table:',size,scheme,flush=True)
    assert page.locator('.projection-qr svg').count()==1
    ctx.close()
   browser.close()
 finally:server.shutdown()
if __name__=='__main__':main()
