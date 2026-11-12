"""08/11/2026: decisão 152 (cuidado em todas as lições), módulo M6. As tabelas novas, a lista nova, o portefólio, os elementos das
grelhas em listas e as referências que não se partem, no navegador, com o CSS e o motor reais, no modelo de tests/browser_cuidado_m1.py
a tests/browser_cuidado_m5.py:
* as 11 tabelas novas, a 360 e a 900 px, em tema claro e escuro: nada desliza para o lado e a tabela não sai do seu contentor; cada
  linha está visível e com as células todas; no telemóvel o cabeçalho sai do ecrã (fica para os leitores de ecrã), as células
  empilham e cada uma leva o rótulo da coluna; no ecrã largo o cabeçalho vê-se e as células de cada linha ficam lado a lado; nenhuma
  palavra se parte a meio. As dez das lições (F02, F04, F05, F06, F07 e F09) montam-se no cartão onde estão; nas duas de termos
  (F02 e F06), no ecrã largo, a primeira coluna fica com 30 %; a de «Frases da rua» vê-se no primeiro passo, depois de «Começar»,
  dentro da nota;
* as listas novas (as regras de produção da F08 e os elementos de cada tema no critério 4 das duas grelhas): à vista, com os itens
  todos e sem deslizar para o lado;
* no portefólio, a tabela da lista de verificação: no telemóvel as células empilham, cada uma com o rótulo da coluna, e o cabeçalho
  sai do ecrã; no ecrã largo, o cabeçalho vê-se; os nomes dos ficheiros (todos em <code>) nunca mudam de linha; nada desliza;
* as referências e os números que o achado protege (U+00A0, U+2060), nas páginas e nos cartões onde estão: cada um fica numa só linha
  no ecrã, e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona).

Uso: python3 tests/browser_cuidado_m6.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_M6_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) de três tabelas novas (a de «O que vê e o que evoca» da F06, a de «Recorda» da F02 e a dos três testes de
«Frases da rua»), a 360 e a 900 px."""
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
from test_cuidado_m6 import TABELAS, LUGARES, cartoes  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('CUIDADO_M6_OUTPUT')
CAPTURAS = {('m6/licao-m6-f06/index.html', 0): 'f06-o-que-ve-e-o-que-evoca', ('m6/licao-m6-f02/index.html', 1): 'f02-recorda',
            ('m6/gram-oracoes-rua/index.html', 0): 'frases-da-rua-testes'}
N, J = '\xa0', '⁠'
RUA = 'm6/gram-oracoes-rua/index.html'
# Referências nas páginas (tal como estão no HTML: só se procuram no texto que se vê).
PAGINAS = {
    'm6/index.html': ['2.º' + N + 'ano', '90' + N + 'minutos', '90' + N + 'min', '22' + N + 'min', '30' + N + '%', '10' + N + '%',
                      'grelha' + N + '/20', 'Grelha' + N + '/20'],
    'm6/guia-da-tarefa-m6/index.html': ['2.º' + N + 'ano', '90' + N + 'minutos', '10' + N + 'minutos', '5' + N + 'minutos', '30' + N + '%',
                                        '10' + N + '%', 'grelha' + N + '/20'],
    'm6/mapa-do-modulo-m6/index.html': ['2.º' + N + 'ano', '1' + N + 'a' + N + '3', '1842–' + J + '1891', '1855–' + J + '1886',
                                        'século' + N + 'XX', '90' + N + 'minutos', '30' + N + '%', 'grelha' + N + '/20', 'Grelha' + N + '/20',
                                        'M6-' + J + 'F01', 'M6-' + J + 'F07'],
    'm6/portefolio-do-modulo-m6/index.html': ['2.º' + N + 'ano', '90' + N + 'minutos', '40' + N + '%', 'grelha' + N + '/20', 'Grelha' + N + '/20'],
    'tarefas/m6-u1/index.html': ['90' + N + 'min', '10' + N + 'min', '10' + N + 'minutos', '200' + N + 'a' + N + '240' + N + 'palavras',
                                 '90' + N + 'a' + N + '130', 'Grelha' + N + '/20'],
    'tarefas/m6-u2/index.html': ['90' + N + 'min', '15' + N + 'minutos', '200' + N + 'a' + N + '240' + N + 'palavras', 'século' + N + 'XIX',
                                 'parte' + N + 'II', '200' + N + 'exemplares', '31' + N + 'anos', 'Grelha' + N + '/20'],
    'tarefas/m6-u1/grelha/index.html': ['20' + N + 'valores', '200' + N + 'e' + N + '240' + N + 'palavras', '200' + N + 'a' + N + '240' + N
                                        + 'palavras', 'c.' + N + '1577'],
    'tarefas/m6-u2/grelha/index.html': ['20' + N + 'valores', '200' + N + 'e' + N + '240' + N + 'palavras'],
}
# No guia, os blocos de hoje («Aquecer, 10 min»…) estão na rota da tarefa, que se abre quando se escolhe uma (e esconde o resto).
ROTA = ['10' + N + 'min', '5' + N + 'min', '60' + N + 'min', '15' + N + 'min', 'grelha' + N + '/20']
# Referências nos cartões das lições: (página, referências); o cartão é o primeiro que as tem todas.
CARTOES = [
    ('m6/licao-m6-f01/index.html', ['1842' + N + 'a' + N + '1891', 'v.' + N + '7', 'v.' + N + '14']),
    ('m6/licao-m6-f01/index.html', ['4' + N + '+' + N + '4' + N + '+' + N + '3' + N + '+' + N + '3']),
    ('m6/licao-m6-f01/index.html', ['c.' + N + '1887']),
    ('m6/licao-m6-f02/index.html', ['2' + N + 'min']),
    ('m6/licao-m6-f04/index.html', ['M6-' + J + 'F07']),
    ('m6/licao-m6-f05/index.html', ['século' + N + 'XIX']),
    ('m6/licao-m6-f06/index.html', ['S.' + N + 'Petersburgo']),
    ('m6/licao-m6-f06/index.html', ['v.' + N + '20', 'v.' + N + '23']),
    ('m6/licao-m6-f07/index.html', ['v.' + N + '28']),
    ('m6/licao-m6-f08/index.html', ['c.' + N + '1900']),
    ('m6/licao-m6-f08/index.html', ['100' + N + 'a' + N + '130' + N + 'palavras', '4' + N + 'min']),
    # Na tabela das encomendas (o «peça» fica solto do número, como na proposta).
    ('m6/licao-m6-f08/index.html', ['30' + N + 'a' + N + '60' + N + 'segundos', '2' + N + 'a' + N + '3' + N + 'min', '3' + N + 'min']),
    ('m6/licao-m6-f11/index.html', ['31' + N + 'anos', '200' + N + 'exemplares']),
    ('m6/licao-m6-f11/index.html', ['25' + N + 'de' + N + 'fevereiro', '19' + N + 'de' + N + 'julho']),
    ('m6/licao-m6-f11/index.html', ['1855' + N + 'a' + N + '1886']),
    ('m6/licao-m6-f11/index.html', ['1' + N + 'min', '54' + N + 'segundos']),
    ('m6/licao-m6-f14/index.html', ['27' + N + 'de' + N + 'maio' + N + 'de' + N + '1871']),
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

# Os nomes do portefólio: em quantas linhas fica cada um e se é nowrap.
NOMES = '''els=>els.map(e=>{const tops=new Set([...e.getClientRects()].map(r=>Math.round(r.top)));return [e.textContent,tops.size,getComputedStyle(e).whiteSpace]})'''


def esperado(rel, k):
    return next((cab, linhas, larg) for r, i, cab, linhas, larg in TABELAS if r == rel and i == k)


def mount(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-m6',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
    }''', card)


def abrir(page):
    """Abre os «details» (salvo os «i») e mostra todos os cartões das tarefas (task-reader.js mostra um de cada vez)."""
    page.evaluate('()=>{document.querySelectorAll("details:not(.info-i)").forEach(d=>d.open=true);'
                  'document.querySelectorAll("[id^=task-card-][hidden]").forEach(e=>e.hidden=false)}')


def sem_deslizar(page, onde):
    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (onde, 'desliza para o lado')


def confere(page, tabela, rel, k, largura, onde):
    cabecalho, linhas, larguras = esperado(rel, k)
    assert tabela.count() == 1, onde
    tabela.evaluate('t=>{for(let d=t.closest("details");d;d=d.parentElement&&d.parentElement.closest("details"))d.open=true}')
    tabela.scroll_into_view_if_needed()
    assert tabela.is_visible(), onde
    assert tabela.locator('thead th[scope="col"]').all_text_contents() == cabecalho, onde
    assert tabela.locator('tbody th[scope="row"]').all_text_contents() == [l[0] for l in linhas], onde
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
    sem_deslizar(page, f'{onde} {largura}')
    assert tabela.evaluate('t=>t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1'), (onde, largura)
    assert tabela.evaluate(MEIO_DA_PALAVRA) == [], (onde, largura, tabela.evaluate(MEIO_DA_PALAVRA))
    cab = tabela.locator('thead')
    if largura <= 620:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'absolute', onde
    else:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'static', onde
        assert cab.is_visible(), onde
        if larguras:
            # Nas de termos, a primeira coluna (o recurso, o conceito) fica com 30 % da tabela.
            primeira, total = (tabela.evaluate(f'e=>{x}') for x in ('e.querySelector("thead th").getBoundingClientRect().width',
                                                                     'e.getBoundingClientRect().width'))
            assert abs(primeira / total - 0.30) < 0.02, (onde, primeira, total)
    th = tabela.locator('tbody th').first
    assert th.evaluate('e=>getComputedStyle(e).textTransform') == 'none', onde
    assert th.evaluate('e=>getComputedStyle(e).backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent'), onde


def confere_lista(page, lista, itens, onde):
    """Uma lista nova: à vista, com os itens todos, dentro do contentor e sem deslizar para o lado."""
    assert lista.count() == 1, onde
    lista.scroll_into_view_if_needed()
    assert lista.is_visible(), onde
    assert lista.locator(':scope > li').count() == itens, (onde, lista.locator(':scope > li').count())
    assert all(li.is_visible() for li in lista.locator(':scope > li').all()), onde
    assert lista.evaluate('l=>l.getBoundingClientRect().right<=l.parentElement.getBoundingClientRect().right+1'), onde
    sem_deslizar(page, onde)


def confere_referencias(page, sel, agulhas, onde):
    for agulha in agulhas:
        r = page.evaluate(REFERENCIAS, [sel, agulha])
        assert r['n'] >= 1, (onde, repr(agulha), 'não aparece no texto que se vê')
        assert r['partidas'] == [], (onde, repr(agulha), r['partidas'])
        assert set(r['caixa']) == {1}, (onde, repr(agulha), r['caixa'])
        assert min(r['controlo']) > 1, (onde, repr(agulha), r['controlo'])


def confere_portefolio(page, largura):
    """A lista de verificação do portefólio: os nomes (todos em <code>, nowrap) numa só linha; no telemóvel, as células empilham,
    cada uma com o rótulo da coluna, e o cabeçalho sai do ecrã; no ecrã largo, o cabeçalho vê-se; nada desliza para o lado."""
    tabela = page.locator('main table')
    assert tabela.count() == 1
    codigos = tabela.locator('td code')
    assert codigos.count() == 15, codigos.count()
    for texto, n, ws in codigos.evaluate_all(NOMES):
        assert ws == 'nowrap' and n == 1, (largura, texto, n, ws)
    linhas = tabela.locator('tbody tr')
    assert linhas.count() == 15
    for linha in linhas.all():
        celulas = linha.locator('td')
        caixas = celulas.evaluate_all('els=>els.map(e=>{const r=e.getBoundingClientRect();return [r.top,r.bottom,r.left]})')
        if largura <= 620:
            assert caixas[1][0] >= caixas[0][1] - 1, (largura, caixas)
            assert celulas.evaluate_all('els=>els.map(e=>getComputedStyle(e).display)') == ['block', 'block']
            rotulos = celulas.evaluate_all('els=>els.map(e=>getComputedStyle(e,"::before").content)')
            assert all(r.startswith('attr(') or ':' in r for r in rotulos), rotulos
        else:
            assert abs(caixas[1][0] - caixas[0][0]) < 2 and caixas[1][2] > caixas[0][2], (largura, caixas)
    posicao = tabela.locator('thead').evaluate('e=>getComputedStyle(e).position')
    assert posicao == ('absolute' if largura <= 620 else 'static'), (largura, posicao)
    sem_deslizar(page, f'portefólio {largura}')
    assert tabela.evaluate('t=>t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1'), largura


def captura(alvo, nome, largura):
    if SAIDA:
        Path(SAIDA).mkdir(parents=True, exist_ok=True)
        alvo.screenshot(path=str(Path(SAIDA) / f'{nome}-{largura}.png'))


def cartao_com(rel, agulhas):
    cards = cartoes((ROOT / rel).read_text('utf-8'))
    return next(c for c in cards if all(a in json.dumps(c, ensure_ascii=False) for a in agulhas))


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
    referencias = tabelas = listas = 0
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
                    for (rel, k), (indice, _, _, _) in sorted(LUGARES.items()):
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
                    # A tabela de «Frases da rua», no primeiro passo, dentro da nota.
                    page.goto(host + '/' + RUA.replace('index.html', ''), wait_until='networkidle')
                    page.get_by_role('button', name='Começar').click()
                    tabela = page.locator('.apoio-tabela')
                    tabela.wait_for(state='attached')
                    confere(page, tabela, RUA, 0, largura, RUA)
                    assert tabela.evaluate('t=>t.parentElement.classList.contains("nota")'), RUA
                    tabelas += 1
                    if esquema == 'light':
                        captura(tabela.locator('xpath=..'), CAPTURAS[(RUA, 0)], largura)
                    # A referência às fontes, no mesmo passo.
                    print('PASS «Ler a fundo»:', RUA, largura, esquema, flush=True)
                    # A lista nova da F08: as cinco regras de produção.
                    page.goto(host + '/m6/licao-m6-f08/', wait_until='networkidle')
                    mount(page, cartoes((ROOT / 'm6/licao-m6-f08/index.html').read_text('utf-8'))[2])
                    confere_lista(page, page.locator('#baralho .cartao .caixa ul'), 5, f'F08 regras de produção {largura}')
                    listas += 1
                    # Os elementos de cada tema no critério 4 das grelhas.
                    for slug in ('m6-u1', 'm6-u2'):
                        page.goto(host + f'/tarefas/{slug}/grelha/', wait_until='networkidle')
                        dd = page.locator('#criterio-4 dd').filter(has_text='Cumpres os cinco elementos')
                        for n, k in enumerate((5, 4)):
                            confere_lista(page, dd.locator('ul').nth(n), k, f'{slug} grelha, critério 4, lista {n} {largura}')
                            listas += 1
                    print('PASS listas:', largura, esquema, flush=True)
                    # O portefólio: a tabela empilhada no telemóvel e os nomes dos ficheiros sem mudar de linha.
                    page.goto(host + '/m6/portefolio-do-modulo-m6/', wait_until='networkidle')
                    confere_portefolio(page, largura)
                    if esquema == 'light':
                        captura(page.locator('main table'), 'portefolio-lista', largura)
                    print('PASS portefólio:', largura, esquema, flush=True)
                    # As referências e os números, nas páginas (com os «details» abertos) e nos cartões.
                    for rel, agulhas in PAGINAS.items():
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        abrir(page)
                        confere_referencias(page, 'body', agulhas, f'{rel} {largura}')
                        referencias += len(agulhas)
                        if rel == 'm6/guia-da-tarefa-m6/index.html':
                            page.locator('button[data-n="1"]').first.click()
                            assert page.locator('#rota').is_visible()
                            confere_referencias(page, '#rota', ROTA, f'{rel} (rota) {largura}')
                            referencias += len(ROTA)
                        print('PASS referências:', rel, largura, esquema, flush=True)
                    for rel, agulhas in CARTOES:
                        card = cartao_com(rel, agulhas)
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        page.evaluate('()=>document.querySelectorAll("#baralho details:not(.info-i)").forEach(d=>d.open=true)')
                        # Na «Linha de vida» da F11, cada data abre-se com um toque (li.aberta): abrem-se todas, para as medir.
                        page.evaluate('()=>document.querySelectorAll("#baralho .vida li").forEach(li=>li.classList.add("aberta"))')
                        confere_referencias(page, '#baralho .cartao', agulhas, f'{rel} {agulhas[0]!r} {largura}')
                        referencias += len(agulhas)
                        print('PASS referências:', rel, [a.replace(N, ' ').replace(J, '') for a in agulhas], largura, esquema, flush=True)
                    assert not erros, (largura, esquema, erros)
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    print(f'PASS: {tabelas // 4} tabelas novas do M6 a 360 e 900 px, nos dois temas, sem transbordar; {listas // 4} listas novas; o '
          f'portefólio empilhado e com os nomes sem partir; {referencias} referências sem se partirem')


if __name__ == '__main__':
    main()
