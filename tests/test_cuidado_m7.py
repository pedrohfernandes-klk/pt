"""11/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M7. Camada literal cuidado_m7_20261111
(scripts/cuidado_m7_20261111.json, gerada por scripts/cuidado_m7_20261111.py; manifesto tests/fixtures/cuidado-m7-edits-20261111.json),
a mais recente, por cima da decisão 152 no M6 (cuidado_m6_20261108).

Este teste confere, no modelo de tests/test_cuidado_m1.py a tests/test_cuidado_m6.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices e o gerador do desenho comum dos índices;
* cada um dos 61 achados confirmados que entram: as 3 tabelas novas (3 achados A), com o cabeçalho (th scope=col), a primeira
  coluna (th scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato, no
  cartão e no sítio certos; os 3 casos do mesmo tipo (C), com o texto exato; os 55 achados B, com a contagem certa de cada par da
  proposta final (com a palavra inteira e fora das cadeias maiores dos outros pares) e a forma da proposta, sem nenhuma ocorrência
  que se parta fora do que fica de fora (o «alt», o data-titulo dos vídeos, a «frase» de um sublinhar, os «passos» de um ordenar,
  a casca das lições, que fica para o molde, e o que a conferência deixou de fora com a razão);
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e mais nenhuma do M7 (a F10 e
  a F15, que já tinham a sua tabela e a folha, ficam como estavam);
* que os 5 achados dos diapositivos, das provas rápidas e dos questionários (4, 56, 57, 58 e 59) ficam de fora, como do M1 ao
  M5, e que nenhum dos 9 achados recusados (0, 3, 5, 20, 28, 34, 35, 47 e 63) entrou;
* as regras do texto: as tabelas e as listas só usam texto que já estava na página (e os cabeçalhos); nada de «professor», «jogar»,
  «jogo», «ficha», «folha», «—» ou «·» novos; nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>,
  data-titulo, chaves JSON, nem da «frase» de um sublinhar, das «palavras» de um cartão frase ou dos «passos» de um ordenar; nas
  passagens mudadas, nenhuma referência nem número que se parta;
* que a tarefa, a grelha e a correção da M7-U3 e os três aquecimentos saem iguais dos dados e dos geradores (e as dos outros
  módulos não mudam), que os painéis do docente seguem os enunciados das lições (com o material do relâmpago como estava) e que
  as cópias do banco das provas rápidas seguem os cartões."""
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
from auditoria_20261028 import undo_cuidado_m7_1111, undo_cuidado_m6_0811  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m7_20261111.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m7-edits-20261111.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
# A camada assenta no ramo da decisão 152 no M6, já com o main 4bf4a053 dentro.
BASE_COMMIT = '2900616656378e4fb39d93747a5c7c450a38179f'
NBSP, WJ = '\xa0', '⁠'
N = NBSP
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
A = {8, 10, 25}
C_ = {6, 18, 54}
# Os achados B dos painéis de projeção (40 a 46 e 48 a 52) e os das outras páginas.
B_PAINEIS = {40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52}
B_PAGINAS = {1, 2, 7, 9, 11, 12, 13, 14, 15, 16, 17, 19, 21, 22, 23, 24, 26, 27, 29, 30, 31, 32, 33, 36, 37, 38, 39, 53, 55, 60, 61,
             62, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74}
# Ficam de fora, por decisão já tomada para todos os módulos (como do M1 ao M5): os diapositivos (4), as três provas rápidas
# (56, 57 e 58) e os questionários (59). Confirmados pela conferência, mas essas páginas não mudam.
FORA_DE_AMBITO = {4: 'm7/diapositivos/index.html', 56: 'm7/prova-a/index.html', 57: 'm7/prova-b/index.html',
                  58: 'm7/prova-c/index.html', 59: 'm7/questionarios/index.html'}
B = B_PAINEIS | B_PAGINAS | set(FORA_DE_AMBITO)
CONFIRMADOS = A | B | C_
APLICADOS = CONFIRMADOS - set(FORA_DE_AMBITO)
RECUSADOS = {0, 3, 5, 20, 28, 34, 35, 47, 63}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)
INDICE, F01, F10, F23 = 'm7/index.html', 'm7/licao-m7-f01/index.html', 'm7/licao-m7-f10/index.html', 'm7/licao-m7-f23/index.html'
GUIA, PORTEFOLIO = 'm7/guia-da-tarefa-m7/index.html', 'm7/portefolio-do-modulo-m7/index.html'

# (página, índice da tabela nova na página, cabeçalho, linhas, larguras): o texto de cada célula, como se lê.
TABELAS = [
    # achado 8, índice do módulo, «Como se cumpre uma unidade»: os pesos, com a coluna do peso estreita (como no índice do M5)
    (INDICE, 0, ['Elemento', 'Peso'],
     [['Tarefa da Unidade 2 («Uma ideia de heterónimo»)', '35' + N + '%'], ['Tarefa da Unidade 3 («Louco, sim»)', '25' + N + '%'],
      ['Provas rápidas', '10' + N + '%'], ['Prova escrita', '30' + N + '%']],
     ['width:auto', 'width:5.5rem']),
    # achado 10, F01, cartão 2 («O essencial»), dobra «As três vidas, segundo a carta»
    (F01, 0, ['Heterónimo', 'Vida'],
     [['Caeiro', 'Lisboa, 1889; morre em 1915; vive quase sempre no campo, sem profissão'],
      ['Reis', 'Porto, 1887; médico e latinista; vive no Brasil'],
      ['Campos', 'Tavira, 1890; engenheiro naval formado em Glasgow']], None),
    # achado 25, F23, cartão 14 («Para entender», «Recorda»)
    (F23, 0, ['Termo', 'O que é'],
     [['Ode', 'poema de tom elevado, em estrofes regulares; Reis segue o modelo do poeta latino Horácio'],
      ['Epicurismo', 'procurar a tranquilidade com prazeres simples, sem excessos, e sem temer a morte'],
      ['Estoicismo', 'dominar as paixões e aceitar a ordem do mundo, incluindo a morte'],
      ['Carpe diem', 'expressão latina que manda aproveitar o dia de hoje']], None),
]
# Onde está cada tabela nas lições: (página, tabela) > (índice do cartão, rótulo do cartão, o que fica por cima, o que fica a seguir).
LUGARES = {
    (F01, 0): (2, 'O essencial', '<details><summary>As três vidas, segundo a carta</summary><div><table class="apoio-tabela" role="table">',
               '</table></div></details>'),
    (F23, 0): (14, 'Para entender', '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela" role="table">',
               '</table><p>Na lição «À beira do rio» viste esta maneira de viver; aqui dás-lhe nome. <span class="sub">Fonte: Wikipédia, '
               '«Ricardo Reis».</span></p></div>'),
}
# As tabelas de apoio que já lá estavam, de outras camadas (a dos seis movimentos da F10 e a dos conceitos da F15): ficam.
JA_TINHAM = {F10: 1, 'm7/licao-m7-f15/index.html': 1}

# O que a proposta final conta, par a par («antes»: as ocorrências que mudam, com a palavra inteira e fora das cadeias maiores),
# tal como está em bordo/cidadania-v3/cuidado-152/m7-confirmados.json.
PROPOSTA = {
    1: {'poema II': 1, 'poema IX': 1},
    2: {'8 palavras': 1},
    7: {'90 minutos': 1, '90 min': 3, '15 min': 2, '60 min': 1, '10 minutos': 2, '100 a 150 palavras': 4,
         '80 a 120 palavras': 1, '180 a 220 palavras': 3, '150 a 180 palavras': 3, '12 a 16 versos': 3, '3.º ano': 2,
         'D. Sebastião': 2},
    9: {'90 minutos': 5, '35 %': 1, '25 %': 1, '10 %': 1, '30 %': 1, '90 min': 6, '22 min': 1, '10 a 15 min': 1, '23 min': 1,
         '10 min': 2, '13 de janeiro de 1935': 2, '8 de março de 1914': 2, '4 de agosto de 1578': 1,
         '15 de outubro de 1890': 1, '3.º ano': 2, '2.ª estrofe': 14, '3.ª estrofe': 13, '5.ª estrofe': 4, '6.ª estrofe': 1,
         '4.ª estrofe': 8, '1.ª estrofe': 2, '6.º verso': 2, '1.ª pessoa': 3, '3.ª estrofes': 1, '4.º verso': 1,
         '5.º verso': 1, '3.ª pessoa': 2, '2.ª pessoa': 1, '1.º verso': 2, 'poemas II e IX': 1, 'poema XX': 2, 'v. 4': 2,
         'vv. 3 e 4': 1, 'v. 2': 1, 'poema I': 3, 'poema II': 6, 'poema IX': 1, 'v. 1': 3, 'v. 8': 4, 'v. 7': 1, 'v. 10': 1,
         'v. 3': 1, 'v. 5': 2, 'D. Sebastião': 10, 'D. João': 3, 'M7-F10': 1},
    11: {'13 de janeiro de 1935': 5, '8 de março': 1, '8 de março de 1914': 3},
    12: {'30 s': 1, '1.ª publicação': 2, '2.ª estrofe': 6, '3.ª estrofe': 3, '1.ª estrofe': 2, 'n.º 36': 1, 'v. 4': 5,
         'vv. 3 e 4': 1, 'v. 2': 1, 'n.º 38': 1, 'v. 6': 1, 'v. 10': 1, 'versos 2 e 3': 1},
    13: {'8 de março': 1, 'Poema II': 1, 'v. 1': 1, 'verso 14': 1, 'verso 15': 1, 'poema IX': 1, 'poema II': 3},
    14: {'1 min': 1, '12 de junho': 1, '1 de julho': 1, '1.ª pessoa': 2, '2.ª estrofe': 2, '3.ª estrofe': 4, '4.ª estrofe': 3,
         '5.ª estrofe': 2, '3.ª estrofes': 1, '1.ª estrofe': 1, 'n.º 1': 1, 'estrofes 1 a 5': 1, 'v. 1': 4, 'v. 8': 1,
         'v. 7': 1, 'vv. 11 e 12': 1, 'vv. 19 e 20': 1},
    15: {'1 min': 1, '15 de outubro': 1, '15 de janeiro': 1, '4.º verso': 2, '5.º verso': 1, 'n.º 39': 1},
    16: {'3 min': 1, '4 de agosto': 1, '10 de dezembro': 1, '20 de fevereiro': 1, '1.ª edição': 1, '3.º verso': 1,
         '1.ª estrofe': 2, '2.ª estrofe': 1, 'v. 1': 1, 'v. 8': 3, 'v. 10': 1, 'D. Sebastião': 2},
    17: {'4 de agosto de 1578': 2, '1.ª pessoa': 5, '3.ª pessoa': 2, '2.ª pessoa': 1, '1.ª estrofe': 1, '2.ª estrofe': 3,
         '6.º verso': 1, '2.º ano': 2, 'v. 3': 1, 'vv. 4 e 5': 1, 'v. 4': 2, 'v. 5': 2, 'v. 11': 1, 'v. 15': 1,
         'D. Sebastião': 13, 'D. João': 5, 'c. 1571-1574': 1},
    19: {'25 %': 2, '180 a 220 palavras': 2, '1.º verso': 2, 'século XV': 1, 'D. Henrique': 1, 'D. Sebastião': 5, 'D. João': 2,
         'M7-F07': 1},
    21: {'15 de outubro de 1890': 1, 'D. Sebastião': 2},
    22: {'3.º ano': 1, '3.ª estrofe': 7, '2.ª estrofe': 3, '4.ª estrofe': 3, '5.ª estrofe': 4, 'n.º 3': 2, 'n.º 2': 1, 'v. 2': 1},
    23: {'1.ª estrofe': 3, '4.º verso': 1, '3.ª estrofe': 13, '2.ª estrofe': 5, '2.º verso': 1, '4.ª estrofe': 5, '6.º verso': 2},
    24: {'2.ª estrofe': 4, 'v. 2': 1, 'v. 9': 1, 'v. 10': 1, 'v. 11': 2, 'vv. 9 a 11': 1},
    26: {'1.ª publicação': 1, '2.ª estrofe': 2, '3.ª estrofe': 1, 'n.º 1': 1, 'vv. 3 e 4': 1, 'v. 1': 1, 'v. 9': 1},
    27: {'n.º 2': 6, 'Poema I': 1, 'parte VI': 4, 'partes I e II': 2, 'poema I': 6, 'Poema II': 1, 'poema II': 8, 'parte I': 1,
         'parte II': 1, 'Orpheu_ 2': 1, 'Orpheu</i> 2': 1},
    29: {'2 min': 1, 'v. 3': 2, 'verso 3': 1, 'v. 6': 1, 'v. 4': 1, 'v. 7': 1, 'v. 14': 2, 'v. 21': 1, 'poemas II e IX': 1,
         'poema XX': 4, 'poema II': 3},
    30: {'2 de fevereiro de 1991': 1, 'n.º 39': 2, 'página 2': 1, 'vv. 1 a 4': 1},
    31: {'n.º 23621': 2, 'número 2': 1, 'Orpheu 2': 4},
    32: {'22 min': 1, '1.ª publ': 4, 'n.º 36': 3, 'n.º 38': 1, 'estrofes 1 e 2': 1},
    33: {'23 min': 1, '13 de janeiro de 1935': 2, 'n.º 2': 1, 'estrofes 1': 1, 'poema X': 2, 'poema IX': 1, '1–3': 1},
    36: {'90 min': 3, '35 %': 2, '25 %': 2, '10 %': 1, '45 minutos': 1, '30 %': 1, '13 de junho de 1888': 2,
         '30 de novembro de 1935': 2, '15 de outubro de 1890': 1, '8 de março de 1914': 1, '13 de janeiro de 1935': 1,
         '3.º ano': 2, '1.ª edição': 2, 'página 2': 2, 'século XV': 1, 'D. Sebastião': 2, 'D. Henrique': 2, 'M7-F01': 4,
         'M7-F04': 3, 'M7-F06': 6, 'M7-F08': 4, 'M7-F05': 3, 'M7-F11': 1, 'M7-F34': 1, 'Orpheu</i> 2': 1},
    37: {'D. João II': 1},
    38: {'ato III': 1, 'século XVI': 1, 'D. João': 4},
    39: {'15 segundos': 1, '8 de março': 1},
    53: {'n.º 3': 2},
    55: {'3.º ano': 2},
    60: {'n.º 46': 3, 'Orpheu 2': 2, 'Orpheu_ 2': 5, '1889–1918': 2, 'Orpheu</i> 2': 1},
    61: {'D. Sebastião': 1},
    62: {'15 de janeiro de 1928': 1, '3.º ano': 2, '2.º ano': 1, '1.ª publ': 1, 'século XIX': 2, 'n.º 39': 2},
    64: {'21 de setembro de 2019': 2, '10 de setembro de 2017': 2, '12 de junho de 2018': 3, '1944–1984': 2},
    65: {'5 de novembro': 1, '3.º ano': 2},
    66: {'80 a 120 palavras': 2, '60 minutos': 1, '1.º verso': 1, '4.ª estrofe': 1, '1.ª pessoa': 1},
    67: {'90 min': 1, '80 a 120 palavras': 2, '10 a 15 minutos': 1},
    68: {'13 de janeiro de 1935': 3, 'M8-F01': 1},
    69: {'90 min': 1, '100 a 150 palavras': 2, '10 minutos': 1},
    70: {'180 a 220 palavras': 1, '1.º verso': 1, '2.º ano': 1, 'D. Sebastião': 3, 'D. João': 2},
    71: {'180 a 220 palavras': 1},
    72: {'180 a 220 palavras': 3, '90 palavras': 1},
    73: {'10 min': 1, '60 minutos': 1, '90 min': 1, '180 a 220 palavras': 2, '10 minutos': 1, '4 de agosto de 1578': 1,
         '20 de fevereiro de 1933': 1, 'v. 1': 1, 'D. Sebastião': 3, 'D. João': 1},
    74: {'40 a 60': 2, '150 a 200': 2, '80 a 120': 1},
}
# O mesmo nos painéis de projeção: (a forma da proposta, com {N} por U+00A0; as ocorrências que mudam, na lista CARTOES e no
# seletor; as que ficam, no material do relâmpago, MATERIAL).
PROPOSTA_PAINEIS = {
    40: {'13 de janeiro de 1935': ('13{N}de janeiro de{N}1935', 2, 1), '8 de março de 1914': ('8{N}de março de{N}1914', 2, 0)},
    41: {'2.ª estrofe': ('2.ª{N}estrofe', 2, 1), '3.ª estrofe': ('3.ª{N}estrofe', 2, 1),
         'versos 2 e 3': ('versos{N}2 e{N}3', 2, 0)},
    42: {'verso 15': ('verso{N}15', 2, 0), 'poema IX': ('poema{N}IX', 2, 0), 'poema II': ('poema{N}II', 2, 0)},
    43: {'2.ª estrofe': ('2.ª{N}estrofe', 4, 0), '4.ª estrofe': ('4.ª{N}estrofe', 2, 0), '3.ª estrofe': ('3.ª{N}estrofe', 2, 0)},
    44: {'4.º verso': ('4.º{N}verso', 2, 0)},
    45: {'2.ª estrofe': ('2.ª{N}estrofe', 2, 0), 'D. Sebastião': ('D.{N}Sebastião', 6, 2), 'D. João': ('D.{N}João', 2, 1)},
    46: {'1.º verso': ('1.º{N}verso', 2, 0), 'D. João': ('D.{N}João', 2, 0), 'D. Sebastião': ('D.{N}Sebastião', 2, 0)},
    48: {'2.ª estrofe': ('2.ª{N}estrofe', 2, 0), '5.ª estrofe': ('5.ª{N}estrofe', 6, 0)},
    49: {'1.ª estrofe': ('1.ª{N}estrofe', 4, 1), '2.ª estrofe': ('2.ª{N}estrofe', 2, 1),
         '3.ª estrofe': ('3.ª{N}estrofe', 4, 1), '4.ª estrofe': ('4.ª{N}estrofe', 2, 0), '6.º verso': ('6.º{N}verso', 2, 0)},
    50: {'2.ª estrofe': ('2.ª{N}estrofe', 2, 0)},
    51: {'2.ª estrofe': ('2.ª{N}estrofe', 4, 0)},
    52: {'poema I': ('poema{N}I', 4, 1), 'poema II': ('poema{N}II', 6, 0), 'parte VI': ('parte{N}VI', 2, 0)},
}
PAINEL = {f'm7/painel-m7-{f}/index.html': i for f, i in (
    ('f01', 40), ('f02', 41), ('f04', 42), ('f05', 43), ('f06', 44), ('f09', 45), ('f10', 46), ('f13', 48), ('f14', 49), ('f15', 50),
    ('f23', 51), ('f34', 52))}
# As trocas que não estão na proposta, com a razão: a meta descrição da tarefa muda com «nao_partir» (como do M1 ao M6).
EXTRAS = {73: {'durante 90 minutos, com entrega'}}
# O que a conferência deixou de fora e o detetor não conhece (a casca, as citações literais e o menu do aquecimento): quantas
# ocorrências tem o par da proposta na página («bruto») para além das que mudam.
FORA = {22: {'pt/3/">3.º ano</a>': 1}, 38: {'«Sou D. João de Portugal»': 1, '«El-Rei D. João Segundo!»': 1},
        70: {'Relembrar F09, «D. Sebastião': 1}}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a proposta pede U+00A0, traço de intervalo sem U+2060
# ou o hífen da sigla «M7-Fxx» sem a junção. As formas do M7: «v.», «vv.», «c.» e «D.» (com o nome), «n.º», «verso(s)», «século»,
# «parte(s)», «poema(s)», «estrofes», «ato», «página», «número» e «Orpheu» com o número, ordinal e nome, número e unidade (min,
# minutos, segundos, s, %, palavras, versos), as datas (o dia preso ao «de» e o ano ao «de», como na proposta do M7), os
# intervalos «N a N» com unidade, os intervalos com traço e a sigla.
MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'
PARTE = re.compile(
    r'(?<![\w.])(?:vv?|c)\. (?=\d)'
    r'|(?<![\w.])D\. (?=[A-Z])'
    r'|n\.º (?=\d)'
    r'|\b(?:versos?|séculos?|partes?|[Pp]oemas?|estrofes|ato|página|número) (?=(?:\d+|[IVXLC]+)\b)'
    r'|(?<![A-Za-zÀ-ÿ])Orpheu(?:_|</i>)? (?=\d\b)'
    r'|\d\.[ºª] (?=(?:ano|estrofes?|versos?|pessoa|publ\w*|edição)\b)'
    r'|\b\d+ (?=(?:min|minutos|segundos|s|%|palavras|versos)(?!\w))'
    r'|\b\d{1,2} de (?=(?i:' + MESES + r'))'
    r'|(?<=\d[ \xa0]de )(?i:' + MESES + r') de (?=\d{4}\b)'
    r'|\b\d+ (?=a \d)|\b\d+\xa0a (?=\d)'
    r'|\d–(?!\u2060)\d|\bM[78]-(?!\u2060)F\d')


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def gerador():
    spec = importlib.util.spec_from_file_location('cuidado_m7_20261111', ROOT / 'scripts/cuidado_m7_20261111.py')
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
    return undo_cuidado_m7_1111(rel, ler(rel))


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
    for m in re.finditer(r'<table class=\\?"apoio-tabela\b', texto):
        fim = texto.index('</table>', m.start()) + len('</table>')
        out.append(texto[m.start():fim].replace('\\"', '"'))
    return out


def tabelas_novas(rel):
    """As tabelas de apoio que esta camada pôs na página (as que não estavam na base), pela ordem da página."""
    antes = tabelas_da_pagina(base(rel))
    return [t for t in tabelas_da_pagina(ler(rel)) if t.replace(N, ' ') not in [a.replace(N, ' ') for a in antes]]


def paginas_do_m7():
    return [Path(p).relative_to(ROOT).as_posix() for p in sorted(glob.glob(str(ROOT / 'm7/**/index.html'), recursive=True))
            + sorted(glob.glob(str(ROOT / 'tarefas/m7-*/**/index.html'), recursive=True))]


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


class CuidadoM7(unittest.TestCase):
    def test_tres_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 3)
        for rel, k, cabecalho, linhas, larguras in TABELAS:
            t = Tabela(tabelas_novas(rel)[k])
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(t.tabela.get('class'), 'apoio-tabela')
                self.assertEqual(t.tabela.get('role'), 'table')
                # Sem <caption>: o título da dobra, da caixa ou o parágrafo «Pesos na avaliação:» já a nomeia.
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
                # Só a dos pesos tem larguras: a coluna do peso só leva o número (5,5 rem), como no índice do M5.
                self.assertEqual([c['attrs'].get('style') for c in topo['celulas']], larguras or [None] * len(cabecalho))
        # Nenhuma página do M7 (nem as suas tarefas, aquecimentos, grelha e correção) tem mais tabelas de apoio novas do que estas;
        # as que já lá estavam (a dos seis movimentos da F10 e a dos conceitos da F15) ficam, uma em cada lição.
        contagem = {}
        for rel, *_ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        for rel in paginas_do_m7():
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
        # Na F01, o resto do «O essencial» fica: o parágrafo das três vidas sai, e a dobra continua a chamar-se como os retornos
        # dos cartões lhe chamam («vê «As três vidas» em «O essencial»»).
        f01 = cartoes(ler(F01))[2]['html']
        self.assertNotIn('<b>Caeiro</b>: Lisboa, 1889', f01)
        self.assertEqual(f01.count('<summary>As três vidas, segundo a carta</summary>'), 1)
        self.assertIn('«As três vidas»', json.dumps(cartoes(ler(F01)), ensure_ascii=False))
        # Na F23, a caixa «Recorda» fica com a tabela e a frase final; os quatro termos já não vêm em negrito num parágrafo.
        f23 = cartoes(ler(F23))[14]['html']
        self.assertNotIn('<b>Ode</b>:', f23)
        self.assertIn('<th scope="row" role="rowheader"><i>Carpe diem</i></th>', f23)
        # No índice, a tabela dos pesos fica em «Como se cumpre uma unidade», entre o rótulo e a frase da grelha.
        indice = ler(INDICE)
        self.assertIn('não exige repetir uma produção já realizada.<p>Pesos na avaliação:</p><table class="apoio-tabela" role="table">', indice)
        self.assertIn('</table><p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20.</p></div></details>', indice)
        self.assertEqual(indice.count('class="avaliacao-tarefas"'), 1)
        self.assertNotIn('Pesos na avaliação: tarefa da Unidade 2', indice)
        # O banco das provas rápidas não leva tabelas.
        self.assertNotIn('apoio-tabela', indice.split('var U=', 1)[1])

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
        # As outras páginas do M7 ficam como estavam: só a F10 e a F15 carregavam a folha (na sua versão), e continuam.
        for rel in paginas_do_m7():
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
        # Achado 6: no guia, «Três antes de mim» numa lista ordenada (o mesmo trecho, letra a letra, do guia do M5).
        regra = ('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a '
                 'rubrica;</li><li>pergunta ao teu par de trabalho.</li></ol>Só depois levantas o braço.</div>')
        self.assertEqual(ler(GUIA).count(regra), 1)
        self.assertIn(regra, ler('m5/guia-da-tarefa-m5/index.html'))
        self.assertNotIn('1) relê o enunciado', ler(GUIA))
        # Achado 18: na F10, o plano do texto, ponto a ponto, numa lista de sete itens, cada um com o «;» ou o ponto que tinha.
        plano = ('<details><summary>O plano do texto, ponto a ponto</summary><div><ul><li>A tese com condição na primeira frase;</li>'
                 '<li>um movimento que dá razão ao outro lado e vira (R ou C);</li><li>mais um movimento (N, M ou P);</li><li>um verso '
                 'exato de <i>Mensagem</i>, explicado;</li><li>um facto datado separado do sentido que o poema lhe dá, ou o confronto com '
                 'Garrett ou com Reis;</li><li>uma conclusão que volta à tese sem a copiar;</li><li>as letras dos movimentos na '
                 'margem.</li></ul></div></details>')
        f10 = cartoes(ler(F10))
        self.assertEqual(f10[1]['rot'], 'O essencial')
        self.assertIn(plano, f10[1]['html'])
        self.assertEqual(sum(plano in c.get('html', '') for c in f10), 1)
        # O texto é o mesmo, letra a letra: os sete itens, de seguida, dão o parágrafo de antes.
        antes = cartoes(base(F10))[1]['html']
        itens = re.findall(r'<li>(.*?)</li>', plano)
        self.assertEqual(len(itens), 7)
        self.assertIn('<summary>O plano do texto, ponto a ponto</summary><div><p>' + ' '.join(itens) + '</p></div></details>', antes)
        # Achado 54: no portefólio, os dezoito nomes de ficheiro em <code> (os nove que estavam em texto simples e os nove que já
        # estavam), sem U+2011, U+2060 nem U+00A0 (o aluno copia-os); os compridos só mudam de linha depois de «M7_», de «U1_» e de
        # «aula_» (<wbr>), como no portefólio do M5.
        port = ler(PORTEFOLIO)
        linhas = re.findall(r'<tr><td>(.*?)</td><td>', port)
        self.assertEqual(len(linhas), 18)
        self.assertTrue(all(re.fullmatch(r'<code>M7_[^<\u2011\u2060\xa0]*(?:<wbr>[^<\u2011\u2060\xa0]*)*</code>', l) for l in linhas), linhas)
        nomes = [f'M7_<wbr>U{u}_<wbr>{n}' for u in (1, 2, 3) for n in ('aula_<wbr>&lt;dia-mês&gt;', 'pergunta', 'o-que-aprendi')]
        self.assertEqual(len(nomes), 9)
        for nome in nomes + ['M7_<wbr>cartao-do-percurso', 'M7_<wbr>Prova-escrita']:
            self.assertEqual(port.count(f'<td><code>{nome}</code></td>'), 1, nome)
        for nome in ('M7_capa', 'M7_Tarefa1', 'M7_Tarefa2', 'M7_Tarefa3', 'M7_Revisao1', 'M7_Revisao2', 'M7_balanco'):
            self.assertEqual(port.count(f'<td><code>{nome}</code></td>'), 1, nome)
        # Os nomes são os mesmos, letra a letra, pela mesma ordem: sem as marcas, a primeira coluna é a de antes.
        limpa = lambda s: re.sub(r'</?code>|<wbr>', '', s)
        self.assertEqual([limpa(l) for l in linhas], [limpa(l) for l in re.findall(r'<tr><td>(.*?)</td><td>', base(PORTEFOLIO))])
        self.assertEqual(port.count('<wbr>'), 9 * 2 + 3 + 2)
        self.assertIn('code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
                      'td code{white-space:nowrap}\n', port)
        self.assertEqual(port.count('td code{white-space:nowrap}'), 1)
        self.assertIn('td code{white-space:nowrap}', ler('m5/portefolio-do-modulo-m5/index.html'))
        # A tabela do portefólio fica como estava (o cabeçalho e a segunda coluna não mudam).
        self.assertIn('<table><tr><th style="width:36%">Nome do ficheiro</th><th>O que é</th></tr>', port)

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
        # A casca das lições (migalhas, «Estás em», título escondido e sigla do rodapé) fica para o molde, como do M1 ao M6.
        self.assertEqual(len(C.CASCA_NO_MOLDE), 16)
        self.assertEqual(C.CASCA_NO_MOLDE, sorted(Path(p).relative_to(ROOT).as_posix() for p in glob.glob(str(ROOT / 'm7/licao-*/index.html'))
                                                  if 'licao-m7-f07' not in p))
        for rel in C.CASCA_NO_MOLDE:
            texto = ler(rel)
            n = re.search(r'licao-m7-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                for trecho in (f'Estás em: Lição M7-{n}', f'<h1 class="c-sr">Lição M7-{n}', f'Português 2026/2027. Lição M7-{n},',
                               '/pt/3/">3.º ano</a>', '>Módulo 7: Lírica pessoana</a>', f'titulo:"Lição M7-{n}"'):
                    self.assertEqual(texto.count(trecho), 1, trecho)
        # Nas outras páginas, as migalhas contam (como na proposta final): o «3.º ano» fica preso nas migalhas e no cabeçalho.
        for rel, cab in ((INDICE, 'Português, 3.º' + N + 'ano, percurso do módulo'), (GUIA, 'Guia da tarefa, 3.º' + N + 'ano'),
                         ('m7/mapa-do-modulo-m7/index.html', 'Português · 3.º' + N + 'ano · Mapa do módulo'),
                         (PORTEFOLIO, 'Português · 3.º' + N + 'ano · Módulo 7'),
                         ('m7/visita-casa-fernando-pessoa/index.html', 'Caderno de campo, 3.º' + N + 'ano')):
            self.assertIn('/pt/3/">3.º' + N + 'ano</a>', ler(rel), rel)
            self.assertIn(cab, ler(rel), rel)
            self.assertNotIn('3.º ano', sem_atributos_nem_desenhos(ler(rel)), rel)
        # Os intervalos com traço levam a junção; a sigla das ligações do mapa e das lições também (os href, em minúsculas, ficam).
        mapa = ler('m7/mapa-do-modulo-m7/index.html')
        self.assertEqual(len(re.findall(r'>[Ll]ição M7-' + WJ + r'F\d\d<', mapa)), 22)
        self.assertNotRegex(mapa, r'>[Ll]ição M7-F\d\d<')
        self.assertIn('licao-m7-f01/">Lição M7-' + WJ + 'F01</a>', mapa)
        self.assertIn('(estrofes' + N + '1–' + WJ + '3)', ler('m7/m7-quatro-vozes-um-problema/index.html'))
        self.assertEqual(ler('m7/santa-rita-fato/index.html').count('(1889–' + WJ + '1918)'), 2)
        self.assertEqual(ler('m7/variacoes-rotulos/index.html').count('(1944–' + WJ + '1984)'), 2)
        self.assertIn('lições M7-' + WJ + 'F07, F08, F09 e F11', ler(F10))
        self.assertIn('(lição M8-' + WJ + 'F01)', ler('tarefas/m7-u2/aquecimento/index.html'))
        # As datas com o dia preso ao «de» e o ano ao «de», como na proposta do M7 (e no M5).
        f01 = ler(F01)
        self.assertEqual(len(inteiras(f01, '13' + N + 'de janeiro de' + N + '1935')), 5)
        self.assertEqual(len(inteiras(f01, '8' + N + 'de março de' + N + '1914')), 3)
        self.assertEqual(len(inteiras(f01, '8' + N + 'de março')), 4)
        self.assertNotRegex(sem_atributos_nem_desenhos(ler('m7/mapa-do-modulo-m7/index.html')), r'\d de (?:' + MESES + r') de \d{4}')
        # Os vídeos: o botão muda, o data-titulo (que vira o title do leitor) fica; nos «alt», os espaços ficam normais.
        f02 = ler('m7/licao-m7-f02/index.html')
        self.assertEqual(f02.count('(30 s)'), 1)
        self.assertEqual(f02.count('(30' + N + 's)'), 1)
        self.assertRegex(f02, r'data-titulo=\\"[^"]*\(30 s\)\\"')
        f09 = ler('m7/licao-m7-f09/index.html')
        self.assertRegex(f09, r'alt=\\"D\. Sebastião \(Cristóvão de Morais, c\. 1571-1574')
        self.assertIn('D.' + N + 'Sebastião (Cristóvão de Morais, c.' + N + '1571-1574, MNAA)', f09)
        # As duas citações literais de «O leme e o retrato» ficam como no original; o resto da página leva o espaço preso.
        leme = ler('m7/mostrengo-leme-ramos/index.html')
        self.assertIn('«Sou D. João de Portugal»', leme)
        self.assertIn('«El-Rei D. João Segundo!»', leme)
        self.assertEqual(leme.count('D.' + N + 'João'), 4)
        self.assertEqual(leme.count('D. João'), 2)
        # A tarefa da M7-U3: os números do molde, pelo gerador (a ligação à grelha fica como estava: a proposta não a pede).
        t = ler('tarefas/m7-u3/index.html')
        self.assertIn('Antes de escrever · 10' + N + 'min · em cartões, com consulta', t)
        self.assertIn('Tarefa individual · Unidade 3 · 90' + N + 'min</p>', t)
        self.assertNotIn('90 min', t)
        self.assertIn('<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>', t)
        # As tarefas da M7-U1 e da M7-U2 (sem gerador): o cabeçalho e o número de palavras.
        for u, palavras_ in ((1, '80' + N + 'a' + N + '120' + N + 'palavras'), (2, '100' + N + 'a' + N + '150' + N + 'palavras')):
            t = ler(f'tarefas/m7-u{u}/index.html')
            self.assertIn(f'Unidade {u} · 90' + N + 'min</p>', t)
            self.assertEqual(t.count(palavras_), 2)

    def test_paineis_seguem_as_licoes(self):
        # Os painéis de projeção das lições do M7 mostram os enunciados dos cartões: onde um mudou, o painel muda igual, na lista
        # (CARTOES) e no seletor; são os 12 achados dos painéis (40 a 46 e 48 a 52), e mais nenhum painel muda.
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
        # Em todos os painéis de projeção do M7, cada enunciado da lista é o do cartão da lição (com ou sem os marcadores de
        # negrito e de itálico e com as lacunas como «…»), e o seletor mostra-o (inteiro ou cortado), com o itálico em <i>.
        conferidos = mudados = 0
        for p in sorted(glob.glob(str(ROOT / 'm7/painel-m7-*/index.html'))):
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
        self.assertGreater(conferidos, 200)
        # Cada enunciado mudado deu duas trocas no painel (a lista e o seletor), salvo onde o seletor corta o enunciado antes da
        # referência.
        trocas_paineis = sum('/painel-' in t['ficheiro'] for t in TROCAS)
        self.assertLessEqual(mudados, trocas_paineis)
        self.assertGreaterEqual(2 * mudados, trocas_paineis)
        # O painel da F11 (achado 47, recusado: só tinha ocorrências no material) fica como estava.
        self.assertNotIn('m7/painel-m7-f11/index.html', MANIFESTO['files'])

    def test_banco_segue_as_licoes(self):
        # As cópias dos cartões no banco das provas rápidas do índice (var U) mudam como as lições de onde vêm: cada cópia que era
        # igual a um cartão da sua lição antes desta camada continua igual depois, campo a campo.
        copias, copias_antes = banco(ler(INDICE)), banco(base(INDICE))
        self.assertEqual(len(copias), len(copias_antes))
        iguais = 0
        for copia, antes in zip(copias, copias_antes):
            licao = f"m7/licao-{antes.get('_l')}/index.html"
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
        self.assertGreater(iguais, 30)
        # Fora das páginas do M7, das suas tarefas e dos dados dos geradores, a camada não toca em nada (as sessões do Exame não
        # repetem nenhum trecho mudado: tests/test_exame_alignment.py continua a comparar as cópias com as lições, letra a letra).
        self.assertEqual(sorted(f for f in MANIFESTO['files'] if not f.startswith(('m7/', 'tarefas/m7-', 'docs/pedagogia/'))), [])
        self.assertEqual(C.NOTAS, [])

    def test_fora_de_ambito_e_recusados(self):
        achados = {n for t in TROCAS for n in achados_da_troca(t)}
        self.assertFalse(RECUSADOS & achados)
        self.assertFalse(set(FORA_DE_AMBITO) & achados)
        self.assertFalse(RECUSADOS & CONFIRMADOS)
        # 4, 56, 57, 58 e 59: os diapositivos, as provas rápidas e os questionários ficam de fora (como do M1 ao M5), e também a
        # página «todos» (63, recusada) e as duas de reencaminhamento (0 e 3): nenhuma está na camada, nem no gerador.
        fora = sorted(FORA_DE_AMBITO.values()) + ['m7/todos/index.html', 'm7/caeiro-o-rio-e-o-olhar/index.html',
                                                   'm7/campos-tabacaria-sonhar-e-viver/index.html']
        for rel in fora:
            with self.subTest(pagina=rel):
                self.assertTrue((ROOT / rel).is_file())
                self.assertNotIn(rel, MANIFESTO['files'])
                self.assertNotIn(rel, {x['ficheiro'] for x in C.ACHADOS_B + C.achados_ac()})
                self.assertEqual(base(rel), ler(rel))
        # Nenhuma página de diapositivos, de provas rápidas, de questionários ou «todos», de módulo nenhum, está na camada.
        self.assertFalse([f for f in MANIFESTO['files'] if re.search(r'/(?:diapositivos|prova-[abc]|questionarios|todos)/', f)])
        # 5: a nota de «Ler a fundo» sobre os valores fica em parágrafo, sem tabela.
        self.assertNotIn('apoio-tabela', ler('m7/gram-valores-pessoa/index.html'))
        self.assertNotIn('m7/gram-valores-pessoa/index.html', MANIFESTO['files'])
        # 20 e 28: as lições sem achado B (a F07) e os cartões recusados ficam sem tabela nem lista novas.
        self.assertNotIn('m7/licao-m7-f07/index.html', MANIFESTO['files'])
        for rel in MANIFESTO['files']:
            if rel.startswith('m7/licao-') and rel not in (F01, F10, F23):
                self.assertEqual(ac_aplicadas(rel, base(rel)), base(rel), rel)
        # 34 e 35: no mapa, os pesos ficam em frase (só com os espaços que não quebram do achado 36), sem tabela.
        mapa = ler('m7/mapa-do-modulo-m7/index.html')
        self.assertNotIn('apoio-tabela', mapa)
        self.assertIn('(35' + N + '% e 25' + N + '%), provas rápidas (10' + N + '%,', mapa)
        self.assertIn('prova escrita de 45' + N + 'minutos (30' + N + '%).', mapa)
        # 47: o painel da F11 fica como estava.
        self.assertEqual(base('m7/painel-m7-f11/index.html'), ler('m7/painel-m7-f11/index.html'))

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, cab, _, _ in TABELAS for c in cab}
        self.assertEqual(cabecalhos, {'Elemento', 'Peso', 'Heterónimo', 'Vida', 'Termo', 'O que é'})
        permitidas = {p for c in cabecalhos for p in palavras(c)}
        # O que sai: os números «1) 2) 3)» que a lista numerada do guia substitui.
        saem = {6: {'1', '2', '3'}}
        css = [t for t in TROCAS if t['novo'].startswith('<link rel="stylesheet"')]
        self.assertEqual(sorted(t['ficheiro'] for t in css), sorted(C.COM_TABELA))
        estilo = [t for t in TROCAS if 'code{white-space:nowrap}' in t['novo']]
        self.assertEqual(len(estilo), 1)
        chaves = [t for t in TROCAS if '"nao_partir' in t['novo'] and '"nao_partir' not in t['antigo']]
        self.assertEqual([t['ficheiro'] for t in chaves], ['docs/pedagogia/tarefas-escolha/m7-u3.json'])
        for t in TROCAS:
            if t in css or t in estilo or t in chaves:
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
                self.assertTrue(t['achado'].startswith('11/11/2026: decisão 152 (cuidado em todas as lições), varredura do M7'))
        for c in cabecalhos:
            self.assertIsNone(PROIBIDAS.search(c), c)
        # Nas tabelas, o texto é o de antes, pela mesma ordem: sem as marcas, sem a pontuação que a tabela substitui e sem os
        # cabeçalhos, as palavras da tabela são as do parágrafo, uma a uma.
        soltas = lambda s: re.findall(r'[\wÀ-ÿ%]+', visivel(s).lower())
        for t in TROCAS:
            if achados_da_troca(t)[0] in A and t not in css:
                cab = [p for c in next(c for r, _, c, _, _ in TABELAS if r == t['ficheiro']) for p in soltas(c)]
                novas = soltas(re.sub(r'<thead.*?</thead>| data-label=\\?"[^"\\]*\\?"', '', t['novo']))
                with self.subTest(tabela=t['ficheiro']):
                    self.assertEqual(novas, soltas(t['antigo']))
                    self.assertTrue(cab)
        # As trocas B só mudam espaços (U+00A0) e põem a junção (U+2060); nenhuma muda uma letra.
        for t in TROCAS:
            if '(B)' in t['achado'] and t not in chaves:
                with self.subTest(local=t['local']):
                    self.assertEqual(t['novo'].replace(N, ' ').replace(WJ, ''), t['antigo'])
        # Nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, data-titulo, <title>, chaves JSON, nem da «frase» de
        # um sublinhar, das «palavras» de um cartão frase ou dos «passos» de um ordenar.
        for rel in MANIFESTO['files']:
            with self.subTest(contextos=rel):
                conta = lambda texto: sum(p.count(N) + p.count(WJ) for p in contextos_proibidos(texto))
                self.assertEqual(conta(ler(rel)), conta(base(rel)))
        # O detetor dos campos dos exercícios apanha-os: a «frase» do sublinhar da F01 com a data da carta fica como estava.
        f01 = ler(F01)
        s = next(m.start() for m in re.finditer(re.escape('13 de janeiro de 1935'), f01)
                 if C.fora_de_alcance(f01, m.start()) == 'frase de um cartão sublinhar')
        self.assertEqual(f01.count('13 de janeiro de 1935'), 1)
        self.assertEqual(f01[s:s + 21], '13 de janeiro de 1935')

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
        for partido in ('v. 7', 'vv. 3 e 4', 'c. 1571-1574', 'D. Sebastião', 'D. João II', 'n.º 36', 'verso 14', 'versos 2 e 3', 'século XV',
                        'parte VI', 'partes I e II', 'poema IX', 'Poema II', 'poemas II e IX', 'estrofes 1 a 5', 'ato III', 'página 2',
                        'número 2', 'Orpheu 2', 'Orpheu_ 2', 'Orpheu</i> 2', '3.º ano', '2.ª estrofe', '1.ª publ', '90 minutos', '10 min',
                        '30 s', '35 %', '15 segundos', '8 palavras', '12 a 16 versos', '80 a 120 palavras', '80' + N + 'a 120',
                        '13 de janeiro de 1935', '13' + N + 'de janeiro de 1935', '8 de março', '1889–1918', 'M7-F10', 'M8-F01'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for x in C.ACHADOS_B:
            for _, novo, _ in x['pares']:
                self.assertIsNone(PARTE.search(C.j(novo) + '0'), novo)

    def test_camada_fechada_reversivel_e_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m7_20261111.json', '--manifesto', MANIFESTO_REL,
                            '--verificar'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), (450, 59))
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertEqual(len(m['base_commit']), 40)
        self.assertTrue(m['_nota'].startswith('11/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M7'))
        self.assertIn('cuidado_m6_20261108', m['_nota'])
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
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_m7_1111(rel, atual)
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
                # A camada de baixo (a decisão 152 no M6) continua a desfazer-se por baixo desta.
                undo_cuidado_m6_0811(rel, atual)
        # Os 61 achados que entram estão todos na camada; os 5 que ficam de fora e os 9 recusados, não.
        achados = {n for t in TROCAS for n in achados_da_troca(t)}
        self.assertEqual(achados, APLICADOS)
        self.assertEqual((len(A), len(B), len(C_), len(CONFIRMADOS)), (3, 60, 3, 66))
        self.assertEqual((len(APLICADOS), len(B_PAGINAS), len(B_PAINEIS), len(FORA_DE_AMBITO), len(RECUSADOS)), (61, 43, 12, 5, 9))
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'A'}), sorted(A))
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'C'}), sorted(C_))
        # 52 achados nas páginas do M7 e 9 nas das tarefas (o 66 e o 74 são do mesmo aquecimento).
        sitio = {x['i']: x['ficheiro'] for x in C.achados_ac() + C.ACHADOS_B}
        sitio.update({i: rel for rel, i in PAINEL.items()})
        self.assertEqual(sorted(sitio), sorted(APLICADOS))
        self.assertEqual(sum(f.startswith('m7/') for f in sitio.values()), 52)
        self.assertEqual(sum(f.startswith('tarefas/') for f in sitio.values()), 9)
        # A e C antes de B, em cada ficheiro.
        for rel in m['files']:
            ordem = ['B' if '(B)' in t['achado'] and '"nao_partir' not in t['novo'] else 'AC' for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual(ordem, sorted(ordem, key=lambda x: x != 'AC'), rel)
        # No topo da cadeia, logo por cima da decisão 152 no M6.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        self.assertEqual(verificar_camadas.LAYERS[0], ('cuidado_m7_20261111', 'cuidado-m7-edits-20261111'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        self.assertEqual(len(verificar_camadas.LAYERS), 41)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 41)
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m6_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m7_1111(path, text)'), corpo.index('_CUIDADO_M6_0811.get('))
        self.assertLess(auditoria.index('def undo_cuidado_m7_1111'), auditoria.index('def undo_cuidado_m6_0811'))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m7-edits-20261111.json'), sala.index('cuidado-m6-edits-20261108.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes da decisão 152 no M6, logo a seguir a --verificar.
        meu, m6 = MANIFESTO_REL, 'tests/fixtures/cuidado-m6-edits-20261108.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + m6 not in linha:
                    continue
                linhas += 1
                self.assertIn(f'--verificar --desfazer-antes {meu} --desfazer-antes {m6}', linha, wf)
        # As 20 cadeias em que a decisão 152 no M6 se desfaz (a conferência da própria camada do M6, que só tem esta por cima, vem abaixo).
        self.assertEqual(linhas, 20)
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m6_20261108.json --manifesto {m6} --verificar --desfazer-antes {meu}\n',
                      tarefas)
        # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça.
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if not linha.lstrip().startswith('#') and '--desfazer-antes ' + meu in linha:
                    self.assertIn('--verificar --desfazer-antes ' + meu, linha, wf)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --verificar '
                      f'--desfazer-antes {meu} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e da decisão 152 no M1 conferem as cadeias com frases partidas em várias linhas (e já
            # exigem esta camada à cabeça); ficam de fora pela mesma razão.
            if p.name in ('test_cuidado_m7.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + m6), plano.count(f'--desfazer-antes {meu} --desfazer-antes {m6}'))
        self.assertIn(f"(ROOT/'{meu}',ROOT/'{m6}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM7['), texto.index('((cuidadoM6['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM7[rel]'), corpo.index('((cuidadoM6[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M7.read_text'), gerador_148.index('CUIDADO_M6.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1 ao M6.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m7_20261111.json --manifesto {meu} --verificar\n', tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m7.py' -v", wf)
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m6.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m7.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m7_20261111.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_dos_dados(self):
        # A tarefa, a grelha e a correção da M7-U3 e os três aquecimentos mudam também nos dados, que estão nesta camada.
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/')}
        self.assertEqual(dados, {'docs/pedagogia/tarefas-escolha/m7-u3.json', 'docs/pedagogia/aquecimentos/m7-u1.json',
                                 'docs/pedagogia/aquecimentos/m7-u2.json', 'docs/pedagogia/aquecimentos/m7-u3.json',
                                 'docs/pedagogia/grelhas-tarefas-20261027.json'})
        d = json.loads(ler('docs/pedagogia/tarefas-escolha/m7-u3.json'))
        self.assertIs(d['nao_partir'], True)
        # As chaves do M6 («nao_partir_grelha», «nao_partir_valores») não entram no M7: a proposta não as pede.
        self.assertNotIn('nao_partir_grelha', d)
        self.assertNotIn('tabela', d['aquecer'])
        grelhas = json.loads(ler('docs/pedagogia/grelhas-tarefas-20261027.json'))['tarefas']
        self.assertEqual(sorted(s for s, t in grelhas.items() if t.get('nao_partir_valores')), ['m6-u1', 'm6-u2'])
        self.assertNotIn('nao_partir', grelhas['m7-u3'])
        self.assertFalse(any(c.get('max_em_listas') for c in grelhas['m7-u3']['criterios']))
        # Nos dados das grelhas, esta camada só mexe na entrada m7-u3 (as outras entradas ficam iguais, campo a campo).
        grelhas_antes = json.loads(base('docs/pedagogia/grelhas-tarefas-20261027.json'))['tarefas']
        self.assertEqual({s for s in grelhas if grelhas[s] != grelhas_antes[s]}, {'m7-u3'})
        # Os dados dizem o mesmo que diziam, letra a letra, salvo os espaços que não quebram e a chave do gerador.
        for rel in sorted(dados):
            solto = lambda s: s.replace(N, ' ').replace(WJ, '')
            antes, depois = json.loads(solto(base(rel))), json.loads(solto(ler(rel)))
            if rel.endswith('tarefas-escolha/m7-u3.json'):
                self.assertIs(depois.pop('nao_partir'), True)
            self.assertEqual(depois, antes, rel)
        with tempfile.TemporaryDirectory() as tmp:
            for pasta, comando in (('te', 'scripts/tarefas_escolha.py'), ('gr', 'scripts/grelhas_tarefas.py'), ('aq', 'scripts/aquecimentos.py')):
                r = subprocess.run([sys.executable, comando, '--saida', str(Path(tmp) / pasta)], cwd=ROOT, capture_output=True, text=True,
                                   encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for esperada in ('te/tarefas/m7-u3/index.html', 'gr/tarefas/m7-u3/grelha/index.html', 'gr/tarefas/m7-u3/correcao/index.html',
                             'aq/tarefas/m7-u1/aquecimento/index.html', 'aq/tarefas/m7-u2/aquecimento/index.html',
                             'aq/tarefas/m7-u3/aquecimento/index.html'):
                self.assertIn(esperada, geradas)
            # As tarefas da M7-U1 e da M7-U2 não são das de escolha: não têm gerador, e mudam só na camada.
            self.assertFalse([g for g in geradas if g.startswith(('te/tarefas/m7-u1/', 'te/tarefas/m7-u2/', 'gr/tarefas/m7-u1/', 'gr/tarefas/m7-u2/'))])
            # O gerador das grelhas não acrescenta outra ligação à tarefa.
            self.assertFalse([g for g in geradas if g.startswith('gr/') and g.count('/') == 3])
            self.assertGreater(len(geradas), 50)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel.split('/', 1)[1]).read_bytes())
        # As páginas geradas que a camada muda são estas seis; as tarefas sem gerador são as outras duas.
        self.assertEqual(sorted(f for f in MANIFESTO['files'] if f.startswith('tarefas/')),
                         ['tarefas/m7-u1/aquecimento/index.html', 'tarefas/m7-u1/index.html', 'tarefas/m7-u2/aquecimento/index.html',
                          'tarefas/m7-u2/index.html', 'tarefas/m7-u3/aquecimento/index.html', 'tarefas/m7-u3/correcao/index.html',
                          'tarefas/m7-u3/grelha/index.html', 'tarefas/m7-u3/index.html'])
        # Nenhuma lição do M7 é gerada: o gerador das lições não conhece nenhuma.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from licoes_20261101 import LESSONS
        finally:
            sys.path.pop(0)
        self.assertFalse([x['id'] for x in LESSONS if x['id'].startswith('m7-')])


if __name__ == '__main__':
    unittest.main()
