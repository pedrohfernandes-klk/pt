"""Opções denunciadoras (pedido do docente de 29/10/2026): as perguntas mudadas, respondidas no navegador a 390 px.

30/10/2026: para cada cartão de lição cujas opções a camada tests/fixtures/opcoes-denunciadoras-edits-20261030.json mudou
(escolha, completar e rever), monta-se o motor da própria página (jogo.js, numa casca sobreposta) só com esse cartão, como
faz tests/browser_jogabilidade.py; a lição M3-F18 lê os cartões de assets/pt-lessons/m3-f18.js. Confere-se que as opções
novas aparecem, que a certa (o mesmo índice de antes) continua a ser aceite e mostra o retorno geral, que uma errada mostra
o seu retorno e que nada passa da largura do ecrã.
O sítio é servido em /pt/ (como no GitHub Pages).
"""
from functools import partial
from html import unescape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import re
import sys
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from auditoria_20261028 import undo_opcoes  # noqa: E402

MANIFESTO = ROOT / 'tests/fixtures/opcoes-denunciadoras-edits-20261030.json'
# A lição M3-F18 lê os cartões de assets/pt-lessons/m3-f18.js (troca irmã da do arquivo do índice).
EXTRA = {'m3/licao-m3-f18/index.html': ('assets/pt-lessons/m3-f18.js', 'Que revisão melhora a análise')}


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def cartoes(texto):
    i = texto.find('CARTOES=')
    return json.JSONDecoder().raw_decode(texto[i + len('CARTOES='):].lstrip())[0] if i >= 0 else None


def mudados():
    """(página, índice do cartão, cartão) de cada cartão de lição que a camada mudou."""
    files = json.loads(MANIFESTO.read_text('utf-8'))['files']
    out = []
    for rel in sorted(files):
        if '/licao-' not in rel or not rel.endswith('index.html'):
            continue
        texto = (ROOT / rel).read_text('utf-8')
        antes, depois = cartoes(undo_opcoes(rel, texto)), cartoes(texto)
        if not depois:
            continue
        for k, (a, b) in enumerate(zip(antes, depois)):
            if a != b and b.get('t') in ('escolha', 'completar', 'rever'):
                out.append((rel, k, b))
    return out


def visivel(s):
    s = unescape(re.sub(r'<[^>]+>', '', str(s or ''))).replace('**', '').replace('_', '')
    return re.sub(r'\s+', ' ', s).strip()


def montar(page, x):
    """Monta o motor da página (jogo.js) só com este cartão, numa casca sobreposta, como tests/browser_jogabilidade.py."""
    page.evaluate('''(x) => {
        document.querySelectorAll('.casca').forEach(n => n.remove());
        window.api = EPIJogo.montar({itens: [x], chave: 'qa-opcoes-' + Math.random(), variar: false});
        document.querySelector('.casca.sobreposta .jogo-alvo').id = 'baralho';
    }''', x)


def responder(page, x, certo):
    """Responde ao cartão; devolve o texto que o retorno tem de mostrar."""
    t = x['t']
    if t == 'escolha':
        j = x['c'] if certo else next(i for i in range(len(x['o'])) if i != x['c'])
        textos = [visivel(s) for s in page.locator('#baralho .ops button.op').all_inner_texts()]
        opcoes = [visivel(o) for o in x['o']]
        # com 4 ou mais opções, o motor mostra a certa e duas erradas ao acaso
        assert opcoes[x['c']] in textos and set(textos) <= set(opcoes), (opcoes, textos)
        assert len(x['o']) > 3 or set(textos) == set(opcoes), (opcoes, textos)
        if page.locator(f'#baralho .ops [data-j="{j}"]').count() == 0:  # com 4 ou mais opções, a errada pode não sair
            j = int(page.locator('#baralho .ops [data-j]').evaluate_all(
                f'(bs) => bs.map(b => +b.dataset.j).filter(v => v !== {x["c"]})[0]'))
        page.locator(f'#baralho .ops [data-j="{j}"]').click()
        fe = None if certo else (x.get('fe') or [None] * len(x['o']))[j] if isinstance(x.get('fe'), list) else x.get('fe')
        return x['f'], (None if certo else fe)
    if t == 'rever':
        j = x['c'] if certo else next(i for i in range(len(x['o'])) if i != x['c'])
        page.locator(f'#baralho [data-rever-op="{j}"]').click()
        assert visivel(x['o'][j]) in visivel(page.locator('#baralho [data-rever-prev]').inner_text())
        page.locator('.casca [data-rever-confirmar]').click()
        return x['f'], (None if certo else x['fe'][j])
    if t == 'completar':
        for n, lacuna in enumerate(x['lacunas']):
            sel = page.locator('#baralho select').nth(n)
            valores = [int(v) for v in sel.locator('option').evaluate_all('(os) => os.map(o => o.value)') if v != '']
            labels = [visivel(s) for s in sel.locator('option').all_inner_texts()][1:]
            opcoes = [visivel(o) for o in lacuna['o']]
            # com 4 ou mais opções, o motor mostra a certa e duas erradas ao acaso
            assert opcoes[lacuna['c']] in labels and set(labels) <= set(opcoes), (opcoes, labels)
            assert len(opcoes) > 3 or set(labels) == set(opcoes), (opcoes, labels)
            j = lacuna['c'] if (certo or n) else next(v for v in valores if v != lacuna['c'])
            sel.select_option(value=str(j))
        fe = None if certo else x.get('fe') if isinstance(x.get('fe'), str) else None
        return x['f'], fe
    raise AssertionError(t)


def conferir(page, rotulo, esperado, fe):
    painel = page.locator('.casca [data-c-folha]:visible')
    painel.wait_for(timeout=5000)
    texto = visivel(painel.inner_text())
    assert visivel(esperado)[:60] in texto, (rotulo, esperado[:80], texto[:300])
    if fe:
        assert visivel(fe)[:60] in texto, (rotulo, fe[:80], texto[:300])
    largura = page.evaluate('[document.documentElement.scrollWidth, innerWidth]')
    assert largura[0] <= largura[1] + 1, (rotulo, largura)


def main():
    lista = mudados()
    assert len(lista) >= 40, len(lista)
    raiz = tempfile.mkdtemp(prefix='opcoes-pt-')
    os.symlink(ROOT, os.path.join(raiz, 'pt'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=raiz))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}/pt'
    feitos = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
            page = ctx.new_page()
            erros = []
            page.on('pageerror', lambda e: erros.append(str(e)))
            alvos = {}
            for rel, k, x in lista:
                alvos.setdefault(rel, []).append((k, x))
            for rel, (fonte, pergunta) in EXTRA.items():
                todos = cartoes((ROOT / fonte).read_text('utf-8'))
                alvos.setdefault(rel, []).extend((k, x) for k, x in enumerate(todos) if pergunta in (x.get('p') or ''))
                assert alvos[rel], (rel, pergunta)
            for rel, cartoes_da_pagina in alvos.items():
                page.goto(f'{host}/{rel[:-len("index.html")]}', wait_until='networkidle')
                page.wait_for_function('window.EPIJogo && window.EPICasca')
                for k, x in cartoes_da_pagina:
                    for certo in (True, False):
                        montar(page, x)
                        esperado, fe = responder(page, x, certo)
                        conferir(page, f'{rel} cartão {k} {"certa" if certo else "errada"}', esperado, fe)
                    feitos += 1
                assert not erros, (rel, erros)
            print(f'PASS opções denunciadoras: {feitos} cartões mudados em {len(alvos)} lições, certa aceite e retorno visível, '
                  f'errada com o seu retorno, 390 px sem deslizar para o lado', flush=True)
            browser.close()
    finally:
        server.shutdown()
        os.unlink(os.path.join(raiz, 'pt'))
        os.rmdir(raiz)


if __name__ == '__main__':
    main()
