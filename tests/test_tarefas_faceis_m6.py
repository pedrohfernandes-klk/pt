"""13/11/2026: as duas tarefas do M6 (m6-u1 e m6-u2) «mais fáceis de fazer» e «tudo junto» no M6 (camada tarefas_faceis_m6_20261113).

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201) e levado ao M1 (pedido #203) e ao M5
(pedido #204). Esta camada leva-o ao M6, e este ficheiro exige das duas tarefas do M6 o que tests/test_tarefas_faceis_m3.py,
tests/test_tarefas_faceis_m1.py e tests/test_tarefas_faceis_m5.py exigem das do M3, do M1 e do M5:

* a tarefa pede o mesmo: os títulos, os nomes e as letras dos temas, os números de palavras, os versos e os títulos que o enunciado
  de antes citava, cada pedido do enunciado de antes (com as mesmas palavras), o dossiê e a pergunta opcional, e os critérios,
  níveis, exemplos e pontos da grelha, iguais aos de antes da camada (a base do manifesto, o main 02606259), salvo os cinco exemplos
  da grelha da m6-u2 que usavam versos ou palavras dos textos da tarefa e a nota que os anuncia (EXEMPLOS_TROCADOS, conferidos um a
  um). Duas decisões do
  docente: na m6-u2, o étimo de «cheio» e de «pleno» é dado no enunciado, e «algo que não podes fotografar» passa a «o que a imagem
  não mostra»; na m6-u1, «para que serve o sonho» diz-se no enunciado e na grelha;
* os textos para análise são os das lições do M6, letra a letra, na grafia das lições: cada verso da página é um verso de um cartão
  da lição, pela ordem, com o vocabulário e a linha de fonte da lição; a página mostra-os junto da pergunta ou do tema que os usa;
  o que as lições não dão não se copiou de fora: o verso 13 de «A um poeta» e os cortes de «Ao Gás» saem como «[…]», e a linha de
  fonte de cada texto di-lo e remete para o manual, sem número de página; não há imagens;
* as decisões do docente, em todos os sítios: tempos 10/10/55/15 (quadro, relógios, guia), nenhum «5 min» nem «60 min» antigos nas
  páginas do M6 ligadas à tarefa; «com consulta» dito uma vez, no primeiro cartão; os versos citados ou copiados não contam para as
  palavras; a autoavaliação da grelha não se entrega (enunciado, grelha e correção); o aquecimento com uma só ligação; no máximo 10
  perguntas de sim ou não na verificação; as mesmas palavras no enunciado, na grelha, na correção, no aquecimento, no guia, no
  índice e no mapa;
* no guia da tarefa do M6 saem a «Autoavaliação» que se copiava para o Teams e «pergunta ao teu par de trabalho» (a regra passa a
  chamar-se «Dois antes de mim»), e o resto do guia é o do main de partida, letra a letra, salvo as trocas da camada;
* no portefólio do M6 saem a autoavaliação de 0 a 20 por parâmetro e «trabalho de equipa», sem nada no lugar; o resto da página é o
  do main de partida, letra a letra;
* as regras do texto: sem as palavras proibidas, sem «·» nem «—» nas nossas frases (nos versos de Antero e de Cesário ficam como no
  original), «Que + nome» ou «Qual das…», referências que não se partem, títulos de livros em itálico, exemplos com outro caso;
* o contrato da página, que substitui o de tests/test_task_choice.py nestas duas tarefas: seis cartões com nome, dois temas, uma
  pergunta opcional com três opções, os dois relógios, os factos do dossiê com fonte e ligação que existe, as citações e os
  números de cada facto na lição para onde aponta, os nomes das secções tal como estão nas lições ligadas;
* as tarefas, grelhas, correções e aquecimentos dos outros módulos são os do main de partida, byte a byte, e saem iguais dos
  geradores;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base, gerador que dá o mesmo JSON, registada na
  auditoria (desfazer), em scripts/desligar_sala.py, na leitura histórica dos enunciados e nas cadeias e caminhos dos fluxos.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em
tests/browser_tarefas_faceis_m6.py."""
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
from auditoria_20261028 import undo_tarefas_faceis_m6_1113, undo_tarefas_faceis_m5_1113, undo_tarefas_faceis_m1_1113, undo_tarefas_faceis_m3_1112  # noqa: E402
import verificar_camadas  # noqa: E402
# 13/11/2026: por cima de todas ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113, com o seu teste,
# tests/test_tarefas_faceis_m7.py). Este teste lê os ficheiros que essa camada muda (os dados das grelhas, os dados e as páginas das
# tarefas do M7) como estavam por baixo dela: desfeita pela auditoria, com contagem estrita. A exigência é a mesma.
from auditoria_20261028 import undo_tarefas_faceis_m7_1113  # noqa: E402
M7_DE_CIMA = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json').read_text('utf-8'))['files']

CAMADA_REL = 'scripts/tarefas_faceis_m6_20261113.json'
MANIFESTO_REL = 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'
M5F = 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
M7F = 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'  # 13/11/2026: a camada das tarefas do M7 mais fáceis de fazer, a mais recente
M1F = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
M3F = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
BASE_COMMIT = '02606259c78dd8ddec2572c6f1a38f4771509f34'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
TROCAS = json.loads((ROOT / CAMADA_REL).read_text('utf-8'))
SLUGS = ('m6-u1', 'm6-u2')
N = '\xa0'
DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DADOS_AQUECIMENTOS = [f'docs/pedagogia/aquecimentos/{s}.json' for s in SLUGS]
ENUNCIADOS = [f'tarefas/{s}/index.html' for s in SLUGS]
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'aquecimento/', 'correcao/')]
AQUECIMENTOS = [f'tarefas/{s}/aquecimento/index.html' for s in SLUGS]
GUIA, INDICE, MAPA = 'm6/guia-da-tarefa-m6/index.html', 'm6/index.html', 'm6/mapa-do-modulo-m6/index.html'
PORTEFOLIO = 'm6/portefolio-do-modulo-m6/index.html'
FICHEIROS = DADOS_TAREFAS + [GRELHAS] + DADOS_AQUECIMENTOS + PAGINAS + [GUIA, INDICE, MAPA, PORTEFOLIO]
# As outras onze tarefas que saem de scripts/tarefas_escolha.py (as do M3, do M1 e do M5 já estão no molde, pelas suas camadas).
OUTRAS = ('m1-u1', 'm1-u2', 'm3-u1', 'm3-u2', 'm5-u1', 'm5-u2', 'm7-u3', 'm8-u1', 'm8-u2', 'm9-u1', 'm9-u2')
NO_MOLDE = ('m1-u1', 'm1-u2', 'm3-u1', 'm3-u2', 'm5-u1', 'm5-u2')
FOLHA = {'m1-u1': 'facil-8', 'm1-u2': 'facil-8', 'm3-u1': 'facil-7', 'm3-u2': 'facil-7', 'm5-u1': 'facil-9', 'm5-u2': 'facil-9'}
CARTOES_NOMES = ['Começar', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Fechar e entregar', 'Rever a matéria']
F01, F02, F04, F05, F06, F07, F12, F13 = (f'm6/licao-m6-f{n}/index.html' for n in ('01', '02', '04', '05', '06', '07', '12', '13'))
# O que cada enunciado de antes pedia, com as suas palavras: cada pedaço está no enunciado de antes e continua no de agora.
PEDIDOS = {
    'm6-u1': ['ndica a quem se dirige a voz', 'para que serve o sonho', 'ita um verso dos tercetos', 'ponta uma semelhança', 'xplica uma diferença',
              '«Singram soberbas naus que eu não verei jámais!» («Ave-Marias»)', 'em orações', 'lassifica',
              'ustifica com a função de «que» na sua oração', 'xplica o que essa oração acrescenta',
              'Reconta «O Palacio da Ventura» em prosa, numa situação atual.', 'Escolhe um ideal e um lugar concretos.',
              'Conta a procura, a chegada e a abertura da porta.', 'A última frase deve contrariar o que se esperava.',
              'Cria uma anáfora ou uma antítese, sem copiar versos para a tua narrativa.', 'o verso de Antero que imitaste',
              'ndica uma diferença entre o teu ideal e o do cavaleiro.',
              'Planeia um vídeo de um minuto sobre «O Palacio da Ventura». Entregas a descrição escrita dos planos.', 'Descreve três planos',
              'ssocia um verso exato a cada', 'Explica se o último plano ilustra, contraria ou acrescenta algo ao verso.',
              'Justifica uma escolha com dois factos do', 'Indica o que o vídeo não pode apresentar como facto.'],
    'm6-u2': ['Classifica a oração com «que»', "«Quizera que o real e a analyse m'o dessem» («Ao Gás»)",
              'estrofe de «Horas Mortas» que termina em «Amarelladamente, os cães parecem lobos.»',
              'istingue o que o sujeito observa daquilo em que o transforma', 'dentifica dois recursos', 'xplica os efeitos',
              'iz se o olhar ultrapassa o real.', '(«Cheio de bellas proporções carnaes») e «pleno» («O sol, já alto e pleno»)', 'com o étimo',
              'via seguiu cada palavra', 'Escreve «bellas» e «Pousára» na grafia atual', 'xplica as mudanças.',
              'Narra em prosa a tua passagem a pé por um lugar, a uma hora definida.', 'duas sensações de sentidos diferentes',
              'uma figura social atual, caracterizada por um gesto.', 'Transforma pela imaginação algo que observas, à maneira de Cesário.',
              'o verso que imitaste', 'ndica uma diferença entre a tua cidade e a dele.',
              'Escolhe duas partes de «O Sentimento dum Ocidental» e imagina uma fotografia atual para cada uma. Entregas as descrições e legendas.',
              'Descreve cada fotografia, com lugar e hora.', 'Legenda-a com um verso exato e o nome da parte do poema.',
              'Explica uma relação entre imagem e verso que vá além de mostrar literalmente as mesmas coisas.',
              'Justifica uma escolha com dois factos do', 'e explica porquê.'],
}
# De onde vem cada texto: a lição, os cartões «O texto» (pela ordem) e as estrofes desses cartões que entram (None: todas); o cartão
# do vocabulário e da linha de fonte, e as palavras do vocabulário que cabem ao texto (None: todas).
TEXTOS = {
    'm6-u1': {'texto-1': (F02, (3, 9), None, 9, None), 'texto-3': (F06, (3, 8, 12, 16), (5,), 16, ['baixeis', 'singram']),
              'texto-4': (F01, (4, 14), None, 14, None)},
    'm6-u2': {'texto-1': (F07, (14, 16, 18), (3,), 18, ['exarcebe', 'analyse', 'ratoneiro imberbe']),
              'texto-2': (F07, (20, 22, 24, 26), (8,), 26, ['dubios', 'osseos']),
              'texto-3': (F06, (3, 8, 12, 16), None, 16, None), 'texto-4': (F07, (3, 6, 9, 13), None, 13, None),
              'texto-5': (F07, (14, 16, 18), None, 18, None), 'texto-6': (F07, (20, 22, 24, 26), None, 26, None)},
}
# Os versos de cada texto (as linhas «[…]» à parte) e as estrofes.
VERSOS = {'m6-u1': {'texto-1': (14, [4, 4, 3, 3]), 'texto-2': (13, [4, 4, 3, 3]), 'texto-3': (4, [4]), 'texto-4': (14, [4, 4, 3, 3])},
          'm6-u2': {'texto-1': (4, [4]), 'texto-2': (4, [4]), 'texto-3': (44, [4] * 11), 'texto-4': (44, [4] * 11),
                    'texto-5': (20, [4, 1, 4, 4, 1, 4, 4]), 'texto-6': (44, [4] * 11)}}
TITULOS = {
    'm6-u1': ['«Ideal», de Antero de Quental', '«A um poeta», de Antero de Quental', '«Ave-Marias», uma estrofe, de Cesário Verde',
              '«O Palacio da Ventura», de Antero de Quental'],
    'm6-u2': ['«Ao Gás», uma estrofe, de Cesário Verde', '«Horas Mortas», uma estrofe, de Cesário Verde',
              '«O Sentimento dum Ocidental», parte I, «Ave-Marias», de Cesário Verde',
              '«O Sentimento dum Ocidental», parte II, «Noite Fechada», de Cesário Verde',
              '«O Sentimento dum Ocidental», parte III, «Ao Gás» (excertos), de Cesário Verde',
              '«O Sentimento dum Ocidental», parte IV, «Horas Mortas», de Cesário Verde'],
}
# O que a página junta à linha de fonte da lição: diz de onde é a estrofe, ou o que as lições não dão (nada se copiou de fora).
FONTE_MAIS = {
    ('m6-u1', 'texto-3'): ' É a estrofe dos versos 21 a 24 de «Ave-Marias», a primeira parte do poema.',
    ('m6-u2', 'texto-1'): ' É uma estrofe de «Ao Gás», a parte III do poema (está também no <a href="#texto-5">Texto 5</a>).',
    ('m6-u2', 'texto-2'): ' É uma estrofe de «Horas Mortas», a parte IV do poema (está também no <a href="#texto-6">Texto 6</a>).',
    ('m6-u2', 'texto-3'): ' A parte I, inteira.', ('m6-u2', 'texto-4'): ' A parte II, inteira.',
    # 13/11/2026: revisão. Com estrofes saltadas, um número contado por cima dos cortes não era o número do verso na parte: o Texto 5
    # deixa de ter números e a linha de fonte di-lo (a exigência fica mais forte: confere-se também que não há nenhum número).
    ('m6-u2', 'texto-5'): ' As lições dão cinco estrofes da parte III; «[…]» marca o que as lições saltam. Por isso estes versos não têm '
                          'número. A parte inteira está no manual.',
    ('m6-u2', 'texto-6'): ' A parte IV, inteira.',
}
# Com as quatro partes de «O Sentimento dum Ocidental» na página da m6-u2, estes exemplos da grelha usavam versos ou palavras desses
# textos. A regra do docente é «exemplos sempre com outro caso, sem as passagens da tarefa»: passam a usar versos de «Num Bairro
# Moderno» (lição F12) e grafias da lição F05 que não estão nos textos da tarefa. São as únicas diferenças nos textos das duas grelhas,
# conferidas uma a uma (antes, depois); os critérios, os níveis e os pontos ficam iguais.
EXEMPLOS_TROCADOS = {
    'm6-u1': [],
    'm6-u2': [
        ('Em «Um sopro que arripia os hombros quasi nús.», a oração com «que» é completiva, porque começa por «que».',
         'Em «Nós levantámos todo aquelle peso / Que ao chão de pedra resistia preso,», a oração com «que» é completiva, porque começa por «que».'),
        ('Noutro verso de «Ao Gás», em «Um sopro que arripia os hombros quasi nús.», a oração com «que» é subordinada adjetiva relativa restritiva: '
         '«que» retoma «sopro» e é sujeito de «arripia». E «Num Bairro Moderno» volta ao real: «Nós levantámos todo aquelle peso» é um gesto.',
         'Noutro poema, «Num Bairro Moderno», em «Nós levantámos todo aquelle peso / Que ao chão de pedra resistia preso,», a oração com «que» é '
         'subordinada adjetiva relativa restritiva: «que» retoma «peso» e é sujeito de «resistia». E o poema volta ao real: levantar o peso é um gesto.'),
        ('Fecho: Passei a ver as montras quando as luzes se apagam. Ensinou-me «Tornam-se mausoléos as armações fulgentes.».',
         'Fecho: Passei a ver o branco das paredes quando o sol lhes bate. Ensinou-me «E fere a vista, com brancuras quentes,».'),
        ('Chave veio pela via popular e clave pela erudita. «Edade-média» hoje escreve-se Idade Média.',
         'Chave veio pela via popular e clave pela erudita. «Occidental» hoje escreve-se ocidental.'),
        ('E de 1887: «Edade-média» passa a Idade Média (a vogal inicial fixou-se em i, o hífen caiu e Média leva maiúscula); «oxygenio» passa a '
         'oxigénio (o y passou a i, com acento gráfico).',
         # 13/11/2026: revisão. «lyrios» não é uma grafia de 1887 (é de «Ideal», na edição de 1886): a lição F05 dá as duas como
         # grafias «do século XIX», e o exemplo passa a dizer o que a lição diz.
         'E do século XIX: «occidental» passa a ocidental (perdeu um c); «lyrios» passa a lírios (o y passou a i, com acento gráfico).'),
        # 13/11/2026: revisão. A nota da grelha que anuncia os exemplos diz o mesmo.
        ('(outra estrofe, outro verso, outras palavras de 1887, outro poema para fotografar)',
         '(outra estrofe, outro verso, outras palavras do século XIX, outro poema para fotografar)'),
    ],
}
# De onde vem cada citação nova dos exemplos: (lição, citação), letra a letra na lição e fora dos textos da tarefa.
EXEMPLOS_DAS_LICOES = {
    'm6-u1': [('m6/licao-m6-f02/index.html', 'Dorme o teu somno, coração liberto,'), ('m6/licao-m6-f07/index.html', 'Triste cidade! Eu temo que me avives'),
              ('m3/licao-m3-f09/index.html', 'Roga a Deus, que teus anos encurtou,')],
    'm6-u2': [(F12, 'Nós levantámos todo aquelle peso'), (F12, 'Que ao chão de pedra resistia preso,'), (F12, 'E fere a vista, com brancuras quentes,'),
              (F05, '«occidental», grafia de 1887, perdeu um'), (F05, 'passou a _i_ em «lyrios», «lírios»'),
              # 13/11/2026: revisão. A lição dá as duas grafias como «do século XIX».
              (F05, '«Occidental», «melancholia», «lyrios», «sómente», «egrejas»: grafias do século XIX')],
}
TROCAS_COMUNS = [
    ['Núcleo comum (duas respostas) e um tema à escolha (A ou B)', 'Duas perguntas e um tema à escolha (A ou B)'],
    ['Respostas articuladas', 'Respostas ligadas'], ['o tema no topo', 'a letra do tema no topo'],
    ['o tema escolhido está no topo', 'a letra do teu tema está no topo'],
    ['Não escrever no topo o tema escolhido (A ou B).', 'Não escrever no topo a letra do teu tema (A ou B).'],
    ['Fecho: ', 'Duas linhas finais: '], ['Fecho genérico, sem verso.', 'Duas linhas finais genéricas, sem verso.']]
TROCAS_U1 = [
    ['nem o que é o sonho ou o ideal', 'nem para que serve o sonho'], ['e o que é o sonho ou o ideal', 'e para que serve o sonho'],
    ['no papel do sonho', 'naquilo para que serve o sonho'],
    # 13/11/2026: revisão, «tudo junto». A grelha e a versão de correção passam a usar as palavras do enunciado: «a quem se dirige a
    # voz», «uma diferença», «a função de «que»» e «recontar».
    ['a quem fala a voz', 'a quem se dirige a voz'], ['uma semelhança e o que muda', 'uma semelhança e uma diferença'],
    ['não explicas o que muda', 'não explicas a diferença'], ['ou o que muda não se apoia', 'ou a diferença não se apoia'],
    ['o que muda de um soneto para o outro', 'uma diferença de um soneto para o outro'],
    ['não dizer o que muda', 'não dizer a diferença'],
    ['Dizer o que muda sem um verso que o mostre', 'Dizer a diferença sem um verso que a mostre'],
    ['com o papel de «que»', 'com a função de «que»'], ['outro soneto para reescrever', 'outro soneto para recontar']]
TROCAS_U2 = [
    ['o que não podes fotografar, e porquê', 'o que a imagem não mostra, e porquê'],
    ['Não posso fotografar a insegurança de que fala o verso', 'A imagem não mostra a insegurança de que fala o verso'],
    ['Inventar um étimo, em vez de o procurar na lição.', 'Usar outro étimo, em vez do que o enunciado dá.']]


def ler(rel):
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    if rel in M7_DE_CIMA:  # 13/11/2026: como estava por baixo da camada do M7
        texto = undo_tarefas_faceis_m7_1113(rel, texto)
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
    """A página sem os versos de Antero e de Cesário (só eles: o título, o vocabulário e a fonte de cada texto ficam)."""
    return re.sub(r'<div class="tt-versos">.*?</div>', ' ', fonte, flags=re.S)


def solto(texto):
    return texto.replace(N, ' ')


def sem_marcas(texto):
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', texto)))


def cartoes(rel):
    """Os cartões de uma lição (CARTOES=[…], numa só linha do ficheiro)."""
    fonte = ler(rel)
    i = fonte.index('CARTOES=[')
    return json.JSONDecoder().raw_decode(fonte[i + 8:])[0]


def estrofes_da_licao(rel, numeros):
    """As estrofes dos cartões «O texto» de uma lição, tal como lá estão, pela ordem: uma lista de listas de versos; a linha «[…]» da
    lição (um corte) fica sozinha, como ['[…]']. As estrofes separam-se onde a lição salta um índice de linha."""
    arr = cartoes(rel)
    linhas = []
    for k in numeros:
        c = arr[k - 1]
        assert c['t'] == 'ler' and c['rot'].startswith('O texto, '), (rel, k)
        v = re.search(r'<p class="v">(.*?)</p>', c['html'], re.S).group(1)
        for m in re.finditer(r'<span class="ln" data-l="\d+-(\d+)"><span class="n">\d*</span>(.*?)</span>(?=\n|$)', v, re.S):
            linhas.append((int(m.group(1)), html.unescape(re.sub(r'<[^>]+>', '', m.group(2)))))
    estrofes, anterior = [], None
    for i, t in linhas:
        if t == '[…]':
            estrofes.append(['[…]'])
            anterior = None
            continue
        if not estrofes or anterior is None or i != anterior + 1:
            estrofes.append([])
        estrofes[-1].append(t)
        anterior = i
    return estrofes


def vocabulario_do_cartao(c):
    """Os pares (palavra, sentido) da lista «Vocabulário» de um cartão; _palavra_ é itálico na lição."""
    g = re.search(r'<p class="gl"><b>Vocabulário:</b> (.*?)</p>', c['html'], re.S).group(1)
    pares = [list(re.fullmatch(r'<b>(.*)</b>, (.*?)', item, re.S).groups()) for item in g.split('; ')]
    return [[re.sub(r'_([^_]+)_', r'<i>\1</i>', p), re.sub(r'_([^_]+)_', r'<i>\1</i>', s)] for p, s in pares]


def fonte_do_cartao(c):
    return re.sub(r'_([^_]+)_', r'<i>\1</i>', re.search(r'<p class="fonte">(.*?)</p>', c['html'], re.S).group(1))


def linhas_do_texto(t):
    """As estrofes de um texto dos dados, com as marcas do que as lições não dão como '[…]'."""
    return [[v if isinstance(v, str) else v['falta'] for v in e['versos']] for e in t['estrofes']]


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


def todas_as_alineas(p):
    return [x for g in p['grupos'] for x in g['alineas']] if p.get('grupos') else p['alineas']


def todos_os_textos(f):
    return ([i for p in f['perguntas'] for i in p['textos']] + [i for t in f['temas'] for i in t['material'].get('textos', [])]
            + f['temas_material']['textos'])


def todos_os_exemplos(f):
    return [x for p in f['perguntas'] for x in p['exemplos']] + [x for t in f['temas'] for x in t['material'].get('exemplos', [])]


class TarefasFaceisM6(unittest.TestCase):
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
                self.assertEqual(lead, 'À mão, com consulta: <strong>200 a 240 palavras no total</strong>. Orientação: cerca de 110 nas respostas e '
                                       '90 a 130 no tema.')
                self.assertEqual(quadro[2][2], {'t': f'orientação: cerca de{N}110 nas duas perguntas', 'linhas': 2})
                self.assertIsNone(quadro[3][2])
                self.assertEqual(solto(quadro[4][2]), 'orientação: 90 a 130')
                self.assertEqual(solto(quadro[-1][2]), '200 a 240')
                self.assertEqual([solto(p['meta']) for p in f['perguntas']], ['Orientação: cerca de 110 palavras nas duas perguntas.'] * 2)
                self.assertEqual(solto(f['temas_nota']), 'Orientação: 90 a 130 palavras.')
                self.assertIn('Tenho 200 a 240 palavras?', [solto(x) for x in f['verificar']])
                # Tudo o que o enunciado de antes citava entre «» continua pedido.
                pedido = solto(sem_marcas(json.dumps([f['perguntas'], f['temas'], f['finais']], ensure_ascii=False)))
                velho = solto(sem_marcas(' '.join(a['nucleo'] + [t['texto'] for t in a['temas']])))
                citados = re.findall(r'«([^»]+)»', velho)
                self.assertGreaterEqual(len(citados), 7)
                for citado in citados:
                    self.assertIn(f'«{citado}»', pedido, citado)
                # Cada pedido do enunciado de antes, com as mesmas palavras.
                self.assertGreaterEqual(len(PEDIDOS[slug]), 23)
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
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        a1, a2 = (json.loads(antes(rel)) for rel in DADOS_TAREFAS)
        # As alíneas das perguntas: os pedidos de antes, um por alínea.
        self.assertEqual([todas_as_alineas(p) for p in u1['perguntas']],
                         [['Indica a quem se dirige a voz.', 'Indica para que serve o sonho.', 'Cita um verso dos tercetos.', 'Aponta uma semelhança.',
                           'Explica uma diferença.'],
                          ['Divide o verso em orações.', 'Classifica cada oração.', 'Justifica com a função de «que» na sua oração.',
                           'Explica o que essa oração acrescenta ao verso.']])
        self.assertEqual([todas_as_alineas(p) for p in u2['perguntas']],
                         [['Classifica a oração com «que».', 'Distingue o que o sujeito observa daquilo em que o transforma.', 'Identifica dois recursos.',
                           'Explica os efeitos.', 'Diz se o olhar ultrapassa o real.'],
                          ['Compara «cheio» e «pleno» com o étimo.', 'Diz que via seguiu cada palavra.', 'Escreve «bellas» e «Pousára» na grafia atual.',
                           'Explica as mudanças.']])
        # Decisão do docente (m6-u1): «para que serve o sonho» diz-se no enunciado (já se dizia) e na grelha (test_tudo_junto).
        self.assertIn('para que serve o sonho', a1['nucleo'][0])
        # Decisão do docente (m6-u2): o étimo de «cheio» e de «pleno» é dado no enunciado. É o que a lição F05 dá.
        self.assertNotIn('plenu', json.dumps(a2, ensure_ascii=False))
        self.assertEqual(u2['perguntas'][1]['grupos'][0]['intro'],
                         '«Cheio» («Cheio de bellas proporções carnaes») e «pleno» («O sol, já alto e pleno») vêm do mesmo étimo latino: <i>plenu-</i>.')
        self.assertIn('<i>plenu-</i> deu «cheio» na boca do povo e «pleno» nos livros', ler(F05).replace('\\"', '"'))
        self.assertEqual(ler(ENUNCIADOS[1]).count('<i>plenu-</i>'), 1)
        # Decisão do docente (m6-u2): «algo que não podes fotografar» passa a dizer-se «o que a imagem não mostra».
        self.assertIn('<li>Indica algo que não podes fotografar e explica porquê.</li>', a2['temas'][1]['texto'])
        self.assertEqual(u2['temas'][1]['passos'][-1], 'Indica o que a imagem não mostra e explica porquê.')
        for parte in ('', 'grelha/', 'correcao/'):
            lido = solto(visivel(ler(f'tarefas/m6-u2/{parte}index.html'), so_main=False))
            self.assertNotRegex(lido, r'(?i)não pod\w+ fotografar|não posso fotografar|não se fotografa', parte)
            self.assertIn('a imagem não mostra', lido.replace('A imagem', 'a imagem'), parte)
        # Os passos de cada tema são os cinco elementos da grelha e a explicação, pela ordem do enunciado de antes (com a escolha do
        # verso a imitar à cabeça do tema A, como no M3).
        self.assertEqual([len(t['passos']) for t in u1['temas']], [8, 5])
        self.assertEqual([len(t['passos']) for t in u2['temas']], [7, 5])
        self.assertEqual(u1['temas'][0]['passos'][0], 'Escolhe um verso de Antero para imitar.')
        self.assertEqual(u2['temas'][0]['passos'][0], 'Escolhe um verso de Cesário para imitar.')
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in SLUGS:
            self.assertEqual(grelhas[slug]['criterios'][3]['nome'], 'Tema à escolha (A ou B): cinco elementos e a explicação')

    def test_criterios_da_grelha_iguais(self):
        agora, base = json.loads(ler(GRELHAS))['tarefas'], json.loads(antes(GRELHAS))['tarefas']
        self.assertEqual(list(agora), list(base))
        for slug, t in agora.items():
            with self.subTest(grelha=slug):
                # («correcao_estreita»: na versão de correção, o cabeçalho «Observações» pode partir-se a 320 px, para a tabela de quatro
                # colunas caber no ecrã; confere-se em tests/browser_revisao_tarefas_20261101.py)
                novas = {'autoavaliacao_so_tua', 'trocas_aluno', 'correcao_estreita'} if slug in SLUGS else set()
                self.assertEqual(set(t) - set(base[slug]), novas)
                # Nas duas grelhas do M6, as únicas diferenças são os exemplos de EXEMPLOS_TROCADOS, cada um uma vez na base e uma vez
                # agora (tudo o resto igual à base, letra a letra; as outras grelhas, iguais sem exceção).
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
        self.assertEqual(len(EXEMPLOS_TROCADOS['m6-u2']), 6)  # 13/11/2026: revisão, mais a nota que anuncia os exemplos
        for slug in SLUGS:
            t = agora[slug]
            self.assertIs(t['autoavaliacao_so_tua'], True)
            self.assertIs(t['correcao_estreita'], True)
            # As trocas são só as palavras que o enunciado novo trocou; cada uma ocorre nos textos da grelha.
            fonte = json.dumps({k: v for k, v in t.items() if k != 'trocas_aluno'}, ensure_ascii=False)
            for outra in OUTRAS:
                self.assertNotIn('correcao_estreita', agora[outra])
                self.assertNotIn('overflow-wrap', ler(f'tarefas/{outra}/correcao/index.html'))
            for a, _ in t['trocas_aluno']:
                self.assertIn(a, fonte)
            grelha = solto(visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False, sem_nav=False))
            self.assertNotRegex(grelha, r'\b[Ff]echo\b')
            self.assertNotRegex(visivel(ler(f'tarefas/{slug}/index.html')), r'\b[Ff]echo\b')
            self.assertEqual(grelha.count('Duas linhas finais: '), 2)
            self.assertEqual(grelha.count('Duas linhas finais genéricas, sem verso.'), 1)
        # Nas duas, as sete trocas das palavras comuns (as cinco das grelhas do M3, do M1 e do M5 e «Duas linhas finais» onde a grelha
        # dizia «Fecho»); na m6-u1, mais três: «para que serve o sonho» (e, desde a revisão de 13/11/2026, mais nove: as palavras do enunciado); na m6-u2, mais três: «o que a imagem não mostra» e o étimo.
        self.assertEqual(agora['m6-u1']['trocas_aluno'], TROCAS_COMUNS + TROCAS_U1)
        self.assertEqual(agora['m6-u2']['trocas_aluno'], TROCAS_COMUNS + TROCAS_U2)
        self.assertEqual(agora['m6-u2']['trocas_aluno'][:5], agora['m3-u2']['trocas_aluno'][:5])
        self.assertEqual(agora['m6-u2']['trocas_aluno'][:5], agora['m5-u2']['trocas_aluno'][:5])

    # ---------- os textos são os das lições, letra a letra ----------

    def test_textos_letra_a_letra_das_licoes(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            f = json.loads(ler(rel))['facil']
            pagina = ler(enunciado)
            lidas = {}
            self.assertEqual([t['id'] for t in f['textos']], list(VERSOS[slug]))
            self.assertEqual([solto(sem_marcas(t['titulo'])) for t in f['textos']], TITULOS[slug])
            self.assertEqual([t['rotulo'] for t in f['textos']], [f'Texto{N}{k}' for k in range(1, len(f['textos']) + 1)])
            for t in f['textos']:
                with self.subTest(tarefa=slug, texto=t['id']):
                    self.assertNotIn('paragrafos', t)
                    linhas = linhas_do_texto(t)
                    versos, estrofes = VERSOS[slug][t['id']]
                    self.assertEqual([len(e) for e in linhas], estrofes)
                    self.assertEqual(sum(1 for e in linhas for v in e if v != '[…]'), versos)
                    for e in linhas:
                        for v in e:
                            self.assertNotRegex(v, r'[<>]')
                    if t['id'] in TEXTOS[slug]:
                        # Cada verso é um verso de um cartão «O texto» da lição, pela ordem, sem saltar nenhum; os cortes da lição
                        # («[…]») ficam onde a lição os tem.
                        licao, numeros, quais, k_vocab, palavras = TEXTOS[slug][t['id']]
                        da_licao = estrofes_da_licao(licao, numeros)
                        self.assertEqual(linhas, da_licao if quais is None else [da_licao[i] for i in quais])
                        c = lidas.setdefault(licao, cartoes(licao))[k_vocab - 1]
                        vocab = vocabulario_do_cartao(c)
                        if palavras is not None:
                            self.assertEqual([p for p, _ in t['glossario']], palavras)
                            vocab = [x for x in vocab if x[0] in palavras]
                        self.assertEqual(t['glossario'], vocab)
                        self.assertEqual(solto(t['fonte']), solto(fonte_do_cartao(c)) + FONTE_MAIS.get((slug, t['id']), ''))
                        self.assertIn('(grafia da edição', t['fonte'])
                        self.assertRegex(t['origem'], r'^' + re.escape(licao) + r', linha \d+, cart(?:ão|ões) [\d, ]+ \(copiado letra a letra')
                        # Cada palavra do vocabulário está nos versos do texto (com outra maiúscula ou flexão, quando muito).
                        juntos = ' '.join(v for e in linhas for v in e).casefold()
                        for palavra, _ in t['glossario']:
                            raiz = re.sub(r'</?i>', '', palavra).casefold()
                            self.assertTrue(raiz in juntos or raiz[:5] in juntos, palavra)
                    # As marcas do que as lições não dão: só em «A um poeta» (um verso, que conta) e nos excertos de «Ao Gás» (dois
                    # cortes, que não contam).
                    marcas = [v for e in t['estrofes'] for v in e['versos'] if isinstance(v, dict)]
                    esperadas = {('m6-u1', 'texto-2'): [{'falta': '[…]', 'conta': 1}], ('m6-u2', 'texto-5'): [{'falta': '[…]', 'conta': 0}] * 2}
                    self.assertEqual(marcas, esperadas.get((slug, t['id']), []))
                    # Na página, o texto está inteiro, pela ordem, com os versos numerados de cinco em cinco.
                    bloco = re.search(r'<section class="tt-texto[^"]*" id="' + t['id'] + r'".*?</section>', pagina, re.S).group(0)
                    na_pagina = [[html.unescape(v) for v in re.findall(r'<span class="tt-l">(.*?)</span>', e)]
                                 for e in re.findall(r'<p class="tt-estrofe">(.*?)</p>', bloco, re.S)]
                    self.assertEqual(na_pagina, linhas)
                    numeros_pag = [n for n in re.findall(r'<span class="tt-n">(\d*)</span>', bloco) if n]
                    contam = versos + sum(m['conta'] for m in marcas)
                    # 13/11/2026: revisão. Os excertos de «Ao Gás» (Texto 5 da m6-u2) não levam números: com estrofes saltadas, o
                    # número contado por cima dos cortes não era o número do verso na parte. Os outros textos numeram-se de 5 em 5.
                    sem_numeros = (slug, t['id']) == ('m6-u2', 'texto-5')
                    self.assertEqual(t['numerar'], 0 if sem_numeros else 5)
                    self.assertEqual(numeros_pag, [] if sem_numeros else [str(k) for k in range(5, contam + 1, 5)])
                    self.assertEqual(bloco.count('class="tt-v tt-falta"'), len(marcas))
                    for palavra, sentido in t.get('glossario', []):
                        self.assertIn(f'<li><b>{palavra}</b>: {sentido}</li>', bloco)
                    self.assertEqual(bloco.count('<li>'), len(t.get('glossario', [])))
                    self.assertIn(f'<p class="tt-fonte">{t["fonte"]}</p>', bloco)
                    self.assertEqual(pagina.count(f'id="{t["id"]}"'), 1)
                    # Em papel: um texto até 24 versos sai inteiro (tt-curto); uma parte de 44 versos sai inteira na sua página
                    # (tt-pagina); os excertos de «Ao Gás» (20 versos) também são curtos.
                    self.assertEqual(bool(t.get('pagina')), versos == 44)
                    classes = 'tt-texto' + (' tt-curto' if versos <= 24 else '') + (' tt-pagina' if versos == 44 else '')
                    self.assertTrue(bloco.startswith(f'<section class="{classes}" id='), bloco[:80])
            # Nada veio de fora das lições e não há imagens.
            self.assertNotIn('class="tt-onde"', pagina)
            for fora in ('gutenberg', 'wikisource', 'archive.org', '<figure', '<img ', 'data:image', 'Surge et ambula', 'sonho puro'):
                self.assertNotIn(fora, pagina)
        # m6-u1: «A um poeta» são os versos que a lição F13 dá, nos seus três cartões «Lê de perto», pela ordem: 1 a 4, 5 a 12 e 14.
        # O verso 13 não está em nenhuma lição do repositório (defeito anotado): não se acrescentou de fora; a página marca-o com
        # «[…]», conta-o na numeração e di-lo na linha de fonte, que remete para o manual sem número de página.
        f = json.loads(ler(DADOS_TAREFAS[0]))['facil']
        arr = cartoes(F13)
        citados = [[html.unescape(v) for v in re.findall(r'<p>(.*?)</p>', b)] for k in (2, 5, 8)
                   for b in re.findall(r'<blockquote>(.*?)</blockquote>', arr[k - 1]['html'], re.S)]
        self.assertEqual([len(b) for b in citados], [4, 4, 4, 1])
        poeta = linhas_do_texto(f['textos'][1])
        self.assertEqual([v for e in poeta for v in e], citados[0] + citados[1] + citados[2] + ['[…]'] + citados[3])
        self.assertEqual(poeta[3], ['Ergue-te pois, soldado do Futuro,', '[…]', 'Sonhador, faze espada de combate!'])
        self.assertIn('Este é o último verso do soneto.', arr[7]['html'])
        for licao in sorted((ROOT / 'm6').glob('licao-*/index.html')):
            self.assertNotIn('sonho puro', licao.read_text('utf-8'), licao)
        self.assertEqual(solto(f['textos'][1]['fonte']), 'Antero de Quental, «A um poeta», <i>Os Sonetos Completos</i>, 1886 (grafia da edição). As lições '
                         'dão 13 dos 14 versos: falta o verso 13, marcado com «[…]». Esse verso está no manual.')
        self.assertIn('Antero de Quental, «A um poeta», <i>Os Sonetos Completos</i>, 1886.', arr[13]['html'])
        # 13/11/2026: revisão. O verso que falta é o único do soneto com a palavra «sonho», e a alínea b) pergunta para que serve o
        # sonho: uma linha de ajuda da pergunta 1 diz que o verso falta e manda reler o cartão da lição F13 que lê o último verso
        # (as lições são material de consulta). O título da lição e o do cartão são os da lição.
        self.assertEqual(f['perguntas'][0]['ajudas'][-1], f'No Texto{N}2 falta o verso{N}13. Para a alínea{N}b), relê na lição{N}F13, '
                         '<a href="../../m6/licao-m6-f13/">O sonho pode pedir ação?</a>, o cartão «Uma espada feita de sonho».')
        self.assertEqual(len(f['perguntas'][0]['ajudas']), 4)
        self.assertIn('<p class="tf-ajuda">' + f['perguntas'][0]['ajudas'][-1] + '</p>', ler(ENUNCIADOS[0]))
        self.assertEqual(arr[7]['titulo'], 'Uma espada feita de sonho')
        self.assertIn('<title>O sonho pode pedir ação? · M6-F13 · Português</title>', ler(F13))
        self.assertTrue((ROOT / 'm6/licao-m6-f13/index.html').is_file())
        # O vocabulário de «A um poeta» é o que a lição diz no texto dos cartões (e «fragor», do vocabulário da lição F01).
        self.assertEqual(f['textos'][1]['glossario'], [['levita', 'aqui, uma figura ligada ao serviço religioso'], ['fragor', 'estrondo'],
                                                       ['larvas tumulares', 'expressão que lembra a morte'], ['rebate', 'sinal de alarme']])
        self.assertIn('«Levita» designa aqui uma figura ligada ao serviço religioso', arr[1]['html'])
        self.assertIn('«Larvas tumulares» lembra a morte; «rebate» é um sinal de alarme.', arr[4]['html'])
        self.assertIn(['fragor', 'estrondo'], vocabulario_do_cartao(cartoes(F01)[13]))
        # Os dois sonetos na pergunta 1 (com a barra nos tercetos), a estrofe das naus na pergunta 2 e «O Palacio da Ventura» para os
        # dois temas.
        self.assertEqual([p['textos'] for p in f['perguntas']], [['texto-1', 'texto-2'], ['texto-3']])
        self.assertEqual([t['material'].get('textos', []) for t in f['temas']], [[], []])
        self.assertEqual(f['temas_material']['textos'], ['texto-4'])
        self.assertEqual(sorted(todos_os_textos(f)), [f'texto-{k}' for k in range(1, 5)])
        self.assertEqual([t.get('escolher') for t in f['textos']], [{'de': 9, 'ate': 14}, {'de': 9, 'ate': 14}, None, None])
        self.assertEqual(f['textos'][2]['estrofes'][0]['versos'][3], 'Singram soberbas naus que eu não verei jámais!')
        self.assertEqual(f['textos'][3]['estrofes'][3]['versos'][2], 'Silencio e escuridão — e nada mais!')
        pagina = ler(ENUNCIADOS[0])
        for k in (1, 2):
            bloco = re.search(rf'<section class="tt-texto[^"]*" id="texto-{k}".*?</section>', pagina, re.S).group(0)
            self.assertEqual(bloco.count('class="tt-v tt-esc"'), 6 if k == 1 else 5)
        # m6-u2: as duas estrofes na pergunta 1 e as quatro partes do poema para os dois temas, pela ordem do poema; a pergunta 2 cita
        # os versos no próprio pedido, com o poema e o autor de cada um, como as lições F12 e F13 os dão.
        f = json.loads(ler(DADOS_TAREFAS[1]))['facil']
        self.assertEqual([p['textos'] for p in f['perguntas']], [['texto-1', 'texto-2'], []])
        self.assertEqual([t['material'].get('textos', []) for t in f['temas']], [[], []])
        self.assertEqual(f['temas_material']['textos'], ['texto-3', 'texto-4', 'texto-5', 'texto-6'])
        # 13/11/2026: revisão. A nota dos números diz que textos se numeram e porque o Texto 5 não tem números.
        self.assertEqual(f['temas_material']['notas'], [f'Nos Textos{N}3, 4{N}e{N}6, os versos numeram-se a partir de{N}1 em cada parte. '
                                                        f'O Texto{N}5 não tem números, porque lhe faltam estrofes.'])
        self.assertEqual(sorted(todos_os_textos(f)), [f'texto-{k}' for k in range(1, 7)])
        self.assertEqual(f['textos'][0]['estrofes'][0]['versos'][1], "Quizera que o real e a analyse m'o dessem;")
        self.assertEqual(f['textos'][1]['estrofes'][0]['versos'][3], 'Amarelladamente, os cães parecem lobos.')
        self.assertEqual(f['textos'][0]['estrofes'][0], f['textos'][4]['estrofes'][3])
        self.assertEqual(f['textos'][1]['estrofes'][0], f['textos'][5]['estrofes'][8])
        self.assertEqual([c['titulo'] for c in (cartoes(F06)[2], cartoes(F07)[2], cartoes(F07)[13], cartoes(F07)[19])],
                         ['I: «Ave-Marias» (na íntegra)', 'II: «Noite Fechada» (na íntegra)', 'III: «Ao Gás» (excertos)', 'IV: «Horas Mortas» (na íntegra)'])
        self.assertEqual(solto(f['perguntas'][1]['ajudas'][1]), '«Cheio de bellas proporções carnaes» e «Pousára, ajoelhando, a sua giga.» são versos de '
                         '«Num Bairro Moderno», de Cesário Verde. «O sol, já alto e pleno» é de «A um poeta», de Antero de Quental.')
        bairro, poeta = plana(F12), plana(F13)
        for verso in ('Cheio de bellas proporções carnaes', 'Pousára, ajoelhando, a sua giga.'):
            self.assertIn(verso, bairro)
        self.assertIn('Cesário Verde, «N\'um Bairro Moderno»', bairro)
        self.assertIn('O sol, já alto e pleno', poeta)
        # O que fica remetido para o manual, sem número de página: o verso 13 de «A um poeta» e o resto da parte III.
        for enunciado, n in zip(ENUNCIADOS, (1, 1)):
            lido = solto(visivel(ler(enunciado)))
            self.assertEqual(len(re.findall(r'\bmanual\b', lido)), n, enunciado)
            self.assertNotRegex(lido, r'(?i)\bp(?:ág)?\. ?\d|\bpágina \d')

    def test_exemplos_com_outro_caso(self):
        # Os exemplos mostram como se faz com outro caso: vêm da grelha pública (como o aluno a lê) e nunca usam as passagens
        # reservadas da tarefa (a lista «reservadas» do aquecimento) nem os textos da página.
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in SLUGS:
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            f = d['facil']
            reservadas = json.loads(ler(f'docs/pedagogia/aquecimentos/{slug}.json'))['reservadas']
            self.assertGreater(len(reservadas), 20)
            # A grelha como o aluno a lê: com as trocas das palavras do enunciado novo.
            publico = json.dumps({k: v for k, v in grelhas[slug].items() if k != 'trocas_aluno'}, ensure_ascii=False)
            for a, b in grelhas[slug]['trocas_aluno']:
                publico = publico.replace(json.dumps(a, ensure_ascii=False)[1:-1], json.dumps(b, ensure_ascii=False)[1:-1])
            publico = solto(' '.join(v for c in json.loads(publico)['criterios'] for nivel in c['niveis'].values() for v in nivel))
            exemplos = todos_os_exemplos(f)
            self.assertEqual(len(exemplos), 4)
            self.assertEqual([len(p['exemplos']) for p in f['perguntas']] + [len(t['material']['exemplos']) for t in f['temas']], [1, 1, 1, 1])
            for x in exemplos:
                self.assertNotIn('html', x)
                self.assertNotIn('de', x)
                for r in reservadas:
                    self.assertNotIn(r, solto(sem_marcas(x['titulo'])), x['titulo'])
                for p in x['paragrafos']:
                    with self.subTest(tarefa=slug, exemplo=p['t'][:50]):
                        for r in reservadas:
                            self.assertNotIn(r, solto(p['t']))
                        # «Passo» e «Alínea» ficam presos ao número ou à letra (U+00A0), como as outras referências.
                        self.assertRegex(p['al'], rf'^(?:Passos?|Alíneas?){N}')
                        self.assertNotRegex(p['al'], r'(?:Passos?|Alíneas?) |\d (?:a|e) \d|\) (?:a|e) [a-h]\)')
                        self.assertIn(solto(re.sub(r'</?i>', '_', p['t'])), publico)
            pagina = ler(f'tarefas/{slug}/index.html')
            # Em desdobrável fechado no ecrã, que não sai em papel.
            self.assertEqual(pagina.count('<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>Ver um exemplo com outro caso</summary>'), 4)
            self.assertEqual(pagina.count('<details class="tf-so-tema tf-exemplos tf-so-ecra">'), 4)
            self.assertNotRegex(pagina, r'<details[^>]* open')
            # Nenhuma citação de um exemplo ocorre nos textos da página (os textos da tarefa), nem inteira nem nas suas frases; e
            # nenhuma sequência de quatro palavras seguidas de um exemplo vem de um texto da tarefa. O mesmo vale para os exemplos da
            # grelha do aluno, que são os mesmos.
            dentro = ' '.join(re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra">.*?</details>', pagina, re.S))
            blocos = re.findall(r'<section class="tt-texto[^"]*" id="texto-\d".*?</section>', pagina, re.S)
            self.assertEqual(len(blocos), len(f['textos']))
            textos_da_pagina = ' '.join(sem_marcas(x) for b in blocos for x in re.findall(r'<span class="tt-l">.*?</span>', b, re.S))
            textos_da_pagina = re.sub(r'\s+', ' ', solto(textos_da_pagina))
            self.assertGreater(len(textos_da_pagina), 1500)
            exemplos_da_grelha = ' '.join(solto(v[1]) for c in grelhas[slug]['criterios'] for v in c['niveis'].values())
            citacoes = re.findall(r'«([^«»]+)»', solto(sem_marcas(dentro))) + re.findall(r'«([^«»]+)»', exemplos_da_grelha)
            self.assertGreaterEqual(len(citacoes), 20)
            for citacao in citacoes:
                with self.subTest(tarefa=slug, citacao=citacao[:50]):
                    for pedaco in [citacao] + [x.strip() for x in re.split(r'[.;:!?…/]', citacao)]:
                        if len(pedaco.split()) >= 2:
                            self.assertNotIn(pedaco.casefold(), textos_da_pagina.casefold())
            palavras_ex = re.findall(r"[\w'’-]+", solto(sem_marcas(dentro)) + ' ' + exemplos_da_grelha)
            juntas = ' ' + ' '.join(re.findall(r"[\w'’-]+", textos_da_pagina)).casefold() + ' '
            for k in range(len(palavras_ex) - 3):
                quatro = ' '.join(palavras_ex[k:k + 4]).casefold()
                self.assertNotIn(' ' + quatro + ' ', juntas, quatro)
            # Na m6-u2, as grafias antigas dos exemplos também não estão nos textos da página.
            if slug == 'm6-u2':
                # 13/11/2026: revisão. O exemplo diz «do século XIX», como a lição F05, e não «de 1887» («lyrios» é de 1886).
                self.assertEqual(f['perguntas'][1]['exemplos'][0]['titulo'], f'Outro étimo e outras grafias do século{N}XIX')
                self.assertIn(f'E do século{N}XIX: «occidental» passa a ocidental', f['perguntas'][1]['exemplos'][0]['paragrafos'][1]['t'])
                for onde in (dentro, exemplos_da_grelha, solto(ler(f'tarefas/{slug}/grelha/index.html'))):
                    self.assertNotIn('E de 1887', solto(onde))
                    self.assertNotIn('grafias de 1887', solto(onde))
                    self.assertNotIn('palavras de 1887', solto(onde))
                for palavra in ('occidental', 'lyrios'):
                    self.assertNotIn(palavra, textos_da_pagina.casefold())
                for palavra in ('Edade-média', 'oxygenio', 'mausoléos', 'arripia'):
                    self.assertIn(palavra, textos_da_pagina)
                    self.assertNotIn(palavra, exemplos_da_grelha)
                    self.assertNotIn(palavra, dentro)
            # As citações dos exemplos estão nas lições, letra a letra, fora dos textos da tarefa, e na grelha do aluno.
            grelha_aluno = solto(sem_marcas(ler(f'tarefas/{slug}/grelha/index.html')))
            for rel_licao, citacao in EXEMPLOS_DAS_LICOES[slug]:
                self.assertIn(citacao, re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', ler(rel_licao)))), citacao)
            for _, novo in EXEMPLOS_TROCADOS[slug]:
                self.assertIn(novo.replace('Fecho: ', 'Duas linhas finais: '), re.sub(r'\s+', ' ', grelha_aluno), novo[:50])
        css = ler('assets/task-textos.css')
        impressao = css[css.index('@media print{'):]
        self.assertIn('[data-task-facil] .tf-so-ecra{display:none!important}', impressao)
        self.assertIn('[data-task-facil] .tt-texto{break-inside:avoid}', impressao)
        self.assertIn('[data-task-facil] .tt-estrofe{margin:0 0 14px;max-width:none;break-inside:avoid}', css)
        self.assertIn('[data-task-facil] :is(h2,h3,h4,summary,.tt-rotulo,.tf-meta,.tf-antes,.tf-fig){break-after:avoid}', impressao)
        self.assertIn('[data-task-facil] .tf-topo{break-after:avoid}', impressao)
        # Em papel, uma parte de 44 versos sai inteira numa página, em letra um pouco mais pequena; não há páginas novas forçadas.
        self.assertIn('[data-task-facil] .tt-texto.tt-pagina .tt-versos,[data-task-facil] .task-theme .tt-texto.tt-pagina .tt-versos{font-size:10pt;line-height:1.2}', impressao)
        self.assertNotRegex(css, r'break-(?:before|after):\s*page')
        # 13/11/2026: revisão. Os passos de um tema e os factos do dossiê saem juntos em papel.
        self.assertIn('[data-task-facil] .tf-juntos{break-inside:avoid}', impressao)
        self.assertIn('[data-task-facil] .task-theme:has(>.tf-juntos)>.tf-p{break-inside:avoid}', impressao)
        self.assertNotIn('tt-pagina{break-inside:auto', css.replace(' ', ''))

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
                                  [15, 'Rever e entregar', f'Confere a grelha{N}/20 e entrega fotografias legíveis no Teams.']])
        self.assertEqual(sum(b[0] for b in blocos), 90)
        self.assertEqual(re.findall(r'<div class="t"><b>([^<]+)</b>', guia),
                         [f'Aquecer, 10{N}min', f'Ler o enunciado, 10{N}min', f'Produzir, 55{N}min', f'Rever e entregar, 15{N}min'])
        self.assertIn(f'faz o aquecimento em cartões (10{N}minutos). Seguem-se 10{N}minutos de leitura, 55 de produção e 15 de revisão e entrega.', guia)
        # Nenhum «5 min» nem «60 min» antigos (nem «5 minutos», «60 minutos», «60 de produção») nas páginas do M6 ligadas à tarefa.
        for rel in PAGINAS + [GUIA, INDICE, MAPA, PORTEFOLIO]:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                self.assertNotRegex(fonte, r'(?<![\d,.])(?:5|60)[ \xa0]min')
                self.assertNotRegex(fonte, r'\b60 de produção|\b5 de leitura')
                self.assertNotIn('10/5/60/15', fonte)

    def test_consulta_versos_autoavaliacao_e_aquecimento(self):
        alineas_por_pergunta = {'m6-u1': [5, 4], 'm6-u2': [5, 4]}
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
                # Os versos citados ou copiados não contam para as palavras (decisão do docente), nem as duas linhas finais: uma vez
                # no enunciado, por baixo do quadro, e na grelha do aluno com as palavras de sempre.
                self.assertIn('<p class="tf-nota">Não contam para as palavras: os versos citados ou copiados e as duas linhas finais.</p>', cabeca)
                self.assertEqual(texto.count('Não contam para as palavras'), 1)
                grelha = solto(ler(f'tarefas/{slug}/grelha/index.html'))
                self.assertEqual(grelha.count('mais duas linhas finais que não contam para as palavras.'), 1)
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
                self.assertIn('<thead><tr><th>Critério</th><th class="n">Máx.</th><th class="n">Docente</th><th style="overflow-wrap:anywhere">Observações</th></tr></thead>', correcao)
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
                self.assertEqual(len(perguntas), 10)
                self.assertTrue(all(p.endswith('?') for p in perguntas), perguntas)
                self.assertEqual(pagina.count('class="task-checklist"'), 1)
                self.assertIn('<p class="tf-p" id="criterios">Responde sim ou não. Se for não, completa o teu trabalho.</p>', pagina)
                # Um pedido por alínea: cada alínea é uma frase só, curta (14 palavras no máximo); as letras continuam de um grupo
                # para o outro.
                d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))['facil']
                contadas = []
                for p in d['perguntas']:
                    alineas = todas_as_alineas(p)
                    contadas.append(len(alineas))
                    for x in alineas:
                        self.assertEqual(len(re.findall(r'[.?!](?:\s|$)', re.sub(r'<[^>]+>', '', x))), 1, x)
                        self.assertLessEqual(len(x.split()), 14, x)
                self.assertEqual(contadas, alineas_por_pergunta[slug])
                self.assertEqual(len(re.findall(r'<ol class="tf-alineas"(?: start="\d")?>', pagina)), 2 + sum(1 for p in d['perguntas'] if p.get('grupos')))
                # Cada passo dos temas é também uma frase só, com 20 palavras no máximo.
                passos = [x for t in d['temas'] for x in t['passos']]
                self.assertGreaterEqual(len(passos), 12)
                for x in passos:
                    self.assertIsInstance(x, str)
                    self.assertLessEqual(len(re.findall(r'[.?!;:](?:\s|$)', re.sub(r'<[^>]+>', '', x))), 1, x)
                    self.assertLessEqual(len(re.sub(r'<[^>]+>', '', x).split()), 20, x)

    def test_tudo_junto_as_mesmas_palavras(self):
        # O enunciado novo diz «as duas perguntas», «a letra do teu tema», «as respostas ligam-se» e «duas linhas finais»: a grelha, a
        # correção, o aquecimento, o guia, o índice e o mapa usam as mesmas palavras, e as antigas saem de todos.
        for slug in SLUGS:
            for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                rel = f'tarefas/{slug}/{parte}index.html'
                with self.subTest(pagina=rel):
                    texto = visivel(ler(rel), so_main=False, sem_nav=False)
                    for velha in ('úcleo', 'tema escolhido', 'articulad', 'tema que escolhes'):
                        self.assertNotIn(velha, texto)
                    self.assertNotRegex(texto, r'\b[Ff]echo\b')
                    self.assertNotRegex(texto, r'(?<!a letra d)o tema no topo')
            enunciado = visivel(ler(f'tarefas/{slug}/index.html'))
            self.assertIn('Responde a duas perguntas.', enunciado)
            self.assertIn(f'Escreve a letra do teu tema (A{N}ou{N}B) no topo.', enunciado)
            self.assertIn('As respostas ligam-se (não estão soltas)?', enunciado)
            self.assertIn(f'A letra do meu tema (A{N}ou{N}B) está no topo?', enunciado)
            self.assertIn(f'<meta name="description" content="Aula de tarefa com consulta: aquecimento, duas perguntas e um tema à escolha, em papel, durante 90{N}minutos, com entrega no Teams.">', ler(f'tarefas/{slug}/index.html'))
            for parte in ('grelha/', 'correcao/'):
                p = solto(ler(f'tarefas/{slug}/{parte}index.html'))
                self.assertIn('Respostas ligadas, extensão e escrita revista', p)
                self.assertIn('a letra do teu tema está no topo', p)
            grelha = solto(ler(f'tarefas/{slug}/grelha/index.html'))
            self.assertEqual(grelha.count('Respostas ligadas, extensão e escrita revista'), 3)
            self.assertIn('<p>Duas perguntas e um tema à escolha (A ou B), à mão, entre 200 e ', grelha)
            self.assertIn('a letra do tema no topo', grelha)
            self.assertIn('<li>Não escrever no topo a letra do teu tema (A ou B).</li>', grelha)
            aquecimento = solto(ler(f'tarefas/{slug}/aquecimento/index.html'))
            self.assertEqual(aquecimento.count('<b>Perguntas 1 e 2.<\\/b>'), 1)
            self.assertIn('Lês o enunciado e escreves no topo a letra do teu tema', aquecimento)
            self.assertIn('A letra do tema fica escrita no topo; as duas perguntas vêm primeiro, porque são para todos;', aquecimento)
        # m6-u1: «para que serve o sonho», no enunciado, na grelha, na correção e no aquecimento (decisão do docente); e «recontado»,
        # «uma diferença» e «a função de «que»», como no enunciado.
        enunciado = visivel(ler(ENUNCIADOS[0]))
        self.assertIn('Indica para que serve o sonho.', enunciado)
        self.assertIn(f'Na pergunta{N}1, indiquei a quem se dirige a voz e para que serve o sonho, nos dois sonetos?', enunciado)
        for parte in ('grelha/', 'correcao/'):
            p = solto(visivel(ler(f'tarefas/m6-u1/{parte}index.html'), so_main=False))
            # 13/11/2026: revisão, «tudo junto». A grelha e a versão de correção dizem «a quem se dirige a voz», «uma diferença» e «a
            # função de «que»», como o enunciado; as palavras antigas («a quem fala a voz», «o que muda», «o papel de «que»») saem.
            self.assertIn('Em cada soneto, dizes a quem se dirige a voz e para que serve o sonho, com um verso exato dos tercetos, explicado.', p)
            self.assertIn('uma diferença de um soneto para o outro naquilo para que serve o sonho.', p)
            self.assertIn('A comparação: uma semelhança e uma diferença', p)
            self.assertIn('justificas com a função de «que» na sua oração', p)
            for velha in ('o que é o sonho ou o ideal', 'papel do sonho', 'a quem fala a voz', 'o que muda', 'o papel de «que»', 'reescrever'):
                self.assertNotIn(velha, p, parte)
        grelha = solto(visivel(ler('tarefas/m6-u1/grelha/index.html'), so_main=False))
        self.assertIn('Não dizes a quem se dirige a voz nem para que serve o sonho, ou não citas nenhum verso.', grelha)
        self.assertIn('mas não explicas a diferença naquilo para que serve o sonho, ou a diferença não se apoia nos versos.', grelha)
        self.assertIn('Ficar na semelhança e não dizer a diferença.', grelha)
        self.assertIn('Dizer a diferença sem um verso que a mostre.', grelha)
        self.assertIn('outro soneto para recontar', grelha)
        # As mesmas palavras no enunciado.
        for frase in ('Indica a quem se dirige a voz.', 'Explica uma diferença.', 'Justifica com a função de «que» na sua oração.',
                      'Reconta «O Palacio da Ventura» em prosa, numa situação atual.'):
            self.assertIn(frase, enunciado)
        aquecimento = solto(ler(AQUECIMENTOS[0]))
        self.assertIn('a quem se dirige a voz e para que serve o sonho em cada soneto, com um verso dos tercetos; uma semelhança e uma diferença; '
                      'as orações do verso de Cesário e a função de «que»;', aquecimento)
        self.assertIn('«O Palacio da Ventura» recontado em prosa.', aquecimento)
        self.assertNotIn('reescrito', aquecimento)
        self.assertIn('Respondes às duas perguntas: os dois sonetos e o verso de Cesário', aquecimento)
        # O enunciado usa as palavras da grelha: a voz não é o poeta, o verso explicado e de que soneto é, o «que» que completa um
        # verbo ou retoma um nome.
        self.assertIn('A voz do soneto não é o poeta.', enunciado)
        self.assertIn('Tomar a voz do soneto pelo próprio poeta', grelha)
        self.assertIn('Explica cada verso que citares e diz de que soneto é.', enunciado)
        self.assertIn('sem dizer de que soneto é o verso', grelha)
        self.assertIn('Um «que» pode completar um verbo ou retomar um nome.', enunciado)
        self.assertIn('a relativa retoma um nome, a completiva completa um verbo', grelha)
        # m6-u2: o étimo dado no enunciado e «o que a imagem não mostra» (decisões do docente), e «uma hora definida».
        enunciado = visivel(ler(ENUNCIADOS[1]))
        self.assertIn('vêm do mesmo étimo latino: plenu-', enunciado)
        self.assertIn('Indica o que a imagem não mostra e explica porquê.', enunciado)
        for parte in ('grelha/', 'correcao/'):
            p = solto(visivel(ler(f'tarefas/m6-u2/{parte}index.html'), so_main=False))
            self.assertIn('o que a imagem não mostra, e porquê', p)
            self.assertNotIn('em vez de o procurar na lição', p)
        grelha = solto(visivel(ler('tarefas/m6-u2/grelha/index.html'), so_main=False))
        self.assertIn('Usar outro étimo, em vez do que o enunciado dá.', grelha)
        self.assertIn('A imagem não mostra a insegurança de que fala o verso: fica na legenda.', grelha)
        aquecimento = solto(ler(AQUECIMENTOS[1]))
        self.assertIn('um lugar por onde passas a pé, a uma hora definida.', aquecimento)
        self.assertNotIn('uma hora certa', aquecimento)
        self.assertIn('Respondes às duas perguntas: a oração, a estrofe e as duas palavras', aquecimento)
        self.assertIn('Na alínea a), mostra porquê: a oração completa um verbo ou retoma um nome?', solto(enunciado))
        self.assertIn('completa um verbo ou retoma um nome?', grelha)
        self.assertIn('Para cada recurso, copia as palavras que o mostram.', enunciado)
        self.assertIn('Nomear um recurso sem as palavras que o mostram.', grelha)
        # O guia, o índice e o mapa do M6.
        for rel, frases in ((GUIA, ['<span>Lê as duas perguntas e os temas A e B.</span>']),
                            (INDICE, ['aquecimento em cartões, duas perguntas, tema A ou B, revisão e fotografias no Teams.',
                                      'com consulta: aquecimento, duas perguntas, tema A ou B, revisão e fotografias no Teams.']),
                            (MAPA, [f'com aquecimento, duas perguntas, tema A ou B e grelha{N}/20;'])):
            fonte = ler(rel)
            self.assertNotIn('núcleo comum', fonte, rel)
            self.assertNotRegex(visivel(fonte, so_main=False, sem_nav=False), r'(?i)\bnúcleo\b')
            for frase in frases:
                self.assertIn(frase, fonte, rel)
        self.assertEqual(ler(INDICE).count('com consulta: aquecimento, duas perguntas, tema A ou B, revisão e fotografias no Teams.'), 2)
        for rel, n in ((INDICE, 2), (MAPA, 1)):
            self.assertEqual(len(MANIFESTO['files'][rel]['edits']), n, rel)

    # ---------- 13/11/2026: a autoavaliação colada no Teams e o par de trabalho saem do guia ----------

    def test_guia_sem_autoavaliacao_para_o_teams_nem_par_de_trabalho(self):
        # Decisão do docente (13/11/2026): no guia da tarefa, a «Autoavaliação» que se copiava para o Teams sai (a autoavaliação é só
        # para o aluno e não se entrega) e «pergunta ao teu par de trabalho» sai (não há trabalho de grupo nem de pares). Como nos
        # guias do M3 e do M5; nada entra no lugar.
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
                '3) pergunta ao teu par de trabalho.',
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
        # O que fica, com a frase certa: a regra com dois passos e o nome a dizer dois (no guia do M6, os passos vão na mesma linha).
        self.assertEqual(guia.count('<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica. '
                                    'Só depois levantas o braço.</div>'), 1)
        self.assertNotRegex(guia, r'\b3\) ')
        self.assertEqual(guia.count('No fim, verificas o trabalho com a lista da rubrica e copias tudo para a tarefa do Teams. '
                                    'O que escreves fica só neste telemóvel.</p>'), 1)
        self.assertEqual(guia.count('Cola na tarefa do Teams, juntamente com o trabalho. O docente vê o teu plano, as notas e a lista.</p>'), 1)
        # O resto do modelo que se copia fica: o plano, as notas e a lista de verificação; a seguir à lista vêm logo os botões.
        self.assertIn('<h2>Verificar antes de entregar</h2>\n<ul class="lista" id="r-verificar"></ul>\n<div class="fila">'
                      '<button class="btn" id="copiar">Copiar para o Teams</button>', guia)
        copiado = guia[guia.index('function texto(){'):guia.index('$("#copiar").onclick')]
        self.assertEqual(re.findall(r'"([A-ZÇÃÕÁÉÍÓÚ ]{5,})"', copiado), ['PLANO', 'NOTAS DE TRABALHO', 'VERIFICAÇÃO'])
        self.assertTrue(copiado.endswith('+p.nome)});return l.join("\\n")}\n'), copiado[-80:])
        self.assertEqual(re.findall(r'<h2[^>]*>([^<]*)</h2>', guia[guia.index('<section id="rota"'):guia.index('</section>', guia.index('<section id="rota"'))]),
                         ['', 'Os blocos de hoje', 'Verificar antes de entregar'])
        # Cada identificador que o código procura existe na página (nada fica a apontar para o bloco que saiu).
        codigo = guia[guia.index('var M="M6"'):]
        for ident in sorted(set(re.findall(r'\$\("#([\w-]+)"\)', codigo))):
            with self.subTest(identificador=ident):
                self.assertEqual(guia.count(f' id="{ident}"'), 1)
        # O código que fica é o dos guias do M3 e do M5 (o mesmo modelo, já sem a autoavaliação), salvo o nome do módulo e os dados.
        corpo6 = guia[guia.index('function texto(){'):guia.index('</script>', guia.index('function texto(){'))]
        for m in ('3', '5'):
            outro = ler(f'm{m}/guia-da-tarefa-m{m}/index.html')
            corpo = outro[outro.index('function texto(){'):outro.index('</script>', outro.index('function texto(){'))]
            self.assertEqual(corpo.replace('M' + m, 'M6').replace('m' + m, 'm6'), corpo6, m)
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

    def test_portefolio_sem_autoavaliacao_de_0_a_20_nem_trabalho_de_equipa(self):
        # Decisão do docente (13/11/2026): no portefólio do módulo saem a autoavaliação de 0 a 20 por parâmetro e «trabalho de
        # equipa», sem pôr nada no lugar (como nos portefólios do M5 e do M3).
        auto = ', e a tua autoavaliação de 0 a 20 por parâmetro, com razões'
        pagina, base = ler(PORTEFOLIO), antes(PORTEFOLIO)
        lido = visivel(pagina, so_main=False, sem_nav=False)
        self.assertEqual(base.count('trabalho de equipa'), 1)
        self.assertEqual(base.count(auto), 1)
        self.assertEqual(len(re.findall(r'(?i)auto-?avalia', base)), 1)
        self.assertNotRegex(pagina, r'(?i)auto-?avalia')
        self.assertNotRegex(pagina, r'(?i)trabalho de equipa|\bequipas?\b|trabalho de (?:grupo|pares)|par de trabalho')
        self.assertNotRegex(solto(pagina), r'\b0 a 20\b(?!0)')
        self.assertNotIn('por parâmetro', pagina)
        # O que fica: a linha do balanço com o cartão do percurso, e a lista do que o portefólio serve para avaliar.
        self.assertEqual(pagina.count('O cartão do percurso (passaporte, selos, desafios e respostas das unidades), copiado do Percurso do módulo.'
                                      '</td></tr></tbody></table>'), 1)
        self.assertEqual(solto(lido).count('É a base da avaliação qualitativa do módulo (40 %): autonomia, responsabilidade, pensamento crítico, entre '
                                           'outros. Não tem nota própria; o que faltar pesa nos parâmetros.'), 1)
        # Nada entrou no lugar: a página é a do main de partida menos os dois pedaços, letra a letra.
        edits = MANIFESTO['files'][PORTEFOLIO]['edits']
        self.assertEqual(len(edits), 2)
        self.assertEqual(edits[0]['old'].replace(auto, ''), edits[0]['new'])
        self.assertEqual(edits[1]['old'].replace(' trabalho de equipa,', ''), edits[1]['new'])
        self.assertEqual(base.replace(auto, '').replace(' trabalho de equipa,', ''), pagina)
        self.assertEqual(len(base) - len(pagina), len(auto) + len(' trabalho de equipa,'))
        do_commit = do_main(PORTEFOLIO)
        if do_commit is not None:
            self.assertEqual(do_commit, base)

    # ---------- as regras do texto ----------

    def test_regras_do_texto(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                # (nos enunciados, os versos de Antero e de Cesário ficam como no original: o travessão de «Silencio e escuridão — e
                # nada mais!», o «professor» de «Ao Gás» e os «jogos malabares» de «Noite Fechada» são dos poetas)
                texto = visivel(sem_textos(fonte))
                baixo = texto.lower()
                for palavra in ('professor', 'jogar', 'jogador', 'ficha', 'folha', 'em grupo', 'em pares', 'fernandes'):
                    self.assertNotIn(palavra, baixo, palavra)
                self.assertNotRegex(baixo, r'\bjog(?:o|os|a|am|ar)\b')
                self.assertNotIn('—', texto)
                self.assertNotRegex(texto, r'\bQual (?!d[aeo]s? )')
                self.assertNotRegex(texto, r'\b[Vv]ocê\b')
        for slug in SLUGS:
            fonte = ler(f'tarefas/{slug}/index.html')
            self.assertEqual(len(re.findall(r'<div class="tt-versos">', fonte)), 4 if slug == 'm6-u1' else 6)
            # Na m6-u1, o único travessão da página é o do último verso de «O Palacio da Ventura»; na m6-u2 não há nenhum. As palavras
            # que não usamos e que os poetas usam estão só nos versos.
            self.assertEqual(visivel(fonte).count('—'), 1 if slug == 'm6-u1' else 0)
            if slug == 'm6-u2':
                versos = ' '.join(re.findall(r'<div class="tt-versos">.*?</div>', fonte, re.S))
                for palavra in ('Meu velho professor nas aulas de latim!', 'os jogos malabares', 'joga-se o dominó', 'as folhas das navalhas'):
                    self.assertEqual(versos.count(palavra), 1, palavra)
            fonte = sem_textos(fonte)
            texto = visivel(fonte)
            principal = fonte[fonte.index('<main'):fonte.index('</main>')]
            with self.subTest(enunciado=slug):
                # «·» só no molde comum (o título da janela e a navegação), nunca numa frase nossa.
                self.assertNotIn('·', texto)
                # Títulos de livros em itálico (fora dos rótulos para leitores de ecrã); os títulos dos poemas ficam entre «».
                sem_italicos = re.sub(r'<i>[^<]*</i>|alt="[^"]*"|aria-label="[^"]*"', '', principal)
                for obra in ('Os Sonetos Completos', 'O Livro de Cesário Verde', 'Rhythmas', 'Odisseia', 'In Memoriam', 'Lavadeiras portuguesas'):
                    self.assertNotIn(obra, sem_italicos, obra)
                self.assertGreaterEqual(principal.count('<i>Os Sonetos Completos</i>' if slug == 'm6-u1' else '<i>O Livro de Cesário Verde</i>'), 4)
                for poema in ('Ideal', 'A um poeta', 'O Palacio da Ventura', 'Ave-Marias') if slug == 'm6-u1' else (
                        'O Sentimento dum Ocidental', 'Ao Gás', 'Horas Mortas', 'Noite Fechada', 'Ave-Marias', 'Num Bairro Moderno'):
                    self.assertGreaterEqual(texto.count(f'«{poema}»'), 1, poema)
                    # («Ideal» é também uma palavra dos versos citados nos exemplos: «já sem Ideal», «Depuz do Ideal»)
                    if poema != 'Ideal':
                        self.assertNotRegex(texto, r'(?<![«“])' + re.escape(poema) + r'(?![»”])', poema)
                # Referências que não se partem (U+00A0), como nas páginas do M3, do M1 e do M5.
                for padrao in (r'\b(?:Texto|Textos|Pergunta|pergunta|Tema|Temas|tema|Lição|lição|canto|Canto|estância|estâncias|verso|versos|Imagem|aula|Passo|Passos|Alínea|Alíneas|alínea|Estrofe|parágrafo|parágrafos|passagem|parte|partes|Plano|plano|Fotografia|fotografia) (?:\d|[AB]\b|[IVX]+\b|F\d|[a-h]\)|\[)',
                               r'\d (?:min|minutos|palavras|versos)\b', r'\b[IVX]+, \d', r'(?:\d|\]) (?:a|e|ou) (?:\d|\[)', r'\bA (?:ou|e) B\b',
                               r'\b[IVX]+ (?:a|e) [IVX]+\b', r'\b(?:cap\.|capítulo) [IVXLC]+\b', r'\bséculo [IVX]+\b', r'\bc\. \d'):
                    # (o «Tema » que só os leitores de ecrã leem antes da letra de cada tema, no molde comum, fica de fora)
                    self.assertNotRegex(visivel(fonte.replace('<span class="sr-only">Tema </span>', '')), padrao)
                # As falas do aluno em discurso direto ficam entre «» (nenhuma aspa direita nem curva nas nossas frases). Só os nomes
                # de duas lições, nas linhas de fonte do dossiê (a chave antiga, igual à de antes), trazem aspas curvas dentro de «».
                sem_origens = re.sub(r'<span class="tf-origem">.*?</span>', ' ', fonte, flags=re.S)
                self.assertNotRegex(visivel(sem_origens), r'[“”"]')
                self.assertEqual(sorted(set(re.findall(r'«[^«»]*“[^«»]*»', texto))),
                                 [] if slug == 'm6-u1' else ['«Da “Noite Fechada” às “Horas Mortas”»', '«“Ave-Marias”»'])
        # No dossiê (a chave antiga, igual à de antes), o verso e a parte ficam presos ao número ao escrever a página.
        self.assertIn(f'corrige o verso{N}6: «rota»', ler(ENUNCIADOS[0]))
        self.assertEqual(ler(ENUNCIADOS[1]).count(f'<li>Na parte{N}II, '), 2)
        # O molde não é o piloto por aprovar: os comentários dizem que foi aprovado.
        for rel in ('scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py', 'scripts/grelhas_tarefas.py', 'assets/task-textos.css', 'assets/task-reader.js',
                    'scripts/tarefas_faceis_m6_20261113.py'):
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
                self.assertIn(f'<p class="task-grelha"><a href="grelha/">Grelha{N}/20: como é avaliado e autoavaliação</a></p>', cabeca)
                # Uma só pergunta opcional, num desdobrável, com três opções, uma certa, explicações diferentes.
                self.assertEqual(p.perguntas, [('1', True)])
                self.assertEqual(len(p.opcoes), 3)
                self.assertEqual(sum(a['data-correct'] == 'true' for a in p.opcoes), 1)
                self.assertEqual(len({a['data-response'] for a in p.opcoes}), 3)
                self.assertEqual(len(re.findall(r'<span class="task-letter">[ABC]<span class="sr-only">:</span></span> ', fonte)), 3)
                # Os recursos: os mesmos do molde de 28/10, o leitor do molde novo e a folha desta versão (facil-10: a folha ganhou as
                # regras do que as lições não dão e das partes de 44 versos; as páginas do M3, do M1 e do M5 pedem as de antes).
                self.assertLess(fonte.index('assets/relogio.js'), fonte.index('pt-lessons/casca.js'))
                for recurso in ('task-choice.css?v=20261028-escolha-2', 'task-90.js?v=20261027-compact-1', 'task-reader.js?v=20261112-facil-7',
                                'task-textos.css?v=20261113-facil-10', 'info-i.css?v=20261105', 'info-i.js?v=20261105'):
                    self.assertEqual(fonte.count(recurso), 1, recurso)
                for fora in ('task-clock', 'rondas', '10/10/60/10'):
                    self.assertNotIn(fora, fonte)
                # As duas linhas finais, a entrega e a letra do tema.
                for frase in ('<h2 id="finais-titulo">Duas linhas finais</h2>', '<h2>Entrega no Teams</h2>', '<h2 id="entregar-title">Antes de entregar, verifica</h2>'):
                    self.assertEqual(fonte.count(frase), 1, frase)
                # Dossiê do tema B: cada facto com a sua fonte e a ligação, que existe; citações e números na página para onde aponta.
                # 13/11/2026: revisão. Em papel, os factos do dossiê e os passos de cada tema não se partem entre duas páginas
                # (classe tf-juntos, da chave «juntos_em_papel»; confere-se no PDF em tests/browser_tarefas_faceis_m6.py).
                dossie = re.findall(r'<section class="task-dossier tf-dossie tf-juntos".*?</section>', fonte, re.S)
                self.assertEqual(len(dossie), 1)
                self.assertIs(d['facil']['juntos_em_papel'], True)
                self.assertEqual(fonte.count('<ol class="tf-passos tf-juntos">'), 2)
                self.assertEqual(fonte.count('tf-juntos'), 3)
                self.assertIn(f'<h4 id="dossie">Dossiê do tema{N}B</h4>', dossie[0])
                factos = re.findall(r'<li>(.*?)<span class="tf-origem">Fonte: <a href="([^"]+)">(.*?)</a></span></li>', dossie[0])
                self.assertEqual(len(factos), dossie[0].count('<li>'))
                self.assertEqual([(solto(x), h, n) for x, h, n in factos], [(solto(x['facto']), x['href'], x['fonte']) for x in d['dossie']])
                self.assertEqual(len(factos), 6)
                for facto, href, _ in factos:
                    alvo = solto(plana(str((Path(rel).parent / href / 'index.html').as_posix()).replace('tarefas/' + slug + '/../../', '')))
                    texto = solto(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', facto))))
                    for pedaco in re.findall(r'«([^»]+)»', texto) + re.findall(r'\b\d{3,4}\b', texto):
                        self.assertIn(pedaco, alvo, (href, pedaco))
                # Todas as ligações internas existem; as âncoras apontam para ids da página; para fora, só o molde comum.
                licoes = [h for h in p.ligacoes if '/m6/licao-' in h]
                self.assertGreaterEqual(len(set(licoes)), 5)
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
                self.assertEqual(sorted({h for h in p.ligacoes if h.startswith('#texto-')}),
                                 ['#texto-1', '#texto-2', '#texto-3', '#texto-4'] if slug == 'm6-u1' else ['#texto-1', '#texto-2', '#texto-3', '#texto-5', '#texto-6'])
                self.assertIn('#dossie', p.ligacoes)
                # «Rever a matéria»: uma linha por pergunta ou tema; o nome da página e os nomes das secções entre «» são os da lição.
                rever = re.search(r'<ul class="tf-rever-lista">(.*?)</ul>', fonte, re.S).group(1)
                itens = re.findall(r'<li><b>((?:Pergunta|Tema|Temas)\xa0(?:[12AB]|A\xa0e\xa0B))\.</b> Lição\xa0F\d\d, <a href="([^"]+)">(.*?)</a>\.? (.*?)</li>', rever)
                self.assertEqual(len(itens), rever.count('<li>'))
                self.assertEqual(len(itens), 5 if slug == 'm6-u1' else 6)
                self.assertEqual({solto(x[0]) for x in itens}, {'Pergunta 1', 'Pergunta 2', 'Tema B'} | ({'Temas A e B'} if slug == 'm6-u1' else {'Tema A'}))
                motor = plana('assets/pt-lessons/jogo.js')
                for _, href, nome, resto in itens:
                    alvo = plana(href.replace('../../', '') + 'index.html')
                    self.assertIn(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', nome))), alvo, href)
                    self.assertRegex(href, r'^\.\./\.\./m6/licao-m6-f\d\d/$')
                    self.assertIn(f'Lição{N}F{href[-3:-1]}, <a href="{href}">', rever)
                    seccoes = re.findall(r'«([^»]+)»', resto)
                    self.assertGreaterEqual(len(seccoes), 1, resto)
                    for secao in seccoes:
                        secao = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', secao)))
                        self.assertTrue(secao in alvo or secao in motor, (href, secao))
                self.assertEqual(fonte.count(f'<p class="tf-p">{d["facil"]["rever_texto"]}</p>'), 1)
                self.assertEqual(d['facil']['rever_texto'], 'Os textos já estão nesta página. As lições servem para rever a matéria.')
                # O que serve aos dois temas: os textos, num desdobrável fechado no ecrã e aberto em papel; sem imagens.
                self.assertEqual(fonte.count('<details class="tf-so-tema tf-dois-temas"><summary>'), 1)
                for marca in ('tf-comum', 'tf-figs', 'tf-fig', 'tt-prosa', 'tt-par', 'tt-longo'):
                    self.assertNotIn(f'class="{marca}', fonte)
        leitor = ler('assets/task-reader.js')
        self.assertIn('page.getAttribute("data-task-opening")||(compact?"Enunciado":"A aula de tarefa")', leitor)
        self.assertIn('node.getAttribute("data-task-card-name")||', leitor)
        self.assertIn('(page.getAttribute("data-task-index")==="nomes"?"":String(i+1)+". ")+item.label', leitor)

    # ---------- as tarefas dos outros módulos não mudam ----------

    def test_as_outras_tarefas_nao_mudam(self):
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(len(FICHEIROS), 17)
        self.assertEqual(sorted(OUTRAS + SLUGS), sorted(p.stem for p in (ROOT / 'docs/pedagogia/tarefas-escolha').glob('*.json')))
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in OUTRAS:
            with self.subTest(tarefa=slug):
                no_molde = slug in NO_MOLDE
                self.assertEqual('facil' in json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json')), no_molde)
                self.assertEqual(bool({'autoavaliacao_so_tua', 'trocas_aluno'} & set(grelhas[slug])), no_molde)
                pagina = ler(f'tarefas/{slug}/index.html')
                if no_molde:
                    # As páginas do M3, do M1 e do M5 continuam a pedir a folha de antes e não usam nenhuma das marcas novas.
                    self.assertEqual(pagina.count(f'task-textos.css?v=2026111{"2" if slug.startswith("m3") else "3"}-{FOLHA[slug]}"'), 1)
                    for marca in ('facil-10', 'tt-falta', 'tt-pagina', 'tf-juntos'):  # 13/11/2026: revisão, mais «tf-juntos»
                        self.assertNotIn(marca, pagina)
                else:
                    for marca in ('data-task-facil', 'task-textos.css', 'facil-', 'class="tf-', 'class="tt-'):
                        self.assertNotIn(marca, pagina)
                    self.assertIn('task-reader.js?v=20261028-escolha-2', pagina)
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertNotIn(f'tarefas/{slug}/{parte}index.html', MANIFESTO['files'])
        # Todas as páginas de tarefas/ que não são as oito desta camada (as tarefas, grelhas, correções e aquecimentos dos outros
        # módulos) são as do main de partida, byte a byte; e os dados também.
        todas = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'tarefas').rglob('*') if p.is_file())
        self.assertGreater(len(todas), 60)
        iguais = 0
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
                    self.assertEqual(conteudo, r.stdout)
        self.assertIn(de_cima, (0, 10))
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
        # 13/11/2026: por cima desta camada ficam as três tarefas do M7 mais fáceis de fazer (tarefas_faceis_m7_20261113): a ordem ganha mais
        # uma posição, com a mesma exigência (51 camadas).
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(len(verificar_camadas.LAYERS), 51)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 51)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertIn('não se edita à mão', MANIFESTO['_nota'])
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(len(TROCAS), sum(len(v['edits']) for v in MANIFESTO['files'].values()))
        self.assertEqual(len(MANIFESTO['files']), 17)
        # 13/11/2026: confere-se com a camada do M7, que está por cima, desfeita primeiro.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar', '--desfazer-antes', M7F],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 17 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        for t in TROCAS:
            self.assertTrue(t['achado'].startswith('13/11/2026: '), t['local'])
            self.assertIn(t['ocorrencias'], (1, 2))
        self.assertEqual([t['ficheiro'] for t in TROCAS if t['ocorrencias'] == 2], [INDICE])
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
                self.assertEqual(undo_tarefas_faceis_m6_1113(rel, atual), base)
                self.assertEqual(undo_tarefas_faceis_m6_1113(rel, base), base)
        # Com as camadas das tarefas do M5, do M1 e do M3, que ficam por baixo, partilha só os dados das grelhas. Aí, o desfazer da
        # auditoria tira primeiro esta e depois as outras; nos outros ficheiros, o desfazer das camadas de baixo dá a base desta.
        m5, m1, m3 = (json.loads(ler(x))['files'] for x in (M5F, M1F, M3F))
        for outra in (m5, m1, m3):
            self.assertEqual(set(MANIFESTO['files']) & set(outra), {GRELHAS})
        for rel in MANIFESTO['files']:
            if rel != GRELHAS:
                for desfazer in (undo_tarefas_faceis_m5_1113, undo_tarefas_faceis_m1_1113, undo_tarefas_faceis_m3_1112):
                    self.assertEqual(desfazer(rel, ler(rel)), antes(rel), rel)
        self.assertEqual(sha_lf(antes(GRELHAS)), m5[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m5_1113(GRELHAS, ler(GRELHAS))), m5[GRELHAS]['base_sha256_lf'])
        self.assertEqual(m5[GRELHAS]['base_sha256_lf'], m1[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m1_1113(GRELHAS, ler(GRELHAS))), m1[GRELHAS]['base_sha256_lf'])
        self.assertEqual(m1[GRELHAS]['base_sha256_lf'], m3[GRELHAS]['after_sha256_lf'])
        sem_as_quatro = undo_tarefas_faceis_m3_1112(GRELHAS, ler(GRELHAS))
        self.assertEqual(sha_lf(sem_as_quatro), m3[GRELHAS]['base_sha256_lf'])
        for chave in ('autoavaliacao_so_tua', 'trocas_aluno'):
            self.assertNotIn(chave, sem_as_quatro)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m6_20261113', ROOT / 'scripts/tarefas_faceis_m6_20261113.py')
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        todas, finais = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(sorted(C.FICHEIROS), sorted(FICHEIROS))
        self.assertEqual(C.BASE_COMMIT, BASE_COMMIT)
        # As quatro páginas do módulo mudam só nas trocas escritas à mão: doze no guia (as cinco saídas são as dos guias do M3 e do
        # M5), duas no índice, uma no mapa e duas no portefólio.
        modulo = (GUIA, INDICE, MAPA, PORTEFOLIO)
        self.assertEqual(sorted((f, a, b, n) for f, a, b, n, _ in C.EDICOES),
                         sorted((t['ficheiro'], t['antigo'], t['novo'], t['ocorrencias']) for t in TROCAS if t['ficheiro'] in modulo))
        self.assertEqual({f: [x for x, *_ in C.EDICOES].count(f) for f in modulo}, {GUIA: 12, INDICE: 2, MAPA: 1, PORTEFOLIO: 2})
        outras = {}
        for nome in ('tarefas_faceis_m3_20261112', 'tarefas_faceis_m1_20261113', 'tarefas_faceis_m5_20261113'):
            spec = importlib.util.spec_from_file_location(nome, ROOT / f'scripts/{nome}.py')
            outras[nome] = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(outras[nome])
        self.assertEqual([(a, s, d, c) for f, a, s, d, c in C.SAI if f == GUIA], [(a, s, d, c) for f, a, s, d, c in outras['tarefas_faceis_m3_20261112'].SAI])
        # As camadas do M3, do M1 e do M5, que ficam por baixo e partilham os dados das grelhas com esta, continuam a dar o seu JSON,
        # com esta desfeita primeiro.
        for nome, modulo_ in outras.items():
            self.assertEqual(modulo_.construir()[0], json.loads(ler(f'scripts/{nome}.json')), nome)

    def test_leitura_historica_dos_enunciados(self):
        # Os contratos históricos leem as tarefas como eram antes do pedido #192 (scripts/tarefas_claras_historico.py). Com esta camada
        # por cima, a leitura dá a base do manifesto do #192, letra a letra, nos enunciados e nos dados da M6-U1 e da M6-U2, a partir
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
                # do M5, do M1 e do M3, tira as quatro, pela ordem.
                esperado = m3[rel]['base_sha256_lf'] if rel == GRELHAS else MANIFESTO['files'][rel]['base_sha256_lf']
                self.assertEqual(sha_lf(sem), esperado)
                self.assertEqual(historico.desfazer_faceis(rel, sem), sem)
                if rel != GRELHAS:
                    self.assertEqual(sem, antes(rel))
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer_faceis(path, text):'):fonte.index('def desfazer(path, text):')]
        self.assertLess(corpo.index('TAREFAS_FACEIS_M6.get(rel)'), corpo.index('TAREFAS_FACEIS_M5.get(rel)'))
        self.assertLess(corpo.index('TAREFAS_FACEIS_M5.get(rel)'), corpo.index('TAREFAS_FACEIS_M1.get(rel)'))
        self.assertLess(corpo.index('TAREFAS_FACEIS_M1.get(rel)'), corpo.index('TAREFAS_FACEIS_M3.get(rel)'))
        self.assertIn("_sha_lf(text) == por_cima['after_sha256_lf']", corpo)
        self.assertIn("assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M6 mais fáceis de fazer não confere: {rel}'", corpo)

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        # A auditoria desfaz primeiro esta camada; o corte da Sala também; as bases das camadas que partilham ficheiros com ela também.
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_tarefas_faceis_m6_1113(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m5_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m6_1113\(path, text\)\n')
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m1_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m5_1113\(path, text\)\n')
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m3_1112\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m1_1113\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('tarefas-faceis-m6-edits-20261113.json'), sala.index('tarefas-faceis-m5-edits-20261113.json'))
        self.assertLess(sala.index('tarefas-faceis-m5-edits-20261113.json'), sala.index('tarefas-faceis-m1-edits-20261113.json'))
        for rel in ('scripts/cuidado_m6_20261108.py', 'scripts/cuidado_m7_20261111.py'):
            self.assertIn('return desfazer_faceis(rel, (ROOT / rel).read_bytes().decode(\'utf-8\'))', ler(rel), rel)
        indices = ler('scripts/cartaz_indices_148_20261106.py')
        corpo = indices[indices.index('def base(rel):'):]
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M6.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M5.read_text'))
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M5.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M1.read_text'))
        for rel in ('scripts/tarefas_faceis_m3_20261112.py', 'scripts/tarefas_faceis_m1_20261113.py', 'scripts/tarefas_faceis_m5_20261113.py'):
            fonte = ler(rel)
            leitura = fonte[fonte.index('def ler(rel):'):fonte.index('def base(rel):')]
            self.assertIn("m6 = ROOT / 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'", leitura, rel)
            if 'm5 = ROOT' in leitura:
                self.assertLess(leitura.index("m6 = ROOT / 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'"),
                                leitura.index("m5 = ROOT / 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'"), rel)
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs', 'tests/browser_creditos_i_pt1.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((tarefasFaceisM6['), texto.index('((tarefasFaceisM5['), rel)
            self.assertLess(texto.index('((tarefasFaceisM5['), texto.index('((tarefasFaceisM1['), rel)
            self.assertEqual(texto.count('((tarefasFaceisM6['), texto.count('((tarefasFaceisM5['), rel)
        # Nos fluxos e nos outros testes, cada cadeia de desfazer começa por esta camada, sem nada entre ela e a das tarefas do M5.
        cadeias = 0
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name in ('test_tarefas_faceis_m6.py', 'test_tarefas_faceis_m5.py', 'test_tarefas_faceis_m1.py', 'test_tarefas_faceis_m3.py'):
                continue
            texto = '\n'.join(linha for linha in p.read_text('utf-8').split('\n') if not linha.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + M5F), plano.count(f'--desfazer-antes {meu} --desfazer-antes {M5F}'))
                self.assertEqual(plano.count('--desfazer-antes {t5}'), plano.count('--desfazer-antes {t6} --desfazer-antes {t5}'))
                self.assertEqual(plano.count('--desfazer-antes {T5}'), plano.count('--desfazer-antes {T6} --desfazer-antes {T5}'))
                self.assertEqual(plano.count(f"ROOT/'{M5F}',"), plano.count(f"(ROOT/'{M7F}',ROOT/'{meu}',ROOT/'{M5F}',"))  # (13/11/2026: a lista abre pela camada do M7)
                self.assertEqual(plano.count("ROOT/'{t5}',"), plano.count("(ROOT/'{t7}',ROOT/'{t6}',ROOT/'{t5}',"))  # (13/11/2026: idem)
                self.assertEqual(plano.count("ROOT/'{T5}',"), plano.count("(ROOT/'{T7}',ROOT/'{T6}',ROOT/'{T5}',"))  # (13/11/2026: idem)
                self.assertEqual(plano.count("' + T5"), plano.count("' + T6 + ' --desfazer-antes ' + T5"))
                # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça.
                if p.suffix == '.yml':
                    # 13/11/2026: à cabeça fica agora a camada do M7, e esta logo a seguir, sem nada pelo meio.
                    self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count('--verificar --desfazer-antes ' + M7F + ' --desfazer-antes ' + meu))
                cadeias += plano.count(f'--desfazer-antes {meu} --desfazer-antes {M5F}')
        self.assertGreater(cadeias, 40)
        # Nos testes das camadas do M5, do M1 e do M3, as cadeias são as mesmas, com esta à cabeça.
        # 13/11/2026: com a camada do M7 à cabeça, e esta logo a seguir.
        self.assertIn("plano.count(f'--verificar --desfazer-antes {M7F} --desfazer-antes {M6F} --desfazer-antes {meu}')", ler('tests/test_tarefas_faceis_m5.py'))
        self.assertIn("plano.count(f'--verificar --desfazer-antes {M7F} --desfazer-antes {M6} --desfazer-antes {M5} --desfazer-antes {meu}')", ler('tests/test_tarefas_faceis_m1.py'))
        self.assertIn("plano.count(f'--verificar --desfazer-antes {M7F} --desfazer-antes {M6} --desfazer-antes {M5} --desfazer-antes {M1} --desfazer-antes {meu}')", ler('tests/test_tarefas_faceis_m3.py'))
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m6_20261113.json --manifesto {meu} --verificar --desfazer-antes {M7F}\n', tarefas)  # 13/11/2026: no fluxo, esta camada confere-se com a do M7 desfeita primeiro, e as de baixo com as duas
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m5_20261113.json --manifesto {M5F} --verificar --desfazer-antes {M7F} --desfazer-antes {meu}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m1_20261113.json --manifesto {M1F} --verificar --desfazer-antes {M7F} --desfazer-antes {meu} --desfazer-antes {M5F}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m3_20261112.json --manifesto {M3F} --verificar --desfazer-antes {M7F} --desfazer-antes {meu} --desfazer-antes {M5F} --desfazer-antes {M1F}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m6.py' -v", tarefas)
        self.assertIn('        run: python tests/browser_tarefas_faceis_m6.py\n', tarefas)
        self.assertTrue((ROOT / 'tests/browser_tarefas_faceis_m6.py').is_file())
        # O trabalho das aulas de tarefa continua com 40 minutos de limite (esta camada não lhe mexe).
        self.assertEqual(re.findall(r'\n  lessons:\n(?:    [^\n]*\n)*?    timeout-minutes: (\d+)\n', tarefas), ['40'])
        # Os fluxos que conferem ou desfazem esta camada arrancam quando ela muda.
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/tarefas_faceis_m6_20261113.*', meu):
                self.assertIn(f"'{caminho}'", texto, nome)
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')):
            texto = p.read_text('utf-8')
            if 'tarefas-faceis-m6-edits-20261113' in texto:
                self.assertRegex(texto.split('\non:')[0], r'\n# 13/11/2026: as duas tarefas do M6 mais fáceis de fazer e «tudo junto» no M6, a camada tarefas_faceis_m6_20261113 ', p.name)
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
        for rel in FICHEIROS + ['scripts/tarefas_faceis_m6_20261113.py', CAMADA_REL, meu, 'scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py',
                                'scripts/grelhas_tarefas.py', 'scripts/aquecimentos.py', 'scripts/tarefas_claras_historico.py',
                                'assets/task-textos.css', 'assets/task-reader.js', 'tests/test_tarefas_faceis_m6.py',
                                'tests/browser_tarefas_faceis_m6.py']:
            self.assertTrue(any(q.match(rel) for q in padroes), rel)


if __name__ == '__main__':
    unittest.main()
