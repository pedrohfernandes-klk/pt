"""08/11/2026: decisão 152 (cuidado em todas as lições), módulo M5. As tabelas novas, as listas novas, os nomes dos ficheiros do
portefólio e as referências que não se partem, no navegador, com o CSS e o motor reais, no modelo de tests/browser_cuidado_m1.py a
tests/browser_cuidado_m4.py:
* as 7 tabelas novas, a 360 e a 900 px, em tema claro e escuro: nada desliza para o lado e a tabela não sai do seu contentor; cada
  linha está visível e com as células todas; no telemóvel o cabeçalho sai do ecrã (fica para os leitores de ecrã), as células
  empilham e cada uma leva o rótulo da coluna; no ecrã largo o cabeçalho vê-se e as células de cada linha ficam lado a lado; nenhuma
  palavra se parte a meio. As duas das lições (F11 e F13) montam-se no cartão onde estão; as dos pesos (índice, guia e mapa) veem-se
  abrindo a secção, com o rótulo à vista no parágrafo de cima e, no ecrã largo, a coluna do peso estreita (5,5 rem); as dos tempos
  das duas tarefas veem-se no cartão «Aquecer», com o rótulo por cima;
* as listas novas (F08, «Três antes de mim» do guia, os temas das duas tarefas e o critério 3 das duas grelhas): à vista, com os
  itens todos e sem deslizar para o lado;
* no portefólio, os nomes dos ficheiros (todos em <code>) só mudam de linha nos pontos marcados (<wbr>, a seguir a «_»), nunca num
  hífen, e a lista não desliza para o lado;
* as referências e os números que o achado protege (U+00A0, U+2060), nas páginas e nos cartões onde estão: cada um fica numa só linha
  no ecrã, e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona). Nas datas com ano, mede-se cada pedaço que não se parte («17 de» e «de 1807»).

Uso: python3 tests/browser_cuidado_m5.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_M5_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) de três tabelas novas (a de «Quem está à mesa» da F11, a dos pesos do índice e a dos tempos da M5-U1), a 360 e
a 900 px."""
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
from test_cuidado_m5 import TABELAS, LUGARES, cartoes  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('CUIDADO_M5_OUTPUT')
CAPTURAS = {'m5/licao-m5-f11/index.html': 'f11-quem-esta-a-mesa', 'm5/index.html': 'indice-pesos', 'tarefas/m5-u1/index.html': 'u1-tempos'}
N, J = '\xa0', '⁠'
FORA = ['m5/index.html', 'm5/guia-da-tarefa-m5/index.html', 'm5/mapa-do-modulo-m5/index.html', 'tarefas/m5-u1/index.html',
        'tarefas/m5-u2/index.html']
# O rótulo de cada tabela fora das lições, no parágrafo logo antes dela.
ROTULOS = {'m5/index.html': 'Pesos na avaliação:', 'm5/guia-da-tarefa-m5/index.html': 'Avaliação:', 'm5/mapa-do-modulo-m5/index.html': 'Avaliação:',
           'tarefas/m5-u1/index.html': 'No início da aula de tarefa:', 'tarefas/m5-u2/index.html': 'No início da aula de tarefa:'}
# Referências nas páginas (tal como estão no HTML: só se procuram no texto que se vê).
PAGINAS = {
    'm5/index.html': ['2.º' + N + 'ano', '90' + N + 'minutos', '90' + N + 'min', '10' + N + 'min', '25' + N + 'min', '30' + N + '%',
                      'século' + N + 'XIX', 'capítulo' + N + 'IV'],
    'm5/guia-da-tarefa-m5/index.html': ['2.º' + N + 'ano', '90' + N + 'minutos', '10' + N + 'minutos', '5' + N + 'minutos', '30' + N + '%',
                                        'século' + N + 'XIX'],
    'm5/mapa-do-modulo-m5/index.html': ['2.º' + N + 'ano', '1825–' + J + '1890', '1845–' + J + '1900', '90' + N + 'minutos', '30' + N + '%',
                                        'M5-' + J + 'F02', 'M5-' + J + 'F10', 'volume' + N + '1', 'século' + N + 'XIX'],
    'm5/portefolio-do-modulo-m5/index.html': ['2.º' + N + 'ano', '90' + N + 'minutos', '40' + N + '%', 'século' + N + 'XIX'],
    'tarefas/m5-u1/index.html': ['90' + N + 'min', '10' + N + 'min', '10' + N + 'minutos', 'cap.' + N + 'IV', '17' + N + 'de', 'de' + N + '1807'],
    'tarefas/m5-u2/index.html': ['90' + N + 'min', '3.ª' + N + 'pessoa', 'cap.' + N + 'VI', 'cap.' + N + 'I', '28' + N + 'de', 'de' + N + '2015',
                                 'de' + N + '2025'],
    'tarefas/m5-u1/grelha/index.html': ['cap.' + N + 'IV'],
    'tarefas/m5-u2/grelha/index.html': ['cap.' + N + 'I', '3.ª' + N + 'pessoa'],
    'tarefas/m5-u2/correcao/index.html': ['cap.' + N + 'I', '3.ª' + N + 'pessoa'],
    # Nas páginas «Ler a fundo», o subtítulo (as fontes estão no menu, fechado).
    'm5/eca-ramalhete/index.html': ['cap.' + N + 'I'],
    'm5/camilo-pai/index.html': ['cap.' + N + 'IV'],
    'm5/eca-hotel/index.html': ['cap.' + N + 'VI'],
}
# No guia, os blocos de hoje («Aquecer, 10 min»…) estão na rota da tarefa, que se abre quando se escolhe uma (e esconde o resto).
ROTA = ['10' + N + 'min', '5' + N + 'min', '60' + N + 'min', '15' + N + 'min']
# Referências nos cartões das lições: (página, cartão, referências).
CARTOES = [
    ('m5/licao-m5-f02/index.html', 3, ['folhas' + N + '232', '5' + N + 'min']),
    ('m5/licao-m5-f02/index.html', 7, ['17' + N + 'de', 'de' + N + '1807']),
    ('m5/licao-m5-f02/index.html', 19, ['1' + N + 'min']),
    ('m5/licao-m5-f04/index.html', 0, ['c.' + N + '1850']),
    ('m5/licao-m5-f08/index.html', 0, ['17' + N + 'de', 'de' + N + '1807']),
    # Na escolha, a opção certa (o motor mostra três das quatro opções).
    ('m5/licao-m5-f08/index.html', 3, ['17' + N + 'de', 'de' + N + '1807']),
    ('m5/licao-m5-f09/index.html', 1, ['3' + N + 'min']),
    ('m5/licao-m5-f10/index.html', 3, ['cap.' + N + 'I', 'D.' + N + 'Maria' + N + 'I', 'sr.' + N + 'D.' + N + 'João' + N + 'V', 'Leão' + N + 'X']),
    ('m5/licao-m5-f10/index.html', 0, ['volume' + N + '1', 'capítulo' + N + 'I']),
    ('m5/licao-m5-f11/index.html', 20, ['cap.' + N + 'VI']),
    ('m5/licao-m5-f12/index.html', 18, ['3.ª' + N + 'pessoa']),
    ('m5/licao-m5-f13/index.html', 0, ['c.' + N + '1895']),
    ('m5/licao-m5-f14/index.html', 2, ['M5-' + J + 'F10', 'capítulo' + N + 'I']),
    ('m5/licao-m5-f15/index.html', 1, ['8' + N + 'de', 'de' + N + '2025', '4' + N + 'min']),
    ('m5/licao-m5-f16/index.html', 3, ['capítulo' + N + 'I', 'capítulo' + N + 'III', 'vol.' + N + 'I', 'pp.' + N + '18–' + J + '19']),
    # A data da fotografia está na tabela dos créditos, atrás do «i» (abre-se para medir).
    ('m5/licao-m5-f17/index.html', 0, ['7' + N + 'de', 'de' + N + '1882']),
    ('m5/licao-m5-f17/index.html', 3, ['capítulo' + N + 'XII', 'p.' + N + '120', 'impressa' + N + '120']),
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


def esperado(rel):
    return next((cab, linhas) for r, _, cab, linhas, _ in TABELAS if r == rel)


def mount(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-m5',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
    }''', card)


def abrir(page):
    """Abre os «details» (salvo os «i») e mostra todos os cartões das tarefas (task-reader.js mostra um de cada vez)."""
    page.evaluate('()=>{document.querySelectorAll("details:not(.info-i)").forEach(d=>d.open=true);'
                  'document.querySelectorAll("[id^=task-card-][hidden]").forEach(e=>e.hidden=false)}')


def sem_deslizar(page, onde):
    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (onde, 'desliza para o lado')


def confere(page, tabela, rel, largura, onde):
    cabecalho, linhas = esperado(rel)
    assert tabela.count() == 1, onde
    tabela.evaluate('t=>{for(let d=t.closest("details");d;d=d.parentElement&&d.parentElement.closest("details"))d.open=true}')
    tabela.scroll_into_view_if_needed()
    assert tabela.is_visible(), onde
    assert tabela.locator('thead th[scope="col"]').all_text_contents() == cabecalho, onde
    assert tabela.locator('tbody th[scope="row"]').all_text_contents() == [l[0] for l in linhas], onde
    if rel in ROTULOS:
        # O rótulo fica à vista, no parágrafo logo antes da tabela.
        rotulo = tabela.locator('xpath=preceding-sibling::p[1]')
        assert rotulo.inner_text().strip() == ROTULOS[rel], onde
        assert rotulo.is_visible(), onde
        assert rotulo.evaluate('e=>e.getBoundingClientRect().bottom') <= tabela.evaluate('e=>e.getBoundingClientRect().top') + 1, onde
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
        if cabecalho == ['Elemento', 'Peso']:
            # A coluna do peso só leva um número: é estreita (5,5 rem) e a do elemento fica com o resto.
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
    assert codigos.count() == 15, codigos.count()
    nomes = codigos.evaluate_all(NOMES)
    for texto, quebras, ws, com_wbr in nomes:
        assert ws == 'nowrap', (largura, texto, ws)
        assert all(q == '_' for q in quebras), (largura, texto, quebras)
        assert com_wbr or not quebras, (largura, texto, quebras)
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
                    for (rel, k), (indice, _, _) in sorted(LUGARES.items()):
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        tabela = page.locator('#baralho .cartao .ler .apoio-tabela')
                        onde = f'{rel} cartão {indice}'
                        confere(page, tabela, rel, largura, onde)
                        tabelas += 1
                        if esquema == 'light' and rel in CAPTURAS:
                            captura(page.locator('#baralho .cartao').first, CAPTURAS[rel], largura)
                        print('PASS tabela:', rel, indice, largura, esquema, flush=True)
                    # As tabelas fora das lições (os pesos e os tempos da aula de tarefa).
                    for rel in FORA:
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        # Só os cartões das tarefas (task-reader.js mostra um de cada vez); os «details» onde está a tabela abrem-se em
                        # confere (os outros, como os menus, ficam fechados e não tapam a captura).
                        page.evaluate('()=>document.querySelectorAll("[id^=task-card-][hidden]").forEach(e=>e.hidden=false)')
                        tabela = page.locator('.apoio-tabela')
                        tabela.wait_for(state='attached')
                        confere(page, tabela, rel, largura, rel)
                        tabelas += 1
                        if esquema == 'light' and rel in CAPTURAS:
                            if rel == 'm5/index.html':
                                # Só para a captura: o cabeçalho fixo da página não tapa a regra.
                                page.evaluate('()=>document.querySelectorAll(".topo,.cz-header,header.topo").forEach(e=>e.style.position="static")')
                            captura(tabela.locator('xpath=..'), CAPTURAS[rel], largura)
                        print('PASS fora das lições:', rel, largura, esquema, flush=True)
                    # As listas novas.
                    card = cartoes((ROOT / 'm5/licao-m5-f08/index.html').read_text('utf-8'))[2]
                    page.goto(host + '/m5/licao-m5-f08/', wait_until='networkidle')
                    mount(page, card)
                    page.evaluate('()=>document.querySelectorAll("#baralho details").forEach(d=>d.open=true)')
                    for n, itens in enumerate((3, 4)):
                        confere_lista(page, page.locator('#baralho .cartao details ul').nth(n), itens, f'F08 lista {n} {largura}')
                        listas += 1
                    page.goto(host + '/m5/guia-da-tarefa-m5/', wait_until='networkidle')
                    # A regra está na rota da tarefa, que se abre escolhendo uma no arquivo das produções.
                    page.locator('#arquivo-producoes summary').click()
                    page.locator('button[data-n="1"]').first.click()
                    assert page.locator('#rota').is_visible()
                    confere_lista(page, page.locator('#rota .regra ol'), 3, f'guia, «Três antes de mim» {largura}')
                    listas += 1
                    for slug, tema in (('m5-u1', 'A'), ('m5-u2', 'B')):
                        page.goto(host + f'/tarefas/{slug}/', wait_until='networkidle')
                        abrir(page)
                        confere_lista(page, page.locator(f'article[data-task-theme="{tema}"] ol'), 5, f'{slug} tema {tema} {largura}')
                        assert page.locator(f'article[data-task-theme="{tema}"] p:empty').count() == 0, slug
                        listas += 1
                    for slug, itens in (('m5-u1', (5, 4)), ('m5-u2', (5, 5))):
                        page.goto(host + f'/tarefas/{slug}/grelha/', wait_until='networkidle')
                        dd = page.locator('#criterio-3 dd').filter(has_text='Cumpres os cinco elementos')
                        for n, k in enumerate(itens):
                            confere_lista(page, dd.locator('ul').nth(n), k, f'{slug} grelha, critério 3, lista {n} {largura}')
                            listas += 1
                    print('PASS listas:', largura, esquema, flush=True)
                    # O portefólio: os nomes dos ficheiros só mudam de linha nos pontos marcados.
                    page.goto(host + '/m5/portefolio-do-modulo-m5/', wait_until='networkidle')
                    quebras += confere_portefolio(page, largura)
                    print('PASS portefólio:', largura, esquema, flush=True)
                    # As referências e os números, nas páginas (com os «details» abertos) e nos cartões.
                    for rel, agulhas in PAGINAS.items():
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        abrir(page)
                        confere_referencias(page, 'body', agulhas, f'{rel} {largura}')
                        referencias += len(agulhas)
                        if rel == 'm5/guia-da-tarefa-m5/index.html':
                            page.locator('button[data-n="1"]').first.click()
                            assert page.locator('#rota').is_visible()
                            confere_referencias(page, '#rota', ROTA, f'{rel} (rota) {largura}')
                            referencias += len(ROTA)
                        print('PASS referências:', rel, largura, esquema, flush=True)
                    for rel, indice, agulhas in CARTOES:
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        assert all(a in json.dumps(card, ensure_ascii=False) for a in agulhas), (rel, indice)
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        page.evaluate('()=>document.querySelectorAll("#baralho details:not(.info-i)").forEach(d=>d.open=true)')
                        if (rel, indice) == ('m5/licao-m5-f17/index.html', 0):
                            page.evaluate('()=>document.querySelectorAll("#baralho details.info-i").forEach(d=>d.open=true)')
                        confere_referencias(page, '#baralho .cartao', agulhas, f'{rel} cartão {indice} {largura}')
                        referencias += len(agulhas)
                        print('PASS referências:', rel, indice, largura, esquema, flush=True)
                    assert not erros, (largura, esquema, erros)
                    ctx.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    # No telemóvel, pelo menos um nome comprido muda de linha (num ponto marcado): o detetor de quebras funciona.
    assert quebras >= 1, quebras
    print(f'PASS: {tabelas // 4} tabelas novas do M5 a 360 e 900 px, nos dois temas, sem transbordar; {listas // 4} listas novas; os nomes do '
          f'portefólio só a mudar de linha nos pontos marcados; {referencias} referências sem se partirem')


if __name__ == '__main__':
    main()
