#!/usr/bin/env python3
"""12/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M8 do Português.

Constrói scripts/cuidado_m8_20261112.json, a camada literal cuidado_m8_20261112, com os achados CONFIRMADOS da varredura do M8
(refeita a 9/11 e conferida a 11/11, só leitura, sobre o main 4bf4a053): dos 44 confirmados (8 A, 30 B e 6 C) entram 36: os 8
achados A (tabelas onde há itens paralelos), 22 de referências e números que se partiam (B) e os 6 casos do mesmo tipo (C).
Ficam de fora, por decisão já tomada para todos os módulos, como do M1 ao M7, os 6 achados B dos diapositivos (20), das três
provas rápidas (43, 44 e 45), dos questionários (46) e da página «todos» (47): essas páginas não mudam. Ficam também de fora os 2
achados B dos painéis da F03 e da F10 (38 e 39): as ocorrências confirmadas estão todas no material do relâmpago (MATERIAL), que
não muda. Os 7 achados que a conferência recusou (9, 10, 13, 16, 17, 19 e 29) também não entram. A camada aplica-se com
scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/cuidado-m8-edits-20261112.json:

  python3 scripts/cuidado_m8_20261112.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m8_20261112.json --manifesto tests/fixtures/cuidado-m8-edits-20261112.json \\
      --base-commit 399a9ce37df64e2dc3d0b62856d85b1b3c00de99 --nota "…"

Fica por cima da decisão 152 no M7 (cuidado_m7_20261111, no ramo do pedido #194, commit 399a9ce3, com o main a7a16f2d já
dentro), que não toca em nenhum ficheiro desta camada.

Segue o modelo da camada do M7 (scripts/cuidado_m7_20261111.py), com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como do M1 ao M7: class apoio-tabela, th scope=col no cabeçalho, th
  scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader, rowheader, cell), porque no
  telemóvel a tabela passa a display:block. Dentro do JSON dos cartões e das atividades, as aspas vão com barra (\\"). São oito:
  os pesos da avaliação no índice, no guia e no mapa do módulo (achados 0, 1 e 2, como no M5 e no M7: o rótulo num parágrafo, a
  tabela Elemento/Peso com a coluna do peso em 5,5 rem, e o resto da frase no p.avaliacao-tarefas, como estava); as noções das
  caixas «Recorda» da F04, da F05 e da F08 (achados 3, 4 e 5: Noção/O que é; na F08, a frase dos três nomes fica num parágrafo a
  seguir); os três termos do «O essencial» da F15 (achado 6: Termo/O que é; lição gerada, com os fechos como «<\\/»); e os quatro
  valores aspetuais de «Fechou, fechava, foi fechando» (achado 8: Valor/Exemplo/O que mostra, a proposta que a conferência
  corrigiu para três colunas). Cada página com uma tabela nova carrega assets/pt-lessons/apoios-tabelas.css antes de
  assets/appearance.css, na versão do M1 (20261106.1: a folha não muda).
- B: U+00A0 (espaço que não quebra) nos espaços que a proposta final prende, e U+2060 (junção de palavras) logo a seguir ao
  traço de intervalo e ao hífen da sigla «M8-Fxx». Cada par da proposta conta-se com a palavra inteira («5 min» não conta dentro
  de «15 min», nem «10 min» dentro de «10 minutos») e fora das cadeias maiores dos outros pares da página («3 de Maio» não conta
  dentro de «3 de Maio de 1808»); a troca leva só os espaços que muda, com o mínimo de contexto que a distingue. Nas datas, a
  proposta prende o dia ao «de» e o ano ao «de», como no M5 e no M7; em «5 a 7 minutos» só prende a unidade, e em «versos 1 e 2»
  prende o nome ao primeiro número e o «e» ao segundo. Ficam de fora: os «alt» (e aria-label, href, title, content e
  data-titulo, que vira o title do vídeo), o <title>, o título que o script do índice guarda (TIT), o texto dos desenhos (SVG),
  a «frase» dos cartões sublinhar, as «palavras» dos cartões frase e os «passos» dos cartões ordenar, as notas internas dos
  dados, a casca das lições (abaixo) e o que a conferência tirou com a razão («nota 2», «Bloco 27», «D. João» sem numeral, os
  traços entre ano e lugar do mapa e o «séc. XX» da casca de «Pastelaria»).
- C: as quatro peças e os três «o que não é» de «O texto de opinião, passo a passo» em duas listas (achado 7, que a conferência
  passou de tabela a listas, com o texto igual); «Três antes de mim», no guia, em lista numerada (achado 11, o mesmo trecho,
  letra a letra, dos guias do M5 e do M7); os três passos da ajuda de «Apontar para trás, apontar para a frente» em lista
  numerada, com a frase final num parágrafo (achado 12); o modelo de interpretação da F13 em lista numerada (achado 14) e as três
  formulações com letra da F15 em lista (achado 15), nas duas lições geradas; e, no portefólio, os oito nomes de ficheiro que
  estavam em texto simples em <code>, como os outros seis, com <wbr> a seguir a cada «_» e «td code{white-space:nowrap}» na folha
  da página (achado 18, como nos portefólios do M5 e do M7: os nomes só mudam de linha nos pontos marcados).
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois. Nas tabelas dos pesos, os números já vão com
  o espaço que não quebra (a conferência tirou esses pares dos achados B 21, 22 e 36).

A casca das lições (migalhas, «Estás em: Lição M8-Fxx», o título escondido e a sigla «Lição M8-Fxx» do rodapé) não muda aqui,
ficheiro a ficheiro: muda no molde, como do M1 ao M7. Nas outras páginas (índice, guia, mapa e portefólio do módulo e o caderno
de campo da visita), a proposta final conta as migalhas e o «3.º ano» fica preso nas migalhas e no cabeçalho.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e das listas (cai o negrito dos nomes que passam a
cabeçalho de linha, os dois pontos e o ponto final de cada célula e os «1) 2) 3)» e «1. 2. 3.» que as listas numeradas
substituem; os cabeçalhos «Elemento», «Peso», «Noção», «Termo», «O que é», «Valor», «Exemplo» e «O que mostra» são os da
proposta), os espaços invisíveis e uma correção que a proposta final faz: «Séc. XX» passa a «século XX» no rótulo do guia, como
o M5 fez na mesma linha do seu guia («Narrativa do Séc. XIX»); nas provas rápidas e nos questionários, que ficam de fora, a
abreviatura continua. O script calcula as trocas sobre a base (a página com esta camada desfeita pelo manifesto, quando ele já
existe): pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.

Páginas geradas: as tarefas da M8-U1 e da M8-U2 (scripts/tarefas_escolha.py) mudam nos dados (docs/pedagogia/tarefas-escolha/
m8-u1.json e m8-u2.json: «nao_partir», como do M1 ao M7, que prende os números do molde e a meta descrição, e os achados B);
os dados estão na mesma camada e as páginas regeneram-se sem diferenças. Os aquecimentos, as grelhas e as correções do M8 não
têm achados. As lições F13, F14, F15 e F16 são geradas (scripts/gerar_licoes_20261101.py): os textos mudam nas fontes
(scripts/licoes_20261101.py e, para a data da fotografia da F14, scripts/imagens_licoes_20261101.py, fora da camada, como no M5 e
no M6; o gerador liga a folha das tabelas na F15), e as lições mudam aqui e saem iguais do gerador; as suas notas do docente não
repetem nenhum trecho mudado. O painel de projeção da F11 segue o enunciado do cartão que mudou (a lista CARTOES e o seletor);
o material do relâmpago (MATERIAL) segue a lição antes das camadas de cuidado (tests/test_sala_desligada.py compara-o com ela)
e não muda, como do M1 ao M7. As cópias dos cartões no banco das provas rápidas do índice (var U) mudam como as lições de onde
vêm (estão nos pares do achado 22).
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m8_20261112.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m8-edits-20261112.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
CONTAR = None
ACHADO = '12/11/2026: decisão 152 (cuidado em todas as lições), varredura do M8, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como do M1 ao M7).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e ao hífen da '
          'sigla).'),
    'C': 'Caso do mesmo tipo.',
}


def j(s):
    """As formas da proposta escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return s.replace('{N}', NBSP).replace('{J}', WJ)



# A folha das tabelas de apoio, antes da camada de aparência (como do M1 ao M7), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
INDICE = 'm8/index.html'
GUIA = 'm8/guia-da-tarefa-m8/index.html'
MAPA = 'm8/mapa-do-modulo-m8/index.html'
F04, F05, F08, F13, F15 = (f'm8/licao-m8-{n}/index.html' for n in ('f04', 'f05', 'f08', 'f13', 'f15'))
ASPETO = 'm8/gramatica-aspeto/index.html'
COM_TABELA = {
    INDICE: ('O índice do módulo passa', [0]),
    GUIA: ('O guia da tarefa passa', [1]),
    MAPA: ('O mapa do módulo passa', [2]),
    F04: ('A lição passa', [3]),
    F05: ('A lição passa', [4]),
    F08: ('A lição passa', [5]),
    F15: ('A lição passa', [6]),
    ASPETO: ('A atividade passa', [8]),
}
# Na tabela dos pesos, a coluna do peso só leva o número (as larguras do índice do M5).
PESOS = [' style="width:auto"', ' style="width:5.5rem"']


def tabela(colunas, linhas, json_=True, larguras=None, fechos=False):
    """A tabela de apoio, igual às do M1 ao M7: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label com
    o nome da coluna, e os role. Com json_, as aspas vão escapadas como no JSON dos cartões; com fechos, os «</» vão como «<\\/»
    (as lições geradas por scripts/gerar_licoes_20261101.py)."""
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
    if fechos:
        html_ = html_.replace('</', '<\\/')
    return html_.replace('"', '\\"') if json_ else html_


# Achados 0, 1 e 2 (A): os pesos da avaliação no índice, no guia e no mapa, como no M5 e no M7 (um parágrafo com o rótulo, a
# tabela Elemento/Peso e o resto da frase no p.avaliacao-tarefas, que fica como estava). Os pesos já vão com o espaço que não
# quebra: a conferência tirou-os dos achados B 22, 21 e 36.
PESOS_LINHAS = [['Tarefa da Unidade 1', '30{N}%'], ['Tarefa da Unidade 2', '30{N}%'], ['Provas rápidas', '10{N}%'],
                ['Prova escrita', '30{N}%']]
PESOS_FRASE = ': tarefa da Unidade 1, 30 %; tarefa da Unidade 2, 30 %; provas rápidas, 10 %; prova escrita, 30 %. '


def pesos(rotulo):
    """(antes, depois) do parágrafo dos pesos, com o rótulo da página («Pesos na avaliação» ou «Avaliação»)."""
    return ('<p class="avaliacao-tarefas">' + rotulo + PESOS_FRASE,
            f'<p>{rotulo}:</p>' + j(tabela(['Elemento', 'Peso'], PESOS_LINHAS, json_=False, larguras=PESOS)) + '<p class="avaliacao-tarefas">')


# Achados 3, 4 e 5 (A): as noções das caixas «Recorda» da F04, da F05 e da F08 (dentro do JSON dos cartões), como na M5-F13.
F04_ANTES = ('<p><b>Arte poética</b>: o poema que fala da própria poesia. <b>Comparação</b>: aproxima elementos por uma relação '
             'explícita, como acontece com «como» nesta abertura. <b>Metáfora</b>: constrói uma identificação figurada; a ausência de '
             '«como» não basta para a reconhecer. <b>Interrogação retórica</b>: pergunta que não espera resposta.</p>')
F04_LINHAS = [['Arte poética', 'o poema que fala da própria poesia'],
              ['Comparação', 'aproxima elementos por uma relação explícita, como acontece com «como» nesta abertura'],
              ['Metáfora', 'constrói uma identificação figurada; a ausência de «como» não basta para a reconhecer'],
              ['Interrogação retórica', 'pergunta que não espera resposta']]
F05_ANTES = ('<p><b>Tradição literária</b>: o que o poema vai buscar a textos antigos. Aqui, a forma da prece e a história dos pães e '
             'dos peixes, dos Evangelhos. <b>Apóstrofe</b>: chamar alguém («Senhor»). <b>Ironia</b>: o contexto leva a entender uma '
             'distância crítica em relação ao que se diz literalmente; nem todo o sentido indireto é irónico.</p>')
F05_LINHAS = [['Tradição literária', 'o que o poema vai buscar a textos antigos. Aqui, a forma da prece e a história dos pães e dos '
               'peixes, dos Evangelhos'],
              ['Apóstrofe', 'chamar alguém («Senhor»)'],
              ['Ironia', 'o contexto leva a entender uma distância crítica em relação ao que se diz literalmente; nem todo o sentido '
               'indireto é irónico']]
F08_ANTES = ('<p><b>Unidade de ação</b>: uma só linha de acontecimentos. <b>Concentração de tempo e de espaço</b>: pouco tempo, poucos '
             'lugares. <b>Discurso direto</b>: as palavras da personagem, com travessão ou aspas. <b>Discurso indireto</b>: o narrador '
             'conta o que foi dito. No conto, a protagonista tem três nomes, um para cada idade: Gi, George, Georgina.</p>')
F08_LINHAS = [['Unidade de ação', 'uma só linha de acontecimentos'],
              ['Concentração de tempo e de espaço', 'pouco tempo, poucos lugares'],
              ['Discurso direto', 'as palavras da personagem, com travessão ou aspas'],
              ['Discurso indireto', 'o narrador conta o que foi dito']]
F08_DEPOIS = '<p>No conto, a protagonista tem três nomes, um para cada idade: Gi, George, Georgina.</p>'

# Achado 6 (A): os três termos do «O essencial» da F15 (lição gerada: na página, os fechos vão como «<\/»).
F15_ANTES = ('<p><strong>Autora:<\\/strong> pessoa real que escreve. <strong>Voz poética:<\\/strong> instância construída no poema. '
             '<strong>Reportagem:<\\/strong> seleção jornalística de informações, declarações e imagens.<\\/p>')
F15_LINHAS = [['Autora', 'pessoa real que escreve'], ['Voz poética', 'instância construída no poema'],
              ['Reportagem', 'seleção jornalística de informações, declarações e imagens']]

# Achado 8 (A): os quatro valores aspetuais de «Fechou, fechava, foi fechando», em três colunas (como a de m3/gram-modalidade).
ASPETO_ANTES = ('<p><b>Perfetivo:</b> «Ontem li o conto até ao fim» apresenta uma leitura concluída. <b>Imperfetivo:</b> «Eu lia o conto '
                'quando ouvi o carro» mostra a leitura em curso; não diz se parei ou se cheguei ao fim.</p><p><b>Habitual:</b> '
                '«Costumava reler o conto aos domingos» apresenta um costume. <b>Iterativo:</b> «Naquela revisão, reli o verso várias '
                'vezes» apresenta repetição num episódio, sem exigir contagem exata.</p>')
ASPETO_LINHAS = [['Perfetivo', '«Ontem li o conto até ao fim»', 'apresenta uma leitura concluída'],
                 ['Imperfetivo', '«Eu lia o conto quando ouvi o carro»', 'mostra a leitura em curso; não diz se parei ou se cheguei ao fim'],
                 ['Habitual', '«Costumava reler o conto aos domingos»', 'apresenta um costume'],
                 ['Iterativo', '«Naquela revisão, reli o verso várias vezes»', 'apresenta repetição num episódio, sem exigir contagem exata']]

# Achado 7 (C): as quatro peças e os três «o que não é» de «O texto de opinião, passo a passo», em duas listas (texto igual).
OPINIAO = 'm8/opiniao-ramos/index.html'
OPINIAO_ANTES = ('<p>Um <b>texto de opinião</b> defende uma ideia. Tem quatro peças: a <b>tese</b> (o que defendes, numa frase); um '
                 '<b>argumento</b> com um <b>exemplo</b> concreto; o <b>contra-argumento</b> (o que diz quem discorda) e a tua resposta; '
                 'a <b>conclusão</b>, que volta à tese com uma palavra nova. O que não é texto de opinião: descrever os dois lados sem '
                 'escolher; afirmar sem exemplo («toda a gente sabe que…»); fingir que ninguém discorda.</p>')
OPINIAO_DEPOIS = ('<p>Um <b>texto de opinião</b> defende uma ideia. Tem quatro peças:</p><ul><li>a <b>tese</b> (o que defendes, numa '
                  'frase);</li><li>um <b>argumento</b> com um <b>exemplo</b> concreto;</li><li>o <b>contra-argumento</b> (o que diz quem '
                  'discorda) e a tua resposta;</li><li>a <b>conclusão</b>, que volta à tese com uma palavra nova.</li></ul><p>O que não é '
                  'texto de opinião:</p><ul><li>descrever os dois lados sem escolher;</li><li>afirmar sem exemplo («toda a gente sabe '
                  'que…»);</li><li>fingir que ninguém discorda.</li></ul>')

# Achado 11 (C): «Três antes de mim», no guia, em lista numerada (o mesmo trecho, letra a letra, dos guias do M5 e do M7).
REGRA_ANTES = ('Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta ao teu par de trabalho. Só depois '
               'levantas o braço.</div>')
REGRA_DEPOIS = ('Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica;</li><li>pergunta ao teu par de '
                'trabalho.</li></ol>Só depois levantas o braço.</div>')

# Achado 12 (C): os três passos da ajuda de «Apontar para trás, apontar para a frente», em lista numerada; a frase final num parágrafo.
ANAFORA = 'm8/anafora-catafora/index.html'
ANAFORA_ANTES = ('<p>1. Escolhe a expressão em análise. 2. Pergunta «a que se refere?». 3. Localiza a resposta: antes, retoma; depois, '
                 'antecipação. Se houver dois referentes possíveis, explicita-os antes de decidir.</p>')
ANAFORA_DEPOIS = ('<ol><li>Escolhe a expressão em análise.</li><li>Pergunta «a que se refere?».</li><li>Localiza a resposta: antes, '
                  'retoma; depois, antecipação.</li></ol><p>Se houver dois referentes possíveis, explicita-os antes de decidir.</p>')

# Achado 14 (C): o modelo de interpretação da F13 (lição gerada), em lista numerada: os retornos pedem os passos «por esta ordem».
F13_ANTES = ('<p><strong>Observação:<\\/strong> a abertura aproxima palavras e desgaste. <strong>Relação:<\\/strong> o que era '
             'partilhado já não chega para sustentar o vínculo. <strong>Limite:<\\/strong> isso não demonstra que a linguagem seja '
             'inútil em todas as relações.<\\/p>')
F13_DEPOIS = ('<ol><li><strong>Observação:<\\/strong> a abertura aproxima palavras e desgaste.<\\/li><li><strong>Relação:<\\/strong> o '
              'que era partilhado já não chega para sustentar o vínculo.<\\/li><li><strong>Limite:<\\/strong> isso não demonstra que a '
              'linguagem seja inútil em todas as relações.<\\/li><\\/ol>')

# Achado 15 (C): as três formulações com letra da F15 (lição gerada), em lista.
F15_FORM_ANTES = ('<p>Formulações criadas para esta lição. A: A página apresenta o livro como atento a desigualdades. B: A autora '
                  'afirmou esta frase. C: A voz deste poema é necessariamente a autora.<\\/p>')
F15_FORM_DEPOIS = ('<p>Formulações criadas para esta lição.<\\/p><ul><li>A: A página apresenta o livro como atento a '
                   'desigualdades.<\\/li><li>B: A autora afirmou esta frase.<\\/li><li>C: A voz deste poema é necessariamente a '
                   'autora.<\\/li><\\/ul>')

# Achado 18 (C): no portefólio, os oito nomes de ficheiro que estavam em texto simples passam a <code>, como os outros seis; os
# nomes podem mudar de linha a seguir a cada «_» (<wbr>, como nos portefólios do M5 e do M7), e só aí.
PORTEFOLIO = 'm8/portefolio-do-modulo-m8/index.html'
PORT_NOMES = ([f'M8_U{u}_{n}' for u in (1, 2) for n in ('registo_&lt;dia-mês&gt;', 'retoma', 'o-que-aprendi')]
              + ['M8_U1_Tarefa', 'M8_U2_Tarefa'])
PORT_JA_CODE = ['M8_capa', 'M8_cartao-do-percurso', 'M8_Revisao1', 'M8_Revisao2', 'M8_Prova-escrita', 'M8_balanco']
PORT_CSS_ANTES = 'code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
PORT_CSS_DEPOIS = PORT_CSS_ANTES + 'td code{white-space:nowrap}\n'


def com_wbr(nome_):
    """O nome com <wbr> a seguir a cada «_» (onde pode mudar de linha)."""
    return nome_.replace('_', '_<wbr>')


def achados_ac():
    """Os 14 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte)."""
    recorda = ('As noções no cabeçalho de linha, sem negrito; caem os dois pontos e o ponto final de cada definição, como na '
               'M5-F13; as palavras ficam todas.')
    out = []
    for i, rel, rotulo, onde in ((0, INDICE, 'Pesos na avaliação', '«Como se cumpre uma unidade»: os pesos na avaliação'),
                                 (1, GUIA, 'Avaliação', '«Tarefas das unidades»: os pesos na avaliação'),
                                 (2, MAPA, 'Avaliação', '«As tarefas das unidades»: os pesos na avaliação')):
        antes, depois = pesos(rotulo)
        out.append(dict(i=i, cat='A', ficheiro=rel, cartao=onde,
                        nota=('Como no M5 e no M7: o rótulo num parágrafo, a tabela Elemento/Peso (a coluna do peso com 5,5 rem) e o '
                              'resto da frase no p.avaliacao-tarefas, como estava. Os pesos já levam o espaço que não quebra.'),
                        antigo=antes, novo=depois))
    out += [
        dict(i=3, cat='A', ficheiro=F04, cartao='cartão 7, Para entender («Recorda»)', nota=recorda,
             antigo=F04_ANTES, novo=tabela(['Noção', 'O que é'], F04_LINHAS)),
        dict(i=4, cat='A', ficheiro=F05, cartao='cartão 7, Para entender («Recorda»)',
             nota=recorda + ' A segunda frase da primeira definição fica na mesma célula; a consulta fica a seguir, como estava.',
             antigo=F05_ANTES, novo=tabela(['Noção', 'O que é'], F05_LINHAS)),
        dict(i=5, cat='A', ficheiro=F08, cartao='cartão 5, Para entender («Recorda»)',
             nota=recorda + ' A frase dos três nomes, que já não é definição, fica num parágrafo a seguir.',
             antigo=F08_ANTES, novo=tabela(['Noção', 'O que é'], F08_LINHAS) + F08_DEPOIS),
        dict(i=6, cat='A', ficheiro=F15, cartao='cartão 3, O essencial',
             nota=('Os três termos no cabeçalho de linha, sem negrito nem dois pontos; cai o ponto final de cada definição. A lição é '
                   'gerada: a fonte (scripts/licoes_20261101.py) muda da mesma maneira e a página sai igual do gerador.'),
             antigo=F15_ANTES, novo=tabela(['Termo', 'O que é'], F15_LINHAS, fechos=True)),
        dict(i=7, cat='C', ficheiro=OPINIAO, cartao='passo 1, «Ler»',
             nota='As quatro peças e os três «o que não é» em duas listas, cada item com o «;» ou o ponto final que tinha; o texto fica igual.',
             antigo=OPINIAO_ANTES, novo=OPINIAO_DEPOIS),
        dict(i=8, cat='A', ficheiro=ASPETO, cartao='passo 1, «A ideia»',
             nota=('Três colunas (valor, exemplo, o que mostra), com as palavras todas; caem os dois pontos, o negrito do valor e o '
                   'ponto final de cada linha.'),
             antigo=ASPETO_ANTES, novo=tabela(['Valor', 'Exemplo', 'O que mostra'], ASPETO_LINHAS)),
        dict(i=11, cat='C', ficheiro=GUIA, cartao='«Três antes de mim» (div.regra)',
             nota='Os três passos numerados à mão passam a lista numerada, como nos guias do M5 e do M7; o texto fica igual.',
             antigo=REGRA_ANTES, novo=REGRA_DEPOIS),
        dict(i=12, cat='C', ficheiro=ANAFORA, cartao='passo 1, «Ajuda: como confirmar a direção?»',
             nota='Os três passos numerados à mão passam a lista numerada; a frase final, que já não é passo, fica num parágrafo.',
             antigo=ANAFORA_ANTES, novo=ANAFORA_DEPOIS),
        dict(i=14, cat='C', ficheiro=F13, cartao='cartão 8, Para entender («Um modelo de interpretação»)',
             nota=('Os três passos com rótulo em lista numerada (os retornos pedem-nos «por esta ordem»); o texto fica igual. A lição é '
                   'gerada: a fonte (scripts/licoes_20261101.py) muda da mesma maneira e a página sai igual do gerador.'),
             antigo=F13_ANTES, novo=F13_DEPOIS),
        dict(i=15, cat='C', ficheiro=F15, cartao='cartão 13, Compara («Reconhecer uma atribuição»)',
             nota=('As três formulações com letra em lista; o texto fica igual. A lição é gerada: a fonte (scripts/licoes_20261101.py) '
                   'muda da mesma maneira e a página sai igual do gerador.'),
             antigo=F15_FORM_ANTES, novo=F15_FORM_DEPOIS),
    ]
    for nome_ in PORT_NOMES:
        out.append(dict(i=18, cat='C', ficheiro=PORTEFOLIO, cartao=f'«A lista de verificação»: o nome {html.unescape(nome_)} em <code>',
                        nota=('O nome do ficheiro, que se copia letra a letra, passa a <code>, como os outros seis da lista; pode mudar '
                              'de linha a seguir a cada «_» (<wbr>), como nos portefólios do M5 e do M7.'),
                        antigo=f'<td>{nome_}</td>', novo=f'<td><code>{com_wbr(nome_)}</code></td>'))
    for nome_ in PORT_JA_CODE:
        out.append(dict(i=18, cat='C', ficheiro=PORTEFOLIO, cartao=f'«A lista de verificação»: o nome {nome_} pode mudar de linha depois de «M8_»',
                        nota='O nome já estava em <code>; leva <wbr> depois de «M8_», como nos portefólios do M5 e do M7.',
                        antigo=f'<td><code>{nome_}</code></td>', novo=f'<td><code>{com_wbr(nome_)}</code></td>'))
    out.append(dict(i=18, cat='C', ficheiro=PORTEFOLIO, cartao='a folha da página: os nomes só mudam de linha onde podem',
                    nota='Como nos portefólios do M5 e do M7: «td code{white-space:nowrap}», a seguir à regra do <code>.',
                    antigo=PORT_CSS_ANTES, novo=PORT_CSS_DEPOIS))
    return out


def ac_grelhas():
    """Sem achados A ou C nas grelhas do M8 (a função fica, como no M6 e no M7, para os testes e para a ordem das trocas)."""
    return []


FUZ = ('3 de maio de 1808', '3{N}de maio de{N}1808')
GOYA = ('3 de Maio de 1808', '3{N}de Maio de{N}1808')
META = ('durante 90 minutos, com entrega', 'durante 90{N}minutos, com entrega',
        'a meta descrição muda com «nao_partir» (o gerador prende os três números do molde, como do M1 ao M7); a proposta '
        'não a lista porque não se vê', 1)
CASCA = 'está nas migalhas da casca da lição, que muda no molde'
NO_SCRIPT = 'é o título que o script do índice guarda (a variável TIT), que não se vê assim; fica como o <title>, como no M5'
ACHADOS_B = [
    dict(i=21, ficheiro=GUIA,
         literais=[('Poesia e Conto do Séc. XX', 'Poesia e Conto do século{N}XX',
                    '«Séc. XX» passa a «século XX», como na proposta final e como o M5 fez na mesma linha do guia («Narrativa do '
                    'Séc. XIX»): é a única forma abreviada do guia; já com o espaço que não quebra', 1)],
         pares=[('90 minutos', '90{N}minutos', 1), ('30 %', '30{N}%', 2), ('10 minutos', '10{N}minutos', 1),
                ('5 minutos', '5{N}minutos', 1), ('10 min', '10{N}min', 1), ('5 min', '5{N}min', 1), ('60 min', '60{N}min', 1),
                ('15 min', '15{N}min', 1), ('3.º ano', '3.º{N}ano', 2)]),
    dict(i=22, ficheiro=INDICE,
         pares=[('90 minutos', '90{N}minutos', 3), ('30 %', '30{N}%', 2), ('90 min', '90{N}min', 4), ('25 min', '25{N}min', 2),
                ('10 min', '10{N}min', 2), ('30 segundos', '30{N}segundos', 4), ('5 a 7 minutos', '5 a 7{N}minutos', 3),
                ('90 segundos', '90{N}segundos', 4), ('3.º ano', '3.º{N}ano', 2), ('século XX</span></h1>', 'século{N}XX</span></h1>', 1),
                ('século XX preferem', 'século{N}XX preferem', 1), ('século XX. Os registos', 'século{N}XX. Os registos', 1),
                ('número 1760', 'número{N}1760', 1), GOYA + (2,), FUZ + (1,), ('3 de Maio', '3{N}de Maio', 2),
                ('M8-F03', 'M8-{J}F03', 1)],
         de={s: 'século XX' for s in ('século XX</span></h1>', 'século XX preferem', 'século XX. Os registos')},
         fora={'TIT="Poesia e conto do século XX"': (1, NO_SCRIPT)}),
    dict(i=23, ficheiro='m8/licao-m8-f01/index.html',
         pares=[('3 min', '3{N}min', 1), ('século XIX', 'século{N}XIX', 1), FUZ + (1,), ('1872–1921', '1872–{J}1921', 1)]),
    dict(i=24, ficheiro='m8/licao-m8-f03/index.html',
         pares=[('2 min', '2{N}min', 1), ('4 min', '4{N}min', 1), ('p. 5', 'p.{N}5', 1), ('pp. 52–53', 'pp.{N}52–{J}53', 1),
                FUZ + (1,), GOYA + (3,)]),
    dict(i=25, ficheiro=F04, pares=[('3 min', '3{N}min', 1), FUZ + (1,)]),
    dict(i=26, ficheiro=F05,
         pares=[('n.º 1760', 'n.º{N}1760', 1), ('n.º 0', 'n.º{N}0', 1), ('pp. 14–15', 'pp.{N}14–{J}15', 1),
                ('página 15', 'página{N}15', 1), FUZ + (1,), ('7 de agosto de 2023', '7{N}de agosto de{N}2023', 1),
                ('1956–2022', '1956–{J}2022', 1)]),
    dict(i=27, ficheiro='m8/licao-m8-f06/index.html', pares=[FUZ + (1,)]),
    dict(i=28, ficheiro=F08, pares=[('1921–1998', '1921–{J}1998', 2)]),
    dict(i=30, ficheiro='m8/licao-m8-f10/index.html',
         pares=[('5 a 7 minutos', '5 a 7{N}minutos', 4), ('30 s', '30{N}s', 1), ('90 segundos', '90{N}segundos', 4),
                ('30 segundos', '30{N}segundos', 3), FUZ + (1,), GOYA + (1,), ('3 de Maio', '3{N}de Maio', 2),
                ('M8-F03', 'M8-{J}F03', 2)]),
    dict(i=31, ficheiro='m8/licao-m8-f11/index.html', pares=[('século XX;', 'século{N}XX;', 2), ('século XX.', 'século{N}XX.', 2), ('século XX*', 'século{N}XX*', 1),
                ('século XX,', 'século{N}XX,', 1)],
         de={s: 'século XX' for s in ('século XX;', 'século XX.', 'século XX*', 'século XX,')},
         fora={'Poesia e conto do século XX</a>': (1, CASCA)}),
    dict(i=32, ficheiro='m8/licao-m8-f14/index.html',
         pares=[('n.º 0', 'n.º{N}0', 1), ('pp. 14–15', 'pp.{N}14–{J}15', 1),
                ('27 de setembro de 2013', '27{N}de setembro de{N}2013', 1)]),
    dict(i=33, ficheiro='m8/licao-m8-f16/index.html', pares=[('12.º ano', '12.º{N}ano', 1), ('página 1', 'página{N}1', 1)]),
    dict(i=34, ficheiro='m8/m8-george-tres-idades/index.html', pares=[('25 min', '25{N}min', 1)]),
    dict(i=35, ficheiro='m8/m8-poema-testemunha/index.html',
         pares=[('25 min', '25{N}min', 1), ('n.º 1760', 'n.º{N}1760', 2), ('versos 1 e 2', 'versos{N}1 e{N}2', 2),
                ('verso 1', 'verso{N}1', 1), FUZ + (1,)]),
    dict(i=36, ficheiro=MAPA,
         pares=[('90 minutos', '90{N}minutos', 2), ('30 %', '30{N}%', 2), ('3.º ano', '3.º{N}ano', 2),
                ('século XX', 'século{N}XX', 3), ('verso 1', 'verso{N}1', 1), FUZ + (2,), ('1923–2005', '1923–{J}2005', 1),
                ('1921–1998', '1921–{J}1998', 1), ('M8-F01', 'M8-{J}F01', 1), ('M8-F08', 'M8-{J}F08', 3),
                ('M8-F03', 'M8-{J}F03', 1)]),
    dict(i=37, ficheiro=OPINIAO, pares=[('século XVI', 'século{N}XVI', 1), ('ato III', 'ato{N}III', 1)]),
    dict(i=41, ficheiro='m8/pastelaria/index.html', pares=[('1923–2006', '1923–{J}2006', 1)]),
    dict(i=42, ficheiro=PORTEFOLIO,
         pares=[('90 minutos', '90{N}minutos', 1), ('40 %', '40{N}%', 1), ('3.º ano', '3.º{N}ano', 2),
                ('século XX', 'século{N}XX', 1)]),
    dict(i=48, ficheiro='m8/visita-caderno-de-campo/index.html', pares=[('3.º ano', '3.º{N}ano', 2)]),
    dict(i=49, ficheiro='tarefas/m8-u1/index.html', literais=[META],
         pares=[('10 min', '10{N}min', 1), ('60 minutos', '60{N}minutos', 1), ('90 min', '90{N}min', 1),
                ('10 minutos', '10{N}minutos', 1), ('n.º 0', 'n.º{N}0', 1), ('pp. 14–15', 'pp.{N}14–{J}15', 1),
                ('7 de agosto de 2023', '7{N}de agosto de{N}2023', 1)]),
    dict(i=50, ficheiro='tarefas/m8-u2/index.html', literais=[META],
         pares=[('10 min', '10{N}min', 1), ('60 minutos', '60{N}minutos', 1), ('90 min', '90{N}min', 1),
                ('10 minutos', '10{N}minutos', 1)]),
]

# Os painéis de projeção: só o da F11 muda (o enunciado do cartão 1, na lista e no seletor). Os achados 38 e 39 (painéis da F03 e
# da F10) e a terceira ocorrência do achado 40 só tinham ocorrências no material do relâmpago (MATERIAL), que não muda.
PAINEIS = {'m8/painel-m8-f11/index.html': 40}

# Sem cópias fora do módulo a mudar nem notas do docente geradas a mudar (as das lições geradas F13 a F16 não repetem os trechos mudados).
NOTAS = []

# A casca das lições fica para o molde, como do M1 ao M7: nenhuma troca. As lições com achado B.
CASCA_NO_MOLDE = sorted(x['ficheiro'] for x in ACHADOS_B if x['ficheiro'].startswith('m8/licao-'))

GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
CHAVES_TAREFA = (' "nao_partir": true,\n',
                 'Os números do molde da tarefa («90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) levam o espaço que não '
                 'quebra pelo gerador (scripts/tarefas_escolha.py), como do M1 ao M7.')
MOLDE = ('10 min', '90 min')
DADOS = [
    dict(ficheiro=f'docs/pedagogia/tarefas-escolha/m8-u{u}.json', achados=(i,), chaves=(f'\n "unidade": {u},\n',) + CHAVES_TAREFA,
         pares=[p for p in next(x for x in ACHADOS_B if x['i'] == i)['pares'] if p[0] not in MOLDE])
    for u, i in ((1, 49), (2, 50))
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


# Os pares da proposta que acabam a meio de uma palavra (a sigla da lição, antes do número): à direita não se exige a palavra inteira.
A_MEIO = set()


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
    raise SystemExit(f'{rel}: não há contexto que distinga «{pre[membros[0][0]:membros[0][1]]}»')


def local_b(pagina):
    def f(k, par, antigo):
        if antigo == par:
            return f'{pagina}: «{par}» que não se parte'
        contexto = antigo if len(antigo) <= 60 else antigo[:57].rstrip() + '…'
        return f'{pagina}: «{par}» que não se parte (com o contexto «{contexto}»)'
    return f


def nome(rel):
    """O nome curto da página no manifesto. Os painéis de projeção (m8/painel-m8-fxx com CARTOES) não são notas do docente: só as
    notas editoriais (as das lições geradas, sem CARTOES) levam «(notas do docente)» (a revisão do M5 viu esse erro)."""
    m = re.match(r'm8/(?:licao|painel)-(m8-f\d+)/', rel)
    if m:
        if '/painel-' not in rel:
            return m.group(1).upper()
        notas = 'CARTOES=' not in ler(rel)
        return m.group(1).upper() + (' (notas do docente)' if notas else ' (painel de projeção)')
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


# Os enunciados dos painéis do docente (m8/painel-m8-fxx) são os dos cartões da lição: o «p» (ou a «frase»), com ou sem os
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
    for licao in sorted(r for r in finais if r.startswith('m8/licao-')):
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
