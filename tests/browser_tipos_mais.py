"""02/11/2026: seis peças reais, com gestos certos/errados e revisão no motor."""
from pathlib import Path
import json,mimetypes,re
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
CARDS=json.loads((ROOT/'tests/fixtures/tipos-mais-ensaio.json').read_text('utf8'))

def pagina(c):
 return '''<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <link rel="stylesheet" href="/assets/pt-lessons/lesson.css"><link rel="stylesheet" href="/assets/pt-lessons/tipos-mais.css?v=20261102-f2">
 <script src="/assets/pt-lessons/casca.js"></script><script src="/assets/pt-lessons/jogo.js"></script><script src="/assets/pt-lessons/tipos-mais.js?v=20261102-f2"></script></head><body><script>
 window.CARTOES='''+json.dumps([c],ensure_ascii=False)+''';window.antes=JSON.stringify(CARTOES);
 window.C=EPICasca.abrir({marca:'Ensaio F2',semVoltar:true});EPIJogo.montar({casca:C,itens:CARTOES,chave:'ensaio-f2',variar:false,pistas:['Relê a relação entre as ideias.']});</script></body></html>'''

def router(c):
 def route(r):
  path=urlsplit(r.request.url).path
  if path=='/ensaio/':r.fulfill(body=pagina(c),content_type='text/html; charset=utf-8');return
  f=(ROOT/path.lstrip('/')).resolve()
  if f.is_relative_to(ROOT) and f.is_file():r.fulfill(path=str(f),content_type=mimetypes.guess_type(f)[0] or 'application/octet-stream')
  else:r.fulfill(status=404,body='missing')
 return route

def escolher(page,c,wrong=False,keyboard=False):
 def click(sel):
  el=page.locator(sel)
  if keyboard:el.focus();page.keyboard.press('Space' if el.get_attribute('type') in ('checkbox','radio') else 'Enter')
  else:el.click()
 t=c['t']
 if t=='varias':
  for i in ([1] if wrong else c['certas']):click(f'[data-op="{i}"]')
 elif t in ('intruso','razao'):
  item,reason=c['certos'][0]
  click(f'[name="i-{c["id"]}"][value="{item}"]')
  click(f'[name="r-{c["id"]}"][value="{(reason+1)%len(c["razoes"]) if wrong else reason}"]')
 elif t=='lacunas':
  for i in range(len(c['espacos'])):
   click(f'[data-bloco="{len(c["espacos"]) if wrong and i==0 else i}"]')
   click(f'[data-espaco="{i}"]')
 elif t=='montar':
  for i in ([1,0,2,3] if wrong else range(len(c['blocos']))):click(f'[data-monta="{i}"]')
 elif t=='corrigir':
  for e in c['erros']:click(f'[data-palavra="{e["em"]}"]')
  assert page.locator('.tm-trocas').is_hidden()
  click('[data-confirmar]');assert page.locator('[data-c-folha]').is_hidden()
  for e in c['erros']:click(f'[name="c-{c["id"]}-{e["em"]}"][value="{(e["c"]+1)%3 if wrong else e["c"]}"]')
 click('[data-confirmar]')

def main():
 count=0
 with sync_playwright() as p:
  b=p.chromium.launch()
  for width,scheme in [(320,'light'),(390,'dark'),(1024,'light'),(1366,'dark')]:
   for c in CARDS:
    for mode in ('correct','wrong','projection'):
     ctx=b.new_context(viewport={'width':width,'height':768},color_scheme=scheme,reduced_motion='no-preference')
     page=ctx.new_page();page.route('**/*',router(c));errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
     page.goto('https://f2.test/ensaio/'+('?projetar=1' if mode=='projection' else ''))
     page.locator('[data-confirmar]').wait_for()
     assert page.locator('[data-confirmar]').is_disabled()
     initial=page.locator('[data-tipo-ext]').inner_text()
     # 03/11/2026: o apoio criado aparece uma vez, sem passar pelo cabeçalho de citação.
     if 'apoio' in c:
      assert initial.count(c['apoio'])==1
      assert page.locator('.cartao > .cita').count()==0
     assert page.locator('[data-tipo-ext]').evaluate('(e)=>e.getAnimations({subtree:true}).length')==0
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(c['t'],width)
     if c['t']=='lacunas' and width==320:assert page.locator('.tm-banco').bounding_box()['height']<=150
     before=page.evaluate('JSON.stringify(localStorage)')
     if mode=='projection':
      page.keyboard.press('r')
      assert page.locator('[data-c-folha] .c-veredito').inner_text()=='✓\nResposta'
      assert page.evaluate('JSON.stringify(localStorage)')==before
     else:
      escolher(page,c,mode=='wrong',width==390)
      verdict=page.locator('[data-c-folha]').inner_text()
      match=re.search(r'Acertaste (\d+) de (\d+)',verdict);assert match,(c['t'],verdict)
      if mode=='correct':assert match[1]==match[2],(c['t'],verdict)
      else:assert match[1]!=match[2],(c['t'],verdict)
     assert page.evaluate('JSON.stringify(CARTOES)===antes')
     assert page.locator('[data-tipo-ext] input:enabled,[data-tipo-ext] button:enabled').count()==0
     page.locator('[data-c-folha] [data-seguinte]').click()
     if mode=='wrong':
      page.locator('[data-errados]').click()
      assert page.locator('[data-tipo-ext]').inner_text()!=initial,(c['t'],'variante igual')
      assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
     else:
      # 02/11/2026: num ensaio de um cartão, a revisão abre pelo resultado.
      page.locator('[data-rever]').click()
      assert page.locator('[data-tipo-ext] input:enabled,[data-tipo-ext] button:enabled').count()==0
     assert not errors,errors
     count+=1;ctx.close()
     print('PASS',count,c['t'],width,mode,flush=True)
  b.close()
 print('PASS',count,'casos F2')
if __name__=='__main__':main()
