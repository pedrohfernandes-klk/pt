"""Unit closure, challenge coverage and legacy-record regression in Chromium."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import json
import threading
import argparse
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler, new_page, ROOT
from browser_m2_complete import respond
from browser_task_contract import TASK_MODULES, assert_task_route, visit_task_from_route

PLAN = json.loads((ROOT / 'docs/pedagogia/percursos-unidades-20261020.json').read_text('utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--legacy-only', action='store_true')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for plan in ([] if args.legacy_only else PLAN):
                m = plan['module']
                for width in (320, 1440):
                    ctx, page = new_page(browser, width)
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    page.goto(f'{host}/m{m}/', wait_until='networkidle')
                    assert not errors, (m, errors)
                    if m in TASK_MODULES:
                        hrefs = assert_task_route(page, m, plan['units'])
                        # Full eight-page/card matrix runs in its separate CI driver.
                        visit_task_from_route(page, m, 1, hrefs[0])
                        # The former pools are optional archive practice, never unit gates.
                        page.locator('.route-teacher-tools > summary').click()
                        page.locator('.route-teacher-tools a[href="?arquivo=1#arquivo-percurso"]').click()
                        page.wait_for_url('**/?arquivo=1#arquivo-percurso')
                        assert page.locator('#arquivo-percurso').is_visible()
                        for unit in plan['units']:
                            n = unit['number']
                            captured = page.evaluate("""n => {
                              const mount=EPIJogo.montar, shuffle=EPIJogo.baralhar;
                              let result, bank=[];
                              try {
                                EPIJogo.baralhar=items=>{bank.push(...items.map(x=>x._l));return shuffle(items)};
                                EPIJogo.montar=cfg=>{result={ids:cfg.itens.map(x=>x._l),count:cfg.itens.length,key:cfg.chave}};
                                document.querySelector('[data-desafio="'+n+'"]').click();
                                return {...result,bank};
                              } finally {EPIJogo.montar=mount;EPIJogo.baralhar=shuffle;}
                            }""", n)
                            assert captured['count'] == 8, (m, n, captured)
                            assert set(captured['ids']).issubset(unit['lessons']), (m, n, captured)
                            # Inspect the full preserved input pool, not a probabilistic sample.
                            assert set(captured['bank']) == set(unit['lessons']), (m, n, captured)
                            prefix = 'desafio-' if m == 4 else 'desafio-unidade-v2-'
                            assert captured['key'] == f'{prefix}M{m}-u{n}'
                        page.locator('[data-desafio="1"]').click()
                        page.locator('.casca.sobreposta .cartao').wait_for()
                        assert not errors, (m, errors)
                    else:
                        assert page.locator('button[data-desafio]').count() == len(plan['units'])
                        # 23/10/2026 (plano de melhoria, fase 0): sem caixa de escrita na síntese; um registo oral / no caderno por unidade.
                        assert page.locator('fieldset[data-sintese]').count() == len(plan['units'])
                        assert page.locator('textarea[data-resp], button[data-copiar]').count() == 0
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'), (m, width, 'overflow')
                        for unit in plan['units']:
                            n = unit['number']
                            section = page.locator(f'.unidade[data-u="{n}"]')
                            assert section.locator('li[data-passo]').count() == len(unit['steps'])
                            assert section.locator('button[data-desafio]').count() == 1
                            assert section.locator('ol.passos').evaluate('(list) => Boolean(list.compareDocumentPosition(list.parentElement.querySelector(".desafio")) & Node.DOCUMENT_POSITION_FOLLOWING)')
                            captured = page.evaluate('''n => {
                              const original=EPIJogo.montar; let result;
                              EPIJogo.montar=cfg=>{result={ids:cfg.itens.map(x=>x._l),count:cfg.itens.length,key:cfg.chave}};
                              document.querySelector('[data-desafio="'+n+'"]').click();
                              EPIJogo.montar=original; return result;
                            }''', n)
                            assert captured['count'] == 8, (m, n, captured)
                            assert set(unit['lessons']).issubset(captured['ids']), (m, n, captured)
                        # Open the actual challenge engine, rather than only inspecting config.
                        page.locator('[data-desafio="1"]').click()
                        page.locator('.casca.sobreposta .cartao').wait_for()
                        assert not errors, (m, errors)
                    if m == 2 and width == 1440:
                        page.locator('.casca.sobreposta [data-c-menu]').click()
                        folder = ROOT.parent / 'qa-unit-images'
                        folder.mkdir(exist_ok=True)
                        page.screenshot(path=str(folder / 'm2-1440.png'), full_page=True)
                    print(f'PASS unit route M{m}; width={width}; checkpoints={len(plan["units"])}', flush=True)
                    ctx.close()
            # 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 passa à aula de tarefa, como M1, M4 e M7.
            # Os registos anteriores leem-se no arquivo (?arquivo=1), como texto e nunca como HTML; as perguntas
            # do arquivo continuam a gravar na chave própria; a síntese separada sai e a resposta anterior fica intacta.
            ctx, page = new_page(browser, 390)
            page.add_init_script('''localStorage.setItem('percurso-M2-u1','A minha resposta anterior <img src=x>');
              localStorage.setItem('desafio-M2-u1',JSON.stringify({ganho:true,melhor:8,total:8}));
              localStorage.setItem('licao-m2-f01',JSON.stringify({lida:true,melhor:10,total:12,xp:100}));''')
            page.goto(f'{host}/m2/?arquivo=1#arquivo-percurso', wait_until='networkidle')
            history = page.locator('#arquivo-percurso [data-route-history]')
            assert page.locator('#arquivo-percurso').is_visible()
            assert '<img src=x>' in history.inner_text()
            assert history.locator('img').count() == 0
            assert 'desafio-M2-u1' in history.inner_text() and '"ganho":true' in history.inner_text()
            assert 'lição feita' in page.locator('#m2-f01 [data-k]').inner_text()
            assert page.evaluate('JSON.parse(localStorage.getItem("licao-m2-f01")).melhor') == 10
            assert page.locator('[data-desafio-estado="1"]').inner_text() == 'Sem tentativas guardadas neste arquivo.'
            assert page.locator('textarea[data-resp], [data-sintese]').count() == 0
            assert not page.evaluate('(JSON.parse(localStorage.getItem("percurso-sintese-M2-u1")||"{}")).feita')
            assert page.evaluate('localStorage.getItem("percurso-M2-u1")').startswith('A minha resposta')
            assert page.locator('[data-passo="m2-f12"],[data-passo="m2-f13"]').count() == 0
            assert page.locator('.unit-complements a[href*="licao-m2-f12"]').count() == 1
            page.locator('.unit-complements').last.locator('summary').click()
            page.locator('.unit-complements a[href*="licao-m2-f12"]').focus()
            focused = page.evaluate('document.activeElement.outerHTML')
            assert page.evaluate('document.activeElement.getAttribute("href")').endswith('licao-m2-f12/'), focused
            print('PASS M2 legacy records in the archive, lesson progress and optional links', flush=True)
            for n in (1, 2):
                page.locator(f'[data-desafio="{n}"]').click()
                page.evaluate('document.querySelector(".casca.sobreposta .jogo-alvo").id="baralho"')
                for action in range(60):
                    if page.locator('#baralho .cartao.fim').count():
                        break
                    respond(page)
                else:
                    raise AssertionError('M2 archive challenge did not finish')
                saved = page.evaluate('k=>JSON.parse(localStorage.getItem(k))', f'desafio-unidade-v2-M2-u{n}')
                assert saved and saved['total'] == 8 and saved['tentativas'] >= 1, saved
                page.locator('.casca.sobreposta [data-c-menu]').click()
                print(f'PASS complete M2 archive challenge {n}: {action} actions; separate progress saved', flush=True)
            page.reload(wait_until='networkidle')
            assert page.evaluate('localStorage.getItem("percurso-sintese-M2-u1")') is None
            assert page.evaluate('localStorage.getItem("percurso-M2-u1")').startswith('A minha resposta')
            assert page.evaluate('localStorage.getItem("desafio-M2-u1")') == '{"ganho":true,"melhor":8,"total":8}'
            print('PASS no separate synthesis gate; previous response and challenge records stay untouched', flush=True)
            page.goto(f'{host}/m2/#m2-f12', wait_until='networkidle')
            assert page.locator('#m2-f12').is_visible()
            assert page.locator('#m2-f12').evaluate('el=>el.closest("details").open')
            print('PASS direct link reveals the complementary material in context', flush=True)
            ctx.close()
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
