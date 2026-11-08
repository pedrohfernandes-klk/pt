"""08/11/2026: decisão 152 (cuidado em todas as lições), módulo M2. As tabelas novas e as referências que não se partem, no
navegador, com o CSS e o motor reais, no modelo de tests/browser_cuidado_m1.py:
* as 6 tabelas novas (F02, F06, F07 duas, F09 e a página «Pensar devagar» A máquina de rir), a 360 e a 900 px, em tema claro e
  escuro: nada desliza para o lado e a tabela não sai do seu contentor; cada linha está visível e com as células todas; no telemóvel
  o cabeçalho sai do ecrã (fica para os leitores de ecrã), as células empilham e cada uma leva o rótulo da coluna (a célula vazia do
  monólogo não leva rótulo); no ecrã largo o cabeçalho vê-se e as células de cada linha ficam lado a lado; nenhuma palavra se parte a
  meio;
* a lista dos ficheiros do portefólio: no telemóvel empilha (o cabeçalho sai do ecrã), no ecrã largo é uma tabela com cabeçalho, e
  nenhum nome de ficheiro se parte;
* as referências e os números que o achado protege (U+00A0, U+2060), nas páginas e nos cartões onde estão: cada um fica numa só linha
  no ecrã, e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona).

Uso: python3 tests/browser_cuidado_m2.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_M2_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) de três tabelas novas e da lista do portefólio, a 360 e a 900 px."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import os
import sys
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler
sys.path.insert(0, str(ROOT / 'tests'))
from test_cuidado_m2 import TABELAS, LUGARES, VAZIAS, cartoes  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('CUIDADO_M2_OUTPUT')
# As três tabelas que ficam em captura: a de três colunas da F02, a do roteiro da F09 e a da máquina de rir.
CAPTURAS = {('m2/licao-m2-f02/index.html', 0): 'f02-recursos', ('m2/licao-m2-f09/index.html', 0): 'f09-roteiro',
            ('m2/m2-maquina-de-rir/index.html', 0): 'maquina-pecas'}
N, J = '\xa0', '⁠'
# Referências nas páginas (tal como estão no HTML: só se procuram no texto que se vê).
PAGINAS = {
    'm2/index.html': ['1.º' + N + 'ano', '90' + N + 'minutos', '90' + N + 'min', '10' + N + 'min', '30' + N + '%', '10' + N + '%'],
    'm2/guia-da-tarefa-m2/index.html': ['1.º' + N + 'ano', '90' + N + 'minutos', '90' + N + 'min', '15' + N + 'min', '60' + N + 'min'],
    'm2/mapa-do-modulo-m2/index.html': ['1.º' + N + 'ano', 'c.' + N + '1465–' + J + 'c.' + N + '1536', 'M2-' + J + 'F01',
                                        'D.' + N + 'João' + N + 'III', '45' + N + 'minutos', '30' + N + '%', '90' + N + 'min'],
    'm2/portefolio-do-modulo-m2/index.html': ['1.º' + N + 'ano'],
    'tarefas/m2-u1/index.html': ['90' + N + 'min', '10' + N + 'min', '180' + N + 'a' + N + '240' + N + 'palavras', '80' + N + 'a' + N + '140',
                                 'D.' + N + 'João' + N + 'III', 'D.' + N + 'Maria' + N + 'II', '90' + N + 'minutos'],
    'tarefas/m2-u2/index.html': ['90' + N + 'min', '10' + N + 'min', '200' + N + 'a' + N + '260' + N + 'palavras', '50' + N + 'a' + N + '80'
                                 + N + 'palavras', 'D.' + N + 'Maria' + N + 'II', '90' + N + 'minutos'],
}
# Referências nos cartões (lições e páginas «Pensar devagar»): (página, cartão, referências).
CARTOES = [
    # (o da linha de vida, no cartão 1, só se vê depois de um toque; o do completar vê-se logo)
    ('m2/licao-m2-f01/index.html', 7, ['D.' + N + 'João' + N + 'III']),
    ('m2/licao-m2-f01/index.html', 3, ['(4' + N + 'min)']),
    ('m2/licao-m2-f07/index.html', 0, ['D.' + N + 'João' + N + 'III']),
    ('m2/licao-m2-f08/index.html', 0, ['180' + N + 'a' + N + '240' + N + 'palavras']),
    ('m2/licao-m2-f08/index.html', 1, ['25' + N + '%']),
    ('m2/licao-m2-f08/index.html', 2, ['D.' + N + 'Maria' + N + 'II', '(5' + N + 'min)']),
    ('m2/licao-m2-f08/index.html', 4, ['180–' + J + '240' + N + 'palavras']),
    ('m2/licao-m2-f09/index.html', 0, ['D.' + N + 'João' + N + 'III']),
    ('m2/licao-m2-f09/index.html', 2, ['30' + N + 'segundos', '(30' + N + 's)', 'D.' + N + 'Maria' + N + 'II']),
    ('m2/licao-m2-f11/index.html', 1, ['100' + N + 'a' + N + '130' + N + 'palavras']),
    ('m2/licao-m2-f12/index.html', 1, ['(3' + N + 'min)']),
    ('m2/licao-m2-f12/index.html', 8, ['(1' + N + 'min)']),
    ('m2/licao-m2-f13/index.html', 8, ['(1' + N + 'min)']),
    ('m2/licao-m2-f15/index.html', 3, ['17' + N + 'de' + N + 'janeiro' + N + 'de' + N + '2023']),
    ('m2/m2-maquina-de-rir/index.html', 0, ['20' + N + 'min']),
    ('m2/m2-ines-escolhe-duas-vezes/index.html', 0, ['22' + N + 'min']),
]

MEIO_DA_PALAVRA = '''t=>{const out=[];
 t.querySelectorAll('th,td').forEach(cell=>{const w=document.createTreeWalker(cell,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){let prevTop=null,prevCh='';for(let i=0;i<n.data.length;i++){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);const rs=r.getClientRects();if(!rs.length)continue;
   const top=Math.round(rs[0].top),ch=n.data[i];if(prevTop!==null&&top>prevTop+2&&!/\\s/.test(ch)&&!/[\\s\\u00ad\\-\\/–]/.test(prevCh))out.push(cell.textContent.trim().slice(0,30)+': '+prevCh+'|'+ch);prevTop=top;prevCh=ch}}});
 return out}'''

# Para cada referência no texto que se vê dentro de raiz (fora dos «details» fechados, que o Chromium ainda mede): quantas há, quais ficam em mais de uma linha no ecrã, e quantas linhas
# ocupa numa caixa de largura zero (com o texto da página e com espaços normais).
REFERENCIAS = '''([sel,agulha])=>{const raiz=document.querySelector(sel);const out={n:0,partidas:[],caixa:[],controlo:[]};
 const w=document.createTreeWalker(raiz,NodeFilter.SHOW_TEXT);let t;
 const linhas=(pai,texto)=>{const s=document.createElement('span');s.style.cssText='display:inline-block;width:0;white-space:normal;overflow-wrap:normal;word-break:normal;hyphens:none;vertical-align:top';
  const u=s.cloneNode();u.textContent='x';s.textContent=texto;pai.appendChild(u);pai.appendChild(s);const h=s.getBoundingClientRect().height,l=u.getBoundingClientRect().height;u.remove();s.remove();return Math.round(h/l)};
 while(t=w.nextNode()){let i=t.data.indexOf(agulha);while(i>=0){const r=document.createRange();r.setStart(t,i);r.setEnd(t,i+agulha.length);const rs=[...r.getClientRects()].filter(x=>x.width>0);
   if(rs.length&&t.parentElement.checkVisibility({contentVisibilityAuto:true,visibilityProperty:true,opacityProperty:false})){out.n++;const tops=rs.map(x=>Math.round(x.top));if(Math.max(...tops)-Math.min(...tops)>2)out.partidas.push(t.data.slice(Math.max(0,i-20),i+agulha.length+20));
    const pai=t.parentElement;out.caixa.push(linhas(pai,agulha));out.controlo.push(linhas(pai,agulha.replace(/\\u00a0/g,' ').replace(/\\u2060/g,'')))}
   i=t.data.indexOf(agulha,i+1)}}
 return out}'''


def esperado(rel, k):
    return next((cab, linhas) for r, i, cab, linhas in TABELAS if r == rel and i == k)


def mount(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-m2',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
    }''', card)


def confere(page, tabela, rel, k, largura, onde):
    cabecalho, linhas = esperado(rel, k)
    assert tabela.count() == 1, onde
    tabela.evaluate('t=>{for(let d=t.closest("details");d;d=d.parentElement&&d.parentElement.closest("details"))d.open=true}')
    tabela.scroll_into_view_if_needed()
    assert tabela.locator('thead th[scope="col"]').all_text_contents() == cabecalho, onde
    assert tabela.locator('tbody th[scope="row"]').all_text_contents() == [l[0] for l in linhas], onde
    for n, linha in enumerate(tabela.locator('tbody tr').all()):
        assert linha.is_visible(), (onde, n)
        celulas = linha.locator('th,td')
        assert celulas.count() == len(cabecalho), (onde, n)
        assert all(celulas.evaluate_all('els=>els.map(e=>getComputedStyle(e).display!=="none")')), (onde, n)
        caixas = celulas.evaluate_all('els=>els.map(e=>{const r=e.getBoundingClientRect();return [r.top,r.bottom,r.left,r.width]})')
        if largura <= 620:
            # No telemóvel, as células de cada linha empilham, uma por baixo da outra.
            assert all(caixas[i + 1][0] >= caixas[i][1] - 1 for i in range(len(caixas) - 1)), (onde, n, caixas)
            assert celulas.evaluate_all('els=>els.map(e=>getComputedStyle(e).display)') == ['block'] * len(cabecalho), (onde, n)
        else:
            # No ecrã largo, ficam lado a lado, na mesma linha.
            assert all(abs(caixas[i + 1][0] - caixas[0][0]) < 2 and caixas[i + 1][2] > caixas[i][2] for i in range(len(caixas) - 1)), (onde, n)
        for coluna in range(1, len(cabecalho)):
            td = linha.locator('td').nth(coluna - 1)
            if (rel, k, n, coluna) in VAZIAS:
                assert td.get_attribute('data-label') is None, (onde, n)
                assert td.evaluate('e=>getComputedStyle(e,"::before").content') in ('none', 'normal'), (onde, n)
            elif largura <= 620:
                rotulo = td.evaluate('e=>getComputedStyle(e,"::before").content')
                assert rotulo.startswith('attr(') or cabecalho[coluna] + ':' in rotulo, (onde, n, rotulo)
    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (onde, largura, 'desliza para o lado')
    assert tabela.evaluate('t=>t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1'), (onde, largura)
    assert tabela.evaluate(MEIO_DA_PALAVRA) == [], (onde, largura, tabela.evaluate(MEIO_DA_PALAVRA))
    cab = tabela.locator('thead')
    if largura <= 620:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'absolute', onde
    else:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'static', onde
        assert cab.is_visible(), onde
    th = tabela.locator('tbody th').first
    assert th.evaluate('e=>getComputedStyle(e).textTransform') == 'none', onde
    assert th.evaluate('e=>getComputedStyle(e).backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent'), onde


def confere_referencias(page, sel, agulhas, onde):
    for agulha in agulhas:
        r = page.evaluate(REFERENCIAS, [sel, agulha])
        assert r['n'] >= 1, (onde, repr(agulha), 'não aparece no texto que se vê')
        assert r['partidas'] == [], (onde, repr(agulha), r['partidas'])
        assert set(r['caixa']) == {1}, (onde, repr(agulha), r['caixa'])
        assert min(r['controlo']) > 1, (onde, repr(agulha), r['controlo'])


def captura(alvo, nome, largura):
    if SAIDA:
        Path(SAIDA).mkdir(parents=True, exist_ok=True)
        alvo.screenshot(path=str(Path(SAIDA) / f'{nome}-{largura}.png'))


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
    referencias = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for largura in LARGURAS:
                for esquema in ('light', 'dark'):
                    ctx = browser.new_context(viewport={'width': largura, 'height': 900}, device_scale_factor=1,
                                              color_scheme=esquema, reduced_motion='reduce')
                    page = ctx.new_page()
                    erros = []
                    page.on('pageerror', lambda e: erros.append(str(e)))
                    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
                    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
                    page.route('**/www.youtube*.com/**', lambda r: r.abort())
                    # As tabelas novas, cada uma no seu cartão.
                    for (rel, k), (indice, _) in sorted(LUGARES.items()):
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        tabela = page.locator('#baralho .cartao .ler .apoio-tabela').nth(k)
                        onde = f'{rel} cartão {indice} tabela {k}'
                        confere(page, tabela, rel, k, largura, onde)
                        if esquema == 'light' and (rel, k) in CAPTURAS:
                            captura(page.locator('#baralho .cartao').first, CAPTURAS[(rel, k)], largura)
                        print('PASS tabela:', rel, indice, k, largura, esquema, flush=True)
                    # A lista dos ficheiros do portefólio.
                    rel = 'm2/portefolio-do-modulo-m2/index.html'
                    page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                    lista = page.locator('table.lista-ficheiros')
                    assert lista.count() == 1
                    lista.scroll_into_view_if_needed()
                    assert lista.locator('tbody tr').count() == 15
                    assert lista.locator('thead th[scope="col"]').all_text_contents() == ['Nome do ficheiro', 'O que é']
                    codigos = lista.locator('tbody code')
                    assert codigos.count() == 15
                    # Nenhum nome se parte (cada <code> numa só linha) nem sai da página.
                    assert codigos.evaluate_all('els=>els.filter(e=>e.getClientRects().length!==1).map(e=>e.textContent)') == []
                    assert codigos.evaluate_all('els=>els.filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>e.textContent)') == []
                    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (rel, largura)
                    if largura <= 560:
                        assert lista.locator('thead').evaluate('e=>getComputedStyle(e).position') == 'absolute'
                        assert set(lista.locator('tbody td').evaluate_all('els=>els.map(e=>getComputedStyle(e).display)')) == {'block'}
                    else:
                        assert lista.locator('thead').evaluate('e=>getComputedStyle(e).position') == 'static'
                        assert lista.locator('thead').is_visible()
                        assert lista.evaluate('e=>getComputedStyle(e).display') == 'table'
                    if esquema == 'light':
                        captura(lista, 'portefolio-lista', largura)
                    print('PASS lista do portefólio:', largura, esquema, flush=True)
                    # As referências e os números, nas páginas (com os «details» abertos) e nos cartões.
                    for rel, agulhas in PAGINAS.items():
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        # Abrem-se as secções; os «i» abrem-se como um leitor os abre, com um toque (o motor do «i» arruma o texto).
                        page.evaluate('()=>document.querySelectorAll("details:not(.info-i)").forEach(d=>d.open=true)')
                        if rel.startswith('tarefas/'):
                            # A tarefa mostra um cartão de cada vez (task-reader.js); aqui mostram-se todos, para medir o texto.
                            page.evaluate('()=>document.querySelectorAll("[id^=task-card-][hidden]").forEach(e=>e.hidden=false)')
                        if rel == 'm2/guia-da-tarefa-m2/index.html':
                            # Os blocos de hoje («Aquecer, 15 min»…) estão na rota da tarefa, que se abre quando se escolhe uma.
                            page.locator('button[data-n="3"]').first.click()
                            assert page.locator('#rota').is_visible()
                        confere_referencias(page, 'body', agulhas, f'{rel} {largura}')
                        referencias += len(agulhas)
                        if rel == 'm2/mapa-do-modulo-m2/index.html':
                            # O crédito de D. João III, no «i» da galeria «Para ver».
                            figura = page.locator('figure', has_text='Anthonis Mor').first
                            figura.scroll_into_view_if_needed()
                            figura.locator('summary').click()
                            assert figura.locator('.info-i-texto').is_visible()
                            page.evaluate('f=>f.setAttribute("data-qa-figura","")', figura.element_handle())
                            confere_referencias(page, '[data-qa-figura]', ['D.' + N + 'João' + N + 'III'], f'{rel} «i» {largura}')
                            referencias += 1
                        print('PASS referências:', rel, largura, esquema, flush=True)
                    for rel, indice, agulhas in CARTOES:
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        assert all(a in json.dumps(card, ensure_ascii=False) for a in agulhas), (rel, indice)
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        page.evaluate('()=>document.querySelectorAll("#baralho details:not(.info-i)").forEach(d=>d.open=true)')
                        confere_referencias(page, '#baralho .cartao', agulhas, f'{rel} cartão {indice} {largura}')
                        referencias += len(agulhas)
                        print('PASS referências:', rel, indice, largura, esquema, flush=True)
                    assert not erros, (largura, esquema, erros)
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    print(f'PASS: 6 tabelas novas do M2 e a lista do portefólio a 360 e 900 px, sem transbordar; {referencias} referências sem se partirem')


if __name__ == '__main__':
    main()
