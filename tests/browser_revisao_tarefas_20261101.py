"""01/11/2026: abertura, alvos de toque e impressão A4 da revisão das tarefas."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ('m1-u1', 'm3-u1', 'm3-u2', 'm5-u1', 'm5-u2', 'm6-u1', 'm6-u2', 'm7-u3')

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for width in (320, 390, 1366):
                for scheme in ('light', 'dark'):
                    ctx = browser.new_context(viewport={'width': width, 'height': 850}, color_scheme=scheme)
                    page = ctx.new_page()
                    page.route('https://fonts.googleapis.com/**', lambda r: r.abort())
                    page.route('https://fonts.gstatic.com/**', lambda r: r.abort())
                    for m in (3, 5, 6):
                        page.goto(f'{host}/m{m}/', wait_until='networkidle')
                        button = page.locator('[data-module-next]').bounding_box()
                        if width == 320:
                            assert button['y'] < 600, (m, width, button)
                        assert page.locator('details.regra p.avaliacao-tarefas').count() == 1
                        page.goto(f'{host}/m{m}/guia-da-tarefa-m{m}/', wait_until='networkidle')
                        size = page.locator('#arquivo-producoes > summary').bounding_box()
                        assert size['height'] >= (88 if width < 640 else 44), (m, width, size)
                    for slug in SLUGS:
                        page.goto(f'{host}/tarefas/{slug}/grelha/', wait_until='networkidle')
                        for link in page.locator('.g-tab td a').all():
                            assert link.bounding_box()['height'] >= 44, (slug, width)
                        assert page.locator('.ex b').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)') >= 13
                        page.goto(f'{host}/tarefas/{slug}/correcao/', wait_until='networkidle')
                        assert page.locator('.g-tab').first.evaluate('e=>e.scrollWidth<=e.clientWidth+1'), (slug, width)
                    ctx.close()
                    print('PASS apresentação', width, scheme, flush=True)
            page = browser.new_page()
            for slug in SLUGS:
                page.goto(f'{host}/tarefas/{slug}/correcao/', wait_until='networkidle')
                pdf = page.pdf(format='A4', prefer_css_page_size=True)
                pages = len(re.findall(rb'/Type\s*/Page\b', pdf))
                assert pages == 1, (slug, pages)
                print('PASS A4, uma página', slug, flush=True)
            browser.close()
    finally:
        server.shutdown()

if __name__ == '__main__':
    main()
