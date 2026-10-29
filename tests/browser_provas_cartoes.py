"""29/10/2026: Provas em cartões no navegador (Prova 639, 1.ª fase, 2026, versão 2).

Para cada grupo, a 320, 390 e 1366 px: abre a lição, percorre todos os cartões pela ordem da prova respondendo certo
(as respostas vêm dos dados da página, lidos com audit_cards.lesson_cards), confere que cada resposta dá «Certo.»,
que não há erros na página nem pedidos internos falhados nem deslocamento horizontal, que nenhuma peça passa da
largura do cartão (com os desdobráveis abertos: tabelas, linhas da prova, etiquetas), que o fim grava o progresso na
chave do grupo e que a segunda visita abre em «Já feita». Os itens de escolha múltipla do Grupo II mostram as quatro
opções da prova, de (A) a (D), pela ordem e sem negrito. No Grupo III, sem a imagem no sítio, os cartões de observação
levam a ligação para a p. 13 do enunciado, e a figura deixa de ser um botão. Em projeção, os três grupos percorrem-se só
com «Mostrar resposta» e «Seguinte» (também nos cartões «rever»), a faixa diz «Resposta» e nada se grava.
Depois, a secção exame/provas/ (estado de cada grupo neste aparelho, versão da lição, impressão) e as ligações a partir
de /exame/ e do laboratório, sem partir as 27 sessões, o filtro dos anos e a ligação ao laboratório.
O sítio é servido em /pt/ (como no GitHub Pages): uma ligação que saísse de /pt/ dava 404 e falhava o teste.
Corre com: python tests/browser_provas_cartoes.py
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards  # noqa: E402

GRUPOS = {1: 'grupo-i', 2: 'grupo-ii', 3: 'grupo-iii'}
ROMANO = {1: 'I', 2: 'II', 3: 'III'}


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


def dentro_do_cartao(page, onde):
    fora = page.evaluate(PASSA_DO_CARTAO)
    assert not fora, f'peças que passam do cartão: {onde}: {fora}'


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


def percorrer(browser, host, g, width):
    slug = GRUPOS[g]
    cards = lesson_cards(ROOT / 'exame/provas/2026-1f' / slug / 'index.html')
    fazer = [c for c in cards if c['t'] != 'ler']
    ctx, page, erros = nova(browser, width)
    page.goto(f'{host}/exame/provas/2026-1f/{slug}/', wait_until='networkidle')
    assert page.title() == f'Prova 639, 1.ª fase, 2026: Grupo {ROMANO[g]}'
    for k, x in enumerate(cards):
        onde = f'{slug} {width}px cartão {k + 1} ({x["t"]})'
        num = page.locator('[data-c-num]').inner_text()
        assert num.split('/')[0].strip() == str(k + 1), (onde, num)
        if x.get('rot'):
            assert x['rot'] in page.locator('#baralho .rot').text_content(), (onde, x['rot'])
        sem_desvio(page, onde)
        dentro_do_cartao(page, onde)
        if g == 3 and x.get('ver'):
            fig = page.locator('#baralho figure.ver-fig')
            assert fig.get_attribute('role') is None and fig.get_attribute('tabindex') is None, (onde, 'a figura da ligação continua um botão')
            href = page.locator('#baralho figure.ver-fig a.ver-pdf').get_attribute('href')
            assert href.endswith('Portugues.pdf#page=13'), (onde, href)
            assert 'p. 13' in page.locator('#baralho figure.ver-fig a.ver-pdf').inner_text()
        responder(page, k, x, onde)
    page.locator('#baralho .cartao.fim').wait_for()
    sem_desvio(page, f'{slug} {width}px fim')
    st = page.evaluate(f'JSON.parse(localStorage.getItem("prova-2026-1f-g{g}"))')
    assert st['lida'] is True and st['certas'] == len(fazer) and st['melhor'] == len(fazer), st
    assert page.evaluate('localStorage.getItem("epi-ultima")') is None
    acoes = page.evaluate('[...document.querySelectorAll("[data-c-acoes] a,[data-c-acoes] button")].map(a=>a.textContent.trim()+"|"+(a.getAttribute("href")||""))')
    if g < 3:
        assert any(a.startswith(f'Grupo {ROMANO[g + 1]}|../{GRUPOS[g + 1]}/') for a in acoes), acoes
    assert any(a.startswith('Provas em cartões|../../#prova-2026-1f') or a.startswith('Voltar às provas') for a in acoes), acoes
    fim = page.locator('#baralho').text_content()
    assert 'Onde se estuda nos módulos' in fim and 'Na preparação de exame' in fim, fim[-400:]
    if g in (1, 2):
        marcas = page.evaluate('(document.querySelector("[data-leste]")||{}).textContent||""')
        assert 'O texto com as tuas marcas' in marcas, marcas
    # menu: migalhas, fonte e ligações
    page.locator('[data-c-menu]').click()
    menu = page.locator('[data-c-painel]')
    menu.wait_for(state='visible')
    texto = menu.text_content()
    for marca in ('Provas em cartões', f'Estás em: Grupo {ROMANO[g]}', 'IAVE', 'EduQA', 'versão 2', 'Aprendes:'):
        assert marca in texto, (slug, marca)
    page.locator('[data-c-fecha-menu]').click()
    # segunda visita: «Já feita»
    page.reload(wait_until='networkidle')
    assert 'Já feita' in page.locator('#baralho .rot').text_content()
    assert page.locator('#baralho .grande').inner_text().strip() == f'{len(fazer)} de {len(fazer)}'
    assert not erros, erros
    ctx.close()
    print(f'PASS {slug} a {width} px: {len(cards)} cartões, {len(fazer)} respondidos certo, progresso e «Já feita», sem erros nem deslocamento', flush=True)


def projecao(browser, host, g):
    """Projetado, só com o teclado: R mostra a resposta e → avança, em todos os cartões (também «item» e «rever»)."""
    slug = GRUPOS[g]
    cards = lesson_cards(ROOT / 'exame/provas/2026-1f' / slug / 'index.html')
    ctx, page, erros = nova(browser, 1366)
    page.goto(f'{host}/exame/provas/2026-1f/{slug}/?projetar=1', wait_until='networkidle')
    externos = 0
    for k, x in enumerate(cards):
        onde = f'projeção {slug} cartão {k + 1} ({x["t"]})'
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
    assert page.evaluate(f'localStorage.getItem("prova-2026-1f-g{g}")') is None
    assert not erros, erros
    ctx.close()
    print(f'PASS projeção do Grupo {ROMANO[g]}: {len(cards)} cartões só com R e →, «Resposta» em todos ({externos} «item» ou «rever»), nada gravado', flush=True)


def seccao(browser, host):
    for width in (320, 390, 1366):
        ctx, page, erros = nova(browser, width)
        page.add_init_script('localStorage.setItem("prova-2026-1f-g1",JSON.stringify({versao:"2026-10-29",lida:true,melhor:54,totalMelhor:54,total:54}));'
                             'localStorage.setItem("prova-2026-1f-g2",JSON.stringify({versao:"2026-10-29",lida:true,melhor:20,totalMelhor:35,total:35}));')
        page.goto(f'{host}/exame/provas/', wait_until='networkidle')
        sem_desvio(page, f'secção {width}px')
        estados = page.evaluate('[...document.querySelectorAll("[data-chave]")].map(a=>a.getAttribute("data-feito")+"|"+a.querySelector("[data-estado]").textContent)')
        assert estados == ['conquistado|Conquistado: melhor resultado 54 de 54', 'feito|Feito: melhor resultado 20 de 35', 'nao|Por fazer'], estados
        hrefs = page.evaluate('[...document.querySelectorAll(".pv-grupo a")].map(a=>a.getAttribute("href"))')
        assert hrefs == ['2026-1f/grupo-i/', '2026-1f/grupo-ii/', '2026-1f/grupo-iii/'], hrefs
        seguir = page.locator('.pv-seguir').text_content()
        for prova in ('2026, 2.ª fase', '2025, 1.ª e 2.ª fases', '2024, 1.ª e 2.ª fases', '2023, 1.ª e 2.ª fases'):
            assert prova in seguir
        page.locator('.pv-grupo a').nth(2).click()
        page.wait_for_url('**/exame/provas/2026-1f/grupo-iii/')
        page.locator('#baralho .cartao').wait_for()
        page.locator('.c-marca').click()
        page.wait_for_url('**/exame/provas/#prova-2026-1f')
        assert not erros, erros
        ctx.close()
    # outra versão da lição gravada neste aparelho: o motor recomeça, a secção diz «Por fazer»
    ctx, page, erros = nova(browser, 390)
    page.add_init_script('localStorage.setItem("prova-2026-1f-g1",JSON.stringify({versao:"2026-01-01",lida:true,melhor:54,totalMelhor:54,total:54}));')
    page.goto(f'{host}/exame/provas/', wait_until='networkidle')
    assert page.locator('[data-chave="prova-2026-1f-g1"] [data-estado]').inner_text() == 'Por fazer'
    nome = page.evaluate('(()=>{const a=document.querySelector(".pv-grupo a");return a.getAttribute("aria-labelledby").split(" ").map(i=>document.getElementById(i).textContent).join(" ")})()')
    assert nome.startswith('Grupo I Baltasar') and nome.endswith('Por fazer'), nome
    # impressão: a secção sai no papel (exame.css esconde main nas páginas das sessões)
    page.emulate_media(media='print')
    assert page.evaluate('getComputedStyle(document.querySelector("main#provas")).display') != 'none'
    assert page.locator('#prova-2026-1f').bounding_box()['height'] > 200
    page.emulate_media(media='screen')
    assert not erros, erros
    ctx.close()
    print('PASS secção Provas em cartões a 320, 390 e 1366 px: três grupos, estado do aparelho e versão, nome acessível, impressão, o que vem a seguir, ida e volta', flush=True)
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
        assert page.locator('#prova-2026-1f').count() == 1
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
    raiz = tempfile.mkdtemp(prefix='provas-pt-')
    os.symlink(ROOT, os.path.join(raiz, 'pt'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=raiz))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}/pt'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for g in GRUPOS:
                for width in (320, 390, 1366):
                    percorrer(browser, host, g, width)
            for g in GRUPOS:
                projecao(browser, host, g)
            seccao(browser, host)
            browser.close()
    finally:
        server.shutdown()
        os.unlink(os.path.join(raiz, 'pt'))
        os.rmdir(raiz)


if __name__ == '__main__':
    main()
