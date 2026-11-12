"""12/11/2026: decisão 152 (cuidado em todas as lições), Exame e páginas transversais. A tabela nova e as referências que não se
partem, no navegador, com o CSS e os motores reais, no modelo de tests/browser_cuidado_m1.py a tests/browser_cuidado_m9.py:
* a tabela das fases da sessão (vista «Programa e fontes» do Exame, «Como cabe em 50 minutos?», que assets/exame/app.js monta), a
  360 e a 900 px, em tema claro e escuro: nada desliza para o lado, a tabela não sai do seu contentor, o cabeçalho e as cinco
  linhas veem-se, cada linha tem a fase e o tempo lado a lado e cada célula fica numa só linha; a frase da soma vem a seguir;
* as referências e os números que a camada prende (U+00A0, U+2060), nas páginas onde estão (a entrada, as páginas dos anos, o
  mapa, as obras, o laboratório e as três vistas do Exame: o catálogo, uma sessão e o programa): cada um fica numa só linha no
  ecrã e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona);
* 12/11/2026 (revisão): as quatro listas novas das provas em cartões (achados C 3, 4, 5 e 6: os níveis de cada parâmetro do
  Grupo III da 2.ª fase, os níveis de pontuação do item 7 das duas fases e os tipos de erro do Grupo III da 1.ª fase), cada uma
  no seu cartão «Escreve no caderno», montado com o motor real, com os desdobráveis abertos, a 360 e a 900 px, nos dois temas:
  cada lista e cada sublista à vista, com os itens todos e o texto esperado, um por linha, dentro do cartão e sem deslizar
  para o lado; e as referências presas desses cartões, de uma prova sem listas novas (o Grupo II da 1.ª fase) e de dois
  aquecimentos do Exame (s01 e s19, com a pergunta copiada da M9-F01), com a mesma exigência das outras páginas.

Uso: python3 tests/browser_cuidado_exame.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_EXAME_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) da tabela nova e dos quatro cartões com listas novas, a 360 e a 900 px, nos dois temas."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import os
import re
import sys
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'scripts'))
from browser_cuidado_m9 import REFERENCIAS, confere_lista, confere_referencias, sem_deslizar  # noqa: E402
from test_cuidado_m9 import cartoes  # noqa: E402
import cuidado_exame_20261112 as C  # noqa: E402

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


# 12/11/2026 (revisão): as listas novas das provas em cartões, por achado: (itens da lista de fora, ou None quando são listas
# soltas; itens de cada sublista, pela ordem).
LISTAS = {3: (3, [3, 3, 3]), 4: (3, [3, 2]), 5: (3, [3, 2]), 6: (None, [4, 2])}
# Cartões com referências presas, além dos quatro das listas: uma prova sem listas novas e dois aquecimentos do Exame (os
# cartões leem-se dos dados; a página é a que os mostra): (página, origem dos cartões, índices dos cartões).
COM_REFERENCIAS = [
    ('exame/provas/2026-1f/grupo-ii/index.html', None, (0, 2, 24)),
    ('exame/aquecimentos/s01/index.html', 'docs/pedagogia/exame-aquecimentos/s01.json', (1, 7, 8)),
    ('exame/aquecimentos/s19/index.html', 'docs/pedagogia/exame-aquecimentos/s19.json', (2, 12)),
]
ITENS = '''l=>[...l.querySelectorAll(':scope > li')].map(li=>{const c=li.cloneNode(true);c.querySelectorAll('ul').forEach(u=>u.remove());
 const r=li.getBoundingClientRect();return [c.textContent,Math.round(r.top),r.right]})'''


def sem_etiquetas(h):
    return re.sub(r'<[^>]+>', '', h)


# 12/11/2026: por cima desta camada ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112), que mudam
# uma linha da lista do achado 3 (no parâmetro C do Grupo III da 2.ª fase, «conectores» dá lugar à formulação do critério,
# «mecanismos de articulação interfrásica»). As listas conferem-se na página de hoje: o texto novo de cada achado com as trocas
# da camada de cima que caem dentro dele (só essa), com a mesma exigência: os itens todos, pela ordem, com o texto exato.
PROVAS_OFICIAL = json.loads((ROOT / 'tests/fixtures/exame-provas-oficial-edits-20261112.json').read_text('utf-8'))['files']
MUDADOS_POR_CIMA = {3: 1, 4: 0, 5: 0, 6: 0}


def como_esta_hoje(x):
    novo, n = x['novo'], 0
    for e in PROVAS_OFICIAL.get(x['pagina'], {}).get('edits', []):
        if e['old'] in novo:
            assert novo.count(e['old']) == e['occurrences'] == 1, (x['i'], e['location'])
            novo, n = novo.replace(e['old'], e['new']), n + 1
    assert n == MUDADOS_POR_CIMA[x['i']], (x['i'], n)
    if n:
        assert '«mecanismos de articulação interfrásica»' in novo and 'conectores' not in novo, x['i']
    return dict(x, novo=novo)


def agulhas_do_cartao(card):
    """As referências presas (com U+00A0 ou U+2060) no texto que o cartão mostra logo: o HTML de um cartão de leitura, ou o
    enunciado e as opções de um cartão de fazer; cada uma dentro de um só nó de texto, como a página a tem."""
    textos = [card.get('html', '')] if card['t'] == 'ler' else [card.get('p', '')] + [o for o in card.get('o') or [] if isinstance(o, str)]
    out = []
    for texto in textos:
        for pedaco in re.split(r'<[^>]+>', texto):
            out += [m for m in re.findall(r'[^\s\xa0]+(?:\xa0[^\s\xa0]+)+|\S*\u2060\S*', pedaco) if '&' not in m and m not in out]
    return out


def montar(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-exame',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
      document.querySelectorAll('#baralho details').forEach(d=>d.open=true);
    }''', card)
    page.locator('#baralho .cartao').first.wait_for()


def listas_esperadas(novo):
    """Do HTML novo do achado (como está nos dados): os textos dos itens da lista de fora (sem as sublistas) e de cada sublista."""
    h = novo.replace('<\\/', '</').replace('\\"', '"')
    subs = [[sem_etiquetas(li) for li in re.findall(r'<li>(.*?)</li>', u, re.S)] for u in re.findall(r'<ul>(.*?)</ul>', h, re.S)]
    fora = None
    if '<ul class="niveis">' in h:
        corpo = re.sub(r'<ul>.*?</ul>', '', h[h.index('<ul class="niveis">'):], flags=re.S)
        fora = [sem_etiquetas(li) for li in re.findall(r'<li>(.*?)</li>', corpo, re.S)]
    return fora, subs


def confere_listas_novas(page, x, largura, esquema):
    """As listas novas de um achado C, no seu cartão: à vista, com os itens todos e o texto esperado, um por linha, dentro do
    cartão e sem deslizar para o lado. Devolve quantas listas e sublistas conferiu."""
    onde = (x['pagina'], 'achado', x['i'], largura, esquema)
    fora, subs = listas_esperadas(x['novo'])
    n_fora, n_subs = LISTAS[x['i']]
    assert [len(s) for s in subs] == n_subs and (fora is None) == (n_fora is None) and (fora is None or len(fora) == n_fora), onde
    cartao = page.locator('#baralho .cartao').first
    direita = cartao.evaluate('c=>c.getBoundingClientRect().right')
    if fora is not None:
        lista = page.locator('#baralho .cartao ul.niveis:has(> li > ul)')
        confere_lista(page, lista, n_fora, onde)
        sublistas = lista.locator(':scope > li > ul')
        alvos = [(lista, fora)]
    else:
        # Os tipos de erro: duas listas, cada uma a seguir ao seu rótulo («Tipo A», «Tipo B»).
        sublistas = page.locator('#baralho .cartao p:has(> b:only-child) + ul')
        rotulos = page.locator('#baralho .cartao p:has(> b:only-child):has(+ ul)').all_text_contents()
        assert rotulos == ['Tipo A', 'Tipo B'], (onde, rotulos)
        alvos = []
    assert sublistas.count() == len(subs), (onde, sublistas.count())
    for k, textos in enumerate(subs):
        confere_lista(page, sublistas.nth(k), len(textos), onde + (k,))
        alvos.append((sublistas.nth(k), textos))
    for lista, textos in alvos:
        itens = lista.evaluate(ITENS)
        assert [i[0].strip() for i in itens] == [t.strip() for t in textos], (onde, itens)
        # Um item por linha, de cima para baixo, e nenhum passa da margem do cartão.
        assert all(b[1] > a[1] for a, b in zip(itens, itens[1:])), (onde, itens)
        assert all(i[2] <= direita + 1 for i in itens), (onde, itens, direita)
        assert lista.evaluate('l=>getComputedStyle(l).display') != 'none', onde
    if SAIDA:
        Path(SAIDA).mkdir(parents=True, exist_ok=True)
        cartao.screenshot(path=str(Path(SAIDA) / f'lista-{x["i"]}-{largura}-{esquema}.png'))
    return len(alvos)


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
    referencias = tabelas = listas = cartoes_vistos = 0
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
                    # 12/11/2026 (revisão): as listas novas das provas em cartões e as referências desses cartões.
                    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
                    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
                    for x in C.PROVAS_C:
                        # 12/11/2026: o achado como a página o tem hoje (com a troca da camada de cima, no achado 3).
                        x = como_esta_hoje(x)
                        novo = x['novo'].replace('<\\/', '</').replace('\\"', '"')
                        baralho = cartoes((ROOT / x['pagina']).read_text('utf-8'))
                        (card,) = [c for c in baralho if novo in c.get('html', '')]
                        assert card['t'] == 'ler' and card['rot'] == 'Escreve no caderno', (x['i'], card.get('rot'))
                        page.goto(f'{host}/{x["pagina"]}', wait_until='networkidle')
                        montar(page, card)
                        listas += confere_listas_novas(page, x, largura, esquema)
                        agulhas = agulhas_do_cartao(card)
                        assert len(agulhas) >= 4, (x['i'], agulhas)
                        confere_referencias(page, '#baralho .cartao', agulhas, (x['pagina'], 'achado', x['i'], largura, esquema))
                        referencias += len(agulhas)
                        cartoes_vistos += 1
                    # Uma prova sem listas novas e dois aquecimentos do Exame: as referências presas, nos cartões que as mostram.
                    for rel, origem, indices in COM_REFERENCIAS:
                        baralho = json.loads((ROOT / origem).read_text('utf-8'))['cartoes'] if origem else cartoes((ROOT / rel).read_text('utf-8'))
                        page.goto(f'{host}/{rel}', wait_until='networkidle')
                        for k in indices:
                            agulhas = agulhas_do_cartao(baralho[k])
                            assert agulhas, (rel, k)
                            montar(page, baralho[k])
                            confere_referencias(page, '#baralho .cartao', agulhas, (rel, 'cartão', k, largura, esquema))
                            sem_deslizar(page, (rel, 'cartão', k, largura, esquema))
                            referencias += len(agulhas)
                            cartoes_vistos += 1
                    assert erros == [], erros
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    assert tabelas == 4, tabelas
    # 12/11/2026 (revisão): 12 listas e sublistas (4 + 3 + 3 + 2, ver LISTAS) em cada uma das quatro combinações de largura e tema.
    assert listas == 4 * sum((n is not None) + len(s) for n, s in LISTAS.values()), listas
    assert cartoes_vistos == 4 * (len(C.PROVAS_C) + sum(len(i) for _, _, i in COM_REFERENCIAS)), cartoes_vistos
    print(f'{tabelas} vistas da tabela das fases, {listas} listas novas das provas em cartões (360 e 900 px, tema claro e escuro) e '
          f'{referencias} referências que não se partem, {cartoes_vistos} cartões de provas e de aquecimentos incluídos: OK')


if __name__ == '__main__':
    main()
