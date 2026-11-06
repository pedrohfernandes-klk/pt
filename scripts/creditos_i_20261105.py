#!/usr/bin/env python3
"""05/11/2026: decisões 153 e 162. O docente: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir».

Constrói scripts/creditos_i_20261105.json, a camada literal dos créditos atrás de um «i» no Português (pedido pt-2 do
plano plano-creditos-i-20261105.md). A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em
tests/fixtures/creditos-i-edits-20261105.json:

  python3 scripts/creditos_i_20261105.py
  python3 scripts/aplicar_trocas.py scripts/creditos_i_20261105.json --manifesto tests/fixtures/creditos-i-edits-20261105.json --nota "…"

Cada família do plano é uma função que devolve trocas {ficheiro, local, antigo, novo, ocorrencias, achado}, calculadas
sobre a base (o texto de cada página com esta camada desfeita, pelo manifesto, quando ele já existe): o script pode voltar a
correr depois de a camada estar aplicada e dá o mesmo JSON. Cada página que ganha um «i» ganha também, uma vez, a folha e o
script da peça comum (assets/info-i.css e assets/info-i.js), antes de </head>.

Regras (secção 1 do plano): o «i» é uma <details class="info-i" name="info-i"> dentro da moldura da imagem (a <span
class="moldura"> passa a <div class="moldura com-i">), com um <summary aria-label="Créditos da imagem"> que só mostra
<span aria-hidden="true">i</span> e um só <p class="info-i-texto"> com o crédito inteiro. O crédito não se encurta: cada
palavra passa para dentro do «i»; a licença CC ganha a ligação (rel="license"), que a impressão escreve por extenso. Se a
legenda fica vazia, sai o <figcaption> e o alt diz o que se vê; o que diz o que se vê e serve a pergunta fica à vista.

Famílias desta camada:
- P7, crédito puro nas lições M1 e M4 (27 páginas, 47 figuras).
- P10, Pessoa, cerca de 1914 (span.tabela da varredura de formatação): M7-F01, M7-F05 e a galeria do mapa M7.
- P11, dupla exposição de «Chuva Oblíqua» (M7-F34): a instrução e os botões ficam à vista; o crédito vai para o «i».
- P12, retratos do «Em paralelo» (p.rosto-c, variante «linha»): M1-F19, M4-F01, M4-F02 e M4-F11 (8 retratos).
- P13, crédito colado à explicação (fim do campo f): sai da explicação e vai para o «i» da imagem do campo ver, nas
  lições M4-F01, M4-F04 e M4-F11 e nos três painéis (o motor das lições põe o «i» fora da figura que amplia).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/creditos_i_20261105.json'
MANIFESTO = ROOT / 'tests/fixtures/creditos-i-edits-20261105.json'
VERSAO = '20261105'
ACHADO = ('05/11/2026: decisão 153 (docente: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir»), '
          'pedido pt-2 do plano dos créditos. {familia}')
LICENCAS = {
    'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/deed.pt',
    'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/deed.pt',
    'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/deed.pt',
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/deed.pt',
    'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/deed.pt',
    'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/deed.pt',
}


def base(rel):
    """O texto da página sem esta camada (desfeita pelo manifesto, da última troca para a primeira)."""
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    if MANIFESTO.is_file():
        for edit in reversed(json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a camada já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    return texto


def em_json(html, barra=False):
    """O HTML tal como fica dentro de uma cadeia JSON dos cartões (aspas com barra; o resto igual). Com barra=True, também
    «</» passa a «<\\/», como no MATERIAL dos painéis."""
    cadeia = json.dumps(html, ensure_ascii=False)[1:-1]
    return cadeia.replace('</', '<\\/') if barra else cadeia


def com_licenca(credito):
    """A licença CC passa a ligação para o texto da licença (a impressão escreve o endereço por extenso)."""
    for nome, url in LICENCAS.items():
        if nome + '.' in credito and '<a' not in credito:
            credito = credito.replace(nome + '.', f'<a rel="license" href="{url}">{nome}</a>.')
    return credito


def sem_quebras(credito):
    """Decisão 152: as datas aproximadas e os intervalos de anos não partem ao mudar de linha (span.nb, na peça comum)."""
    return re.sub(r'(?<![\w>])(c\. \d{3,4}(?:-\d{2,4})?|\d{3,4}-\d{2,4})(?![\w<])', r'<span class="nb">\1</span>', credito)


def peca_i(credito, rotulo='Créditos da imagem', linha=False):
    classe = 'info-i info-i--linha' if linha else 'info-i'
    return (f'<details class="{classe}" name="info-i"><summary aria-label="{rotulo}"><span aria-hidden="true">i</span>'
            f'</summary><p class="info-i-texto">{sem_quebras(com_licenca(credito))}</p></details>')


# ---------------------------------------------------------------------------------------------------------------------
# P7: crédito puro nas lições M1 e M4 (figure.fig > span.moldura + figcaption), montante aulas-claras/licao_v2.py fig().
# O que vem depois dos dois pontos diz o que se vê e serve a pergunta («as muralhas», «a primeira página do sermão»):
# fica à vista, numa legenda curta; o crédito (obra, data, licença) vai para o «i». As outras legendas são só crédito:
# saem inteiras para o «i» e o figcaption sai (o alt de cada imagem já diz o que se vê).
P7_A_VISTA = {
    '<i>Cancioneiro da Biblioteca Nacional</i>, cópia do século XVI: cantigas de D. Dinis. Domínio público.':
        ('Cantigas de D. Dinis.', '<i>Cancioneiro da Biblioteca Nacional</i>, cópia do século XVI. Domínio público.'),
    '<i>Crónicas</i> de Froissart, século XV (pormenor): as muralhas. Domínio público.':
        ('Pormenor: as muralhas.', '<i>Crónicas</i> de Froissart, século XV (pormenor). Domínio público.'),
    '<i>Crónicas</i> de Froissart, século XV (pormenor): o arraial. Domínio público.':
        ('Pormenor: o arraial.', '<i>Crónicas</i> de Froissart, século XV (pormenor). Domínio público.'),
    '<i>Sermoens</i> de Vieira, Lisboa, 1682: a primeira página do sermão. Domínio público.':
        ('A primeira página do sermão.', '<i>Sermoens</i> de Vieira, Lisboa, 1682. Domínio público.'),
    '<i>Sermoens</i>, Lisboa, 1682: o começo do cap. I. Domínio público.':
        # «cap. I» não parte ao mudar de linha (decisão 152): espaço inseparável.
        ('O começo do cap.\u00a0I.', '<i>Sermoens</i>, Lisboa, 1682. Domínio público.'),
    '<i>Sermoens</i> de Vieira, Lisboa, 1682: a nota por baixo do título. Domínio público.':
        ('A nota por baixo do título.', '<i>Sermoens</i> de Vieira, Lisboa, 1682. Domínio público.'),
    '<i>Frei Luiz de Sousa</i>, primeira edição, 1844: a lista de personagens. Domínio público.':
        ('A lista de personagens.', '<i>Frei Luiz de Sousa</i>, primeira edição, 1844. Domínio público.'),
    '<i>Frei Luiz de Sousa</i>, primeira edição, 1844: a lista das pessoas. Domínio público.':
        ('A lista das pessoas.', '<i>Frei Luiz de Sousa</i>, primeira edição, 1844. Domínio público.'),
}
# Imagens com menos de 240 px de largura no cartão (medidas a 320, 390, 852 e 1366 px: a gravura de D. Dinis tem 229 a
# 239 px e a cantiga de Codax, 207 a 215 px): variante «linha», com o crédito por baixo da imagem.
P7_LINHA = {'../../img/fontes/dinis-gravura-1594.jpg', '../../img/fontes/codax-ondas-1915.jpg'}
P7_FIGURA = re.compile(r'<figure class=\\"fig([^"\\]*)\\"><span class=\\"moldura\\">(<img [^>]*>)</span>'
                       r'<figcaption>((?:(?!</figcaption>).)*)</figcaption></figure>')


def p7():
    trocas = []
    for caminho in sorted(ROOT.glob('m[14]/licao-m[14]-f*/index.html')):
        rel = caminho.relative_to(ROOT).as_posix()
        texto = base(rel)
        for m in P7_FIGURA.finditer(texto):
            classes, img, legenda = m.group(1), m.group(2), json.loads('"' + m.group(3) + '"')
            src = re.search(r'src=\\"([^"\\]+)\\"', img).group(1)
            visivel, credito = P7_A_VISTA.get(legenda, (None, legenda))
            novo = ('<figure class="fig' + classes + '"><div class="moldura com-i">' + json.loads('"' + img + '"')
                    + peca_i(credito, linha=src in P7_LINHA) + '</div>'
                    + (f'<figcaption>{visivel}</figcaption>' if visivel else '') + '</figure>')
            trocas.append({'ficheiro': rel, 'local': f'P7, crédito puro: {legenda[:70]}', 'antigo': m.group(0),
                           'novo': em_json(novo), 'ocorrencias': texto.count(m.group(0)),
                           'achado': ACHADO.format(familia='Família P7 (crédito puro nas lições M1 e M4): o crédito passa '
                                                   'inteiro para o «i»; o que diz o que se vê fica à vista.')})
    return trocas


def troca(rel, texto, local, antigo, novo, familia, contagem=1):
    """Uma troca literal sobre a base, com a contagem exata conferida já aqui."""
    assert texto.count(antigo) == contagem, (rel, local, texto.count(antigo))
    return {'ficheiro': rel, 'local': local, 'antigo': antigo, 'novo': novo, 'ocorrencias': contagem,
            'achado': ACHADO.format(familia=familia)}


def confere_json(antigo, novo, barra=False):
    """O texto novo de uma cadeia JSON lê-se e volta a escrever-se igual, com a convenção de escape da página."""
    for cadeia in (antigo, novo):
        assert em_json(json.loads('"' + cadeia + '"'), barra) == cadeia, cadeia[:80]


# ---------------------------------------------------------------------------------------------------------------------
# P10: Pessoa, cerca de 1914 (span.tabela da varredura de formatação de 01/11, «sem controlo de abertura»). A decisão 153
# substitui essa regra: os seis campos do crédito («Fotógrafo não identificado», «retrato de Fernando Pessoa com chapéu»,
# «cerca de 1914 (data incerta)», «reprodução no Wikimedia Commons», «original sem instituição indicada», a ligação
# «domínio público» para File:PessoaChapeu.jpg) passam inteiros para o «i»; o rótulo «Fernando Pessoa, cerca de 1914.» fica à
# vista (secção 4 do plano), e no mapa M7 também a ligação «Lição M7-F01». Variante «linha»: nas lições, a fotografia tem 220 a
# 253 px de largura no cartão (medida a 320, 390, 852 e 1366 px), e na galeria do mapa as miniaturas têm 150 px ou pouco mais.
P10_ROTULO = 'Fernando Pessoa, cerca de 1914.'
P10_ALT = 'alt="Fernando Pessoa de chapéu e óculos, cerca de 1914" loading="lazy">'
P10_TABELA = re.compile(r'<span class="tabela">((?:(?!</span>).)*</a>\.)</span>')
P10_FAMILIA = ('Família P10 (Pessoa, cerca de 1914): os seis campos do crédito passam inteiros para o «i»; o rótulo '
               '«Fernando Pessoa, cerca de 1914.» fica à vista.')


def p10():
    trocas = []
    for rel in ('m7/licao-m7-f01/index.html', 'm7/licao-m7-f05/index.html'):
        texto = base(rel)
        # A abertura da figura: a moldura passa a div (a <details> não cabe num span). O começo do src (a fotografia vem em
        # data:) é único na página; o resto da imagem fica igual e fora da troca.
        abre = '<figure class=\\"fig\\"><span class=\\"moldura\\"><img src=\\"data:image/jpeg;base64,'
        trocas.append(troca(rel, texto, 'P10, Pessoa: a moldura da fotografia passa a div.moldura.com-i', abre,
                            abre.replace('<span class=\\"moldura\\">', '<div class=\\"moldura com-i\\">'), P10_FAMILIA))
        fim = re.search(re.escape(em_json(P10_ALT)) + r'</span><figcaption>' + re.escape(P10_ROTULO) +
                        r'(<span class=\\"tabela\\">(?:(?!</span>).)*</span>)</figcaption></figure>', texto)
        credito = P10_TABELA.fullmatch(json.loads('"' + fim.group(1) + '"')).group(1)
        novo = (em_json(P10_ALT) + em_json(peca_i(credito, linha=True)) + '</div><figcaption>' + P10_ROTULO
                + '</figcaption></figure>')
        confere_json(fim.group(0), novo)
        trocas.append(troca(rel, texto, 'P10, Pessoa: o crédito (span.tabela) passa para o «i»; o rótulo fica', fim.group(0),
                            novo, P10_FAMILIA))
    rel = 'm7/mapa-do-modulo-m7/index.html'
    texto = base(rel)
    m = re.search(re.escape(P10_ALT) + r'<figcaption>' + re.escape(P10_ROTULO) + r' (<a href="[^"]+">Lição M7-F01</a>)'
                  r'<span class="tabela">((?:(?!</span>).)*</a>\.)</span></figcaption>', texto)
    novo = (P10_ALT + peca_i(m.group(2), 'Créditos da imagem: Fernando Pessoa', linha=True) + '<figcaption>' + P10_ROTULO
            + ' ' + m.group(1) + '</figcaption>')
    trocas.append(troca(rel, texto, 'P10, Pessoa na galeria «Para ver»: o crédito passa para o «i»; o rótulo e «Lição M7-F01» '
                        'ficam', m.group(0), novo, P10_FAMILIA))
    return trocas


# ---------------------------------------------------------------------------------------------------------------------
# P11: a dupla exposição de «Chuva Oblíqua» (M7-F34). A instrução («Toca num pedaço do verso: acende-se o seu plano.») e os
# botões dos versos ficam à vista; a frase do crédito sai inteira do <small> para o «i». O «i» não pode viver dentro do
# div.dupla-foto, que tem role="img" (os filhos de uma imagem não chegam aos leitores de ecrã): a fotografia e o «i» ficam
# juntos num div.com-i, que toma a largura da fotografia (até 560 px, centrada, como o div.dupla-foto).
P11_REL = 'm7/licao-m7-f34/index.html'
P11_INSTRUCAO = 'Toca num pedaço do verso: acende-se o seu plano.'
P11_ESTILO = ('/* 05/11/2026: decisão 153. O «i» da dupla exposição: a moldura toma a largura da fotografia. */'
              '.dupla>.com-i{max-width:560px;margin:0 auto}')
P11_FAMILIA = ('Família P11 (dupla exposição de «Chuva Oblíqua»): a instrução e os botões ficam à vista; o crédito das duas '
               'fotografias passa inteiro para o «i».')


def p11():
    texto = base(P11_REL)
    m = re.search(r'<figure class=\\"dupla\\">(<div class=\\"dupla-foto\\"(?:(?!</div>).)*</div>)<figcaption>'
                  r'((?:(?!</figcaption>).)*)<small>' + re.escape(P11_INSTRUCAO) + r' ((?:(?!</small>).)*)</small>'
                  r'</figcaption></figure>', texto)
    credito = json.loads('"' + m.group(3) + '"')
    novo = (f'<figure class=\\"dupla\\"><div class=\\"com-i\\">{m.group(1)}{em_json(peca_i(credito))}</div><figcaption>'
            f'{m.group(2)}<small>{P11_INSTRUCAO}</small></figcaption></figure>')
    confere_json(m.group(0), novo)
    return [troca(P11_REL, texto, 'P11, dupla exposição: o crédito sai do small para o «i»; a instrução fica', m.group(0), novo,
                  P11_FAMILIA)]


# ---------------------------------------------------------------------------------------------------------------------
# P12: retratos do «Em paralelo» (p.rosto-c por baixo do retrato redondo de 76 px). Variante «linha»: o «i» logo por baixo do
# retrato, alinhado à direita dele, e o crédito abre no fluxo, com a largura da coluna (assets/pt-lessons/aula-clara.css).
# Cada parágrafo era só crédito (autor, obra, data, licença): sai inteiro para o «i»; o alt do retrato e o título da coluna
# (h3) dizem o que se vê. Dois retratos no mesmo cartão: o nome acessível junta a identificação curta de cada um.
P12_PAGINAS = ('m1/licao-m1-f19/index.html', 'm4/licao-m4-f01/index.html', 'm4/licao-m4-f02/index.html',
               'm4/licao-m4-f11/index.html')
P12_IDENTIFICACAO = {'Mendinho': 'ilha de San Simón', 'Martim Codax': 'Pergaminho Vindel', 'Santo António': 'Santo António',
                     'António Vieira': 'António Vieira', 'Almeida Garrett': 'Almeida Garrett'}
P12_ROSTO = re.compile(r'<p class=\\"rosto-c\\">((?:(?!</p>).)*)</p><h3>((?:(?!</h3>).)*)</h3>')
P12_FAMILIA = ('Família P12 (retratos do «Em paralelo»): o crédito do retrato passa inteiro para o «i», variante «linha»; o '
               'título da coluna fica à vista.')


def p12():
    trocas = []
    for rel in P12_PAGINAS:
        texto = base(rel)
        for m in P12_ROSTO.finditer(texto):
            credito, titulo = json.loads('"' + m.group(1) + '"'), m.group(2)
            # «séc. XVIII» não parte ao mudar de linha (decisão 152): espaço inseparável.
            credito = credito.replace('séc. ', 'séc.\u00a0')
            novo = em_json(peca_i(credito, f'Créditos da imagem: {P12_IDENTIFICACAO[titulo]}', linha=True)) + f'<h3>{titulo}</h3>'
            confere_json(m.group(0), novo)
            trocas.append(troca(rel, texto, f'P12, retrato do «Em paralelo» ({titulo}): o crédito passa para o «i»',
                                m.group(0), novo, P12_FAMILIA))
    return trocas


# ---------------------------------------------------------------------------------------------------------------------
# P13: o crédito colado ao fim da explicação (campo f) das perguntas que mostram uma imagem (campo ver). Sai da explicação e
# vai, letra a letra, para o «i» dessa imagem (variante «canto», num div.com-i); o itálico do motor (_…_) passa a <i> e o «&»
# a «&amp;». Nas lições, o motor (assets/pt-lessons/jogo.js, corpo()) põe o «i» fora da figura que amplia, que é um botão;
# a imagem ocupa a largura do cartão. Nos painéis, o MATERIAL mostra a imagem num figure.mat-ver, com 30vh de altura, onde a
# moldura se ajusta à imagem: a imagem tem 154 a 346 px de largura (medida a 320, 390, 852 e 1366 px), menos de 240 px em
# pelo menos uma largura nos três painéis, e por isso o «i» é da variante «linha».
P13_CREDITOS = {
    'peixe-voador-1889.jpg': 'Cromolitografia: Allen & Ginter, _Peixe-voador_ (série _Fish from American Waters_), 1889, The Met. '
                             'Domínio público.',
    'boccioni-cidade-que-sobe-1910.jpg': 'Pintura: Umberto Boccioni, _A cidade que sobe_, 1910, MoMA. Domínio público.',
    'frei-luis-personagens-1844.jpg': 'Imagem: _Frei Luiz de Sousa_, primeira edição, 1844. Domínio público.',
}
P13_PAGINAS = {'m4/licao-m4-f01/index.html': 'peixe-voador-1889.jpg', 'm4/painel-m4-f01/index.html': 'peixe-voador-1889.jpg',
               'm4/licao-m4-f04/index.html': 'boccioni-cidade-que-sobe-1910.jpg',
               'm4/painel-m4-f04/index.html': 'boccioni-cidade-que-sobe-1910.jpg',
               'm4/licao-m4-f11/index.html': 'frei-luis-personagens-1844.jpg',
               'm4/painel-m4-f11/index.html': 'frei-luis-personagens-1844.jpg'}
P13_ESTILO_PAINEL = ('/* 05/11/2026: decisão 153. O «i» da imagem do material: a moldura ajusta-se à imagem. */'
                     '.material .mat-ver>.com-i{width:fit-content;max-width:100%}')
P13_FAMILIA = ('Família P13 (crédito colado à explicação): o crédito sai do fim do campo f e passa inteiro para o «i» da '
               'imagem do campo ver.')


def md_para_html(texto):
    """O itálico do motor (_…_) em <i>, e o «&» em entidade, como o it() das lições e o md() dos painéis o mostravam."""
    return re.sub(r'_([^_]+)_', r'<i>\1</i>', texto.replace('&', '&amp;'))


def p13():
    trocas = []
    for rel, imagem in P13_PAGINAS.items():
        texto, painel = base(rel), '/painel-' in rel
        credito = P13_CREDITOS[imagem]
        # O campo f inteiro (o texto novo tem de ser único na página, para a camada se desfazer letra a letra).
        f = [m for m in re.finditer(r'"f":"((?:[^"\\]|\\.)*)"', texto) if m.group(1).endswith(' ' + credito)]
        assert len(f) == 1, (rel, len(f))
        antigo = f[0].group(0)
        trocas.append(troca(rel, texto, f'P13, explicação: o crédito ({imagem}) sai do fim do campo f', antigo,
                            antigo[:-len(' ' + credito + '"')] + '"', P13_FAMILIA))
        ver = re.search(r'"ver":"(<img src=\\"\.\./\.\./img/fontes/' + re.escape(imagem) + r'\\"[^>]*>)"', texto)
        img = json.loads('"' + ver.group(1) + '"')
        novo = '"ver":"' + em_json(f'<div class="com-i">{img}{peca_i(md_para_html(credito), linha=painel)}</div>', painel) + '"'
        confere_json(ver.group(0)[7:-1], novo[7:-1], painel)
        trocas.append(troca(rel, texto, f'P13, imagem do campo ver ({imagem}): ganha o «i» com o crédito', ver.group(0), novo,
                            P13_FAMILIA))
    return trocas


FAMILIAS = [p7, p10, p11, p12, p13]
# Estilos próprios de uma página, que entram na cabeça com a peça comum (depois dela, para a acertar àquela página).
ESTILOS = {P11_REL: P11_ESTILO, 'm4/painel-m4-f01/index.html': P13_ESTILO_PAINEL,
           'm4/painel-m4-f04/index.html': P13_ESTILO_PAINEL, 'm4/painel-m4-f11/index.html': P13_ESTILO_PAINEL}
CABECA = (f'<link rel="stylesheet" href="../../assets/info-i.css?v={VERSAO}">'
          f'<script defer src="../../assets/info-i.js?v={VERSAO}"></script></head>')


def main():
    trocas = []
    for familia in FAMILIAS:
        trocas += familia()
    ficheiros = []
    for troca in trocas:
        if troca['ficheiro'] not in ficheiros:
            ficheiros.append(troca['ficheiro'])
    for rel in ficheiros:
        texto = base(rel)
        assert texto.count('</head>') == 1 and 'assets/info-i.' not in texto, rel
        cabeca = CABECA.replace('</head>', f'<style>{ESTILOS[rel]}</style></head>') if rel in ESTILOS else CABECA
        trocas.append({'ficheiro': rel, 'local': 'A peça comum do «i» (assets/info-i.css e assets/info-i.js)',
                       'antigo': '</head>', 'novo': cabeca, 'ocorrencias': 1,
                       'achado': ACHADO.format(familia='A página carrega a peça comum do «i», igual no Português e no Lente.')})
    for troca in trocas:
        assert base(troca['ficheiro']).count(troca['antigo']) == troca['ocorrencias'], troca['local']
    trocas.sort(key=lambda t: (t['ficheiro'], t['antigo'] == '</head>'))
    CAMADA.write_text(json.dumps(trocas, ensure_ascii=False, indent=1) + '\n', 'utf-8', newline='\n')
    print(f'{len(trocas)} trocas em {len(ficheiros)} ficheiros')


if __name__ == '__main__':
    main()
