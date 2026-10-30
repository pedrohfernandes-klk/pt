"""Provas em cartões no navegador: piloto de 29/10/2026 (Prova 639, 1.ª fase, 2026, versão 2); um caso por prova desde
30/10/2026 (cada fixture tests/fixtures/prova-639-AAAA-Nf-vN.json, como em tests/provas_casos.py).

Para cada prova e cada grupo, a 320, 390 e 1366 px: abre a lição, percorre todos os cartões pela ordem da prova
respondendo certo (as respostas vêm dos dados da página, lidos com audit_cards.lesson_cards), confere que cada resposta dá
«Certo.», que não há erros na página nem pedidos internos falhados nem deslocamento horizontal, que nenhuma peça passa da
largura do cartão (com os desdobráveis abertos: tabelas, linhas da prova, etiquetas), que o fim grava o progresso na
chave do grupo (prova-AAAA-Nf-gN) e que a segunda visita abre em «Já feita». Os itens de escolha múltipla mostram as
quatro opções da prova, de (A) a (D), pela ordem e sem negrito. Com uma imagem com direitos que não se reproduz (o Grupo III
de 2026-1f), os cartões de observação levam a ligação para a página do enunciado, e a figura deixa de ser um botão.
Prosa da prova em texto corrido (pedido do docente de 30/10/2026): em cada cartão com prosa da prova, cada linha impressa
(span.ln) segue na mesma linha do ecrã que a anterior, salvo no início de parágrafo ou quando a primeira palavra já não
cabia; nenhuma linha começa numa linha nova do ecrã com espaço livre no fim da anterior (o texto «partido»), e o número da
linha (data-l, ou data-n nos excertos repetidos) está à vista antes dela. Nos excertos que saltam linhas, a linha que não
segue a anterior («salto») começa numa linha nova do ecrã, em vez de ficar colada. As estrofes ficam em verso: um verso por
linha.
Em projeção, cada grupo percorre-se só com «Mostrar resposta» e «Seguinte» (também nos cartões «rever»), a faixa diz
«Resposta» e nada se grava.
Depois, a secção exame/provas/ (um bloco por prova, a mais recente primeiro; estado de cada grupo neste aparelho, versão da
lição, impressão) e as ligações a partir de /exame/ e do laboratório, sem partir as 27 sessões, o filtro dos anos e a
ligação ao laboratório.
O sítio é servido em /pt/ (como no GitHub Pages): uma ligação que saísse de /pt/ dava 404 e falhava o teste.
Corre com: python tests/browser_provas_cartoes.py [AAAA-Nf ...] (sem pastas, todas as provas).
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import re
import sys
import tempfile
import threading

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provas_casos import DADOS, PROVAS, ROMANOS, ROOT  # noqa: E402


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def nova(browser, width, **kw):
    ctx = browser.new_context(viewport={'width': width, 'height': 860}, reduced_motion='reduce', **kw)
    page = ctx.new_page()
    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
    erros = []
    page.on('pageerror', lambda e: erros.append('pageerror: ' + str(e)))
    page.on('console', lambda m: erros.append('console: ' + m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    page.on('requestfailed', lambda r: erros.append('pedido: ' + r.url) if r.url.startswith('http://127.0.0.1') else None)
    page.on('response', lambda r: erros.append(f'{r.status}: {r.url}') if r.url.startswith('http://127.0.0.1') and r.status >= 400 else None)
    return ctx, page, erros


def sem_desvio(page, onde):
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), f'deslocamento horizontal: {onde}'


PASSA_DO_CARTAO = """() => {
  const c = document.querySelector('#baralho .cartao'); if (!c) return [];
  c.querySelectorAll('details').forEach(d => { if (!d.open) { d.open = true; d.dataset.abertoTeste = '1'; } });
  const lim = c.getBoundingClientRect().right + 1, fora = [];
  c.querySelectorAll('table, .prova-l, .ln, p, li, button, img, figure, .ops, .pares, .classes, select').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width > 0 && r.right > lim) fora.push(e.tagName + '.' + e.className + ' +' + Math.round(r.right - lim) + 'px');
  });
  c.querySelectorAll('details[data-aberto-teste]').forEach(d => { d.open = false; delete d.dataset.abertoTeste; });
  return fora.slice(0, 5);
}"""

# Prosa em texto corrido: uma linha impressa que não começa parágrafo só pode começar numa linha nova do ecrã se a primeira
# palavra (com o número pequeno antes dela, folga de 3em) não cabia no espaço que sobrava no fim da linha anterior.
PROSA = """() => {
  const c = document.querySelector('#baralho .cartao'); if (!c) return {linhas: 0, versos: 0, partidas: []};
  c.querySelectorAll('details').forEach(d => { if (!d.open) { d.open = true; d.dataset.abertoProsa = '1'; } });
  const partidas = []; let linhas = 0, versos = 0;
  const primeira = ln => {
    const w = document.createTreeWalker(ln, NodeFilter.SHOW_TEXT, {acceptNode: t => t.parentElement.closest('.n') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT});
    for (let t = w.nextNode(); t; t = w.nextNode()) {
      const m = /\\S+/.exec(t.data); if (!m) continue;
      const r = document.createRange(); r.setStart(t, m.index); r.setEnd(t, m.index + m[0].length);
      return r.getBoundingClientRect().width;
    }
    return 0;
  };
  c.querySelectorAll('.prova-l').forEach(bl => {
    const lns = [...bl.querySelectorAll(':scope > .ln')];
    if (bl.classList.contains('estrofe')) {
      lns.forEach((ln, i) => { versos++; if (i && ln.getClientRects()[0].top < lns[i - 1].getClientRects()[0].bottom - 2) partidas.push('verso ' + (ln.dataset.l || '?') + ' na linha do anterior'); });
      return;
    }
    const dir = bl.getBoundingClientRect().right;
    lns.forEach((ln, i) => {
      linhas++;
      const nome = 'linha ' + (ln.dataset.l || '(sem número) ' + ln.textContent.slice(0, 30));
      const cs = getComputedStyle(ln);
      if (cs.display !== 'inline') { partidas.push(nome + ': display ' + cs.display); return; }
      const num = ln.dataset.l || ln.dataset.n;
      if (!num || !getComputedStyle(ln, '::before').content.includes(num)) partidas.push(nome + ': sem o número à vista');
      if (i === 0) return;
      // o «\\A» do início de parágrafo ou de salto deixa um pedaço vazio no fim da linha anterior: conta o primeiro com largura
      const a = lns[i - 1].getClientRects(), b = [...ln.getClientRects()].filter(r => r.width > 5);
      if (!a.length || !b.length) return;
      const fim = a[a.length - 1], ini = b[0], nova = ini.top >= fim.bottom - 2;
      if (ln.classList.contains('salto') && !nova) partidas.push(nome + ': não segue a anterior, mas está colada a ela');
      if (ln.classList.contains('par') || ln.classList.contains('salto') || !nova) return;
      const sobra = dir - fim.right, precisa = primeira(ln) + 3 * parseFloat(cs.fontSize);
      if (sobra > precisa) partidas.push(nome + ': começa numa linha nova com ' + Math.round(sobra) + ' px livres no fim da anterior');
    });
  });
  c.querySelectorAll('details[data-aberto-prosa]').forEach(d => { d.open = false; delete d.dataset.abertoProsa; });
  return {linhas, versos, partidas: partidas.slice(0, 5)};
}"""


def dentro_do_cartao(page, onde):
    fora = page.evaluate(PASSA_DO_CARTAO)
    assert not fora, f'peças que passam do cartão: {onde}: {fora}'


def prosa_corrida(page, onde):
    r = page.evaluate(PROSA)
    assert not r['partidas'], f'prosa partida: {onde}: {r["partidas"]}'
    return r


def seguinte_na_faixa(page, onde):
    folha = page.locator('[data-c-folha]')
    folha.wait_for(state='visible')
    titulo = folha.text_content()
    assert re.match(r'^\W*Certo\.', titulo.strip()), f'{onde}: a resposta certa não deu «Certo.»: {titulo[:120]!r}'
    page.locator('[data-c-folha] [data-seguinte]').click()


def responder(page, k, x, onde):
    t = x['t']
    if t == 'ler':
        page.locator('[data-c-acoes] [data-seguinte]').click()
        return
    if t in ('escolha', 'item'):
        if t == 'item':
            letras = page.evaluate('[...document.querySelectorAll("#baralho .ops .op")].map(b=>b.dataset.j+":"+b.querySelector(".letra").textContent)')
            assert letras == ['0:(A)', '1:(B)', '2:(C)', '3:(D)'], (onde, letras)
            peso = page.evaluate('getComputedStyle(document.querySelector("#baralho .ops-item .op .tx")).fontWeight')
            assert peso in ('400', 'normal'), (onde, 'opções do item a negrito', peso)
            assert page.locator('#baralho .cartao.oficial').count() == 1, (onde, 'cartão oficial sem a classe')
            assert page.locator('#baralho .cartao.oficial .cit').count() == 0 or page.evaluate(
                'getComputedStyle(document.querySelector("#baralho .cartao.oficial .cit")).fontStyle') == 'normal'
        page.locator(f'#baralho .ops .op[data-j="{x["c"]}"]').click()
    elif t == 'vf':
        page.locator(f'#baralho .ops .op[data-j="{1 if x["v"] else 0}"]').click()
    elif t == 'sublinhar':
        for j in x['certas']:
            page.locator(f'#baralho .pal[data-j="{j}"]').click()
        page.locator('[data-c-acoes] [data-confirmar]').click()
    elif t == 'completar':
        for kk, lac in enumerate(x['lacunas']):
            page.locator(f'#baralho select[data-k="{kk}"]').select_option(value=str(lac['c']))
    elif t in ('ordenar', 'versos'):
        for j in range(len(x.get('passos') or x.get('linhas'))):
            page.locator(f'#baralho .soltos .op[data-j="{j}"]').click()
    elif t == 'emparelhar':
        direitas = []
        for _, d in x['pares']:
            if d not in direitas:
                direitas.append(d)
        classes = page.locator('#baralho .classes').count() > 0
        for j, (_, d) in enumerate(x['pares']):
            page.locator(f'#baralho [data-e="{j}"]').click()
            alvo = f'#baralho .regiao .cab[data-d="{direitas.index(d)}"]' if classes else f'#baralho [data-d="{direitas.index(d)}"]'
            page.locator(alvo).click()
    elif t == 'rever':
        page.locator(f'#baralho [data-rever-op="{x["c"]}"]').click()
        page.locator('[data-c-acoes] [data-rever-confirmar]').click()
    else:
        raise AssertionError(f'{onde}: tipo sem percurso no teste: {t}')
    seguinte_na_faixa(page, onde)


def percorrer(browser, host, P, g, width):
    slug = P.grupos[g]
    cards = P.cartoes(g)
    fazer = [c for c in cards if c['t'] != 'ler']
    img = P.imagem()
    liga_imagem = img and img['grupo'] == g and not img.get('reproduzir')
    ctx, page, erros = nova(browser, width)
    page.goto(f'{host}/exame/provas/{P.pasta}/{slug}/', wait_until='networkidle')
    assert page.title() == f'{P.nome}: Grupo {ROMANOS[g - 1]}', page.title()
    linhas = versos = 0
    for k, x in enumerate(cards):
        onde = f'{P.pasta} {slug} {width}px cartão {k + 1} ({x["t"]})'
        num = page.locator('[data-c-num]').inner_text()
        assert num.split('/')[0].strip() == str(k + 1), (onde, num)
        if x.get('rot'):
            assert x['rot'] in page.locator('#baralho .rot').text_content(), (onde, x['rot'])
        sem_desvio(page, onde)
        dentro_do_cartao(page, onde)
        if x['t'] == 'ler' and 'prova-l' in x.get('html', ''):
            r = prosa_corrida(page, onde)
            linhas, versos = linhas + r['linhas'], versos + r['versos']
        if liga_imagem and x.get('ver'):
            fig = page.locator('#baralho figure.ver-fig')
            assert fig.get_attribute('role') is None and fig.get_attribute('tabindex') is None, (onde, 'a figura da ligação continua um botão')
            href = page.locator('#baralho figure.ver-fig a.ver-pdf').get_attribute('href')
            assert href == f'{P.url_enunciado}#page={img["pagina_pdf"]}', (onde, href)
            assert f'p. {img["pagina_pdf"]}' in page.locator('#baralho figure.ver-fig a.ver-pdf').inner_text()
        responder(page, k, x, onde)
    page.locator('#baralho .cartao.fim').wait_for()
    sem_desvio(page, f'{P.pasta} {slug} {width}px fim')
    st = page.evaluate(f'JSON.parse(localStorage.getItem("{P.chave(g)}"))')
    assert st['lida'] is True and st['certas'] == len(fazer) and st['melhor'] == len(fazer), st
    assert st['versao'] == P.versao_licao(g), st
    assert page.evaluate('localStorage.getItem("epi-ultima")') is None
    acoes = page.evaluate('[...document.querySelectorAll("[data-c-acoes] a,[data-c-acoes] button")].map(a=>a.textContent.trim()+"|"+(a.getAttribute("href")||""))')
    if g < len(P.grupos):
        assert any(a.startswith(f'Grupo {ROMANOS[g]}|../{P.grupos[g + 1]}/') for a in acoes), acoes
    assert any(a.startswith(f'Provas em cartões|../../#prova-{P.pasta}') or a.startswith('Voltar às provas') for a in acoes), acoes
    fim = page.locator('#baralho').text_content()
    assert 'Onde se estuda nos módulos' in fim and 'Na preparação de exame' in fim, fim[-400:]
    if any(c['t'] == 'ler' and 'data-l=' in c.get('html', '') for c in cards):
        marcas = page.evaluate('(document.querySelector("[data-leste]")||{}).textContent||""')
        assert 'O texto com as tuas marcas' in marcas, marcas
    # menu: migalhas, fonte e ligações
    page.locator('[data-c-menu]').click()
    menu = page.locator('[data-c-painel]')
    menu.wait_for(state='visible')
    texto = menu.text_content()
    marcas_menu = ['Provas em cartões', f'Estás em: Grupo {ROMANOS[g - 1]}', 'IAVE', f'versão {P.versao}', 'Aprendes:']
    if P.autor_nao_iave():
        marcas_menu.append(P.autor_nao_iave().split(',')[0])
    for marca in marcas_menu:
        assert marca in texto, (slug, marca)
    page.locator('[data-c-fecha-menu]').click()
    # segunda visita: «Já feita»
    page.reload(wait_until='networkidle')
    assert 'Já feita' in page.locator('#baralho .rot').text_content()
    assert page.locator('#baralho .grande').inner_text().strip() == f'{len(fazer)} de {len(fazer)}'
    assert not erros, erros
    ctx.close()
    print(f'PASS {P.pasta} {slug} a {width} px: {len(cards)} cartões, {len(fazer)} respondidos certo, progresso e «Já feita», '
          f'prosa corrida ({linhas} linhas e {versos} versos da prova vistos), sem erros nem deslocamento', flush=True)


def projecao(browser, host, P, g):
    """Projetado, só com o teclado: R mostra a resposta e → avança, em todos os cartões (também «item» e «rever»)."""
    slug = P.grupos[g]
    cards = P.cartoes(g)
    ctx, page, erros = nova(browser, 1366)
    page.goto(f'{host}/exame/provas/{P.pasta}/{slug}/?projetar=1', wait_until='networkidle')
    externos = 0
    for k, x in enumerate(cards):
        onde = f'projeção {P.pasta} {slug} cartão {k + 1} ({x["t"]})'
        if x['t'] != 'ler':
            assert page.locator('[data-c-acoes] [data-mostrar]').count() == 1, (onde, 'sem «Mostrar resposta»')
            page.keyboard.press('r')
            folha = page.locator('[data-c-folha]')
            folha.wait_for(state='visible')
            titulo = page.locator('[data-c-folha] .c-veredito').inner_text()
            assert 'Resposta' in titulo and 'Certo' not in titulo and 'pontos' not in titulo, (onde, titulo)
            externos += x['t'] in ('item', 'rever')
        page.keyboard.press('ArrowRight')
    page.locator('#baralho .cartao.fim').wait_for()
    assert page.evaluate(f'localStorage.getItem("{P.chave(g)}")') is None
    assert not erros, erros
    ctx.close()
    print(f'PASS projeção {P.pasta} Grupo {ROMANOS[g - 1]}: {len(cards)} cartões só com R e →, «Resposta» em todos ({externos} «item» ou «rever»), nada gravado', flush=True)


def rotulos_a_seguir():
    sec = json.loads((DADOS / 'seccao.json').read_text('utf-8'))
    feitas = {(P.ano, P.fase) for P in PROVAS}
    faltam = {}
    for ano, fase in sec['previstas']:
        if (ano, fase) not in feitas:
            faltam.setdefault(ano, []).append(fase)
    out = []
    for ano in sorted(faltam, reverse=True):
        fs = sorted(faltam[ano])
        out.append(f'{ano}, {fs[0]}.ª fase' if len(fs) == 1 else f'{ano}, ' + ', '.join(f'{f}.ª' for f in fs[:-1]) + f' e {fs[-1]}.ª fases')
    return out


def seccao(browser, host):
    P0 = PROVAS[0]  # a mais recente: o primeiro bloco
    f1 = len([c for c in P0.cartoes(1) if c['t'] != 'ler'])
    f2 = len([c for c in P0.cartoes(2) if c['t'] != 'ler'])
    m2 = f2 // 2  # «Feito», abaixo dos 80 % do «Conquistado»
    estado = (f'localStorage.setItem("{P0.chave(1)}",JSON.stringify({{versao:"{P0.versao_licao(1)}",lida:true,melhor:{f1},totalMelhor:{f1},total:{f1}}}));'
              f'localStorage.setItem("{P0.chave(2)}",JSON.stringify({{versao:"{P0.versao_licao(2)}",lida:true,melhor:{m2},totalMelhor:{f2},total:{f2}}}));')
    esperados = [f'conquistado|Conquistado: melhor resultado {f1} de {f1}', f'feito|Feito: melhor resultado {m2} de {f2}', 'nao|Por fazer']
    esperados += ['nao|Por fazer'] * (sum(len(P.grupos) for P in PROVAS) - 3)
    hrefs_esperados = [f'{P.pasta}/{slug}/' for P in PROVAS for slug in P.grupos.values()]
    for width in (320, 390, 1366):
        ctx, page, erros = nova(browser, width)
        page.add_init_script(estado)
        page.goto(f'{host}/exame/provas/', wait_until='networkidle')
        sem_desvio(page, f'secção {width}px')
        estados = page.evaluate('[...document.querySelectorAll("[data-chave]")].map(a=>a.getAttribute("data-feito")+"|"+a.querySelector("[data-estado]").textContent)')
        assert estados == esperados, estados
        hrefs = page.evaluate('[...document.querySelectorAll(".pv-grupo a")].map(a=>a.getAttribute("href"))')
        assert hrefs == hrefs_esperados, hrefs
        blocos = page.evaluate('[...document.querySelectorAll("section.pv-prova")].map(s=>s.id)')
        assert blocos == [f'prova-{P.pasta}' for P in PROVAS], blocos
        seguir = page.locator('.pv-seguir').text_content()
        for rot in rotulos_a_seguir():
            assert rot in seguir, rot
        page.locator('.pv-grupo a').nth(2).click()
        page.wait_for_url(f'**/exame/provas/{P0.pasta}/{P0.grupos[3]}/')
        page.locator('#baralho .cartao').wait_for()
        page.locator('.c-marca').click()
        page.wait_for_url(f'**/exame/provas/#prova-{P0.pasta}')
        assert not erros, erros
        ctx.close()
    # outra versão da lição gravada neste aparelho: o motor recomeça, a secção diz «Por fazer»
    ctx, page, erros = nova(browser, 390)
    page.add_init_script(f'localStorage.setItem("{P0.chave(1)}",JSON.stringify({{versao:"2026-01-01",lida:true,melhor:{f1},totalMelhor:{f1},total:{f1}}}));')
    page.goto(f'{host}/exame/provas/', wait_until='networkidle')
    assert page.locator(f'[data-chave="{P0.chave(1)}"] [data-estado]').inner_text() == 'Por fazer'
    # nome acessível de cada ligação: «Grupo n, título, estado»
    nomes = page.evaluate('[...document.querySelectorAll(".pv-grupo a")].map(a=>a.getAttribute("aria-labelledby").split(" ").map(i=>document.getElementById(i).textContent).join(" "))')
    titulos = [json.loads((DADOS / P.pasta / f'{slug}.json').read_text('utf-8'))['titulo'] for P in PROVAS for slug in P.grupos.values()]
    grupos = [ROMANOS[g - 1] for P in PROVAS for g in P.grupos]
    for nome, titulo, rom in zip(nomes, titulos, grupos):
        assert nome == f'Grupo {rom} {titulo} Por fazer', nome
    # impressão: a secção sai no papel (exame.css esconde main nas páginas das sessões)
    page.emulate_media(media='print')
    assert page.evaluate('getComputedStyle(document.querySelector("main#provas")).display') != 'none'
    for P in PROVAS:
        assert page.locator(f'#prova-{P.pasta}').bounding_box()['height'] > 200
    page.emulate_media(media='screen')
    assert not erros, erros
    ctx.close()
    print(f'PASS secção Provas em cartões a 320, 390 e 1366 px: {len(PROVAS)} prova(s), a mais recente primeiro, estado do aparelho e versão, '
          'nome acessível, impressão, o que vem a seguir, ida e volta', flush=True)
    for width in (320, 1366):
        ctx, page, erros = nova(browser, width)
        page.goto(f'{host}/exame/', wait_until='networkidle')
        page.locator('.session-card').first.wait_for()
        assert page.locator('.session-card').count() == 27
        assert page.locator('a[href="laboratorio/"]').count() == 1
        assert page.locator('select').first.get_attribute('id') == 'group'
        assert page.locator('.site-head a[href="provas/"]').count() == 1
        assert page.locator('#app .provas-porta a[href="provas/"]').count() == 1
        sem_desvio(page, f'/exame/ {width}px')
        page.locator('#app .provas-porta a[href="provas/"]').click()
        page.wait_for_url('**/exame/provas/')
        for P in PROVAS:
            assert page.locator(f'#prova-{P.pasta}').count() == 1
        page.goto(f'{host}/exame/#s19/aquecer', wait_until='networkidle')
        page.locator('[data-action="another"]').wait_for()
        page.goto(f'{host}/exame/laboratorio/', wait_until='networkidle')
        assert page.locator('.site-head a[href="../provas/"]').count() == 1
        sem_desvio(page, f'laboratório {width}px')
        page.locator('.site-head a[href="../provas/"]').click()
        page.wait_for_url('**/exame/provas/')
        assert not erros, erros
        ctx.close()
    print('PASS /exame/ e laboratório: ligação às provas no cabeçalho e no catálogo; 27 sessões, filtro e laboratório como antes; sem deslocamento a 320 e 1366 px', flush=True)


def main():
    pedidas = sys.argv[1:]
    provas = [P for P in PROVAS if not pedidas or P.pasta in pedidas]
    assert provas, f'sem provas para {pedidas}'
    raiz = tempfile.mkdtemp(prefix='provas-pt-')
    os.symlink(ROOT, os.path.join(raiz, 'pt'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=raiz))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}/pt'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for P in provas:
                for g in P.grupos:
                    for width in (320, 390, 1366):
                        percorrer(browser, host, P, g, width)
                for g in P.grupos:
                    projecao(browser, host, P, g)
            seccao(browser, host)
            browser.close()
    finally:
        server.shutdown()
        os.unlink(os.path.join(raiz, 'pt'))
        os.rmdir(raiz)


if __name__ == '__main__':
    main()
