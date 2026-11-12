"""12/11/2026: a ligação «Treinos» na navegação da página principal do Exame (camada exame_ligacao_treinos_20261112), no navegador,
com o CSS e os motores reais, a 360 e a 900 px, em tema claro e escuro:
* a ligação vê-se no cabeçalho de exame/index.html, com o rótulo «Treinos», logo a seguir a «Provas em cartões» e antes de
  «Programa e fontes», numa só linha, dentro da navegação e do ecrã, sem tapar nem ser tapada pelas vizinhas, e a página não
  desliza para o lado;
* tem o aspeto das outras ligações da mesma navegação (a mesma letra, o mesmo tamanho, o mesmo peso, a mesma cor e o mesmo
  sublinhado de «Provas em cartões») e o mesmo aspeto da ligação «Treinos» dos cabeçalhos de exame/provas/ e de
  exame/laboratorio/ (a mesma letra, o mesmo tamanho, o mesmo peso, o mesmo sublinhado e o mesmo enchimento; a cor é a da tinta
  de cada página, que no tema escuro já diferia entre a página principal e as outras duas antes desta camada, e por isso
  compara-se com a da vizinha da mesma navegação), com contraste de pelo menos 4,5:1 sobre o fundo;
* chega-se a ela com a tecla Tab, pela ordem da navegação, e o foco de teclado vê-se (contorno ou sombra);
* Enter abre exame/treinos/ (a entrada dos três treinos), e um clique também.

Uso: python3 tests/browser_exame_ligacao_treinos.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com EXAME_LIGACAO_TREINOS_OUTPUT, guarda aí as
capturas (deviceScaleFactor 1) do cabeçalho com a ligação em foco e da página aberta, a 360 e a 900 px, nos dois temas."""
from functools import partial
from http.server import ThreadingHTTPServer
import argparse
import os
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler

LARGURAS = (360, 900)
SAIDA = os.environ.get('EXAME_LIGACAO_TREINOS_OUTPUT')
ORDEM = ['Sessões', 'Laboratório de respostas', 'Provas em cartões', 'Treinos', 'Programa e fontes', 'Dossiê']
OUTROS = ('exame/provas/index.html', 'exame/laboratorio/index.html')
MEDIR = r'''sel=>{const a=document.querySelector(sel),nav=a.closest('nav'),todas=[...nav.querySelectorAll('a')];
 const cs=e=>{const c=getComputedStyle(e);return {familia:c.fontFamily,tamanho:c.fontSize,peso:c.fontWeight,cor:c.color,
  sublinhado:c.textDecorationLine,maiusculas:c.textTransform,espacamento:c.letterSpacing,enchimento:c.padding}};
 const caixa=e=>{const r=e.getBoundingClientRect();return {l:r.left,r:r.right,t:r.top,b:r.bottom,w:r.width,h:r.height}};
 const rg=document.createRange();rg.selectNodeContents(a);
 const lum=s=>{const m=s.match(/[\d.]+/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};
  return {l:.2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2]),alfa:m.length>3?m[3]:1}};
 let fundo=null;for(let e=a;e;e=e.parentElement){const b=getComputedStyle(e).backgroundColor;if(lum(b).alfa===1){fundo=b;break}}
 if(!fundo)fundo=getComputedStyle(document.documentElement).backgroundColor;
 const l1=lum(getComputedStyle(a).color).l,l2=lum(fundo).l;
 const i=todas.indexOf(a),viz=todas[i-1];
 return {n:document.querySelectorAll(sel).length,texto:a.textContent,href:a.getAttribute('href'),atributos:a.getAttributeNames(),
  rotulos:todas.map(x=>x.textContent),ve:a.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}),
  caixa:caixa(a),nav:caixa(nav),outras:todas.filter(x=>x!==a&&x.checkVisibility()).map(caixa),
  linhas:new Set([...rg.getClientRects()].filter(x=>x.width>0).map(x=>Math.round(x.top))).size,
  estilo:cs(a),vizinha:cs(viz),vizinhaTexto:viz.textContent,fundo,contraste:(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05),
  largura:innerWidth,desliza:document.documentElement.scrollWidth-innerWidth,
  topo:(()=>{const r=a.getBoundingClientRect(),e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return e===a||a.contains(e)})()}}'''
FOCO = r'''()=>{const a=document.activeElement,c=getComputedStyle(a);
 return {href:a.getAttribute&&a.getAttribute('href'),texto:a.textContent,visivel:a.matches(':focus-visible'),
  contorno:[c.outlineStyle,parseFloat(c.outlineWidth),c.outlineColor],sombra:c.boxShadow}}'''


def confere(page, m, onde):
    assert m['n'] == 1 and m['texto'] == 'Treinos' and m['href'] == 'treinos/' and m['atributos'] == ['href'], (onde, m)
    assert m['rotulos'] == ORDEM, (onde, m['rotulos'])
    assert m['ve'] and m['caixa']['w'] > 20 and m['caixa']['h'] > 10, (onde, m['caixa'])
    assert m['topo'], (onde, 'a ligação está tapada')
    c, nav = m['caixa'], m['nav']
    # Dentro do ecrã e da navegação, numa só linha, sem deslizar para o lado.
    assert c['l'] >= 0 and c['r'] <= m['largura'] + .5, (onde, c)
    assert c['l'] >= nav['l'] - .5 and c['r'] <= nav['r'] + .5 and c['t'] >= nav['t'] - .5 and c['b'] <= nav['b'] + .5, (onde, c, nav)
    assert m['linhas'] == 1, (onde, m['linhas'])
    assert m['desliza'] <= 0, (onde, m['desliza'])
    # Não tapa nem é tapada pelas vizinhas.
    for o in m['outras']:
        assert o['r'] <= c['l'] + .5 or o['l'] >= c['r'] - .5 or o['b'] <= c['t'] + .5 or o['t'] >= c['b'] - .5, (onde, c, o)
    # O aspeto das outras ligações da mesma navegação.
    assert m['vizinhaTexto'] == 'Provas em cartões' and m['estilo'] == m['vizinha'], (onde, m['estilo'], m['vizinha'])
    assert m['contraste'] >= 4.5, (onde, m['contraste'], m['estilo']['cor'], m['fundo'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='servidor já aberto (por omissão, um próprio numa porta livre)')
    args = ap.parse_args()
    server = None
    if args.url:
        host = args.url.rstrip('/')
    else:
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        host = f'http://127.0.0.1:{server.server_port}'
    vistas = aberturas = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for largura in LARGURAS:
                for esquema in ('light', 'dark'):
                    onde = (largura, esquema)
                    ctx = browser.new_context(viewport={'width': largura, 'height': 900}, device_scale_factor=1,
                                              color_scheme=esquema, reduced_motion='reduce')
                    page = ctx.new_page()
                    erros = []
                    page.on('pageerror', lambda e: erros.append(str(e)))
                    page.goto(f'{host}/exame/index.html')
                    page.wait_for_selector('#app .hero')
                    assert page.evaluate("matchMedia('(prefers-color-scheme: dark)').matches") == (esquema == 'dark'), onde
                    m = page.evaluate(MEDIR, 'header.site-head nav a[href="treinos/"]')
                    confere(page, m, onde)
                    vistas += 1
                    # O mesmo aspeto da ligação «Treinos» dos outros cabeçalhos do Exame, na mesma largura e no mesmo tema.
                    for rel in OUTROS:
                        outra = ctx.new_page()
                        outra.goto(f'{host}/{rel}')
                        outra.wait_for_load_state('load')
                        o = outra.evaluate(MEDIR, 'header.site-head nav a[href="../treinos/"]')
                        sem_cor = lambda e: {k: v for k, v in e.items() if k != 'cor'}  # noqa: E731
                        assert o['texto'] == m['texto'] and sem_cor(o['estilo']) == sem_cor(m['estilo']), (onde, rel, o['estilo'], m['estilo'])
                        assert o['contraste'] >= 4.5, (onde, rel, o['estilo'], o['contraste'])
                        assert o['vizinhaTexto'] == 'Provas em cartões', (onde, rel, o['vizinhaTexto'])
                        outra.close()
                    # Foco de teclado: chega-se à ligação com Tab, logo a seguir a «Provas em cartões», e o foco vê-se.
                    anterior = None
                    for _ in range(12):
                        page.keyboard.press('Tab')
                        f = page.evaluate(FOCO)
                        if f['href'] == 'treinos/':
                            break
                        anterior = f
                    assert f['href'] == 'treinos/' and f['texto'] == 'Treinos', (onde, f)
                    assert anterior and anterior['texto'] == 'Provas em cartões', (onde, anterior)
                    assert f['visivel'], (onde, f)
                    assert (f['contorno'][0] != 'none' and f['contorno'][1] >= 1) or f['sombra'] != 'none', (onde, f)
                    if SAIDA:
                        os.makedirs(SAIDA, exist_ok=True)
                        page.screenshot(path=os.path.join(SAIDA, f'exame-ligacao-treinos-{largura}-{esquema}-foco.png'),
                                        clip={'x': 0, 'y': 0, 'width': largura, 'height': 420})
                    # Enter abre a entrada dos treinos.
                    with page.expect_navigation():
                        page.keyboard.press('Enter')
                    assert page.url == f'{host}/exame/treinos/', (onde, page.url)
                    # 12/11/2026: com os treinos das sessões 17 e 18 a entrada passa a ter cinco treinos; a exigência é a mesma, com o título novo.
                    assert page.locator('h1').inner_text() == 'Cinco treinos de exame', onde
                    aberturas += 1
                    if SAIDA:
                        page.screenshot(path=os.path.join(SAIDA, f'exame-ligacao-treinos-{largura}-{esquema}-aberta.png'),
                                        clip={'x': 0, 'y': 0, 'width': largura, 'height': 420})
                    # Um clique também, e a entrada dos treinos volta à página principal do Exame.
                    page.goto(f'{host}/exame/index.html')
                    page.wait_for_selector('#app .hero')
                    with page.expect_navigation():
                        page.click('header.site-head nav a[href="treinos/"]')
                    assert page.url == f'{host}/exame/treinos/', (onde, page.url)
                    resposta = page.request.get(page.url)
                    assert resposta.status == 200, (onde, resposta.status)
                    aberturas += 1
                    with page.expect_navigation():
                        page.click('header.site-head a.wordmark')
                    assert page.url == f'{host}/exame/', (onde, page.url)
                    page.wait_for_selector('#app .hero')
                    assert erros == [], (onde, erros)
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    assert vistas == 4 and aberturas == 8, (vistas, aberturas)
    print(f'{vistas} vistas da ligação «Treinos» na página principal do Exame (360 e 900 px, tema claro e escuro): à vista, sem '
          f'transbordar, com foco de teclado, igual à dos outros cabeçalhos, e {aberturas} aberturas de exame/treinos/: OK')


if __name__ == '__main__':
    main()
