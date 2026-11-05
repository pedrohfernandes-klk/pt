"""02/11/2026: regressão PT150-01, imagem inteira, zoom, teclado, foco e progresso."""
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser_licoes_20261101 import local, ROOT

def main():
    cases=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        for width in (320,390,1366):
            for scheme in ('light','dark'):
                for lesson in ('m3-f19','m5-f17','m6-f14'):
                    ctx=browser.new_context(viewport={'width':width,'height':900},color_scheme=scheme,reduced_motion='reduce')
                    page=ctx.new_page();page.route('**/*',local)
                    projection='?projetar=1' if width==1366 else ''
                    url=f'https://licoes.test/{lesson[:2]}/licao-{lesson}/{projection}'
                    page.goto(url,wait_until='networkidle')
                    link=page.locator('#baralho .documento > a');link.wait_for()
                    state=page.evaluate('JSON.stringify(localStorage)')
                    link.focus();page.keyboard.press('Enter')
                    dialog=page.get_by_role('dialog');dialog.wait_for()
                    assert page.url==url
                    # 05/11/2026: revisão de 5/11 (pt-conteudos-lote2-2): a legenda do leitor é só o texto visível, sem a tabela
                    # escondida de créditos nem parágrafos colados.
                    leg=dialog.locator('.amp-leg').inner_text()
                    assert leg and 'Créditos e fonte da imagem' not in leg and 'Identificação do documento visual' not in leg,(lesson,leg)
                    assert not re.search(r'[a-zà-ú][.!?»][A-ZÀ-Ú]',leg),(lesson,leg)
                    im=dialog.locator('img')
                    # 03/11/2026: aguarda a imagem recém-aberta; uma imagem inválida continua a falhar.
                    im.evaluate('(im)=>im.decode()')
                    assert im.evaluate('(im)=>im.complete && im.naturalWidth>0')
                    box=im.bounding_box();area=dialog.locator('.amp-area').bounding_box()
                    assert box['width']<=area['width']+1 and box['height']<=area['height']+1,(lesson,width,box,area)
                    dialog.get_by_role('button',name='Ampliar',exact=True).click()
                    assert dialog.locator('output').inner_text()=='150 %'
                    page.keyboard.press('+');assert dialog.locator('output').inner_text()=='200 %'
                    page.keyboard.press('-');assert dialog.locator('output').inner_text()=='150 %'
                    dialog.get_by_role('button',name='Imagem inteira').click()
                    assert dialog.locator('output').inner_text()=='100 %'
                    for _ in range(9):
                        page.keyboard.press('Tab')
                        assert page.evaluate('document.querySelector(".amp-ov").contains(document.activeElement)')
                    page.keyboard.press('Escape');assert dialog.count()==0
                    assert link.evaluate('(a)=>a===document.activeElement')
                    assert page.evaluate('JSON.stringify(localStorage)')==state
                    assert page.locator('#baralho .cartao').count()==1
                    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                    cases+=1;ctx.close()
        browser.close()
    print(f'{cases} casos: imagem inteira, zoom, teclado, foco e progresso conferidos.')

if __name__=='__main__':main()
