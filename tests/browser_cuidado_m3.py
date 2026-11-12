"""08/11/2026: decisão 152 (cuidado em todas as lições), módulo M3. As tabelas novas e as referências que não se partem, no
navegador, com o CSS e o motor reais, no modelo de tests/browser_cuidado_m1.py e tests/browser_cuidado_m2.py:
* as 9 tabelas novas, a 360 e a 900 px, em tema claro e escuro: nada desliza para o lado e a tabela não sai do seu contentor;
  cada linha está visível e com as células todas; no telemóvel o cabeçalho sai do ecrã (fica para os leitores de ecrã), as células
  empilham e cada uma leva o rótulo da coluna; no ecrã largo o cabeçalho vê-se e as células de cada linha ficam lado a lado;
  nenhuma palavra se parte a meio. As cinco das lições (F05, F09, F13, F15 e a do baralho da F18) montam-se no cartão onde estão;
  a da página «Ler a fundo» da modalidade vê-se no primeiro passo; as dos pesos (índice, guia e mapa) veem-se abrindo a secção, com
  o rótulo à vista, logo antes da tabela, e no ecrã largo a coluna do peso é estreita e a do componente fica com o resto;
* as referências e os números que o achado protege (U+00A0, U+2060), nas páginas e nos cartões onde estão: cada um fica numa só linha
  no ecrã, e, posto numa caixa de largura zero (que parte em todas as oportunidades), continua numa só linha; com espaços normais, a
  mesma caixa parte-o (o detetor funciona).

Uso: python3 tests/browser_cuidado_m3.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com CUIDADO_M3_OUTPUT, guarda aí as capturas
(deviceScaleFactor 1) de três tabelas novas (a das modalidades da F15, a da página «Ler a fundo» e a dos pesos do índice), a 360 e a
900 px."""
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
from test_cuidado_m3 import TABELAS, LUGARES, PAGINA, cartoes  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('CUIDADO_M3_OUTPUT')
CAPTURAS = {'m3/licao-m3-f15/index.html': 'f15-modalidades', 'm3/gram-modalidade/index.html': 'ler-a-fundo-modalidade',
            'm3/index.html': 'indice-pesos'}
N, J = '\xa0', '⁠'
# As tabelas fora das lições: (página, como se chega lá).
FORA = ['m3/gram-modalidade/index.html', 'm3/index.html', 'm3/guia-da-tarefa-m3/index.html', 'm3/mapa-do-modulo-m3/index.html']
# Referências nas páginas (tal como estão no HTML: só se procuram no texto que se vê).
PAGINAS = {
    'm3/index.html': ['1.º' + N + 'ano', '90' + N + 'minutos', '90' + N + 'min', '10' + N + 'min', '20' + N + 'min', '30' + N + '%',
                      'I,' + N + '106', 'VIII,' + N + '96' + N + 'a' + N + '99', 'X,' + N + '145'],
    # 12/11/2026: no guia, a produção passa a 55 minutos (decisão do docente, camada tarefas_faceis_m3_20261112): a mesma referência,
    # com o número novo, continua sem se partir.
    'm3/guia-da-tarefa-m3/index.html': ['1.º' + N + 'ano', '90' + N + 'minutos', '10' + N + 'minutos', '30' + N + '%', '10' + N + 'min',
                                        '55' + N + 'min'],
    'm3/mapa-do-modulo-m3/index.html': ['1.º' + N + 'ano', 'c.' + N + '1524–' + J + '1580', '1497–' + J + '1499', '90' + N + 'minutos',
                                        '30' + N + '%', 'versos' + N + '1' + N + 'e' + N + '2', 'c.' + N + '1524'],
    'm3/portefolio-do-modulo-m3/index.html': ['1.º' + N + 'ano', '90' + N + 'minutos', '0' + N + 'a' + N + '20', '40' + N + '%'],
    'tarefas/m3-u1/index.html': ['90' + N + 'min', '10' + N + 'min', '200' + N + 'a' + N + '240' + N + 'palavras', '80' + N + 'a' + N + '120',
                                 'D.' + N + 'Manuel' + N + 'I', 'I,' + N + '1' + N + 'a' + N + '3', '90' + N + 'minutos', 'século' + N + 'XVI'],
    'tarefas/m3-u2/index.html': ['90' + N + 'min', '10' + N + 'min', '200' + N + 'a' + N + '250' + N + 'palavras', '90' + N + 'a' + N + '140',
                                 # 12/11/2026: no molde «mais fácil de fazer» (camada tarefas_faceis_m3_20261112) sai o exemplo com VIII, 97;
                                 # ficam, presas da mesma maneira, as referências a VIII, 96, a VIII, 96 a 99 e a VIII, 98 ou 99, e as novas
                                 # («55 min», «Texto 1», «Pergunta 2», «canto VIII», «estância 145»).
                                 'I,' + N + '4' + N + 'e' + N + '5', 'X,' + N + '145', 'VIII,' + N + '96', 'VIII,' + N + '96' + N + 'a' + N + '99',
                                 'VIII,' + N + '98' + N + 'ou' + N + '99', 'IV,' + N + '95' + N + 'a' + N + '104', '55' + N + 'min', 'Texto' + N + '1',
                                 'Pergunta' + N + '2', 'Canto' + N + 'VIII', 'estância' + N + '145'],
    'tarefas/m3-u1/grelha/index.html': ['1' + N + 'a' + N + '3', '1' + N + 'a' + N + '2', '1' + N + 'a' + N + '5',
                                        '200' + N + 'a' + N + '240' + N + 'palavras', 'I,' + N + '106'],
    'tarefas/m3-u2/grelha/index.html': ['1' + N + 'a' + N + '3', '1' + N + 'a' + N + '2', 'IX,' + N + '92', 'VIII,' + N + '98'],
    # (nas páginas «Ler a fundo», as migalhas estão no menu, fechado: mede-se o primeiro passo, depois de «Começar», e a capa)
    'm3/camoes-invocacoes/index.html': ['canto' + N + 'I', 'estância' + N + '4', 'canto' + N + 'X', 'estância' + N + '145'],
    'm3/bicho-da-terra/index.html': ['I,' + N + '106', 'VIII,' + N + '98'],
}
# Referências nos cartões (lições, baralho da F18 e exercícios longos): (página, cartão, referências).
CARTOES = [
    ('m3/licao-m3-f02/index.html', 3, ['I,' + N + '1' + N + 'a' + N + '3']),
    ('m3/licao-m3-f03/index.html', 3, ['IV,' + N + '94' + N + 'e' + N + '95']),
    ('m3/licao-m3-f05/index.html', 2, ['1' + N + 'min']),
    ('m3/licao-m3-f05/index.html', 7, ['t.' + N + 'III']),
    ('m3/licao-m3-f10/index.html', 2, ['Canto' + N + 'I,' + N + '4']),
    ('m3/licao-m3-f10/index.html', 0, ['c.' + N + '1520–' + J + '1540', 'canto' + N + 'I']),
    ('m3/licao-m3-f13/index.html', 2, ['I,' + N + '106']),
    ('m3/licao-m3-f13/index.html', 12, ['Canto' + N + 'VIII,' + N + '97']),
    ('m3/licao-m3-f15/index.html', 0, ['c.' + N + '1560']),
    ('m3/licao-m3-f16/index.html', 1, ['30' + N + 'segundos']),
    ('m3/licao-m3-f17/index.html', 2, ['2' + N + 'min']),
    ('assets/pt-lessons/m3-f18.js', 1, ['I,' + N + '19–' + J + '20', 'I,' + N + '19']),
    ('assets/pt-lessons/m3-f18.js', 3, ['II,' + N + '109–' + J + '110', 'III,' + N + '3–' + J + '5', 'IV,' + N + '84–' + J + '93']),
    ('assets/pt-lessons/m3-f18.js', 7, ['III,' + N + '1–' + J + '5']),
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


def esperado(rel):
    return next((leg, cab, linhas) for r, i, leg, cab, linhas in TABELAS if r == rel)


def mount(page, card):
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-cuidado-m3',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
    }''', card)


def confere(page, tabela, rel, largura, onde):
    legenda, cabecalho, linhas = esperado(rel)
    assert tabela.count() == 1, onde
    tabela.evaluate('t=>{for(let d=t.closest("details");d;d=d.parentElement&&d.parentElement.closest("details"))d.open=true}')
    tabela.scroll_into_view_if_needed()
    assert tabela.locator('thead th[scope="col"]').all_text_contents() == cabecalho, onde
    assert tabela.locator('tbody th[scope="row"]').all_text_contents() == [l[0] for l in linhas], onde
    if legenda:
        # O rótulo dos pesos fica à vista, no parágrafo logo antes da tabela.
        rotulo = tabela.locator('xpath=preceding-sibling::p[1]')
        assert rotulo.inner_text().strip() == legenda + ':', onde
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
    assert not page.evaluate('()=>document.documentElement.scrollWidth>innerWidth+3'), (onde, largura, 'desliza para o lado')
    assert tabela.evaluate('t=>t.getBoundingClientRect().right<=t.parentElement.getBoundingClientRect().right+1'), (onde, largura)
    assert tabela.evaluate(MEIO_DA_PALAVRA) == [], (onde, largura, tabela.evaluate(MEIO_DA_PALAVRA))
    cab = tabela.locator('thead')
    if largura <= 620:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'absolute', onde
    else:
        assert cab.evaluate('e=>getComputedStyle(e).position') == 'static', onde
        assert cab.is_visible(), onde
        if cabecalho == ['Componente', 'Peso']:
            # A coluna do peso só leva um número: é estreita (5,5 rem) e a do componente fica com o resto.
            peso, comp = (tabela.locator('thead th').nth(i).evaluate('e=>e.getBoundingClientRect().width') for i in (1, 0))
            rem = page.evaluate('()=>parseFloat(getComputedStyle(document.documentElement).fontSize)')
            assert abs(peso - 5.5 * rem) < 2 and comp > 2 * peso, (onde, peso, comp, rem)
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
                    # As tabelas das lições, cada uma no seu cartão (a da F18 no baralho, montada na página da lição).
                    for (rel, k), (indice, _) in sorted(LUGARES.items()):
                        card = cartoes((ROOT / rel).read_text('utf-8'))[indice]
                        page.goto(host + '/' + PAGINA.get(rel, rel).replace('index.html', ''), wait_until='networkidle')
                        mount(page, card)
                        tabela = page.locator('#baralho .cartao .ler .apoio-tabela')
                        onde = f'{rel} cartão {indice}'
                        confere(page, tabela, rel, largura, onde)
                        tabelas += 1
                        if esquema == 'light' and rel in CAPTURAS:
                            captura(page.locator('#baralho .cartao').first, CAPTURAS[rel], largura)
                        print('PASS tabela:', rel, indice, largura, esquema, flush=True)
                    # As tabelas fora das lições.
                    for rel in FORA:
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        if rel == 'm3/gram-modalidade/index.html':
                            page.get_by_role('button', name='Começar').click()
                        tabela = page.locator('.apoio-tabela')
                        tabela.wait_for(state='attached')
                        confere(page, tabela, rel, largura, rel)
                        tabelas += 1
                        if rel == 'm3/gram-modalidade/index.html':
                            # Dentro do div.nota: a letra pequena e o filete da nota ficam.
                            assert tabela.evaluate('t=>t.parentElement.classList.contains("nota")'), rel
                        if esquema == 'light' and rel in CAPTURAS:
                            # O contentor da tabela: no índice, a regra «Como se cumpre uma unidade» (com o rótulo e o parágrafo a
                            # seguir); na página «Ler a fundo», a nota.
                            alvo = tabela.locator('xpath=..')
                            captura(alvo, CAPTURAS[rel], largura)
                        print('PASS fora das lições:', rel, largura, esquema, flush=True)
                    # As referências e os números, nas páginas (com os «details» abertos) e nos cartões.
                    for rel, agulhas in PAGINAS.items():
                        page.goto(host + '/' + rel.replace('index.html', ''), wait_until='networkidle')
                        page.evaluate('()=>document.querySelectorAll("details:not(.info-i)").forEach(d=>d.open=true)')
                        if rel.startswith('tarefas/m3-u') and rel.count('/') == 2:
                            # A tarefa mostra um cartão de cada vez (task-reader.js); aqui mostram-se todos, para medir o texto.
                            page.evaluate('()=>document.querySelectorAll("[id^=task-card-][hidden]").forEach(e=>e.hidden=false)')
                        if rel == 'm3/camoes-invocacoes/index.html':
                            page.get_by_role('button', name='Começar').click()
                        if rel == 'm3/guia-da-tarefa-m3/index.html':
                            # Os blocos de hoje («Aquecer, 10 min»…) estão na rota da tarefa, que se abre quando se escolhe uma.
                            page.locator('button[data-n="1"]').first.click()
                            assert page.locator('#rota').is_visible()
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
    print(f'PASS: {tabelas // 4} tabelas novas do M3 a 360 e 900 px, nos dois temas, sem transbordar; {referencias} referências sem se partirem')


if __name__ == '__main__':
    main()
