"""28/10/2026: a Sala de aula em tempo real está desligada (decisão do docente de 17/10/2026), no navegador.

Abre e responde a uma lição (M2-F01, até ao fim), abre outras duas lições (M1-F05, congelada, e M4-F20, onde o
canal vinha noutra posição), abre três painéis (M1, M3 e M4: as variantes com e sem itálico, com e sem Atlas) e usa
o relâmpago, a pausa, o fim do cronómetro, a tecla Esc e o «Quem sou eu?», abre o índice do M3 e corre o fim do
Desafio da unidade (onde estava o envio do resultado), abre o índice do M1, abre o Atlas e corre o fim de uma
ronda (onde estava o envio para o mapa da turma), abre o antigo mapa da turma e a página inicial.
28/10/2026 (revisão): nos painéis, o relâmpago mostra o material do cartão e, no fim do tempo, a correção; o
«Quem sou eu?» (tecla A) dá uma pista por cada terço do tempo e a resposta no fim; I volta ao ecrã de abertura.

Em todas as páginas:
- page.on('request') regista cada pedido; falha se algum sair da origem local, exceto os que essa página pede de
  facto por outros motivos (FONTES e POR_PAGINA, com a justificação). Esses pedidos são abortados, para o teste
  correr sem rede; nenhum é POST. No fim, cada entrada da lista tem de ter sido pedida pelo menos uma vez, para
  a lista não guardar entradas mortas.
- EventSource, BroadcastChannel, WebSocket e navigator.sendBeacon ficam vigiados: se uma página os usar, falha.
- antes de a página correr, o contexto guarda o que a Sala deixava no aparelho (epi-sala, epi-sala-atlas,
  painel-sala-*, epi-atlas-sala em sessionStorage) e uma chave que não é da Sala; depois de carregar, a limpeza
  tem de ter apagado as da Sala e deixado a outra.
Precisa da árvore numa pasta chamada «pt» (os endereços são /pt/...), como browser_atlas_exploracao.py.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import re
import threading
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from browser_m1_and_inventory import ROOT, QuietHandler
from browser_m2_complete import respond
from browser_paineis_relampago import material_visivel

# Pedidos para fora permitidos, por prefixo: só GET, nenhum leva dados do aluno.
# 28/10/2026 (revisão): a lista era por domínio, valia para todas as páginas e tinha domínios que nenhuma página aberta
# pede (vídeos, miniaturas, Commons). Agora tem só o que as páginas abertas pedem de facto, e por página.
# Os ficheiros dos tipos de letra (fonts.gstatic.com) não chegam a ser pedidos, porque o CSS que os pede é abortado.
FONTES = {
    'https://fonts.googleapis.com/': 'CSS dos tipos de letra Bebas Neue e Special Elite (lições, painéis, '
                                     'índices, Atlas e página inicial; já antes da Sala)',
}
POR_PAGINA = {
    '/pt/': {'https://pedrohfernandes-klk.github.io/lente/assets/':
             'a página inicial usa o estilo e o script editorial do Lente, o sítio irmão (já antes da Sala)'},
    '/pt/m1/': {'https://pedrohfernandes-klk.github.io/pt/img/':
                'imagem com endereço absoluto do sítio publicado que o índice já carregava antes da Sala '
                '(cancioneiro-biblioteca-nacional.jpg; o mesmo nos índices do M2, M4 e M6 a M9)'},
    '/pt/atlas/sala/': {'https://pedrohfernandes-klk.github.io/pt/atlas/':
                        'pedido novo e de propósito, igual ao das fontes: a página curta que substitui o mapa da '
                        'turma leva ao Atlas publicado (meta refresh); é uma navegação, não leva dados'},
}
USADOS = set()

SEMENTE = '''(() => {
  window.__canais = [];
  const vigiar = nome => function (...a) { window.__canais.push(nome + ' ' + String(a[0] || '')); throw new Error('canal ' + nome + ' usado'); };
  for (const nome of ['EventSource', 'BroadcastChannel', 'WebSocket']) {
    try { Object.defineProperty(window, nome, {value: vigiar(nome), configurable: true, writable: true}); } catch (e) {}
  }
  try { navigator.sendBeacon = u => { window.__canais.push('sendBeacon ' + u); return false; }; } catch (e) {}
  try {
    if (!localStorage.getItem('qa-semeado')) {
      localStorage.setItem('qa-semeado', '1');
      localStorage.setItem('qa-outra-chave', 'fica');
      localStorage.setItem('epi-sala', JSON.stringify({cod: 'QATST', alc: 'Ana', t: Date.now()}));
      localStorage.setItem('epi-sala-atlas', JSON.stringify({cod: 'QATST', alc: 'Ana', t: Date.now()}));
      localStorage.setItem('painel-sala-m3-f02', JSON.stringify({cod: 'QATST', t: Date.now()}));
      localStorage.setItem('painel-sala-m1-f04', JSON.stringify({cod: 'QATST', t: Date.now()}));
      sessionStorage.setItem('epi-atlas-sala', 'QATST');
    }
  } catch (e) {}
})();'''

LIMPO = '''() => {
  const sala = [];
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (k === 'epi-sala' || k === 'epi-sala-atlas' || k.startsWith('painel-sala-')) sala.push(k);
  }
  if (sessionStorage.getItem('epi-atlas-sala') !== null) sala.push('sessionStorage:epi-atlas-sala');
  return {sala, outra: localStorage.getItem('qa-outra-chave'), canais: window.__canais || [], episala: typeof window.EPISala};
}'''


class Visita:
    """Um contexto novo por página: semente da Sala, pedidos registados e abortados se saírem da origem."""

    def __init__(self, browser, host, largura=390, caminho=None):
        self.host = host
        self.permitidos = dict(FONTES, **POR_PAGINA.get(caminho, {}))
        self.ctx = browser.new_context(viewport={'width': largura, 'height': 850}, reduced_motion='reduce')
        self.ctx.add_init_script(SEMENTE)
        self.page = self.ctx.new_page()
        self.pedidos, self.erros = [], []
        self.page.on('request', lambda r: self.pedidos.append((r.method, r.url)))
        self.page.on('pageerror', lambda e: self.erros.append(str(e)))
        origem = urlsplit(host).netloc
        self.page.route(lambda url: urlsplit(url).scheme in ('http', 'https') and urlsplit(url).netloc != origem,
                        lambda route: route.abort())

    def abrir(self, caminho, espera='networkidle'):
        r = self.page.goto(self.host + caminho, wait_until=espera)
        assert r is None or r.ok, caminho
        return self.page

    def fora(self):
        origem = urlsplit(self.host).netloc
        maus = []
        for metodo, url in self.pedidos:
            partes = urlsplit(url)
            if partes.scheme not in ('http', 'https') or partes.netloc == origem:
                continue
            prefixo = next((p for p in self.permitidos if url.startswith(p)), None)
            if metodo != 'GET' or prefixo is None:
                maus.append((metodo, url))
            else:
                USADOS.add(prefixo)
        return maus

    def confirmar(self, onde, limpeza=True):
        estado = self.page.evaluate(LIMPO)
        assert not self.erros, (onde, self.erros)
        assert not estado['canais'], (onde, estado['canais'])
        assert estado['episala'] == 'undefined', (onde, 'window.EPISala existe')
        if limpeza:
            assert estado['sala'] == [], (onde, 'a limpeza não apagou', estado['sala'])
            assert estado['outra'] == 'fica', (onde, 'a limpeza apagou uma chave que não é da Sala')
        maus = self.fora()
        assert not maus, (onde, 'pedidos para fora da origem local', maus)
        externos = sorted({urlsplit(u).netloc for _, u in self.pedidos if urlsplit(u).netloc not in ('', urlsplit(self.host).netloc)})
        return externos

    def fechar(self):
        self.ctx.close()


def licao_respondida(browser, host):
    v = Visita(browser, host)
    page = v.abrir('/pt/m2/licao-m2-f01/')
    page.locator('#baralho .cartao').wait_for()
    assert page.locator('#liga-sala, [data-sala], #sala, #faixa-pausa, #sobre').count() == 0
    page.locator('[data-c-menu]').first.click()
    menu = page.locator('.casca-menu').first
    menu.wait_for()
    assert menu.locator('button', has_text=re.compile(r'^\s*Sala')).count() == 0
    assert 'Código da sala' not in menu.inner_text()
    assert 'O que marcas fica só neste aparelho' in menu.inner_text()
    page.keyboard.press('Escape')
    for _ in range(160):
        if page.locator('#baralho .cartao.fim').count():
            break
        respond(page)
        assert not v.erros, v.erros
    else:
        raise AssertionError('M2-F01: não chegou ao fim')
    estado = page.evaluate('JSON.parse(localStorage.getItem("licao-m2-f01")||"null")')
    assert estado and estado.get('lida'), estado
    externos = v.confirmar('lição M2-F01 respondida')
    v.fechar()
    print('PASS lição M2-F01 respondida até ao fim, sem menu «Sala» nem pedidos para fora:', externos, flush=True)
    for caminho in ('/pt/m1/licao-m1-f05/', '/pt/m4/licao-m4-f20/'):
        v = Visita(browser, host)
        page = v.abrir(caminho)
        page.locator('#baralho .cartao').wait_for()
        respond(page)
        externos = v.confirmar(caminho)
        v.fechar()
        print('PASS', caminho, 'abre e responde ao primeiro cartão, limpeza feita:', externos, flush=True)


def cartoes(page):
    texto = page.content()
    inicio = texto.index('CARTOES=') + len('CARTOES=')
    return json.JSONDecoder().raw_decode(texto[inicio:])[0]


def material(page):
    texto = page.content()
    inicio = texto.index(',MATERIAL=') + len(',MATERIAL=')
    return json.JSONDecoder().raw_decode(texto[inicio:])[0]


ABERTURA = """() => [document.querySelector('[data-rot]').textContent, document.querySelector('[data-pedido]').textContent,
  !!document.querySelector('.como'), document.querySelector('[data-crono]').hidden, document.querySelector('.qr img').getBoundingClientRect().width]"""


def painel(browser, host, caminho, italico, com_atlas):
    v = Visita(browser, host, largura=1440, caminho=caminho)
    page = v.abrir(caminho)
    assert page.locator('.placar, [data-cod], .sala-cod, [data-nova], [data-sorteio], [data-votacao], [data-codigo]').count() == 0
    assert page.locator('[data-pedido]').inner_text() == 'Abre a lição no telemóvel pelo QR'
    assert page.locator('.qr img').evaluate('i => i.complete && i.naturalWidth > 100'), 'QR da lição'
    abertura = page.evaluate(ABERTURA)
    # 28/10/2026 (revisão): no ecrã de abertura o QR, agora a única entrada dos alunos, ocupa o lugar do placar
    assert abertura[2] and abertura[3] and abertura[4] >= 300, abertura
    C, M = cartoes(page), material(page)
    assert C and page.locator('[data-r-k] option').count() == len(C)
    for c in C[:3]:
        page.locator('[data-r-k]').select_option(str(c['k']))
        page.locator('[data-relampago]').click()
        assert page.locator('[data-crono]').is_visible()
        assert page.locator('[data-rot]').text_content() == 'Relâmpago, 60 segundos'
        esperado = re.sub(r'_([^_]+)_', r'\1', c['p']) if italico else c['p']
        assert page.locator('[data-pedido]').text_content() == esperado, (caminho, c['k'])
        if italico and '_' in c['p']:
            assert page.locator('[data-pedido] i').count() >= 1
        material_visivel(page, c, M)
        page.keyboard.press('Escape')
        assert page.locator('[data-crono]').is_hidden()
    # no fim do tempo, a correção do cartão
    page.fill('[data-r-s]', '1')
    page.locator('[data-r-k]').select_option(str(C[0]['k']))
    page.locator('[data-relampago]').click()
    page.locator('[data-extra] .mat-correcao').wait_for(timeout=5000)
    page.fill('[data-r-s]', '60')
    page.locator('body').click(position={'x': 5, 'y': 200})
    page.keyboard.press('r')
    assert page.locator('[data-crono]').is_visible()
    page.locator('[data-fecha]').click()
    assert page.locator('[data-fecha]').text_content() == 'Parar o cronómetro'
    assert page.locator('[data-crono]').is_hidden()
    # I volta ao ecrã de abertura (antes, depois do primeiro relâmpago, só recarregando)
    page.keyboard.press('i')
    assert page.evaluate(ABERTURA) == abertura, page.evaluate(ABERTURA)
    page.keyboard.press('p')
    assert page.locator('[data-rot]').text_content() == 'Pausa de 3 minutos'
    assert page.locator('[data-pedido]').text_content() == 'Cartões 1 a 4, no telemóvel'
    page.fill('[data-p-min]', '0.05')
    page.locator('[data-pausa]').click()
    page.wait_for_function('() => document.querySelector("[data-rot]").textContent === "Tempo"', timeout=10000)
    assert page.locator('[data-pedido]').text_content() == 'Pousa o telemóvel e olha para o projetor'
    assert page.locator('[data-crono]').evaluate('c => c.classList.contains("fim")')
    if com_atlas:
        # tecla A (o botão anunciava-a e não fazia nada); uma pista por cada terço do tempo; a resposta no fim
        page.fill('[data-a-s]', '3')
        page.locator('body').click(position={'x': 5, 'y': 200})
        page.keyboard.press('a')
        assert page.locator('[data-rot]').text_content() == 'Quem sou eu? 3 segundos'
        assert page.locator('[data-pedido]').text_content() == 'Quem sou eu?'
        assert page.locator('[data-extra] .mat-pistas li').count() == 1
        assert page.locator('[data-extra] .material > ol:not(.mat-pistas) li').count() >= 2
        page.wait_for_function('() => document.querySelectorAll("[data-extra] .mat-pistas li").length === 2', timeout=3000)
        page.locator('[data-extra] .mat-remate').wait_for(timeout=5000)
        assert page.locator('[data-extra] .mat-pistas li').count() == 3
        assert page.locator('[data-pedido]').text_content() != 'Quem sou eu?'
        page.keyboard.press('i')
        assert page.evaluate(ABERTURA) == abertura
    else:
        assert page.locator('[data-atlas]').count() == 0
    externos = v.confirmar(caminho)
    # o antigo modo «?local» (BroadcastChannel) também já não existe
    page.goto(host + caminho + '?local', wait_until='networkidle')
    page.keyboard.press('r')
    externos += v.confirmar(caminho + '?local')
    v.fechar()
    print('PASS painel', caminho, f'relâmpago com material ({min(3, len(C))} cartões), correção no fim, pausa, Esc, I',
          '«Quem sou eu?» com a tecla A' if com_atlas else 'sem Atlas', 'sem placar nem pedidos para fora:',
          sorted(set(externos)), flush=True)


def indice_e_desafio(browser, host):
    v = Visita(browser, host, caminho='/pt/m3/')
    page = v.abrir('/pt/m3/')
    page.evaluate('''() => { const m = EPIJogo.montar; window.__desafio = null;
      EPIJogo.montar = cfg => { if (/^Desafio da unidade/.test(cfg.titulo || '')) window.__desafio = cfg; return m(cfg); }; }''')
    page.locator('[data-desafio="1"]').click()
    page.locator('.casca.sobreposta .cartao').wait_for()
    page.evaluate('() => window.__desafio.fim({certas: 8, total: 8, n: 8})')
    guardado = page.evaluate('JSON.parse(localStorage.getItem("desafio-unidade-v2-M3-u1") || "null")')
    assert guardado and guardado.get('ganho') is True and guardado.get('total') == 8, guardado
    externos = v.confirmar('índice M3 e fim do Desafio')
    v.fechar()
    print('PASS índice M3: fim do Desafio da unidade grava no aparelho e não envia nada:', externos, flush=True)
    # 28/10/2026 (revisão): o índice do M1 pede uma imagem com endereço absoluto do sítio publicado (já antes da Sala)
    v = Visita(browser, host, caminho='/pt/m1/')
    v.abrir('/pt/m1/')
    externos = v.confirmar('índice M1')
    v.fechar()
    print('PASS índice M1: limpeza feita, só os pedidos que já fazia:', externos, flush=True)


def atlas(browser, host):
    v = Visita(browser, host, largura=1440, caminho='/pt/atlas/')
    page = v.abrir('/pt/atlas/')
    assert page.locator('[data-sala], .sala-f').count() == 0
    assert page.get_by_role('button', name=re.compile('Sala')).count() == 0
    page.locator('#atlas-memoria>summary').click()
    page.locator('[data-passaporte]').click()
    assert page.get_by_role('dialog').is_visible()
    page.locator('.folha-c .fechar').press('Escape')
    page.evaluate('''() => { const m = EPIJogo.montar; window.__ronda = null;
      EPIJogo.montar = cfg => { if (cfg.marca === 'Atlas') window.__ronda = cfg; return m(cfg); }; }''')
    page.locator('#desafio [data-comecar]').click()
    page.locator('.casca.sobreposta').wait_for()
    assert page.evaluate('() => !!window.__ronda'), 'a ronda do Atlas não abriu'
    page.evaluate('() => window.__ronda.fim({certas: 0, total: window.__ronda.itens.length})')
    page.get_by_role('button', name='Fechar', exact=True).click()
    externos = v.confirmar('Atlas e fim de uma ronda')
    v.fechar()
    print('PASS Atlas: sem «Sala de aula»; o fim da ronda não envia nada:', externos, flush=True)
    # o antigo mapa da turma: limpa e leva ao Atlas publicado (o pedido do refresh é abortado aqui)
    v = Visita(browser, host, caminho='/pt/atlas/sala/')
    v.page.goto(host + '/pt/atlas/sala/', wait_until='load')
    v.page.wait_for_timeout(800)
    assert any(u == 'https://pedrohfernandes-klk.github.io/pt/atlas/' for _, u in v.pedidos), v.pedidos
    assert not v.erros, v.erros
    # o refresh abortado deixa o separador numa página de erro; volta-se à origem local, no mesmo separador (o mesmo
    # sessionStorage), numa página sem a limpeza (404.html), para ler o que ficou guardado
    assert 'epi-sala' not in (ROOT / '404.html').read_text('utf-8')
    v.page.goto(host + '/pt/404.html', wait_until='load')
    externos = v.confirmar('mapa da turma')
    v.fechar()
    print('PASS atlas/sala: limpa o aparelho e leva ao Atlas:', externos, flush=True)


def inicio(browser, host):
    v = Visita(browser, host, caminho='/pt/')
    page = v.abrir('/pt/')
    assert 'registo' in page.locator('[data-pf-conta]').inner_text()
    externos = v.confirmar('página inicial')
    v.fechar()
    print('PASS página inicial: a limpeza corre antes do progresso:', externos, flush=True)


def main():
    assert ROOT.name == 'pt', 'Corre numa cópia da árvore numa pasta chamada «pt»'
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT.parent)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            licao_respondida(browser, host)
            painel(browser, host, '/pt/m1/painel-m1-f04/', italico=True, com_atlas=False)
            painel(browser, host, '/pt/m3/painel-m3-f02/', italico=False, com_atlas=True)
            painel(browser, host, '/pt/m4/painel-m4-f20/', italico=True, com_atlas=True)
            indice_e_desafio(browser, host)
            atlas(browser, host)
            inicio(browser, host)
            browser.close()
    finally:
        server.shutdown()
    listados = set(FONTES) | {p for d in POR_PAGINA.values() for p in d}
    assert USADOS == listados, ('entradas da lista que nenhuma página pediu', sorted(listados - USADOS))
    print('Pedidos para fora permitidos (só GET, nenhum com dados do aluno):', flush=True)
    for prefixo, porque in FONTES.items():
        print(f'  todas: {prefixo}: {porque}', flush=True)
    for pagina, lista in POR_PAGINA.items():
        for prefixo, porque in lista.items():
            print(f'  {pagina}: {prefixo}: {porque}', flush=True)


if __name__ == '__main__':
    main()
