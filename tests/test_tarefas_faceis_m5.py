"""13/11/2026: as duas tarefas do M5 (m5-u1 e m5-u2) «mais fáceis de fazer» e «tudo junto» no M5, com dois acertos do M3 (camada
tarefas_faceis_m5_20261113).

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201) e levado ao M1 (pedido #203). Esta camada
leva-o ao M5, e este ficheiro exige das duas tarefas do M5 o que tests/test_tarefas_faceis_m3.py e tests/test_tarefas_faceis_m1.py
exigem das do M3 e das do M1:

* a tarefa pede o mesmo: os títulos, os nomes e as letras dos temas, os números de palavras, as passagens, as expressões e os
  capítulos que o enunciado de antes citava, cada pedido do enunciado de antes (com as mesmas palavras), o dossiê e a pergunta
  opcional, e os critérios, níveis, exemplos e pontos da grelha, iguais aos de antes da camada (a base do manifesto, o main e2e73379),
  salvo os exemplos que usavam passagens dos textos da tarefa (revisão de 13/11/2026: EXEMPLOS_TROCADOS, conferidos um a um).
  Uma só mudança, decidida pelo docente: o tema B da m5-u2 tem 100 a 150 palavras (o enunciado de antes dizia «100 a 150 no tema»
  em cima e «100 a 130» no tema B);
* os textos para análise são os das lições do M5, letra a letra, na grafia das lições: cada parágrafo da página é um parágrafo de um
  cartão «O texto» (o mesmo número, as mesmas palavras, os mesmos itálicos), com o vocabulário e a linha de fonte da lição; a página
  mostra-os inteiros e pela ordem, junto da pergunta ou do tema que os usa; o que as lições não dão não se copiou de fora, e a linha
  de fonte de cada texto di-lo; não há imagens;
* as decisões do docente, em todos os sítios: tempos 10/10/55/15 (quadro, relógios, guia), nenhum «5 min» nem «60 min» antigos nas
  páginas do M5 ligadas à tarefa; «com consulta» dito uma vez, no primeiro cartão; a autoavaliação da grelha não se entrega
  (enunciado, grelha e correção); o aquecimento com uma só ligação; no máximo 10 perguntas de sim ou não na verificação; as mesmas
  palavras no enunciado, na grelha, na correção, no aquecimento, no guia, no índice e no mapa;
* no guia da tarefa do M5 saem a «Autoavaliação» que se copiava para o Teams e «pergunta ao teu par de trabalho» (a regra passa a
  chamar-se «Dois antes de mim»), e o resto do guia é o do main de partida, letra a letra, salvo as trocas da camada;
* nos portefólios do M5 e do M3 saem a autoavaliação de 0 a 20 por parâmetro e «trabalho de equipa», sem nada no lugar; o resto de
  cada página é o do main de partida, letra a letra;
* no tema B da m3-u2, a página diz que os argumentos de IV, 94 e 95 chegam, em vez de remeter para o manual;
* as regras do texto: sem as palavras proibidas, sem «·» nem «—» nas nossas frases (nos textos de Camilo e de Eça ficam como no
  original), «Que + nome» ou «Qual das…», referências que não se partem, títulos de obras em itálico, exemplos com outro caso;
* o contrato da página, que substitui o de tests/test_task_choice.py nestas duas tarefas: seis cartões com nome, dois temas, uma
  pergunta opcional com três opções, os dois relógios, os factos do dossiê com fonte e ligação que existe, as citações e os
  números de cada facto na lição para onde aponta, os nomes das secções tal como estão nas lições ligadas;
* as tarefas, grelhas, correções e aquecimentos dos outros módulos são os do main de partida, byte a byte (salvo a frase do tema B
  da m3-u2), e saem iguais dos geradores;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base, gerador que dá o mesmo JSON, registada na
  auditoria (desfazer), em scripts/desligar_sala.py, na leitura histórica dos enunciados e nas cadeias e caminhos dos fluxos.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em
tests/browser_tarefas_faceis_m5.py."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
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
sys.path.insert(0, str(ROOT / 'scripts'))
from auditoria_20261028 import undo_tarefas_faceis_m5_1113, undo_tarefas_faceis_m1_1113, undo_tarefas_faceis_m3_1112, undo_tarefas_faceis_m6_1113  # noqa: E402
import verificar_camadas  # noqa: E402
# 13/11/2026: por cima de todas ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113, com o seu teste,
# tests/test_tarefas_faceis_m7.py). Este teste lê os ficheiros que essa camada muda (os dados das grelhas, os dados e as páginas das
# tarefas do M7) como estavam por baixo dela: desfeita pela auditoria, com contagem estrita. A exigência é a mesma.
from auditoria_20261028 import undo_tarefas_faceis_m7_1113  # noqa: E402
M7_DE_CIMA = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json').read_text('utf-8'))['files']

CAMADA_REL = 'scripts/tarefas_faceis_m5_20261113.json'
MANIFESTO_REL = 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
M1F = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
M3F = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
# 13/11/2026: por cima desta camada ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113, o mesmo molde), que
# se desfazem primeiro em todas as cadeias e partilham com ela um ficheiro, os dados das grelhas.
M6F = 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'
M7F = 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'  # 13/11/2026: a camada das tarefas do M7 mais fáceis de fazer, a mais recente
M6_FICHEIROS = json.loads((ROOT / M6F).read_text('utf-8'))['files']
BASE_COMMIT = 'e2e73379e75fd5dd4bc68009e63071c836333356'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
TROCAS = json.loads((ROOT / CAMADA_REL).read_text('utf-8'))
SLUGS = ('m5-u1', 'm5-u2')
N = '\xa0'
DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
DADOS_M3U2, ENUNCIADO_M3U2 = 'docs/pedagogia/tarefas-escolha/m3-u2.json', 'tarefas/m3-u2/index.html'
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DADOS_AQUECIMENTOS = [f'docs/pedagogia/aquecimentos/{s}.json' for s in SLUGS]
ENUNCIADOS = [f'tarefas/{s}/index.html' for s in SLUGS]
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'aquecimento/', 'correcao/')]
AQUECIMENTOS = [f'tarefas/{s}/aquecimento/index.html' for s in SLUGS]
GUIA, INDICE, MAPA = 'm5/guia-da-tarefa-m5/index.html', 'm5/index.html', 'm5/mapa-do-modulo-m5/index.html'
PORTEFOLIO, PORTEFOLIO_M3 = 'm5/portefolio-do-modulo-m5/index.html', 'm3/portefolio-do-modulo-m3/index.html'
FICHEIROS = (DADOS_TAREFAS + [DADOS_M3U2, GRELHAS] + DADOS_AQUECIMENTOS + PAGINAS + [ENUNCIADO_M3U2]
             + [GUIA, INDICE, MAPA, PORTEFOLIO, PORTEFOLIO_M3])
# As outras onze tarefas que saem de scripts/tarefas_escolha.py (as do M3 e as do M1 já estão no molde, pelas suas camadas).
OUTRAS = ('m1-u1', 'm1-u2', 'm3-u1', 'm3-u2', 'm6-u1', 'm6-u2', 'm7-u3', 'm8-u1', 'm8-u2', 'm9-u1', 'm9-u2')
NO_MOLDE = ('m1-u1', 'm1-u2', 'm3-u1', 'm3-u2')
CARTOES_NOMES = ['Começar', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Fechar e entregar', 'Rever a matéria']
F02, F04, F07, F08, F10, F11, F12, F13, F14 = (f'm5/licao-m5-f{n}/index.html' for n in ('02', '04', '07', '08', '10', '11', '12', '13', '14'))
# O que cada enunciado de antes pedia, com as suas palavras: cada pedaço está no enunciado de antes e continua no de agora.
PEDIDOS = {
    'm5-u1': ['uma passagem da Introdução', 'outra do capítulo IV', 'em que o narrador comenta o que conta', 'Identifica um recurso numa delas.',
              'Explica o efeito de cada passagem em quem lê.', '«Não te posso dar minha filha, porque já não tenho filha.»', 'de «te»',
              '«minha filha»', 'um teste para cada função', 'o que a frase mostra', 'lugar de Teresa na visão do pai',
              'Imagina a carta que Simão escreveria a Teresa, na nau, depois da morte dela.',
              'Escreve 90 a 120 palavras, com local, data, vocativo, despedida e assinatura.', 'Responde a uma pergunta de Teresa',
              'uma memória dos dois', 'um recurso expressivo teu', 'uma expressão do romance entre «»', 'Depois da carta, escreve duas frases:',
              'que facto do romance respeitaste', 'que efeito produz o teu recurso expressivo.',
              'Escreve o painel de entrada da antiga Cadeia da Relação, hoje Centro Português de Fotografia, para quem nunca leu o romance.',
              '70 a 100 palavras', 'dois factos do', 'uma frase curta do romance entre «»',
              'Depois do painel, explica por que escolheste essa frase.', 'Indica o que o painel não pode afirmar sobre Camilo e Simão.'],
    'm5-u2': ['No último capítulo', "antes de Carlos dizer «é n'ella que me parece estar mettida a minha vida inteira!»",
              'uma expressão repetida do capítulo I', 'outra nova', 'a estrutura do romance que esta repetição revela',
              'mostram sobre a vida de Carlos', 'No capítulo VI', 'Alencar «supplicou que se não discutisse» o realismo;',
              "depois lê-se «Alli todos eram homens d'aceio, de sala, hein?».", 'dentifica o modo de relato', 'com duas marcas',
              'em discurso direto',
              'Imagina uma conversa séria à mesa, nos dias de hoje, interrompida por algo banal, como no Hotel Central.',
              'Narra a cena na 3.ª pessoa, em 70 a 100 palavras.', 'Inclui uma fala em discurso direto',
              'um pensamento em discurso indireto livre', 'Depois, escreve duas frases:', 'o que imitaste de Eça', 'o que criticas.',
              '«Falhámos a vida, menino!» ainda diz alguma coisa a alguém da tua idade?', 'Escreve um parágrafo de opinião de 100 a 1',
              'Começa pela tua posição', 'outra citação do último capítulo', 'explicada', 'um facto datado do', 'ligado à tua posição.',
              'Apresenta uma ideia contrária à tua', 'esponde-lhe', 'ermina com uma conclusão.'],
}
# De onde vem cada texto em prosa: (lição, número do cartão, números dos parágrafos desse cartão que entram), pela ordem.
PROSA = {
    'm5-u1': {'texto-1': [(F02, 4, (1, 2, 3)), (F02, 8, (4, 5, 6)), (F02, 14, (7,))],
              'texto-2': [(F04, 3, (1, 2, 3)), (F04, 7, (4, 5)), (F04, 11, (6, 7, 8)), (F04, 13, (9, 10, 11)), (F04, 17, (12, 13, 14)),
                          (F04, 19, (15, 16, 17)), (F04, 22, (18,))]},
    'm5-u2': {'texto-1': [(F10, 4, (1, 2))], 'texto-2': [(F10, 15, (1, 2, 3))], 'texto-3': [(F11, 3, (1,))],
              # 13/11/2026 (revisão): o Texto 4 começa pela marca «[2] […]» da lição F11, para se ver que as lições saltam uma parte
              # do capítulo entre o Texto 3 e o Texto 4 (a mesma exigência, com mais um parágrafo conferido contra a lição).
              'texto-4': [(F11, 3, (2, 3)), (F11, 8, (4, 5, 6)), (F11, 10, (7, 8, 9))],
              'texto-5': [(F13, 3, (1, 2, 3)), (F13, 8, (4, 5, 6)), (F13, 11, (7, 8, 9)), (F13, 14, (10, 11, 12)), (F13, 16, (13,))]},
}
PALAVRAS_PROSA = {'m5-u1': {'texto-1': 357, 'texto-2': 685, 'texto-3': 23},
                  'm5-u2': {'texto-1': 361, 'texto-2': 83, 'texto-3': 65, 'texto-4': 240, 'texto-5': 439}}
# Os parágrafos que trazem itálicos da lição (o assento que Camilo transcreve; as palavras estrangeiras e os destaques de Eça).
ITALICOS = {'m5-u1': {'texto-1': ['[2]', '[3]', '[4]'], 'texto-2': [], 'texto-3': []},
            'm5-u2': {'texto-1': ['[1]', '[2]'], 'texto-2': [], 'texto-3': ['[1]'], 'texto-4': ['[8]', '[9]'], 'texto-5': ['[2]', '[3]', '[6]']}}
# O cartão que traz o vocabulário e a linha de fonte de cada texto, e a fatia do vocabulário que cabe ao texto (None: todo).
VOCABULARIO = {
    'm5-u1': {'texto-1': (F02, 14, None), 'texto-2': (F04, 22, None)},
    'm5-u2': {'texto-1': (F10, 4, None), 'texto-2': (F10, 19, ()), 'texto-3': (F11, 21, (0, 4)), 'texto-4': (F11, 21, (4, 10)),
              'texto-5': (F13, 16, None)},
}
LONGOS = {'m5-u1': ['texto-1', 'texto-2'], 'm5-u2': ['texto-1', 'texto-4', 'texto-5']}
TITULOS = {
    'm5-u1': ['Amor de Perdição, Introdução, de Camilo Castelo Branco',
              'Amor de Perdição, capítulo IV (do início à fala de Tadeu ao sobrinho), de Camilo Castelo Branco',
              'As perguntas de Teresa a Simão, como estão na lição F08'],
    'm5-u2': ['Os Maias, capítulo I (o Ramalhete, no início), de Eça de Queirós', 'Os Maias, último capítulo (o Ramalhete, no fim), de Eça de Queirós',
              'Os Maias, capítulo VI (Alencar e o realismo, ao jantar), de Eça de Queirós',
              'Os Maias, capítulo VI (a discussão à mesa e a interrupção), de Eça de Queirós',
              'Os Maias, último capítulo (o balanço final), de Eça de Queirós'],
}
# O que a página junta à linha de fonte da lição: diz o que as lições não dão (nada se copiou de fora).
FONTE_MAIS = {
    ('m5-u1', 'texto-1'): ' São os sete parágrafos que as lições dão; a Introdução tem mais um, no fim.',
    # 13/11/2026 (revisão): a lição F04 corta o capítulo IV a meio do parágrafo [2] da edição e em [3]; a lição F11 salta mais do
    # que um parágrafo da edição em «[2] […]». As linhas de fonte dizem-no assim (antes diziam «Em [3]» e «o parágrafo [2]»).
    ('m5-u1', 'texto-2'): ' No fim de [2] e em [3], as lições saltam uma parte do capítulo.',
    ('m5-u2', 'texto-4'): ' Vem depois do Texto 3. Em [2], as lições saltam uma parte do capítulo.',
}
# 13/11/2026 (revisão): com os textos inteiros na página, estes exemplos da grelha usavam passagens dos textos da tarefa (o capítulo IV
# de Amor de Perdição e o balanço final de Os Maias). A regra do docente é «exemplos sempre com outro caso, sem as passagens da
# tarefa»: passam a usar frases que as lições dão e que não estão nos textos da tarefa. São as únicas diferenças nos textos das duas
# grelhas, conferidas uma a uma (antes, depois); os critérios, os níveis e os pontos ficam iguais. Nos dados da grelha, «cap. IV»
# leva espaço que não quebra.
EXEMPLOS_TROCADOS = {
    'm5-u1': [
        ('Em «Teu primo é um composto de todas as virtudes», virtudes é o sujeito, porque é a palavra mais importante.',
         'Em «Domingos Botelho era extremamente feio», feio é o sujeito, porque é a palavra mais importante.'),
        ('Em «Teu primo é um composto de todas as virtudes», «Teu primo» é o sujeito e «um composto de todas as virtudes» é predicativo do sujeito.',
         'Em «Domingos Botelho era extremamente feio», «Domingos Botelho» é o sujeito e «extremamente feio» é predicativo do sujeito.'),
        ('Em «Teu primo é um composto de todas as virtudes» (cap.\xa0IV), «Teu primo» é o sujeito: responde à pergunta _quem é um composto de todas '
         'as virtudes?_, e o verbo concorda com ele. A expressão «um composto de todas as virtudes» é predicativo do sujeito: com _ser_, diz como é '
         'o sujeito, e a frase não se aguenta sem ele. O sujeito é Baltasar e o predicativo é só elogio: Tadeu vende o noivo à filha.',
         'Em «Domingos Botelho era extremamente feio» (lição F07), «Domingos Botelho» é o sujeito: responde à pergunta _quem era extremamente '
         'feio?_, e o verbo concorda com ele. A expressão «extremamente feio» é predicativo do sujeito: com _ser_, diz como é o sujeito, e a frase '
         'não se aguenta sem ele. O predicativo é um juízo sobre a personagem: a frase apresenta-a pelo aspeto, sem a poupar.'),
        ('A (uma carta inventada de Tadeu à filha, no convento): Teresa, espero que estejas bem.',
         'A (uma carta inventada da mãe de Simão ao filho): Meu filho, espero que estejas bem.'),
        ('A: Na casa de meus avós, dia de Natal. Teresa: o teu primo ainda espera por ti. Que Deus te guarde. Teu pai. (As marcas',
         'A: Em casa, dia de Natal. Meu filho: aqui está tudo como deixaste. Deus te guarde. Tua mãe. (As marcas'),
        ('A, noutra voz (uma carta inventada de Tadeu à filha, no convento): Na casa de meus avós, dia de Natal. Teresa: perguntas-me se ainda tens '
         'pai. Tens, e és tu que o recusas. Lembras-te da manhã de domingo em que te chamei para a missa? Já então te disse que «a violencia de um '
         'pae é sempre amor». A tua teimosia é um muro alto entre nós. Que Deus te dê juízo. Teu pai, Tadeu de Albuquerque. Respeitei o romance: '
         'Teresa está no convento com que o pai a ameaçou, e ele não se desdiz. A metáfora do muro mostra que Tadeu põe a culpa na filha.',
         'A, noutra voz (uma carta inventada da mãe de Simão ao filho): Em casa, dia de Natal. Meu filho: hás de perguntar se a tua mãe ainda pensa '
         'em ti. Pensa, todos os dias. Lembras-te das cartas que te escrevi? Foram tantas, e eu «não recebia resposta». O teu silêncio é uma porta '
         'fechada. Deus te guarde. Tua mãe. Respeitei o romance: a mãe escrevia a Simão e pensava que o filho não respondia. A metáfora da porta '
         'fechada mostra que a mãe se sente posta de fora.'),
        ('Num romance dele, uma filha ameaçada pelo pai responde assim: «Thereza ergueu-se sem lagrimas, e entrou serenamente no seu quarto.» '
         'Escolhi a frase porque quem visita uma casa entra em quartos.',
         'Num romance dele, uma rapariga despede-se assim de quem ama: «Simão, adeus até à eternidade!» Escolhi a frase porque quem sai de uma '
         'casa também se despede.'),
        # (o exemplo do nível 0 do rigor já não aponta para uma carta que a grelha deixou de mostrar)
        ('Na carta inventada de Tadeu, Teresa já casou com o primo.', 'Numa carta inventada de Tadeu, Teresa já casou com o primo.'),
    ],
    'm5-u2': [
        ("Em «Então Ega perguntou, do fundo do sofá onde se enterrára, se, n'esses ultimos annos, elle não tivera a idéa», há discurso direto.",
         'Em «Simão disse que estava ali», há discurso direto.'),
        ("Em «Então Ega perguntou, do fundo do sofá onde se enterrára, se, n'esses ultimos annos, elle não tivera a idéa», há discurso indireto, "
         'porque está na terceira pessoa.', 'Em «Simão disse que estava ali», há discurso indireto, porque está na terceira pessoa.'),
        ("Em «Então Ega perguntou, do fundo do sofá onde se enterrára, se, n'esses ultimos annos, elle não tivera a idéa» (último capítulo), o "
         'relato é indireto: há um verbo declarativo, _perguntou_, e uma oração subordinada com _se_. Em discurso direto, Ega diria, depois de um '
         'travessão: _Nestes últimos anos, não tiveste a ideia, o vago desejo de voltar para Portugal?_ Ega fala com Carlos: _elle_ passa a _tu_ e '
         '_tivera_ passa a _tiveste_.',
         'Em «Simão disse que estava ali» (um exemplo inventado da lição F12), o relato é indireto: há um verbo declarativo, _disse_, e uma oração '
         'subordinada com _que_. Em discurso direto, Simão diria, depois de um travessão: _Estou aqui._ Quem fala é o próprio Simão, no momento e '
         'no lugar da fala: _estava_ passa a _estou_ e _ali_ passa a _aqui_.'),
        ('(uma cantiga de Mendinho, uma pergunta de Ega, uma cena noutro espaço', '(uma cantiga de Mendinho, uma fala relatada de Simão, uma cena noutro espaço'),
    ],
}
# De onde vem cada citação nova dos exemplos: (lição, citação), letra a letra na lição e fora dos textos da tarefa.
EXEMPLOS_DAS_LICOES = {
    'm5-u1': [('m5/licao-m5-f07/index.html', 'Domingos Botelho era extremamente feio'), ('m5/licao-m5-f07/index.html', 'Simão, adeus até à eternidade!'),
              ('m5/licao-m5-f17/index.html', 'Escrevia a mãe a Simão, e não recebia resposta. Pensava ela que o filho não respondia')],
    'm5-u2': [('m5/licao-m5-f12/index.html', 'Simão disse que estava ali'), ('m5/licao-m5-f12/index.html', 'Simão diz «Estou aqui»'),
              ('m1/licao-m1-f02/index.html', "Eu atendendo meu amig', eu a[tendendo]")],
}
TROCAS_COMUNS = [
    ['Núcleo comum (duas respostas) e um tema à escolha (A ou B)', 'Duas perguntas e um tema à escolha (A ou B)'],
    ['Respostas articuladas', 'Respostas ligadas'], ['o tema no topo', 'a letra do tema no topo'],
    ['o tema escolhido está no topo', 'a letra do teu tema está no topo'],
    ['Não escrever no topo o tema escolhido (A ou B).', 'Não escrever no topo a letra do teu tema (A ou B).'],
    ['Fecho: ', 'Duas linhas finais: '], ['Fecho, noutra obra: ', 'Duas linhas finais, noutra obra: '],
    ['Fecho genérico, sem passagem.', 'Duas linhas finais genéricas, sem passagem.']]
TROCAS_U1 = [
    ['e o que quer de quem lê', 'e o efeito em quem lê'], ['só explicas o que o narrador quer numa delas', 'só explicas o efeito numa delas'],
    ['explicas, para cada passagem, o que o narrador quer provocar em quem lê', 'explicas o efeito de cada passagem em quem lê'],
    ['o recurso e o eco.)', 'o recurso e a expressão do romance.)'], ['um eco do romance, entre «»', 'uma expressão do romance, entre «»']]


def ler(rel):
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    if rel in M7_DE_CIMA:  # 13/11/2026: como estava por baixo da camada do M7
        texto = undo_tarefas_faceis_m7_1113(rel, texto)
    # 13/11/2026: os dados das grelhas levam agora por cima a camada das tarefas do M6 (duas chaves novas nas grelhas do M6 e cinco
    # exemplos da grelha da m6-u2). Este teste lê-os como a camada do M5 os deixou: com a do M6 desfeita pela auditoria, com contagem
    # estrita. Nos outros dezanove ficheiros a árvore é o «after» desta camada, como antes.
    if rel == GRELHAS:
        texto = undo_tarefas_faceis_m6_1113(rel, texto)
    return texto


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def antes(rel):
    """O ficheiro como estava por baixo desta camada (desfeita pelo manifesto, com contagem estrita): o main de partida."""
    texto = ler(rel)
    for e in reversed(MANIFESTO['files'].get(rel, {}).get('edits', [])):
        assert texto.count(e['new']) == e['occurrences'], (rel, e['location'])
        texto = texto.replace(e['new'], e['old'])
    return texto


def do_main(rel):
    """O ficheiro no commit de partida, ou None num clone raso que não o tenha."""
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    return r.stdout.decode('utf-8') if r.returncode == 0 else None


def visivel(fonte, so_main=True, sem_nav=True):
    """O texto que se lê numa página: sem scripts, estilos nem etiquetas, com os espaços normais juntos (U+00A0 fica)."""
    if so_main and '<main' in fonte:
        fonte = fonte[fonte.index('<main'):fonte.index('</main>')]
    fonte = re.sub(r'<(script|style)\b.*?</\1>', ' ', fonte, flags=re.S)
    if sem_nav:
        fonte = re.sub(r'<nav\b.*?</nav>', ' ', fonte, flags=re.S)
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fonte))).strip()


def sem_textos(fonte):
    """A página sem os parágrafos dos textos de Camilo e de Eça (só eles: o título, o vocabulário e a fonte de cada texto ficam)."""
    return re.sub(r'<div class="tt-prosa">.*?</div>', ' ', fonte, flags=re.S)


def solto(texto):
    return texto.replace(N, ' ')


def sem_marcas(texto):
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', texto)))


def cartoes(rel):
    """Os cartões de uma lição (CARTOES=[…], numa só linha do ficheiro)."""
    fonte = ler(rel)
    i = fonte.index('CARTOES=[')
    return json.JSONDecoder().raw_decode(fonte[i + 8:])[0]


def paragrafos_do_cartao(c):
    """Os parágrafos numerados de um cartão «O texto» em prosa: {número: (com os itálicos da lição, sem marcas)}. As palavras do
    vocabulário vêm marcadas na lição (<b class="gt" data-s="…">): a marca sai, a palavra fica."""
    out = {}
    for n, corpo in re.findall(r'<p class="pr" data-l="[\d-]+"><b>\[(\d+)\]</b> (.*?)</p>', c['html'], re.S):
        com_i = re.sub(r'<b class="gt" data-s="[^"]*">(.*?)</b>', r'\1', corpo)
        assert not re.search(r'<(?!/?i>)', com_i), com_i
        out[int(n)] = (com_i, html.unescape(re.sub(r'</?i>', '', com_i)))
    return out


def vocabulario_do_cartao(c):
    """Os pares (palavra, sentido) da lista «Vocabulário» de um cartão; _palavra_ é itálico na lição."""
    g = re.search(r'<p class="gl"><b>Vocabulário:</b> (.*?)</p>', c['html'], re.S).group(1)
    pares = [list(re.fullmatch(r'<b>(.*)</b>, (.*?)', item, re.S).groups()) for item in g.split('; ')]
    return [[re.sub(r'_([^_]+)_', r'<i>\1</i>', p), s] for p, s in pares]


def fonte_do_cartao(c):
    return re.sub(r'_([^_]+)_', r'<i>\1</i>', re.search(r'<p class="fonte">(.*?)</p>', c['html'], re.S).group(1))


def palavras(texto):
    return re.findall(r"[0-9A-Za-zÀ-ÿ]+(?:[-'][0-9A-Za-zÀ-ÿ]+)*", texto)


class Pagina(HTMLParser):
    """A estrutura de uma página de tarefa: os filhos de <main>, os temas, as perguntas com opções e as ligações."""

    def __init__(self, fonte):
        super().__init__()
        self.pilha, self.raiz, self.ids, self.ligacoes, self.temas, self.perguntas, self.opcoes = [], [], [], [], [], [], []
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.pilha and self.pilha[-1][0] == 'main':
            self.raiz.append((tag, a.get('id'), a.get('data-task-card-name')))
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a':
            self.ligacoes.append(a.get('href', ''))
        if 'data-task-theme' in a:
            self.temas.append(a['data-task-theme'])
        if 'data-task-question' in a:
            self.perguntas.append((a['data-task-question'], any(x[0] == 'details' for x in self.pilha)))
        if tag == 'button' and 'data-response' in a:
            self.opcoes.append(a)
        if tag not in ('meta', 'link', 'br', 'img', 'input'):
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        if any(x[0] == tag for x in self.pilha):
            self.pilha = self.pilha[:max(i for i, x in enumerate(self.pilha) if x[0] == tag)]


def plana(rel):
    """Texto de uma página do sítio, sem marcas nem entidades, com os espaços juntos (como tests/test_task_choice.py)."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', ler(rel))))


def todos_os_textos(f):
    return [i for p in f['perguntas'] for i in p['textos']] + [i for t in f['temas'] for i in t['material'].get('textos', [])]


def todos_os_exemplos(f):
    return [x for p in f['perguntas'] for x in p['exemplos']] + [x for t in f['temas'] for x in t['material'].get('exemplos', [])]


class TarefasFaceisM5(unittest.TestCase):
    maxDiff = None

    # ---------- a tarefa pede o mesmo ----------

    def test_a_tarefa_pede_o_mesmo(self):
        for slug in SLUGS:
            rel = f'docs/pedagogia/tarefas-escolha/{slug}.json'
            d, a = json.loads(ler(rel)), json.loads(antes(rel))
            f = d['facil']
            with self.subTest(tarefa=slug):
                # As chaves de antes ficam todas, iguais: a camada só acrescenta «facil».
                self.assertNotIn('facil', a)
                self.assertEqual({k: v for k, v in d.items() if k != 'facil'}, a)
                self.assertEqual(list(d)[-1], 'facil')
                # O título, os títulos das duas perguntas, as letras e os nomes dos dois temas.
                self.assertEqual([solto(p['titulo']) for p in f['perguntas']],
                                 [solto(re.match(r'<strong>(.*?)</strong>', n).group(1)) for n in a['nucleo']])
                self.assertEqual([(t['letra'], t['nome']) for t in f['temas']], [(t['letra'], t['nome']) for t in a['temas']])
                self.assertEqual(len(f['perguntas']), 2)
                # Os números: os do «lead» de antes, no quadro, junto de cada parte e na verificação.
                lead, quadro = solto(a['lead']), f['quadro']['linhas']
                self.assertIn('<strong>200 a 250 palavras no total</strong>', lead)
                self.assertIn('Orientação: cerca de 50 por resposta e 100 a 150 no tema, incluindo a explicação final', lead)
                self.assertEqual([solto(l[2]) for l in quadro[2:4]], ['orientação: cerca de 50', 'orientação: cerca de 50'])
                self.assertTrue(solto(quadro[4][2]).startswith('orientação: 100 a 150'), quadro[4][2])
                self.assertEqual(solto(quadro[-1][2]), '200 a 250')
                self.assertEqual([solto(p['meta']) for p in f['perguntas']], ['Orientação: cerca de 50 palavras.'] * 2)
                self.assertTrue(solto(f['temas_nota']).startswith('Orientação: 100 a 150 palavras'), f['temas_nota'])
                self.assertIn('Tenho 200 a 250 palavras?', [solto(x) for x in f['verificar']])
                # A explicação final conta para as 100 a 150 palavras do tema, como antes («incluindo a explicação final»; na
                # m5-u2, «quando pedida»: só o tema A a pede).
                if slug == 'm5-u1':
                    self.assertTrue(lead.endswith('incluindo a explicação final.'))
                    self.assertEqual(solto(quadro[4][2]), 'orientação: 100 a 150, com a explicação final')
                    self.assertEqual(solto(f['temas_nota']), 'Orientação: 100 a 150 palavras, com a explicação final.')
                else:
                    self.assertTrue(lead.endswith('incluindo a explicação final quando pedida.'))
                    self.assertEqual(solto(quadro[4][2]), 'orientação: 100 a 150')
                    self.assertEqual(solto(f['temas_nota']), 'Orientação: 100 a 150 palavras. No tema A, incluem a explicação final.')
                # Tudo o que o enunciado de antes citava entre «» ou localizava por capítulo continua pedido.
                pedido = solto(sem_marcas(json.dumps([f['perguntas'], f['temas'], f['finais']], ensure_ascii=False)))
                velho = solto(sem_marcas(' '.join(a['nucleo'] + [t['texto'] for t in a['temas']])))
                citados = re.findall(r'«([^»]+)»', velho)
                self.assertGreaterEqual(len(citados), 3)
                for citado in citados:
                    self.assertIn(f'«{citado}»', pedido, citado)
                refs = re.findall(r'cap(?:ítulo|\.) [IVXLC]+', velho)
                self.assertGreaterEqual(len(refs), 1)
                for ref in refs:
                    self.assertIn(ref, pedido, ref)
                # Cada pedido do enunciado de antes, com as mesmas palavras.
                self.assertGreaterEqual(len(PEDIDOS[slug]), 26)
                for pedaco in PEDIDOS[slug]:
                    self.assertIn(pedaco, velho, pedaco)
                    self.assertIn(pedaco, pedido, pedaco)
                # A pergunta das duas linhas finais é a de antes.
                pergunta = re.search(r'contagem: (.*?\?)', a['fecho']).group(1)
                self.assertEqual(f['finais']['passos'][0], 'Responde: ' + pergunta)
                self.assertEqual(f['finais']['passos'][1], a['fecho'].split('? ')[1])
                # O dossiê e a pergunta opcional são os de antes (a página lê-os das chaves antigas).
                self.assertEqual(d['dossie'], a['dossie'])
                self.assertEqual(d['opcional'], a['opcional'])
        # Os números de cada tema são os de antes: a carta com 90 a 120 palavras, o painel com 70 a 100, a cena com 70 a 100.
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        a1, a2 = (json.loads(antes(rel)) for rel in DADOS_TAREFAS)
        self.assertIn('Escreve 90 a 120 palavras', solto(a1['temas'][0]['texto']))
        self.assertEqual(solto(u1['temas'][0]['passos'][0]), 'Escreve 90 a 120 palavras, com local, data, vocativo, despedida e assinatura.')
        self.assertIn('O painel tem 70 a 100 palavras', solto(a1['temas'][1]['texto']))
        self.assertEqual(solto(u1['temas'][1]['passos'][0]), 'Escreve o painel em 70 a 100 palavras.')
        self.assertIn('em 70 a 100 palavras', solto(a2['temas'][0]['texto']))
        self.assertEqual(solto(u2['temas'][0]['passos'][0]), 'Narra a cena na 3.ª pessoa, em 70 a 100 palavras.')
        # Decisão do docente (13/11/2026): o tema B da m5-u2 tem 100 a 150 palavras. O enunciado de antes dizia «100 a 150 no tema»
        # em cima e «100 a 130» no tema B; agora diz 100 a 150 nos dois sítios, e «130» não aparece em parte nenhuma da página.
        self.assertIn('de 100 a 130 palavras', solto(a2['temas'][1]['texto']))
        self.assertEqual(solto(u2['temas'][1]['passos'][0]), 'Escreve um parágrafo de opinião de 100 a 150 palavras.')
        pagina = solto(visivel(sem_textos(ler(ENUNCIADOS[1]))))
        self.assertNotIn('130', pagina)
        self.assertEqual(pagina.count('100 a 150'), 3)
        # Os passos de cada tema são os cinco elementos da grelha e a explicação (ou a conclusão), pela ordem do enunciado de antes.
        self.assertEqual([len(t['passos']) for t in u1['temas']], [6, 5])
        self.assertEqual([len(t['passos']) for t in u2['temas']], [4, 7])
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        self.assertEqual(grelhas['m5-u1']['criterios'][2]['nome'], 'Tema à escolha (A ou B): cinco elementos e a explicação')
        self.assertEqual(grelhas['m5-u2']['criterios'][2]['nome'], 'Tema à escolha (A ou B): cinco elementos e a explicação ou a conclusão')

    def test_criterios_da_grelha_iguais(self):
        agora, base = json.loads(ler(GRELHAS))['tarefas'], json.loads(antes(GRELHAS))['tarefas']
        self.assertEqual(list(agora), list(base))
        for slug, t in agora.items():
            with self.subTest(grelha=slug):
                novas = {'autoavaliacao_so_tua', 'trocas_aluno'} if slug in SLUGS else set()
                self.assertEqual(set(t) - set(base[slug]), novas)
                # 13/11/2026 (revisão): nas duas grelhas do M5, as únicas diferenças são os exemplos de EXEMPLOS_TROCADOS, cada um uma
                # vez na base e uma vez agora (a exigência é a mesma: tudo o resto igual à base, letra a letra; as outras grelhas,
                # iguais sem exceção).
                esperado = json.dumps(base[slug], ensure_ascii=False)
                agora_json = json.dumps({k: v for k, v in t.items() if k not in novas}, ensure_ascii=False)
                for velho, novo in EXEMPLOS_TROCADOS.get(slug, []):
                    self.assertEqual(esperado.count(json.dumps(velho, ensure_ascii=False)[1:-1]), 1, velho[:60])
                    self.assertEqual(esperado.count(json.dumps(novo, ensure_ascii=False)[1:-1]), 0, novo[:60])
                    esperado = esperado.replace(json.dumps(velho, ensure_ascii=False)[1:-1], json.dumps(novo, ensure_ascii=False)[1:-1])
                    self.assertEqual(agora_json.count(json.dumps(novo, ensure_ascii=False)[1:-1]), 1, novo[:60])
                self.assertEqual({k: v for k, v in t.items() if k not in novas}, json.loads(esperado))
                # Os critérios, os pontos e os descritores de cada nível são os da base, sem exceção.
                self.assertEqual([(c['nome'], c['max'], {k: v[0] for k, v in c['niveis'].items()}, c.get('custa')) for c in t['criterios']],
                                 [(c['nome'], c['max'], {k: v[0] for k, v in c['niveis'].items()}, c.get('custa')) for c in base[slug]['criterios']])
                self.assertEqual(sum(c['max'] for c in t['criterios']), 20)
        for slug in SLUGS:
            t = agora[slug]
            self.assertIs(t['autoavaliacao_so_tua'], True)
            # As trocas são só as palavras que o enunciado novo trocou; cada uma ocorre nos textos da grelha.
            fonte = json.dumps({k: v for k, v in t.items() if k != 'trocas_aluno'}, ensure_ascii=False)
            for a, _ in t['trocas_aluno']:
                self.assertIn(a, fonte)
            grelha = visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False, sem_nav=False)
            self.assertNotRegex(grelha, r'\b[Ff]echo\b')
            self.assertNotRegex(visivel(ler(f'tarefas/{slug}/index.html')), r'\b[Ff]echo\b')
            self.assertEqual(grelha.count('Duas linhas finais: '), 1)
            self.assertEqual(grelha.count('Duas linhas finais, noutra obra: '), 1)
            self.assertEqual(grelha.count('Duas linhas finais genéricas, sem passagem.'), 1)
        # Nas duas, as oito trocas das palavras comuns (as cinco das grelhas do M3 e do M1 e «Duas linhas finais» nos três sítios
        # onde a grelha dizia «Fecho»); na m5-u1, mais cinco: «o efeito em quem lê» e «uma expressão do romance», como o enunciado.
        self.assertEqual(agora['m5-u2']['trocas_aluno'], TROCAS_COMUNS)
        self.assertEqual(agora['m5-u1']['trocas_aluno'], TROCAS_COMUNS + TROCAS_U1)
        self.assertEqual(agora['m5-u2']['trocas_aluno'][:5], agora['m3-u2']['trocas_aluno'][:5])

    # ---------- os textos são os das lições, letra a letra ----------

    def test_textos_em_prosa_letra_a_letra_das_licoes(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            f = json.loads(ler(rel))['facil']
            pagina = ler(enunciado)
            lidas = {}
            self.assertEqual([t['id'] for t in f['textos']], list(PALAVRAS_PROSA[slug]))
            self.assertEqual([solto(sem_marcas(t['titulo'])) for t in f['textos']], TITULOS[slug])
            self.assertEqual([solto(t['rotulo']) for t in f['textos']], [f'Texto {k}' for k in range(1, len(f['textos']) + 1)])
            for t in f['textos']:
                if t['id'] not in PROSA[slug]:
                    continue
                with self.subTest(tarefa=slug, texto=t['id']):
                    self.assertNotIn('estrofes', t)
                    # Cada parágrafo é um parágrafo de um cartão «O texto» da lição: o mesmo número, as mesmas palavras e os mesmos
                    # itálicos, pela ordem da lição, sem saltar nenhum parágrafo dos cartões de onde vem.
                    esperados = []
                    for licao, k, numeros in PROSA[slug][t['id']]:
                        c = lidas.setdefault(licao, cartoes(licao))[k - 1]
                        self.assertTrue(c['rot'].startswith('O texto'), (licao, k))
                        do_cartao = paragrafos_do_cartao(c)
                        for n in numeros:
                            esperados.append((f'[{n}]',) + do_cartao[n])
                    self.assertEqual([x['n'] for x in t['paragrafos']], [n for n, _, _ in esperados])
                    numeros = [int(x['n'][1:-1]) for x in t['paragrafos']]
                    self.assertEqual(numeros, list(range(numeros[0], numeros[0] + len(numeros))))
                    for x, (n, com_i, plano) in zip(t['paragrafos'], esperados):
                        self.assertEqual(x['t'], plano, n)
                        self.assertEqual(x['partes'], [plano], n)
                        self.assertEqual(x.get('html'), com_i if '<i>' in com_i else None, n)
                        self.assertNotRegex(x['t'], r'[“”"<>]')
                    self.assertEqual([x['n'] for x in t['paragrafos'] if 'html' in x], ITALICOS[slug][t['id']])
                    junto = ' '.join(x['t'] for x in t['paragrafos'])
                    self.assertEqual(len(palavras(junto)), PALAVRAS_PROSA[slug][t['id']])
                    # Contínuo: nenhum corte, salvo o que a lição F04 tem no capítulo IV («[3] […]»), que a linha de fonte diz.
                    # 13/11/2026 (revisão): e salvo a marca «[2] […]» da lição F11, com que o Texto 4 da m5-u2 começa.
                    if (slug, t['id']) == ('m5-u1', 'texto-2'):
                        self.assertEqual(junto.count('[…]'), 1)
                        self.assertEqual(t['paragrafos'][2], {'n': '[3]', 't': '[…]', 'partes': ['[…]']})
                    elif (slug, t['id']) == ('m5-u2', 'texto-4'):
                        self.assertEqual(junto.count('[…]'), 1)
                        self.assertEqual(t['paragrafos'][0], {'n': '[2]', 't': '[…]', 'partes': ['[…]']})
                    else:
                        self.assertNotIn('[…]', junto)
                    # O vocabulário e a linha de fonte são os da lição (o cartão que os traz), sem uma palavra a mais.
                    licao, k, fatia = VOCABULARIO[slug][t['id']]
                    c = lidas.setdefault(licao, cartoes(licao))[k - 1]
                    if fatia == ():
                        self.assertNotIn('glossario', t)
                    else:
                        da_licao = vocabulario_do_cartao(c)
                        self.assertEqual(t['glossario'], da_licao if fatia is None else da_licao[fatia[0]:fatia[1]])
                        self.assertEqual(len({p for p, _ in t['glossario']}), len(t['glossario']))
                    mais = FONTE_MAIS.get((slug, t['id']), '')
                    self.assertEqual(solto(t['fonte']), solto(fonte_do_cartao(c)).replace(' (1862) (grafia', ' (1862), Introdução (grafia') + mais)
                    self.assertIn('(grafia da edição).', t['fonte'])
                    self.assertRegex(t['origem'], r'^' + re.escape(PROSA[slug][t['id']][0][0]) + r', linha \d+, cart(?:ão|ões) [\d, ]+.*\(copiado letra a letra\)$')
                    # Na página, o texto está inteiro, pela ordem, com os parágrafos numerados como nas lições e os itálicos.
                    bloco = re.search(r'<section class="tt-texto[^"]*" id="' + t['id'] + r'".*?</section>', pagina, re.S).group(0)
                    self.assertEqual(re.findall(r'<p class="tt-par"><span class="tt-pn">(\[\d+\])</span> (.*?)</p>', bloco),
                                     [(n, com_i) for n, com_i, _ in esperados])
                    self.assertEqual(bloco.count('<div class="tt-prosa">'), 1)
                    for palavra, sentido in t.get('glossario', []):
                        self.assertIn(f'<li><b>{palavra}</b>: {sentido}</li>', bloco)
                    self.assertEqual(bloco.count('<li>'), len(t.get('glossario', [])))
                    self.assertIn(f'<p class="tt-fonte">{t["fonte"]}</p>', bloco)
                    self.assertEqual(pagina.count(f'id="{t["id"]}"'), 1)
                    # Um texto comprido pode passar de uma página em papel (parte-se só entre parágrafos); os curtos saem inteiros.
                    self.assertEqual(bool(t.get('longo')), t['id'] in LONGOS[slug])
                    self.assertTrue(bloco.startswith(f'<section class="tt-texto {"tt-longo" if t["id"] in LONGOS[slug] else "tt-curto"}" id='))
            # Nenhum texto ficou remetido para o manual, nada veio de fora das lições e não há imagens.
            self.assertNotRegex(visivel(pagina), r'(?i)\bmanual\b|Onde está o texto')
            self.assertNotIn('class="tt-onde"', pagina)
            for fora in ('gutenberg', 'wikisource', 'archive.org', '<figure', '<img ', 'data:image'):
                self.assertNotIn(fora, pagina)
        # m5-u1: a Introdução e o capítulo IV na pergunta 1, e as perguntas de Teresa só no tema A.
        # 13/11/2026 (revisão): a pergunta 1 pede uma passagem da Introdução e outra do capítulo IV, por isso os dois textos ficam no
        # cartão da pergunta 1 (antes, o capítulo IV estava no cartão da pergunta 2 e a ligação levava a outro cartão, sem regresso);
        # a pergunta 2 só usa a fala de Tadeu (parágrafo [18]), que o próprio pedido cita inteira, e diz onde está o Texto 2.
        f = json.loads(ler(DADOS_TAREFAS[0]))['facil']
        self.assertEqual([p['textos'] for p in f['perguntas']], [['texto-1', 'texto-2'], []])
        self.assertEqual(solto(f['perguntas'][1]['intro']), 'No <a href="#texto-2">Texto 2</a> (na pergunta 1, parágrafo [18]), Tadeu diz ao sobrinho: '
                         '«Não te posso dar minha filha, porque já não tenho filha.»')
        self.assertEqual(solto(f['perguntas'][0]['escolhas'][1]), 'outra do capítulo IV (<a href="#texto-2">Texto 2</a>).')
        self.assertEqual([solto(x) for x in f['temas'][1]['antes']],
                         ['A frase do romance pode vir do <a href="#texto-1">Texto 1</a> ou do <a href="#texto-2">Texto 2</a> (os dois na pergunta 1).'])
        pagina_u1 = ler(ENUNCIADOS[0])
        cartao_1 = pagina_u1[pagina_u1.index('<section class="task-section tf-pergunta" id="produzir" data-task-card-name="Pergunta 1"'):pagina_u1.index('<section class="task-section tf-pergunta" id="pergunta-2"')]
        cartao_2 = pagina_u1[pagina_u1.index('<section class="task-section tf-pergunta" id="pergunta-2"'):pagina_u1.index('<section class="task-section tf-tema"')]
        self.assertEqual(re.findall(r'<section class="tt-texto[^"]*" id="(texto-\d)"', cartao_1), ['texto-1', 'texto-2'])
        self.assertNotIn('class="tt-texto', cartao_2)
        self.assertNotIn('na pergunta 2', solto(visivel(pagina_u1)))
        self.assertEqual([t['material'].get('textos', []) for t in f['temas']], [['texto-3'], []])
        self.assertEqual(sorted(todos_os_textos(f)), ['texto-1', 'texto-2', 'texto-3'])
        capitulo = f['textos'][1]['paragrafos']
        self.assertEqual(capitulo[-1]['n'], '[18]')
        self.assertTrue(capitulo[-1]['t'].startswith('— Não te posso dar minha filha, porque já não tenho filha.'))
        self.assertTrue(capitulo[-2]['t'].endswith('Thadeu de Albuquerque foi encontrar seu sobrinho, e disse-lhe:'))
        self.assertTrue(capitulo[0]['t'].startswith('O coração de Thereza estava mentindo.'))
        self.assertTrue(f['textos'][0]['paragrafos'][0]['t'].startswith('Folheando os livros de antigos assentamentos'))
        self.assertTrue(f['textos'][0]['paragrafos'][-1]['t'].endswith('dormir de innocentes desejos?!'))
        # As três perguntas de Teresa, os factos e as marcas de uma carta são os da lição F08 («Para entender»), letra a letra.
        recorda = cartoes(F08)[2]
        self.assertEqual(recorda['rot'], 'Para entender')
        perguntas = re.findall(r'<li>(.*?)</li>', re.search(r'<p><b>As perguntas de Teresa:</b></p><ul>(.*?)</ul>', recorda['html']).group(1))
        self.assertEqual(perguntas, ['Podias tu com a desesperança e com a vida?', 'Que farias da vida sem a tua companheira?', 'Nunca hás de amar outra vez?'])
        self.assertEqual(f['textos'][2]['paragrafos'], [{'n': f'[{k}]', 't': p, 'partes': [p]} for k, p in enumerate(perguntas, 1)])
        self.assertNotIn('glossario', f['textos'][2])
        self.assertEqual(solto(f['textos'][2]['fonte']), 'Lição F08, «Para entender». As perguntas são da última carta de Teresa (<i>Amor de Perdição</i>, '
                         'Conclusão). A lição dá-as em português atual, e não na grafia da edição.')
        self.assertIn('Camilo Castelo Branco, _Amor de Perdição_, 1862 · Conclusão', ler('m5/camilo-carta/index.html'))
        factos = re.findall(r'<li>(.*?)</li>', re.search(r'<p><b>Os factos:</b></p><ul>(.*?)</ul>', recorda['html']).group(1))
        marcas = re.search(r'<p><b>As marcas de uma carta:</b> (.*?)</p>', recorda['html']).group(1)
        self.assertEqual(len(factos), 4)
        self.assertEqual(f['temas'][0]['material']['notas'], [f'<b>Os factos, como estão na lição{N}F08:</b> ' + ' '.join(factos),
                                                              f'<b>As marcas de uma carta, como estão na lição{N}F08:</b> ' + marcas])
        pagina = ler(ENUNCIADOS[0])
        dentro = pagina[pagina.index(f'<summary>Só para o tema{N}A: o Texto{N}3 e os factos</summary>'):]
        dentro = dentro[:dentro.index('</details>')]
        self.assertEqual(re.findall(r'<section class="tt-texto tt-curto" id="(texto-\d)"', dentro), ['texto-3'])
        for nota in f['temas'][0]['material']['notas']:
            self.assertEqual(dentro.count(f'<p class="tf-p">{nota}</p>'), 1)
        # m5-u2: o Ramalhete (início e fim) na pergunta 1, o parágrafo de Alencar na pergunta 2, a discussão e a interrupção só no
        # tema A e o balanço final só no tema B.
        f = json.loads(ler(DADOS_TAREFAS[1]))['facil']
        self.assertEqual([p['textos'] for p in f['perguntas']], [['texto-1', 'texto-2'], ['texto-3']])
        self.assertEqual([t['material'].get('textos', []) for t in f['temas']], [['texto-4'], ['texto-5']])
        self.assertEqual(sorted(todos_os_textos(f)), ['texto-1', 'texto-2', 'texto-3', 'texto-4', 'texto-5'])
        textos = {t['id']: ' '.join(x['t'] for x in t['paragrafos']) for t in f['textos']}
        # As passagens que o enunciado cita estão nos textos, letra a letra, cada uma uma vez.
        self.assertEqual(textos['texto-2'].count("é n'ella que me parece estar mettida a minha vida inteira!"), 1)
        self.assertEqual(textos['texto-3'].count('supplicou que se não discutisse'), 1)
        self.assertEqual(textos['texto-3'].count("Alli todos eram homens d'aceio, de sala, hein?"), 1)
        self.assertLess(textos['texto-3'].index('supplicou que se não discutisse'), textos['texto-3'].index('Alli todos eram homens'))
        self.assertEqual(textos['texto-5'].count('Falhámos a vida, menino!'), 1)
        self.assertEqual(textos['texto-4'].count('Sole normande'), 1)
        # 13/11/2026 (revisão): com a marca «[2] […]» da lição no início.
        self.assertEqual([x['n'] for x in f['textos'][3]['paragrafos']], [f'[{k}]' for k in range(2, 10)])
        # 13/11/2026 (revisão): o Texto 5 é só o balanço final, e a página não diz que traz «o resto do último capítulo».
        self.assertEqual([solto(x) for x in f['temas'][1]['antes']],
                         ['A frase de Ega e o passo do último capítulo em que ela aparece estão no <a href="#texto-5">Texto 5</a>.'])
        self.assertNotIn('o resto do último capítulo', solto(visivel(ler(ENUNCIADOS[1]))))
        self.assertTrue(textos['texto-1'].startswith('A casa que os Maias vieram habitar em Lisboa, no outono de 1875'))
        self.assertTrue(textos['texto-1'].endswith('E o Ramalhete continuou deshabitado.'))
        # O Texto 2 (o olhar final ao Ramalhete) faz parte do balanço final (Texto 5), como no romance.
        for x in f['textos'][1]['paragrafos']:
            self.assertEqual(textos['texto-5'].count(x['t']), 1, x['n'])
        # As duas palavras do vocabulário da lição F11 que ficam de fora são de parágrafos que a página não traz.
        for palavra, _ in vocabulario_do_cartao(cartoes(F11)[20])[10:]:
            self.assertNotIn(palavra, textos['texto-3'] + textos['texto-4'])
        pagina = ler(ENUNCIADOS[1])
        for tema, ids in (('A', ['texto-4']), ('B', ['texto-5'])):
            artigo = pagina[pagina.index(f'<article class="task-theme" data-task-theme="{tema}"'):]
            artigo = artigo[:artigo.index('</article>')]
            self.assertEqual(re.findall(r'<section class="tt-texto tt-longo" id="(texto-\d)"', artigo), ids)

    def test_exemplos_com_outro_caso(self):
        # Os exemplos mostram como se faz com outro caso: vêm da grelha pública e nunca usam as passagens reservadas da tarefa (a
        # lista «reservadas» do aquecimento).
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in SLUGS:
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            f = d['facil']
            reservadas = json.loads(ler(f'docs/pedagogia/aquecimentos/{slug}.json'))['reservadas']
            self.assertGreater(len(reservadas), 30)
            # (dentro de uma citação «…», a grelha usa aspas curvas; na página, as falas ficam todas entre «»)
            publico = solto(json.dumps(grelhas[slug], ensure_ascii=False)).replace('“', '«').replace('”', '»')
            exemplos = todos_os_exemplos(f)
            self.assertEqual(len(exemplos), 4)
            self.assertEqual([len(p['exemplos']) for p in f['perguntas']] + [len(t['material']['exemplos']) for t in f['temas']], [1, 1, 1, 1])
            for x in exemplos:
                self.assertNotIn('html', x)
                self.assertNotIn('de', x)
                for r in reservadas:
                    self.assertNotIn(r, solto(sem_marcas(x['titulo'])), x['titulo'])
                for p in x['paragrafos']:
                    texto = p if isinstance(p, str) else p['t']
                    with self.subTest(tarefa=slug, exemplo=texto[:50]):
                        # 13/11/2026 (revisão): sem exceções (antes, o exemplo das funções sintáticas usava outra frase do capítulo IV
                        # e passava com uma exceção para «Baltasar»; agora usa uma frase da lição F07 que não está nos textos).
                        for r in reservadas:
                            self.assertNotIn(r, solto(texto))
                        # «Passo» e «Alínea» ficam presos ao número ou à letra (U+00A0), como as outras referências.
                        if isinstance(p, dict):
                            self.assertRegex(p['al'], rf'^(?:Passos?|Alíneas?){N}')
                            self.assertNotRegex(p['al'], r'(?:Passos?|Alíneas?) |\d (?:a|e) \d|\) (?:a|e) [a-h]\)')
                        self.assertIn(solto(re.sub(r'</?i>', '_', texto)), publico)
            pagina = ler(f'tarefas/{slug}/index.html')
            # Em desdobrável fechado no ecrã, que não sai em papel.
            self.assertEqual(pagina.count('<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>'), 4)
            self.assertEqual(pagina.count('<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>Ver um exemplo com outro caso</summary>'), 4)
            self.assertNotRegex(pagina, r'<details[^>]* open')
            # Nenhum exemplo usa as passagens que a tarefa cita.
            dentro = ' '.join(re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra">.*?</details>', pagina, re.S))
            for passagem in ('Não te posso dar', 'supplicou', 'Alli todos', 'mettida a minha vida', 'Falhámos a vida', 'Sole normande'):
                self.assertNotIn(passagem, dentro)
            # 13/11/2026 (revisão): nenhuma citação de um exemplo ocorre nos textos da página (os textos da tarefa), nem inteira nem
            # nas suas frases; e nenhuma sequência de quatro palavras seguidas de um exemplo vem de um texto da tarefa. O mesmo vale
            # para os exemplos da grelha do aluno, que são os mesmos.
            blocos = re.findall(r'<section class="tt-texto[^"]*" id="texto-\d".*?</section>', pagina, re.S)
            self.assertEqual(len(blocos), len(f['textos']))
            textos_da_pagina = ' '.join(sem_marcas(x) for b in blocos for x in re.findall(r'<p class="tt-par">.*?</p>', b, re.S))
            textos_da_pagina = re.sub(r'\s+', ' ', solto(textos_da_pagina))
            self.assertGreater(len(textos_da_pagina), 3000)
            grelha_aluno = solto(sem_marcas(ler(f'tarefas/{slug}/grelha/index.html')))
            exemplos_da_grelha = ' '.join(solto(v[1]) for c in grelhas[slug]['criterios'][1:3] for v in c['niveis'].values())
            # (uma só exceção, só na grelha, que já vinha do main: o exemplo do tema A da m5-u2 diz o nome do gesto que o próprio
            # tema manda imitar, «Sole normande?»; o desdobrável do enunciado não o traz, como se confere acima)
            da_grelha = [c for c in re.findall(r'«([^«»]+)»', exemplos_da_grelha) if (slug, c) != ('m5-u2', 'Sole normande?')]
            citacoes = re.findall(r'«([^«»]+)»', solto(sem_marcas(dentro))) + da_grelha
            self.assertGreaterEqual(len(citacoes), 6)
            for citacao in citacoes:
                with self.subTest(tarefa=slug, citacao=citacao[:50]):
                    for pedaco in [citacao] + [x.strip() for x in re.split(r'[.;:!?…]', citacao)]:
                        if len(pedaco.split()) >= 2:
                            self.assertNotIn(pedaco.casefold(), textos_da_pagina.casefold())
            palavras_ex = re.findall(r"[\w'’-]+", solto(sem_marcas(dentro)) + ' ' + exemplos_da_grelha)
            juntas = ' ' + ' '.join(re.findall(r"[\w'’-]+", textos_da_pagina)).casefold() + ' '
            for k in range(len(palavras_ex) - 3):
                quatro = ' '.join(palavras_ex[k:k + 4]).casefold()
                self.assertNotIn(' ' + quatro + ' ', juntas, quatro)
            # As citações novas estão nas lições, letra a letra, e na grelha do aluno.
            for rel_licao, citacao in EXEMPLOS_DAS_LICOES[slug]:
                self.assertIn(citacao, re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', ler(rel_licao)))), citacao)
                self.assertNotIn(citacao.casefold(), textos_da_pagina.casefold())
            for _, novo in EXEMPLOS_TROCADOS[slug][:-1]:
                self.assertIn(re.sub(r'_', '', novo), re.sub(r'\s+', ' ', grelha_aluno).replace('“', '«').replace('”', '»'), novo[:50])
        css = ler('assets/task-textos.css')
        impressao = css[css.index('@media print{'):]
        self.assertIn('[data-task-facil] .tf-so-ecra{display:none!important}', impressao)
        self.assertIn('[data-task-facil] .tt-texto{break-inside:avoid}', impressao)
        self.assertIn('[data-task-facil] :is(h2,h3,h4,summary,.tt-rotulo,.tf-meta,.tf-antes,.tf-fig){break-after:avoid}', impressao)
        self.assertIn('[data-task-facil] .tf-topo{break-after:avoid}', impressao)
        # Em papel, nenhum parágrafo se parte; um texto comprido parte-se só entre parágrafos, e o título não fica sozinho.
        self.assertIn('[data-task-facil] .tt-par{margin:0 0 4pt;break-inside:avoid}', impressao)
        self.assertIn('[data-task-facil] .tt-texto.tt-longo{break-inside:auto}', impressao)
        self.assertIn('[data-task-facil] .tt-texto.tt-longo>h3{break-after:avoid}', impressao)
        self.assertLess(impressao.index('[data-task-facil] .tt-texto{break-inside:avoid}'), impressao.index('[data-task-facil] .tt-texto.tt-longo{break-inside:auto}'))

    # ---------- as decisões do docente, em todos os sítios ----------

    def test_tempos_10_10_55_15_em_todos_os_sitios(self):
        for slug in SLUGS:
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            f = d['facil']
            pagina = ler(f'tarefas/{slug}/index.html')
            with self.subTest(tarefa=slug):
                tempos = [solto(l[0]['t'] if isinstance(l[0], dict) else l[0]) for l in f['quadro']['linhas'] if l[0]]
                self.assertEqual(tempos, ['10 min', '10 min', '55 min', '15 min', '90 min'])
                self.assertEqual([solto(l[1]) for l in f['quadro']['linhas']],
                                 ['Aquecimento em cartões', 'Leitura do enunciado', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Revisão e entrega', 'Total'])
                self.assertEqual(f['quadro']['linhas'][2][0], {'t': f'55{N}min', 'linhas': 3})
                self.assertEqual(f['producao_minutos'], 55)
                self.assertEqual(d['aquecer']['minutos'], 10)
                # Na página: o quadro, e os dois relógios (10 e 55 minutos).
                quadro = re.search(r'<table class="tf-quadro">.*?</table>', pagina, re.S).group(0)
                self.assertEqual(re.findall(r'<th scope="row(?:group)?"(?: rowspan="3")?>(\d+)\xa0min</th>', quadro), ['10', '10', '55', '15', '90'])
                self.assertIn(f'<th scope="rowgroup" rowspan="3">55{N}min</th><td>Pergunta{N}1</td>', quadro)
                self.assertEqual(re.findall(r'data-relogio data-max="(\d+)" data-passo="(\d)" data-rotulo="([^"]+)" data-chave="pt-relogio:tarefas/' + slug + r':(\w+)"', pagina),
                                 [('10', '1', 'Aquecimento', 'aquecimento'), ('55', '5', 'Produção em papel', 'producao')])
                self.assertEqual(pagina.count('data-relogio'), 2)
                self.assertIn(f'Faz o aquecimento (10{N}minutos).', pagina)
                self.assertIn(f'Nos 10{N}minutos de leitura, lê as duas perguntas e os passos dos dois temas.', pagina)
                self.assertIn(f'<p class="task-kicker">Tarefa individual, 90{N}minutos</p>', pagina)
        # O aquecimento diz «Dez minutos»; o guia da tarefa tem os mesmos quatro blocos, que somam 90.
        for rel in AQUECIMENTOS:
            self.assertEqual(ler(rel).count('Dez minutos, com consulta.'), 1)
        guia = ler(GUIA)
        blocos = json.JSONDecoder().raw_decode(guia.split('BLOCOS=', 1)[1])[0]
        self.assertEqual(blocos, [[10, 'Aquecer', 'Faz os cartões com consulta.'], [10, 'Ler o enunciado', 'Lê as duas perguntas e os temas A e B.'],
                                  [55, 'Produzir', 'Escreve individualmente, em papel, com consulta.'],
                                  [15, 'Rever e entregar', 'Confere a grelha /20 e entrega fotografias legíveis no Teams.']])
        self.assertEqual(sum(b[0] for b in blocos), 90)
        self.assertEqual(re.findall(r'<div class="t"><b>([^<]+)</b>', guia),
                         [f'Aquecer, 10{N}min', f'Ler o enunciado, 10{N}min', f'Produzir, 55{N}min', f'Rever e entregar, 15{N}min'])
        self.assertIn(f'faz o aquecimento em cartões (10{N}minutos). Seguem-se 10{N}minutos de leitura, 55 de produção e 15 de revisão e entrega.', guia)
        # Nenhum «5 min» nem «60 min» antigos (nem «5 minutos», «60 minutos», «60 de produção») nas páginas do M5 ligadas à tarefa.
        for rel in PAGINAS + [GUIA, INDICE, MAPA, PORTEFOLIO]:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                self.assertNotRegex(fonte, r'(?<![\d,.])(?:5|60)[ \xa0]min')
                self.assertNotRegex(fonte, r'\b60 de produção|\b5 de leitura')
                self.assertNotIn('10/5/60/15', fonte)

    def test_consulta_autoavaliacao_e_aquecimento(self):
        alineas_por_pergunta = {'m5-u1': [4, 4], 'm5-u2': [5, 4]}
        for slug in SLUGS:
            pagina = ler(f'tarefas/{slug}/index.html')
            texto = visivel(sem_textos(pagina))
            cabeca = pagina.split('<header>', 1)[1].split('</header>', 1)[0]
            with self.subTest(tarefa=slug):
                # «Com consulta» diz-se uma vez, no primeiro cartão, e diz o que é.
                frase = 'Trabalhas à mão. O aquecimento e a tarefa são com consulta: podes usar as lições do site, o caderno e o dicionário.'
                self.assertIn(f'<p class="tf-p">{frase}</p>', cabeca)
                self.assertEqual(texto.count('com consulta'), 1)
                self.assertEqual(len(re.findall(r'\bconsulta\b', texto)), 1)
                # O que não conta para as palavras: as duas linhas finais, como antes; uma vez no enunciado, por baixo do quadro, e
                # na grelha do aluno com as palavras de sempre. (A decisão do docente sobre os versos citados ou copiados não tem
                # aqui onde entrar: as duas tarefas do M5 não pedem versos.)
                self.assertIn('<p class="tf-nota">As duas linhas finais não contam para as palavras.</p>', cabeca)
                self.assertEqual(texto.count('não contam para as palavras'), 1)
                grelha = ler(f'tarefas/{slug}/grelha/index.html')
                self.assertEqual(grelha.count('mais duas linhas finais que não contam para as palavras.'), 1)
                self.assertNotIn('versos', texto)
                # A autoavaliação é só para o aluno: não se entrega (enunciado, grelha e correção).
                self.assertIn('<p class="tf-nota tf-grelha-nota">A autoavaliação da grelha é só para ti: não se entrega.</p>', cabeca)
                self.assertEqual(texto.count('autoavaliação'), 2)
                entrega = pagina[pagina.index('<h2>Entrega no Teams</h2>'):pagina.index('</section>', pagina.index('<h2>Entrega no Teams</h2>'))]
                self.assertEqual(re.findall(r'<li>(.*?)</li>', entrega), ['Fotografa as respostas, o texto do teu tema e as duas linhas finais.',
                                                                          'Confirma que as fotografias mostram o trabalho completo.',
                                                                          'Entrega as fotografias na tarefa do Teams.'])
                self.assertEqual(grelha.count('Esta autoavaliação é só para ti: não se entrega.'), 1)
                self.assertNotIn('Entrega esta autoavaliação', grelha)
                self.assertNotIn('comenta a diferença', grelha)
                correcao = ler(f'tarefas/{slug}/correcao/index.html')
                self.assertIn('<thead><tr><th>Critério</th><th class="n">Máx.</th><th class="n">Docente</th><th>Observações</th></tr></thead>', correcao)
                self.assertNotIn('Aluno</th>', correcao)
                self.assertNotIn('Diferença entre a tua nota e a minha', correcao)
                self.assertNotIn('Onde nos afastámos', correcao)
                # Cada linha da tabela de notas tem quatro células (critério, máximo, docente, observações); antes tinha cinco.
                linhas = re.findall(r'<tr(?: class="total")?>(.*?)</tr>', correcao[correcao.index('<tbody>'):correcao.index('</tbody>')])
                self.assertEqual(len(linhas), 6)
                for l in linhas:
                    self.assertEqual(len(re.findall(r'<t[dh][ >]', l)), 4, l[:80])
                for parte in ('<h2 class="g-fb-t">Comentário ao aluno</h2>', '<h3>O que funciona</h3>', '<h3>O que te custa pontos</h3>', '<h3>Próximo passo</h3>'):
                    self.assertEqual(correcao.count(parte), 1)
                # O aquecimento é o primeiro passo, com uma só ligação.
                self.assertEqual(pagina.count('href="aquecimento/"'), 1)
                self.assertIn(f'<ol class="tf-fazer"><li>Faz o aquecimento (10{N}minutos).<span class="task-aquecer tf-abrir"><a href="aquecimento/">Abrir o aquecimento em cartões</a></span></li>', cabeca)
                self.assertLess(cabeca.index('href="aquecimento/"'), cabeca.index('O que entregas'))
                # A verificação final: 10 perguntas de sim ou não (o máximo), numa só lista.
                lista = re.search(r'<fieldset class="task-checklist" aria-labelledby="entregar-title">(.*?)</fieldset>', pagina, re.S).group(1)
                perguntas = re.findall(r'<label><input type="checkbox"> <span>(.*?)</span></label>', lista)
                self.assertEqual(lista.count('<label>'), len(perguntas))
                self.assertLessEqual(len(perguntas), 10)
                self.assertGreaterEqual(len(perguntas), 9)
                self.assertTrue(all(p.endswith('?') for p in perguntas), perguntas)
                self.assertEqual(pagina.count('class="task-checklist"'), 1)
                self.assertIn('<p class="tf-p" id="criterios">Responde sim ou não. Se for não, completa o teu trabalho.</p>', pagina)
                # Um pedido por alínea: cada alínea é uma frase só, curta (14 palavras no máximo).
                d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))['facil']
                contadas = []
                for p in d['perguntas']:
                    self.assertNotIn('grupos', p)
                    contadas.append(len(p['alineas']))
                    for x in p['alineas']:
                        self.assertEqual(len(re.findall(r'[.?!](?:\s|$)', re.sub(r'<[^>]+>', '', x))), 1, x)
                        self.assertLessEqual(len(x.split()), 14, x)
                self.assertEqual(contadas, alineas_por_pergunta[slug])
                # Cada passo dos temas (e cada condição de um passo) é também uma frase só, com 20 palavras no máximo.
                passos = [x for t in d['temas'] for x in t['passos']]
                self.assertGreaterEqual(len(passos), 11)
                for x in passos:
                    for frase in ([x] if isinstance(x, str) else [x['t']] + x['sub']):
                        self.assertLessEqual(len(re.findall(r'[.?!;:](?:\s|$)', re.sub(r'<[^>]+>', '', frase))), 1, frase)
                        self.assertLessEqual(len(re.sub(r'<[^>]+>', '', frase).split()), 20, frase)

    def test_tudo_junto_as_mesmas_palavras(self):
        # O enunciado novo diz «as duas perguntas», «a letra do teu tema», «as respostas ligam-se» e «duas linhas finais»: a grelha, a
        # correção, o aquecimento, o guia, o índice e o mapa usam as mesmas palavras, e as antigas saem de todos.
        for slug in SLUGS:
            for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                rel = f'tarefas/{slug}/{parte}index.html'
                with self.subTest(pagina=rel):
                    texto = visivel(ler(rel), so_main=False, sem_nav=False)
                    for velha in ('úcleo', 'tema escolhido', 'articulad', 'tema que escolheste'):
                        self.assertNotIn(velha, texto)
                    # («fechou» é um verbo das frases inventadas do aquecimento e do romance; o nome «fecho» é que sai)
                    self.assertNotRegex(texto, r'\b[Ff]echo\b')
                    self.assertNotRegex(texto, r'(?<!a letra d)o tema no topo')
            enunciado = visivel(ler(f'tarefas/{slug}/index.html'))
            self.assertIn('Responde a duas perguntas.', enunciado)
            self.assertIn(f'Escreve a letra do teu tema (A{N}ou{N}B) no topo.', enunciado)
            self.assertIn('As respostas ligam-se (não estão soltas)?', enunciado)
            self.assertIn(f'A letra do meu tema (A{N}ou{N}B) está no topo?', enunciado)
            self.assertIn(f'<meta name="description" content="Aula de tarefa com consulta: aquecimento, duas perguntas e um tema à escolha, em papel, durante 90{N}minutos, com entrega no Teams.">', ler(f'tarefas/{slug}/index.html'))
            for parte in ('grelha/', 'correcao/'):
                p = ler(f'tarefas/{slug}/{parte}index.html')
                self.assertIn('Respostas ligadas, extensão e escrita revista', p)
                self.assertIn('a letra do teu tema está no topo', p)
            grelha = ler(f'tarefas/{slug}/grelha/index.html')
            self.assertEqual(grelha.count('Respostas ligadas, extensão e escrita revista'), 3)
            self.assertIn('<p>Duas perguntas e um tema à escolha (A ou B), à mão, entre 200 e ', grelha)
            self.assertIn('a letra do tema no topo', grelha)
            self.assertIn('<li>Não escrever no topo a letra do teu tema (A ou B).</li>', grelha)
            aquecimento = ler(f'tarefas/{slug}/aquecimento/index.html')
            self.assertEqual(aquecimento.count(f'<b>Perguntas{N}1{N}e{N}2.<\\/b>'), 1)
        # m5-u1: «o efeito em quem lê» e «uma expressão do romance», no enunciado, na grelha, na correção e no aquecimento.
        enunciado = visivel(ler(ENUNCIADOS[0]))
        self.assertIn('Explica o efeito de cada passagem em quem lê.', enunciado)
        self.assertIn('Inclui uma expressão do romance entre «».', enunciado)
        for parte in ('grelha/', 'correcao/'):
            p = visivel(ler(f'tarefas/m5-u1/{parte}index.html'), so_main=False)
            self.assertIn('Narrador: duas passagens, um recurso e o efeito em quem lê', p)
            self.assertIn('e explicas o efeito de cada passagem em quem lê.', p)
            self.assertIn('uma expressão do romance, entre «»', p)
            for velha in ('eco do romance', 'o eco', 'o que quer de quem lê', 'o que o narrador quer'):
                self.assertNotIn(velha, p, parte)
        grelha = visivel(ler('tarefas/m5-u1/grelha/index.html'), so_main=False)
        self.assertIn('ou só explicas o efeito numa delas', grelha)
        self.assertIn('faltam a resposta, a memória, o recurso e a expressão do romance.)', grelha)
        aquecimento = ler(AQUECIMENTOS[0])
        self.assertIn('duas passagens do narrador e o efeito de cada uma em quem lê;', aquecimento)
        self.assertIn('Escreves no topo a letra do teu tema, A ou B', aquecimento)
        self.assertIn('Respondes às duas perguntas: o narrador, depois as funções', aquecimento)
        self.assertIn('A letra do tema fica no topo, as duas perguntas vêm primeiro e o tema a seguir;', aquecimento)
        self.assertIn('a letra do tema escreve-se no topo, antes de tudo.', aquecimento)
        # O enunciado usa as palavras da grelha: os testes da lição, «pelo nome», «comenta, julga ou fala com quem lê».
        self.assertIn('Os testes da lição: trocar por um pronome, perguntar, cortar, passar à passiva.', enunciado)
        self.assertIn('um teste da lição (trocar por um pronome, perguntar, cortar, passar à passiva)', grelha)
        self.assertIn('Serve uma passagem em que o narrador comenta, julga ou fala com quem lê.', enunciado)
        self.assertIn('em que o narrador comenta, julga ou fala com quem lê;', grelha)
        self.assertIn(f'A seguir, escreve de onde é: (Introdução) ou (cap.{N}IV).', enunciado)
        self.assertIn('com o lugar (Introdução ou capítulo)', grelha)
        # m5-u2: o enunciado diz «a tua posição», «uma ideia contrária à tua» e «responde-lhe», como antes, e junta entre parênteses
        # os nomes que a grelha, o aquecimento e a lição F13 usam (tese, contra-argumento, refutação).
        enunciado = visivel(ler(ENUNCIADOS[1]))
        for passo in ('Começa pela tua posição (a tese).', 'Apresenta uma ideia contrária à tua (o contra-argumento).', 'Responde-lhe (a refutação).',
                      'Termina com uma conclusão.'):
            self.assertIn(passo, enunciado)
        grelha = visivel(ler('tarefas/m5-u2/grelha/index.html'), so_main=False)
        self.assertIn('a tese na primeira frase; outra citação do último capítulo, explicada; um facto datado do dossiê, ligado à tese; um contra-argumento; a tua refutação.', grelha)
        self.assertIn('Tese, argumento, contra-argumento, refutação, conclusão', ler(AQUECIMENTOS[1]))
        self.assertIn('Os modos de relato: discurso direto, discurso indireto e discurso indireto livre.', enunciado)
        self.assertIn('Modos de relato: as duas passagens, duas marcas e o discurso direto', grelha)
        self.assertIn(f'Na alínea{N}d), usa travessão e muda o que o novo contexto pede.', enunciado)
        self.assertIn('com travessão, mudando o que o novo contexto pede (pessoa, tempo, deíticos)', grelha)
        # O guia, o índice e o mapa do M5.
        for rel, frases in ((GUIA, ['<span>Lê as duas perguntas e os temas A e B.</span>']),
                            (INDICE, ['aquecimento em cartões, duas perguntas, tema A ou B, revisão e fotografias no Teams.',
                                      'com consulta: aquecimento, duas perguntas, tema A ou B, revisão e fotografias no Teams.',
                                      'preparação para a tarefa desta unidade, com duas perguntas e tema A ou B.']),
                            (MAPA, ['com aquecimento, duas perguntas, tema A ou B e grelha /20;'])):
            fonte = ler(rel)
            self.assertNotIn('núcleo comum', fonte, rel)
            self.assertNotRegex(visivel(fonte, so_main=False, sem_nav=False), r'(?i)\bnúcleo\b')
            for frase in frases:
                self.assertIn(frase, fonte, rel)
        self.assertEqual(ler(INDICE).count('com consulta: aquecimento, duas perguntas, tema A ou B, revisão e fotografias no Teams.'), 2)
        self.assertEqual(ler(INDICE).count('preparação para a tarefa desta unidade, com duas perguntas e tema A ou B.'), 2)
        for rel, n in ((INDICE, 3), (MAPA, 1)):
            self.assertEqual(len(MANIFESTO['files'][rel]['edits']), n, rel)

    # ---------- 13/11/2026: a autoavaliação colada no Teams e o par de trabalho saem do guia ----------

    def test_guia_sem_autoavaliacao_para_o_teams_nem_par_de_trabalho(self):
        # Decisão do docente (13/11/2026): no guia da tarefa, a «Autoavaliação» que se copiava para o Teams sai (a autoavaliação é só
        # para o aluno e não se entrega) e «pergunta ao teu par de trabalho» sai (não há trabalho de grupo nem de pares). Como no guia
        # do M3; nada entra no lugar.
        guia, base = ler(GUIA), antes(GUIA)
        lido = visivel(guia, so_main=False, sem_nav=False)
        # As frases de antes estavam na base (o main de partida) e já não estão na página, nem no código.
        saem = ['<h2>Autoavaliação</h2>',
                'Em cada parâmetro, toca no nível que achas que tens. O 4 é o melhor. Escreve uma linha a dizer porquê.',
                '<div id="r-auto"></div>',
                'dás-te um nível em cada parâmetro',
                'O docente vê o teu plano, as notas, a lista e a autoavaliação.',
                'l.push("","AUTOAVALIAÇÃO");',
                '$("#r-auto").innerHTML=',
                '(extra sem nota)',
                'placeholder="Porquê, numa linha."',
                'if(t.dataset.auto!=null)',
                'ev.target.closest(".niveis button")',
                '<li>pergunta ao teu par de trabalho.</li>',
                '<b>Três antes de mim.</b>']
        for frase in saem:
            with self.subTest(sai=frase):
                self.assertEqual(base.count(frase), 1)
                self.assertNotIn(frase, guia)
        # Nenhuma autoavaliação, nenhum nível para tocar e nenhum par, grupo ou equipa em todo o guia (texto e código). Ficam
        # só a regra «Original» (copiar de um colega não conta) e a chave «grupo» dos dados das produções antigas, sempre falsa.
        self.assertNotRegex(guia, r'(?i)auto-?avalia')
        self.assertNotRegex(guia, r'r-auto|data-auto|dataset\.auto|D\.auto|\.niveis button"|class="niveis"|aria-pressed="')
        # O estilo dos níveis fica na folha de estilo, sem uso e igual ao do main: os guias da tarefa têm o mesmo estilo, letra a
        # letra (tests/test_tasks_m356.py). Nada na página nem no código o usa.
        estilo = guia[guia.index('<style>'):guia.index('</style>')]
        self.assertEqual(estilo, base[base.index('<style>'):base.index('</style>')])
        self.assertEqual(guia.count('niveis button'), estilo.count('niveis button'))
        self.assertEqual(guia.count('aria-pressed'), estilo.count('aria-pressed'))
        self.assertNotRegex(lido, r'(?i)\bpar(?:es)?\b|\bgrupos?\b|\bequipas?\b|\bduplas?\b|em conjunto')
        self.assertEqual(re.findall(r'(?i)colegas?', guia), ['colega'])
        self.assertIn('Copiar de uma página ou de um colega, ou mandar fazer a uma máquina, não conta como tarefa.', guia)
        self.assertEqual(set(re.findall(r'"grupo":(\w+)', guia)), {'false'})
        self.assertEqual(len(re.findall(r'(?i)\bgrupo', guia)), guia.count('"grupo":false'))
        # O que fica, com a frase certa: a regra com dois passos (uma lista de dois itens) e o nome a dizer dois.
        self.assertEqual(guia.count('<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li>'
                                    '<li>vê a rubrica.</li></ol>Só depois levantas o braço.</div>'), 1)
        regra = guia[guia.index('<b>Dois antes de mim.</b>'):]
        regra = regra[:regra.index('</div>')]
        self.assertEqual(regra.count('<li>'), 2)
        self.assertEqual(guia.count('No fim, verificas o trabalho com a lista da rubrica e copias tudo para a tarefa do Teams. '
                                    'O que escreves fica só neste telemóvel.</p>'), 1)
        self.assertEqual(guia.count('Cola na tarefa do Teams, juntamente com o trabalho. O docente vê o teu plano, as notas e a lista.</p>'), 1)
        # O resto do modelo que se copia fica: o plano, as notas e a lista de verificação; a seguir à lista vêm logo os botões.
        self.assertIn('<h2>Verificar antes de entregar</h2>\n<ul class="lista" id="r-verificar"></ul>\n<div class="fila">'
                      '<button class="btn" id="copiar">Copiar para o Teams</button>', guia)
        copiado = guia[guia.index('function texto(){'):guia.index('$("#copiar").onclick')]
        self.assertEqual(re.findall(r'"([A-ZÇÃÕÁÉÍÓÚ ]{5,})"', copiado), ['PLANO', 'NOTAS DE TRABALHO', 'VERIFICAÇÃO'])
        self.assertTrue(copiado.endswith('+p.nome)});return l.join("\\n")}\n'), copiado[-80:])
        self.assertEqual(re.findall(r'<h2[^>]*>([^<]*)</h2>', guia[guia.index('<section id="rota"'):]),
                         ['', 'Os blocos de hoje', 'Verificar antes de entregar'])
        # Cada identificador que o código procura existe na página (nada fica a apontar para o bloco que saiu).
        codigo = guia[guia.index('var M="M5"'):]
        for ident in sorted(set(re.findall(r'\$\("#([\w-]+)"\)', codigo))):
            with self.subTest(identificador=ident):
                self.assertEqual(guia.count(f' id="{ident}"'), 1)
        # O código que fica é o do guia do M3 (o mesmo modelo, já sem a autoavaliação), salvo o nome do módulo e os dados.
        m3 = ler('m3/guia-da-tarefa-m3/index.html')
        corpo3, corpo5 = m3[m3.index('function texto(){'):m3.index('</script>', m3.index('function texto(){'))], guia[guia.index('function texto(){'):guia.index('</script>', guia.index('function texto(){'))]
        self.assertEqual(corpo3.replace('M3', 'M5').replace('m3', 'm5'), corpo5)
        # O resto da página é o main de partida, letra a letra, salvo as doze trocas da camada: as quatro dos tempos e de «as duas
        # perguntas» e as oito da decisão de 13/11/2026. Cada troca que tira um pedaço inteiro só tira: fica a base sem esse pedaço.
        edits = MANIFESTO['files'][GUIA]['edits']
        self.assertEqual(len(edits), 12)
        do_commit = do_main(GUIA)
        if do_commit is not None:
            self.assertEqual(do_commit, base)
        self.assertEqual(sha_lf(base), MANIFESTO['files'][GUIA]['base_sha256_lf'])
        de_novo = base
        for e in edits:
            self.assertEqual(de_novo.count(e['old']), 1, e['location'])
            de_novo = de_novo.replace(e['old'], e['new'])
        self.assertEqual(de_novo, guia)
        so_tiram = 0
        for e in edits[7:]:
            i = 0
            while i < len(e['new']) and e['old'][i] == e['new'][i]:
                i += 1
            resto = e['new'][i:]
            if resto and e['old'].endswith(resto):
                so_tiram += 1
        self.assertEqual(so_tiram, 5)
        self.assertEqual(len(base) - len(guia), sum(len(e['old']) - len(e['new']) for e in edits))
        # As páginas das duas tarefas dizem o mesmo: a autoavaliação da grelha é só do aluno e não se entrega; nenhum par nem grupo.
        for slug in SLUGS:
            self.assertIn('A autoavaliação da grelha é só para ti: não se entrega.', ler(f'tarefas/{slug}/index.html'))
            self.assertIn('Esta autoavaliação é só para ti: não se entrega.', ler(f'tarefas/{slug}/grelha/index.html'))
            for parte in ('', 'grelha/', 'correcao/'):
                self.assertNotRegex(visivel(ler(f'tarefas/{slug}/{parte}index.html'), so_main=False, sem_nav=False),
                                    r'(?i)par de trabalho|trabalho de (?:grupo|pares)|em pares|com (?:o|a) (?:teu|tua) colega')

    def test_portefolios_sem_autoavaliacao_de_0_a_20_nem_trabalho_de_equipa(self):
        # Decisão do docente (13/11/2026): no portefólio do módulo saem a autoavaliação de 0 a 20 por parâmetro e «trabalho de
        # equipa», sem pôr nada no lugar. No do M5 e, no mesmo pedido, no do M3.
        for rel, modulo, auto in ((PORTEFOLIO, 'M5', ', e a tua autoavaliação de 0 a 20 por parâmetro, com razões'),
                                  (PORTEFOLIO_M3, 'M3', f', e a tua autoavaliação de 0{N}a{N}20 por parâmetro, com razões')):
            pagina, base = ler(rel), antes(rel)
            lido = visivel(pagina, so_main=False, sem_nav=False)
            with self.subTest(portefolio=rel):
                self.assertEqual(base.count('trabalho de equipa'), 1)
                self.assertEqual(base.count(auto), 1)
                self.assertEqual(len(re.findall(r'(?i)auto-?avalia', base)), 1)
                self.assertNotRegex(pagina, r'(?i)auto-?avalia')
                self.assertNotRegex(pagina, r'(?i)trabalho de equipa|\bequipas?\b|trabalho de (?:grupo|pares)|par de trabalho')
                self.assertNotRegex(solto(pagina), r'\b0 a 20\b(?!0)')
                self.assertNotIn('por parâmetro', pagina)
                # O que fica: a linha do balanço com o cartão do percurso, e a lista do que o portefólio serve para avaliar.
                self.assertEqual(pagina.count(f'<tr><td><code>{modulo}_balanco</code></td><td>O cartão do percurso (passaporte, selos, desafios e respostas das '
                                              'unidades), copiado do Percurso do módulo.</td></tr></table>'), 1)
                self.assertEqual(solto(lido).count('É a base da avaliação qualitativa do módulo (40 %): autonomia, responsabilidade, pensamento crítico, entre '
                                                   'outros. Não tem nota própria; o que faltar pesa nos parâmetros.'), 1)
                # A grelha /20 das tarefas continua referida, como antes (não é a autoavaliação).
                self.assertEqual(pagina.count('Grelha /20.'), base.count('Grelha /20.'))
                self.assertEqual(pagina.count('Grelha /20.'), 2)
                # Nada entrou no lugar: a página é a do main de partida menos os dois pedaços, letra a letra.
                edits = MANIFESTO['files'][rel]['edits']
                self.assertEqual(len(edits), 2)
                self.assertEqual(edits[0]['old'].replace(auto, ''), edits[0]['new'])
                self.assertEqual(edits[1]['old'].replace(' trabalho de equipa,', ''), edits[1]['new'])
                self.assertEqual(base.replace(auto, '').replace(' trabalho de equipa,', ''), pagina)
                self.assertEqual(len(base) - len(pagina), len(auto) + len(' trabalho de equipa,'))
                do_commit = do_main(rel)
                if do_commit is not None:
                    self.assertEqual(do_commit, base)

    def test_tema_b_da_m3_u2_os_argumentos_de_iv_94_e_95_chegam(self):
        # Decisão do docente (13/11/2026): no tema B da m3-u2 (o Velho do Restelo, hoje), a página diz que os argumentos das
        # estâncias IV, 94 e 95 (as que as lições dão, no Texto 3) chegam, em vez de remeter para o manual para IV, 96 a 104.
        velha = f'O Texto{N}3 tem as estâncias{N}IV,{N}94{N}e{N}95, as mesmas das lições. O resto da fala do Velho (IV,{N}96{N}a{N}104) está no manual.'
        nova = f'O Texto{N}3 tem as estâncias{N}IV,{N}94{N}e{N}95, as mesmas das lições. Os argumentos dessas duas estâncias chegam.'
        d, a = json.loads(ler(DADOS_M3U2)), json.loads(antes(DADOS_M3U2))
        tema_b, tema_b_antes = d['facil']['temas'][1], a['facil']['temas'][1]
        self.assertEqual(tema_b['letra'], 'B')
        self.assertEqual(tema_b_antes['antes'][1], velha)
        self.assertEqual(tema_b['antes'], [tema_b_antes['antes'][0], nova])
        # Só essa frase muda, nos dados e na página; o resto é o main de partida, letra a letra.
        tema_b_antes['antes'][1] = nova
        self.assertEqual(d, a)
        for rel in (DADOS_M3U2, ENUNCIADO_M3U2):
            atual, base = ler(rel), antes(rel)
            self.assertEqual(base.count(velha), 1, rel)
            self.assertEqual(base.replace(velha, nova), atual, rel)
            self.assertEqual(len(MANIFESTO['files'][rel]['edits']), 1, rel)
            do_commit = do_main(rel)
            if do_commit is not None:
                self.assertEqual(do_commit, base)
        pagina = ler(ENUNCIADO_M3U2)
        self.assertEqual(pagina.count(f'<p class="tf-p tf-antes">{nova}</p>'), 1)
        lido = visivel(pagina)
        self.assertNotRegex(lido, r'(?i)\bmanual\b')
        self.assertNotRegex(solto(lido), r'96 a 104|IV, 9[6-9]|IV, 10\d')
        # O tema continua a pedir o mesmo (dois argumentos do Velho, com a expressão e a estância), e o Texto 3 tem as duas estâncias.
        self.assertEqual(tema_b['passos'][:3], ['Adapta dois argumentos do Velho.', 'Para cada argumento, cita a expressão do Velho.',
                                                'Para cada argumento, indica a estância.'])
        texto3 = [t for t in d['facil']['textos'] if t['id'] == 'texto-3'][0]
        self.assertEqual([e['rotulo'] for e in texto3['estrofes']], [f'Canto{N}IV, estância{N}94', f'Canto{N}IV, estância{N}95'])

    # ---------- as regras do texto ----------

    def test_regras_do_texto(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                # (nos enunciados, os parágrafos de Camilo e de Eça ficam como no original: os travessões das falas são do autor)
                texto = visivel(sem_textos(fonte))
                baixo = texto.lower()
                if rel == ENUNCIADOS[0]:
                    # («a folhas 232» é uma expressão de Camilo, no parágrafo [1] da Introdução; a lição F02 explica-a no
                    # vocabulário, e a página copia essa linha: é a única «folha» da página, e não é nossa)
                    linha = f'<li><b>a folhas{N}232</b>: na página{N}232</li>'
                    self.assertEqual(fonte.count(linha), 1)
                    self.assertEqual(baixo.count('folha'), 1)
                    baixo = visivel(sem_textos(fonte.replace(linha, ''))).lower()
                for palavra in ('professor', 'jogar', 'jogador', 'ficha', 'folha', 'em grupo', 'em pares', 'fernandes'):
                    self.assertNotIn(palavra, baixo, palavra)
                self.assertNotRegex(baixo, r'\bjog(?:o|os|a|am|ar)\b')
                self.assertNotIn('—', texto)
                self.assertNotRegex(texto, r'\bQual (?!d[aeo]s? )')
                self.assertNotRegex(texto, r'\b[Vv]ocê\b')
        for slug in SLUGS:
            fonte = ler(f'tarefas/{slug}/index.html')
            self.assertEqual(len(re.findall(r'<div class="tt-prosa">', fonte)), 3 if slug == 'm5-u1' else 5)
            # Os travessões da página são só os das falas dos romances, dentro dos textos.
            self.assertGreater(visivel(fonte).count('—'), 10)
            fonte = sem_textos(fonte)
            texto = visivel(fonte)
            principal = fonte[fonte.index('<main'):fonte.index('</main>')]
            with self.subTest(enunciado=slug):
                # «·» só no molde comum (o título da janela e a navegação), nunca numa frase nossa.
                self.assertNotIn('·', texto)
                # Títulos de obras em itálico (fora dos rótulos para leitores de ecrã).
                sem_italicos = re.sub(r'<i>[^<]*</i>|alt="[^"]*"|aria-label="[^"]*"', '', principal)
                for obra in ('Amor de Perdição', 'Os Maias', 'Assommoir'):
                    self.assertNotIn(obra, sem_italicos, obra)
                self.assertGreaterEqual(principal.count('<i>Amor de Perdição</i>' if slug == 'm5-u1' else '<i>Os Maias</i>'), 7)
                # Referências que não se partem (U+00A0), como nas páginas do M3 e do M1, e mais as que estas páginas trazem: os
                # parágrafos numerados, as passagens numeradas e a pessoa gramatical.
                for padrao in (r'\b(?:Texto|Textos|Pergunta|pergunta|Tema|Temas|tema|Lição|lição|canto|Canto|estância|estâncias|verso|versos|Imagem|aula|Passo|Passos|Alínea|Alíneas|alínea|Estrofe|parágrafo|parágrafos|passagem) (?:\d|[AB]\b|[IVX]+\b|F\d|[a-h]\)|\[)',
                               r'\d (?:min|minutos|palavras)\b', r'\b[IVX]+, \d', r'(?:\d|\]) (?:a|e|ou) (?:\d|\[)', r'\bA (?:ou|e) B\b',
                               r'\b(?:cap\.|capítulo) [IVXLC]+\b', r'\bséculo [IVX]+\b', r'\bc\. \d', r'3\.ª pessoa'):
                    # (o «Tema » que só os leitores de ecrã leem antes da letra de cada tema, no molde comum, fica de fora)
                    self.assertNotRegex(visivel(fonte.replace('<span class="sr-only">Tema </span>', '')), padrao)
                # As falas do aluno em discurso direto ficam entre «» (nenhuma aspa direita nem curva nas nossas frases).
                self.assertNotRegex(texto, r'[“”"]')
                self.assertNotRegex(visivel(ler(f'tarefas/{slug}/index.html')), r'[“”"]')
        # No dossiê (a chave antiga, igual à de antes), os anos e o capítulo ficam presos ao escrever a página.
        self.assertIn(f'no livro de entradas da cadeia de 1803{N}a{N}1805.', ler(ENUNCIADOS[0]))
        self.assertIn(f'o hotel do cap.{N}VI, trinta anos depois', ler(ENUNCIADOS[1]))
        # O molde não é o piloto por aprovar: os comentários dizem que foi aprovado.
        for rel in ('scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py', 'scripts/grelhas_tarefas.py', 'assets/task-textos.css', 'assets/task-reader.js',
                    'scripts/tarefas_faceis_m5_20261113.py'):
            self.assertNotIn('por aprovar', ler(rel), rel)

    # ---------- o contrato da página (substitui o de tests/test_task_choice.py nestas duas tarefas) ----------

    def test_contrato_da_pagina(self):
        for slug in SLUGS:
            rel = f'tarefas/{slug}/index.html'
            fonte = ler(rel)
            p = Pagina(fonte)
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            with self.subTest(tarefa=slug):
                self.assertIn('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil data-task-opening="Começar" data-task-index="nomes">', fonte)
                self.assertEqual([t for t, _, _ in p.raiz], ['nav', 'header', 'section', 'section', 'section', 'section', 'section'])
                self.assertEqual([i for _, i, _ in p.raiz][2:], ['produzir', 'pergunta-2', 'tema', 'entregar', 'apoios'])
                self.assertEqual(['Começar'] + [c for _, _, c in p.raiz][2:], CARTOES_NOMES)
                self.assertEqual(p.temas, ['A', 'B'])
                self.assertEqual(len(re.findall(r'<h3 id="tema-([AB])"><span><span class="sr-only">Tema </span>\1</span> ', fonte)), 2)
                self.assertEqual(len(p.ids), len(set(p.ids)))
                # O primeiro cartão: o que vais fazer, o que entregas, o quadro, a grelha.
                cabeca = fonte.split('<header>', 1)[1].split('</header>', 1)[0]
                self.assertEqual(re.findall(r'<h2 class="task-part"[^>]*>(.*?)</h2>', cabeca), ['O que vais fazer', 'Relógio do aquecimento', 'O que entregas', 'Tempo e tamanho'])
                self.assertEqual(cabeca.count('<ol class="tf-fazer">'), 1)
                self.assertEqual(len(re.findall(r'<li>', cabeca.split('<ol class="tf-fazer">')[1].split('</ol>')[0])), 5)
                self.assertIn('<p class="tf-p">Fotografias do teu trabalho em papel, na tarefa do Teams.</p>', cabeca)
                self.assertEqual(fonte.count('<a href="grelha/">'), 1)
                self.assertIn('<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>', cabeca)
                # Uma só pergunta opcional, num desdobrável, com três opções, uma certa, explicações diferentes.
                self.assertEqual(p.perguntas, [('1', True)])
                self.assertEqual(len(p.opcoes), 3)
                self.assertEqual(sum(a['data-correct'] == 'true' for a in p.opcoes), 1)
                self.assertEqual(len({a['data-response'] for a in p.opcoes}), 3)
                self.assertEqual(len(re.findall(r'<span class="task-letter">[ABC]<span class="sr-only">:</span></span> ', fonte)), 3)
                # Os recursos: os mesmos do molde de 28/10, o leitor do molde novo e a folha desta versão (facil-9: a folha ganhou
                # as regras do texto comprido; as páginas do M3 e do M1 pedem as de antes).
                self.assertLess(fonte.index('assets/relogio.js'), fonte.index('pt-lessons/casca.js'))
                for recurso in ('task-choice.css?v=20261028-escolha-2', 'task-90.js?v=20261027-compact-1', 'task-reader.js?v=20261112-facil-7',
                                'task-textos.css?v=20261113-facil-9', 'info-i.css?v=20261105', 'info-i.js?v=20261105'):
                    self.assertEqual(fonte.count(recurso), 1, recurso)
                for fora in ('task-clock', 'rondas', '10/10/60/10'):
                    self.assertNotIn(fora, fonte)
                # As duas linhas finais, a entrega e a letra do tema.
                for frase in ('<h2 id="finais-titulo">Duas linhas finais</h2>', '<h2>Entrega no Teams</h2>', '<h2 id="entregar-title">Antes de entregar, verifica</h2>'):
                    self.assertEqual(fonte.count(frase), 1, frase)
                # Dossiê do tema B: cada facto com a sua fonte e a ligação, que existe; citações e números na página para onde aponta.
                dossie = re.findall(r'<section class="task-dossier tf-dossie".*?</section>', fonte, re.S)
                self.assertEqual(len(dossie), 1)
                self.assertIn(f'<h4 id="dossie">Dossiê do tema{N}B</h4>', dossie[0])
                factos = re.findall(r'<li>(.*?)<span class="tf-origem">Fonte: <a href="([^"]+)">(.*?)</a></span></li>', dossie[0])
                self.assertEqual(len(factos), dossie[0].count('<li>'))
                self.assertEqual([(solto(x), h, n) for x, h, n in factos], [(solto(x['facto']), x['href'], x['fonte']) for x in d['dossie']])
                self.assertEqual(len(factos), 5)
                for facto, href, _ in factos:
                    alvo = solto(plana(str((Path(rel).parent / href / 'index.html').as_posix()).replace('tarefas/' + slug + '/../../', '')))
                    texto = solto(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', facto))))
                    for pedaco in re.findall(r'«([^»]+)»', texto) + re.findall(r'\b\d{3,4}\b', texto):
                        self.assertIn(pedaco, alvo, (href, pedaco))
                # Todas as ligações internas existem; as âncoras apontam para ids da página; para fora, só o molde comum.
                licoes = [h for h in p.ligacoes if '/m5/licao-' in h]
                self.assertGreaterEqual(len(set(licoes)), 4)
                for href in p.ligacoes:
                    url = urlsplit(href)
                    if url.scheme:
                        self.assertEqual((url.scheme, url.netloc), ('https', 'pedrohfernandes-klk.github.io'), href)
                        continue
                    if not url.path:
                        self.assertIn(url.fragment, p.ids, href)
                        continue
                    alvo = (ROOT / rel).parent / unquote(url.path)
                    self.assertTrue(((alvo / 'index.html') if alvo.is_dir() else alvo).is_file(), href)
                self.assertGreaterEqual(len([h for h in p.ligacoes if h.startswith('#texto-')]), 5)
                self.assertEqual(sorted({h for h in p.ligacoes if h.startswith('#texto-')}), [f'#{t["id"]}' for t in d['facil']['textos']])
                self.assertIn('#dossie', p.ligacoes)
                # «Rever a matéria»: uma linha por pergunta ou tema; o nome da página e os nomes das secções entre «» são os da lição.
                rever = re.search(r'<ul class="tf-rever-lista">(.*?)</ul>', fonte, re.S).group(1)
                itens = re.findall(r'<li><b>((?:Pergunta|Tema)\xa0[12AB])\.</b> Lição\xa0F\d\d, <a href="([^"]+)">(.*?)</a>\.? (.*?)</li>', rever)
                self.assertEqual(len(itens), rever.count('<li>'))
                self.assertEqual(len(itens), 5)
                self.assertEqual({solto(x[0]) for x in itens}, {'Pergunta 1', 'Pergunta 2', 'Tema A', 'Tema B'})
                motor = plana('assets/pt-lessons/jogo.js')
                for _, href, nome, resto in itens:
                    alvo = plana(href.replace('../../', '') + 'index.html')
                    self.assertIn(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', nome))), alvo, href)
                    self.assertRegex(href, r'^\.\./\.\./m5/licao-m5-f\d\d/$')
                    self.assertIn(f'Lição{N}F{href[-3:-1]}, <a href="{href}">', rever)
                    seccoes = re.findall(r'«([^»]+)»', resto)
                    self.assertGreaterEqual(len(seccoes), 1, resto)
                    for secao in seccoes:
                        secao = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', secao)))
                        self.assertTrue(secao in alvo or secao in motor, (href, secao))
                self.assertEqual(fonte.count(f'<p class="tf-p">{d["facil"]["rever_texto"]}</p>'), 1)
                self.assertTrue(d['facil']['rever_texto'].startswith(f'Os Textos{N}1,{N}2{N}e{N}3 ' if slug == 'm5-u1' else f'Os Textos{N}1{N}a{N}5 '))
                self.assertTrue(d['facil']['rever_texto'].endswith(' já estão nesta página. As lições servem para rever a matéria.'))
                # Nenhuma pergunta tem grupos de alíneas, nem nada que sirva aos dois temas, nem imagens (as chaves do M1).
                for marca in ('tf-grupo', 'tf-comum', 'tf-dois-temas', 'tf-figs', 'tf-fig'):
                    self.assertNotIn(f'class="{marca}', fonte)
        # A linha «Rever» da pergunta 1 da m5-u2 não manda para os cartões da lição F10 que dizem a resposta («O essencial» e «Em
        # paralelo» nomeiam a estrutura): manda para a «Linha de vida».
        u2 = ler(ENUNCIADOS[1])
        rever = re.search(r'<ul class="tf-rever-lista">(.*?)</ul>', u2, re.S).group(1)
        primeira = re.search(r'<li><b>Pergunta\xa01\.</b>(.*?)</li>', rever).group(1)
        self.assertIn('Relê a «Linha de vida»', primeira)
        self.assertNotRegex(primeira, r'O essencial|Em paralelo')
        self.assertNotRegex(visivel(sem_textos(u2)), r'(?i)\bcircular')
        leitor = ler('assets/task-reader.js')
        self.assertIn('page.getAttribute("data-task-opening")||(compact?"Enunciado":"A aula de tarefa")', leitor)
        self.assertIn('node.getAttribute("data-task-card-name")||', leitor)
        self.assertIn('(page.getAttribute("data-task-index")==="nomes"?"":String(i+1)+". ")+item.label', leitor)

    # ---------- as tarefas dos outros módulos não mudam ----------

    def test_acertos_de_13_11_a_carta_de_exemplo_e_dois_exemplos_da_grelha(self):
        # 13/11/2026: acertos decididos pelo docente no pedido das tarefas do M7. A carta de exemplo do tema A da m5-u1 refaz-se só com
        # matéria que as lições dão (sem «dia de Natal», «todos os dias» e «Foram tantas»), e os dois exemplos da grelha que ainda citavam
        # os textos da própria tarefa («a violencia de um pae é sempre amor», na m5-u1; «Sole normande?», na m5-u2, a exceção que
        # test_exemplos_com_outro_caso ainda admite no texto desta camada) deixam de os citar. Mudam na camada de cima
        # (tarefas_faceis_m7_20261113), que não reescreve esta: os outros testes deste ficheiro leem os ficheiros como esta camada os
        # deixou (ler() desfaz a de cima), e aqui confere-se o que a árvore tem agora, com a mesma exigência e sem a exceção.
        arvore = lambda rel: (ROOT / rel).read_bytes().decode('utf-8')
        grelhas = json.loads(arvore(GRELHAS))['tarefas']
        for slug in SLUGS:
            pagina, grelha = arvore(f'tarefas/{slug}/index.html'), arvore(f'tarefas/{slug}/grelha/index.html')
            for fora in ('dia de Natal', 'todos os dias', 'Foram tantas', 'a violencia de um pae é sempre amor»', 'Sole normande?»'):
                self.assertNotIn(fora, grelha, (slug, fora))
            dentro = ' '.join(re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra">.*?</details>', pagina, re.S))
            for fora in ('dia de Natal', 'todos os dias', 'Foram tantas', 'Sole normande'):
                self.assertNotIn(fora, dentro, (slug, fora))
            blocos = re.findall(r'<section class="tt-texto[^"]*" id="texto-\d".*?</section>', pagina, re.S)
            textos_da_pagina = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', ' '.join(blocos)))).casefold()
            self.assertGreater(len(textos_da_pagina), 3000)
            # nenhuma citação dos exemplos da grelha (todos os critérios, sem exceções) ocorre nos textos da tarefa
            exemplos_da_grelha = ' '.join(v[1] for c in grelhas[slug]['criterios'] for v in c['niveis'].values()).replace('“', '«').replace('”', '»')
            for citacao in re.findall(r'«([^«»]+)»', exemplos_da_grelha):
                if len(citacao.split()) >= 2:
                    self.assertNotIn(citacao.casefold().rstrip('.!?'), textos_da_pagina, (slug, citacao))
        # o exemplo do enunciado continua a vir da grelha pública, letra a letra
        carta = json.loads(arvore('docs/pedagogia/tarefas-escolha/m5-u1.json'))['facil']['temas'][0]['material']['exemplos'][0]['paragrafos']
        self.assertEqual(re.findall(r'«([^«»]+)»', carta[0]['t']), ['não recebia resposta'])
        for p in carta:
            self.assertIn(p if isinstance(p, str) else p['t'], json.dumps(grelhas['m5-u1'], ensure_ascii=False))
        self.assertIn('«O latim era um luxo d’erudito»', re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', arvore('m5/licao-m5-f16/index.html')))))
        self.assertIn('«O latim era um luxo d’erudito»', grelhas['m5-u1']['criterios'][3]['niveis']['max'][1])
        self.assertIn('Imitei a interrupção do jantar do Hotel Central:', grelhas['m5-u2']['criterios'][2]['niveis']['max'][1])

    def test_as_outras_tarefas_nao_mudam(self):
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(len(FICHEIROS), 20)
        self.assertEqual(sorted(OUTRAS + SLUGS), sorted(p.stem for p in (ROOT / 'docs/pedagogia/tarefas-escolha').glob('*.json')))
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in OUTRAS:
            with self.subTest(tarefa=slug):
                no_molde = slug in NO_MOLDE
                # 13/11/2026: a m6-u1 e a m6-u2 passaram também ao molde, pela camada que fica por cima desta (tarefas_faceis_m6_20261113,
                # com o seu teste, tests/test_tarefas_faceis_m6.py). Os dados das grelhas leem-se aqui como esta camada os deixou (sem as
                # chaves novas do M6); os dados e a página das duas tarefas são os da árvore, e pedem a folha da sua versão (facil-10).
                no_molde_m6 = slug in ('m6-u1', 'm6-u2')
                self.assertEqual('facil' in json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json')), no_molde or no_molde_m6)
                self.assertEqual(bool({'autoavaliacao_so_tua', 'trocas_aluno'} & set(grelhas[slug])), no_molde)
                pagina = ler(f'tarefas/{slug}/index.html')
                if no_molde_m6:
                    self.assertEqual(pagina.count('task-textos.css?v=20261113-facil-10'), 1)
                    self.assertNotIn('facil-9', pagina)
                    self.assertEqual(undo_tarefas_faceis_m6_1113(f'tarefas/{slug}/index.html', pagina).count('data-task-facil'), 0)
                elif no_molde:
                    # As páginas do M3 e do M1 continuam a pedir a folha de antes e não usam nenhuma das marcas novas.
                    self.assertEqual(pagina.count('task-textos.css?v=20261112-facil-7' if slug.startswith('m3') else 'task-textos.css?v=20261113-facil-8'), 1)
                    for marca in ('facil-9', 'tt-longo'):
                        self.assertNotIn(marca, pagina)
                    self.assertNotRegex(pagina, r'<p class="tt-par"><span class="tt-pn">\[\d+\]</span> [^<]*<i>')
                else:
                    for marca in ('data-task-facil', 'task-textos.css', 'facil-', 'class="tf-', 'class="tt-'):
                        self.assertNotIn(marca, pagina)
                    self.assertIn('task-reader.js?v=20261028-escolha-2', pagina)
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    if (slug, parte) != ('m3-u2', ''):
                        self.assertNotIn(f'tarefas/{slug}/{parte}index.html', MANIFESTO['files'])
        # Todas as páginas de tarefas/ que não são as nove desta camada (as tarefas, grelhas, correções e aquecimentos dos outros
        # módulos) são as do main de partida, byte a byte; e os dados também. No enunciado e nos dados da m3-u2 só muda a frase do
        # tema B (tests acima).
        todas = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'tarefas').rglob('*') if p.is_file())
        self.assertGreater(len(todas), 60)
        iguais = 0
        # 13/11/2026: os ficheiros que a camada de cima muda (as tarefas do M6 mais fáceis de fazer: as páginas e os dados da m6-u1 e da
        # m6-u2) comparam-se com essa camada desfeita pela auditoria, com contagem estrita: por baixo dela, continuam a ser os do main
        # de partida, byte a byte.
        de_cima = 0
        for rel in todas + sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs/pedagogia').rglob('*.json')):
            if rel in MANIFESTO['files']:
                continue
            r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
            if r.returncode == 0:
                iguais += 1
                with self.subTest(igual_ao_main=rel):
                    conteudo = (ROOT / rel).read_bytes()
                    # 13/11/2026: e os ficheiros que a camada do M7 muda (os dados e as páginas das tarefas do M7), com essa camada
                    # desfeita pela auditoria, com contagem estrita: por baixo dela, continuam a ser os do main de partida.
                    if rel in M7_DE_CIMA:
                        de_cima += 1
                        conteudo = undo_tarefas_faceis_m7_1113(rel, conteudo.decode('utf-8')).encode('utf-8')
                    if rel in M6_FICHEIROS:
                        de_cima += 1
                        conteudo = undo_tarefas_faceis_m6_1113(rel, conteudo.decode('utf-8')).encode('utf-8')
                    self.assertEqual(conteudo, r.stdout)
        # 13/11/2026: 12 da camada do M6 e 10 da do M7.
        # 13/11/2026, revisão: a camada do M7 passou a levar os acertos do M1 e do M5; fora dos ficheiros desta camada, muda mais
        # três (os dados, o enunciado e a grelha da m1-u2): 13 da do M7, 25 ao todo, com a mesma exigência.
        self.assertIn(de_cima, (0, 25))
        if do_main(GUIA) is not None:
            self.assertGreater(iguais, 60)
        # Os três geradores, com os dados da árvore, dão todas as páginas da árvore, byte a byte (as treze tarefas, as grelhas, as
        # correções e os aquecimentos).
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for slug in OUTRAS + SLUGS:
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertIn(f'tarefas/{slug}/{parte}index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())

    # ---------- a camada ----------

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        # 13/11/2026: mais uma camada, a das tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113): 50.
        # 13/11/2026: mais uma camada, a das tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113): 51.
        self.assertEqual(len(verificar_camadas.LAYERS), 51)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 51)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertIn('não se edita à mão', MANIFESTO['_nota'])
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(len(TROCAS), sum(len(v['edits']) for v in MANIFESTO['files'].values()))
        self.assertEqual(len(MANIFESTO['files']), 20)
        # 13/11/2026: confere-se com a camada do M6, que está por cima, desfeita primeiro.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar',
                            # 13/11/2026: e a camada do M7 (tarefas_faceis_m7_20261113), a mais recente, antes de todas.
                            '--desfazer-antes', M7F, '--desfazer-antes', M6F], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 20 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        for t in TROCAS:
            self.assertTrue(t['achado'].startswith('13/11/2026: '), t['local'])
            self.assertIn(t['ocorrencias'], (1, 2))
        self.assertEqual([t['ficheiro'] for t in TROCAS if t['ocorrencias'] == 2], [INDICE, INDICE])
        # Ida e volta, letra a letra: a árvore é o «after» do manifesto; desfeita a camada, cada ficheiro é a base (o main de partida);
        # voltando a aplicar, é outra vez a árvore.
        for rel, registo in MANIFESTO['files'].items():
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = antes(rel)
                self.assertEqual(sha_lf(base), registo['base_sha256_lf'])
                self.assertNotEqual(base, atual)
                de_novo = base
                for e in registo['edits']:
                    self.assertEqual(de_novo.count(e['old']), e['occurrences'], e['location'])
                    de_novo = de_novo.replace(e['old'], e['new'])
                self.assertEqual(de_novo, atual)
                # A base é o ficheiro do commit de partida, byte a byte (quando o repositório o tem: num clone raso, vale o resumo).
                do_commit = do_main(rel)
                if do_commit is not None:
                    self.assertEqual(do_commit, base)
                # O desfazer da auditoria dá o mesmo, e não desfaz nada segunda vez.
                self.assertEqual(undo_tarefas_faceis_m5_1113(rel, atual), base)
                self.assertEqual(undo_tarefas_faceis_m5_1113(rel, base), base)
        # Com a camada que fica logo abaixo (as tarefas do M1) partilha só os dados das grelhas; com a das tarefas do M3, os dados
        # das grelhas e os dados e o enunciado da m3-u2. Aí, o desfazer da auditoria tira primeiro esta e depois as outras; nos
        # outros ficheiros, o desfazer das camadas de baixo dá a base desta.
        m1, m3 = json.loads(ler(M1F))['files'], json.loads(ler(M3F))['files']
        self.assertEqual(set(MANIFESTO['files']) & set(m1), {GRELHAS})
        # 13/11/2026: com a camada do M6, que fica por cima, partilha também só os dados das grelhas.
        self.assertEqual(set(MANIFESTO['files']) & set(M6_FICHEIROS), {GRELHAS})
        # 13/11/2026: por cima da do M6 fica a do M7, que também muda os dados das grelhas: a árvore é o «after» da do M7 e, com ela desfeita, o da do M6.
        self.assertEqual(sha_lf((ROOT / GRELHAS).read_bytes().decode('utf-8')), M7_DE_CIMA[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m7_1113(GRELHAS, (ROOT / GRELHAS).read_bytes().decode('utf-8'))), M6_FICHEIROS[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(ler(GRELHAS)), M6_FICHEIROS[GRELHAS]['base_sha256_lf'])
        self.assertEqual(set(MANIFESTO['files']) & set(m3), {GRELHAS, DADOS_M3U2, ENUNCIADO_M3U2})
        for rel in MANIFESTO['files']:
            if rel != GRELHAS:
                self.assertEqual(undo_tarefas_faceis_m1_1113(rel, ler(rel)), antes(rel), rel)
            if rel not in (GRELHAS, DADOS_M3U2, ENUNCIADO_M3U2):
                self.assertEqual(undo_tarefas_faceis_m3_1112(rel, ler(rel)), antes(rel), rel)
        self.assertEqual(sha_lf(antes(GRELHAS)), m1[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m1_1113(GRELHAS, ler(GRELHAS))), m1[GRELHAS]['base_sha256_lf'])
        self.assertEqual(m1[GRELHAS]['base_sha256_lf'], m3[GRELHAS]['after_sha256_lf'])
        sem_as_tres = undo_tarefas_faceis_m3_1112(GRELHAS, ler(GRELHAS))
        self.assertEqual(sha_lf(sem_as_tres), m3[GRELHAS]['base_sha256_lf'])
        for chave in ('autoavaliacao_so_tua', 'trocas_aluno'):
            self.assertNotIn(chave, sem_as_tres)
        for rel in (DADOS_M3U2, ENUNCIADO_M3U2):
            self.assertEqual(sha_lf(antes(rel)), m3[rel]['after_sha256_lf'], rel)
            self.assertEqual(sha_lf(undo_tarefas_faceis_m3_1112(rel, ler(rel))), m3[rel]['base_sha256_lf'], rel)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m5_20261113', ROOT / 'scripts/tarefas_faceis_m5_20261113.py')
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        todas, finais = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(sorted(C.FICHEIROS), sorted(FICHEIROS))
        self.assertEqual(C.BASE_COMMIT, BASE_COMMIT)
        # As cinco páginas dos módulos mudam só nas trocas escritas à mão: doze no guia (as cinco saídas são as do guia do M3), três
        # no índice, uma no mapa e duas em cada portefólio.
        modulo = (GUIA, INDICE, MAPA, PORTEFOLIO, PORTEFOLIO_M3)
        self.assertEqual(sorted((f, a, b, n) for f, a, b, n, _ in C.EDICOES),
                         sorted((t['ficheiro'], t['antigo'], t['novo'], t['ocorrencias']) for t in TROCAS if t['ficheiro'] in modulo))
        self.assertEqual({f: [x for x, *_ in C.EDICOES].count(f) for f in modulo}, {GUIA: 12, INDICE: 3, MAPA: 1, PORTEFOLIO: 2, PORTEFOLIO_M3: 2})
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m3_20261112', ROOT / 'scripts/tarefas_faceis_m3_20261112.py')
        C3 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C3)
        self.assertEqual([(a, s, d, c) for f, a, s, d, c in C.SAI if f == GUIA], [(a, s, d, c) for f, a, s, d, c in C3.SAI])
        # As camadas do M3 e do M1, que ficam por baixo e partilham ficheiros com esta, continuam a dar o seu JSON, com esta desfeita
        # primeiro.
        self.assertEqual(C3.construir()[0], json.loads(ler('scripts/tarefas_faceis_m3_20261112.json')))
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m1_20261113', ROOT / 'scripts/tarefas_faceis_m1_20261113.py')
        C1 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C1)
        self.assertEqual(C1.construir()[0], json.loads(ler('scripts/tarefas_faceis_m1_20261113.json')))

    def test_leitura_historica_dos_enunciados(self):
        # Os contratos históricos leem as tarefas como eram antes do pedido #192 (scripts/tarefas_claras_historico.py). Com esta camada
        # por cima, a leitura dá a base do manifesto do #192, letra a letra, nos enunciados e nos dados da M5-U1, da M5-U2 e da M3-U2,
        # a partir da página inteira ou com esta camada já desfeita; e não desfaz nada segunda vez.
        import tarefas_claras_historico as historico
        claras = json.loads(ler('tests/fixtures/tarefas-claras-edits-20261110.json'))['files']
        nossos = sorted(set(MANIFESTO['files']) & set(claras))
        self.assertEqual(nossos, sorted(DADOS_TAREFAS + [DADOS_M3U2] + ENUNCIADOS + [ENUNCIADO_M3U2]))
        for rel in nossos:
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                antes_192 = historico.desfazer(rel, atual)
                self.assertEqual(sha_lf(antes_192), claras[rel]['base_sha256_lf'])
                self.assertEqual(historico.desfazer(rel, antes(rel)), antes_192)
                self.assertEqual(historico.desfazer(rel, antes_192), antes_192)
        m1, m3 = json.loads(ler(M1F))['files'], json.loads(ler(M3F))['files']
        for rel in MANIFESTO['files']:
            with self.subTest(faceis=rel):
                sem = historico.desfazer_faceis(rel, ler(rel))
                # Nos ficheiros que só esta camada muda, a leitura tira esta e dá a base; nos que partilha com as do M1 e do M3,
                # tira as três, pela ordem.
                esperado = m3[rel]['base_sha256_lf'] if rel in m3 else MANIFESTO['files'][rel]['base_sha256_lf']
                self.assertEqual(sha_lf(sem), esperado)
                self.assertEqual(historico.desfazer_faceis(rel, sem), sem)
                if rel not in m3 and rel not in m1:
                    self.assertEqual(sem, antes(rel))
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer_faceis(path, text):'):fonte.index('def desfazer(path, text):')]
        # 13/11/2026: a leitura histórica tira primeiro a camada do M6, que está por cima desta.
        self.assertLess(corpo.index('TAREFAS_FACEIS_M6.get(rel)'), corpo.index('TAREFAS_FACEIS_M5.get(rel)'))
        self.assertLess(corpo.index('TAREFAS_FACEIS_M5.get(rel)'), corpo.index('TAREFAS_FACEIS_M1.get(rel)'))
        self.assertLess(corpo.index('TAREFAS_FACEIS_M1.get(rel)'), corpo.index('TAREFAS_FACEIS_M3.get(rel)'))
        self.assertIn("_sha_lf(text) == por_cima['after_sha256_lf']", corpo)
        self.assertIn("assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M5 mais fáceis de fazer não confere: {rel}'", corpo)

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        # A auditoria desfaz primeiro esta camada; o corte da Sala também; as bases das camadas que partilham ficheiros com ela também.
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_tarefas_faceis_m5_1113(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m1_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m5_1113\(path, text\)\n')
        # 13/11/2026: e o desfazer desta camada tira primeiro a do M6, que está por cima.
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m5_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m6_1113\(path, text\)\n')
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m3_1112\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m1_1113\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('tarefas-faceis-m5-edits-20261113.json'), sala.index('tarefas-faceis-m1-edits-20261113.json'))
        self.assertLess(sala.index('tarefas-faceis-m1-edits-20261113.json'), sala.index('tarefas-faceis-m3-edits-20261112.json'))
        for rel in ('scripts/cuidado_m6_20261108.py', 'scripts/cuidado_m7_20261111.py'):
            self.assertIn('return desfazer_faceis(rel, (ROOT / rel).read_bytes().decode(\'utf-8\'))', ler(rel), rel)
        indices = ler('scripts/cartaz_indices_148_20261106.py')
        corpo = indices[indices.index('def base(rel):'):]
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M5.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M1.read_text'))
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M1.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M3.read_text'))
        for rel in ('scripts/tarefas_faceis_m3_20261112.py', 'scripts/tarefas_faceis_m1_20261113.py'):
            fonte = ler(rel)
            self.assertIn("m5 = ROOT / 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'", fonte[fonte.index('def ler(rel):'):fonte.index('def base(rel):')], rel)
        m3 = ler('scripts/tarefas_faceis_m3_20261112.py')
        leitura = m3[m3.index('def ler(rel):'):m3.index('def base(rel):')]
        self.assertLess(leitura.index("m5 = ROOT / 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'"), leitura.index("m1 = ROOT / 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'"))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs', 'tests/browser_creditos_i_pt1.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((tarefasFaceisM5['), texto.index('((tarefasFaceisM1['), rel)
            self.assertLess(texto.index('((tarefasFaceisM1['), texto.index('((tarefasFaceisM3['), rel)
            self.assertEqual(texto.count('((tarefasFaceisM5['), texto.count('((tarefasFaceisM1['), rel)
        # Nos fluxos e nos outros testes, cada cadeia de desfazer começa por esta camada, sem nada entre ela e a das tarefas do M1.
        cadeias = 0
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            # (13/11/2026: o teste da camada do M6 tem as suas próprias asserções sobre as cadeias)
            if p.name in ('test_tarefas_faceis_m5.py', 'test_tarefas_faceis_m1.py', 'test_tarefas_faceis_m3.py', 'test_tarefas_faceis_m6.py'):
                continue
            texto = '\n'.join(linha for linha in p.read_text('utf-8').split('\n') if not linha.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + M1F), plano.count(f'--desfazer-antes {meu} --desfazer-antes {M1F}'))
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes {t1}'), plano.count('--desfazer-antes {t7} --desfazer-antes {t6} --desfazer-antes {t5} --desfazer-antes {t1}'))
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes {T1}'), plano.count('--desfazer-antes {T7} --desfazer-antes {T6} --desfazer-antes {T5} --desfazer-antes {T1}'))
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count(f"ROOT/'{M1F}',"), plano.count(f"(ROOT/'{M7F}',ROOT/'{M6F}',ROOT/'{meu}',ROOT/'{M1F}',"))  # (13/11/2026: a lista abre pela camada do M6)
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count("ROOT/'{t1}',"), plano.count("(ROOT/'{t7}',ROOT/'{t6}',ROOT/'{t5}',ROOT/'{t1}',"))
                # 13/11/2026: por cima das tarefas do M5 mais fáceis de fazer ficam as duas tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertEqual(plano.count("ROOT/'{T1}',"), plano.count("(ROOT/'{T7}',ROOT/'{T6}',ROOT/'{T5}',ROOT/'{T1}',"))
                self.assertEqual(plano.count("' + T1"), plano.count("' + T5 + ' --desfazer-antes ' + T1"))
                # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça.
                if p.suffix == '.yml':
                    # (13/11/2026: logo a seguir à do M6)
                    # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                    self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count(f'--verificar --desfazer-antes {M7F} --desfazer-antes {M6F} --desfazer-antes {meu}'))
                cadeias += plano.count(f'--desfazer-antes {meu} --desfazer-antes {M1F}')
        self.assertGreater(cadeias, 40)
        # Nos testes das camadas do M1 e do M3, as cadeias são as mesmas, com esta à cabeça.
        # (13/11/2026: com a do M6 antes desta)
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn("plano.count(f'--verificar --desfazer-antes {M7F} --desfazer-antes {M6} --desfazer-antes {M5} --desfazer-antes {meu}')", ler('tests/test_tarefas_faceis_m1.py'))
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn("plano.count(f'--verificar --desfazer-antes {M7F} --desfazer-antes {M6} --desfazer-antes {M5} --desfazer-antes {M1} --desfazer-antes {meu}')", ler('tests/test_tarefas_faceis_m3.py'))
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        # 13/11/2026: no fluxo, esta camada confere-se com a do M6 desfeita primeiro, e as do M1 e do M3 com as duas.
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m5_20261113.json --manifesto {meu} --verificar --desfazer-antes {M7F} --desfazer-antes {M6F}\n', tarefas)
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m1_20261113.json --manifesto {M1F} --verificar --desfazer-antes {M7F} --desfazer-antes {M6F} --desfazer-antes {meu}\n', tarefas)
        # 13/11/2026: por cima das tarefas do M6 mais fáceis de fazer ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m3_20261112.json --manifesto {M3F} --verificar --desfazer-antes {M7F} --desfazer-antes {M6F} --desfazer-antes {meu} --desfazer-antes {M1F}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m5.py' -v", tarefas)
        self.assertIn('        run: python tests/browser_tarefas_faceis_m5.py\n', tarefas)
        self.assertTrue((ROOT / 'tests/browser_tarefas_faceis_m5.py').is_file())
        # Os fluxos que conferem ou desfazem esta camada arrancam quando ela muda.
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/tarefas_faceis_m5_20261113.*', meu):
                self.assertIn(f"'{caminho}'", texto, nome)
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')):
            texto = p.read_text('utf-8')
            if 'tarefas-faceis-m5-edits-20261113' in texto:
                self.assertRegex(texto.split('\non:')[0], r'\n# 13/11/2026: as duas tarefas do M5 mais fáceis de fazer e «tudo junto» no M5, com dois acertos do M3, a camada tarefas_faceis_m5_20261113 ', p.name)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        blocos = re.findall(r'^    paths: (\[.*\])$', cartaz, re.M)
        self.assertEqual(len(blocos), 2)
        self.assertEqual(blocos[0], blocos[1])

        # No fluxo das tarefas, tudo o que a camada muda, os geradores, o molde e os seus testes estão nos caminhos do pedido.
        def padrao(glob):
            partes = re.split(r'(\*\*|\*|\[[^\]]+\])', glob)
            return re.compile(''.join('.*' if x == '**' else '[^/]*' if x == '*' else x if x.startswith('[') else re.escape(x)
                                      for x in partes) + '$')
        cabeca = tarefas[tarefas.index('  pull_request:\n    paths:\n'):tarefas.index('\npermissions:')]
        padroes = [padrao(g) for g in re.findall(r"^      - '([^']+)'$", cabeca, re.M)]
        self.assertGreater(len(padroes), 50)
        for rel in FICHEIROS + ['scripts/tarefas_faceis_m5_20261113.py', CAMADA_REL, meu, 'scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py',
                                'scripts/grelhas_tarefas.py', 'scripts/aquecimentos.py', 'scripts/tarefas_claras_historico.py',
                                'assets/task-textos.css', 'assets/task-reader.js', 'tests/test_tarefas_faceis_m5.py',
                                'tests/browser_tarefas_faceis_m5.py']:
            self.assertTrue(any(q.match(rel) for q in padroes), rel)


if __name__ == '__main__':
    unittest.main()
