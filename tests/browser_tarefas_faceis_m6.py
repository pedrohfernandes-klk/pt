"""13/11/2026: as duas tarefas do M6 «mais fáceis de fazer» (camada tarefas_faceis_m6_20261113), no navegador, com o CSS e o motor
reais (o leitor em cartões, os relógios). As mesmas exigências de tests/browser_tarefas_faceis_m3.py, de
tests/browser_tarefas_faceis_m1.py e de tests/browser_tarefas_faceis_m5.py:

* a 390 e a 1280 px, em tema claro e em escuro, nos seis cartões de cada enunciado: a página não desliza para o lado, o cartão não
  transborda e nenhum elemento sai do ecrã (também com todos os desdobráveis abertos); o índice mostra os seis nomes; não há erros
  de página; não há imagens; a grelha, a versão de correção, o aquecimento, o guia da tarefa, o índice, o mapa e o portefólio do M6
  também não deslizam;
* no guia da tarefa do M6: os quatro blocos somam 90 minutos (10, 10, 55, 15), diz «as duas perguntas», e nas três produções antigas
  não há «Autoavaliação» para copiar para o Teams nem «par de trabalho»: a regra chama-se «Dois antes de mim» e tem dois passos, e o
  que se copia para o Teams traz o plano, as notas e a lista;
* no portefólio do M6 não há autoavaliação de 0 a 20 por parâmetro nem «trabalho de equipa»;
* os desdobráveis abrem com o teclado (Enter e Espaço no <summary>) e mostram o que guardam: os exemplos com outro caso, o material
  dos temas (o dossiê, «O Palacio da Ventura», as quatro partes de «O Sentimento dum Ocidental») e a pergunta opcional;
* o relógio de produção é de 55 minutos («até 55 min», 55:00) e o do aquecimento de 10;
* as ligações internas funcionam: «Texto N» noutro cartão abre esse cartão com o texto à vista; «dossiê» e os textos dos temas
  abrem o desdobrável que os guarda, e o alvo tem lá todos os versos e todo o vocabulário;
* o que as lições não dão vê-se: o verso 13 de «A um poeta» sai como «[…]» e o verso seguinte é o 14; os dois cortes de «Ao Gás»
  saem como «[…]», sem número, e os excertos de «Ao Gás» (Texto 5 da m6-u2) não levam número nenhum (revisão de 13/11/2026: com
  estrofes saltadas, o número contado por cima dos cortes não era o número do verso na parte);
* em papel (A4, margens de 12 mm): os desdobráveis de apoio (.tf-so-ecra: exemplos) e o cartão «Rever a matéria» não saem; o
  material dos temas sai aberto; nenhum texto e nenhuma estrofe se parte entre duas páginas (cada soneto, cada estrofe e cada
  parte de 44 versos sai inteira numa página, com o vocabulário e a fonte); o cabeçalho do cartão dos temas sai na página onde
  começa o tema A; os passos de cada tema saem todos na mesma página, e os seis factos do dossiê também (revisão de 13/11/2026);
  a m6-u1 cabe em 8 páginas e a m6-u2, que leva as quatro partes do poema (152 versos), em 9; a versão de correção
  cabe numa página.

Uso: python3 tests/browser_tarefas_faceis_m6.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com TAREFAS_FACEIS_M6_OUTPUT, guarda aí as
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

SLUGS = ('m6-u1', 'm6-u2')
LARGURAS = ((390, 844), (1280, 800))
CARTOES = ['Começar', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Fechar e entregar', 'Rever a matéria']
SAIDA = os.environ.get('TAREFAS_FACEIS_M6_OUTPUT')
# Ligações internas a conferir: (cartão de partida, seletor da ligação, alvo, cartão onde o alvo está).
LIGACOES = {
    'm6-u1': [(1, '.tf-pedido a[href="#texto-1"]', '#texto-1', 1), (1, '.tf-pedido a[href="#texto-2"]', '#texto-2', 1),
              (2, '.tf-pedido a[href="#texto-3"]', '#texto-3', 2), (3, '[data-task-theme="A"] a[href="#texto-4"]', '#texto-4', 3),
              (3, '[data-task-theme="B"] .tf-antes a[href="#texto-4"]', '#texto-4', 3), (3, '[data-task-theme="B"] a[href="#dossie"]', '#dossie', 3)],
    'm6-u2': [(1, '.tf-pedido a[href="#texto-1"]', '#texto-1', 1), (1, '.tf-pedido a[href="#texto-2"]', '#texto-2', 1),
              (1, '#texto-1 a[href="#texto-5"]', '#texto-5', 3), (1, '#texto-2 a[href="#texto-6"]', '#texto-6', 3),
              (3, '[data-task-theme="A"] a[href="#texto-3"]', '#texto-3', 3), (3, '[data-task-theme="B"] a[href="#texto-3"]', '#texto-3', 3),
              (3, '[data-task-theme="B"] a[href="#dossie"]', '#dossie', 3)],
}
# O que cada alvo tem de mostrar: as linhas do texto (os versos e as marcas «[…]») e as linhas do seu vocabulário (ou os seis factos
# do dossiê).
NO_ALVO = {('m6-u1', '#texto-1'): 14 + 4, ('m6-u1', '#texto-2'): 14 + 4, ('m6-u1', '#texto-3'): 4 + 2, ('m6-u1', '#texto-4'): 14 + 6,
           ('m6-u1', '#dossie'): 6,
           ('m6-u2', '#texto-1'): 4 + 3, ('m6-u2', '#texto-2'): 4 + 2, ('m6-u2', '#texto-3'): 44 + 25, ('m6-u2', '#texto-5'): 22 + 13,
           ('m6-u2', '#texto-6'): 44 + 21, ('m6-u2', '#dossie'): 6}
# Quantos desdobráveis tem cada enunciado: os exemplos (4), o material do tema B, o dos dois temas e a pergunta opcional.
DESDOBRAVEIS = {'m6-u1': 7, 'm6-u2': 7}
EXEMPLOS = {'m6-u1': 4, 'm6-u2': 4}
# Os textos de cada enunciado, pela ordem da página: (linhas, das quais marcas «[…]», sai inteiro numa página própria de letra menor).
TEXTOS = {'m6-u1': [(14, 0, False), (14, 1, False), (4, 0, False), (14, 0, False)],
          'm6-u2': [(4, 0, False), (4, 0, False), (44, 0, True), (44, 0, True), (22, 2, False), (44, 0, True)]}
# O que sai aberto em papel em cada desdobrável dos temas: os factos do dossiê (tema B) e as linhas dos textos dos dois temas.
SO_TEMA = {'m6-u1': [6, 14], 'm6-u2': [6, 44 + 44 + 22 + 44]}
# As páginas A4 de cada enunciado. A m6-u1 cabe em 8, como as tarefas do M3, do M1 e do M5. A m6-u2 leva em papel as quatro partes de
# «O Sentimento dum Ocidental» que o tema B manda escolher (152 versos das lições): cada parte de 44 versos sai inteira na sua página,
# para não se partir um poema, e por isso o enunciado pode ter 9 páginas.
MAX_PAGINAS = {'m6-u1': 8, 'm6-u2': 9}
# O que as lições não dão: (texto, linha da marca, número que a linha seguinte mostra ou None, linhas numeradas do texto).
# 13/11/2026: revisão. Os excertos de «Ao Gás» não levam números (a linha a seguir ao primeiro corte já não mostra «5»).
FALTA = {'m6-u1': [('#texto-2', 12, None, ['5', '10'])], 'm6-u2': [('#texto-5', 4, None, None), ('#texto-5', 13, None, None)]}
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
            # O que as lições não dão vê-se: «[…]» no lugar do verso que falta (conta para a numeração) e nos cortes (sem número).
            for texto, linha, seguinte, _ in FALTA[slug]:
                marca = page.evaluate("""([t, k]) => { const vs = [...document.querySelectorAll(t + ' .tt-v')]; const v = vs[k];
                    return { falta: v.classList.contains('tt-falta'), l: v.querySelector('.tt-l').textContent, n: v.querySelector('.tt-n').textContent,
                             faltas: vs.filter(x => x.classList.contains('tt-falta')).length }; }""", [texto, linha])
                assert marca['falta'] and marca['l'] == '[…]' and marca['n'] == '', (onde, texto, linha, marca)
            if slug == 'm6-u1':
                # «A um poeta»: 14 linhas (13 versos e a marca do verso 13); os números 5 e 10 estão nos versos certos.
                numeros = page.evaluate("""() => [...document.querySelectorAll('#texto-2 .tt-v')].map(v => [v.querySelector('.tt-n').textContent, v.querySelector('.tt-l').textContent])""")
                assert len(numeros) == 14 and [n for n, _ in numeros if n] == ['5', '10'], (onde, numeros)
                assert numeros[4][0] == '5' and numeros[9][0] == '10' and numeros[13][1] == 'Sonhador, faze espada de combate!', (onde, numeros)
            else:
                # 13/11/2026: revisão. «Ao Gás» (excertos): 22 linhas (20 versos e os dois cortes), nenhuma com número. Antes, os números
                # 5, 10, 15 e 20 contavam-se por cima dos cortes e não eram os números dos versos na parte. As partes inteiras
                # (Textos 3, 4 e 6) numeram-se de 5 em 5, de 5 a 40, e a nota por cima dos textos di-lo.
                numeros = page.evaluate("""() => [...document.querySelectorAll('#texto-5 .tt-v')].map(v => [v.querySelector('.tt-n').textContent, v.querySelector('.tt-l').textContent])""")
                assert len(numeros) == 22 and not [n for n, _ in numeros if n], (onde, numeros)
                assert numeros[5] == ['', "N'um cutileiro, de avental, ao torno,"], (onde, numeros[5])
                for t in ('#texto-3', '#texto-4', '#texto-6'):
                    ns = page.evaluate("""(t) => [...document.querySelectorAll(t + ' .tt-n')].map(e => e.textContent).filter(x => x)""", t)
                    assert ns == [str(k) for k in range(5, 45, 5)], (onde, t, ns)
                nota = page.evaluate("""() => document.querySelector('details.tf-dois-temas .tf-p').textContent""")
                assert nota == ('Nos Textos\xa03, 4\xa0e\xa06, os versos numeram-se a partir de\xa01 em cada parte. '
                                'O Texto\xa05 não tem números, porque lhe faltam estrofes.'), (onde, nota)
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
                # As duas tarefas do M6 não têm imagens.
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
            # E o alvo tem lá o texto todo: os versos com o vocabulário, ou os factos do dossiê.
            tem = page.evaluate('s => [...document.querySelector(s).closest("section").querySelectorAll(".tt-l, li")].filter(e => e.getClientRects().length).length', alvo)
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
            page.goto(f'{host}/m6/guia-da-tarefa-m6/', wait_until='networkidle')
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
                # (no guia do M6 os passos da regra vão na mesma linha: «1) …; 2) ….»)
                assert regra.inner_text().strip() == ('Dois antes de mim. Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica. '
                                                      'Só depois levantas o braço.'), (k, regra.inner_text())
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
                page.screenshot(path=str(Path(SAIDA) / f'guia-m6-producao-antiga-{largura}.png'), full_page=True)
            # O índice e o mapa do M6 dizem «duas perguntas» e não deslizam.
            for rel, frase in (('m6/', 'aquecimento em cartões, duas perguntas, tema A ou B, revisão e fotografias no Teams.'),
                               ('m6/mapa-do-modulo-m6/', 'com aquecimento, duas perguntas, tema A ou B e grelha')):
                page.goto(f'{host}/{rel}', wait_until='networkidle')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (rel, largura)
                assert frase in page.content() and 'núcleo comum' not in page.content(), (rel, largura)
            # O portefólio do M6: sem a autoavaliação de 0 a 20 por parâmetro e sem «trabalho de equipa»; a linha do balanço e a lista
            # do que o portefólio serve para avaliar ficam inteiras, e a página não desliza.
            page.goto(f'{host}/m6/portefolio-do-modulo-m6/', wait_until='networkidle')
            lido = page.locator('body').inner_text().replace('\xa0', ' ')
            assert not re.search(r'(?i)auto-?avalia|trabalho de equipa|\bequipas?\b|por parâmetro|\b0 a 20\b', lido), largura
            assert 'copiado do Percurso do módulo.' in lido, largura
            assert 'autonomia, responsabilidade, pensamento crítico, entre outros.' in lido, largura
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), ('portefólio', largura)
            if SAIDA and esquema == 'light':
                page.screenshot(path=str(Path(SAIDA) / f'portefolio-m6-{largura}.png'), full_page=True)
            assert not erros, erros
            ctx.close()
            print('PASS grelha, correção, aquecimento, guia (sem autoavaliação para o Teams nem par de trabalho), índice, mapa e portefólio', largura, esquema, flush=True)


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
        .map(d => [...d.querySelectorAll('.tt-l, .tf-dossie li')].filter(e => e.getClientRects().length).length)''')
    assert so_tema == SO_TEMA[slug], (slug, so_tema)
    assert page.evaluate('''() => [...document.querySelectorAll('details.tf-so-tema:not(.tf-so-ecra)')].every(d => !d.open)'''), slug
    # Todos os textos e todas as perguntas saem.
    textos = page.evaluate('[...document.querySelectorAll(".tt-texto")].filter(e => e.getClientRects().length).length')
    assert textos == len(TEXTOS[slug]), (slug, textos)
    # Todas as linhas de todos os textos saem (os versos e as marcas «[…]»), e as partes de 44 versos são as que a página marca.
    linhas = page.evaluate('[...document.querySelectorAll(".tt-texto")].map(t => [[...t.querySelectorAll(".tt-l")].filter(e => e.getClientRects().length).length, t.querySelectorAll(".tt-falta").length, t.classList.contains("tt-pagina")])')
    assert [tuple(x) for x in linhas] == TEXTOS[slug], (slug, linhas)
    assert page.locator('.tt-par, .tt-prosa').count() == 0, slug
    assert page.locator('img, figure').count() == 0, slug
    assert page.evaluate('[...document.querySelectorAll(".task-checklist label")].filter(e => e.getClientRects().length).length') == 10, slug
    # 13/11/2026: revisão. Os passos de cada tema e os factos do dossiê não se partem entre duas páginas (classe tf-juntos): a regra,
    # tal como o navegador a aplica; mais abaixo, confere-se no PDF.
    juntos = page.evaluate("""() => [...document.querySelectorAll('.task-theme > ol.tf-passos, .tf-dossie')].map(e => [e.classList.contains('tf-juntos'), getComputedStyle(e).breakInside])""")
    assert juntos == [[True, 'avoid']] * 3, (slug, juntos)
    pdf = page.pdf(format='A4', print_background=False, margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
    if SAIDA:
        (Path(SAIDA) / f'{slug}-impressao.pdf').write_bytes(pdf)
    paginas = len(re.findall(rb'/Type\s*/Page\b', pdf))
    assert 3 <= paginas <= MAX_PAGINAS[slug], (slug, paginas)
    # Nenhum texto e nenhuma estrofe se parte entre duas páginas: no PDF, cada texto (título, versos, vocabulário e fonte) está
    # inteiro numa só página. Vale para os sonetos, para as estrofes soltas e para as partes de 44 versos (.tt-pagina).
    try:
        from pypdf import PdfReader
        import io
        junto = lambda x: re.sub(r'[\s\-]+', '', x)
        folhas = [junto(p.extract_text() or '') for p in PdfReader(io.BytesIO(pdf)).pages]
        blocos = page.evaluate("""() => [...document.querySelectorAll('.tt-texto')].map(t => ({
            titulo: t.querySelector('.tt-num').textContent, cabeca: t.querySelector('h3').textContent, fonte: t.querySelector('.tt-fonte').textContent,
            vocabulario: [...t.querySelectorAll('.tt-gloss li')].map(e => e.textContent),
            estrofes: [...t.querySelectorAll('.tt-estrofe')].map(e => [...e.querySelectorAll('.tt-l')].map(v => v.textContent)) }))""")
        # (os textos saem pela ordem da página, e há estrofes que aparecem em dois textos: na m6-u2, a estrofe do Texto 1 está também
        # no Texto 5 e a do Texto 2 no Texto 6; por isso cada verso procura-se a partir de onde o anterior acabou)
        k, pos = 0, 0
        for b in blocos:
            onde = []
            for estrofe in b['estrofes']:
                desta = []
                for verso in estrofe:
                    alvo, achado = junto(verso), None
                    for kk in range(k, len(folhas)):
                        i = folhas[kk].find(alvo, pos if kk == k else 0)
                        if i >= 0:
                            achado = (kk, i)
                            break
                    assert achado, (slug, b['titulo'], verso, 'verso que não saiu')
                    k, pos = achado[0], achado[1] + len(alvo)
                    desta.append(k)
                assert len(set(desta)) == 1, (slug, b['titulo'], estrofe[0], 'estrofe partida')
                onde.append(desta[0])
            assert len(set(onde)) == 1, (slug, b['titulo'], sorted(set(onde)), 'texto partido entre páginas')
            assert junto(b['cabeca']) in folhas[onde[0]], (slug, b['titulo'], 'o título ficou noutra página')
            assert junto(b['fonte']) in folhas[onde[0]], (slug, b['titulo'], 'a linha de fonte ficou noutra página')
            assert all(junto(v) in folhas[onde[0]] for v in b['vocabulario']), (slug, b['titulo'], 'o vocabulário ficou noutra página')
        # O cabeçalho do cartão dos temas («Escolhe um tema», a orientação e «Escreve a letra do teu tema») não fica sozinho no fundo
        # de uma página: sai na página onde começa o tema A, com as margens de 12 mm e sem margens.
        topo = page.evaluate("""() => ({ titulo: document.querySelector('#tema-titulo').textContent, topo: document.querySelector('.tf-topo').textContent,
            a_seguir: document.querySelector('.task-theme .tf-passos li').textContent })""")
        for nome, doc in (('12 mm', pdf), ('sem margens', page.pdf(format='A4', print_background=False))):
            fs = [junto(p.extract_text() or '') for p in PdfReader(io.BytesIO(doc)).pages]
            pag = [kk for kk, f in enumerate(fs) if junto(topo['topo']) in f]
            assert len(pag) == 1 and junto(topo['titulo']) in fs[pag[0]], (slug, nome, pag)
            assert junto(topo['a_seguir'])[:40] in fs[pag[0]], (slug, nome, pag, 'o cabeçalho dos temas ficou sozinho no fundo da página')
        # 13/11/2026: revisão. No PDF, com as margens de 12 mm e sem margens: os passos de cada tema estão todos na mesma página (com a
        # frase que os apresenta), e os seis factos do dossiê também (com o título do dossiê).
        grupos = page.evaluate("""() => [...document.querySelectorAll('.task-theme')].map(a => ({ nome: 'tema ' + a.dataset.taskTheme,
            itens: [a.querySelector('.tf-p').textContent, ...[...a.querySelectorAll(':scope > ol.tf-passos > li')].map(e => e.textContent)] }))
            .concat([{ nome: 'dossiê', itens: [document.querySelector('#dossie').textContent,
                       ...[...document.querySelectorAll('.tf-dossie li')].map(e => e.textContent)] }])""")
        assert [len(g['itens']) for g in grupos] == [len(page.query_selector_all(f'[data-task-theme="{x}"] > ol.tf-passos > li')) + 1 for x in 'AB'] + [7], (slug, grupos)
        for nome, doc in (('12 mm', pdf), ('sem margens', page.pdf(format='A4', print_background=False))):
            fs = [junto(p.extract_text() or '') for p in PdfReader(io.BytesIO(doc)).pages]
            for g in grupos:
                pags = [[kk for kk, f in enumerate(fs) if junto(x) in f] for x in g['itens']]
                assert all(len(x) == 1 for x in pags) and len({x[0] for x in pags}) == 1, (slug, nome, g['nome'], pags, 'partido entre páginas')
        partido = 'conferido no PDF'
    except ImportError:
        # Sem pypdf (o fluxo só instala o Playwright): conferem-se as regras que o impedem, tal como o navegador as aplica, e que
        # cada texto cabe na altura útil de uma página A4 com margens de 12 mm (273 mm).
        regras = page.evaluate("""() => [...document.querySelectorAll('.tt-texto, .tt-estrofe, .tt-gloss')].map(e => getComputedStyle(e).breakInside)""")
        assert regras and all(r == 'avoid' for r in regras), (slug, regras)
        alturas = page.evaluate("""() => [...document.querySelectorAll('.tt-texto')].map(e => e.getBoundingClientRect().height)""")
        assert all(a <= 273 / 25.4 * 96 for a in alturas), (slug, alturas)
        assert page.evaluate("""() => getComputedStyle(document.querySelector('.tf-topo')).breakAfter""") == 'avoid', slug
        partido = 'conferido nas regras de impressão'
    ctx.close()
    print(f'PASS impressão: {paginas} páginas A4, apoio fora do papel, nenhum texto nem estrofe partidos ({partido})', slug, flush=True)
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
    print('PASS tarefas do M6 mais fáceis de fazer', flush=True)


if __name__ == '__main__':
    main()
