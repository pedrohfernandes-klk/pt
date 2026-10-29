"""Painéis corrigidos (27/10/2026): cada pergunta-relâmpago do painel mostra o exercício da lição que anuncia.

28/10/2026: a Sala de aula em tempo real saiu (decisão do docente de 17/10/2026; scripts/desligar_sala.py). Este
teste abria uma sala local (`?local`, BroadcastChannel) e conferia que a lição, no telemóvel, abria a sobreposição
«Relâmpago» com o enunciado enviado pelo painel. Esse canal já não existe, por isso o teste muda de propósito:
o relâmpago passou a ser só do projetor. Confere-se agora, nos quatro painéis corrigidos por conteúdo, que cada
pergunta do seletor, lançada no painel, mostra em letra de cartaz o mesmo enunciado do cartão da lição (o índice
nunca aponta para uma leitura), com o cronómetro a correr e a tecla Esc a escondê-lo, sem erros e sem pedidos para
fora da origem local (os tipos de letra do Google, que as páginas já carregavam, são abortados).

28/10/2026 (revisão): sem telemóveis do outro lado, um enunciado como «Toca nas duas palavras…» ou «Põe … pela
ordem» não se responde se o material não estiver à vista. Confere-se também que cada pergunta lançada mostra por
baixo o material do cartão da lição (opções, pares, itens, palavras, frase com lacunas), sem o QR por cima, e que,
quando o tempo acaba, aparece a correção do cartão; a tecla I volta ao ecrã de abertura.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import html
import json
import threading
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler
from test_paineis_cartoes import CORRIGIDOS, banco, enunciado

FONTES = ('fonts.googleapis.com', 'fonts.gstatic.com')

# o que tem de estar à vista, por tipo de cartão (o material vem de MATERIAL, gerado por scripts/desligar_sala.py)
VISTO = '''m => { const e = document.querySelector('[data-extra] .material'); if (!e) return null;
  const vis = el => !!el && el.getBoundingClientRect().height > 0 && getComputedStyle(el).visibility !== 'hidden';
  return {itens: [...e.querySelectorAll('ol li')].filter(vis).length, frase: vis(e.querySelector('.mat-frase')),
          lacunas: e.querySelectorAll('.mat-frase .lac').length, opcoes: [...e.querySelectorAll('.mat-lac')].filter(vis).length,
          palavras: [...e.querySelectorAll('.mat-pal span')].filter(vis).length, pares: vis(e.querySelector('.mat-pares')),
          esperado: {o: (m.o || []).length, itens: (m.itens || []).length, palavras: (m.palavras || []).length,
                     pares: (m.esq || []).length + (m.dir || []).length, lac: (m.lac || []).length},
          rot: e.querySelector('.rot').textContent, qr: vis(document.querySelector('.qr')), correcao: !!e.querySelector('.mat-correcao')} }'''


def material(texto):
    """MATERIAL do painel (fica dentro da função da página; lê-se do código)."""
    i = texto.index(',MATERIAL=') + len(',MATERIAL=')
    return json.JSONDecoder().raw_decode(texto, i)[0]


def material_visivel(page, c, MAT):
    """O material do cartão c está à vista no projetor (e a correção ainda não)."""
    v = page.evaluate(VISTO, MAT[str(c['k'])])
    assert v, (c['k'], 'sem material')
    t, e = c['t'], v['esperado']
    assert v['rot'].endswith('; depois, em voz alta') and not v['qr'] and not v['correcao'], (c['k'], v)
    if t in ('escolha', 'rever'):
        assert e['o'] >= 2 and v['itens'] == e['o'], (c['k'], v)
    elif t in ('ordenar', 'versos'):
        assert e['itens'] >= 2 and v['itens'] == e['itens'], (c['k'], v)
    elif t == 'frase':
        assert e['palavras'] >= 2 and v['palavras'] == e['palavras'], (c['k'], v)
    elif t == 'emparelhar':
        assert v['pares'] and v['itens'] == e['pares'] >= 4, (c['k'], v)
    elif t == 'completar':
        assert v['frase'] and v['lacunas'] == v['opcoes'] == e['lac'] >= 1, (c['k'], v)
    elif t == 'sublinhar':
        assert v['frase'], (c['k'], v)
    else:
        assert t == 'vf', (c['k'], t)
    return v


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}'
    origem = urlsplit(host).netloc
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(headless=True)
            for pasta in CORRIGIDOS:
                texto = (ROOT / pasta / 'index.html').read_text('utf-8')
                P = banco(texto)
                MAT = material(texto)
                L = banco((ROOT / pasta.replace('painel-', 'licao-') / 'index.html').read_text('utf-8'))
                ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
                painel = ctx.new_page()
                erros, fora = [], []
                painel.on('pageerror', lambda e: erros.append(str(e)))
                painel.on('request', lambda r: fora.append(r.url) if urlsplit(r.url).scheme in ('http', 'https') and urlsplit(r.url).netloc != origem else None)
                painel.route(lambda u: urlsplit(u).scheme in ('http', 'https') and urlsplit(u).netloc != origem, lambda r: r.abort())
                painel.goto(host + '/' + pasta + '/', wait_until='networkidle')
                opcoes = painel.locator('[data-r-k] option')
                assert opcoes.count() == len(P), pasta
                for i, c in enumerate(P):
                    assert L[c['k']]['t'] != 'ler' and enunciado(L[c['k']]) == c['p'], (pasta, c['k'])
                    assert html.unescape(opcoes.nth(i).inner_html()) == c['p'], (pasta, c['k'])
                    painel.locator('[data-r-k]').select_option(str(c['k']))
                    painel.locator('[data-relampago]').click()
                    assert painel.locator('[data-rot]').text_content() == 'Relâmpago, 60 segundos', (pasta, c['k'])
                    assert painel.locator('[data-pedido]').text_content() == c['p'], (pasta, c['k'])
                    assert painel.locator('[data-crono]').is_visible(), (pasta, c['k'])
                    material_visivel(painel, c, MAT)
                    painel.keyboard.press('Escape')
                    assert painel.locator('[data-crono]').is_hidden(), (pasta, c['k'])
                # no fim do tempo, a correção do cartão; I volta ao ecrã de abertura, com o QR
                painel.fill('[data-r-s]', '1')
                painel.locator('[data-r-k]').select_option(str(P[0]['k']))
                painel.locator('[data-relampago]').click()
                painel.locator('[data-extra] .mat-correcao').wait_for(timeout=5000)
                painel.locator('body').click(position={'x': 5, 'y': 200})
                painel.keyboard.press('i')
                assert painel.locator('[data-pedido]').text_content() == 'Abre a lição no telemóvel pelo QR', pasta
                assert painel.locator('.como').is_visible() and painel.locator('.qr img').is_visible(), pasta
                assert painel.locator('[data-crono]').is_hidden(), pasta
                assert not erros, (pasta, erros)
                assert all(urlsplit(u).netloc in FONTES for u in fora), (pasta, fora)
                print('PASS', pasta, len(P), 'perguntas-relâmpago mostram no projetor o enunciado e o material da lição;'
                      ' correção no fim; I volta ao início', flush=True)
                ctx.close()
            b.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
