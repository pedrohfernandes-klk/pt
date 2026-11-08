#!/usr/bin/env python3
"""07/11/2026: decisões 153, 176 e 177 (pedido pt-1 do plano plano-creditos-i-20261105.md, secções 1, 2.1 e 2.3).

O docente, na 153: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir»; na 176: «o "i" é para todos os
textos demasiado grandes que fiquem mal no site»; na 177: «"parar desenho" soa muito mal. "parar animação", ou assim, é melhor».

Constrói scripts/creditos_i_pt1_20261107.json, a camada literal dos créditos atrás de um «i» na entrada, nos nove índices e no
Atlas, com a peça comum que já existe no Português (assets/info-i.css e assets/info-i.js, publicados no pt-2, pedido #181). A
camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/creditos-i-pt1-edits-20261107.json:

  python3 scripts/creditos_i_pt1_20261107.py
  python3 scripts/aplicar_trocas.py scripts/creditos_i_pt1_20261107.json --manifesto tests/fixtures/creditos-i-pt1-edits-20261107.json --nota "…"

Cada família é uma função que devolve trocas {ficheiro, local, antigo, novo, ocorrencias, achado}, calculadas sobre a base (o
texto de cada página com esta camada desfeita, pelo manifesto, quando ele já existe): o script pode voltar a correr depois de a
camada estar aplicada e dá o mesmo JSON. As contagens conferem-se aqui e outra vez no fim. Cada página que ganha um «i» ganha
também, uma vez, a folha e o script da peça comum e uma folha própria, curta, que acerta o «i» àquela página.

Famílias desta camada (secção 2.1 do plano):
- P1, entrada: o crédito do fundo da calçada (p.cf-credito, com o botão dentro) passa para trás de um «i» da variante «linha»; o
  botão sai do crédito, para a .fundo-acoes, e fica sempre à vista. Decisão 177: o botão passa a «Parar a animação» (o motor
  comum, assets/fundos.js, escreve «Parar a animação» e, parado, «Retomar a animação»), e a página carrega o motor com versão nova.
- P2, imagem documental dos nove índices (figure.doc > figcaption.cz-credit): o crédito inteiro vai para o «i» no canto da imagem
  e o figcaption sai (o alt diz o que se vê); aberto, o crédito fica onde estava a legenda (ao lado da imagem a partir de 640 px,
  por baixo dela abaixo disso). No M3 e no M5, a imagem está dentro de uma ligação: a ligação e o «i» ficam lado a
  lado num div.com-i, e o «i» fica fora da ligação. O M8 é CC BY-SA 2.0: a licença ganha a ligação (rel="license").
- P3, fotografia de Muybridge no portal do Lente: o primeiro p.sp-credit (Library of Congress) vai para um «i» da variante
  «linha», por baixo da imagem, à direita (como o «i» de Pessoa no portal do Lente, pedido lente-1); o segundo p.sp-credit
  (ligação cruzada) e o rótulo span.sp-image-label ficam.
- P4, mapa do Atlas: o p.credito (Natural Earth, Equal Earth, OpenStreetMap) vai para o «i» no canto do mapa; à vista fica, no
  outro canto de baixo, um «© OpenStreetMap» curto (decisão 162; a ODbL pede a atribuição à vista).

O crédito não se encurta: cada palavra e cada ligação passam para dentro do «i». Só mudam os separadores «·» (passam a pontos
finais, como no pt-2 e no lente-1), a primeira letra que fica a abrir uma frase e o itálico dos títulos de obras (regra da casa).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/creditos_i_pt1_20261107.json'
MANIFESTO = ROOT / 'tests/fixtures/creditos-i-pt1-edits-20261107.json'
# A peça comum com a versão do pt-2 (a mesma folha e o mesmo script em cache); o motor dos fundos com a versão desta camada.
VERSAO_I = '20261105'
VERSAO_FUNDOS = '20261107'
ACHADO = ('07/11/2026: decisões 153, 176 e 177 (docente: «não quero tanto texto, prefiro um botão com um "i" que o user possa '
          'abrir»; «"parar desenho" soa muito mal. "parar animação", ou assim, é melhor»), pedido pt-1 do plano dos créditos. {f}')
LICENCAS = {'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/deed.pt'}
INDICES = tuple(f'm{n}/index.html' for n in range(1, 10))


def base(rel):
    """O texto da página sem esta camada (desfeita pelo manifesto, da última troca para a primeira)."""
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    if MANIFESTO.is_file():
        for edit in reversed(json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a camada já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    return texto


def troca(rel, texto, local, antigo, novo, familia, contagem=1):
    """Uma troca literal sobre a base, com a contagem exata conferida já aqui."""
    assert texto.count(antigo) == contagem, (rel, local, texto.count(antigo))
    return {'ficheiro': rel, 'local': local, 'antigo': antigo, 'novo': novo, 'ocorrencias': contagem,
            'achado': ACHADO.format(f=familia)}


def peca_i(credito, rotulo, classes='info-i', texto_classes='info-i-texto'):
    return (f'<details class="{classes}" name="info-i"><summary aria-label="{rotulo}"><span aria-hidden="true">i</span>'
            f'</summary><p class="{texto_classes}">{credito}</p></details>')


def com_licenca(credito):
    """A licença CC passa a ligação para o texto da licença (a impressão escreve o endereço por extenso)."""
    for nome, url in LICENCAS.items():
        if nome + '.' in credito and 'rel="license"' not in credito:
            credito = credito.replace(nome + '.', f'<a rel="license" href="{url}">{nome}</a>.')
    return credito


# ---------------------------------------------------------------------------------------------------------------------
# P1 e P3: a entrada (index.html).
P1_FAMILIA = ('Família P1 (fundo da calçada na entrada): o crédito passa inteiro para o «i»; o botão sai do crédito, fica sempre à '
              'vista e passa a «Parar a animação» (decisão 177).')
P1_CREDITO = ('Grafismo gerado com recurso a IA, EPI, 2026, a partir do padrão de ondas da calçada portuguesa (o «mar largo» do '
              'Rossio, Lisboa).')
P1_ANTIGO = (f'<p class="cf-credito">{P1_CREDITO} <button type="button" class="fundo-botao" data-fundo-botao="cf" hidden>Parar o '
             'desenho</button></p>')
P1_NOVO = ('<div class="fundo-acoes cf-credito"><button type="button" class="fundo-botao" data-fundo-botao="cf" hidden>Parar a '
           'animação</button>' + peca_i(P1_CREDITO, 'Créditos do desenho', 'info-i info-i--linha') + '</div>')
P3_FAMILIA = ('Família P3 (fotografia de Muybridge no portal do Lente): o crédito passa inteiro para o «i» («linha», por baixo da '
              'imagem); o rótulo e a ligação cruzada ficam à vista.')
P3_LIGACAO = '<a href="https://www.loc.gov/item/2005684184/">Library of Congress</a>'
P3_ANTIGO = f'<p class="sp-credit">Estudo do movimento · domínio público · {P3_LIGACAO}</p>'
# Os «·» passam a pontos finais (nunca «·» dentro de frases); nenhuma palavra sai e a ligação fica igual.
P3_NOVO = peca_i(f'Estudo do movimento. Domínio público. {P3_LIGACAO}.', 'Créditos da fotografia', 'info-i info-i--linha sp-i')
ENTRADA_ESTILO = (
    '/* 07/11/2026: decisões 153, 176 e 177 (pedido pt-1). Créditos atrás do «i» (assets/info-i.css). O botão do fundo fica fora '
    'do crédito, sempre à vista, na mesma linha do «i» do desenho; aberto, o crédito abre por baixo dos dois e o botão continua '
    'livre; fechada, a linha tem 48 px de altura (eram 97 px a 390 px). O «i» da fotografia do portal do Lente fica por baixo da '
    'imagem, à direita. */'
    'body[data-site="pt"] .raiz .fundo-acoes.cf-credito{min-height:44px;padding:2px 0 1px}'
    '.raiz .fundo-acoes .fundo-botao{margin:0;padding:0}'
    '.raiz .fundo-acoes>details.info-i[open]{flex:1 0 100%}'
    '.raiz .fundo-acoes>.fundo-botao:not([hidden])+details.info-i[open]{margin-block-start:-44px;pointer-events:none}'
    '.raiz .fundo-acoes>details.info-i>.info-i-texto{padding-block-end:6px;color:var(--suave,#444);max-inline-size:60rem}'
    '.site-portal-wrap>details.sp-i{margin-block-start:4px}'
    '.site-portal-wrap>details.sp-i>.info-i-texto{color:var(--suave,#555)}')


def entrada():
    rel = 'index.html'
    texto = base(rel)
    antigo_motor = '<script defer src="assets/fundos.js?v=20261102-1"></script>'
    novo_motor = (f'<link rel="stylesheet" href="assets/info-i.css?v={VERSAO_I}"><style id="creditos-i-pt1">{ENTRADA_ESTILO}'
                  f'</style><script defer src="assets/fundos.js?v={VERSAO_FUNDOS}"></script>'
                  f'<script defer src="assets/info-i.js?v={VERSAO_I}"></script>')
    return [
        troca(rel, texto, 'A peça comum do «i» (assets/info-i.css e assets/info-i.js) e o motor dos fundos com versão nova '
              '(decisão 177)', antigo_motor, novo_motor,
              'A página carrega a peça comum do «i» e o motor dos fundos com o botão novo («Parar a animação»).'),
        troca(rel, texto, 'P1, fundo da calçada: o crédito no «i», o botão fora dele', P1_ANTIGO, P1_NOVO, P1_FAMILIA),
        troca(rel, texto, 'P3, fotografia de Muybridge: o crédito no «i»', P3_ANTIGO, P3_NOVO, P3_FAMILIA),
    ]


# ---------------------------------------------------------------------------------------------------------------------
# P2: a imagem documental dos nove índices (figure.doc), a seguir às unidades (decisão 148). O crédito é só crédito (a obra, a
# data, a fonte, a licença): sai inteiro para o «i» e o figcaption sai. Os títulos de obras ficam em itálico (<em>, como no resto
# dos índices); no M1, «Cancioneiro da Biblioteca Nacional» passa a itálico, como no «i» das lições (pt-2). O texto do «i» leva
# também a classe cz-credit, a do crédito da casa «Cartaz» (alvo de 44 px nas ligações, como no figcaption de antes).
P2_FAMILIA = ('Família P2 (imagem documental do índice do módulo): o crédito passa inteiro para o «i» no canto da imagem; o '
              'figcaption sai e o alt diz o que se vê.')
P2_ITALICO = {'m1/index.html': ('Cancioneiro da Biblioteca Nacional, página', '<em>Cancioneiro da Biblioteca Nacional</em>, página')}
# Decisão 152: «n.º 2» não parte ao mudar de linha (espaço inseparável; as letras são as mesmas).
P2_SEM_QUEBRA = {'m7/index.html': ('n.º 2', 'n.º 2')}
P2_FIGURA = re.compile(r'<figure class="doc">((?:<a [^>]*>)?<img [^>]*>(?:</a>)?)<figcaption class="cz-credit">'
                       r'((?:(?!</figcaption>).)*)</figcaption></figure>')
P2_ESTILO = (
    '/* 07/11/2026: decisões 153, 176 e 177 (pedido pt-1). A imagem documental do índice: o «i» no canto da imagem '
    '(assets/info-i.css). Aberto, a partir de 640 px, o crédito inteiro fica ao lado da imagem, onde estava a legenda, rente ao fundo '
    'dela (e rola por dentro se não couber); abaixo de 640 px, onde a legenda ficava por baixo da imagem, o crédito abre por baixo '
    'dela, no fluxo, com a largura da coluna, e o «i» continua no canto da imagem (a imagem tem a altura fixa de 200 px, de '
    'cartaz-indice-comum.css, e a largura em --doc-w). Na impressão, o crédito sai por extenso ao lado da imagem. */'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc{container-type:inline-size}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i{position:relative;display:block;flex:none;'
    'max-width:45%;line-height:0}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>a{display:block;width:fit-content;line-height:0}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i img{max-width:100%}'
    # Ao lado da imagem, com a letra da legenda de antes. As faixas de 16 px em cima e em baixo guardam o alvo de 44 px das ligações
    # (o ::before da casa «Cartaz») dentro da caixa que rola, e a última linha fica rente ao fundo da imagem, como a legenda.
    '@media screen{body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i>.info-i-texto{'
    'inset-inline:calc(100% + 24px) auto;inset-block:auto -16px;inline-size:calc(100cqi - 100% - 24px);'
    'max-block-size:calc(100% + 32px);overflow:auto;padding:16px 0;border:0;background:none;color:var(--suave);'
    'font:400 .8125rem/1.5 Arial,Helvetica,sans-serif}'
    # Como no crédito da casa «Cartaz» (.cz-credit), o texto deixa passar o toque e só a ligação o recebe, com o alvo de 44 px nos
    # quatro cantos mesmo entre duas linhas; um ::after por baixo de tudo apanha o toque no resto da caixa, que fica do «i» (um
    # toque no crédito não o fecha).
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i>.info-i-texto.cz-credit{'
    'pointer-events:none;isolation:isolate}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i>.info-i-texto.cz-credit::after{'
    'content:"";position:absolute;inset:0;z-index:-2;pointer-events:auto}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i>.info-i-texto.cz-credit a{'
    'pointer-events:auto}}'
    '@media screen and (max-width:639.98px){body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i{max-width:100%;'
    'width:100%}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i{position:static}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i>summary{inset-block:148px auto;'
    'inset-inline:calc(min(var(--doc-w),100%) - 52px) auto}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i>.info-i-texto{position:relative;'
    'inset:auto;inline-size:auto;max-block-size:none;overflow:visible;padding:16px 0 0}}'
    'html:has(main[data-cz-indice].cz-sala) body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc .info-i-texto{'
    'font-size:1.25rem}'
    '@media print{body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i{display:flex;align-items:flex-end;gap:24px;'
    'max-width:none;line-height:normal}body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>:is(img,a){flex:none}'
    'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i>details.info-i{flex:1 1 0;min-width:0}}')
# A largura da imagem com a altura fixa de 200 px (pela proporção dos atributos width e height), para o «i» ficar no canto dela
# quando o crédito abre por baixo, abaixo de 640 px.
P2_LARGURA = 'body.pt-module-layout main.cz-index[data-cz-indice]>figure.doc>.doc-i{{--doc-w:{w}px}}'



def indices():
    trocas = []
    for rel in INDICES:
        texto = base(rel)
        m = P2_FIGURA.search(texto)
        assert m and len(P2_FIGURA.findall(texto)) == 1, rel
        imagem, credito = m.group(1), m.group(2)
        for par in (P2_ITALICO.get(rel), P2_SEM_QUEBRA.get(rel)):
            if par:
                assert credito.count(par[0]) == 1, (rel, par)
                credito = credito.replace(*par)
        largura = int(re.search(r'width="(\d+)"', imagem).group(1))
        altura = int(re.search(r'height="(\d+)"', imagem).group(1))
        estilo = P2_ESTILO + P2_LARGURA.format(w=f'{200 * largura / altura:.2f}')
        novo = (f'<figure class="doc"><div class="doc-i com-i">{imagem}'
                + peca_i(com_licenca(credito), 'Créditos da imagem', texto_classes='info-i-texto cz-credit') + '</div></figure>')
        trocas.append(troca(rel, texto, 'P2, imagem documental do índice: o crédito no «i», o figcaption sai', m.group(0), novo,
                            P2_FAMILIA))
        trocas.append(troca(rel, texto, 'A peça comum do «i» (assets/info-i.css e assets/info-i.js) e a folha da imagem documental',
                            '</head>', f'<link rel="stylesheet" href="../assets/info-i.css?v={VERSAO_I}"><style id="creditos-i-pt1">'
                            f'{estilo}</style><script defer src="../assets/info-i.js?v={VERSAO_I}"></script></head>',
                            'A página carrega a peça comum do «i», igual no Português e no Lente.'))
    return trocas


# ---------------------------------------------------------------------------------------------------------------------
# P4: o mapa do Atlas (atlas/index.html). O «i» fica no canto de baixo à direita do mapa (o .mapa-quadro, que já é a moldura
# posicionada do mapa); o nome do país escolhido, que vivia nesse canto, passa para a esquerda do «i». No canto de baixo à esquerda
# fica à vista o «© OpenStreetMap» curto, decisão 162. O crédito inteiro, letra a letra, vai para o «i».
P4_FAMILIA = ('Família P4 (mapa do Atlas): o crédito passa inteiro para o «i» no canto do mapa; à vista fica um «© OpenStreetMap» '
              'curto, no outro canto (decisão 162).')
P4_CREDITO = ('Mapa: Natural Earth (domínio público), projeção Equal Earth; pontos de passagem: © contribuidores do '
              'OpenStreetMap')
P4_ESTILO = (
    '/* 07/11/2026: decisões 153, 162, 176 e 177 (pedido pt-1). O crédito do mapa no «i» (assets/info-i.css), no canto de baixo à '
    'direita; o nome do país escolhido fica à esquerda do «i»; à vista, no canto de baixo à esquerda, o «© OpenStreetMap» curto, que '
    'se esconde, com o nome do país, enquanto o crédito inteiro está aberto por cima deles. */'
    '.mapa-quadro.com-i .mapa-nome{right:60px}'
    '.mapa-osm{position:absolute;left:8px;bottom:4px;z-index:1;margin:0;padding:0 4px;font:.7rem/1.35 var(--sans);'
    'color:var(--suave);pointer-events:none;text-shadow:0 0 3px var(--papel),0 0 3px var(--papel),0 0 6px var(--papel)}'
    '@media screen{.mapa-quadro>details.info-i>.info-i-texto{font:.8125rem/1.45 var(--sans)}}'
    # Aberto, o crédito inteiro (que já diz «© contribuidores do OpenStreetMap») fica por cima do fundo do mapa: a linha curta e o
    # nome do país, que vivem nesse fundo, escondem-se enquanto ele está aberto, para nada ficar tapado.
    '.mapa-quadro:has(>details.info-i[open]) :is(.mapa-osm,.mapa-nome){visibility:hidden}'
    '@media print{.mapa-osm{position:static;display:block}}')


def atlas():
    rel = 'atlas/index.html'
    texto = base(rel)
    return [
        troca(rel, texto, 'A peça comum do «i» (assets/info-i.css e assets/info-i.js) e a folha do mapa', '</head>',
              f'<link rel="stylesheet" href="../assets/info-i.css?v={VERSAO_I}"><style id="creditos-i-pt1">{P4_ESTILO}</style>'
              f'<script defer src="../assets/info-i.js?v={VERSAO_I}"></script></head>',
              'A página carrega a peça comum do «i», igual no Português e no Lente.'),
        troca(rel, texto, 'P4, mapa do Atlas: a moldura do mapa leva o «i»', '<div class="mapa-quadro">',
              '<div class="mapa-quadro com-i">', P4_FAMILIA),
        troca(rel, texto, 'P4, mapa do Atlas: o «© OpenStreetMap» à vista e o crédito no «i», no canto do mapa',
              '<g class="farol-m"></g></svg></div>',
              '<g class="farol-m"></g></svg><p class="mapa-osm">© OpenStreetMap</p>'
              + peca_i(P4_CREDITO, 'Créditos do mapa') + '</div>', P4_FAMILIA),
        troca(rel, texto, 'P4, mapa do Atlas: sai o crédito por baixo do mapa',
              f'<p class="mapa-nasc" aria-live="polite"></p><p class="credito">{P4_CREDITO}</p></section>',
              '<p class="mapa-nasc" aria-live="polite"></p></section>', P4_FAMILIA),
    ]


FAMILIAS = [entrada, indices, atlas]


def construir():
    """As trocas da camada, pela ordem do JSON (ficheiro a ficheiro; a cabeça da página no fim de cada ficheiro)."""
    trocas = []
    for familia in FAMILIAS:
        trocas += familia()
    for t in trocas:
        assert base(t['ficheiro']).count(t['antigo']) == t['ocorrencias'], t['local']
    trocas.sort(key=lambda t: (t['ficheiro'], t['antigo'] == '</head>'))
    return trocas


def main():
    trocas = construir()
    CAMADA.write_text(json.dumps(trocas, ensure_ascii=False, indent=1) + '\n', 'utf-8', newline='\n')
    print(f'{len(trocas)} trocas em {len({t["ficheiro"] for t in trocas})} ficheiros')


if __name__ == '__main__':
    main()
