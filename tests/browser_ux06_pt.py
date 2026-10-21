from functools import partial
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit
import threading,json,re,os
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler,new_page,ROOT
PLANS=json.loads((ROOT/'docs/pedagogia/percursos-unidades-20261020.json').read_text('utf-8'))
OUT=ROOT.parents[1]/'outputs/design-pt'

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
     ctx,page=new_page(browser,width);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
     def local(route):
      u=urlsplit(route.request.url);response=route.fetch(url=host+u.path+('?' +u.query if u.query else ''));route.fulfill(response=response)
     page.route('https://pedrohfernandes-klk.github.io/pt/**',local)
     page.route('https://pedrohfernandes-klk.github.io/lente/**',lambda r:r.abort())
     first,second=plan['units'][0]['lessons'][:2]
     if width==320:
      page.goto(host+'/pt/',wait_until='networkidle');page.locator(f'a[href="m{m}/"],a[href$="/m{m}/"]').first.click();page.wait_for_url(f'**/pt/m{m}/')
     else:page.goto(host+f'/pt/m{m}/',wait_until='networkidle')
     assert page.locator('nav.migalhas').bounding_box()['height']<=64
     action=page.locator('[data-module-next]');assert action.is_visible();assert 'Começar:' in action.inner_text()
     assert action.bounding_box()['y']<600,(m,width,action.bounding_box())
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
     assert page.locator('.module-context figure.doc').count()==1 and page.locator('.module-progress .passaporte').count()==1
     assert not page.locator('figure.doc').is_visible()
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
      page.locator('.module-context summary').focus();page.locator('.module-context summary').press('Enter');assert page.locator('figure.doc').is_visible()
      page.locator('.module-context summary').press('Enter');assert not page.locator('figure.doc').is_visible()
      page.locator('[data-module-next]').focus();assert page.locator('[data-module-next]').evaluate('e=>getComputedStyle(e).outlineStyle')!='none'
      page.evaluate('document.documentElement.style.fontSize="200%"');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),('root zoom',m,page.evaluate('({scroll:document.documentElement.scrollWidth,client:innerWidth,x:scrollX,large:[...document.querySelectorAll("body *")].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>({cl:e.className,scroll:e.scrollWidth,client:e.clientWidth})).slice(0,15)})'),page.locator('body *').evaluate_all('(els)=>els.filter(e=>e.getBoundingClientRect().right>innerWidth+2).map(e=>({tag:e.tagName,cl:e.className,w:e.getBoundingClientRect().width,text:(e.innerText||"").slice(0,80)})).slice(0,12)'))
     assert not errors,(m,width,errors)
     results.append({'module':m,'width':width,'path_clicks':width==320,'overflow':False,'javascript_errors':errors});print('PASS UX-06 module',m,'width',width,flush=True)
     ctx.close()
   # Retoma uses existing completion criteria, including extra activities.
   ctx,page=new_page(browser,320);page.goto(host+'/pt/m1/',wait_until='networkidle')
   page.evaluate("localStorage.setItem('licao-m1-f01',JSON.stringify({lida:true}));localStorage.setItem('licao-m1-f01-a1',JSON.stringify({lida:true}));localStorage.setItem('epi-pt-olhar-ajuda',JSON.stringify({fim:true}))")
   page.reload(wait_until='networkidle');assert 'Continuar: Cercada pelas ondas' in page.locator('[data-module-next]').inner_text()
   page.evaluate("localStorage.removeItem('licao-m1-f01-a1')");page.reload(wait_until='networkidle');assert 'Retomar:' in page.locator('[data-module-next]').inner_text()
   # Full first unit: go to the pending checkpoint, then to the synthesis.
   plan=PLANS[0];source=(ROOT/'m1/index.html').read_text('utf-8');match=re.search(r'\bU\s*=\s*(\[)',source);units=json.JSONDecoder().raw_decode(source[match.start(1):])[0]
   page.evaluate('''steps=>{for(const p of steps){if(p.licao){localStorage.setItem('licao-'+p.licao,JSON.stringify({lida:true}));localStorage.setItem('licao-'+p.licao+'-a1',JSON.stringify({lida:true}));}for(const id of [...p.exs,...(p.ativ||[]).filter(a=>a!=='ler')])localStorage.setItem('epi-pt-'+id,JSON.stringify({fim:true}));}}''',units[0]['passos'])
   page.reload(wait_until='networkidle');assert page.locator('[data-module-next]').get_attribute('href')=='#desafio-unidade-1'
   page.evaluate("localStorage.setItem('desafio-unidade-v2-M1-u1',JSON.stringify({ganho:true,melhor:8,total:8}))")
   page.reload(wait_until='networkidle');assert page.locator('[data-module-next]').get_attribute('href')=='#sintese-unidade-1';page.locator('[data-module-next]').click();assert page.locator('[data-fim="1"]').evaluate('e=>e.open')
   print('PASS resume, outstanding checkpoint and synthesis reveal',flush=True);ctx.close();browser.close()
 finally:server.shutdown()
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'validacao-ux06.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
