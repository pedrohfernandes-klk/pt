"""M2 browser smoke checks against actual page and its embedded lesson engine.

Use: python tests/browser_m2.py --lessons 01,02,07
Needs: pip install playwright; python -m playwright install chromium
Runs a local HTTP server; test data and localStorage never leave the browser.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CARD_TESTS = {
    '01': {'choices': [10, 20], 'vf': [], 'read': [23]},
    '02': {'choices': [25], 'vf': [17], 'read': [1, 27]},
    '07': {'choices': [8, 15, 23], 'vf': [9], 'read': [1, 24]},
    '06': {'choices': [25], 'vf': [], 'read': [33]},
    '08': {'choices': [16], 'vf': [], 'read': [1, 21]},
    '10': {'choices': [18], 'vf': [9, 12], 'read': [4]},
    '11': {'choices': [15], 'vf': [], 'read': [0, 1]},
}
PASS = 0


def bank(lesson):
    src = (ROOT / f'm2/licao-m2-f{lesson}/index.html').read_text('utf-8')
    return json.JSONDecoder().raw_decode(src.split('CARTOES=', 1)[1].lstrip())[0]


def check(condition, message):
    global PASS
    if not condition:
        raise AssertionError(message)
    PASS += 1


def close_modal(page):
    modal = page.locator('.casca.sobreposta')
    if modal.count():
        modal.locator('[data-c-menu]').click(timeout=5000)
        check(modal.count() == 0, 'Modal failed to close')


def fixture(page, card, key):
    close_modal(page)
    page.evaluate("""({card,key}) => {
      window.EPIJogo.montar({itens:[card],chave:key,marca:'QA',titulo:'QA',variar:false});
    }""", {'card': card, 'key': key})
    modal = page.locator('.casca.sobreposta')
    modal.locator('.cartao').wait_for(timeout=10000)
    return modal


def check_choices(page, card, lesson, index):
    check(card['t'] == 'escolha', f'{lesson}/{index} not choice')
    incorrect = [j for j in range(len(card['o'])) if j != card['c']]
    for j in incorrect:
        for attempt in range(12):
            modal = fixture(page, card, f'qa-{lesson}-{index}-{j}-{attempt}')
            target = modal.locator(f'button.op[data-j="{j}"]')
            if target.count():
                break
        else:
            raise AssertionError(f'{lesson}/{index}: option {j} never displayed')
        target.click()
        feedback = modal.locator('.casca-folha').inner_text()
        expected = card['fe'][j] if isinstance(card['fe'], list) else card['fe'][str(j)]
        check(expected in feedback, f'{lesson}/{index}: missing specific feedback for wrong option {j}')
    modal = fixture(page, card, f'qa-{lesson}-{index}-correct')
    modal.locator(f'button.op[data-j="{card["c"]}"]').click()
    check('Certo.' in modal.locator('.casca-folha').inner_text(),
          f'{lesson}/{index}: correct option not accepted')
    modal.locator('[data-seguinte]').click()
    check(modal.locator('.cartao.fim').count() == 1, f'{lesson}/{index}: result not reached')
    key = f'qa-{lesson}-{index}-correct'
    value = page.evaluate('key => JSON.parse(localStorage.getItem(key))', key)
    check(bool(value and value.get('lida') and value.get('melhor') == 1),
          f'{lesson}/{index}: progress was not saved')
    close_modal(page)


def check_vf(page, card, lesson, index):
    check(card['t'] == 'vf', f'{lesson}/{index}: not V/F')
    modal = fixture(page, card, f'qa-{lesson}-{index}-vf')
    wrong = 0 if card['v'] else 1
    modal.locator(f'button.op[data-j="{wrong}"]').click()
    check(card['fe'] in modal.locator('.casca-folha').inner_text(),
          f'{lesson}/{index}: specific V/F error feedback missing')
    close_modal(page)


def check_reading(page, card, lesson, index):
    check(card['t'] == 'ler', f'{lesson}/{index}: not reading')
    modal = fixture(page, card, f'qa-{lesson}-{index}-reading')
    check(modal.locator('.ler').count() == 1, f'{lesson}/{index}: no reading')
    details = modal.locator('details')
    if details.count():
        details.first.locator('summary').click()
        check(details.first.get_attribute('open') is not None,
              f'{lesson}/{index}: explanation failed to expand')
    modal.locator('[data-seguinte]').click()
    check(modal.locator('.cartao.fim').count() == 1,
          f'{lesson}/{index}: reading did not complete')
    close_modal(page)


def page_smoke(browser, base, lesson, cards):
    for width in (320, 390, 1440):
        context = browser.new_context(viewport={'width': width, 'height': 850},
                                      reduced_motion='reduce')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.route('**/fonts.googleapis.com/**', lambda route: route.abort())
        page.route('**/fonts.gstatic.com/**', lambda route: route.abort())
        resp = page.goto(f'{base}/m2/licao-m2-f{lesson}/',
                         wait_until='domcontentloaded', timeout=30000)
        check(resp is not None and resp.ok, f'{lesson}/{width}: page failed')
        page.locator('#baralho .cartao').wait_for(timeout=20000)
        check(not errors, f'{lesson}/{width}: JavaScript errors: {errors[:3]}')
        overflow = page.evaluate('document.documentElement.scrollWidth - innerWidth')
        check(overflow <= 3, f'{lesson}/{width}: document overflow {overflow}px')
        if width == 390:
            page.locator('.casca:not(.sobreposta) [data-seguinte]').click()
            check(page.locator('#baralho .cartao').count() == 1,
                  f'{lesson}: first-page navigation failed')
            for i in CARD_TESTS[lesson]['choices']:
                check_choices(page, cards[i], lesson, i)
            for i in CARD_TESTS[lesson]['vf']:
                check_vf(page, cards[i], lesson, i)
            for i in CARD_TESTS[lesson]['read']:
                check_reading(page, cards[i], lesson, i)
            check(not errors, f'{lesson}: runtime errors after interaction: {errors[:3]}')
        context.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lessons', required=True, help='comma-separated M2 lesson numbers')
    args = parser.parse_args()
    lessons = args.lessons.split(',')
    for lesson in lessons:
        if lesson not in CARD_TESTS:
            raise ValueError(f'Unsupported lesson: {lesson}')
    server = ThreadingHTTPServer(('127.0.0.1', 0),
                                 partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                                        args=['--disable-dev-shm-usage', '--no-sandbox'])
            for lesson in lessons:
                page_smoke(browser, base, lesson, bank(lesson))
                print(f'PASS browser: M2-F{lesson}', flush=True)
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS: {PASS} browser assertions over {len(lessons)} lessons')


if __name__ == '__main__':
    main()
