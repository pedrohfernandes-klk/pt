"""29/10/2026: aquecimentos em cartões do M7 e a tarefa nova da unidade 3, no Chromium (decisões do docente de 29/10).

Para cada uma das três páginas tarefas/m7-uN/aquecimento/, a 390 px em tema claro e a 1366 px em tema escuro: sem erros
de página, sem deslizar na horizontal em nenhum cartão, o baralho todo até ao fim, e no fim só a chave
«aquecimento-<slug>» (nada de licao-, percurso-, desafio-, epi-pt- nem epi-ultima). Com ?projetar=1 percorre-se o baralho
e não fica nada gravado. Nas tarefas, a ligação em destaque está no cartão «Enunciado» (e, na U3, também no cartão
«Aquecer», o primeiro) e abre o aquecimento; no percurso, a linha «A» vem logo antes da linha «T» e abre o aquecimento.
A F10 reescrita («Argumentar com versos») percorre-se até ao fim e fica marcada como lida.

29/10/2026 (revisão pedagógica e técnica): a F10 guarda a versão nova (regra de 23/10); na página dos diapositivos, depois
do «load» (o lançador da projeção já correu), a lista mostra as sessões 14 e 15 pelo nome e nenhuma linha «Projetar esta
página»; no arquivo do guia, a tarefa da unidade 3 mostra _Mensagem_ em itálico e os blocos somam 90 minutos.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import threading

from playwright.sync_api import sync_playwright

from browser_m1_and_inventory import ROOT, QuietHandler
from browser_m2_complete import respond

# 30/10/2026: aquecimento em cartões (decisão do docente)
# 30/10/2026: o M4 também liga aos aquecimentos (camada tests/fixtures/aquecimentos-m4-edits-20261030.json).
TAREFAS_LIGADAS = ['m1-u1', 'm1-u2', 'm2-u1', 'm2-u2', 'm4-u1', 'm4-u2', 'm4-u3-discurso', 'm7-u1', 'm7-u2', 'm7-u3']
# 30/10/2026: M2 recebe páginas novas (aquecimentos em cartões das duas unidades).
SLUGS = ['m1-u1', 'm1-u2', 'm2-u1', 'm2-u2', 'm4-u1', 'm4-u2', 'm4-u3-discurso', 'm7-u1', 'm7-u2', 'm7-u3']
CHAVES = r"""() => Object.keys(localStorage).filter(k => /^(licao-|percurso-|desafio-|epi-pt-|epi-ultima|aquecimento-)/.test(k)).sort()"""


def contexto(browser, width, scheme='light'):
    ctx = browser.new_context(viewport={'width': width, 'height': 860}, color_scheme=scheme, reduced_motion='reduce')
    page = ctx.new_page()
    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    return ctx, page, errors


def sem_deslizar(page, onde):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (onde, page.evaluate('document.documentElement.scrollWidth'))


def percorrer(page, total, onde):
    passos = 0
    while not page.locator('#baralho .cartao.fim').count():
        sem_deslizar(page, onde)
        respond(page)
        page.wait_for_timeout(40)
        passos += 1
        assert passos <= total * 4, (onde, 'o baralho não chega ao fim')
    return passos


def aquecimentos(browser, host):
    for slug in SLUGS:
        dados = json.loads((ROOT / 'docs/pedagogia/aquecimentos' / f'{slug}.json').read_text('utf-8'))
        total = len(dados['cartoes'])
        for width, scheme in ((390, 'light'), (1366, 'dark')):
            ctx, page, errors = contexto(browser, width, scheme)
            page.goto(f'{host}/tarefas/{slug}/aquecimento/', wait_until='networkidle')
            page.locator('#baralho .cartao').first.wait_for()
            assert page.evaluate('matchMedia("(prefers-color-scheme: dark)").matches') == (scheme == 'dark')
            assert page.evaluate(CHAVES) == [], (slug, 'grava antes do fim')
            passos = percorrer(page, total, f'{slug}@{width}')
            fim = page.locator('#baralho .cartao.fim').inner_text()
            assert 'Abrir a aula de tarefa' in page.locator('#baralho .cartao.fim').inner_text() or \
                page.locator('.casca [data-c-acoes]').get_by_text('Abrir a aula de tarefa').count(), (slug, fim[:200])
            chaves = page.evaluate(CHAVES)
            assert chaves == [f'aquecimento-{slug}'], (slug, chaves)
            guardado = json.loads(page.evaluate(f'localStorage.getItem("aquecimento-{slug}")'))
            assert guardado.get('tentativas', 0) >= 1, guardado
            sem_deslizar(page, f'{slug}@{width} fim')
            assert not errors, (slug, width, errors)
            print('PASS aquecimento:', slug, width, scheme, 'cartões', total, 'passos', passos, 'chave', chaves, flush=True)
            ctx.close()
        # Projeção: começa do início, mostra a resposta e não grava nada.
        ctx, page, errors = contexto(browser, 1366)
        page.goto(f'{host}/tarefas/{slug}/aquecimento/?projetar=1', wait_until='networkidle')
        page.locator('#baralho .cartao').first.wait_for()
        for _ in range(total * 4):
            if page.locator('#baralho .cartao.fim').count():
                break
            if page.locator('[data-mostrar]').count():
                page.locator('[data-mostrar]').first.click()
            if page.locator('.casca [data-seguinte]').count():
                page.locator('.casca [data-seguinte]').last.click()
            else:
                respond(page)
            page.wait_for_timeout(40)
        assert page.locator('#baralho .cartao.fim').count(), (slug, 'projeção sem fim')
        assert page.evaluate(CHAVES) == [], (slug, 'a projeção gravou', page.evaluate(CHAVES))
        assert not errors, (slug, 'projeção', errors)
        print('PASS projeção sem gravar:', slug, flush=True)
        ctx.close()


def tarefas(browser, host):
    # 30/10/2026: a integração do M4 fica para a camada literal, sem omitir testes existentes.
    for slug in TAREFAS_LIGADAS:
        for width, scheme in ((390, 'light'), (1366, 'dark')):
            ctx, page, errors = contexto(browser, width, scheme)
            page.goto(f'{host}/tarefas/{slug}/', wait_until='networkidle')
            page.locator('[data-task-reader].task-reader-ready').wait_for()
            enunciado = page.locator('#produzir').evaluate('e=>+e.closest("[data-task-card]").dataset.taskCard')
            ligacao = page.locator(f'[data-task-card="{enunciado}"] header .task-aquecer a[href="aquecimento/"]')
            assert ligacao.count() == 1, slug
            # 30/10/2026: aquecimento em cartões (decisão do docente)
            # 30/10/2026: as tarefas do M2 também passam ao formato com o cartão «Aquecer» em cartões.
            if slug in {'m1-u1', 'm1-u2', 'm2-u1', 'm2-u2', 'm7-u3'}:
                # Os cartões substituem as máquinas em papel: o cartão «Aquecer» é o primeiro e liga ao aquecimento.
                assert enunciado == 1
                primeiro = page.locator('[data-task-card="0"]')
                assert primeiro.is_visible() and primeiro.locator('#aquecer[data-task-warm="cartoes"]').count() == 1
                destaque = primeiro.locator('.task-aquecer a[href="aquecimento/"]')
                assert destaque.is_visible()
                assert page.locator('[data-task-question]').count() == 1
                if slug == 'm7-u3':
                    assert page.locator('#exemplos').count() == 1 and page.locator('.task-example').count() == 2
            else:
                assert enunciado == 0 and ligacao.is_visible()
                destaque = ligacao
            box = destaque.bounding_box()
            assert box and box['height'] >= 44, (slug, box)
            sem_deslizar(page, f'tarefa {slug}@{width}')
            destaque.click()
            page.wait_for_url(f'**/tarefas/{slug}/aquecimento/')
            page.locator('#baralho .cartao').first.wait_for()
            page.locator('.c-marca').click()
            page.wait_for_url(f'**/tarefas/{slug}/')
            page.locator('[data-task-reader].task-reader-ready').wait_for()
            assert not errors, (slug, width, errors)
            print('PASS tarefa com ligação ao aquecimento:', slug, width, scheme, flush=True)
            ctx.close()


def percurso(browser, host):
    # 30/10/2026: aquecimento em cartões (decisão do docente)
    for n in (1, 2):
        ctx, page, errors = contexto(browser, 390)
        page.goto(f'{host}/m1/', wait_until='networkidle')
        a = page.locator(f'#aquecimento-unidade-{n}')
        assert a.is_visible()
        assert a.evaluate('e=>e.nextElementSibling.id') == f'tarefa-unidade-{n}'
        assert a.evaluate('e=>!e.hasAttribute("data-passo") && !e.hasAttribute("data-task-lesson")')
        sem_deslizar(page, f'percurso m1 unidade {n}')
        a.locator('a').click()
        page.wait_for_url(f'**/tarefas/m1-u{n}/aquecimento/')
        assert not errors, errors
        ctx.close()
    print('PASS percurso M1: A antes de T nas duas unidades', flush=True)

    ctx, page, errors = contexto(browser, 390)
    page.goto(f'{host}/m7/', wait_until='networkidle')
    for n in (1, 2, 3):
        a = page.locator(f'#aquecimento-unidade-{n}')
        assert a.is_visible(), n
        assert a.evaluate('e=>e.nextElementSibling && e.nextElementSibling.id') == f'tarefa-unidade-{n}'
        assert a.evaluate('e=>!e.hasAttribute("data-passo") && !e.hasAttribute("data-task-lesson")')
        t = page.locator(f'#tarefa-unidade-{n}')
        assert t.evaluate('(el)=>el===el.parentElement.lastElementChild')
    assert 'Argumentar com versos' in page.locator('#m7-f10').inner_text()
    assert 'Louco, sim' in page.locator('#tarefa-unidade-3').inner_text()
    assert 'pequenos grupos' in page.locator('#tarefa-unidade-2').inner_text()
    sem_deslizar(page, 'percurso m7')
    page.locator('#aquecimento-unidade-3 a').click()
    page.wait_for_url('**/tarefas/m7-u3/aquecimento/')
    page.locator('#baralho .cartao').first.wait_for()
    assert not errors, errors
    print('PASS percurso: linhas A antes das linhas T, F10 e tarefa 3 com títulos novos', flush=True)
    ctx.close()


def f10(browser, host):
    ctx, page, errors = contexto(browser, 390)
    page.goto(f'{host}/m7/licao-m7-f10/', wait_until='networkidle')
    page.locator('#baralho .cartao').first.wait_for()
    assert 'Argumentar com versos' in page.title()
    percorrer(page, 20, 'F10')
    page.wait_for_timeout(200)
    guardado = json.loads(page.evaluate('localStorage.getItem("licao-m7-f10")') or '{}')
    assert guardado.get('lida'), guardado
    assert guardado.get('versao') == '2026-10-29', guardado  # 29/10/2026 (revisão técnica, P2)
    assert not errors, errors
    ctx.close()
    ctx, page, errors = contexto(browser, 1366)
    page.goto(f'{host}/m7/painel-m7-f10/', wait_until='networkidle')
    assert page.locator('select[data-r-k] option').count() == 16
    assert 'Argumentar com versos' in page.title()
    assert not errors, errors
    ctx.close()
    print('PASS F10 reescrita até ao fim e painel com 16 relâmpagos', flush=True)


def diapositivos(browser, host):
    # 29/10/2026 (revisão pedagógica, G1 e G2): o teste antigo só conferia o HTML; o lançador da projeção troca qualquer
    # ligação com «projetar=1» pelo seu botão, e a sessão 14 desaparecia da lista.
    ctx, page, errors = contexto(browser, 390)
    page.goto(f'{host}/m7/diapositivos/', wait_until='load')
    page.wait_for_timeout(300)
    linhas = page.locator('main li').all_inner_texts()
    assert any(t.startswith('Sessão 14: Argumentar com versos') for t in linhas), linhas[12:]
    assert any(t.startswith('Sessão 15: Quantas vozes cabem num homem') for t in linhas), linhas[12:]
    assert not any('Projetar esta página' in t for t in linhas), linhas[12:]
    assert page.locator('main a[href="../licao-m7-f10/"]').count() == 1
    assert page.locator('main a[href="../licao-m7-f11/"]').count() == 1
    sem_deslizar(page, 'diapositivos m7')
    assert not errors, errors
    ctx.close()
    print('PASS diapositivos: sessões 14 e 15 pelo nome, sem PDF com «Dia Pessoa»', flush=True)


def guia(browser, host):
    # 29/10/2026 (revisão pedagógica, C9; técnica, P7): no arquivo do guia, a tarefa da unidade 3 mostra o título da obra em
    # itálico e os três blocos somam os 90 minutos da aula.
    ctx, page, errors = contexto(browser, 390)
    page.goto(f'{host}/m7/guia-da-tarefa-m7/', wait_until='load')
    page.locator('#arquivo-producoes summary').click()
    page.locator('button.tarefa[data-n="2"]').click()
    page.locator('#rota').wait_for(state='visible')
    assert page.locator('#r-titulo i').inner_text() == 'Mensagem'
    rota = page.locator('#rota').inner_text()
    assert '_Mensagem_' not in rota and 'M7_Tarefa3_Opiniao' in rota, rota[:400]  # os nomes de ficheiro guardam o «_»
    assert page.locator('#r-criterios i').first.inner_text() == 'Mensagem'
    blocos = page.locator('#blocos .bloco b').all_inner_texts()
    assert blocos == ['Aquecer, 15 min', 'Produzir, 60 min', 'Rever, apresentar e entregar, 15 min'], blocos
    assert page.locator('#relogio').inner_text() == '15:00'
    sem_deslizar(page, 'guia m7')
    assert not errors, errors
    ctx.close()
    print('PASS guia: _Mensagem_ em itálico e blocos de 90 minutos', flush=True)


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            aquecimentos(browser, host)
            tarefas(browser, host)
            percurso(browser, host)
            f10(browser, host)
            diapositivos(browser, host)
            guia(browser, host)
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
