"""08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M5. Camada literal cuidado_m5_20261108
(scripts/cuidado_m5_20261108.json, gerada por scripts/cuidado_m5_20261108.py; manifesto tests/fixtures/cuidado-m5-edits-20261108.json),
a mais recente, por cima da decisão 152 no M4 (cuidado_m4_20261108).

Este teste confere, no modelo de tests/test_cuidado_m1.py a tests/test_cuidado_m4.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices e o gerador do desenho comum dos índices;
* cada um dos 52 achados confirmados: as 7 tabelas novas (7 achados A), com o cabeçalho (th scope=col), a primeira coluna (th
  scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato, no cartão e no
  sítio certos (a coluna do peso estreita); os 10 casos do mesmo tipo (C), com o texto exato; os 35 achados B, com a contagem certa
  de cada par da proposta final (no contexto que a proposta dá) e a forma da proposta, sem nenhuma ocorrência que se parta fora do
  que fica de fora (o «alt», o data-titulo dos vídeos, o que outra camada já tinha posto), e a casca das lições, que fica para o
  molde; onde o número que se muda não é o da proposta, o achado diz porquê;
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e mais nenhuma do M5;
* que nenhum dos 11 achados recusados (2, 3, 4, 5, 7, 8, 10, 11, 16, 17 e 19) entrou;
* as regras do texto: as tabelas e as listas só usam texto que já estava na página (e os cabeçalhos); nada de «professor», «jogar»,
  «jogo», «ficha», «folha», «—» ou «·» novos; nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>, chaves
  JSON ou da «frase» de um sublinhar; nas passagens mudadas, nenhuma referência nem número que se parta;
* que as tarefas, os aquecimentos, as grelhas e a correção da M5-U1 e da M5-U2 saem iguais dos dados e dos geradores, que as lições
  F16 e F17 e as suas notas saem iguais do gerador das lições, e que os painéis do docente seguem os enunciados das lições."""
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
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
from tarefas_claras_historico import desfazer as desfazer_enunciados
sys.path.insert(0, str(ROOT / 'tests'))
from auditoria_20261028 import undo_cuidado_m5_0811, undo_cuidado_m4_0811  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m5_20261108.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m5-edits-20261108.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
BASE_COMMIT = 'c08631983dbe552afba3689202d7ed9e8cf5074b'
NBSP, WJ = '\xa0', '⁠'
N = NBSP
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
A = {0, 1, 6, 9, 12, 13, 14}
B = set(range(28, 63))
C_ = {15, 18, 20, 21, 22, 23, 24, 25, 26, 27}
CONFIRMADOS = A | B | C_
# O achado 30 (F07) é só a casca da lição, que fica para o molde: não tem troca.
SO_CASCA = {30}
RECUSADOS = {2, 3, 4, 5, 7, 8, 10, 11, 16, 17, 19}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)

PESOS = [['Tarefa da Unidade 1', '30' + N + '%'], ['Tarefa da Unidade 2', '30' + N + '%'], ['Provas rápidas', '10' + N + '%'],
         ['Prova escrita', '30' + N + '%']]
TEMPOS = [['Cartões com consulta', '10' + N + 'minutos'], ['Lês o enunciado', '5' + N + 'minutos'], ['Produção', '60' + N + 'minutos'],
          ['Revisão e entrega', '15' + N + 'minutos'], ['Total', '90' + N + 'minutos']]
# (página, índice da tabela na página, cabeçalho, linhas, larguras): o texto de cada célula, como se lê.
TABELAS = [
    # achado 0, guia da tarefa: os pesos (a coluna do peso estreita, como no M3)
    ('m5/guia-da-tarefa-m5/index.html', 0, ['Elemento', 'Peso'], PESOS, ['width:auto', 'width:5.5rem']),
    # achado 1, índice do módulo: os pesos
    ('m5/index.html', 0, ['Elemento', 'Peso'], PESOS, ['width:auto', 'width:5.5rem']),
    # achado 12, mapa do módulo: os pesos
    ('m5/mapa-do-modulo-m5/index.html', 0, ['Elemento', 'Peso'], PESOS, ['width:auto', 'width:5.5rem']),
    # achado 6, F11, cartão 23 («Para entender»): quem está à mesa
    ('m5/licao-m5-f11/index.html', 0, ['Personagem', 'Quem é'],
     [['Ega', 'amigo de Carlos, defende o naturalismo'], ['Alencar', 'um poeta romântico, mais velho'],
      ['Craft', 'um inglês rico, colecionador de arte'], ['Cohen', 'um homem das finanças'], ['Dâmaso', 'imita o que lhe parece elegante']],
     None),
    # achado 9, F13, cartão 19 («Para entender»): as peças de um texto de opinião
    ('m5/licao-m5-f13/index.html', 0, ['Peça', 'O que é'],
     [['Tese', 'a tua posição, numa frase'], ['Argumento', 'uma razão que a prova, com um exemplo'],
      ['Contra-argumento', 'o que dirá quem discorda'], ['Refutação', 'a tua resposta'],
      ['Modalização', 'as palavras que mostram o grau de certeza («talvez», «sem dúvida», «parece-me»)']], None),
    # achados 13 e 14, tarefas da M5-U1 e da M5-U2: os tempos da aula de tarefa (pelo gerador das tarefas, como no M1)
    ('tarefas/m5-u1/index.html', 0, ['Momento', 'Tempo'], TEMPOS, None),
    ('tarefas/m5-u2/index.html', 0, ['Momento', 'Tempo'], TEMPOS, None),
]
# Onde está cada tabela nas lições: (página, tabela) > (índice do cartão, o que fica por cima da tabela, o que fica a seguir).
LUGARES = {
    ('m5/licao-m5-f11/index.html', 0): (23, '<div class="caixa"><h3>Quem está à mesa</h3><table class="apoio-tabela" role="table">',
                                        '</table><p>O <b>realismo</b> quer mostrar a sociedade como ela é'),
    ('m5/licao-m5-f13/index.html', 0): (19, '<h3>Recorda: as peças de um texto de opinião</h3><table class="apoio-tabela" role="table">',
                                        '</table><p>Para a crítica social, junta a este excerto o jantar do Hotel Central'),
}
# Onde está cada tabela fora das lições: o que fica por cima e o que fica a seguir.
FORA_DAS_LICOES = {
    'm5/guia-da-tarefa-m5/index.html': ('<h1>Tarefas das unidades</h1><p>Avaliação:</p><table class="apoio-tabela" role="table">',
                                        '</table><p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20.'),
    'm5/index.html': ('<p>Pesos na avaliação:</p><table class="apoio-tabela" role="table">',
                      '</table><p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20.'),
    'm5/mapa-do-modulo-m5/index.html': ('<summary>As tarefas do Teams</summary><p>Avaliação:</p><table class="apoio-tabela" role="table">',
                                        '</table><p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20.'),
    'tarefas/m5-u1/index.html': ('<p>No início da aula de tarefa:</p><table class="apoio-tabela" role="table">',
                                 '</table><p>O relógio de produção começa depois da leitura.</p>'),
    'tarefas/m5-u2/index.html': ('<p>No início da aula de tarefa:</p><table class="apoio-tabela" role="table">',
                                 '</table><p>O relógio de produção começa depois da leitura.</p>'),
}

# O que a proposta final conta, par a par (o contexto da proposta e o número; nas páginas geradas, a forma concreta da página).
PROPOSTA = {
    28: {"Estás em: Lição M5-F02": 1, "Português 2026/2027. Lição M5-F02,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "A 17 de março, Simão parte": 1, ">a folhas 232</b>, o seguinte": 1, "<b>a folhas 232</b>, na página 232": 1, "lida por Sónia Pedro (5 min)": 2, "<i>Foi para a India em 17 de Março de 1807</i>": 1, "«Foi para a India em 17 de Março de 1807» fecha": 1, "escripto: Foi para a India em 17 de Março de 1807.": 1, "Ensina RTP (1 min)": 2},
    29: {"Estás em: Lição M5-F04": 1, "Português 2026/2027. Lição M5-F04,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "primeira parte, cap. IV.": 1, "Lucas de Almeida Marrão, c. 1850)": 2, "\"titulo\":\"Capítulo IV\"": 1, "_Amor de Perdição_ (1862), cap. IV (grafia": 1, "Ler o capítulo IV na Wikisource": 1, "_Amor de Perdição_, 1862, cap. IV</p>": 1},
    30: {"Estás em: Lição M5-F07": 1, "Português 2026/2027. Lição M5-F07,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1},
    31: {"Estás em: Lição M5-F08": 1, "Português 2026/2027. Lição M5-F08,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "Lucas de Almeida Marrão, c. 1850)": 2, "17 de março de 1807": 7, "26 de setembro de 1861": 2, "A 28 de dezembro de 1815": 1, "(primeiros 4 min)": 2},
    32: {"Estás em: Lição M5-F09": 1, "Português 2026/2027. Lição M5-F09,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "(3 min)": 2, "(2 min)": 2, "aos 26 de Setembro de 1861": 1},
    33: {"Estás em: Lição M5-F10": 1, "Português 2026/2027. Lição M5-F10,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "(1888), cap. I e último": 1, "(1888), volume 1, página": 1, "aparece logo no capítulo I.": 1, "A 28 de dezembro, a RTP1": 1, "Ensina RTP (1 min)": 2, "\"A: Início (cap. I)\"": 1, "sr.ª</b> D. Maria I:": 1, "papa rico do século XVI\\\">Leão X</b>": 1, "sr. D. João V.": 1, "<b>Leão X</b>, papa rico do século XVI</p>": 1, "(1888), cap. I (grafia": 1, "Sónia Pedro (3 min)": 2, "do segundo parágrafo do cap. I.": 1, "1888, cap. I e último": 1},
    34: {"Estás em: Lição M5-F11": 1, "Português 2026/2027. Lição M5-F11,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "(cap. VI). O que marcas": 1, "Benoliel, c. 1910)": 1, "O hotel do capítulo VI,": 1, "(1888), cap. VI (grafia": 1, "1888, cap. VI</p>": 1},
    35: {"Estás em: Lição M5-F12": 1, "Português 2026/2027. Lição M5-F12,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "(1888), cap. VI e último": 1, "1.ª pessoa": 3, "3.ª pessoa": 7},
    36: {"Estás em: Lição M5-F13": 1, "Português 2026/2027. Lição M5-F13,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "Porto, c. 1895)": 2},
    37: {"Estás em: Lição M5-F14": 1, "Português 2026/2027. Lição M5-F14,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "Benoliel, c. 1910)": 2, "O hotel do capítulo VI,": 1, "(2 min)": 4, "(capítulo I; retoma": 1, ">M5-F10</a>": 1},
    38: {"Estás em: Lição M5-F15": 1, "Português 2026/2027. Lição M5-F15,": 1, "pt/2/\">2.º ano</a>": 1, "Narrativa do século XIX</a>": 1, "(1888), volume 1, página": 2, "(primeiros 4 min)": 2, "(8 de janeiro de 2025)": 1},
    39: {"No capítulo I, o padre": 1, "No capítulo III, Brown": 1, "vol. I, Porto": 1, "do capítulo I (pp. 18–19)": 1, "do capítulo III (pp. 82–83)": 1, "capítulos I e III": 1, "resumo do capítulo III:": 1, "capítulo III, p. 90.": 1, "No mesmo capítulo III,": 1},
    40: {"7 de março de 1882": 1, "capítulo XII, edição de Ivo Castro": 1, "2020, p. 120.": 1, "Procura o capítulo XII e a página impressa 120.": 1, "recorte do capítulo XII.": 1, "Relê o recorte do capítulo XII e": 1},
    41: {"aula de tarefa de 90 minutos: aquecimento": 1, "tarefa 90 min</small>": 2, "cerca de 25 min, sem nada": 2, "<span class=\"chip\">10 min</span>": 2, "<span class=\"chip\">90 min</span>": 2, "90 minutos com consulta": 2, "Grelha /20; 30 %.": 2, "Narrativa do século XIX</span></h1>": 1, "Módulo 5, Narrativa do século XIX. Nada": 1, "2.º ano": 2, "a folhas 232.": 1, "17 de Março de 1807": 2, "26 de Setembro de 1861": 2, "capítulo IV": 3, "17 de março de 1807": 6, "26 de setembro de 1861": 2, "28 de dezembro de 1815": 1, "no capítulo VI?": 1, ".ª pessoa": 12, "28 de dezembro de 2015": 1},
    42: {"tarefa de 90 minutos, com aquecimento": 1, "em cartões (10 minutos). Seguem-se 5 minutos de": 1, "</a><br>30 %, individual": 2, "Narrativa do Séc. XIX": 1, "<b>Aquecer, 10 min</b>": 1, "<b>Ler o enunciado, 5 min</b>": 1, "<b>Produzir, 60 min</b>": 1, "<b>Rever e entregar, 15 min</b>": 1, "2.º ano": 2},
    43: {"Camilo Castelo Branco (1825–1890)": 1, "Eça de Queirós (1845–1900)": 1, "individual, 90 minutos, 30 %.": 2, "tarefa de 90 minutos, com aquecimento": 1, "Marrão, c. 1850)": 2, "Porto, c. 1895)": 2, "Benoliel, c. 1910)": 2, "(1888), volume 1, página": 2, "\">Lição M5-F": 7, "\">lição M5-F": 4, "<h1>Narrativa do século XIX</h1>": 1, "2.º ano": 2},
    44: {"tarefa de 90 minutos, com grelha": 1, "(40 %)": 1, "2.º ano": 2, "Narrativa do século XIX.</p>": 1},
    45: {"Antes de escrever · 10 min ·": 1, "Unidade 1 · 90 min": 1, "outra do cap. IV em que": 1, "virtudes» (cap. IV), «Teu primo»": 1, "a 17 de março de 1807;": 1},
    46: {"Antes de escrever · 10 min ·": 1, "Unidade 2 · 90 min": 1, "que vem do cap. I e outra nova.": 1, "No cap. VI, Alencar": 1, "Narra na 3.ª pessoa": 1, "o hotel do cap. VI, trinta": 1, "A 28 de dezembro de 2015, a RTP1": 1, "A 8 de janeiro de 2025, Eça": 1},
    47: {"na Introdução e no cap. IV;": 1},
    48: {"no cap. I, há uma": 1},
    49: {"outra do cap. IV em que": 1, "virtudes» (cap. IV), «Teu primo»": 1, "amor» (cap. IV): copio": 1},
    50: {"o que vem do cap. I e o que é novo": 1, "já estava no cap. I e outra": 1, "narrada na 3.ª pessoa;": 1, "primo!» (cap. IV de": 1},
    51: {"outra do cap. IV em que": 1},
    52: {"já estava no cap. I e outra": 1, "narrada na 3.ª pessoa;": 1},
    53: {"Gutenberg n.º 16425)": 2, "folhas 232": 3, "na página 232": 1, "17 de Março de 1807": 2},
    54: {"Gutenberg n.º 16425)": 2},
    55: {"Gutenberg n.º 16425)": 2, "1862, cap. IV": 2},
    56: {"Gutenberg n.º 16425)": 3},
    57: {"Gutenberg n.º 40409)": 2},
    58: {"Gutenberg n.º 40409)": 2, "1888, cap. VI": 2},
    59: {"Gutenberg n.º 40409)": 2, "1888, cap. I e último": 2, "sr.ª D. Maria I:": 1},
    60: {"Gutenberg n.º 40409)": 3},
    61: {"cerca de 25 min</p>": 1, "a folhas 232, o seguinte": 1, "em 17 de Março de 1807": 1, "</i>, Capítulo IV (o retrato": 2, "Gutenberg n.º 16425": 5},
    62: {"cerca de 25 min</p>": 1, "O hotel do capítulo VI,": 1, "</i>, cap. VI, o jantar": 2, "</i>, cap. IV, uma vida": 1, "Gutenberg n.º 40409": 5, "no capítulo IV: resoluções": 1, "O diletante do capítulo IV e": 1},
}

# As trocas que não estão na proposta, com a razão: a meta descrição das tarefas muda com «nao_partir» (como no M1 e no M3).
EXTRAS = {45: {'durante 90 minutos, com entrega'}, 46: {'durante 90 minutos, com entrega'}}
# As trocas B que não são só de espaços (com a proposta): «Séc. XIX» do guia passa a «século XIX».
TEXTO_MUDA = {('m5/guia-da-tarefa-m5/index.html', 'Narrativa do Séc. XIX')}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a proposta pede U+00A0, traço de intervalo sem U+2060
# ou o hífen da sigla «M5-Fxx» sem a junção. As formas do M5: «cap.», «capítulo(s)», «vol.», «volume», «pp.», «p.», «c.», «sr.»,
# «n.º», «século», «Séc.», «folhas», «página», «impressa», «D.», os reis e papas («Maria I», «João V», «Leão X»), ordinal e nome,
# número e unidade, datas (o dia preso ao «de» e o «de» preso ao ano; o espaço entre o mês e o «de» do ano fica), intervalos e a
# sigla. Nas listas, «capítulos I e III» prende o primeiro espaço e o que vem a seguir ao «e».
MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'
PARTE = re.compile(
    r'(?<![\w.])(?:[Cc]aps?|vol|séc|[Ss]éc|c|pp?|sr)\. (?=[\dIVXLC])'
    r'|n\.º (?=\d)|\bD\. (?=[A-Z])'
    r'|\b(?:[Cc]apítulos?|[Vv]olume|séculos?|folhas|página|impressa|Maria|Leão|João) (?=[\dIVXLC]+\b)'
    r'|\bcapítulos\xa0[IVX]+ e (?=[IVX])'
    r'|\d\.[ºª] (?=\w)'
    r'|\b\d+ (?=(?:min|minutos|segundos|%)(?!\w))'
    r'|\b\d{1,2} de (?=(?i:' + MESES + r'))'
    r'|(?i:' + MESES + r') de (?=\d{4}\b)'
    r'|\d–(?!⁠)\d|\bM5-(?!⁠)F\d')


def ler(rel):
    return desfazer_enunciados(rel, (ROOT / rel).read_bytes().decode('utf-8'))


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def gerador():
    spec = importlib.util.spec_from_file_location('cuidado_m5_20261108', ROOT / 'scripts/cuidado_m5_20261108.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


C = gerador()


def cartoes(texto):
    """Os cartões de uma lição."""
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0]


def visivel(fragmento):
    # O <wbr> (o ponto onde um nome do portefólio pode mudar de linha) não separa palavras.
    fragmento = fragmento.replace('<wbr>', '')
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragmento.replace('\\"', '"').replace('<\\/', '</').replace('\\n', '\n')))


def palavras(texto):
    return set(re.findall(r'[\wÀ-ÿ]+', visivel(texto).lower()))


def base(rel):
    """A página sem esta camada (desfeita pelo manifesto, com contagem estrita)."""
    return undo_cuidado_m5_0811(rel, ler(rel))


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
    for m in re.finditer(r'<table class=\\?"apoio-tabela\\?"', texto):
        fim = texto.index('</table>', m.start()) + len('</table>')
        out.append(texto[m.start():fim].replace('\\"', '"'))
    return out


def contextos_proibidos(texto):
    """Os pedaços onde não pode entrar U+00A0 nem U+2060: alt, aria-label, href e title, <title>, as chaves JSON e a «frase» de um
    sublinhar."""
    out = [m.group(2) for m in re.finditer(r'\b(alt|aria-label|href|title)=\\?"((?:(?!\\?").)*)', texto)]
    out += re.findall(r'<title>(.*?)</title>', texto, re.S)
    out += re.findall(r'"((?:[^"\\]|\\.)*)"\s*:', texto)
    for m in re.finditer(r'\{\s*"t":\s*"sublinhar"', texto):
        f = re.compile(r'"frase":\s*"((?:[^"\\]|\\.)*)"').search(texto, m.end())
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


def em_alcance(texto, s, antigo, novo):
    """As ocorrências de um par que contam: com a palavra inteira (salvo os pares que acabam na sigla) e nenhuma edição fora de
    alcance."""
    if not C._palavra_inteira(texto, s, s + len(antigo), antigo):
        return False
    return all(C.fora_de_alcance(texto, s + p) is None for p, _ in C.edicoes(antigo, C.j(novo)))


class CuidadoM5(unittest.TestCase):
    def test_sete_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 7)
        for rel, k, cabecalho, linhas, larguras in TABELAS:
            t = Tabela(tabelas_da_pagina(ler(rel))[k])
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(t.tabela.get('class'), 'apoio-tabela')
                self.assertEqual(t.tabela.get('role'), 'table')
                # Sem <caption>: nas lições, o título da caixa já a nomeia; fora delas, o rótulo fica num parágrafo antes (como no M3).
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
                # Só as dos pesos têm larguras: a coluna do peso (só um número) fica estreita e a primeira fica com o resto.
                self.assertEqual([c['attrs'].get('style') for c in topo['celulas']], larguras or [None] * len(cabecalho))
        # Nenhuma página do M5 (nem as suas tarefas, aquecimentos e grelhas) tem mais tabelas de apoio do que estas.
        contagem = {}
        for rel, *_ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        for p in sorted(glob.glob(str(ROOT / 'm5/**/index.html'), recursive=True)) + sorted(glob.glob(str(ROOT / 'tarefas/m5-*/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            with self.subTest(pagina=rel):
                self.assertEqual(len(tabelas_da_pagina(ler(rel))), contagem.get(rel, 0))

    def test_tabelas_nos_cartoes_e_nos_sitios_certos(self):
        for (rel, k), (indice, antes, depois) in LUGARES.items():
            cards = cartoes(ler(rel))
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(cards[indice]['t'], 'ler')
                self.assertEqual(cards[indice]['rot'], 'Para entender')
                self.assertIn(antes, cards[indice]['html'])
                self.assertIn(depois, cards[indice]['html'])
                self.assertEqual([i for i, c in enumerate(cards) if 'apoio-tabela' in c.get('html', '')], [indice])
        # O parágrafo do realismo e do naturalismo da F11 fica igual, depois da tabela.
        self.assertIn('</table><p>O <b>realismo</b> quer mostrar a sociedade como ela é, sem a embelezar.', cartoes(ler('m5/licao-m5-f11/index.html'))[23]['html'])
        for rel, (antes, depois) in FORA_DAS_LICOES.items():
            texto = ler(rel)
            with self.subTest(pagina=rel):
                self.assertEqual(texto.count(antes), 1)
                self.assertEqual(texto.count(depois), 1)
                self.assertLess(texto.index(antes), texto.index(depois))
        # Os pesos: o parágrafo avaliacao-tarefas continua a ser um só e fica sem a enumeração; no índice, dentro de details.regra.
        for rel in ('m5/index.html', 'm5/guia-da-tarefa-m5/index.html', 'm5/mapa-do-modulo-m5/index.html'):
            texto = ler(rel)
            self.assertEqual(texto.count('class="avaliacao-tarefas"'), 1, rel)
            self.assertNotRegex(re.search(r'<p class="avaliacao-tarefas">(.*?)</p>', texto).group(1), r'\d[ \xa0]%')
        self.assertIn('</tbody></table><p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20. Na primeira recuperação, fazes a tarefa '
                      'da unidade em falta, com a mesma grelha /20.</p></div></details>', ler('m5/index.html'))

    def test_folha_das_tabelas_antes_da_aparencia(self):
        com_tabela = sorted({r for r, *_ in TABELAS})
        self.assertEqual(com_tabela, sorted(C.COM_TABELA))
        for rel in com_tabela:
            cabeca = ler(rel).split('</head>')[0]
            with self.subTest(pagina=rel):
                self.assertEqual(cabeca.count(FOLHA), 1)
                self.assertLess(cabeca.index(FOLHA), cabeca.index('assets/appearance.css'))
        for p in sorted(glob.glob(str(ROOT / 'm5/**/index.html'), recursive=True)) + sorted(glob.glob(str(ROOT / 'tarefas/m5-*/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            if rel not in com_tabela:
                self.assertNotIn('apoios-tabelas.css', ler(rel), rel)
        # A folha é a do M1 e não muda: as regras das lições (.jogo .ler) e as de fora das lições já lá estão.
        css = ler('assets/pt-lessons/apoios-tabelas.css')
        self.assertIn('.jogo .ler .apoio-tabela td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertIn('.apoio-tabela:not(.jogo .ler .apoio-tabela) td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertNotIn('assets/pt-lessons/apoios-tabelas.css', {t['ficheiro'] for t in TROCAS})

    def test_casos_do_mesmo_tipo(self):
        # Achado 15: no guia, «Três antes de mim» numa lista ordenada.
        self.assertIn('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a '
                      'rubrica;</li><li>pergunta ao teu par de trabalho.</li></ol>Só depois levantas o braço.</div>', ler('m5/guia-da-tarefa-m5/index.html'))
        # Nos outros guias, a regra fica como estava (este pedido é do M5).
        for m in (2, 3, 6, 7, 8, 9):
            self.assertIn('Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta', ler(f'm{m}/guia-da-tarefa-m{m}/index.html'))
        # Achado 18: na F08, as perguntas e os factos em listas; as marcas da carta ficam em linha.
        f08 = cartoes(ler('m5/licao-m5-f08/index.html'))[2]['html']
        self.assertIn('<p><b>As perguntas de Teresa:</b></p><ul><li>Podias tu com a desesperança e com a vida?</li><li>Que farias da vida '
                      'sem a tua companheira?</li><li>Nunca hás de amar outra vez?</li></ul><p><b>Os factos:</b></p><ul><li>Simão matou '
                      'Baltasar e vai degredado para a Índia;</li><li>a nau saiu do Porto a 17' + N + 'de março de' + N + '1807;</li><li>Teresa '
                      'morreu no convento de Monchique;</li><li>Mariana, a filha do ferrador, vai a bordo com ele.</li></ul><p><b>As marcas de '
                      'uma carta:</b> local e data, vocativo, despedida, assinatura.</p>', f08)
        # Achados 20, 21 e 22: no vocabulário, os nomes a negrito, o último ligado com «e» (a linha do vocabulário fica em linha).
        self.assertIn('<b>Claude Bernard</b>, <b>Stuart Mill</b> e <b>Darwin</b>, cientistas e filósofos citados pelo naturalismo;',
                      cartoes(ler('m5/licao-m5-f11/index.html'))[20]['html'])
        self.assertIn('<b>Gremio</b> e <b>Casa Havaneza</b>, locais de convívio na Lisboa da época;', cartoes(ler('m5/licao-m5-f12/index.html'))[2]['html'])
        f13 = cartoes(ler('m5/licao-m5-f13/index.html'))[15]['html']
        self.assertIn('<b>Gremio</b> e <b>Casa Havaneza</b>, clube e tabacaria do Chiado;', f13)
        self.assertIn('<b>Bois</b>, <b>Bignon</b>, <b>Trouville</b> e <b>Saint-Cloud</b>, lugares elegantes de Paris e arredores;', f13)
        for rel, k in (('m5/licao-m5-f11/index.html', 20), ('m5/licao-m5-f12/index.html', 2), ('m5/licao-m5-f13/index.html', 15)):
            self.assertIn('<p class="gl"><b>Vocabulário:</b> ', cartoes(ler(rel))[k]['html'], rel)
        # Achado 23: no portefólio, todos os nomes em <code>, os longos com um ponto para mudar de linha a seguir a cada «_», e os
        # nomes não se partem nos hífenes.
        port = ler('m5/portefolio-do-modulo-m5/index.html')
        linhas = re.findall(r'<tr><td>(.*?)</td><td>', port)
        self.assertEqual(len(linhas), 15)
        self.assertTrue(all(re.fullmatch(r'<code>M5_[^<]*(?:<wbr>[^<]*)*</code>', l) for l in linhas), linhas)
        for nome in ('M5_<wbr>cartao-do-percurso', 'M5_<wbr>U1_<wbr>registo_<wbr>&lt;dia-mês&gt;', 'M5_<wbr>U1_<wbr>pergunta',
                     'M5_<wbr>U1_<wbr>o-que-aprendi', 'M5_<wbr>U2_<wbr>registo_<wbr>&lt;dia-mês&gt;', 'M5_<wbr>U2_<wbr>pergunta',
                     'M5_<wbr>U2_<wbr>o-que-aprendi', 'M5_<wbr>Prova-escrita'):
            self.assertEqual(port.count(f'<td><code>{nome}</code></td>'), 1, nome)
        for nome in ('M5_capa', 'M5_U1_Tarefa', 'M5_U2_Tarefa', 'M5_Extras', 'M5_Revisao1', 'M5_Revisao2', 'M5_balanco'):
            self.assertEqual(port.count(f'<td><code>{nome}</code></td>'), 1, nome)
        self.assertIn('padding:1px 4px}\ntd code{white-space:nowrap}\n', port)
        # Achados 25 e 27: os elementos dos temas em listas numeradas, pelo gerador (e nos dados); a frase seguinte do tema A fica.
        u1, u2 = ler('tarefas/m5-u1/index.html'), ler('tarefas/m5-u2/index.html')
        self.assertIn('Escreve a carta (90 a 120 palavras):</p><ol><li>local e data, vocativo, despedida e assinatura;</li><li>resposta a uma '
                      'pergunta dela;</li><li>uma memória dos dois;</li><li>um recurso expressivo teu;</li><li>um eco do romance, entre '
                      '«».</li></ol><p>Depois, em duas frases, diz que facto do romance respeitaste e o que faz o recurso.</p></article>', u1)
        self.assertIn('Num parágrafo de opinião (100 a 130 palavras):</p><ol><li>tese na primeira frase;</li><li>outra citação do último '
                      'capítulo, explicada;</li><li>um facto datado do dossiê, ligado à tese;</li><li>contra-argumento e refutação;</li>'
                      '<li>conclusão.</li></ol></article>', u2)
        self.assertNotIn('<p></p>', u2)
        for slug in ('m5-u1', 'm5-u2'):
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            self.assertEqual(sum('<ol>' in t['texto'] for t in d['temas']), 1, slug)
        # Achados 24 e 26: o descritor do nível máximo do critério 3 em listas, pelo gerador das grelhas («max_em_listas», como no M1);
        # a versão de correção fica com o texto corrido.
        grelhas = json.loads(ler('docs/pedagogia/grelhas-tarefas-20261027.json'))['tarefas']
        for slug in ('m5-u1', 'm5-u2'):
            self.assertEqual([c.get('max_em_listas') for c in grelhas[slug]['criterios']], [None, None, True, None, None], slug)
        g1, g2 = ler('tarefas/m5-u1/grelha/index.html'), ler('tarefas/m5-u2/grelha/index.html')
        self.assertIn('<p><b>Tema A</b>:</p><ul><li>as marcas da carta (local e data, vocativo, despedida e assinatura);</li><li>a resposta a '
                      'uma pergunta de Teresa;</li><li>uma memória dos dois;</li><li>um recurso expressivo teu;</li><li>um eco do romance, '
                      'entre «».</li></ul><p>Explicação: o facto do romance que a carta respeita e o que faz o recurso.</p><p><b>Tema B</b>:</p>'
                      '<ul><li>um painel para quem nunca leu o romance;</li><li>dois factos do dossiê (contam como dois);</li><li>uma frase '
                      'curta do romance, entre «»;</li><li>o que o painel não pode afirmar.</li></ul><p>Explicação: porque escolheste a '
                      'frase.</p>', g1)
        self.assertIn('<p><b>Tema A</b>:</p><ul><li>uma mesa de hoje narrada na 3.ª' + N + 'pessoa;</li><li>uma conversa séria;</li><li>uma '
                      'coisa banal que a corta ou desmonta;</li><li>uma fala em discurso direto;</li><li>um pensamento em indireto '
                      'livre.</li></ul><p>Explicação: o que imitaste de Eça e o que critica a tua interrupção.</p><p><b>Tema B</b>:</p><ul>'
                      '<li>a tese na primeira frase;</li><li>outra citação do último capítulo, explicada;</li><li>um facto datado do dossiê, '
                      'ligado à tese;</li><li>um contra-argumento;</li><li>a tua refutação.</li></ul><p>Conclusão: volta à tese com outras '
                      'palavras.</p>', g2)
        for slug in ('m5-u1', 'm5-u2'):
            self.assertNotIn('<ul>', re.sub(r'<style>.*?</style>', '', ler(f'tarefas/{slug}/correcao/index.html'), flags=re.S).split('Cumpres os cinco')[1].split('</small>')[0])

    def test_achados_b_com_a_contagem_certa(self):
        self.assertEqual(sorted(x['i'] for x in C.ACHADOS_B), sorted(B))
        self.assertEqual(sorted(PROPOSTA), sorted(B))
        vistos = 0
        for x in C.ACHADOS_B:
            rel, i = x['ficheiro'], x['i']
            prop = PROPOSTA[i]
            mudam = {p[0]: p[2] for p in x['pares']}
            fora = {s: n for s, (n, _) in x.get('fora', {}).items()}
            casca = x.get('casca', {})
            literais = {a for a, _, _ in x.get('literais', [])}
            # Cada par da proposta está no achado: muda, fica de fora (com a razão), é casca ou é uma troca literal com a razão; as
            # literais que não estão na proposta são as de EXTRAS.
            self.assertEqual(set(prop), set(mudam) | set(fora) | set(casca) | (literais - EXTRAS.get(i, set())), i)
            self.assertEqual(literais - set(prop), EXTRAS.get(i, set()), i)
            for seq, n in prop.items():
                total = mudam.get(seq, 0) + fora.get(seq, 0) + casca.get(seq, 0) + (1 if seq in literais else 0)
                with self.subTest(achado=i, trecho=seq):
                    if total != n:
                        # Onde se muda outro número, o achado diz o número da proposta e porquê.
                        self.assertEqual(x['mais'][seq][0], n)
                        self.assertTrue(x['mais'][seq][1])
                    else:
                        self.assertNotIn(seq, x.get('mais', {}))
            pre, final = ac_aplicadas(rel, base(rel)), ler(rel)
            for antigo, novo, n in x['pares']:
                with self.subTest(achado=i, trecho=antigo):
                    # Antes, cada par aparece (fora do que fica de fora) exatamente as vezes do achado; depois, nenhuma ocorrência se
                    # parte, e a forma da proposta final está lá.
                    antes = [m.start() for m in re.finditer(re.escape(antigo), pre) if em_alcance(pre, m.start(), antigo, novo)]
                    depois = [m.start() for m in re.finditer(re.escape(antigo), final) if em_alcance(final, m.start(), antigo, novo)]
                    self.assertEqual(len(antes), n)
                    self.assertEqual(depois, [])
                    self.assertGreaterEqual(final.count(C.j(novo)), n)
                    # As ocorrências de fora (o «alt», o data-titulo) ficam como estavam.
                    self.assertEqual(final.count(antigo), fora.get(antigo, 0) + (pre.count(antigo) - n - fora.get(antigo, 0)))
                    vistos += 1
        self.assertEqual(vistos, sum(len(x['pares']) for x in C.ACHADOS_B))
        # A casca das lições (migalhas, «Estás em», título escondido e sigla do rodapé) fica para o molde, como do M1 ao M4.
        self.assertEqual(len(C.CASCA_NO_MOLDE), 11)
        for rel in C.CASCA_NO_MOLDE:
            texto = ler(rel)
            n = re.search(r'licao-m5-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                for trecho in (f'Estás em: Lição M5-{n}', f'<h1 class="c-sr">Lição M5-{n}', f'Português 2026/2027. Lição M5-{n},',
                               '/pt/2/">2.º ano</a>', '>Módulo 5: Narrativa do século XIX</a>'):
                    self.assertEqual(texto.count(trecho), 1, trecho)
                self.assertEqual(next(x for x in C.ACHADOS_B if x['ficheiro'] == rel)['casca'], C.casca(n))
        # As fontes do rodapé (c-menu-extra) mudam, como no M1.
        for rel, fonte in (('m5/licao-m5-f04/index.html', '(1862), primeira parte, cap.' + N + 'IV. O que marcas'),
                           ('m5/licao-m5-f10/index.html', '(1888), cap.' + N + 'I e último capítulo. O que marcas'),
                           ('m5/licao-m5-f11/index.html', 'jantar no Hotel Central (cap.' + N + 'VI). O que marcas'),
                           ('m5/licao-m5-f12/index.html', '(1888), cap.' + N + 'VI e último capítulo; Dicionário Terminológico.')):
            self.assertIn(fonte, ler(rel), rel)
        # Nas outras páginas, as migalhas mudam onde o achado da página as inclui.
        for rel in ('m5/index.html', 'm5/guia-da-tarefa-m5/index.html', 'm5/mapa-do-modulo-m5/index.html', 'm5/portefolio-do-modulo-m5/index.html'):
            self.assertIn('/pt/2/">2.º' + N + 'ano</a>', ler(rel), rel)
        # Os intervalos levam a junção; a sigla das ligações do mapa também (os href, em minúsculas, ficam); e a da F14.
        mapa = ler('m5/mapa-do-modulo-m5/index.html')
        self.assertIn('Camilo Castelo Branco (1825–' + WJ + '1890)', mapa)
        self.assertIn('Eça de Queirós (1845–' + WJ + '1900)', mapa)
        self.assertEqual(len(re.findall(r'>[Ll]ição M5-' + WJ + r'F\d\d<', mapa)), 11)
        self.assertNotRegex(mapa, r'>[Ll]ição M5-F\d\d<')
        self.assertIn('>M5-' + WJ + 'F10</a>', ler('m5/licao-m5-f14/index.html'))
        self.assertIn('(pp.' + N + '18–' + WJ + '19)', ler('m5/licao-m5-f16/index.html'))
        # Os créditos do «i» que outra camada já tinha posto com U+00A0 ficam; os «alt» ficam com espaços normais.
        for c in ('c.' + N + '1850', 'c.' + N + '1895', 'c.' + N + '1910'):
            self.assertEqual(mapa.count('<span class="nb">' + c + '</span>'), 1, c)
        self.assertIn('alt="Os Maias, primeira edição (1888), volume 1, página de rosto"', mapa)
        self.assertIn('<p class="info-i-texto"><i>Os Maias</i>, primeira edição (1888), volume' + N + '1, página de rosto.', mapa)
        # «Séc. XIX» do guia passa a «século XIX» (a proposta), já com o espaço que não quebra; os vídeos: o botão muda, o data-titulo
        # (que vira o title do leitor) fica.
        self.assertIn('<p class="rot">Módulo 5: Narrativa do século' + N + 'XIX</p>', ler('m5/guia-da-tarefa-m5/index.html'))
        f02 = ler('m5/licao-m5-f02/index.html')
        self.assertIn('data-titulo=\\"a introdução de Amor de Perdição, lida por Sónia Pedro (5 min)\\"', f02)
        self.assertIn('data-yt-abrir>Ouvir: a introdução de Amor de Perdição, lida por Sónia Pedro (5' + N + 'min)</button>', f02)
        # Os pesos do índice, do guia e do mapa, e as tarefas, os aquecimentos e as grelhas, com os números do molde.
        for slug in ('m5-u1', 'm5-u2'):
            t = ler(f'tarefas/{slug}/index.html')
            self.assertIn('Antes de escrever · 10' + N + 'min · em cartões, com consulta', t)
            self.assertIn(f'Tarefa individual · Unidade {slug[-1]} · 90' + N + 'min</p>', t)
            self.assertNotIn('90 min', t)

    def test_nenhum_recusado_aplicado(self):
        achados = {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertFalse(RECUSADOS & achados)
        # 2, 5, 7, 10 e 11: os cartões «Em paralelo» ficam com o componente comum (sem tabela).
        for rel in ('m5/licao-m5-f02/index.html', 'm5/licao-m5-f10/index.html', 'm5/licao-m5-f12/index.html', 'm5/licao-m5-f14/index.html',
                    'm5/licao-m5-f15/index.html'):
            texto = ler(rel)
            self.assertEqual(texto.count('<div class=\\"paralelo\\">'), base(rel).count('<div class=\\"paralelo\\">'), rel)
            self.assertGreaterEqual(texto.count('<div class=\\"paralelo\\">'), 1, rel)
            self.assertNotIn('apoio-tabela', texto, rel)
        # 3, 4 e 8: os «O essencial» da F07, da F09 e da F12 ficam como estavam.
        self.assertIn('<span>Ao nível da frase: sujeito, predicado, vocativo, modificador de frase.', ler('m5/licao-m5-f07/index.html'))
        self.assertIn('<span>O caderno de campo tem três colunas: o que observar, o que vi e', ler('m5/licao-m5-f09/index.html'))
        self.assertIn('<span>Direto: travessão ou aspas. Indireto: verbo declarativo e subordinação', ler('m5/licao-m5-f12/index.html'))
        # 16, 17 e 19: os vocabulários da F02, da F04 e da F10 ficam em linha.
        for rel, inicio in (('m5/licao-m5-f02/index.html', '<b>assentamentos</b>, registos; <b>a folhas' + N + '232</b>, na página' + N + '232;'),
                            ('m5/licao-m5-f04/index.html', '<b>varonil</b>, forte como um homem; <b>despêgo</b>,'),
                            ('m5/licao-m5-f10/index.html', '<b>renque</b>, fila; <b>sr.ª</b>, senhora (abreviatura')):
            self.assertIn('<p class=\\"gl\\"><b>Vocabulário:</b> ' + inicio, ler(rel), rel)

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, cab, _, _ in TABELAS for c in cab}
        permitidas = {p for c in cabecalhos for p in palavras(c)}
        # O que entra de propósito: «lês» na tabela dos tempos (o texto atual diz «para leres o enunciado»), «século» no guia (a
        # proposta escreve «século XIX» por extenso) e, nos dados das tarefas e das grelhas, as chaves que os geradores leem.
        entram = {13: {'lês', 'tabela', 'colunas', 'linhas', 'depois'}, 14: {'lês', 'tabela', 'colunas', 'linhas', 'depois'},
                  42: {'século'}, 24: {'max_em_listas', 'true'}, 26: {'max_em_listas', 'true'}}
        # O que sai: a numeração dentro da frase de «Três antes de mim» (15), e «para» e «leres» dos tempos (13 e 14: «Lês o enunciado»),
        # «Séc» (42).
        saem = {15: {'1', '2', '3'}, 13: {'para', 'leres'}, 14: {'para', 'leres'}, 42: {'séc'}}
        css = [t for t in TROCAS if t['novo'].startswith('<link rel="stylesheet"')]
        self.assertEqual(sorted(t['ficheiro'] for t in css), sorted(C.COM_TABELA))
        estilo = [t for t in TROCAS if 'td code{white-space:nowrap}' in t['novo']]
        self.assertEqual(len(estilo), 1)
        chaves = [t for t in TROCAS if '"nao_partir": true' in t['novo']]
        self.assertEqual(sorted(t['ficheiro'] for t in chaves), ['docs/pedagogia/tarefas-escolha/m5-u1.json', 'docs/pedagogia/tarefas-escolha/m5-u2.json'])
        for t in TROCAS:
            if t in css or t in estilo or t in chaves:
                continue
            i = int(re.search(r'achado (\d+)', t['achado']).group(1))
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                antes, depois = visivel(t['antigo']), visivel(t['novo'])
                novas = palavras(t['novo']) - palavras(t['antigo']) - permitidas - entram.get(i, set())
                self.assertEqual(novas - palavras(base(t['ficheiro'])), set())
                self.assertEqual(palavras(t['antigo']) - palavras(t['novo']) - saem.get(i, set()), set())
                self.assertLessEqual(depois.count('·'), antes.count('·'))
                self.assertEqual(depois.count('—'), antes.count('—'))
                self.assertEqual(len(PROIBIDAS.findall(depois)), len(PROIBIDAS.findall(antes)))
                self.assertTrue(t['achado'].startswith('08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M5'))
        for c in cabecalhos:
            self.assertIsNone(PROIBIDAS.search(c), c)
        # As trocas B só mudam espaços (U+00A0) e põem a junção (U+2060), salvo «Séc. XIX» do guia (TEXTO_MUDA).
        for t in TROCAS:
            if '(B)' in t['achado'] and (t['ficheiro'], t['antigo']) not in TEXTO_MUDA and '"nao_partir"' not in t['novo']:
                with self.subTest(local=t['local']):
                    self.assertEqual(t['novo'].replace(N, ' ').replace(WJ, ''), t['antigo'])
        self.assertEqual(sum((t['ficheiro'], t['antigo']) in TEXTO_MUDA for t in TROCAS), 1)
        # Nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>, chaves JSON nem da «frase» de um sublinhar.
        for rel in MANIFESTO['files']:
            with self.subTest(contextos=rel):
                conta = lambda texto: sum(p.count(N) + p.count(WJ) for p in contextos_proibidos(texto))
                self.assertEqual(conta(ler(rel)), conta(base(rel)))

    def test_passagens_mudadas_sem_referencias_que_se_partam(self):
        for t in TROCAS:
            if t['novo'].startswith('<link rel="stylesheet"') or 'td code{' in t['novo']:
                continue
            texto = sem_atributos_nem_desenhos(t['novo'])
            texto = visivel(texto) if '<' in texto else texto
            m = PARTE.search(texto)
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                self.assertIsNone(m, m and texto[max(0, m.start() - 30):m.end() + 30])
        # Cada troca B arranja alguma coisa que se partia: na base, com o texto à volta, o detetor apanha uma forma que se parte
        # dentro do trecho da troca.
        for t in TROCAS:
            if '(B)' in t['achado'] and '"nao_partir"' not in t['novo']:
                texto = base(t['ficheiro'])
                s = texto.index(t['antigo'])
                janela = texto[max(0, s - 40):s + len(t['antigo']) + 40]
                a = s - max(0, s - 40)
                with self.subTest(local=t['local']):
                    self.assertTrue(any(m.start() < a + len(t['antigo']) and m.end() > a for m in PARTE.finditer(janela)), t['antigo'])
        # Nas páginas tocadas, o que se vê já não tem nenhum dos pares dos achados que se parta (fora do que fica de fora).
        for x in C.ACHADOS_B:
            final = ler(x['ficheiro'])
            for antigo, novo, _ in x['pares']:
                for m in re.finditer(re.escape(antigo), final):
                    self.assertFalse(em_alcance(final, m.start(), antigo, novo), (x['ficheiro'], antigo))
        # E o contrário: o detetor apanha as formas que partem, e deixa as inteiras (com os espaços que a proposta deixa).
        for partido in ('cap. IV', 'capítulo XII', 'capítulos I e III', 'vol. I', 'volume 1', 'pp. 18–19', 'p. 90', 'c. 1850', 'n.º 16425',
                        'século XIX', 'Séc. XIX', 'folhas 232', 'página 232', 'impressa 120', 'D. Maria I', 'Leão X', 'sr. D. João V',
                        '2.º ano', '3.ª pessoa', '90 minutos', '10 min', '30 %', '17 de março de 1807', '17' + N + 'de março de 1807',
                        'A 28 de dezembro', '1825–1890', 'M5-F02'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for x in C.ACHADOS_B:
            for _, novo, _ in x['pares']:
                self.assertIsNone(PARTE.search(re.sub(r'\b(?:alt|title|data-titulo)=\\?"[^"]*', '', C.j(novo)) + '0'), novo)

    def test_camada_fechada_reversivel_e_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m5_20261108.json', '--manifesto', MANIFESTO_REL,
                            '--verificar', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), (210, 42))
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M5'))
        self.assertIn('cuidado_m4_20261108', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_m5_0811(rel, atual)
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
                # A camada de baixo (a decisão 152 no M4) continua a desfazer-se por baixo desta.
                undo_cuidado_m4_0811(rel, atual)
        # Os 52 achados confirmados estão todos na camada, salvo o 30 (só a casca, que fica para o molde); nenhum recusado.
        achados = {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertEqual(achados, CONFIRMADOS - SO_CASCA)
        self.assertEqual((len(A), len(B), len(C_)), (7, 35, 10))
        self.assertEqual(next(x for x in C.ACHADOS_B if x['i'] == 30)['pares'], [])
        self.assertEqual(sorted({x['i'] for x in C.ACHADOS_AC + C.ac_grelhas() if x['cat'] == 'A'}), sorted(A))
        self.assertEqual(sorted({x['i'] for x in C.ACHADOS_AC + C.ac_grelhas() if x['cat'] == 'C'}), sorted(C_))
        # A e C antes de B, em cada ficheiro.
        for rel in m['files']:
            ordem = ['B' if '(B)' in t['achado'] and '"nao_partir"' not in t['novo'] else 'AC' for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual(ordem, sorted(ordem, key=lambda x: x != 'AC'), rel)
        # No topo da cadeia.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('cuidado_m4_20261108', 'cuidado-m4-edits-20261108'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m4_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m5_0811(path, text)'), corpo.index('_CUIDADO_M4_0811.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m5-edits-20261108.json'), sala.index('cuidado-m4-edits-20261108.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes da decisão 152 no M4, logo a seguir a --verificar.
        meu, m4 = MANIFESTO_REL, 'tests/fixtures/cuidado-m4-edits-20261108.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + m4 not in linha:
                    continue
                linhas += 1
                self.assertIn(f'--verificar --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {meu} --desfazer-antes {m4}', linha, wf)
        # As 17 cadeias da decisão 152 no M4 e a da decisão 152 no M3 em pt-tarefas-qa.
        self.assertEqual(linhas, 18)
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m4_20261108.json --manifesto {m4} --verificar --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {meu}\n',
                      tarefas)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --verificar --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json '
                      f'--desfazer-antes {meu} --desfazer-antes {m4} --desfazer-antes tests/fixtures/cuidado-m3-edits-20261108.json', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e da decisão 152 no M1 conferem as cadeias com frases partidas em várias linhas (e já
            # exigem esta camada à cabeça); ficam de fora pela mesma razão.
            if p.name in ('test_cuidado_m5.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + m4), plano.count(f'--desfazer-antes {meu} --desfazer-antes {m4}'))
        self.assertIn(f"(ROOT/'{meu}',ROOT/'{m4}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM5['), texto.index('((cuidadoM4['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM5[rel]'), corpo.index('((cuidadoM4[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M5.read_text'), gerador_148.index('CUIDADO_M4.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1 ao M4.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m5_20261108.json --manifesto {meu} --verificar --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json\n', tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m5.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m5.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m5_20261108.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_dos_dados(self):
        # As tarefas, os aquecimentos, as grelhas e a correção da M5-U1 e da M5-U2 mudam também nos dados, que estão nesta camada.
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/')}
        self.assertEqual(dados, {'docs/pedagogia/tarefas-escolha/m5-u1.json', 'docs/pedagogia/tarefas-escolha/m5-u2.json',
                                 'docs/pedagogia/aquecimentos/m5-u1.json', 'docs/pedagogia/aquecimentos/m5-u2.json',
                                 'docs/pedagogia/grelhas-tarefas-20261027.json'})
        for slug in ('m5-u1', 'm5-u2'):
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            self.assertIs(d['nao_partir'], True)
            self.assertEqual(d['aquecer']['tabela'], {'colunas': ['Momento', 'Tempo'], 'linhas': TEMPOS})
            self.assertEqual((d['aquecer']['texto'], d['aquecer']['depois']),
                             ('No início da aula de tarefa:', 'O relógio de produção começa depois da leitura.'))
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for slug in ('m5-u1', 'm5-u2'):
                for pagina in ('', 'aquecimento/', 'grelha/', 'correcao/'):
                    self.assertIn(f'tarefas/{slug}/{pagina}index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())
        # As lições F16 e F17 e as suas notas do docente saem iguais do gerador das lições (as fontes mudaram fora da camada).
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from licoes_20261101 import LESSONS
            from gerar_licoes_20261101 import render, sequences, render_notes
        finally:
            sys.path.pop(0)
        unidades = sequences()
        for ident in ('m5-f16', 'm5-f17'):
            item = next(x for x in LESSONS if x['id'] == ident)
            self.assertEqual(ler(f'm5/licao-{ident}/index.html'), render(item, unidades), ident)
            self.assertEqual(ler(f'm5/painel-{ident}/index.html'), render_notes(item), ident)
        cards = json.dumps(next(x for x in LESSONS if x['id'] == 'm5-f16')['cards'], ensure_ascii=False)
        self.assertIn('capítulos' + N + 'I e' + N + 'III', cards)
        self.assertIn('(pp.' + N + '82–' + WJ + '83)', cards)
        self.assertIn('7' + N + 'de março de' + N + '1882', json.dumps(next(x for x in LESSONS if x['id'] == 'm5-f17')['cards'], ensure_ascii=False))

    def test_paineis_seguem_as_licoes(self):
        # Os painéis do docente das lições do M5 projetam os enunciados dos cartões: onde um mudou, o painel muda igual, na lista e no
        # seletor; e cada enunciado que seguia a lição antes desta camada continua a segui-la.
        paineis = sorted({t['ficheiro'] for t in TROCAS if '/painel-' in t['ficheiro']})
        # O da F10 (o «cap. I» do enunciado do cartão de ordenar) e as notas geradas da F16 e da F17 (os retornos com os capítulos).
        self.assertEqual(paineis, ['m5/painel-m5-f10/index.html', 'm5/painel-m5-f16/index.html', 'm5/painel-m5-f17/index.html'])
        seguidos = 0
        for p in sorted(glob.glob(str(ROOT / 'm5/painel-m5-f*/index.html'))):
            rel = Path(p).relative_to(ROOT).as_posix()
            licao = rel.replace('/painel-', '/licao-')
            if 'CARTOES=' not in ler(rel):
                continue
            itens, itens_antes = cartoes(ler(rel)), cartoes(base(rel))
            L, L_antes = cartoes(ler(licao)), cartoes(base(licao))
            for item, antes in zip(itens, itens_antes):
                f = next((f for f in C.ENUNCIADOS if f(L_antes[antes['k']]) == antes['p']), None)
                if f is None:
                    continue
                with self.subTest(painel=rel, k=item['k']):
                    self.assertEqual(item['p'], f(L[item['k']]))
                    seguidos += 1
                    m = re.search(r'<option value="%d">([^<]*)</option>' % item['k'], ler(rel))
                    if not m:
                        continue
                    opcao = m.group(1)
                    self.assertTrue(html.escape(re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', item['p']), quote=False).startswith(opcao)
                                    or html.escape(item['p'], quote=False).startswith(opcao))
        self.assertGreater(seguidos, 80)


if __name__ == '__main__':
    unittest.main()
