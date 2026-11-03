"""02/11/2026: impressão sem soluções, miniaturas/visor e medidas de projeção."""
import copy,json
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_tipos_mais import CARDS,pagina,router,escolher,ROOT

def main():
 with sync_playwright() as p:
  b=p.chromium.launch()
  for c in CARDS:
   page=b.new_page(viewport={'width':390,'height':900});page.route('**/*',router(c))
   page.goto('https://f2.test/ensaio/')
   assert page.locator('.tm-impressao').is_hidden()
   # 02/11/2026: compara a impressão inicial e final no mesmo meio visual.
   page.emulate_media(media='print');initial=page.locator('.tm-impressao').inner_text()
   page.emulate_media(media='screen')
   escolher(page,c)
   page.emulate_media(media='print')
   assert page.locator('.tm-impressao').is_visible()
   assert page.locator('.tm-impressao').inner_text()==initial
   assert page.locator('.f-rev').is_hidden()
   assert page.locator('.tm-impressao input,.tm-impressao button').count()==0
   print('PASS impressão inicial',c['t'],flush=True);page.close()
  for width,minimum in [(320,136),(390,170)]:
   c=copy.deepcopy(next(c for c in CARDS if c['t']=='intruso'))
   c['itens']=[{'img':'/ensaio-imagem.svg','alt':'Forma '+str(i+1),'autor':'Ensaio técnico','obra':'Retângulo','data':'2026','origem':'https://example.test/ensaio','licenca':'CC0'} for i in range(4)]
   page=b.new_page(viewport={'width':width,'height':900})
   def route(r):
    if r.request.url.endswith('/ensaio-imagem.svg'):r.fulfill(body='<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600"><rect x="100" y="100" width="700" height="400" fill="black"/></svg>',content_type='image/svg+xml')
    elif '/ensaio/' in r.request.url:r.fulfill(body=pagina(c).replace('</head>','<link rel="stylesheet" href="/assets/ampliar-documentos.css"><script src="/assets/ampliar-documentos.js"></script></head>'),content_type='text/html; charset=utf-8')
    else:router(c)(r)
   page.route('**/*',route);page.goto('https://f2.test/ensaio/')
   for im in page.locator('.tm-imagem img').all():assert im.bounding_box()['width']>=minimum,(width,im.bounding_box())
   for el in page.locator('.casca-topo,.casca-corpo,.q').all():
    bb=el.bounding_box();assert bb['x']>=-1 and bb['x']+bb['width']<=width+1,(width,bb)
   button=page.locator('[data-ampliar="0"]');button.focus();page.keyboard.press('Enter')
   page.locator('.amp-ov').wait_for();page.get_by_role('button',name='Ampliar',exact=True).click()
   assert page.locator('.amp-tools output').inner_text()=='150 %'
   page.keyboard.press('Escape');assert page.locator('.amp-ov').count()==0;assert button.evaluate('(e)=>document.activeElement===e')
   page.emulate_media(media='print')
   assert page.locator('.tm-impressao img').count()==4
   assert all(im.is_visible() for im in page.locator('.tm-impressao img').all())
   assert 'CC0' in page.locator('.tm-impressao').inner_text()
   print('PASS imagem/visor/impressão',width,flush=True);page.close()
  c=copy.deepcopy(CARDS[0]);c['texto']=' '.join(['chuva']*70)+' [1] [2]'
  page=b.new_page(viewport={'width':1366,'height':768});page.route('**/*',router(c));page.goto('https://f2.test/ensaio/?projetar=1')
  for el in page.locator('.q,.tm-texto,.tm-banco').all():
   bb=el.bounding_box();assert bb['y']>=0 and bb['y']+bb['height']<=768,(bb,el.inner_text())
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
  print('PASS projeção texto de 70 palavras',flush=True);page.close()
  c=copy.deepcopy(CARDS[2]);c['aceita']=[[[3,0,1,2],'Ontem, não o vi.']]
  page=b.new_page();page.route('**/*',router(c));page.goto('https://f2.test/ensaio/?projetar=1');page.keyboard.press('r')
  assert 'Também certo: Ontem, não o vi.' in page.locator('.tm-montar').inner_text()
  print('PASS ordem aceite com pontuação própria',flush=True);page.close()
  c=copy.deepcopy(CARDS[0]);page=b.new_page(viewport={'width':320,'height':240});page.route('**/*',router(c));page.goto('https://f2.test/ensaio/')
  page.locator('[data-espaco="0"]').click()
  assert page.locator('.tm-banco').evaluate('(e)=>e.style.position')=='static'
  assert page.locator('.tm-banco').evaluate('(e)=>e.parentElement.classList.contains("tm-texto")')
  page.keyboard.press('Escape');assert page.locator('[data-espaco="0"]').evaluate('(e)=>e===document.activeElement')
  print('PASS banco em ecrã baixo e Escape',flush=True);page.close()
  # 03/11/2026: o motor já apresenta cita; o tipo não a pode duplicar.
  c=copy.deepcopy(CARDS[2]);c.pop('apoio');c['cita']='Passagem de ensaio para verificar a apresentação.'
  page=b.new_page();page.route('**/*',router(c));page.goto('https://f2.test/ensaio/')
  assert page.locator('.cartao').inner_text().count(c['cita'])==1
  page.emulate_media(media='print')
  assert page.locator('.cartao').inner_text().count(c['cita'])==1
  print('PASS citação única no ecrã e na impressão',flush=True);page.close();b.close()
if __name__=='__main__':main()
