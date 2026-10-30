"""30/10/2026: texto corrido justificado, com hifenização em português europeu (decisão do docente), no navegador.

Abre uma página de cada família do sítio a 390 e a 1366 px e confere, pelo estilo calculado:

* o texto corrido (textos das obras, leituras, excertos, explicações, parágrafos das páginas) tem text-align justify,
  text-align-last auto e hyphens auto, numa caixa com pelo menos cerca de 22 caracteres por linha, e a língua efetiva
  (o lang do antepassado mais próximo) é pt-PT;
* os versos, as opções, os botões, o retorno curto, as listas, as tabelas, as legendas e os créditos não se justificam;
* não há deslocamento horizontal nem erros na página;
* (30/10/2026, revisão) nenhum bloco justificado tem um botão ou um campo no meio do texto, e a 390 e a 1366 px nenhuma
  linha de um bloco justificado (salvo a última) tem um espaço entre palavras de 4 em ou mais (um nome de ficheiro ou um
  controlo que não parte); o limite é largo porque este Chromium não hifeniza;
* no índice das provas (30/10/2026: deixou de ser área reservada com o #137) justificam-se a entrada e o colofão, como no
  laboratório, e os blocos de cada prova ficam à esquerda; nas provas em cartões, a prosa da prova (.prova-l sem .estrofe)
  justifica-se e as estrofes não.

Também a 320 px (30/10/2026, revisão: abaixo de 22.5em, telemóveis pequenos ou ampliação), em todos os casos, e a 300 px:
o texto corrido volta à esquerda e a hifenização mantém-se, sem deslocamento horizontal nem controlos em texto justificado.
Nas lições, percorre os cartões com «Seguinte» (e, em projeção, com «Mostrar resposta») até ao cartão pedido; numa
escolha responde mal de propósito para ver o retorno da opção escolhida (à esquerda) e a explicação (justificada).
O sítio é servido em /pt/ (como no GitHub Pages). O Chromium sem interface não traz dicionários de hifenização, por isso
só se confere o valor calculado de hyphens, não os cortes.
Corre com: python tests/browser_texto_justificado.py
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

# Seletores que, se existirem, nunca podem estar justificados (em qualquer página).
NUNCA = ('.jogo .ler .v:not(.prova-l:not(.estrofe))', '.jogo .ler .v:not(.prova-l:not(.estrofe)) *', '.pass-verso .vl', 'div.verso', 'blockquote.cit:not(.prosa) p', 'p.verso',
         'button', 'button *', 'li', 'td', 'th', 'figcaption', 'label', 'summary', 'h1', 'h2', 'h3', 'p.fonte',
         'p.fonte-x', 'p.rodape', '.casca-folha .c-veredito', '.casca-folha .c-expl .resp-proj',
         '#palco .caixa p:not(.prosa):has(br)', '#palco .caixa:has(>.chips) p', '.jogo .ler p.cita', '.jogo .ler p.q', 'p.perg',
         # 30/10/2026 (revisão): o retorno da opção escolhida (.fe) passou a acompanhar a explicação e saiu desta lista; entram
         # o parágrafo com o botão de imprimir dos mapas, as especificações de entrega das guias e a pergunta de abertura a
         # negrito do Pensar devagar
         'details.sec > p:has(button)', '#arquivo-producoes section.tarefa-c > p:not([class])', '.jogo .ler p.etq-m + p')


# 30/10/2026 (revisão): a 320 px, os questionários já se deslocavam na base (865aa802): o estado de cada questionário
# (span.estado, em maiúsculas e sem quebra) tem 322 a 344 px. Não é do alinhamento; fica registado e fora desta verificação.
DESLOCAMENTO_ANTERIOR = {('m8/questionarios/', 320)}


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def ler_seguinte(page):
    """Carrega em «Seguinte» (ou «Começar», «Continuar», «Mostrar resposta») se houver; devolve se carregou."""
    return page.evaluate("""() => {
      const vis = b => { const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !b.disabled; };
      const b = [...document.querySelectorAll('button')].filter(vis)
        .find(b => /^(Seguinte|Começar|Continuar|Mostrar resposta)/.test(b.textContent.trim()));
      if (b) { b.click(); return true; } return false;
    }""")


def projetar_ate(page, seletor, maximo=60):
    """30/10/2026: em projeção (sem respostas), avança com R e → até haver um elemento visível com este seletor; as provas
    em cartões pedem resposta antes de «Seguinte», e o texto da prova só existe no cartão em que aparece."""
    vis = 's => [...document.querySelectorAll(s)].some(e => e.getBoundingClientRect().height > 0)'
    for _ in range(maximo):
        if page.evaluate(vis, seletor):
            return True
        page.keyboard.press('r')
        page.wait_for_timeout(120)
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(300)
    return page.evaluate(vis, seletor)


def ate(page, seletor, maximo=20):
    """Avança nos cartões até haver um elemento visível com este seletor (com folga para as transições dos cartões)."""
    for _ in range(maximo):
        if page.evaluate('s => [...document.querySelectorAll(s)].some(e => e.getBoundingClientRect().height > 0)', seletor):
            return True
        if not ler_seguinte(page):
            page.wait_for_timeout(400)
            if not ler_seguinte(page):
                break
        page.wait_for_timeout(350)
    return page.evaluate('s => [...document.querySelectorAll(s)].some(e => e.getBoundingClientRect().height > 0)', seletor)


def responder_mal(page):
    """M6-F12: os dois cartões de leitura e depois uma escolha (certas: 0 e 1; as opções 2 e 3 estão erradas). O motor
    varia as opções mostradas entre tentativas, por isso escolhe-se a primeira opção errada que estiver no cartão."""
    errada = '.jogo button.op:is([data-j="2"],[data-j="3"])'
    assert ate(page, errada), 'não chegou à escolha da M6-F12'
    page.locator(errada).filter(visible=True).first.click()
    page.wait_for_selector('.casca-folha.aberta .c-expl .fe', timeout=5000)


def html_do_cartao(rel, trecho):
    """30/10/2026 (revisão): o HTML de um cartão «ler» tal como está nos dados (o primeiro que contém o trecho). Serve os
    cartões que só aparecem depois de responder a perguntas: o teste põe esse HTML no cartão aberto e confere a regra
    sobre a marcação real."""
    texto = (ROOT / rel).read_text('utf-8')
    for m in re.finditer(r'"html":("(?:[^"\\]|\\.)*")', texto):
        h = json.loads(m.group(1))
        if trecho in h:
            return h
    raise AssertionError(f'{rel}: nenhum cartão com {trecho!r}')


def injetar(rel, trecho):
    def preparar(page):
        page.evaluate("""h => { const ler = [...document.querySelectorAll('.jogo .ler')].find(e => e.getBoundingClientRect().height > 0);
          ler.innerHTML = h; }""", html_do_cartao(rel, trecho))
    return preparar


def cena_das_posicoes(rel):
    """30/10/2026 (revisão): a cena do cartão «Quem sabe o quê» (p.cid-cena), gerada pelo próprio motor
    (EPITipos.posicoes.html) com a cena que está nos dados, no cartão aberto."""
    cena = json.loads(re.search(r'"cena":("(?:[^"\\]|\\.)*")', (ROOT / rel).read_text('utf-8')).group(1))

    def preparar(page):
        page.evaluate("""c => { const ler = [...document.querySelectorAll('.jogo .ler')].find(e => e.getBoundingClientRect().height > 0);
          ler.innerHTML = EPITipos.posicoes.html({cena: c, p: 'Pergunta', papeis: []}); }""", cena)
    return preparar


def projecao_ate_explicacao(page):
    for _ in range(20):
        if page.locator('.casca-folha.aberta .c-expl').count():
            return
        if not ler_seguinte(page):
            break
        page.wait_for_timeout(250)
    raise AssertionError('em projeção, nenhuma explicação apareceu')


# (família, página, preparação, seletores de texto corrido justificado, seletores que ficam à esquerda)
CASOS = [
    ('lições em cartões: leitura e verso', 'm7/licao-m7-f34/', lambda p: None,
     ['.jogo .ler p.abre'], ['.casca-topo .c-marca']),
    ('lições em cartões: verso', 'm7/licao-m7-f34/', lambda p: ate(p, '.jogo .ler .v'),
     [], ['.jogo .ler .v', '.jogo .ler .v .ln']),
    ('lições em cartões: texto da obra', 'm4/licao-m4-f07/', lambda p: ate(p, '.jogo .ler p.pr'),
     ['.jogo .ler p.pr'], []),
    # 30/10/2026 (revisão): o retorno da opção escolhida (.fe) acompanha a explicação (três a quatro linhas no telemóvel)
    ('lições em cartões: retorno e explicação', 'm6/licao-m6-f12/', responder_mal,
     ['.casca-folha .c-expl', '.casca-folha .c-expl .fe'], ['.casca-folha .c-veredito', '.jogo button.op .tx']),
    ('lições em cartões: falas de teatro com <br> (texto da obra)', 'm4/licao-m4-f08/',
     injetar('m4/licao-m4-f08/index.html', 'Procurai nestes retratos'), ['.jogo .ler p.pr:has(br)'], []),
    ('lições em cartões: fala em blockquote sem parágrafos (recursos .js)', 'm4/licao-m4-f28/',
     injetar('m4/recursos/tpc-entrada.js', 'Lê a primeira fala de Madalena'), ['.jogo .ler blockquote.prosa'], ['.jogo .ler p.fonte']),
    ('lições em cartões: linha do plano da aula', 'm4/licao-m4-f11/', lambda p: None, ['.jogo p.aula-linha'], []),
    ('Pensar devagar: cena das posições', 'm5/m5-o-pais-ou-eles/', cena_das_posicoes('m5/m5-o-pais-ou-eles/index.html'),
     ['.jogo p.cid-cena'], ['.jogo p.q']),
    ('Pensar devagar: pergunta de abertura a negrito', 'm8/m8-george-tres-idades/', lambda p: None,
     [], ['.jogo .ler p.etq-m + p']),
    ('exercícios de telemóvel: rótulo com verso citado', 'm7/gram-valores-pessoa/', lambda p: ate(p, '#palco .caixa p.verso'),
     [], ['#palco .caixa p.verso']),
    ('lições em cartões: projeção', 'm7/licao-m7-f34/?projetar=1', projecao_ate_explicacao,
     ['.casca-folha .c-expl'], ['.casca-folha .c-expl .resp-proj']),
    ('lições novas', 'm9/licao-m9-f12/', lambda p: None, ['.jogo .ler p.abre', '.jogo .ler p:not([class])'], []),
    ('aquecimentos', 'tarefas/m7-u1/aquecimento/', lambda p: None, ['.jogo .ler p.abre'], []),
    ('provas em cartões (herdam a regra dos cartões)', 'exame/provas/2026-1f/grupo-i/', lambda p: None,
     ['.jogo .ler p:not([class])'], ['.jogo .ler li']),
    # 30/10/2026: a prosa da prova (o Memorial do Convento da captura do docente) justifica-se; as estrofes não
    ('provas em cartões: prosa da prova', 'exame/provas/2026-1f/grupo-i/?projetar=1',
     lambda p: projetar_ate(p, '.jogo .ler .prova-l:not(.estrofe)'), ['.jogo .ler .prova-l:not(.estrofe)'], []),
    ('provas em cartões: estrofes', 'exame/provas/2026-1f/grupo-i/?projetar=1',
     lambda p: projetar_ate(p, '.jogo .ler .prova-l.estrofe'), [], ['.jogo .ler .prova-l.estrofe']),
    ('Pensar devagar: excerto em prosa', 'm4/m4-sermao-tribunal/', lambda p: ate(p, 'blockquote.prosa p'),
     ['blockquote.prosa > p', '.jogo .ler p:not([class])'], []),
    ('Pensar devagar: estrofes', 'm1/m1-voz-emprestada/', lambda p: ate(p, 'blockquote.cit:not(.prosa) p'),
     [], ['blockquote.cit:not(.prosa) p']),
    ('exercícios de telemóvel: prosa dialogada', 'm5/eca-hotel/', lambda p: ate(p, '#palco .caixa p.prosa'),
     ['#palco .caixa p.prosa'], []),
    ('exercícios de telemóvel: verso com <br>', 'm7/pessoa-ceifeira/', lambda p: ate(p, '#palco .caixa p:has(br)'),
     [], ['#palco .caixa p:has(br)']),
    ('exercícios de telemóvel: prosa de teatro com <br>', 'm4/frei-luis-ninguem/', lambda p: ate(p, '#palco .caixa p.prosa'),
     ['#palco .caixa p.prosa', '#palco .caixa p:not([class]):not(:has(br))'], []),
    ('exercícios de telemóvel: estrofe citada numa linha', 'm6/cesario-gas/', lambda p: ate(p, '#palco .caixa p.verso'),
     [], ['#palco .caixa p.verso']),
    ('exercícios de telemóvel: versos com lacuna', 'm2/ines-panela/', lambda p: ate(p, '#palco .caixa > .chips'),
     [], ['#palco .caixa:has(> .chips) p']),
    ('exercícios de telemóvel: itens a classificar', 'm3/camoes-desconcerto/', lambda p: ate(p, '#palco .caixa > .chips'),
     [], ['#palco .caixa:has(> .chips) p']),
    ('lições em cartões: verso citado num caso', 'm1/licao-m1-f04/', lambda p: ate(p, '.jogo .ler p.cx.verso'),
     [], ['.jogo .ler p.cx.verso']),
    ('Tabacaria', 'm7/tabacaria/', lambda p: None, [], ['div.verso']),
    ('índice do módulo', 'm8/', lambda p: None,
     ['.pt-module details.regra > div', '.pt-module p.regras', '.pt-module section.cartao > p.pequeno'],
     ['p.rodape', 'header.topo p.lead.mod-pergunta', 'header.topo p.lead.mod-ambito']),
    ('mapa do módulo', 'm8/mapa-do-modulo-m8/', lambda p: None,
     ['header.topo > p.lead', 'aside.unit-map-note > p', 'details.sec > p:not([class]):not(:has(button))'],
     ['aside.unit-map-note li', 'details.sec > p:has(button)']),
    ('guia da tarefa', 'm8/guia-da-tarefa-m8/', lambda p: None, ['#escolha > p:not([class])'], []),
    ('guia da tarefa com o arquivo das produções', 'm4/guia-da-tarefa-m4/', lambda p: None,
     ['main > p:not([class])', '#arquivo-producoes > p:not([class])', '#arquivo-producoes p.ex'],
     ['#arquivo-producoes li', '#arquivo-producoes p.quem', '#arquivo-producoes section.tarefa-c > p:not([class])']),
    ('mapa do módulo sem nota de unidades', 'm1/mapa-do-modulo-m1/', lambda p: None, ['main > header.topo > p.lead'], []),
    ('portefólio do módulo com secções', 'm6/portefolio-do-modulo-m6/', lambda p: None,
     ['main > section > p:not([class])'], ['table td']),
    ('índice do módulo com nota', 'm7/', lambda p: None, ['.pt-module main > p.pequeno'], ['p.rodape']),
    ('portefólio do módulo', 'm8/portefolio-do-modulo-m8/', lambda p: None,
     ['main > div.regra', 'main > h2 + p:not([class])'], ['table td']),
    ('visitas', 'm8/visita-caderno-de-campo/', lambda p: None, ['section[id] .cx > p:not([class])'], ['label']),
    ('painel de aula (sem texto corrido)', 'm8/painel-m8-f10/', lambda p: None, [], ['p.como']),
    ('painel de notas', 'm2/painel-m2-f12/', lambda p: None, ['main.pg > p:not([class])'], []),
    ('painel de notas (notas.css)', 'm9/painel-m9-f11/', lambda p: None, ['main > h1 ~ p:not(:has(a))'],
     ['main > p:first-child', 'main li']),
    ('painel de notas (notas.css, bloco que se abre)', 'm4/painel-m4-f28/', lambda p: None, ['main > details p'],
     ['main > p:first-child', 'main li', 'main summary']),
    ('painel de notas (notes.css, main sem classe)', 'm6/painel-m6-f12/', lambda p: None,
     ['main > h1 ~ p:not([class]):not(:has(a))', 'main li > details > p'],
     ['main > p:first-child', 'main > p:has(a)', 'main li > p', 'main summary']),
    ('prova rápida', 'm8/prova-a/', lambda p: None, ['section#entrada > .aviso'], []),
    ('questionários', 'm8/questionarios/', lambda p: None, ['section#indice > .aviso'], []),
    ('guião de aula', 'm4/aulas/aula-06/', lambda p: None, ['.dois .caixa p:not([class])', 'ol.disc p.r'],
     ['ol.disc p.p', 'p.meta']),
    ('índice dos guiões', 'm4/aulas/', lambda p: None, ['header.cab + p.nota', 'header.cab > p.meta'], ['ol.lista-u p.d']),
    ('tarefa', 'tarefas/m4-u3/', lambda p: None, ['.task-page .task-consultation', '.task-texts blockquote'], []),
    ('tarefa com exemplos', 'tarefas/m7-u3/', lambda p: ate(p, '.task-example > p:not([class])'),
     ['.task-example > p:not([class])', '.task-example > p.task-example-text'], []),
    ('grelha', 'tarefas/m7-u3/grelha/', lambda p: None, ['main.grelha > header > p:not([class])'], ['dd > p']),
    ('obras', 'obras/memorial/', lambda p: None, ['main.ob > p:not([class])', '.ob-aviso'], []),
    ('entrada do sítio', 'index.html', lambda p: None, ['.pt-entry-lead'], []),
    ('portal do ano', '3/', lambda p: None, ['.p-cab .p-lead'], []),
    ('atlas', 'atlas/', lambda p: None, ['.atlas-investigar > p:not([class])'], []),
    ('portal dos exercícios comuns', 'c/', lambda p: None, ['main.pg > p:not([class])'], []),
    ('exame: sessão em prosa', 'exame/#s02/ler', lambda p: p.wait_for_selector('.pass-prosa .par'),
     ['.pass-prosa .par', '#app .source > p.context', '#app p.callout'], ['.pass-credito']),
    ('exame: sessão em verso', 'exame/#s01/ler', lambda p: p.wait_for_selector('.pass-verso .vl'),
     [], ['.pass-verso .vl', '.pass-credito']),
    ('exame: laboratório', 'exame/laboratorio/', lambda p: None,
     ['#laboratorio .of-rosto > .of-entrada', '#laboratorio .of-colofao-texto > p:not(:has(a))'],
     ['#laboratorio .of-colofao-texto > p:has(a)']),
    # 30/10/2026: o índice das provas deixou de ser área reservada com o #137
    ('índice das provas', 'exame/provas/', lambda p: None,
     ['main#provas .of-rosto > .of-entrada', 'main#provas .of-colofao-texto > p:not(:has(a))'], ['.pv-prova p']),
    ('página não encontrada (texto centrado)', '404.html', lambda p: None, [], []),
]

MEDIR = """([j, e, nunca]) => {
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
  const info = el => { const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    const lang = el.closest('[lang]');
    return { ta: cs.textAlign, tal: cs.textAlignLast, hy: cs.hyphens, w: r.width, fs: parseFloat(cs.fontSize),
             lang: lang ? lang.getAttribute('lang') : null, t: el.textContent.trim().slice(0, 50) }; };
  const out = { j: {}, e: {}, nunca: [], sw: document.documentElement.scrollWidth, iw: innerWidth,
                html: document.documentElement.getAttribute('lang') };
  for (const s of j) out.j[s] = [...document.querySelectorAll(s)].filter(vis).filter(x => x.textContent.trim()).map(info);
  for (const s of e) out.e[s] = [...document.querySelectorAll(s)].filter(vis).map(info);
  for (const s of nunca) for (const el of document.querySelectorAll(s)) {
    if (vis(el) && getComputedStyle(el).textAlign === 'justify') out.nunca.push(s + ' :: ' + el.textContent.trim().slice(0, 50));
  }
  const just = [...document.querySelectorAll('body *')].filter(el => vis(el) && getComputedStyle(el).textAlign === 'justify'
    && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
  out.todos = just.map(el => el.textContent.trim().slice(0, 40));
  // 30/10/2026 (revisão): controlos dentro de texto justificado e o maior espaço entre palavras de cada bloco (fora da última
  // linha), medido com Range espaço a espaço; só nos blocos curtos (até 2500 caracteres, os 200 primeiros da página)
  out.controlos = just.filter(el => el.querySelector('button,input,select,textarea')).map(el => el.textContent.trim().slice(0, 50));
  out.buracos = [];
  for (const el of just.slice(0, 200)) {
    if (el.textContent.length > 2500 || el.querySelector('p,div,li,blockquote')) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize), esp = [];
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n;
    while ((n = tw.nextNode())) for (let i = 0; i < n.textContent.length; i++) if (n.textContent[i] === ' ') {
      const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1); const b = r.getBoundingClientRect();
      if (b.width > 0) esp.push({ w: b.width / fs, y: Math.round(b.top), t: n.textContent.slice(Math.max(0, i - 20), i + 20) });
    }
    const ultima = Math.max(...esp.map(e => e.y));
    const pior = esp.filter(e => e.y !== ultima).sort((a, b) => b.w - a.w)[0];
    if (pior && pior.w >= 4) out.buracos.push(pior.w.toFixed(1) + ' em: «' + pior.t + '»');
  }
  return out;
}"""


def nova(browser, width, erros):
    ctx = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
    page = ctx.new_page()
    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
    page.route('**/*youtube*/**', lambda r: r.abort())
    page.on('pageerror', lambda e: erros.append('pageerror: ' + str(e)))
    page.on('response', lambda r: erros.append(f'{r.status}: {r.url}')
            if r.url.startswith('http://127.0.0.1') and r.status >= 400 and not r.url.endswith('/404-teste') else None)
    return ctx, page


def verificar(browser, host, width, falhas):
    for familia, url, preparar, justificados, esquerda in CASOS:
        erros = []
        ctx, page = nova(browser, width, erros)
        onde = f'{familia} ({url}, {width} px)'
        try:
            page.goto(f'{host}/{url}', wait_until='load')
            page.wait_for_timeout(400)
            preparar(page)
            page.evaluate("() => document.querySelectorAll('details').forEach(d => { d.open = true; })")
            page.wait_for_timeout(150)
            r = page.evaluate(MEDIR, [justificados, esquerda, list(NUNCA)])
        except Exception as e:  # noqa: BLE001
            falhas.append(f'{onde}: {e}')
            ctx.close()
            continue
        if r['html'] != 'pt-PT':
            falhas.append(f'{onde}: <html lang> é {r["html"]}')
        if r['sw'] > r['iw'] + 1 and (url, width) not in DESLOCAMENTO_ANTERIOR:
            falhas.append(f'{onde}: deslocamento horizontal ({r["sw"]} > {r["iw"]})')
        for s, els in r['j'].items():
            if not els:
                falhas.append(f'{onde}: nenhum elemento visível para {s}')
            for el in els:
                if width < 360:
                    # 30/10/2026 (revisão): abaixo de 22.5em o texto corrido volta à esquerda e a hifenização fica
                    if el['ta'] == 'justify' or el['hy'] != 'auto':
                        falhas.append(f'{onde}: {s} devia voltar à esquerda e manter a hifenização: {el}')
                    continue
                cpl = el['w'] / (el['fs'] * 0.5)
                if el['ta'] != 'justify' or el['tal'] != 'auto' or el['hy'] != 'auto':
                    falhas.append(f'{onde}: {s} devia estar justificado e hifenizado: {el}')
                if el['lang'] != 'pt-PT':
                    falhas.append(f'{onde}: {s} com língua efetiva {el["lang"]}: {el["t"]}')
                if cpl < 22:
                    falhas.append(f'{onde}: {s} justificado numa caixa estreita ({cpl:.0f} caracteres): {el["t"]}')
        for s, els in r['e'].items():
            if not els:
                falhas.append(f'{onde}: nenhum elemento visível para {s} (o teste perdeu o sentido)')
            for el in els:
                if el['ta'] == 'justify':
                    falhas.append(f'{onde}: {s} não se justifica: {el["t"]}')
        for x in r['nunca']:
            falhas.append(f'{onde}: justificado sem dever: {x}')
        for x in r['controlos']:
            falhas.append(f'{onde}: controlo dentro de texto justificado: {x}')
        if width >= 390:
            for x in r['buracos']:
                falhas.append(f'{onde}: buraco num bloco justificado: {x}')
        if 'área reservada' in familia and r['todos']:
            falhas.append(f'{onde}: a área reservada não muda, mas há texto justificado: {r["todos"][:3]}')
        for x in erros:
            falhas.append(f'{onde}: {x}')
        ctx.close()


def verificar_estreito(browser, host, falhas):
    """Abaixo de 22.5em (300 px, ampliação forte): o texto volta à esquerda; a hifenização fica."""
    erros = []
    ctx, page = nova(browser, 300, erros)
    page.goto(f'{host}/obras/memorial/', wait_until='load')
    page.wait_for_timeout(300)
    r = page.evaluate("""() => [...document.querySelectorAll('main.ob > p:not([class])')].map(el => {
        const cs = getComputedStyle(el); return { ta: cs.textAlign, hy: cs.hyphens }; })""")
    if not r:
        falhas.append('300 px: nenhum parágrafo em obras/memorial')
    for x in r:
        if x['ta'] == 'justify' or x['hy'] != 'auto':
            falhas.append(f'300 px: o texto devia voltar à esquerda e manter a hifenização: {x}')
    if page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'):
        falhas.append('300 px: deslocamento horizontal em obras/memorial')
    falhas.extend('300 px: ' + x for x in erros)
    ctx.close()


def main():
    raiz = tempfile.mkdtemp(prefix='justificado-pt-')
    os.symlink(ROOT, os.path.join(raiz, 'pt'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=raiz))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}/pt'
    falhas = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for width in (320, 390, 1366):  # 30/10/2026 (revisão): também 320 px, abaixo do limiar (texto à esquerda)
                verificar(browser, host, width, falhas)
            verificar_estreito(browser, host, falhas)
            browser.close()
    finally:
        server.shutdown()
    if falhas:
        print('\n'.join(falhas))
        sys.exit(1)
    print(f'texto justificado: {len(CASOS)} casos de todas as famílias a 390 e 1366 px (justificados) e a 320 px (à esquerda), '
          'e a 300 px; tudo certo')


if __name__ == '__main__':
    main()
