"""11/11/2026: decisão 152 (cuidado em todas as lições), módulo M7. As tabelas novas, as listas novas, o portefólio e as referências
que não se partem, no navegador, com o CSS e o motor reais, no modelo de tests/browser_cuidado_m1.py a tests/browser_cuidado_m6.py:
* as 3 tabelas novas, a 360 e a 900 px, em tema claro e escuro: nada desliza para o lado e a tabela não sai do seu contentor; cada
  linha está visível e com as células todas; no telemóvel o cabeçalho sai do ecrã (fica para os leitores de ecrã), as células
  empilham e cada uma leva o rótulo da coluna; no ecrã largo o cabeçalho vê-se e as células de cada linha ficam lado a lado; nenhuma
  palavra se parte a meio. As duas das lições (F01 e F23) montam-se no cartão onde estão (a da F01, dentro da dobra «As três
  vidas, segundo a carta», que se abre); a dos pesos vê-se no índice, abrindo «Como se cumpre uma unidade», com o rótulo à vista no
  parágrafo de cima e, no ecrã largo, a coluna do peso estreita (5,5 rem);
* as listas novas (o plano do texto da F10, ponto a ponto, e «Três antes de mim», no guia): à vista, com os itens todos e sem
  deslizar para o lado;
* no portefólio, os dezoito nomes dos ficheiros (todos em <code>) só mudam de linha nos pontos marcados (<wbr>, a seguir a «_»),
  nunca num hífen; nada desliza;
* as referências e os números que o achado protege (U+00A0, U+2060), nas páginas e nos cartões onde estão: cada um fica numa só linha
  no ecrã, e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona).

Uso: python3 tests/browser_cuidado_m7.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_M7_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) das três tabelas novas (a dos pesos do índice, a das três vidas da F01 e a dos termos da F23), a 360 e a 900 px,
nos dois temas."""
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
from test_cuidado_m7 import TABELAS, LUGARES, INDICE, F10, GUIA, PORTEFOLIO, cartoes  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('CUIDADO_M7_OUTPUT')
CAPTURAS = {'m7/licao-m7-f01/index.html': 'f01-as-tres-vidas', 'm7/licao-m7-f23/index.html': 'f23-recorda', INDICE: 'indice-pesos'}
N, J = '\xa0', '\u2060'
def r(*agulhas):
    """As referências escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return [a.replace('{N}', N).replace('{J}', J) for a in agulhas]


# Referências nas páginas (tal como estão no HTML: só se procuram no texto que se vê). Nas datas, a proposta do M7 prende o dia ao
# «de» e o ano ao «de»: cada metade fica inteira («13 de», «de 1888»); o mesmo nos pares «N e N» com nome antes («poemas II», «e IX»).
PAGINAS = {
    INDICE: r('3.º{N}ano', '90{N}minutos', '90{N}min', '22{N}min', '23{N}min', '10{N}a{N}15{N}min', '10{N}min', '35{N}%', '25{N}%', '10{N}%',
              '30{N}%', 'poemas{N}II', 'e{N}IX', 'poema{N}XX', 'D.{N}Sebastião', 'M7-{J}F10'),
    GUIA: r('3.º{N}ano', '90{N}minutos', '90{N}min'),
    'm7/mapa-do-modulo-m7/index.html': r('3.º{N}ano', '90{N}min', '35{N}%', '25{N}%', '10{N}%', '30{N}%', '45{N}minutos', '13{N}de', 'de{N}1888',
                                         '30{N}de', 'de{N}1935', '1.ª{N}edição', 'página{N}2', 'D.{N}Sebastião', 'D.{N}Henrique',
                                         'M7-{J}F01', 'M7-{J}F06', 'M7-{J}F34'),
    PORTEFOLIO: r('3.º{N}ano'),
    'm7/tabacaria/index.html': r('3.º{N}ano', '1.ª{N}publ', 'n.º{N}39', '15{N}de', 'de{N}1928'),
    'm7/lima-orpheu/index.html': r('Orpheu{N}2'),
    'm7/santa-rita-fato/index.html': r('Orpheu{N}2', '1889–{J}1918'),
    'm7/variacoes-rotulos/index.html': r('1944–{J}1984'),
    'm7/m7-fingidor-maquina/index.html': r('22{N}min'),
    'm7/m7-quatro-vozes-um-problema/index.html': r('23{N}min', 'n.º{N}2'),
    'm7/visita-casa-fernando-pessoa/index.html': r('3.º{N}ano'),
    'tarefas/m7-u1/index.html': r('90{N}min', '80{N}a{N}120{N}palavras', '10{N}a{N}15{N}minutos'),
    'tarefas/m7-u2/index.html': r('90{N}min', '100{N}a{N}150{N}palavras', '10{N}minutos'),
    'tarefas/m7-u3/index.html': r('10{N}min', '90{N}min', '60{N}minutos', '10{N}minutos', '180{N}a{N}220{N}palavras', '4{N}de', 'de{N}1578',
                                  '20{N}de', 'de{N}1933', 'v.{N}1', 'D.{N}Sebastião', 'D.{N}João'),
    'tarefas/m7-u3/aquecimento/index.html': r('180{N}a{N}220{N}palavras'),
    'tarefas/m7-u3/grelha/index.html': r('180{N}a{N}220{N}palavras', '90{N}palavras'),
    'tarefas/m7-u3/correcao/index.html': r('180{N}a{N}220{N}palavras'),
}
# No guia, os blocos de hoje («Aquecer, 15 min»…) e o produto estão na rota da tarefa, que se abre quando se escolhe uma.
ROTA = r('15{N}min', '60{N}min', '10{N}minutos', '100{N}a{N}150{N}palavras')
# Referências nos cartões das lições: (página, índice do cartão, referências que se veem nesse cartão).
L = 'm7/licao-m7-{}/index.html'
CARTOES = [
    (L.format('f01'), 1, r('8{N}de')), (L.format('f01'), 2, r('13{N}de', 'de{N}1935')), (L.format('f01'), 15, r('8{N}de', 'de{N}1914')),
    (L.format('f02'), 2, r('30{N}s', '1.ª{N}publicação', 'n.º{N}36')), (L.format('f02'), 7, r('2.ª{N}estrofe')),
    (L.format('f02'), 10, r('3.ª{N}estrofe')), (L.format('f02'), 11, r('n.º{N}38')), (L.format('f02'), 21, r('versos{N}2', 'e{N}3')),
    (L.format('f04'), 1, r('8{N}de', 'Poema{N}II')), (L.format('f04'), 7, r('verso{N}15')), (L.format('f04'), 11, r('poema{N}IX')),
    (L.format('f04'), 21, r('poema{N}II')),
    (L.format('f05'), 1, r('12{N}de', '1{N}de', 'n.º{N}1')), (L.format('f05'), 3, r('1{N}min', 'estrofes{N}1', 'a{N}5')),
    (L.format('f05'), 8, r('2.ª{N}estrofe')), (L.format('f05'), 24, r('3.ª{N}estrofe')),
    (L.format('f06'), 0, r('n.º{N}39')), (L.format('f06'), 1, r('15{N}de')), (L.format('f06'), 3, r('1{N}min')),
    (L.format('f06'), 11, r('4.º{N}verso')),
    (L.format('f08'), 0, r('1.ª{N}edição')), (L.format('f08'), 1, r('4{N}de', '10{N}de', '20{N}de', 'D.{N}Sebastião')),
    (L.format('f08'), 3, r('3{N}min')),
    (L.format('f09'), 0, r('D.{N}Sebastião', 'c.{N}1571')), (L.format('f09'), 1, r('1.ª{N}pessoa')), (L.format('f09'), 17, r('2.º{N}ano', 'D.{N}João')),
    (L.format('f09'), 20, r('4{N}de', 'de{N}1578')),
    (L.format('f10'), 0, r('século{N}XV', 'D.{N}Henrique')), (L.format('f10'), 1, r('25{N}%', '180{N}a{N}220{N}palavras')),
    (L.format('f10'), 18, r('1.º{N}verso')),
    (L.format('f11'), 4, r('D.{N}Sebastião')), (L.format('f11'), 9, r('15{N}de', 'de{N}1890')),
    (L.format('f13'), 0, r('n.º{N}2')), (L.format('f13'), 2, r('3.º{N}ano')), (L.format('f13'), 10, r('n.º{N}3')), (L.format('f13'), 14, r('5.ª{N}estrofe')),
    (L.format('f14'), 4, r('1.ª{N}estrofe')), (L.format('f14'), 15, r('6.º{N}verso')),
    (L.format('f15'), 6, r('2.ª{N}estrofe')),
    (L.format('f23'), 4, r('1.ª{N}publicação', 'n.º{N}1')), (L.format('f23'), 8, r('2.ª{N}estrofe')),
    (L.format('f34'), 1, r('Poema{N}I')), (L.format('f34'), 2, r('parte{N}VI', 'partes{N}I', 'e{N}II')), (L.format('f34'), 10, r('n.º{N}2')),
    (L.format('f34'), 13, r('poema{N}II')),
    (L.format('f35'), 16, r('2{N}min', 'poemas{N}II', 'e{N}IX', 'poema{N}XX')),
    (L.format('f36'), 0, r('2{N}de', 'de{N}1991', 'n.º{N}39', 'página{N}2')), (L.format('f36'), 2, r('vv.{N}1', 'a{N}4')),
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

# Os nomes do portefólio: onde muda de linha cada um (o carácter antes de cada quebra) e se é nowrap.
NOMES = '''els=>els.map(e=>{const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n,prevTop=null,prev='',quebras=[];
 while(n=w.nextNode()){for(let i=0;i<n.data.length;i++){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);const rs=r.getClientRects();if(!rs.length)continue;
  const top=Math.round(rs[0].top);if(prevTop!==null&&top>prevTop+2)quebras.push(prev);prevTop=top;prev=n.data[i]}}
 return [e.textContent,quebras,getComputedStyle(e).whiteSpace,e.innerHTML.includes('<wbr>')]})'''




def esperado(rel, k):
    return next((cab, linhas, larg) for r, i, cab, linhas, larg in TABELAS if r == rel and i == k)


def mount(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-m7',variar:false});
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
        assert celulas.all_text_contents() == linhas[n], (onde, n)
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
            # A coluna do peso só leva um número: é estreita (5,5 rem) e a do elemento fica com o resto.
            assert cabecalho == ['Elemento', 'Peso'], onde
            peso, elem = (tabela.locator('thead th').nth(i).evaluate('e=>e.getBoundingClientRect().width') for i in (1, 0))
            rem = page.evaluate('()=>parseFloat(getComputedStyle(document.documentElement).fontSize)')
            assert abs(peso - 5.5 * rem) < 2 and elem > 2 * peso, (onde, peso, elem, rem)
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
    # Os nomes dos ficheiros (todos em <code>, nowrap) só mudam de linha nos pontos marcados (<wbr>, a seguir a «_»), nunca num
    # hífen; e a lista não desliza para o lado.
    codigos = page.locator('table td code')
    assert codigos.count() == 18, codigos.count()
    nomes = codigos.evaluate_all(NOMES)
    for texto, quebras, ws, com_wbr in nomes:
        assert ws == 'nowrap', (largura, texto, ws)
        assert all(q == '_' for q in quebras), (largura, texto, quebras)
        assert com_wbr or not quebras, (largura, texto, quebras)
    assert sum(1 for *_, com_wbr in nomes if com_wbr) == 11, nomes
    sem_deslizar(page, f'portefólio {largura}')
    assert page.evaluate('()=>{const t=document.querySelector("main table");return t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1}'), largura
    return sum(1 for _, q, _, _ in nomes if q)


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
    referencias = tabelas = listas = quebras = 0
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
                        captura(page.locator('#baralho .cartao').first, f'{CAPTURAS[rel]}-{esquema}', largura)
                        print('PASS tabela:', rel, indice, largura, esquema, flush=True)
                    # A tabela dos pesos, no índice, em «Como se cumpre uma unidade» (os «details» onde está abrem-se em confere).
                    page.goto(host + '/m7/', wait_until='networkidle')
                    tabela = page.locator('.apoio-tabela')
                    tabela.wait_for(state='attached')
                    confere(page, tabela, INDICE, 0, largura, INDICE)
                    rotulo = tabela.locator('xpath=preceding-sibling::p[1]')
                    assert rotulo.inner_text() == 'Pesos na avaliação:' and rotulo.is_visible(), INDICE
                    assert tabela.locator('xpath=following-sibling::p[1]').inner_text() == 'Cada tarefa tem uma grelha /20.', INDICE
                    tabelas += 1
                    # Só para a captura: o cabeçalho fixo da página não tapa a regra.
                    page.evaluate('()=>document.querySelectorAll(".topo,.cz-header,header.topo").forEach(e=>e.style.position="static")')
                    captura(tabela.locator('xpath=..'), f'{CAPTURAS[INDICE]}-{esquema}', largura)
                    print('PASS fora das lições:', INDICE, largura, esquema, flush=True)
                    # As listas novas: o plano do texto da F10 (na dobra, que se abre) e «Três antes de mim», no guia.
                    page.goto(host + '/' + F10.replace('index.html', ''), wait_until='networkidle')
                    mount(page, cartoes((ROOT / F10).read_text('utf-8'))[1])
                    page.evaluate('()=>document.querySelectorAll("#baralho details").forEach(d=>d.open=true)')
                    plano = page.locator('#baralho .cartao details').filter(has_text='O plano do texto, ponto a ponto').locator('ul')
                    confere_lista(page, plano, 7, f'F10, o plano do texto {largura}')
                    listas += 1
                    captura(page.locator('#baralho .cartao').first, f'f10-plano-{esquema}', largura)
                    page.goto(host + '/' + GUIA.replace('index.html', ''), wait_until='networkidle')
                    # A regra está na rota da tarefa, que se abre escolhendo uma no arquivo das produções.
                    page.locator('#arquivo-producoes summary').click()
                    page.locator('button[data-n="1"]').first.click()
                    assert page.locator('#rota').is_visible()
                    confere_lista(page, page.locator('#rota .regra ol'), 3, f'guia, «Três antes de mim» {largura}')
                    listas += 1
                    confere_referencias(page, '#rota', ROTA, f'{GUIA} (rota) {largura}')
                    referencias += len(ROTA)
                    captura(page.locator('#rota .regra').filter(has_text='Três antes de mim'), f'guia-tres-antes-de-mim-{esquema}', largura)
                    print('PASS listas:', largura, esquema, flush=True)
                    # O portefólio: os nomes dos ficheiros só mudam de linha nos pontos marcados.
                    page.goto(host + '/' + PORTEFOLIO.replace('index.html', ''), wait_until='networkidle')
                    quebras += confere_portefolio(page, largura)
                    captura(page.locator('main table'), f'portefolio-lista-{esquema}', largura)
                    print('PASS portefólio:', largura, esquema, flush=True)
                    # As referências e os números, nas páginas (com os «details» abertos) e nos cartões.
                    for rel, agulhas in PAGINAS.items():
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        abrir(page)
                        confere_referencias(page, 'body', agulhas, f'{rel} {largura}')
                        referencias += len(agulhas)
                        print('PASS referências:', rel, largura, esquema, flush=True)
                    for rel, indice, agulhas in CARTOES:
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        assert all(a in json.dumps(card, ensure_ascii=False) for a in agulhas), (rel, indice)
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        page.evaluate('()=>document.querySelectorAll("#baralho details:not(.info-i)").forEach(d=>d.open=true)')
                        # Nas linhas de vida, cada data abre-se com um toque (li.aberta): abrem-se todas, para as medir.
                        page.evaluate('()=>document.querySelectorAll("#baralho .vida li").forEach(li=>li.classList.add("aberta"))')
                        confere_referencias(page, '#baralho .cartao', agulhas, f'{rel} cartão {indice} {largura}')
                        referencias += len(agulhas)
                        print('PASS referências:', rel, indice, [a.replace(N, ' ').replace(J, '') for a in agulhas], largura, esquema, flush=True)
                    assert not erros, (largura, esquema, erros)
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    # No telemóvel, pelo menos um nome comprido muda de linha (num ponto marcado): o detetor de quebras funciona.
    assert quebras >= 1, quebras
    print(f'PASS: {tabelas // 4} tabelas novas do M7 a 360 e 900 px, nos dois temas, sem transbordar; {listas // 4} listas novas; os nomes '
          f'do portefólio só a mudar de linha nos pontos marcados; {referencias} referências sem se partirem')


if __name__ == '__main__':
    main()
