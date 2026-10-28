"""Dedicated responsive task-lesson CI driver; intentionally separate from inventory."""
from functools import partial
from http.server import ThreadingHTTPServer
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler
from browser_task_contract import responsive_task_matrix, fallback_task_pages, grelha_pages

def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            responsive_task_matrix(browser, f'http://127.0.0.1:{server.server_port}')
            fallback_task_pages(browser, f'http://127.0.0.1:{server.server_port}')
            # 28/10/2026: grelhas /20 sem deslizar na horizontal (320 a 1440 px).
            grelha_pages(browser, f'http://127.0.0.1:{server.server_port}')
            browser.close()
    finally:
        server.shutdown()

if __name__ == '__main__':
    main()
