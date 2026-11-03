"""03/11/2026: sequência de tipos e erro de identificação sem erro de correção."""
import json
from playwright.sync_api import sync_playwright, expect
from browser_tipos_mais import CARDS,pagina,router,escolher

def main():
 with sync_playwright() as p:
  b=p.chromium.launch()
  page=b.new_page(viewport={'width':390,'height':900})
  def route(r):
   if '/ensaio/' in r.request.url:
    html=pagina(CARDS[0]).replace(json.dumps([CARDS[0]],ensure_ascii=False),json.dumps(CARDS,ensure_ascii=False))
    # 03/11/2026: a sequência usa o modo aula, que conserva a ordem do núcleo.
    html=html.replace('variar:false','variar:false,aula:true')
    r.fulfill(body=html,content_type='text/html; charset=utf-8')
   else:router(CARDS[0])(r)
  page.route('**/*',route);page.goto('https://f2.test/ensaio/')
  page.evaluate('window.confirmacoes=0;document.addEventListener("click",e=>{if(e.target.closest("[data-confirmar]"))confirmacoes++},true)')
  for c in CARDS:
   assert page.locator('.q').inner_text()==c['p']
   escolher(page,c,keyboard=True)
   page.locator('[data-c-folha] [data-seguinte]').click()
  # 03/11/2026: esperar pela animação real do total, mantendo o valor exato.
  expect(page.locator('.cartao.fim .grande')).to_have_text('6 de 6')
  assert page.evaluate('confirmacoes')==7
  print('PASS seis tipos em sequência, sete confirmações exatas',flush=True);page.close()
  c=CARDS[-1];page=b.new_page(viewport={'width':390,'height':900});page.route('**/*',router(c));page.goto('https://f2.test/ensaio/')
  # 03/11/2026: F2-02, concordância exata em 0/1/2 seleções, sem mudar a confirmação.
  for index,count in ((0,1),(2,2),(2,1),(0,0)):
   page.locator(f'[data-palavra="{index}"]').click()
   message=f'Marcaste {count} '+('palavra.' if count==1 else 'palavras.')
   assert page.locator('.tm-conta').inner_text()==message
   assert page.locator('.tm-viva').inner_text()==message
   assert page.locator('[data-palavra][aria-pressed="true"]').count()==count
   assert page.locator('[data-confirmar]').is_enabled()==(count>0)
  assert page.evaluate('JSON.stringify(CARTOES)===antes')
  print('PASS concordância e confirmação: 0, 1 e 2 palavras',flush=True)
  for i in (0,2,5):page.locator(f'[data-palavra="{i}"]').click()
  page.locator('[data-confirmar]').click()
  for e in c['erros']:page.locator(f'[name="c-{c["id"]}-{e["em"]}"][value="{e["c"]}"]').check()
  page.locator('[data-confirmar]').click()
  assert 'Acertaste 8 de 9' in page.locator('[data-c-folha]').inner_text()
  assert page.locator('.tm-balanco').inner_text()=='Identificação: 6 de 7 decisões corretas. Formas: 2 de 2 correções.'
  page.locator('[data-c-folha] [data-seguinte]').click();page.locator('[data-errados]').click()
  assert page.locator('[data-erro]').count()==0
  assert page.locator('[data-local]').count()==1
  assert page.locator('[data-local="5"] legend').inner_text()=='A forma na precisa de correção?'
  page.locator(f'[name="l-{c["id"]}-5"][value="0"]').check();page.locator('[data-confirmar]').click()
  assert 'Acertaste 1 de 1' in page.locator('[data-c-folha]').inner_text()
  print('PASS falso positivo: só a decisão falhada volta, sem inventar erro de forma',flush=True)
  b.close()
if __name__=='__main__':main()
