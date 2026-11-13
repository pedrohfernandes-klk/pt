"""06/11/2026: decisão 152 (cuidado em todas as lições), módulo M1. As 12 tabelas novas no navegador, com o CSS e o motor reais:
a 320, 390 e 1366 px, em tema claro e escuro, nada desliza para o lado; cada linha está visível e com as células todas; no
telemóvel o cabeçalho sai do ecrã (fica para os leitores de ecrã) e cada célula leva o rótulo da coluna; no ecrã largo o
cabeçalho vê-se. No cartão escuro («Para levar» da M1-F08, M1-F15 e M1-F20) o cabeçalho é uma linha da cor do texto e os
rótulos herdam essa cor. Fora das lições (índice do módulo, guia, tarefas e «Ler a fundo») o cabeçalho de linha não fica em
maiúsculas nem a negro. Nenhuma palavra se parte a meio (só nos espaços, nos hífenes e nas barras).

Uso: python3 tests/browser_cuidado_m1.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim."""
from functools import partial
from http.server import ThreadingHTTPServer
import argparse
import sys
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
from audit_cards import lesson_cards  # noqa: E402
from test_cuidado_m1 import TABELAS  # noqa: E402

LARGURAS = (320, 390, 1366)
# Lições: (página, índice do cartão, índice da tabela na página, cartão escuro).
LICOES = [('m1/licao-m1-f05/index.html', 5, 0, False), ('m1/licao-m1-f08/index.html', 18, 0, False),
          ('m1/licao-m1-f08/index.html', 19, 1, True), ('m1/licao-m1-f11/index.html', 14, 0, False),
          ('m1/licao-m1-f15/index.html', 19, 0, True), ('m1/licao-m1-f20/index.html', 16, 0, True),
          ('m1/licao-m1-f10/index.html', 1, 0, False)]
FORA = ['m1/index.html', 'm1/guia-da-tarefa-m1/index.html', 'tarefas/m1-u1/index.html', 'tarefas/m1-u2/index.html',
        'm1/gram-fonologia/index.html']

MEIO_DA_PALAVRA = '''t=>{const out=[];
 t.querySelectorAll('th,td').forEach(cell=>{const w=document.createTreeWalker(cell,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){let prevTop=null,prevCh='';for(let i=0;i<n.data.length;i++){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);const rs=r.getClientRects();if(!rs.length)continue;
   const top=Math.round(rs[0].top),ch=n.data[i];if(prevTop!==null&&top>prevTop+2&&!/\\s/.test(ch)&&!/[\\s\\u00ad\\-\\/–]/.test(prevCh))out.push(cell.textContent.trim().slice(0,30)+': '+prevCh+'|'+ch);prevTop=top;prevCh=ch}}});
 return out}'''


def esperado(rel, k):
    return next((cab, linhas) for r, i, cab, linhas in TABELAS if r == rel and i == k)


def mount(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-m1',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
    }''', card)


def confere(page, tabela, cabecalho, linhas, largura, onde):
    assert tabela.count() == 1, onde
    # Abre o «details» onde a tabela está (na M1-F05, «Um esquema curto e duas tentativas»; no índice, «Como se cumpre uma
    # unidade»; na «Ler a fundo», o esquema PEP/ASA).
    tabela.evaluate('t=>{for(let d=t.closest("details");d;d=d.parentElement&&d.parentElement.closest("details"))d.open=true}')
    tabela.scroll_into_view_if_needed()
    assert tabela.locator('thead th[scope="col"]').all_text_contents() == cabecalho, onde
    assert tabela.locator('tbody th[scope="row"]').all_text_contents() == [l[0] for l in linhas], onde
    for n, linha in enumerate(tabela.locator('tbody tr').all()):
        assert linha.is_visible(), (onde, n)
        celulas = linha.locator('th,td')
        assert celulas.count() == len(cabecalho), (onde, n)
        assert all(celulas.evaluate_all('els=>els.map(e=>e.getBoundingClientRect().width>0&&getComputedStyle(e).display!=="none")')), (onde, n)
    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (onde, largura, 'desliza para o lado')
    # A tabela não sai do seu contentor.
    assert tabela.evaluate('t=>t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1'), (onde, largura)
    assert tabela.evaluate(MEIO_DA_PALAVRA) == [], (onde, largura, tabela.evaluate(MEIO_DA_PALAVRA))
    cab = tabela.locator('thead')
    if largura <= 620:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'absolute', onde
        rotulo = tabela.locator('td[data-label]').first.evaluate('e=>getComputedStyle(e,"::before").content')
        assert rotulo.startswith('attr(') or ':' in rotulo, (onde, rotulo)
    else:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'static', onde
        assert cab.is_visible(), onde
    # O cabeçalho de linha não fica em maiúsculas nem com fundo (regras gerais de lesson.css).
    th = tabela.locator('tbody th').first
    assert th.evaluate('e=>getComputedStyle(e).textTransform') == 'none', onde
    assert th.evaluate('e=>getComputedStyle(e).backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent'), onde


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='servidor já aberto (por omissão, um próprio numa porta livre)')
    args = ap.parse_args()
    server = None
    if args.url:
        host = args.url.rstrip('/')
    else:
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for largura in LARGURAS:
                for esquema in ('light', 'dark'):
                    ctx = browser.new_context(viewport={'width': largura, 'height': 900}, color_scheme=esquema, reduced_motion='reduce')
                    page = ctx.new_page()
                    erros = []
                    page.on('pageerror', lambda e: erros.append(str(e)))
                    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
                    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
                    for rel, indice, k, escuro in LICOES:
                        cabecalho, linhas = esperado(rel, k)
                        card = lesson_cards(ROOT / rel)[indice]
                        assert bool(card.get('escuro')) == escuro, rel
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        tabela = page.locator('#baralho .cartao .ler .apoio-tabela')
                        onde = f'{rel} cartão {indice}'
                        confere(page, tabela, cabecalho, linhas, largura, onde)
                        assert page.locator('#baralho .cartao').evaluate('e=>e.classList.contains("escuro")') == escuro, onde
                        if escuro:
                            cor = page.locator('#baralho .cartao').evaluate('e=>getComputedStyle(e).color')
                            if largura <= 620:
                                rotulo = tabela.locator('td[data-label]').first.evaluate('e=>getComputedStyle(e,"::before").color')
                                assert rotulo == cor, (onde, rotulo, cor)
                            else:
                                th = tabela.locator('thead th').first
                                assert th.evaluate('e=>getComputedStyle(e).backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent'), onde
                                assert th.evaluate('e=>getComputedStyle(e).borderBottomColor') == cor, onde
                                assert th.evaluate('e=>getComputedStyle(e).color') == cor, onde
                        print('PASS lição:', rel, indice, largura, esquema, flush=True)
                    for rel in FORA:
                        cabecalho, linhas = esperado(rel, 0)
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        if rel.startswith('tarefas/'):
                            # 13/11/2026: as duas tarefas do M1 passaram ao molde «mais fácil de fazer» (camada tarefas_faceis_m1_20261113):
                            # a tabela dos tempos (momento e tempo) deu lugar a um só quadro, «Tempo e tamanho», com os tempos que o
                            # docente decidiu (10, 10, 55, 15). Exige-se dele o mesmo: é uma tabela com cabeçalhos de coluna e de
                            # linha, todas as linhas se veem, a página não desliza para o lado, o quadro não sai do contentor, nenhuma
                            # palavra se parte a meio e os números não se separam da unidade.
                            assert page.locator('.apoio-tabela').count() == 0 and page.locator('main[data-task-facil]').count() == 1, rel
                            quadro = page.locator('.tf-quadro')
                            assert quadro.count() == 1, rel
                            quadro.scroll_into_view_if_needed()
                            assert quadro.locator('thead th[scope="col"]').all_text_contents() == ['Tempo', 'O que fazes', 'Palavras'], rel
                            assert quadro.locator('tbody th').all_text_contents() == ['10\xa0min', '10\xa0min', '55\xa0min', '15\xa0min', '90\xa0min'], rel
                            assert quadro.locator('tbody tr').count() == 7 and all(l.is_visible() for l in quadro.locator('tbody tr').all()), rel
                            assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (rel, largura, 'desliza para o lado')
                            assert quadro.evaluate('t=>t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1'), (rel, largura)
                            assert quadro.evaluate(MEIO_DA_PALAVRA) == [], (rel, largura, quadro.evaluate(MEIO_DA_PALAVRA))
                            assert quadro.locator('thead').is_visible(), rel
                            print('PASS fora das lições (quadro «Tempo e tamanho»):', rel, largura, esquema, flush=True)
                            continue
                        if rel == 'm1/gram-fonologia/index.html':
                            page.get_by_role('button', name='Começar').click()
                        tabela = page.locator('.apoio-tabela')
                        tabela.wait_for(state='attached')
                        confere(page, tabela, cabecalho, linhas, largura, rel)
                        if largura > 620:
                            th = tabela.locator('thead th').first
                            assert th.evaluate('e=>getComputedStyle(e).textTransform') == 'none', rel
                        print('PASS fora das lições:', rel, largura, esquema, flush=True)
                    assert not erros, (largura, esquema, erros)
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    print('PASS: 12 tabelas novas do M1 a 320, 390 e 1366 px, sem deslizar para o lado')


if __name__ == '__main__':
    main()
