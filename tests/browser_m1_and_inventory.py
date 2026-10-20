"""Inventory smoke checks plus full M1/M2 paths and deterministic roles QA.

Fresh browser contexts never access a pupil's saved progress. Full paths use
the normal random deck; isolated cards additionally cover every target variant.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
import argparse
from playwright.sync_api import sync_playwright
from browser_m2_complete import respond

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def new_page(browser, width):
    ctx = browser.new_context(viewport={'width': width, 'height': 850}, reduced_motion='reduce')
    page = ctx.new_page()
    page.route('**/fonts.googleapis.com/**', lambda route: route.abort())
    page.route('**/fonts.gstatic.com/**', lambda route: route.abort())
    return ctx, page


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--focused-only', action='store_true')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            pages = sorted(ROOT.glob('m[1-9]/licao-*/index.html'))
            assert len(pages) == 108
            for path in ([] if args.focused_only else pages):
                for width in (320, 1440):
                    ctx, page = new_page(browser, width)
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    response = page.goto(host + '/' + path.parent.relative_to(ROOT).as_posix() + '/', wait_until='networkidle')
                    assert response.ok, path
                    assert not errors, (path, errors)
                    assert page.locator('html').get_attribute('lang') == 'pt-PT', path
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'), (path, width, 'overflow')
                    assert page.title().strip(), path
                    assert page.locator('#baralho .cartao').count() == 1, path
                    ctx.close()
                print('PASS load 320/1440: ' + path.parent.name, flush=True)

            for lesson in ('m1/licao-m1-f01', 'm1/licao-m1-f11', 'm2/licao-m2-f01',
                           'm8/licao-m8-f03', 'm9/licao-m9-f03',
                           'm3/licao-m3-f18', 'm9/licao-m9-f11',
                           'm9/licao-m9-f12', 'm9/licao-m9-f13'):
                ctx, page = new_page(browser, 390)
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.goto(f'{host}/{lesson}/', wait_until='networkidle')
                for action in range(150):
                    if page.locator('#baralho .cartao.fim').count():
                        break
                    respond(page)
                else:
                    raise AssertionError('Path did not finish: ' + lesson)
                key = lesson.split('/')[-1]
                saved = page.evaluate('k => JSON.parse(localStorage.getItem(k))', key)
                assert saved and saved['lida'] and saved['tentativas'] >= 1, (lesson, saved)
                page.reload(wait_until='networkidle')
                assert page.locator('#baralho .cartao.fim').count() == 1, lesson
                assert not errors, errors
                print(f'PASS full path + reload: {lesson}; actions={action}', flush=True)
                ctx.close()

            source = (ROOT / 'm1/licao-m1-f01/index.html').read_text('utf-8')
            bank = json.JSONDecoder().raw_decode(source.split('CARTOES=', 1)[1].lstrip())[0]
            for index in (3, 4, 8, 9, 10):
                for width in (320, 390, 1440):
                    # Repeat both truth values / each choice, including wrong answers.
                    answers = range(4) if index == 8 else range(2) if index == 9 else (None,)
                    for answer in answers:
                        ctx, page = new_page(browser, width)
                        page.goto(f'{host}/m1/licao-m1-f01/', wait_until='networkidle')
                        page.evaluate('card => EPIJogo.montar({itens:[card],chave:"qa-roles",variar:false})', bank[index])
                        modal = page.locator('.casca.sobreposta')
                        if answer is not None:
                            for attempt in range(20):
                                if modal.locator(f'button[data-j="{answer}"]').count():
                                    break
                                page.reload(wait_until='networkidle')
                                page.evaluate('card => EPIJogo.montar({itens:[card],chave:"qa-roles",variar:false})', bank[index])
                            button = modal.locator(f'button[data-j="{answer}"]')
                            button.focus()
                            button.press('Enter')
                        elif index == 4:
                            for i, (_, target) in enumerate(bank[index]['pares']):
                                modal.locator(f'button[data-e="{i}"]').click()
                                # Classification targets use first-seen unique labels.
                                targets = list(dict.fromkeys(p[1] for p in bank[index]['pares']))
                                modal.locator(f'button[data-d="{targets.index(target)}"]').click()
                        elif index == 10:
                            for i in range(3):
                                modal.locator(f'.soltos button[data-j="{i}"]').click()
                        if index != 3:
                            text = modal.locator('.casca-folha').inner_text()
                            assert len(text) > 60, (index, text)
                            if index == 8:
                                assert ('Certo.' in text) == (answer == 0), text
                                assert 'jograis' in text.lower() or answer in (0, 3), text
                            if index == 9:
                                assert ('Certo.' in text) == (answer == 0), text
                            if index == 10:
                                assert 'Certo.' in text and 'simplificação tradicional' in text, text
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'), (index, width)
                        modal.locator('[data-seguinte]').click()
                        assert modal.locator('.cartao.fim').count() == 1
                        print(f'PASS roles: index={index}; width={width}; answer={answer}', flush=True)
                        ctx.close()
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
