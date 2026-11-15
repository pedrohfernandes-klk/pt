"""15/11/2026: a tarefa m4-u2 no molde «mais fácil de fazer», com «Tema A ou B» (camada tarefa_m4u2_tema_b_20261115), no navegador,
com o CSS e o motor reais (o leitor em cartões, os relógios). As mesmas exigências de tests/browser_tarefas_faceis_m9.py:

* a 390 e a 1280 px, em tema claro e em escuro, em todos os cartões: a página não desliza para o lado, o cartão não transborda e
  nenhum elemento sai do ecrã (também com todos os desdobráveis abertos); o índice mostra os nomes dos cartões, sem números; não há
  erros de página; não há imagens; o aquecimento, o guia da tarefa, o portefólio, o mapa e o índice do M4, e o enunciado, a grelha e
  o guia da tarefa do M8 (o acerto do M8) também não deslizam;
* as falas de Garrett: o Texto 1 tem as nove falas do diálogo do retrato (ato II, cena I), seguidas, com o vocabulário e a linha de
  fonte; o Texto 2 tem as seis falas curtas, uma por bloco; a peça lê-se no livro (nunca «manual», nunca «edição da turma»);
* os dois temas: A, a apreciação crítica do espetáculo; B, a pergunta do docente, letra a letra; não há «Se não foste ao teatro»;
* os desdobráveis abrem com o teclado (Enter e Espaço no <summary>) e mostram o que guardam;
* o relógio de produção é de 55 minutos («até 55 min», 55:00) e o do aquecimento de 10; a única ligação ao aquecimento está no
  primeiro cartão;
* as ligações internas funcionam: «Texto 1» e «Textos 1 e 2» abrem o cartão e o desdobrável que guarda os textos;
* em papel (A4, margens de 12 mm): os exemplos (.tf-so-ecra) e o cartão «Rever a matéria» não saem; os textos saem abertos; nenhuma
  fala do Texto 1 nem nenhuma citação do Texto 2 se parte entre duas páginas; o enunciado cabe em 5 páginas (cada cartão de pedido começa página nova);
* no guia da tarefa do M4: a unidade 2 com os tempos 10/10/55/15 e a frase do que não conta para as palavras; nada de «síntese»,
  «Se faltaste», «autoavaliação» nem «par de trabalho»; no portefólio, nada de «trabalho de equipa»;
* no M8: as quatro linhas de fonte dizem «O poema completo lê-se no manual.», e a alínea e a grelha dizem «o manual, a publicação
  que a lição indica ou outra edição».

Uso: python3 tests/browser_tarefas_faceis_m4.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com TAREFAS_FACEIS_M4_OUTPUT, guarda aí as
capturas de cada cartão (390 px em claro e 1280 px em escuro) e o PDF da impressão."""
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
SLUG = 'm4-u2'
NOMES = ['Começar', 'Tema A ou B', 'O teu texto', 'Fechar e entregar', 'Rever a matéria']
SAIDA = os.environ.get('TAREFAS_FACEIS_M4_OUTPUT')
DESDOBRAVEIS = 4  # os dois exemplos (um por tema), os textos para os dois temas e as perguntas opcionais
SO_ECRA = 2
MAX_PAGINAS = 5  # cada cartão de pedido começa página nova (a folha do molde); com o diálogo inteiro, a m4-u2 ocupa 5
NAO_CONTAM = 'Não contam para as palavras: as passagens citadas ou copiadas e as duas linhas finais.'
PERGUNTA = 'Que juízo merece Telmo, quando cala o nome do retrato no ato II de Frei Luís de Sousa: cumpre a palavra dada ou engana Maria?'
EDICAO_M8 = 'o manual, a publicação que a lição indica ou outra edição'
LIGACOES = [(1, '[data-task-theme="A"] a[href="#texto-1"]', '#texto-1', 1), (1, '[data-task-theme="B"] a[href="#texto-1"]', '#texto-1', 1)]
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


def ecra(host, browser):
    for largura, altura in LARGURAS:
        for esquema in ('light', 'dark'):
            onde = f'{SLUG} {largura} {esquema}'
            ctx, page, erros = contexto(browser, largura, altura, esquema)
            page.goto(f'{host}/tarefas/{SLUG}/', wait_until='networkidle')
            assert page.evaluate('window.EPITaskReader && EPITaskReader.count') == len(NOMES), onde
            fundo = page.evaluate('getComputedStyle(document.body).backgroundColor')
            claro = sum(int(x) for x in re.findall(r'\d+', fundo)[:3]) > 384
            assert claro == (esquema == 'light'), (onde, fundo)
            nomes = page.evaluate('[...document.querySelectorAll("[data-task-reader-jump]")].map(b => b.textContent.trim())')
            assert nomes == NOMES, (onde, nomes)
            assert page.locator('main img').count() == 0, onde
            assert page.locator('main details').count() == DESDOBRAVEIS, (onde, page.locator('main details').count())
            assert page.locator('main details.tf-so-ecra').count() == SO_ECRA, onde
            # As falas de Garrett: o Texto 1, nove falas seguidas; o Texto 2, seis falas curtas.
            assert page.locator('#texto-1 .tt-par').count() == 9 and page.locator('#texto-1 .tt-fonte').count() == 1, onde
            assert page.locator('#texto-2 .tt-cit').count() == 6 and page.locator('#texto-2 .tt-fonte').count() == 1, onde
            fontes = page.evaluate('[...document.querySelectorAll(".tt-fonte")].map(e => e.textContent)')
            assert all(f.endswith('A peça inteira lê-se no livro.') and 'manual' not in f for f in fontes), (onde, fontes)
            texto = page.evaluate('() => document.querySelector("main").textContent').replace(N, ' ')
            assert texto.count(PERGUNTA) == 1, onde
            assert 'não foste ao teatro' not in texto.lower() and 'edição da turma' not in texto, onde
            for i in range(len(NOMES)):
                ir(page, i)
                m = page.evaluate(MEDIR)
                assert m['nome'] == NOMES[i] and m['pagina'] and m['corpo'] and not m['fora'], (onde, i, m)
                page.evaluate('document.querySelectorAll(".task-reader-card:not([hidden]) details").forEach(d => d.open = true)')
                page.wait_for_timeout(60)
                m = page.evaluate(MEDIR)
                assert m['pagina'] and m['corpo'] and not m['fora'], (onde, i, 'abertos', m)
                if SAIDA and ((largura == 390 and esquema == 'light') or (largura == 1280 and esquema == 'dark')):
                    page.screenshot(path=str(Path(SAIDA) / f'{SLUG}-{largura}-{esquema}-cartao{i + 1}.png'), full_page=True)
                page.evaluate('document.querySelectorAll(".task-reader-card:not([hidden]) details").forEach(d => d.open = false)')
            assert not erros, (onde, erros)
            ctx.close()


def relogios_teclado_e_ligacoes(host, browser):
    ctx, page, erros = contexto(browser, 390, 844, 'light')
    page.goto(f'{host}/tarefas/{SLUG}/', wait_until='networkidle')
    r = page.evaluate("""() => [...document.querySelectorAll('[data-relogio]')].map(e => [e.dataset.max, e.dataset.rotulo, e.closest('.task-reader-card').getAttribute('data-task-card'), e.textContent])""")
    assert [x[:3] for x in r] == [['10', 'Aquecimento', '0'], ['55', 'Produção em papel', '1']], r
    assert re.search(r'até\s55\smin', r[1][3]) and '55:00' in r[1][3], r[1][3]
    assert re.search(r'até\s10\smin', r[0][3]) and '10:00' in r[0][3], r[0][3]
    assert page.locator('a[href="aquecimento/"]').count() == 1 and page.locator('[data-task-card="0"] a[href="aquecimento/"]').count() == 1
    for k in range(page.locator('main details').count()):
        d = page.locator('main details').nth(k)
        cartao = int(d.evaluate('e => e.closest(".task-reader-card").getAttribute("data-task-card")'))
        ir(page, cartao)
        for pai in d.locator('xpath=ancestor::details').all():
            pai.evaluate('e => e.open = true')
        resumo = d.locator(':scope > summary')
        assert not d.evaluate('e => e.open'), k
        resumo.focus()
        resumo.press('Enter' if k % 2 == 0 else 'Space')
        assert d.evaluate('e => e.open'), (k, 'não abriu')
        dentro = d.evaluate('e => [...e.children].filter(x => x.tagName !== "SUMMARY").map(x => x.getBoundingClientRect().height).reduce((a, b) => a + b, 0)')
        assert dentro > 20, (k, dentro)
        resumo.press('Enter')
        assert not d.evaluate('e => e.open'), (k, 'não fechou')
    for partida, ligacao, alvo, chegada in LIGACOES:
        ir(page, partida)
        assert not page.evaluate(VISIVEL, alvo), (alvo, 'já estava à vista')
        page.locator(ligacao).first.click()
        page.wait_for_timeout(250)
        assert page.evaluate('EPITaskReader.current()') == chegada, ligacao
        assert page.evaluate(VISIVEL, alvo), (ligacao, alvo)
        assert page.locator('#texto-1 .tt-par:visible').count() == 9 and page.locator('#texto-2 .tt-cit:visible').count() == 6, ligacao
        page.evaluate('document.querySelectorAll("main details").forEach(d => d.open = false)')
    assert not erros, erros
    ctx.close()


def papel(host, browser):
    ctx, page, erros = contexto(browser, 1280, 800, 'light')
    page.goto(f'{host}/tarefas/{SLUG}/', wait_until='networkidle')
    page.emulate_media(media='print')
    page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
    page.wait_for_timeout(100)
    m = page.evaluate("""() => { const vis = e => !!e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
        return { ecra: [...document.querySelectorAll('.tf-so-ecra')].filter(vis).length, rever: vis(document.querySelector('.tf-rever')),
                 relogios: [...document.querySelectorAll('.task-relogio')].filter(vis).length,
                 falas: [...document.querySelectorAll('#texto-1 .tt-par')].filter(vis).length, citacoes: [...document.querySelectorAll('.tt-cit')].filter(vis).length,
                 botao: [...document.querySelectorAll('.tf-imprimir')].filter(vis).length,
                 pedidos: [...document.querySelectorAll('.tf-alineas > li')].filter(vis).length, verificar: [...document.querySelectorAll('.task-checklist label')].filter(vis).length,
                 passos: [...document.querySelectorAll('.task-theme .tf-passos > li')].filter(vis).length,
                 partir: [...document.querySelectorAll('#texto-1 .tt-par, .tt-cit')].map(e => getComputedStyle(e).breakInside) }; }""")
    assert m['ecra'] == 0 and not m['rever'] and m['relogios'] == 0 and m['botao'] == 0, m
    assert m['falas'] == 9 and m['citacoes'] == 6, m
    assert m['pedidos'] == 11 and m['verificar'] == 9 and m['passos'] == 4, m
    assert all(x == 'avoid' for x in m['partir']) and len(m['partir']) == 15, m['partir']
    pdf = page.pdf(format='A4', margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
    paginas = len(re.findall(rb'/Type\s*/Page\b', pdf))
    assert 1 <= paginas <= MAX_PAGINAS, paginas
    if SAIDA:
        (Path(SAIDA) / f'{SLUG}.pdf').write_bytes(pdf)
    assert not erros, erros
    ctx.close()
    return paginas


def outras_paginas(host, browser):
    for largura in (320, 390, 1280):
        ctx, page, erros = contexto(browser, largura, 844, 'light')
        for rel in ('tarefas/m4-u2/aquecimento/', 'm4/guia-da-tarefa-m4/', 'm4/portefolio-do-modulo-m4/', 'm4/mapa-do-modulo-m4/', 'm4/',
                    'tarefas/m8-u1/', 'tarefas/m8-u1/grelha/', 'm8/guia-da-tarefa-m8/'):
            page.goto(f'{host}/{rel}', wait_until='networkidle')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (rel, largura)
        assert not erros, erros
        ctx.close()
    ctx, page, erros = contexto(browser, 390, 844, 'light')
    page.goto(f'{host}/tarefas/{SLUG}/', wait_until='networkidle')
    principal = page.locator('main').text_content()
    assert principal.count(NAO_CONTAM) == 1 and principal.count('com consulta') == 1
    rotulos = page.evaluate('[...document.querySelectorAll(".task-checklist label")].map(e => e.textContent.trim())')
    assert len(rotulos) <= 10 and all(r.endswith('?') for r in rotulos) and 'Escrevi as duas linhas finais?' in rotulos, rotulos
    assert page.locator('.tf-exemplos .tf-exemplo').count() == 2
    exemplos = page.evaluate('[...document.querySelectorAll(".tf-exemplos")].map(e => e.textContent).join(" ")')
    for fora in ('Telmo', 'Maria', 'Madalena', 'retrato', 'Porta aberta', 'cadeira'):
        assert fora not in exemplos.replace('Não fala de Telmo', ''), fora
    page.goto(f'{host}/tarefas/{SLUG}/aquecimento/', wait_until='networkidle')
    texto = page.locator('body').text_content()
    assert 'alternativa de leitura' not in texto and 'na tua apreciação' not in texto
    page.goto(f'{host}/m4/guia-da-tarefa-m4/', wait_until='networkidle')
    texto = page.locator('body').text_content().replace(N, ' ')
    assert NAO_CONTAM in texto and 'Seguem-se 10 minutos de leitura, 55 de produção em papel e 15 de revisão e entrega no Teams.' in texto
    assert not re.search(r'(?i)síntese|faltaste|autoavaliação|par de trabalho', texto)
    for rel in ('m4/', 'm4/mapa-do-modulo-m4/', 'm4/portefolio-do-modulo-m4/'):
        page.goto(f'{host}/{rel}', wait_until='networkidle')
        texto = page.locator('body').text_content()
        assert 'síntese' not in texto.lower() and 'duas linhas finais' in texto and 'O espetáculo ou Telmo, em Frei Luís de Sousa' in texto, rel
        assert 'trabalho de equipa' not in texto, rel
    page.goto(f'{host}/tarefas/m8-u1/', wait_until='networkidle')
    fontes = page.evaluate('[...document.querySelectorAll(".tt-onde .tt-fonte")].map(e => e.textContent)')
    assert len(fontes) == 4 and all('O poema completo lê-se no manual.' in f for f in fontes), fontes
    assert f'Indica onde leste os poemas: {EDICAO_M8}.' in page.locator('main').text_content()
    page.goto(f'{host}/tarefas/m8-u1/grelha/', wait_until='networkidle')
    assert f'Não indicar onde leste os poemas ({EDICAO_M8}).' in page.locator('body').text_content()
    page.goto(f'{host}/m8/guia-da-tarefa-m8/', wait_until='networkidle')
    assert 'lê os dois poemas de cada tema antes da aula, no manual.' in page.locator('body').text_content()
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
            ecra(host, browser)
            relogios_teclado_e_ligacoes(host, browser)
            paginas = papel(host, browser)
            outras_paginas(host, browser)
            browser.close()
    finally:
        if servidor:
            servidor.shutdown()
    print(f'Tarefa m4-u2 mais fácil de fazer: OK ({SLUG}: {paginas} páginas A4)')


if __name__ == '__main__':
    main()
