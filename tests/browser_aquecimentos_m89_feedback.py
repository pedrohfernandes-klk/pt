"""01/11/2026: respostas certas e duas tentativas erradas nas quatro tarefas novas."""
from browser_aquecimentos_m2_feedback import (ThreadingHTTPServer, partial, QuietHandler, ROOT, threading, sync_playwright, verificar)

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            verificar(browser,f'http://127.0.0.1:{server.server_port}', tuple(f'm{m}-u{u}' for m in (8,9) for u in (1,2)))
            browser.close()
    finally:server.shutdown()


if __name__=='__main__':main()
