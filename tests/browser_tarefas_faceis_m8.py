"""13/11/2026: as duas tarefas do M8 «mais fáceis de fazer» (camada tarefas_faceis_m8_20261113), no navegador, com o CSS e o motor
reais (o leitor em cartões, os relógios). As mesmas exigências de tests/browser_tarefas_faceis_m3.py, de
tests/browser_tarefas_faceis_m6.py e de tests/browser_tarefas_faceis_m7.py:

* a 390 e a 1280 px, em tema claro e em escuro, em todos os cartões de cada enunciado: a página não desliza para o lado, o cartão não
  transborda e nenhum elemento sai do ecrã (também com todos os desdobráveis abertos); o índice mostra os nomes dos cartões, sem
  números; não há erros de página; não há imagens; a grelha, a versão de correção (também a 320 px), os aquecimentos, o guia da
  tarefa, o portefólio, o mapa e o índice do M8 também não deslizam;
* os textos do M8 ainda têm direitos de autor e não se copiam: cada bloco «Onde está o texto» mostra só as linhas que as lições
  citam (2, 2, 2 e 4 versos na m8-u1; um recorte de prosa na m8-u2) e a linha de fonte, sem número de página, que diz onde ler o
  texto completo (14/11/2026: o manual só onde uma lição o confirma; nos outros poemas, o cartão da lição que dá a publicação); não há nenhum verso numerado nem texto em prosa copiado (.tt-versos, .tt-prosa);
* no guia da tarefa do M8: os quatro blocos somam 90 minutos (10, 10, 55, 15) e, nas três produções antigas, não há «Autoavaliação»
  para copiar para o Teams nem «par de trabalho»: a regra chama-se «Dois antes de mim» e tem dois passos, e o que se copia para o
  Teams traz o plano, as notas e a lista;
* no portefólio do M8 não há «trabalho de equipa» nem «autoavaliação /20»;
* os desdobráveis abrem com o teclado (Enter e Espaço no <summary>) e mostram o que guardam;
* o relógio de produção é de 55 minutos («até 55 min», 55:00) e o do aquecimento de 10;
* as ligações internas funcionam: «onde está cada poema» e «onde está o conto» abrem o cartão e o desdobrável que guarda o bloco;
* em papel (A4, margens de 12 mm): os desdobráveis de apoio (.tf-so-ecra) e o cartão «Rever a matéria» não saem; os blocos «Onde
  está o texto» saem abertos; nenhuma citação e nenhum bloco se parte entre duas páginas; cada enunciado cabe em 4 páginas.

Uso: python3 tests/browser_tarefas_faceis_m8.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com TAREFAS_FACEIS_M8_OUTPUT, guarda aí as
capturas de cada cartão (390 px em claro e 1280 px em escuro) e os PDF da impressão."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import argparse
import os
import re
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler

N = '\xa0'
LARGURAS = ((390, 844), (1280, 800))
NOMES = ['Começar', 'Tema A ou B', 'O teu plano', 'O teu texto', 'Fechar e entregar', 'Rever a matéria']
CARTOES = {'m8-u1': NOMES, 'm8-u2': NOMES}
SAIDA = os.environ.get('TAREFAS_FACEIS_M8_OUTPUT')
# Os blocos «Onde está o texto» de cada enunciado: (alvo, linhas da citação, primeira linha).
ONDE = {'m8-u1': [('#texto-1', 2, 'São como um cristal,'), ('#texto-2', 2, 'Já gastámos as palavras pela rua, meu amor,'),
                  ('#texto-3', 2, 'Em vez de peixes, Senhor,'), ('#texto-4', 4, 'A minha filha partiu uma tigela')],
        'm8-u2': [('#texto-1', 1, '«À sua frente uma senhora de idade, primeiro esboçada, finalmente completa, olha-a atentamente. De idade não, George '
                                  'detesta eufemismos, mesmo só pensados, uma mulher velha.»')]}
# Ligações internas: (cartão de partida, seletor da ligação, alvo, cartão onde o alvo está).
LIGACOES = {'m8-u1': [(1, '[data-task-theme="A"] a[href="#texto-1"]', '#texto-1', 1), (1, '[data-task-theme="B"] a[href="#texto-3"]', '#texto-3', 1)],
            'm8-u2': [(1, '.tf-topo a[href="#texto-1"]', '#texto-1', 1)]}
# Os desdobráveis de cada enunciado (o material dos temas, os dois exemplos e a pergunta opcional) e os que não saem em papel.
DESDOBRAVEIS = {'m8-u1': 5, 'm8-u2': 4}
SO_ECRA = {'m8-u1': 2, 'm8-u2': 2}
MAX_PAGINAS = {'m8-u1': 4, 'm8-u2': 4}
NAO_CONTAM = 'Não contam para as palavras: os versos e as passagens citados ou copiados, o plano e as duas linhas finais.'
MEDIR = '''() => { const c = document.querySelector('.casca-corpo'); const cartao = document.querySelector('.task-reader-card:not([hidden])');
  return { nome: cartao.getAttribute('aria-label'), pagina: document.documentElement.scrollWidth <= innerWidth + 1,
    corpo: c.scrollWidth <= c.clientWidth + 1,
    fora: [...cartao.querySelectorAll('*')].filter(e => e.getClientRects().length && !e.closest('.sr-only') && e.getBoundingClientRect().right > innerWidth + 0.5)
      .map(e => e.tagName + '.' + e.className).slice(0, 5) }; }'''
VISIVEL = '''(sel) => { const e = document.querySelector(sel); if (!e) return false; const r = e.getBoundingClientRect();
  const c = e.closest('.task-reader-card'); return !!(r.width && r.height) && !(c && c.hidden) && r.top < innerHeight && r.bottom > 0; }'''


# 14/11/2026: o fim da linha de fonte de cada bloco «Onde está o texto».
FIM_FONTE = {('m8-u1', '#texto-1'): 'O poema completo lê-se no manual. A lição' + N + 'F04 também diz onde o ler: cartão «O texto».',
             ('m8-u1', '#texto-2'): 'A lição' + N + 'F04 diz onde ler o poema completo: cartão «Outra leitura».',
             ('m8-u1', '#texto-3'): 'A lição' + N + 'F05 diz onde ler o poema completo: cartão «O texto».',
             ('m8-u1', '#texto-4'): 'A lição' + N + 'F05 diz onde ler o poema completo: cartão «Outra leitura».',
             ('m8-u2', '#texto-1'): 'O conto completo lê-se no manual.'}
ANTES_DA_AULA = 'Antes da aula, lê os dois poemas de cada tema.'


def contexto(browser, largura, altura, esquema):
    ctx = browser.new_context(viewport={'width': largura, 'height': altura}, color_scheme=esquema, reduced_motion='reduce')
    page = ctx.new_page()
    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
    erros = []
    page.on('pageerror', lambda e: erros.append(str(e)))
    page.on('console', lambda m: erros.append(m.text) if m.type == 'error' and 'fonts.g' not in m.text and 'ERR_FAILED' not in m.text else None)
    return ctx, page, erros


def ir(page, i):
    page.evaluate('i => EPITaskReader.go(i)', i)
    page.wait_for_timeout(120)


def ecra(host, browser, slug):
    for largura, altura in LARGURAS:
        for esquema in ('light', 'dark'):
            onde = f'{slug} {largura} {esquema}'
            ctx, page, erros = contexto(browser, largura, altura, esquema)
            page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
            assert page.evaluate('window.EPITaskReader && EPITaskReader.count') == len(CARTOES[slug]), onde
            fundo = page.evaluate('getComputedStyle(document.body).backgroundColor')
            claro = sum(int(x) for x in re.findall(r'\d+', fundo)[:3]) > 384
            assert claro == (esquema == 'light'), (onde, fundo)
            nomes = page.evaluate('[...document.querySelectorAll("[data-task-reader-jump]")].map(b => b.textContent.trim())')
            assert nomes == CARTOES[slug], (onde, nomes)
            assert page.locator('main img').count() == 0, onde
            assert page.locator('main details').count() == DESDOBRAVEIS[slug], (onde, page.locator('main details').count())
            assert page.locator('main details.tf-so-ecra').count() == SO_ECRA[slug], onde
            # Nenhum texto copiado (têm direitos de autor): só os blocos «Onde está o texto», com as linhas que as lições citam.
            assert page.locator('main .tt-versos, main .tt-prosa, main .tt-texto, main .tt-v').count() == 0, onde
            assert page.locator('main .tt-onde').count() == len(ONDE[slug]), onde
            for alvo, linhas, primeira in ONDE[slug]:
                t = page.evaluate("""(t) => { const q = document.querySelectorAll(t + ' .tt-cit'); return { n: q.length,
                    linhas: q.length ? q[0].innerHTML.split('<br>') : [], fonte: document.querySelector(t + ' .tt-fonte').textContent,
                    num: document.querySelector(t + ' .tt-num').textContent }; }""", alvo)
                assert t['n'] == 1 and len(t['linhas']) == linhas and t['linhas'][0] == primeira, (onde, alvo, t)
                # 14/11/2026: «lê-se no manual» só onde uma lição o confirma («As Palavras», «George»); nos outros três poemas, a linha
                # diz que cartão da lição dá a publicação. Sem número de página, como antes.
                assert t['fonte'].endswith(FIM_FONTE[(slug, alvo)]) and not re.search(r'p(ág)?\. ?\d|página \d', t['fonte']), (onde, alvo, t)
                assert ('manual' in t['fonte']) == ((slug, alvo) in (('m8-u1', '#texto-1'), ('m8-u2', '#texto-1'))), (onde, alvo, t)
                assert t['num'] == 'Texto' + N + alvo[-1], (onde, alvo, t)
            for i in range(len(CARTOES[slug])):
                ir(page, i)
                m = page.evaluate(MEDIR)
                assert m['nome'] == CARTOES[slug][i] and m['pagina'] and m['corpo'] and not m['fora'], (onde, i, m)
                # Com todos os desdobráveis abertos, também nada transborda.
                page.evaluate('document.querySelectorAll(".task-reader-card:not([hidden]) details").forEach(d => d.open = true)')
                page.wait_for_timeout(60)
                m = page.evaluate(MEDIR)
                assert m['pagina'] and m['corpo'] and not m['fora'], (onde, i, 'abertos', m)
                if SAIDA and ((largura == 390 and esquema == 'light') or (largura == 1280 and esquema == 'dark')):
                    page.screenshot(path=str(Path(SAIDA) / f'{slug}-{largura}-{esquema}-cartao{i + 1}.png'), full_page=True)
                page.evaluate('document.querySelectorAll(".task-reader-card:not([hidden]) details").forEach(d => d.open = false)')
            assert not erros, (onde, erros)
            ctx.close()


def relogios_teclado_e_ligacoes(host, browser, slug):
    ctx, page, erros = contexto(browser, 390, 844, 'light')
    page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
    # Os relógios: o do aquecimento no primeiro cartão (10 minutos) e o de produção no segundo (55 minutos).
    r = page.evaluate("""() => [...document.querySelectorAll('[data-relogio]')].map(e => [e.dataset.max, e.dataset.rotulo, e.closest('.task-reader-card').getAttribute('data-task-card'), e.textContent])""")
    assert [x[:3] for x in r] == [['10', 'Aquecimento', '0'], ['55', 'Produção em papel', '1']], (slug, r)
    assert re.search(r'até\s55\smin', r[1][3]) and '55:00' in r[1][3], (slug, r[1][3])
    assert re.search(r'até\s10\smin', r[0][3]) and '10:00' in r[0][3], (slug, r[0][3])
    # A única ligação ao aquecimento está no primeiro cartão.
    assert page.locator('a[href="aquecimento/"]').count() == 1 and page.locator('[data-task-card="0"] a[href="aquecimento/"]').count() == 1, slug
    # Os desdobráveis abrem com o teclado e mostram o que guardam.
    for k in range(page.locator('main details').count()):
        d = page.locator('main details').nth(k)
        cartao = int(d.evaluate('e => e.closest(".task-reader-card").getAttribute("data-task-card")'))
        ir(page, cartao)
        for pai in d.locator('xpath=ancestor::details').all():
            pai.evaluate('e => e.open = true')
        resumo = d.locator(':scope > summary')
        assert not d.evaluate('e => e.open'), (slug, k)
        resumo.focus()
        resumo.press('Enter' if k % 2 == 0 else 'Space')
        assert d.evaluate('e => e.open'), (slug, k, 'não abriu')
        dentro = d.evaluate('e => [...e.children].filter(x => x.tagName !== "SUMMARY").map(x => x.getBoundingClientRect().height).reduce((a, b) => a + b, 0)')
        assert dentro > 20, (slug, k, dentro)
        resumo.press('Enter')
        assert not d.evaluate('e => e.open'), (slug, k, 'não fechou')
    # As ligações internas abrem o cartão e o desdobrável do alvo, com o bloco à vista e completo.
    citacoes = {alvo: n for alvo, n, _ in ONDE[slug]}
    for partida, ligacao, alvo, chegada in LIGACOES[slug]:
        ir(page, partida)
        assert not page.evaluate(VISIVEL, alvo), (slug, alvo, 'já estava à vista')
        page.locator(ligacao).first.click()
        page.wait_for_timeout(250)
        assert page.evaluate('EPITaskReader.current()') == chegada, (slug, ligacao)
        assert page.evaluate(VISIVEL, alvo), (slug, ligacao, alvo)
        assert page.locator(f'{alvo} .tt-cit:visible').count() == 1 and page.locator(f'{alvo} .tt-fonte:visible').count() == 1, (slug, alvo)
        assert page.locator(f'{alvo} .tt-cit').inner_html().count('<br>') == citacoes[alvo] - 1, (slug, alvo)
        page.evaluate('document.querySelectorAll("main details").forEach(d => d.open = false)')
    assert not erros, (slug, erros)
    ctx.close()


def papel(host, browser, slug):
    ctx, page, erros = contexto(browser, 1280, 800, 'light')
    page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
    page.emulate_media(media='print')
    page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
    page.wait_for_timeout(100)
    # O apoio e o cartão «Rever a matéria» não saem; os blocos «Onde está o texto» saem abertos, com as citações.
    m = page.evaluate("""() => { const vis = e => !!e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
        return { ecra: [...document.querySelectorAll('.tf-so-ecra')].filter(vis).length, rever: vis(document.querySelector('.tf-rever')),
                 relogios: [...document.querySelectorAll('.task-relogio')].filter(vis).length, onde: [...document.querySelectorAll('.tt-onde')].filter(vis).length,
                 citacoes: [...document.querySelectorAll('.tt-cit')].filter(vis).length, fontes: [...document.querySelectorAll('.tt-onde .tt-fonte')].filter(vis).length,
                 botao: [...document.querySelectorAll('.tf-imprimir')].filter(vis).length, grelha: [...document.querySelectorAll('.task-grelha, .tf-grelha-nota')].filter(vis).length,
                 pedidos: [...document.querySelectorAll('.tf-alineas > li')].filter(vis).length, verificar: [...document.querySelectorAll('.task-checklist label')].filter(vis).length,
                 passos: [...document.querySelectorAll('.task-theme .tf-passos > li')].filter(vis).length,
                 partir: [...document.querySelectorAll('.tt-onde, .tt-cit')].map(e => getComputedStyle(e).breakInside) }; }""")
    assert m['ecra'] == 0 and not m['rever'] and m['relogios'] == 0 and m['botao'] == 0 and m['grelha'] == 0, (slug, m)
    # 14/11/2026: na m8-u1, a ordem de ler os poemas antes da aula sai em papel, no primeiro cartão.
    if slug == 'm8-u1':
        assert page.locator('header .tf-p', has_text=ANTES_DA_AULA).count() == 1 and page.locator('header .tf-p', has_text=ANTES_DA_AULA).is_visible(), slug
    assert m['onde'] == m['citacoes'] == m['fontes'] == len(ONDE[slug]), (slug, m)
    assert m['pedidos'] == (10 if slug == 'm8-u1' else 11) and m['verificar'] == 10 and m['passos'] == (3 if slug == 'm8-u1' else 4), (slug, m)
    # Nenhum bloco e nenhuma citação se parte entre duas páginas.
    assert all(x == 'avoid' for x in m['partir']) and len(m['partir']) == 2 * len(ONDE[slug]), (slug, m['partir'])
    pdf = page.pdf(format='A4', margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
    paginas = len(re.findall(rb'/Type\s*/Page\b', pdf))
    assert 1 <= paginas <= MAX_PAGINAS[slug], (slug, paginas)
    if SAIDA:
        (Path(SAIDA) / f'{slug}.pdf').write_bytes(pdf)
    assert not erros, (slug, erros)
    ctx.close()
    return paginas


def outras_paginas(host, browser):
    for largura in (320, 390, 1280):
        ctx, page, erros = contexto(browser, largura, 844, 'light')
        for rel in ('tarefas/m8-u1/grelha/', 'tarefas/m8-u1/correcao/', 'tarefas/m8-u2/grelha/', 'tarefas/m8-u2/correcao/', 'tarefas/m8-u1/aquecimento/',
                    'tarefas/m8-u2/aquecimento/', 'm8/guia-da-tarefa-m8/', 'm8/portefolio-do-modulo-m8/', 'm8/mapa-do-modulo-m8/', 'm8/'):
            page.goto(f'{host}/{rel}', wait_until='networkidle')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (rel, largura)
        assert not erros, erros
        ctx.close()
    ctx, page, erros = contexto(browser, 390, 844, 'light')
    for slug, onde_li in (('m8-u1', 'Não indicar onde leste os poemas (o manual ou outra edição).'), ('m8-u2', 'Não indicar onde leste o conto (o manual ou outra edição).')):
        # A grelha e a versão de correção: as palavras do enunciado novo, a autoavaliação só para o aluno, sem a coluna «Aluno».
        page.goto(f'{host}/tarefas/{slug}/grelha/', wait_until='networkidle')
        texto = page.locator('body').text_content()
        assert 'Esta autoavaliação é só para ti: não se entrega.' in texto and onde_li in texto, slug
        assert not re.search(r'núcleo|síntese|edição consultada|\btese\b|fora da contagem', texto), slug
        assert 'com plano e duas linhas finais. ' + NAO_CONTAM in texto, slug
        page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
        principal = page.locator('main').text_content()
        assert principal.count(NAO_CONTAM) == 1 and principal.count('com consulta') == 1, slug
        assert page.locator('.task-checklist label').count() == 10, slug
        rotulos = page.evaluate('[...document.querySelectorAll(".task-checklist label")].map(e => e.textContent.trim())')
        assert all(r.endswith('?') for r in rotulos) and 'Escrevi as duas linhas finais?' in rotulos, rotulos
        assert page.locator('.tf-exemplos .tf-exemplo').count() == 2, slug
        # Os exemplos usam o caso inventado do aquecimento e nenhuma palavra dos textos da tarefa.
        exemplos = page.evaluate('[...document.querySelectorAll(".tf-exemplos")].map(e => e.textContent).join(" ")')
        for fora in ('cristal', 'gastámos', 'peixes', 'tigela', 'George', 'senhora de idade', 'eufemismos', 'Georgina'):
            assert fora not in exemplos, (slug, fora)
        assert ('A janela bebe a manhã.' if slug == 'm8-u1' else 'Inês recebe um convite para cantar.') in exemplos, slug
        page.goto(f'{host}/tarefas/{slug}/correcao/', wait_until='networkidle')
        cab = page.evaluate('[...document.querySelectorAll("table")[0].querySelectorAll("thead th")].map(e => e.textContent.trim())')
        assert 'Aluno' not in cab and 'Docente' in cab, cab
        texto = page.locator('body').text_content()
        assert 'o plano e as duas linhas finais' in texto and not re.search(r'núcleo|síntese|Diferença entre a tua nota', texto), slug
        pdf = page.pdf(format='A4', margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
        assert len(re.findall(rb'/Type\s*/Page\b', pdf)) == 1, slug
    # O índice e o mapa do módulo: 10 minutos nos dois aquecimentos, 90 nas duas tarefas e as palavras do enunciado.
    page.goto(f'{host}/m8/', wait_until='domcontentloaded')
    chips = page.evaluate('''[...document.querySelectorAll('a[href*="tarefas/m8-u"] .chip')].map(e => e.textContent)''')
    assert chips == ['10' + N + 'min', '90' + N + 'min'] * 2, chips
    texto = page.locator('body').text_content()
    assert texto.count('tema A ou B, plano, texto, revisão e fotografias no Teams') == 3 and 'planificação' not in texto
    page.goto(f'{host}/m8/mapa-do-modulo-m8/', wait_until='networkidle')
    texto = page.locator('body').text_content()
    assert 'As duas linhas finais fazem parte da entrega' in texto and 'A síntese faz parte' not in texto
    # O guia da tarefa: quatro blocos (10, 10, 55, 15), «Dois antes de mim», sem «Autoavaliação» nem par de trabalho, em cada produção.
    page.goto(f'{host}/m8/guia-da-tarefa-m8/', wait_until='networkidle')
    texto = page.locator('#tarefas-das-unidades').text_content()
    assert NAO_CONTAM in texto and re.search(r'10\sminutos de leitura, 55 de produção individual em papel e 15 de revisão', texto), texto
    # 14/11/2026: sem «, no manual» (as lições não dizem que os quatro poemas estão no manual); a ordem de ler antes da aula fica.
    assert 'núcleo' not in texto and 'nas lições F04 e F05 antes da aula' not in texto and 'antes da aula, no manual' not in texto
    assert 'lê os dois poemas de cada tema antes da aula. As lições F04 e F05 citam só alguns versos' in texto
    page.evaluate('document.querySelector("#arquivo-producoes").open = true')
    for n in (1, 2, 3):
        page.locator(f'button.tarefa[data-n="{n}"]').click()
        page.wait_for_timeout(80)
        rota = page.locator('#rota').text_content()
        blocos = [int(x) for x in re.findall(r', (\d+)' + N + 'min', page.locator('#blocos').text_content())]
        assert blocos == [10, 10, 55, 15] and sum(blocos) == 90, blocos
        assert 'Dois antes de mim.' in rota and 'Três antes' not in rota and 'par de trabalho' not in rota and 'núcleo' not in rota, n
        assert 'Autoavaliação' not in rota and 'autoavaliação' not in rota and page.locator('#r-auto, .niveis').count() == 0, n
        assert page.locator('.regra ol li').count() == 2, n
        assert page.locator('#r-verificar li').count() >= 3, n
        copiado = page.evaluate('''() => { let t = null; navigator.clipboard.writeText = (x) => { t = x; return Promise.resolve(); };
            document.querySelector('#copiar').click(); return t; }''')
        assert 'PLANO' in copiado and 'NOTAS DE TRABALHO' in copiado and 'VERIFICAÇÃO' in copiado and 'AUTOAVALIAÇÃO' not in copiado, (n, copiado)
        # O segundo bloco (ler o enunciado) dura 10 minutos; ao voltar, o relógio do guia mostra os 10 minutos do primeiro bloco.
        page.locator('button[data-ir="1"]').click()
        assert re.fullmatch(r'10:00|9:5\d', page.locator('#relogio').text_content()), n
        page.locator('#voltar').click()
        assert page.locator('#relogio').text_content() == '10:00', n
        page.evaluate('document.querySelector("#arquivo-producoes").open = true')
    page.goto(f'{host}/m8/portefolio-do-modulo-m8/', wait_until='networkidle')
    texto = page.locator('body').text_content()
    assert 'trabalho de equipa' not in texto and 'autonomia, responsabilidade, pensamento crítico' in texto
    assert 'autoavaliação' not in texto and texto.count('tema A ou B, plano, texto e duas linhas finais.') == 2 and 'núcleo' not in texto
    assert not erros, erros
    ctx.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url')
    args = ap.parse_args()
    servidor = None
    host = args.url
    if not host:
        servidor = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
        threading.Thread(target=servidor.serve_forever, daemon=True).start()
        host = f'http://127.0.0.1:{servidor.server_address[1]}'
    if SAIDA:
        Path(SAIDA).mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            paginas = {}
            for slug in CARTOES:
                ecra(host, browser, slug)
                relogios_teclado_e_ligacoes(host, browser, slug)
                paginas[slug] = papel(host, browser, slug)
            outras_paginas(host, browser)
            browser.close()
    finally:
        if servidor:
            servidor.shutdown()
    print('Tarefas do M8 mais fáceis de fazer: OK (' + ', '.join(f'{s}: {n} páginas A4' for s, n in paginas.items()) + ')')


if __name__ == '__main__':
    main()
