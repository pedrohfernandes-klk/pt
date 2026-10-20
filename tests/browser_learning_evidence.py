"""Focused Chromium checks on the three evidenced cross-module editorial fixes."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CASES = [('m3', '17', 11, 'pairs'), ('m5', '12', 20, 'gaps'),
         ('m7', '11', 9, 'gaps'), ('m7', '11', 20, 'read')]
count = 0


def expect(predicate, context):
    global count
    assert predicate, context
    count += 1


def cards(module, id_):
    raw = (ROOT / f'{module}/licao-{module}-f{id_}/index.html').read_text('utf-8')
    return json.JSONDecoder().raw_decode(raw.split('CARTOES=', 1)[1].lstrip())[0]


def run_case(browser, host, mod, id_, index, kind):
    bank = cards(mod, id_)
    for width in (320, 390, 1440):
        ctx = browser.new_context(viewport={'width': width, 'height': 850},
                                  reduced_motion='reduce')
        page = ctx.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.route('**/fonts.googleapis.com/**', lambda route: route.abort())
        page.route('**/fonts.gstatic.com/**', lambda route: route.abort())
        resp = page.goto(f'{host}/{mod}/licao-{mod}-f{id_}/',
                         wait_until='domcontentloaded', timeout=30000)
        expect(resp and resp.ok, f'HTTP {mod}/{id_}')
        page.locator('#baralho .cartao').wait_for(timeout=15000)
        expect(not errors, f'Page errors {mod}/{id_}: {errors}')
        expect(page.evaluate('document.documentElement.scrollWidth - innerWidth') <= 3,
               f'Overflow {mod}/{id_} at {width}')
        if width == 390:
            page.evaluate("""({card,key}) => {
                window.EPIJogo.montar({itens:[card],chave:key,
                                      marca:'QA',titulo:'QA',variar:false});
            }""", {'card': bank[index], 'key': f'qa-{mod}-{id_}-{index}'})
            modal = page.locator('.casca.sobreposta')
            modal.locator('.cartao').wait_for(timeout=10000)
            card = bank[index]
            if kind == 'pairs':
                expect(card['t'] == 'emparelhar', 'wrong kind')
                for i in range(len(card['pares'])):
                    modal.locator(f'button[data-e="{i}"]').click()
                    modal.locator(f'button[data-d="{i}"]').click()
            elif kind == 'gaps':
                expect(card['t'] == 'completar', 'wrong kind')
                for i, lacuna in enumerate(card['lacunas']):
                    modal.locator(f'select[data-k="{i}"]').select_option(str(lacuna['c']))
            else:
                expect(card['t'] == 'ler', 'wrong kind')
                expect('Forma e pensamento' in modal.locator('.ler').inner_text(),
                       'grammatical meaning absent')
                modal.locator('[data-seguinte]').click()
            if kind != 'read':
                msg = modal.locator('.casca-folha').inner_text()
                expect('Certo.' in msg and len(msg) > 60,
                       f'Incorrect feedback on {mod}/{id_}:{index} — {msg[:200]}')
                modal.locator('[data-seguinte]').click()
            expect(modal.locator('.cartao.fim').count() == 1,
                   f'No completion for {mod}/{id_}:{index}')
            progress = page.evaluate("""key => JSON.parse(localStorage.getItem(key))""",
                                     f'qa-{mod}-{id_}-{index}')
            expect(bool(progress and progress.get('lida')),
                   f'No persisted completion for {mod}/{id_}:{index}')
            modal.locator('[data-c-menu]').click()
            expect(modal.count() == 0, f'Modal not closed {mod}/{id_}:{index}')
        ctx.close()
    print(f'PASS: {mod}-f{id_}, card {index} ({kind})', flush=True)


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0),
                                 partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                                        args=['--disable-dev-shm-usage', '--no-sandbox'])
            for mod, id_, i, kind in CASES:
                run_case(browser, f'http://127.0.0.1:{server.server_port}',
                         mod, id_, i, kind)
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {count} Chromium assertions')


if __name__ == '__main__':
    main()
