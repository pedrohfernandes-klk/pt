"""12/11/2026: as duas tarefas do M3 «mais fáceis de fazer» (camada tarefas_faceis_m3_20261112), no navegador, com o CSS e o motor
reais (o leitor em cartões, os relógios, a peça «i»).

* a 390 e a 1280 px, em tema claro e em escuro, nos seis cartões de cada enunciado: a página não desliza para o lado, o cartão não
  transborda e nenhum elemento sai do ecrã (também com todos os desdobráveis abertos); o índice mostra os seis nomes; não há erros
  de página; a grelha, a versão de correção, o aquecimento e o guia da tarefa do M3 também não deslizam;
* 13/11/2026 (decisão do docente): no guia da tarefa do M3, nas três produções antigas, não há «Autoavaliação» nem botões de nível,
  a regra antes de chamar o docente tem dois passos (sem «par de trabalho») e o que se copia para o Teams traz só o plano, as notas
  e a lista de verificação;
* os desdobráveis abrem com o teclado (Enter e Espaço no <summary>) e mostram o que guardam: os exemplos com outro caso, o material
  que é só de um tema, as descrições do Kit (m3-u1), o quadro das modalidades (m3-u2) e a pergunta opcional;
* o relógio de produção é de 55 minutos («até 55 min», 55:00) e o do aquecimento de 10; os blocos do guia somam 10, 10, 55 e 15;
* as ligações internas funcionam: «Texto N» noutro cartão abre esse cartão com o texto à vista; «dossiê» e o texto que é só do
  tema B abrem o desdobrável que os guarda;
* em papel (A4, margens de 12 mm): os desdobráveis de apoio (.tf-so-ecra: exemplos, descrições, quadro) e o cartão «Rever a
  matéria» não saem; o material de um só tema sai aberto; nenhum texto e nenhuma estrofe se parte entre duas páginas; o cabeçalho
  do cartão dos temas sai na página onde começa o tema A; cada enunciado cabe em 8 páginas; a versão de correção cabe numa página.

Uso: python3 tests/browser_tarefas_faceis_m3.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com TAREFAS_FACEIS_M3_OUTPUT, guarda aí as
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

SLUGS = ('m3-u1', 'm3-u2')
LARGURAS = ((390, 844), (1280, 800))
CARTOES = ['Começar', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Fechar e entregar', 'Rever a matéria']
SAIDA = os.environ.get('TAREFAS_FACEIS_M3_OUTPUT')
# Ligações internas a conferir: (cartão de partida, seletor da ligação, alvo, cartão onde o alvo está).
LIGACOES = {
    'm3-u1': [(3, '[data-task-theme="A"] a[href="#texto-2"]', '#texto-2', 2), (3, '[data-task-theme="B"] a[href="#texto-1"]', '#texto-1', 1),
              (3, '[data-task-theme="B"] a[href="#dossie"]', '#dossie', 3), (3, '[data-task-theme="B"] a[href="#texto-4"]', '#texto-4', 3)],
    'm3-u2': [(2, '.tf-pedido a[href="#texto-1"]', '#texto-1', 1), (2, '.tf-pedido a[href="#texto-2"]', '#texto-2', 2),
              (3, '[data-task-theme="A"] a[href="#texto-2"]', '#texto-2', 2), (3, '[data-task-theme="B"] a[href="#texto-3"]', '#texto-3', 3),
              (3, '[data-task-theme="B"] a[href="#dossie"]', '#dossie', 3)],
}
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
        # m3-u1: exemplos (4), tema B, Kit e opcional; m3-u2: exemplos (4), quadro das modalidades, tema B e opcional.
        assert total == 7, (onde, total)
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
            # E o alvo tem lá o texto: versos, ou os factos do dossiê.
            assert page.evaluate('s => document.querySelector(s).closest("section").querySelectorAll(".tt-l, li").length >= 5', alvo), (onde, alvo)
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
            page.goto(f'{host}/m3/guia-da-tarefa-m3/', wait_until='networkidle')
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
                assert 'Dois antes de mim. Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica. Só depois levantas o braço.' in rota, (k, rota)
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
                page.screenshot(path=str(Path(SAIDA) / f'guia-m3-producao-antiga-{largura}.png'), full_page=True)
            assert not erros, erros
            ctx.close()
            print('PASS grelha, correção, aquecimento e guia (sem autoavaliação para o Teams nem par de trabalho)', largura, esquema, flush=True)


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
    assert page.locator('details.tf-exemplos').count() == 4, slug
    so_tema = page.evaluate('''() => [...document.querySelectorAll('details.tf-so-tema:not(.tf-so-ecra)')]
        .map(d => [...d.querySelectorAll('.tt-l, .tf-dossie li')].filter(e => e.getClientRects().length).length)''')
    assert so_tema and all(n >= 5 for n in so_tema), (slug, so_tema)
    assert page.evaluate('''() => [...document.querySelectorAll('details.tf-so-tema:not(.tf-so-ecra)')].every(d => !d.open)'''), slug
    # Todos os textos e todas as perguntas saem.
    textos = page.evaluate('[...document.querySelectorAll(".tt-texto")].filter(e => e.getClientRects().length).length')
    assert textos == (4 if slug == 'm3-u1' else 3), (slug, textos)
    versos = page.evaluate('[...document.querySelectorAll(".tt-l")].filter(e => e.getClientRects().length).length')
    assert versos == (71 if slug == 'm3-u1' else 72), (slug, versos)
    assert page.evaluate('[...document.querySelectorAll(".task-checklist label")].filter(e => e.getClientRects().length).length') in (9, 10), slug
    pdf = page.pdf(format='A4', print_background=False, margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
    if SAIDA:
        (Path(SAIDA) / f'{slug}-impressao.pdf').write_bytes(pdf)
    paginas = len(re.findall(rb'/Type\s*/Page\b', pdf))
    assert 3 <= paginas <= 8, (slug, paginas)
    # Nenhum texto e nenhuma estrofe se parte entre duas páginas: no PDF, os versos de cada estrofe estão todos na mesma página, e
    # o texto inteiro (título, versos e vocabulário) também.
    try:
        from pypdf import PdfReader
        import io
        folhas = [re.sub(r'\s+', ' ', p.extract_text() or '') for p in PdfReader(io.BytesIO(pdf)).pages]
        blocos = page.evaluate('''() => [...document.querySelectorAll('.tt-texto')].map(t => ({
            titulo: t.querySelector('.tt-num').textContent, fonte: t.querySelector('.tt-fonte').textContent,
            estrofes: [...t.querySelectorAll('.tt-estrofe')].map(e => [...e.querySelectorAll('.tt-l')].map(v => v.textContent)) }))''')
        junto = lambda s: re.sub(r'\s+', ' ', s).strip()
        for b in blocos:
            onde = set()
            for estrofe in b['estrofes']:
                paginas_da_estrofe = {k for k, f in enumerate(folhas) for v in estrofe if junto(v) in f}
                primeira = [k for k, f in enumerate(folhas) if junto(estrofe[0]) in f]
                assert primeira, (slug, b['titulo'], estrofe[0])
                # cada verso da estrofe está na página onde a estrofe começa
                assert all(junto(v) in folhas[primeira[0]] for v in estrofe), (slug, b['titulo'], estrofe[0], 'estrofe partida')
                onde.add(primeira[0])
            assert len(onde) == 1, (slug, b['titulo'], sorted(onde), 'texto partido entre páginas')
            assert junto(b['fonte']) in folhas[onde.pop()], (slug, b['titulo'], 'a linha de fonte ficou noutra página')
        # 13/11/2026: o cabeçalho do cartão dos temas («Escolhe um tema», a orientação e «Escreve a letra do teu tema») não fica
        # sozinho no fundo de uma página: sai na página onde começa o tema A, com as margens de 12 mm e sem margens (achado de uma
        # revisão: na m3-u2 ficava no fundo da página 3 e o tema A só começava na 4).
        topo = page.evaluate('''() => ({ titulo: document.querySelector('#tema-titulo').textContent,
            topo: document.querySelector('.tf-topo').textContent, passo: document.querySelector('.task-theme .tf-passos li').textContent })''')
        for nome, doc in (('12 mm', pdf), ('sem margens', page.pdf(format='A4', print_background=False))):
            fs = [re.sub(r'\s+', ' ', p.extract_text() or '') for p in PdfReader(io.BytesIO(doc)).pages]
            pag = [k for k, f in enumerate(fs) if junto(topo['topo']) in f]
            assert len(pag) == 1 and junto(topo['titulo']) in fs[pag[0]], (slug, nome, pag)
            assert junto(topo['passo'])[:40] in fs[pag[0]], (slug, nome, pag, 'o cabeçalho dos temas ficou sozinho no fundo da página')
        partido = 'conferido no PDF'
    except ImportError:
        # Sem pypdf (o fluxo só instala o Playwright): confere-se a regra que o impede, tal como o navegador a aplica.
        regras = page.evaluate('''() => [...document.querySelectorAll('.tt-texto, .tt-estrofe')].map(e => getComputedStyle(e).breakInside)''')
        assert regras and all(r == 'avoid' for r in regras), (slug, regras)
        # 13/11/2026: e a regra que prende o cabeçalho do cartão dos temas ao primeiro tema.
        assert page.evaluate('''() => getComputedStyle(document.querySelector('.tf-topo')).breakAfter''') == 'avoid', slug
        partido = 'conferido nas regras de impressão'
    ctx.close()
    print(f'PASS impressão: {paginas} páginas A4, apoio fora do papel, nenhum poema partido ({partido})', slug, flush=True)
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
    print('PASS tarefas do M3 mais fáceis de fazer', flush=True)


if __name__ == '__main__':
    main()
