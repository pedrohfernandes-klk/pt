"""12/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M8. Camada literal cuidado_m8_20261112
(scripts/cuidado_m8_20261112.json, gerada por scripts/cuidado_m8_20261112.py; manifesto tests/fixtures/cuidado-m8-edits-20261112.json),
a mais recente, por cima da decisão 152 no M7 (cuidado_m7_20261111).

Este teste confere, no modelo de tests/test_cuidado_m1.py a tests/test_cuidado_m7.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices, o gerador do desenho comum dos índices e a leitura
  histórica das tarefas (scripts/tarefas_claras_historico.py);
* cada um dos 36 achados confirmados que entram: as 8 tabelas novas (8 achados A), com o cabeçalho (th scope=col), a primeira
  coluna (th scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato, no
  cartão e no sítio certos; os 6 casos do mesmo tipo (C), com o texto exato; os 22 achados B, com a contagem certa de cada par da
  proposta final (com a palavra inteira e fora das cadeias maiores dos outros pares) e a forma da proposta, sem nenhuma ocorrência
  que se parta fora do que fica de fora (o «alt», o data-titulo dos vídeos, a casca das lições, que fica para o molde, e o
  título que o script do índice guarda);
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e mais nenhuma do M8;
* que os 6 achados dos diapositivos, das provas rápidas, dos questionários e da página «todos» (20 e 43 a 47) ficam de fora, como
  do M1 ao M7, que os 2 dos painéis da F03 e da F10 (38 e 39), só com ocorrências no material do relâmpago, também, e que nenhum
  dos 7 achados recusados (9, 10, 13, 16, 17, 19 e 29) entrou;
* as regras do texto: as tabelas e as listas só usam texto que já estava na página (e os cabeçalhos); nada de «professor», «jogar»,
  «jogo», «ficha», «folha», «—» ou «·» novos; nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>,
  data-titulo, chaves JSON, nem da «frase» de um sublinhar, das «palavras» de um cartão frase ou dos «passos» de um ordenar; nas
  passagens mudadas, nenhuma referência nem número que se parta; a única letra que muda é «Séc. XX», que passa a «século XX» no
  rótulo do guia (a proposta final, como no guia do M5);
* que as tarefas da M8-U1 e da M8-U2 saem iguais dos dados e do gerador (e as dos outros módulos não mudam), que as lições geradas
  (F13 a F16) e as suas notas saem iguais das fontes, que o painel do docente da F11 segue o enunciado da lição (com o material do
  relâmpago como estava) e que as cópias do banco das provas rápidas seguem os cartões."""
from html.parser import HTMLParser
from pathlib import Path
import glob
import hashlib
import html
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from auditoria_20261028 import undo_cuidado_m8_1112, undo_cuidado_m7_1111  # noqa: E402
# 12/11/2026: por cima desta camada fica a decisão 152 no M9 (camada cuidado_m9_20261112).
from auditoria_20261028 import undo_cuidado_m9_1112  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m8_20261112.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m8-edits-20261112.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
# As camadas de baixo com que esta se cruza nos testes: a decisão 152 no M7 e a revisão dos enunciados das tarefas (#192).
M7 = json.loads((ROOT / 'tests/fixtures/cuidado-m7-edits-20261111.json').read_text('utf-8'))
CLARAS = json.loads((ROOT / 'tests/fixtures/tarefas-claras-edits-20261110.json').read_text('utf-8'))['files']
# A camada assenta no ramo da decisão 152 no M7 (pedido #194), já com o main a7a16f2d dentro.
# 12/11/2026: o M7 foi publicado no main em 40f9505c (#194), com a mesma árvore de 399a9ce3; a base passa a ser esse commit do main, sem mudar resumos nem trocas.
BASE_COMMIT = '40f9505c53c6125cf3faa9d219a965d22c42bd27'
NBSP, WJ = '\xa0', '⁠'
N = NBSP
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
A = {0, 1, 2, 3, 4, 5, 6, 8}
C_ = {7, 11, 12, 14, 15, 18}
# O achado B do painel de projeção da F11 (40) e os das outras páginas.
B_PAINEIS = {40}
B_PAGINAS = {21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 41, 42, 48, 49, 50}
# Ficam de fora, por decisão já tomada para todos os módulos (como do M1 ao M7): os diapositivos (20), as três provas rápidas
# (43, 44 e 45), os questionários (46) e a página «todos» (47). Confirmados pela conferência, mas essas páginas não mudam.
FORA_DE_AMBITO = {20: 'm8/diapositivos/index.html', 43: 'm8/prova-a/index.html', 44: 'm8/prova-b/index.html',
                  45: 'm8/prova-c/index.html', 46: 'm8/questionarios/index.html', 47: 'm8/todos/index.html'}
# E os dois painéis de projeção em que as ocorrências confirmadas estão todas no material do relâmpago (MATERIAL), que não muda.
SO_MATERIAL = {38: 'm8/painel-m8-f03/index.html', 39: 'm8/painel-m8-f10/index.html'}
B = B_PAINEIS | B_PAGINAS | set(FORA_DE_AMBITO) | set(SO_MATERIAL)
CONFIRMADOS = A | B | C_
APLICADOS = CONFIRMADOS - set(FORA_DE_AMBITO) - set(SO_MATERIAL)
RECUSADOS = {9, 10, 13, 16, 17, 19, 29}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)
INDICE, GUIA, MAPA = 'm8/index.html', 'm8/guia-da-tarefa-m8/index.html', 'm8/mapa-do-modulo-m8/index.html'
F04, F05, F08, F11, F13, F15 = (f'm8/licao-m8-{n}/index.html' for n in ('f04', 'f05', 'f08', 'f11', 'f13', 'f15'))
ASPETO, OPINIAO, ANAFORA = 'm8/gramatica-aspeto/index.html', 'm8/opiniao-ramos/index.html', 'm8/anafora-catafora/index.html'
PORTEFOLIO = 'm8/portefolio-do-modulo-m8/index.html'
GERADAS = ('m8-f13', 'm8-f14', 'm8-f15', 'm8-f16')

PESOS = [['Tarefa da Unidade 1', '30' + N + '%'], ['Tarefa da Unidade 2', '30' + N + '%'], ['Provas rápidas', '10' + N + '%'],
         ['Prova escrita', '30' + N + '%']]
LARGURAS = ['width:auto', 'width:5.5rem']
# (página, índice da tabela nova na página, cabeçalho, linhas, larguras): o texto de cada célula, como se lê.
TABELAS = [
    # achados 0, 1 e 2: os pesos no índice, no guia e no mapa do módulo, com a coluna do peso estreita (como no M5 e no M7)
    (INDICE, 0, ['Elemento', 'Peso'], PESOS, LARGURAS),
    (GUIA, 0, ['Elemento', 'Peso'], PESOS, LARGURAS),
    (MAPA, 0, ['Elemento', 'Peso'], PESOS, LARGURAS),
    # achado 3, F04, «Para entender», dobra «Recorda»
    (F04, 0, ['Noção', 'O que é'],
     [['Arte poética', 'o poema que fala da própria poesia'],
      ['Comparação', 'aproxima elementos por uma relação explícita, como acontece com «como» nesta abertura'],
      ['Metáfora', 'constrói uma identificação figurada; a ausência de «como» não basta para a reconhecer'],
      ['Interrogação retórica', 'pergunta que não espera resposta']], None),
    # achado 4, F05, «Para entender», dobra «Recorda»
    (F05, 0, ['Noção', 'O que é'],
     [['Tradição literária', 'o que o poema vai buscar a textos antigos. Aqui, a forma da prece e a história dos pães e dos peixes, '
       'dos Evangelhos'],
      ['Apóstrofe', 'chamar alguém («Senhor»)'],
      ['Ironia', 'o contexto leva a entender uma distância crítica em relação ao que se diz literalmente; nem todo o sentido indireto '
       'é irónico']], None),
    # achado 5, F08, «Para entender», caixa «Recorda»
    (F08, 0, ['Noção', 'O que é'],
     [['Unidade de ação', 'uma só linha de acontecimentos'], ['Concentração de tempo e de espaço', 'pouco tempo, poucos lugares'],
      ['Discurso direto', 'as palavras da personagem, com travessão ou aspas'],
      ['Discurso indireto', 'o narrador conta o que foi dito']], None),
    # achado 6, F15 (lição gerada), «O essencial»
    (F15, 0, ['Termo', 'O que é'],
     [['Autora', 'pessoa real que escreve'], ['Voz poética', 'instância construída no poema'],
      ['Reportagem', 'seleção jornalística de informações, declarações e imagens']], None),
    # achado 8, «Fechou, fechava, foi fechando», passo 1 («A ideia»): três colunas
    (ASPETO, 0, ['Valor', 'Exemplo', 'O que mostra'],
     [['Perfetivo', '«Ontem li o conto até ao fim»', 'apresenta uma leitura concluída'],
      ['Imperfetivo', '«Eu lia o conto quando ouvi o carro»', 'mostra a leitura em curso; não diz se parei ou se cheguei ao fim'],
      ['Habitual', '«Costumava reler o conto aos domingos»', 'apresenta um costume'],
      ['Iterativo', '«Naquela revisão, reli o verso várias vezes»', 'apresenta repetição num episódio, sem exigir contagem exata']], None),
]
# Onde está cada tabela nas lições: (página, tabela) > (índice do cartão, rótulo do cartão, o que fica por cima, o que fica a seguir).
LUGARES = {
    (F04, 0): (6, 'Para entender', '<details><summary>Recorda</summary><div><table class="apoio-tabela" role="table">',
               '</table></div></details><div class="painel corte-modelo">'),
    (F05, 0): (6, 'Para entender', '<details><summary>Recorda</summary><div><table class="apoio-tabela" role="table">',
               '</table><p><small>Consulta: <a href="https://dt.dge.mec.pt/index.php?id=n522" target="_blank" rel="noopener">Dicionário '
               'Terminológico, ironia'),
    (F08, 0): (4, 'Para entender', '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela" role="table">',
               '</table><p>No conto, a protagonista tem três nomes, um para cada idade: Gi, George, Georgina.</p></div>'),
    (F15, 0): (2, 'O essencial', '<table class="apoio-tabela" role="table">',
               '</table><p>Uma reportagem pode documentar uma declaração da autora.'),
}
# Nenhuma página do M8 tinha tabelas de apoio antes desta camada.
JA_TINHAM = {}

# O que a proposta final conta, par a par («antes»: as ocorrências que mudam, com a palavra inteira e fora das cadeias maiores),
# tal como está em bordo/cidadania-v3/cuidado-152/m8-confirmados.json (os pares com contexto, juntos pelo par que prendem).
FUZ, GOYA = '3 de maio de 1808', '3 de Maio de 1808'
PROPOSTA = {
    21: {'90 minutos': 1, '30 %': 2, '10 minutos': 1, '5 minutos': 1, '10 min': 1, '5 min': 1, '60 min': 1, '15 min': 1, '3.º ano': 2},
    22: {'90 minutos': 3, '30 %': 2, '90 min': 4, '25 min': 2, '10 min': 2, '30 segundos': 4, '5 a 7 minutos': 3, '90 segundos': 4,
         '3.º ano': 2, 'século XX': 3, 'número 1760': 1, GOYA: 2, FUZ: 1, '3 de Maio': 2, 'M8-F03': 1},
    23: {'3 min': 1, 'século XIX': 1, FUZ: 1, '1872–1921': 1},
    24: {'2 min': 1, '4 min': 1, 'p. 5': 1, 'pp. 52–53': 1, FUZ: 1, GOYA: 3},
    25: {'3 min': 1, FUZ: 1},
    26: {'n.º 1760': 1, 'n.º 0': 1, 'pp. 14–15': 1, 'página 15': 1, FUZ: 1, '7 de agosto de 2023': 1, '1956–2022': 1},
    27: {FUZ: 1},
    28: {'1921–1998': 2},
    30: {'5 a 7 minutos': 4, '30 s': 1, '90 segundos': 4, '30 segundos': 3, FUZ: 1, GOYA: 1, '3 de Maio': 2, 'M8-F03': 2},
    31: {'século XX': 6},
    32: {'n.º 0': 1, 'pp. 14–15': 1, '27 de setembro de 2013': 1},
    33: {'12.º ano': 1, 'página 1': 1},
    34: {'25 min': 1},
    35: {'25 min': 1, 'n.º 1760': 2, 'versos 1 e 2': 2, 'verso 1': 1, FUZ: 1},
    36: {'90 minutos': 2, '30 %': 2, '3.º ano': 2, 'século XX': 3, 'verso 1': 1, FUZ: 2, '1923–2005': 1, '1921–1998': 1, 'M8-F01': 1,
         'M8-F08': 3, 'M8-F03': 1},
    37: {'século XVI': 1, 'ato III': 1},
    41: {'1923–2006': 1},
    42: {'90 minutos': 1, '40 %': 1, '3.º ano': 2, 'século XX': 1},
    48: {'3.º ano': 2},
    49: {'10 min': 1, '60 minutos': 1, '90 min': 1, '10 minutos': 1, 'n.º 0': 1, 'pp. 14–15': 1, '7 de agosto de 2023': 1},
    50: {'10 min': 1, '60 minutos': 1, '90 min': 1, '10 minutos': 1},
}
# O mesmo no painel de projeção da F11: (a forma da proposta, com {N} por U+00A0; as ocorrências que mudam, na lista CARTOES e
# no seletor; as que ficam, no material do relâmpago, MATERIAL).
PROPOSTA_PAINEIS = {40: {'século XX': ('século{N}XX', 2, 1)}}
PAINEL = {'m8/painel-m8-f11/index.html': 40}
# As trocas que não estão nos pares da proposta, com a razão: a meta descrição das tarefas muda com «nao_partir» (como do M1 ao
# M7), e «Séc. XX» passa a «século XX» no rótulo do guia (a proposta final, como no guia do M5).
META = 'durante 90 minutos, com entrega'
SEC = 'Poesia e Conto do Séc. XX'
EXTRAS = {21: {SEC}, 49: {META}, 50: {META}}
# O que a conferência deixou de fora e o detetor não conhece (o título que o script do índice guarda e a casca da F11): quantas
# ocorrências tem o par da proposta na página («bruto») para além das que mudam.
FORA = {22: {'TIT="Poesia e conto do século XX"': 1}, 31: {'Poesia e conto do século XX</a>': 1}}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a proposta pede U+00A0, traço de intervalo sem U+2060
# ou o hífen da sigla «M8-Fxx» sem a junção. As formas do M8: «p.» e «pp.», «n.º», «verso(s)», «século» (e «Séc.»), «ato»,
# «página» e «número» com o número, ordinal e nome, número e unidade (min, minutos, segundos, s, %), as datas (o dia preso ao
# «de» e o ano ao «de», como no M5 e no M7), os intervalos com traço e a sigla. Os intervalos «N a N» ficam como a proposta os
# deixou («5 a 7 minutos» só prende a unidade).
MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'
PARTE = re.compile(
    r'(?<![\w.])pp?\. (?=\d)'
    r'|n\.º (?=\d)'
    r'|\b(?:versos?|séculos?|ato|página|número) (?=(?:\d+|[IVXLC]+)\b)'
    r'|\bSéc\. (?=[IVXLC]+\b)'
    r'|\d\.[ºª] (?=ano\b)'
    r'|\b\d+ (?=(?:min|minutos|segundos|s|%)(?!\w))'
    r'|\b\d{1,2} de (?=(?i:' + MESES + r'))'
    r'|(?<=\d[ \xa0]de )(?i:' + MESES + r') de (?=\d{4}\b)'
    r'|\d–(?!⁠)\d|\bM8-(?!⁠)F\d')


def ler(rel):
    # 12/11/2026: por cima de todas as camadas ficam as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112), que
    # mudam os enunciados, as grelhas, as correções e os aquecimentos da M3-U1 e da M3-U2, os seus dados, e o guia, o índice e o mapa
    # do M3. Os testes desta camada leem cada ficheiro como ela o deixou: com a camada de cima desfeita pelo manifesto, com contagem
    # estrita (nos ficheiros que ela não muda, é o ficheiro da árvore). As exigências são as mesmas, letra a letra.
    from auditoria_20261028 import undo_tarefas_faceis_m3_1112
    return undo_tarefas_faceis_m3_1112(rel, (ROOT / rel).read_bytes().decode('utf-8'))


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def gerador():
    spec = importlib.util.spec_from_file_location('cuidado_m8_20261112', ROOT / 'scripts/cuidado_m8_20261112.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


C = gerador()


def cartoes(texto):
    """Os cartões de uma lição (ou a lista de um painel)."""
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0]


def banco(texto):
    """As cópias dos cartões no banco das provas rápidas do índice (var U)."""
    return [x for u in json.JSONDecoder().raw_decode(texto.split('var U=', 1)[1])[0] for x in u.get('pool', [])]


def visivel(fragmento):
    # O <wbr> (o ponto onde um nome do portefólio pode mudar de linha) não separa palavras.
    fragmento = fragmento.replace('<wbr>', '')
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragmento.replace('\\"', '"').replace('<\\/', '</').replace('\\n', '\n')))


def palavras(texto):
    return set(re.findall(r'[\wÀ-ÿ]+', visivel(texto).lower()))


def base(rel):
    """A página sem esta camada (desfeita pelo manifesto, com contagem estrita)."""
    return undo_cuidado_m8_1112(rel, ler(rel))


class Tabela(HTMLParser):
    def __init__(self, fonte):
        super().__init__()
        self.tabela, self.legenda, self.linhas, self.atual, self.grupos = None, None, [], None, []
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'table':
            self.tabela = a
        elif tag == 'caption':
            self.legenda = ''
        elif tag in ('thead', 'tbody', 'tfoot'):
            self.grupos.append((tag, a))
        elif tag == 'tr':
            self.linhas.append({'attrs': a, 'grupo': self.grupos[-1][0], 'celulas': []})
        elif tag in ('th', 'td'):
            self.atual = {'tag': tag, 'attrs': a, 'texto': ''}
            self.linhas[-1]['celulas'].append(self.atual)

    def handle_data(self, data):
        if self.atual is not None:
            self.atual['texto'] += data

    def handle_endtag(self, tag):
        if tag in ('th', 'td'):
            self.atual = None


def tabelas_da_pagina(texto):
    out = []
    # Nas lições geradas (scripts/gerar_licoes_20261101.py), os fechos vão como «<\/» no JSON dos cartões.
    texto = texto.replace('<\\/', '</')
    for m in re.finditer(r'<table class=\\?"apoio-tabela\b', texto):
        fim = texto.index('</table>', m.start()) + len('</table>')
        out.append(texto[m.start():fim].replace('\\"', '"'))
    return out


def tabelas_novas(rel):
    """As tabelas de apoio que esta camada pôs na página (as que não estavam na base), pela ordem da página."""
    antes = tabelas_da_pagina(base(rel))
    return [t for t in tabelas_da_pagina(ler(rel)) if t.replace(N, ' ') not in [a.replace(N, ' ') for a in antes]]


def paginas_do_m8():
    return [Path(p).relative_to(ROOT).as_posix() for p in sorted(glob.glob(str(ROOT / 'm8/**/index.html'), recursive=True))
            + sorted(glob.glob(str(ROOT / 'tarefas/m8-*/**/index.html'), recursive=True))]


def contextos_proibidos(texto):
    """Os pedaços onde não pode entrar U+00A0 nem U+2060: alt, aria-label, href, title e data-titulo, <title>, as chaves JSON e
    a «frase» de um sublinhar, as «palavras» de um cartão frase e os «passos» de um ordenar."""
    out = [m.group(2) for m in re.finditer(r'\b(alt|aria-label|href|title|data-titulo)=\\?"((?:(?!\\?").)*)', texto)]
    out += re.findall(r'<title>(.*?)</title>', texto, re.S)
    out += re.findall(r'"((?:[^"\\]|\\.)*)"\s*:', texto)
    for tipo, campo in (('sublinhar', 'frase'), ('frase', 'palavras'), ('ordenar', 'passos')):
        for m in re.finditer(r'"t":\s*"%s"' % tipo, texto):
            f = re.compile(r'"%s":\s*("(?:[^"\\]|\\.)*"|\[(?:[^\]"]|"(?:[^"\\]|\\.)*")*\])' % campo).search(texto, m.end())
            if f:
                out.append(f.group(1))
    return out


def ac_aplicadas(rel, texto):
    """O texto com só as trocas A e C desta camada (e a folha das tabelas) aplicadas por cima da base."""
    for t in TROCAS:
        if t['ficheiro'] == rel and '(B)' not in t['achado']:
            texto = texto.replace(t['antigo'], t['novo'])
    return texto


def sem_atributos_nem_desenhos(texto):
    """O texto sem os atributos e o <title> que ficam de fora e sem os desenhos (SVG): o que se vê e pode mudar de linha."""
    texto = texto.replace('\\"', '"').replace('<\\/', '</')
    texto = re.sub(r'<svg\b.*?</svg>', ' ', texto, flags=re.S)
    texto = re.sub(r'\b(?:alt|aria-label|href|title|content|data-titulo)="[^"]*"', '', texto)
    return re.sub(r'<title>.*?</title>', ' ', texto, flags=re.S)


def pares_da_pagina(rel):
    """Todos os pares B da página (de todos os seus achados): uma ocorrência dentro de uma cadeia maior conta para a maior."""
    return [p for x in C.ACHADOS_B if x['ficheiro'] == rel for p in x['pares']]


def achados_da_troca(t):
    return [int(n) for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])]


def inteiras(texto, seq, a=0, b=None):
    """As posições de seq em texto[a:b] com a palavra inteira («poema I» não conta dentro de «poema II»)."""
    b = len(texto) if b is None else b
    return [m.start() for m in re.finditer(re.escape(seq), texto) if a <= m.start() and m.end() <= b
            and C._palavra_inteira(texto, m.start(), m.end(), seq)]


class CuidadoM8(unittest.TestCase):
    def test_oito_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 8)
        for rel, k, cabecalho, linhas, larguras in TABELAS:
            t = Tabela(tabelas_novas(rel)[k])
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(t.tabela.get('class'), 'apoio-tabela')
                self.assertEqual(t.tabela.get('role'), 'table')
                # Sem <caption>: o título da dobra, da caixa, do cartão ou o parágrafo dos pesos já a nomeia.
                self.assertIsNone(t.legenda)
                self.assertEqual([g for g, _ in t.grupos], ['thead', 'tbody'])
                self.assertTrue(all(a.get('role') == 'rowgroup' for _, a in t.grupos))
                topo, corpo = t.linhas[0], t.linhas[1:]
                self.assertEqual(topo['grupo'], 'thead')
                self.assertEqual([c['texto'] for c in topo['celulas']], cabecalho)
                for c in topo['celulas']:
                    self.assertEqual((c['tag'], c['attrs'].get('scope'), c['attrs'].get('role')), ('th', 'col', 'columnheader'))
                self.assertEqual([[c['texto'] for c in l['celulas']] for l in corpo], linhas)
                for linha in t.linhas:
                    self.assertEqual(linha['attrs'].get('role'), 'row')
                for linha in corpo:
                    self.assertEqual(linha['grupo'], 'tbody')
                    primeira, resto = linha['celulas'][0], linha['celulas'][1:]
                    self.assertEqual((primeira['tag'], primeira['attrs'].get('scope'), primeira['attrs'].get('role')), ('th', 'row', 'rowheader'))
                    self.assertEqual(len(linha['celulas']), len(cabecalho))
                    for coluna, c in enumerate(resto, 1):
                        self.assertEqual((c['tag'], c['attrs'].get('role'), c['attrs'].get('data-label')), ('td', 'cell', cabecalho[coluna]))
                # Só as dos pesos têm larguras: a coluna do peso só leva o número (5,5 rem), como no M5 e no M7.
                self.assertEqual([c['attrs'].get('style') for c in topo['celulas']], larguras or [None] * len(cabecalho))
        # Nenhuma página do M8 (nem as suas tarefas, aquecimentos, grelhas e correções) tem mais tabelas de apoio novas do que
        # estas; antes desta camada não havia nenhuma.
        contagem = {}
        for rel, *_ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        for rel in paginas_do_m8():
            with self.subTest(pagina=rel):
                self.assertEqual(len(tabelas_da_pagina(ler(rel))), contagem.get(rel, 0) + JA_TINHAM.get(rel, 0))
                self.assertEqual(len(tabelas_da_pagina(base(rel))), JA_TINHAM.get(rel, 0))
                self.assertEqual(len(tabelas_novas(rel)), contagem.get(rel, 0))

    def test_tabelas_nos_cartoes_e_nos_sitios_certos(self):
        for (rel, k), (indice, rot, antes, depois) in LUGARES.items():
            cards = cartoes(ler(rel))
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(cards[indice]['t'], 'ler')
                self.assertEqual(cards[indice]['rot'], rot)
                self.assertIn(antes, cards[indice]['html'])
                self.assertIn(depois, cards[indice]['html'])
                self.assertEqual(cards[indice]['html'].count('<table class="apoio-tabela"'), 1)
        # Em cada lição, só os cartões com tabela nova a têm.
        for rel in sorted({r for r, _ in LUGARES}):
            esperados = sorted(i for (r, _), (i, *_) in LUGARES.items() if r == rel)
            self.assertEqual([i for i, c in enumerate(cartoes(ler(rel))) if 'apoio-tabela' in c.get('html', '')], esperados, rel)
        # Nas caixas «Recorda» da F04, da F05 e da F08, as noções já não vêm em negrito num parágrafo; a frase dos três nomes da
        # F08 fica num parágrafo a seguir, e a «frase» do cartão de sublinhar que a repete fica como estava.
        for rel, k, primeira in ((F04, 6, 'Arte poética'), (F05, 6, 'Tradição literária'), (F08, 4, 'Unidade de ação')):
            caixa = cartoes(ler(rel))[k]['html']
            self.assertNotIn(f'<b>{primeira}</b>:', caixa)
            self.assertIn(f'<th scope="row" role="rowheader">{primeira}</th>', caixa)
            self.assertIn(f'<b>{primeira}</b>:', cartoes(base(rel))[k]['html'])
        f08 = cartoes(ler(F08))
        self.assertEqual([c['frase'] for c in f08 if c['t'] == 'sublinhar'], [c['frase'] for c in cartoes(base(F08)) if c['t'] == 'sublinhar'])
        # Na F15, os retornos continuam a mandar reler as definições, que agora estão na tabela do «O essencial».
        f15 = cartoes(ler(F15))
        self.assertNotIn('<strong>Autora:</strong>', f15[2]['html'])
        self.assertTrue(f15[2]['html'].startswith('<table class="apoio-tabela" role="table">'))
        # No índice, no guia e no mapa, a tabela dos pesos fica entre o rótulo e a frase da grelha, que continua no seu parágrafo.
        resto = '</table><p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20. Na primeira recuperação, fazes a tarefa da unidade em falta, com a mesma grelha /20.</p>'
        for rel, rotulo, antes in ((INDICE, 'Pesos na avaliação', 'A avaliação é feita pelo docente.'),
                                   (GUIA, 'Avaliação', '<h1>Tarefas das unidades</h1>'), (MAPA, 'Avaliação', 'grelha /20.</span></p>')):
            texto = ler(rel)
            with self.subTest(pesos=rel):
                self.assertEqual(texto.count(f'{antes}<p>{rotulo}:</p><table class="apoio-tabela" role="table">'), 1)
                self.assertEqual(texto.count(resto), 1)
                self.assertEqual(texto.count('class="avaliacao-tarefas"'), 1)
                self.assertNotIn(f'{rotulo}: tarefa da Unidade 1', texto)
                self.assertIn(f'<p class="avaliacao-tarefas">{rotulo}: tarefa da Unidade 1, 30 %; tarefa da Unidade 2, 30 %; provas rápidas, '
                              '10 %; prova escrita, 30 %. Cada tarefa tem uma grelha /20.', base(rel))
        # O banco das provas rápidas não leva tabelas.
        self.assertNotIn('apoio-tabela', ler(INDICE).split('var U=', 1)[1])
        # Em «Fechou, fechava, foi fechando», a tabela fica no passo «A ideia», entre a frase de abertura e a dos valores que coexistem.
        aspeto = ler(ASPETO)
        self.assertEqual(aspeto.count('e não apenas quando acontece.</p><table class=\\"apoio-tabela\\" role=\\"table\\">'), 1)
        self.assertEqual(aspeto.count('</table><p>Os valores podem coexistir:'), 1)
        self.assertNotIn('<b>Perfetivo:</b>', aspeto)

    def test_folha_das_tabelas_antes_da_aparencia(self):
        com_tabela = sorted({r for r, *_ in TABELAS})
        self.assertEqual(com_tabela, sorted(C.COM_TABELA))
        for rel in com_tabela:
            cabeca = ler(rel).split('</head>')[0]
            with self.subTest(pagina=rel):
                self.assertEqual(cabeca.count(FOLHA), 1)
                self.assertEqual(cabeca.count('apoios-tabelas.css'), 1)
                self.assertLess(cabeca.index(FOLHA), cabeca.index('assets/appearance.css'))
                self.assertNotIn('apoios-tabelas.css', base(rel))
        # As outras páginas do M8 ficam como estavam: nenhuma carregava a folha, e continuam sem ela.
        for rel in paginas_do_m8():
            if rel not in com_tabela:
                with self.subTest(pagina=rel):
                    self.assertEqual(ler(rel).count('apoios-tabelas.css'), 1 if rel in JA_TINHAM else 0)
                    self.assertEqual(ler(rel).count('apoios-tabelas.css'), base(rel).count('apoios-tabelas.css'))
        # A folha é a do M1 e não muda: as regras das lições (.jogo .ler) e as de fora das lições já lá estão.
        css = ler('assets/pt-lessons/apoios-tabelas.css')
        self.assertIn('.jogo .ler .apoio-tabela td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertIn('.apoio-tabela:not(.jogo .ler .apoio-tabela) td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertNotIn('assets/pt-lessons/apoios-tabelas.css', {t['ficheiro'] for t in TROCAS})

    def test_casos_do_mesmo_tipo(self):
        # Achado 11: no guia, «Três antes de mim» numa lista ordenada (o mesmo trecho, letra a letra, dos guias do M5 e do M7).
        regra = ('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a '
                 'rubrica;</li><li>pergunta ao teu par de trabalho.</li></ol>Só depois levantas o braço.</div>')
        self.assertEqual(ler(GUIA).count(regra), 1)
        self.assertIn(regra, ler('m5/guia-da-tarefa-m5/index.html'))
        self.assertIn(regra, ler('m7/guia-da-tarefa-m7/index.html'))
        self.assertNotIn('1) relê o enunciado', ler(GUIA))
        # Achado 7: em «O texto de opinião, passo a passo», as quatro peças e os três «o que não é» em duas listas; o texto é o
        # mesmo, letra a letra: os itens, de seguida, dão o parágrafo de antes.
        opiniao = ('<p>Um <b>texto de opinião</b> defende uma ideia. Tem quatro peças:</p><ul><li>a <b>tese</b> (o que defendes, numa '
                   'frase);</li><li>um <b>argumento</b> com um <b>exemplo</b> concreto;</li><li>o <b>contra-argumento</b> (o que diz quem '
                   'discorda) e a tua resposta;</li><li>a <b>conclusão</b>, que volta à tese com uma palavra nova.</li></ul><p>O que não é '
                   'texto de opinião:</p><ul><li>descrever os dois lados sem escolher;</li><li>afirmar sem exemplo («toda a gente sabe '
                   'que…»);</li><li>fingir que ninguém discorda.</li></ul>')
        self.assertEqual(ler(OPINIAO).count('"rot":"Ler","html":"' + opiniao), 1)
        self.assertEqual(ler(OPINIAO).count('<ul>'), base(OPINIAO).count('<ul>') + 2)
        itens = re.findall(r'<li>(.*?)</li>', opiniao)
        self.assertEqual(len(itens), 7)
        self.assertEqual(base(OPINIAO).count('<p>Um <b>texto de opinião</b> defende uma ideia. Tem quatro peças: ' + ' '.join(itens[:4])
                                             + ' O que não é texto de opinião: ' + ' '.join(itens[4:]) + '</p>'), 1)
        # Achado 12: em «Apontar para trás, apontar para a frente», os três passos da ajuda em lista numerada e a frase final num
        # parágrafo; os números «1. 2. 3.» passam a ser os da lista.
        ajuda = ('<details><summary>Ajuda: como confirmar a direção?</summary><ol><li>Escolhe a expressão em análise.</li><li>Pergunta «a '
                 'que se refere?».</li><li>Localiza a resposta: antes, retoma; depois, antecipação.</li></ol><p>Se houver dois referentes '
                 'possíveis, explicita-os antes de decidir.</p>')
        self.assertEqual(ler(ANAFORA).count(ajuda), 1)
        passos = re.findall(r'<li>(.*?)</li>', ajuda)
        self.assertEqual(base(ANAFORA).count('<p>' + ' '.join(f'{n}. {p}' for n, p in enumerate(passos, 1))
                                             + ' Se houver dois referentes possíveis, explicita-os antes de decidir.</p>'), 1)
        # Achado 14: na F13 (gerada), o modelo de interpretação em lista numerada, cada passo com o rótulo a negrito e a frase que tinha.
        modelo = ('<ol><li><strong>Observação:</strong> a abertura aproxima palavras e desgaste.</li><li><strong>Relação:</strong> o que '
                  'era partilhado já não chega para sustentar o vínculo.</li><li><strong>Limite:</strong> isso não demonstra que a '
                  'linguagem seja inútil em todas as relações.</li></ol>')
        f13 = cartoes(ler(F13))
        self.assertEqual((f13[7]['rot'], f13[7]['titulo']), ('Para entender', 'Um modelo de interpretação'))
        self.assertTrue(f13[7]['html'].startswith(modelo + '<p>No poema completo,'))
        self.assertEqual(sum(modelo in c.get('html', '') for c in f13), 1)
        self.assertTrue(cartoes(base(F13))[7]['html'].startswith('<p>' + ' '.join(re.findall(r'<li>(.*?)</li>', modelo)) + '</p><p>No poema completo,'))
        # Achado 15: na F15 (gerada), as três formulações com letra em lista; o parágrafo seguinte continua a chamá-las pela letra.
        formulacoes = ('<p>Formulações criadas para esta lição.</p><ul><li>A: A página apresenta o livro como atento a desigualdades.</li>'
                       '<li>B: A autora afirmou esta frase.</li><li>C: A voz deste poema é necessariamente a autora.</li></ul>')
        f15 = cartoes(ler(F15))
        self.assertEqual((f15[12]['rot'], f15[12]['titulo']), ('Compara', 'Reconhecer uma atribuição'))
        self.assertTrue(f15[12]['html'].startswith(formulacoes + '<p>A exige conferir a apresentação.'))
        self.assertTrue(cartoes(base(F15))[12]['html'].startswith(
            '<p>Formulações criadas para esta lição. ' + ' '.join(re.findall(r'<li>(.*?)</li>', formulacoes)) + '</p><p>A exige conferir'))
        # Achado 18: no portefólio, os catorze nomes de ficheiro em <code> (os oito que estavam em texto simples e os seis que já
        # estavam), sem U+2011, U+2060 nem U+00A0 (o aluno copia-os); só mudam de linha a seguir a cada «_» (<wbr>), como nos
        # portefólios do M5 e do M7.
        port = ler(PORTEFOLIO)
        linhas = re.findall(r'<tr><td>(.*?)</td><td>', port)
        self.assertEqual(len(linhas), 14)
        self.assertTrue(all(re.fullmatch(r'<code>M8_[^<\u2011\u2060\xa0]*(?:<wbr>[^<\u2011\u2060\xa0]*)*</code>', l) for l in linhas), linhas)
        nomes = [f'M8_<wbr>U{u}_<wbr>{n}' for u in (1, 2) for n in ('registo_<wbr>&lt;dia-mês&gt;', 'retoma', 'o-que-aprendi', 'Tarefa')]
        self.assertEqual(len(nomes), 8)
        for nome in nomes + ['M8_<wbr>capa', 'M8_<wbr>cartao-do-percurso', 'M8_<wbr>Revisao1', 'M8_<wbr>Revisao2',
                             'M8_<wbr>Prova-escrita', 'M8_<wbr>balanco']:
            self.assertEqual(port.count(f'<td><code>{nome}</code></td>'), 1, nome)
        # Cada «_» de cada nome leva o seu <wbr>, e não há <wbr> em mais lado nenhum.
        self.assertTrue(all(l.count('_') == l.count('_<wbr>') for l in linhas))
        self.assertEqual(port.count('<wbr>'), sum(l.count('_') for l in linhas))
        self.assertEqual(port.count('<wbr>'), 6 * 2 + 2 * 3 + 6)
        # Os nomes são os mesmos, letra a letra, pela mesma ordem: sem as marcas, a primeira coluna é a de antes.
        limpa = lambda s: re.sub(r'</?code>|<wbr>', '', s)
        self.assertEqual([limpa(l) for l in linhas], [limpa(l) for l in re.findall(r'<tr><td>(.*?)</td><td>', base(PORTEFOLIO))])
        self.assertIn('code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
                      'td code{white-space:nowrap}\n', port)
        self.assertEqual(port.count('td code{white-space:nowrap}'), 1)
        self.assertIn('td code{white-space:nowrap}', ler('m5/portefolio-do-modulo-m5/index.html'))
        self.assertIn('td code{white-space:nowrap}', ler('m7/portefolio-do-modulo-m7/index.html'))
        # A tabela do portefólio fica como estava (o cabeçalho e a segunda coluna não mudam).
        self.assertEqual(re.findall(r'<table><tr><th[^>]*>Nome do ficheiro</th><th>O que é</th></tr>', port),
                         re.findall(r'<table><tr><th[^>]*>Nome do ficheiro</th><th>O que é</th></tr>', base(PORTEFOLIO)))
        self.assertEqual(len(re.findall(r'<table><tr><th[^>]*>Nome do ficheiro</th><th>O que é</th></tr>', port)), 1)
        self.assertEqual(re.findall(r'</td><td>(.*?)</td></tr>', port), re.findall(r'</td><td>(.*?)</td></tr>', base(PORTEFOLIO)))

    def test_achados_b_com_a_contagem_certa(self):
        self.assertEqual(sorted({x['i'] for x in C.ACHADOS_B}), sorted(B_PAGINAS))
        self.assertEqual(sorted(PROPOSTA), sorted(B_PAGINAS))
        self.assertEqual(len(C.ACHADOS_B), len(B_PAGINAS))
        vistos = 0
        for x in C.ACHADOS_B:
            rel, i = x['ficheiro'], x['i']
            prop = PROPOSTA[i]
            de = x.get('de', {})
            mudam = {}
            for p in x['pares']:
                mudam[de.get(p[0], p[0])] = mudam.get(de.get(p[0], p[0]), 0) + p[2]
            refeitos = {s: n for s, (n, _) in x.get('refeitos', {}).items()}
            literais = {a: n for a, _, _, n in x.get('literais', [])}
            # Cada par da proposta está no achado: muda (às vezes com o contexto que o distingue do que fica de fora) ou já foi
            # refeito por um achado A com o espaço preso; as trocas literais são as de EXTRAS, com a razão.
            self.assertTrue(all(razao for _, _, razao, _ in x.get('literais', [])), i)
            self.assertEqual(set(prop), set(mudam) | set(refeitos), i)
            self.assertEqual(set(literais), EXTRAS.get(i, set()), i)
            self.assertEqual(C.proposta(x), {**prop, **literais}, i)
            for seq, n in prop.items():
                with self.subTest(achado=i, trecho=seq):
                    self.assertEqual(mudam.get(seq, 0) + refeitos.get(seq, 0), n)
            # Um par com contexto é o par da proposta com texto à volta; o que fica de fora diz porquê.
            for contexto, par in de.items():
                self.assertIn(par, contexto)
                self.assertIn(par, prop)
            self.assertEqual({s: n for s, (n, _) in x.get('fora', {}).items()}, FORA.get(i, {}), i)
            for seq, (_, razao) in list(x.get('fora', {}).items()) + list(x.get('refeitos', {}).items()):
                self.assertTrue(razao, seq)
            pre, final = ac_aplicadas(rel, base(rel)), ler(rel)
            todos = pares_da_pagina(rel)
            for antigo, novo, n in x['pares']:
                with self.subTest(achado=i, trecho=antigo):
                    # Antes, cada par aparece (fora do que fica de fora e das cadeias maiores) exatamente as vezes do achado;
                    # depois, nenhuma ocorrência se parte, e a forma da proposta final está lá.
                    self.assertEqual(len(C.ocorrencias(pre, antigo, novo, todos)), n)
                    self.assertEqual(C.ocorrencias(final, antigo, novo, todos), [])
                    self.assertGreaterEqual(final.count(C.j(novo)), n)
                    self.assertEqual(C.j(novo).replace(N, ' ').replace(WJ, ''), antigo)
                    vistos += 1
            # O que a conferência deixou de fora fica como estava, as mesmas vezes; o que um achado A refez está lá com o espaço
            # que não quebra.
            for seq, (n, _) in x.get('fora', {}).items():
                with self.subTest(achado=i, fora=seq):
                    self.assertEqual(final.count(seq), n)
                    self.assertEqual(base(rel).count(seq), n)
            for seq, (n, _) in x.get('refeitos', {}).items():
                with self.subTest(achado=i, refeito=seq):
                    self.assertEqual(len(inteiras(final, seq.replace(' ', N))), n)
                    self.assertEqual(inteiras(final, seq), [])
            for antigo, novo, _, n in x.get('literais', []):
                with self.subTest(achado=i, literal=antigo):
                    self.assertEqual(base(rel).count(antigo), n)
                    self.assertEqual(final.count(C.j(novo)), n)
        self.assertEqual(vistos, sum(len(x['pares']) for x in C.ACHADOS_B))
        # A casca das lições (migalhas, «Estás em», título escondido e sigla do rodapé) fica para o molde, como do M1 ao M7.
        self.assertEqual(len(C.CASCA_NO_MOLDE), 10)
        self.assertEqual(C.CASCA_NO_MOLDE, sorted(Path(p).relative_to(ROOT).as_posix() for p in glob.glob(str(ROOT / 'm8/licao-*/index.html'))
                                                  if not re.search(r'licao-m8-f(?:09|12|13|15)/', p)))
        for rel in sorted(Path(p).relative_to(ROOT).as_posix() for p in glob.glob(str(ROOT / 'm8/licao-*/index.html'))):
            texto = ler(rel)
            n = re.search(r'licao-m8-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                # As lições geradas (F13 a F16) têm outra casca, sem a migalha do ano.
                if n.lower() not in [g.split('-')[1] for g in GERADAS]:
                    self.assertEqual(texto.count('/pt/3/">3.º ano</a>'), 1)
                    self.assertEqual(texto.count('>Módulo 8: Poesia e conto do século XX</a>'), 1)
                    self.assertGreaterEqual(texto.count(f'Lição M8-{n}'), 2)
                self.assertEqual(texto.count('3.º' + N + 'ano'), 0)
                self.assertNotIn(f'M8-{WJ}{n}', texto)
                self.assertEqual(texto.count(f'Lição M8-{n}'), base(rel).count(f'Lição M8-{n}'))
        # Nas outras páginas, as migalhas contam (como na proposta final): o «3.º ano» fica preso nas migalhas e no cabeçalho.
        for rel, cab in ((INDICE, 'Português, 3.º' + N + 'ano, percurso do módulo'), (GUIA, 'Guia da tarefa, 3.º' + N + 'ano'),
                         (MAPA, 'Português · 3.º' + N + 'ano · Mapa do módulo'), (PORTEFOLIO, 'Português · 3.º' + N + 'ano · Módulo 8'),
                         ('m8/visita-caderno-de-campo/index.html', 'Caderno de campo, 3.º' + N + 'ano')):
            self.assertIn('/pt/3/">3.º' + N + 'ano</a>', ler(rel), rel)
            self.assertIn(cab, ler(rel), rel)
            self.assertNotIn('3.º ano', sem_atributos_nem_desenhos(ler(rel)), rel)
        # Os intervalos com traço levam a junção; a sigla das ligações do mapa também (os href, em minúsculas, ficam).
        mapa = ler(MAPA)
        self.assertEqual(len(re.findall(r'>[Ll]ição M8-' + WJ + r'F\d\d<', mapa)), 5)
        self.assertNotRegex(mapa, r'>[Ll]ição M8-F\d\d<')
        self.assertIn('licao-m8-f01/">Lição M8-' + WJ + 'F01</a>', mapa)
        self.assertIn('Eugénio de Andrade (1923–' + WJ + '2005)', mapa)
        self.assertIn('Maria Judite de Carvalho (Lisboa, 1921–' + WJ + '1998)', mapa)
        self.assertEqual(ler(F08).count('1921–' + WJ + '1998'), 2)
        self.assertNotIn('1921–1998', ler(F08))
        self.assertIn('Mário Cesariny (Lisboa, 1923–' + WJ + '2006)', ler('m8/pastelaria/index.html'))
        self.assertIn('pp.' + N + '52–' + WJ + '53', ler('m8/licao-m8-f03/index.html'))
        # O que a conferência tirou fica como estava: os traços entre ano e lugar e a legenda já presa do mapa, «nota 2», «Bloco
        # 27», o «séc. XX» da casca de «Pastelaria» e o «D. João» de «O texto de opinião» (o M5 só prendeu «D.» com numeral).
        for trecho in ('1919–Califórnia', '1956–Porto', '<span class="nb">'):
            self.assertEqual(mapa.count(trecho), base(MAPA).count(trecho), trecho)
            self.assertIn(trecho, mapa)
        self.assertIn('p.' + N + '5, nota 2, remetendo', ler('m8/licao-m8-f03/index.html'))
        self.assertIn('12.º' + N + 'ano, Bloco 27.', ler('m8/licao-m8-f16/index.html'))
        self.assertIn('séc. XX', ler('m8/pastelaria/index.html'))
        self.assertEqual(ler('m8/pastelaria/index.html').count('séc. XX'), base('m8/pastelaria/index.html').count('séc. XX'))
        self.assertIn('D. João', ler(OPINIAO))
        self.assertNotIn('D.' + N, ler(OPINIAO))
        # «5 a 7 minutos» só prende a unidade, como na proposta.
        self.assertEqual(len(inteiras(ler('m8/licao-m8-f10/index.html'), '5 a 7' + N + 'minutos')), 4)
        self.assertNotIn('5' + N + 'a', ler('m8/licao-m8-f10/index.html'))
        # As datas com o dia preso ao «de» e o ano ao «de», como no M5 e no M7; «3 de Maio», sem ano, só prende o dia.
        f03 = ler('m8/licao-m8-f03/index.html')
        self.assertEqual(len(inteiras(f03, '3' + N + 'de Maio de' + N + '1808')), 3)
        self.assertEqual(len(inteiras(ler('m8/licao-m8-f10/index.html'), '3' + N + 'de Maio"')), 2)
        self.assertNotRegex(sem_atributos_nem_desenhos(mapa), r'\d de (?i:' + MESES + r') de \d{4}')
        # Os vídeos: o botão muda, o data-titulo (que vira o title do leitor) fica; nos «alt», os espaços ficam normais.
        self.assertEqual(f03.count('(2 min)'), 1)
        self.assertEqual(f03.count('(2' + N + 'min)</button>'), 1)
        self.assertRegex(f03, r'data-titulo=\\"[^"]*\(2 min\)\\"')
        for rel in ('m8/licao-m8-f01/index.html', 'm8/licao-m8-f03/index.html', 'm8/licao-m8-f06/index.html', 'm8/licao-m8-f10/index.html'):
            texto = ler(rel)
            self.assertRegex(texto, r'alt=\\"[^"]*3 de maio de 1808', rel)
            self.assertEqual(texto.count('<figcaption>Os fuzilamentos de 3' + N + 'de maio de' + N + '1808 (Francisco de Goya, 1814'), 1, rel)
        # «Séc. XX» passa a «século XX» só no rótulo do guia (a proposta final, como no guia do M5); o título que o script do
        # índice guarda e o <title> ficam como estavam.
        guia = ler(GUIA)
        self.assertEqual(guia.count('<p class="rot">Módulo 8: Poesia e Conto do século' + N + 'XX</p>'), 1)
        self.assertNotIn('Séc.', guia)
        self.assertEqual(base(GUIA).count('<p class="rot">Módulo 8: Poesia e Conto do Séc. XX</p>'), 1)
        self.assertIn('class="rot">Módulo 5: Narrativa do século' + N + 'XIX', ler('m5/guia-da-tarefa-m5/index.html'))
        indice = ler(INDICE)
        self.assertEqual(indice.count('TIT="Poesia e conto do século XX"'), 1)
        self.assertRegex(indice, r'<title>[^<]*século XX</title>')
        # As tarefas da M8-U1 e da M8-U2: os números do molde, pelo gerador (a ligação à grelha fica como estava).
        for u in (1, 2):
            t = ler(f'tarefas/m8-u{u}/index.html')
            self.assertIn('Antes de escrever · 10' + N + 'min · em cartões, com consulta', t)
            self.assertIn(f'Tarefa individual · Unidade {u} · 90' + N + 'min</p>', t)
            self.assertNotIn('90 min', t)
            self.assertRegex(t, r'<meta name="description" content="[^"]*durante 90' + N + 'minutos, com entrega')
            self.assertEqual(t.count('<p class="task-grelha">'), base(f'tarefas/m8-u{u}/index.html').count('<p class="task-grelha">'))

    def test_paineis_seguem_as_licoes(self):
        # Os painéis de projeção das lições do M8 mostram os enunciados dos cartões: onde um mudou, o painel muda igual, na lista
        # (CARTOES) e no seletor; é o achado do painel da F11 (40), e mais nenhum painel muda.
        paineis = sorted({t['ficheiro'] for t in TROCAS if '/painel-' in t['ficheiro']})
        self.assertEqual(paineis, sorted(PAINEL))
        self.assertEqual(C.PAINEIS, PAINEL)
        self.assertEqual(sorted(PROPOSTA_PAINEIS), sorted(B_PAINEIS))
        self.assertEqual(sorted(PAINEL.values()), sorted(B_PAINEIS))
        for rel in paineis:
            i = PAINEL[rel]
            antes, depois = base(rel), ler(rel)
            # O material do relâmpago (MATERIAL) segue a lição antes das camadas de cuidado (tests/test_sala_desligada.py): não muda.
            a, b = depois.index(',MATERIAL='), depois.index(',crono=')
            self.assertLess(a, b)
            self.assertEqual(antes.split(',MATERIAL=', 1)[1].split(',crono=')[0], depois[a + len(',MATERIAL='):b], rel)
            for t in TROCAS:
                if t['ficheiro'] == rel:
                    self.assertEqual(achados_da_troca(t), [i], t['local'])
                    self.assertIn('(painel de projeção)', t['local'])
                    self.assertTrue(t['antigo'].startswith(('{"k":', '<option value="')), t['local'])
                    self.assertEqual(t['novo'].replace(N, ' ').replace(WJ, ''), t['antigo'])
            # Cada par da proposta: as ocorrências que mudam estão na lista e no seletor; as do material ficam como estavam.
            for seq, (forma, n, material) in PROPOSTA_PAINEIS[i].items():
                presa = C.j(forma)
                self.assertEqual(presa.replace(N, ' ').replace(WJ, ''), seq)
                with self.subTest(painel=rel, trecho=seq):
                    self.assertEqual(len(inteiras(depois, presa)), n)
                    self.assertEqual(inteiras(depois, presa, a, b), [])
                    self.assertEqual(len(inteiras(depois, seq)), material)
                    self.assertEqual(len(inteiras(depois, seq, a, b)), material)
                    self.assertEqual(len(inteiras(antes, seq)), n + material)
        # Em todos os painéis de projeção do M8, cada enunciado da lista é o do cartão da lição (com ou sem os marcadores de
        # negrito e de itálico e com as lacunas como «…»), e o seletor mostra-o (inteiro ou cortado), com o itálico em <i>.
        conferidos = mudados = 0
        for p in sorted(glob.glob(str(ROOT / 'm8/painel-m8-*/index.html'))):
            rel = Path(p).relative_to(ROOT).as_posix()
            texto = ler(rel)
            if 'CARTOES=' not in texto:
                continue
            licao = cartoes(ler(rel.replace('/painel-', '/licao-')))
            antes = {x['k']: x for x in cartoes(base(rel))}
            for item in cartoes(texto):
                with self.subTest(painel=rel, k=item['k']):
                    self.assertIn(item['p'], [f(licao[item['k']]) for f in C.ENUNCIADOS])
                    opcao = re.search(r'<option value="%d">(.*?)</option>' % item['k'], texto).group(1)
                    opcao_antes = re.search(r'<option value="%d">(.*?)</option>' % item['k'], base(rel)).group(1)
                    # O seletor diz o mesmo que dizia, letra a letra (só os espaços presos mudam) e, onde o enunciado mudou,
                    # mostra-o (inteiro ou cortado no mesmo sítio), com o itálico em <i>.
                    self.assertEqual(opcao.replace(N, ' ').replace(WJ, ''), opcao_antes)
                    if item != antes[item['k']]:
                        formas = (html.escape(item['p'], quote=False),
                                  html.escape(re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', item['p']), quote=False),
                                  re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<i>\1</i>', html.escape(item['p'], quote=False)))
                        self.assertTrue(any(f.startswith(opcao) for f in formas), opcao)
                        self.assertEqual(item['p'].replace(N, ' ').replace(WJ, ''), antes[item['k']]['p'])
                        mudados += 1
                    conferidos += 1
            if rel not in PAINEL:
                self.assertEqual(texto, base(rel), rel)
                self.assertNotIn(rel, MANIFESTO['files'])
        self.assertGreater(conferidos, 150)
        # Cada enunciado mudado deu duas trocas no painel (a lista e o seletor), salvo onde o seletor corta o enunciado antes da
        # referência.
        trocas_paineis = sum('/painel-' in t['ficheiro'] for t in TROCAS)
        self.assertLessEqual(mudados, trocas_paineis)
        self.assertGreaterEqual(2 * mudados, trocas_paineis)
        self.assertEqual((mudados, trocas_paineis), (1, 2))
        # No painel da F11 muda só o enunciado do cartão 1 («A visita é a um lugar ligado à poesia ou ao conto do século XX.»).
        f11 = {x['k']: x['p'] for x in cartoes(ler('m8/painel-m8-f11/index.html'))}
        self.assertEqual([k for k, v in f11.items() if N in v], [k for k, v in f11.items() if 'século' in v])
        self.assertEqual(sum('século' + N + 'XX.' in v for v in f11.values()), 1)
        # Os painéis da F03 e da F10 (achados 38 e 39: só tinham ocorrências no material) ficam como estavam.
        for rel in SO_MATERIAL.values():
            self.assertNotIn(rel, MANIFESTO['files'])

    def test_banco_segue_as_licoes(self):
        # As cópias dos cartões no banco das provas rápidas do índice (var U) mudam como as lições de onde vêm: cada cópia que era
        # igual a um cartão da sua lição antes desta camada continua igual depois, campo a campo.
        copias, copias_antes = banco(ler(INDICE)), banco(base(INDICE))
        self.assertEqual(len(copias), len(copias_antes))
        iguais = 0
        for copia, antes in zip(copias, copias_antes):
            licao = f"m8/licao-{antes.get('_l')}/index.html"
            if not (ROOT / licao).is_file():
                continue
            L, L_antes = cartoes(ler(licao)), cartoes(base(licao))
            for c, c_antes in zip(L, L_antes):
                comuns = [k for k in ('p', 'o', 'c', 'f', 'fe', 'frase', 'v') if k in antes]
                if comuns and all(c_antes.get(k) == antes[k] for k in comuns):
                    with self.subTest(licao=licao, p=antes.get('p', '')[:40]):
                        self.assertEqual({k: copia[k] for k in comuns}, {k: c.get(k) for k in comuns})
                        iguais += 1
                    break
        self.assertGreater(iguais, 40)
        # Fora das páginas do M8, das suas tarefas e dos dados dos geradores, a camada não toca em nada (as sessões do Exame não
        # repetem nenhum trecho mudado: tests/test_exame_alignment.py continua a comparar as cópias com as lições, letra a letra).
        self.assertEqual(sorted(f for f in MANIFESTO['files'] if not f.startswith(('m8/', 'tarefas/m8-', 'docs/pedagogia/'))), [])
        self.assertEqual(C.NOTAS, [])

    def test_fora_de_ambito_e_recusados(self):
        achados = {n for t in TROCAS for n in achados_da_troca(t)}
        self.assertFalse(RECUSADOS & achados)
        self.assertFalse(set(FORA_DE_AMBITO) & achados)
        self.assertFalse(set(SO_MATERIAL) & achados)
        self.assertFalse(RECUSADOS & CONFIRMADOS)
        # 20 e 43 a 47: os diapositivos, as provas rápidas, os questionários e a página «todos» ficam de fora (como do M1 ao M7);
        # 38 e 39: os painéis da F03 e da F10, só com ocorrências no material do relâmpago, também. Nenhuma está na camada, nem no
        # gerador.
        for rel in sorted(FORA_DE_AMBITO.values()) + sorted(SO_MATERIAL.values()):
            with self.subTest(pagina=rel):
                self.assertTrue((ROOT / rel).is_file())
                self.assertNotIn(rel, MANIFESTO['files'])
                self.assertNotIn(rel, {x['ficheiro'] for x in C.ACHADOS_B + C.achados_ac()})
                self.assertNotIn(rel, C.PAINEIS)
                self.assertEqual(base(rel), ler(rel))
        # Nenhuma página de diapositivos, de provas rápidas, de questionários ou «todos», de módulo nenhum, está na camada.
        self.assertFalse([f for f in MANIFESTO['files'] if re.search(r'/(?:diapositivos|prova-[abc]|questionarios|todos)/', f)])
        # Nos painéis da F03 e da F10, as ocorrências confirmadas estão todas no material do relâmpago.
        for rel, trechos in ((SO_MATERIAL[38], ('3 de Maio de 1808',)), (SO_MATERIAL[39], ('5 a 7 minutos', '30 segundos', '90 segundos', '3 de Maio'))):
            texto = ler(rel)
            a, b = texto.index(',MATERIAL='), texto.index(',crono=')
            for trecho in trechos:
                posicoes = [m.start() for m in re.finditer(re.escape(trecho), texto)]
                self.assertTrue(posicoes, (rel, trecho))
                self.assertTrue(all(a < p < b for p in posicoes), (rel, trecho))
        # 9 e 10: as lentes da F09 e da F12 ficam em ol.ess-mini, sem tabela; 13, 16 e 17: sem listas de dois itens; 19: a ligação
        # do menu da atividade fica como estava; 29: a F09 e a F12 não estão na camada.
        for rel in ('m8/licao-m8-f09/index.html', 'm8/licao-m8-f12/index.html', 'm8/lentes-poema/index.html', 'm8/conto-perguntas/index.html',
                    'm8/oficina-sugerir/index.html'):
            self.assertNotIn(rel, MANIFESTO['files'])
            self.assertNotIn('apoio-tabela', ler(rel))
        # As lições sem achado A ou C ficam sem tabela nem lista novas.
        for rel in MANIFESTO['files']:
            if rel.startswith('m8/licao-') and rel not in (F04, F05, F08, F13, F15):
                self.assertEqual(ac_aplicadas(rel, base(rel)), base(rel), rel)

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, cab, _, _ in TABELAS for c in cab}
        self.assertEqual(cabecalhos, {'Elemento', 'Peso', 'Noção', 'Termo', 'O que é', 'Valor', 'Exemplo', 'O que mostra'})
        permitidas = {p for c in cabecalhos for p in palavras(c)}
        # O que sai: os números «1) 2) 3)» e «1. 2. 3.» que as listas numeradas do guia e da ajuda substituem.
        saem = {11: {'1', '2', '3'}, 12: {'1', '2', '3'}}
        css = [t for t in TROCAS if t['novo'].startswith('<link rel="stylesheet"')]
        self.assertEqual(sorted(t['ficheiro'] for t in css), sorted(C.COM_TABELA))
        estilo = [t for t in TROCAS if 'code{white-space:nowrap}' in t['novo']]
        self.assertEqual(len(estilo), 1)
        chaves = [t for t in TROCAS if '"nao_partir' in t['novo'] and '"nao_partir' not in t['antigo']]
        self.assertEqual([t['ficheiro'] for t in chaves], ['docs/pedagogia/tarefas-escolha/m8-u1.json', 'docs/pedagogia/tarefas-escolha/m8-u2.json'])
        # A única troca que muda letras: «Séc. XX» passa a «século XX» no rótulo do guia (a proposta final, como no guia do M5).
        seculo = [t for t in TROCAS if 'Séc.' in t['antigo']]
        self.assertEqual([(t['ficheiro'], t['antigo'], t['novo'], t['ocorrencias']) for t in seculo],
                         [(GUIA, SEC, 'Poesia e Conto do século' + N + 'XX', 1)])
        self.assertFalse([t for t in TROCAS if 'Séc.' in t['novo']])
        for t in TROCAS:
            if t in css or t in estilo or t in chaves or t in seculo:
                continue
            i = achados_da_troca(t)[0]
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                antes, depois = visivel(t['antigo']), visivel(t['novo'])
                # Nada de novo, salvo os cabeçalhos das tabelas; nada sai, salvo os números da lista do guia.
                self.assertEqual(palavras(t['novo']) - palavras(t['antigo']) - (permitidas if i in A else set()), set())
                self.assertEqual(palavras(t['antigo']) - palavras(t['novo']) - saem.get(i, set()), set())
                self.assertLessEqual(depois.count('·'), antes.count('·'))
                self.assertEqual(depois.count('—'), antes.count('—'))
                self.assertEqual(len(PROIBIDAS.findall(depois)), len(PROIBIDAS.findall(antes)))
                self.assertTrue(t['achado'].startswith('12/11/2026: decisão 152 (cuidado em todas as lições), varredura do M8'))
        for c in cabecalhos:
            self.assertIsNone(PROIBIDAS.search(c), c)
        # Nas tabelas, o texto é o de antes, pela mesma ordem: sem as marcas, sem a pontuação que a tabela substitui e sem os
        # cabeçalhos, as palavras da tabela são as do parágrafo, uma a uma.
        soltas = lambda s: re.findall(r'[\wÀ-ÿ%]+', visivel(s).lower())
        for t in TROCAS:
            if achados_da_troca(t)[0] in A and t not in css:
                cab = [p for c in next(c for r, _, c, _, _ in TABELAS if r == t['ficheiro']) for p in soltas(c)]
                novas = soltas(re.sub(r'<thead.*?</thead>| data-label=\\?"[^"\\]*\\?"', '', t['novo'].replace('<\\/', '</')))
                with self.subTest(tabela=t['ficheiro']):
                    self.assertEqual(novas, soltas(t['antigo']))
                    self.assertTrue(cab)
        # As trocas B só mudam espaços (U+00A0) e põem a junção (U+2060); nenhuma muda uma letra.
        for t in TROCAS:
            if '(B)' in t['achado'] and t not in chaves and t not in seculo:
                with self.subTest(local=t['local']):
                    self.assertEqual(t['novo'].replace(N, ' ').replace(WJ, ''), t['antigo'])
        # Nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, data-titulo, <title>, chaves JSON, nem da «frase» de
        # um sublinhar, das «palavras» de um cartão frase ou dos «passos» de um ordenar.
        for rel in MANIFESTO['files']:
            with self.subTest(contextos=rel):
                conta = lambda texto: sum(p.count(N) + p.count(WJ) for p in contextos_proibidos(texto))
                self.assertEqual(conta(ler(rel)), conta(base(rel)))
        # O detetor deixa de fora o que não se vê: o «alt» da pintura de Goya e o data-titulo dos vídeos ficam como estavam.
        f03 = ler('m8/licao-m8-f03/index.html')
        fora = sorted({C.fora_de_alcance(f03, m.start()) for seq in ('3 de maio de 1808', '2 min', '4 min')
                       for m in re.finditer(re.escape(seq), f03)})
        self.assertEqual(fora, ['atributo alt', 'atributo data-titulo'])

    def test_passagens_mudadas_sem_referencias_que_se_partam(self):
        for t in TROCAS:
            if t['novo'].startswith('<link rel="stylesheet"') or 'code{' in t['novo']:
                continue
            texto = sem_atributos_nem_desenhos(t['novo'])
            texto = visivel(texto) if '<' in texto else texto
            m = PARTE.search(texto)
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                self.assertIsNone(m, m and texto[max(0, m.start() - 30):m.end() + 30])
        # Cada troca B arranja alguma coisa que se partia: na base, com o texto à volta, o detetor apanha uma forma que se parte
        # dentro do trecho da troca (a chave do gerador prende os números do molde, conferidos noutro teste).
        for t in TROCAS:
            if '(B)' in t['achado'] and '"nao_partir' not in t['novo']:
                texto = base(t['ficheiro'])
                s = texto.index(t['antigo'])
                janela = texto[max(0, s - 40):s + len(t['antigo']) + 40]
                a = s - max(0, s - 40)
                with self.subTest(local=t['local']):
                    self.assertTrue(any(m.start() < a + len(t['antigo']) and m.end() > a for m in PARTE.finditer(janela)), t['antigo'])
        # Nas páginas tocadas, o que se vê já não tem nenhum dos pares dos achados que se parta (fora do que fica de fora).
        for x in C.ACHADOS_B:
            final = ler(x['ficheiro'])
            todos = pares_da_pagina(x['ficheiro'])
            for antigo, novo, _ in x['pares']:
                self.assertEqual(C.ocorrencias(final, antigo, novo, todos), [], (x['ficheiro'], antigo))
        # E o contrário: o detetor apanha as formas que partem, e deixa as inteiras.
        for partido in ('p. 5', 'pp. 52–53', 'pp.' + N + '52–53', 'n.º 1760', 'verso 1', 'versos 1 e 2', 'século XX', 'século XVI', 'Séc. XX',
                        'ato III', 'página 15', 'número 1760', '3.º ano', '12.º ano', '90 minutos', '10 min', '30 s', '30 %', '30 segundos',
                        '5 a 7 minutos', '3 de Maio', '3 de maio de 1808', '3' + N + 'de maio de 1808', '7 de agosto de 2023',
                        '1921–1998', 'M8-F03'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for x in C.ACHADOS_B:
            for _, novo, _ in x['pares']:
                self.assertIsNone(PARTE.search(C.j(novo) + '0'), novo)

    def test_camada_fechada_reversivel_e_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m8_20261112.json', '--manifesto', MANIFESTO_REL,
                            # 12/11/2026: por cima desta camada fica agora a decisão 152 no M9 (cuidado_m9_20261112, que não toca em nenhum
                            # ficheiro desta); desfaz-se primeiro, com a mesma exigência, e as contagens são as mesmas.
                            # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            '--verificar', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-provas-oficial-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-exame-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m9-edits-20261112.json'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), (152, 28))
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertEqual(len(m['base_commit']), 40)
        self.assertTrue(m['_nota'].startswith('12/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M8'))
        self.assertIn('cuidado_m8_20261112', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        # O rótulo «(notas do docente)» só nas notas editoriais; os painéis de projeção dizem «(painel de projeção)».
        for t in TROCAS:
            if '/painel-' in t['ficheiro']:
                self.assertIn('CARTOES=', ler(t['ficheiro']))
                self.assertIn('(painel de projeção)', t['local'])
            self.assertNotIn('(notas do docente)', t['local'])
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                # 12/11/2026: a página como esta camada a deixou: com a camada de cima (cuidado_m9_20261112) desfeita, com contagem
                # estrita; undo_cuidado_m8_1112 desfaz as duas, a partir da página inteira.
                atual = undo_cuidado_m9_1112(rel, ler(rel))
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_m8_1112(rel, ler(rel))
                self.assertEqual(sha_lf(b), registo['base_sha256_lf'])
                # Ida e volta: refazer as trocas sobre a base devolve a página, letra a letra.
                refeito = b
                for e in registo['edits']:
                    self.assertEqual(refeito.count(e['old']), e['occurrences'], (rel, e['location']))
                    refeito = refeito.replace(e['old'], e['new'])
                self.assertEqual(refeito, atual)
                for e in registo['edits']:
                    self.assertEqual(atual.count(e['new']), e['occurrences'], (rel, e['location']))
                    self.assertEqual(atual.replace(e['new'], '\0').count(e['old']), 0, (rel, e['location']))
                # A camada de baixo (a decisão 152 no M7) continua a desfazer-se por baixo desta, e não toca em nenhum ficheiro dela.
                # 12/11/2026: na página inteira, porque a cadeia de desfazer começa agora pela decisão 152 no M9.
                self.assertEqual(undo_cuidado_m7_1111(rel, ler(rel)), b)
                self.assertNotIn(rel, M7['files'])
        # Os 36 achados que entram estão todos na camada; os 8 que ficam de fora e os 7 recusados, não.
        achados = {n for t in TROCAS for n in achados_da_troca(t)}
        self.assertEqual(achados, APLICADOS)
        self.assertEqual((len(A), len(B), len(C_), len(CONFIRMADOS)), (8, 30, 6, 44))
        self.assertEqual((len(APLICADOS), len(B_PAGINAS), len(B_PAINEIS), len(FORA_DE_AMBITO), len(SO_MATERIAL), len(RECUSADOS)),
                         (36, 21, 1, 6, 2, 7))
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'A'}), sorted(A))
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'C'}), sorted(C_))
        # 34 achados nas páginas do M8 e 2 nas das tarefas.
        sitio = {x['i']: x['ficheiro'] for x in C.achados_ac() + C.ACHADOS_B}
        sitio.update({i: rel for rel, i in PAINEL.items()})
        self.assertEqual(sorted(sitio), sorted(APLICADOS))
        self.assertEqual(sum(f.startswith('m8/') for f in sitio.values()), 34)
        self.assertEqual(sum(f.startswith('tarefas/') for f in sitio.values()), 2)
        # A e C antes de B, em cada ficheiro.
        for rel in m['files']:
            ordem = ['B' if '(B)' in t['achado'] and '"nao_partir' not in t['novo'] else 'AC' for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual(ordem, sorted(ordem, key=lambda x: x != 'AC'), rel)
        # No topo da cadeia, logo por cima da decisão 152 no M7.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 12/11/2026: por cima da decisão 152 no M8 fica a decisão 152 no M9 (cuidado_m9_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M9 fica a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no Exame e nas páginas transversais fica a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da ligação «Treinos» na página principal do Exame ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima das provas em cartões com os documentos oficiais ficam as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M3 mais fáceis de fazer ficam as duas tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M1 mais fáceis de fazer ficam as duas tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('cuidado_m9_20261112', 'cuidado-m9-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[7], ('cuidado_m8_20261112', 'cuidado-m8-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[8], ('cuidado_m7_20261111', 'cuidado-m7-edits-20261111'))
        self.assertEqual(verificar_camadas.LAYERS[9], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[10], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[11], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        # 12/11/2026: com a decisão 152 no M9 por cima, as camadas passam a 43.
        # 12/11/2026: com a decisão 152 no Exame e nas páginas transversais, as camadas passam a ser mais uma.
        # 12/11/2026: com a ligação «Treinos» na página principal do Exame, as camadas passam a ser mais uma.
        # 12/11/2026: com as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112), as camadas passam a ser mais uma.
        # 12/11/2026: com as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112) no topo, as camadas passam de 46 a 47, todas diferentes.
        # 13/11/2026: com a camada das tarefas do M1 mais fáceis de fazer, são 48.
        # 13/11/2026: mais uma camada, as tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): 49 em vez de 48.
        self.assertEqual(len(verificar_camadas.LAYERS), 49)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 49)
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m7_1111'):]
        self.assertLess(corpo.index('undo_cuidado_m8_1112(path, text)'), corpo.index('_CUIDADO_M7_1111.get('))
        self.assertLess(corpo.index('undo_cuidado_m8_1112(path, text)'), corpo.index('_TAREFAS_CLARAS.get('))
        self.assertLess(auditoria.index('def undo_cuidado_m8_1112'), auditoria.index('def undo_cuidado_m7_1111'))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m8-edits-20261112.json'), sala.index('cuidado-m7-edits-20261111.json'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9, agora a mais recente.
        self.assertLess(sala.index('cuidado-m9-edits-20261112.json'), sala.index('cuidado-m8-edits-20261112.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes da decisão 152 no M7, logo a seguir a --verificar.
        meu, m7 = MANIFESTO_REL, 'tests/fixtures/cuidado-m7-edits-20261111.json'
        # 12/11/2026: e logo a seguir à decisão 152 no M9, que se desfaz primeiro, logo a seguir a --verificar, sem nada pelo meio.
        m9 = 'tests/fixtures/cuidado-m9-edits-20261112.json'
        # 12/11/2026: e, por cima da do M9, a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112).
        ex = 'tests/fixtures/cuidado-exame-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (a ligação «Treinos» na página principal do Exame).
        lt = 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (as provas em cartões com os documentos oficiais).
        po = 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (as duas tarefas do M3 mais fáceis de fazer).
        tf = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
        # 13/11/2026: por cima das tarefas do M3 ficam as tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M1 ficam as tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
        t5 = 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
        t1 = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + m7 not in linha:
                    continue
                linhas += 1
                # 12/11/2026: antes desta, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertIn(f'--verificar --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {meu} --desfazer-antes {m7}', linha, wf)
        # As 21 cadeias em que a decisão 152 no M7 se desfaz (as 20 que já desfaziam a do M6 e a conferência da própria camada do
        # M6; a conferência da camada do M7, que só tem esta por cima, vem abaixo).
        self.assertEqual(linhas, 21)
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        # 12/11/2026: a decisão 152 no M7 desfaz primeiro a do M9 e depois esta.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m7_20261111.json --manifesto {m7} --verificar --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {meu}\n',
                      tarefas)
        # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça.
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if not linha.lstrip().startswith('#') and '--desfazer-antes ' + meu in linha:
                    # 12/11/2026: à cabeça fica agora a decisão 152 no M9, e esta logo a seguir, sem nada pelo meio.
                    # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    self.assertIn(f'--verificar --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {meu}', linha, wf)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --verificar '
                      # 12/11/2026: o cartaz «Ler a cidade» desfaz primeiro a decisão 152 no M9, depois esta.
                      # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      f'--desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {meu} --desfazer-antes {m7} --desfazer-antes tests/fixtures/cuidado-m6-edits-20261108.json', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e da decisão 152 no M1 conferem as cadeias com frases partidas em várias linhas (e já
            # exigem esta camada à cabeça); ficam de fora pela mesma razão.
            # 12/11/2026: e o teste da decisão 152 no M9, pela mesma razão.
            if p.name in ('test_cuidado_m8.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py', 'test_cuidado_m9.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                # 12/11/2026: e, antes desta, a decisão 152 no M9, sem nada pelo meio.
                # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes ' + m7), plano.count(f'--desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {meu} --desfazer-antes {m7}'))
        # 12/11/2026: nas rotas, a decisão 152 no M9 vem primeiro, logo antes desta.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f"(ROOT/'{t5}',ROOT/'{t1}',ROOT/'{tf}',ROOT/'{po}',ROOT/'{lt}',ROOT/'{ex}',ROOT/'{m9}',ROOT/'{meu}',ROOT/'{m7}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM8['), texto.index('((cuidadoM7['), rel)
            # 12/11/2026: e, antes da do M8, a decisão 152 no M9.
            self.assertLess(texto.index('((cuidadoM9['), texto.index('((cuidadoM8['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM8[rel]'), corpo.index('((cuidadoM7[rel]'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9.
        self.assertLess(corpo.index('((cuidadoM9[rel]'), corpo.index('((cuidadoM8[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M8.read_text'), gerador_148.index('CUIDADO_M7.read_text'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9.
        self.assertLess(gerador_148.index('CUIDADO_M9.read_text'), gerador_148.index('CUIDADO_M8.read_text'))
        # O gerador dos acertos dos índices (as contagens do M8, onde esta camada prende «90 min») desfaz primeiro esta camada.
        acertos = ler('scripts/indices_acertos_20261107.py')
        self.assertLess(acertos.index('CUIDADO_M8.read_text'), acertos.index('MANIFESTO.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1 ao M7.
        # 12/11/2026: conferem-na com a decisão 152 no M9, a única por cima, desfeita antes.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m8_20261112.json --manifesto {meu} --verificar --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9}\n', tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m8.py' -v", wf)
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m7.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m8.py', apoios)
        for n in range(1, 9):
            self.assertIn(f'python tests/browser_cuidado_m{n}.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m8_20261112.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)

    def test_leitura_historica_das_tarefas_com_esta_camada_por_cima(self):
        # Os contratos históricos leem as tarefas como eram antes do pedido #192 (scripts/tarefas_claras_historico.py). Com esta
        # camada por cima, a leitura dá a base do manifesto do #192, letra a letra, em todas as páginas e dados que ele mudou: a
        # partir da página inteira, com esta camada já desfeita, com esta e a do M7 já desfeitas, ou com as três de cuidado já
        # desfeitas; e a cadeia de desfazer não desfaz nada segunda vez sobre esse texto.
        from auditoria_20261028 import undo_cuidado_m5_0811, undo_cuidado_m6_0811
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import tarefas_claras_historico as historico
        finally:
            sys.path.pop(0)
        claras = CLARAS
        m6 = json.loads(ler('tests/fixtures/cuidado-m6-edits-20261108.json'))['files']
        self.assertEqual(len(claras), 33)
        # Nesta camada e na dos enunciados, as tarefas do M8 (as páginas e os dados); nesta e nas do M7 e do M6, nenhum ficheiro.
        nossos = {'tarefas/m8-u1/index.html', 'tarefas/m8-u2/index.html', 'docs/pedagogia/tarefas-escolha/m8-u1.json',
                  'docs/pedagogia/tarefas-escolha/m8-u2.json'}
        self.assertEqual(set(MANIFESTO['files']) & set(claras), nossos)
        self.assertEqual(set(MANIFESTO['files']) & set(M7['files']), set())
        self.assertEqual(set(MANIFESTO['files']) & set(m6), set())
        # 12/11/2026: e nesta e na do M9, que fica por cima, também nenhum.
        m9 = json.loads(ler('tests/fixtures/cuidado-m9-edits-20261112.json'))['files']
        self.assertEqual(set(MANIFESTO['files']) & set(m9), set())
        for rel, registo in claras.items():
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                antes_192 = historico.desfazer(rel, atual)
                self.assertEqual(sha_lf(antes_192), registo['base_sha256_lf'])
                sem_m8 = undo_cuidado_m8_1112(rel, atual)
                self.assertEqual(historico.desfazer(rel, sem_m8), antes_192)
                sem_m7 = undo_cuidado_m7_1111(rel, atual)
                self.assertEqual(historico.desfazer(rel, sem_m7), antes_192)
                sem_m6 = undo_cuidado_m6_0811(rel, atual)
                self.assertEqual(sha_lf(sem_m6), registo['after_sha256_lf'])
                self.assertEqual(historico.desfazer(rel, sem_m6), antes_192)
                self.assertEqual(historico.desfazer(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m8_1112(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m7_1111(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m6_0811(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m5_0811(rel, antes_192), undo_cuidado_m5_0811(rel, atual))
                if rel in MANIFESTO['files']:
                    self.assertNotEqual(sem_m8, atual)
                    self.assertEqual(sha_lf(atual), MANIFESTO['files'][rel]['after_sha256_lf'])
                    self.assertEqual(sha_lf(sem_m8), MANIFESTO['files'][rel]['base_sha256_lf'])
                    self.assertEqual(sem_m7, sem_m8)
                    # Fora da exceção (a base exata do #192), a contagem continua estrita: um texto a que falta uma troca falha.
                    e = MANIFESTO['files'][rel]['edits'][0]
                    with self.assertRaises(AssertionError):
                        undo_cuidado_m8_1112(rel, atual.replace(e['new'], e['old'], 1))
                # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112) fica por cima e desfaz-se primeiro: nas tarefas do M9, que estão
                # nela e não nesta, o texto sem esta camada é a base do manifesto do M9; nos outros ficheiros, fica igual, como antes.
                elif rel in m9:
                    self.assertEqual(sha_lf(atual), m9[rel]['after_sha256_lf'])
                    self.assertEqual(sha_lf(sem_m8), m9[rel]['base_sha256_lf'])
                else:
                    self.assertEqual(sem_m8, atual)
        self.assertEqual(sorted(rel for rel in claras if rel in MANIFESTO['files']), sorted(nossos))
        # A ordem no leitor histórico: primeiro esta camada, depois a do M7, depois a do M6, depois os enunciados.
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer'):]
        self.assertLess(corpo.index('CUIDADO_M8.get(rel)'), corpo.index('CUIDADO_M7.get(rel)'))
        self.assertLess(corpo.index('CUIDADO_M7.get(rel)'), corpo.index('CUIDADO_M6.get(rel)'))
        self.assertLess(corpo.index('CUIDADO_M6.get(rel)'), corpo.index("entry['edits']"))

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_da_origem(self):
        # As tarefas da M8-U1 e da M8-U2 mudam também nos dados, que estão nesta camada.
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/')}
        self.assertEqual(dados, {'docs/pedagogia/tarefas-escolha/m8-u1.json', 'docs/pedagogia/tarefas-escolha/m8-u2.json'})
        for u in (1, 2):
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/m8-u{u}.json'))
            self.assertIs(d['nao_partir'], True)
            # As chaves do M6 («nao_partir_grelha», «nao_partir_valores») não entram no M8: a proposta não as pede.
            self.assertNotIn('nao_partir_grelha', d)
            self.assertNotIn('tabela', d['aquecer'])
        grelhas = json.loads(ler('docs/pedagogia/grelhas-tarefas-20261027.json'))['tarefas']
        self.assertEqual(sorted(s for s, t in grelhas.items() if t.get('nao_partir_valores')), ['m6-u1', 'm6-u2'])
        self.assertNotIn('docs/pedagogia/grelhas-tarefas-20261027.json', MANIFESTO['files'])
        self.assertFalse([f for f in MANIFESTO['files'] if f.startswith('docs/pedagogia/aquecimentos/')])
        # Os dados dizem o mesmo que diziam, letra a letra, salvo os espaços que não quebram e a chave do gerador.
        for rel in sorted(dados):
            solto = lambda s: s.replace(N, ' ').replace(WJ, '')
            antes, depois = json.loads(solto(base(rel))), json.loads(solto(ler(rel)))
            self.assertIs(depois.pop('nao_partir'), True)
            self.assertEqual(depois, antes, rel)
        with tempfile.TemporaryDirectory() as tmp:
            for pasta, comando in (('te', 'scripts/tarefas_escolha.py'), ('gr', 'scripts/grelhas_tarefas.py'), ('aq', 'scripts/aquecimentos.py')):
                r = subprocess.run([sys.executable, comando, '--saida', str(Path(tmp) / pasta)], cwd=ROOT, capture_output=True, text=True,
                                   encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for esperada in ('te/tarefas/m8-u1/index.html', 'te/tarefas/m8-u2/index.html', 'gr/tarefas/m8-u1/grelha/index.html',
                             'gr/tarefas/m8-u2/grelha/index.html', 'gr/tarefas/m8-u1/correcao/index.html', 'gr/tarefas/m8-u2/correcao/index.html',
                             'aq/tarefas/m8-u1/aquecimento/index.html', 'aq/tarefas/m8-u2/aquecimento/index.html'):
                self.assertIn(esperada, geradas)
            # O gerador das grelhas não acrescenta outra ligação à tarefa.
            self.assertFalse([g for g in geradas if g.startswith('gr/') and g.count('/') == 3])
            self.assertGreater(len(geradas), 50)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel.split('/', 1)[1]).read_bytes())
        # As páginas das tarefas que a camada muda são estas duas; os aquecimentos, as grelhas e as correções do M8 ficam como estavam.
        self.assertEqual(sorted(f for f in MANIFESTO['files'] if f.startswith('tarefas/')), ['tarefas/m8-u1/index.html', 'tarefas/m8-u2/index.html'])
        # As lições F13, F14, F15 e F16 são geradas (scripts/gerar_licoes_20261101.py): mudam nas fontes, fora da camada (como no M5
        # e no M6), e as lições e as suas notas saem iguais do gerador, letra a letra; as notas não mudam.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import gerar_licoes_20261101 as gerador_licoes
            from licoes_20261101 import LESSONS
        finally:
            sys.path.pop(0)
        self.assertEqual(sorted(x['id'] for x in LESSONS if x['id'].startswith('m8-')), sorted(GERADAS))
        unidades = gerador_licoes.sequences()
        for item in LESSONS:
            licao, notas = f"{item['id'][:2]}/licao-{item['id']}/index.html", f"{item['id'][:2]}/painel-{item['id']}/index.html"
            with self.subTest(licao=item['id']):
                self.assertEqual(gerador_licoes.render(item, unidades), ler(licao))
                self.assertEqual(gerador_licoes.render_notes(item), ler(notas))
                self.assertNotIn(notas, MANIFESTO['files'])
                if item['id'] in GERADAS:
                    self.assertIn(licao, MANIFESTO['files'])
                    self.assertEqual(base(notas), ler(notas))
                else:
                    self.assertNotIn(licao, MANIFESTO['files'])
        # A folha das tabelas entra na F15 pelo gerador, e só nela; nenhuma fonte fica com um trecho de antes.
        for item in LESSONS:
            pagina = gerador_licoes.render(item, unidades)
            self.assertEqual(pagina.count('apoios-tabelas.css'), 1 if item['id'] == 'm8-f15' else ler(f"{item['id'][:2]}/licao-{item['id']}/index.html").count('apoios-tabelas.css'))
        fontes = ler('scripts/licoes_20261101.py') + ler('scripts/imagens_licoes_20261101.py')
        for antigo in ('<strong>Autora:</strong> pessoa real', 'Formulações criadas para esta lição. A:', '<p><strong>Observação:</strong>',
                       'n.º 0, Casa Comum', 'pp. 14–15', '12.º ano, Bloco 27', 'na página 1 do documento', "data='27 de setembro de 2013'"):
            self.assertNotIn(antigo, fontes, antigo)
        self.assertEqual(fontes.count('decisão 152 no M8'), 6)


if __name__ == '__main__':
    unittest.main()
