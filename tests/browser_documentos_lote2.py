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
                    # 05/11/2026: decisão 153. A ficha («Identificação do documento visual»), a linha da licença com «Fonte ↗» e
                    # a ligação para a fonte e os direitos passam para o «i» (details.info-i, fechado ao carregar), por baixo da
                    # imagem; continua a exigir-se a ficha inteira, agora dentro do «i», e nada dela fora; «Abrir a imagem
                    # inteira» fica igual.
                    assert link.get_attribute('aria-label')=='Abrir a imagem inteira',lesson
                    info=page.locator('#baralho .documento > details.info-i')
                    assert info.count()==1,(lesson,'um «i»')
                    assert info.evaluate('(d)=>!d.open'),(lesson,'fechado ao carregar')
                    assert info.locator(':scope > summary').get_attribute('aria-label')=='Créditos da imagem',lesson
                    ficha=page.evaluate('''()=>{const f=document.querySelector("#baralho .documento"),i=f.querySelector(":scope > details.info-i");
                      return {dentro:[...i.querySelectorAll("table caption")].map(c=>c.textContent.trim()),
                        linhas:[...i.querySelectorAll("table th")].map(t=>t.textContent.trim()),
                        fora:[...f.querySelectorAll("table,details:not(.info-i)")].filter(e=>!i.contains(e)).length,
                        legenda:[...f.querySelectorAll("figcaption > *")].map(e=>e.tagName),
                        consultar:[...i.querySelectorAll("a")].some(a=>a.textContent.startsWith("Consultar a fonte e os direitos")),
                        fonte:[...i.querySelectorAll("a")].some(a=>a.textContent==="Fonte ↗")}}''')
                    assert ficha['dentro']==['Identificação do documento visual'],(lesson,ficha)
                    assert ficha['linhas']==['Autor','Obra','Data','Instituição ou acervo','Licença'],(lesson,ficha)
                    assert ficha['fora']==0 and ficha['legenda']==['P'],(lesson,ficha)
                    assert ficha['consultar'] and ficha['fonte'],(lesson,ficha)
                    state=page.evaluate('JSON.stringify(localStorage)')
                    link.focus();page.keyboard.press('Enter')
                    dialog=page.get_by_role('dialog');dialog.wait_for()
                    assert page.url==url
                    # 05/11/2026: revisão de 5/11 (pt-conteudos-lote2-2): a legenda do leitor é só o texto visível, sem a tabela
                    # escondida de créditos nem parágrafos colados.
                    leg=dialog.locator('.amp-leg').inner_text()
                    primeiro=page.evaluate('()=>document.querySelector("#baralho .documento figcaption > p").textContent.replace(/\\s+/g," ").trim()')
                    assert leg.strip()==primeiro,(lesson,leg,primeiro)
                    assert 'Créditos e fonte da imagem' not in leg and 'Identificação do documento visual' not in leg,(lesson,leg)
                    # 05/11/2026: decisão 153. A legenda do leitor é a legenda visível, sem nada do «i».
                    visivel=page.evaluate('()=>document.querySelector("#baralho .documento figcaption").textContent.replace(/\\s+/g," ").trim()')
                    assert leg.strip()==visivel,(lesson,leg,visivel)
                    assert not any(x in leg for x in ('Fonte ↗','Consultar a fonte','Reprodução redimensionada','Domínio público','CC BY')),(lesson,leg)
                    assert dialog.locator('.amp-leg').evaluate('(e)=>e.scrollHeight<=e.clientHeight+1'),(lesson,'a legenda rola')
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
