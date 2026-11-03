"""03/11/2026: documento real do aluno, em ecrã e impressão, sem correção."""
import copy
import json
import os
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from cartoes_papel import pagina
from tipos_regras import DICAS_PAPEL
CARDS=json.loads((ROOT/'tests/fixtures/tipos-mais-ensaio.json').read_text('utf8'))


def main():
 cards=copy.deepcopy(CARDS)
 for c in cards:c['f']='SEGREDO_NAO_ENTRA_NO_PAPEL'
 before=copy.deepcopy(cards)
 html=pagina(cards)
 out=Path(os.environ['F2_PROVAS']) if os.environ.get('F2_PROVAS') else None
 if out:out.mkdir(parents=True,exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for width in (320,390,1366):
   page=browser.new_page(viewport={'width':width,'height':900})
   page.set_content(html)
   assert page.locator('.cartao-papel').count()==6
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert page.locator('.pedido').all_text_contents()==[c['p'] for c in cards]
   assert page.locator('.dica').all_text_contents()==[DICAS_PAPEL[c['t']] for c in cards]
   assert 'SEGREDO_NAO_ENTRA_NO_PAPEL' not in page.content()
   assert page.locator('script,input,button,select').count()==0
   for el in page.locator('.cartao-papel,.material ol,.pedido').all():
    box=el.bounding_box();assert box['x']>=0 and box['x']+box['width']<=width
   if out:page.screenshot(path=str(out/f'papel-{width}.png'),full_page=True)
   page.emulate_media(media='print')
   assert page.locator('.pedido').all_text_contents()==[c['p'] for c in cards]
   assert page.locator('main').evaluate('(e)=>getComputedStyle(e).padding')=='0px'
   assert page.locator('.cartao-papel').first.evaluate('(e)=>getComputedStyle(e).breakInside')=='avoid-page'
   if out and width==1366:
    page.screenshot(path=str(out/'papel-impressao.png'),full_page=True)
   page.close();print('PASS papel completo, ecrã e impressão',width,flush=True)
  browser.close()
 assert cards==before
if __name__=='__main__':main()
