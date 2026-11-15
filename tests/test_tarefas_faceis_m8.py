"""13/11/2026: as duas tarefas do M8 (m8-u1 e m8-u2) «mais fáceis de fazer» e «tudo junto» no M8 (camada tarefas_faceis_m8_20261113).

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201) e levado ao M1, ao M5, ao M6 e ao M7. Esta
camada leva-o ao M8, e este ficheiro exige das duas tarefas do M8 o que tests/test_tarefas_faceis_m6.py exige das do M6:

* a tarefa pede o mesmo: os títulos, os nomes e as letras dos temas, os números de palavras, cada pedido do enunciado de antes (com as
  mesmas palavras), a pergunta das duas linhas finais e a pergunta opcional, e os critérios, níveis, exemplos e pontos das grelhas,
  iguais aos de antes da camada (a base do manifesto, o main f8959def);
* DIREITOS DE AUTOR (decisão do docente para o M8): os poemas e o conto ainda têm direitos (Eugénio de Andrade, 2005; Ana Luísa
  Amaral, 2022; Maria Judite de Carvalho, 1998: as datas conferem-se nas lições) e não se copiam para a página. Cada um tem um bloco
  «Onde está o texto» com as citações curtas que as lições do M8 já publicam, conferidas letra a letra no cartão da lição de destino,
  e a linha de fonte da lição, que remete para o manual sem número de página; nada veio de fora das lições; não há imagens;
* os exemplos usam outro caso (os casos inventados dos aquecimentos, com as frases dos aquecimentos, letra a letra), sem palavras dos
  textos da tarefa, sem dar feita nenhuma alínea e sem a resposta certa da pergunta opcional;
* as decisões do docente, em todos os sítios: tempos 10/10/55/15 (quadro, relógios, guia), nenhum «5 min» nem «60 min» antigos nas
  páginas do M8 ligadas à tarefa; «com consulta» dito uma vez, no primeiro cartão; os versos e as passagens citados ou copiados não
  contam para as palavras (a mesma frase no enunciado, na grelha e no guia); a autoavaliação da grelha não se entrega (enunciado,
  grelha e correção); o aquecimento com uma só ligação; no máximo 10 perguntas de sim ou não na verificação; as mesmas palavras no
  enunciado, na grelha, na correção, no guia, no índice e no mapa;
* o guia, o portefólio, o índice e o mapa do M8 são os do main de partida, letra a letra, salvo as trocas da camada, conferidas uma a
  uma: no guia saem a «Autoavaliação» que se copiava para o Teams e «pergunta ao teu par de trabalho» (a regra passa a chamar-se
  «Dois antes de mim»); no portefólio saem «autoavaliação /20» e «trabalho de equipa», sem nada no lugar;
* as regras do texto: sem as palavras proibidas, sem «·» nem «—» nas nossas frases, «Que + nome» ou «Qual das…», referências que não
  se partem, títulos de livros em itálico, falas do aluno entre «»;
* o contrato da página, que substitui o de tests/test_task_choice.py nestas duas tarefas: seis cartões com nome, dois temas, uma
  pergunta opcional com três opções, os dois relógios, as ligações internas com alvo, as lições ligadas existem e têm os títulos e
  as secções que a página manda reler;
* as tarefas, grelhas, correções e aquecimentos dos outros módulos (e os aquecimentos do M8) são os do main de partida, byte a byte,
  e saem iguais dos geradores;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base, gerador que dá o mesmo JSON, registada na
  auditoria (desfazer), em scripts/desligar_sala.py, na leitura histórica dos enunciados e nas cadeias e caminhos dos fluxos.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em
tests/browser_tarefas_faceis_m8.py."""
from html.parser import HTMLParser
from pathlib import Path
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
from auditoria_20261028 import undo_tarefas_faceis_m8_1113, undo_tarefas_faceis_m7_1113, undo_tarefas_faceis_m3_1112  # noqa: E402
# 14/11/2026: por cima desta camada ficam as duas tarefas do M9 mais fáceis de fazer (tarefas_faceis_m9_20261114, com o seu teste,
# tests/test_tarefas_faceis_m9.py), que partilham com esta os dados das grelhas. Este teste lê os ficheiros que essa camada muda como
# estavam por baixo dela: desfeita pela auditoria, com contagem estrita. A exigência é a mesma.
from auditoria_20261028 import undo_tarefas_faceis_m9_1114  # noqa: E402
from auditoria_20261028 import undo_tarefa_m4u2_1115  # noqa: E402  (15/11/2026: a camada da tarefa m4-u2, a mais recente)
import verificar_camadas  # noqa: E402

CAMADA_REL = 'scripts/tarefas_faceis_m8_20261113.json'
MANIFESTO_REL = 'tests/fixtures/tarefas-faceis-m8-edits-20261113.json'
M7F = 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'
M3F = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
M9F = 'tests/fixtures/tarefas-faceis-m9-edits-20261114.json'  # 14/11/2026: a camada das tarefas do M9 mais fáceis de fazer, a mais recente
M9F_m4u2 = 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json'  # 15/11/2026: a camada da tarefa m4-u2 com «Tema A ou B», a mais recente
M9F_fila = 'tests/fixtures/fila-final-edits-20261115.json'  # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
M9F_sintese = 'tests/fixtures/sintese-duas-linhas-edits-20261115.json'  # 15/11/2026: por cima da tarefa m4-u2 fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
M9_DE_CIMA = json.loads((ROOT / M9F).read_text('utf-8'))['files']
# 15/11/2026: e, por cima da do M9, a da tarefa m4-u2 com «Tema A ou B» e o acerto do M8 (tarefa_m4u2_tema_b_20261115, com o seu teste,
# tests/test_tarefas_faceis_m4.py), que muda os dados, o enunciado e a grelha da m8-u1, o guia do M8 e os dados das grelhas. Este teste lê
# esses ficheiros como estavam por baixo dela: desfeita pela auditoria, com contagem estrita. A exigência é a mesma.
M4U2_DE_CIMA = json.loads((ROOT / 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json').read_text('utf-8'))['files']
# 15/11/2026: e, por cima de todas, «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115, com o seu teste,
# tests/test_sintese_duas_linhas.py), que muda os índices, os portefólios, os mapas e o guia da tarefa do M1, do M3, do M5, do M6, do M7
# e do M8: os ficheiros que ela muda leem-se como estavam por baixo dela (a auditoria desfá-la primeiro, com contagem estrita). A
# exigência é a mesma.
SINTESE_DE_CIMA = json.loads((ROOT / 'tests/fixtures/sintese-duas-linhas-edits-20261115.json').read_text('utf-8'))['files']
# 15/11/2026: e a fila final (fila_final_20261115), por cima de todas (muda, entre outras, o guia da tarefa do M2 e os portefólios do M4 e do M8): também se leem os ficheiros dela como estavam por baixo, com contagem estrita.
FILA_DE_CIMA = json.loads((ROOT / 'tests/fixtures/fila-final-edits-20261115.json').read_text('utf-8'))['files']
DADOS_M4U2 = 'docs/pedagogia/tarefas-escolha/m4-u2.json'  # 15/11/2026: os dados novos da m4-u2 (não são de nenhuma camada)
BASE_COMMIT = 'f8959def7249a79865345782c813e3e49553acff'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
TROCAS = json.loads((ROOT / CAMADA_REL).read_text('utf-8'))
SLUGS = ('m8-u1', 'm8-u2')
N = '\xa0'
DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
ENUNCIADOS = [f'tarefas/{s}/index.html' for s in SLUGS]
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'correcao/')]
AQUECIMENTOS = [f'tarefas/{s}/aquecimento/index.html' for s in SLUGS]
DADOS_AQUECIMENTOS = [f'docs/pedagogia/aquecimentos/{s}.json' for s in SLUGS]
GUIA, INDICE, MAPA = 'm8/guia-da-tarefa-m8/index.html', 'm8/index.html', 'm8/mapa-do-modulo-m8/index.html'
PORTEFOLIO = 'm8/portefolio-do-modulo-m8/index.html'
FICHEIROS = DADOS_TAREFAS + [GRELHAS] + PAGINAS + [GUIA, PORTEFOLIO, INDICE, MAPA]
F03, F04, F05, F06, F08, F10, F12, F16 = (f'm8/licao-m8-f{k}/index.html' for k in ('03', '04', '05', '06', '08', '10', '12', '16'))
OUTRAS = ('m1-u1', 'm1-u2', 'm3-u1', 'm3-u2', 'm5-u1', 'm5-u2', 'm6-u1', 'm6-u2', 'm7-u3', 'm9-u1', 'm9-u2')
CARTOES_NOMES = ['Começar', 'Tema A ou B', 'O teu plano', 'O teu texto', 'Fechar e entregar', 'Rever a matéria']
NAO_CONTAM = 'Não contam para as palavras: os versos e as passagens citados ou copiados, o plano e as duas linhas finais.'
CONSULTA = 'Trabalhas à mão. O aquecimento e a tarefa são com consulta: podes usar as lições do site, o caderno e o dicionário.'
# O que cada enunciado de antes pedia, com as suas palavras: cada pedaço está no enunciado de antes (ou no seu dossiê) e continua no
# de agora.
PEDIDOS = {
    'm8-u1': ['Compara «As Palavras» e «Adeus», de Eugénio de Andrade.', 'Explica como a linguagem ganha ou perde força em cada poema.',
              'Apoia a tua apreciação numa diferença entre eles.', 'Compara «Prece no Mediterrâneo» e «A verdade histórica», de Ana Luísa Amaral.',
              'Explica como a forma de prece ou de relato doméstico nos faz prestar atenção à experiência apresentada.',
              'a tua opinião inicial', 'uma dificuldade que a comparação terá de resolver', 'Escolhe um indício de cada poema',
              'xplica o efeito de cada', 'compara os poemas, em vez de escrever dois resumos', 'Cita no máximo quatro versos de cada poema.',
              'que diferença entre os poemas mais alterou a tua leitura?', 'Indica o indício que a sustenta.',
              'Fotografa o plano, o texto e as duas linhas finais.', 'Eugénio de Andrade', 'Ana Luísa Amaral',
              'A manhã vai de alimento a medida.', 'Que frase explica o contraste entre os dois verbos?'],
    'm8-u2': ['Partir é, para George, libertação, perda ou ambas?', 'efende a tua leitura', 'uma passagem que a ponha em causa',
              'O encontro com a mulher mais velha abre uma possibilidade ou parece fechar o futuro?', 'o que o conto diz do que tu concluis',
              'a tua posição', 'ndica dois momentos do conto que a apoiem', 'onde se encontram', 'Anota uma dificuldade para a tua posição.',
              'esenvolve os argumentos', 'presenta uma objeção', 'com apoio no conto',
              'Distingue a tua interpretação do que o conto permite afirmar sobre a personagem.', 'dois momentos distintos',
              'Não é pedido qualquer relato da tua vida.', 'que objeção te obrigou a precisar a tua posição?',
              'Mostra o momento do conto a que voltaste.', 'Fotografa o plano, o texto e as duas linhas finais.', 'Partir', 'Encontrar o futuro',
              'Pode estar a repetir um ensaio habitual.', 'Que objeção testa a leitura de que Inês ensaia para aceitar?'],
}
ALINEAS = {
    'm8-u1': [['Escreve a tua opinião inicial sobre os dois poemas.', 'Escreve uma dificuldade que a comparação terá de resolver.',
               'Escolhe um indício de cada poema.', 'Indica onde está cada indício: o título do poema e o verso ou a estrofe.'],
              ['Apresenta a tua apreciação: o que pensas dos dois poemas, e porquê.', 'Explica o efeito de cada indício.',
               'Relaciona-os: compara os poemas, em vez de escrever dois resumos.', 'Cita no máximo quatro versos de cada poema.',
               'Indica onde leste os poemas: o manual ou outra edição.', 'Escreve o total de palavras no fim.']],
    'm8-u2': [['Escreve a tua posição: a tua resposta à pergunta do tema.', 'Indica dois momentos do conto que a apoiem.',
               'Indica onde se encontram: a página do teu manual e o início de cada passagem.', 'Anota uma dificuldade para a tua posição.'],
              ['Apresenta a tua posição.', 'Desenvolve os argumentos com os dois momentos do conto.', 'Apresenta uma objeção.',
               'Responde à objeção com apoio no conto.', 'Distingue a tua interpretação do que o conto permite afirmar sobre a personagem.',
               'Indica onde leste o conto: o manual ou outra edição.', 'Escreve o total de palavras no fim.']],
}
PASSOS = {'m8-u1': [['Explica como a linguagem ganha ou perde força em cada poema.', 'Apoia a tua apreciação numa diferença entre eles.'],
                    ['Explica como a forma de prece ou de relato doméstico nos faz prestar atenção à experiência apresentada.']],
          'm8-u2': [['Defende a tua leitura.', 'Considera uma passagem que a ponha em causa.'],
                    ['Defende a tua leitura.', 'Distingue o que o conto diz do que tu concluis.']]}
# Os blocos «Onde está o texto»: o título, a lição e o cartão de onde vem a citação, a forma como a lição a escreve (com « / » entre
# os versos, num <blockquote> com <br>, ou em prosa), as linhas, a lição e o cartão da linha de fonte e o princípio dessa linha (que a
# página copia letra a letra), e a lição, o cartão e o ano em que a lição diz que o autor morreu.
ONDE = {
    'm8-u1': [
        ('texto-1', '«As Palavras», de Eugénio de Andrade', F04, 7, 'barra', ['São como um cristal,', 'as palavras.'],
         F04, 4, 'Eugénio de Andrade, «As Palavras»', (F04, 2, '<b>2005</b><span class="tx">Morre no Porto.</span>', 2005)),
        ('texto-2', '«Adeus», de Eugénio de Andrade', F04, 25, 'br', ['Já gastámos as palavras pela rua, meu amor,', 'e o que nos ficou não chega'],
         F04, 25, 'Eugénio de Andrade, «Adeus», de <i>Os Amantes sem Dinheiro</i> (1950).', (F04, 2, '<b>2005</b><span class="tx">Morre no Porto.</span>', 2005)),
        ('texto-3', '«Prece no Mediterrâneo», de Ana Luísa Amaral', F05, 3, 'barra', ['Em vez de peixes, Senhor,', 'dai-nos a paz'],
         F05, 4, 'Ana Luísa Amaral, «Prece no Mediterrâneo», <i>Ágora</i>, Assírio &amp; Alvim, 2019.', (F05, 2, '<b>2022</b><span class="tx">Morre no Porto.</span>', 2022)),
        ('texto-4', '«A verdade histórica», de Ana Luísa Amaral', F05, 24, 'br',
         ['A minha filha partiu uma tigela', 'na cozinha.', 'E eu que me apetecia escrever', 'sobre o evento,'],
         F05, 24, f'Ana Luísa Amaral, «A verdade histórica», em <i>PÁ: Poesia &amp; Outras Artes</i>, n.º{N}0, Casa Comum/U.Porto Press, setembro de 2023',
         (F05, 2, '<b>2022</b><span class="tx">Morre no Porto.</span>', 2022)),
    ],
    'm8-u2': [
        ('texto-1', '«George», de Maria Judite de Carvalho', F16, 4, 'prosa',
         ['«À sua frente uma senhora de idade, primeiro esboçada, finalmente completa, olha-a atentamente. De idade não, George detesta '
          'eufemismos, mesmo só pensados, uma mulher velha.»'],
         F16, 4, 'Maria Judite de Carvalho, «George», em <i>Seta Despedida</i>, Mem Martins, Europa-América, 1995.',
         (F08, 2, 'Maria Judite de Carvalho (1921–⁠1998)', 1998)),
    ],
}
# 14/11/2026: a linha de fonte de cada bloco, inteira. Só diz «lê-se no manual» onde uma lição o confirma (a lição F04 manda usar «a
# edição do manual» para «As Palavras»; a lição F12, «a passagem do manual» para «George»); para os outros três poemas diz que cartão
# da lição dá a publicação onde se lê o poema completo (as lições não dizem que estão no manual). Fica igual ou mais exigente: confere-se
# a linha inteira, letra a letra, e o que diz confere-se na lição.
FONTE_PAGINA = {
    ('m8-u1', 'texto-1'): f'Eugénio de Andrade, «As Palavras», de <i>Até Amanhã</i>. O poema completo lê-se no manual. A lição{N}F04 também diz onde o ler: cartão «O texto».',
    ('m8-u1', 'texto-2'): f'Eugénio de Andrade, «Adeus», de <i>Os Amantes sem Dinheiro</i> (1950). A lição{N}F04 diz onde ler o poema completo: cartão «Outra leitura».',
    ('m8-u1', 'texto-3'): f'Ana Luísa Amaral, «Prece no Mediterrâneo», <i>Ágora</i>, Assírio &amp; Alvim, 2019. A lição{N}F05 diz onde ler o poema completo: cartão «O texto».',
    ('m8-u1', 'texto-4'): f'Ana Luísa Amaral, «A verdade histórica», em <i>PÁ: Poesia &amp; Outras Artes</i>, n.º{N}0, Casa Comum/U.Porto Press, setembro de 2023. A lição{N}F05 diz onde ler o poema completo: cartão «Outra leitura».',
    ('m8-u2', 'texto-1'): 'Maria Judite de Carvalho, «George», em <i>Seta Despedida</i>, Mem Martins, Europa-América, 1995. O conto completo lê-se no manual.',
}
# Onde uma lição diz que o texto se lê no manual: (lição, cartão, frase letra a letra).
NO_MANUAL = {('m8-u1', 'texto-1'): (F04, 4, 'Usa o texto publicado nessa página ou a edição do manual.'),
             ('m8-u2', 'texto-1'): (F12, 11, 'Para «George», usa a passagem do manual.')}
# 14/11/2026: a ordem de ler os poemas antes da aula (a do enunciado de antes, «Lê os poemas completos antes da aula», e a do guia),
# no primeiro cartão da m8-u1, à vista no ecrã e em papel.
ANTES_DA_AULA = 'Antes da aula, lê os dois poemas de cada tema.'
# 14/11/2026: na m8-u1, «manual» fica duas vezes à vista: a linha de fonte de «As Palavras» e a alínea de onde se leu (eram 10).
MANUAL_U1 = 2
# De onde vem o caso dos exemplos: os dados do aquecimento da mesma tarefa, letra a letra (fora as marcas de itálico _…_).
# 14/11/2026: só o caso vem do aquecimento. As frases dos exemplos já não copiam respostas do aquecimento (a objeção do ensaio
# habitual, que é a resposta certa da pergunta opcional; a frase de completar já preenchida; os passos de ordenar; a frase
# «a manhã passa de experiência a medida», quase a opção certa A): test_exemplos_com_outro_caso confere que nenhuma resposta do
# aquecimento aparece nos exemplos, o que é mais exigente do que conferir só a resposta certa da pergunta opcional.
EXEMPLOS_DO_AQUECIMENTO = {
    'm8-u1': ['Dois textos inventados: A. A janela bebe a manhã. B. A janela mede a manhã.'],
    'm8-u2': ['Caso inventado: Inês recebe um convite para cantar. Guarda-o no bolso e continua a ensaiar em voz baixa. O narrador não diz se ela '
              'aceita o convite.'],
}


def respostas_do_aquecimento(aq):
    """14/11/2026: as respostas que o aquecimento dá (sem as marcas _…_, em minúsculas): a opção certa de cada escolha, as palavras
    certas e a frase preenchida de cada cartão de completar, a frase revista de cada cartão de rever, cada passo de ordenar (sem o verbo
    de ordem do princípio) e cada par de emparelhar."""
    tira = lambda s: solto(re.sub(r'_([^_]+)_', r'\1', s)).strip().rstrip('.').lower()
    out = []
    for c in aq['cartoes']:
        if c['t'] == 'escolha':
            out.append(tira(c['o'][c['c']]))
        elif c['t'] == 'completar':
            frase = c['frase']
            for i, l in enumerate(c['lacunas'], 1):
                out.append(tira(l['o'][l['c']]))
                frase = frase.replace(f'[{i}]', l['o'][l['c']])
            out.append(tira(frase))
        elif c['t'] == 'rever':
            out.append(tira(c['o'][c['c']]))
            out.append(tira(c['frase'].replace(c['trecho'], c['o'][c['c']])))
        elif c['t'] == 'ordenar':
            out += [tira(x.split(' ', 1)[1]) for x in c['passos']]
        elif c['t'] == 'emparelhar':
            out += [tira(b) for a, b in c['pares']]
    return [x for x in out if x]
# As trocas de palavras das duas grelhas (página do aluno e versão de correção): as palavras do enunciado novo.
TROCAS_COMUNS = [
    ['com núcleo de planificação e síntese de duas linhas fora da contagem.', 'com plano e duas linhas finais. ' + NAO_CONTAM],
    ['extensão, identificação, núcleo ou síntese', 'extensão, identificação, plano ou duas linhas finais'],
    ['a identificação do tema, o núcleo e a síntese', 'a identificação do tema, o plano e as duas linhas finais'],
    ['separo dele o núcleo e as duas linhas finais', 'separo dele o plano e as duas linhas finais'],
    ['falta a contagem e o tema', 'falta a contagem e a letra do tema']]
TROCAS_GRELHA = {
    'm8-u1': TROCAS_COMUNS + [['Não identificar a edição consultada.', 'Não indicar onde leste os poemas (o manual ou outra edição).']],
    'm8-u2': TROCAS_COMUNS + [['Não identificar a edição consultada.', 'Não indicar onde leste o conto (o manual ou outra edição).'],
                              ['Repetir a tese como se fosse uma resposta.', 'Repetir a posição como se fosse uma resposta.']],
}
# As trocas das quatro páginas do módulo: (antes, depois, vezes). Aplicadas à base, dão a página da árvore, letra a letra.
TROCAS_MODULO = {
    GUIA: [
        (f'Seguem-se 5{N}minutos de leitura, 60 de produção individual em papel e 15 de revisão e entrega no Teams. O núcleo integra a planificação; não é uma resposta pronta.</p>',
         f'Seguem-se 10{N}minutos de leitura, 55 de produção individual em papel e 15 de revisão e entrega no Teams. O plano prepara o texto; não é uma resposta pronta. {NAO_CONTAM}</p>', 1),
        ('<p>Unidade 1: lê os dois poemas de cada tema nas lições F04 e F05 antes da aula. Os cartões «Outra leitura» são um primeiro contacto; as leituras completas continuam disponíveis nas fontes indicadas. Unidade 2: traz o conto «George» completo.</p>',
         # 14/11/2026: «O texto» e «Outra leitura», como no enunciado da m8-u1 (o poema 1 de cada lição está no cartão «O texto», o
         # poema 2 no cartão «Outra leitura»); a troca continua a conferir-se inteira, letra a letra.
         # 14/11/2026: sem «, no manual» depois de «antes da aula» (as lições só dizem que «As Palavras» está no manual; os cartões
         # dizem onde ler cada poema); a troca continua a conferir-se inteira, letra a letra.
         '<p>Unidade 1: lê os dois poemas de cada tema antes da aula. As lições F04 e F05 citam só alguns versos; os cartões «O texto» e «Outra leitura» dizem onde ler cada poema. Unidade 2: traz o conto «George» completo, no manual.</p>', 1),
        ('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica;</li><li>pergunta ao teu par de trabalho.</li></ol>',
         '<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica.</li></ol>', 1),
        (f'<b>Ler o enunciado, 5{N}min</b><span>Lê o núcleo comum e os temas A e B.</span>',
         f'<b>Ler o enunciado, 10{N}min</b><span>Lê os temas A e B, o que o plano leva e o que o texto leva.</span>', 1),
        (f'<b>Produzir, 60{N}min</b>', f'<b>Produzir, 55{N}min</b>', 1),
        ('[5, "Ler o enunciado", "Lê o núcleo comum e os temas A e B."], [60, "Produzir",',
         '[10, "Ler o enunciado", "Lê os temas A e B, o que o plano leva e o que o texto leva."], [55, "Produzir",', 1),
        ('<h2>Autoavaliação</h2>\n<p class="pequeno">Em cada parâmetro, toca no nível que achas que tens. O 4 é o melhor. Escreve uma linha a dizer porquê.</p>\n<div id="r-auto"></div>\n', '', 1),
        ('O docente vê o teu plano, as notas, a lista e a autoavaliação.</p>', 'O docente vê o teu plano, as notas e a lista.</p>', 1),
        ('''  $("#r-auto").innerHTML=atual.rubrica.map(function(p,i){var a=D.auto[i]||{};return '<p style="margin:10px 0 4px"><b>'+esc(p.nome)+'</b> <span class="pequeno">(extra sem nota)</span></p><div class="niveis" data-p="'+i+'">'+[4,3,2,1].map(function(n){return '<button aria-pressed="'+(a.n===n?"true":"false")+'" data-n="'+n+'">'+n+'</button>'}).join("")+'</div><textarea data-auto="'+i+'" placeholder="Porquê, numa linha." style="min-height:56px">'+esc(a.j||"")+'</textarea>'}).join("");\n''', '', 1),
        ('if(t.dataset.k){d().campos[t.dataset.k]=t.value;guardar()}if(t.dataset.auto!=null){var a=d().auto;a[t.dataset.auto]=a[t.dataset.auto]||{};a[t.dataset.auto].j=t.value;guardar()}});',
         'if(t.dataset.k){d().campos[t.dataset.k]=t.value;guardar()}});', 1),
        ('''document.addEventListener("click",function(ev){var b=ev.target.closest(".niveis button");if(!b||!atual)return;var p=b.parentNode.dataset.p;b.parentNode.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-pressed","false")});b.setAttribute("aria-pressed","true");var a=d().auto;a[p]=a[p]||{};a[p].n=Number(b.dataset.n);guardar()});\n''', '', 1),
        ('''")+p.nome)});l.push("","AUTOAVALIAÇÃO");\n  atual.rubrica.forEach(function(p,i){var a=D.auto[i]||{};l.push(p.nome+": nível "+(a.n||"-")+(a.j?" · "+a.j:""))});return l.join("\\n")}''',
         '''")+p.nome)});return l.join("\\n")}''', 1),
    ],
    INDICE: [
        ('aquecimento em cartões, planificação, tema A ou B, revisão e fotografias no Teams.', 'aquecimento em cartões, tema A ou B, plano, texto, revisão e fotografias no Teams.', 1),
        ('com consulta: aquecimento, planificação, tema A ou B, revisão e fotografias no Teams.', 'com consulta: aquecimento, tema A ou B, plano, texto, revisão e fotografias no Teams.', 2),
    ],
    MAPA: [('A síntese faz parte da entrega e não cria outro registo de conclusão.', 'As duas linhas finais fazem parte da entrega e não criam outro registo de conclusão.', 1)],
    PORTEFOLIO: [
        (': tema A ou B, núcleo, texto, duas linhas e autoavaliação /20.', ': tema A ou B, plano, texto e duas linhas finais.', 2),
        ('A tarefa da unidade inclui as duas linhas de síntese;', 'A tarefa da unidade inclui as duas linhas finais;', 1),
        ('autonomia, responsabilidade, trabalho de equipa, pensamento crítico', 'autonomia, responsabilidade, pensamento crítico', 1),
    ],
}
# As lições que o cartão «Rever a matéria» manda reler: (para, lição, título da lição, secções).
REVER = {
    'm8-u1': [(f'Tema{N}A', F04, 'Eugénio de Andrade: a palavra essencial', ['Para entender', 'Outra leitura']),
              (f'Tema{N}B', F05, 'Ana Luísa Amaral: reescrever a tradição', ['Para entender', 'Outra leitura']),
              ('O teu plano', F03, 'Jorge de Sena, poeta testemunha', ['Para entender']),
              ('O teu texto', F10, 'Poema com pintura ou álbum', ['Em paralelo'])],
    'm8-u2': [('O conto', F08, '«George», uma mulher em três idades', ['O essencial']),
              (f'Texto{N}1', F16, 'Recorte de «George»', ['Lê de perto', 'Para entender']),
              ('O teu texto', F12, 'Sugerir em vez de explicar', ['Compara']),
              ('A escrita', F06, 'Verbos que duram, palavras que apontam', ['Em paralelo'])],
}


def ler(rel):
    # 14/11/2026: os ficheiros que a camada do M9 muda leem-se como estavam por baixo dela (desfeita pela auditoria, com contagem
    # estrita); os outros, como estão na árvore.
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 15/11/2026: e, antes, a da tarefa m4-u2 (a mais recente), nos ficheiros que ela muda.
    if rel in M4U2_DE_CIMA or rel in SINTESE_DE_CIMA or rel in FILA_DE_CIMA:  # 15/11/2026: e os da camada das duas linhas finais, por cima de todas
        texto = undo_tarefa_m4u2_1115(rel, texto)
    if rel in M9_DE_CIMA:
        texto = undo_tarefas_faceis_m9_1114(rel, texto)
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
    """O ficheiro no commit de partida (os fluxos que correm este teste descarregam o histórico: fetch-depth: 0)."""
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    assert r.returncode == 0, f'{rel}: falta o commit de partida {BASE_COMMIT[:8]} (o fluxo tem de fazer checkout com fetch-depth: 0)'
    return r.stdout.decode('utf-8')


def visivel(fonte, so_main=True, sem_nav=True):
    """O texto que se lê numa página: sem scripts, estilos nem etiquetas, com os espaços normais juntos (U+00A0 fica)."""
    if so_main and '<main' in fonte:
        fonte = fonte[fonte.index('<main'):fonte.index('</main>')]
    fonte = re.sub(r'<(script|style)\b.*?</\1>', ' ', fonte, flags=re.S)
    if sem_nav:
        fonte = re.sub(r'<nav\b.*?</nav>', ' ', fonte, flags=re.S)
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fonte))).strip()


def solto(texto):
    return texto.replace(N, ' ')


def sem_marcas(texto):
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', texto)))


def cartoes(rel):
    """Os cartões de uma lição (CARTOES=[…], numa só linha do ficheiro)."""
    fonte = ler(rel)
    return json.JSONDecoder().raw_decode(fonte[fonte.index('CARTOES=[') + 8:])[0]


def blocos_onde(f):
    """Os blocos «Onde está o texto» dos dados, pela ordem da página (os dos temas e, depois, o que serve aos dois)."""
    return [o for t in f['temas'] for o in t['material'].get('onde', [])] + f.get('temas_material', {}).get('onde', [])


class Pagina(HTMLParser):
    """A estrutura de uma página de tarefa: os filhos de <main>, os temas, as perguntas com opções, os ids e as ligações."""

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


class TarefasFaceisM8(unittest.TestCase):
    maxDiff = None

    # ---------- a tarefa pede o mesmo ----------

    def test_a_tarefa_pede_o_mesmo(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            d, a = json.loads(ler(rel)), json.loads(antes(rel))
            f = d['facil']
            with self.subTest(tarefa=slug):
                # As chaves de antes ficam todas, iguais: a camada só acrescenta «facil», no fim. A base é o main de partida.
                self.assertNotIn('facil', a)
                self.assertEqual({k: v for k, v in d.items() if k != 'facil'}, a)
                self.assertEqual(list(d)[-1], 'facil')
                self.assertEqual(antes(rel), do_main(rel))
                # O título, as letras e os nomes dos dois temas.
                pagina, velha = ler(enunciado), do_main(enunciado)
                self.assertEqual(re.search(r'<h1>(.*?)</h1>', velha).group(1), re.search(r'<h1>(.*?)</h1>', pagina).group(1))
                self.assertEqual(re.search(r'<title>(.*?)</title>', velha).group(1), re.search(r'<title>(.*?)</title>', pagina).group(1))
                self.assertEqual([(t['letra'], t['nome']) for t in f['temas']], [(t['letra'], t['nome']) for t in a['temas']])
                self.assertEqual(re.findall(r'data-task-theme="([AB])"', pagina), ['A', 'B'])
                # Os números: 200 a 240 palavras, como no «lead» de antes, no quadro, junto do tema e do texto e na verificação.
                self.assertIn('<strong>200 a 240 palavras</strong>', solto(a['lead']))
                quadro = f['quadro']['linhas']
                self.assertEqual([solto(x[2]) for x in quadro], ['', '', '200 a 240', '', '200 a 240'])
                self.assertIn('200 a 240 palavras.', solto(f['temas_nota']))
                self.assertEqual(solto(f['depois'][1]['meta']), '200 a 240 palavras, sobre o tema A ou o tema B.')
                self.assertIn('Tenho 200 a 240 palavras, com o total no fim, e revi a escrita?', [solto(x) for x in f['verificar']])
                self.assertEqual(len(re.findall(r'\b\d+ a \d+\b', solto(visivel(pagina)))), solto(visivel(pagina)).count('200 a 240'))
                # Tudo o que o enunciado de antes citava entre «» continua pedido.
                pedido = solto(sem_marcas(json.dumps([f['temas'], f['depois'], f['finais'], f['entrega'], f['verificar']], ensure_ascii=False)))
                velho = solto(sem_marcas(' '.join(a['nucleo'] + [t['texto'] for t in a['temas']] + [a['clareza']['produto']])))
                citados = re.findall(r'«([^»]+)»', velho)
                self.assertGreaterEqual(len(citados), 1)
                for citado in citados:
                    self.assertIn(f'«{citado}»', pedido + solto(sem_marcas(json.dumps(f['fazer'], ensure_ascii=False))), citado)
                # Cada pedido do enunciado de antes, com as mesmas palavras, na página de antes e na de agora.
                self.assertGreaterEqual(len(PEDIDOS[slug]), 18)
                for pedaco in PEDIDOS[slug]:
                    self.assertIn(pedaco, solto(velha), pedaco)
                    self.assertIn(pedaco, solto(pagina), pedaco)
                # As alíneas do plano e do texto: os pedidos de antes, um por alínea; os passos de cada tema são as ordens do tema.
                self.assertEqual([p['nome'] for p in f['depois']], ['O teu plano', 'O teu texto'])
                self.assertEqual([p['alineas'] for p in f['depois']], ALINEAS[slug])
                self.assertEqual([t['passos'] for t in f['temas']], PASSOS[slug])
                for t, de_antes in zip(f['temas'], a['temas']):
                    for x in [t['intro']] + t['passos']:
                        self.assertIn(x.rstrip('.?').split(' ', 1)[1], solto(de_antes['texto']), x)
                # Um pedido por alínea: uma só frase, com um só ponto final (os dois pontos explicam, não juntam outro pedido).
                for p in f['depois']:
                    for x in p['alineas']:
                        self.assertEqual(len(re.findall(r'[.?!](?: |$)', x)), 1, x)
                        self.assertNotIn(';', x)
                # A pergunta das duas linhas finais é a de antes.
                pergunta = re.search(r'contagem do texto: (.*?\?)', a['fecho']).group(1)
                self.assertEqual(f['finais']['passos'], ['Responde: ' + pergunta, a['fecho'].split('? ')[1]])
                # A entrega é a de antes, em passos; a letra do tema escreve-se no topo, logo ao escolher.
                self.assertIn('Fotografa o plano, o texto e as duas linhas finais.', a['clareza']['entrega'])
                self.assertEqual(f['entrega'][0], 'Fotografa o plano, o texto e as duas linhas finais.')
                self.assertEqual(len(f['entrega']), 3)
                self.assertTrue(solto(f['temas_topo']).startswith('Escreve a letra do teu tema (A ou B) no topo.'))
                self.assertIn('o plano, o texto e as duas linhas finais', f['entregas']['intro'])
                # A pergunta opcional é a de antes (a página lê-a da chave antiga).
                self.assertNotIn('opcional', f)
                self.assertEqual(d['opcional'], a['opcional'])
                op = d['opcional']
                self.assertIn(html.escape(op['pergunta'], quote=False), pagina)
                for o in op['opcoes']:
                    self.assertIn(f'data-response="{o["resposta"]}"', pagina)
                # O dossiê antigo fica nos dados, igual, e já não aparece na página: as condições de consulta passaram a alíneas e a
                # linhas de ajuda; as ligações para as publicações continuam nas lições, para onde a página remete.
                self.assertEqual(d['dossie'], a['dossie'])
                self.assertNotIn('class="task-dossier', pagina)
                self.assertNotIn('tf-origem', pagina)
                for facto in d['dossie']:
                    if facto['href'].startswith('http'):
                        self.assertNotIn(facto['href'], pagina)
                        # (as publicações dos quatro poemas, com o mesmo endereço; da DGE, a lição F16 liga o excerto escrito do conto)
                        licoes = ''.join(ler(x) for x in (F04, F05, F08, F12, F16))
                        self.assertIn('//' + facto['href'].split('/')[2] + '/', licoes, facto['href'])
                        if slug == 'm8-u1':
                            self.assertIn(facto['href'].split('#')[0], licoes, facto['href'])
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        a1, a2 = (json.loads(antes(rel)) for rel in DADOS_TAREFAS)
        # m8-u1: as condições do dossiê de antes são agora alíneas (onde está cada indício; quatro versos no máximo; onde leste).
        self.assertIn('indica título e verso ou estrofe de cada indício. Cita no máximo quatro versos de cada poema. Se usares outro exemplar, regista a edição.',
                      a1['dossie'][4]['facto'])
        self.assertIn('Lê os poemas completos antes da aula.', a1['dossie'][4]['facto'])
        # 14/11/2026: no guia, sem «no manual» (as lições não dizem que os quatro poemas estão no manual); no enunciado, a mesma ordem.
        self.assertIn('lê os dois poemas de cada tema antes da aula. As lições F04 e F05 citam só alguns versos', ler(GUIA))
        self.assertNotIn('antes da aula, no manual', ler(GUIA))
        self.assertTrue(u1['modo'].startswith(ANTES_DA_AULA))
        # m8-u2: as condições do dossiê de antes são agora alíneas e linhas de ajuda.
        self.assertIn('Usa dois momentos distintos. A localização pode ser a página do teu exemplar e o início da passagem, sem copiar o conto. '
                      'Não é pedido qualquer relato da tua vida.', a2['dossie'][2]['facto'])
        self.assertEqual(u2['depois'][0]['ajudas'], ['Usa dois momentos distintos.', 'Basta o início de cada passagem: não copies o conto para o plano.'])
        self.assertEqual(u2['depois'][1]['ajudas'][-1], 'Não é pedido qualquer relato da tua vida.')
        self.assertIn('identifica editora, ano e páginas desse exemplar', a2['dossie'][0]['facto'])
        # As palavras difíceis ficam (são as da grelha) e levam uma linha de ajuda: «indício», «efeito», «objeção», «precisar».
        self.assertEqual(u1['depois'][0]['ajudas'], ['Um indício é uma palavra ou um verso do poema que apoia o que dizes.'])
        self.assertEqual(u1['depois'][1]['ajudas'], ['O efeito é o que o indício faz sentir ou pensar a quem lê.'])
        self.assertEqual(u2['depois'][1]['ajudas'][0], 'Uma objeção é o que diria quem não concorda contigo. A dificuldade do teu plano pode dar a objeção.')
        self.assertEqual(u2['finais']['texto'], 'Ficam fora da contagem. «Precisar a tua posição» quer dizer torná-la mais exata.')
        self.assertEqual(u1['grelha_nota'], 'A autoavaliação da grelha é só para ti: não se entrega. Na grelha, a tua apreciação chama-se «juízo crítico».')
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        self.assertEqual(grelhas['m8-u1']['criterios'][0]['nome'], 'Juízo crítico pertinente e desenvolvido')

    def test_criterios_da_grelha_iguais(self):
        agora, base = json.loads(ler(GRELHAS))['tarefas'], json.loads(antes(GRELHAS))['tarefas']
        self.assertEqual(antes(GRELHAS), do_main(GRELHAS))
        self.assertEqual(list(agora), list(base))
        novas = {'autoavaliacao_so_tua', 'correcao_estreita', 'trocas_aluno'}
        for slug, t in agora.items():
            with self.subTest(grelha=slug):
                # Nas duas grelhas do M8, só as três chaves novas; tudo o resto é a base, letra a letra (critérios, níveis, exemplos,
                # o que custa pontos e os pontos). As outras grelhas são as da base, sem exceção.
                self.assertEqual(set(t) - set(base[slug]), novas if slug in SLUGS else set())
                self.assertEqual({k: v for k, v in t.items() if k not in novas} if slug in SLUGS else t, base[slug])
                self.assertEqual(sum(c['max'] for c in t['criterios']), 20)
        self.assertEqual([c['max'] for c in agora['m8-u1']['criterios']], [4, 5, 5, 3, 3])
        self.assertEqual([c['max'] for c in agora['m8-u2']['criterios']], [3, 5, 6, 3, 3])
        for slug in SLUGS:
            t = agora[slug]
            self.assertIs(t['autoavaliacao_so_tua'], True)
            self.assertIs(t['correcao_estreita'], True)
            self.assertEqual(t['trocas_aluno'], TROCAS_GRELHA[slug])
            # As trocas são só as palavras que o enunciado novo trocou; cada uma ocorre nos textos da grelha.
            fonte = json.dumps({k: v for k, v in t.items() if k != 'trocas_aluno'}, ensure_ascii=False)
            for a, _ in t['trocas_aluno']:
                self.assertIn(a, fonte)
            # A página do aluno e a versão de correção são a base com as trocas e a decisão da autoavaliação, e mais nada: os nomes
            # dos critérios, os descritores e os exemplos leem-se como na base, com as palavras trocadas.
            for parte in ('grelha/', 'correcao/'):
                lida = solto(visivel(ler(f'tarefas/{slug}/{parte}index.html'), so_main=False, sem_nav=False))
                self.assertNotRegex(lida, r'(?i)\bnúcleo\b|\bsíntese\b|edição consultada|\btese\b|fora da contagem')
                for c in t['criterios']:
                    self.assertIn(c['nome'], lida)
            grelha = solto(visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False, sem_nav=False))
            esperado = json.dumps(base[slug], ensure_ascii=False)
            for a, b in t['trocas_aluno']:
                esperado = esperado.replace(json.dumps(a, ensure_ascii=False)[1:-1], json.dumps(b, ensure_ascii=False)[1:-1])
            esperado = json.loads(esperado)
            for c in esperado['criterios']:
                for desc, ex in c['niveis'].values():
                    self.assertIn(desc, grelha)
                    self.assertIn(ex, grelha)
                for x in c['custa']:
                    self.assertIn(x, grelha)
            self.assertIn(esperado['produto'], grelha)
            self.assertEqual(grelha.count(NAO_CONTAM), 1)
        for outra in OUTRAS:
            self.assertEqual(ler(f'tarefas/{outra}/grelha/index.html'), do_main(f'tarefas/{outra}/grelha/index.html'), outra)
            self.assertEqual(ler(f'tarefas/{outra}/correcao/index.html'), do_main(f'tarefas/{outra}/correcao/index.html'), outra)

    # ---------- os textos têm direitos de autor: não se copiam ----------

    def test_textos_com_direitos_so_as_citacoes_das_licoes_letra_a_letra(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            f = json.loads(ler(rel))['facil']
            pagina = ler(enunciado)
            principal = pagina[pagina.index('<main'):pagina.index('</main>')]
            blocos = blocos_onde(f)
            self.assertEqual([o['id'] for o in blocos], [x[0] for x in ONDE[slug]])
            # Nenhum texto copiado: a página não tem versos numerados, prosa copiada, imagens nem ligações para fora.
            self.assertEqual(f['textos'], [])
            for fora in ('class="tt-versos"', 'class="tt-prosa"', 'class="tt-texto', 'tt-estrofe', '<img', '<figure', 'data:image', 'href="http',
                         'ensina.rtp.pt', 'searanova', 'up.pt', 'dge.mec.pt', 'gutenberg', 'wikisource'):
                self.assertNotIn(fora, principal, fora)
            self.assertEqual(principal.count('<section class="tt-onde"'), len(blocos))
            self.assertEqual(principal.count('<blockquote class="tt-cit">'), len(blocos))
            for o, (ident, titulo, licao, k, forma, linhas, licao_fonte, k_fonte, fonte, (licao_morte, k_morte, frase_morte, ano)) in zip(blocos, ONDE[slug]):
                with self.subTest(tarefa=slug, texto=ident):
                    numero = ident[-1]
                    self.assertEqual(o['titulo'], f'<span class="tt-num">Texto{N}{numero}</span> {titulo}')
                    # O autor morreu depois de 1955 (di-lo a lição): o texto ainda tem direitos e não se reproduz.
                    self.assertIn(frase_morte, cartoes(licao_morte)[k_morte - 1]['html'])
                    self.assertGreater(ano, 1955)
                    self.assertIn(str(ano), frase_morte)
                    # A citação é a que a lição publica, letra a letra, no cartão indicado, na forma em que a lição a escreve.
                    self.assertEqual(len(o['citacoes']), 1)
                    cit = o['citacoes'][0]
                    self.assertEqual(cit['linhas'], linhas)
                    cartao = cartoes(licao)[k - 1]
                    self.assertEqual(cartao['t'], 'ler')
                    na_licao = {'barra': '«' + ' / '.join(linhas), 'br': '<blockquote class="verso">' + '<br>'.join(linhas) + '</blockquote>',
                                'prosa': '<blockquote class="prosa">' + linhas[0] + '</blockquote>'}[forma]
                    self.assertIn(na_licao, cartao['html'])
                    self.assertEqual(cit['intro'], ('Recorte' if forma == 'prosa' else 'Versos') + f' que a lição{N}F{licao[13:15]} cita:')
                    # É uma citação curta: quatro versos no máximo, ou um recorte de 25 palavras.
                    self.assertLessEqual(len(linhas), 4)
                    self.assertLessEqual(len(' '.join(linhas).split()), 25)
                    # A linha de fonte é a da lição (o seu princípio, letra a letra) e diz que o texto completo se lê no manual, sem
                    # número de página.
                    self.assertIn(fonte, cartoes(licao_fonte)[k_fonte - 1]['html'])
                    # 14/11/2026: a linha inteira, letra a letra (antes: o princípio da lição e «lê-se no manual» em todas).
                    self.assertTrue(o['fonte'].startswith(fonte), (o['fonte'], fonte))
                    self.assertEqual(o['fonte'], FONTE_PAGINA[(slug, ident)])
                    if (slug, ident) in NO_MANUAL:
                        # Diz que o texto se lê no manual só porque uma lição o diz.
                        l_m, k_m, frase_m = NO_MANUAL[(slug, ident)]
                        self.assertIn(frase_m, cartoes(l_m)[k_m - 1]['html'])
                        self.assertIn(' completo lê-se no manual.', o['fonte'])
                    else:
                        # Não diz que está no manual (nenhuma lição o diz); diz que cartão da lição dá a publicação, e esse cartão
                        # tem o nome, o título do poema e a ligação para a publicação.
                        self.assertNotIn('manual', o['fonte'])
                        rot = re.search(r'cartão «([^»]+)»\.$', o['fonte']).group(1)
                        self.assertIn(f'A lição{N}F{licao_fonte[13:15]} ', o['fonte'])
                        c_pub = cartoes(licao_fonte)[k_fonte - 1]
                        self.assertEqual(c_pub.get('rot'), rot)
                        self.assertIn(titulo.split('»')[0] + '»', c_pub['html'])
                        self.assertRegex(c_pub['html'], r'<a href="https://[^"]+" target="_blank" rel="noopener">Ler ')
                        manual_na_licao = [c for c in cartoes(licao_fonte) if titulo.split('»')[0][1:] in json.dumps(c, ensure_ascii=False) and 'manual' in json.dumps(c, ensure_ascii=False)]
                        self.assertEqual(manual_na_licao, [], ident)
                    self.assertNotRegex(solto(sem_marcas(o['fonte'])), r'(?i)\bpp?\. ?\d|\bpágina \d|\bpág')
                    self.assertIn(licao, o['origem'])
                    self.assertIn(f'cartão {k} ', o['origem'])
                    # Na página: o bloco com o número, o título, a citação (os versos, um por linha) e a linha de fonte.
                    bloco = re.search(r'<section class="tt-onde" id="' + ident + r'".*?</section>', pagina, re.S).group(0)
                    self.assertIn(f'<h3 id="{ident}-titulo">{o["titulo"]}</h3>', bloco)
                    self.assertIn(f'<p class="tf-p tt-cit-intro">{cit["intro"]}</p><blockquote class="tt-cit">' + '<br>'.join(linhas) + '</blockquote>', bloco)
                    self.assertIn(f'<p class="tt-fonte">{o["fonte"]}</p>', bloco)
                    self.assertEqual(pagina.count(f'id="{ident}"'), 1)
                    # Fora do bloco, nenhuma linha da citação aparece na página (nem nos exemplos, nem nos pedidos).
                    resto = pagina.replace(bloco, '')
                    # (as duas palavras de «as palavras.» são também do título da tarefa; confere-se a citação inteira)
                    for linha in linhas:
                        if len(linha.split()) >= 3:
                            self.assertNotIn(linha.strip('«».,'), resto, linha)
                    self.assertNotIn(linhas[0].strip('«».,'), resto)
            # Fora das citações, a página não tem nenhum verso nem frase dos textos: tudo o que está entre «» na página é um título, uma
            # palavra do enunciado ou uma frase dos exemplos (caso inventado).
            lido = solto(visivel(pagina))
            # 14/11/2026: na m8-u1, «manual» só fica onde uma lição o confirma («As Palavras») e na alínea e na pergunta de onde se leu.
            self.assertEqual(len(re.findall(r'\bmanual\b', lido)), {'m8-u1': MANUAL_U1, 'm8-u2': 6}[slug], slug)
            self.assertNotRegex(lido, r'(?i)\bpp?\. ?\d|\bpágina \d')
            self.assertIn('direitos de autor', lido)
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        # m8-u1: dois blocos em cada tema (no desdobrável do tema, que sai aberto em papel); a razão e a ordem dizem-se uma vez, no tema.
        self.assertEqual([[o['id'] for o in t['material']['onde']] for t in u1['temas']], [['texto-1', 'texto-2'], ['texto-3', 'texto-4']])
        self.assertNotIn('temas_material', u1)
        for t, k, licao in zip(u1['temas'], (1, 3), ('F04', 'F05')):
            # 14/11/2026: sem «lê-os no teu manual» (as lições só o dizem de «As Palavras»); a linha de fonte de cada bloco diz onde ler.
            self.assertEqual(t['antes'][0], 'Os dois poemas têm direitos de autor. Por isso não estão copiados nesta página. '
                             f'Vê <a href="#texto-{k}">onde ler cada poema</a>, por baixo dos passos.')
            self.assertEqual(t['material']['notas'], [])
            self.assertEqual([o['frases'] for o in t['material']['onde']], [[], []])
        for licao in (F04, F05):
            arr = cartoes(licao)
            self.assertEqual([c.get('rot') for c in arr if c.get('rot') in ('O texto', 'Outra leitura')], ['O texto', 'Outra leitura'])
            for c in arr:
                if c.get('rot') in ('O texto', 'Outra leitura'):
                    self.assertRegex(c['html'], r'<a href="https://[^"]+" target="_blank" rel="noopener">Ler ')
        self.assertIn('Usa o texto publicado nessa página ou a edição do manual.', cartoes(F04)[3]['html'])
        self.assertEqual(u1['temas'][1]['antes'][1], 'Uma prece é uma oração: um pedido. Um relato doméstico conta um caso passado em casa.')
        self.assertIn('É uma oração, dita por quem atravessa o mar.', cartoes(F05)[6]['html'])
        self.assertIn('Distingue o acontecimento doméstico da hipótese imaginada.', cartoes(F05)[23]['html'])
        # m8-u2: um bloco para os dois temas; di-lo o cartão dos temas, com a ligação.
        self.assertEqual([t['material'] for t in u2['temas']], [{}, {}])
        self.assertEqual([o['id'] for o in u2['temas_material']['onde']], ['texto-1'])
        self.assertEqual(u2['temas_material']['onde'][0]['frases'], ['Este conto tem direitos de autor. Por isso não está copiado aqui.'])
        self.assertEqual(u2['temas_topo'], f'Escreve a letra do teu tema (A{N}ou{N}B) no topo. O conto não está copiado nesta página: lê-o completo no teu manual. '
                         'Vê <a href="#texto-1">onde está o conto</a>, por baixo dos temas.')
        self.assertIn('Recorte de 25 palavras', cartoes(F16)[3]['html'])
        self.assertEqual(len(ONDE['m8-u2'][0][5][0].strip('«»').split()), 25)
        self.assertIn('Para «George», usa a passagem do manual.', cartoes(F12)[10]['html'])
        # O molde: «citacoes» e «onde» são chaves novas e opcionais; as páginas do M3 (que têm o bloco do Kit) saem iguais.
        molde = ler('scripts/tarefa_facil.py')
        self.assertIn("for c in o.get('citacoes', []))", molde)
        self.assertIn("''.join(onde_esta(x) for x in m.get('onde', []))", molde)
        self.assertEqual(ler('tarefas/m3-u1/index.html'), do_main('tarefas/m3-u1/index.html'))

    def test_exemplos_com_outro_caso(self):
        for slug, rel, enunciado, dados_aq in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS, DADOS_AQUECIMENTOS):
            d = json.loads(ler(rel))
            f = d['facil']
            pagina = ler(enunciado)
            aq = json.loads(ler(dados_aq))
            with self.subTest(tarefa=slug):
                # Um exemplo no plano e outro no texto, cada um num desdobrável fechado no ecrã que não sai em papel.
                self.assertEqual([len(p['exemplos']) for p in f['depois']], [1, 1])
                apoios = re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>Ver um exemplo com outro caso</summary>.*?</details>', pagina, re.S)
                self.assertEqual(len(apoios), 2)
                self.assertEqual(pagina.count('<aside class="tf-exemplo">'), 2)
                self.assertEqual(pagina.count('tf-so-ecra'), 3)  # os dois exemplos e a frase do quadro que fala deles
                juntos = solto(sem_marcas(' '.join(apoios)))
                # Nenhuma palavra reservada do aquecimento, nenhuma linha das citações, nenhum título nem autor dos textos da tarefa.
                for fora in aq['reservadas'] + [l for x in ONDE[slug] for l in x[5]] + ['Palavras', 'Prece', 'verdade histórica', 'George', 'Eugénio', 'Amaral',
                                                                                        'Judite', 'cristal', 'peixes', 'tigela', 'senhora', 'eufemismo', 'manual']:
                    self.assertNotIn(fora.strip('«».,'), juntos, fora)
                # O caso é o do aquecimento, com as suas frases, letra a letra.
                fonte_aq = solto(re.sub(r'_([^_]+)_', r'\1', json.dumps(aq, ensure_ascii=False)))
                for frase in EXEMPLOS_DO_AQUECIMENTO[slug]:
                    self.assertIn(frase, fonte_aq, frase)
                for x in f['depois']:
                    ex = x['exemplos'][0]
                    self.assertIn('outro caso', ex['titulo'])
                    self.assertTrue(ex['contexto'].startswith(EXEMPLOS_DO_AQUECIMENTO[slug][0]), ex['contexto'])
                    # Cada parágrafo diz a que alínea corresponde (é sempre outro caso: nenhuma alínea da tarefa fica feita).
                    rotulos = [solto(p['al']) for p in ex['paragrafos']]
                    for r in rotulos:
                        self.assertRegex(r, r'^Alíneas? [a-g]\)(?: e [a-g]\))?:$')
                    letras = set(re.findall(r'([a-g])\)', ' '.join(rotulos)))
                    self.assertLessEqual(len(letras), len(x['alineas']))
                    self.assertTrue(letras <= set('abcdefg'[:len(x['alineas'])]))
                # 14/11/2026: nenhuma resposta do aquecimento está nos exemplos (fora o caso, que é o mesmo), nem uma frase do aquecimento
                # já preenchida; e nenhuma frase dos exemplos (fora o contexto) está nos dados do aquecimento.
                juntos_min = juntos.lower()
                for r in respostas_do_aquecimento(aq):
                    self.assertNotIn(r, juntos_min.replace(EXEMPLOS_DO_AQUECIMENTO[slug][0].lower().rstrip('.'), ''), (slug, r))
                for x in f['depois']:
                    for par in x['exemplos'][0]['paragrafos']:
                        self.assertNotIn(solto(par['t']).rstrip('.'), fonte_aq, par['t'])
                # A resposta certa da pergunta opcional (que é também um cartão do aquecimento) não está nos exemplos.
                certa = [o['texto'] for o in d['opcional']['opcoes'] if o['certa']]
                self.assertEqual(len(certa), 1)
                self.assertNotIn(certa[0].rstrip('.'), juntos)
                self.assertNotIn(certa[0].rstrip('.').split(' ', 2)[-1], juntos)
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        self.assertEqual([p['t'] for p in u1['depois'][1]['exemplos'][0]['paragrafos']],
                         # 14/11/2026: frases novas, que não repetem a frase de completar do aquecimento já preenchida nem a opção certa A.
                         ['Em A, «bebe» faz a janela receber a manhã como quem tem sede. Em B, «mede» faz a janela olhar a manhã de fora, como uma régua.',
                          'Nos dois textos, a janela e a manhã são as mesmas. Só o verbo muda, e com ele a distância: A junta a janela à manhã, B separa-as.'])
        self.assertEqual([p['t'] for p in u2['depois'][1]['exemplos'][0]['paragrafos']],
                         # 14/11/2026: outra objeção (a voz baixa como receio), que não é a resposta certa da pergunta opcional, e uma
                         # resposta que não é a frase de completar do aquecimento já preenchida.
                         ['Há quem possa dizer que ensaiar em voz baixa mostra receio de cantar em público.',
                          'Mesmo com receio, Inês não para de ensaiar depois de guardar o convite: o receio não apaga a preparação.',
                          'O caso diz que Inês continua a ensaiar. Eu concluo que talvez se prepare para aceitar: o narrador não diz se ela aceita o convite.'])
        self.assertEqual([p['t'] for p in u2['depois'][0]['exemplos'][0]['paragrafos']][0::2],
                         ['Penso que Inês talvez se prepare para aceitar o convite.', 'Ensaiar em voz baixa pode mostrar receio de cantar em público.'])
        # As notas das grelhas continuam verdadeiras: os exemplos das grelhas são inventados e usam outros casos.
        for slug in SLUGS:
            self.assertIn('Os exemplos são inventados e usam outros casos. Não são respostas à tarefa.', json.loads(ler(GRELHAS))['tarefas'][slug]['nota'])

    # ---------- as decisões do docente ----------

    def test_tempos_10_10_55_15_em_todos_os_sitios(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            d = json.loads(ler(rel))
            f, pagina = d['facil'], ler(enunciado)
            with self.subTest(tarefa=slug):
                quadro = pagina[pagina.index('<table class="tf-quadro">'):pagina.index('</table>')]
                tempos = [int(x) for x in re.findall(r'<th scope="row">(\d+)' + N + 'min</th>', quadro)]
                self.assertEqual(tempos, [10, 10, 55, 15, 90])
                self.assertEqual(sum(tempos[:4]), 90)
                self.assertEqual([x[1] for x in f['quadro']['linhas']][:2] + [f['quadro']['linhas'][3][1], f['quadro']['linhas'][4][1]],
                                 ['Aquecimento em cartões', 'Leitura do enunciado', 'Revisão e entrega', 'Total'])
                self.assertEqual(d['aquecer']['minutos'], 10)
                self.assertEqual(f['producao_minutos'], 55)
                self.assertEqual(pagina.count('data-max="10" data-passo="1" data-rotulo="Aquecimento"'), 1)
                self.assertEqual(pagina.count('data-max="55" data-passo="5" data-rotulo="Produção em papel"'), 1)
                self.assertEqual(pagina.count('data-relogio'), 2)
                self.assertEqual(f['kicker'], f'Tarefa individual, 90{N}minutos')
                self.assertEqual(f['fazer'][0], f'Faz o aquecimento (10{N}minutos).')
        # Nenhum «5 min» nem «60 min» antigos nas páginas do M8 ligadas à tarefa (nem por extenso).
        for rel in PAGINAS + AQUECIMENTOS + [GUIA, MAPA, PORTEFOLIO]:
            lido = solto(visivel(ler(rel), so_main=False, sem_nav=False))
            self.assertNotRegex(lido, r'(?<![\d,])\b(?:5|60) min(?:utos)?\b|\b[Ss]essenta minutos|\b[Cc]inco minutos de leitura', rel)
        indice = ler(INDICE)
        chips = re.findall(r'<a class="cz-row" href="\.\./tarefas/m8-u\d/(aquecimento/)?">.*?<span class="chip">([^<]*)</span>', indice, re.S)
        self.assertEqual(chips, [('aquecimento/', f'10{N}min'), ('', f'90{N}min')] * 2)
        # O guia: o texto e os quatro blocos, na página e no relógio (BLOCOS), com os mesmos números.
        guia = ler(GUIA)
        self.assertIn(f'fazes os cartões durante 10{N}minutos. Seguem-se 10{N}minutos de leitura, 55 de produção individual em papel e 15 de revisão e entrega no Teams.', guia)
        blocos = json.JSONDecoder().raw_decode(guia.split('BLOCOS=', 1)[1])[0]
        self.assertEqual([b[0] for b in blocos], [10, 10, 55, 15])
        self.assertEqual(sum(b[0] for b in blocos), 90)
        self.assertEqual(re.findall(r'<b>([^<,]+), (\d+)' + N + r'min</b><span>([^<]*)</span>', guia), [(b[1], str(b[0]), b[2]) for b in blocos])
        self.assertIn('<span class="relogio" id="relogio">10:00</span>', guia)
        # Os aquecimentos do M8 já diziam «Dez minutos» e não falam da produção: ficam como no main.
        for rel in DADOS_AQUECIMENTOS:
            self.assertIn('Dez minutos com consulta, sem nota.', ler(rel))

    def test_consulta_contagem_autoavaliacao_e_aquecimento(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            f, pagina = json.loads(ler(rel))['facil'], ler(enunciado)
            lido = solto(visivel(pagina))
            with self.subTest(tarefa=slug):
                # «Com consulta» diz-se uma vez, no primeiro cartão, com o que quer dizer.
                # 14/11/2026: na m8-u1, a frase do «com consulta» vem depois da ordem de ler os poemas antes da aula; a frase fica igual.
                self.assertEqual(f['modo'], (ANTES_DA_AULA + ' ' if slug == 'm8-u1' else '') + CONSULTA)
                self.assertEqual(lido.count('com consulta'), 1)
                self.assertEqual(len(re.findall(r'\bconsultas?\b', lido.lower())), 1)
                cabeca = pagina[pagina.index('<header>'):pagina.index('</header>')]
                self.assertIn(f'<p class="tf-p">{f["modo"]}</p>', cabeca)
                # 14/11/2026: a ordem de ler os poemas antes da aula está no primeiro cartão (à vista e em papel: fora de .tf-so-ecra e
                # de qualquer desdobrável), uma só vez, e o guia diz o mesmo; na m8-u2 não há poemas.
                if slug == 'm8-u1':
                    self.assertEqual(lido.count(ANTES_DA_AULA), 1)
                    self.assertNotIn('<details', cabeca)
                    self.assertNotIn('tf-so-ecra', cabeca[:cabeca.index(ANTES_DA_AULA)].rsplit('<p', 1)[-1])
                    self.assertIn('lê os dois poemas de cada tema antes da aula.', ler(GUIA))
                else:
                    self.assertNotIn('antes da aula', lido)
                # O que não conta para as palavras: a mesma frase no enunciado, na grelha e no guia.
                self.assertEqual(f['quadro']['notas'][1], NAO_CONTAM)
                self.assertEqual(lido.count(NAO_CONTAM), 1)
                self.assertEqual(solto(visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False)).count(NAO_CONTAM), 1)
                self.assertEqual([p['meta'] for p in f['depois']][0], 'Não conta para as palavras.')
                self.assertEqual(f['finais']['texto'].split('.')[0], 'Ficam fora da contagem')
                # A autoavaliação da grelha é só para o aluno: não se entrega (enunciado, grelha e versão de correção).
                self.assertTrue(f['grelha_nota'].startswith('A autoavaliação da grelha é só para ti: não se entrega.'))
                self.assertEqual(lido.count('A autoavaliação da grelha é só para ti: não se entrega.'), 1)
                self.assertNotIn('autoavaliação', ' '.join(f['entrega'] + f['verificar'] + [f['entregas']['intro']]))
                grelha, correcao = ler(f'tarefas/{slug}/grelha/index.html'), ler(f'tarefas/{slug}/correcao/index.html')
                self.assertEqual(grelha.count('Esta autoavaliação é só para ti: não se entrega.'), 1)
                self.assertNotIn('Entrega esta autoavaliação', grelha)
                self.assertNotIn('<th class="n">Aluno</th>', correcao)
                self.assertNotIn('Diferença entre a tua nota e a minha', correcao)
                self.assertIn('<th class="n">Docente</th>', correcao)
                self.assertIn('<th class="n">Aluno</th>', do_main(f'tarefas/{slug}/correcao/index.html'))
                # O aquecimento é o primeiro passo, com uma só ligação.
                self.assertEqual(pagina.count('href="aquecimento/"'), 1)
                self.assertIn(f'<ol class="tf-fazer"><li>Faz o aquecimento (10{N}minutos).<span class="task-aquecer tf-abrir"><a href="aquecimento/">Abrir o aquecimento em cartões</a></span></li>', cabeca)
                self.assertNotIn('Antes de começar: aquecer', lido)
                # A verificação: dez perguntas de sim ou não, no máximo, na primeira pessoa.
                self.assertLessEqual(len(f['verificar']), 10)
                self.assertEqual(len(f['verificar']), 10)
                for x in f['verificar']:
                    self.assertTrue(x.endswith('?'), x)
                    self.assertEqual(x.count('?'), 1, x)
                    self.assertRegex(solto(x), r'\b(?:meu|minha|Tenho|Expliquei|Comparei|Citei|Indiquei|Escrevi|Anotei|Desenvolvi|Apresentei|Distingui|penso)\b', x)
                self.assertEqual(pagina.count('<label><input type="checkbox">'), 10)
                self.assertEqual(f['verificar_texto'], 'Responde sim ou não. Se for não, completa o teu trabalho.')
                # O primeiro cartão: o que vais fazer, o que entregas e o quadro, por esta ordem; a grelha fica ligada a seguir.
                ordem = [cabeca.index(x) for x in ('O que vais fazer</h2>', 'O que entregas</h2>', 'Tempo e tamanho</h2>', '<p class="task-grelha">')]
                self.assertEqual(ordem, sorted(ordem))
        self.assertEqual(solto(ler(GUIA)).count(NAO_CONTAM), 1)

    def test_tudo_junto_as_mesmas_palavras(self):
        # As palavras que o enunciado novo deixou de usar não aparecem em nenhuma página das duas tarefas nem no guia.
        for rel in PAGINAS + [GUIA]:
            lido = solto(visivel(ler(rel), so_main=False, sem_nav=False))
            with self.subTest(pagina=rel):
                self.assertNotRegex(lido, r'(?i)\bnúcleo\b|\bsíntese\b|\bplanificação\b|opção escolhida|edição consultada|publicação consultada|\bexemplar\b|par de poemas')
                self.assertNotRegex(lido, r'(?i)para todos\b|\bsó um\b|Relembrar|Fecha o trabalho')
        for slug in SLUGS:
            lido = solto(visivel(ler(f'tarefas/{slug}/index.html')))
            for palavra in ('plano', 'duas linhas finais', 'a letra do teu tema'):
                self.assertIn(palavra, lido, palavra)
            self.assertNotRegex(lido, r'(?i)\btese\b|\bopção\b')
            for parte in ('grelha/', 'correcao/'):
                self.assertIn('o plano e as duas linhas finais', solto(visivel(ler(f'tarefas/{slug}/{parte}index.html'), so_main=False)), parte)
        grelha_u1 = solto(visivel(ler('tarefas/m8-u1/grelha/index.html'), so_main=False))
        grelha_u2 = solto(visivel(ler('tarefas/m8-u2/grelha/index.html'), so_main=False))
        self.assertIn('Não indicar onde leste os poemas (o manual ou outra edição).', grelha_u1)
        self.assertIn('Não indicar onde leste o conto (o manual ou outra edição).', grelha_u2)
        self.assertIn('Repetir a posição como se fosse uma resposta.', grelha_u2)
        self.assertIn('falta a contagem e a letra do tema', grelha_u1)
        # As palavras da grelha que o enunciado usa: «indício», «efeito», «posição», «objeção», «momentos», e a ponte para «juízo crítico».
        for palavra in ('indício', 'efeito'):
            self.assertIn(palavra, grelha_u1)
            self.assertIn(palavra, solto(visivel(ler(ENUNCIADOS[0]))))
        for palavra in ('posição', 'objeção', 'momentos'):
            self.assertIn(palavra, grelha_u2)
            self.assertIn(palavra, solto(visivel(ler(ENUNCIADOS[1]))))
        self.assertIn('Na grelha, a tua apreciação chama-se «juízo crítico».', visivel(ler(ENUNCIADOS[0])))
        # O índice, o mapa e o portefólio do M8: as mesmas palavras nas frases que falam da aula de tarefa.
        indice = solto(visivel(ler(INDICE), so_main=False, sem_nav=False))
        self.assertEqual(indice.count('tema A ou B, plano, texto, revisão e fotografias no Teams.'), 3)
        self.assertNotIn('planificação', indice)
        mapa = solto(visivel(ler(MAPA), so_main=False, sem_nav=False))
        self.assertIn('As duas linhas finais fazem parte da entrega e não criam outro registo de conclusão.', mapa)
        self.assertNotIn('A síntese faz parte', mapa)
        self.assertEqual(mapa.count('30 %, individual, com consulta; grelha /20.'), 2)
        portefolio = solto(visivel(ler(PORTEFOLIO), so_main=False, sem_nav=False))
        self.assertEqual(portefolio.count('tema A ou B, plano, texto e duas linhas finais.'), 2)
        self.assertIn('A tarefa da unidade inclui as duas linhas finais;', portefolio)
        self.assertNotRegex(portefolio, r'(?i)\bnúcleo\b|duas linhas de síntese')
        # Os aquecimentos do M8 dizem a tarefa com as palavras do enunciado (um indício de cada poema; uma posição, dois momentos, a
        # objeção) e ficam como no main.
        self.assertIn('Na tarefa, relaciona um indício de cada poema', ler(DADOS_AQUECIMENTOS[0]))
        self.assertIn('Na tarefa, defende uma posição sobre dois momentos do conto e responde à objeção', ler(DADOS_AQUECIMENTOS[1]))
        for rel in AQUECIMENTOS + DADOS_AQUECIMENTOS:
            self.assertEqual(ler(rel), do_main(rel), rel)
            self.assertNotRegex(ler(rel), r'(?i)\bnúcleo\b|\bsíntese\b')

    def test_guia_portefolio_indice_e_mapa_so_mudam_nas_trocas_da_camada(self):
        for rel, trocas in TROCAS_MODULO.items():
            with self.subTest(pagina=rel):
                esperado = do_main(rel)
                self.assertEqual(esperado, antes(rel))
                for a, b, n in trocas:
                    self.assertEqual(esperado.count(a), n, a[:60])
                    esperado = esperado.replace(a, b)
                self.assertEqual(esperado, ler(rel))
        guia = ler(GUIA)
        # No guia saem a «Autoavaliação» que se copiava para o Teams e o par de trabalho; nada entra no lugar.
        lido = solto(visivel(guia, so_main=False, sem_nav=False))
        self.assertNotRegex(lido, r'(?i)autoavaliação|par de trabalho|Três antes de mim')
        self.assertNotIn('AUTOAVALIAÇÃO', guia)
        self.assertNotIn('r-auto', guia)
        self.assertNotIn('dataset.auto', guia)
        self.assertNotIn('closest(".niveis button")', guia)
        self.assertEqual(guia.count('<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica.</li></ol>Só depois levantas o braço.</div>'), 1)
        self.assertIn('"VERIFICAÇÃO"];', guia)
        self.assertIn('O docente vê o teu plano, as notas e a lista.', guia)
        self.assertEqual(len(TROCAS_MODULO[GUIA]), 12)
        # No portefólio saem «autoavaliação /20» e «trabalho de equipa»; nada entra no lugar.
        portefolio = solto(visivel(ler(PORTEFOLIO), so_main=False, sem_nav=False))
        self.assertNotRegex(portefolio, r'(?i)autoavaliação|trabalho de equipa|em equipa|em grupo|em pares')
        self.assertIn('É a base da avaliação qualitativa do módulo (40 %): autonomia, responsabilidade, pensamento crítico, entre outros.', portefolio)

    # ---------- as regras do texto ----------

    def test_regras_do_texto(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                texto = visivel(ler(rel))
                baixo = texto.lower()
                for palavra in ('professor', 'jogar', 'jogador', 'ficha', 'folha', 'em grupo', 'em pares', 'colega', 'fernandes'):
                    self.assertNotIn(palavra, baixo, palavra)
                self.assertNotRegex(baixo, r'\bjog(?:o|os|a|am|ar)\b')
                self.assertNotIn('—', texto)
                self.assertNotRegex(texto, r'\bQual (?!d[aeo]s? )')
                self.assertNotRegex(texto, r'\b[Vv]ocê\b')
        for slug in SLUGS:
            fonte = ler(f'tarefas/{slug}/index.html')
            texto = visivel(fonte)
            principal = fonte[fonte.index('<main'):fonte.index('</main>')]
            with self.subTest(enunciado=slug):
                # «·» só no molde comum (o título da janela e a navegação), nunca numa frase nossa; nenhum travessão nem meia-risca.
                self.assertNotIn('·', texto)
                self.assertNotRegex(texto, r'[—–]')
                # Títulos de livros em itálico; os títulos dos poemas e do conto ficam entre «».
                sem_italicos = re.sub(r'<i>[^<]*</i>|alt="[^"]*"|aria-label="[^"]*"', '', principal)
                for obra in ('Os Amantes sem Dinheiro', 'Ágora', 'Poesia &amp; Outras Artes', 'Seta Despedida', 'Até Amanhã'):
                    self.assertNotIn(obra, sem_italicos, obra)
                for obra in (('<i>Os Amantes sem Dinheiro</i>', '<i>Ágora</i>', '<i>PÁ: Poesia &amp; Outras Artes</i>') if slug == 'm8-u1' else ('<i>Seta Despedida</i>',)):
                    self.assertEqual(principal.count(obra), 1, obra)
                for titulo in ('As Palavras', 'Adeus', 'Prece no Mediterrâneo', 'A verdade histórica') if slug == 'm8-u1' else ('George',):
                    self.assertGreaterEqual(texto.count(f'«{titulo}»'), 2, titulo)
                    if titulo != 'George':  # (George é também o nome da personagem)
                        self.assertNotRegex(texto, r'(?<!«)' + re.escape(titulo) + r'(?!»)', titulo)
                # Referências que não se partem (U+00A0), como nas páginas do M3, do M1, do M5, do M6 e do M7.
                for padrao in (r'\b(?:Texto|Textos|Pergunta|pergunta|Tema|Temas|tema|Lição|lição|verso|versos|aula|Passo|Passos|Alínea|Alíneas|alínea|Estrofe|parágrafo|parágrafos|passagem|parte|partes) (?:\d|[AB]\b|[IVX]+\b|F\d|[a-h]\)|\[)',
                               r'\d (?:min|minutos|palavras|versos)\b', r'(?:\d|\]|\)) (?:a|e|ou) (?:\d|\[|[a-h]\))', r'\bA (?:ou|e) B\b', r'\bn\.º \d'):
                    # (o «Tema » que só os leitores de ecrã leem antes da letra de cada tema, no molde comum, fica de fora)
                    self.assertNotRegex(visivel(fonte.replace('<span class="sr-only">Tema </span>', '')), padrao)
                # As falas do aluno em discurso direto ficam entre «» (nenhuma aspa direita nem curva nas nossas frases).
                self.assertNotRegex(texto, r'[“”"]')
                # Sem trabalho de grupo nem de pares; tu sem género.
                self.assertNotRegex(texto.lower(), r'\bsozinh[oa]\b|\bo aluno\b|\ba aluna\b|\bpar de\b|\bem equipa\b')
        # «n.º 0» (o número da revista) vem da linha de fonte da lição F05, letra a letra, com o espaço que não parte.
        self.assertIn(f'n.º{N}0, Casa Comum/U.Porto Press', cartoes(F05)[23]['html'])
        self.assertIn(f'n.º{N}0, Casa Comum/U.Porto Press', ler(ENUNCIADOS[0]))
        # O molde não é o piloto por aprovar: os comentários dizem que foi aprovado.
        for rel in ('scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py', 'scripts/grelhas_tarefas.py', 'assets/task-textos.css', 'scripts/tarefas_faceis_m8_20261113.py'):
            self.assertNotIn('por aprovar', ler(rel), rel)

    # ---------- o contrato da página (substitui o de tests/test_task_choice.py nestas duas tarefas) ----------

    def test_contrato_da_pagina(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            d = json.loads(ler(rel))
            f, fonte = d['facil'], ler(enunciado)
            p = Pagina(fonte)
            with self.subTest(tarefa=slug):
                self.assertEqual(fonte.count('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil '
                                             'data-task-opening="Começar" data-task-index="nomes">'), 1)
                # Seis cartões com nome, pela ordem: o primeiro é o cabeçalho («Começar»).
                self.assertEqual([x[0] for x in p.raiz], ['nav', 'header', 'section', 'section', 'section', 'section', 'section'])
                self.assertEqual(['Começar'] + [x[2] for x in p.raiz if x[0] == 'section'], CARTOES_NOMES)
                self.assertEqual([x[1] for x in p.raiz if x[0] == 'section'], ['tema', 'o-teu-plano', 'o-teu-texto', 'entregar', 'apoios'])
                for nome in CARTOES_NOMES:
                    self.assertNotRegex(nome, '[\xa0⁠]')
                self.assertEqual(len(p.ids), len(set(p.ids)), [x for x in p.ids if p.ids.count(x) > 1])
                # Dois temas; uma pergunta opcional com três opções, uma certa, dentro do desdobrável do último cartão.
                self.assertEqual(p.temas, ['A', 'B'])
                self.assertEqual(p.perguntas, [('1', True)])
                self.assertEqual(len(p.opcoes), 3)
                self.assertEqual([o['data-correct'] for o in p.opcoes].count('true'), 1)
                self.assertEqual(fonte.count('<details data-task-optional-preparation><summary>Experimentar uma pergunta</summary>'), 1)
                # O relógio de produção fica no cartão dos temas (escolhe-se primeiro), antes dos temas.
                tema = fonte[fonte.index('<section class="task-section tf-tema"'):fonte.index('<section class="task-section tf-pergunta" id="o-teu-plano"')]
                self.assertLess(tema.index('data-rotulo="Produção em papel"'), tema.index('<div class="task-themes">'))
                self.assertIn(f'data-chave="pt-relogio:tarefas/{slug}:producao"', tema)
                self.assertIn('<p class="tf-nota tf-relogio-nota" id="produzir">Começa este relógio depois da leitura.</p>', tema)
                # As ligações: as internas têm alvo na página; as outras são páginas do sítio que existem; nenhuma sai do sítio.
                principal = fonte[fonte.index('<main'):fonte.index('</main>')]
                for href in re.findall(r'<a href="([^"]+)"', principal):
                    if href.startswith('#'):
                        self.assertIn(href[1:], p.ids, href)
                    else:
                        self.assertFalse(href.startswith('http'), href)
                        alvo = (ROOT / 'tarefas' / slug / href.split('#')[0]).resolve()
                        self.assertTrue((alvo / 'index.html').is_file() if not alvo.suffix else alvo.is_file(), href)
                self.assertEqual(len(re.findall(r'<a href="#texto-\d">', principal)), 2 if slug == 'm8-u1' else 1)
                # A folha: só as duas páginas do M8 pedem a versão facil-12, com as regras das citações.
                self.assertEqual(f['folha_versao'], '20261113-facil-12')
                self.assertEqual(fonte.count('assets/task-textos.css?v=20261113-facil-12"'), 1)
                self.assertEqual(fonte.count('task-textos.css'), 1)
                self.assertIn('assets/task-reader.js?v=20261112-facil-7"', fonte)
                # Os desdobráveis: o material dos temas (aberto em papel), os dois exemplos (só no ecrã) e a pergunta opcional.
                self.assertEqual(fonte.count('<details'), 5 if slug == 'm8-u1' else 4)
                self.assertEqual(fonte.count('<details class="tf-so-tema">'), 2 if slug == 'm8-u1' else 0)
                self.assertEqual(fonte.count('<details class="tf-so-tema tf-dois-temas">'), 0 if slug == 'm8-u1' else 1)
                # O botão de imprimir e a ligação à grelha, no primeiro cartão.
                self.assertEqual(fonte.count('<button type="button" data-task-print hidden>Imprimir o enunciado</button>'), 1)
                self.assertEqual(fonte.count('<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>'), 1)
                # «Rever a matéria»: uma linha por tema ou parte; cada lição existe, tem o título dito e as secções que se mandam reler.
                self.assertEqual([x['para'] for x in f['rever']], [x[0] for x in REVER[slug]])
                for x, (para, licao, titulo, seccoes) in zip(f['rever'], REVER[slug]):
                    numero = licao[13:15]
                    self.assertTrue(x['texto'].startswith(f'Lição{N}F{numero}, <a href="../../m8/licao-m8-f{numero}/">{titulo}</a>'), x['texto'])
                    self.assertTrue((ROOT / licao).is_file())
                    arr = cartoes(licao)
                    self.assertEqual(html.unescape(arr[0]['titulo']), titulo, licao)
                    rotulos = [c.get('rot') for c in arr if c['t'] == 'ler']
                    for s in seccoes:
                        self.assertIn(f'«{s}»', x['texto'])
                        self.assertIn(s, rotulos, (licao, s))
                    self.assertEqual(re.findall(r'Relê (.*?)[:.]', x['texto'])[0].count('«') >= len(seccoes), True)
        # O que as linhas de «Rever» dizem de cada secção está na lição.
        self.assertIn('cita pouco e sempre com o número do verso', cartoes(F03)[7]['html'])
        self.assertIn('<b>Observação:</b>', cartoes(F10)[2]['html'])
        self.assertIn('<b>Ligação possível:</b>', cartoes(F10)[2]['html'])
        self.assertIn('separas facto verificável, inferência a discutir, interpretação a defender com provas e opinião', cartoes(F08)[1]['html'])
        self.assertIn('Distingue o que o texto afirma do que inferes', cartoes(F12)[10]['html'])
        self.assertIn('«nele» retoma o espelho', cartoes(F06)[2]['html'])
        # A folha de estilos: as regras novas são só para classes que as outras páginas não têm.
        folha = ler('assets/task-textos.css')
        novas = folha[folha.index('/* 13/11/2026: o M8 no mesmo molde'):]
        self.assertTrue(do_main('assets/task-textos.css') + '\n' + novas == folha)
        for regra in re.findall(r'(\[data-task-facil\][^{]*)\{', novas):
            self.assertRegex(regra, r'\.tt-cit|\.tt-onde')
        for slug in OUTRAS:
            self.assertNotIn('tt-cit', ler(f'tarefas/{slug}/index.html'))
            self.assertNotIn('facil-12', ler(f'tarefas/{slug}/index.html'))

    # ---------- as outras tarefas não mudam ----------

    def test_as_outras_tarefas_nao_mudam(self):
        r = subprocess.run(['git', 'ls-tree', '-r', '--name-only', BASE_COMMIT, 'tarefas', 'docs/pedagogia/tarefas-escolha', 'docs/pedagogia/aquecimentos',
                            'docs/pedagogia/tarefas-individuais', GRELHAS], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        nomes = r.stdout.split()
        self.assertGreater(len(nomes), 100)
        na_arvore = sorted(p.relative_to(ROOT).as_posix() for pasta in ('tarefas', 'docs/pedagogia/tarefas-escolha', 'docs/pedagogia/aquecimentos',
                                                                      'docs/pedagogia/tarefas-individuais') for p in (ROOT / pasta).rglob('*') if p.is_file())
        # 15/11/2026: na árvore há um ficheiro novo, os dados da m4-u2 (tests/test_tarefas_faceis_m4.py confere-o); todos os outros são os do main.
        self.assertEqual(sorted(n for n in nomes if n != GRELHAS), [x for x in na_arvore if x != DADOS_M4U2])
        self.assertIn(DADOS_M4U2, na_arvore)
        iguais = 0
        for rel in nomes:
            if rel in FICHEIROS:
                continue
            with self.subTest(igual_ao_main=rel):
                # 14/11/2026: os ficheiros que a camada do M9 muda comparam-se com ela desfeita (ler), com contagem estrita.
                # 15/11/2026: e os que a camada da tarefa m4-u2 muda, com ela desfeita (ler), com contagem estrita.
                # 15/11/2026: e os ficheiros da camada das duas linhas finais (sintese_duas_linhas_20261115), por cima de todas, com a mesma exigência.
                self.assertEqual(ler(rel).encode('utf-8') if rel in M9_DE_CIMA or rel in M4U2_DE_CIMA or rel in SINTESE_DE_CIMA or rel in FILA_DE_CIMA else (ROOT / rel).read_bytes(),
                                 subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True).stdout)
                iguais += 1
        # Nestas pastas, a camada muda nove ficheiros: os dados das grelhas e, de cada tarefa do M8, os dados, o enunciado, a grelha e a
        # versão de correção. Todos os outros são os do main, byte a byte: as outras onze tarefas de escolha, as duas individuais do M7,
        # as suas grelhas, correções e aquecimentos, e os aquecimentos do M8.
        self.assertEqual(iguais, len(nomes) - 9)
        self.assertEqual(sorted(f for f in FICHEIROS if f in nomes), sorted(DADOS_TAREFAS + [GRELHAS] + PAGINAS))
        for rel in AQUECIMENTOS + DADOS_AQUECIMENTOS + ['tarefas/m9-u1/index.html', 'tarefas/m7-u3/index.html', 'tarefas/m3-u1/index.html', 'tarefas/m7-u1/index.html']:
            self.assertIn(rel, nomes)
            self.assertNotIn(rel, FICHEIROS)
        # As outras tarefas de escolha: as que já estavam no molde continuam com a sua folha; a m9-u1 e a m9-u2 continuam fora dele.
        for slug in OUTRAS:
            dados = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            self.assertEqual('facil' in dados, not slug.startswith('m9'), slug)
        # Os quatro geradores, com os dados da árvore, dão todas as páginas da árvore, byte a byte.
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/tarefas_individuais_faceis.py', '--saida', tmp], ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            self.assertGreaterEqual(len(geradas), 13 + 26 + 2 + 20)
            for slug in OUTRAS + SLUGS:
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertIn(f'tarefas/{slug}/{parte}index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    # 14/11/2026: com os dados da árvore (já com a camada do M9), as páginas da árvore, byte a byte.
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())

    # ---------- a camada ----------

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 14/11/2026: por cima desta ficam as duas tarefas do M9 mais fáceis de fazer (tarefas_faceis_m9_20261114): esta passa a ser a
        # segunda, logo abaixo, sem nada pelo meio; a ordem ganha mais uma posição, com a mesma exigência.
        # 15/11/2026: por cima das tarefas do M9 mais fáceis de fazer fica a tarefa m4-u2 com «Tema A ou B» e o acerto do M8 (tarefa_m4u2_tema_b_20261115): a ordem ganha mais uma posição, com a mesma exigência.
        # 15/11/2026: por cima da tarefa m4-u2 fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115): a ordem ganha mais uma posição, com a mesma exigência.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertEqual(verificar_camadas.LAYERS[0], ('fila_final_20261115', 'fila-final-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('sintese_duas_linhas_20261115', 'sintese-duas-linhas-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefa_m4u2_tema_b_20261115', 'tarefa-m4u2-tema-b-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('tarefas_faceis_m9_20261114', 'tarefas-faceis-m9-edits-20261114'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('tarefas_faceis_m8_20261113', 'tarefas-faceis-m8-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        # 15/11/2026: mais uma camada, sintese_duas_linhas_20261115, no topo.
        # 15/11/2026: mais uma camada, fila_final_20261115, no topo.
        self.assertEqual(len(verificar_camadas.LAYERS), 56)
        # 15/11/2026: mais uma camada, sintese_duas_linhas_20261115, no topo.
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 56)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertIn('não se edita à mão', MANIFESTO['_nota'])
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(len(FICHEIROS), 13)
        self.assertEqual(len(set(FICHEIROS)), 13)
        self.assertEqual(len(TROCAS), sum(len(v['edits']) for v in MANIFESTO['files'].values()))
        # 14/11/2026: confere-se com a camada do M9, que fica por cima, desfeita primeiro (sem nada pelo meio).
        # 15/11/2026: por cima da tarefa m4-u2 fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar', '--desfazer-antes', M9F_fila, '--desfazer-antes', M9F_sintese, '--desfazer-antes', M9F_m4u2, '--desfazer-antes', M9F],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 13 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        for t in TROCAS:
            self.assertTrue(t['achado'].startswith('13/11/2026: '), t['local'])
            self.assertEqual(t['ocorrencias'], 1)
            self.assertNotIn('—', t['local'])
        # Ida e volta, letra a letra: a árvore é o «after» do manifesto; desfeita a camada, cada ficheiro é a base, que é o ficheiro
        # do main de partida, byte a byte; voltando a aplicar, é outra vez a árvore.
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
                self.assertEqual(do_main(rel), base)
                # O desfazer da auditoria dá o mesmo, e não desfaz nada segunda vez.
                self.assertEqual(undo_tarefas_faceis_m8_1113(rel, atual), base)
                self.assertEqual(undo_tarefas_faceis_m8_1113(rel, base), base)
        # Com as camadas das tarefas do M7, do M6, do M5, do M1 e do M3, que ficam por baixo, partilha só os dados das grelhas. Aí, o
        # desfazer da auditoria tira primeiro esta e depois as outras, até à grelha sem nenhuma das chaves novas.
        m7, m3 = (json.loads(ler(x))['files'] for x in (M7F, M3F))
        self.assertEqual(set(MANIFESTO['files']) & set(m7), {GRELHAS})
        self.assertEqual(set(MANIFESTO['files']) & set(m3), {GRELHAS})
        self.assertEqual(sha_lf(antes(GRELHAS)), m7[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m7_1113(GRELHAS, ler(GRELHAS))), m7[GRELHAS]['base_sha256_lf'])
        sem_todas = undo_tarefas_faceis_m3_1112(GRELHAS, ler(GRELHAS))
        self.assertEqual(sha_lf(sem_todas), m3[GRELHAS]['base_sha256_lf'])
        for chave in ('autoavaliacao_so_tua', 'trocas_aluno'):
            self.assertNotIn(chave, sem_todas)
        for rel in MANIFESTO['files']:
            if rel != GRELHAS:
                for desfazer in (undo_tarefas_faceis_m7_1113, undo_tarefas_faceis_m3_1112):
                    self.assertEqual(desfazer(rel, ler(rel)), antes(rel), rel)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m8_20261113', ROOT / 'scripts/tarefas_faceis_m8_20261113.py')
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        todas, finais = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', ler(CAMADA_REL))
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(sorted(C.FICHEIROS), sorted(FICHEIROS))
        self.assertEqual(C.BASE_COMMIT, BASE_COMMIT)
        for rel, (a, b) in finais.items():
            self.assertEqual(a, antes(rel), rel)
            self.assertEqual(b, ler(rel), rel)
        # As camadas de baixo que partilham os dados das grelhas com esta continuam a dar o seu JSON, com esta desfeita primeiro.
        for nome in ('tarefas_faceis_m7_20261113', 'tarefas_faceis_m6_20261113', 'tarefas_faceis_m5_20261113', 'tarefas_faceis_m1_20261113',
                     'tarefas_faceis_m3_20261112'):
            spec = importlib.util.spec_from_file_location(nome, ROOT / f'scripts/{nome}.py')
            outra = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(outra)
            self.assertEqual(outra.construir()[0], json.loads(ler(f'scripts/{nome}.json')), nome)
        # E a decisão 152 no M8, que partilha com esta as páginas e os dados das duas tarefas e as quatro páginas do módulo.
        spec = importlib.util.spec_from_file_location('cuidado_m8_20261112', ROOT / 'scripts/cuidado_m8_20261112.py')
        cuidado = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cuidado)
        self.assertEqual(cuidado.construir()[0], json.loads(ler('scripts/cuidado_m8_20261112.json')))
        partilhados = set(MANIFESTO['files']) & set(json.loads(ler('tests/fixtures/cuidado-m8-edits-20261112.json'))['files'])
        self.assertTrue({GUIA, INDICE, MAPA, PORTEFOLIO} <= partilhados, partilhados)

    def test_leitura_historica_dos_enunciados(self):
        # Os contratos históricos leem as tarefas como eram antes do pedido #192 (scripts/tarefas_claras_historico.py). Com esta camada
        # por cima, a leitura dá a base do manifesto do #192, letra a letra, nos enunciados e nos dados da M8-U1 e da M8-U2, a partir
        # da página inteira ou com esta camada já desfeita; e não desfaz nada segunda vez.
        import tarefas_claras_historico as historico
        claras = json.loads(ler('tests/fixtures/tarefas-claras-edits-20261110.json'))['files']
        nossos = sorted(set(MANIFESTO['files']) & set(claras))
        self.assertEqual(nossos, sorted(DADOS_TAREFAS + ENUNCIADOS))
        for rel in nossos:
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                antes_192 = historico.desfazer(rel, atual)
                self.assertEqual(sha_lf(antes_192), claras[rel]['base_sha256_lf'])
                self.assertEqual(historico.desfazer(rel, antes(rel)), antes_192)
                self.assertEqual(historico.desfazer(rel, antes_192), antes_192)
        m3 = json.loads(ler(M3F))['files']
        for rel in MANIFESTO['files']:
            with self.subTest(faceis=rel):
                sem = historico.desfazer_faceis(rel, ler(rel))
                # Nos ficheiros que só esta camada muda, a leitura tira esta e dá a base; nos dados das grelhas, que partilha com as
                # do M7, do M6, do M5, do M1 e do M3, tira as seis, pela ordem.
                esperado = m3[rel]['base_sha256_lf'] if rel == GRELHAS else MANIFESTO['files'][rel]['base_sha256_lf']
                self.assertEqual(sha_lf(sem), esperado)
                self.assertEqual(historico.desfazer_faceis(rel, sem), sem)
                if rel != GRELHAS:
                    self.assertEqual(sem, antes(rel))
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer_faceis(path, text):'):fonte.index('def desfazer(path, text):')]
        self.assertLess(corpo.index('TAREFAS_FACEIS_M8.get(rel)'), corpo.index('TAREFAS_FACEIS_M7.get(rel)'))
        self.assertLess(corpo.index('TAREFAS_FACEIS_M7.get(rel)'), corpo.index('TAREFAS_FACEIS_M6.get(rel)'))
        self.assertIn("_sha_lf(text) == por_cima['after_sha256_lf']", corpo)
        self.assertIn("assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M8 mais fáceis de fazer não confere: {rel}'", corpo)

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        # A auditoria desfaz primeiro esta camada; o corte da Sala também; as bases das camadas que partilham ficheiros com ela também.
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_tarefas_faceis_m8_1113(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m7_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m8_1113\(path, text\)\n')
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m6_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m7_1113\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('tarefas-faceis-m8-edits-20261113.json'), sala.index('tarefas-faceis-m7-edits-20261113.json'))
        self.assertIn("raise ManifestoDesatualizado(f'{rel}: tarefas do M8 mais fáceis de fazer não confere')", sala)
        for rel in ('scripts/cuidado_m6_20261108.py', 'scripts/cuidado_m7_20261111.py', 'scripts/cuidado_m8_20261112.py'):
            self.assertIn('return desfazer_faceis(rel, (ROOT / rel).read_bytes().decode(\'utf-8\'))', ler(rel), rel)
        indices = ler('scripts/cartaz_indices_148_20261106.py')
        corpo = indices[indices.index('def base(rel):'):]
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M8.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M7.read_text'))
        for rel in ('scripts/tarefas_faceis_m3_20261112.py', 'scripts/tarefas_faceis_m1_20261113.py', 'scripts/tarefas_faceis_m5_20261113.py',
                    'scripts/tarefas_faceis_m6_20261113.py', 'scripts/tarefas_faceis_m7_20261113.py'):
            fonte = ler(rel)
            leitura = fonte[fonte.index('def ler(rel):'):fonte.index('def base(rel):')]
            self.assertIn("m8 = ROOT / 'tests/fixtures/tarefas-faceis-m8-edits-20261113.json'", leitura, rel)
            if 'm7 = ROOT' in leitura:
                self.assertLess(leitura.index("m8 = ROOT / 'tests/fixtures/tarefas-faceis-m8-edits-20261113.json'"),
                                leitura.index("m7 = ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'"), rel)
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs', 'tests/browser_creditos_i_pt1.cjs'):
            texto = ler(rel)
            self.assertEqual(texto.count('for(const e of [...((tarefasFaceisM8['), 1, rel)
            self.assertLess(texto.index('((tarefasFaceisM8['), texto.index('((tarefasFaceisM7['), rel)
        # Em todos os fluxos e em todos os testes: onde a camada do M7 se desfaz, a do M8 desfaz-se logo antes, sem nada pelo meio, e
        # é sempre a primeira da cadeia.
        fluxos = sorted((ROOT / '.github/workflows').glob('*.yml'))
        com_cadeia = 0
        for p in fluxos:
            fluxo = p.read_text('utf-8')
            self.assertEqual(fluxo.count(f'--desfazer-antes {M7F}'), fluxo.count(f'--desfazer-antes {meu} --desfazer-antes {M7F}'), p.name)
            # 14/11/2026: logo antes desta, a do M9 (a mais recente), sem nada pelo meio.
            # 15/11/2026: por cima das tarefas do M9 mais fáceis de fazer fica a tarefa m4-u2 com «Tema A ou B» e o acerto do M8 (tarefa_m4u2_tema_b_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 15/11/2026: por cima da tarefa m4-u2 fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            self.assertEqual(fluxo.count(f'--desfazer-antes {meu}'), fluxo.count(f'--verificar --desfazer-antes {M9F_fila} --desfazer-antes {M9F_sintese} --desfazer-antes {M9F_m4u2} --desfazer-antes {M9F} --desfazer-antes {meu}'), p.name)
            self.assertEqual(fluxo.count("'scripts/tarefas_faceis_m7_20261113.*'"), fluxo.count("'scripts/tarefas_faceis_m8_20261113.*'"), p.name)
            self.assertEqual(fluxo.count("'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'"), fluxo.count("'tests/fixtures/tarefas-faceis-m8-edits-20261113.json'"), p.name)
            self.assertEqual(fluxo.count("- 'tests/test_tarefas_faceis_m7.py'"), fluxo.count("- 'tests/test_tarefas_faceis_m8.py'"), p.name)
            self.assertEqual(fluxo.count("- 'tests/browser_tarefas_faceis_m7.py'"), fluxo.count("- 'tests/browser_tarefas_faceis_m8.py'"), p.name)
            com_cadeia += bool(fluxo.count(f'--desfazer-antes {meu}'))
        self.assertEqual(com_cadeia, 7)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name in ('test_tarefas_faceis_m8.py', 'test_tarefas_faceis_m7.py'):
                continue
            texto = p.read_text('utf-8')
            with self.subTest(teste=p.name):
                self.assertEqual(texto.count(f"'--desfazer-antes', '{M7F}'"), texto.count(f"'--desfazer-antes', '{meu}', '--desfazer-antes', '{M7F}'"))
                self.assertEqual(texto.count(f'--desfazer-antes {M7F}'), texto.count(f'--desfazer-antes {meu} --desfazer-antes {M7F}'))
                for velho, novo in (('t7', 't8f'), ('T7', 'T8F'), ('M7F', 'M8F')):
                    self.assertEqual(texto.count('--desfazer-antes {%s}' % velho), texto.count('--desfazer-antes {%s} --desfazer-antes {%s}' % (novo, velho)))
                    self.assertEqual(texto.count("'--desfazer-antes', %s," % velho) + texto.count("'--desfazer-antes', %s]" % velho),
                                     texto.count("'--desfazer-antes', %s, '--desfazer-antes', %s," % (novo, velho))
                                     + texto.count("'--desfazer-antes', %s, '--desfazer-antes', %s]" % (novo, velho)))
        # O fluxo das aulas de tarefa: confere a camada do M7 com esta desfeita primeiro, depois esta sem nada por cima, com o seu teste
        # e o seu teste de navegador; os caminhos do fluxo incluem os ficheiros desta camada; o limite de tempo não muda.
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        # 14/11/2026: com a camada do M9 por cima, desfeita primeiro em todas as cadeias.
        # 15/11/2026: por cima das tarefas do M9 mais fáceis de fazer fica a tarefa m4-u2 com «Tema A ou B» e o acerto do M8 (tarefa_m4u2_tema_b_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima da tarefa m4-u2 fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m7_20261113.json --manifesto {M7F} --verificar --desfazer-antes {M9F_fila} --desfazer-antes {M9F_sintese} --desfazer-antes {M9F_m4u2} --desfazer-antes {M9F} --desfazer-antes {meu}\n', tarefas)
        # 15/11/2026: por cima das tarefas do M9 mais fáceis de fazer fica a tarefa m4-u2 com «Tema A ou B» e o acerto do M8 (tarefa_m4u2_tema_b_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima da tarefa m4-u2 fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py {CAMADA_REL} --manifesto {meu} --verificar --desfazer-antes {M9F_fila} --desfazer-antes {M9F_sintese} --desfazer-antes {M9F_m4u2} --desfazer-antes {M9F}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m8.py' -v\n", tarefas)
        self.assertIn('      - name: Tarefas do M8 mais fáceis de fazer\n        run: python tests/browser_tarefas_faceis_m8.py\n', tarefas)
        self.assertLess(tarefas.index("-p 'test_tarefas_faceis_m7.py'"), tarefas.index("-p 'test_tarefas_faceis_m8.py'"))
        for caminho in ("'m8/**'", "'tarefas/m8-u1/**'", "'tarefas/m8-u2/**'", "'scripts/tarefa_facil.py'", "'assets/task-textos.css'",
                        "'docs/pedagogia/tarefas-escolha/**'", "'docs/pedagogia/grelhas-tarefas-20261027.json'"):
            self.assertIn(f'      - {caminho}\n', tarefas, caminho)
        self.assertEqual(tarefas.count('timeout-minutes: 40'), 1)
        self.assertEqual(do_main('.github/workflows/pt-tarefas-qa.yml').count('timeout-minutes: 40'), 1)
        self.assertEqual(re.findall(r'timeout-minutes: \d+', tarefas), re.findall(r'timeout-minutes: \d+', do_main('.github/workflows/pt-tarefas-qa.yml')))
        # Este teste lê o main de partida (git show): o trabalho que o corre descarrega o histórico (fetch-depth: 0), e é o único fluxo
        # que o corre.
        trabalho = tarefas[tarefas.index('  lessons:'):]
        self.assertLess(trabalho.index('fetch-depth: 0'), trabalho.index('actions/setup-python'))
        correm = [p.name for p in fluxos if "-p 'test_tarefas_faceis_m8.py'" in p.read_text('utf-8') or re.search(r'unittest discover -s tests(?: -v)?\s*$', p.read_text('utf-8'), re.M)]
        self.assertEqual(correm, ['pt-tarefas-qa.yml'])


if __name__ == '__main__':
    unittest.main()
