"""Real full-lesson traversal of M2 card engines in Chromium.

Each run answers every displayed item (not necessarily correctly), advances to
the actual result, reloads, and checks local progress. This does not cover all
random combinations, external services, Safari, or learning outcomes.
"""
import argparse
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

    if page.locator(root + ' .classes .soltos [data-e]').count():
        n = page.locator(root + ' .classes .soltos [data-e]').count()
        for _ in range(n):
            tap(page, root + ' .classes .soltos [data-e]', 'classifiable')
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


def traverse(browser, host, id_):
    ctx = browser.new_context(viewport={'width': 390, 'height': 850},
                              reduced_motion='reduce')
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
    assert ('Resultado' in result_text or 'Lido até ao fim' in result_text), \
           f'{id_}: invalid result'
    state = page.evaluate("""() => Object.entries(localStorage).filter(([k,v])=>{
      try {let x=JSON.parse(v);return x && x.lida === true && typeof x.t === 'number';}
      catch(e){return false;}
    }).map(([k,v])=>({key:k,value:JSON.parse(v)}))""")
    assert state, f'{id_}: no saved progress'
    page.reload(wait_until='domcontentloaded', timeout=30000)
    page.locator('#baralho .cartao').wait_for(timeout=15000)
    newer = page.evaluate("""key=>JSON.parse(localStorage.getItem(key))""",
                          state[0]['key'])
    assert newer and newer.get('lida') and newer.get('tentativas', 0) >= 1, \
           f'{id_}: lost saved progress'
    assert not issues, f'{id_}: JS errors after reload: {issues}'
    ctx.close()
    print(f'PASS full path: {id_}; actions={len(visited)}, '
          f'modes={sorted(set(visited))}', flush=True)
    return len(visited)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lessons', required=True)
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
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {len(ids)} complete M2 routes, {total} navigation actions')


if __name__ == '__main__':
    main()
