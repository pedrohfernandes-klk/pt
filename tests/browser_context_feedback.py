"""Rendered feedback checks for the contextual editorial corrections."""
from functools import partial
from http.server import ThreadingHTTPServer
import sys
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import QuietHandler, new_page, ROOT

sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for module, lesson, index, keyword in (
                    # 24/10/2026 (aulas claras M1, decisão do docente de 23/10): a lição foi refeita no molde do M4; os cartões verificados ficam iguais, mudam de propósito a contagem e os índices. M1-F11: 15, 16 e 19 passam a 8, 9 e 15.
                    ('m1', '11', 8, 'narrador construído'),
                    ('m1', '11', 9, 'Fernão Lopes é o autor'),
                    ('m1', '11', 15, 'contexto'),
                    ('m8', '03', 14, '1808'),
                    ('m8', '03', 15, 'Goya'),
                    ('m8', '03', 20, 'Goya'),
                    ('m8', '03', 22, '1919'),
                    ('m8', '03', 23, 'caderno'),
                    ('m9', '03', 12, 'perguntou dentro de quê')):
                path = f'{module}/licao-{module}-f{lesson}'
                card = lesson_cards(ROOT / path / 'index.html')[index]
                for width in (320, 1440):
                    ctx, page = new_page(browser, width)
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    page.goto(f'{host}/{path}/', wait_until='networkidle')
                    page.evaluate('card => EPIJogo.montar({itens:[card],chave:"qa-context",variar:false})', card)
                    modal = page.locator('.casca.sobreposta')
                    if card['t'] == 'vf':
                        button = modal.locator(f'[data-j="{int(card["v"])}"]')
                        button.focus()
                        button.press('Enter')
                    elif card['t'] == 'ordenar':
                        for i in range(len(card['passos'])):
                            button = modal.locator(f'.soltos button[data-j="{i}"]')
                            button.focus()
                            button.press('Enter')
                    elif card['t'] == 'completar':
                        for i, gap in enumerate(card['lacunas']):
                            modal.locator(f'select[data-k="{i}"]').select_option(str(gap['c']))
                    elif card['t'] == 'emparelhar':
                        targets = list(dict.fromkeys(p[1] for p in card['pares']))
                        for i, (_, target) in enumerate(card['pares']):
                            modal.locator(f'[data-e="{i}"]').click()
                            j = targets.index(target) if len(targets) < len(card['pares']) else i
                            modal.locator(f'[data-d="{j}"]').click()
                    text = modal.inner_text() if card['t'] == 'ler' else modal.locator('.casca-folha').inner_text()
                    assert keyword in text, (path, index, text)
                    if card['t'] != 'ler':
                        assert 'Certo.' in text, text
                    assert not errors, errors
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'), (path, index, width)
                    if width == 320:
                        folder = ROOT.parent / 'qa-images'
                        folder.mkdir(exist_ok=True)
                        page.screenshot(path=str(folder / f'{module}-f{lesson}-{index}.png'), full_page=True)
                    modal.locator('[data-seguinte]').click()
                    assert modal.locator('.cartao.fim').count() == 1
                    saved = page.evaluate('JSON.parse(localStorage.getItem("qa-context"))')
                    assert saved and saved['lida']
                    print(f'PASS context: {path}:{index}; width={width}', flush=True)
                    ctx.close()
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
