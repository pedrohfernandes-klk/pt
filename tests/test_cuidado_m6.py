"""08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M6. Camada literal cuidado_m6_20261108
(scripts/cuidado_m6_20261108.json, gerada por scripts/cuidado_m6_20261108.py; manifesto tests/fixtures/cuidado-m6-edits-20261108.json),
a mais recente, por cima da decisão 152 no M5 (cuidado_m5_20261108).
11/11/2026 (fusão do main 4bf4a053 no pedido #191): entre as duas fica a revisão dos enunciados das tarefas (tarefas_claras_20261110,
pedido #192); esta camada foi refeita sobre ela e continua a mais recente.

Este teste confere, no modelo de tests/test_cuidado_m1.py a tests/test_cuidado_m5.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices e o gerador do desenho comum dos índices;
* cada um dos 43 achados confirmados: as 11 tabelas novas (11 achados A), com o cabeçalho (th scope=col), a primeira coluna (th
  scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato, no cartão e no
  sítio certos; os 4 casos do mesmo tipo (C), com o texto exato; os 28 achados B, com a contagem certa de cada par da proposta
  final (no contexto que a proposta dá) e a forma da proposta, sem nenhuma ocorrência que se parta fora do que fica de fora (o
  «alt», o data-titulo dos vídeos, a «frase» de um sublinhar, os «passos» de um ordenar, o que outra camada já tinha posto), e a
  casca das lições, que fica para o molde; onde o número que se muda não é o da proposta, o achado diz porquê;
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e mais nenhuma do M6;
* que nenhum dos 7 achados recusados (9, 11, 12, 13, 14, 15 e 21) entrou;
* as regras do texto: as tabelas e as listas só usam texto que já estava na página (e os cabeçalhos); nada de «professor», «jogar»,
  «jogo», «ficha», «folha», «—» ou «·» novos; nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>,
  data-titulo, chaves JSON, nem da «frase» de um sublinhar, das «palavras» de um cartão frase ou dos «passos» de um ordenar; nas
  passagens mudadas, nenhuma referência nem número que se parta;
* que as tarefas, os aquecimentos, as grelhas e a correção da M6-U1 e da M6-U2 saem iguais dos dados e dos geradores (e as dos
  outros módulos não mudam), que a lição F14 sai igual do gerador das lições, que os painéis do docente seguem os enunciados das
  lições e que as cópias do banco das provas rápidas seguem os cartões;
* 11/11/2026: as 23 reposições «(R)» depois do pedido #192, que ao reescrever os enunciados tirou espaços que não quebram às tarefas
  do M1, do M3, do M4 e do M5: cada troca só muda espaços, por cima do texto exato do #192; cada página volta a ter os U+00A0 que
  tinha antes dele; nos enunciados dessas tarefas não fica nenhuma referência do mesmo tipo que se parta; as páginas geradas saem
  iguais dos dados; e os contratos históricos continuam a ler estas páginas como eram antes do #192."""
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
from auditoria_20261028 import undo_cuidado_m6_0811, undo_cuidado_m5_0811  # noqa: E402
# 11/11/2026: por cima desta camada fica a decisão 152 no M7 (camada cuidado_m7_20261111).
from auditoria_20261028 import undo_cuidado_m7_1111  # noqa: E402
# 12/11/2026 (junção do ramo do M6 49871e08 no do M7): ficam as duas importações, a do M7 e a da leitura histórica dos enunciados.
sys.path.insert(0, str(ROOT / 'scripts'))
from tarefas_claras_historico import desfazer as desfazer_enunciados  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m6_20261108.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m6-edits-20261108.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
# 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a camada foi refeita sobre o main com a revisão dos enunciados das tarefas (#192).
BASE_COMMIT = '4bf4a0538cd5f883448d179973ef016023a58f86'
NBSP, WJ = '\xa0', '⁠'
N = NBSP
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
A = {0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 16}
B = set(range(22, 50))
C_ = {17, 18, 19, 20}
CONFIRMADOS = A | B | C_
# 11/11/2026: as reposições depois do pedido #192 (tarefas_claras_20261110), que ao reescrever os enunciados tirou espaços que não
# quebram às tarefas do M1, do M3, do M4 e do M5. Não são achados da varredura do M6: levam «(R)» e conferem-se à parte
# (test_reposicoes_depois_do_192), com exigência própria; os testes dos achados olham para as outras trocas (VARREDURA).
REPOSICAO = '11/11/2026: decisão 152 (cuidado em todas as lições), reposição depois do pedido #192 (R). '
REPOSTAS = [t for t in TROCAS if t['achado'].startswith(REPOSICAO)]
VARREDURA = [t for t in TROCAS if t not in REPOSTAS]
# Tarefa > (módulo, página gerada dos dados?, [(trecho do #192, trecho reposto, ocorrências, a forma que a decisão 152 tinha posto
# antes do #192)]). Onde o #192 trocou «cap.» por «capítulo», a forma de antes já não existe e prende-se a nova.
REPOR = {
    'm1-u2': ('M1', True, [('capítulo XII', 'capítulo' + N + 'XII', 2, 'cap.' + N + 'XII')]),
    'm3-u1': ('M3', True, [('(I, 1' + N + 'a' + N + '3)', '(I,' + N + '1' + N + 'a' + N + '3)', 1, '(I,' + N + '1' + N + 'a' + N + '3)')]),
    'm3-u2': ('M3', True, [('(I, 4' + N + 'e' + N + '5)', '(I,' + N + '4' + N + 'e' + N + '5)', 1, '(I,' + N + '4' + N + 'e' + N + '5)'),
                           ('(X, 145)', '(X,' + N + '145)', 2, '(X,' + N + '145)'),
                           ('curioso» (VIII, 96)', 'curioso» (VIII,' + N + '96)', 1, 'curioso» (VIII,' + N + '96)'),
                           ('VIII, 96' + N + 'a' + N + '99', 'VIII,' + N + '96' + N + 'a' + N + '99', 1, 'VIII,' + N + '96' + N + 'a' + N + '99'),
                           ('VIII, 98 ou 99', 'VIII,' + N + '98 ou 99', 1, 'VIII,' + N + '98 ou 99')]),
    'm4-u1': ('M4', False, [('<strong>3 a 4 minutos</strong>', '<strong>3' + N + 'a' + N + '4' + N + 'minutos</strong>', 1,
                             '3' + N + 'a' + N + '4' + N + 'minutos')]),
    'm4-u2': ('M4', False, [('<strong>180 a 240 palavras</strong>', '<strong>180' + N + 'a' + N + '240' + N + 'palavras</strong>', 1,
                             '180' + N + 'a' + N + '240' + N + 'palavras')]),
    'm4-u3-discurso': ('M4', False, [('<strong>2 minutos</strong>', '<strong>2' + N + 'minutos</strong>', 1, '2' + N + 'minutos')]),
    'm5-u1': ('M5', True, [('do capítulo IV em que', 'do capítulo' + N + 'IV em que', 1, 'cap.' + N + 'IV')]),
    'm5-u2': ('M5', True, [('do capítulo I e outra nova', 'do capítulo' + N + 'I e outra nova', 1, 'cap.' + N + 'I'),
                           ('No capítulo VI,', 'No capítulo' + N + 'VI,', 1, 'cap.' + N + 'VI')]),
}
# O que se parte num enunciado (o <header> da tarefa), pelas regras da decisão 152 em cada módulo: em todos, «cap.», «capítulo»
# e o numeral, canto e estância, número e «min», «minutos» ou «%», ordinal e nome; no M3 e no M4, também os intervalos «N a N» e
# «N e N» e número e «palavras» (o M1 só prende o número a «palavras»; o M5 deixa os intervalos de palavras como estavam).
PARTE_ENUNCIADO = (r'(?<![\w.])[Cc]aps?\. (?=[\dIVXLC])|\b[Cc]apítulos? (?=[\dIVXLC]+\b)|\b[IVXLC]+, (?=\d)'
                   r'|\b\d+ (?=(?:min|minutos|%)(?!\w))|\d\.[ºª] (?=\w)')
PARTE_REPOR = {'M1': re.compile(PARTE_ENUNCIADO + r'|\b\d+ (?=palavras(?!\w))'),
               'M3': re.compile(PARTE_ENUNCIADO + r'|\b\d+ (?=palavras(?!\w))|\b\d+ (?=[ae] \d)|\b\d+\xa0[ae] (?=\d)'),
               'M4': re.compile(PARTE_ENUNCIADO + r'|\b\d+ (?=palavras(?!\w))|\b\d+ (?=[ae] \d)|\b\d+\xa0[ae] (?=\d)'),
               'M5': re.compile(PARTE_ENUNCIADO)}
# O achado 29 (F09) é só a casca da lição, que fica para o molde: não tem troca.
SO_CASCA = {29}
RECUSADOS = {9, 11, 12, 13, 14, 15, 21}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)
TERMOS = 'width:30%'

# (página, índice da tabela na página, cabeçalho, linhas, larguras): o texto de cada célula, como se lê.
TABELAS = [
    # achado 3, F02, cartão 18 («Em paralelo»)
    ('m6/licao-m6-f02/index.html', 0, ['Aspeto', '«Ideal»', '«Na mão de Deus»'],
     [['O Ideal', 'visão sem nome, miragem, «Nuvem, sonho impalpavel»', '«forma transitoria e imperfeita» que o sujeito depõe'],
      ['O sujeito', 'inquieto: «A mim mesmo pergunto, e não atino»', 'em repouso: «Descançou a final meu coração»'],
      ['Recursos', 'anáfora e enumeração negativa: não é Vénus, Circe, Amazona', 'comparação da criança ao colo e apóstrofe ao coração']],
     None),
    # achado 6, F02, cartão 20 («Recorda»): a primeira coluna com 30 %
    ('m6/licao-m6-f02/index.html', 1, ['Recurso', 'O que é', 'Exemplo'],
     [['Apóstrofe', 'chamar alguém ou alguma coisa', "«Abri-vos, portas d'ouro»"],
      ['Metáfora', 'dizer uma coisa por outra', '«Paladino do amor»'],
      ['Personificação', 'dar gesto ou voz de pessoa a uma coisa ou a uma ideia', 'as portas, a que o cavaleiro fala como se fossem pessoas'],
      ['Comparação', 'aproximar duas coisas com «como»', '«Como criança, em lobrega jornada»'],
      ['Anáfora', 'repetir a mesma palavra no princípio de versos ou frases', '«Por desertos, por sóes, por noite escura»']],
     [TERMOS, None, None]),
    # achado 4, F04, cartão 2 («Em paralelo»)
    ('m6/licao-m6-f04/index.html', 0, ['Aspeto', 'Coordenação', 'Subordinação'],
     [['O que faz', 'liga orações sem dependência sintática entre si', 'uma oração depende de outra, a subordinante'],
      ['Conectores', 'e, mas, ou, pois (confirma a relação na frase)', 'que, quando, se, porque, como (decide a construção)'],
      ['Exemplo', '«Abrem-se as portas de ouro» e «Mas dentro encontro só»', '«Sonho» e «que sou um cavaleiro andante», substantiva completiva']],
     None),
    # achado 5, F04, cartão 4 («Para entender»)
    ('m6/licao-m6-f04/index.html', 1, ['Relação', 'Exemplo', 'O que observar'],
     [['Completiva', '«Sonho que sou um cavaleiro»', 'a oração completa o verbo; «Sonho isso» ajuda a verificar.'],
      ['Relativa com antecedente', '«os filhos que depois naufragam»', '«que» retoma «filhos» e é sujeito de «naufragam».'],
      ['Adverbial', '«tal… que»', 'pode apresentar uma consequência; confirma-se na frase, não na palavra «que» isolada.']],
     None),
    # achado 16, F05, cartão 2 («Em paralelo»)
    ('m6/licao-m6-f05/index.html', 0, ['Étimo', 'Via popular', 'Via erudita'],
     [['plenu-', '«cheio»', '«pleno»'], ['clave-', '«chave»', '«clave»'], ['macula-', '«mancha» ou «malha»', '«mácula»']], None),
    # achado 0, F06, cartão 20 («Em paralelo»)
    ('m6/licao-m6-f06/index.html', 0, ['Elemento', 'O que vê', 'O que evoca'],
     [['Barcos', 'os botes atracados e os escaleres de um couraçado', '«soberbas naus que eu não verei jámais!»'],
      ['Gente', 'calafates «enfarruscados, seccos»', '«Mouros, baixeis, heroes», Camões a nado'],
      ['Tempo', 'o fim da tarde que «inspira» e «incommoda»', 'o passado das «chronicas navaes»']], None),
    # achado 7, F06, cartão 22 («Recorda»): a primeira coluna com 30 %
    ('m6/licao-m6-f06/index.html', 1, ['Conceito', 'O que é'],
     [['Deambulação', 'andar pela cidade sem destino, a ver.'],
      ['Perceção sensorial', 'o que chega pelos sentidos (ver, ouvir, cheirar, sentir na pele).'],
      ['Transfiguração do real', 'o que se vê torna-se outra coisa pela imaginação.'],
      ['Tipos sociais', 'figuras que valem por um grupo inteiro, como um ofício.'],
      ['Imaginário épico', 'as imagens que a epopeia deixou (naus, heróis, mares).']], [TERMOS, None]),
    # achado 1, F07, cartão 28 («Em paralelo»)
    ('m6/licao-m6-f07/index.html', 0, ['Elemento', 'A reportagem', 'O sonho'],
     [['Programa', '«o real e a analyse», um livro feito do observado', '«a chimera azul de transmigrar», mudar de vida'],
      ['Gente', 'o forjador ao torno, o ratoneiro imberbe, o cauteleiro rouco', '«castissimas esposas», filhos, «mansões de vidro transparente»'],
      ['Lugar', '«Sem arvores, no valle escuro das muralhas»', '«todos os continentes» e «as vastidões aquaticas»']], None),
    # achado 8, F07, cartão 30 («Recorda»): o exemplo da antítese é o do «O essencial» (cartão 1)
    ('m6/licao-m6-f07/index.html', 1, ['Recurso', 'O que é', 'Exemplo'],
     [['Antítese', 'duas ideias opostas lado a lado', '«Inflamma-se um palacio em face de um casebre» (v.' + N + '28)'],
      ['Sinestesia', 'mistura de sentidos na mesma expressão', '«um silêncio frio»'],
      ['Hipálage', 'dar a uma coisa a qualidade que pertence a uma pessoa', '«a cadeira cansada»']], None),
    # achado 2, F09, cartão 2 («Em paralelo»)
    ('m6/licao-m6-f09/index.html', 0, ['Aspeto', 'Antero', 'Cesário'],
     [['Temas', 'angústia existencial, o Ideal, a morte, Deus', 'a cidade, os tipos sociais, o trabalho'],
      ['Forma', 'o soneto, com chave de ouro', 'quadras de alexandrinos e decassílabos'],
      ['Real', 'pensado: «O palacio encantado da Ventura»', 'observado e transfigurado: «a pão no forno»']], None),
    # achado 10, «Frases da rua» (gram-oracoes-rua), passo 0: os três testes, num div.nota (como em gram-modalidade, no M3)
    ('m6/gram-oracoes-rua/index.html', 0, ['Teste', 'Condição', 'A oração é'],
     [['teste do «isso»', 'se a oração se troca por «isso»', 'substantiva'],
      ['teste do «o qual»', 'se «que» se troca por «o qual», «os quais»', 'relativa'],
      ['teste da pergunta', 'se responde a «quando?», «porquê?» ou «com que resultado?»', 'adverbial']], None),
]
# Onde está cada tabela nas lições: (página, tabela) > (índice do cartão, rótulo do cartão, o que fica por cima, o que fica a seguir).
LUGARES = {
    ('m6/licao-m6-f02/index.html', 0): (18, 'Em paralelo', '<table class="apoio-tabela" role="table">',
                                        '</table><p class="liga">Dois desfechos para a busca de «O Palacio da Ventura»'),
    ('m6/licao-m6-f02/index.html', 1): (20, 'Para entender', '<h3>Recorda</h3><p>Os exemplos vêm de «O Palácio da Ventura»; o da comparação, '
                                        'de «Na mão de Deus».</p><table class="apoio-tabela" role="table">', '</table></div>'),
    ('m6/licao-m6-f04/index.html', 0): (2, 'Em paralelo', '<table class="apoio-tabela" role="table">',
                                        '</table><p class="liga">Primeiro põe-se o verso em ordem direta'),
    ('m6/licao-m6-f04/index.html', 1): (4, 'Para entender', '<div class="painel"><b>Três relações a observar</b><table class="apoio-tabela" role="table">',
                                        '</table><details><summary>Outras construções e o «pois» no poema</summary>'),
    ('m6/licao-m6-f05/index.html', 0): (2, 'Em paralelo', '<p><b>Via popular</b>: evolução fonética lenta. <b>Via erudita</b>: tomada mais '
                                        'tarde, próxima do latim.</p><table class="apoio-tabela" role="table">',
                                        '</table><p class="liga">Do mesmo étimo latino nascem as duas'),
    ('m6/licao-m6-f06/index.html', 0): (20, 'Em paralelo', '<table class="apoio-tabela" role="table">',
                                        '</table><p class="liga">Os botes do cais acordam as naus'),
    ('m6/licao-m6-f06/index.html', 1): (22, 'Para entender', '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela" role="table">',
                                        '</table></div><details><summary>Uma palavra ajuda a ver uma vida</summary>'),
    ('m6/licao-m6-f07/index.html', 0): (28, 'Em paralelo', '<table class="apoio-tabela" role="table">',
                                        '</table><p class="liga">O «Mas» de «Horas Mortas» corta o sonho'),
    ('m6/licao-m6-f07/index.html', 1): (30, 'Para entender', '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela" role="table">',
                                        '</table></div><details><summary>Porque é «honesto» uma pista de hipálage?</summary>'),
    ('m6/licao-m6-f09/index.html', 0): (2, 'Em paralelo', '<table class="apoio-tabela" role="table">',
                                        '</table><p class="liga">Um procura fora do mundo, o outro encontra no mundo'),
}
# As lições onde um cartão «Em paralelo» passou a tabela (achados 0 a 4 e 16) e a que fica (F11, como a varredura propôs).
PARALELOS = {'m6/licao-m6-f02/index.html': 18, 'm6/licao-m6-f04/index.html': 2, 'm6/licao-m6-f05/index.html': 2,
             'm6/licao-m6-f06/index.html': 20, 'm6/licao-m6-f07/index.html': 28, 'm6/licao-m6-f09/index.html': 2}

# O que a proposta final conta, par a par (no contexto da proposta e com o número que ela dá ou que a conferência confirmou; nas
# páginas geradas, a forma concreta da página). A casca das lições conta-se à parte (casca).
V = lambda *ns: {f'(v. {n})': k for n, k in ns}
PROPOSTA = {
    22: {**V((1, 3), (7, 2), (9, 3), (10, 1), (11, 1), (12, 1), (14, 3)), 'v. 6 corrigido': 1, '(c. 1887)': 1,
         'Quental (fotografia, c. 1887,': 1, '(1842 a 1891)': 1, '(1842–1891)': 1, '4 + 4 + 3 + 3': 2},
    23: {'(v. 1 a 4)': 1, '(v. 1 e 2)': 1, '(v. 9 e 10)': 2, **V((4, 1), (5, 1), (6, 1), (7, 1), (8, 1)), 'v. 14 corrigido': 1,
         'de Antero, com imagens (2 min)': 2},
    24: {'>M6-F07</a>': 1},
    25: {'século XIX': 5},
    26: {'(v. 16 e 17)': 1, **V((3, 1), (5, 2), (7, 2), (8, 1), (9, 1), (10, 2), (16, 1), (17, 1), (20, 1), (23, 1), (24, 1), (29, 1),
                               (32, 1), (44, 2)),
         'os versos 27 e 28': 1, 'no verso 28': 1, 'parte I': 3, 'S. Petersburgo': 3, 'Tiago Barbosa (3 min)': 2},
    27: {**V((1, 1), (7, 1), (10, 1), (15, 1), (23, 2), (28, 1), (29, 1), (51, 1)), 'verso 36': 1, 'verso 66': 1, 'verso 74': 1,
         'parte II': 1, 'parte IV': 1},
    28: {'Bárcia, c. 1900)': 2, '(parte I)': 2, 'Villas Boas (4 min)': 2, '100 a 130 palavras': 2, '30 a 60 segundos': 1,
         'peça 3 min': 1, 'curta 2 a 3 min': 1, '45 minutos': 2, 'grelha /20': 1},
    29: {},
    30: {'31 anos': 9, '200 exemplares': 5, 'a 25 de fevereiro.': 1, 'Morre a 19 de julho,': 1, '19 de julho de 1886': 2,
         '19 de julho de **1886**': 1, '25 de fevereiro de 1855': 2, '(Lisboa, 1855 a 1886)': 1, 'Ensina RTP (1 min)': 2,
         '(54 segundos)': 1},
    31: {'conferência de 27 de maio de 1871': 1},
    32: {'aula de tarefa de 90 minutos': 1, 'Unidade 1, 90 minutos': 1, 'Unidade 2, 90 minutos': 1, 'tarefa 90 min</small>': 2,
         'cerca de 22 min': 2, '30 %': 5, '10 %': 1, 'grelha /20': 2, 'Grelha /20': 2, 'Português, 2.º ano, percurso do módulo': 1,
         # O banco das provas rápidas: as mesmas trocas que nas lições (a conferência contou «v. N» ×20, com «v. 1 a 4» e «v. 13 e
         # 14», «século XIX» ×3, «31 anos» ×4, «100 a 130 palavras» e «45 minutos»).
         '(v. 1 a 4)': 1, '(v. 13 e 14)': 1, **V((1, 4), (5, 1), (7, 4), (8, 1), (9, 1), (10, 3), (14, 4)), 'verso 36': 1,
         '4 + 4 + 3 + 3': 1, 'S. Petersburgo': 1, 'parte I': 1, 'século XIX': 3, '31 anos': 4, '200 exemplares': 4,
         '25 de fevereiro de 1855': 1, '19 de julho de 1886': 1, '45 minutos': 1, 'de 100 a 130 palavras': 1},
    33: {'aula de tarefa de 90 minutos': 1, '(10 minutos)': 1, 'Seguem-se 5 minutos': 1, '30 %': 5, '10 %': 1, 'grelha /20': 7,
         '<b>Aquecer, 10 min</b>': 1, '<b>Ler o enunciado, 5 min</b>': 1, '<b>Produzir, 60 min</b>': 1,
         '<b>Rever e entregar, 15 min</b>': 1, 'Guia da tarefa, 2.º ano': 1},
    34: {'versos 1 a 3': 1, '1842–1891': 1, '1855–1886': 1, 'Quental (fotografia, c. 1887,': 2, 'Bárcia, c. 1900)': 1, 'século XX': 1,
         '30 %': 5, '10 %': 1, '90 minutos': 3, 'grelha /20': 3, 'Grelha /20': 2, '">Lição M6-F': 7, '">lição M6-F': 1,
         'Português · 2.º ano · Mapa do módulo': 1},
    35: {'aula de tarefa de 90 minutos': 1, '(40 %)': 1, 'grelha /20': 1, 'Grelha /20.': 2, 'Português · 2.º ano · Módulo 6': 1},
    36: {'n.º 8698': 7, 'fecham a parte I.': 1, 'da parte III.': 1, 'S. Petersburgo': 1, 'cerca de 22 min': 1},
    37: {'n.º 20142': 6, 'prefácio, parte I.': 1, 'cerca de 22 min': 1},
    38: {'(1842–1891)': 1, '(v. 7)': 1, '(v. 14)': 1, 'até 15 palavras': 1, 'n.º 20142': 2},
    39: {'n.º 20142': 3, 'até 25 palavras': 1, 'menos de 25 palavras': 1},
    40: {'n.º 8698': 3, 'num verso de 16 palavras': 1},
    41: {'n.º 8698': 3, 'os momentos da parte IV.': 1},
    42: {'n.º 8698': 3, 'n.º 20142': 3},
    43: {'9 de abril de 2021': 3, '3 de julho de 2021': 3},
    44: {'Antes de escrever · 10 min ·': 1, 'Unidade 1 · 90 min': 1, '10 minutos de cartões': 1, '5 minutos para': 1, '60 minutos de': 1,
         '15 minutos de': 1, 'Total: 90 minutos': 1, '200 a 240 palavras': 2, '90 a 130 no tema': 1, 'Grelha /20: como': 1},
    45: {'Antes de escrever · 10 min ·': 1, 'Unidade 2 · 90 min': 1, '10 minutos de cartões': 1, '5 minutos para': 1, '60 minutos de': 1,
         '15 minutos de': 1, 'Total: 90 minutos': 1, '200 a 240 palavras': 2, 'grafias do século XIX': 1, 'Na parte II,': 2,
         '200 exemplares': 1, 'aos 31 anos': 1, 'Grelha /20: como': 1},
    46: {'À mão, 200 a 240 palavras.': 1, 'contas as palavras: 200 a 240': 1, '4 + 4 + 3 + 3 (lição F01)': 1},
    47: {'À mão, 200 a 240 palavras.': 1, 'contas as palavras: 200 a 240': 1},
    48: {'20 valores em cinco critérios': 1, 'entre 200 e 240 palavras': 1, 'das 200 a 240 palavras': 1, '(c. 1577)': 1},
    49: {'20 valores em cinco critérios': 1, 'entre 200 e 240 palavras': 1, 'das 200 a 240 palavras': 1},
}
# As trocas que não estão na proposta, com a razão: a meta descrição das tarefas muda com «nao_partir» (como do M1 ao M5).
EXTRAS = {44: {'durante 90 minutos, com entrega'}, 45: {'durante 90 minutos, com entrega'}}
# As trocas B que não são só de espaços (com a proposta): os intervalos de versos passam à forma «vv. N–N» da M7-F10.
TEXTO_MUDA = {('m6/licao-m6-f02/index.html', '(v. 1 a 4)'), ('m6/licao-m6-f02/index.html', '(v. 1 e 2)'),
              ('m6/licao-m6-f02/index.html', '(v. 9 e 10)'), ('m6/licao-m6-f06/index.html', '(v. 16 e 17)'),
              ('m6/index.html', '(v. 1 a 4)'), ('m6/index.html', '(v. 13 e 14)')}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a proposta pede U+00A0, traço de intervalo sem U+2060
# ou o hífen da sigla «M6-Fxx» sem a junção. As formas do M6: «v.», «vv.», «verso(s)», «c.», «n.º», «S.», «século», «parte»,
# ordinal e nome, número e unidade (min, minutos, segundos, %, palavras, anos, exemplares, valores), «grelha /20», as datas (todos
# os espaços, como na proposta do M6), os intervalos «N a N» e «N e N» de números (e a soma «4 + 4 + 3 + 3»), os intervalos com
# traço e a sigla.
MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'
PARTE = re.compile(
    r'(?<![\w.])(?:vv?|c|S)\. (?=[\dIVXLCP])'
    r'|n\.º (?=\d)'
    r'|\b(?:verso|séculos?|partes?) (?=[\dIVXLC]+\b)'
    r'|\d\.[ºª] (?=\w)'
    r'|\b\d+ (?=(?:min|minutos|segundos|%|palavras|anos|exemplares|valores)(?!\w))'
    r'|[Gg]relha (?=/20)'
    r'|\b\d{1,2} de (?=(?i:' + MESES + r'))|\b\d{1,2}\xa0de (?=(?i:' + MESES + r'))'
    r'|(?i:' + MESES + r') (?=de \d{4}\b)|(?i:' + MESES + r')\xa0de (?=\d{4}\b)'
    r'|\b\d+ (?=[ae] \d)|\b\d+\xa0[ae] (?=\d)|\b\d (?=\+ \d)|\+ (?=\d)'
    r'|\d–(?!⁠)\d|\bM6-(?!⁠)F\d')


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
    spec = importlib.util.spec_from_file_location('cuidado_m6_20261108', ROOT / 'scripts/cuidado_m6_20261108.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


C = gerador()


def cartoes(texto):
    """Os cartões de uma lição."""
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0]


def banco(texto):
    """As cópias dos cartões no banco das provas rápidas do índice (var U)."""
    return [x for u in json.JSONDecoder().raw_decode(texto.split('var U=', 1)[1])[0] for x in u.get('pool', [])]


def visivel(fragmento):
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragmento.replace('\\"', '"').replace('<\\/', '</').replace('\\n', '\n')))


def palavras(texto):
    return set(re.findall(r'[\wÀ-ÿ]+', visivel(texto).lower()))


def base(rel):
    """A página sem esta camada (desfeita pelo manifesto, com contagem estrita)."""
    return undo_cuidado_m6_0811(rel, ler(rel))


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


def em_alcance(texto, s, antigo, novo):
    """As ocorrências de um par que contam: com a palavra inteira (salvo os pares que acabam na sigla) e nenhuma edição fora de
    alcance."""
    if not C._palavra_inteira(texto, s, s + len(antigo), antigo):
        return False
    return all(C.fora_de_alcance(texto, s + p) is None for p, _ in C.edicoes(antigo, C.j(novo)))


class CuidadoM6(unittest.TestCase):
    def test_onze_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 11)
        for rel, k, cabecalho, linhas, larguras in TABELAS:
            t = Tabela(tabelas_da_pagina(ler(rel))[k])
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(t.tabela.get('class'), 'apoio-tabela')
                self.assertEqual(t.tabela.get('role'), 'table')
                # Sem <caption>: o título da caixa ou do cartão já a nomeia.
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
                # Só as duas de termos têm larguras: a primeira coluna (o recurso, o conceito) fica com 30 %.
                self.assertEqual([c['attrs'].get('style') for c in topo['celulas']], larguras or [None] * len(cabecalho))
        # Nenhuma página do M6 (nem as suas tarefas, aquecimentos e grelhas) tem mais tabelas de apoio do que estas.
        contagem = {}
        for rel, *_ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        for p in sorted(glob.glob(str(ROOT / 'm6/**/index.html'), recursive=True)) + sorted(glob.glob(str(ROOT / 'tarefas/m6-*/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            with self.subTest(pagina=rel):
                self.assertEqual(len(tabelas_da_pagina(ler(rel))), contagem.get(rel, 0))

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
        # Os cartões «Em paralelo» que passaram a tabela já não têm o div.paralelo nem os desenhos dos lados; o liga e o que vem a
        # seguir ficam (o vídeo da F06, o segundo liga da F07, que test_m6_observar_imaginar procura, e o painel da F09).
        for rel, k in PARALELOS.items():
            html_ = cartoes(ler(rel))[k]['html']
            with self.subTest(paralelo=rel):
                self.assertEqual(cartoes(ler(rel))[k]['rot'], 'Em paralelo')
                self.assertNotIn('class="paralelo"', html_)
                self.assertNotIn('<svg', html_)
                self.assertTrue(html_.startswith(('<table class="apoio-tabela"', '<p><b>Via popular</b>')), html_[:60])
        self.assertIn('<div class="yt" data-yt="amC-PySWaKs"', cartoes(ler('m6/licao-m6-f06/index.html'))[20]['html'])
        self.assertIn('designa o ponto de partida na cidade observada', cartoes(ler('m6/licao-m6-f07/index.html'))[28]['html'])
        self.assertIn('<div class="painel"><h3>Do indício ao efeito</h3>', cartoes(ler('m6/licao-m6-f09/index.html'))[2]['html'])
        # O «Em paralelo» da F11 (Facto e Interpretação) fica, como a varredura propôs.
        self.assertEqual(sum('class="paralelo"' in c.get('html', '') for c in cartoes(ler('m6/licao-m6-f11/index.html'))), 1)
        # «Frases da rua»: a tabela dos três testes, num div.nota, no passo 0, logo a seguir aos três versos.
        rua = ler('m6/gram-oracoes-rua/index.html')
        self.assertIn('Os filhos que depois naufragam nas tormentas»</p><div class=\\"nota\\"><table class=\\"apoio-tabela\\" role=\\"table\\">', rua)
        self.assertIn('</table></div>","links":[["Cesário Verde, _O Livro de Cesário Verde_ (Project Gutenberg n.º' + N + '8698)', rua)
        self.assertNotIn('<p class=\\"nota\\"><b>teste do', rua)

    def test_folha_das_tabelas_antes_da_aparencia(self):
        com_tabela = sorted({r for r, *_ in TABELAS})
        self.assertEqual(com_tabela, sorted(C.COM_TABELA))
        for rel in com_tabela:
            cabeca = ler(rel).split('</head>')[0]
            with self.subTest(pagina=rel):
                self.assertEqual(cabeca.count(FOLHA), 1)
                self.assertLess(cabeca.index(FOLHA), cabeca.index('assets/appearance.css'))
        for p in sorted(glob.glob(str(ROOT / 'm6/**/index.html'), recursive=True)) + sorted(glob.glob(str(ROOT / 'tarefas/m6-*/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            if rel not in com_tabela:
                self.assertNotIn('apoios-tabelas.css', ler(rel), rel)
        # A folha é a do M1 e não muda: as regras das lições (.jogo .ler) e as de fora das lições já lá estão.
        css = ler('assets/pt-lessons/apoios-tabelas.css')
        self.assertIn('.jogo .ler .apoio-tabela td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertIn('.apoio-tabela:not(.jogo .ler .apoio-tabela) td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertNotIn('assets/pt-lessons/apoios-tabelas.css', {t['ficheiro'] for t in TROCAS})

    def test_casos_do_mesmo_tipo(self):
        # Achado 17: na F08, as cinco regras de produção numa lista; a frase da encomenda fica.
        self.assertIn('<div class="caixa"><h3>Regras de produção</h3><ul><li>Pedir autorização a quem aparece reconhecível.</li><li>Não '
                      'fotografar pessoas em situação vulnerável sem consentimento (sem-abrigo, crianças).</li><li>Nada de fotografar às '
                      'escondidas.</li><li>Sair em grupo e dentro do horário combinado.</li><li>Música e sons próprios ou livres de '
                      'direitos.</li></ul><p>Cada curso tem a sua encomenda: procura a do teu.</p></div>',
                      cartoes(ler('m6/licao-m6-f08/index.html'))[2]['html'])
        # Achado 18: no portefólio, a tabela com cabeçalho (thead, th scope=col, sem a largura de 36 %), os role, o rótulo da coluna
        # em cada célula e todos os nomes em <code>, sem U+2011 nem U+2060 (o aluno copia-os); o estilo empilha-a no telemóvel.
        port = ler('m6/portefolio-do-modulo-m6/index.html')
        self.assertIn('<table role="table"><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">Nome do ficheiro</th>'
                      '<th scope="col" role="columnheader">O que é</th></tr></thead><tbody role="rowgroup">', port)
        self.assertNotIn('width:36%', port)
        linhas = re.findall(r'<tr role="row"><td role="cell" data-label="Nome do ficheiro">(.*?)</td><td role="cell" data-label="O que é">', port)
        self.assertEqual(len(linhas), 15)
        self.assertTrue(all(re.fullmatch(r'<code>M6_[^<\u2011\u2060\xa0]*</code>', l) for l in linhas), linhas)
        for nome in ('M6_U1_registo_&lt;dia-mês&gt;', 'M6_U1_pergunta', 'M6_U1_o-que-aprendi', 'M6_U2_registo_&lt;dia-mês&gt;',
                     'M6_U2_pergunta', 'M6_U2_o-que-aprendi', 'M6_capa', 'M6_cartao-do-percurso', 'M6_U1_Tarefa', 'M6_U2_Tarefa'):
            self.assertEqual(port.count(f'<td role="cell" data-label="Nome do ficheiro"><code>{nome}</code></td>'), 1, nome)
        self.assertEqual(port.count('<tr><td>'), 0)
        self.assertEqual(port.count('Grelha' + N + '/20.</td>'), 2)
        self.assertIn('code{white-space:nowrap}\n@media(max-width:620px){table,tbody,tr,td{display:block;width:auto}thead{position:absolute;'
                      'width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}tr{border-top:2px solid var(--tinta)}td[data-label]::before'
                      '{content:attr(data-label) ": ";font-weight:700}}\n', port)
        # Achados 19 e 20: o descritor do nível máximo do critério 4 em listas, pelo gerador das grelhas («max_em_listas», como no
        # M1 e no M5); a versão de correção fica com o texto corrido.
        grelhas = json.loads(ler('docs/pedagogia/grelhas-tarefas-20261027.json'))['tarefas']
        for slug in ('m6-u1', 'm6-u2'):
            self.assertEqual([c.get('max_em_listas') for c in grelhas[slug]['criterios']], [None, None, None, True, None], slug)
        g1, g2 = ler('tarefas/m6-u1/grelha/index.html'), ler('tarefas/m6-u2/grelha/index.html')
        # Na forma do gerador, como no M1 e no M5 (o parágrafo de abertura acaba no espaço que vinha antes de «Tema A»).
        for g in (g1, g2):
            self.assertIn('<p>Cumpres os cinco elementos do teu tema (um ponto cada) e explicas o que o tema pede (mais um ponto). </p>'
                          '<p><b>Tema A</b>:</p><ul>', g)
        self.assertIn('<p><b>Tema A</b>:</p><ul><li>um ideal de hoje num lugar concreto;</li><li>a procura, a chegada e a porta aberta;</li>'
                      '<li>uma última frase que vira o que o texto prometia;</li><li>uma anáfora ou uma antítese tua;</li><li>uma diferença '
                      'entre o teu ideal e o do cavaleiro.</li></ul><p>Explicação: o verso de Antero que imitaste, citado e explicado.</p>'
                      '<p><b>Tema B</b>:</p><ul><li>três planos;</li><li>um verso exato em cada um;</li><li>dois factos do dossiê (contam '
                      'como dois);</li><li>o que o vídeo não pode dar como facto.</li></ul><p>Explicação: se o último plano ilustra, contraria '
                      'ou acrescenta algo ao verso, e porquê.</p>', g1)
        self.assertIn('<p><b>Tema A</b>:</p><ul><li>um lugar e uma hora, percorridos a pé;</li><li>duas sensações de sentidos diferentes;</li>'
                      '<li>um tipo social de hoje com um gesto;</li><li>uma transfiguração tua;</li><li>uma diferença entre a tua cidade e a '
                      'dele.</li></ul><p>Explicação: o verso de Cesário que imitaste, citado e explicado.</p><p><b>Tema B</b>:</p><ul><li>duas '
                      'fotografias, cada uma com lugar e hora;</li><li>em cada uma, a legenda com um verso exato e a parte;</li><li>dois '
                      'factos do dossiê (contam como dois);</li><li>o que não podes fotografar, e porquê.</li></ul><p>Explicação: a relação, '
                      'não literal, entre uma fotografia e o seu verso.</p>', g2)
        for slug in ('m6-u1', 'm6-u2'):
            correcao = re.sub(r'<style>.*?</style>', '', ler(f'tarefas/{slug}/correcao/index.html'), flags=re.S)
            self.assertNotIn('<ul>', correcao.split('Cumpres os cinco')[1].split('</small>')[0])

    def test_achados_b_com_a_contagem_certa(self):
        self.assertEqual(sorted(x['i'] for x in C.ACHADOS_B), sorted(B))
        self.assertEqual(sorted(PROPOSTA), sorted(B))
        vistos = 0
        for x in C.ACHADOS_B:
            rel, i = x['ficheiro'], x['i']
            prop = PROPOSTA[i]
            mudam = {}
            for p in x['pares']:
                mudam[p[0]] = mudam.get(p[0], 0) + p[2]
            fora = {s: n for s, (n, _) in x.get('fora', {}).items()}
            literais = {a: n for a, _, _, n in x.get('literais', [])}
            # O que muda sem estar na proposta (com «mais», número 0 e a razão) fica fora da comparação.
            alem = {s for s, (n, _) in x.get('mais', {}).items() if n == 0}
            # Cada par da proposta está no achado: muda, fica de fora (com a razão) ou é uma troca literal com a razão; as literais
            # que não estão na proposta são as de EXTRAS.
            self.assertEqual(set(prop), (set(mudam) - alem) | set(fora) | (set(literais) - EXTRAS.get(i, set())), i)
            self.assertEqual(set(literais) - set(prop), EXTRAS.get(i, set()), i)
            for seq, n in prop.items():
                total = mudam.get(seq, 0) + fora.get(seq, 0) + literais.get(seq, 0)
                with self.subTest(achado=i, trecho=seq):
                    self.assertEqual(total, n)
            # O que muda sem estar na proposta diz porquê (o «90 a 130 no tema» da M6-U2, como na M6-U1).
            for seq, (n, razao) in x.get('mais', {}).items():
                self.assertIn(seq, mudam)
                self.assertTrue(razao)
            for seq, (_, razao) in x.get('fora', {}).items():
                self.assertTrue(razao, seq)
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
                    vistos += 1
            # O que fica de fora fica como estava; o que outro achado (A ou C) já refez está lá com o espaço que não quebra.
            for seq, (n, razao) in x.get('fora', {}).items():
                with self.subTest(achado=i, fora=seq):
                    if razao.startswith('o achado'):
                        self.assertGreaterEqual(final.count(seq.replace(' ', N)), n)
                    else:
                        self.assertGreaterEqual(final.count(seq), n)
            for antigo, novo, _, n in x.get('literais', []):
                with self.subTest(achado=i, literal=antigo):
                    self.assertEqual(base(rel).count(antigo), n)
                    self.assertEqual(final.count(C.j(novo)), n)
        self.assertEqual(vistos, sum(len(x['pares']) for x in C.ACHADOS_B))
        # A casca das lições (migalhas, «Estás em», título escondido e sigla do rodapé) fica para o molde, como do M1 ao M5.
        self.assertEqual(len(C.CASCA_NO_MOLDE), 9)
        for rel in C.CASCA_NO_MOLDE:
            texto = ler(rel)
            n = re.search(r'licao-m6-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                for trecho in (f'Estás em: Lição M6-{n}', f'<h1 class="c-sr">Lição M6-{n}', f'Português 2026/2027. Lição M6-{n},',
                               '/pt/2/">2.º ano</a>', '>Módulo 6: Poesia Realista</a>'):
                    self.assertEqual(texto.count(trecho), 1, trecho)
                self.assertEqual(next(x for x in C.ACHADOS_B if x['ficheiro'] == rel)['casca'], C.casca(n))
        # Nas outras páginas, as migalhas ficam (a conferência viu que o «2.º ano» das migalhas não se parte) e muda o cabeçalho.
        for rel, cab in (('m6/index.html', 'Português, 2.º' + N + 'ano, percurso do módulo'),
                         ('m6/guia-da-tarefa-m6/index.html', 'Guia da tarefa, 2.º' + N + 'ano'),
                         ('m6/mapa-do-modulo-m6/index.html', 'Português · 2.º' + N + 'ano · Mapa do módulo'),
                         ('m6/portefolio-do-modulo-m6/index.html', 'Português · 2.º' + N + 'ano · Módulo 6')):
            self.assertIn('/pt/2/">2.º ano</a>', ler(rel), rel)
            self.assertIn(cab, ler(rel), rel)
        # Os intervalos levam a junção; a sigla das ligações do mapa também (os href, em minúsculas, ficam); e a da F04.
        mapa = ler('m6/mapa-do-modulo-m6/index.html')
        self.assertIn('(Ponta Delgada, 1842–' + WJ + '1891)', mapa)
        self.assertIn('(Lisboa, 1855–' + WJ + '1886)', mapa)
        self.assertEqual(len(re.findall(r'>[Ll]ição M6-' + WJ + r'F\d\d<', mapa)), 8)
        self.assertNotRegex(mapa, r'>[Ll]ição M6-F\d\d<')
        self.assertIn('href="https://pedrohfernandes-klk.github.io/pt/m6/licao-m6-f07/">Lição M6-' + WJ + 'F07</a>', mapa)
        self.assertIn('<a href=\\"../licao-m6-f07/\\">M6-' + WJ + 'F07</a>', ler('m6/licao-m6-f04/index.html'))
        # As legendas e os créditos do «i» do mapa que outra camada já tinha posto com U+00A0 ficam; os «alt» ficam com espaços normais.
        self.assertIn('<figcaption>Antero de Quental (fotografia, c.' + N + '1887).', mapa)
        self.assertIn('<span class="nb">c.' + N + '1900</span>', mapa)
        self.assertIn('alt="Antero de Quental (fotografia, c. 1887, publicada em In Memoriam, 1896)"', mapa)
        # Os intervalos de versos na forma da M7-F10 (F02, F06 e as cópias do banco).
        f02 = ler('m6/licao-m6-f02/index.html')
        for vv in ('(vv.' + N + '1–' + WJ + '4)', '(vv.' + N + '1–' + WJ + '2)'):
            self.assertEqual(f02.count(vv), 1, vv)
        self.assertEqual(f02.count('(vv.' + N + '9–' + WJ + '10)'), 2)
        self.assertNotRegex(f02, r'\(v\.[ \xa0]\d+ [ae] \d+\)')
        self.assertEqual(ler('m6/licao-m6-f06/index.html').count('(vv.' + N + '16–' + WJ + '17)'), 1)
        indice = ler('m6/index.html')
        self.assertEqual(indice.count('(vv.' + N + '1–' + WJ + '4)'), 1)
        self.assertEqual(indice.count('(vv.' + N + '13–' + WJ + '14)'), 1)
        # Os vídeos: o botão muda, o data-titulo (que vira o title do leitor) fica.
        self.assertIn('data-titulo=\\"«Na mão de Deus», de Antero, com imagens (2 min)\\"', f02)
        self.assertIn('data-yt-abrir>Ouvir: «Na mão de Deus», de Antero, com imagens (2' + N + 'min)</button>', f02)
        # As datas da F11 e de «Os bairros da Sam» com todos os espaços presos, como na proposta do M6.
        f11 = ler('m6/licao-m6-f11/index.html')
        self.assertIn('pistas:["Cesário Verde: Lisboa, 25' + N + 'de' + N + 'fevereiro' + N + 'de' + N + '1855 a 19' + N + 'de' + N + 'julho'
                      + N + 'de' + N + '1886, tuberculose, 31' + N + 'anos;', f11)
        self.assertEqual(ler('m6/sam-chelas/index.html').count('9' + N + 'de' + N + 'abril' + N + 'de' + N + '2021'), 3)
        # As tarefas: os números do molde e a ligação à grelha, pelo gerador.
        for slug in ('m6-u1', 'm6-u2'):
            t = ler(f'tarefas/{slug}/index.html')
            self.assertIn('Antes de escrever · 10' + N + 'min · em cartões, com consulta', t)
            self.assertIn(f'Tarefa individual · Unidade {slug[-1]} · 90' + N + 'min</p>', t)
            self.assertIn('<p class="task-grelha"><a href="grelha/">Grelha' + N + '/20: como é avaliado e autoavaliação</a></p>', t)
            self.assertNotIn('90 min', t)
            self.assertIn('<p class="lead">20' + N + 'valores em cinco critérios.', ler(f'tarefas/{slug}/grelha/index.html'))

    def test_nenhum_recusado_aplicado(self):
        # 11/11/2026: as reposições depois do #192 não são achados da varredura (test_reposicoes_depois_do_192).
        achados = {int(n) for t in VARREDURA for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertFalse(RECUSADOS & achados)
        # 9: o cartão da F13 fica em frase.
        self.assertIn('a apóstrofe escolhe', ler('m6/licao-m6-f13/index.html'))
        self.assertNotIn('apoio-tabela', ler('m6/licao-m6-f13/index.html'))
        # 11, 12 e 13: os pesos da avaliação ficam no parágrafo (só com os espaços que não quebram dos achados 32 a 34).
        for rel in ('m6/index.html', 'm6/guia-da-tarefa-m6/index.html', 'm6/mapa-do-modulo-m6/index.html'):
            pesos = re.search(r'<p class="avaliacao-tarefas">(.*?)</p>', ler(rel)).group(1)
            self.assertIn('tarefa da Unidade 1, 30' + N + '%; tarefa da Unidade 2, 30' + N + '%; provas rápidas, 10' + N + '%; prova escrita, '
                          '30' + N + '%.', pesos, rel)
        # 14 e 15: os tempos da aula de tarefa ficam em frase (nos dados e na página), sem «tabela».
        for slug in ('m6-u1', 'm6-u2'):
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            self.assertNotIn('tabela', d['aquecer'])
            self.assertIn('<p>No início da aula de tarefa: 10' + N + 'minutos de cartões com consulta, 5' + N + 'minutos para leres o '
                          'enunciado, 60' + N + 'minutos de produção e 15' + N + 'minutos de revisão e entrega. Total: 90' + N + 'minutos.',
                          ler(f'tarefas/{slug}/index.html'))
        # 21: «Três antes de mim» fica como estava no guia do M6.
        self.assertIn('Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta', ler('m6/guia-da-tarefa-m6/index.html'))

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, cab, _, _ in TABELAS for c in cab} | {'Nome do ficheiro', 'O que é'}
        # Os rótulos das linhas que a proposta tira da estrutura (não estavam escritos como rótulo).
        rotulos = {'Recursos', 'O que faz', 'Exemplo', 'Real', 'Relação'}
        permitidas = {p for c in cabecalhos | rotulos for p in palavras(c)}
        # O que entra de propósito: o verso da comparação da F02 (o verso 10 de «Na mão de Deus», no poema da lição) e a frase que o
        # anuncia; o exemplo da antítese da F07 (o do «O essencial», cartão 1); «vv.» dos intervalos; nos dados, as chaves que os
        # geradores leem.
        entram = {6: {'o', 'da', 'comparação', 'de', 'na', 'mão', 'deus', 'como', 'criança', 'em', 'lobrega', 'jornada'},
                  8: {'inflamma', 'se', 'um', 'palacio', 'em', 'face', 'de', 'casebre', 'v', '28'},
                  23: {'vv'}, 26: {'vv'}, 32: {'vv'}, 19: {'max_em_listas', 'true'}, 20: {'max_em_listas', 'true'}}
        # O que sai: o «v.», o «e» e o «a» dos intervalos de versos («v. 1 e 2» passa a «vv. 1–2», «v. 1 a 4» a «vv. 1–4»), e as
        # palavras de ligação que a tabela substitui pelas colunas («em» na F04, «dá» na F05, «como» na F07).
        saem = {23: {'v', 'e', 'a'}, 26: {'v', 'e'}, 32: {'v', 'e', 'a'}, 5: {'em'}, 16: {'dá'}, 8: {'como'}}
        css = [t for t in TROCAS if t['novo'].startswith('<link rel="stylesheet"')]
        self.assertEqual(sorted(t['ficheiro'] for t in css), sorted(C.COM_TABELA))
        estilo = [t for t in TROCAS if 'code{white-space:nowrap}' in t['novo']]
        self.assertEqual(len(estilo), 1)
        chaves = [t for t in TROCAS if '"nao_partir' in t['novo'] and '"nao_partir' not in t['antigo']]
        self.assertEqual(sorted(t['ficheiro'] for t in chaves), ['docs/pedagogia/grelhas-tarefas-20261027.json'] * 2
                         + ['docs/pedagogia/tarefas-escolha/m6-u1.json', 'docs/pedagogia/tarefas-escolha/m6-u2.json'])
        for t in TROCAS:
            # 11/11/2026: as reposições depois do #192 só mudam espaços e não têm número de achado: test_reposicoes_depois_do_192.
            if t in css or t in estilo or t in chaves or t in REPOSTAS:
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
                self.assertTrue(t['achado'].startswith('08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M6'))
        # O que entra de propósito está mesmo na lição: o verso da comparação no poema da F02 e o exemplo da antítese no cartão 1 da F07.
        self.assertIn('Como criança, em <b class=\\"gt\\" data-s=\\"escura, triste\\">lobrega</b> jornada', base('m6/licao-m6-f02/index.html'))
        self.assertIn('«Inflamma-se um palacio em face de um casebre» (v. 28)', base('m6/licao-m6-f07/index.html'))
        for c in cabecalhos | rotulos:
            self.assertIsNone(PROIBIDAS.search(c), c)
        # As trocas B só mudam espaços (U+00A0) e põem a junção (U+2060), salvo os intervalos de versos (TEXTO_MUDA).
        for t in TROCAS:
            if '(B)' in t['achado'] and (t['ficheiro'], t['antigo']) not in TEXTO_MUDA and t not in chaves:
                with self.subTest(local=t['local']):
                    self.assertEqual(t['novo'].replace(N, ' ').replace(WJ, ''), t['antigo'])
        self.assertEqual(sum((t['ficheiro'], t['antigo']) in TEXTO_MUDA for t in TROCAS), len(TEXTO_MUDA))
        # Nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, data-titulo, <title>, chaves JSON, nem da «frase» de
        # um sublinhar, das «palavras» de um cartão frase ou dos «passos» de um ordenar.
        for rel in MANIFESTO['files']:
            with self.subTest(contextos=rel):
                conta = lambda texto: sum(p.count(N) + p.count(WJ) for p in contextos_proibidos(texto))
                self.assertEqual(conta(ler(rel)), conta(base(rel)))
        # O detetor dos campos dos exercícios apanha-os: a «frase» do sublinhar da F05 e os «passos» do ordenar do aquecimento.
        f05 = ler('m6/licao-m6-f05/index.html')
        self.assertEqual(C.fora_de_alcance(f05, f05.index('"frase":"As edições do século XIX') + 30), 'frase de um cartão sublinhar')
        self.assertIn('"frase":"As edições do século XIX mostram', f05)
        aq = ler('docs/pedagogia/aquecimentos/m6-u1.json')
        self.assertEqual(C.fora_de_alcance(aq, aq.index('contas as palavras: 200 a 240') + 22), 'passos de um cartão ordenar')

    def test_passagens_mudadas_sem_referencias_que_se_partam(self):
        for t in TROCAS:
            if t['novo'].startswith('<link rel="stylesheet"') or 'code{' in t['novo']:
                continue
            texto = sem_atributos_nem_desenhos(t['novo'])
            texto = visivel(texto) if '<' in texto else texto
            # O que fica de fora dentro de uma troca maior: a frase da pista da F11 (« a » entre as duas datas, que juntas não caberiam
            # numa linha) e a autoavaliação «de 0 a 20» do portefólio (a proposta não a pede; está na tabela que o achado 18 refaz).
            m = PARTE.search(texto.replace('1855 a 19' + N, '1855·a·19' + N).replace('de 0 a 20 por parâmetro', 'de 0·a·20 por parâmetro'))
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                self.assertIsNone(m, m and texto[max(0, m.start() - 30):m.end() + 30])
        # Cada troca B arranja alguma coisa que se partia: na base, com o texto à volta, o detetor apanha uma forma que se parte
        # dentro do trecho da troca (as chaves dos geradores prendem os números do molde, conferidos noutro teste).
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
            for antigo, novo, _ in x['pares']:
                for m in re.finditer(re.escape(antigo), final):
                    self.assertFalse(em_alcance(final, m.start(), antigo, novo), (x['ficheiro'], antigo))
        # E o contrário: o detetor apanha as formas que partem, e deixa as inteiras.
        for partido in ('v. 7', '(vv. 1–4)', 'verso 36', 'versos 27 e 28', 'versos 1 a 3', 'c. 1887', 'n.º 8698', 'S. Petersburgo', 'século XIX', 'parte I',
                        '2.º ano', '90 minutos', '10 min', '30 %', '200 exemplares', '31 anos', '54 segundos', '20 valores', 'grelha /20',
                        '15 palavras', '19 de julho de 1886', '19' + N + 'de julho', '1855 a 1886', '200 e 240', '4 + 4 + 3 + 3', '1842–1891',
                        'M6-F07'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for x in C.ACHADOS_B:
            for _, novo, _ in x['pares']:
                self.assertIsNone(PARTE.search(C.j(novo) + '0'), novo)

    def test_camada_fechada_reversivel_e_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m6_20261108.json', '--manifesto', MANIFESTO_REL,
                            # 11/11/2026: por cima desta camada fica agora a decisão 152 no M7 (cuidado_m7_20261111, que só partilha com esta os
                            # dados das grelhas, na entrada m7-u3); desfaz-se primeiro, com a mesma exigência, e as contagens são as mesmas.
                            # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M9, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», as atividades e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            '--verificar', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-provas-oficial-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-exame-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m9-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m8-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m7-edits-20261111.json'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        # 11/11/2026: às 270 trocas em 38 ficheiros da varredura juntam-se as 23 reposições depois do #192, em 13 ficheiros (os dados
        # e as páginas das tarefas M1-U2, M3-U1, M3-U2, M5-U1 e M5-U2 e as páginas das três tarefas do M4).
        self.assertEqual((len(VARREDURA), len({t['ficheiro'] for t in VARREDURA})), (270, 38))
        self.assertEqual((len(REPOSTAS), len({t['ficheiro'] for t in REPOSTAS})), (23, 13))
        self.assertFalse({t['ficheiro'] for t in VARREDURA} & {t['ficheiro'] for t in REPOSTAS})
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), (293, 51))
        self.assertIn('11/11/2026 (reposição, no mesmo pedido #191): a camada repõe também os espaços que não quebram (U+00A0) que o #192 '
                      'tirou às tarefas do M1, do M3, do M4 e do M5', m_nota := MANIFESTO['_nota'])
        self.assertIn('23 trocas «(R)» em 13 ficheiros, só de espaços', m_nota)
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M6'))
        self.assertIn('cuidado_m5_20261108', m['_nota'])
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
                # 11/11/2026: a página como esta camada a deixou: com a camada de cima (cuidado_m7_20261111) desfeita, com contagem
                # estrita; undo_cuidado_m6_0811 desfaz as duas, a partir da página inteira.
                atual = undo_cuidado_m7_1111(rel, ler(rel))
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_m6_0811(rel, ler(rel))
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
                # A camada de baixo (a decisão 152 no M5) continua a desfazer-se por baixo desta.
                # 11/11/2026: na página inteira, porque a cadeia de desfazer começa agora pela decisão 152 no M7.
                undo_cuidado_m5_0811(rel, ler(rel))
        # Os 43 achados confirmados estão todos na camada, salvo o 29 (só a casca, que fica para o molde); nenhum recusado.
        # 11/11/2026: sem as reposições depois do #192, que não são achados da varredura.
        achados = {int(n) for t in VARREDURA for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertEqual(achados, CONFIRMADOS - SO_CASCA)
        self.assertEqual((len(A), len(B), len(C_)), (11, 28, 4))
        self.assertEqual(next(x for x in C.ACHADOS_B if x['i'] == 29)['pares'], [])
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'A'}), sorted(A))
        self.assertEqual(sorted({x['i'] for x in C.achados_ac() + C.ac_grelhas() if x['cat'] == 'C'}), sorted(C_))
        # 35 achados nas páginas do M6 e 8 nas das tarefas, como na varredura.
        sitio = {x['i']: x['ficheiro'] for x in C.achados_ac() + C.ac_grelhas() + C.ACHADOS_B}
        self.assertEqual(sum(f.startswith('m6/') for f in sitio.values()), 35)
        self.assertEqual(sum(f.startswith('tarefas/') for f in sitio.values()), 8)
        # A e C antes de B, em cada ficheiro.
        for rel in m['files']:
            ordem = ['B' if '(B)' in t['achado'] and '"nao_partir' not in t['novo'] else 'AC' for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual(ordem, sorted(ordem, key=lambda x: x != 'AC'), rel)
        # No topo da cadeia.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 11/11/2026: por cima da decisão 152 no M6 fica a decisão 152 no M7 (cuidado_m7_20261111): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M7 fica a decisão 152 no M8 (cuidado_m8_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M8 fica a decisão 152 no M9 (cuidado_m9_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M9 fica a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no Exame e nas páginas transversais fica a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da ligação «Treinos» na página principal do Exame ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima das provas em cartões com os documentos oficiais ficam as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M3 mais fáceis de fazer ficam as duas tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M1 mais fáceis de fazer ficam as duas tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[7], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[8], ('cuidado_m9_20261112', 'cuidado-m9-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[9], ('cuidado_m8_20261112', 'cuidado-m8-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[10], ('cuidado_m7_20261111', 'cuidado-m7-edits-20261111'))
        self.assertEqual(verificar_camadas.LAYERS[11], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): logo abaixo da decisão 152 no M6 fica a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192), por cima da decisão 152 no M5; as posições seguintes descem uma.
        self.assertEqual(verificar_camadas.LAYERS[12], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[13], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m5_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m6_0811(path, text)'), corpo.index('_CUIDADO_M5_0811.get('))
        # 11/11/2026: e a decisão 152 no M6 chama primeiro a decisão 152 no M7, que está por cima.
        self.assertLess(auditoria.index('undo_cuidado_m7_1111(path, text)', auditoria.index('def undo_cuidado_m6_0811')), auditoria.index('_CUIDADO_M6_0811.get('))
        # 12/11/2026: e a decisão 152 no M7 chama primeiro a decisão 152 no M8, que está por cima.
        self.assertLess(auditoria.index('undo_cuidado_m8_1112(path, text)', auditoria.index('def undo_cuidado_m7_1111')), auditoria.index('_CUIDADO_M7_1111.get('))
        # 12/11/2026: e a decisão 152 no M8 chama primeiro a decisão 152 no M9, que está por cima.
        self.assertLess(auditoria.index('undo_cuidado_m9_1112(path, text)', auditoria.index('def undo_cuidado_m8_1112')), auditoria.index('_CUIDADO_M8_1112.get('))
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): entre as duas desfaz-se a revisão dos enunciados das tarefas (#192): primeiro
        # esta camada, depois a dos enunciados, depois a do M5.
        self.assertLess(corpo.index('undo_cuidado_m6_0811(path, text)'), corpo.index('text = desfazer(path, text)'))
        self.assertLess(corpo.index('text = desfazer(path, text)'), corpo.index('_CUIDADO_M5_0811.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m6-edits-20261108.json'), sala.index('cuidado-m5-edits-20261108.json'))
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7, agora a mais recente.
        self.assertLess(sala.index('cuidado-m7-edits-20261111.json'), sala.index('cuidado-m6-edits-20261108.json'))
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8, agora a mais recente.
        self.assertLess(sala.index('cuidado-m8-edits-20261112.json'), sala.index('cuidado-m7-edits-20261111.json'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9, agora a mais recente.
        self.assertLess(sala.index('cuidado-m9-edits-20261112.json'), sala.index('cuidado-m8-edits-20261112.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes da decisão 152 no M5, logo a seguir a --verificar.
        meu, m5 = MANIFESTO_REL, 'tests/fixtures/cuidado-m5-edits-20261108.json'
        # 11/11/2026: e logo a seguir à decisão 152 no M7, que se desfaz primeiro, logo a seguir a --verificar, sem nada pelo meio.
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
        # 13/11/2026: por cima das tarefas do M3 ficam as tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M1 ficam as tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): desfazem-se primeiro em todas as cadeias, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        t6 = 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'
        t7 = 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'  # 13/11/2026: a camada das tarefas do M7 mais fáceis de fazer, a mais recente
        t5 = 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
        t1 = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): entre esta camada e a do M5 fica a revisão dos enunciados das tarefas
        # (tarefas_claras_20261110, #192): em cada cadeia dos fluxos, esta desfaz-se primeiro, a dos enunciados a seguir, e só depois a do M5.
        claras = 'tests/fixtures/tarefas-claras-edits-20261110.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + m5 not in linha:
                    continue
                linhas += 1
                # 11/11/2026: antes desta, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertIn(f'--verificar --desfazer-antes {t7} --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {meu} --desfazer-antes {claras} --desfazer-antes {m5}', linha, wf)
        # As 18 cadeias da decisão 152 no M5 e a da decisão 152 no M4 em pt-tarefas-qa.
        self.assertEqual(linhas, 19)
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        # 11/11/2026: a decisão 152 no M5 desfaz primeiro a do M7 e depois esta.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m5_20261108.json --manifesto {m5} --verificar --desfazer-antes {t7} --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {meu} --desfazer-antes {claras}\n',
                      tarefas)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --verificar '
                      # 11/11/2026: o cartaz «Ler a cidade» desfaz primeiro a decisão 152 no M7, depois esta.
                      # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                      # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                      f'--desfazer-antes {t7} --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {meu} --desfazer-antes {claras} --desfazer-antes {m5} --desfazer-antes tests/fixtures/cuidado-m4-edits-20261108.json', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e da decisão 152 no M1 conferem as cadeias com frases partidas em várias linhas (e já
            # exigem esta camada à cabeça); ficam de fora pela mesma razão.
            # 11/11/2026: e o teste da decisão 152 no M7, pela mesma razão.
            if p.name in ('test_cuidado_m6.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py', 'test_cuidado_m7.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): entre a decisão 152 no M6 e a do M5 fica a revisão dos enunciados das tarefas
            # (tarefas_claras_20261110), nas cadeias onde o #192 a pôs; nas que o #192 não mudou (test_cartaz_m4_piloto.py e test_variedade_f0.py),
            # a do M5 continua logo a seguir à do M6. A contagem lê as duas formas como uma só; nada mais cabe entre as duas.
            plano = plano.replace('--desfazer-antes ' + meu + ' --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json ', '--desfazer-antes ' + meu + ' ')
            with self.subTest(teste=p.name):
                # 11/11/2026: e, antes desta, a decisão 152 no M7, sem nada pelo meio.
                # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes ' + m5), plano.count(f'--desfazer-antes {t7} --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {meu} --desfazer-antes {m5}'))
        # 11/11/2026: nas rotas, a decisão 152 no M7 vem primeiro, logo antes desta.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f"(ROOT/'{t7}',ROOT/'{t6}',ROOT/'{t5}',ROOT/'{t1}',ROOT/'{tf}',ROOT/'{po}',ROOT/'{lt}',ROOT/'{ex}',ROOT/'{m9}',ROOT/'{m8}',ROOT/'{m7}',ROOT/'{meu}',ROOT/'{m5}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM6['), texto.index('((cuidadoM5['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM6[rel]'), corpo.index('((cuidadoM5[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M6.read_text'), gerador_148.index('CUIDADO_M5.read_text'))
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7.
        self.assertLess(gerador_148.index('CUIDADO_M7.read_text'), gerador_148.index('CUIDADO_M6.read_text'))
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8.
        self.assertLess(gerador_148.index('CUIDADO_M8.read_text'), gerador_148.index('CUIDADO_M7.read_text'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9.
        self.assertLess(gerador_148.index('CUIDADO_M9.read_text'), gerador_148.index('CUIDADO_M8.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1 ao M5.
        # 11/11/2026: conferem-na com a decisão 152 no M7, a única por cima, desfeita antes.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m6_20261108.json --manifesto {meu} --verificar --desfazer-antes {t7} --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7}\n', tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m6.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m6.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m6_20261108.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)
        # O teste de navegador das comparações conta agora os 53 cartões «Em paralelo» que ficam.
        self.assertIn('assert len(examples)>=53', ler('tests/browser_comparacao_layout.py'))

    def test_reposicoes_depois_do_192(self):
        # 11/11/2026: o pedido #192 (tarefas_claras_20261110) reescreveu os enunciados das tarefas e deixou cair espaços que não
        # quebram que a decisão 152 tinha posto do M1 ao M5 (tests/browser_cuidado_m3.py falhava, também no main). Esta camada, por
        # cima dele, repõe-os: as trocas são exatamente estas, nos dados (nas tarefas geradas) e na página.
        claras = json.loads(ler('tests/fixtures/tarefas-claras-edits-20261110.json'))['files']
        esperadas = []
        for slug, (mod, gerada, pares) in REPOR.items():
            for rel in ([f'docs/pedagogia/tarefas-escolha/{slug}.json'] if gerada else []) + [f'tarefas/{slug}/index.html']:
                esperadas += [(rel, antigo, novo, n) for antigo, novo, n, _ in pares]
        self.assertEqual(sorted((t['ficheiro'], t['antigo'], t['novo'], t['ocorrencias']) for t in REPOSTAS), sorted(esperadas))
        self.assertEqual(len(REPOSTAS), 23)
        for t in REPOSTAS:
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                # Só espaços: nenhuma outra letra do texto do #192 muda, e nenhum espaço preso se solta.
                self.assertEqual(t['novo'].replace(N, ' '), t['antigo'].replace(N, ' '))
                self.assertGreater(t['novo'].count(N), t['antigo'].count(N))
                self.assertTrue(all(a == b or (a, b) == (' ', N) for a, b in zip(t['antigo'], t['novo'])))
                self.assertNotIn(WJ, t['novo'])
                self.assertNotIn('varredura do M6', t['achado'])
                slug = re.search(r'(m\d-u\d(?:-discurso)?)', t['ficheiro']).group(1)
                self.assertIn(f'a decisão 152 no {REPOR[slug][0]} tinha posto', t['achado'])
        for slug, (mod, gerada, pares) in REPOR.items():
            pagina = f'tarefas/{slug}/index.html'
            for rel in ([f'docs/pedagogia/tarefas-escolha/{slug}.json'] if gerada else []) + [pagina]:
                with self.subTest(ficheiro=rel):
                    atual = ler(rel)
                    # Por baixo desta camada está o texto do #192, letra a letra (o «after» do manifesto dele).
                    do_192 = base(rel)
                    self.assertEqual(sha_lf(do_192), claras[rel]['after_sha256_lf'])
                    self.assertEqual(atual.replace(N, ' '), do_192.replace(N, ' '))
                    # Os contratos históricos leem a página como era antes do #192 (a base do manifesto dele): a partir da página
                    # inteira (desfaz esta camada e a dos enunciados), ou só da dos enunciados, se esta já saiu.
                    antes_192 = desfazer_enunciados(rel, atual)
                    self.assertEqual(sha_lf(antes_192), claras[rel]['base_sha256_lf'])
                    self.assertEqual(desfazer_enunciados(rel, do_192), antes_192)
                    self.assertEqual(undo_cuidado_m6_0811(rel, antes_192), antes_192)
                    # A página volta a ter os espaços que não quebram que tinha antes do #192 (ele tinha-lhe tirado os desta conta).
                    repostos = sum((novo.count(N) - antigo.count(N)) * n for antigo, novo, n, _ in pares)
                    self.assertEqual(do_192.count(N), antes_192.count(N) - repostos)
                    self.assertEqual(atual.count(N), antes_192.count(N))
                    for antigo, novo, n, de_antes in pares:
                        self.assertEqual(do_192.count(antigo), n, antigo)
                        self.assertEqual(atual.count(novo), n, novo)
                        self.assertNotIn(antigo, atual)
                        # A forma que a decisão 152 tinha posto estava na página antes do #192; onde o #192 trocou «cap.» por
                        # «capítulo», essas ocorrências da abreviatura já não existem (as outras, fora do que ele reescreveu,
                        # continuam presas), e é a forma nova que fica presa.
                        self.assertGreaterEqual(antes_192.count(de_antes), n)
                        if de_antes.startswith('cap.'):
                            self.assertEqual(atual.count(de_antes + ' ') + atual.count(de_antes + ',') + atual.count(de_antes + '.'),
                                             antes_192.count(de_antes + ' ') + antes_192.count(de_antes + ',')
                                             + antes_192.count(de_antes + '.') - n)
                            self.assertNotIn(de_antes.replace(N, ' '), atual)
                            self.assertNotIn(novo, antes_192)
                        else:
                            self.assertEqual(atual.count(de_antes), antes_192.count(de_antes))
            # No enunciado (o <header> da tarefa), nenhuma referência do tipo que a decisão 152 prende nesse módulo se parte; antes
            # desta reposição, o detetor apanhava cada uma delas.
            with self.subTest(enunciado=slug):
                enunciado = lambda texto: visivel(texto.split('<header>', 1)[1].split('</header>', 1)[0])
                self.assertIsNone(PARTE_REPOR[mod].search(enunciado(ler(pagina))))
                self.assertIsNotNone(PARTE_REPOR[mod].search(enunciado(base(pagina))))
                for antigo, novo, _, _ in pares:
                    self.assertIsNotNone(PARTE_REPOR[mod].search(visivel(antigo)), antigo)
                    self.assertIsNone(PARTE_REPOR[mod].search(visivel(novo)), novo)
        # As tarefas geradas saem iguais dos dados, byte a byte.
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, 'scripts/tarefas_escolha.py', '--saida', tmp], cwd=ROOT, capture_output=True, text=True,
                               encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for slug, (_, gerada, _) in REPOR.items():
                if gerada:
                    self.assertEqual((Path(tmp) / f'tarefas/{slug}/index.html').read_bytes(), (ROOT / f'tarefas/{slug}/index.html').read_bytes(), slug)
                else:
                    self.assertFalse((ROOT / f'docs/pedagogia/tarefas-escolha/{slug}.json').exists(), slug)
        # O gerador da camada tem as mesmas reposições.
        self.assertEqual({x['slug']: (x['mod'], x['gerada'], [(C.j(a), C.j(b), n) for a, b, n, _ in x['pares']]) for x in C.REPOR},
                         {slug: (mod, gerada, [(a, b, n) for a, b, n, _ in pares]) for slug, (mod, gerada, pares) in REPOR.items()})

    def test_cartoes_em_paralelo_que_ficam(self):
        # Os seis «Em paralelo» do M6 que passaram a tabela saem da conta de tests/browser_comparacao_layout.py: eram 59, ficam 53.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from audit_cards import lesson_cards
        finally:
            sys.path.pop(0)
        n = sum('class="paralelo"' in c.get('html', '') for p in ROOT.glob('m[1-9]/licao-*/index.html') for c in lesson_cards(p))
        self.assertEqual(n, 53)

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_dos_dados(self):
        # As tarefas, os aquecimentos, as grelhas e a correção da M6-U1 e da M6-U2 mudam também nos dados, que estão nesta camada.
        # 11/11/2026: os dados das cinco tarefas geradas com reposições depois do #192 conferem-se em test_reposicoes_depois_do_192.
        dados = {t['ficheiro'] for t in VARREDURA if t['ficheiro'].startswith('docs/')}
        self.assertEqual({t['ficheiro'] for t in REPOSTAS if t['ficheiro'].startswith('docs/')},
                         {f'docs/pedagogia/tarefas-escolha/{slug}.json' for slug, (_, gerada, _) in REPOR.items() if gerada})
        self.assertEqual(dados, {'docs/pedagogia/tarefas-escolha/m6-u1.json', 'docs/pedagogia/tarefas-escolha/m6-u2.json',
                                 'docs/pedagogia/aquecimentos/m6-u1.json', 'docs/pedagogia/aquecimentos/m6-u2.json',
                                 'docs/pedagogia/grelhas-tarefas-20261027.json'})
        for slug in ('m6-u1', 'm6-u2'):
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            self.assertIs(d['nao_partir'], True)
            self.assertIs(d['nao_partir_grelha'], True)
        # As chaves novas só estão no M6 (as outras tarefas e grelhas saem iguais, byte a byte).
        for p in sorted((ROOT / 'docs/pedagogia/tarefas-escolha').glob('*.json')):
            if not p.name.startswith('m6-'):
                self.assertNotIn('nao_partir_grelha', json.loads(p.read_text('utf-8')), p.name)
        grelhas = json.loads(ler('docs/pedagogia/grelhas-tarefas-20261027.json'))['tarefas']
        self.assertEqual(sorted(s for s, t in grelhas.items() if t.get('nao_partir_valores')), ['m6-u1', 'm6-u2'])
        with tempfile.TemporaryDirectory() as tmp:
            for pasta, comando in (('te', 'scripts/tarefas_escolha.py'), ('gr', 'scripts/grelhas_tarefas.py'), ('aq', 'scripts/aquecimentos.py')):
                r = subprocess.run([sys.executable, comando, '--saida', str(Path(tmp) / pasta)], cwd=ROOT, capture_output=True, text=True,
                                   encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for slug in ('m6-u1', 'm6-u2'):
                for pasta, pagina in (('te', ''), ('aq', 'aquecimento/'), ('gr', 'grelha/'), ('gr', 'correcao/')):
                    self.assertIn(f'{pasta}/tarefas/{slug}/{pagina}index.html', geradas)
            # O gerador das grelhas não acrescenta outra ligação à tarefa: a do M6, com «Grelha /20» preso, já conta.
            self.assertFalse([g for g in geradas if g.startswith('gr/') and g.count('/') == 3])
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel.split('/', 1)[1]).read_bytes())
        # A correção não muda (os descritores do nível máximo da correção ficam em texto corrido e sem pares B).
        for slug in ('m6-u1', 'm6-u2'):
            self.assertNotIn(f'tarefas/{slug}/correcao/index.html', MANIFESTO['files'])
        # A lição F14 e as suas notas do docente saem iguais do gerador das lições (a fonte mudou fora da camada).
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from licoes_20261101 import LESSONS
            from gerar_licoes_20261101 import render, sequences, render_notes
        finally:
            sys.path.pop(0)
        unidades = sequences()
        item = next(x for x in LESSONS if x['id'] == 'm6-f14')
        self.assertEqual(ler('m6/licao-m6-f14/index.html'), render(item, unidades))
        self.assertEqual(ler('m6/painel-m6-f14/index.html'), render_notes(item))
        self.assertIn('conferência de 27' + N + 'de' + N + 'maio' + N + 'de' + N + '1871', json.dumps(item['cards'], ensure_ascii=False))

    def test_paineis_seguem_as_licoes(self):
        # Os painéis de projeção das lições do M6 mostram os enunciados dos cartões: onde um mudou, o painel muda igual, na lista e no
        # seletor (como scripts/sync_teacher_labels.py os escreve); e cada enunciado segue a lição.
        paineis = sorted({t['ficheiro'] for t in TROCAS if '/painel-' in t['ficheiro']})
        self.assertEqual(paineis, ['m6/painel-m6-f01/index.html', 'm6/painel-m6-f06/index.html', 'm6/painel-m6-f08/index.html',
                                   'm6/painel-m6-f11/index.html'])
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from sync_teacher_labels import synchronize
        finally:
            sys.path.pop(0)
        r = synchronize(ROOT, modules=('m6',))
        self.assertEqual(r['different'], [])
        self.assertEqual(len(r['checked']), 9)
        # O material do relâmpago (MATERIAL) segue a lição antes das camadas de cuidado (tests/test_sala_desligada.py): não muda.
        for rel in paineis:
            antes, depois = base(rel), ler(rel)
            self.assertEqual(antes.split(',MATERIAL=', 1)[1].split(',crono=')[0], depois.split(',MATERIAL=', 1)[1].split(',crono=')[0], rel)

    def test_banco_segue_as_licoes(self):
        # As cópias dos cartões no banco das provas rápidas do índice (var U) mudam como as lições de onde vêm: cada cópia que era
        # igual a um cartão da sua lição antes desta camada continua igual depois, campo a campo.
        copias, copias_antes = banco(ler('m6/index.html')), banco(base('m6/index.html'))
        self.assertEqual(len(copias), len(copias_antes))
        iguais = 0
        for copia, antes in zip(copias, copias_antes):
            licao = f"m6/licao-{antes.get('_l')}/index.html"
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
        # Os testes do M6 que comparam as cópias com os cartões continuam a passar com a mesma exigência (test_m6_observar_imaginar,
        # test_m6_recursos), e o «Em paralelo» do banco, se o houver, não tem tabela.
        self.assertNotIn('apoio-tabela', ler('m6/index.html'))
        # A cópia do retorno do cartão da F01 nas sessões do Exame (s10, na pergunta e na verificação) segue a lição, letra a letra
        # (tests/test_exame_alignment.py): é a única troca da camada fora das páginas do M6, das tarefas e dos dados dos geradores.
        f01 = next(c for c in cartoes(ler('m6/licao-m6-f01/index.html')) if c.get('f', '').startswith('«Sonho que sou um cavalleiro andante»'))
        sessoes = ler('assets/exame/sessoes.json')
        self.assertEqual(sessoes.count(json.dumps(f01['f'].replace('**', ''), ensure_ascii=False)), 2)
        self.assertIn('(v.' + N + '1): o sujeito', f01['f'])
        # 11/11/2026: e as páginas das oito tarefas do M1, do M3, do M4 e do M5 a que a camada repõe os espaços que o #192 tirou.
        self.assertEqual(sorted(f for f in MANIFESTO['files'] if not f.startswith(('m6/', 'tarefas/m6-', 'docs/pedagogia/'))),
                         ['assets/exame/sessoes.json'] + sorted(f'tarefas/{slug}/index.html' for slug in REPOR))


if __name__ == '__main__':
    unittest.main()
