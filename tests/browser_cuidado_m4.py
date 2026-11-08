"""08/11/2026: decisão 152 (cuidado em todas as lições), módulo M4. As tabelas novas, a lista dos ficheiros do portefólio e as
referências que não se partem, no navegador, com o CSS e o motor reais, no modelo de tests/browser_cuidado_m1.py,
tests/browser_cuidado_m2.py e tests/browser_cuidado_m3.py:
* as 6 tabelas novas, a 360 e a 900 px, em tema claro e escuro: nada desliza para o lado e a tabela não sai do seu contentor;
  cada linha está visível e com as células todas; no telemóvel o cabeçalho sai do ecrã (fica para os leitores de ecrã), as células
  empilham e cada uma leva o rótulo da coluna; no ecrã largo o cabeçalho vê-se e as células de cada linha ficam lado a lado;
  nenhuma palavra se parte a meio. As cinco das lições (F06, F10 com duas, F14 e F25) montam-se no cartão onde estão, com os
  «Ler mais» abertos; nos dois cartões escuros («Para levar» da F06 e da F25), o cabeçalho e os rótulos do telemóvel têm a cor do
  texto do cartão (não ficam negro sobre negro nem cinzento sobre negro). A do guia vê-se abrindo o arquivo e o exemplo, dentro do
  div.ex, com a primeira coluna estreita no ecrã largo;
* no portefólio, os nomes dos ficheiros (todos em <code>) ficam numa só linha e a lista não desliza para o lado;
* as referências e os números que o achado protege (U+00A0, U+2060), nas páginas e nos cartões onde estão: cada um fica numa só linha
  no ecrã, e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona). Nas formas da proposta que deixam um espaço (datas com ano, listas, «aulas 1 a 8»),
  mede-se cada pedaço que não se parte.

Uso: python3 tests/browser_cuidado_m4.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_M4_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) de três tabelas novas (a dos atos de fala da F06, no cartão escuro, a dos peixes da F10 e a do guião do guia),
a 360 e a 900 px."""
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
from test_cuidado_m4 import TABELAS, LUGARES, ESCUROS, cartoes  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('CUIDADO_M4_OUTPUT')
CAPTURAS = {('m4/licao-m4-f06/index.html', 0): 'f06-atos-de-fala', ('m4/licao-m4-f10/index.html', 1): 'f10-quatro-peixes',
            ('m4/guia-da-tarefa-m4/index.html', 0): 'guia-guiao'}
N, J = '\xa0', '⁠'
# As páginas onde se vê cada banco de cartões (o da F28 vê-se na lição M4-F28).
PAGINA = {'m4/recursos/tpc-entrada.js': 'm4/licao-m4-f28/index.html'}
# Referências nas páginas (tal como estão no HTML: só se procuram no texto que se vê).
PAGINAS = {
    'm4/index.html': ['2.º' + N + 'ano', '90' + N + 'minutos', '90' + N + 'min', '25' + N + '%', '10' + N + '%', '15' + N + '%'],
    'm4/guia-da-tarefa-m4/index.html': ['2.º' + N + 'ano', '90' + N + 'min', 'aulas' + N + '1', 'a' + N + '18', '150' + N + 'a' + N + '200' + N + 'palavras',
                                        '220' + N + 'a' + N + '280' + N + 'palavras', '180' + N + 'a' + N + '240' + N + 'palavras', 'ato' + N + 'I',
                                        'capítulo' + N + 'V', '3' + N + 'minutos'],
    'm4/mapa-do-modulo-m4/index.html': ['2.º' + N + 'ano', '13' + N + 'de' + N + 'junho', 'de' + N + '1654', '4' + N + 'de' + N + 'agosto',
                                        'de' + N + '1578', '1608' + N + '–', '1799' + N + '–', 'M4-' + J + 'F01', '25' + N + '%', 'caps.' + N + 'II',
                                        'e' + N + 'III', 'aulas' + N + '9', 'a' + N + '15', '45' + N + 'minutos'],
    'm4/portefolio-do-modulo-m4/index.html': ['2.º' + N + 'ano', 'aulas' + N + '16', 'a' + N + '18'],
    'tarefas/m4-u1/index.html': ['90' + N + 'min', '10' + N + 'minutos', '150' + N + 'a' + N + '200' + N + 'palavras', '3' + N + 'a' + N + '4' + N + 'minutos'],
    'tarefas/m4-u2/index.html': ['90' + N + 'min', '10' + N + 'minutos', '180' + N + 'a' + N + '240' + N + 'palavras', 'ato' + N + 'I'],
    'tarefas/m4-u3-discurso/index.html': ['90' + N + 'min', '10' + N + 'minutos', '220' + N + 'a' + N + '280' + N + 'palavras', '2' + N + 'minutos'],
    'tarefas/m4-u3/index.html': ['100' + N + 'a' + N + '140' + N + 'palavras', '60' + N + 'min', 'M4-' + J + 'F11', 'cena' + N + 'XII'],
}
# Referências nos cartões (lições, banco da F28 e aquecimentos): (página, cartão, referências).
CARTOES = [
    ('m4/licao-m4-f01/index.html', 5, ['cap.' + N + 'I', '13' + N + 'de' + N + 'junho', 'de' + N + '1654']),
    ('m4/licao-m4-f02/index.html', 3, ['Mateus' + N + '5,' + N + '13']),
    ('m4/licao-m4-f04/index.html', 1, ['cap.' + N + 'IV']),
    ('m4/licao-m4-f07/index.html', 3, ['cenas' + N + 'XI', 'e' + N + 'XII']),
    ('m4/licao-m4-f08/index.html', 7, ['cenas' + N + 'XIV', 'e' + N + 'XV']),
    ('m4/licao-m4-f09/index.html', 1, ['ato' + N + 'III', 'cena' + N + 'XI']),
    ('m4/licao-m4-f10/index.html', 3, ['20' + N + 'segundos', '150' + N + 'a' + N + '200' + N + 'palavras']),
    ('m4/licao-m4-f11/index.html', 7, ['100' + N + 'a' + N + '140' + N + 'palavras']),
    ('m4/licao-m4-f14/index.html', 1, ['5' + N + 'de' + N + 'outubro', 'de' + N + '1915']),
    ('m4/licao-m4-f15/index.html', 1, ['cap.' + N + 'IV']),
    ('m4/licao-m4-f26/index.html', 6, ['ato' + N + 'II', 'cena' + N + 'II']),
    ('m4/recursos/tpc-entrada.js', 1, ['1799–' + J + '1854']),
    ('m4/recursos/tpc-entrada.js', 0, ['45' + N + 'minutos']),
    ('tarefas/m4-u2/aquecimento/index.html', 4, ['ato' + N + 'II', 'cena' + N + 'IV']),
    ('tarefas/m4-u3-discurso/aquecimento/index.html', 11, ['220' + N + 'a' + N + '280' + N + 'palavras']),
]

MEIO_DA_PALAVRA = '''t=>{const out=[];
 t.querySelectorAll('th,td').forEach(cell=>{const w=document.createTreeWalker(cell,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){let prevTop=null,prevCh='';for(let i=0;i<n.data.length;i++){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);const rs=r.getClientRects();if(!rs.length)continue;
   const top=Math.round(rs[0].top),ch=n.data[i];if(prevTop!==null&&top>prevTop+2&&!/\\s/.test(ch)&&!/[\\s\\u00ad\\-\\/–]/.test(prevCh))out.push(cell.textContent.trim().slice(0,30)+': '+prevCh+'|'+ch);prevTop=top;prevCh=ch}}});
 return out}'''

# Para cada referência no texto que se vê dentro de raiz: quantas há, quais ficam em mais de uma linha no ecrã, e quantas linhas
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
    return next((leg, cab, linhas) for r, i, leg, cab, linhas, _ in TABELAS if (r, i) == (rel, k))


def mount(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-m4',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
    }''', card)


def abrir_details(locator):
    locator.evaluate('t=>{for(let d=t.closest("details");d;d=d.parentElement&&d.parentElement.closest("details"))d.open=true}')


def confere(page, tabela, rel, k, largura, onde):
    legenda, cabecalho, linhas = esperado(rel, k)
    assert tabela.count() == 1, onde
    abrir_details(tabela)
    tabela.scroll_into_view_if_needed()
    assert tabela.locator('thead th[scope="col"]').all_text_contents() == cabecalho, onde
    assert tabela.locator('tbody th[scope="row"]').all_text_contents() == [l[0] for l in linhas], onde
    if legenda:
        # A legenda vê-se, por cima da tabela.
        cap = tabela.locator('caption')
        assert cap.inner_text().strip().lower() == legenda.lower(), onde
        assert cap.is_visible(), onde
    for n, linha in enumerate(tabela.locator('tbody tr').all()):
        assert linha.is_visible(), (onde, n)
        celulas = linha.locator('th,td')
        assert celulas.count() == len(cabecalho), (onde, n)
        caixas = celulas.evaluate_all('els=>els.map(e=>{const r=e.getBoundingClientRect();return [r.top,r.bottom,r.left,r.width]})')
        if largura <= 620:
            # No telemóvel, as células de cada linha empilham, uma por baixo da outra, e cada td leva o rótulo da sua coluna.
            assert all(caixas[i + 1][0] >= caixas[i][1] - 1 for i in range(len(caixas) - 1)), (onde, n, caixas)
            assert celulas.evaluate_all('els=>els.map(e=>getComputedStyle(e).display)') == ['block'] * len(cabecalho), (onde, n)
            for coluna in range(1, len(cabecalho)):
                rotulo = linha.locator('td').nth(coluna - 1).evaluate('e=>getComputedStyle(e,"::before").content')
                assert rotulo.startswith('attr(') or cabecalho[coluna] + ':' in rotulo, (onde, n, rotulo)
        else:
            # No ecrã largo, ficam lado a lado, na mesma linha.
            assert all(abs(caixas[i + 1][0] - caixas[0][0]) < 2 and caixas[i + 1][2] > caixas[i][2] for i in range(len(caixas) - 1)), (onde, n)
    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (onde, largura, 'desliza para o lado')
    assert tabela.evaluate('t=>t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1'), (onde, largura)
    assert tabela.evaluate(MEIO_DA_PALAVRA) == [], (onde, largura, tabela.evaluate(MEIO_DA_PALAVRA))
    cab = tabela.locator('thead')
    if largura <= 620:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'absolute', onde
    else:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'static', onde
        assert cab.is_visible(), onde
        if rel == 'm4/guia-da-tarefa-m4/index.html':
            # A parte do guião (uma palavra) fica numa coluna estreita; o texto fica com o resto.
            parte, texto = (tabela.locator('thead th').nth(i).evaluate('e=>e.getBoundingClientRect().width') for i in (0, 1))
            assert texto > 2 * parte, (onde, parte, texto)
    th = tabela.locator('tbody th').first
    assert th.evaluate('e=>getComputedStyle(e).textTransform') == 'none', onde
    assert th.evaluate('e=>getComputedStyle(e).backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent'), onde
    if (rel, k) in ESCUROS:
        # No cartão escuro, o cabeçalho (no ecrã largo) e os rótulos (no telemóvel) têm a cor do texto do cartão: não ficam negro
        # sobre negro nem cinzento sobre negro.
        cor = tabela.evaluate('t=>getComputedStyle(t).color')
        if largura <= 620:
            rotulos = tabela.locator('tbody td').evaluate_all('els=>els.map(e=>getComputedStyle(e,"::before").color)')
            assert set(rotulos) == {cor}, (onde, cor, rotulos)
        else:
            th0 = tabela.locator('thead th').first
            assert th0.evaluate('e=>getComputedStyle(e).backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent'), onde
            assert th0.evaluate('e=>getComputedStyle(e).color') == cor, onde


def confere_referencias(page, sel, agulhas, onde):
    for agulha in agulhas:
        r = page.evaluate(REFERENCIAS, [sel, agulha])
        assert r['n'] >= 1, (onde, repr(agulha), 'não aparece no texto que se vê')
        assert r['partidas'] == [], (onde, repr(agulha), r['partidas'])
        assert set(r['caixa']) == {1}, (onde, repr(agulha), r['caixa'])
        assert min(r['controlo']) > 1, (onde, repr(agulha), r['controlo'])


def confere_portefolio(page, largura):
    # Os nomes dos ficheiros (todos em <code>) ficam numa só linha, e a lista não desliza para o lado.
    codigos = page.locator('table td code')
    assert codigos.count() == 18, codigos.count()
    alturas = codigos.evaluate_all('els=>els.map(e=>{const rs=[...e.getClientRects()];return [e.textContent,rs.length,getComputedStyle(e).whiteSpace]})')
    assert all(n == 1 and ws == 'nowrap' for _, n, ws in alturas), (largura, [a for a in alturas if a[1] != 1 or a[2] != 'nowrap'])
    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (largura, 'desliza para o lado')
    assert page.evaluate('()=>{const t=document.querySelector("main table");return t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1}'), largura
    assert page.locator('table th[scope="col"]').count() == 2


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
    referencias = tabelas = 0
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
                    # As tabelas das lições, cada uma no seu cartão.
                    for (rel, k), (indice, _, _) in sorted(LUGARES.items()):
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        tabela = page.locator('#baralho .cartao .ler .apoio-tabela')
                        onde = f'{rel} cartão {indice}'
                        confere(page, tabela, rel, k, largura, onde)
                        tabelas += 1
                        if esquema == 'light' and (rel, k) in CAPTURAS:
                            captura(page.locator('#baralho .cartao').first, CAPTURAS[(rel, k)], largura)
                        print('PASS tabela:', rel, indice, largura, esquema, flush=True)
                    # A tabela do guia (fora das lições), no arquivo, dentro do exemplo da Tarefa 1.
                    rel = 'm4/guia-da-tarefa-m4/index.html'
                    page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                    tabela = page.locator('.apoio-tabela')
                    tabela.wait_for(state='attached')
                    confere(page, tabela, rel, 0, largura, rel)
                    assert tabela.evaluate('t=>t.parentElement.classList.contains("ex")'), rel
                    tabelas += 1
                    if esquema == 'light':
                        # Só para a captura: o cabeçalho fixo da página e o botão flutuante não tapam o exemplo.
                        page.evaluate('()=>{const t=document.querySelector(".topo");if(t)t.style.position="static";'
                                      'document.querySelectorAll(".projection-launcher,[data-projection-launcher],.pl-fab").forEach(e=>e.style.display="none")}')
                        captura(tabela.locator('xpath=ancestor::details[1]'), CAPTURAS[(rel, 0)], largura)
                    print('PASS fora das lições:', rel, largura, esquema, flush=True)
                    # O portefólio: os nomes dos ficheiros sem partir.
                    page.goto(host + '/m4/portefolio-do-modulo-m4/', wait_until='networkidle')
                    confere_portefolio(page, largura)
                    print('PASS portefólio:', largura, esquema, flush=True)
                    # As referências e os números, nas páginas (com os «details» abertos) e nos cartões.
                    for rel, agulhas in PAGINAS.items():
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        page.evaluate('()=>document.querySelectorAll("details:not(.info-i)").forEach(d=>d.open=true)')
                        if rel.startswith('tarefas/m4-u'):
                            # A tarefa mostra um cartão de cada vez (task-reader.js); aqui mostram-se todos, para medir o texto.
                            page.evaluate('()=>document.querySelectorAll("[id^=task-card-][hidden]").forEach(e=>e.hidden=false)')
                        confere_referencias(page, 'body', agulhas, f'{rel} {largura}')
                        referencias += len(agulhas)
                        print('PASS referências:', rel, largura, esquema, flush=True)
                    for rel, indice, agulhas in CARTOES:
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        assert all(a in json.dumps(card, ensure_ascii=False) for a in agulhas), (rel, indice)
                        page.goto(host + '/' + PAGINA.get(rel, rel).replace('index.html', ''), wait_until='networkidle')
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
    print(f'PASS: {tabelas // 4} tabelas novas do M4 a 360 e 900 px, nos dois temas, sem transbordar; os nomes do portefólio sem partir; '
          f'{referencias} referências sem se partirem')


if __name__ == '__main__':
    main()
