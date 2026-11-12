"""12/11/2026: decisão 152 (cuidado em todas as lições), Exame e páginas transversais. A tabela nova e as referências que não se
partem, no navegador, com o CSS e os motores reais, no modelo de tests/browser_cuidado_m1.py a tests/browser_cuidado_m9.py:
* a tabela das fases da sessão (vista «Programa e fontes» do Exame, «Como cabe em 50 minutos?», que assets/exame/app.js monta), a
  360 e a 900 px, em tema claro e escuro: nada desliza para o lado, a tabela não sai do seu contentor, o cabeçalho e as cinco
  linhas veem-se, cada linha tem a fase e o tempo lado a lado e cada célula fica numa só linha; a frase da soma vem a seguir;
* as referências e os números que a camada prende (U+00A0, U+2060), nas páginas onde estão (a entrada, as páginas dos anos, o
  mapa, as obras, o laboratório e as três vistas do Exame: o catálogo, uma sessão e o programa): cada um fica numa só linha no
  ecrã e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona).

Uso: python3 tests/browser_cuidado_exame.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_EXAME_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) da tabela nova, a 360 e a 900 px, nos dois temas."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import argparse
import os
import sys
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler
sys.path.insert(0, str(ROOT / 'tests'))
from browser_cuidado_m9 import REFERENCIAS, confere_referencias, sem_deslizar  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('CUIDADO_EXAME_OUTPUT')
N, J = '\xa0', '⁠'
FASES = [('Aquecer', f'10{N}min'), ('Ler e planear', f'8{N}min'), ('Escrever', f'10–{J}20{N}min'), ('Corrigir', f'7–{J}17{N}min'),
         ('Fechar', f'5{N}min')]


def r(*agulhas):
    """As referências escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return [a.replace('{N}', N).replace('{J}', J) for a in agulhas]


# Referências nas páginas (tal como estão no HTML: só se procuram no texto que se vê, com as dobras abertas).
PAGINAS = {
    'index.html': r('1.º{N}ano', '2.º{N}ano', '3.º{N}ano', 'século{N}XIX', 'século{N}XX'),
    '1/index.html': r('1.º{N}ano'),
    '2/index.html': r('2.º{N}ano', 'século{N}XIX'),
    '3/index.html': r('3.º{N}ano', 'século{N}XX'),
    'mapa/index.html': r('1.º{N}ano', '2.º{N}ano', '3.º{N}ano', '45{N}minutos', 'século{N}XIX', 'século{N}XX'),
    'exame/laboratorio/index.html': r('Prova{N}639', '1.ª{N}fase', 'pp.{N}1–{J}3'),
    'obras/lusiadas/index.html': r('Canto{N}I', 'estâncias{N}100', 'a{N}106', 'estância{N}18', '12{N}min', 'n.º{N}3333'),
    'obras/cronica/index.html': r('D.{N}João{N}I', 'capítulos{N}XII', 'e{N}CXLVIII', 'século{N}XIV', '27{N}min'),
    'obras/index.html': None,
}
# As vistas do Exame (assets/exame/app.js monta-as a partir de assets/exame/sessoes.json): (o que vem a seguir a exame/, o que se
# espera ver, as referências).
VISTAS = [
    ('', '.hero', r('10.º–{J}12.º{N}ano', '10–{J}20{N}minutos', '50{N}min', 'Prova{N}639')),
    ('#s01', '.session-heading', r('50{N}minutos')),
    ('#s01/ler', '.session-heading', r('50{N}minutos', 'D.{N}Dinis', 'cantiga{N}1308', 'séc.{N}XIII')),
    ('#cobertura', 'table.apoio-tabela', r('50{N}minutos', '10{N}min', '8{N}min', '10–{J}20{N}min', '7–{J}17{N}min', '5{N}min',
                                           'Prova{N}639')),
]
TABELA = '''t=>{const linhas=el=>{const rg=document.createRange();rg.selectNodeContents(el);
  return new Set([...rg.getClientRects()].filter(x=>x.width>0).map(x=>Math.round(x.top))).size};
 const caixa=t.getBoundingClientRect(),pai=t.parentElement.getBoundingClientRect();
 return {cab:[...t.querySelectorAll('thead th')].map(th=>[th.textContent,th.checkVisibility(),th.getAttribute('scope'),th.getAttribute('role')]),
  linhas:[...t.querySelectorAll('tbody tr')].map(tr=>{const th=tr.querySelector('th'),td=tr.querySelector('td'),a=th.getBoundingClientRect(),b=td.getBoundingClientRect();
   return {fase:th.textContent,tempo:td.textContent,rotulo:td.dataset.label,escopo:th.getAttribute('scope'),ve:th.checkVisibility()&&td.checkVisibility(),
    lado:Math.abs(a.top-b.top)<2&&b.left>=a.right-1,linhas:[linhas(th),linhas(td)],largura:b.width}}),
  dentro:caixa.left>=pai.left-1&&caixa.right<=pai.right+1&&caixa.right<=innerWidth+1,
  seguinte:t.nextElementSibling&&t.nextElementSibling.textContent,anterior:t.previousElementSibling&&t.previousElementSibling.textContent,
  cor:getComputedStyle(t.querySelector('td')).color,fundo:getComputedStyle(document.body).backgroundColor}}'''


def confere_tabela(page, largura, esquema):
    onde = ('exame/#cobertura', largura, esquema)
    tabela = page.locator('#app table.apoio-tabela')
    assert tabela.count() == 1, onde
    t = tabela.evaluate(TABELA)
    assert t['cab'] == [['Fase', True, 'col', 'columnheader'], ['Tempo', True, 'col', 'columnheader']], (onde, t['cab'])
    assert [(x['fase'], x['tempo']) for x in t['linhas']] == FASES, (onde, t['linhas'])
    for x in t['linhas']:
        assert x['rotulo'] == 'Tempo' and x['escopo'] == 'row' and x['ve'], (onde, x)
        # A fase e o tempo lado a lado, cada um numa só linha (os tempos não se partem no traço nem antes de «min»).
        assert x['lado'] and x['linhas'] == [1, 1] and x['largura'] > 40, (onde, x)
    assert t['dentro'], onde
    assert t['anterior'] == f'Como cabe em 50{N}minutos?', (onde, t['anterior'])
    assert t['seguinte'] == 'A soma é sempre 50. O relógio não avança fases nem revela correções automaticamente.', (onde, t['seguinte'])
    assert t['cor'] != t['fundo'], onde
    sem_deslizar(page, onde)
    if SAIDA:
        Path(SAIDA).mkdir(parents=True, exist_ok=True)
        tabela.locator('xpath=..').screenshot(path=str(Path(SAIDA) / f'fases-{largura}-{esquema}.png'))


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
    referencias = tabelas = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for largura in LARGURAS:
                for esquema in ('light', 'dark'):
                    ctx = browser.new_context(viewport={'width': largura, 'height': 900}, device_scale_factor=1,
                                              color_scheme=esquema, reduced_motion='reduce')
                    page = ctx.new_page()
                    erros = []
                    page.on('pageerror', lambda e: erros.append(str(e)))
                    for sufixo, espera, agulhas in VISTAS:
                        page.goto(f'{host}/exame/index.html{sufixo}')
                        page.reload()
                        page.wait_for_selector(f'#app {espera}')
                        if sufixo == '#cobertura':
                            confere_tabela(page, largura, esquema)
                            tabelas += 1
                        confere_referencias(page, '#app', agulhas, ('exame/' + sufixo, largura, esquema))
                        referencias += len(agulhas)
                    if esquema == 'light':
                        for rel, agulhas in PAGINAS.items():
                            if not agulhas:
                                continue
                            page.goto(f'{host}/{rel}')
                            page.wait_for_load_state('load')
                            page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                            confere_referencias(page, 'body', agulhas, (rel, largura))
                            sem_deslizar(page, (rel, largura))
                            referencias += len(agulhas)
                    assert erros == [], erros
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    assert tabelas == 4, tabelas
    print(f'{tabelas} vistas da tabela das fases (360 e 900 px, tema claro e escuro) e {referencias} referências que não se partem: OK')


if __name__ == '__main__':
    main()
