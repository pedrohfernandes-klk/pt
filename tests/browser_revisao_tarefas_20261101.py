"""01/11/2026: abertura, alvos de toque e impressão A4 da revisão das tarefas."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
# 01/11/2026: acrescenta as quatro tarefas seguintes sem retirar a cobertura anterior.
SLUGS = ('m1-u1', 'm3-u1', 'm3-u2', 'm5-u1', 'm5-u2', 'm6-u1', 'm6-u2', 'm7-u3',
         'm8-u1', 'm8-u2', 'm9-u1', 'm9-u2')
# 01/11/2026: as nove versões de correção, para a impressão A4, e as quatro do M8 e do M9, que já iam à A4 pelo SLUGS.
CORRECOES = ('m1-u1', 'm1-u2', 'm3-u1', 'm3-u2', 'm5-u1', 'm5-u2', 'm6-u1', 'm6-u2', 'm7-u3',
             'm8-u1', 'm8-u2', 'm9-u1', 'm9-u2')

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
                    for m in (3, 5, 6, 8, 9):
                        page.goto(f'{host}/m{m}/', wait_until='networkidle')
                        button = page.locator('[data-module-next]').bounding_box()
                        if width == 320:
                            assert button['y'] < 600, (m, width, button)
                        assert page.locator('details.regra p.avaliacao-tarefas').count() == 1
                        page.goto(f'{host}/m{m}/guia-da-tarefa-m{m}/', wait_until='networkidle')
                        size = page.locator('#arquivo-producoes > summary').bounding_box()
                        # 01/11/2026: 44 px é o alvo do sistema; 88 px abria uma faixa vazia. O teto são duas linhas:
                        # 2 x 20,16 px (.9rem com 1.4) + 24 px de margem interior dão 64,3 px a 320 px, ou seja, 64 px.
                        assert 44 <= size['height'] < 64.5, (m, width, size)
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
            # 01/11/2026: largura útil do A4 com margens de 12 mm (210 - 24 = 186 mm, 703 px a 96 ppp), como na medição
            # da revisão; as nove correções, incluindo a do M1-U2, e as quatro do M8 e do M9.
            page.set_viewport_size({'width': 703, 'height': 1000})
            for slug in CORRECOES:
                page.goto(f'{host}/tarefas/{slug}/correcao/', wait_until='networkidle')
                page.emulate_media(media='print')
                # 01/11/2026: nenhum cabeçalho transborda na impressão
                assert page.evaluate("[...document.querySelectorAll('.g-tab thead th')].every(t=>t.scrollWidth<=t.clientWidth)"), slug
                # 01/11/2026: as caixas do comentário guardam espaço para escrever
                assert page.locator('.g-fb>div').first.evaluate("e=>e.getBoundingClientRect().height>=7*parseFloat(getComputedStyle(e).fontSize)"), slug
                pdf = page.pdf(format='A4', prefer_css_page_size=True)
                pages = len(re.findall(rb'/Type\s*/Page\b', pdf))
                assert pages == 1, (slug, pages)
                print('PASS A4, uma página', slug, flush=True)
            browser.close()
    finally:
        server.shutdown()

if __name__ == '__main__':
    main()
