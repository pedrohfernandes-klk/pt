#!/usr/bin/env python3
"""12/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M9 do Português.

Constrói scripts/cuidado_m9_20261112.json, a camada literal cuidado_m9_20261112, com os achados CONFIRMADOS da varredura do M9
(refeita a 9/11 e conferida a 11/11, só leitura, sobre o main 4bf4a053): dos 52 confirmados (7 A, 41 B e 4 C) entram 44: os 7
achados A (tabelas onde há itens paralelos), 33 de referências e números que se partiam (B) e os 4 casos do mesmo tipo (C).
Ficam de fora, por decisão já tomada para todos os módulos, como do M1 ao M8, os 6 achados B dos diapositivos (20), das três
provas rápidas (48, 49 e 50), dos questionários (51) e da página «todos» (56): essas páginas não mudam. Ficam também de fora os 2
achados B dos painéis da F04 e da F10 (41 e 44): as ocorrências confirmadas estão todas no material do relâmpago (MATERIAL) e nas
pistas do «Quem sou eu?» (ATL), que não mudam. Os 8 achados que a conferência recusou (7, 8, 12, 13, 14, 16, 17 e 18) também não
entram. A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/cuidado-m9-edits-20261112.json:

  python3 scripts/cuidado_m9_20261112.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m9_20261112.json --manifesto tests/fixtures/cuidado-m9-edits-20261112.json \\
      --base-commit 899576905d085e9552a70fe82d050c13f78dda2f --nota "…"

Fica por cima da decisão 152 no M8 (cuidado_m8_20261112, no ramo do pedido #195, commit 0c85d555, com o main 40f9505c já
dentro), que não toca em nenhum ficheiro desta camada.

Segue o modelo da camada do M8 (scripts/cuidado_m8_20261112.py), com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como do M1 ao M8: class apoio-tabela, th scope=col no cabeçalho, th
  scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader, rowheader, cell), porque no
  telemóvel a tabela passa a display:block. Dentro do JSON dos cartões, as aspas vão com barra (\\"). São sete: os pesos da
  avaliação no índice, no guia e no mapa do módulo (achados 0, 1 e 2, como no M5, no M7 e no M8: o rótulo num parágrafo, a tabela
  Elemento/Peso com a coluna do peso em 5,5 rem, e o resto da frase no p.avaliacao-tarefas, como estava); as noções das caixas
  «Recorda» da F01, da F02 e da F03 (achados 3, 4 e 5: Noção/O que é; na F02, a frase dos dois nomes fica num parágrafo a
  seguir; na F02 e na F03, a primeira coluna leva 30 %, como as caixas de termos do M6, porque «Caracterização» e
  «Intertextualidade» não cabiam nos 25 % da folha no ecrã largo e partiam-se na última letra); e os quatro termos da caixa «Recorda» da F10 (achado 6: Termo/O que é; a frase dos conectores fica num parágrafo a
  seguir). Cada página com uma tabela nova carrega assets/pt-lessons/apoios-tabelas.css antes de assets/appearance.css, na
  versão do M1 (20261106.1: a folha não muda).
- B: U+00A0 (espaço que não quebra) nos espaços que a proposta final prende, e U+2060 (junção de palavras) logo a seguir ao
  hífen da sigla «M9-Fxx». A proposta do M9 dá cada par como a cadeia exata a procurar, com o contexto mínimo que a separa do que
  fica de fora («D. João V p», «século XVIII"», «capítulo XXI)»): cada par conta-se nesse contexto (com a palavra inteira; à
  direita, o contexto pode acabar a meio de uma palavra) e fora das cadeias maiores dos outros pares da página, e «de» diz a
  referência que o par prende; a troca leva só os espaços que muda, com o mínimo de contexto que a distingue (quando o mesmo
  texto aparece num sítio que não muda e nenhuma janela igual para todas serve, cada ocorrência cresce por si). Nas datas, a
  proposta prende o dia ao «de» e o ano ao «de», como do M5 ao M8; nas listas («capítulos I, XIX e XXI», «pp. 291 a 293»)
  prende o nome ao primeiro número e o «e» ou o «a» ao último; «D. João V» prende os dois espaços. Ficam de fora: os «alt» (e
  aria-label, href, title, content e data-titulo, que vira o title do vídeo), o <title>, o texto dos desenhos (SVG), a «frase»
  dos cartões sublinhar, as «palavras» dos cartões frase e os «passos» dos cartões ordenar, as notas internas dos dados, a casca
  das lições (abaixo) e o que a conferência deixou com o contexto dos pares ou tirou com a razão: os excertos do romance, as
  citações entre «» e as «linhas» dos versos, «D.» com nome e sem numeral («D. Maria Ana», «D. Sebastião»), o mês e o ano sem
  dia («outubro de 1730»), «52 mil» e o traço entre ano e lugar do mapa.
- C: «Três antes de mim», no guia, em lista numerada (achado 9, o mesmo trecho, letra a letra, dos guias do M5, do M7 e do
  M8); as quatro linhas de ação do «O essencial» da F01 em lista, com a frase seguinte num parágrafo (achado 11); as quatro
  estações da oficina da F13 em lista numerada, com a frase seguinte num parágrafo (achado 15); e, no portefólio, os oito nomes
  de ficheiro que estavam em texto simples em <code>, como os outros seis, com <wbr> a seguir a cada «_», um <wbr> nos dois nomes
  compridos que já estavam em <code> e «td code{white-space:nowrap}» na folha da página (achado 10, a proposta final, como nos
  portefólios do M5 e do M7: os nomes só mudam de linha nos pontos marcados).
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois. Nas tabelas dos pesos, os números já vão com
  o espaço que não quebra (a conferência tirou esses pares dos achados B 22, 23 e 36).

A casca das lições (migalhas, «Estás em: Lição M9-Fxx», o título escondido e a sigla «Lição M9-Fxx» do rodapé) não muda aqui,
ficheiro a ficheiro: muda no molde, como do M1 ao M8. Nas outras páginas (índice, guia, mapa e portefólio do módulo e o caderno
de campo da visita), a proposta final conta as migalhas e o «3.º ano» fica preso nas migalhas e no cabeçalho.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e das listas (cai o negrito dos nomes que passam a
cabeçalho de linha, os dois pontos e o ponto final de cada célula e os «1) 2) 3)» que a lista numerada do guia substitui; os
cabeçalhos «Elemento», «Peso», «Noção», «Termo» e «O que é» são os da proposta) e os espaços invisíveis. «séc. XVIII» fica
abreviado, só com o espaço preso (como o «séc. XIII» do M1). O script calcula as trocas sobre a base (a página com esta camada
desfeita pelo manifesto, quando ele já existe): pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.

Páginas geradas: as tarefas da M9-U1 e da M9-U2 (scripts/tarefas_escolha.py) mudam nos dados (docs/pedagogia/tarefas-escolha/
m9-u1.json e m9-u2.json: «nao_partir», como do M1 ao M8, que prende os números do molde e a meta descrição, e os achados B);
os dados estão na mesma camada e as páginas regeneram-se sem diferenças. Os aquecimentos, as grelhas e as correções do M9 não
têm achados. As lições F14, F15 e F16 são geradas (scripts/gerar_licoes_20261101.py): os textos mudam nas fontes
(scripts/licoes_20261101.py e, para o retorno que as notas do docente da F14 repetem, scripts/revisao_confirmacao_20261101.py,
fora da camada, como no M5, no M6 e no M8), e as lições e as notas da F14 mudam aqui e saem iguais do gerador. Os cartões das
lições F11, F12 e F13 estão em m9/recursos/f11.js, f12.js e f13.js (ficheiros estáticos, sem gerador, que as páginas das
lições carregam): mudam aí. Os painéis de projeção da F01, da F02, da F03, da F05 e da F07 seguem os enunciados dos cartões que
mudaram (a lista CARTOES e o seletor); o material do relâmpago (MATERIAL) segue a lição antes das camadas de cuidado
(tests/test_sala_desligada.py compara-o com ela) e não muda, como do M1 ao M8, e as pistas do «Quem sou eu?» (ATL) também não.
As cópias dos cartões no banco das provas rápidas do índice (var U) estão nos pares do achado 23. A resposta certa e o retorno
do cartão 11 da F01 estão copiados nas sessões do Exame (assets/exame/sessoes.json, sessão s19), que
tests/test_exame_alignment.py compara com a lição: mudam como na lição (como a cópia da M6-F01 no M6).

As camadas de baixo que mexem no mesmo texto desfazem primeiro esta: os geradores do desenho comum dos índices
(scripts/cartaz_indices_148_20261106.py), dos acertos dos índices (scripts/indices_acertos_20261107.py) e dos créditos atrás de
um «i» do pedido pt-1 (scripts/creditos_i_pt1_20261107.py: o crédito da imagem documental do índice do M9, onde esta camada
prende «século XVIII»).

12/11/2026: o M8 foi publicado no main em 89957690 (#195), com a mesma árvore de 0c85d555; a base passa a ser esse commit do main, sem mudar resumos nem trocas.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m9_20261112.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m9-edits-20261112.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
CONTAR = None
ACHADO = '12/11/2026: decisão 152 (cuidado em todas as lições), varredura do M9, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como do M1 ao M8).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e ao hífen da '
          'sigla).'),
    'C': 'Caso do mesmo tipo.',
}


def j(s):
    """As formas da proposta escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return s.replace('{N}', NBSP).replace('{J}', WJ)


# A folha das tabelas de apoio, antes da camada de aparência (como do M1 ao M8), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
INDICE = 'm9/index.html'
GUIA = 'm9/guia-da-tarefa-m9/index.html'
MAPA = 'm9/mapa-do-modulo-m9/index.html'
F01, F02, F03, F10 = (f'm9/licao-m9-{n}/index.html' for n in ('f01', 'f02', 'f03', 'f10'))
F13_JS = 'm9/recursos/f13.js'
SESSOES = 'assets/exame/sessoes.json'
COM_TABELA = {
    INDICE: ('O índice do módulo passa', [0]),
    GUIA: ('O guia da tarefa passa', [1]),
    MAPA: ('O mapa do módulo passa', [2]),
    F01: ('A lição passa', [3]),
    F02: ('A lição passa', [4]),
    F03: ('A lição passa', [5]),
    F10: ('A lição passa', [6]),
}
# Na tabela dos pesos, a coluna do peso só leva o número (as larguras do índice do M5).
PESOS = [' style="width:auto"', ' style="width:5.5rem"']
# Nas caixas «Recorda» da F02 e da F03, a primeira coluna fica com 30 % (como as caixas de termos do M6): com os 25 % da folha,
# «Caracterização» e «Intertextualidade» não cabiam numa linha no ecrã largo e partiam-se na última letra.
TERMOS = [' style="width:30%"', '']


def tabela(colunas, linhas, json_=True, larguras=None):
    """A tabela de apoio, igual às do M1 ao M8: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label com
    o nome da coluna, e os role. Com json_, as aspas vão escapadas como no JSON dos cartões."""
    larguras = larguras or [''] * len(colunas)
    cab = ''.join(f'<th scope="col" role="columnheader"{w}>{c}</th>' for c, w in zip(colunas, larguras))
    corpo = ''
    for linha in linhas:
        corpo += '<tr role="row"><th scope="row" role="rowheader">' + linha[0] + '</th>'
        for k, v in enumerate(linha[1:], 1):
            corpo += f'<td role="cell" data-label="{colunas[k]}">{v}</td>'
        corpo += '</tr>'
    html_ = (f'<table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row">{cab}</tr></thead>'
             f'<tbody role="rowgroup">{corpo}</tbody></table>')
    return html_.replace('"', '\\"') if json_ else html_


# Achados 0, 1 e 2 (A): os pesos da avaliação no índice, no guia e no mapa, como no M5, no M7 e no M8 (um parágrafo com o
# rótulo, a tabela Elemento/Peso e o resto da frase no p.avaliacao-tarefas, que fica como estava). Os pesos já vão com o espaço
# que não quebra: a conferência tirou-os dos achados B 23, 22 e 36.
PESOS_LINHAS = [['Tarefa da Unidade 1', '30{N}%'], ['Tarefa da Unidade 2', '30{N}%'], ['Provas rápidas', '10{N}%'],
                ['Prova escrita', '30{N}%']]
PESOS_FRASE = ': tarefa da Unidade 1, 30 %; tarefa da Unidade 2, 30 %; provas rápidas, 10 %; prova escrita, 30 %. '


def pesos(rotulo):
    """(antes, depois) do parágrafo dos pesos, com o rótulo da página («Pesos na avaliação» ou «Avaliação»)."""
    return ('<p class="avaliacao-tarefas">' + rotulo + PESOS_FRASE,
            f'<p>{rotulo}:</p>' + j(tabela(['Elemento', 'Peso'], PESOS_LINHAS, json_=False, larguras=PESOS)) + '<p class="avaliacao-tarefas">')


# Achados 3, 4, 5 e 6 (A): as noções das caixas «Recorda» da F01, da F02, da F03 e da F10 (dentro do JSON dos cartões), como na
# M5-F13 e nas M8-F04, F05 e F08.
F01_ANTES = ('<p><b>Tempo histórico</b>: a época em que a história se passa. <b>Organização temporal do relato</b>: a ordem em que o '
             'narrador apresenta os acontecimentos, com recuos e avanços. <b>Tempo da narração</b>: o momento de onde a voz conta, que '
             'pode distinguir-se da época narrada. <b>Prolepse</b>: o narrador adianta o que ainda vai acontecer. <b>Romance '
             'histórico</b>: ficção que se passa numa época real e usa figuras e factos dela.</p>')
F01_LINHAS = [['Tempo histórico', 'a época em que a história se passa'],
              ['Organização temporal do relato', 'a ordem em que o narrador apresenta os acontecimentos, com recuos e avanços'],
              ['Tempo da narração', 'o momento de onde a voz conta, que pode distinguir-se da época narrada'],
              ['Prolepse', 'o narrador adianta o que ainda vai acontecer'],
              ['Romance histórico', 'ficção que se passa numa época real e usa figuras e factos dela']]
F02_ANTES = ('<p><b>Símbolo</b>: uma coisa concreta que representa uma ideia (a passarola, o sonho). <b>Caracterização direta</b>: o '
             'narrador ou uma personagem diz como alguém é. <b>Caracterização indireta</b>: percebe-se pelo que a personagem faz e diz. '
             'Baltasar chama-se Sete-Sóis; Blimunda, Sete-Luas.</p>')
F02_LINHAS = [['Símbolo', 'uma coisa concreta que representa uma ideia (a passarola, o sonho)'],
              ['Caracterização direta', 'o narrador ou uma personagem diz como alguém é'],
              ['Caracterização indireta', 'percebe-se pelo que a personagem faz e diz']]
F02_DEPOIS = '<p>Baltasar chama-se Sete-Sóis; Blimunda, Sete-Luas.</p>'
F03_ANTES = ('<p><b>Discurso direto</b>: as palavras da personagem, tal como as disse. <b>Discurso indireto</b>: o narrador conta o que '
             'foi dito, com «que» e mudança de tempos e de pessoas. <b>Discurso indireto livre</b>: a voz da personagem dentro da voz do '
             'narrador, sem verbo a anunciar. <b>Ironia</b>: dizer uma coisa para dar a entender outra. <b>Intertextualidade</b>: um '
             'texto que chama outros textos.</p>')
F03_LINHAS = [['Discurso direto', 'as palavras da personagem, tal como as disse'],
              ['Discurso indireto', 'o narrador conta o que foi dito, com «que» e mudança de tempos e de pessoas'],
              ['Discurso indireto livre', 'a voz da personagem dentro da voz do narrador, sem verbo a anunciar'],
              ['Ironia', 'dizer uma coisa para dar a entender outra'],
              ['Intertextualidade', 'um texto que chama outros textos']]
F10_ANTES = ('<p><b>Tese</b>: a posição que se defende. <b>Argumento</b>: uma razão, com prova. <b>Contra-argumento</b>: a razão de '
             'quem discorda. <b>Refutação</b>: a resposta a essa razão. Conectores que ajudam: «porque», «no entanto», «ainda que», '
             '«portanto».</p>')
F10_LINHAS = [['Tese', 'a posição que se defende'], ['Argumento', 'uma razão, com prova'],
              ['Contra-argumento', 'a razão de quem discorda'], ['Refutação', 'a resposta a essa razão']]
F10_DEPOIS = '<p>Conectores que ajudam: «porque», «no entanto», «ainda que», «portanto».</p>'

# Achado 9 (C): «Três antes de mim», no guia, em lista numerada (o mesmo trecho, letra a letra, dos guias do M5, do M7 e do M8).
REGRA_ANTES = ('Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta ao teu par de trabalho. Só depois '
               'levantas o braço.</div>')
REGRA_DEPOIS = ('Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica;</li><li>pergunta ao teu par de '
                'trabalho.</li></ol>Só depois levantas o braço.</div>')

# Achado 11 (C): as quatro linhas de ação do «O essencial» da F01, em lista; a frase seguinte fica num parágrafo (texto igual).
LINHAS_ANTES = ('<p>«Memorial» é texto de memória e monumento que lembra. O romance histórico cruza ficção e história em quatro linhas '
                'de ação: a construção do convento, a passarola, o amor de Baltasar e Blimunda, a corte e a Inquisição. Assim dá lugar '
                'a quem a história oficial esquece.</p>')
LINHAS_DEPOIS = ('<p>«Memorial» é texto de memória e monumento que lembra. O romance histórico cruza ficção e história em quatro linhas '
                 'de ação:</p><ul><li>a construção do convento,</li><li>a passarola,</li><li>o amor de Baltasar e Blimunda,</li><li>a '
                 'corte e a Inquisição.</li></ul><p>Assim dá lugar a quem a história oficial esquece.</p>')

# Achado 15 (C): as quatro estações da oficina da F13 (os cartões estão em m9/recursos/f13.js), em lista numerada; a frase
# seguinte fica num parágrafo (texto igual).
ESTACOES_ANTES = ('<p>Oficina longa, com o livro aberto, em quatro estações: hipótese inicial; confronto de episódios; contraexemplo e '
                  'revisão; síntese fundamentada. Entre estações, confronta a tua leitura com uma passagem do livro e anota a página da '
                  'edição.</p>')
ESTACOES_DEPOIS = ('<p>Oficina longa, com o livro aberto, em quatro estações:</p><ol><li>hipótese inicial;</li><li>confronto de '
                   'episódios;</li><li>contraexemplo e revisão;</li><li>síntese fundamentada.</li></ol><p>Entre estações, confronta a '
                   'tua leitura com uma passagem do livro e anota a página da edição.</p>')

# Achado 10 (C): no portefólio, os oito nomes de ficheiro que estavam em texto simples passam a <code>, como os outros seis; os
# nomes podem mudar de linha a seguir a cada «_» (<wbr>), e só aí. Dos seis que já estavam em <code>, só os dois compridos
# levam <wbr> (a proposta final, como nos portefólios do M5 e do M7).
PORTEFOLIO = 'm9/portefolio-do-modulo-m9/index.html'
PORT_NOMES = ([f'M9_U{u}_{n}' for u in (1, 2) for n in ('registo_&lt;dia-mês&gt;', 'retoma', 'o-que-aprendi')]
              + ['M9_U1_Tarefa', 'M9_U2_Tarefa'])
PORT_JA_CODE = ['M9_cartao-do-percurso', 'M9_Prova-escrita']
PORT_CSS_ANTES = 'code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
PORT_CSS_DEPOIS = PORT_CSS_ANTES + 'td code{white-space:nowrap}\n'


def com_wbr(nome_):
    """O nome com <wbr> a seguir a cada «_» (onde pode mudar de linha)."""
    return nome_.replace('_', '_<wbr>')


def achados_ac():
    """Os 11 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte)."""
    recorda = ('As noções no cabeçalho de linha, sem negrito; caem os dois pontos e o ponto final de cada definição, como na '
               'M5-F13; as palavras ficam todas.')
    out = []
    for i, rel, rotulo, onde in ((0, INDICE, 'Pesos na avaliação', '«Como se cumpre uma unidade»: os pesos na avaliação'),
                                 (1, GUIA, 'Avaliação', '«Tarefas das unidades»: os pesos na avaliação'),
                                 (2, MAPA, 'Avaliação', '«As tarefas das unidades»: os pesos na avaliação')):
        antes, depois = pesos(rotulo)
        out.append(dict(i=i, cat='A', ficheiro=rel, cartao=onde,
                        nota=('Como no M5, no M7 e no M8: o rótulo num parágrafo, a tabela Elemento/Peso (a coluna do peso com 5,5 rem) '
                              'e o resto da frase no p.avaliacao-tarefas, como estava. Os pesos já levam o espaço que não quebra.'),
                        antigo=antes, novo=depois))
    out += [
        dict(i=3, cat='A', ficheiro=F01, cartao='cartão 9, Para entender («Recorda»)', nota=recorda,
             antigo=F01_ANTES, novo=tabela(['Noção', 'O que é'], F01_LINHAS)),
        dict(i=11, cat='C', ficheiro=F01, cartao='cartão 3, O essencial («O título e as quatro linhas de ação»)',
             nota=('As quatro linhas de ação em lista, cada item com a vírgula ou o ponto final que tinha; a frase seguinte fica num '
                   'parágrafo; o texto fica igual.'),
             antigo=LINHAS_ANTES, novo=LINHAS_DEPOIS),
        dict(i=4, cat='A', ficheiro=F02, cartao='cartão 7, Para entender («Recorda»)',
             nota=(recorda + ' A frase dos dois nomes, que já não é definição, fica num parágrafo a seguir. A primeira coluna fica com '
                   '30 %, como as caixas de termos do M6, para «Caracterização» caber numa linha no ecrã largo.'),
             antigo=F02_ANTES, novo=tabela(['Noção', 'O que é'], F02_LINHAS, larguras=TERMOS) + F02_DEPOIS),
        dict(i=5, cat='A', ficheiro=F03, cartao='cartão 5, Para entender («Recorda»)',
             nota=(recorda + ' A primeira coluna fica com 30 %, como as caixas de termos do M6, para «Intertextualidade» caber numa '
                   'linha no ecrã largo.'),
             antigo=F03_ANTES, novo=tabela(['Noção', 'O que é'], F03_LINHAS, larguras=TERMOS)),
        dict(i=6, cat='A', ficheiro=F10, cartao='cartão 5, Para entender («Recorda»)',
             nota=('Os quatro termos no cabeçalho de linha, sem negrito; caem os dois pontos e o ponto final de cada definição, como '
                   'na M5-F13; as palavras ficam todas. A frase dos conectores, que já não é definição, fica num parágrafo a seguir.'),
             antigo=F10_ANTES, novo=tabela(['Termo', 'O que é'], F10_LINHAS) + F10_DEPOIS),
        dict(i=9, cat='C', ficheiro=GUIA, cartao='«Três antes de mim» (div.regra)',
             nota='Os três passos numerados à mão passam a lista numerada, como nos guias do M5, do M7 e do M8; o texto fica igual.',
             antigo=REGRA_ANTES, novo=REGRA_DEPOIS),
        dict(i=15, cat='C', ficheiro=F13_JS, cartao='cartão 2, Lê e confronta («Caderno de leitura: quatro estações»)',
             nota=('As quatro estações, que têm ordem (os cartões seguintes chamam-se «Estação 1» a «Estação 4»), em lista numerada, '
                   'cada item com o «;» ou o ponto final que tinha; a frase seguinte fica num parágrafo; o texto fica igual.'),
             antigo=ESTACOES_ANTES, novo=ESTACOES_DEPOIS),
    ]
    for nome_ in PORT_NOMES:
        out.append(dict(i=10, cat='C', ficheiro=PORTEFOLIO, cartao=f'«A lista de verificação»: o nome {html.unescape(nome_)} em <code>',
                        nota=('O nome do ficheiro, que se copia letra a letra, passa a <code>, como os outros seis da lista; pode mudar '
                              'de linha a seguir a cada «_» (<wbr>), como nos portefólios do M5, do M7 e do M8.'),
                        antigo=f'<td>{nome_}</td>', novo=f'<td><code>{com_wbr(nome_)}</code></td>'))
    for nome_ in PORT_JA_CODE:
        out.append(dict(i=10, cat='C', ficheiro=PORTEFOLIO, cartao=f'«A lista de verificação»: o nome {nome_} pode mudar de linha depois de «M9_»',
                        nota='O nome já estava em <code>; por ser comprido, leva <wbr> depois de «M9_», como nos portefólios do M5 e do M7.',
                        antigo=f'<td><code>{nome_}</code></td>', novo=f'<td><code>{com_wbr(nome_)}</code></td>'))
    out.append(dict(i=10, cat='C', ficheiro=PORTEFOLIO, cartao='a folha da página: os nomes só mudam de linha onde podem',
                    nota='Como nos portefólios do M5, do M7 e do M8: «td code{white-space:nowrap}», a seguir à regra do <code>.',
                    antigo=PORT_CSS_ANTES, novo=PORT_CSS_DEPOIS))
    return out


def ac_grelhas():
    """Sem achados A ou C nas grelhas do M9 (a função fica, como do M6 ao M8, para os testes e para a ordem das trocas)."""
    return []


META = ('durante 90 minutos, com entrega', 'durante 90{N}minutos, com entrega',
        'a meta descrição muda com «nao_partir» (o gerador prende os três números do molde, como do M1 ao M8); a proposta '
        'não a lista porque não se vê', 1)
ACHADOS_B = [
    dict(i=19, ficheiro='m9/biblioteca-fogo/index.html',
         pares=[('30 segundos', '30{N}segundos', 1)]),
    dict(i=21, ficheiro='m9/gramatica-saramago/index.html',
         pares=[('D. João V', 'D.{N}João{N}V', 2)]),
    dict(i=22, ficheiro='m9/guia-da-tarefa-m9/index.html',
         pares=[('3.º ano', '3.º{N}ano', 2), ('90 minutos', '90{N}minutos', 1), ('30 %,', '30{N}%,', 2),
                ('10 minutos', '10{N}minutos', 1), ('5 minutos', '5{N}minutos', 1),
                ('capítulos I e V', 'capítulos{N}I e{N}V', 1), ('10 min<', '10{N}min<', 1), (' 5 min<', ' 5{N}min<', 1),
                ('60 min', '60{N}min', 1), ('15 min', '15{N}min', 1), ('7 minutos', '7{N}minutos', 1)],
         de={'30 %,': '30 %', '10 min<': '10 min', ' 5 min<': '5 min'}),
    dict(i=23, ficheiro='m9/index.html',
         pares=[('3.º ano', '3.º{N}ano', 2), ('90 minutos', '90{N}minutos', 3), ('90 min<', '90{N}min<', 4),
                ('capítulo XXI', 'capítulo{N}XXI', 4), ('22 min', '22{N}min', 2), ('10 min', '10{N}min', 2),
                ('30 %.<', '30{N}%.<', 2), ('século XVIII (fac-símile, BNP).', 'século{N}XVIII (fac-símile, BNP).', 1),
                ('século XVI"', 'século{N}XVI"', 1), ('século XVIII"', 'século{N}XVIII"', 3),
                ('século XX', 'século{N}XX', 9), ('século XVII"', 'século{N}XVII"', 1), ('D. João V', 'D.{N}João{N}V', 15),
                ('século XVIII;', 'século{N}XVIII;', 1), ('século XVI ', 'século{N}XVI ', 1),
                ('século XVIII.', 'século{N}XVIII.', 1), ('século XVIII (l', 'século{N}XVIII (l', 1),
                ('22 de outubro de 1982', '22{N}de outubro de{N}1982', 1),
                ('22 de outubro de 1730', '22{N}de outubro de{N}1730', 1),
                ('22 de outubro de 1523', '22{N}de outubro de{N}1523', 1), ('capítulo I', 'capítulo{N}I', 1),
                ('século XVI,', 'século{N}XVI,', 3), ('século XVIII c', 'século{N}XVIII c', 2),
                ('Século XVI', 'Século{N}XVI', 1), ('cap. XXI', 'cap.{N}XXI', 1)],
         de={'90 min<': '90 min', '30 %.<': '30 %', 'século XVIII (fac-símile, BNP).': 'século XVIII',
             'século XVI"': 'século XVI', 'século XVIII"': 'século XVIII', 'século XVII"': 'século XVII',
             'século XVIII;': 'século XVIII', 'século XVI ': 'século XVI', 'século XVIII.': 'século XVIII',
             'século XVIII (l': 'século XVIII', 'século XVI,': 'século XVI', 'século XVIII c': 'século XVIII'}),
    dict(i=24, ficheiro='m9/licao-m9-f01/index.html',
         pares=[('12.º ano', '12.º{N}ano', 1), ('D. João V p', 'D.{N}João{N}V p', 1), ('2 min)<', '2{N}min)<', 1),
                ('séc. XVIII', 'séc.{N}XVIII', 2), ('>D. João V', '>D.{N}João{N}V', 1),
                ('capítulo XXI, o', 'capítulo{N}XXI, o', 2), ('22 de outubro,', '22{N}de outubro,', 1),
                ('século XVIII', 'século{N}XVIII', 7), (': D. João V', ': D.{N}João{N}V', 3),
                ('Século XVIII', 'Século{N}XVIII', 1), ('"D. João V', '"D.{N}João{N}V', 1),
                ('D. João V s', 'D.{N}João{N}V s', 1), ('capítulo XXI)', 'capítulo{N}XXI)', 3),
                ('capítulo XXI;', 'capítulo{N}XXI;', 1), ('p>No capítulo XXI', 'p>No capítulo{N}XXI', 1),
                ('D. João V fecha-se numa sala do torreão, ', 'D.{N}João{N}V fecha-se numa sala do torreão, ', 1),
                (' 22 de outubro de 1730,', ' 22{N}de outubro de{N}1730,', 2), ('pp. 291 a 293', 'pp.{N}291 a{N}293', 1),
                (' D. João V e', ' D.{N}João{N}V e', 5), ('século XVI"', 'século{N}XVI"', 1),
                ('século XX', 'século{N}XX', 4), ('século XVII"', 'século{N}XVII"', 1), ('século XVI ', 'século{N}XVI ', 1),
                ('D. João V.', 'D.{N}João{N}V.', 2), ('D. João V:', 'D.{N}João{N}V:', 1),
                ('capítulo XXI.', 'capítulo{N}XXI.', 2), ('22 de outubro de 1730*', '22{N}de outubro de{N}1730*', 2),
                ('D. João V"', 'D.{N}João{N}V"', 1), ('capítulo I', 'capítulo{N}I', 3),
                ('D. João V a', 'D.{N}João{N}V a', 1), ('D. João V, e', 'D.{N}João{N}V, e', 1)],
         de={'D. João V p': 'D. João V', '2 min)<': '2 min', '>D. João V': 'D. João V', 'capítulo XXI, o': 'capítulo XXI',
             '22 de outubro,': '22 de', ': D. João V': 'D. João V', '"D. João V': 'D. João V', 'D. João V s': 'D. João V',
             'capítulo XXI)': 'capítulo XXI', 'capítulo XXI;': 'capítulo XXI', 'p>No capítulo XXI': 'capítulo XXI',
             'D. João V fecha-se numa sala do torreão, ': 'D. João V', ' 22 de outubro de 1730,': '22 de outubro de 1730',
             ' D. João V e': 'D. João V', 'século XVI"': 'século XVI', 'século XVII"': 'século XVII',
             'século XVI ': 'século XVI', 'D. João V.': 'D. João V', 'D. João V:': 'D. João V',
             'capítulo XXI.': 'capítulo XXI', '22 de outubro de 1730*': '22 de outubro de 1730', 'D. João V"': 'D. João V',
             'D. João V a': 'D. João V', 'D. João V, e': 'D. João V'}),
    dict(i=25, ficheiro='m9/licao-m9-f02/index.html',
         pares=[('12.º ano', '12.º{N}ano', 1), ('capítulo XVI', 'capítulo{N}XVI', 3), ('2 min)<', '2{N}min)<', 1),
                ('pp. 196 e 197', 'pp.{N}196 e{N}197', 1), ('capítulo XXV', 'capítulo{N}XXV', 3),
                ('D. João V', 'D.{N}João{N}V', 2)],
         de={'2 min)<': '2 min'}),
    dict(i=26, ficheiro='m9/licao-m9-f03/index.html',
         pares=[('>D. João V', '>D.{N}João{N}V', 1), ('4 min)<', '4{N}min)<', 2), ('capítulo I', 'capítulo{N}I', 2),
                ('capítulo XXI', 'capítulo{N}XXI', 4)],
         de={'>D. João V': 'D. João V', '4 min)<': '4 min'}),
    dict(i=27, ficheiro='m9/licao-m9-f04/index.html',
         pares=[('século XX', 'século{N}XX', 10), ('século XVI ', 'século{N}XVI ', 2), ('2 min)<', '2{N}min)<', 2),
                ('século XVIII', 'século{N}XVIII', 4), ('século XVI;', 'século{N}XVI;', 1),
                ('século XVI,', 'século{N}XVI,', 2), ('Século XVI', 'Século{N}XVI', 1)],
         de={'século XVI ': 'século XVI', '2 min)<': '2 min', 'século XVI;': 'século XVI', 'século XVI,': 'século XVI'}),
    dict(i=28, ficheiro='m9/licao-m9-f05/index.html',
         pares=[('12.º ano', '12.º{N}ano', 1), ('4 min)<', '4{N}min)<', 1), ('30 segundos', '30{N}segundos', 1),
                ('3 min,', '3{N}min,', 1), ('3 minutos', '3{N}minutos', 1), ('capítulo XIX', 'capítulo{N}XIX', 2),
                ('capítulo XXV', 'capítulo{N}XXV', 2)],
         de={'4 min)<': '4 min', '3 min,': '3 min'}),
    dict(i=29, ficheiro='m9/licao-m9-f07/index.html',
         pares=[('D. João V', 'D.{N}João{N}V', 8), ('capítulo XXI', 'capítulo{N}XXI', 2), ('canto I', 'canto{N}I', 4),
                ('capítulo XIX', 'capítulo{N}XIX', 2)]),
    dict(i=30, ficheiro='m9/licao-m9-f10/index.html',
         pares=[('3 min)<', '3{N}min)<', 1), ('8 de outubro de 1998', '8{N}de outubro de{N}1998', 1),
                ('cap. XXI', 'cap.{N}XXI', 1)],
         de={'3 min)<': '3 min'}),
    dict(i=31, ficheiro='m9/licao-m9-f14/index.html',
         pares=[('D. João V', 'D.{N}João{N}V', 3), ('capítulo I', 'capítulo{N}I', 1), ('p. 22', 'p.{N}22', 1),
                ('n.º 2', 'n.º{N}2', 1), ('p. 33', 'p.{N}33', 1)]),
    dict(i=32, ficheiro='m9/licao-m9-f15/index.html',
         pares=[('capítulo V', 'capítulo{N}V', 3), ('página 78', 'página{N}78', 1), ('p. 49', 'p.{N}49', 1)]),
    dict(i=33, ficheiro='m9/licao-m9-f16/index.html',
         pares=[('página 1', 'página{N}1', 1)]),
    dict(i=34, ficheiro='m9/m9-de-quem-e-o-convento/index.html',
         pares=[('22 min', '22{N}min', 1), ('capítulo XXI', 'capítulo{N}XXI', 1), ('D. João V f', 'D.{N}João{N}V f', 1),
                ('22 de outubro de 1730', '22{N}de outubro de{N}1730', 1), ('capítulo XIX', 'capítulo{N}XIX', 1),
                ('D. João V.', 'D.{N}João{N}V.', 1), ('D. João V m', 'D.{N}João{N}V m', 1), ('canto III', 'canto{N}III', 5),
                ('canto VIII', 'canto{N}VIII', 3), ('estância 20', 'estância{N}20', 3), ('estância 78', 'estância{N}78', 2),
                ('século XX', 'século{N}XX', 1), ('capítulos I, XIX e XXI', 'capítulos{N}I, XIX e{N}XXI', 1)],
         de={'D. João V f': 'D. João V', 'D. João V.': 'D. João V', 'D. João V m': 'D. João V'}),
    dict(i=35, ficheiro='m9/m9-ver-e-nao-ver/index.html',
         pares=[('22 min', '22{N}min', 1), ('capítulo XVI', 'capítulo{N}XVI', 1), ('D. João V', 'D.{N}João{N}V', 1),
                ('capítulo XXV', 'capítulo{N}XXV', 2), ('capítulo XXI', 'capítulo{N}XXI', 1),
                ('22 de outubro de 1730', '22{N}de outubro de{N}1730', 1), ('século XVIII', 'século{N}XVIII', 1),
                ('século XX', 'século{N}XX', 4), ('capítulo XIX', 'capítulo{N}XIX', 2), ('cap. 1', 'cap.{N}1', 1),
                ('capítulos XVI, XIX, XXI e XXV', 'capítulos{N}XVI, XIX, XXI e{N}XXV', 1), ('capítulo 1', 'capítulo{N}1', 1)]),
    dict(i=36, ficheiro='m9/mapa-do-modulo-m9/index.html',
         pares=[('3.º ano', '3.º{N}ano', 2), ('90 minutos', '90{N}minutos', 2), ('>D. João V', '>D.{N}João{N}V', 4),
                ('22 de outubro de 1730', '22{N}de outubro de{N}1730', 2), ('século XVIII d', 'século{N}XVIII d', 1),
                ('D. João V,', 'D.{N}João{N}V,', 1), ('século XX', 'século{N}XX', 1), ('30 %,', '30{N}%,', 2),
                ('M9-F01', 'M9-{J}F01', 4), ('século XVIII (fac-símile, BNP).', 'século{N}XVIII (fac-símile, BNP).', 1),
                ('século XVIII.', 'século{N}XVIII.', 1), ('M9-F04', 'M9-{J}F04', 4), ('M9-F02', 'M9-{J}F02', 1),
                ('D. João V e', 'D.{N}João{N}V e', 1)],
         de={'>D. João V': 'D. João V', 'século XVIII d': 'século XVIII', 'D. João V,': 'D. João V', '30 %,': '30 %',
             'século XVIII (fac-símile, BNP).': 'século XVIII', 'século XVIII.': 'século XVIII', 'D. João V e': 'D. João V'}),
    dict(i=37, ficheiro='m9/memorial-promessa/index.html',
         pares=[('D. João V q', 'D.{N}João{N}V q', 1)],
         de={'D. João V q': 'D. João V'}),
    dict(i=46, ficheiro='m9/passarola-ramos/index.html',
         pares=[('ato III', 'ato{N}III', 1), ('século XVI', 'século{N}XVI', 1)]),
    dict(i=47, ficheiro='m9/portefolio-do-modulo-m9/index.html',
         pares=[('3.º ano', '3.º{N}ano', 2), ('90 minutos', '90{N}minutos', 1), ('40 %', '40{N}%', 1)]),
    dict(i=52, ficheiro='m9/recursos/f11.js',
         pares=[('capítulo I', 'capítulo{N}I', 5), ('capítulo XXV', 'capítulo{N}XXV', 2),
                ('capítulo XVI', 'capítulo{N}XVI', 1)]),
    dict(i=53, ficheiro='m9/recursos/f12.js',
         pares=[('século XVIII', 'século{N}XVIII', 1), ('4 min)<', '4{N}min)<', 1)],
         de={'4 min)<': '4 min'}),
    dict(i=54, ficheiro='m9/recursos/f13.js',
         pares=[('capítulo XVI', 'capítulo{N}XVI', 1), ('capítulo XIX', 'capítulo{N}XIX', 1),
                ('capítulo XXV', 'capítulo{N}XXV', 1), ('M9-F03', 'M9-{J}F03', 1)]),
    dict(i=55, ficheiro='m9/reis-regresso/index.html',
         pares=[('13 de janeiro de 1935', '13{N}de janeiro de{N}1935', 1)]),
    dict(i=57, ficheiro='m9/visita-fundacao-jose-saramago/index.html',
         pares=[('3.º ano', '3.º{N}ano', 2)]),
    dict(i=58, ficheiro='tarefas/m9-u1/index.html', literais=[META],
         pares=[('10 min', '10{N}min', 1), ('60 minutos', '60{N}minutos', 1), ('90 min', '90{N}min', 1),
                ('10 minutos', '10{N}minutos', 1), ('capítulo I', 'capítulo{N}I', 2), ('capítulo V', 'capítulo{N}V', 2)]),
    dict(i=59, ficheiro='tarefas/m9-u2/index.html', literais=[META],
         pares=[('10 min', '10{N}min', 1), ('60 minutos', '60{N}minutos', 1), ('90 min', '90{N}min', 1),
                ('10 minutos', '10{N}minutos', 1)]),
]

# Os painéis de projeção seguem as lições: só mudam os enunciados dos cartões (a lista CARTOES e o seletor). O material do
# relâmpago (MATERIAL), as pistas do «Quem sou eu?» (ATL) e o cabeçalho não mudam, como do M1 ao M8.
PAINEIS = {f'm9/painel-m9-{f}/index.html': i for f, i in (('f01', 38), ('f02', 39), ('f03', 40), ('f05', 42),
                                                          ('f07', 43))}

# As notas do docente da lição gerada F14 (m9/painel-m9-f14, de scripts/gerar_licoes_20261101.py, render_notes) repetem um
# retorno da lição: o par do achado que lá está muda também, e as notas saem iguais do gerador.
NOTAS = [
    dict(i=45, ficheiro='m9/painel-m9-f14/index.html', pares=[('D. João V', 'D.{N}João{N}V', 1)]),
    # A resposta certa e o retorno do cartão 11 da F01 estão copiados (na pergunta e na verificação «Depois da revisão») nas
    # sessões do Exame, que tests/test_exame_alignment.py compara com a lição, letra a letra: mudam como na lição (como no M6).
    dict(i=24, ficheiro=SESSOES,
         nota_copia=('Na cópia da resposta certa e do retorno do cartão 11 da F01 nas sessões do Exame (assets/exame/sessoes.json, '
                     'sessão s19), que tests/test_exame_alignment.py compara com a lição.'),
         pares=[('No início do século XVIII"', 'No início do século{N}XVIII"', 2),
                ('Reinado de D. João V e tempo', 'Reinado de D.{N}João{N}V e tempo', 2),
                ('início do século XVIII; o século XX é', 'início do século{N}XVIII; o século{N}XX é', 2)],
         de={'No início do século XVIII"': 'século XVIII', 'Reinado de D. João V e tempo': 'D. João V'}),
]

# A casca das lições fica para o molde, como do M1 ao M8: nenhuma troca. As lições com achado B.
CASCA_NO_MOLDE = sorted(x['ficheiro'] for x in ACHADOS_B if x['ficheiro'].startswith('m9/licao-'))

GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
CHAVES_TAREFA = (' "nao_partir": true,\n',
                 'Os números do molde da tarefa («90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) levam o espaço que não '
                 'quebra pelo gerador (scripts/tarefas_escolha.py), como do M1 ao M8.')
MOLDE = ('10 min', '90 min')
DADOS = [
    dict(ficheiro=f'docs/pedagogia/tarefas-escolha/m9-u{u}.json', achados=(i,), chaves=(f'\n "unidade": {u},\n',) + CHAVES_TAREFA,
         pares=[p for p in next(x for x in ACHADOS_B if x['i'] == i)['pares'] if p[0] not in MOLDE])
    for u, i in ((1, 58), (2, 59))
]


def bloco(rel, inicio, fim, inclui_fim=False):
    """O trecho da base que começa em «inicio» (único na página) e acaba logo antes de «fim» (ou com ele, com inclui_fim)."""
    texto = base(rel)
    if texto.count(inicio) != 1:
        raise SystemExit(f'{rel}: «{inicio[:60]}» não aparece uma vez')
    a = texto.index(inicio)
    b = texto.index(fim, a) + (len(fim) if inclui_fim else 0)
    return texto[a:b]


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def base(rel):
    """O texto do ficheiro sem esta camada (desfeita pelo manifesto, da última troca para a primeira)."""
    texto = ler(rel)
    if MANIFESTO.is_file():
        for edit in reversed(json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a camada já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    return texto


def edicoes(antigo, novo):
    """As edições atómicas que levam o trecho antigo ao novo: (posição, 'nbsp') troca o espaço nessa posição por U+00A0;
    (posição, 'wj') põe U+2060 antes do carácter nessa posição; (posição, 'traco') troca o hífen nessa posição por traço de
    intervalo. Mais nada é permitido num par B."""
    i = k = 0
    out = []
    while i < len(antigo) or k < len(novo):
        if k < len(novo) and novo[k] == WJ and (i >= len(antigo) or antigo[i] != WJ):
            out.append((i, 'wj'))
            k += 1
        elif i < len(antigo) and k < len(novo) and antigo[i] == novo[k]:
            i += 1
            k += 1
        elif i < len(antigo) and k < len(novo) and antigo[i] == ' ' and novo[k] == NBSP:
            out.append((i, 'nbsp'))
            i += 1
            k += 1
        elif i < len(antigo) and k < len(novo) and antigo[i] == '-' and novo[k] == TRACO:
            out.append((i, 'traco'))
            i += 1
            k += 1
        else:
            raise SystemExit(f'par B com uma mudança que não é de espaço nem de traço: {antigo!r} > {novo!r}')
    return out


def aplicar_edicoes(texto, eds):
    # Da última posição para a primeira; na mesma posição, a junção (que se insere antes) vem depois da troca do carácter.
    for pos, tipo in sorted(eds, key=lambda e: (e[0], e[1] != 'wj'), reverse=True):
        if tipo == 'nbsp':
            assert texto[pos] == ' ', (pos, texto[pos - 20:pos + 20])
            texto = texto[:pos] + NBSP + texto[pos + 1:]
        elif tipo == 'traco':
            assert texto[pos] == '-', (pos, texto[pos - 20:pos + 20])
            texto = texto[:pos] + TRACO + texto[pos + 1:]
        else:
            texto = texto[:pos] + WJ + texto[pos:]
    return texto


def janela_novo(pre, s, e, eds):
    """O texto da janela [s, e) de pre com as edições dela aplicadas."""
    return aplicar_edicoes(pre[s:e], [(p - s, t) for p, t in eds])


def _atributo(texto, s):
    """O nome do atributo HTML em cujo valor está a posição s, ou None (também com as aspas escapadas do JSON)."""
    lt, gt = texto.rfind('<', 0, s), texto.rfind('>', 0, s)
    if lt <= gt:
        return None
    m = re.findall(r'([\w:-]+)=\\?"[^"]*$', texto[lt:s])
    return m[-1] if m else None


# Os campos dos exercícios que não levam U+00A0 nem U+2060: a «frase» de um sublinhar, as «palavras» de um cartão frase e os
# «passos» de um ordenar (o motor parte o sublinhar nos espaços; os outros dois mostram as peças como estão escritas).
CAMPOS_DE_EXERCICIO = {'frase': 'sublinhar', 'palavras': 'frase', 'passos': 'ordenar'}


def _fim_do_valor(texto, i):
    """A posição logo a seguir ao valor JSON (texto ou lista de textos) que começa em i (salta os espaços)."""
    while texto[i] in ' \n\t':
        i += 1
    if texto[i] == '"':
        m = re.compile(r'(?<!\\)(?:\\\\)*"').search(texto, i + 1)
        return m.end()
    if texto[i] == '[':
        k, fundo, dentro = i, 0, False
        while k < len(texto):
            c = texto[k]
            if dentro:
                if c == '\\':
                    k += 2
                    continue
                if c == '"':
                    dentro = False
            elif c == '"':
                dentro = True
            elif c == '[':
                fundo += 1
            elif c == ']':
                fundo -= 1
                if fundo == 0:
                    return k + 1
            k += 1
    return i


def _campo_de_exercicio(texto, s):
    """O campo de exercício (sublinhar.frase, frase.palavras, ordenar.passos) em cujo valor está a posição s, ou None."""
    for campo, tipo in CAMPOS_DE_EXERCICIO.items():
        k = texto.rfind(f'"{campo}":', 0, s)
        if k < 0 or _fim_do_valor(texto, texto.index(':', k) + 1) <= s:
            continue
        kt = texto.rfind('"t":', 0, k)
        t = re.match(r'"t":\s*"(\w+)"', texto[kt:kt + 40]) if kt >= 0 else None
        if t and t.group(1) == tipo:
            return f'{campo} de um cartão {tipo}'
    return None


def _nota_interna(texto, s):
    """A posição s está no valor de uma chave JSON que começa por «_» (as notas internas dos dados, que não se publicam)."""
    i = s
    while i > 0:
        i -= 1
        if texto[i] == '"' and texto[i - 1] != '\\':
            break
    return re.search(r'"_\w+"\s*:\s*$', texto[max(0, i - 40):i]) is not None


def _em_desenho(texto, s):
    """A posição s está dentro de um desenho (<svg>…</svg>, também no JSON dos cartões, onde «</» pode vir como «<\\/»)."""
    a = texto.rfind('<svg', 0, s)
    if a < 0:
        return False
    fim = min((k for k in (texto.find('</svg>', a), texto.find('<\\/svg>', a)) if k >= 0), default=-1)
    return fim > s


def _em_comentario(texto, s):
    """A posição s está num comentário de HTML ou de CSS (dentro de <style>)."""
    if texto.rfind('<!--', 0, s) > texto.rfind('-->', 0, s):
        return True
    return texto.rfind('/*', 0, s) > texto.rfind('*/', 0, s) and texto.rfind('<style', 0, s) > texto.rfind('</style>', 0, s)


def fora_de_alcance(texto, s):
    """Porque é que a ocorrência em s não muda (ou None): os atributos que não se veem ou que não podem levar U+00A0 (alt,
    aria-label, href, title, src, o content da meta descrição e o data-titulo do vídeo, que vira title), o <title>, a «frase» de um
    sublinhar, as «palavras» de um cartão frase, os «passos» de um ordenar, o texto dos desenhos (SVG, que não muda de linha), os comentários e as notas internas dos dados («_nota»)."""
    if _nota_interna(texto, s):
        return 'nota interna dos dados'
    attr = _atributo(texto, s)
    if attr in ('alt', 'aria-label', 'href', 'title', 'src', 'content', 'data-titulo'):
        return 'atributo ' + attr
    if texto.rfind('<title>', 0, s) > texto.rfind('</title>', 0, s):
        return '<title>'
    campo = _campo_de_exercicio(texto, s)
    if campo:
        return campo
    if _em_desenho(texto, s):
        return 'texto de um desenho (SVG)'
    if _em_comentario(texto, s):
        return 'comentário'
    return None


# Os pares da proposta que trazem contexto à direita e acabam a meio de uma palavra («D. João V p», de «D. João V prometeu»): à
# direita não se exige a palavra inteira (a referência que muda, que «de» diz, fica inteira dentro do par).
A_MEIO = {p[0] for x in ACHADOS_B for p in x['pares']
          if p[0] in x.get('de', {}) and not p[0].endswith(x['de'][p[0]]) and p[0][-1].isalnum()}


def _palavra_inteira(texto, s, e, seq):
    antes, depois = texto[s - 1:s], texto[e:e + 1]
    return not ((seq[0].isalnum() and antes.isalnum()) or (seq[-1].isalnum() and depois.isalnum() and seq not in A_MEIO))


def _letra(c):
    return c.isalnum() or c in 'ºª%'


def nucleos(pre, eds):
    """Divide as edições de uma ocorrência em núcleos (as que estão na mesma referência: entre duas edições só há letras,
    números, espaços, pontos e traços) e devolve, para cada um, [início, fim, edições]: a referência inteira à volta das edições
    (à esquerda também com o ponto de «cap.», «n.º», «D.»; à direita, o ponto só quando vem outra letra, como em «sr.ª»)."""
    eds = sorted(eds)
    grupos, atual = [], [eds[0]]
    for e in eds[1:]:
        entre = pre[atual[-1][0]:e[0]]
        if re.fullmatch(r'[\w\s.ºª–\-' + NBSP + WJ + ']*', entre):
            atual.append(e)
        else:
            grupos.append(atual)
            atual = [e]
    grupos.append(atual)
    out = []
    for g in grupos:
        lo = g[0][0] - (1 if g[0][1] == 'wj' else 0)
        hi = g[-1][0] + 1
        while lo > 0 and (_letra(pre[lo - 1]) or pre[lo - 1] == '.'):
            lo -= 1
        while hi < len(pre) and (_letra(pre[hi]) or (pre[hi] == '.' and hi + 1 < len(pre) and _letra(pre[hi + 1]))):
            hi += 1
        out.append([lo, hi, set(g)])
    return out


def cadeias(texto, pares):
    """Onde está cada par no texto, com a palavra inteira: [(início, fim)]. Serve para ver se uma ocorrência de um par mais curto
    está dentro de uma cadeia maior de outro par («8 de março» dentro de «8 de março de 1914», «80 a 120» dentro de «80 a 120
    palavras»): essa ocorrência conta para o par maior, não para o mais curto."""
    out = []
    for antigo in dict.fromkeys(p[0] for p in pares):
        for m in re.finditer(re.escape(antigo), texto):
            if _palavra_inteira(texto, m.start(), m.end(), antigo):
                out.append((m.start(), m.end()))
    return out


def _em_cadeia_maior(s, e, onde):
    return any(a <= s and e <= b and b - a > e - s for a, b in onde)


def ocorrencias(texto, antigo, novo, todos):
    """As posições onde o par conta: com a palavra inteira, fora das cadeias maiores dos outros pares da página (todos) e com
    todas as edições em alcance."""
    onde = cadeias(texto, todos)
    eds_rel = edicoes(antigo, j(novo))
    return [m.start() for m in re.finditer(re.escape(antigo), texto)
            if _palavra_inteira(texto, m.start(), m.end(), antigo) and not _em_cadeia_maior(m.start(), m.end(), onde)
            and all(fora_de_alcance(texto, m.start() + p) is None for p, _ in eds_rel)]


def janelas_pares(rel, pre, pares, regioes, limite=None, todos=None):
    """As janelas dos pares (antigo, novo, n) em pre (a base com as trocas A, C e literais já feitas): [início, fim, {edições},
    índice do par]. Cada par conta-se com a palavra inteira e fora das cadeias maiores dos outros pares da página (todos); as
    ocorrências fora de alcance não contam. Cada par tem de aparecer exatamente n vezes. Devolve também as que ficaram de fora,
    com a razão."""
    janelas, fora, vistas = [], [], set()
    onde = cadeias(pre, todos or pares)
    for k, (antigo, novo, esperado) in enumerate(pares):
        eds_rel = edicoes(antigo, j(novo))
        achadas = []
        for m in re.finditer(re.escape(antigo), pre):
            s, e = m.start(), m.end()
            if limite and not (limite[0] <= s and e <= limite[1]):
                continue
            if not _palavra_inteira(pre, s, e, antigo) or _em_cadeia_maior(s, e, onde):
                continue
            absolutas = {(s + p, t) for p, t in eds_rel}
            razoes = {fora_de_alcance(pre, p) for p, _ in absolutas} - {None}
            if razoes:
                fora.append((antigo, s, sorted(razoes)[0]))
                continue
            if any(a <= p < b for p, _ in absolutas for a, b in regioes):
                raise SystemExit(f'{rel}: «{antigo}» dentro do texto novo de um achado A/C')
            achadas.append(absolutas)
        if len(achadas) != esperado:
            if CONTAR is not None:
                CONTAR.append((rel, antigo, len(achadas), esperado))
            else:
                raise SystemExit(f'{rel}: «{antigo}» aparece {len(achadas)} vez(es), e o achado conta {esperado}')
        for absolutas in achadas:
            for lo, hi, g in nucleos(pre, absolutas):
                chave = frozenset(g)
                if chave in vistas:
                    continue
                vistas.add(chave)
                janelas.append([lo, hi, g, k])
    return janelas, fora


def juntar(janelas):
    """Junta as janelas que partilham uma edição ou em que uma tem uma edição da outra lá dentro: uma troca nunca leva uma edição
    de outra."""
    janelas = sorted(janelas, key=lambda x: (x[0], x[1]))
    mudou = True
    while mudou:
        mudou = False
        for a in range(len(janelas)):
            for b in range(a + 1, len(janelas)):
                A, B = janelas[a], janelas[b]
                if A[2] & B[2] or any(A[0] <= p < A[1] for p, _ in B[2]) or any(B[0] <= p < B[1] for p, _ in A[2]):
                    janelas[a] = [min(A[0], B[0]), max(A[1], B[1]), A[2] | B[2], min(A[3], B[3])]
                    del janelas[b]
                    mudou = True
                    break
            if mudou:
                break
    return janelas


def trocas_de_janelas(rel, base_txt, pre, janelas, pares, achado, local):
    """Uma troca por texto de janela (o mesmo texto, venha de que par vier, faz uma troca só); quando esse texto aparece noutro
    sítio que não muda, a janela cresce para os dois lados (sem apanhar edições de outras janelas) até ficar única para as suas
    ocorrências. Devolve (trocas, texto final)."""
    todas = set().union(*[x[2] for x in janelas]) if janelas else set()
    final = aplicar_edicoes(pre, todas)
    grupos = {}
    for s, e, eds, k in janelas:
        grupos.setdefault(pre[s:e], []).append((s, e, eds, k))
    trocas = []
    for _, membros in sorted(grupos.items(), key=lambda g: (min(m[3] for m in g[1]), g[1][0][0])):
        ks = sorted({m[3] for m in membros})
        for antigo, novo, n in _contexto(rel, base_txt, pre, final, [m[:3] for m in membros], todas):
            # O achado e o sítio dizem de onde vêm as ocorrências que a troca leva (nos dados, podem ser de entradas diferentes).
            trocas.append({'ficheiro': rel, 'local': local(ks[0], pares[ks[0]][0], antigo), 'antigo': antigo, 'novo': novo,
                           'ocorrencias': n, 'achado': achado(ks)})
    return trocas, final


def _contexto(rel, base_txt, pre, final, membros, todas):
    # Por fim, a linha inteira (nos dados dos geradores, cada texto está numa linha).
    for L, R in [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (2, 0), (2, 2), (0, 4), (4, 0), (4, 4), (8, 8), (16, 16), (32, 32),
                 (64, 64), (24, 0), (0, 24), (48, 0), (0, 48), (64, 0), (0, 64), (96, 0), (0, 96)] + [('linhas', n) for n in range(0, 8)]:
        sub = {}
        ok = True
        for s, e, eds in membros:
            if L == 'linhas':
                a, b = pre.rfind('\n', 0, s) + 1, pre.find('\n', e)
                for _ in range(R):
                    a = pre.rfind('\n', 0, max(a - 1, 0)) + 1
                    b = pre.find('\n', b + 1) if pre.find('\n', b + 1) > 0 else len(pre)
            else:
                a, b = s - L, e + R
            if a < 0 or b > len(pre) or any(a <= p < b and (p, t) not in eds for p, t in todas):
                ok = False
                break
            chave = (pre[a:b], janela_novo(pre, a, b, eds))
            sub[chave] = sub.get(chave, 0) + 1
        if ok and all(base_txt.count(an) == n and pre.count(an) == n and final.count(no) == n and base_txt.count(no) == 0
                      and final.replace(no, '\0').count(an) == 0 for (an, no), n in sub.items()):
            return [(an, no, n) for (an, no), n in sub.items()]
    # Quando nenhuma janela igual para todas serve (o mesmo texto aparece num sítio que não muda, como um «alt» ou um excerto do
    # romance, e à volta de outras ocorrências há mais edições), cada ocorrência cresce por si, primeiro para a direita e depois
    # para a esquerda, sem apanhar edições de outras janelas, até deixar de se confundir com os sítios que não mudam.
    texto = pre[membros[0][0]:membros[0][1]]
    mudam = {s for s, _, _ in membros}
    ficam = [m.start() for m in re.finditer(re.escape(texto), pre) if m.start() not in mudam]
    sub = {}
    for s, e, eds in membros:
        a, b = s, e
        livre = lambda x, y: 0 <= x and y <= len(pre) and not any(x <= p < y and (p, t) not in eds for p, t in todas)
        while any(pre[q - (s - a):q + (b - s)] == pre[a:b] for q in ficam):
            if livre(a, b + 1) and pre[b:b + 1] not in ('\n', ''):
                b += 1
            elif livre(a - 1, b) and pre[a - 1:a] != '\n':
                a -= 1
            else:
                raise SystemExit(f'{rel}: não há contexto que distinga «{texto}»')
        chave = (pre[a:b], janela_novo(pre, a, b, eds))
        sub[chave] = sub.get(chave, 0) + 1
    if all(base_txt.count(an) == n and pre.count(an) == n and final.count(no) == n and base_txt.count(no) == 0
           and final.replace(no, '\0').count(an) == 0 for (an, no), n in sub.items()):
        return [(an, no, n) for (an, no), n in sub.items()]
    raise SystemExit(f'{rel}: não há contexto que distinga «{texto}»')


def local_b(pagina):
    def f(k, par, antigo):
        if antigo == par:
            return f'{pagina}: «{par}» que não se parte'
        contexto = antigo if len(antigo) <= 60 else antigo[:57].rstrip() + '…'
        return f'{pagina}: «{par}» que não se parte (com o contexto «{contexto}»)'
    return f


def nome(rel):
    """O nome curto da página no manifesto. Os painéis de projeção (m9/painel-m9-fxx com CARTOES) não são notas do docente: só as
    notas editoriais (as das lições geradas, sem CARTOES) levam «(notas do docente)» (a revisão do M5 viu esse erro). Os cartões
    das lições F11, F12 e F13 estão em m9/recursos/f11.js, f12.js e f13.js, que as páginas das lições carregam."""
    m = re.match(r'm9/(?:licao|painel)-(m9-f\d+)/', rel)
    if m:
        if '/painel-' not in rel:
            return m.group(1).upper()
        notas = 'CARTOES=' not in ler(rel)
        return m.group(1).upper() + (' (notas do docente)' if notas else ' (painel de projeção)')
    m = re.match(r'm9/recursos/(f\d+)\.js$', rel)
    if m:
        return 'M9-' + m.group(1).upper() + ' (cartões da lição, em ' + rel + ')'
    return rel.replace('/index.html', '')


def substituir(pre, regioes, antes, depois, n=1):
    """Troca um trecho (que aparece n vezes) e atualiza as regiões de texto novo (onde nenhum par B pode cair)."""
    if pre.count(antes) != n:
        raise SystemExit(f'trecho que não aparece {n} vez(es): {antes[:80]!r}')
    for _ in range(n):
        inicio = pre.index(antes)
        delta = len(depois) - len(antes)
        regioes = [(a if a < inicio else a + delta, b if b <= inicio else b + delta) for a, b in regioes]
        pre = pre[:inicio] + depois + pre[inicio + len(antes):]
        regioes = regioes + [(inicio, inicio + len(depois))]
    return pre, regioes


def proposta(x):
    """O que o achado põe na conta, par a par da proposta (para o relatório e para os testes): o que muda (os pares com contexto
    contam para o par da proposta que «de» diz), o que outro achado (A) já refez com o espaço preso («refeitos») e as trocas
    literais. O que a conferência deixou de fora («fora») não entra no número da proposta."""
    out = {}
    de = x.get('de', {})
    for seq, n in ([(de.get(p[0], p[0]), p[2]) for p in x['pares']] + [(s, n) for s, (n, _) in x.get('refeitos', {}).items()]
                   + [(a, n) for a, _, _, n in x.get('literais', [])]):
        out[seq] = out.get(seq, 0) + n
    return out


def b_da_pagina(rel, base_txt, pre, regioes, x, rotulo=None, todos=None):
    """As trocas de um achado B numa página: primeiro as literais (com a razão), depois os pares."""
    trocas = []
    for antigo, novo, razao, n in x.get('literais', []):
        pre, regioes = substituir(pre, regioes, antigo, j(novo), n)
        trocas.append({'ficheiro': rel, 'local': f'{rotulo or nome(rel)}: «{antigo}»', 'antigo': antigo, 'novo': j(novo),
                       'ocorrencias': n, 'achado': ACHADO.format(i=x['i'], cat='B', texto=TEXTO_CAT['B'] + ' ' + razao[0].upper()
                                                                  + razao[1:] + '.')})
    pares = x['pares']
    janelas, _ = janelas_pares(rel, pre, pares, regioes, todos=todos)
    texto = TEXTO_CAT['B'] + (' Nas notas do docente, geradas a partir dos cartões da lição (scripts/gerar_licoes_20261101.py).'
                              if '/painel-' in rel else '') + (' ' + x['nota_copia'] if x.get('nota_copia') else '')
    ts, final = trocas_de_janelas(rel, base_txt, pre, juntar(janelas), pares,
                                  lambda ks, i=x['i']: ACHADO.format(i=i, cat='B', texto=texto), local_b(rotulo or nome(rel)))
    return trocas + ts, final, regioes


def trocas_pagina(rel, achados_ac, achados_b):
    base_txt = base(rel)
    pre, regioes, trocas, relatorio = base_txt, [], [], []
    for x in achados_ac:
        pre, regioes = substituir(pre, regioes, x['antigo'], x['novo'])
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}, {x["cartao"]}', 'antigo': x['antigo'], 'novo': x['novo'],
                       'ocorrencias': 1,
                       'achado': ACHADO.format(i=x['i'], cat=x['cat'], texto=TEXTO_CAT[x['cat']] + (' ' + x['nota'] if x.get('nota') else ''))})
        relatorio.append((rel, x['i'], x['cat'], 1, 1, ''))
    if rel in COM_TABELA:
        frase, quais = COM_TABELA[rel]
        ligacoes = re.findall(r'<link rel="stylesheet" href="((?:\.\./)+)assets/appearance\.css\?v=[^"]+">', pre)
        if len(ligacoes) != 1:
            raise SystemExit(f'{rel}: a ligação à camada de aparência não aparece uma vez')
        aparencia = re.search(r'<link rel="stylesheet" href="(?:\.\./)+assets/appearance\.css\?v=[^"]+">', pre).group(0)
        folha = FOLHA.format(ligacoes[0])
        pre, regioes = substituir(pre, regioes, aparencia, folha + aparencia)
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}, cabeça: a folha das tabelas de apoio, antes da camada de aparência',
                       'antigo': aparencia, 'novo': folha + aparencia, 'ocorrencias': 1,
                       'achado': ACHADO.format(i=', '.join(map(str, quais)), cat='A',
                                               texto=f'{frase} a carregar as tabelas de apoio, antes da camada de aparência.')})
    todos = [p for x in achados_b for p in x['pares']]
    for x in achados_b:
        ts, pre, regioes = b_da_pagina(rel, base_txt, pre, regioes, x, todos=todos)
        trocas += ts
        relatorio.append((rel, x['i'], 'B', sum(p[2] for p in x['pares']) + sum(l[3] for l in x.get('literais', [])), sum(proposta(x).values()), ''))
    return base_txt, pre, trocas, relatorio


def _limite(pre, entrada):
    inicio = pre.index(f'\n  "{entrada}": {{')
    fim = pre.find('\n  "', inicio + 5)
    return inicio, (fim if fim > 0 else len(pre))


def trocas_dados(specs):
    """As trocas de um ficheiro de dados (uma ou mais entradas): as A e C, «nao_partir» e «max_em_listas» onde o gerador os lê,
    e os achados B nos textos."""
    rel = specs[0]['ficheiro']
    base_txt = base(rel)
    pre, regioes, trocas = base_txt, [], []
    rotulo = 'Dados ' + '/'.join(Path(rel).parts[-2:])
    for spec in specs:
        if spec.get('chaves'):
            # As chaves que o gerador lê para prender os números do molde, logo a seguir à âncora (na entrada, nas grelhas).
            ancora, chaves, texto = spec['chaves']
            a, b = _limite(pre, spec['entrada']) if 'entrada' in spec else (0, len(pre))
            if pre.count(ancora, a, b) != 1:
                raise SystemExit(f'{rel}: a âncora das chaves não aparece uma vez: {ancora!r}')
            k = pre.index(ancora, a, b) + len(ancora)
            fim = k + 1
            # Único no texto de agora e na base (o aplicar_trocas.py procura cada troca no texto inteiro, antes de aplicar).
            while pre.count(pre[k - len(ancora):fim]) != 1 or base_txt.count(pre[k - len(ancora):fim]) != 1:
                fim += 1
            antes = pre[k - len(ancora):fim]
            depois = ancora + chaves + pre[k:fim]
            pre, regioes = substituir(pre, regioes, antes, depois)
            onde = f'Dados das grelhas, {spec["entrada"]}' if 'entrada' in spec else 'Dados da tarefa'
            nomes_ = ', '.join('«' + c + '»' for c in re.findall(r'"(\w+)": true', chaves))
            trocas.append({'ficheiro': rel, 'local': f'{onde}: {nomes_}, os números do molde com espaço que não quebra',
                           'antigo': antes, 'novo': depois, 'ocorrencias': 1,
                           'achado': ACHADO.format(i='/'.join(map(str, spec['achados'])), cat='B', texto=TEXTO_CAT['B'] + ' ' + texto)})
        for i, cat, local, antes, depois in spec.get('ac', []):
            if depois is None:
                depois = tempos_json()
            pre, regioes = substituir(pre, regioes, antes, depois)
            trocas.append({'ficheiro': rel, 'local': local, 'antigo': antes, 'novo': depois, 'ocorrencias': 1,
                           'achado': ACHADO.format(i=i, cat=cat, texto=TEXTO_CAT[cat] + ' Nos dados do gerador das tarefas, que '
                                                   'passam iguais para a página.')})
        if spec.get('max_em_listas'):
            # O critério 4 desta entrada (o tema à escolha): «"max": 6,» passa a levar «"max_em_listas": true,» a seguir, como no M1. O trecho cresce
            # para a direita até ser único no ficheiro (agora e na base).
            a, b = _limite(pre, spec['entrada'])
            k = pre.index('"nome": "Tema à escolha (A ou B)', a, b)
            k = pre.index('"max": 6,\n', k) + len('"max": 6,\n')
            fim = k + 1
            while pre.count(pre[k - len('"max": 6,\n'):fim]) != 1 or base_txt.count(pre[k - len('"max": 6,\n'):fim]) != 1:
                fim += 1
            antes = pre[k - len('"max": 6,\n'):fim]
            depois = '"max": 6,\n     "max_em_listas": true,\n' + pre[k:fim]
            pre, regioes = substituir(pre, regioes, antes, depois)
            trocas.append({'ficheiro': rel, 'local': f'Dados das grelhas, {spec["entrada"]}: «max_em_listas» no critério 4',
                           'antigo': antes, 'novo': depois, 'ocorrencias': 1,
                           'achado': ACHADO.format(i=spec['max_em_listas'], cat='C', texto=TEXTO_CAT['C'] + (
                               ' O descritor do nível máximo do critério 4 abre os elementos de cada tema em listas, pelo gerador das '
                               'grelhas (scripts/grelhas_tarefas.py), como no M1 e no M5; a versão de correção fica com o texto corrido.'))})
    janelas, pares, nomes = [], [], []
    for spec in specs:
        limite = _limite(pre, spec['entrada']) if 'entrada' in spec else None
        js, _ = janelas_pares(rel, pre, spec['pares'], regioes, limite, todos=[p for s in specs for p in s['pares']])
        for x in js:
            x[3] += len(pares)
        janelas += js
        pares += spec['pares']
        nomes += [(spec.get('entrada'), '/'.join(map(str, spec['achados'])))] * len(spec['pares'])
    def achado_dados(ks):
        quais = '/'.join(dict.fromkeys(n for k in ks for n in nomes[k][1].split('/')))
        entradas = list(dict.fromkeys(nomes[k][0] for k in ks if nomes[k][0]))
        mais = f' A troca leva as ocorrências das entradas {" e ".join(entradas)}.' if len(entradas) > 1 else ''
        return ACHADO.format(i=quais, cat='B', texto=TEXTO_CAT['B'] + ' Nos dados do gerador, que passam iguais para as páginas.' + mais)
    ts, final = trocas_de_janelas(
        rel, base_txt, pre, juntar(janelas), pares, achado_dados,
        lambda k, par, antigo: local_b(rotulo + (f', {nomes[k][0]}' if nomes[k][0] else ''))(k, par, antigo))
    return base_txt, final, trocas + ts


def cartoes_de(texto):
    """Os cartões de uma lição (CARTOES=[…])."""
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0] if m else None


# Os enunciados dos painéis do docente (m9/painel-m9-fxx) são os dos cartões da lição: o «p» (ou a «frase»), com ou sem os
# marcadores de negrito e de itálico e com as lacunas «[1]» como «…» (tests/test_paineis_cartoes.py e test_transversal_clareza.py).
ENUNCIADOS = [
    lambda c: c.get('p') or c.get('frase') or '',
    lambda c: re.sub(r'\[\d\]', '…', re.sub(r'\*\*(.+?)\*\*', r'\1', c.get('p') or c.get('frase') or '')),
    lambda c: re.sub(r'\[\d\]', '…', re.sub(r'\*\*(.+?)\*\*', r'\1', re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', c.get('p') or c.get('frase') or ''))),
]


def trocas_paineis(finais):
    """Os painéis do docente seguem a lição: onde um enunciado de um cartão mudou (achados B e C), o enunciado do painel muda da
    mesma maneira, na lista do painel (CARTOES) e no seletor (<select data-r-k>). Só espaços que não quebram e junções."""
    out = {}
    for licao in sorted(r for r in finais if r.startswith('m9/licao-')):
        painel = licao.replace('/licao-', '/painel-')
        if not (ROOT / painel).is_file() or any(x['ficheiro'] == painel for x in NOTAS):
            continue
        base_txt = base(painel)
        itens = cartoes_de(base_txt)
        if itens is None:
            continue
        antes, depois = cartoes_de(finais[licao][0]), cartoes_de(finais[licao][1])
        i = PAINEIS.get(painel)
        pre, trocas = base_txt, []
        for item in itens:
            k = item['k']
            f = next((f for f in ENUNCIADOS if f(antes[k]) == item['p']), None)
            if f is None or f(depois[k]) == item['p']:
                continue
            novo = dict(item, p=f(depois[k]))
            # No seletor, alguns enunciados estão cortados: o corte fica no mesmo sítio do texto.
            # O seletor mostra o enunciado sem os marcadores de itálico (_…_) ou, nos painéis do M7 e do M8, com o itálico em <i>.
            opcao = re.search(r'<option value="%d">(.*?)</option>' % k, pre).group(1)
            formas = (lambda x: html.escape(x, quote=False),
                      lambda x: html.escape(re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', x), quote=False),
                      lambda x: re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<i>\1</i>', html.escape(x, quote=False)))
            g = next((g for g in formas if g(item['p']).startswith(opcao)), None)
            if g is None:
                raise SystemExit(f'{painel}: o seletor do cartão {k} não é o enunciado do painel')
            novo_esc = g(novo['p'])
            corte = next(n for n in range(len(novo_esc) + 1) if novo_esc[:n].replace(NBSP, ' ').replace(WJ, '') == opcao
                         and not novo_esc[n:n + 1] == WJ)
            pares = [(json.dumps(item, ensure_ascii=False, separators=(',', ':')), json.dumps(novo, ensure_ascii=False, separators=(',', ':')),
                      'a lista do painel'),
                     (f'<option value="{k}">{opcao}</option>', f'<option value="{k}">{novo_esc[:corte]}</option>', 'o seletor')]
            for antigo, novo_txt, onde in pares:
                if antigo == novo_txt:
                    continue
                if pre.count(antigo) != 1:
                    raise SystemExit(f'{painel}: o enunciado do cartão {k} não aparece uma vez em {onde}')
                pre = pre.replace(antigo, novo_txt)
                trocas.append({'ficheiro': painel, 'local': f'{nome(painel)}: o enunciado do cartão {k} igual ao da lição, em {onde}',
                               'antigo': antigo, 'novo': novo_txt, 'ocorrencias': 1,
                               'achado': ACHADO.format(i=i, cat='B', texto=TEXTO_CAT['B'] + ' No painel do docente, que segue os '
                                                       'enunciados dos cartões da lição.')})
        if trocas:
            if i is None:
                raise SystemExit(f'{painel}: o painel muda com a lição e não tem achado')
            out[painel] = (base_txt, pre, trocas)
    return out


def _por_pagina():
    por_pagina = {}
    for x in achados_ac() + ac_grelhas():
        por_pagina.setdefault(x['ficheiro'], ([], []))[0].append(x)
    for x in ACHADOS_B + NOTAS:
        por_pagina.setdefault(x['ficheiro'], ([], []))[1].append(x)
    for rel in COM_TABELA:
        por_pagina.setdefault(rel, ([], []))
    return por_pagina


def construir_sem_conferir():
    for rel, (ac, bs) in sorted(_por_pagina().items()):
        try:
            trocas_pagina(rel, ac, bs)
        except SystemExit as erro:
            print('ERRO', rel, erro)
    dados = {}
    for spec in DADOS:
        dados.setdefault(spec['ficheiro'], []).append(spec)
    for rel, specs in dados.items():
        try:
            trocas_dados(specs)
        except SystemExit as erro:
            print('ERRO', rel, erro)


def construir():
    finais, relatorio = {}, []
    for rel, (ac, bs) in sorted(_por_pagina().items()):
        base_txt, final, trocas, rel_pag = trocas_pagina(rel, ac, bs)
        if trocas:
            finais[rel] = (base_txt, final, trocas)
        relatorio += rel_pag
    dados = {}
    for spec in DADOS:
        dados.setdefault(spec['ficheiro'], []).append(spec)
    for rel, specs in dados.items():
        finais[rel] = trocas_dados(specs)
    finais.update(trocas_paineis(finais))
    # Confere cada ficheiro como o aplicar_trocas.py o vai conferir: a partir da base, e com tudo já aplicado.
    for rel, (base_txt, final, trocas) in finais.items():
        lista = list(enumerate(trocas, 1))
        try:
            b, depois, _ = processar(rel, lista, base_txt)
            assert b == base_txt and depois == final, rel
            b, depois, _ = processar(rel, lista, final)
            assert b == base_txt and depois == final, rel
        except (TrocaFalhou, AssertionError) as erro:
            raise SystemExit(f'{rel}: as trocas não conferem: {erro}')
    # A ordem dos ficheiros: os dados dos geradores primeiro (como as páginas saem deles), depois as páginas, por nome.
    ordem = sorted(finais, key=lambda r: (not r.startswith('docs/'), r))
    return [t for rel in ordem for t in finais[rel][2]], relatorio, len(finais)


def main():
    global CONTAR
    if '--contar' in sys.argv:
        # Só para conferir as contagens: diz onde o número de ocorrências não é o do achado, sem escrever nada.
        CONTAR = []
        construir_sem_conferir()
        for r in CONTAR:
            print(*r)
        return
    todas, relatorio, n = construir()
    if '--relatorio' in sys.argv:
        for r in relatorio:
            print(*r)
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {n} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
