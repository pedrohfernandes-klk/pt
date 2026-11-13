"""12/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M9. Camada literal cuidado_m9_20261112
(scripts/cuidado_m9_20261112.json, gerada por scripts/cuidado_m9_20261112.py; manifesto tests/fixtures/cuidado-m9-edits-20261112.json),
a mais recente, por cima da decisão 152 no M8 (cuidado_m8_20261112).

Este teste confere, no modelo de tests/test_cuidado_m1.py a tests/test_cuidado_m8.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices, os geradores das camadas de baixo que mexem no índice do M9
  e a leitura histórica das tarefas (scripts/tarefas_claras_historico.py);
* cada um dos 44 achados confirmados que entram: as 7 tabelas novas (7 achados A), com o cabeçalho (th scope=col), a primeira
  coluna (th scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato, no
  cartão e no sítio certos; os 4 casos do mesmo tipo (C), com o texto exato; os 33 achados B (27 em páginas, 5 em painéis de
  projeção e 1 nas notas do docente da F14), com a contagem certa de cada par da proposta final (com a palavra inteira e fora das
  cadeias maiores dos outros pares) e a forma da proposta, sem nenhuma ocorrência que se parta fora do que fica de fora (os «alt»,
  o data-titulo dos vídeos, a casca das lições, que fica para o molde, e o que a conferência deixou com o contexto dos pares: os
  excertos do romance, as citações e as peças dos exercícios);
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e mais nenhuma do M9;
* que os 6 achados dos diapositivos, das provas rápidas, dos questionários e da página «todos» (20, 48 a 51 e 56) ficam de fora,
  como do M1 ao M8, que os 2 dos painéis da F04 e da F10 (41 e 44), só com ocorrências no material do relâmpago e nas pistas do
  «Quem sou eu?», também, e que nenhum dos 8 achados recusados (7, 8, 12, 13, 14, 16, 17 e 18) entrou;
* as regras do texto: as tabelas e as listas só usam texto que já estava na página (e os cabeçalhos); nada de «professor», «jogar»,
  «jogo», «ficha», «folha», «—» ou «·» novos; nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>,
  data-titulo, chaves JSON, nem da «frase» de um sublinhar, das «palavras» de um cartão frase ou dos «passos» de um ordenar; nas
  passagens mudadas, nenhuma referência nem número que se parta; nenhuma letra muda;
* que as tarefas da M9-U1 e da M9-U2 saem iguais dos dados e do gerador (e as dos outros módulos não mudam), que as lições geradas
  (F14 a F16) e as suas notas saem iguais das fontes, que os painéis de projeção seguem os enunciados das lições (com o material
  do relâmpago e as pistas do «Quem sou eu?» como estavam), que as cópias do banco das provas rápidas seguem os cartões e que a
  cópia do cartão 11 da F01 nas sessões do Exame segue a lição."""
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
from auditoria_20261028 import undo_cuidado_m9_1112, undo_cuidado_m8_1112  # noqa: E402
# 12/11/2026: por cima desta camada fica a decisão 152 no Exame e nas páginas transversais (camada cuidado_exame_20261112).
from auditoria_20261028 import undo_cuidado_exame_1112  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m9_20261112.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m9-edits-20261112.json'
# 12/11/2026: o manifesto da camada de cima (a decisão 152 no Exame e nas páginas transversais).
EX = 'tests/fixtures/cuidado-exame-edits-20261112.json'
# 12/11/2026: o manifesto da camada que fica por cima dela (a ligação «Treinos» na página principal do Exame).
LT = 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json'
# 12/11/2026: o manifesto da camada que fica por cima dela (as provas em cartões com os documentos oficiais).
PO = 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
# 12/11/2026: o manifesto da camada que fica por cima dela (as duas tarefas do M3 mais fáceis de fazer).
TF = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
# 13/11/2026: por cima das tarefas do M3 ficam as tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
# 13/11/2026: por cima das tarefas do M1 ficam as tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
# 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
T6 = 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'
T5 = 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
T1 = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
# As camadas de baixo com que esta se cruza nos testes: a decisão 152 no M8 e a revisão dos enunciados das tarefas (#192).
M8 = json.loads((ROOT / 'tests/fixtures/cuidado-m8-edits-20261112.json').read_text('utf-8'))
CLARAS = json.loads((ROOT / 'tests/fixtures/tarefas-claras-edits-20261110.json').read_text('utf-8'))['files']
# A camada assenta no ramo da decisão 152 no M8 (pedido #195, ainda por publicar), já com o main 40f9505c dentro.
# 12/11/2026: o M8 foi publicado no main em 89957690 (#195), com a mesma árvore de 0c85d555; a base passa a ser esse commit do main, sem mudar resumos nem trocas.
BASE_COMMIT = '899576905d085e9552a70fe82d050c13f78dda2f'
NBSP, WJ = '\xa0', '⁠'
N = NBSP
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
A = {0, 1, 2, 3, 4, 5, 6}
C_ = {9, 10, 11, 15}
# Os achados B dos painéis de projeção que seguem as lições (F01, F02, F03, F05 e F07), o das notas do docente da lição gerada
# F14 (45) e os das outras páginas (os cartões das lições F11, F12 e F13 estão em m9/recursos/f11.js, f12.js e f13.js).
B_PAINEIS = {38, 39, 40, 42, 43}
B_NOTAS = {45}
B_PAGINAS = {19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 46, 47, 52, 53, 54, 55, 57, 58, 59}
# Ficam de fora, por decisão já tomada para todos os módulos (como do M1 ao M8): os diapositivos (20), as três provas rápidas
# (48, 49 e 50), os questionários (51) e a página «todos» (56). Confirmados pela conferência, mas essas páginas não mudam.
FORA_DE_AMBITO = {20: 'm9/diapositivos/index.html', 48: 'm9/prova-a/index.html', 49: 'm9/prova-b/index.html',
                  50: 'm9/prova-c/index.html', 51: 'm9/questionarios/index.html', 56: 'm9/todos/index.html'}
# E os dois painéis de projeção em que as ocorrências confirmadas estão todas no material do relâmpago (MATERIAL) e nas pistas do
# «Quem sou eu?» (ATL), que não mudam.
SO_MATERIAL = {41: 'm9/painel-m9-f04/index.html', 44: 'm9/painel-m9-f10/index.html'}
B = B_PAINEIS | B_NOTAS | B_PAGINAS | set(FORA_DE_AMBITO) | set(SO_MATERIAL)
CONFIRMADOS = A | B | C_
APLICADOS = CONFIRMADOS - set(FORA_DE_AMBITO) - set(SO_MATERIAL)
RECUSADOS = {7, 8, 12, 13, 14, 16, 17, 18}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)
INDICE, GUIA, MAPA = 'm9/index.html', 'm9/guia-da-tarefa-m9/index.html', 'm9/mapa-do-modulo-m9/index.html'
F01, F02, F03, F04, F07, F10 = (f'm9/licao-m9-{n}/index.html' for n in ('f01', 'f02', 'f03', 'f04', 'f07', 'f10'))
F11_JS, F12_JS, F13_JS = (f'm9/recursos/{n}.js' for n in ('f11', 'f12', 'f13'))
PORTEFOLIO = 'm9/portefolio-do-modulo-m9/index.html'
SESSOES = 'assets/exame/sessoes.json'
NOTAS_F14 = 'm9/painel-m9-f14/index.html'
GERADAS = ('m9-f14', 'm9-f15', 'm9-f16')

PESOS = [['Tarefa da Unidade 1', '30' + N + '%'], ['Tarefa da Unidade 2', '30' + N + '%'], ['Provas rápidas', '10' + N + '%'],
         ['Prova escrita', '30' + N + '%']]
LARGURAS = ['width:auto', 'width:5.5rem']
# (página, índice da tabela nova na página, cabeçalho, linhas, larguras): o texto de cada célula, como se lê.
TABELAS = [
    # achados 0, 1 e 2: os pesos no índice, no guia e no mapa do módulo, com a coluna do peso estreita (como no M5, no M7 e no M8)
    (INDICE, 0, ['Elemento', 'Peso'], PESOS, LARGURAS),
    (GUIA, 0, ['Elemento', 'Peso'], PESOS, LARGURAS),
    (MAPA, 0, ['Elemento', 'Peso'], PESOS, LARGURAS),
    # achado 3, F01, «Para entender», dobra «Recorda»
    (F01, 0, ['Noção', 'O que é'],
     [['Tempo histórico', 'a época em que a história se passa'],
      ['Organização temporal do relato', 'a ordem em que o narrador apresenta os acontecimentos, com recuos e avanços'],
      ['Tempo da narração', 'o momento de onde a voz conta, que pode distinguir-se da época narrada'],
      ['Prolepse', 'o narrador adianta o que ainda vai acontecer'],
      ['Romance histórico', 'ficção que se passa numa época real e usa figuras e factos dela']], None),
    # achado 4, F02, «Para entender», dobra «Recorda» (a primeira coluna com 30 %, como as caixas de termos do M6: «Caracterização»
    # não cabia nos 25 % da folha no ecrã largo)
    (F02, 0, ['Noção', 'O que é'],
     [['Símbolo', 'uma coisa concreta que representa uma ideia (a passarola, o sonho)'],
      ['Caracterização direta', 'o narrador ou uma personagem diz como alguém é'],
      ['Caracterização indireta', 'percebe-se pelo que a personagem faz e diz']], ['width:30%', None]),
    # achado 5, F03, «Para entender», dobra «Recorda» (a primeira coluna com 30 %, pela mesma razão: «Intertextualidade»)
    (F03, 0, ['Noção', 'O que é'],
     [['Discurso direto', 'as palavras da personagem, tal como as disse'],
      ['Discurso indireto', 'o narrador conta o que foi dito, com «que» e mudança de tempos e de pessoas'],
      ['Discurso indireto livre', 'a voz da personagem dentro da voz do narrador, sem verbo a anunciar'],
      ['Ironia', 'dizer uma coisa para dar a entender outra'],
      ['Intertextualidade', 'um texto que chama outros textos']], ['width:30%', None]),
    # achado 6, F10, «Para entender», caixa «Recorda»
    (F10, 0, ['Termo', 'O que é'],
     [['Tese', 'a posição que se defende'], ['Argumento', 'uma razão, com prova'],
      ['Contra-argumento', 'a razão de quem discorda'], ['Refutação', 'a resposta a essa razão']], None),
]
# Onde está cada tabela nas lições: (página, tabela) > (índice do cartão, rótulo do cartão, o que fica por cima, o que fica a seguir).
LUGARES = {
    (F01, 0): (8, 'Para entender', 'oje, não a da época.</p></div><details><summary>Recorda</summary><div><table class="apoio-tabela" role="table">',
               '</table></div></details>'),
    (F02, 0): (6, 'Para entender', '<details><summary>Recorda</summary><div><table class="apoio-tabela" role="table">',
               '</table><p>Baltasar chama-se Sete-Sóis; Blimunda, Sete-Luas.</p></div></details>'),
    (F03, 0): (4, 'Para entender', '<details><summary>Recorda</summary><div><table class="apoio-tabela" role="table">',
               '</table></div></details><div class="yt" data-yt="TS6fTIpNG6s"'),
    (F10, 0): (4, 'Para entender', '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela" role="table">',
               '</table><p>Conectores que ajudam: «porque», «no entanto», «ainda que», «portanto».</p></div>'),
}
# Nenhuma página do M9 tinha tabelas de apoio antes desta camada.
JA_TINHAM = {}

# O que a proposta final conta, par a par («antes»: as ocorrências que mudam, com a palavra inteira e fora das cadeias maiores),
# tal como está em bordo/cidadania-v3/cuidado-152/m9-confirmados.json (os pares com contexto, juntos pela referência que prendem).
PROPOSTA = {
    19: {'30 segundos': 1},
    21: {'D. João V': 2},
    22: {'3.º ano': 2, '90 minutos': 1, '30 %': 2, '10 minutos': 1, '5 minutos': 1, 'capítulos I e V': 1, '10 min': 1,
         '5 min': 1, '60 min': 1, '15 min': 1, '7 minutos': 1},
    23: {'3.º ano': 2, '90 minutos': 3, '90 min': 4, 'capítulo XXI': 4, '22 min': 2, '10 min': 2, '30 %': 2,
         'século XVIII': 9, 'século XVI': 5, 'século XX': 9, 'século XVII': 1, 'D. João V': 15, '22 de outubro de 1982': 1,
         '22 de outubro de 1730': 1, '22 de outubro de 1523': 1, 'capítulo I': 1, 'Século XVI': 1, 'cap. XXI': 1},
    24: {'12.º ano': 1, 'D. João V': 19, '2 min': 1, 'séc. XVIII': 2, 'capítulo XXI': 9, '22 de': 1, 'século XVIII': 7,
         'Século XVIII': 1, '22 de outubro de 1730': 4, 'pp. 291 a 293': 1, 'século XVI': 2, 'século XX': 4,
         'século XVII': 1, 'capítulo I': 3},
    25: {'12.º ano': 1, 'capítulo XVI': 3, '2 min': 1, 'pp. 196 e 197': 1, 'capítulo XXV': 3, 'D. João V': 2},
    26: {'D. João V': 1, '4 min': 2, 'capítulo I': 2, 'capítulo XXI': 4},
    27: {'século XX': 10, 'século XVI': 5, '2 min': 2, 'século XVIII': 4, 'Século XVI': 1},
    28: {'12.º ano': 1, '4 min': 1, '30 segundos': 1, '3 min': 1, '3 minutos': 1, 'capítulo XIX': 2, 'capítulo XXV': 2},
    29: {'D. João V': 8, 'capítulo XXI': 2, 'canto I': 4, 'capítulo XIX': 2},
    30: {'3 min': 1, '8 de outubro de 1998': 1, 'cap. XXI': 1},
    31: {'D. João V': 3, 'capítulo I': 1, 'p. 22': 1, 'n.º 2': 1, 'p. 33': 1},
    32: {'capítulo V': 3, 'página 78': 1, 'p. 49': 1},
    33: {'página 1': 1},
    34: {'22 min': 1, 'capítulo XXI': 1, 'D. João V': 3, '22 de outubro de 1730': 1, 'capítulo XIX': 1, 'canto III': 5,
         'canto VIII': 3, 'estância 20': 3, 'estância 78': 2, 'século XX': 1, 'capítulos I, XIX e XXI': 1},
    35: {'22 min': 1, 'capítulo XVI': 1, 'D. João V': 1, 'capítulo XXV': 2, 'capítulo XXI': 1, '22 de outubro de 1730': 1,
         'século XVIII': 1, 'século XX': 4, 'capítulo XIX': 2, 'cap. 1': 1, 'capítulos XVI, XIX, XXI e XXV': 1,
         'capítulo 1': 1},
    36: {'3.º ano': 2, '90 minutos': 2, 'D. João V': 6, '22 de outubro de 1730': 2, 'século XVIII': 3, 'século XX': 1,
         '30 %': 2, 'M9-F01': 4, 'M9-F04': 4, 'M9-F02': 1},
    37: {'D. João V': 1},
    46: {'ato III': 1, 'século XVI': 1},
    47: {'3.º ano': 2, '90 minutos': 1, '40 %': 1},
    52: {'capítulo I': 5, 'capítulo XXV': 2, 'capítulo XVI': 1},
    53: {'século XVIII': 1, '4 min': 1},
    54: {'capítulo XVI': 1, 'capítulo XIX': 1, 'capítulo XXV': 1, 'M9-F03': 1},
    55: {'13 de janeiro de 1935': 1},
    57: {'3.º ano': 2},
    58: {'10 min': 1, '60 minutos': 1, '90 min': 1, '10 minutos': 1, 'capítulo I': 2, 'capítulo V': 2},
    59: {'10 min': 1, '60 minutos': 1, '90 min': 1, '10 minutos': 1},
}
PROPOSTA_PAINEIS = {
    38: {'D. João V': ('D.{N}João{N}V', 3, 5, 1), 'capítulo I': ('capítulo{N}I', 1, 0, 0),
         'capítulo XXI': ('capítulo{N}XXI', 6, 1, 0), 'século XVI': ('século{N}XVI', 0, 1, 0),
         'século XVII': ('século{N}XVII', 0, 1, 0), 'século XVIII': ('século{N}XVIII', 0, 3, 0),
         'século XX': ('século{N}XX', 0, 2, 0), '22 de outubro de 1730': ('22{N}de outubro de{N}1730', 0, 4, 0)},
    39: {'D. João V': ('D.{N}João{N}V', 0, 1, 1), 'capítulo XVI': ('capítulo{N}XVI', 1, 0, 0),
         'capítulo XXV': ('capítulo{N}XXV', 2, 0, 0)},
    40: {'D. João V': ('D.{N}João{N}V', 0, 0, 1), 'capítulo I': ('capítulo{N}I', 1, 0, 0),
         'capítulo XXI': ('capítulo{N}XXI', 1, 0, 0)},
    42: {'D. João V': ('D.{N}João{N}V', 0, 0, 1), 'capítulo XIX': ('capítulo{N}XIX', 1, 0, 0),
         'capítulo XXV': ('capítulo{N}XXV', 1, 0, 0)},
    43: {'D. João V': ('D.{N}João{N}V', 1, 5, 1), 'capítulo XIX': ('capítulo{N}XIX', 1, 0, 0),
         'capítulo XXI': ('capítulo{N}XXI', 1, 0, 0), 'canto I': ('canto{N}I', 0, 1, 0)},
}
# Nos painéis de projeção que mudam: (a forma da proposta, com {N} por U+00A0; as ocorrências que mudam, na lista CARTOES e no
# seletor; as que ficam no material do relâmpago, MATERIAL; as que ficam nas pistas do «Quem sou eu?», ATL).
PAINEL = {f'm9/painel-m9-{f}/index.html': i for f, i in (('f01', 38), ('f02', 39), ('f03', 40), ('f05', 42), ('f07', 43))}
# As trocas que não estão nos pares da proposta, com a razão: a meta descrição das tarefas muda com «nao_partir» (como do M1 ao M8).
META = 'durante 90 minutos, com entrega'
EXTRAS = {58: {META}, 59: {META}}
# O que a conferência deixou de fora vem no contexto dos pares (os excertos do romance, as citações, os «alt» e as peças dos
# exercícios): o gerador não tem nenhuma entrada «fora».
FORA = {}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a proposta pede U+00A0, traço de intervalo sem U+2060
# ou o hífen da sigla «M9-Fxx» sem a junção. As formas do M9: «p.» e «pp.», «n.º», «capítulo(s)», «cap.», «canto», «estância»,
# «século» (e «séc.»), «ato» e «página» com o número, o «e» antes do último capítulo de uma lista, «D. João V», ordinal e nome, número e unidade (min, minutos, segundos, %),
# as datas (o dia preso ao «de» e o ano ao «de», como do M5 ao M8), os intervalos com traço e a sigla.
MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'
PARTE = re.compile(
    r'(?<![\w.])pp?\. (?=\d)'
    r'|n\.º (?=\d)'
    r'|\b(?:capítulos?|cantos?|estâncias?|[Ss]éculos?|ato|página) (?=(?:\d+|[IVXLC]+)\b)'
    r'|\b(?:[Ss]éc|cap)\. (?=(?:\d+|[IVXLC]+)\b)'
    r'|\bD\. (?=João[ \xa0]V\b)|(?<=\bD\.[ \xa0])João (?=V\b)'
    r'|(?<=[IVXLC] )e (?=[IVXLC]+\b)'
    r'|\d\.[ºª] (?=ano\b)'
    r'|\b\d+ (?=(?:min|minutos|segundos|%)(?!\w))'
    r'|\b\d{1,2} de (?=(?i:' + MESES + r'))'
    r'|(?<=\d[ \xa0]de )(?i:' + MESES + r') de (?=\d{4}\b)'
    r'|\d–(?!⁠)\d|\bM9-(?!⁠)F\d')


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
    spec = importlib.util.spec_from_file_location('cuidado_m9_20261112', ROOT / 'scripts/cuidado_m9_20261112.py')
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
    return undo_cuidado_m9_1112(rel, ler(rel))


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


def paginas_do_m9():
    return [Path(p).relative_to(ROOT).as_posix() for p in sorted(glob.glob(str(ROOT / 'm9/**/index.html'), recursive=True))
            + sorted(glob.glob(str(ROOT / 'tarefas/m9-*/**/index.html'), recursive=True))]


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


class CuidadoM9(unittest.TestCase):
    def test_sete_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 7)
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
                # Só as dos pesos e as da F02 e da F03 têm larguras: a coluna do peso só leva o número (5,5 rem), como no M5 e no
                # M8, e a das noções da F02 e da F03 leva 30 %, como as caixas de termos do M6.
                self.assertEqual([c['attrs'].get('style') for c in topo['celulas']], larguras or [None] * len(cabecalho))
        # Nenhuma página do M9 (nem as suas tarefas, aquecimentos, grelhas e correções) tem mais tabelas de apoio novas do que
        # estas; antes desta camada não havia nenhuma.
        contagem = {}
        for rel, *_ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        for rel in paginas_do_m9():
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
        # Nas caixas «Recorda» da F01, da F02, da F03 e da F10, as noções já não vêm em negrito num parágrafo; a frase dos dois
        # nomes da F02 e a dos conectores da F10 ficam num parágrafo a seguir, e os outros cartões ficam como estavam.
        for rel, k, primeira in ((F01, 8, 'Tempo histórico'), (F02, 6, 'Símbolo'), (F03, 4, 'Discurso direto'), (F10, 4, 'Tese')):
            caixa = cartoes(ler(rel))[k]['html']
            self.assertNotIn(f'<b>{primeira}</b>:', caixa)
            self.assertIn(f'<th scope="row" role="rowheader">{primeira}</th>', caixa)
            self.assertIn(f'<b>{primeira}</b>:', cartoes(base(rel))[k]['html'])
        self.assertIn('<b>Caracterização indireta</b>: percebe-se pelo que a personagem faz e diz. Baltasar chama-se Sete-Sóis; '
                      'Blimunda, Sete-Luas.</p>', cartoes(base(F02))[6]['html'])
        self.assertIn('<b>Refutação</b>: a resposta a essa razão. Conectores que ajudam: «porque», «no entanto», «ainda que», '
                      '«portanto».</p>', cartoes(base(F10))[4]['html'])
        # O cartão de emparelhar da F01 que pede as cinco noções continua a pedi-las com as mesmas palavras.
        f01, f01_antes = cartoes(ler(F01)), cartoes(base(F01))
        solto = lambda s: json.dumps(s, ensure_ascii=False).replace(N, ' ').replace(WJ, '')
        self.assertEqual([solto(c) for c in f01 if c['t'] == 'emparelhar'], [solto(c) for c in f01_antes if c['t'] == 'emparelhar'])
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
        # Os ficheiros dos cartões da F11, da F12 e da F13 não levam tabelas (a F13 leva a lista das estações).
        for rel in (F11_JS, F12_JS, F13_JS):
            self.assertNotIn('apoio-tabela', ler(rel))

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
        # As outras páginas do M9 ficam como estavam: nenhuma carregava a folha, e continuam sem ela.
        for rel in paginas_do_m9():
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
        # Achado 9: no guia, «Três antes de mim» numa lista ordenada (o mesmo trecho, letra a letra, dos guias do M5, do M7 e do M8).
        regra = ('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a '
                 'rubrica;</li><li>pergunta ao teu par de trabalho.</li></ol>Só depois levantas o braço.</div>')
        self.assertEqual(ler(GUIA).count(regra), 1)
        self.assertIn(regra, ler('m5/guia-da-tarefa-m5/index.html'))
        self.assertIn(regra, ler('m7/guia-da-tarefa-m7/index.html'))
        self.assertIn(regra, ler('m8/guia-da-tarefa-m8/index.html'))
        self.assertNotIn('1) relê o enunciado', ler(GUIA))
        self.assertEqual(base(GUIA).count('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; '
                                          '2) vê a rubrica; 3) pergunta ao teu par de trabalho. Só depois levantas o braço.</div>'), 1)
        # Achado 11: na F01, as quatro linhas de ação do «O essencial» em lista, cada item com a vírgula ou o ponto final que tinha, e
        # a frase seguinte num parágrafo; o texto é o mesmo, letra a letra: os itens, de seguida, dão o parágrafo de antes.
        linhas_acao = ('<p>«Memorial» é texto de memória e monumento que lembra. O romance histórico cruza ficção e história em quatro '
                       'linhas de ação:</p><ul><li>a construção do convento,</li><li>a passarola,</li><li>o amor de Baltasar e '
                       'Blimunda,</li><li>a corte e a Inquisição.</li></ul><p>Assim dá lugar a quem a história oficial esquece.</p>')
        f01, f01_antes = cartoes(ler(F01)), cartoes(base(F01))
        self.assertEqual(f01[2]['rot'], 'O essencial')
        self.assertEqual(f01[2]['html'].count('<details><summary>O título e as quatro linhas de ação</summary><div>' + linhas_acao), 1)
        self.assertEqual(sum(linhas_acao in c.get('html', '') for c in f01), 1)
        itens = re.findall(r'<li>(.*?)</li>', linhas_acao)
        self.assertEqual(len(itens), 4)
        self.assertEqual(f01_antes[2]['html'].count(
            '<p>«Memorial» é texto de memória e monumento que lembra. O romance histórico cruza ficção e história em quatro linhas de '
            'ação: ' + ' '.join(itens) + ' Assim dá lugar a quem a história oficial esquece.</p>'), 1)
        self.assertEqual(ler(F01).count('<ul><li>a construção do convento,'), 1)
        # Achado 15: na F13 (os cartões estão em m9/recursos/f13.js), as quatro estações em lista numerada, cada uma com o «;» ou o
        # ponto final que tinha, e a frase seguinte num parágrafo; os cartões seguintes continuam a chamar-se «Estação 1» a «Estação 4».
        estacoes = ('<p>Oficina longa, com o livro aberto, em quatro estações:</p><ol><li>hipótese inicial;</li><li>confronto de '
                    'episódios;</li><li>contraexemplo e revisão;</li><li>síntese fundamentada.</li></ol><p>Entre estações, confronta a '
                    'tua leitura com uma passagem do livro e anota a página da edição.</p>')
        f13, f13_antes = cartoes(ler(F13_JS)), cartoes(base(F13_JS))
        self.assertEqual((f13[1]['rot'], f13[1]['titulo']), ('Lê e confronta', 'Caderno de leitura: quatro estações'))
        self.assertTrue(f13[1]['html'].startswith(estacoes))
        self.assertEqual(sum(estacoes in c.get('html', '') for c in f13), 1)
        passos = re.findall(r'<li>(.*?)</li>', estacoes)
        self.assertEqual(len(passos), 4)
        self.assertTrue(f13_antes[1]['html'].startswith(
            '<p>Oficina longa, com o livro aberto, em quatro estações: ' + ' '.join(passos) + ' Entre estações, confronta a tua leitura '
            'com uma passagem do livro e anota a página da edição.</p>'))
        self.assertEqual(sorted(re.findall(r'Estação \d', ' '.join(c.get('titulo') or '' for c in f13))),
                         ['Estação 1', 'Estação 2', 'Estação 3', 'Estação 4'])
        self.assertEqual(ler(F13_JS).count('<ol>'), base(F13_JS).count('<ol>') + 1)
        # Achado 10: no portefólio, os catorze nomes de ficheiro em <code> (os oito que estavam em texto simples e os seis que já
        # estavam), sem U+2011, U+2060 nem U+00A0 (o aluno copia-os). Os oito novos mudam de linha a seguir a cada «_» (<wbr>); dos
        # seis que já estavam em <code>, só os dois compridos levam <wbr> (a proposta final, como nos portefólios do M5 e do M7).
        port = ler(PORTEFOLIO)
        linhas = re.findall(r'<tr><td>(.*?)</td><td>', port)
        self.assertEqual(len(linhas), 14)
        self.assertTrue(all(re.fullmatch(r'<code>M9_[^<‑⁠\xa0]*(?:<wbr>[^<‑⁠\xa0]*)*</code>', l) for l in linhas), linhas)
        nomes = [f'M9_<wbr>U{u}_<wbr>{n}' for u in (1, 2) for n in ('registo_<wbr>&lt;dia-mês&gt;', 'retoma', 'o-que-aprendi', 'Tarefa')]
        self.assertEqual(len(nomes), 8)
        curtos = ['M9_capa', 'M9_Revisao1', 'M9_Revisao2', 'M9_balanco']
        for nome in nomes + ['M9_<wbr>cartao-do-percurso', 'M9_<wbr>Prova-escrita'] + curtos:
            self.assertEqual(port.count(f'<td><code>{nome}</code></td>'), 1, nome)
        for nome in curtos:
            self.assertEqual(base(PORTEFOLIO).count(f'<td><code>{nome}</code></td>'), 1, nome)
        # Nos oito novos e nos dois compridos, cada «_» leva o seu <wbr>; nos quatro curtos, nenhum; e não há <wbr> em mais lado nenhum.
        for l in linhas:
            self.assertEqual(l.count('_<wbr>'), 0 if re.sub(r'</?code>', '', l) in curtos else l.count('_'), l)
        self.assertEqual(port.count('<wbr>'), sum(l.count('<wbr>') for l in linhas))
        self.assertEqual(port.count('<wbr>'), 6 * 2 + 2 * 3 + 2)
        self.assertNotIn('<wbr>', base(PORTEFOLIO))
        # Os nomes são os mesmos, letra a letra, pela mesma ordem: sem as marcas, a primeira coluna é a de antes.
        limpa = lambda s: re.sub(r'</?code>|<wbr>', '', s)
        self.assertEqual([limpa(l) for l in linhas], [limpa(l) for l in re.findall(r'<tr><td>(.*?)</td><td>', base(PORTEFOLIO))])
        self.assertIn('code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
                      'td code{white-space:nowrap}\n', port)
        self.assertEqual(port.count('td code{white-space:nowrap}'), 1)
        self.assertNotIn('td code{white-space:nowrap}', base(PORTEFOLIO))
        for m in (5, 7, 8):
            self.assertIn('td code{white-space:nowrap}', ler(f'm{m}/portefolio-do-modulo-m{m}/index.html'))
        # A tabela do portefólio fica como estava (o cabeçalho e a segunda coluna não mudam, salvo os espaços presos do achado 47).
        self.assertEqual(re.findall(r'<table><tr><th[^>]*>Nome do ficheiro</th><th>O que é</th></tr>', port),
                         re.findall(r'<table><tr><th[^>]*>Nome do ficheiro</th><th>O que é</th></tr>', base(PORTEFOLIO)))
        self.assertEqual(len(re.findall(r'<table><tr><th[^>]*>Nome do ficheiro</th><th>O que é</th></tr>', port)), 1)
        self.assertEqual([c.replace(N, ' ') for c in re.findall(r'</td><td>(.*?)</td></tr>', port)],
                         re.findall(r'</td><td>(.*?)</td></tr>', base(PORTEFOLIO)))

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
        # A casca das lições (migalhas, «Estás em», título escondido e sigla do rodapé) fica para o molde, como do M1 ao M8.
        self.assertEqual(len(C.CASCA_NO_MOLDE), 10)
        self.assertEqual(C.CASCA_NO_MOLDE, sorted(Path(p).relative_to(ROOT).as_posix() for p in glob.glob(str(ROOT / 'm9/licao-*/index.html'))
                                                  if not re.search(r'licao-m9-f(?:11|12|13)/', p)))
        for rel in sorted(Path(p).relative_to(ROOT).as_posix() for p in glob.glob(str(ROOT / 'm9/licao-*/index.html'))):
            texto = ler(rel)
            n = re.search(r'licao-m9-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                # As lições geradas (F14 a F16) e as que carregam os cartões de m9/recursos (F11 a F13) têm outra casca, sem a
                # migalha do ano; as páginas da F11, da F12 e da F13 não estão na camada (só os ficheiros dos cartões).
                if n.lower() not in [g.split('-')[1] for g in GERADAS] + ['f11', 'f12', 'f13']:
                    self.assertEqual(texto.count('/pt/3/">3.º ano</a>'), 1)
                    self.assertEqual(texto.count('>Módulo 9: Romance Saramaguiano</a>'), 1)
                    self.assertGreaterEqual(texto.count(f'Lição M9-{n}'), 2)
                self.assertEqual(texto.count('3.º' + N + 'ano'), 0)
                self.assertNotIn(f'M9-{WJ}{n}', texto)
                self.assertEqual(texto.count(f'Lição M9-{n}'), base(rel).count(f'Lição M9-{n}'))
                if n.lower() in ('f11', 'f12', 'f13'):
                    self.assertNotIn(rel, MANIFESTO['files'])
                    self.assertIn(f'recursos/{n.lower()}.js', texto)
        # Nas outras páginas, as migalhas contam (como na proposta final): o «3.º ano» fica preso nas migalhas e no cabeçalho.
        for rel, cab in ((INDICE, 'Português, 3.º' + N + 'ano, percurso do módulo'), (GUIA, 'Guia da tarefa, 3.º' + N + 'ano'),
                         (MAPA, 'Português · 3.º' + N + 'ano · Mapa do módulo'), (PORTEFOLIO, 'Português · 3.º' + N + 'ano · Módulo 9'),
                         ('m9/visita-fundacao-jose-saramago/index.html', 'Caderno de campo, 3.º' + N + 'ano')):
            self.assertIn('/pt/3/">3.º' + N + 'ano</a>', ler(rel), rel)
            self.assertIn(cab, ler(rel), rel)
            self.assertNotIn('3.º ano', sem_atributos_nem_desenhos(ler(rel)), rel)
        # A sigla das ligações do mapa leva a junção (os href, em minúsculas, ficam); a da F13, no ficheiro dos cartões, também.
        mapa = ler(MAPA)
        self.assertEqual(len(re.findall(r'M9-' + WJ + r'F\d\d', mapa)), 9)
        self.assertNotRegex(sem_atributos_nem_desenhos(mapa), r'M9-F\d\d')
        self.assertIn('licao-m9-f01/">Lição M9-' + WJ + 'F01</a>', mapa)
        self.assertEqual(ler(F13_JS).count('M9-' + WJ + 'F03'), 1)
        # O que a conferência tirou fica como estava: o traço entre ano e lugar do mapa, «D.» com nome e sem numeral («D. Maria
        # Ana», «D. Sebastião»; o M5 só prendeu «D.» com numeral), o mês e o ano sem dia («outubro de 1730») e «52 mil».
        self.assertEqual(mapa.count('1922–Lanzarote'), 1)
        self.assertEqual(base(MAPA).count('1922–Lanzarote'), 1)
        self.assertNotIn('–' + WJ, mapa)
        f01 = ler(F01)
        for trecho in ('D. Maria Ana', 'outubro de 1730, no reinado', 'outubro de 1982'):
            self.assertIn(trecho, f01)
            self.assertEqual(f01.count(trecho), base(F01).count(trecho), trecho)
        self.assertNotRegex(f01, r'D\.' + N + r'(?!João' + N + r'V\b)')
        self.assertIn('D. Sebastião', ler(F07))
        self.assertEqual(ler(F07).count('D. Sebastião'), base(F07).count('D. Sebastião'))
        self.assertIn('52 mil', ler('m9/memorial-promessa/index.html'))
        # «séc. XVIII» fica abreviado, só com o espaço preso (como o «séc. XIII» do M1): a letra não muda.
        self.assertEqual(f01.count('início do séc.' + N + 'XVIII</b>'), 2)
        self.assertNotIn('séc. XVIII', sem_atributos_nem_desenhos(f01))
        # Os excertos do romance, as citações e as «linhas» dos versos ficam como estavam (a conferência deixou-os de fora com o
        # contexto dos pares): o nome do rei dentro do excerto do capítulo XXI não leva espaços presos.
        for trecho in ('Carregou-se o sobrecenho de D. João V, porque', 'Porém, D. João V teve um pensamento negro',
                       'E então D. João V disse, A sagração', '"linhas":["No capítulo XXI, D. João V fecha-se numa sala do torreão,'):
            self.assertEqual(f01.count(trecho), 1, trecho)
            self.assertEqual(base(F01).count(trecho), 1, trecho)
        # As listas de capítulos e de páginas prendem o nome ao primeiro número e o «e» (ou o «a») ao último, como no M8.
        self.assertIn('capítulos' + N + 'I, XIX e' + N + 'XXI</li>', ler('m9/m9-de-quem-e-o-convento/index.html'))
        self.assertIn('capítulos' + N + 'XVI, XIX, XXI e' + N + 'XXV', ler('m9/m9-ver-e-nao-ver/index.html'))
        self.assertIn('capítulos' + N + 'I e' + N + 'V de <i>Memorial do Convento</i>', ler(GUIA))
        self.assertIn('pp.' + N + '291 a' + N + '293', f01)
        self.assertIn('pp.' + N + '196 e' + N + '197', ler(F02))
        # As datas com o dia preso ao «de» e o ano ao «de», como do M5 ao M8; «22 de outubro», sem ano, só prende o dia.
        self.assertEqual(len(inteiras(f01, '22' + N + 'de outubro de' + N + '1730')), 4)
        self.assertEqual(len(inteiras(f01, '22' + N + 'de outubro,')), 1)
        self.assertIn('13' + N + 'de janeiro de' + N + '1935', ler('m9/reis-regresso/index.html'))
        self.assertIn('8' + N + 'de outubro de' + N + '1998', ler(F10))
        self.assertNotRegex(sem_atributos_nem_desenhos(mapa), r'\d de (?i:' + MESES + r') de \d{4}')
        # Os vídeos: o botão muda, o data-titulo (que vira o title do leitor) fica; nos «alt», os espaços ficam normais.
        self.assertEqual(f01.count('(2 min)'), 1)
        self.assertEqual(f01.count('(2' + N + 'min)</button>'), 1)
        self.assertRegex(f01, r'data-titulo=\\"[^"]*\(2 min\)\\"')
        indice = ler(INDICE)
        self.assertEqual(indice.count('desenho do século XVIII (fac-símile, BNP)" loading="lazy"'), 1)
        self.assertEqual(indice.count('desenho do século' + N + 'XVIII (fac-símile, BNP). Domínio público.</p>'), 1)
        self.assertEqual(mapa.count('desenho do século' + N + 'XVIII (fac-símile, BNP). Domínio público.</p>'), 1)
        self.assertEqual(mapa.count('alt="A Passarola de Bartolomeu de Gusmão, desenho do século XVIII (fac-símile, BNP)"'), 1)
        self.assertRegex(indice, r'<title>[^<]*</title>')
        self.assertEqual(re.search(r'<title>[^<]*</title>', indice).group(0), re.search(r'<title>[^<]*</title>', base(INDICE)).group(0))
        # As tarefas da M9-U1 e da M9-U2: os números do molde, pelo gerador (a ligação à grelha fica como estava).
        for u in (1, 2):
            t = ler(f'tarefas/m9-u{u}/index.html')
            self.assertIn('Antes de escrever · 10' + N + 'min · em cartões, com consulta', t)
            self.assertIn(f'Tarefa individual · Unidade {u} · 90' + N + 'min</p>', t)
            self.assertNotIn('90 min', t)
            self.assertRegex(t, r'<meta name="description" content="[^"]*durante 90' + N + 'minutos, com entrega')
            self.assertEqual(t.count('<p class="task-grelha">'), base(f'tarefas/m9-u{u}/index.html').count('<p class="task-grelha">'))

    def test_paineis_seguem_as_licoes(self):
        # Os painéis de projeção das lições do M9 mostram os enunciados dos cartões: onde um mudou, o painel muda igual, na lista
        # (CARTOES) e no seletor; são os achados dos painéis da F01, da F02, da F03, da F05 e da F07 (38, 39, 40, 42 e 43), e mais
        # nenhum painel de projeção muda. As notas do docente da F14 (45), que não têm lista, conferem-se nas páginas geradas.
        paineis = sorted({t['ficheiro'] for t in TROCAS if '/painel-' in t['ficheiro']} - {NOTAS_F14})
        self.assertEqual(paineis, sorted(PAINEL))
        self.assertEqual(C.PAINEIS, PAINEL)
        self.assertEqual(sorted(PROPOSTA_PAINEIS), sorted(B_PAINEIS))
        self.assertEqual(sorted(PAINEL.values()), sorted(B_PAINEIS))
        for rel in paineis:
            i = PAINEL[rel]
            antes, depois = base(rel), ler(rel)
            # O material do relâmpago (MATERIAL) segue a lição antes das camadas de cuidado (tests/test_sala_desligada.py): não
            # muda; as pistas do «Quem sou eu?» (ATL) e o resto da página também não.
            a, b, atl = depois.index(',MATERIAL='), depois.index(',crono='), depois.index('var ATL=')
            self.assertLess(a, b)
            self.assertLess(b, atl)
            self.assertEqual(antes.split(',MATERIAL=', 1)[1], depois[a + len(',MATERIAL='):], rel)
            for t in TROCAS:
                if t['ficheiro'] == rel:
                    self.assertEqual(achados_da_troca(t), [i], t['local'])
                    self.assertIn('(painel de projeção)', t['local'])
                    self.assertTrue(t['antigo'].startswith(('{"k":', '<option value="')), t['local'])
                    self.assertEqual(t['novo'].replace(N, ' ').replace(WJ, ''), t['antigo'])
            # Cada referência da proposta: as ocorrências que mudam estão na lista e no seletor; as do material e as das pistas
            # ficam como estavam.
            for seq, (forma, n, material, pistas) in PROPOSTA_PAINEIS[i].items():
                presa = C.j(forma)
                self.assertEqual(presa.replace(N, ' ').replace(WJ, ''), seq)
                with self.subTest(painel=rel, trecho=seq):
                    self.assertEqual(len(inteiras(depois, presa)), n)
                    self.assertEqual(inteiras(depois, presa, a), [])
                    self.assertEqual(len(inteiras(depois, seq)), material + pistas)
                    self.assertEqual(len(inteiras(depois, seq, a, b)), material)
                    self.assertEqual(len(inteiras(depois, seq, atl)), pistas)
                    self.assertEqual(len(inteiras(antes, seq)), n + material + pistas)
            self.assertTrue(any(n for _, n, _, _ in PROPOSTA_PAINEIS[i].values()), rel)
        # Em todos os painéis de projeção do M9, cada enunciado da lista é o do cartão da lição (com ou sem os marcadores de
        # negrito e de itálico e com as lacunas como «…»), e o seletor mostra-o (inteiro ou cortado), com o itálico em <i>.
        conferidos = mudados = 0
        for p in sorted(glob.glob(str(ROOT / 'm9/painel-m9-*/index.html'))):
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
        self.assertGreater(conferidos, 120)
        # Cada enunciado mudado deu duas trocas no painel (a lista e o seletor), salvo onde o seletor corta o enunciado antes da
        # referência.
        trocas_paineis = sum(t['ficheiro'] in PAINEL for t in TROCAS)
        self.assertLessEqual(mudados, trocas_paineis)
        self.assertGreaterEqual(2 * mudados, trocas_paineis)
        self.assertEqual((mudados, trocas_paineis), (15, 20))
        # No painel da F01, o enunciado do cartão 25 («… figuras reais da época, como D. João V, entram na ficção.») muda na lista
        # e no seletor.
        f01 = {x['k']: x['p'] for x in cartoes(ler('m9/painel-m9-f01/index.html'))}
        self.assertEqual(f01[25], 'No romance histórico, figuras reais da época, como D.' + N + 'João' + N + 'V, entram na ficção.')
        self.assertIn('<option value="25">' + f01[25] + '</option>', ler('m9/painel-m9-f01/index.html'))
        # Os painéis da F04 e da F10 (achados 41 e 44: só tinham ocorrências no material e nas pistas) ficam como estavam.
        for rel in SO_MATERIAL.values():
            self.assertNotIn(rel, MANIFESTO['files'])

    def test_banco_segue_as_licoes(self):
        # As cópias dos cartões no banco das provas rápidas do índice (var U) mudam como as lições de onde vêm: cada cópia que era
        # igual a um cartão da sua lição antes desta camada continua igual depois, campo a campo. No M9, o banco reescreve muitas
        # perguntas (das 90 cópias, 17 são iguais ao cartão inteiro), por isso confere-se também campo a campo: nas 45 cópias com o
        # enunciado de um cartão da sua lição, cada campo que era igual ao do cartão continua igual ao do cartão.
        copias, copias_antes = banco(ler(INDICE)), banco(base(INDICE))
        self.assertEqual(len(copias), len(copias_antes))
        self.assertEqual(len(copias), 90)
        iguais = com_enunciado = campos = 0
        for copia, antes in zip(copias, copias_antes):
            licao = f"m9/licao-{antes.get('_l')}/index.html"
            if not (ROOT / licao).is_file() or 'CARTOES' not in ler(licao):
                continue
            L, L_antes = cartoes(ler(licao)), cartoes(base(licao))
            for c, c_antes in zip(L, L_antes):
                comuns = [k for k in ('p', 'o', 'c', 'f', 'fe', 'frase', 'v') if k in antes]
                if comuns and all(c_antes.get(k) == antes[k] for k in comuns):
                    with self.subTest(licao=licao, p=antes.get('p', '')[:40]):
                        self.assertEqual({k: copia[k] for k in comuns}, {k: c.get(k) for k in comuns})
                        iguais += 1
                    break
            for c, c_antes in zip(L, L_antes):
                if antes.get('p') and antes['p'] in (c_antes.get('p'), c_antes.get('p2')):
                    com_enunciado += 1
                    for k in ('o', 'c', 'f', 'fe', 'frase', 'v'):
                        if k in antes and c_antes.get(k) == antes[k]:
                            with self.subTest(licao=licao, p=antes['p'][:40], campo=k):
                                self.assertEqual(copia[k], c.get(k))
                                campos += 1
                    break
        self.assertEqual((iguais, com_enunciado, campos), (17, 45, 95))
        # O banco diz o mesmo que dizia, letra a letra: só mudam os espaços presos (as 16 cópias com uma referência do achado 23).
        solto = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True).replace(N, ' ').replace(WJ, '')
        self.assertEqual([solto(x) for x in copias], [solto(x) for x in copias_antes])
        self.assertEqual(sum(a != b for a, b in zip(copias, copias_antes)), 16)
        # Fora das páginas do M9, das suas tarefas e dos dados dos geradores, a camada só toca nas sessões do Exame, onde a
        # resposta certa e o retorno do cartão 11 da F01 estão copiados (na pergunta e na verificação «Depois da revisão»):
        # tests/test_exame_alignment.py continua a comparar as cópias com a lição, letra a letra (como no M6).
        self.assertEqual(sorted(f for f in MANIFESTO['files'] if not f.startswith(('m9/', 'tarefas/m9-', 'docs/pedagogia/'))), [SESSOES])
        self.assertEqual([(x['i'], x['ficheiro']) for x in C.NOTAS], [(45, NOTAS_F14), (24, SESSOES)])
        cartao = cartoes(ler(F01))[10]
        self.assertEqual(cartao['p'], 'Em que época se passa a história do _Memorial do Convento_?')
        certa, retorno = cartao['o'][cartao['c']], cartao['f'].replace('**', '')
        self.assertEqual(certa, 'No início do século' + N + 'XVIII')
        self.assertEqual(retorno, 'Reinado de D.' + N + 'João' + N + 'V e tempo da Inquisição: início do século' + N + 'XVIII; o século' + N
                         + 'XX é o da escrita.')
        # 12/11/2026: as sessões como esta camada as deixou: com a camada de cima (cuidado_exame_20261112, que também as muda)
        # desfeita, com contagem estrita; as contas são as mesmas.
        sessoes, sessoes_antes = undo_cuidado_exame_1112(SESSOES, ler(SESSOES)), base(SESSOES)
        self.assertEqual(sessoes.count(json.dumps(certa, ensure_ascii=False)), 2)
        self.assertEqual(sessoes.count('"feedback": ' + json.dumps(retorno, ensure_ascii=False)), 2)
        # (As sessões já tinham os espaços presos da cópia da M6-F01, que a camada do M6 lá pôs; ficam como estavam.)
        self.assertEqual(sessoes.replace(N, ' '), sessoes_antes.replace(N, ' '))
        self.assertEqual(sessoes.count(N) - sessoes_antes.count(N), 2 * (1 + 4))
        self.assertEqual(sessoes.count(WJ), sessoes_antes.count(WJ))
        for t in TROCAS:
            if t['ficheiro'] == SESSOES:
                self.assertEqual(achados_da_troca(t), [24])
                self.assertIn('sessão s19', t['achado'])
        # Três trocas: «século XVIII» (quatro vezes: a resposta e o retorno, nas duas cópias), «D. João V» e «século XX» (duas cada).
        self.assertEqual(sorted(t['ocorrencias'] for t in TROCAS if t['ficheiro'] == SESSOES), [2, 2, 4])
        dados = json.loads(sessoes)
        s19 = next(s for s in (dados['sessions'] if isinstance(dados, dict) else dados) if s['id'] == 's19')
        self.assertEqual(s19['source']['url'], '/pt/m9/licao-m9-f01/')
        # As outras opções da pergunta, que o teste do Exame não compara com a lição, ficam como estavam.
        q1 = next(q for q in s19['warmup'] if q['id'] == 's19-q1')
        self.assertEqual([o for o in q1['options'] if N in o], [certa])

    def test_fora_de_ambito_e_recusados(self):
        achados = {n for t in TROCAS for n in achados_da_troca(t)}
        self.assertFalse(RECUSADOS & achados)
        self.assertFalse(set(FORA_DE_AMBITO) & achados)
        self.assertFalse(set(SO_MATERIAL) & achados)
        self.assertFalse(RECUSADOS & CONFIRMADOS)
        # 20, 48 a 51 e 56: os diapositivos, as provas rápidas, os questionários e a página «todos» ficam de fora (como do M1 ao
        # M8); 41 e 44: os painéis da F04 e da F10, só com ocorrências no material do relâmpago e nas pistas, também. Nenhuma está
        # na camada, nem no gerador.
        for rel in sorted(FORA_DE_AMBITO.values()) + sorted(SO_MATERIAL.values()):
            with self.subTest(pagina=rel):
                self.assertTrue((ROOT / rel).is_file())
                self.assertNotIn(rel, MANIFESTO['files'])
                self.assertNotIn(rel, {x['ficheiro'] for x in C.ACHADOS_B + C.NOTAS + C.achados_ac()})
                self.assertNotIn(rel, C.PAINEIS)
                self.assertEqual(base(rel), ler(rel))
        # Nenhuma página de diapositivos, de provas rápidas, de questionários ou «todos», de módulo nenhum, está na camada.
        self.assertFalse([f for f in MANIFESTO['files'] if re.search(r'/(?:diapositivos|prova-[abc]|questionarios|todos)/', f)])
        # Nos painéis da F04 e da F10, as ocorrências confirmadas estão todas no material do relâmpago ou nas pistas do «Quem sou eu?».
        for rel, trechos in ((SO_MATERIAL[41], ('século XVI', 'século XX', 'século XVIII', 'D. João V')),
                             (SO_MATERIAL[44], ('cap. XXI', 'D. João V'))):
            texto = ler(rel)
            a, b, atl = texto.index(',MATERIAL='), texto.index(',crono='), texto.index('var ATL=')
            for trecho in trechos:
                posicoes = inteiras(texto, trecho)
                self.assertTrue(posicoes, (rel, trecho))
                self.assertTrue(all(a < p < b or p > atl for p in posicoes), (rel, trecho))
        # 7: a nota de «gram-aspeto-memorial» fica como estava; 8 e 13: as entradas de ol.ess-mini da F07 e da F04 ficam sem tabela
        # nem lista; 12, 14, 16 e 17: sem listas de dois itens; 18: o campo «produto» do guia fica sem <code>.
        self.assertNotIn('m9/gram-aspeto-memorial/index.html', MANIFESTO['files'])
        self.assertNotIn('apoio-tabela', ler('m9/gram-aspeto-memorial/index.html'))
        for rel in (F04, F07, 'm9/licao-m9-f05/index.html', 'm9/licao-m9-f14/index.html', 'm9/licao-m9-f15/index.html',
                    'm9/licao-m9-f16/index.html', F11_JS, F12_JS):
            self.assertNotIn('apoio-tabela', ler(rel), rel)
            self.assertEqual(ler(rel).count('<li>'), base(rel).count('<li>'), rel)
            self.assertEqual(ac_aplicadas(rel, base(rel)), base(rel), rel)
        self.assertEqual(ler(GUIA).count('<code>'), base(GUIA).count('<code>'))
        # As lições e os ficheiros de cartões sem achado A ou C ficam sem tabela nem lista novas.
        for rel in MANIFESTO['files']:
            if rel.startswith(('m9/licao-', 'm9/recursos/')) and rel not in (F01, F02, F03, F10, F13_JS):
                self.assertEqual(ac_aplicadas(rel, base(rel)), base(rel), rel)

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, cab, _, _ in TABELAS for c in cab}
        self.assertEqual(cabecalhos, {'Elemento', 'Peso', 'Noção', 'Termo', 'O que é'})
        permitidas = {p for c in cabecalhos for p in palavras(c)}
        # O que sai: os números «1) 2) 3)» que a lista numerada do guia substitui.
        saem = {9: {'1', '2', '3'}}
        css = [t for t in TROCAS if t['novo'].startswith('<link rel="stylesheet"')]
        self.assertEqual(sorted(t['ficheiro'] for t in css), sorted(C.COM_TABELA))
        estilo = [t for t in TROCAS if 'code{white-space:nowrap}' in t['novo']]
        self.assertEqual(len(estilo), 1)
        chaves = [t for t in TROCAS if '"nao_partir' in t['novo'] and '"nao_partir' not in t['antigo']]
        self.assertEqual([t['ficheiro'] for t in chaves], ['docs/pedagogia/tarefas-escolha/m9-u1.json', 'docs/pedagogia/tarefas-escolha/m9-u2.json'])
        # Nenhuma troca muda letras: «séc. XVIII» fica abreviado, só com o espaço preso.
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS if 'séc.' in t['antigo']}), [F01])
        for t in TROCAS:
            if 'séc.' in t['antigo'] or 'séc.' in t['novo']:
                self.assertEqual(t['novo'].replace(N, ' '), t['antigo'])
        self.assertFalse([t for t in TROCAS if 'Séc.' in t['antigo'] + t['novo']])
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
                self.assertTrue(t['achado'].startswith('12/11/2026: decisão 152 (cuidado em todas as lições), varredura do M9'))
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
        # Nas listas (achados 11 e 15), o texto é o de antes, letra a letra: sem as marcas, fica o parágrafo que lá estava.
        for t in TROCAS:
            if achados_da_troca(t)[0] in (11, 15):
                with self.subTest(lista=t['ficheiro']):
                    self.assertEqual(soltas(t['novo']), soltas(t['antigo']))
                    self.assertEqual(re.sub(r'\s+', ' ', visivel(t['novo'])).replace(' ,', ',').strip(),
                                     re.sub(r'\s+', ' ', visivel(t['antigo'])).strip())
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
        # O detetor deixa de fora o que não se vê: o data-titulo dos vídeos da F01 e o «alt» da imagem do índice ficam como estavam.
        f01 = ler(F01)
        fora = sorted({C.fora_de_alcance(f01, m.start()) for seq in ('século XVIII', '2 min', 'D. João V', 'capítulo XXI')
                       for m in re.finditer(re.escape(seq), f01)} - {None})
        self.assertEqual(fora, ['atributo data-titulo'])
        indice = ler(INDICE)
        self.assertEqual(sorted({C.fora_de_alcance(indice, m.start()) for m in re.finditer('século XVIII', indice)} - {None}), ['atributo alt'])

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
        for x in C.ACHADOS_B + C.NOTAS:
            final = ler(x['ficheiro'])
            todos = pares_da_pagina(x['ficheiro'])
            for antigo, novo, _ in x['pares']:
                self.assertEqual(C.ocorrencias(final, antigo, novo, todos), [], (x['ficheiro'], antigo))
        # E o contrário: o detetor apanha as formas que partem, e deixa as inteiras.
        for partido in ('p. 22', 'pp. 291 a 293', 'n.º 2', 'capítulo XXI', 'capítulos I e V', 'cap. XXI',
                        'cap. 1', 'canto III', 'estância 20', 'século XVIII', 'Século XVI', 'séc. XVIII', 'ato III', 'página 78',
                        'D. João V', 'D.' + N + 'João V', '3.º ano', '12.º ano', '90 minutos', '10 min', '30 %', '30 segundos',
                        '22 de outubro', '22 de outubro de 1730', '22' + N + 'de outubro de 1730', '13 de janeiro de 1935', 'M9-F03'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for x in C.ACHADOS_B + C.NOTAS:
            for _, novo, _ in x['pares']:
                self.assertIsNone(PARTE.search(C.j(novo) + '0'), novo)
        # O que a conferência tirou não é uma forma que parte: «D.» com nome e sem numeral, e o mês e o ano sem dia.
        for inteiro in ('D. Maria Ana', 'D. Sebastião', 'outubro de 1730', 'agosto de 1709', '52 mil'):
            self.assertIsNone(PARTE.search(inteiro), inteiro)

    def test_camada_fechada_reversivel_e_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m9_20261112.json', '--manifesto', MANIFESTO_REL,
                            # 12/11/2026: por cima desta camada fica agora a decisão 152 no Exame e nas páginas transversais
                            # (cuidado_exame_20261112, que também muda as sessões do Exame); desfaz-se primeiro, com a mesma exigência, e
                            # as contagens são as mesmas.
                            # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            '--verificar', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-provas-oficial-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-exame-edits-20261112.json'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), (242, 36))
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertEqual(len(m['base_commit']), 40)
        self.assertTrue(m['_nota'].startswith('12/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M9'))
        self.assertIn('cuidado_m9_20261112', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        # O rótulo «(notas do docente)» só nas notas editoriais (as da lição gerada F14, sem lista de cartões); os painéis de
        # projeção dizem «(painel de projeção)».
        for t in TROCAS:
            if t['ficheiro'] == NOTAS_F14:
                self.assertNotIn('CARTOES=', ler(t['ficheiro']))
                self.assertIn('(notas do docente)', t['local'])
            elif '/painel-' in t['ficheiro']:
                self.assertIn('CARTOES=', ler(t['ficheiro']))
                self.assertIn('(painel de projeção)', t['local'])
                self.assertNotIn('(notas do docente)', t['local'])
            else:
                self.assertNotIn('(notas do docente)', t['local'])
                self.assertNotIn('(painel de projeção)', t['local'])
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                # 12/11/2026: a página como esta camada a deixou: com a camada de cima (cuidado_exame_20261112) desfeita, com contagem
                # estrita; undo_cuidado_m9_1112 desfaz as duas, a partir da página inteira.
                atual = undo_cuidado_exame_1112(rel, ler(rel))
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_m9_1112(rel, ler(rel))
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
                # A camada de baixo (a decisão 152 no M8) continua a desfazer-se por baixo desta, e não toca em nenhum ficheiro dela.
                # 12/11/2026: na página inteira, porque a cadeia de desfazer começa agora pela decisão 152 no Exame.
                self.assertEqual(undo_cuidado_m8_1112(rel, ler(rel)), b)
                self.assertNotIn(rel, M8['files'])
        # Os 44 achados que entram estão todos na camada; os 8 que ficam de fora e os 8 recusados, não.
        achados = {n for t in TROCAS for n in achados_da_troca(t)}
        self.assertEqual(achados, APLICADOS)
        self.assertEqual((len(A), len(B), len(C_), len(CONFIRMADOS)), (7, 41, 4, 52))
        self.assertEqual((len(APLICADOS), len(B_PAGINAS), len(B_PAINEIS), len(B_NOTAS), len(FORA_DE_AMBITO), len(SO_MATERIAL), len(RECUSADOS)),
                         (44, 27, 5, 1, 6, 2, 8))
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'A'}), sorted(A))
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'C'}), sorted(C_))
        # 42 achados nas páginas do M9 (com os ficheiros dos cartões da F11, da F12 e da F13) e 2 nas das tarefas; a cópia nas
        # sessões do Exame é do achado da F01 (24).
        sitio = {x['i']: x['ficheiro'] for x in C.achados_ac() + C.ACHADOS_B}
        sitio.update({i: rel for rel, i in PAINEL.items()})
        sitio[45] = NOTAS_F14
        self.assertEqual(sorted(sitio), sorted(APLICADOS))
        self.assertEqual(sum(f.startswith('m9/') for f in sitio.values()), 42)
        self.assertEqual(sum(f.startswith('tarefas/') for f in sitio.values()), 2)
        self.assertEqual(sorted(sitio[i] for i in (52, 53, 54)), [F11_JS, F12_JS, F13_JS])
        # A e C antes de B, em cada ficheiro.
        for rel in m['files']:
            ordem = ['B' if '(B)' in t['achado'] and '"nao_partir' not in t['novo'] else 'AC' for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual(ordem, sorted(ordem, key=lambda x: x != 'AC'), rel)
        # No topo da cadeia, logo por cima da decisão 152 no M8.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 12/11/2026: por cima da decisão 152 no M9 fica a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no Exame e nas páginas transversais fica a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da ligação «Treinos» na página principal do Exame ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima das provas em cartões com os documentos oficiais ficam as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M3 mais fáceis de fazer ficam as duas tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M1 mais fáceis de fazer ficam as duas tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[7], ('cuidado_m9_20261112', 'cuidado-m9-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[8], ('cuidado_m8_20261112', 'cuidado-m8-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[9], ('cuidado_m7_20261111', 'cuidado-m7-edits-20261111'))
        self.assertEqual(verificar_camadas.LAYERS[10], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[11], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[12], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        # 12/11/2026: com a decisão 152 no Exame e nas páginas transversais, as camadas passam a ser mais uma.
        # 12/11/2026: com a ligação «Treinos» na página principal do Exame, as camadas passam a ser mais uma.
        # 12/11/2026: com as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112), as camadas passam a ser mais uma.
        # 12/11/2026: com as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112) no topo, as camadas passam de 46 a 47, todas diferentes.
        # 13/11/2026: com a camada das tarefas do M1 mais fáceis de fazer, são 48.
        # 13/11/2026: mais uma camada, as tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): 49 em vez de 48.
        # 13/11/2026: mais uma camada, a das tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113): 50.
        self.assertEqual(len(verificar_camadas.LAYERS), 50)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 50)
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m8_1112'):]
        self.assertLess(corpo.index('undo_cuidado_m9_1112(path, text)'), corpo.index('_CUIDADO_M8_1112.get('))
        self.assertLess(corpo.index('undo_cuidado_m9_1112(path, text)'), corpo.index('_TAREFAS_CLARAS.get('))
        self.assertLess(auditoria.index('def undo_cuidado_m9_1112'), auditoria.index('def undo_cuidado_m8_1112'))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m9-edits-20261112.json'), sala.index('cuidado-m8-edits-20261112.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes da decisão 152 no M8, logo a seguir a --verificar.
        meu, m8 = MANIFESTO_REL, 'tests/fixtures/cuidado-m8-edits-20261112.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + m8 not in linha:
                    continue
                linhas += 1
                # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima desta; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertIn(f'--verificar --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {LT} --desfazer-antes {EX} --desfazer-antes {meu} --desfazer-antes {m8}', linha, wf)
        # As 22 cadeias em que a decisão 152 no M8 se desfaz (as 21 que já desfaziam a do M7 e a conferência da própria camada do
        # M7; a conferência da camada do M8, que só tem esta por cima, vem abaixo).
        self.assertEqual(linhas, 22)
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima desta; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m8_20261112.json --manifesto {m8} --verificar --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {LT} --desfazer-antes {EX} --desfazer-antes {meu}\n',
                      tarefas)
        # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça.
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if not linha.lstrip().startswith('#') and '--desfazer-antes ' + meu in linha:
                    # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) desfaz-se primeiro, logo antes desta.
                    # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    self.assertIn('--verificar --desfazer-antes ' + T6 + ' --desfazer-antes ' + T5 + ' --desfazer-antes ' + T1 + ' --desfazer-antes ' + TF + ' --desfazer-antes ' + PO + ' --desfazer-antes ' + LT + ' --desfazer-antes ' + EX + ' --desfazer-antes ' + meu, linha, wf)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --verificar '
                      # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) desfaz-se primeiro, logo antes desta.
                      # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      f'--desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {LT} --desfazer-antes {EX} --desfazer-antes {meu} --desfazer-antes {m8} --desfazer-antes tests/fixtures/cuidado-m7-edits-20261111.json', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e das decisões 152 no M1 e no M8 conferem as cadeias com frases partidas em várias
            # linhas (e já exigem esta camada à cabeça); ficam de fora pela mesma razão.
            if p.name in ('test_cuidado_m9.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py', 'test_cuidado_m8.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + m8), plano.count(f'--desfazer-antes {meu} --desfazer-antes {m8}'))
        # Nos três que ficam de fora, a cadeia confere-se pelas frases que eles próprios exigem.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn("f'--verificar --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {meu} --desfazer-antes {m7}'", ler('tests/test_cuidado_m8.py'))
        for nome in ('tests/test_creditos_i_pt1.py', 'tests/test_cuidado_m1.py'):
            texto = ler(nome)
            self.assertEqual(texto.count('--desfazer-antes ' + m8), texto.count(f'--desfazer-antes {meu} --desfazer-antes {m8}'), nome)
            # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima desta; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            self.assertEqual(texto.count(f"ROOT/'{m8}',"), texto.count(f"(ROOT/'{T6}',ROOT/'{T5}',ROOT/'{T1}',ROOT/'{TF}',ROOT/'{PO}',ROOT/'{LT}',ROOT/'{EX}',ROOT/'{meu}',ROOT/'{m8}',"), nome)
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima desta; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f"(ROOT/'{T6}',ROOT/'{T5}',ROOT/'{T1}',ROOT/'{TF}',ROOT/'{PO}',ROOT/'{LT}',ROOT/'{EX}',ROOT/'{meu}',ROOT/'{m8}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM9['), texto.index('((cuidadoM8['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM9[rel]'), corpo.index('((cuidadoM8[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M9.read_text'), gerador_148.index('CUIDADO_M8.read_text'))
        # Os geradores dos acertos dos índices (as contagens do M9, onde esta camada prende «90 min») e dos créditos atrás de um «i»
        # do pedido pt-1 (o crédito da imagem do índice do M9, onde esta camada prende «século XVIII») desfazem primeiro esta camada.
        for nome in ('scripts/indices_acertos_20261107.py', 'scripts/creditos_i_pt1_20261107.py'):
            fonte = ler(nome)
            self.assertLess(fonte.index('CUIDADO_M9.read_text'), fonte.index('MANIFESTO.read_text'), nome)
        acertos = ler('scripts/indices_acertos_20261107.py')
        self.assertLess(acertos.index('CUIDADO_M9.read_text'), acertos.index('CUIDADO_M8.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1 ao M8.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima desta; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m9_20261112.json --manifesto {meu} --verificar --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO} --desfazer-antes {LT} --desfazer-antes {EX}\n', tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m9.py' -v", wf)
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m8.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m9.py', apoios)
        for n in range(1, 10):
            self.assertIn(f'python tests/browser_cuidado_m{n}.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m9_20261112.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)

    def test_leitura_historica_das_tarefas_com_esta_camada_por_cima(self):
        # Os contratos históricos leem as tarefas como eram antes do pedido #192 (scripts/tarefas_claras_historico.py). Com esta
        # camada por cima, a leitura dá a base do manifesto do #192, letra a letra, em todas as páginas e dados que ele mudou: a
        # partir da página inteira, com esta camada já desfeita, com esta e a do M8 já desfeitas, com estas e a do M7, ou com as
        # quatro de cuidado já desfeitas; e a cadeia de desfazer não desfaz nada segunda vez sobre esse texto.
        from auditoria_20261028 import undo_cuidado_m5_0811, undo_cuidado_m6_0811, undo_cuidado_m7_1111
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import tarefas_claras_historico as historico
        finally:
            sys.path.pop(0)
        claras = CLARAS
        m7 = json.loads(ler('tests/fixtures/cuidado-m7-edits-20261111.json'))['files']
        m6 = json.loads(ler('tests/fixtures/cuidado-m6-edits-20261108.json'))['files']
        self.assertEqual(len(claras), 33)
        # Nesta camada e na dos enunciados, as tarefas do M9 (as páginas e os dados); nesta e nas do M8 e do M7, nenhum ficheiro; nesta
        # e na do M6, só as sessões do Exame (cada uma com a cópia da sua lição), que a revisão dos enunciados não mudou.
        nossos = {'tarefas/m9-u1/index.html', 'tarefas/m9-u2/index.html', 'docs/pedagogia/tarefas-escolha/m9-u1.json',
                  'docs/pedagogia/tarefas-escolha/m9-u2.json'}
        self.assertEqual(set(MANIFESTO['files']) & set(claras), nossos)
        self.assertEqual(set(MANIFESTO['files']) & set(M8['files']), set())
        self.assertEqual(set(MANIFESTO['files']) & set(m7), set())
        self.assertEqual(set(MANIFESTO['files']) & set(m6), {SESSOES})
        self.assertNotIn(SESSOES, claras)
        for rel, registo in claras.items():
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                antes_192 = historico.desfazer(rel, atual)
                self.assertEqual(sha_lf(antes_192), registo['base_sha256_lf'])
                sem_m9 = undo_cuidado_m9_1112(rel, atual)
                self.assertEqual(historico.desfazer(rel, sem_m9), antes_192)
                sem_m8 = undo_cuidado_m8_1112(rel, atual)
                self.assertEqual(historico.desfazer(rel, sem_m8), antes_192)
                sem_m7 = undo_cuidado_m7_1111(rel, atual)
                self.assertEqual(historico.desfazer(rel, sem_m7), antes_192)
                sem_m6 = undo_cuidado_m6_0811(rel, atual)
                self.assertEqual(sha_lf(sem_m6), registo['after_sha256_lf'])
                self.assertEqual(historico.desfazer(rel, sem_m6), antes_192)
                self.assertEqual(historico.desfazer(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m9_1112(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m8_1112(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m7_1111(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m6_0811(rel, antes_192), antes_192)
                self.assertEqual(undo_cuidado_m5_0811(rel, antes_192), undo_cuidado_m5_0811(rel, atual))
                if rel in MANIFESTO['files']:
                    self.assertNotEqual(sem_m9, atual)
                    self.assertEqual(sha_lf(atual), MANIFESTO['files'][rel]['after_sha256_lf'])
                    self.assertEqual(sha_lf(sem_m9), MANIFESTO['files'][rel]['base_sha256_lf'])
                    self.assertEqual(sem_m8, sem_m9)
                    self.assertEqual(sem_m7, sem_m9)
                    # Fora da exceção (a base exata do #192), a contagem continua estrita: um texto a que falta uma troca falha.
                    e = MANIFESTO['files'][rel]['edits'][0]
                    with self.assertRaises(AssertionError):
                        undo_cuidado_m9_1112(rel, atual.replace(e['new'], e['old'], 1))
                else:
                    self.assertEqual(sem_m9, atual)
        self.assertEqual(sorted(rel for rel in claras if rel in MANIFESTO['files']), sorted(nossos))
        # A ordem no leitor histórico: primeiro esta camada, depois a do M8, a do M7 e a do M6, depois os enunciados.
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer'):]
        self.assertLess(corpo.index('CUIDADO_M9.get(rel)'), corpo.index('CUIDADO_M8.get(rel)'))
        self.assertLess(corpo.index('CUIDADO_M8.get(rel)'), corpo.index('CUIDADO_M7.get(rel)'))
        self.assertLess(corpo.index('CUIDADO_M7.get(rel)'), corpo.index('CUIDADO_M6.get(rel)'))
        self.assertLess(corpo.index('CUIDADO_M6.get(rel)'), corpo.index("entry['edits']"))
        # A camada só se desfaz ali quando o texto é a página como ela a deixou (o hash «after» do manifesto), com contagem estrita.
        self.assertIn("_sha_lf(text) == mais_recente['after_sha256_lf']", corpo)
        self.assertIn("assert text.count(edit['new']) == edit['occurrences'], f'Decisão 152 no M9 não confere: {rel}'", corpo)

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_da_origem(self):
        # As tarefas da M9-U1 e da M9-U2 mudam também nos dados, que estão nesta camada.
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/')}
        self.assertEqual(dados, {'docs/pedagogia/tarefas-escolha/m9-u1.json', 'docs/pedagogia/tarefas-escolha/m9-u2.json'})
        for u in (1, 2):
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/m9-u{u}.json'))
            self.assertIs(d['nao_partir'], True)
            # As chaves do M6 («nao_partir_grelha», «nao_partir_valores») não entram no M9: a proposta não as pede.
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
            for esperada in ('te/tarefas/m9-u1/index.html', 'te/tarefas/m9-u2/index.html', 'gr/tarefas/m9-u1/grelha/index.html',
                             'gr/tarefas/m9-u2/grelha/index.html', 'gr/tarefas/m9-u1/correcao/index.html', 'gr/tarefas/m9-u2/correcao/index.html',
                             'aq/tarefas/m9-u1/aquecimento/index.html', 'aq/tarefas/m9-u2/aquecimento/index.html'):
                self.assertIn(esperada, geradas)
            # O gerador das grelhas não acrescenta outra ligação à tarefa.
            self.assertFalse([g for g in geradas if g.startswith('gr/') and g.count('/') == 3])
            self.assertGreater(len(geradas), 50)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel.split('/', 1)[1]).read_bytes())
        # As páginas das tarefas que a camada muda são estas duas; os aquecimentos, as grelhas e as correções do M9 ficam como estavam.
        self.assertEqual(sorted(f for f in MANIFESTO['files'] if f.startswith('tarefas/')), ['tarefas/m9-u1/index.html', 'tarefas/m9-u2/index.html'])
        # As lições F14, F15 e F16 são geradas (scripts/gerar_licoes_20261101.py): mudam nas fontes, fora da camada (como no M5,
        # no M6 e no M8), e as lições e as suas notas saem iguais do gerador, letra a letra. Das notas, só as da F14 mudam (um
        # retorno que repete o nome do rei, o achado 45).
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import gerar_licoes_20261101 as gerador_licoes
            from licoes_20261101 import LESSONS
        finally:
            sys.path.pop(0)
        self.assertEqual(sorted(x['id'] for x in LESSONS if x['id'].startswith('m9-')), sorted(GERADAS))
        unidades = gerador_licoes.sequences()
        for item in LESSONS:
            licao, notas = f"{item['id'][:2]}/licao-{item['id']}/index.html", f"{item['id'][:2]}/painel-{item['id']}/index.html"
            with self.subTest(licao=item['id']):
                self.assertEqual(gerador_licoes.render(item, unidades), ler(licao))
                self.assertEqual(gerador_licoes.render_notes(item), ler(notas))
                if item['id'] in GERADAS:
                    self.assertIn(licao, MANIFESTO['files'])
                    self.assertEqual(notas in MANIFESTO['files'], notas == NOTAS_F14)
                    if notas != NOTAS_F14:
                        self.assertEqual(base(notas), ler(notas))
                else:
                    self.assertNotIn(licao, MANIFESTO['files'])
                    self.assertNotIn(notas, MANIFESTO['files'])
        # Nas notas da F14 muda uma referência só, e mais nada: o mesmo retorno, com o nome do rei preso.
        notas = ler(NOTAS_F14)
        self.assertEqual(notas.replace(N, ' '), base(NOTAS_F14))
        self.assertEqual((notas.count(N) - base(NOTAS_F14).count(N), notas.count('ficcional do reinado de D.' + N + 'João' + N + 'V.</li>')), (2, 1))
        self.assertEqual([(achados_da_troca(t), t['ocorrencias']) for t in TROCAS if t['ficheiro'] == NOTAS_F14], [([45], 1)])
        # Nenhuma lição gerada do M9 leva tabela nova: a folha das tabelas fica como o gerador a punha (só na M8-F15).
        for item in LESSONS:
            pagina = gerador_licoes.render(item, unidades)
            self.assertEqual(pagina.count('apoios-tabelas.css'), 1 if item['id'] == 'm8-f15' else 0, item['id'])
        # Nenhuma fonte fica com um trecho de antes; cada linha mudada leva o seu comentário datado.
        licoes, confirmacao = ler('scripts/licoes_20261101.py'), ler('scripts/revisao_confirmacao_20261101.py')
        for antigo in ('ficcional do reinado de D. João V', 'Resumo didático do capítulo I:', 'Porto Editora, p. 22)', ', n.º 2, julho de 2015, p. 33',
                       'No capítulo V de <i>Memorial', 'anexo XI, página 78 do PDF', 'indica p. 49 do romance', 'recurso 2363389, página 1 do PDF'):
            self.assertNotIn(antigo, licoes + confirmacao, antigo)
        self.assertEqual(licoes.count('decisão 152 no M9'), 6)
        self.assertEqual(confirmacao.count('decisão 152 no M9'), 1)
        for fonte in (licoes, confirmacao):
            for linha in fonte.split('\n'):
                if 'decisão 152 no M9' in linha:
                    self.assertTrue(linha.lstrip().startswith('# 12/11/2026: decisão 152 no M9 (achado'), linha[:80])
                    self.assertIn('camada cuidado_m9_20261112', linha)


if __name__ == '__main__':
    unittest.main()
