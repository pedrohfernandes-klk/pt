"""Real Chromium page/navigation smoke for both unmodified long M2 case studies."""
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PATHS = ('m2-ines-escolhe-duas-vezes', 'm2-maquina-de-rir')


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0),
                                 partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    assertions = 0
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                                        args=['--no-sandbox', '--disable-dev-shm-usage'])
            for entry in PATHS:
                for width in (320, 390, 1440):
                    ctx = browser.new_context(viewport={'width': width, 'height': 850},
                                              reduced_motion='reduce')
                    page = ctx.new_page()
                    problems = []
                    page.on('pageerror', lambda e: problems.append(str(e)))
                    page.route('**/fonts.googleapis.com/**', lambda route: route.abort())
                    page.route('**/fonts.gstatic.com/**', lambda route: route.abort())
                    response = page.goto(
                        f'http://127.0.0.1:{server.server_port}/m2/{entry}/',
                        wait_until='domcontentloaded', timeout=30000)
                    assert response and response.ok, (entry, width, 'HTTP')
                    page.locator('#baralho .cartao').wait_for(timeout=15000)
                    assert not problems, (entry, width, problems)
                    over = page.evaluate('document.documentElement.scrollWidth - innerWidth')
                    assert over <= 3, (entry, width, over)
                    assertions += 3
                    if width == 390:
                        before = page.locator('.casca [data-c-num]').first.inner_text()
                        page.locator('.casca [data-seguinte]').first.click()
                        after = page.locator('.casca [data-c-num]').first.inner_text()
                        assert before != after, (entry, 'first transition')
                        assertions += 1
                        menu = page.locator('[data-c-menu]').first
                        menu.click()
                        panel = page.locator('[data-c-painel]').first
                        assert panel.is_visible(), (entry, 'menu did not open')
                        page.keyboard.press('Escape')
                        assert panel.is_hidden(), (entry, 'menu did not close')
                        assertions += 2
                    ctx.close()
                print('PASS long case:', entry, flush=True)
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS: {assertions} assertions for {len(PATHS)} extended routes')


if __name__ == '__main__':
    main()
