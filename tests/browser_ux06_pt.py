# 31/10/2026: M3, M5 e M6 passam ao contrato das aulas de tarefa.
from functools import partial
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit
import threading,json,re,os
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
PLANS=json.loads((ROOT/'docs/pedagogia/percursos-unidades-20261020.json').read_text('utf-8'))
OUT=ROOT.parents[1]/'outputs/design-pt'
# 24/10/2026 (aulas claras do M1, como o M4 a 23/10): o percurso do M1 passa a lista simples de aulas, sem passaporte
# 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 passa ao mesmo modelo, com duas aulas de tarefa.
# 01/11/2026: M8/M9 também têm aula de tarefa; os limites visuais não mudam.
SEM_PASSAPORTE={1,2,3,4,5,6,7,8,9}

def main():
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
 threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}';results=[]
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(headless=True)
   for width in (320,1280):
    for plan in PLANS:
     m=plan['module'];
     if os.environ.get('UX_MODULE') and str(m)!=os.environ['UX_MODULE']:continue
     ctx,page=new_page(browser,width);
     # 01/11/2026: ação inteira no primeiro ecrã real de 320 × 568.
     if width==320:page.set_viewport_size({'width':320,'height':568})
     errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
     def local(route):
      # 01/11/2026: mesmos ficheiros locais sem uma segunda ligação HTTP (Windows).
      from urllib.parse import unquote
      import mimetypes
      asset=(ROOT/unquote(urlsplit(route.request.url).path.removeprefix('/pt/'))).resolve()
      if not asset.is_relative_to(ROOT.resolve()):
       route.fulfill(status=403,body='Forbidden');return
      if asset.is_dir():asset=asset/'index.html'
      if asset.is_file():route.fulfill(path=str(asset),content_type=mimetypes.guess_type(str(asset))[0] or 'application/octet-stream')
      else:route.fulfill(status=404,body='Not found')
     page.route('https://pedrohfernandes-klk.github.io/pt/**',local)
     page.route('https://pedrohfernandes-klk.github.io/lente/**',lambda r:r.abort())
     first,second=plan['units'][0]['lessons'][:2]
     if width==320:
      page.goto(host+'/pt/',wait_until='networkidle');page.locator(f'a[href="m{m}/"],a[href$="/m{m}/"]').first.click();page.wait_for_url(f'**/pt/m{m}/')
     else:page.goto(host+f'/pt/m{m}/',wait_until='networkidle')
     assert page.locator('nav.migalhas').bounding_box()['height']<=64
     action=page.locator('[data-module-next]');assert action.is_visible()
     assert action.get_attribute('href').endswith('/licao-'+first+'/')
     assert any(label in action.inner_text() for label in (('Começar:','Continuar:') if m in SEM_PASSAPORTE else ('Começar:',)))
     assert action.bounding_box()['y']<600,(m,width,action.bounding_box())
     if width==320:assert action.bounding_box()['y']+action.bounding_box()['height']<=568,(m,action.bounding_box())
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
     # 23/10/2026 (decisão do docente, aulas claras): o M4 é o piloto do percurso como lista simples de aulas, sem passaporte, níveis nem pontos
     # 03/11/2026: a imagem documental do piloto M4 abre nos recursos, pelo teclado (06/11/2026: deixou de valer com a decisão 148).
     # 06/11/2026: decisão 148, volta a exigir-se o mesmo nos nove: uma imagem documental, à vista sem abrir nada, fora de
     # qualquer details, logo a seguir à última unidade (já não há exceção para o M4).
     assert page.locator('main > figure.doc').count()==1 and page.locator('figure.doc').count()==1 and page.locator('.module-progress .passaporte').count()==(0 if m in SEM_PASSAPORTE else 1)
     assert page.evaluate('()=>{const f=document.querySelector("main > figure.doc"),u=[...document.querySelectorAll("main > section.unidade-pedagogica")].pop();return f.previousElementSibling===u&&!f.closest("details")}')
     assert page.locator('figure.doc').is_visible()
     # 06/11/2026: decisão 148, sai o passo que voltava a fechar os recursos do M4 (a imagem já não está lá dentro).
     if m in (1,2):
      OUT.mkdir(parents=True,exist_ok=True);page.screenshot(path=str(OUT/f'm{m}-{width}-depois.png'))
      page.locator('.unidade-pedagogica').first.screenshot(path=str(OUT/f'm{m}-unidade-{width}-depois.png'))
     if width==320:
      # Actual clicks: home -> module -> lesson -> next lesson -> curricular unit.
      action.click();page.wait_for_url(f'**/licao-{first}/');page.locator('#baralho .cartao').wait_for()
      page.locator('[data-c-menu]').first.click();page.locator(f'[data-c-painel] a[href$="/licao-{second}/"]').first.click();page.wait_for_url(f'**/licao-{second}/')
      page.locator('.c-marca').first.click();page.wait_for_url(f'**/m{m}/#unidade-pedagogica-1');assert page.locator('#unidade-pedagogica-1').is_visible()
      # Map counts must describe this same route.
      page.goto(host+f'/pt/m{m}/mapa-do-modulo-m{m}/',wait_until='networkidle');counts=page.locator('.numeros b').all_text_contents()
      assert int(counts[0])==len(plan['units']) and int(counts[2])==len(plan['units'])
      assert int(counts[1])==sum(len(u['lessons']) for u in plan['units'])
      # Same interaction hierarchy in dark mode and enlarged root text.
      page.goto(host+f'/pt/m{m}/',wait_until='networkidle');page.emulate_media(color_scheme='dark')
      if m not in SEM_PASSAPORTE:
       page.locator('.module-progress summary').focus();page.locator('.module-progress summary').press('Enter');assert page.locator('.passaporte').is_visible()
       page.locator('.module-progress summary').press('Enter');assert not page.locator('.passaporte').is_visible()
      page.locator('[data-module-next]').focus();assert page.locator('[data-module-next]').evaluate('e=>getComputedStyle(e).outlineStyle')!='none'
      page.evaluate('document.documentElement.style.fontSize="200%"');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('root zoom',m,page.evaluate('({scroll:document.documentElement.scrollWidth,client:innerWidth,x:scrollX,large:[...document.querySelectorAll("body *")].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>({cl:e.className,scroll:e.scrollWidth,client:e.clientWidth})).slice(0,15)})'),page.locator('body *').evaluate_all('(els)=>els.filter(e=>e.getBoundingClientRect().right>innerWidth+2).map(e=>({tag:e.tagName,cl:e.className,w:e.getBoundingClientRect().width,text:(e.innerText||"").slice(0,80)})).slice(0,12)'))
     assert not errors,(m,width,errors)
     results.append({'module':m,'width':width,'path_clicks':width==320,'overflow':False,'javascript_errors':errors});print('PASS UX-06 module',m,'width',width,flush=True)
     ctx.close()
   # Retoma uses existing completion criteria, including extra activities.
   ctx,page=new_page(browser,320);page.goto(host+'/pt/m1/',wait_until='networkidle')
   page.evaluate("localStorage.setItem('licao-m1-f01',JSON.stringify({lida:true}));localStorage.setItem('licao-m1-f01-a1',JSON.stringify({lida:true}));localStorage.setItem('epi-pt-olhar-ajuda',JSON.stringify({fim:true}))")
   page.reload(wait_until='networkidle');assert 'Continuar: Cercada pelas ondas' in page.locator('[data-module-next]').inner_text()
   # 24/10/2026 (aulas claras do M1): uma aula está feita ou por fazer; feita = a lição acabada. Tirar a atividade -a1 já não
   # deixa a aula 1 «começada» (deixa de haver «Retomar:»), e o botão continua na aula 2.
   page.evaluate("localStorage.removeItem('licao-m1-f01-a1')");page.reload(wait_until='networkidle');assert 'Continuar: Cercada pelas ondas' in page.locator('[data-module-next]').inner_text()
   # 26/10: finishing reading opens no extra gate. Remaining lessons stay navigable;
   # the task is its own classroom row and no archive score assesses it.
   plan=PLANS[0];source=(ROOT/'m1/index.html').read_text('utf-8');match=re.search(r'\bU\s*=\s*(\[)',source);units=json.JSONDecoder().raw_decode(source[match.start(1):])[0]
   page.evaluate("""steps=>{for(const p of steps){if(p.licao){localStorage.setItem('licao-'+p.licao,JSON.stringify({lida:true}));localStorage.setItem('licao-'+p.licao+'-a1',JSON.stringify({lida:true}));}for(const id of [...p.exs,...(p.ativ||[]).filter(a=>a!=='ler')])localStorage.setItem('epi-pt-'+id,JSON.stringify({fim:true}));}}""",units[0]['passos'])
   page.reload(wait_until='networkidle')
   expected='./licao-'+plan['units'][1]['lessons'][0]+'/'
   assert page.locator('[data-module-next]').get_attribute('href')==expected
   page.evaluate("localStorage.setItem('desafio-unidade-v2-M1-u1',JSON.stringify({ganho:true,melhor:8,total:8}))")
   page.reload(wait_until='networkidle')
   assert page.locator('[data-module-next]').get_attribute('href')==expected
   assert page.locator('[data-sintese], #cartao, #copiar-cartao').count()==0
   assert page.locator('button[data-desafio]:visible').count()==0
   task=page.locator('[data-task-lesson="1"] > a')
   # 01/11/2026: a unidade já lida fica dobrada; reabre-se pelo teclado para a tarefa.
   from browser_task_contract import open_route_unit
   open_route_unit(page, 1)
   task.focus();task.press('Enter');page.wait_for_url('**/tarefas/m1-u1/')
   # 30/10/2026 (decisão do docente de 29/10): o aquecimento em papel passou a cartões numa página própria; na tarefa
   # fica só a pergunta opcional.
   assert page.locator('[data-task-question]').count()==1
   # 28/10/2026 (decisão do docente, PR #122): a tarefa do M1 passa ao formato com escolha, com um cartão de
   # aquecimento antes do enunciado (aquecer, enunciado, relembrar, verificar).
   assert page.locator('main[data-task-choice]').count()==1
   # 13/11/2026: a m1-u1 passou ao molde «mais fácil de fazer» (camada tarefas_faceis_m1_20261113): seis cartões em vez de
   # quatro, e a página traz a marca do molde novo. As outras exigências ficam como estavam.
   assert page.locator('main[data-task-facil]').count()==1
   assert page.locator('[data-task-card]').count()==6
   assert not page.locator('[data-task-optional-preparation]').evaluate('e=>e.open')
   assert not page.evaluate('localStorage.getItem("percurso-sintese-M1-u1")')
   print('PASS resume, navigable task lesson, no independent gate or automatic assessment',flush=True);ctx.close();browser.close()
 finally:server.shutdown()
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'validacao-ux06.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
