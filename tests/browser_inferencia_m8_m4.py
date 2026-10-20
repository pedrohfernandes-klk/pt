"""Chromium QA: complete passages, exact feedback and persistence on M8/M4.

Requires playwright Chromium. Run:
    python tests/browser_inferencia_m8_m4.py
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    ('m8', '08'): [8, 13],
    ('m8', '09'): [10],
    ('m8', '12'): [6],
    ('m4', '27'): [3, 6, 12],
}
CHECKS = 0

def verify(expression, message):
    global CHECKS
    if not expression:
        raise AssertionError(message)
    CHECKS += 1

def cards(mod, num):
    source = (ROOT / mod / f'licao-{mod}-f{num}' / 'index.html').read_text('utf-8')
    return json.JSONDecoder().raw_decode(source.split('CARTOES=', 1)[1].lstrip())[0]

def tap(page, locator):
    page.locator(locator).first.click(timeout=6000)

def next_card(page):
    """Use the real engine; wrong answers are valid for navigation tests."""
    if page.locator('.casca [data-c-folha]:visible [data-seguinte]').count():
        tap(page, '.casca [data-c-folha]:visible [data-seguinte]')
        return 'feedback'
    if page.locator('.casca [data-c-acoes] [data-seguinte]').count():
        tap(page, '.casca [data-c-acoes] [data-seguinte]')
        return 'ler'
    root='#baralho'
    if page.locator(root+' .inline select').count():
        items=page.locator(root+' .inline select')
        for i in range(items.count()):
            opts=items.nth(i).locator('option')
            val=next((opts.nth(j).get_attribute('value')
                      for j in range(opts.count())
                      if opts.nth(j).get_attribute('value')),None)
            assert val is not None, 'No select value'
            items.nth(i).select_option(val)
        return 'lacunas'
    if page.locator(root+' .palavras button.pal').count():
        tap(page,root+' .palavras button.pal')
        tap(page,'.casca [data-c-acoes] [data-confirmar]')
        return 'sublinhar'
    if page.locator(root+' .ordem .soltos button.op').count():
        n=page.locator(root+' .ordem .soltos button.op').count()
        for _ in range(n):
            tap(page,root+' .ordem .soltos button.op')
        return 'ordenar'
    if page.locator(root+' .classes').count() and page.locator(root+' .soltos [data-e]').count():
        n=page.locator(root+' .soltos [data-e]').count()
        for _ in range(n):
            tap(page,root+' .soltos [data-e]')
            tap(page,root+' .classes [data-d="0"]')
        return 'classificar'
    if page.locator(root+' .pares .col.esq [data-e]').count():
        n=page.locator(root+' .pares .col.esq [data-e]').count()
        for i in range(n):
            tap(page,root+f' .pares .col.esq [data-e="{i}"]')
            tap(page,root+f' .pares .col.dir [data-d="{i}"]')
        return 'associar'
    if page.locator(root+' .ops button.op[data-j]').count():
        tap(page,root+' .ops button.op[data-j]')
        return 'escolha'
    raise AssertionError('Unknown input: '+page.locator('#baralho .cartao').inner_text()[:300])

def complete_lesson(page, mod, num):
    navigated=[]
    for _ in range(110):
        if page.locator('#baralho .cartao.fim').count():
            break
        last=page.locator('.casca [data-c-num]').first.inner_text()
        action=next_card(page)
        navigated.append(action)
        current=page.locator('.casca [data-c-num]').first.inner_text()
        if last==current and not page.locator('.casca [data-c-folha]:visible').count():
            raise AssertionError(f'{mod}-f{num}: stalled after {action}')
    else:
        raise AssertionError(f'{mod}-f{num}: 110 navigation actions without result')
    verify(page.locator('#baralho .cartao.fim').count()==1,f'{mod}-f{num}: no result')
    key=f'licao-{mod}-f{num}'
    before=page.evaluate("""key=>JSON.parse(localStorage.getItem(key))""",key)
    verify(bool(before and before.get('lida') and before.get('tentativas',0)>=1),
           f'{mod}-f{num}: no saved result')
    page.reload(wait_until='domcontentloaded',timeout=30000)
    page.locator('#baralho .cartao.fim').wait_for(timeout=12000)
    after=page.evaluate("""key=>JSON.parse(localStorage.getItem(key))""",key)
    verify(bool(after and after.get('lida') and after.get('tentativas')==before['tentativas']),
           f'{mod}-f{num}: saved result lost or altered after reload')
    print(f'PASS full: {mod}-f{num}, actions={len(navigated)}, types={sorted(set(navigated))}',flush=True)

def open_card(page,card,key):
    page.evaluate("""({item,key})=>{
      window.EPIJogo.montar({itens:[item],chave:key,marca:'QA',titulo:'QA',variar:false});
    }""",{'item':card,'key':key})
    modal=page.locator('.casca.sobreposta')
    modal.locator('.cartao').wait_for(timeout=10000)
    return modal

def close_card(page):
    modal=page.locator('.casca.sobreposta')
    if modal.count():
        modal.locator('[data-c-menu]').click(timeout=5000)
    verify(modal.count()==0,'QA overlay did not close')

def feedback_case(page,mod,num,index,card):
    verify(card['t']=='escolha',f'{mod}-f{num}:{index} not a choice')
    for wrong in range(len(card['o'])):
        if wrong==card['c']:
            continue
        for attempt in range(15):
            modal=open_card(page,card,f'qa-{mod}-{num}-{index}-{wrong}-{attempt}')
            if modal.locator(f'button.op[data-j="{wrong}"]').count():
                break
            close_card(page)
        else:
            raise AssertionError(f'{mod}-f{num}:{index} unavailable wrong option {wrong}')
        modal.locator(f'button.op[data-j="{wrong}"]').click()
        note=modal.locator('.casca-folha').inner_text()
        verify(card['fe'][wrong] in note,
               f'{mod}-f{num}:{index} missing specific feedback {wrong}')
        close_card(page)
    modal=open_card(page,card,f'qa-{mod}-{num}-{index}-right')
    modal.locator(f'button.op[data-j="{card["c"]}"]').click()
    verify('Certo.' in modal.locator('.casca-folha').inner_text(),
           f'{mod}-f{num}:{index} correct response not accepted')
    modal.locator('[data-seguinte]').click()
    verify(modal.locator('.cartao.fim').count()==1,
           f'{mod}-f{num}:{index} not completed')
    close_card(page)

def run_one(browser,host,mod,num):
    bank=cards(mod,num)
    for width in (320,390,1440):
        ctx=browser.new_context(viewport={'width':width,'height':850},
                                reduced_motion='reduce')
        page=ctx.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('**/fonts.googleapis.com/**',lambda route:route.abort())
        page.route('**/fonts.gstatic.com/**',lambda route:route.abort())
        resp=page.goto(f'{host}/{mod}/licao-{mod}-f{num}/',
                       wait_until='domcontentloaded',timeout=30000)
        verify(resp is not None and resp.ok,f'{mod}-f{num}/{width}: HTTP')
        page.locator('#baralho .cartao').wait_for(timeout=15000)
        verify(not errors,f'{mod}-f{num}/{width}: script errors {errors}')
        overflow=page.evaluate('document.documentElement.scrollWidth - innerWidth')
        verify(overflow<=3,f'{mod}-f{num}/{width}: horizontal overflow {overflow}px')
        if width==390:
            complete_lesson(page,mod,num)
            for index in TARGETS[(mod,num)]:
                feedback_case(page,mod,num,index,bank[index])
            verify(not errors,f'{mod}-f{num}: JS exception after interactions: {errors}')
        ctx.close()

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),
                               partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True,
                    args=['--disable-dev-shm-usage','--no-sandbox'])
            host=f'http://127.0.0.1:{server.server_port}'
            for mod,num in TARGETS:
                run_one(browser,host,mod,num)
                print(f'PASS browser: {mod}-f{num}',flush=True)
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {CHECKS} browser assertions, 4 complete lessons')

if __name__=='__main__':
    main()
