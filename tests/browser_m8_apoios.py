"""M8 (27/10/2026): os três cartões com apoio novo, no motor real das lições.

F09 cartão 7 (emparelhar) e F08 cartão 14 (escolha) passam a mostrar o texto de que dependem;
F09 cartão 18 (frase) deixa de falar de uma «lista final» que o aluno não vê. Confere-se: o apoio
aparece por cima da pergunta, uma só vez entre aspas, sem transbordo de 320 a 1440 px, nos dois
temas, no fim do cartão e na projeção em três tamanhos.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import sys,threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards

CASOS=[('m8/licao-m8-f09',6,'Uma mulher encontra uma chave'),('m8/licao-m8-f08',13,'No verso da carta, uma data: 1979'),('m8/licao-m8-f09',17,None)]

def mount(page,card):
 page.evaluate('''card=>{
  document.querySelectorAll('.casca').forEach(e=>e.remove());
  EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Fim do apoio.</p>'}],chave:'qa-apoio-m8',variar:false});
  document.querySelector('.jogo-alvo').id='baralho';
 }''',card)

def check(scope,apoio):
 if apoio:
  cita=scope.locator('#baralho .cartao .cita')
  assert cita.count()==1 and cita.is_visible()
  texto=cita.text_content()
  assert apoio in texto,texto
  assert texto.count('«')==1 and texto.count('»')==1,texto
  q=scope.locator('#baralho .cartao .q')
  assert cita.evaluate('e=>e.getBoundingClientRect().bottom')<=q.evaluate('e=>e.getBoundingClientRect().top')+1
  assert cita.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')>=15
 else:
  assert scope.locator('#baralho .cartao .cita').count()==0
  assert 'lista final' not in scope.locator('#baralho .cartao .q').text_content()
 assert not scope.locator('html').evaluate('e=>e.scrollWidth>innerWidth+3')

def main():
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(headless=True)
   for pasta,i,apoio in CASOS:
    card=lesson_cards(ROOT/pasta/'index.html')[i]
    for width in (320,390,900,1440):
     for scheme in ('light','dark'):
      ctx=browser.new_context(viewport={'width':width,'height':900},color_scheme=scheme,reduced_motion='reduce')
      page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
      page.route('**/fonts.googleapis.com/**',lambda r:r.abort());page.route('**/fonts.gstatic.com/**',lambda r:r.abort())
      page.goto(host+'/'+pasta+'/',wait_until='networkidle');mount(page,card)
      check(page,apoio)
      assert not errors,(pasta,i,width,scheme,errors)
      ctx.close()
    print('PASS',pasta,'cartão',i+1,'320 a 1440 px, claro e escuro',flush=True)
    ctx=browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
    page=ctx.new_page()
    page.route('**/fonts.googleapis.com/**',lambda r:r.abort());page.route('**/fonts.gstatic.com/**',lambda r:r.abort())
    def local(route):
     response=route.fetch(url=host+route.request.url.split(host+'/pt',1)[1]);route.fulfill(response=response)
    page.route(host+'/pt/**',local)
    page.goto(host+'/pt/projetar/?pagina=%2Fpt%2F'+pasta.replace('/','%2F')+'%2F',wait_until='networkidle')
    frame=page.frame_locator('#lesson-frame');frame.locator('#baralho .cartao').wait_for()
    child=next(f for f in page.frames if '/'+pasta+'/' in f.url)
    mount(child,card)
    for size in ('small','medium','large'):
     page.locator(f'[data-projection-size="{size}"]').click()
     check(frame,apoio)
    print('PASS',pasta,'cartão',i+1,'projeção em três tamanhos',flush=True)
    ctx.close()
   browser.close()
 finally:server.shutdown()
if __name__=='__main__':main()
