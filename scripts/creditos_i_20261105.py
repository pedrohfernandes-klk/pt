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


def em_json(html):
    """O HTML tal como fica dentro de uma cadeia JSON dos cartões (aspas com barra; o resto igual)."""
    return json.dumps(html, ensure_ascii=False)[1:-1]


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


FAMILIAS = [p7]
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
        trocas.append({'ficheiro': rel, 'local': 'A peça comum do «i» (assets/info-i.css e assets/info-i.js)',
                       'antigo': '</head>', 'novo': CABECA, 'ocorrencias': 1,
                       'achado': ACHADO.format(familia='A página carrega a peça comum do «i», igual no Português e no Lente.')})
    for troca in trocas:
        assert base(troca['ficheiro']).count(troca['antigo']) == troca['ocorrencias'], troca['local']
    trocas.sort(key=lambda t: (t['ficheiro'], t['antigo'] == '</head>'))
    CAMADA.write_text(json.dumps(trocas, ensure_ascii=False, indent=1) + '\n', 'utf-8', newline='\n')
    print(f'{len(trocas)} trocas em {len(ficheiros)} ficheiros')


if __name__ == '__main__':
    main()
