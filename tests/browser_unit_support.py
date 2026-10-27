"""Maps, task guides, portfolios and M2 lesson menus after regrouping."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler, new_page, ROOT
from browser_task_contract import TASK_MODULES, TASK_SLUGS


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for m in range(1, 10):
                for role in ('mapa-do-modulo', 'guia-da-tarefa', 'portefolio-do-modulo'):
                    ctx, page = new_page(browser, 320)
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    path = f'm{m}/{role}-m{m}/'
                    response = page.goto(f'http://127.0.0.1:{server.server_port}/{path}', wait_until='networkidle')
                    assert response.ok and not errors, (path, errors)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'), path
                    if role == 'guia-da-tarefa' and m in TASK_MODULES:
                        archive = page.locator('#arquivo-producoes')
                        assert archive.count() == 1 and not archive.evaluate('e=>e.open')
                        for slug in TASK_SLUGS[m]:
                            link = page.locator(f'a[href="../../tarefas/{slug}/"]')
                            assert link.count() == 1 and link.is_visible()
                            link.focus()
                            assert link.evaluate('e=>e===document.activeElement')
                        archive.locator(':scope > summary').focus()
                        archive.locator(':scope > summary').press('Enter')
                        assert archive.evaluate('e=>e.open')
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'), path
                    if role == 'mapa-do-modulo':
                        assert page.locator('#caminho .unidade-pedagogica').count() >= 2
                        assert page.locator('button[onclick="window.print()"]').count() == 1
                    print('PASS support: ' + path, flush=True)
                    ctx.close()
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
