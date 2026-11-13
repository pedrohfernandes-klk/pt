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
                    # 08/11/2026: decisão 152 no M3 (achado 43): no guia do M3, o número e a unidade não se partem (U+00A0); nos
                    # outros, como estava. Os mesmos quatro blocos, pela mesma ordem.
                    # 08/11/2026: decisão 152 no M5 (achado 42): também no guia do M5, com a mesma exigência.
                    # 08/11/2026: decisão 152 no M6 (achado 33): também no guia do M6, com a mesma exigência.
                    sep = '\xa0' if m in (3, 5, 6) else ' '
                    # 12/11/2026: decisão do docente para as tarefas do M3 (camada tarefas_faceis_m3_20261112): no guia do M3, 10 minutos
                    # de leitura e 55 de produção, como no enunciado; no M5 e no M6, como estava. Os mesmos quatro blocos, pela mesma ordem.
                    # 13/11/2026: o mesmo no guia do M5 (camada tarefas_faceis_m5_20261113).
                    ler_min, produzir_min = (10, 55) if m in (3, 5) else (5, 60)
                    assert page.locator('#blocos .bloco b').all_inner_texts() == [
                        f'Aquecer, 10{sep}min', f'Ler o enunciado, {ler_min}{sep}min', f'Produzir, {produzir_min}{sep}min', f'Rever e entregar, 15{sep}min']
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
