"""08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M4. Camada literal cuidado_m4_20261108
(scripts/cuidado_m4_20261108.json, gerada por scripts/cuidado_m4_20261108.py; manifesto tests/fixtures/cuidado-m4-edits-20261108.json),
a mais recente, por cima da decisão 152 no M3 (cuidado_m3_20261108).

Este teste confere, no modelo de tests/test_cuidado_m1.py, tests/test_cuidado_m2.py e tests/test_cuidado_m3.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices e o gerador do desenho comum dos índices;
* cada um dos 38 achados confirmados: as 6 tabelas novas (6 achados A), com a legenda, o cabeçalho (th scope=col), a primeira coluna
  (th scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato, no cartão e no
  sítio certos (as listas que fecham e reabrem com start); os 3 casos do mesmo tipo (C), com o texto exato; os 29 achados B, com a
  contagem certa de cada sequência (das mais longas para as mais curtas, como a varredura) e a forma da proposta final, sem nenhuma
  ocorrência que se parta fora do que fica de fora (o «alt», o <title>, os desenhos, a «frase» de um sublinhar), e a casca das
  lições, que fica para o molde; onde o número que se muda não é o da proposta, o achado diz porquê;
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e que a folha (a do M1) já tem
  as regras do cartão escuro e as de fora das lições;
* que nenhum dos 9 achados recusados (5, 6, 7, 8, 9, 10, 11, 12 e 17) entrou;
* as regras do texto: as tabelas só usam texto que já estava na página (o do trecho, o de outros cartões da mesma lição, como pede a
  proposta, e os cabeçalhos); nada de «professor», «jogar», «jogo», «ficha», «folha», «—» ou «·» novos; nenhum U+00A0 nem U+2060
  novo dentro de alt, aria-label, href, title, <title>, chaves JSON ou da «frase» de um sublinhar; nas passagens mudadas, nenhuma
  referência nem número que se parta;
* que os aquecimentos da M4-U1, da M4-U2 e da M4-U3 (discurso) saem iguais dos dados e do gerador, e que os painéis do docente
  seguem os enunciados das lições."""
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
from auditoria_20261028 import undo_cuidado_m4_0811, undo_cuidado_m3_0811  # noqa: E402
# 08/11/2026: por cima desta camada fica a decisão 152 no M5 (camada cuidado_m5_20261108).
from auditoria_20261028 import undo_cuidado_m5_0811  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m4_20261108.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m4-edits-20261108.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
BASE_COMMIT = 'e0057725ef24acd7ee02d578f980051870bc86dc'
NBSP, WJ = '\xa0', '⁠'
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
A = {0, 1, 2, 3, 4, 13}
B = set(range(18, 47))
C_ = {14, 15, 16}
CONFIRMADOS = A | B | C_
RECUSADOS = {5, 6, 7, 8, 9, 10, 11, 12, 17}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)
N = NBSP

# (página, índice da tabela na página, legenda, cabeçalho, linhas, larguras): o texto de cada célula, como se lê.
TABELAS = [
    # achado 3, F10, cartão 8 («Decide», Ler mais): as passagens das aulas
    ('m4/licao-m4-f10/index.html', 0, None, ['Aula', 'Passagem'],
     [['aula' + N + '1', '«Mudou somente o púlpito e o auditório, mas não desistiu da doutrina»; «faltou pouco, para que lhe não tirassem a '
       'vida»'],
      ['aulas' + N + '2 e' + N + '4', '«os ouvintes, sendo verdadeira a doutrina que lhes dão, a não querem receber»'],
      ['aula' + N + '3', '«para a cidade é que haveis de olhar»'],
      ['aula' + N + '4', '«Ao menos têm os peixes duas boas qualidades de ouvintes: ouvem e não falam»'],
      ['aula' + N + '5', '«A vossa bruteza é melhor que a minha razão»'],
      ['aulas' + N + '5 e' + N + '6', '«Oh que boa doutrina era esta para a terra, se eu não pregara para o mar!»']], None),
    # achado 0, F10, cartão 13 («Recorda»): os quatro peixes
    ('m4/licao-m4-f10/index.html', 1, None, ['Peixe', 'No texto', 'Traço'],
     [['Roncadores', 'pequenos e barulhentos, «as roncas do mar»', 'fazer mais ruído do que se vale'],
      ['Pegadores', '«nunca os desferram»', 'viver à custa de quem tem poder'],
      ['Voadores', '«porque vos quereis ser aves?»', 'querer ser mais do que se é'],
      ['Polvo', '«parece» manso e ataca de emboscada', 'trair com cara de bondade']], None),
    # achado 1, F25, cartão 17 («Para levar», cartão escuro)
    ('m4/licao-m4-f25/index.html', 0, 'Quatro peixes repreendidos, quatro vícios', ['Peixe', 'Traço e palavras', 'Vício dos homens'],
     [['Roncadores', 'pequenos e barulhentos, «as roncas do mar»', 'barulho sem valor'],
      ['Pegadores', '«nunca os desferram» e vivem à custa do maior', 'viver à custa dos poderosos'],
      ['Voadores', 'querem ser aves, e ao voador «mata-o a vaidade de voar»', 'presunção'],
      ['Polvo', '«parece um monge» e ataca de emboscada', 'traição com cara mansa']], None),
    # achado 2, F06, cartão 16 («Para levar», cartão escuro)
    ('m4/licao-m4-f06/index.html', 0, 'Os cinco atos de fala', ['Ato', 'O que faz', 'Exemplo'],
     [['Assertivo', 'afirma, e pode ser verdadeiro ou falso', '«os grandes comem os pequenos»'],
      ['Diretivo', 'leva quem ouve a fazer alguma coisa; obriga quem ouve', '«Olhai, peixes»; «traz-me»'],
      ['Expressivo', 'mostra o que sente quem fala', '«Oh…!»; «Quem me dera…»'],
      ['Compromissivo', 'obriga quem fala', '«trago-te»'],
      ['Declarativo', 'muda a realidade quando o diz quem tem autoridade; não é o mesmo que frase declarativa',
       '«Declaro eleita delegada de turma a Marta.»']], ['width:11em', None, None]),
    # achado 4, F14, cartão 16 («Agora, em papel», Um exemplo)
    ('m4/licao-m4-f14/index.html', 0, None, ['Peça', 'No exemplo'],
     [['Regra', 'comemos todos à mesma mesa, três vezes por dia, à mesma hora.'],
      ['Argumento' + N + '1', 'a comida chega para todos se for repartida às claras; ontem à noite a caixa das bolachas ficou vazia e hoje de '
       'manhã ninguém sabia quem as tinha comido.'],
      ['Argumento' + N + '2', 'à mesa fala-se; a discussão de terça sobre o gerador acabou ao jantar, com toda a gente sentada.'],
      ['Objeção', '«E quem tem fome fora de horas?»'],
      ['Resposta', 'cada um guarda uma peça de fruta com o seu nome na prateleira; ninguém passa fome, só não se come o que é dos outros.'],
      ['Apelo', 'votem a mesa comum.']], None),
    # achado 13, guia da tarefa (fora das lições): o guião de exemplo dos pegadores
    ('m4/guia-da-tarefa-m4/index.html', 0, None, ['Parte', 'No guião'],
     [['Abertura', '«Quem aqui já viu alguém subir agarrado a outro?»'],
      ['Vieira', 'no capítulo' + N + 'V, repreende os pegadores: peixes pequenos que se colam aos grandes e vivem do que eles comem; o recurso '
       'é a antítese entre o grande que trabalha e o pequeno que só se agarra.'],
      ['Hoje', 'a conta que cresce a repetir o que outra conta diz, sem fazer nada de seu.'],
      ['Objeção', '«mas partilhar também é trabalho».'],
      ['Resposta', 'Vieira distingue quem nada ao lado de quem se cola; partilhar com nome e ideia própria é nadar ao lado.'],
      ['Fecho', 'a pergunta do princípio, agora com o peixe à vista.'],
      ['Imagens', 'a gravura do peixe, uma captura de ecrã sem nomes, a frase de Vieira.']], ['width:25%', 'width:auto']),
]
# Onde está cada tabela nas lições: (página, tabela) > (índice do cartão, o que fica por cima da tabela, o que fica a seguir).
LUGARES = {
    ('m4/licao-m4-f10/index.html', 0): (8, '<summary>Ler mais</summary><div><p>Passagens das aulas da unidade que servem a resposta:</p>'
                                           '<table class="apoio-tabela"', '</table></div></details>'),
    ('m4/licao-m4-f10/index.html', 1): (13, 'Procura na tabela a frase em que Vieira lhe pergunta porquê.</p><table class="apoio-tabela"',
                                        '</table><details class="mais"><summary>Ler mais</summary>'),
    ('m4/licao-m4-f25/index.html', 0): (17, 'É a ironia.</li></ol><table class="apoio-tabela" role="table"><caption>',
                                        '</table><ol start="3"><li>Uma comparação de hoje precisa de prova'),
    ('m4/licao-m4-f06/index.html', 0): (16, 'exprimir, declarar).</li></ol><table class="apoio-tabela" role="table"><caption>',
                                        '</table><ol start="2"><li>A forma não decide o ato:'),
    ('m4/licao-m4-f14/index.html', 0): (16, '<summary>Um exemplo</summary><div><table class="apoio-tabela"', '</table></div></details>'),
}
# Os cartões escuros («Para levar»), onde valem as regras do cartão escuro da folha.
ESCUROS = {('m4/licao-m4-f25/index.html', 0), ('m4/licao-m4-f06/index.html', 0)}

# O que a proposta final conta, sequência a sequência (o primeiro número de cada linha; None onde não dá número).
PROPOSTA = {
    18: {'cap. I': 12, 'cap. VI': 2, 'caps. II e III': 1, 'caps. IV e V': 2, 'séc. XVIII': 1, '13 de junho de 1654': 2, '90 minutos': 1, '1 min': 1, '2.º ano': 1, '1.º sermão': 1, '1.º tomo': 1, 'M4-F01': 2, 'c. 1535-1540': 1, 'Mateus 5,13': 1, 'aula 2': 1},
    19: {'cap. I': 13, 'cap. VI': 1, 'caps. II e III': 1, 'séc. XVIII': 1, '13 de junho de 1654': 1, '13 de junho': 1, '90 minutos': 1, '2.º ano': 1, 'M4-F02': 2, 'c. 1535-1540': 1, 'Mateus 5, 13': 3, '§ I': 3, '(IV e V)': 1, 'aula 1': 4},
    20: {'cap. IV': 10, 'caps. II e III': 1, 'cap. V': 2, 'caps. I e V': 1, 'cap. I': 1, '90 minutos': 1, '2.º ano': 1, 'M4-F04': 2},
    21: {'caps. II, IV, V e VI': 1, 'cap. V': 1, 'cap. IV': 3, '90 minutos': 1, '2.º ano': 1, 'M4-F06': 2},
    22: {'século XVI': 1, 'ato I': 8, 'cenas XI e XII': 3, 'cena XI': 3, 'cena V': 2, 'cenas VII e VIII': 1, 'cena IX': 1, 'Ato I': 2, 'cena XII': 1, 'cena VIII': 5, 'cena VII': 3, 'Cena XII': 1, 'Ato II': 1, 'cena I': 3, 'cena IV': 1, 'ato II': 2, '90 minutos': 1, '2.º ano': 1, 'M4-F07': 2, 'aula 4': 1},
    23: {'ato II': 8, 'cenas I, XIV e XV': 1, 'cena I': 5, 'Ato II': 2, 'cena II': 1, 'ato I': 1, 'cenas XIV e XV': 2, 'cena XV': 1, 'Cena XIV': 1, 'Cena XV': 1, 'cenas I e XIV': 1, 'ato III': 2, 'cena V': 1, '90 minutos': 1, '2.º ano': 1, 'M4-F08': 2},
    24: {'ato III': 13, 'cena XI': 14, 'ato II': 16, 'cenas X e XI': 1, 'cena I': 7, 'Ato III': 4, 'ato I': 2, 'cena VIII': 1, 'cenas I e VIII': 1, 'cena XII': 3, 'cena V': 2, '90 minutos': 1, '2.º ano': 1, 'M4-F09': 2, 'aula 1': 1, 'aula 4': 3, 'aula 10': 2, 'aula 12': 1},
    25: {'cap. V': 4, 'cap. IV': 2, 'cap. I': 2, 'cap. VI': 1, 'capítulo V': 2, '90 minutos': 1, '20 segundos': 2, '150 a 200 palavras': 1, '1 min': 1, '2.º ano': 1, 'M4-F10': 2, 'aula 1': None, 'aula 3': None, 'aula 4': None, 'aula 5': None},
    26: {'cap. I': 4, 'caps. II e III': 1, 'caps. IV e V': 1, 'cap. VI': 1, 'séc. XVIII': 1, 'ato I': 2, 'cenas XI e XII': 2, 'cena XI': 2, 'cena XII': 1, 'ato III': 3, 'cena V': 1, '13 de junho de 1654': 1, '90 minutos': 1, '100 a 140 palavras': 4, '140 palavras': 1, '131 palavras': 1, '2.º ano': 1, 'M4-F11': 2},
    27: {'5 de outubro de 1915': 4, '5 de outubro de 1910': 1, '14 de maio': 1, '9 de março de 1916': 1, '90 minutos': 1, '2.º ano': 1, '3.º parágrafo': 2, '5.º aniversário': 1, '1.ª frase': 1, '2.ª frase': 1, 'n.º 7': 1, 'M4-F14': 2, 'aula 8': 1},
    28: {'cap. IV': 11, '90 minutos': 1, '2.º ano': 1, 'M4-F15': 2, 'aula 3': 2, 'aula 12': 1},
    29: {'Cena XI': 1, 'Cena XII': 1, 'ato I': 5, 'cena XI': 2, 'cena XII': 5, '90 minutos': 2, '2.º ano': 1, 'M4-F20': 2},
    30: {'caps. I, II e V': 1, 'cap. IV': 1, 'caps. I e II': 1, 'cap. I': 1, 'cap. II': 3, 'caps. II e III': 1, 'caps. IV e V': 1, 'cap. V': 6, '90 minutos': 1, '2.º ano': 1, 'M4-F25': 2, 'aula 1': 2, 'aula 2': 1, 'aula 6': 1},
    31: {'ato I': 3, 'cenas XI e XII': 3, 'ato II': 11, 'cenas I, XIV e XV': 1, 'ato III': 5, 'cena XI': 4, 'cena VIII': 1, 'cena XII': 1, 'cena I': 2, 'cena II': 5, 'cenas XIV e XV': 1, 'cena XV': 2, 'cena XIV': 1, '90 minutos': 1, '2.º ano': 1, 'M4-F26': 2, 'c. 1571-1574': 1},
    32: {'cap. IV': 2, 'ato II': 5, 'cena I': 4, 'ato I': 2, 'cena II': 2, '90 minutos': 1, '2.º ano': 1, 'M4-F27': 2, 'aula 3': 1},
    33: {'ato I': 4, 'cena II': 1, 'cena I': 3, '5 min': 1, '45 minutos': 3, '15 minutos': 1, '8 min': 2, '7 min': 1, '15 min': 1, '3 min': 1, '80 a 120 palavras': 1, '60 segundos': 1, '4 min': 1, '10 min': 1, '1799–1854': 1},
    34: {'cap. I': 5, 'ato I': 2, 'ato II': 8, 'cena XI': 1, 'ato III': 2, 'cena I': 1, 'cena XV': 2, '13 de junho de 1654': 2, '5 de outubro de 1915': 1, '90 minutos': 6, '25 %': 1, '10 %': 1, '15 %': 1, '90 min': 6, '10 min': 3, '150 a 200 palavras': 1, '100 a 140 palavras': 1, '2.º ano': 2, '1665–1667': 1, 'Mateus 5, 13': 1},
    35: {'90 min': 1, '10 minutos': 1, '150 a 200 palavras': 1, '3 a 4 minutos': 1},
    36: {'Ato I': 1, 'ato I': 1, '90 min': 1, '10 minutos': 1, '180 a 240 palavras': 1},
    37: {'90 min': 1, '10 minutos': 1, '220 a 280 palavras': 1, '2 minutos': 1},
    38: {'ato I': 1, 'cena XII': 1, '100 a 140 palavras': 2, '10 min': 4, '60 min': 1, '30 min': 1, '15 min': 1, '5 min': 1, '140 palavras': 2, 'M4-F11': 3},
    39: {'cap. I': 4, 'cap. V': 2},
    40: {'ato III': 1, 'ato II': 7, 'cena IV': 8},
    41: {'350 palavras': 1, '220 a 280 palavras': 2, '7.º B': 1},
    42: {'capítulo V': 1, 'ato I': 1, 'ato II': 1, '90 min': 3, '150 a 200 palavras': 1, '3 minutos': 1, '220 a 280 palavras': 2, '180 a 240 palavras': 2, '2.º ano': 2, 'aulas 1 a 8': 1, 'aulas 9 a 15': 1, 'aulas 16 a 18': 1},
    43: {'ato I': 12, 'Ato I': 1, 'cena II': 1, 'ato II': 7, 'cena I': 3, 'cena VIII': 2, 'Ato II': 1, 'cena XIV': 2, 'cenas XIV e XV': 1, 'cena XV': 1, 'ato III': 6, 'Ato III': 1, 'cena XI': 1, '25 min': 1, '2.º ano': 1, 'n.º 17591': 6},
    44: {'Cap. I': 1, 'Cap. IV': 1, 'cap. V': 1, 'Cap. V': 1, 'Cap. VI': 1, 'capítulo IV': 3, 'capítulo V': 2, '13 de junho de 1654': 1, '25 min': 1, '2.º ano': 1, 'a objeção do Ato 4': 1},
    45: {'cap. I': 1, 'caps. II e III': 1, 'caps. IV e V': 1, 'séc. XVIII': 1, 'século II d.C.': 1, '13 de junho de 1654': 2, '4 de agosto de 1578': 1, '90 min': 3, '25 %': 4, '10 %': 1, '45 minutos': 1, '15 %': 1, '2.º ano': 2, 'c. 1535-1540': 1, 'c. 1571-1574': 1, 'aulas 1 a 8': 1, 'aulas 9 a 15': 1, 'aulas 16 a 18': 1, 'M4-F01': 5, 'M4-F08': 3, 'M4-F07': 1, 'M4-F14': 1, 'M4-F10': 1, 'M4-F26': 1, '1608 – Bahia': 1, '1799 – Lisboa': 1},
    46: {'2.º ano': 2, 'aulas 1 a 8': 1, 'aulas 9 a 15': 1, 'aulas 16 a 18': 1},
}
# As formas da proposta final que não prendem todos os espaços (as outras prendem cada espaço, e o traço de intervalo leva a junção).
FORMAS = {
    'caps. II e III': 'caps.' + N + 'II e' + N + 'III', 'caps. IV e V': 'caps.' + N + 'IV e' + N + 'V', 'caps. I e V': 'caps.' + N + 'I e' + N + 'V',
    'caps. I e II': 'caps.' + N + 'I e' + N + 'II', 'caps. II, IV, V e VI': 'caps.' + N + 'II, IV, V e' + N + 'VI',
    'caps. I, II e V': 'caps.' + N + 'I, II e' + N + 'V', '(IV e V)': '(IV e' + N + 'V)',
    'cenas XI e XII': 'cenas' + N + 'XI e' + N + 'XII', 'cenas VII e VIII': 'cenas' + N + 'VII e' + N + 'VIII',
    'cenas I, XIV e XV': 'cenas' + N + 'I, XIV e' + N + 'XV', 'cenas XIV e XV': 'cenas' + N + 'XIV e' + N + 'XV',
    'cenas I e XIV': 'cenas' + N + 'I e' + N + 'XIV', 'cenas X e XI': 'cenas' + N + 'X e' + N + 'XI', 'cenas I e VIII': 'cenas' + N + 'I e' + N + 'VIII',
    '13 de junho de 1654': '13' + N + 'de' + N + 'junho de' + N + '1654', '5 de outubro de 1915': '5' + N + 'de' + N + 'outubro de' + N + '1915',
    '5 de outubro de 1910': '5' + N + 'de' + N + 'outubro de' + N + '1910', '9 de março de 1916': '9' + N + 'de' + N + 'março de' + N + '1916',
    '4 de agosto de 1578': '4' + N + 'de' + N + 'agosto de' + N + '1578',
    'aulas 1 a 8': 'aulas' + N + '1 a' + N + '8', 'aulas 9 a 15': 'aulas' + N + '9 a' + N + '15', 'aulas 16 a 18': 'aulas' + N + '16 a' + N + '18',
    'a objeção do Ato 4': 'a objeção do Ato' + N + '4', '1608 – Bahia': '1608' + N + '– Bahia', '1799 – Lisboa': '1799' + N + '– Lisboa',
    'M4-F01': 'M4-' + WJ + 'F01', 'M4-F07': 'M4-' + WJ + 'F07', 'M4-F08': 'M4-' + WJ + 'F08', 'M4-F10': 'M4-' + WJ + 'F10',
    'M4-F11': 'M4-' + WJ + 'F11', 'M4-F14': 'M4-' + WJ + 'F14', 'M4-F26': 'M4-' + WJ + 'F26',
    '1799–1854': '1799–' + WJ + '1854', '1665–1667': '1665–' + WJ + '1667', 'Mateus 5,13': 'Mateus' + N + '5,13',
}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a proposta pede U+00A0, ou traço de intervalo sem U+2060,
# ou hífen entre anos, ou o hífen da sigla «M4-Fxx» sem a junção. As formas do M4 (capítulo, ato e cena com o número romano, «séc.»,
# «c.», «n.º», «§», ordinal e nome, número e unidade, datas, intervalos «N a M», «aula» e «aulas» com o número, «Mateus 5, 13»,
# «século II d.C.», o ano antes do traço «1608 – Bahia»). Os espaços que a proposta deixa ficam: nas datas, entre o mês e o «de» do
# ano; nas listas, à volta das vírgulas e antes do «e»; em «aulas 1 a 8», antes do «a».
MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'
PARTE = re.compile(
    r'(?<![\w.])(?:[Cc]aps?|séc|c)\. (?=[\dIVXLC])'
    r'|n\.º (?=\d)|§ (?=[IVX])'
    r'|\b(?:[Cc]apítulos?|[Aa]tos?|[Cc]enas?|séculos?|aulas?|Mateus) (?=[\dIVXLC]+\b)'
    r'|\d\.[ºª] (?=\w)'
    r'|\d (?=(?:min|minutos|segundos|palavras|%)(?!\w))'
    r'|(?<!aulas\xa0)\b\d+ [ae][ \xa0]\d|\b\d+[ \xa0][ae] \d'
    r'|\b\d{1,2} de (?=' + MESES + r')|\b\d{1,2}\xa0de (?=' + MESES + r')'
    r'|\b[IVX]+ d\.C\.'
    r'|\b1\d{3} –'
    r'|\d–(?!⁠)\S|\b1\d{3}-\d{4}\b|\bM4-(?!⁠)F\d')


def ler(rel):
    return desfazer_enunciados(rel, (ROOT / rel).read_bytes().decode('utf-8'))


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def gerador():
    spec = importlib.util.spec_from_file_location('cuidado_m4_20261108', ROOT / 'scripts/cuidado_m4_20261108.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


C = gerador()


def cartoes(texto):
    """Os cartões de uma lição (ou do banco da F28)."""
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0]


def visivel(fragmento):
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragmento.replace('\\"', '"').replace('<\\/', '</').replace('\\n', '\n')))


def palavras(texto):
    return set(re.findall(r'[\wÀ-ÿ]+', visivel(texto).lower()))


def base(rel):
    """A página sem esta camada (desfeita pelo manifesto, com contagem estrita)."""
    return undo_cuidado_m4_0811(rel, ler(rel))


class Tabela(HTMLParser):
    def __init__(self, fonte):
        super().__init__()
        self.tabela, self.legenda, self.linhas, self.atual, self.grupos, self.em_legenda = None, None, [], None, [], False
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'table':
            self.tabela = a
        elif tag == 'caption':
            self.em_legenda, self.legenda = True, ''
        elif tag in ('thead', 'tbody'):
            self.grupos.append((tag, a))
        elif tag == 'tr':
            self.linhas.append({'attrs': a, 'grupo': self.grupos[-1][0], 'celulas': []})
        elif tag in ('th', 'td'):
            self.atual = {'tag': tag, 'attrs': a, 'texto': ''}
            self.linhas[-1]['celulas'].append(self.atual)

    def handle_data(self, data):
        if self.em_legenda:
            self.legenda += data
        elif self.atual is not None:
            self.atual['texto'] += data

    def handle_endtag(self, tag):
        if tag in ('th', 'td'):
            self.atual = None
        elif tag == 'caption':
            self.em_legenda = False


def tabelas_da_pagina(texto, classe='apoio-tabela'):
    out = []
    for m in re.finditer(r'<table class=\\?"' + classe + r'\\?"', texto):
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


class CuidadoM4(unittest.TestCase):
    def test_seis_tabelas_com_legenda_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 6)
        for rel, k, legenda, cabecalho, linhas, larguras in TABELAS:
            t = Tabela(tabelas_da_pagina(ler(rel))[k])
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(t.tabela.get('class'), 'apoio-tabela')
                self.assertEqual(t.tabela.get('role'), 'table')
                # A legenda só nas duas «Para levar» (F06 e F25), como na proposta; nas lições, a folha dá-lhe estilo.
                self.assertEqual(t.legenda, legenda)
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
                    self.assertTrue(primeira['texto'].strip())
                    for coluna, c in enumerate(resto, 1):
                        self.assertEqual((c['tag'], c['attrs'].get('role'), c['attrs'].get('data-label')), ('td', 'cell', cabecalho[coluna]))
                        self.assertTrue(c['texto'].strip())
                # Só duas têm larguras: a do guia (fora das lições), onde a parte do guião, uma palavra, fica estreita e o texto fica com
                # o resto; e a da F06, onde a coluna do ato leva 11em (cresce com a letra), para «Compromissivo» não se partir a meio.
                self.assertEqual([c['attrs'].get('style') for c in topo['celulas']], larguras or [None] * len(cabecalho))
        # Nenhuma página do M4 (nem as suas tarefas e aquecimentos, nem o banco da F28) tem mais tabelas de apoio do que estas.
        contagem = {}
        for rel, *_ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        paginas = (sorted(glob.glob(str(ROOT / 'm4/**/index.html'), recursive=True))
                   + sorted(glob.glob(str(ROOT / 'tarefas/m4-*/**/index.html'), recursive=True)) + [str(ROOT / 'm4/recursos/tpc-entrada.js')])
        for p in paginas:
            rel = Path(p).relative_to(ROOT).as_posix()
            with self.subTest(pagina=rel):
                self.assertEqual(len(tabelas_da_pagina(ler(rel))), contagem.get(rel, 0))

    def test_tabelas_nos_cartoes_e_nos_sitios_certos(self):
        for (rel, k), (indice, antes, depois) in LUGARES.items():
            cards = cartoes(ler(rel))
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(cards[indice]['t'], 'ler')
                self.assertIn(antes, cards[indice]['html'])
                self.assertIn(depois, cards[indice]['html'])
                self.assertEqual(cards[indice].get('escuro') is True, (rel, k) in ESCUROS)
        # Na F10, as duas tabelas estão nos cartões 8 e 13; nas outras lições, cada uma no seu cartão.
        for rel in sorted({r for r, _ in LUGARES}):
            esperados = sorted(i for (r, _), (i, _, _) in LUGARES.items() if r == rel)
            self.assertEqual([i for i, c in enumerate(cartoes(ler(rel))) if 'apoio-tabela' in c.get('html', '')], esperados, rel)
        # As duas listas «As frases da aula» fecham antes da tabela e reabrem a seguir com start: a numeração continua.
        f06, f25 = cartoes(ler('m4/licao-m4-f06/index.html'))[16]['html'], cartoes(ler('m4/licao-m4-f25/index.html'))[17]['html']
        self.assertEqual(re.findall(r'<li>', f06), ['<li>'] * 2)
        self.assertEqual(re.findall(r'<li>', f25), ['<li>'] * 3)
        self.assertEqual((f06.count('<ol>'), f06.count('<ol start="2">'), f06.count('</ol>')), (1, 1, 2))
        self.assertEqual((f25.count('<ol>'), f25.count('<ol start="3">'), f25.count('</ol>')), (1, 1, 2))
        # O guia: a tabela fica dentro de um div.ex (a letra do exemplo), e a nota «Porque funciona» fica a seguir, igual.
        guia = ler('m4/guia-da-tarefa-m4/index.html')
        self.assertIn('(guião da apresentação, 3' + N + 'minutos)</summary><div><div class="ex"><table class="apoio-tabela" role="table">', guia)
        self.assertIn('</tbody></table></div><p class="pequeno">Porque funciona: Citação localizada', guia)
        self.assertNotIn('<p class="ex">Abertura:', guia)
        self.assertIn('.ex{font-family:Georgia,"Times New Roman",serif;line-height:1.55}', guia)
        # O M4 não ganha a tabela dos pesos (achado 17, recusado): o índice continua com o parágrafo.
        self.assertNotIn('apoio-tabela', ler('m4/index.html'))

    def test_folha_das_tabelas_antes_da_aparencia(self):
        com_tabela = sorted({r for r, *_ in TABELAS})
        self.assertEqual(com_tabela, sorted(C.COM_TABELA))
        for rel in com_tabela:
            cabeca = ler(rel).split('</head>')[0]
            with self.subTest(pagina=rel):
                self.assertEqual(cabeca.count(FOLHA), 1)
                self.assertLess(cabeca.index(FOLHA), cabeca.index('assets/appearance.css'))
        # As outras páginas do M4 não carregam a folha.
        for p in sorted(glob.glob(str(ROOT / 'm4/**/index.html'), recursive=True)) + sorted(glob.glob(str(ROOT / 'tarefas/m4-*/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            if rel not in com_tabela:
                self.assertNotIn('apoios-tabelas.css', ler(rel), rel)
        # A folha é a do M1 e não muda: as regras das lições (.jogo .ler), as do cartão escuro e as de fora das lições já lá estão.
        css = ler('assets/pt-lessons/apoios-tabelas.css')
        self.assertIn('.jogo .ler .apoio-tabela td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertIn('.jogo .cartao.escuro .ler .apoio-tabela thead th{background:transparent;color:inherit;border-bottom:2px solid currentColor}', css)
        self.assertIn('.jogo .cartao.escuro .ler .apoio-tabela td[data-label]::before{color:inherit}', css)
        self.assertIn('.apoio-tabela:not(.jogo .ler .apoio-tabela) td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertNotIn('assets/pt-lessons/apoios-tabelas.css', {t['ficheiro'] for t in TROCAS})

    def test_casos_do_mesmo_tipo(self):
        # Achado 14: na F10, «O que conta» do cartão 3 passa a lista numerada, como nos outros cartões; o resto do parágrafo fica.
        c3 = cartoes(ler('m4/licao-m4-f10/index.html'))[3]['html']
        self.assertIn('<p>O que conta:</p><ol><li>A citação certa e localizada.</li><li>O recurso nomeado e explicado.</li><li>O comportamento '
                      'de hoje sem visar ninguém.</li><li>A objeção respondida com prova no texto.</li><li>Três a quatro minutos.</li><li>Imagens '
                      'com crédito.</li></ol><p>Conta também o processo: três aberturas de 20' + N + 'segundos (uma pergunta, uma imagem ou uma '
                      'citação lida como sermão), testadas para escolher uma, e um ensaio com relógio em que se muda alguma coisa.</p>', c3)
        self.assertNotIn('O que conta: a citação', c3)
        # Achado 15: no mapa, cada termo junto da sua definição, sem linhas novas (os mesmos dt e dd).
        mapa = ler('m4/mapa-do-modulo-m4/index.html')
        self.assertIn('<dt>apóstrofe, anáfora, antítese, gradação</dt><dd>apóstrofe, chamar («irmãos peixes»); anáfora, repetir no início; '
                      'antítese, opor contrários; gradação, subir degrau a degrau.</dd>', mapa)
        self.assertIn('<dt>presságio, revelação, catástrofe</dt><dd>os passos da tragédia: presságio, os sinais; revelação, a verdade que se '
                      'descobre; catástrofe, a queda.</dd>', mapa)
        dl = re.search(r'<details class="sec" id="palavras">.*?</details>', mapa, re.S).group(0)
        dl_base = re.search(r'<details class="sec" id="palavras">.*?</details>', base('m4/mapa-do-modulo-m4/index.html'), re.S).group(0)
        self.assertEqual((dl.count('<dt>'), dl.count('<dd>')), (dl_base.count('<dt>'), dl_base.count('<dd>')))
        # Achado 16: no portefólio, os cabeçalhos com scope e sem a largura fixa; todos os nomes de ficheiro em <code>, sem partir.
        port = ler('m4/portefolio-do-modulo-m4/index.html')
        self.assertIn('<table><tr><th scope="col">Nome do ficheiro</th><th scope="col">O que é</th></tr>', port)
        self.assertNotIn('width:36%', port)
        linhas = re.findall(r'<tr><td>(.*?)</td><td>', port)
        self.assertEqual(len(linhas), 18)
        self.assertTrue(all(re.fullmatch(r'<code>M4_[^<]+</code>', l) for l in linhas), linhas)
        for u in (1, 2, 3):
            for nome in (f'M4_U{u}_folha_&lt;dia-mês&gt;', f'M4_U{u}_pergunta', f'M4_U{u}_o-que-aprendi'):
                self.assertEqual(port.count(f'<td><code>{nome}</code></td>'), 1, nome)
        self.assertIn('padding:1px 4px}\ntd code{white-space:nowrap}\n', port)

    def test_achados_b_com_a_contagem_certa(self):
        self.assertEqual(sorted(x['i'] for x in C.ACHADOS_B), sorted(B))
        self.assertEqual(sorted(PROPOSTA), sorted(B))
        vistos = 0
        for x in C.ACHADOS_B:
            rel = x['ficheiro']
            pre, final = ac_aplicadas(rel, base(rel)), ler(rel)
            seqs = [s for s, _ in x['pares']]
            antes, _ = C.ocorrencias(rel, pre, seqs, [])
            depois, ficaram = C.ocorrencias(rel, final, seqs, [])
            fora = {s: n for s, (n, _) in x.get('fora', {}).items()}
            nb = {s.replace(N, ' '): n for s, n in x.get('nb', [])}
            mudam = dict(x['pares'])
            # Cada sequência da proposta está no achado: muda, fica de fora (com a razão) ou é um crédito que já tinha U+00A0.
            self.assertEqual(set(PROPOSTA[x['i']]), set(mudam) | set(fora) | set(nb), x['i'])
            for seq, prop in PROPOSTA[x['i']].items():
                total = mudam.get(seq, 0) + fora.get(seq, 0) + nb.get(seq, 0)
                with self.subTest(achado=x['i'], trecho=seq):
                    if prop is not None and total != prop:
                        # Onde se muda outro número, o achado diz o número da proposta e porquê.
                        self.assertIn(seq, x.get('mais', {}))
                        self.assertEqual(x['mais'][seq][0], prop)
                        self.assertTrue(x['mais'][seq][1])
                    else:
                        self.assertNotIn(seq, x.get('mais', {}))
            for seq, n in x['pares']:
                with self.subTest(achado=x['i'], trecho=seq):
                    # Antes, cada sequência aparece (fora do que fica de fora) exatamente as vezes do achado; depois, nenhuma se parte, e a
                    # forma da proposta final está lá.
                    self.assertEqual(len(antes[seq]), n)
                    self.assertEqual(depois[seq], [])
                    self.assertEqual(C.alvo(seq), FORMAS.get(seq, seq.replace(' ', N)))
                    self.assertGreaterEqual(final.count(C.alvo(seq)), n)
                    vistos += 1
            # Os créditos em <span class="nb">: só o hífen passa a traço de intervalo, com a junção.
            for seq, n in x.get('nb', []):
                with self.subTest(achado=x['i'], credito=seq):
                    self.assertEqual(final.count('<span class=' + ('\\"nb\\"' if rel.startswith('m4/licao-') else '"nb"') + '>'
                                                 + seq.replace('-', '–' + WJ) + '</span>'), n)
                    self.assertNotIn('<span class="nb">' + seq + '</span>', final.replace('\\"', '"'))
            # O que fica com o espaço normal está só onde não pode levar U+00A0 (o «alt», o <title>, a meta descrição, os desenhos).
            for seq, s, razao in ficaram:
                self.assertTrue(razao.startswith(('atributo alt', 'atributo aria-label', 'atributo content', '<title>', 'texto de um desenho',
                                                  'frase de um sublinhar')), (rel, seq, razao))
        self.assertEqual(vistos, sum(len(x['pares']) for x in C.ACHADOS_B))
        # A casca das lições (migalhas, «Estás em», título escondido e sigla do rodapé) fica para o molde, como no M1, no M2 e no M3:
        # nenhuma lição a muda.
        self.assertEqual(len(C.CASCA_NO_MOLDE), 15)
        for rel in C.CASCA_NO_MOLDE:
            texto = ler(rel)
            n = re.search(r'licao-m4-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                self.assertIn('/pt/2/">2.º ano</a>', texto)
                self.assertIn(f'Estás em: Lição M4-{n}', texto)
                self.assertIn(f'<h1 class="c-sr">Lição M4-{n}', texto)
                self.assertIn(f'Lição M4-{n}, ', texto)
                self.assertNotIn('M4-' + WJ, texto)
                self.assertNotIn('2.º' + N, texto)
                x = next(x for x in C.ACHADOS_B if x['ficheiro'] == rel)
                self.assertEqual(x['fora'].get('2.º ano'), (1, C.CASCA))
                self.assertEqual(x['fora'].get('M4-' + n), (2, C.CASCA))
        # As fontes do rodapé mudam, como no M1.
        self.assertIn('ortografia atualizada, caps.' + N + 'I, II e' + N + 'V (excertos; o cap.' + N + 'IV lê-se na lição',
                      ler('m4/licao-m4-f25/index.html'))
        self.assertIn('ortografia atualizada, ato' + N + 'I, cenas' + N + 'XI e' + N + 'XII; Wikipédia', ler('m4/licao-m4-f07/index.html'))
        # Nas outras páginas, as migalhas mudam onde o achado da página as inclui (como no M2 e no M3).
        for rel in ('m4/index.html', 'm4/guia-da-tarefa-m4/index.html', 'm4/mapa-do-modulo-m4/index.html',
                    'm4/portefolio-do-modulo-m4/index.html', 'm4/m4-frei-luis-quem-sabia/index.html', 'm4/m4-sermao-tribunal/index.html'):
            self.assertIn('/pt/2/">2.º' + N + 'ano</a>', ler(rel), rel)
        # Os intervalos: traço com junção; o hífen dos créditos «c. 1535-1540» e «c. 1571-1574» passa a traço (os «alt» ficam).
        self.assertIn('Garrett (1799–' + WJ + '1854)', ler('m4/recursos/tpc-entrada.js'))
        self.assertIn('1665–' + WJ + '1667', ler('m4/index.html'))
        mapa = ler('m4/mapa-do-modulo-m4/index.html')
        self.assertIn('alt="Santo António a pregar aos peixes (Garcia Fernandes, c. 1535-1540, MNAA)"', mapa)
        self.assertIn('alt="D. Sebastião (Cristóvão de Morais, c. 1571-1574, MNAA)"', mapa)
        self.assertIn('(Lisboa, 1608' + N + '– Bahia, 1697)', mapa)
        self.assertIn('(Porto, 1799' + N + '– Lisboa, 1854)', mapa)
        self.assertIn('cópia romana (século' + N + 'II' + N + 'd.C., The Met)', mapa)
        self.assertIn('alt="Cabeça de Demóstenes, mármore, cópia romana (século II d.C., The Met)"', mapa)
        # A sigla «Lição M4-Fxx» nas ligações do mapa leva a junção (os href, em minúsculas, ficam).
        self.assertEqual(len(re.findall(r'>[Ll]ição M4-' + WJ + r'F\d\d<', mapa)), 12)
        self.assertNotRegex(mapa, r'>[Ll]ição M4-F\d\d<')
        # O vídeo da F01 e da F10: o botão e o data-dur (de onde aula-clara.js refaz o botão), com o espaço que não quebra.
        for rel in ('m4/licao-m4-f01/index.html', 'm4/licao-m4-f10/index.html'):
            texto = ler(rel)
            self.assertEqual(texto.count('data-dur=\\"1' + N + 'min\\"'), 1, rel)
            self.assertEqual(texto.count('<span>(1' + N + 'min)</span>'), 1, rel)
        # Os pesos do índice ficam no parágrafo (achado 17, recusado), com o espaço que não quebra (achado 34).
        pesos = re.search(r'Pesos na avaliação:[^<]*', ler('m4/index.html')).group(0)
        self.assertEqual(re.findall(r'(\d+)' + N + '%', pesos), ['25', '10', '15'])
        self.assertNotRegex(pesos, r'\d %')

    def test_nenhum_recusado_aplicado(self):
        achados = {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertFalse(RECUSADOS & achados)
        # 5, 6, 7, 8, 9, 10, 11 e 12: as frases, as biografias, as listas e os desenhos dos cartões ficam como estavam (sem tabela).
        for rel in ('m4/licao-m4-f01/index.html', 'm4/licao-m4-f02/index.html', 'm4/licao-m4-f04/index.html', 'm4/licao-m4-f07/index.html',
                    'm4/licao-m4-f08/index.html', 'm4/licao-m4-f09/index.html', 'm4/licao-m4-f11/index.html', 'm4/licao-m4-f15/index.html',
                    'm4/licao-m4-f20/index.html', 'm4/licao-m4-f26/index.html', 'm4/licao-m4-f27/index.html', 'm4/recursos/tpc-entrada.js'):
            self.assertNotIn('apoio-tabela', ler(rel), rel)
        # 17: os pesos do índice continuam numa frase.
        self.assertRegex(ler('m4/index.html'), r'Pesos na avaliação: [^<]*25' + N + '%')

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, _, cab, _, _ in TABELAS for c in cab}
        permitidas = {p for c in cabecalhos for p in palavras(c)}
        # O que entra de propósito (proposta final da conferência): «na tabela» em vez de «na lista» (0); a legenda «Os cinco atos de
        # fala» (2). O resto do texto novo das tabelas vem da própria página (o trecho, o parágrafo do cartão e os cartões que a
        # proposta cita: o cartão 8 da F06, os cartões 15 e 16 da F25), e confere-se aí. O que sai: «lista» (0), «como» (2: os exemplos
        # passam à coluna), «que a turma pode fazer» (13: «Objeção que a turma pode fazer» passa a «Objeção»).
        entram = {0: {'tabela'}, 2: {'cinco', 'atos'}}
        saem = {0: {'lista'}, 2: {'como'}, 13: {'que', 'turma', 'pode', 'fazer'}}
        css = [t for t in TROCAS if t['novo'].startswith('<link rel="stylesheet"')]
        self.assertEqual(sorted(t['ficheiro'] for t in css), sorted(C.COM_TABELA))
        estilo = [t for t in TROCAS if 'td code{white-space:nowrap}' in t['novo']]
        self.assertEqual(len(estilo), 1)
        for t in TROCAS:
            if t in css or t in estilo:
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
                self.assertTrue(t['achado'].startswith('08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M4'))
        for c in cabecalhos:
            self.assertIsNone(PROIBIDAS.search(c), c)
        # As trocas B só mudam espaços (U+00A0), põem a junção (U+2060) e trocam o hífen dos créditos por traço de intervalo.
        for t in TROCAS:
            if '(B)' in t['achado']:
                with self.subTest(local=t['local']):
                    antigo = re.sub(r'(?<=\d{4})-(?=\d{4})', '–', t['antigo'].replace(N, ' '))
                    self.assertEqual(t['novo'].replace(N, ' ').replace(WJ, ''), antigo)
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
        # Nas páginas tocadas, o que se vê já não tem nenhuma das sequências dos achados que se parta (fora da casca das lições).
        for x in C.ACHADOS_B:
            final = ler(x['ficheiro'])
            for seq, _ in x['pares']:
                for m in re.finditer(re.escape(seq), final):
                    if C._palavra_inteira(final, m.start(), m.end(), seq):
                        self.assertIsNotNone(C.fora_de_alcance(final, m.start()), (x['ficheiro'], seq))
        # E o contrário: o detetor apanha as formas que partem, e deixa as inteiras (com os espaços que a proposta deixa).
        for partido in ('cap. I', 'caps. II e III', 'Cap. VI', 'capítulo V', 'ato II', 'Ato III', 'cena XI', 'cenas XIV e XV', 'séc. XVIII',
                        'século XVI', 'século II d.C.', 'c. 1535-1540', 'c. 1535–1540', '1799–1854', 'n.º 17591', '§ I', '2.º ano', '1.ª frase',
                        '7.º B', '90 minutos', '1 min', '20 segundos', '25 %', '150 a 200 palavras', '3 a 4 minutos', 'aulas 1 a 8', 'aula 12',
                        '13 de junho de 1654', '14 de maio', 'Mateus 5, 13', 'Mateus 5,13', '1608 – Bahia', 'M4-F11', 'a objeção do Ato 4'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for seq in [s for x in C.ACHADOS_B for s, _ in x['pares']]:
            self.assertIsNone(PARTE.search(C.alvo(seq)), seq)
        for inteiro in ('caps.' + N + 'I, II e' + N + 'V', 'cenas' + N + 'I, XIV e' + N + 'XV', '13' + N + 'de' + N + 'junho de' + N + '1654',
                        'aulas' + N + '16 a' + N + '18', 'c.' + N + '1535–' + WJ + '1540', 'Lição M4-' + WJ + 'F01'):
            self.assertIsNone(PARTE.search(inteiro), inteiro)

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 08/11/2026: por cima desta camada fica agora a decisão 152 no M5 (cuidado_m5_20261108, que não mexe em nenhuma página do
        # M4); desfaz-se primeiro, com a mesma exigência, e as contagens são as mesmas.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m4_20261108.json', '--manifesto', MANIFESTO_REL,
                            # 08/11/2026: a decisão 152 no M6 (cuidado_m6_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M6, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M5; desfaz-se primeiro, com a mesma exigência.
                            # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
                            # 11/11/2026: a decisão 152 no M7 (cuidado_m7_20261111: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M7, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo», «Olhar» e «Pensar devagar», e nas tarefas, nos aquecimentos e na grelha das suas unidades) passa a camada mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M9, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», as atividades e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            '--verificar', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-provas-oficial-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-exame-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m9-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m8-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m7-edits-20261111.json', '--desfazer-antes', 'tests/fixtures/cuidado-m6-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json', '--desfazer-antes', 'tests/fixtures/cuidado-m5-edits-20261108.json'], cwd=ROOT,
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), (412, 35))
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M4'))
        self.assertIn('cuidado_m3_20261108', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                # 08/11/2026: a página como esta camada a deixou: com a camada de cima (cuidado_m5_20261108) desfeita, com contagem
                # estrita; undo_cuidado_m4_0811 desfaz as duas, a partir da página inteira.
                atual = undo_cuidado_m5_0811(rel, ler(rel))
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_m4_0811(rel, ler(rel))
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
                # A camada de baixo (a decisão 152 no M3) continua a desfazer-se por baixo desta.
                # 08/11/2026: na página inteira, porque a cadeia de desfazer começa agora pela decisão 152 no M5.
                undo_cuidado_m3_0811(rel, ler(rel))
        # Os 38 achados confirmados estão todos na camada; nenhum recusado.
        achados = {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertEqual(achados, CONFIRMADOS)
        self.assertEqual((len(A), len(B), len(C_)), (6, 29, 3))
        self.assertEqual(sorted({x['i'] for x in C.ACHADOS_AC if x['cat'] == 'A'}), sorted(A))
        self.assertEqual(sorted({x['i'] for x in C.ACHADOS_AC if x['cat'] == 'C'}), sorted(C_))
        # A e C antes de B, em cada ficheiro.
        for rel in m['files']:
            ordem = ['B' if '(B)' in t['achado'] else 'AC' for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual(ordem, sorted(ordem, key=lambda x: x != 'AC'), rel)
        # No topo da cadeia.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 08/11/2026: por cima da decisão 152 no M4 fica a decisão 152 no M5 (cuidado_m5_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 08/11/2026: por cima da decisão 152 no M5 fica a decisão 152 no M6 (cuidado_m6_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 11/11/2026: por cima da decisão 152 no M6 fica a decisão 152 no M7 (cuidado_m7_20261111): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M7 fica a decisão 152 no M8 (cuidado_m8_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M8 fica a decisão 152 no M9 (cuidado_m9_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M9 fica a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no Exame e nas páginas transversais fica a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da ligação «Treinos» na página principal do Exame ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima das provas em cartões com os documentos oficiais ficam as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('cuidado_m9_20261112', 'cuidado-m9-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cuidado_m8_20261112', 'cuidado-m8-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('cuidado_m7_20261111', 'cuidado-m7-edits-20261111'))
        self.assertEqual(verificar_camadas.LAYERS[7], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): logo abaixo da decisão 152 no M6 fica a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192), por cima da decisão 152 no M5; as posições seguintes descem uma.
        self.assertEqual(verificar_camadas.LAYERS[8], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[9], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[10], ('cuidado_m4_20261108', 'cuidado-m4-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[11], ('cuidado_m3_20261108', 'cuidado-m3-edits-20261108'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m3_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m4_0811(path, text)'), corpo.index('_CUIDADO_M3_0811.get('))
        # 08/11/2026: e esta camada desfaz primeiro a da decisão 152 no M5, que está por cima dela.
        corpo = auditoria[auditoria.index('def undo_cuidado_m4_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m5_0811(path, text)'), corpo.index('_CUIDADO_M4_0811.get('))
        # 08/11/2026: e a decisão 152 no M5 chama primeiro a decisão 152 no M6, que está por cima.
        corpo = auditoria[auditoria.index('def undo_cuidado_m5_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m6_0811(path, text)'), corpo.index('_CUIDADO_M5_0811.get('))
        # 11/11/2026: e a decisão 152 no M6 chama primeiro a decisão 152 no M7, que está por cima.
        self.assertLess(auditoria.index('undo_cuidado_m7_1111(path, text)', auditoria.index('def undo_cuidado_m6_0811')), auditoria.index('_CUIDADO_M6_0811.get('))
        # 12/11/2026: e a decisão 152 no M7 chama primeiro a decisão 152 no M8, que está por cima.
        self.assertLess(auditoria.index('undo_cuidado_m8_1112(path, text)', auditoria.index('def undo_cuidado_m7_1111')), auditoria.index('_CUIDADO_M7_1111.get('))
        # 12/11/2026: e a decisão 152 no M8 chama primeiro a decisão 152 no M9, que está por cima.
        self.assertLess(auditoria.index('undo_cuidado_m9_1112(path, text)', auditoria.index('def undo_cuidado_m8_1112')), auditoria.index('_CUIDADO_M8_1112.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m4-edits-20261108.json'), sala.index('cuidado-m3-edits-20261108.json'))
        # 08/11/2026: e, antes desta, a decisão 152 no M5.
        self.assertLess(sala.index('cuidado-m5-edits-20261108.json'), sala.index('cuidado-m4-edits-20261108.json'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6, agora a mais recente.
        self.assertLess(sala.index('cuidado-m6-edits-20261108.json'), sala.index('cuidado-m5-edits-20261108.json'))
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7, agora a mais recente.
        self.assertLess(sala.index('cuidado-m7-edits-20261111.json'), sala.index('cuidado-m6-edits-20261108.json'))
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8, agora a mais recente.
        self.assertLess(sala.index('cuidado-m8-edits-20261112.json'), sala.index('cuidado-m7-edits-20261111.json'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9, agora a mais recente.
        self.assertLess(sala.index('cuidado-m9-edits-20261112.json'), sala.index('cuidado-m8-edits-20261112.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes da decisão 152 no M3, sem nada pelo meio.
        meu, m3 = MANIFESTO_REL, 'tests/fixtures/cuidado-m3-edits-20261108.json'
        # 08/11/2026: e logo a seguir à decisão 152 no M5, que se desfaz primeiro, logo a seguir a --verificar, sem nada pelo meio.
        m5 = 'tests/fixtures/cuidado-m5-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M5, a do M6 (cuidado_m6_20261108), agora a primeira, logo a seguir a --verificar.
        m6 = 'tests/fixtures/cuidado-m6-edits-20261108.json'
        # 11/11/2026: e, antes da decisão 152 no M6, a do M7 (cuidado_m7_20261111), agora a primeira, logo a seguir a --verificar.
        m7 = 'tests/fixtures/cuidado-m7-edits-20261111.json'
        # 12/11/2026: e, antes da decisão 152 no M7, a do M8 (cuidado_m8_20261112), agora a primeira, logo a seguir a --verificar.
        m8 = 'tests/fixtures/cuidado-m8-edits-20261112.json'
        # 12/11/2026: e, antes da decisão 152 no M8, a do M9 (cuidado_m9_20261112), agora a primeira, logo a seguir a --verificar.
        m9 = 'tests/fixtures/cuidado-m9-edits-20261112.json'
        # 12/11/2026: e, por cima da do M9, a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112).
        ex = 'tests/fixtures/cuidado-exame-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (a ligação «Treinos» na página principal do Exame).
        lt = 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (as provas em cartões com os documentos oficiais).
        po = 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (as duas tarefas do M3 mais fáceis de fazer).
        tf = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + m3 not in linha:
                    continue
                linhas += 1
                # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
                # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
                # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertIn(f'--verificar --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {meu} --desfazer-antes {m3}', linha, wf)
        # As 16 cadeias da decisão 152 no M3 e a da decisão 152 no M2 em pt-tarefas-qa.
        self.assertEqual(linhas, 17)
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        # 08/11/2026: a decisão 152 no M3 e a do M2 desfazem primeiro a do M5 e depois esta.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m3_20261108.json --manifesto {m3} --verificar --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} '
                      f'--desfazer-antes {meu}\n', tarefas)
        self.assertIn('python scripts/aplicar_trocas.py scripts/cuidado_m2_20261108.json --manifesto tests/fixtures/cuidado-m2-edits-20261108.json '
                      # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
                      # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      f'--verificar --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {meu} --desfazer-antes {m3}\n', tarefas)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        # 08/11/2026: o cartaz «Ler a cidade» desfaz primeiro a decisão 152 no M5, depois esta, a do M3 e a do M2.
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --verificar '
                      # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
                      # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      f'--desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {meu} --desfazer-antes {m3} --desfazer-antes tests/fixtures/cuidado-m2-edits-20261108.json\n', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e da decisão 152 no M1 conferem as cadeias com frases partidas em várias linhas
            # (e já exigem esta camada à cabeça); ficam de fora pela mesma razão.
            # 08/11/2026: e o teste da decisão 152 no M5, pela mesma razão.
            # 08/11/2026: e o teste da decisão 152 no M6, pela mesma razão.
            if p.name in ('test_cuidado_m4.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py', 'test_cuidado_m5.py', 'test_cuidado_m6.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + m3), plano.count(f'--desfazer-antes {meu} --desfazer-antes {m3}'))
        # 08/11/2026: nas rotas, a decisão 152 no M5 vem primeiro, logo antes desta.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f"(ROOT/'{tf}',ROOT/'{po}',ROOT/'{lt}',ROOT/'{ex}',ROOT/'{m9}',ROOT/'{m8}',ROOT/'{m7}',ROOT/'{m6}',ROOT/'{m5}',ROOT/'{meu}',ROOT/'{m3}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM4['), texto.index('((cuidadoM3['), rel)
            # 08/11/2026: e, antes desta, a decisão 152 no M5.
            self.assertLess(texto.index('((cuidadoM5['), texto.index('((cuidadoM4['), rel)
            # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (que mexe no índice do M6).
            self.assertLess(texto.index('((cuidadoM6['), texto.index('((cuidadoM5['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM4[rel]'), corpo.index('((cuidadoM3[rel]'))
        # 08/11/2026: e, antes desta, a decisão 152 no M5.
        self.assertLess(corpo.index('((cuidadoM5[rel]'), corpo.index('((cuidadoM4[rel]'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6.
        self.assertLess(corpo.index('((cuidadoM6[rel]'), corpo.index('((cuidadoM5[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M4.read_text'), gerador_148.index('CUIDADO_M3.read_text'))
        # 08/11/2026: e, antes desta, a decisão 152 no M5.
        self.assertLess(gerador_148.index('CUIDADO_M5.read_text'), gerador_148.index('CUIDADO_M4.read_text'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6.
        self.assertLess(gerador_148.index('CUIDADO_M6.read_text'), gerador_148.index('CUIDADO_M5.read_text'))
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7.
        self.assertLess(gerador_148.index('CUIDADO_M7.read_text'), gerador_148.index('CUIDADO_M6.read_text'))
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8.
        self.assertLess(gerador_148.index('CUIDADO_M8.read_text'), gerador_148.index('CUIDADO_M7.read_text'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9.
        self.assertLess(gerador_148.index('CUIDADO_M9.read_text'), gerador_148.index('CUIDADO_M8.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1, do M2 e do M3.
        # 08/11/2026: conferem-na com a decisão 152 no M5, a única por cima, desfeita antes.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m4_20261108.json --manifesto {meu} --verificar --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5}\n',
                      tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m4.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m4.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m4_20261108.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_dos_dados(self):
        # Os aquecimentos da M4-U1, da M4-U2 e da M4-U3 (discurso) mudam também nos dados, que estão nesta camada, e saem iguais do
        # gerador; as tarefas das unidades do M4 não têm gerador (não estão em docs/pedagogia/tarefas-escolha).
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/')}
        self.assertEqual(dados, {'docs/pedagogia/aquecimentos/m4-u1.json', 'docs/pedagogia/aquecimentos/m4-u2.json',
                                 'docs/pedagogia/aquecimentos/m4-u3-discurso.json'})
        for slug in ('m4-u1', 'm4-u2', 'm4-u3', 'm4-u3-discurso'):
            self.assertFalse((ROOT / f'docs/pedagogia/tarefas-escolha/{slug}.json').exists(), slug)
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, 'scripts/aquecimentos.py', '--saida', tmp], cwd=ROOT, capture_output=True, text=True,
                               encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for slug in ('m4-u1', 'm4-u2', 'm4-u3-discurso'):
                self.assertIn(f'tarefas/{slug}/aquecimento/index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())
        # Os dados e as páginas dizem o mesmo (o «ato III» da opção da M4-U2 também, antes do «ato II»).
        u2 = json.loads(ler('docs/pedagogia/aquecimentos/m4-u2.json'))
        texto = json.dumps(u2['cartoes'], ensure_ascii=False)
        self.assertEqual((texto.count('ato' + N + 'III'), texto.count('ato' + N + 'II'), texto.count('cena' + N + 'IV')), (1, 8, 8))
        self.assertNotRegex(texto, r'\b(?:ato|cena) [IVX]')

    def test_paineis_seguem_as_licoes(self):
        # Os painéis do docente das lições do M4 projetam os enunciados dos cartões: onde um mudou, o painel muda igual, na lista e no
        # seletor; e cada enunciado que seguia a lição antes desta camada continua a segui-la.
        paineis = sorted({t['ficheiro'] for t in TROCAS if '/painel-' in t['ficheiro']})
        self.assertEqual(paineis, ['m4/painel-m4-f01/index.html', 'm4/painel-m4-f09/index.html', 'm4/painel-m4-f11/index.html'])
        seguidos = 0
        for p in sorted(glob.glob(str(ROOT / 'm4/painel-m4-f*/index.html'))):
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
        # Os três que mudam: o cap. I da F01 (cartão 15), o ato II e o ato III da F09 (cartão 14) e o cartão 8 da F11.
        self.assertIn('cap.' + N + 'I', json.dumps(cartoes(ler('m4/painel-m4-f01/index.html')), ensure_ascii=False))
        f09 = next(i for i in cartoes(ler('m4/painel-m4-f09/index.html')) if i['k'] == 14)['p']
        self.assertIn('ato' + N + 'II', f09)
        self.assertIn('ato' + N + 'III', f09)


if __name__ == '__main__':
    unittest.main()
