"""13/11/2026: as duas tarefas do M5 «mais fáceis de fazer» (camada tarefas_faceis_m5_20261113), no navegador, com o CSS e o motor
reais (o leitor em cartões, os relógios). As mesmas exigências de tests/browser_tarefas_faceis_m3.py e de
tests/browser_tarefas_faceis_m1.py:

* a 390 e a 1280 px, em tema claro e em escuro, nos seis cartões de cada enunciado: a página não desliza para o lado, o cartão não
  transborda e nenhum elemento sai do ecrã (também com todos os desdobráveis abertos); o índice mostra os seis nomes; não há erros
  de página; não há imagens; a grelha, a versão de correção, o aquecimento, o guia da tarefa, o índice, o mapa e o portefólio do M5
  e o portefólio do M3 também não deslizam;
* no guia da tarefa do M5: os quatro blocos somam 90 minutos (10, 10, 55, 15), diz «as duas perguntas», e nas três produções antigas
  não há «Autoavaliação» para copiar para o Teams nem «par de trabalho»: a regra chama-se «Dois antes de mim» e tem dois passos, e o
  que se copia para o Teams traz o plano, as notas e a lista;
* nos portefólios do M5 e do M3 não há autoavaliação de 0 a 20 por parâmetro nem «trabalho de equipa»; no tema B da m3-u2, a página
  diz que os argumentos de IV, 94 e 95 chegam e não remete para o manual;
* os desdobráveis abrem com o teclado (Enter e Espaço no <summary>) e mostram o que guardam: os exemplos com outro caso, o material
  de cada tema (as perguntas de Teresa e os factos, o dossiê, os Textos 4 e 5) e a pergunta opcional;
* o relógio de produção é de 55 minutos («até 55 min», 55:00) e o do aquecimento de 10;
* as ligações internas funcionam: «Texto N» noutro cartão abre esse cartão com o texto à vista; «dossiê» e os textos de um só tema
  abrem o desdobrável que os guarda;
* em papel (A4, margens de 12 mm): os desdobráveis de apoio (.tf-so-ecra: exemplos) e o cartão «Rever a matéria» não saem; o
  material dos temas sai aberto; nenhum parágrafo se parte entre duas páginas; um texto curto sai inteiro numa página, com o
  vocabulário e a fonte; um texto comprido (.tt-longo) pode passar para a página seguinte, só entre parágrafos, com o título na
  página do primeiro parágrafo e o vocabulário e a fonte juntos; o cabeçalho do cartão dos temas sai na página onde começa o que
  vem a seguir; cada enunciado cabe em 8 páginas; a versão de correção cabe numa página.

Uso: python3 tests/browser_tarefas_faceis_m5.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com TAREFAS_FACEIS_M5_OUTPUT, guarda aí as
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

SLUGS = ('m5-u1', 'm5-u2')
LARGURAS = ((390, 844), (1280, 800))
CARTOES = ['Começar', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Fechar e entregar', 'Rever a matéria']
SAIDA = os.environ.get('TAREFAS_FACEIS_M5_OUTPUT')
# Ligações internas a conferir: (cartão de partida, seletor da ligação, alvo, cartão onde o alvo está).
LIGACOES = {
    # 13/11/2026 (revisão): na m5-u1, o Texto 2 (capítulo IV) passa para o cartão da pergunta 1, que pede uma passagem dele: a ligação
    # da pergunta 1 já não leva a outro cartão (antes levava ao cartão 2, sem regresso). A mesma exigência: cada ligação mostra o alvo.
    'm5-u1': [(1, '.tf-pedido a[href="#texto-1"]', '#texto-1', 1), (1, '.tf-pedido a[href="#texto-2"]', '#texto-2', 1),
              (2, '.tf-pedido a[href="#texto-2"]', '#texto-2', 1), (3, '[data-task-theme="A"] .tf-antes a[href="#texto-3"]', '#texto-3', 3),
              (3, '[data-task-theme="A"] .tf-passos a[href="#texto-3"]', '#texto-3', 3), (3, '[data-task-theme="B"] a[href="#texto-1"]', '#texto-1', 1),
              (3, '[data-task-theme="B"] a[href="#texto-2"]', '#texto-2', 1), (3, '[data-task-theme="B"] a[href="#dossie"]', '#dossie', 3)],
    'm5-u2': [(1, '.tf-pedido a[href="#texto-1"]', '#texto-1', 1), (1, '.tf-pedido a[href="#texto-2"]', '#texto-2', 1),
              (2, '.tf-pedido a[href="#texto-3"]', '#texto-3', 2), (3, '[data-task-theme="A"] a[href="#texto-4"]', '#texto-4', 3),
              (3, '[data-task-theme="B"] .tf-antes a[href="#texto-5"]', '#texto-5', 3),
              (3, '[data-task-theme="B"] .tf-passos a[href="#texto-5"]', '#texto-5', 3), (3, '[data-task-theme="B"] a[href="#dossie"]', '#dossie', 3)],
}
# 13/11/2026 (revisão): o Texto 4 da m5-u2 começa pela marca «[2] […]» da lição F11 (mais um parágrafo: 8 em vez de 7).
# O que cada alvo tem de mostrar: os parágrafos do texto e as linhas do seu vocabulário (ou os cinco factos do dossiê).
NO_ALVO = {('m5-u1', '#texto-1'): 7 + 13, ('m5-u1', '#texto-2'): 18 + 14, ('m5-u1', '#texto-3'): 3, ('m5-u1', '#dossie'): 5,
           ('m5-u2', '#texto-1'): 2 + 13, ('m5-u2', '#texto-2'): 3, ('m5-u2', '#texto-3'): 1 + 4, ('m5-u2', '#texto-4'): 8 + 6,
           ('m5-u2', '#texto-5'): 13 + 10, ('m5-u2', '#dossie'): 5}
# Quantos desdobráveis tem cada enunciado: os exemplos (4), o material do tema A, o do tema B e a pergunta opcional.
DESDOBRAVEIS = {'m5-u1': 7, 'm5-u2': 7}
EXEMPLOS = {'m5-u1': 4, 'm5-u2': 4}
# Os textos de cada enunciado, pela ordem da página: (parágrafos, comprido).
TEXTOS = {'m5-u1': [(7, True), (18, True), (3, False)], 'm5-u2': [(2, True), (3, False), (1, False), (8, True), (13, True)]}
# O que sai aberto em papel dentro de cada tema: os parágrafos e os factos do dossiê.
SO_TEMA = {'m5-u1': [3, 5], 'm5-u2': [8, 5 + 13]}
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
            assert page.evaluate('window.EPITaskReader && EPITaskReader.count') == 6, onde
            # O tema pedido é o que se vê (o fundo do cartão muda com o tema).
            fundo = page.evaluate('getComputedStyle(document.body).backgroundColor')
            claro = sum(int(x) for x in re.findall(r'\d+', fundo)[:3]) > 384
            assert claro == (esquema == 'light'), (onde, fundo)
            # O índice mostra os seis nomes, sem números.
            nomes = page.evaluate('[...document.querySelectorAll("[data-task-reader-jump]")].map(b => b.textContent.trim())')
            assert nomes == CARTOES, (onde, nomes)
            for i in range(6):
                ir(page, i)
                m = page.evaluate(MEDIR)
                assert m['nome'] and CARTOES[i] in m['nome'], (onde, i, m['nome'])
                assert m['pagina'] and m['corpo'] and not m['fora'], (onde, CARTOES[i], m)
                # Com todos os desdobráveis do cartão abertos, também nada transborda.
                abertos = page.evaluate('''() => { const ds = [...document.querySelectorAll('.task-reader-card:not([hidden]) details')];
                    ds.forEach(d => d.open = true); return ds.length; }''')
                page.wait_for_timeout(60)
                m = page.evaluate(MEDIR)
                assert m['pagina'] and m['corpo'] and not m['fora'], (onde, CARTOES[i], 'abertos', m)
                if SAIDA and (largura, esquema) in ((390, 'light'), (1280, 'dark')):
                    alto = page.evaluate('document.querySelector(".casca-corpo").scrollHeight + innerHeight - document.querySelector(".casca-corpo").clientHeight')
                    page.set_viewport_size({'width': largura, 'height': min(alto + 2, 15000)})
                    page.wait_for_timeout(100)
                    page.screenshot(path=str(Path(SAIDA) / f'{slug}-{largura}-{"claro" if esquema == "light" else "escuro"}-cartao{i + 1}.png'))
                    page.set_viewport_size({'width': largura, 'height': altura})
                page.evaluate('''() => document.querySelectorAll('.task-reader-card:not([hidden]) details').forEach(d => d.open = false)''')
                assert abertos >= (0 if i in (0, 4) else 1), (onde, CARTOES[i], abertos)
                # As duas tarefas do M5 não têm imagens.
                assert page.locator('.task-reader-card:not([hidden]) img, .task-reader-card:not([hidden]) figure').count() == 0, (onde, CARTOES[i])
            # Os relógios: 10 minutos de aquecimento e 55 de produção.
            ir(page, 0)
            relogio = page.locator('.task-relogio[data-chave$=":aquecimento"]')
            assert relogio.get_attribute('data-max') == '10', onde
            assert '10:00' in relogio.inner_text(), (onde, relogio.inner_text())
            ir(page, 1)
            relogio = page.locator('.task-relogio[data-chave$=":producao"]')
            assert relogio.get_attribute('data-max') == '55', onde
            texto = relogio.inner_text()
            assert 'até 55\xa0min' in texto.replace(' min', '\xa0min') and '55:00' in texto, (onde, texto)
            assert page.locator('.task-relogio').count() == 2, onde
            # O quadro do primeiro cartão: 10, 10, 55, 15 e 90 minutos.
            ir(page, 0)
            tempos = page.locator('.tf-quadro tbody th').all_inner_texts()
            assert [t.replace('\xa0', ' ') for t in tempos] == ['10 min', '10 min', '55 min', '15 min', '90 min'], (onde, tempos)
            assert not erros, (onde, erros)
            ctx.close()
            print('PASS seis cartões sem transbordar, índice e relógios', onde, flush=True)


def teclado(host, browser, slug):
    for largura, altura in LARGURAS:
        onde = f'{slug} {largura}'
        ctx, page, erros = contexto(browser, largura, altura, 'light')
        page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
        total = 0
        for i in range(1, 6):
            ir(page, i)
            n = page.locator('.task-reader-card:not([hidden]) details:not(.info-i) > summary').count()
            for k in range(n):
                s = page.locator('.task-reader-card:not([hidden]) details:not(.info-i) > summary').nth(k)
                d = s.locator('xpath=..')
                assert d.evaluate('e => e.open') is False, (onde, i, k)
                s.focus()
                assert s.evaluate('e => document.activeElement === e'), (onde, i, k)
                page.keyboard.press('Enter' if k % 2 == 0 else 'Space')
                page.wait_for_timeout(60)
                assert d.evaluate('e => e.open') is True, (onde, i, k, 'não abriu com o teclado')
                # O que estava guardado vê-se (tem altura) e cabe na largura.
                assert d.evaluate('e => [...e.children].some(c => c.tagName !== "SUMMARY" && c.getBoundingClientRect().height > 20)'), (onde, i, k)
                m = page.evaluate(MEDIR)
                assert m['pagina'] and m['corpo'] and not m['fora'], (onde, i, k, m)
                # O foco vê-se (contorno) no rótulo.
                assert s.evaluate('e => { const c = getComputedStyle(e); return c.outlineStyle !== "none" && parseFloat(c.outlineWidth) >= 2 }'), (onde, i, k)
                s.focus()
                page.keyboard.press('Enter')
                page.wait_for_timeout(60)
                assert d.evaluate('e => e.open') is False, (onde, i, k, 'não fechou com o teclado')
                total += 1
        assert total == DESDOBRAVEIS[slug], (onde, total)
        # As setas do teclado percorrem os cartões.
        ir(page, 0)
        page.locator('.casca-corpo').focus()
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(120)
        assert page.evaluate('EPITaskReader.current()') == 1, onde
        page.keyboard.press('ArrowLeft')
        page.wait_for_timeout(120)
        assert page.evaluate('EPITaskReader.current()') == 0, onde
        assert not erros, (onde, erros)
        ctx.close()
        print('PASS desdobráveis com o teclado', onde, total, flush=True)


def ligacoes(host, browser, slug):
    for largura, altura in LARGURAS:
        onde = f'{slug} {largura}'
        ctx, page, erros = contexto(browser, largura, altura, 'light')
        for de, seletor, alvo, cartao in LIGACOES[slug]:
            page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
            ir(page, de)
            a = page.locator('.task-reader-card:not([hidden]) ' + seletor)
            assert a.count() == 1, (onde, seletor)
            assert not page.evaluate(VISIVEL, alvo) or cartao == de, (onde, alvo)
            a.focus()
            page.keyboard.press('Enter')
            page.wait_for_timeout(350)
            assert page.evaluate('EPITaskReader.current()') == cartao, (onde, seletor, page.evaluate('EPITaskReader.current()'))
            assert page.evaluate(VISIVEL, alvo), (onde, seletor, 'o alvo não ficou à vista')
            # Um alvo guardado num desdobrável fica com o desdobrável aberto.
            assert page.evaluate('s => { const d = document.querySelector(s).closest("details"); return !d || d.open }', alvo), (onde, alvo)
            # E o alvo tem lá o texto todo: os parágrafos com o vocabulário, ou os factos do dossiê.
            tem = page.evaluate('s => [...document.querySelector(s).closest("section").querySelectorAll(".tt-par, li")].filter(e => e.getClientRects().length).length', alvo)
            assert tem == NO_ALVO[(slug, alvo)], (onde, alvo, tem)
        assert not erros, (onde, erros)
        ctx.close()
        print('PASS ligações internas aos textos e ao dossiê', onde, len(LIGACOES[slug]), flush=True)


def outras_paginas(host, browser):
    for largura, altura in LARGURAS:
        for esquema in ('light', 'dark'):
            ctx, page, erros = contexto(browser, largura, altura, esquema)
            for slug in SLUGS:
                for parte in ('grelha/', 'correcao/', 'aquecimento/'):
                    page.goto(f'{host}/tarefas/{slug}/{parte}', wait_until='networkidle')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (slug, parte, largura)
                corpo = page.locator('body')
                page.goto(f'{host}/tarefas/{slug}/grelha/', wait_until='networkidle')
                assert 'Esta autoavaliação é só para ti: não se entrega.' in corpo.inner_text(), slug
                page.goto(f'{host}/tarefas/{slug}/correcao/', wait_until='networkidle')
                assert page.locator('.g-tab thead th').all_inner_texts() == ['Critério', 'Máx.', 'Docente', 'Observações'], slug
                assert 'Diferença entre a tua nota e a minha' not in corpo.inner_text(), slug
            page.goto(f'{host}/m5/guia-da-tarefa-m5/', wait_until='networkidle')
            page.locator('#arquivo-producoes summary').click()
            page.locator('button.tarefa').first.click()
            page.locator('#rota').wait_for(state='visible')
            assert page.locator('#blocos .bloco b').all_inner_texts() == [
                'Aquecer, 10\xa0min', 'Ler o enunciado, 10\xa0min', 'Produzir, 55\xa0min', 'Rever e entregar, 15\xa0min'], largura
            assert page.locator('#blocos .bloco span').nth(1).inner_text() == 'Lê as duas perguntas e os temas A e B.'
            page.locator('#blocos .bloco button').nth(2).click()
            page.wait_for_timeout(200)
            assert re.match(r'5[45]:\d\d', page.locator('#relogio').inner_text()), page.locator('#relogio').inner_text()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), ('guia', largura)
            # 13/11/2026 (decisão do docente): no guia, a «Autoavaliação» que se copiava para o Teams e «pergunta ao teu par de
            # trabalho» saíram. Em cada uma das três produções antigas: a página abre sem erros, não tem o título nem os botões dos
            # níveis, a regra tem dois passos, e o que se copia para o Teams traz o plano, as notas e a lista, sem autoavaliação.
            page.evaluate('''() => { window.__copiado = null;
                Object.defineProperty(navigator, 'clipboard', { configurable: true,
                    value: { writeText: t => { window.__copiado = t; return Promise.resolve(); } } }); }''')
            for k in range(3):
                page.locator('#voltar').click()
                page.locator('button.tarefa').nth(k).click()
                page.locator('#rota').wait_for(state='visible')
                rota = page.locator('#rota').inner_text()
                assert page.locator('#rota h2').all_inner_texts()[1:] == ['Os blocos de hoje', 'Verificar antes de entregar'], (k, largura)
                assert not re.search(r'(?i)autoavalia|nível que achas|par de trabalho|Três antes de mim', rota), (k, largura)
                regra = page.locator('#rota .regra', has_text='antes de mim')
                assert regra.locator('b').first.inner_text() == 'Dois antes de mim.', (k, largura)
                assert regra.locator('li').all_inner_texts() == ['relê o enunciado;', 'vê a rubrica.'], (k, regra.inner_text())
                assert regra.inner_text().rstrip().endswith('Só depois levantas o braço.'), (k, regra.inner_text())
                assert 'O docente vê o teu plano, as notas e a lista.' in rota, (k, largura)
                assert page.locator('#rota .niveis, #rota [aria-pressed], #rota [data-auto], #r-auto').count() == 0, (k, largura)
                assert page.locator('#r-verificar input[type=checkbox]').count() >= 3, (k, largura)
                assert page.locator('#rota textarea').count() == 2, (k, largura)
                page.locator('#plano').fill('1. Ler. 2. Escrever. 3. Rever.')
                page.locator('#r-verificar input').first.check()
                page.locator('#copiar').click()
                page.wait_for_function('window.__copiado !== null')
                copiado = page.evaluate('window.__copiado')
                page.evaluate('window.__copiado = null')
                linhas = copiado.split('\n')
                assert [x for x in linhas if x.isupper() and not x.startswith('ROTA')] == ['PLANO', 'NOTAS DE TRABALHO', 'VERIFICAÇÃO'], (k, copiado)
                assert '1. Ler. 2. Escrever. 3. Rever.' in linhas and linhas[linhas.index('VERIFICAÇÃO') + 1].startswith('[x] '), (k, copiado)
                assert not re.search(r'(?i)autoavalia|nível', copiado), (k, copiado)
                assert len(linhas) - linhas.index('VERIFICAÇÃO') - 1 == page.locator('#r-verificar input').count(), (k, copiado)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), ('guia, produção antiga', k, largura)
            page.locator('#voltar').click()
            assert 'verificas o trabalho com a lista da rubrica e copias tudo para a tarefa do Teams.' in page.locator('#escolha').inner_text()
            if SAIDA and esquema == 'light':
                page.locator('button.tarefa').first.click()
                page.locator('#rota').wait_for(state='visible')
                page.screenshot(path=str(Path(SAIDA) / f'guia-m5-producao-antiga-{largura}.png'), full_page=True)
            # O índice e o mapa do M5 dizem «duas perguntas» e não deslizam.
            for rel, frase in (('m5/', 'aquecimento em cartões, duas perguntas, tema A ou B, revisão e fotografias no Teams.'),
                               ('m5/mapa-do-modulo-m5/', 'com aquecimento, duas perguntas, tema A ou B e grelha /20;')):
                page.goto(f'{host}/{rel}', wait_until='networkidle')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (rel, largura)
                assert frase in page.content() and 'núcleo comum' not in page.content(), (rel, largura)
            # Os portefólios do M5 e do M3: sem a autoavaliação de 0 a 20 por parâmetro e sem «trabalho de equipa»; a linha do balanço e
            # a lista do que o portefólio serve para avaliar ficam inteiras, e a página não desliza.
            for m in (5, 3):
                page.goto(f'{host}/m{m}/portefolio-do-modulo-m{m}/', wait_until='networkidle')
                lido = page.locator('body').inner_text().replace('\xa0', ' ')
                assert not re.search(r'(?i)auto-?avalia|trabalho de equipa|\bequipas?\b|por parâmetro|\b0 a 20\b', lido), (m, largura)
                assert 'copiado do Percurso do módulo.' in lido, (m, largura)
                assert 'autonomia, responsabilidade, pensamento crítico, entre outros.' in lido, (m, largura)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), ('portefólio', m, largura)
                if SAIDA and esquema == 'light':
                    page.screenshot(path=str(Path(SAIDA) / f'portefolio-m{m}-{largura}.png'), full_page=True)
            # O tema B da m3-u2: os argumentos de IV, 94 e 95 chegam; a página não remete para o manual.
            page.goto(f'{host}/tarefas/m3-u2/', wait_until='networkidle')
            page.evaluate('EPITaskReader.go(3)')
            page.wait_for_timeout(120)
            tema_b = page.locator('[data-task-theme="B"]').inner_text().replace('\xa0', ' ')
            assert 'O Texto 3 tem as estâncias IV, 94 e 95, as mesmas das lições. Os argumentos dessas duas estâncias chegam.' in tema_b, largura
            assert not re.search(r'(?i)\bmanual\b', page.locator('main').inner_text()), largura
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), ('m3-u2', largura)
            assert not erros, erros
            ctx.close()
            print('PASS grelha, correção, aquecimento, guia (sem autoavaliação para o Teams nem par de trabalho), índice, mapa, portefólios e tema B da m3-u2', largura, esquema, flush=True)


def impressao(host, browser, slug):
    ctx = browser.new_context(viewport={'width': 703, 'height': 1000})
    page = ctx.new_page()
    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
    page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
    page.emulate_media(media='print')
    page.wait_for_timeout(200)
    # Os desdobráveis de apoio e o cartão «Rever a matéria» não saem; o material de um só tema sai aberto, sem depender de JavaScript.
    apoio = page.evaluate('''() => [...document.querySelectorAll('.tf-so-ecra, .tf-rever, .task-relogio, .tf-imprimir, .task-grelha')]
        .filter(e => e.getClientRects().length).map(e => e.className)''')
    assert not apoio, (slug, apoio)
    assert page.locator('details.tf-exemplos').count() == EXEMPLOS[slug], slug
    so_tema = page.evaluate('''() => [...document.querySelectorAll('details.tf-so-tema:not(.tf-so-ecra)')]
        .map(d => [...d.querySelectorAll('.tt-l, .tt-par, .tf-dossie li')].filter(e => e.getClientRects().length).length)''')
    assert so_tema == SO_TEMA[slug], (slug, so_tema)
    assert page.evaluate('''() => [...document.querySelectorAll('details.tf-so-tema:not(.tf-so-ecra)')].every(d => !d.open)'''), slug
    # Todos os textos e todas as perguntas saem.
    textos = page.evaluate('[...document.querySelectorAll(".tt-texto")].filter(e => e.getClientRects().length).length')
    assert textos == len(TEXTOS[slug]), (slug, textos)
    # Todos os parágrafos de todos os textos saem (m5-u1: 28; m5-u2: 26), e os textos compridos são os que a página marca.
    versos = page.evaluate('[...document.querySelectorAll(".tt-l")].filter(e => e.getClientRects().length).length')
    paragrafos = page.evaluate('[...document.querySelectorAll(".tt-texto")].map(t => [[...t.querySelectorAll(".tt-par")].filter(e => e.getClientRects().length).length, t.classList.contains("tt-longo")])')
    assert versos == 0 and [tuple(x) for x in paragrafos] == TEXTOS[slug], (slug, versos, paragrafos)
    assert page.locator('img, figure').count() == 0, slug
    assert page.evaluate('[...document.querySelectorAll(".task-checklist label")].filter(e => e.getClientRects().length).length') == 10, slug
    pdf = page.pdf(format='A4', print_background=False, margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
    if SAIDA:
        (Path(SAIDA) / f'{slug}-impressao.pdf').write_bytes(pdf)
    paginas = len(re.findall(rb'/Type\s*/Page\b', pdf))
    assert 3 <= paginas <= 8, (slug, paginas)
    # Nenhum parágrafo se parte entre duas páginas: no PDF, cada parágrafo está inteiro numa página. Um texto curto sai todo na mesma
    # página, com o vocabulário e a fonte. Um texto comprido pode passar para a página seguinte (só entre parágrafos): as suas
    # páginas são seguidas, o título fica na página do primeiro parágrafo e o vocabulário e a fonte ficam juntos, na última.
    try:
        from pypdf import PdfReader
        import io
        # (sem espaços nem hífenes: a extração do PDF parte as linhas da prosa onde o papel as parte)
        junto = lambda x: re.sub(r'[\s\-]+', '', x)
        folhas = [junto(p.extract_text() or '') for p in PdfReader(io.BytesIO(pdf)).pages]
        blocos = page.evaluate("""() => [...document.querySelectorAll('.tt-texto')].map(t => ({
            titulo: t.querySelector('.tt-num').textContent, cabeca: t.querySelector('h3').textContent, fonte: t.querySelector('.tt-fonte').textContent,
            longo: t.classList.contains('tt-longo'), vocabulario: [...t.querySelectorAll('.tt-gloss li')].map(e => e.textContent),
            paragrafos: [...t.querySelectorAll('.tt-par')].map(e => e.textContent) }))""")
        # (os textos saem pela ordem da página, e há parágrafos que aparecem em dois textos: na m5-u2, o olhar final ao Ramalhete
        # está no Texto 2 e no Texto 5; por isso cada parágrafo procura-se a partir de onde o anterior acabou)
        k, pos = 0, 0
        for b in blocos:
            onde = []
            for paragrafo in b['paragrafos']:
                alvo, achado = junto(paragrafo), None
                for kk in range(k, len(folhas)):
                    i = folhas[kk].find(alvo, pos if kk == k else 0)
                    if i >= 0:
                        achado = (kk, i)
                        break
                # o parágrafo inteiro (letra a letra, sem contar espaços) está numa só página
                assert achado, (slug, b['titulo'], paragrafo[:40], 'parágrafo partido entre páginas')
                k, pos = achado[0], achado[1] + len(alvo)
                onde.append(k)
            assert onde == sorted(onde) and set(onde) == set(range(onde[0], onde[-1] + 1)), (slug, b['titulo'], onde)
            if not b['longo']:
                assert len(set(onde)) == 1, (slug, b['titulo'], sorted(set(onde)), 'texto curto partido entre páginas')
            assert junto(b['cabeca']) in folhas[onde[0]], (slug, b['titulo'], 'o título ficou longe do primeiro parágrafo')
            ultima = [kk for kk in range(onde[-1], min(onde[-1] + 2, len(folhas))) if junto(b['fonte']) in folhas[kk]]
            assert ultima, (slug, b['titulo'], 'a linha de fonte ficou longe do texto')
            assert all(junto(v) in folhas[ultima[0]] for v in b['vocabulario']), (slug, b['titulo'], 'o vocabulário ficou longe da fonte')
            if not b['longo']:
                assert ultima[0] == onde[0], (slug, b['titulo'], 'a fonte de um texto curto ficou noutra página')
        # O cabeçalho do cartão dos temas («Escolhe um tema», a orientação e «Escreve a letra do teu tema») não fica sozinho no fundo
        # de uma página: sai na página onde começa o tema A, com as margens de 12 mm e sem margens.
        topo = page.evaluate("""() => ({ titulo: document.querySelector('#tema-titulo').textContent, topo: document.querySelector('.tf-topo').textContent,
            a_seguir: document.querySelector('.task-theme .tf-passos li').textContent })""")
        for nome, doc in (('12 mm', pdf), ('sem margens', page.pdf(format='A4', print_background=False))):
            fs = [junto(p.extract_text() or '') for p in PdfReader(io.BytesIO(doc)).pages]
            pag = [kk for kk, f in enumerate(fs) if junto(topo['topo']) in f]
            assert len(pag) == 1 and junto(topo['titulo']) in fs[pag[0]], (slug, nome, pag)
            assert junto(topo['a_seguir'])[:40] in fs[pag[0]], (slug, nome, pag, 'o cabeçalho dos temas ficou sozinho no fundo da página')
        partido = 'conferido no PDF'
    except ImportError:
        # Sem pypdf (o fluxo só instala o Playwright): conferem-se as regras que o impedem, tal como o navegador as aplica.
        regras = page.evaluate('''() => [...document.querySelectorAll('.tt-texto:not(.tt-longo), .tt-par, .tt-gloss')].map(e => getComputedStyle(e).breakInside)''')
        assert regras and all(r == 'avoid' for r in regras), (slug, regras)
        longos = page.evaluate('''() => [...document.querySelectorAll('.tt-texto.tt-longo')].map(e => [getComputedStyle(e).breakInside,
            getComputedStyle(e.querySelector('h3')).breakAfter, getComputedStyle(e.querySelector('.tt-fonte')).breakBefore])''')
        assert longos and all(x == ['auto', 'avoid', 'avoid'] for x in longos), (slug, longos)
        assert page.evaluate('''() => getComputedStyle(document.querySelector('.tf-topo')).breakAfter''') == 'avoid', slug
        partido = 'conferido nas regras de impressão'
    ctx.close()
    print(f'PASS impressão: {paginas} páginas A4, apoio fora do papel, nenhum parágrafo partido ({partido})', slug, flush=True)
    # A versão de correção cabe numa página (sem a coluna «Aluno» nem a nota da diferença).
    ctx = browser.new_context(viewport={'width': 703, 'height': 1000})
    page = ctx.new_page()
    page.goto(f'{host}/tarefas/{slug}/correcao/', wait_until='networkidle')
    page.emulate_media(media='print')
    assert page.evaluate("[...document.querySelectorAll('.g-tab thead th')].every(t=>t.scrollWidth<=t.clientWidth)"), slug
    pdf = page.pdf(format='A4', prefer_css_page_size=True)
    assert len(re.findall(rb'/Type\s*/Page\b', pdf)) == 1, slug
    ctx.close()
    print('PASS correção numa página A4', slug, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url')
    args = ap.parse_args()
    server = None
    host = args.url
    if not host:
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        host = f'http://127.0.0.1:{server.server_port}'
    if SAIDA:
        Path(SAIDA).mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for slug in SLUGS:
                ecra(host, browser, slug)
                teclado(host, browser, slug)
                ligacoes(host, browser, slug)
                impressao(host, browser, slug)
            outras_paginas(host, browser)
            browser.close()
    finally:
        if server:
            server.shutdown()
    print('PASS tarefas do M5 mais fáceis de fazer', flush=True)


if __name__ == '__main__':
    main()
