"""31/10/2026: percursos e guias das seis novas aulas de tarefa."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import threading

from playwright.sync_api import sync_playwright
from browser_task_aquecimentos import ROOT, QuietHandler, contexto, sem_deslizar
from browser_task_contract import assert_task_route, learning_storage


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for m in (3, 5, 6):
                for width, scheme in ((390, 'light'), (1366, 'dark')):
                    ctx, page, errors = contexto(browser, width, scheme)
                    page.goto(f'{host}/m{m}/', wait_until='networkidle')
                    units = json.loads(page.locator('#epi-unidades-pedagogicas').text_content())
                    before = learning_storage(page)
                    assert_task_route(page, m, units)
                    sem_deslizar(page, f'm{m} percurso {width}')
                    assert learning_storage(page) == before
                    if m == 5:
                        ids = page.locator('.unidade[data-u="2"] ol.passos > li').evaluate_all('(els)=>els.map(e=>e.id)')
                        assert ids[-3:] == ['m5-f15', 'aquecimento-unidade-2', 'tarefa-unidade-2']
                    page.goto(f'{host}/m{m}/?arquivo=1', wait_until='networkidle')
                    assert page.locator('#arquivo-percurso').is_visible()
                    page.goto(f'{host}/m{m}/guia-da-tarefa-m{m}/', wait_until='networkidle')
                    for u in (1, 2):
                        assert page.locator(f'a[href="../../tarefas/m{m}-u{u}/"]').is_visible()
                    page.locator('#arquivo-producoes summary').click()
                    page.locator('button.tarefa').first.click()
                    page.locator('#rota').wait_for(state='visible')
                    assert page.locator('#blocos .bloco b').all_inner_texts() == [
                        'Aquecer, 10 min', 'Ler o enunciado, 5 min', 'Produzir, 60 min', 'Rever e entregar, 15 min']
                    assert page.locator('#r-exemplo').is_hidden()
                    sem_deslizar(page, f'm{m} guia {width}')
                    assert not errors, errors
                    ctx.close()
                    print('PASS percurso, arquivo e guia', m, width, scheme, flush=True)
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
