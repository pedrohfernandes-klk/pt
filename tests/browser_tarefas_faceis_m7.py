"""13/11/2026: as três tarefas do M7 «mais fáceis de fazer» (camada tarefas_faceis_m7_20261113), no navegador, com o CSS e o motor
reais (o leitor em cartões, os relógios). As mesmas exigências de tests/browser_tarefas_faceis_m3.py e de
tests/browser_tarefas_faceis_m6.py:

* a 390 e a 1280 px, em tema claro e em escuro, em todos os cartões de cada enunciado: a página não desliza para o lado, o cartão não
  transborda e nenhum elemento sai do ecrã (também com todos os desdobráveis abertos); o índice mostra os nomes dos cartões, sem
  números; não há erros de página; não há imagens; a grelha, a versão de correção (também a 320 px), os aquecimentos, o guia da
  tarefa e o portefólio do M7 também não deslizam;
* no guia da tarefa do M7: os quatro blocos somam 90 minutos (10, 10, 55, 15) e, nas três produções, não há «Autoavaliação» para
  copiar para o Teams nem «par de trabalho»: a regra chama-se «Dois antes de mim» e tem dois passos, e o que se copia para o Teams
  traz o plano, as notas e a lista;
* no portefólio do M7 não há «trabalho de equipa»;
* os desdobráveis abrem com o teclado (Enter e Espaço no <summary>) e mostram o que guardam;
* o relógio de produção é de 55 minutos («até 55 min», 55:00) e o do aquecimento de 10; na m7-u2, o da apresentação é de 2;
* as ligações internas funcionam: «Texto N» e «dossiê» abrem o cartão e o desdobrável que os guarda, com todos os versos;
* em papel (A4, margens de 12 mm): os desdobráveis de apoio (.tf-so-ecra) e o cartão «Rever a matéria» não saem; os dois poemas da
  m7-u3 e o dossiê saem abertos; nenhum poema e nenhuma estrofe se parte entre duas páginas; cada enunciado cabe em 4 páginas.

Uso: python3 tests/browser_tarefas_faceis_m7.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com TAREFAS_FACEIS_M7_OUTPUT, guarda aí as
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
CARTOES = {'m7-u1': ['Começar', 'A comparação', 'Fechar e entregar', 'Rever a matéria'],
           'm7-u2': ['Começar', 'Parte' + N + '1: o perfil', 'Parte' + N + '2: o texto', 'Parte' + N + '3: escolhas e fontes', 'Parte' + N + '4: a apresentação',
                     'Fechar e entregar', 'Rever a matéria'],
           'm7-u3': ['Começar', 'Tema A ou B', 'O teu texto', 'Fechar e entregar', 'Rever a matéria']}
SAIDA = os.environ.get('TAREFAS_FACEIS_M7_OUTPUT')
# Os textos de cada enunciado: (alvo, versos, estrofes, linhas de vocabulário).
TEXTOS = {'m7-u1': [('#texto-1', 24, 4, 4), ('#texto-2', 12, 3, 0)], 'm7-u2': [], 'm7-u3': [('#texto-1', 12, 2, 1), ('#texto-2', 10, 2, 1)]}
# Ligações internas: (cartão de partida, seletor da ligação, alvo, cartão onde o alvo está).
LIGACOES = {'m7-u1': [(1, '.tf-pedido a[href="#texto-1"]', '#texto-1', 1), (1, '.tf-pedido a[href="#texto-2"]', '#texto-2', 1)],
            'm7-u2': [],
            'm7-u3': [(1, '[data-task-theme="A"] a[href="#texto-1"]', '#texto-1', 1), (1, '[data-task-theme="B"] a[href="#texto-2"]', '#texto-2', 1),
                      (1, '[data-task-theme="B"] a[href="#dossie"]', '#dossie', 1)]}
# Os desdobráveis de cada enunciado (exemplos e apoios, material dos temas, perguntas opcionais) e os que não saem em papel.
DESDOBRAVEIS = {'m7-u1': 2, 'm7-u2': 4, 'm7-u3': 5}
SO_ECRA = {'m7-u1': 1, 'm7-u2': 3, 'm7-u3': 2}
MAX_PAGINAS = {'m7-u1': 4, 'm7-u2': 4, 'm7-u3': 4}
MEDIR = '''() => { const c = document.querySelector('.casca-corpo'); const cartao = document.querySelector('.task-reader-card:not([hidden])');
  return { nome: cartao.getAttribute('aria-label'), pagina: document.documentElement.scrollWidth <= innerWidth + 1,
    corpo: c.scrollWidth <= c.clientWidth + 1,
    fora: [...cartao.querySelectorAll('*')].filter(e => e.getClientRects().length && !e.closest('.sr-only') && e.getBoundingClientRect().right > innerWidth + 0.5)
      .map(e => e.tagName + '.' + e.className).slice(0, 5) }; }'''
VISIVEL = '''(sel) => { const e = document.querySelector(sel); if (!e) return false; const r = e.getBoundingClientRect();
  const c = e.closest('.task-reader-card'); return !!(r.width && r.height) && !(c && c.hidden) && r.top < innerHeight && r.bottom > 0; }'''


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
            # Os textos: todos os versos, as estrofes, os números de 5 em 5 e o vocabulário.
            for alvo, versos, estrofes, voc in TEXTOS[slug]:
                t = page.evaluate("""(t) => ({ v: document.querySelectorAll(t + ' .tt-v').length, e: document.querySelectorAll(t + ' .tt-estrofe').length,
                    n: [...document.querySelectorAll(t + ' .tt-n')].map(e => e.textContent).filter(x => x), g: document.querySelectorAll(t + ' .tt-gloss li').length,
                    falta: document.querySelectorAll(t + ' .tt-falta').length })""", alvo)
                assert t == {'v': versos, 'e': estrofes, 'n': [str(k) for k in range(5, versos + 1, 5)], 'g': voc, 'falta': 0}, (onde, alvo, t)
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
    assert [x[:3] for x in r[:2]] == [['10', 'Aquecimento', '0'], ['55', 'Produção em papel', '1']], (slug, r)
    assert re.search(r'até\s55\smin', r[1][3]) and '55:00' in r[1][3], (slug, r[1][3])
    assert re.search(r'até\s10\smin', r[0][3]) and '10:00' in r[0][3], (slug, r[0][3])
    assert len(r) == (3 if slug == 'm7-u2' else 2), (slug, len(r))
    if slug == 'm7-u2':
        assert r[2][:3] == ['2', 'Apresentação da voz', '4'], r[2]
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
    # As ligações internas abrem o cartão e o desdobrável do alvo, com o alvo à vista e completo.
    versos = {alvo: v for alvo, v, _, _ in TEXTOS[slug]}
    for partida, ligacao, alvo, chegada in LIGACOES[slug]:
        ir(page, partida)
        page.locator(ligacao).first.click()
        page.wait_for_timeout(250)
        assert page.evaluate('EPITaskReader.current()') == chegada, (slug, ligacao)
        assert page.evaluate(VISIVEL, alvo), (slug, ligacao, alvo)
        if alvo in versos:
            assert page.locator(f'{alvo} .tt-v:visible').count() == versos[alvo], (slug, alvo)
        else:
            assert page.locator('section.tf-dossie li:visible').count() == 5, (slug, alvo)
        page.evaluate('document.querySelectorAll("main details").forEach(d => d.open = false)')
    assert not erros, (slug, erros)
    ctx.close()


def papel(host, browser, slug):
    ctx, page, erros = contexto(browser, 1280, 800, 'light')
    page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
    page.emulate_media(media='print')
    page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
    page.wait_for_timeout(100)
    # O apoio e o cartão «Rever a matéria» não saem; os textos e o dossiê saem.
    m = page.evaluate("""() => { const vis = e => !!e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
        return { ecra: [...document.querySelectorAll('.tf-so-ecra')].filter(vis).length, rever: vis(document.querySelector('.tf-rever')),
                 relogios: [...document.querySelectorAll('.task-relogio')].filter(vis).length, versos: [...document.querySelectorAll('.tt-v')].filter(vis).length,
                 dossie: [...document.querySelectorAll('section.tf-dossie li')].filter(vis).length, botao: [...document.querySelectorAll('.tf-imprimir')].filter(vis).length,
                 pedidos: [...document.querySelectorAll('.tf-alineas > li')].filter(vis).length, verificar: [...document.querySelectorAll('.task-checklist label')].filter(vis).length,
                 partir: [...document.querySelectorAll('.tt-texto, .tt-estrofe')].map(e => getComputedStyle(e).breakInside) }; }""")
    total = sum(v for _, v, _, _ in TEXTOS[slug])
    assert m['ecra'] == 0 and not m['rever'] and m['relogios'] == 0 and m['botao'] == 0, (slug, m)
    assert m['versos'] == total and m['dossie'] == (5 if slug == 'm7-u3' else 0), (slug, m)
    assert m['pedidos'] >= 6 and 9 <= m['verificar'] <= 10, (slug, m)
    # Nenhum poema e nenhuma estrofe se parte entre duas páginas.
    assert all(x == 'avoid' for x in m['partir']) and len(m['partir']) == len(TEXTOS[slug]) + sum(e for _, _, e, _ in TEXTOS[slug]), (slug, m['partir'])
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
        for rel in ('tarefas/m7-u3/grelha/', 'tarefas/m7-u3/correcao/', 'tarefas/m7-u1/aquecimento/', 'tarefas/m7-u2/aquecimento/', 'tarefas/m7-u3/aquecimento/',
                    'm7/guia-da-tarefa-m7/', 'm7/portefolio-do-modulo-m7/'):
            page.goto(f'{host}/{rel}', wait_until='networkidle')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (rel, largura)
        assert not erros, erros
        ctx.close()
    ctx, page, erros = contexto(browser, 390, 844, 'light')
    # A grelha e a versão de correção: as palavras do enunciado novo, a autoavaliação só para o aluno, sem a coluna «Aluno».
    page.goto(f'{host}/tarefas/m7-u3/grelha/', wait_until='networkidle')
    texto = page.locator('body').text_content()
    assert 'Opinião e conclusão' in texto and 'Facto ou comparação' in texto and 'Esta autoavaliação é só para ti: não se entrega.' in texto
    assert not re.search(r'[Tt]ese\b', texto) and 'outra voz' not in texto
    page.goto(f'{host}/tarefas/m7-u3/correcao/', wait_until='networkidle')
    cab = page.evaluate('[...document.querySelectorAll("table")[0].querySelectorAll("thead th")].map(e => e.textContent.trim())')
    assert 'Aluno' not in cab and 'Docente' in cab, cab
    pdf = page.pdf(format='A4', margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
    assert len(re.findall(rb'/Type\s*/Page\b', pdf)) == 1
    # O guia da tarefa: quatro blocos (10, 10, 55, 15), «Dois antes de mim», sem «Autoavaliação» nem par de trabalho, em cada produção.
    page.goto(f'{host}/m7/guia-da-tarefa-m7/', wait_until='networkidle')
    page.evaluate('document.querySelector("#arquivo-producoes").open = true')
    for n in (1, 2, 3):
        page.locator(f'button.tarefa[data-n="{n}"]').click()
        page.wait_for_timeout(80)
        rota = page.locator('#rota').text_content()
        blocos = [int(x) for x in re.findall(r', (\d+)' + N + 'min', page.locator('#blocos').text_content())]
        assert blocos == [10, 10, 55, 15] and sum(blocos) == 90, blocos
        assert 'Dois antes de mim.' in rota and 'Três antes' not in rota and 'par de trabalho' not in rota, n
        assert 'Autoavaliação' not in rota and 'autoavaliação' not in rota and page.locator('#r-auto, .niveis').count() == 0, n
        assert page.locator('.regra ol li').count() == 2, n
        assert page.locator('#r-verificar li').count() >= 3, n
        copiado = page.evaluate('''() => { let t = null; navigator.clipboard.writeText = (x) => { t = x; return Promise.resolve(); };
            document.querySelector('#copiar').click(); return t; }''')
        assert 'PLANO' in copiado and 'NOTAS DE TRABALHO' in copiado and 'VERIFICAÇÃO' in copiado and 'AUTOAVALIAÇÃO' not in copiado, (n, copiado)
        if n == 2:
            assert 'Opinião e conclusão' in copiado and 'Facto ou comparação' in copiado and 'Tese' not in copiado, copiado
        # o relógio do guia começa nos 10 minutos do primeiro bloco
        page.locator('#voltar').click()
        assert page.locator('#relogio').text_content() == '10:00', n
        page.evaluate('document.querySelector("#arquivo-producoes").open = true')
    page.goto(f'{host}/m7/portefolio-do-modulo-m7/', wait_until='networkidle')
    texto = page.locator('body').text_content()
    assert 'trabalho de equipa' not in texto and 'autonomia, responsabilidade, pensamento crítico' in texto
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
    print('Tarefas do M7 mais fáceis de fazer: OK (' + ', '.join(f'{s}: {n} páginas A4' for s, n in paginas.items()) + ')')


if __name__ == '__main__':
    main()
