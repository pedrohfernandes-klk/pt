"""Open access, useful searches, investigation navigation and preserved game state."""
from functools import partial
from http.server import ThreadingHTTPServer
import json,threading,re
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page

source=(ROOT/'atlas/index.html').read_text('utf8')
base_figures=json.JSONDecoder().raw_decode(source.split('window.ATLAS_DADOS=',1)[1])[0]['FIG']
editorial=json.JSONDecoder().raw_decode((ROOT/'assets/atlas-editorial.js').read_text('utf8').split('window.ATLAS_EDITORIAL=',1)[1])[0]
figures=base_figures+editorial['autores']
assert len(base_figures)==107 and len(figures)==110
assert set(editorial['propostas'])=={f['id'] for f in base_figures if not f.get('paraTi')},'New proposals must close the exact gap without replacing existing ones'
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/pt'

def no_overflow(page):
 assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+3')
 assert not page.locator('.folha-c').evaluate_all('(els)=>els.some(el=>el.scrollWidth>el.clientWidth+3)')

try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in (320,1440):
   ctx,page=new_page(browser,width);errors=[]
   page.on('pageerror',lambda error:errors.append(str(error)))
   page.goto(host+'/atlas/',wait_until='networkidle')
   assert page.locator('[data-atlas-resultados]').inner_text()==f'{len(figures)} pessoas encontradas'
   assert page.locator('#atlas-memoria').get_attribute('open') is None
   assert '107 pessoas' in page.locator('#atlas-memoria').text_content()
   assert page.locator('#pessoas-PT li').count()==26
   state=page.evaluate('localStorage.getItem("epi-atlas")')
   search=page.locator('[data-atlas-pesquisa]')
   search.fill('escrevivencia')
   assert page.locator('[data-atlas-resultados]').inner_text()=='1 pessoa encontrada'
   assert page.locator('#pessoas-pais li:visible').count()==1
   assert 'Conceição Evaristo' in page.locator('#pessoas-pais li:visible').inner_text()
   search.fill('nome-sem-correspondencia')
   assert page.locator('#pessoas-pais li:visible').count()==0
   page.locator('[data-atlas-limpar]').click()
   assert page.locator('[data-atlas-resultados]').inner_text()==f'{len(figures)} pessoas encontradas'
   page.locator('[data-atlas-area]').select_option('arquitetura')
   assert page.locator('[data-atlas-resultados]').inner_text()=='1 pessoa encontrada'
   assert 'Siza' in page.locator('#pessoas-pais li:visible').inner_text()
   page.locator('[data-atlas-limpar]').click()
   # Every profile must open in a fresh visitor's session, without a quiz answer.
   for f in figures:
    group=page.locator('#pessoas-'+f['pais'])
    if group.get_attribute('open') is None:group.locator('summary').click()
    page.locator('#pessoas-pais a[href="#figura-'+f['id']+'"]').click()
    dialog=page.get_by_role('dialog')
    assert dialog.locator('h3').inner_text()==f['nome']
    assert dialog.locator('h4').filter(has_text='Uma ideia para experimentar').count()==1
    expected=editorial['propostas'].get(f['id'],f.get('paraTi'))
    assert expected and re.sub(r'_([^_]+)_',lambda m: m.group(1),expected) in dialog.inner_text()
    assert 'Ainda não conheces esta pessoa' not in dialog.inner_text()
    assert dialog.locator('h4').filter(has_text='Um momento do percurso').count()==1
    dialog.locator('.atlas-fontes-perfil summary').click()
    assert dialog.locator('.fontes li').count()==len(f['fontes'])
    if f['obra'].get('liga'):
     assert dialog.locator('a[href="'+f['obra']['liga']+'"]').count()>=1
    no_overflow(page)
    page.locator('.folha-c .fechar').press('Escape')
    assert not page.locator('#folha').is_visible()
   assert page.evaluate('localStorage.getItem("epi-atlas")')==state,'Reading must not manufacture game progress'
   for key in ('imagem','vozes','voz-poema'):
    page.locator('#atlas-investigar [data-atlas-investigar="'+key+'"]').click()
    choices=page.locator('#folha [data-atlas-lente]')
    first=page.locator('#atlas-pista').inner_text()
    choices.nth(1).click()
    assert choices.nth(1).get_attribute('aria-pressed')=='true'
    assert page.locator('#atlas-pista').inner_text()!=first
    page.locator('#folha .atlas-rever summary').press('Enter')
    assert page.locator('#folha .atlas-rever').get_attribute('open') is not None
    page.locator('#folha [data-atlas-pessoa]').first.click()
    assert page.get_by_role('dialog').locator('.atlas-fontes-perfil').count()==1
    page.locator('[data-atlas-regresso]').click()
    assert page.locator('#folha [data-atlas-lente="1"]').get_attribute('aria-pressed')=='true'
    no_overflow(page)
    page.locator('.folha-c .fechar').press('Escape')
   # A hash link from any lesson opens a profile directly after reload.
   page.goto(host+'/atlas/#figura-angelo-de-lima',wait_until='networkidle')
   assert page.get_by_role('dialog').locator('h3').inner_text()=='Ângelo de Lima'
   page.locator('.folha-c .fechar').press('Escape')
   for f in editorial['autores']:
    page.goto(host+'/atlas/#figura-'+f['id'],wait_until='networkidle')
    assert page.get_by_role('dialog').locator('h3').inner_text()==f['nome']
    page.locator('.folha-c .fechar').press('Escape')
   page.locator('#atlas-memoria>summary').click()
   page.locator('#desafio [data-comecar]').click()
   assert page.locator('.casca.sobreposta').is_visible(),'Legacy game remains available'
   page.get_by_role('button',name='Fechar',exact=True).click()
   assert not errors,errors
   print(f'PASS Atlas: 110 unlocked profiles and individual proposals, search, investigations, sources, reload and optional game {width}',flush=True)
   ctx.close()
  ctx,page=new_page(browser,1440)
  page.goto(host+'/projetar/?pagina=/pt/atlas/',wait_until='networkidle')
  frame=page.frame_locator('#lesson-frame')
  page.locator('[data-projection-size="large"]').click()
  frame.locator('#atlas-investigar [data-atlas-investigar="imagem"]').click()
  assert frame.get_by_role('dialog').is_visible()
  assert frame.locator('html').get_attribute('data-projection-size')=='large'
  assert not frame.locator('html').evaluate('(el)=>el.scrollWidth>innerWidth+3')
  assert not frame.locator('.folha-c').evaluate('(el)=>el.scrollWidth>el.clientWidth+3')
  ctx.close();print('PASS Atlas large projection and investigation',flush=True)
  # Preserve an established game record while opening an unearned profile.
  ctx,page=new_page(browser,1440)
  page.goto(host+'/atlas/',wait_until='networkidle')
  saved=page.evaluate('localStorage.getItem("epi-atlas")')
  if saved:
   old=json.loads(saved);old['dom']={'PT':123456789};old['erros']={'angelo-de-lima':2}
   page.evaluate('(s)=>localStorage.setItem("epi-atlas",s)',json.dumps(old))
   page.reload(wait_until='networkidle')
   before=page.evaluate('localStorage.getItem("epi-atlas")')
   page.goto(host+'/atlas/#figura-paulina-chiziane',wait_until='networkidle')
   assert page.get_by_role('dialog').locator('h3').inner_text()=='Paulina Chiziane'
   assert page.evaluate('localStorage.getItem("epi-atlas")')==before
  for f in figures:
   for kind in ('ponte','comparar'):
    link=f.get(kind)
    if not link:continue
    path=urlsplit(link['url']).path
    if path.startswith('/pt/'):
     target=ROOT/path[4:]
     if target.is_dir():target=target/'index.html'
     assert target.is_file(),link['url']
  ctx.close();browser.close()
finally:server.shutdown()
