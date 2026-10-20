"""Real full-lesson traversal of M2 card engines in Chromium.

Each run answers every displayed item (not necessarily correctly), advances to
the actual result, reloads, and checks local progress. This does not cover all
random combinations, external services, Safari, or learning outcomes.
"""
import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

ROUTES = {
    '01': 'licao-m2-f01',
    '02': 'licao-m2-f02',
    '07': 'licao-m2-f07',
    '06': 'licao-m2-f06',
    '08': 'licao-m2-f08',
    '09': 'licao-m2-f09',
    '10': 'licao-m2-f10',
    '11': 'licao-m2-f11',
    '12': 'licao-m2-f12',
    '13': 'licao-m2-f13',
    'escolhas': 'm2-ines-escolhe-duas-vezes',
    'riso': 'm2-maquina-de-rir',
}


def tap(page, selector, description):
    page.locator(selector).first.click(timeout=5000)


def respond(page):
    """Advance exactly one active card using the rendered engine's controls."""
    root = '#baralho'
    if page.locator('.casca [data-c-folha]:visible [data-seguinte]').count():
        tap(page, '.casca [data-c-folha]:visible [data-seguinte]', 'feedback next')
        return 'feedback'

    if page.locator('.casca [data-c-acoes] [data-seguinte]').count():
        tap(page, '.casca [data-c-acoes] [data-seguinte]', 'reading next')
        return 'reading'

    if page.locator(root + ' .inline select').count():
        selects = page.locator(root + ' .inline select')
        count = selects.count()
        for i in range(count):
            options = selects.nth(i).locator('option')
            choices = [options.nth(j).get_attribute('value') for j in range(options.count())]
            good = next((x for x in choices if x is not None and x != ''), None)
            assert good is not None, 'Select with no value'
            selects.nth(i).select_option(good)
        return 'completar'

    if page.locator(root + ' .palavras .pal').count():
        tap(page, root + ' .palavras .pal', 'word')
        tap(page, '.casca [data-c-acoes] [data-confirmar]', 'confirm words')
        return 'sublinhar'

    if page.locator(root + ' .ordem .soltos button.op').count():
        initial = page.locator(root + ' .ordem .soltos button.op').count()
        for _ in range(initial):
            tap(page, root + ' .ordem .soltos button.op', 'order part')
        return 'ordenar/frase/versos'

    if page.locator(root + ' .classes').count() and page.locator(root + ' .soltos [data-e]').count():
        n = page.locator(root + ' .soltos [data-e]').count()
        for _ in range(n):
            tap(page, root + ' .soltos [data-e]', 'classifiable')
            tap(page, root + ' .classes [data-d="0"]', 'class target')
        return 'classe'

    if page.locator(root + ' .pares .col.esq [data-e]').count():
        n = page.locator(root + ' .pares .col.esq [data-e]').count()
        # The same original index on both sides is a legal, uniquely mapped guess
        # when the engine renders one-to-one pairing rather than classification.
        for i in range(n):
            tap(page, root + f' .pares .col.esq [data-e="{i}"]', 'left match')
            tap(page, root + f' .pares .col.dir [data-d="{i}"]', 'right match')
        return 'emparelhar'

    if page.locator(root + ' .calcada-v .pedra').count():
        tap(page, root + ' .calcada-v .pedra', 'calçada')
        if page.locator('.casca [data-c-acoes] [data-confirmar]:enabled').count():
            tap(page, '.casca [data-c-acoes] [data-confirmar]', 'confirm calçada')
        return 'calcada'

    if page.locator(root + ' .ops button.op[data-j]').count():
        tap(page, root + ' .ops button.op[data-j]', 'answer choice')
        return 'choice'

    raise AssertionError('No supported active input: ' +
                         page.locator('#baralho .cartao').inner_text()[:350])


def traverse(browser, host, id_, legacy=None):
    ctx = browser.new_context(viewport={'width': 390, 'height': 850},
                              reduced_motion='reduce')
    if legacy:
        key = 'licao-m2-f' + id_
        val = json.dumps(json.dumps(legacy, ensure_ascii=False))
        ctx.add_init_script(
            f"try {{ if (!localStorage.getItem({json.dumps(key)})) "
            f"localStorage.setItem({json.dumps(key)}, {val}); }} catch(e) {{}}"
        )
    page = ctx.new_page()
    issues = []
    page.on('pageerror', lambda error: issues.append(str(error)))
    page.route('**/fonts.googleapis.com/**', lambda route: route.abort())
    page.route('**/fonts.gstatic.com/**', lambda route: route.abort())
    url = f'{host}/m2/{ROUTES[id_]}/'
    r = page.goto(url, wait_until='domcontentloaded', timeout=30000)
    assert r and r.ok, f'{id_}: URL failed'
    page.locator('#baralho .cartao').wait_for(timeout=15000)
    assert not issues, f'{id_}: JS error on load: {issues}'
    if legacy:
        saved_view = page.locator('#baralho .cartao.fim').inner_text()
        assert 'Já feita' in saved_view or 'JÁ FEITA' in saved_view, \
               f'{id_}: previous completion not shown'
        assert '12 de 12' in saved_view, f'{id_}: previous best score not shown'
        button = page.locator('.casca [data-c-acoes] [data-repetir]')
        assert button.count() == 1, f'{id_}: new-attempt action absent'
        button.click()
        assert not page.locator('#baralho .cartao.fim').count(), \
               f'{id_}: new attempt did not start'
    visited = []
    for iteration in range(120):
        if page.locator('#baralho .cartao.fim').count():
            break
        before = page.locator('.casca [data-c-num]').first.inner_text()
        kind = respond(page)
        visited.append(kind)
        # An exercise's answer opens the feedback overlay, so its card number
        # advances only on the next iteration; a reading moves immediately.
        after = page.locator('.casca [data-c-num]').first.inner_text()
        if before == after and not page.locator('.casca [data-c-folha]:visible').count():
            raise AssertionError(f'{id_}: stalled at card {before}, action={kind}')
        if issues:
            raise AssertionError(f'{id_}: JS error after {kind}: {issues[:3]}')
    else:
        raise AssertionError(f'{id_}: did not finish in 120 actions')
    assert page.locator('#baralho .cartao.fim').count() == 1, f'{id_}: no final result'
    result_text = page.locator('#baralho .cartao.fim').inner_text()
    assert ('resultado' in result_text.lower() or 'lido até ao fim' in result_text.lower()), \
           f'{id_}: invalid result — {result_text[:250]!r}'
    key = ('licao-m2-f' + id_) if id_.isdigit() else ('epi-pt-longos-' + ROUTES[id_])
    state = page.evaluate("""key => {
      let value = localStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    }""", key)
    assert state and state.get('lida') and state.get('tentativas', 0) >= 1, \
           f'{id_}: completion was not saved under {key!r}: {state!r}'
    page.reload(wait_until='domcontentloaded', timeout=30000)
    page.locator('#baralho .cartao').wait_for(timeout=15000)
    newer = page.evaluate("""key=>JSON.parse(localStorage.getItem(key))""", key)
    assert newer and newer.get('lida') and newer.get('tentativas', 0) >= 1, \
           f'{id_}: lost saved progress'
    if legacy:
        assert newer.get('melhor', 0) >= legacy['melhor'], \
               f'{id_}: historical best score was reduced'
        assert newer.get('tentativas', 0) > legacy['tentativas'], \
               f'{id_}: historical attempt count not preserved'
    assert not issues, f'{id_}: JS errors after reload: {issues}'
    ctx.close()
    print(f'PASS full path: {id_}; actions={len(visited)}, '
          f'modes={sorted(set(visited))}', flush=True)
    return len(visited)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lessons', required=True)
    p.add_argument('--legacy-f07', action='store_true')
    args = p.parse_args()
    ids = [x.strip() for x in args.lessons.split(',')]
    assert ids and all(x in ROUTES for x in ids)
    server = ThreadingHTTPServer(('127.0.0.1', 0),
                                 partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True,
                                         args=['--disable-dev-shm-usage', '--no-sandbox'])
            total = 0
            for id_ in ids:
                total += traverse(browser, f'http://127.0.0.1:{server.server_port}', id_)
            if args.legacy_f07:
                historical = {
                    'lida': True, 'tentativas': 3, 'melhor': 12,
                    'totalMelhor': 12, 'certas': 12, 'total': 12,
                    'xp': 125, 'seq': 3, 't': 1790000000000
                }
                actions = traverse(
                    browser, f'http://127.0.0.1:{server.server_port}',
                    '07', legacy=historical
                )
                print(f'PASS legacy F07: historical best 12/12 preserved '
                      f'after {actions} navigation actions')
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {len(ids)} complete M2 routes, {total} navigation actions')


if __name__ == '__main__':
    main()
