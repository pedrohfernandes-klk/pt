"""Respostas certas e erradas em todos os tipos dos dois baralhos novos, a 390 px."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import threading
from playwright.sync_api import sync_playwright
from browser_task_aquecimentos import ROOT, QuietHandler, contexto, sem_deslizar


# 30/10/2026: aquecimento em cartões (decisão do docente)
def verificar(browser, host):
    for slug in ('m2-u1', 'm2-u2'):
        dados=json.loads((ROOT / 'docs/pedagogia/aquecimentos' / f'{slug}.json').read_text('utf-8'))
        for tentativa in (0, 1, 2):
            acertar = tentativa == 0
            ctx,page,errors=contexto(browser,390)
            page.goto(f'{host}/tarefas/{slug}/aquecimento/',wait_until='networkidle')
            for n,c in enumerate(dados['cartoes'],1):
                page.locator('#baralho .cartao').first.wait_for()
                sem_deslizar(page,f'{slug} {n} antes')
                t=c['t']
                if t=='ler':
                    page.locator('.casca [data-c-acoes] [data-seguinte]').click()
                    continue
                if t in ('escolha','rever'):
                    i=c['c'] if acertar else (c['c']+tentativa)%len(c['o'])
                    if t=='rever':
                        # 30/10/2026: confirmar a frase inteira após substituir apenas o trecho, em todas as opções.
                        preview=page.locator('#baralho [data-rever-prev]')
                        assert preview.inner_text()==c['frase'],(slug,n,preview.inner_text())
                        assert c['trecho']!=c['frase']
                        for j,opcao in enumerate(c['o']):
                            page.locator(f'#baralho .ops [data-j="{j}"]').click()
                            esperado_preview=c['frase'].replace(c['trecho'],opcao,1)
                            assert preview.inner_text()==esperado_preview,(slug,n,j,preview.inner_text(),esperado_preview)
                            sem_deslizar(page,f'{slug} {n} pré-visualização {j}')
                    page.locator(f'#baralho .ops [data-j="{i}"]').click()
                    if t=='rever':page.locator('.casca [data-rever-confirmar]').click()
                    esperado=c['f'] if acertar else c['fe'][i]
                elif t=='vf':
                    v=c['v'] if acertar else not c['v']
                    page.locator(f'#baralho .ops [data-j="{int(v)}"]').click()
                    esperado=c['f'] if acertar else c['fe']
                elif t=='completar':
                    for j,l in enumerate(c['lacunas']):
                        i=l['c'] if acertar else (l['c']+tentativa)%len(l['o'])
                        page.locator('#baralho .inline select').nth(j).select_option(label=l['o'][i])
                    esperado=c['f'] if acertar else c['fe']
                elif t=='ordenar':
                    sequencia=list(range(len(c['passos'])))
                    if not acertar:sequencia.reverse()
                    for i in sequencia:page.locator(f'#baralho .soltos [data-j="{i}"]').click()
                    esperado=c['f'] if acertar else c['fe']
                elif t=='emparelhar':
                    total=len(c['pares'])
                    for i in range(total):
                        page.locator(f'#baralho .esq [data-e="{i}"]').click()
                        j=i if acertar else (i+1)%total
                        page.locator(f'#baralho .dir [data-d="{j}"]').click()
                    esperado=c['f'] if acertar else c['fe']
                else:raise AssertionError(t)
                feedback=page.locator('.casca [data-c-folha]:visible')
                feedback.wait_for()
                assert esperado.replace('**','').replace('_','') in feedback.inner_text(),(slug,n,acertar,feedback.inner_text())
                sem_deslizar(page,f'{slug} {n} feedback')
                feedback.locator('[data-seguinte]').click()
            assert page.locator('#baralho .cartao.fim').count()
            assert not errors,errors
            print('PASS feedback M2',slug,'certo' if acertar else f'errado {tentativa}','10 cartões, seis tipos, 390 px',flush=True)
            ctx.close()


def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            verificar(browser,f'http://127.0.0.1:{server.server_port}')
            browser.close()
    finally:server.shutdown()


if __name__=='__main__':main()
