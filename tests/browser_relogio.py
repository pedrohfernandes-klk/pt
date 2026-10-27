"""Relógio do aluno (27/10/2026): duração escolhida até ao máximo, duas pausas, depois recomeço obrigatório.
Corre num navegador com relógio controlado; não depende de rede nem de servidor."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / 'assets/relogio.js').read_text('utf-8')
STYLE = (ROOT / 'assets/relogio.css').read_text('utf-8')
PAGE = '<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><style>' + STYLE + '</style><script defer src="relogio.js"></script></head><body><main><div id="a" data-relogio data-max="60" data-passo="5" data-rotulo="Produção" data-chave="teste-relogio"></div><div id="b"></div></main></body></html>'


def text(page, sel):
    return page.locator(sel).inner_text().strip()


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.route('http://relogio.test/**', lambda route: route.fulfill(content_type='application/javascript' if route.request.url.endswith('.js') else 'text/html', body=SCRIPT if route.request.url.endswith('.js') else PAGE))
    page.clock.install(time=1_000_000_000_000)
    page.goto('http://relogio.test/')
    a = '#a .relogio'
    assert text(page, a + ' .relogio-mostrador') == '60:00'
    assert text(page, a + ' .relogio-max') == 'até 60 min'
    assert page.locator(a + ' .relogio-passo').nth(1).is_disabled(), 'não passa do máximo'
    page.locator(a + ' .relogio-passo').nth(0).click()
    assert text(page, a + ' .relogio-mostrador') == '55:00'
    page.fill(a + ' input', '200'); page.locator(a + ' input').dispatch_event('change')
    assert text(page, a + ' .relogio-mostrador') == '60:00', 'o campo respeita o máximo'
    page.fill(a + ' input', '1'); page.locator(a + ' input').dispatch_event('change')
    assert text(page, a + ' .relogio-mostrador') == '05:00', 'o campo respeita o mínimo (um passo)'
    page.fill(a + ' input', '20'); page.locator(a + ' input').dispatch_event('change')
    main = page.locator(a + ' .relogio-principal')
    assert main.inner_text() == 'Iniciar' and page.locator(a + ' .relogio-recomecar').is_disabled()
    main.click(); page.clock.run_for(3000)
    assert text(page, a + ' .relogio-mostrador') == '19:57'
    assert page.locator(a + ' input').is_disabled(), 'a duração fixa-se ao iniciar'
    assert main.inner_text() == 'Pausar'
    main.click()
    assert main.inner_text() == 'Continuar' and 'Pausa 1 de 2' in text(page, a + ' .relogio-estado')
    assert text(page, a + ' .relogio-pausas') == 'Resta 1 pausa'
    page.clock.run_for(5000)
    assert text(page, a + ' .relogio-mostrador') == '19:57', 'em pausa, o tempo não corre'
    # O estado guardado sobrevive a um recarregamento.
    page.reload()
    assert text(page, a + ' .relogio-mostrador') == '19:57' and main.inner_text() == 'Continuar'
    main.click(); page.clock.run_for(2000); main.click()
    assert 'Pausa 2 de 2' in text(page, a + ' .relogio-estado') and 'recomeça do início' in text(page, a + ' .relogio-estado')
    main.click()
    assert main.inner_text() == 'Parar e recomeçar'
    assert text(page, a + ' .relogio-pausas') == 'Sem pausas: parar recomeça do início'
    page.clock.run_for(1000); main.click()
    assert text(page, a + ' .relogio-mostrador') == '20:00' and main.inner_text() == 'Iniciar'
    assert 'voltou ao início' in text(page, a + ' .relogio-estado')
    assert text(page, a + ' .relogio-pausas') == 'Restam 2 pausas' and not page.locator(a + ' input').is_disabled()
    # Até ao fim: o relógio para e avisa.
    main.click(); page.clock.run_for(20 * 60 * 1000 + 500)
    assert text(page, a + ' .relogio-mostrador') == '00:00' and main.inner_text() == 'Terminado' and main.is_disabled()
    assert 'Tempo terminado' in text(page, a + ' .relogio-estado')
    page.locator(a + ' .relogio-recomecar').click()
    assert text(page, a + ' .relogio-mostrador') == '20:00'
    # Uma paragem vinda de fora conta como pausa; espelho no topo da página.
    page.evaluate("""() => { window.r = EPIRelogio.criar(document.getElementById('b'), {max: 2, passo: 0.5, rotulo: 'Resposta'});
      window.m = window.r.espelhar(Object.assign(document.createElement('span'), {className: 'relogio-mini'})); document.body.append(window.m); }""")
    b = '#b .relogio'
    assert text(page, b + ' .relogio-mostrador') == '02:00' and page.locator(b + ' input').get_attribute('step') == '0.5'
    page.locator(b + ' .relogio-principal').click(); page.clock.run_for(1500)
    assert page.evaluate('r.pausar()') is True and page.evaluate('r.estado().pausasUsadas') == 1
    assert page.evaluate('m.textContent') == text(page, b + ' .relogio-mostrador')
    page.locator(b + ' .relogio-principal').click(); assert page.evaluate('r.pausar()') is True
    page.locator(b + ' .relogio-principal').click(); assert page.evaluate('r.pausar()') is True
    assert page.evaluate('r.estado()')['iniciado'] is False and text(page, b + ' .relogio-mostrador') == '02:00'
    # Sem armazenamento disponível, continua a funcionar.
    page.evaluate("() => { Object.defineProperty(window, 'localStorage', {get() { throw new Error('bloqueado'); }}); }")
    page.evaluate("() => { window.c = EPIRelogio.criar(document.body.appendChild(document.createElement('div')), {max: 3, chave: 'x'}); }")
    assert page.evaluate('c.estado().duracao') == 180
    browser.close()
print('PASS relógio: máximo e passo, início, duas pausas, recomeço obrigatório, fim, persistência, pausa externa, espelho, sem armazenamento')
