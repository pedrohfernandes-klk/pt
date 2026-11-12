#!/usr/bin/env python3
"""12/11/2026: decisão 152 do docente, «cuidado em todas as lições», no Exame e nas páginas transversais do Português.

Constrói scripts/cuidado_exame_20261112.json, a camada literal cuidado_exame_20261112, com os achados CONFIRMADOS da varredura do
Exame e das páginas transversais (refeita a 9/11 e conferida a 11/11, só leitura, sobre o main 4bf4a053, em 139 ficheiros): dos 55
confirmados (1 A, 50 B e 4 C) entram 50: o achado A (uma tabela onde havia itens paralelos), os 4 casos do mesmo tipo (C) e 45 de
referências e números que se partiam (B). Ficam de fora, por decisão já tomada para todos os módulos, como do M1 ao M9, os achados B
dos diapositivos (57) e das três páginas «todos» (60, 61 e 62): essas páginas não mudam. Fica também de fora, para um pedido
próprio, o achado B da secção das provas (28, exame/provas/index.html), que sai inteira do molde do gerador das provas
(scripts/provas/gerar.py) e de prova.json e seccao.json, que esta camada não muda. Os 24 achados que a conferência recusou (1, 2,
7 a 25, 33, 77 e 78) não entram. As páginas exame/treinos/ não foram lidas pela varredura e ficam fora desta camada. A camada
aplica-se com scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/cuidado-exame-edits-20261112.json:

  python3 scripts/cuidado_exame_20261112.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_exame_20261112.json --manifesto tests/fixtures/cuidado-exame-edits-20261112.json \\
      --base-commit e4b0e4c3fd8d2e970278ce326f0ac417c01d72ea --nota "…"

Fica por cima da decisão 152 no M9 (cuidado_m9_20261112, no ramo do pedido #197, commit e4b0e4c3, com o main 89957690 já dentro),
com a qual só partilha as sessões do Exame (assets/exame/sessoes.json).

Segue o modelo da camada do M9 (scripts/cuidado_m9_20261112.py; o livro de regras é a docstring de scripts/cuidado_m5_20261108.py):
- A: as cinco fases da sessão e o tempo de cada uma, na vista «Programa e fontes» do Exame («Como cabe em 50 minutos?», que
  assets/exame/app.js monta), passam a tabela (achado 0), como a dos tempos da aula de tarefa do M5: class apoio-tabela, th
  scope=col no cabeçalho (Fase, Tempo), th scope=row na primeira coluna, td data-label e os role. A vista já tem uma tabela e a
  folha do Exame dá o estilo às duas: a página não carrega assets/pt-lessons/apoios-tabelas.css e a tabela, de duas colunas
  curtas, não empilha no telemóvel. A frase da soma fica num parágrafo a seguir.
- B: U+00A0 (espaço que não quebra) nos espaços que a proposta final prende, e U+2060 (junção de palavras) logo a seguir ao
  traço de intervalo («10–20 minutos», «pp. 1–3», «10.º–12.º ano»). A proposta dá cada par como a expressão inteira e o número
  de ocorrências que mudam: cada par conta-se com a palavra inteira, fora das cadeias maiores dos outros pares da página e fora
  dos sítios que não mudam, e a troca leva só os espaços que muda, com o mínimo de contexto que a distingue. Entram os pares «por
  analogia» que a conferência confirmou (referências de exame que o M5 não tinha: Prova, Grupo, item, linha, verso, nível, versão,
  pontos, MiB), que ficam marcados em ANALOGIA para poderem sair em bloco se o docente não quiser a extensão. Ficam de fora: os
  «alt» (e aria-label, href, title, content e data-titulo), o <title>, o texto dos desenhos (SVG), a «frase» dos cartões
  sublinhar, as «palavras» dos cartões frase e os «passos» dos cartões ordenar, as notas internas dos dados, como do M1 ao M9; o
  texto de apoio dos aquecimentos (<p class="pr">: as obras e o resumo que as acompanha); e, nas sessões do Exame, o texto das
  obras (a chave «text»), os rótulos dos trechos de vídeo (que assets/exame/app.js também põe no title do vídeo) e as perguntas
  antigas («warmup», que a página não mostra e que tests/test_exame_alignment.py compara com as lições), salvo as quatro opções da pergunta da s19 copiada da M9-F01, que mudam nas duas cópias (AJUSTES).
- C: nas provas em cartões, quatro enumerações da nossa leitura dos critérios passam a lista: os níveis de cada parâmetro do
  Grupo III da 2.ª fase (achado 3: a conferência ficou com a sublista em vez da tabela), os níveis de pontuação do item 7 das duas
  fases (achados 4 e 5) e os tipos de erro do Quadro 1 no Grupo III da 1.ª fase (achado 6). As palavras ficam todas, pela mesma
  ordem.
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois.

As provas em cartões (exame/provas/AAAA-Nf/grupo-x/, de scripts/provas/gerar.py e scripts/provas/dados/): só muda texto nosso. O
texto oficial (o texto e os itens da prova, as grelhas, os tópicos e as regras dos critérios, transcritos) não muda, nem com
espaços invisíveis. Cada ocorrência só muda se estiver num campo nosso de um cartão (o retorno; o enunciado, as opções e os pares
dos cartões que não são itens da prova; as ligações; o HTML dos cartões de leitura fora dos blocos oficiais), fora das citações
entre «» e num pedaço que não esteja, letra a letra, na transcrição conferida (tests/fixtures/prova-639-*.json), como
tests/provas_casos.py a lê. Ficam também como estavam os rótulos e os títulos dos cartões (pelos quais os testes e o motor
reconhecem os itens), as indicações de fonte (<p class="fonte">), os campos dos exercícios e a moldura que o gerador escreve (o
título, as migalhas, o menu, o rodapé, o fim da lição e as ligações da imagem com direitos). Cada par leva o número de
ocorrências que ficam nesse texto, nunca mais do que as que a conferência contou; o par que desse mais fica de fora, na dúvida.
Das 1667 ocorrências que a conferência contou nas seis provas (sem o par «p. 13» do achado 67), mudam 1280.

O texto visível fica igual, letra a letra, salvo a estrutura da tabela e das listas (os cabeçalhos «Fase» e «Tempo», a maiúscula
no início de cada linha, os parênteses, as vírgulas, os «;» e o «e» final que a tabela e as listas substituem, e «Conteúdo, 8
pontos:», que se desdobra em «Conteúdo:» e «8 pontos:») e os espaços invisíveis. «séc. XIII» fica abreviado, só com o espaço
preso (como no M1). O script calcula as trocas sobre a base (o ficheiro com esta camada desfeita pelo manifesto, quando ele já
existe): pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.

Páginas geradas: os aquecimentos do Exame (scripts/exame_aquecimentos.py) mudam nos bancos (docs/pedagogia/exame-aquecimentos/
sNN.json) e as provas em cartões (scripts/provas/gerar.py) mudam nos dados (scripts/provas/dados/AAAA-Nf/grupo-x.json); os dados
estão na mesma camada e as páginas regeneram-se sem diferenças (construir() confere-o, com os geradores). A entrada, as páginas
dos anos, o mapa, as obras e o laboratório são páginas estáticas; as vistas do Exame (exame/index.html) são montadas por
assets/exame/app.js a partir de assets/exame/sessoes.json, e o laboratório e o dossiê por assets/exame/laboratorio.js e
dossier.js: mudam aí.

As camadas de baixo que mexem nos mesmos ficheiros desfazem primeiro esta: scripts/verificar_camadas.py (LAYERS[0]),
tests/auditoria_20261028.py, scripts/desligar_sala.py e os geradores do desenho comum dos índices
(scripts/cartaz_indices_148_20261106.py), dos acertos dos índices (scripts/indices_acertos_20261107.py) e dos créditos atrás de
um «i» (scripts/creditos_i_pt1_20261107.py). Esta camada não toca nas tarefas das unidades (a leitura histórica de
scripts/tarefas_claras_historico.py fica como está).
"""
import html
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_exame_20261112.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-exame-edits-20261112.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
CONTAR = None
ACHADO = ('12/11/2026: decisão 152 (cuidado em todas as lições), varredura do Exame e das páginas transversais, achado {i} ({cat}). '
          '{texto}')
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como do M1 ao M9).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e ao hífen da '
          'sigla).'),
    'C': 'Caso do mesmo tipo.',
}


def j(s):
    """As formas da proposta escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return s.replace('{N}', NBSP).replace('{J}', WJ)


APP = 'assets/exame/app.js'
SESSOES = 'assets/exame/sessoes.json'


def tabela(colunas, linhas):
    """A tabela de apoio, igual às do M1 ao M9: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label com
    o nome da coluna, e os role. Aqui vai dentro de uma cadeia de JavaScript entre plicas: as aspas ficam como estão."""
    cab = ''.join(f'<th scope="col" role="columnheader">{c}</th>' for c in colunas)
    corpo = ''
    for linha in linhas:
        corpo += '<tr role="row"><th scope="row" role="rowheader">' + linha[0] + '</th>'
        for k, v in enumerate(linha[1:], 1):
            corpo += f'<td role="cell" data-label="{colunas[k]}">{v}</td>'
        corpo += '</tr>'
    return (f'<table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row">{cab}</tr></thead>'
            f'<tbody role="rowgroup">{corpo}</tbody></table>')


# Achado 0 (A): as cinco fases da sessão e o tempo de cada uma, na vista «Programa e fontes» do Exame («Como cabe em 50 minutos?»,
# que assets/exame/app.js monta), como a tabela dos tempos da aula de tarefa do M5. Os tempos já vão com o espaço que não quebra
# e com a junção a seguir ao traço de intervalo (a conferência contou esses pares do achado B 74 nas células).
FASES_ANTES = ('<p>Aquecer (10 min), ler e planear (8 min), escrever (10–20 min), corrigir (7–17 min) e fechar (5 min). A soma é sempre '
               '50. O relógio não avança fases nem revela correções automaticamente.</p>')
FASES_LINHAS = [['Aquecer', '10{N}min'], ['Ler e planear', '8{N}min'], ['Escrever', '10–{J}20{N}min'], ['Corrigir', '7–{J}17{N}min'],
                ['Fechar', '5{N}min']]
FASES_DEPOIS = '<p>A soma é sempre 50. O relógio não avança fases nem revela correções automaticamente.</p>'
FASES_REFEITAS = {'10 min': 1, '8 min': 1, '10–20 min': 1, '7–17 min': 1, '5 min': 1}


# Achados 3, 4, 5 e 6 (C): nas provas em cartões, quatro enumerações da nossa leitura dos critérios passam a lista (um nível, ou um
# tipo de erro, por linha). O trecho e a proposta são os da conferência, na forma da página (dentro do JavaScript dos cartões, com
# «<\\/»); nos dados (scripts/provas/dados), o mesmo com «</». O texto novo fica com espaços normais.
PROVAS_C = [
    dict(i=3, pagina='exame/provas/2026-2f/grupo-iii/index.html',
         cartao='cartão «Escreve no caderno» do Grupo III, «O que separa 10, 8 e 5 pontos em cada parâmetro»',
         nota=('Cada parâmetro abre uma sublista com um nível por linha, no modelo «10:» dos cartões do Grupo I; as pala'
              'vras ficam todas, pela mesma ordem; os «;» passam a ponto final e entram os dois pontos a seguir ao núme'
              'ro. A conferência ficou com a sublista em vez da tabela do varredor. É a nossa leitura dos critérios, nã'
              'o a grelha oficial, que fica como está.'),
         antigo=('<ul class=\\"niveis\\"><li><b>Parâmetro A:<\\/b> 10 com o ponto de vista explícito, dois argumentos distint'
                'os, um exemplo em cada um, juízo de valor e conclusão adequada; 8 se só um argumento tem exemplo, ou se '
                'falham um ou dois dos outros aspetos; 5 com um só argumento e o seu exemplo, ou com um só exemplo e outr'
                'as falhas.<\\/li><li><b>Parâmetro B:<\\/b> 10 sem desvios, com argumentos e exemplos pertinentes, ideias q'
                'ue progridem e registo adequado; 8 com falhas pontuais na eficácia argumentativa, ou com desvios pouco s'
                'ignificativos; 5 com desvios pouco significativos e falhas pontuais, ou com falhas significativas.<\\/li>'
                '<li><b>Parâmetro C:<\\/b> 10 com partes proporcionadas, parágrafos marcados, conectores, retomas sem repe'
                'tições e pessoa e tempo coerentes; 8 com falhas pontuais em um ou dois destes aspetos; 5 com falhas pont'
                'uais em três ou mais, ou com falhas significativas.<\\/li><\\/ul>'),
         novo=('<ul class=\\"niveis\\"><li><b>Parâmetro A:<\\/b><ul><li><b>10:<\\/b> com o ponto de vista explícito, dois ar'
              'gumentos distintos, um exemplo em cada um, juízo de valor e conclusão adequada.<\\/li><li><b>8:<\\/b> se s'
              'ó um argumento tem exemplo, ou se falham um ou dois dos outros aspetos.<\\/li><li><b>5:<\\/b> com um só ar'
              'gumento e o seu exemplo, ou com um só exemplo e outras falhas.<\\/li><\\/ul><\\/li><li><b>Parâmetro B:<\\/b>'
              '<ul><li><b>10:<\\/b> sem desvios, com argumentos e exemplos pertinentes, ideias que progridem e registo a'
              'dequado.<\\/li><li><b>8:<\\/b> com falhas pontuais na eficácia argumentativa, ou com desvios pouco signifi'
              'cativos.<\\/li><li><b>5:<\\/b> com desvios pouco significativos e falhas pontuais, ou com falhas significa'
              'tivas.<\\/li><\\/ul><\\/li><li><b>Parâmetro C:<\\/b><ul><li><b>10:<\\/b> com partes proporcionadas, parágrafo'
              's marcados, conectores, retomas sem repetições e pessoa e tempo coerentes.<\\/li><li><b>8:<\\/b> com falha'
              's pontuais em um ou dois destes aspetos.<\\/li><li><b>5:<\\/b> com falhas pontuais em três ou mais, ou com'
              ' falhas significativas.<\\/li><\\/ul><\\/li><\\/ul>')),
    dict(i=4, pagina='exame/provas/2026-1f/grupo-i/index.html',
         cartao='cartão «Escreve no caderno» do item 7, «O que separa as pontuações»',
         nota=('Os níveis de pontuação, que vinham seguidos na mesma linha e separados por «;», passam a sublista, um po'
              'r linha, como nos itens 1, 2, 4 e 5 do mesmo grupo; «Conteúdo, 8 pontos:» desdobra-se em «Conteúdo:» e «'
              '8 pontos:» (e o mesmo na estruturação do discurso); as palavras ficam todas, pela mesma ordem.'),
         antigo=('<ul class=\\"niveis\\"><li><b>Conteúdo, 8 pontos:<\\/b> duas situações ou dois momentos de denúncia, os doi'
                's explicitados adequadamente; <b>6:<\\/b> um adequado e o outro com pequenas imprecisões ou omissões; <b>'
                '4:<\\/b> só um adequado, ou os dois com imprecisões.<\\/li><li><b>Estruturação do discurso, 3 pontos:<\\/b>'
                ' introdução, desenvolvimento e conclusão proporcionados e bem ligados; <b>2:<\\/b> com desequilíbrios de '
                'proporção ou falhas de coesão que não comprometem o conjunto.<\\/li><li><b>Correção linguística, 2 pontos'
                ':<\\/b> no máximo um erro do tipo A e nenhum do tipo B.<\\/li><\\/ul>'),
         novo=('<ul class=\\"niveis\\"><li><b>Conteúdo:<\\/b><ul><li><b>8\xa0pontos:<\\/b> duas situações ou dois momentos de d'
              'enúncia, os dois explicitados adequadamente.<\\/li><li><b>6:<\\/b> um adequado e o outro com pequenas impr'
              'ecisões ou omissões.<\\/li><li><b>4:<\\/b> só um adequado, ou os dois com imprecisões.<\\/li><\\/ul><\\/li><l'
              'i><b>Estruturação do discurso:<\\/b><ul><li><b>3\xa0pontos:<\\/b> introdução, desenvolvimento e conclusão pro'
              'porcionados e bem ligados.<\\/li><li><b>2:<\\/b> com desequilíbrios de proporção ou falhas de coesão que n'
              'ão comprometem o conjunto.<\\/li><\\/ul><\\/li><li><b>Correção linguística, 2\xa0pontos:<\\/b> no máximo um err'
              'o do tipo A e nenhum do tipo B.<\\/li><\\/ul>')),
    dict(i=5, pagina='exame/provas/2026-2f/grupo-i/index.html',
         cartao='cartão «Escreve no caderno» do item 7, «O que separa as pontuações»',
         nota=('O mesmo caso do achado 4, na 2.ª fase: os níveis de pontuação passam a sublista, um por linha; as palavr'
              'as ficam todas, pela mesma ordem.'),
         antigo=('<ul class=\\"niveis\\"><li><b>Conteúdo, 8 pontos:<\\/b> duas reflexões sobre a existência humana, as duas e'
                'xplicitadas adequadamente; <b>6:<\\/b> uma adequada e a outra com pequenas imprecisões ou omissões; <b>4:'
                '<\\/b> só uma adequada, ou as duas com imprecisões.<\\/li><li><b>Estruturação do discurso, 3 pontos:<\\/b> '
                'introdução, desenvolvimento e conclusão proporcionados e bem ligados; <b>2:<\\/b> com desequilíbrios de p'
                'roporção ou falhas de coesão que não comprometem o conjunto.<\\/li><li><b>Correção linguística, 2 pontos:'
                '<\\/b> no máximo um erro do tipo A e nenhum do tipo B.<\\/li><\\/ul>'),
         novo=('<ul class=\\"niveis\\"><li><b>Conteúdo:<\\/b><ul><li><b>8\xa0pontos:<\\/b> duas reflexões sobre a existência hu'
              'mana, as duas explicitadas adequadamente.<\\/li><li><b>6:<\\/b> uma adequada e a outra com pequenas imprec'
              'isões ou omissões.<\\/li><li><b>4:<\\/b> só uma adequada, ou as duas com imprecisões.<\\/li><\\/ul><\\/li><li'
              '><b>Estruturação do discurso:<\\/b><ul><li><b>3\xa0pontos:<\\/b> introdução, desenvolvimento e conclusão prop'
              'orcionados e bem ligados.<\\/li><li><b>2:<\\/b> com desequilíbrios de proporção ou falhas de coesão que nã'
              'o comprometem o conjunto.<\\/li><\\/ul><\\/li><li><b>Correção linguística, 2\xa0pontos:<\\/b> no máximo um erro'
              ' do tipo A e nenhum do tipo B.<\\/li><\\/ul>')),
    dict(i=6, pagina='exame/provas/2026-1f/grupo-iii/index.html',
         cartao='cartão «Escreve no caderno» do Grupo III, «A tabela da correção linguística, lida por linhas»: os tipos de erro',
         nota=('Os seis tipos de erro, em dois grupos, passam a duas listas («Tipo A» e «Tipo B», com maiúscula no iníci'
              'o da linha), como no Quadro 1 dos cartões do Grupo I; saem as vírgulas e os «;» que a lista substitui. É'
              ' a nossa leitura; o Quadro 1 oficial fica como está.'),
         antigo=('<p>Os tipos de erro (Quadro 1): <b>tipo A<\\/b>, erro inequívoco de pontuação; erro de ortografia (inclui'
                'ndo erro de acentuação, erro de translineação e uso indevido de letra minúscula ou de letra maiúscula); '
                'erro de morfologia; incumprimento das regras de citação de texto ou de referência a título de uma obra; '
                '<b>tipo B<\\/b>, erro de sintaxe; impropriedade lexical.<\\/p>'),
         novo=('<p>Os tipos de erro (Quadro 1):<\\/p><p><b>Tipo A<\\/b><\\/p><ul><li>erro inequívoco de pontuação<\\/li><li>'
              'erro de ortografia (incluindo erro de acentuação, erro de translineação e uso indevido de letra minúscul'
              'a ou de letra maiúscula)<\\/li><li>erro de morfologia<\\/li><li>incumprimento das regras de citação de tex'
              'to ou de referência a título de uma obra<\\/li><\\/ul><p><b>Tipo B<\\/b><\\/p><ul><li>erro de sintaxe<\\/li><'
              'li>impropriedade lexical<\\/li><\\/ul>')),
]

def dados_da_prova(pagina):
    """exame/provas/AAAA-Nf/grupo-x/index.html > scripts/provas/dados/AAAA-Nf/grupo-x.json"""
    return re.sub(r'^exame/provas/(.+)/index\.html$', r'scripts/provas/dados/\1.json', pagina)


def achados_ac():
    """Os achados A e C confirmados que entram (trecho atual e proposta final da conferência, na forma da fonte)."""
    return [
        dict(i=0, cat='A', ficheiro=APP, cartao='vista «Programa e fontes», «Como cabe em 50 minutos?»: as fases da sessão e os tempos',
             nota=('As cinco fases no cabeçalho de linha, com maiúscula no início, e o tempo de cada uma na segunda coluna; caem os '
                   'parênteses, as vírgulas e o «e» final, que a tabela substitui; a frase da soma fica num parágrafo a seguir. A '
                   'vista já tem uma tabela e a folha do Exame (assets/exame/exame.css) dá-lhe o estilo: não é preciso carregar a '
                   'folha das tabelas de apoio. Os tempos já levam o espaço que não quebra e a junção a seguir ao traço de intervalo.'),
             antigo=FASES_ANTES, novo=j(tabela(['Fase', 'Tempo'], FASES_LINHAS)) + FASES_DEPOIS),
    ] + [dict(i=x['i'], cat='C', ficheiro=rel, cartao=x['cartao'],
              nota=x['nota'] + (' Nos dados do gerador das provas (scripts/provas/gerar.py), que passam iguais para a página.' if k else ''),
              antigo=x['antigo'].replace('<\\/', '</') if k else x['antigo'], novo=x['novo'].replace('<\\/', '</') if k else x['novo'])
         for x in PROVAS_C for k, rel in enumerate((x['pagina'], dados_da_prova(x['pagina'])))]


# Os achados B que entram: cada par é (a cadeia a procurar, a mesma cadeia com {N} e {J}, o número de ocorrências que mudam). Os
# pares e os números são os da conferência (bordo/cidadania-v3/cuidado-152/exame-confirmados.json), conferidos no ficheiro real;
# onde o número é outro, a razão está em AJUSTES.
ACHADOS_B = [
    dict(i=26, ficheiro='exame/laboratorio/index.html',
         pares=[('Prova 639', 'Prova{N}639', 1), ('1.ª fase', '1.ª{N}fase', 1), ('pp. 1–3', 'pp.{N}1–{J}3', 1)]),
    dict(i=27, ficheiro='mapa/index.html',
         pares=[('século XIX', 'século{N}XIX', 2), ('45 minutos', '45{N}minutos', 1), ('século XX', 'século{N}XX', 2),
                ('1.º ano', '1.º{N}ano', 1), ('2.º ano', '2.º{N}ano', 1), ('3.º ano', '3.º{N}ano', 1)]),
    dict(i=29, ficheiro='exame/aquecimentos/s14/index.html',
         pares=[('1.ª publicação', '1.ª{N}publicação', 1), ('2.ª estrofe', '2.ª{N}estrofe', 2), ('n.º 1', 'n.º{N}1', 1)]),
    dict(i=30, ficheiro='exame/aquecimentos/s10/index.html',
         pares=[('verso 12', 'verso{N}12', 1), ('verso 6', 'verso{N}6', 1), ('verso 3', 'verso{N}3', 1),
                ('v. 14', 'v.{N}14', 1), ('v. 6', 'v.{N}6', 1), ('v. 1', 'v.{N}1', 1)]),
    dict(i=31, ficheiro='exame/aquecimentos/s12/index.html',
         pares=[('1.ª publicação', '1.ª{N}publicação', 2), ('2.ª estrofe', '2.ª{N}estrofe', 2),
                ('1.ª estrofe', '1.ª{N}estrofe', 1), ('3.ª estrofe', '3.ª{N}estrofe', 1), ('verso 4', 'verso{N}4', 1),
                ('verso 2', 'verso{N}2', 1), ('v. 4', 'v.{N}4', 1), ('v. 6', 'v.{N}6', 1), ('n.º 36', 'n.º{N}36', 1),
                ('n.º 38', 'n.º{N}38', 1)]),
    dict(i=32, ficheiro='exame/aquecimentos/s15/index.html',
         pares=[('vv. 1 a 4', 'vv.{N}1 a{N}4', 1)]),
    dict(i=34, ficheiro='exame/aquecimentos/s19/index.html',
         pares=[('capítulo XXI', 'capítulo{N}XXI', 2), ('século XVIII', 'século{N}XVIII', 3),
                ('século XVII', 'século{N}XVII', 1), ('século XVI', 'século{N}XVI', 2), ('D. João V', 'D.{N}João{N}V', 9),
                ('século XX', 'século{N}XX', 1)]),
    dict(i=35, ficheiro='exame/aquecimentos/s13/index.html',
         pares=[('v. 21', 'v.{N}21', 1)]),
    dict(i=36, ficheiro='exame/aquecimentos/s09/index.html',
         pares=[('cap. I', 'cap.{N}I', 1)]),
    dict(i=37, ficheiro='exame/aquecimentos/s06/index.html',
         pares=[('caps. I e II', 'caps.{N}I e{N}II', 1), ('cap. V', 'cap.{N}V', 2)]),
    dict(i=38, ficheiro='exame/aquecimentos/s02/index.html',
         pares=[('cap. CXLVIII', 'cap.{N}CXLVIII', 1), ('D. João I', 'D.{N}João{N}I', 2), ('cap. CXVI', 'cap.{N}CXVI', 1),
                ('cap. XII', 'cap.{N}XII', 2), ('cap. 115', 'cap.{N}115', 1), ('cap. 148', 'cap.{N}148', 1),
                ('cap. 11', 'cap.{N}11', 1)]),
    dict(i=39, ficheiro='exame/aquecimentos/s04/index.html',
         pares=[('soneto XIII', 'soneto{N}XIII', 1)]),
    dict(i=40, ficheiro='exame/aquecimentos/s05/index.html',
         pares=[('Canto VIII, 96 a 99', 'Canto{N}VIII, 96 a{N}99', 2), ('estância 99', 'estância{N}99', 1),
                ('canto VIII', 'canto{N}VIII', 3), ('Canto I', 'Canto{N}I', 2), ('canto I', 'canto{N}I', 4)]),
    dict(i=41, ficheiro='exame/aquecimentos/s01/index.html',
         pares=[('D. Dinis, cantiga 544', 'D.{N}Dinis, cantiga{N}544', 1), ('cantiga 1308', 'cantiga{N}1308', 1),
                ('cantiga 1520', 'cantiga{N}1520', 1), ('séc. XIII', 'séc.{N}XIII', 1), ('estrofe 3', 'estrofe{N}3', 2),
                ('estrofe 2', 'estrofe{N}2', 5), ('2.º verso', '2.º{N}verso', 2), ('estrofe 1', 'estrofe{N}1', 3)]),
    dict(i=42, ficheiro='exame/aquecimentos/s07/index.html',
         pares=[('ato II, cenas XIV e XV', 'ato{N}II, cenas{N}XIV e{N}XV', 1),
                ('ato I, cenas XI e XII', 'ato{N}I, cenas{N}XI e{N}XII', 1), ('ato III, cena XI', 'ato{N}III, cena{N}XI', 1),
                ('ato II, cena I', 'ato{N}II, cena{N}I', 1), ('D. João', 'D.{N}João', 3), ('ato III', 'ato{N}III', 1)]),
    dict(i=43, ficheiro='exame/aquecimentos/s03/index.html',
         pares=[('vv. 10 a 13 e 23 a 25', 'vv.{N}10 a{N}13 e{N}23 a{N}25', 1),
                ('vv. 63 a 65 e 74 a 76', 'vv.{N}63 a{N}65 e{N}74 a{N}76', 1)]),
    dict(i=44, ficheiro='obras/mensagem/index.html',
         pares=[('1 de dezembro de 1934', '1{N}de dezembro de{N}1934', 1), ('5 min', '5{N}min', 1)]),
    dict(i=45, ficheiro='obras/antero/index.html',
         pares=[('3 min', '3{N}min', 1), ('n.º 20142', 'n.º{N}20142', 1)]),
    dict(i=46, ficheiro='obras/cronica/index.html',
         pares=[('capítulos XII, CXVI e CXLVIII', 'capítulos{N}XII, CXVI e{N}CXLVIII', 1),
                ('10.º ano, aula 10', '10.º{N}ano, aula{N}10', 1), ('Capítulo XI', 'Capítulo{N}XI', 1),
                ('capítulo XI', 'capítulo{N}XI', 1), ('século XIV', 'século{N}XIV', 1), ('D. João I', 'D.{N}João{N}I', 3),
                ('29 min', '29{N}min', 1), ('27 min', '27{N}min', 1), ('5 min', '5{N}min', 1)]),
    dict(i=47, ficheiro='obras/lirica-camoes/index.html',
         pares=[('54 min', '54{N}min', 1), ('1 min', '1{N}min', 1)]),
    dict(i=48, ficheiro='obras/memorial/index.html',
         pares=[('35 min', '35{N}min', 1), ('7 min', '7{N}min', 1), ('5 min', '5{N}min', 1)]),
    dict(i=49, ficheiro='obras/index.html',
         pares=[('D. João I', 'D.{N}João{N}I', 1), ('D. Dinis', 'D.{N}Dinis', 1)]),
    dict(i=50, ficheiro='obras/cesario/index.html',
         pares=[('38 min', '38{N}min', 1), ('31 min', '31{N}min', 1), ('3 min', '3{N}min', 1)]),
    dict(i=51, ficheiro='obras/ines/index.html',
         pares=[('11 min', '11{N}min', 1), ('51 min', '51{N}min', 1), ('32 min', '32{N}min', 1)]),
    dict(i=52, ficheiro='obras/frei-luis/index.html',
         pares=[('Ato I, cenas I e II', 'Ato{N}I, cenas{N}I e{N}II', 1),
                ('ato I, cenas I e II', 'ato{N}I, cenas{N}I e{N}II', 1), ('50 min', '50{N}min', 1), ('3 min', '3{N}min', 1)]),
    dict(i=53, ficheiro='obras/sermao/index.html',
         pares=[('capítulos I, II, IV, V e VI', 'capítulos{N}I, II, IV, V e{N}VI', 1),
                ('13 de junho de 1654', '13{N}de junho de{N}1654', 1), ('capítulos IV e V', 'capítulos{N}IV e{N}V', 1),
                ('Capítulo I', 'Capítulo{N}I', 1), ('capítulo I', 'capítulo{N}I', 3), ('48 min', '48{N}min', 1)]),
    dict(i=54, ficheiro='obras/cantigas/index.html',
         pares=[('D. Dinis', 'D.{N}Dinis', 2), ('29 min', '29{N}min', 1), ('4 min', '4{N}min', 1)]),
    dict(i=55, ficheiro='obras/amor-perdicao/index.html',
         pares=[('Capítulo IV', 'Capítulo{N}IV', 1), ('capítulo IV', 'capítulo{N}IV', 1), ('16 minutos', '16{N}minutos', 1),
                ('5 h 11 min', '5{N}h 11{N}min', 1), ('48 min', '48{N}min', 1), ('5 min', '5{N}min', 1),
                ('6 min', '6{N}min', 1), ('n.º 16425', 'n.º{N}16425', 1)]),
    dict(i=56, ficheiro='obras/maias/index.html',
         pares=[('Capítulo VI', 'Capítulo{N}VI', 1), ('capítulo VI', 'capítulo{N}VI', 1), ('Capítulo I', 'Capítulo{N}I', 1),
                ('1 h 11 min', '1{N}h 11{N}min', 1), ('capítulo I', 'capítulo{N}I', 2), ('49 min', '49{N}min', 1),
                ('6 min', '6{N}min', 1), ('n.º 40409', 'n.º{N}40409', 1)]),
    dict(i=58, ficheiro='obras/lusiadas/index.html',
         pares=[('Canto I, estâncias 100 a 106', 'Canto{N}I, estâncias{N}100 a{N}106', 2),
                ('Canto IV, estâncias 94 a 104', 'Canto{N}IV, estâncias{N}94 a{N}104', 2),
                ('Canto I, estâncias 1 a 18', 'Canto{N}I, estâncias{N}1 a{N}18', 2), ('estância 106', 'estância{N}106', 1),
                ('estância 18', 'estância{N}18', 1), ('Canto I', 'Canto{N}I', 3), ('12 min', '12{N}min', 1),
                ('41 min', '41{N}min', 1), ('17 min', '17{N}min', 1), ('4 min', '4{N}min', 2), ('6 min', '6{N}min', 1),
                ('3 min', '3{N}min', 1), ('n.º 3333', 'n.º{N}3333', 1)]),
    dict(i=59, ficheiro='obras/pessoa/index.html',
         pares=[('19 min', '19{N}min', 1), ('10 min', '10{N}min', 1), ('2 min', '2{N}min', 2), ('6 min', '6{N}min', 1),
                ('8 min', '8{N}min', 1)]),
    dict(i=63, ficheiro='1/index.html',
         pares=[('1.º ano', '1.º{N}ano', 2)]),
    dict(i=64, ficheiro='3/index.html',
         pares=[('século XX', 'século{N}XX', 2), ('3.º ano', '3.º{N}ano', 2)]),
    dict(i=65, ficheiro='2/index.html',
         pares=[('século XIX', 'século{N}XIX', 1), ('2.º ano', '2.º{N}ano', 2)]),
    dict(i=66, ficheiro='exame/provas/2026-1f/grupo-ii/index.html',
         pares=[('Prova 639, 1.ª fase, 2026, versão 2', 'Prova{N}639, 1.ª{N}fase, 2026, versão{N}2', 2),
                ('28 de setembro de 2025, p. 22', '28{N}de setembro de{N}2025, p.{N}22', 2),
                ('Prova 639, 1.ª fase', 'Prova{N}639, 1.ª{N}fase', 1), ('versão 2, Grupo II', 'versão{N}2, Grupo{N}II', 1),
                ('itens 1, 2, 6 e 7', 'itens{N}1, 2, 6 e{N}7', 1), ('itens 3, 4 e 5', 'itens{N}3, 4 e{N}5', 1),
                ('linhas 13 e 14', 'linhas{N}13 e{N}14', 1), ('linhas 35 a 40', 'linhas{N}35 a{N}40', 2),
                ('Linhas 10 a 22', 'Linhas{N}10 a{N}22', 1), ('Linhas 23 a 34', 'Linhas{N}23 a{N}34', 1),
                ('linhas 30 a 34', 'linhas{N}30 a{N}34', 1), ('linhas 30 e 31', 'linhas{N}30 e{N}31', 3),
                ('linhas 10 e 22', 'linhas{N}10 e{N}22', 1), ('linhas 10 a 22', 'linhas{N}10 a{N}22', 1),
                ('Linhas 15 a 29', 'Linhas{N}15 a{N}29', 1), ('linhas 15 a 29', 'linhas{N}15 a{N}29', 1),
                ('Linhas 30 e 31', 'Linhas{N}30 e{N}31', 1), ('Linhas 31 a 34', 'Linhas{N}31 a{N}34', 1),
                ('Linhas 35 a 47', 'Linhas{N}35 a{N}47', 1), ('linhas 41 e 42', 'linhas{N}41 e{N}42', 1),
                ('linhas 45 a 47', 'linhas{N}45 a{N}47', 1), ('linhas 35 a 47', 'linhas{N}35 a{N}47', 2),
                ('linhas 41 a 43', 'linhas{N}41 a{N}43', 1), ('linhas 44 a 47', 'linhas{N}44 a{N}47', 1),
                ('linhas 38 a 40', 'linhas{N}38 a{N}40', 1), ('Linhas 41 e 42', 'Linhas{N}41 e{N}42', 1),
                ('linhas 46 e 47', 'linhas{N}46 e{N}47', 2), ('Itens 5, 6 e 7', 'Itens{N}5, 6 e{N}7', 1),
                ('itens 5, 6 e 7', 'itens{N}5, 6 e{N}7', 1), ('linhas 15 a 22', 'linhas{N}15 a{N}22', 1),
                ('linhas 38 e 39', 'linhas{N}38 e{N}39', 2), ('linhas 35 e 36', 'linhas{N}35 e{N}36', 1),
                ('linhas 6 a 14', 'linhas{N}6 a{N}14', 1), ('Linhas 6 a 22', 'Linhas{N}6 a{N}22', 1),
                ('linhas 6 a 22', 'linhas{N}6 a{N}22', 1), ('Linhas 1 a 9', 'Linhas{N}1 a{N}9', 1),
                ('linhas 6 a 8', 'linhas{N}6 a{N}8', 2), ('linhas 2 e 3', 'linhas{N}2 e{N}3', 2),
                ('linhas 4 e 5', 'linhas{N}4 e{N}5', 3), ('linhas 3 e 4', 'linhas{N}3 e{N}4', 2),
                ('linhas 7 e 8', 'linhas{N}7 e{N}8', 2), ('Linhas 7 e 8', 'Linhas{N}7 e{N}8', 1),
                ('itens 3 e 6', 'itens{N}3 e{N}6', 1), ('120 minutos', '120{N}minutos', 1),
                ('itens 1 a 4', 'itens{N}1 a{N}4', 1), ('itens 6 e 7', 'itens{N}6 e{N}7', 1),
                ('Grupo III', 'Grupo{N}III', 1), ('13 pontos', '13{N}pontos', 3), ('52 pontos', '52{N}pontos', 1),
                ('2.ª fases', '2.ª{N}fases', 1), ('Sessão 22', 'Sessão{N}22', 1), ('Sessão 21', 'Sessão{N}21', 1),
                ('Grupo II', 'Grupo{N}II', 5), ('versão 2', 'versão{N}2', 2), ('linha 14', 'linha{N}14', 2),
                ('linha 10', 'linha{N}10', 3), ('linha 15', 'linha{N}15', 4), ('linha 17', 'linha{N}17', 3),
                ('linha 12', 'linha{N}12', 2), ('linha 19', 'linha{N}19', 2), ('linha 31', 'linha{N}31', 1),
                ('linha 44', 'linha{N}44', 2), ('linha 37', 'linha{N}37', 2), ('linha 43', 'linha{N}43', 1),
                ('linha 46', 'linha{N}46', 2), ('linha 36', 'linha{N}36', 3), ('linha 38', 'linha{N}38', 2),
                ('linha 21', 'linha{N}21', 2), ('linha 20', 'linha{N}20', 4), ('linha 23', 'linha{N}23', 2),
                ('linha 28', 'linha{N}28', 1), ('linha 26', 'linha{N}26', 1), ('linha 25', 'linha{N}25', 1),
                ('Grupo I', 'Grupo{N}I', 2), ('linha 1', 'linha{N}1', 5), ('linha 9', 'linha{N}9', 2),
                ('linha 5', 'linha{N}5', 2), ('linha 6', 'linha{N}6', 3), ('linha 3', 'linha{N}3', 3),
                ('linha 7', 'linha{N}7', 2), ('Linha 6', 'Linha{N}6', 1), ('item 1', 'item{N}1', 1),
                ('Item 1', 'Item{N}1', 1), ('item 2', 'item{N}2', 2), ('M6-F09', 'M6-{J}F09', 2), ('Item 2', 'Item{N}2', 1),
                ('Item 3', 'Item{N}3', 1), ('M4-F25', 'M4-{J}F25', 2), ('Item 4', 'Item{N}4', 1), ('M4-F15', 'M4-{J}F15', 2),
                ('item 5', 'item{N}5', 2), ('Item 5', 'Item{N}5', 1), ('item 6', 'item{N}6', 3), ('Item 6', 'Item{N}6', 1),
                ('item 7', 'item{N}7', 3), ('M5-F07', 'M5-{J}F07', 2), ('Item 7', 'Item{N}7', 1), ('M6-F07', 'M6-{J}F07', 1),
                ('p. 13', 'p.{N}13', 1), ('1 (B)', '1{N}(B)', 1), ('2 (C)', '2{N}(C)', 1), ('3 (A)', '3{N}(A)', 1),
                ('4 (D)', '4{N}(D)', 1), ('5 (B)', '5{N}(B)', 1), ('6 (C)', '6{N}(C)', 1), ('7 (D)', '7{N}(D)', 1),
                ('p. 1', 'p.{N}1', 1)]),
    dict(i=67, ficheiro='exame/provas/2026-1f/grupo-iii/index.html',
         pares=[('Prova 639, 1.ª fase, 2026, versão 2', 'Prova{N}639, 1.ª{N}fase, 2026, versão{N}2', 2),
                ('Prova 639, 1.ª fase', 'Prova{N}639, 1.ª{N}fase', 2), ('200 a 350 palavras', '200{N}a{N}350{N}palavras', 5),
                ('Quadro 1, p. 2', 'Quadro{N}1, p.{N}2', 1), ('353 palavras', '353{N}palavras', 2),
                ('150 palavras', '150{N}palavras', 3), ('220 palavras', '220{N}palavras', 1),
                ('290 palavras', '290{N}palavras', 1), ('210 palavras', '210{N}palavras', 1),
                ('350 palavras', '350{N}palavras', 1), ('286 palavras', '286{N}palavras', 1),
                ('120 minutos', '120{N}minutos', 1), ('70 palavras', '70{N}palavras', 1),
                ('20 palavras', '20{N}palavras', 2), ('50 palavras', '50{N}palavras', 1),
                ('40 palavras', '40{N}palavras', 1), ('80 palavras', '80{N}palavras', 2),
                ('pp. 14 a 16', 'pp.{N}14 a{N}16', 1), ('3 palavras', '3{N}palavras', 1), ('5 palavras', '5{N}palavras', 1),
                ('Grupo III', 'Grupo{N}III', 13), ('44 pontos', '44{N}pontos', 3), ('30 pontos', '30{N}pontos', 1),
                ('Sessão 25', 'Sessão{N}25', 2), ('10 pontos', '10{N}pontos', 3), ('14 pontos', '14{N}pontos', 2),
                ('11 pontos', '11{N}pontos', 1), ('pp. 1 a 3', 'pp.{N}1 a{N}3', 2), ('2.ª fases', '2.ª{N}fases', 1),
                ('Sessão 24', 'Sessão{N}24', 1), ('Grupo II', 'Grupo{N}II', 1), ('versão 2', 'versão{N}2', 1),
                ('5 pontos', '5{N}pontos', 4), ('3 pontos', '3{N}pontos', 3), ('8 pontos', '8{N}pontos', 4),
                ('Quadro 1', 'Quadro{N}1', 2), ('2.ª fase', '2.ª{N}fase', 1), ('1.ª fase', '1.ª{N}fase', 1),
                ('nível 3', 'nível{N}3', 3), ('nível 4', 'nível{N}4', 8), ('nível 2', 'nível{N}2', 2),
                ('M4-F15', 'M4-{J}F15', 2), ('tipo A', 'tipo{N}A', 16), ('M5-F07', 'M5-{J}F07', 2),
                ('tipo B', 'tipo{N}B', 16), ('M2-F08', 'M2-{J}F08', 1), ('M4-F20', 'M4-{J}F20', 1),
                ('M6-F11', 'M6-{J}F11', 1), ('p. 16', 'p.{N}16', 1), ('22 %', '22{N}%', 1),
                ('parâmetros A, B e C', 'parâmetros{N}A, B e{N}C', 3), ('parâmetro B', 'parâmetro{N}B', 2),
                ('parâmetro A', 'parâmetro{N}A', 11), ('parâmetro C', 'parâmetro{N}C', 3),
                ('Parâmetro C', 'Parâmetro{N}C', 2), ('Parâmetro B', 'Parâmetro{N}B', 1), ('Tipo A', 'Tipo{N}A', 4),
                ('Tipo B', 'Tipo{N}B', 3)]),
    dict(i=68, ficheiro='index.html',
         pares=[('século XIX', 'século{N}XIX', 1), ('século XX', 'século{N}XX', 1), ('1.º ano', '1.º{N}ano', 2),
                ('2.º ano', '2.º{N}ano', 2), ('3.º ano', '3.º{N}ano', 2)]),
    dict(i=69, ficheiro='exame/provas/2026-2f/grupo-ii/index.html',
         pares=[('Prova 639, 2.ª fase, 2026, versão 2', 'Prova{N}639, 2.ª{N}fase, 2026, versão{N}2', 2),
                ('10 de março de 2024, p. 22', '10{N}de março de{N}2024, p.{N}22', 3),
                ('Linhas 13 a 18 e 44 a 46', 'Linhas{N}13 a{N}18 e{N}44 a{N}46', 1),
                ('Prova 639, 2.ª fase', 'Prova{N}639, 2.ª{N}fase', 1), ('versão 2, Grupo II', 'versão{N}2, Grupo{N}II', 1),
                ('itens 1, 3, 4 e 7', 'itens{N}1, 3, 4 e{N}7', 1), ('itens 2, 5 e 6', 'itens{N}2, 5 e{N}6', 1),
                ('Linhas 13 a 22', 'Linhas{N}13 a{N}22', 1), ('Linhas 23 a 36', 'Linhas{N}23 a{N}36', 1),
                ('Linhas 13 a 36', 'Linhas{N}13 a{N}36', 1), ('linhas 13 a 36', 'linhas{N}13 a{N}36', 3),
                ('linhas 13 a 18', 'linhas{N}13 a{N}18', 1), ('linhas 20 a 27', 'linhas{N}20 a{N}27', 1),
                ('linhas 28 a 36', 'linhas{N}28 a{N}36', 1), ('linhas 13 e 36', 'linhas{N}13 e{N}36', 1),
                ('linhas 18 a 20', 'linhas{N}18 a{N}20', 1), ('linhas 31 e 32', 'linhas{N}31 e{N}32', 2),
                ('linhas 25 a 27', 'linhas{N}25 a{N}27', 1), ('linhas 21 a 25', 'linhas{N}21 a{N}25', 1),
                ('linhas 13 a 20', 'linhas{N}13 a{N}20', 1), ('linhas 23 a 27', 'linhas{N}23 a{N}27', 4),
                ('linhas 26 e 27', 'linhas{N}26 e{N}27', 2), ('linhas 33 a 36', 'linhas{N}33 a{N}36', 1),
                ('linhas 33 e 34', 'linhas{N}33 e{N}34', 1), ('linhas 35 e 36', 'linhas{N}35 e{N}36', 1),
                ('linhas 34 a 36', 'linhas{N}34 a{N}36', 1), ('Linhas 23 a 27', 'Linhas{N}23 a{N}27', 1),
                ('linhas 25 e 26', 'linhas{N}25 e{N}26', 3), ('linhas 23 e 24', 'linhas{N}23 e{N}24', 7),
                ('linhas 24 a 26', 'linhas{N}24 a{N}26', 1), ('Linhas 23 e 24', 'Linhas{N}23 e{N}24', 1),
                ('Linhas 26 e 27', 'Linhas{N}26 e{N}27', 1), ('Linhas 37 a 46', 'Linhas{N}37 a{N}46', 1),
                ('linhas 40 a 44', 'linhas{N}40 a{N}44', 1), ('linhas 38 e 39', 'linhas{N}38 e{N}39', 1),
                ('linhas 37 a 43', 'linhas{N}37 a{N}43', 1), ('linhas 44 a 46', 'linhas{N}44 a{N}46', 1),
                ('linhas 40 e 41', 'linhas{N}40 e{N}41', 2), ('linhas 37 a 39', 'linhas{N}37 a{N}39', 2),
                ('Itens 5, 6 e 7', 'Itens{N}5, 6 e{N}7', 1), ('itens 5, 6 e 7', 'itens{N}5, 6 e{N}7', 1),
                ('linhas 14 a 18', 'linhas{N}14 a{N}18', 4), ('linhas 45 e 46', 'linhas{N}45 e{N}46', 3),
                ('linhas 15 a 17', 'linhas{N}15 a{N}17', 1), ('linhas 15 e 16', 'linhas{N}15 e{N}16', 2),
                ('Linhas 15 e 16', 'Linhas{N}15 e{N}16', 1), ('Linhas 1 a 12', 'Linhas{N}1 a{N}12', 1),
                ('Linhas 1 a 46', 'Linhas{N}1 a{N}46', 1), ('linhas 8 a 12', 'linhas{N}8 a{N}12', 1),
                ('linhas 9 a 11', 'linhas{N}9 a{N}11', 1), ('linhas 1 a 12', 'linhas{N}1 a{N}12', 1),
                ('linhas 6 e 7', 'linhas{N}6 e{N}7', 3), ('linhas 8 e 9', 'linhas{N}8 e{N}9', 1),
                ('linhas 3 e 4', 'linhas{N}3 e{N}4', 2), ('Linhas 6 e 7', 'Linhas{N}6 e{N}7', 1),
                ('linhas 2 a 4', 'linhas{N}2 a{N}4', 1), ('linhas 2 e 3', 'linhas{N}2 e{N}3', 1),
                ('linhas 6 a 9', 'linhas{N}6 a{N}9', 2), ('linhas 1 a 7', 'linhas{N}1 a{N}7', 1),
                ('Linhas 1 e 2', 'Linhas{N}1 e{N}2', 1), ('itens 3 e 6', 'itens{N}3 e{N}6', 1),
                ('120 minutos', '120{N}minutos', 1), ('itens 1 a 4', 'itens{N}1 a{N}4', 1), ('Grupo III', 'Grupo{N}III', 1),
                ('13 pontos', '13{N}pontos', 2), ('52 pontos', '52{N}pontos', 1), ('2.ª fases', '2.ª{N}fases', 1),
                ('Sessão 22', 'Sessão{N}22', 1), ('Sessão 21', 'Sessão{N}21', 1), ('Sessão 24', 'Sessão{N}24', 1),
                ('Grupo II', 'Grupo{N}II', 4), ('versão 2', 'versão{N}2', 9), ('linha 12', 'linha{N}12', 4),
                ('linha 13', 'linha{N}13', 3), ('linha 22', 'linha{N}22', 2), ('linha 25', 'linha{N}25', 8),
                ('linha 28', 'linha{N}28', 2), ('linha 32', 'linha{N}32', 5), ('linha 36', 'linha{N}36', 1),
                ('linha 21', 'linha{N}21', 6), ('linha 27', 'linha{N}27', 4), ('linha 34', 'linha{N}34', 1),
                ('linha 18', 'linha{N}18', 2), ('linha 37', 'linha{N}37', 4), ('linha 41', 'linha{N}41', 3),
                ('linha 45', 'linha{N}45', 2), ('linha 33', 'linha{N}33', 2), ('Linha 37', 'Linha{N}37', 1),
                ('linha 38', 'linha{N}38', 1), ('linha 39', 'linha{N}39', 1), ('linha 19', 'linha{N}19', 4),
                ('linha 26', 'linha{N}26', 1), ('linha 20', 'linha{N}20', 1), ('linha 23', 'linha{N}23', 1),
                ('linha 29', 'linha{N}29', 1), ('linha 17', 'linha{N}17', 4), ('linha 30', 'linha{N}30', 3),
                ('linha 15', 'linha{N}15', 2), ('linha 14', 'linha{N}14', 1), ('linha 44', 'linha{N}44', 2),
                ('linha 16', 'linha{N}16', 1), ('Grupo I', 'Grupo{N}I', 2), ('linha 1', 'linha{N}1', 15),
                ('linha 7', 'linha{N}7', 4), ('linha 8', 'linha{N}8', 6), ('linha 4', 'linha{N}4', 3),
                ('linha 6', 'linha{N}6', 3), ('linha 2', 'linha{N}2', 2), ('linha 3', 'linha{N}3', 2),
                ('linha 9', 'linha{N}9', 1), ('linha 5', 'linha{N}5', 1), ('Linha 1', 'Linha{N}1', 1),
                ('item 1', 'item{N}1', 1), ('Item 1', 'Item{N}1', 1), ('item 2', 'item{N}2', 4), ('Item 2', 'Item{N}2', 1),
                ('item 3', 'item{N}3', 3), ('Item 3', 'Item{N}3', 1), ('item 4', 'item{N}4', 4), ('Item 4', 'Item{N}4', 1),
                ('M4-F15', 'M4-{J}F15', 2), ('item 5', 'item{N}5', 1), ('Item 5', 'Item{N}5', 1), ('M3-F15', 'M3-{J}F15', 2),
                ('item 6', 'item{N}6', 4), ('Item 6', 'Item{N}6', 1), ('item 7', 'item{N}7', 3), ('M6-F04', 'M6-{J}F04', 2),
                ('Item 7', 'Item{N}7', 1), ('M2-F07', 'M2-{J}F07', 1), ('p. 13', 'p.{N}13', 1), ('1 (C)', '1{N}(C)', 1),
                ('2 (B)', '2{N}(B)', 1), ('3 (A)', '3{N}(A)', 1), ('4 (B)', '4{N}(B)', 1), ('5 (D)', '5{N}(D)', 1),
                ('6 (C)', '6{N}(C)', 1), ('7 (A)', '7{N}(A)', 1), ('p. 1', 'p.{N}1', 1)]),
    dict(i=70, ficheiro='exame/provas/2026-2f/grupo-iii/index.html',
         pares=[('Prova 639, 2.ª fase, 2026, versão 2', 'Prova{N}639, 2.ª{N}fase, 2026, versão{N}2', 2),
                ('Prova 639, 2.ª fase', 'Prova{N}639, 2.ª{N}fase', 3), ('200 a 350 palavras', '200{N}a{N}350{N}palavras', 5),
                ('Quadro 1, p. 2', 'Quadro{N}1, p.{N}2', 1), ('196 palavras', '196{N}palavras', 2),
                ('160 palavras', '160{N}palavras', 1), ('290 palavras', '290{N}palavras', 1),
                ('213 palavras', '213{N}palavras', 1), ('350 palavras', '350{N}palavras', 1),
                ('257 palavras', '257{N}palavras', 1), ('120 minutos', '120{N}minutos', 1),
                ('75 palavras', '75{N}palavras', 2), ('50 palavras', '50{N}palavras', 1),
                ('20 palavras', '20{N}palavras', 3), ('40 palavras', '40{N}palavras', 2),
                ('80 palavras', '80{N}palavras', 2), ('pp. 14 a 16', 'pp.{N}14 a{N}16', 1),
                ('4 palavras', '4{N}palavras', 1), ('5 palavras', '5{N}palavras', 1), ('século XIX', 'século{N}XIX', 1),
                ('Grupo III', 'Grupo{N}III', 16), ('44 pontos', '44{N}pontos', 3), ('30 pontos', '30{N}pontos', 1),
                ('Sessão 24', 'Sessão{N}24', 2), ('10 pontos', '10{N}pontos', 3), ('14 pontos', '14{N}pontos', 3),
                ('11 pontos', '11{N}pontos', 2), ('pp. 1 a 3', 'pp.{N}1 a{N}3', 2), ('2.ª fases', '2.ª{N}fases', 1),
                ('Sessão 22', 'Sessão{N}22', 1), ('Grupo II', 'Grupo{N}II', 1), ('versão 2', 'versão{N}2', 1),
                ('5 pontos', '5{N}pontos', 9), ('1.ª fase', '1.ª{N}fase', 2), ('4 pontos', '4{N}pontos', 3),
                ('0 pontos', '0{N}pontos', 1), ('8 pontos', '8{N}pontos', 6), ('3 pontos', '3{N}pontos', 1),
                ('Quadro 1', 'Quadro{N}1', 3), ('2.ª fase', '2.ª{N}fase', 1), ('nível 4', 'nível{N}4', 11),
                ('nível 3', 'nível{N}3', 5), ('nível 2', 'nível{N}2', 4), ('nível 1', 'nível{N}1', 2),
                ('M5-F13', 'M5-{J}F13', 2), ('M7-F10', 'M7-{J}F10', 2), ('M4-F15', 'M4-{J}F15', 2),
                ('tipo A', 'tipo{N}A', 40), ('M5-F07', 'M5-{J}F07', 2), ('tipo B', 'tipo{N}B', 24), ('25 de', '25{N}de', 1),
                ('p. 16', 'p.{N}16', 1), ('22 %', '22{N}%', 1), ('parâmetros A, B e C', 'parâmetros{N}A, B e{N}C', 3),
                ('parâmetro A', 'parâmetro{N}A', 15), ('parâmetro B', 'parâmetro{N}B', 5),
                ('parâmetro C', 'parâmetro{N}C', 3), ('Parâmetro B', 'Parâmetro{N}B', 2),
                ('Parâmetro C', 'Parâmetro{N}C', 3), ('Parâmetro A', 'Parâmetro{N}A', 1), ('Tipo A', 'Tipo{N}A', 4),
                ('Tipo B', 'Tipo{N}B', 3)]),
    dict(i=71, ficheiro='exame/provas/2026-1f/grupo-i/index.html',
         pares=[('Prova 639, 1.ª fase, 2026, Grupo I, item 1', 'Prova{N}639, 1.ª{N}fase, 2026, Grupo{N}I, item{N}1', 1),
                ('Prova 639, 1.ª fase, 2026, Grupo I, item 2', 'Prova{N}639, 1.ª{N}fase, 2026, Grupo{N}I, item{N}2', 1),
                ('Prova 639, 1.ª fase, 2026, Grupo I, item 4', 'Prova{N}639, 1.ª{N}fase, 2026, Grupo{N}I, item{N}4', 1),
                ('Prova 639, 1.ª fase, 2026, Grupo I, item 5', 'Prova{N}639, 1.ª{N}fase, 2026, Grupo{N}I, item{N}5', 1),
                ('Prova 639, 1.ª fase, 2026, versão 2', 'Prova{N}639, 1.ª{N}fase, 2026, versão{N}2', 2),
                ('versos 4 a 7 e 17 a 20', 'versos{N}4 a{N}7 e{N}17 a{N}20', 1),
                ('itens 1, 2, 4, 5 e 7', 'itens{N}1, 2, 4, 5 e{N}7', 1),
                ('item 6, I, III e IV', 'item{N}6, I, III e{N}IV', 1), ('Prova 639, 1.ª fase', 'Prova{N}639, 1.ª{N}fase', 1),
                ('itens 1, 2, 4 e 5', 'itens{N}1, 2, 4 e{N}5', 1), ('versão 2, Grupo I', 'versão{N}2, Grupo{N}I', 1),
                ('itens 3, 4 e 5', 'itens{N}3, 4 e{N}5', 1), ('linhas 11 a 19', 'linhas{N}11 a{N}19', 1),
                ('linhas 23 a 27', 'linhas{N}23 a{N}27', 3), ('Linhas 11 e 12', 'Linhas{N}11 e{N}12', 1),
                ('linhas 11 e 12', 'linhas{N}11 e{N}12', 6), ('linhas 15 e 16', 'linhas{N}15 e{N}16', 2),
                ('linhas 20 a 27', 'linhas{N}20 a{N}27', 1), ('linhas 22 e 23', 'linhas{N}22 e{N}23', 4),
                ('linhas 26 e 27', 'linhas{N}26 e{N}27', 5), ('linhas 25 a 27', 'linhas{N}25 a{N}27', 2),
                ('linhas 24 e 25', 'linhas{N}24 e{N}25', 1), ('linhas 27 a 38', 'linhas{N}27 a{N}38', 1),
                ('Linhas 28 e 29', 'Linhas{N}28 e{N}29', 1), ('linhas 33 e 34', 'linhas{N}33 e{N}34', 1),
                ('linhas 31 a 33', 'linhas{N}31 a{N}33', 2), ('linhas 37 e 38', 'linhas{N}37 e{N}38', 1),
                ('linhas 34 a 36', 'linhas{N}34 a{N}36', 1), ('linhas 32 e 33', 'linhas{N}32 e{N}33', 1),
                ('linhas 35 a 38', 'linhas{N}35 a{N}38', 1), ('linhas 35 e 36', 'linhas{N}35 e{N}36', 2),
                ('linhas 34 e 35', 'linhas{N}34 e{N}35', 1), ('versos 12 e 17', 'versos{N}12 e{N}17', 1),
                ('versos 17 e 18', 'versos{N}17 e{N}18', 4), ('versos 19 e 20', 'versos{N}19 e{N}20', 1),
                ('versos 15 e 16', 'versos{N}15 e{N}16', 1), ('linhas 1 a 10', 'linhas{N}1 a{N}10', 1),
                ('Linhas 1 a 10', 'Linhas{N}1 a{N}10', 1), ('linhas 7 a 10', 'linhas{N}7 a{N}10', 1),
                ('Versos 9 a 20', 'Versos{N}9 a{N}20', 1), ('versos 1 a 20', 'versos{N}1 a{N}20', 2),
                ('versos 9 a 12', 'versos{N}9 a{N}12', 1), ('século XVIII', 'século{N}XVIII', 3),
                ('linhas 2 a 4', 'linhas{N}2 a{N}4', 1), ('linhas 3 e 4', 'linhas{N}3 e{N}4', 3),
                ('Linhas 2 a 6', 'Linhas{N}2 a{N}6', 1), ('linhas 5 e 6', 'linhas{N}5 e{N}6', 4),
                ('linhas 6 e 7', 'linhas{N}6 e{N}7', 1), ('versos 1 a 8', 'versos{N}1 a{N}8', 1),
                ('itens 3 e 6', 'itens{N}3 e{N}6', 3), ('120 minutos', '120{N}minutos', 1),
                ('pp. 4 a 13', 'pp.{N}4 a{N}13', 1), ('pp. 41-42', 'pp.{N}41-{J}42', 4), ('13 pontos', '13{N}pontos', 10),
                ('65 pontos', '65{N}pontos', 1), ('século XX', 'século{N}XX', 2), ('10 pontos', '10{N}pontos', 2),
                ('2.ª fases', '2.ª{N}fases', 1), ('pp. 1 a 3', 'pp.{N}1 a{N}3', 1), ('Sessão 19', 'Sessão{N}19', 1),
                ('Sessão 11', 'Sessão{N}11', 1), ('Sessão 23', 'Sessão{N}23', 1), ('Grupo II', 'Grupo{N}II', 2),
                ('versão 2', 'versão{N}2', 2), ('linha 10', 'linha{N}10', 2), ('6 pontos', '6{N}pontos', 8),
                ('3 pontos', '3{N}pontos', 4), ('linha 11', 'linha{N}11', 1), ('linha 12', 'linha{N}12', 2),
                ('linha 15', 'linha{N}15', 3), ('linha 23', 'linha{N}23', 4), ('linha 22', 'linha{N}22', 1),
                ('Linha 24', 'Linha{N}24', 1), ('linha 24', 'linha{N}24', 1), ('linha 25', 'linha{N}25', 2),
                ('linha 16', 'linha{N}16', 3), ('8 pontos', '8{N}pontos', 1), ('linha 34', 'linha{N}34', 1),
                ('linha 35', 'linha{N}35', 1), ('linha 29', 'linha{N}29', 4), ('linha 33', 'linha{N}33', 1),
                ('linha 30', 'linha{N}30', 2), ('linha 36', 'linha{N}36', 5), ('linha 37', 'linha{N}37', 2),
                ('verso 17', 'verso{N}17', 7), ('verso 12', 'verso{N}12', 5), ('verso 18', 'verso{N}18', 1),
                ('verso 19', 'verso{N}19', 1), ('verso 20', 'verso{N}20', 2), ('verso 11', 'verso{N}11', 6),
                ('verso 14', 'verso{N}14', 6), ('verso 16', 'verso{N}16', 1), ('Verso 11', 'Verso{N}11', 1),
                ('verso 13', 'verso{N}13', 2), ('verso 10', 'verso{N}10', 3), ('4 pontos', '4{N}pontos', 1),
                ('Grupo I', 'Grupo{N}I', 8), ('27.ª ed', '27.ª{N}ed', 2), ('17.ª ed', '17.ª{N}ed', 2),
                ('Parte A', 'Parte{N}A', 4), ('Texto 1', 'Texto{N}1', 2), ('linha 3', 'linha{N}3', 7),
                ('linha 1', 'linha{N}1', 4), ('linha 4', 'linha{N}4', 10), ('linha 9', 'linha{N}9', 1),
                ('linha 6', 'linha{N}6', 2), ('linha 7', 'linha{N}7', 1), ('nível 5', 'nível{N}5', 2),
                ('nível 3', 'nível{N}3', 4), ('Texto 2', 'Texto{N}2', 2), ('nível 4', 'nível{N}4', 1),
                ('Parte B', 'Parte{N}B', 2), ('verso 5', 'verso{N}5', 7), ('Verso 4', 'Verso{N}4', 1),
                ('verso 4', 'verso{N}4', 5), ('verso 3', 'verso{N}3', 1), ('verso 8', 'verso{N}8', 4),
                ('verso 7', 'verso{N}7', 1), ('verso 1', 'verso{N}1', 2), ('Verso 1', 'Verso{N}1', 1),
                ('verso 9', 'verso{N}9', 1), ('verso 2', 'verso{N}2', 3), ('Parte C', 'Parte{N}C', 1),
                ('nível 2', 'nível{N}2', 2), ('p. 123', 'p.{N}123', 3), ('item 3', 'item{N}3', 5), ('item 6', 'item{N}6', 2),
                ('item 2', 'item{N}2', 9), ('Item 1', 'Item{N}1', 3), ('item 1', 'item{N}1', 9), ('tipo A', 'tipo{N}A', 5),
                ('tipo B', 'tipo{N}B', 5), ('Item 2', 'Item{N}2', 2), ('Item 3', 'Item{N}3', 2), ('nota 3', 'nota{N}3', 1),
                ('Item 4', 'Item{N}4', 3), ('item 4', 'item{N}4', 4), ('Item 5', 'Item{N}5', 3), ('item 5', 'item{N}5', 3),
                ('Item 6', 'Item{N}6', 1), ('nota 1', 'nota{N}1', 2), ('Item 7', 'Item{N}7', 4), ('item 7', 'item{N}7', 6),
                ('M9-F01', 'M9-{J}F01', 1), ('M9-F02', 'M9-{J}F02', 1), ('M9-F03', 'M9-{J}F03', 1),
                ('M9-F05', 'M9-{J}F05', 1), ('M6-F06', 'M6-{J}F06', 1), ('M6-F07', 'M6-{J}F07', 1)]),
    dict(i=72, ficheiro='exame/provas/2026-2f/grupo-i/index.html',
         pares=[('Prova 639, 2.ª fase, 2026, Grupo I, item 1', 'Prova{N}639, 2.ª{N}fase, 2026, Grupo{N}I, item{N}1', 1),
                ('Prova 639, 2.ª fase, 2026, Grupo I, item 2', 'Prova{N}639, 2.ª{N}fase, 2026, Grupo{N}I, item{N}2', 1),
                ('Prova 639, 2.ª fase, 2026, Grupo I, item 4', 'Prova{N}639, 2.ª{N}fase, 2026, Grupo{N}I, item{N}4', 1),
                ('Prova 639, 2.ª fase, 2026, Grupo I, item 5', 'Prova{N}639, 2.ª{N}fase, 2026, Grupo{N}I, item{N}5', 1),
                ('Prova 639, 2.ª fase, 2026, versão 2', 'Prova{N}639, 2.ª{N}fase, 2026, versão{N}2', 2),
                ('Linhas 8 a 10, 15 e 16, 27 a 30', 'Linhas{N}8 a{N}10, 15 e{N}16, 27 a{N}30', 2),
                ('Linhas 8 a 10, 15 a 17, 27 a 31', 'Linhas{N}8 a{N}10, 15 a{N}17, 27 a{N}31', 1),
                ('Linhas 1 a 7, 11 a 14, 17 a 26', 'Linhas{N}1 a{N}7, 11 a{N}14, 17 a{N}26', 1),
                ('Poema 1, versos 10 e 11', 'Poema{N}1, versos{N}10 e{N}11', 1),
                ('versos 1 a 9 e 15 a 18', 'versos{N}1 a{N}9 e{N}15 a{N}18', 2),
                ('Poema 1, versos 8 e 9', 'Poema{N}1, versos{N}8 e{N}9', 1),
                ('itens 1, 2, 4, 5 e 7', 'itens{N}1, 2, 4, 5 e{N}7', 1),
                ('linhas 16 e 28 a 30', 'linhas{N}16 e{N}28 a{N}30', 1),
                ('item 6, II, III e V', 'item{N}6, II, III e{N}V', 1), ('Prova 639, 2.ª fase', 'Prova{N}639, 2.ª{N}fase', 1),
                ('Poema 1, verso 15', 'Poema{N}1, verso{N}15', 1), ('linhas 8, 15 e 27', 'linhas{N}8, 15 e{N}27', 2),
                ('linhas 1, 11 e 17', 'linhas{N}1, 11 e{N}17', 1), ('itens 1, 2, 4 e 5', 'itens{N}1, 2, 4 e{N}5', 1),
                ('versão 2, Grupo I', 'versão{N}2, Grupo{N}I', 1), ('Poema 1, verso 8', 'Poema{N}1, verso{N}8', 1),
                ('Poema 2, verso 2', 'Poema{N}2, verso{N}2', 1), ('Poema 2, verso 3', 'Poema{N}2, verso{N}3', 1),
                ('Poema 2, verso 5', 'Poema{N}2, verso{N}5', 1), ('Poema 2, verso 1', 'Poema{N}2, verso{N}1', 1),
                ('itens 2, 5 e 6', 'itens{N}2, 5 e{N}6', 1), ('versos 12 e 13', 'versos{N}12 e{N}13', 4),
                ('versos 11 a 15', 'versos{N}11 a{N}15', 1), ('versos 10 e 11', 'versos{N}10 e{N}11', 2),
                ('versos 16 e 17', 'versos{N}16 e{N}17', 4), ('versos 14 e 15', 'versos{N}14 e{N}15', 1),
                ('versos 13 a 15', 'versos{N}13 a{N}15', 1), ('versos 18 e 19', 'versos{N}18 e{N}19', 3),
                ('versos 13 e 14', 'versos{N}13 e{N}14', 2), ('versos 10 a 14', 'versos{N}10 a{N}14', 2),
                ('linhas 12 e 13', 'linhas{N}12 e{N}13', 2), ('linhas 12 a 14', 'linhas{N}12 a{N}14', 1),
                ('linhas 18 e 19', 'linhas{N}18 e{N}19', 4), ('linhas 17 a 36', 'linhas{N}17 a{N}36', 1),
                ('Linhas 25 e 26', 'Linhas{N}25 e{N}26', 1), ('linhas 32 a 36', 'linhas{N}32 a{N}36', 4),
                ('linhas 17 e 31', 'linhas{N}17 e{N}31', 1), ('linhas 28 a 30', 'linhas{N}28 a{N}30', 3),
                ('linhas 19 e 20', 'linhas{N}19 e{N}20', 2), ('versos 5 a 12', 'versos{N}5 a{N}12', 1),
                ('linhas 1 a 16', 'linhas{N}1 a{N}16', 1), ('linhas 1 a 36', 'linhas{N}1 a{N}36', 1),
                ('versos 1 a 9', 'versos{N}1 a{N}9', 1), ('versos 3 e 4', 'versos{N}3 e{N}4', 3),
                ('versos 1 e 2', 'versos{N}1 e{N}2', 1), ('versos 1 a 4', 'versos{N}1 a{N}4', 4),
                ('linhas 3 e 4', 'linhas{N}3 e{N}4', 4), ('linhas 2 e 3', 'linhas{N}2 e{N}3', 2),
                ('Linhas 6 e 7', 'Linhas{N}6 e{N}7', 1), ('linhas 6 e 7', 'linhas{N}6 e{N}7', 2),
                ('itens 3 e 6', 'itens{N}3 e{N}6', 3), ('pp. 237-239', 'pp.{N}237-{J}239', 2),
                ('120 minutos', '120{N}minutos', 1), ('D. Madalena', 'D.{N}Madalena', 3), ('13 pontos', '13{N}pontos', 10),
                ('65 pontos', '65{N}pontos', 1), ('10 pontos', '10{N}pontos', 5), ('36 linhas', '36{N}linhas', 2),
                ('2.ª fases', '2.ª{N}fases', 1), ('pp. 1 a 3', 'pp.{N}1 a{N}3', 1), ('Sessão 17', 'Sessão{N}17', 1),
                ('Sessão 13', 'Sessão{N}13', 1), ('Sessão 23', 'Sessão{N}23', 1), ('Grupo II', 'Grupo{N}II', 2),
                ('versão 2', 'versão{N}2', 2), ('verso 16', 'verso{N}16', 5), ('verso 12', 'verso{N}12', 4),
                ('verso 14', 'verso{N}14', 5), ('verso 15', 'verso{N}15', 7), ('verso 19', 'verso{N}19', 7),
                ('verso 17', 'verso{N}17', 7), ('Verso 15', 'Verso{N}15', 1), ('verso 10', 'verso{N}10', 3),
                ('6 pontos', '6{N}pontos', 7), ('3 pontos', '3{N}pontos', 4), ('verso 11', 'verso{N}11', 3),
                ('verso 18', 'verso{N}18', 5), ('verso 13', 'verso{N}13', 3), ('linha 13', 'linha{N}13', 6),
                ('linha 12', 'linha{N}12', 5), ('linha 18', 'linha{N}18', 7), ('linha 20', 'linha{N}20', 2),
                ('linha 33', 'linha{N}33', 3), ('linha 25', 'linha{N}25', 1), ('linha 16', 'linha{N}16', 10),
                ('linha 30', 'linha{N}30', 6), ('linha 29', 'linha{N}29', 2), ('linha 28', 'linha{N}28', 1),
                ('linha 32', 'linha{N}32', 3), ('linha 35', 'linha{N}35', 3), ('Linha 20', 'Linha{N}20', 1),
                ('4 pontos', '4{N}pontos', 1), ('Sessão 7', 'Sessão{N}7', 1), ('Sessão 4', 'Sessão{N}4', 1),
                ('Grupo I', 'Grupo{N}I', 8), ('Parte A', 'Parte{N}A', 4), ('Poema 1', 'Poema{N}1', 22),
                ('verso 5', 'verso{N}5', 6), ('verso 1', 'verso{N}1', 5), ('verso 6', 'verso{N}6', 6),
                ('verso 8', 'verso{N}8', 6), ('verso 3', 'verso{N}3', 5), ('nível 5', 'nível{N}5', 4),
                ('nível 3', 'nível{N}3', 3), ('Poema 2', 'Poema{N}2', 27), ('verso 4', 'verso{N}4', 3),
                ('Parte B', 'Parte{N}B', 2), ('linha 3', 'linha{N}3', 4), ('linha 4', 'linha{N}4', 3),
                ('D. João', 'D.{N}João', 21), ('linha 6', 'linha{N}6', 1), ('linha 9', 'linha{N}9', 9),
                ('linha 5', 'linha{N}5', 2), ('linha 2', 'linha{N}2', 1), ('Parte C', 'Parte{N}C', 1),
                ('nível 2', 'nível{N}2', 2), ('2.ª ed', '2.ª{N}ed', 2), ('3.ª ed', '3.ª{N}ed', 2), ('p. 110', 'p.{N}110', 2),
                ('item 3', 'item{N}3', 5), ('item 6', 'item{N}6', 2), ('Item 1', 'Item{N}1', 3), ('item 1', 'item{N}1', 7),
                ('nota 1', 'nota{N}1', 3), ('nota 2', 'nota{N}2', 2), ('tipo A', 'tipo{N}A', 5), ('tipo B', 'tipo{N}B', 5),
                ('Item 2', 'Item{N}2', 3), ('item 2', 'item{N}2', 6), ('Item 3', 'Item{N}3', 2), ('Item 4', 'Item{N}4', 3),
                ('item 4', 'item{N}4', 6), ('nota 3', 'nota{N}3', 1), ('nota 8', 'nota{N}8', 1), ('Item 5', 'Item{N}5', 3),
                ('item 5', 'item{N}5', 6), ('nota 6', 'nota{N}6', 1), ('Item 6', 'Item{N}6', 1), ('Item 7', 'Item{N}7', 4),
                ('item 7', 'item{N}7', 6), ('M3-F09', 'M3-{J}F09', 2), ('M8-F04', 'M8-{J}F04', 1),
                ('M7-F04', 'M7-{J}F04', 1), ('M4-F09', 'M4-{J}F09', 1), ('M4-F07', 'M4-{J}F07', 1),
                ('M4-F08', 'M4-{J}F08', 1), ('p. 35', 'p.{N}35', 2), ('ato I', 'ato{N}I', 2)]),
    dict(i=73, ficheiro='assets/exame/sessoes.json',
         pares=[('D. Dinis, cantiga 544', 'D.{N}Dinis, cantiga{N}544', 1),
                ('ato I, cenas XI e XII', 'ato{N}I, cenas{N}XI e{N}XII', 1),
                ('200 a 350 palavras', '200{N}a{N}350{N}palavras', 3), ('100 a 150 palavras', '100{N}a{N}150{N}palavras', 1),
                ('80 a 100 palavras', '80{N}a{N}100{N}palavras', 1), ('80 a 110 palavras', '80{N}a{N}110{N}palavras', 1),
                ('200–350 palavras', '200–{J}350{N}palavras', 3), ('100–150 palavras', '100–{J}150{N}palavras', 1),
                ('100–140 palavras', '100–{J}140{N}palavras', 1), ('80–120 palavras', '80–{J}120{N}palavras', 20),
                ('80–100 palavras', '80–{J}100{N}palavras', 2), ('80–110 palavras', '80–{J}110{N}palavras', 1),
                ('estrofes 1 e 5', 'estrofes{N}1 e{N}5', 1), ('ato II, cena I', 'ato{N}II, cena{N}I', 1),
                ('1.ª publicação', '1.ª{N}publicação', 3), ('cantiga 1308', 'cantiga{N}1308', 1),
                ('caps. I e II', 'caps.{N}I e{N}II', 2), ('cantiga 861', 'cantiga{N}861', 1),
                ('soneto XIII', 'soneto{N}XIII', 1), ('séc. XIII', 'séc.{N}XIII', 2), ('cap. CXVI', 'cap.{N}CXVI', 1),
                ('vv. 1 a 4', 'vv.{N}1 a{N}4', 1), ('12.º anos', '12.º{N}anos', 1), ('D. Dinis', 'D.{N}Dinis', 2),
                ('cap. XII', 'cap.{N}XII', 1), ('cap. 115', 'cap.{N}115', 1), ('D. João', 'D.{N}João', 2),
                ('cap. 11', 'cap.{N}11', 1), ('cap. V', 'cap.{N}V', 2), ('ato II', 'ato{N}II', 1), ('cap. I', 'cap.{N}I', 2),
                ('ato I', 'ato{N}I', 1), ('v. 6', 'v.{N}6', 1), ('n.º 36', 'n.º{N}36', 1), ('n.º 38', 'n.º{N}38', 1),
                ('n.º 1', 'n.º{N}1', 1)]),
    dict(i=74, ficheiro='assets/exame/app.js',
         pares=[('Prova 639 de 2026, 1.ª fase', 'Prova{N}639 de 2026, 1.ª{N}fase', 1),
                ("+' min de escrita</p>", "+'{N}min de escrita</p>", 1),
                ('Informação-Prova 639', 'Informação-Prova{N}639', 1), ("+' minutos · '+", "+'{N}minutos · '+", 1),
                ('10.º–12.º ano', '10.º–{J}12.º{N}ano', 1), ('10–20 minutos', '10–{J}20{N}minutos', 1),
                ('50 minutos', '50{N}minutos', 3), ('50 min', '50{N}min', 1), ('64 MiB', '64{N}MiB', 1),
                ('8 MiB', '8{N}MiB', 1)]),
    dict(i=75, ficheiro='assets/exame/laboratorio.js',
         pares=[('Prova 639, 2026, 1.ª fase', 'Prova{N}639, 2026, 1.ª{N}fase', 1), ('linhas 2 a 4', 'linhas{N}2 a{N}4', 1),
                ('linhas 2–4', 'linhas{N}2–{J}4', 2), ('linha 2', 'linha{N}2', 9), ('linha 4', 'linha{N}4', 2),
                ('linha 1', 'linha{N}1', 1), ('pp. 1–3', 'pp.{N}1–{J}3', 1)]),
    dict(i=76, ficheiro='assets/exame/dossier.js',
         pares=[('64 MiB', '64{N}MiB', 2), ('8 MiB', '8{N}MiB', 1)]),
]

# Os pares «por analogia» de cada achado (a classe que a conferência lhes deu).
ANALOGIA = {26: ['Prova 639'],
 66: ['Prova 639, 1.ª fase, 2026, versão 2', 'Prova 639, 1.ª fase', 'versão 2, Grupo II', 'itens 1, 2, 6 e 7', 'itens 3, 4 e 5',
      'linhas 13 e 14', 'linhas 35 a 40', 'Linhas 10 a 22', 'Linhas 23 a 34', 'linhas 30 a 34', 'linhas 30 e 31',
      'linhas 10 e 22', 'linhas 10 a 22', 'Linhas 15 a 29', 'linhas 15 a 29', 'Linhas 30 e 31', 'Linhas 31 a 34',
      'Linhas 35 a 47', 'linhas 41 e 42', 'linhas 45 a 47', 'linhas 35 a 47', 'linhas 41 a 43', 'linhas 44 a 47',
      'linhas 38 a 40', 'Linhas 41 e 42', 'linhas 46 e 47', 'Itens 5, 6 e 7', 'itens 5, 6 e 7', 'linhas 15 a 22',
      'linhas 38 e 39', 'linhas 35 e 36', 'linhas 6 a 14', 'Linhas 6 a 22', 'linhas 6 a 22', 'Linhas 1 a 9', 'linhas 6 a 8',
      'linhas 2 e 3', 'linhas 4 e 5', 'linhas 3 e 4', 'linhas 7 e 8', 'Linhas 7 e 8', 'itens 3 e 6', 'itens 1 a 4',
      'itens 6 e 7', 'Grupo III', '13 pontos', '52 pontos', 'Sessão 22', 'Sessão 21', 'Grupo II', 'versão 2', 'linha 14',
      'linha 10', 'linha 15', 'linha 17', 'linha 12', 'linha 19', 'linha 31', 'linha 44', 'linha 37', 'linha 43', 'linha 46',
      'linha 36', 'linha 38', 'linha 21', 'linha 20', 'linha 23', 'linha 28', 'linha 26', 'linha 25', 'Grupo I', 'linha 1',
      'linha 9', 'linha 5', 'linha 6', 'linha 3', 'linha 7', 'Linha 6', 'item 1', 'Item 1', 'item 2', 'Item 2', 'Item 3',
      'Item 4', 'item 5', 'Item 5', 'item 6', 'Item 6', 'item 7', 'Item 7', '1 (B)', '2 (C)', '3 (A)', '4 (D)', '5 (B)',
      '6 (C)', '7 (D)'],
 67: ['Prova 639, 1.ª fase, 2026, versão 2', 'Prova 639, 1.ª fase', 'Quadro 1, p. 2', 'Grupo III', '44 pontos', '30 pontos',
      'Sessão 25', '10 pontos', '14 pontos', '11 pontos', 'Sessão 24', 'Grupo II', 'versão 2', '5 pontos', '3 pontos',
      '8 pontos', 'Quadro 1', 'nível 3', 'nível 4', 'nível 2', 'tipo A', 'tipo B', 'parâmetros A, B e C', 'parâmetro B',
      'parâmetro A', 'parâmetro C', 'Parâmetro C', 'Parâmetro B', 'Tipo A', 'Tipo B'],
 69: ['Prova 639, 2.ª fase, 2026, versão 2', 'Linhas 13 a 18 e 44 a 46', 'Prova 639, 2.ª fase', 'versão 2, Grupo II',
      'itens 1, 3, 4 e 7', 'itens 2, 5 e 6', 'Linhas 13 a 22', 'Linhas 23 a 36', 'Linhas 13 a 36', 'linhas 13 a 36',
      'linhas 13 a 18', 'linhas 20 a 27', 'linhas 28 a 36', 'linhas 13 e 36', 'linhas 18 a 20', 'linhas 31 e 32',
      'linhas 25 a 27', 'linhas 21 a 25', 'linhas 13 a 20', 'linhas 23 a 27', 'linhas 26 e 27', 'linhas 33 a 36',
      'linhas 33 e 34', 'linhas 35 e 36', 'linhas 34 a 36', 'Linhas 23 a 27', 'linhas 25 e 26', 'linhas 23 e 24',
      'linhas 24 a 26', 'Linhas 23 e 24', 'Linhas 26 e 27', 'Linhas 37 a 46', 'linhas 40 a 44', 'linhas 38 e 39',
      'linhas 37 a 43', 'linhas 44 a 46', 'linhas 40 e 41', 'linhas 37 a 39', 'Itens 5, 6 e 7', 'itens 5, 6 e 7',
      'linhas 14 a 18', 'linhas 45 e 46', 'linhas 15 a 17', 'linhas 15 e 16', 'Linhas 15 e 16', 'Linhas 1 a 12',
      'Linhas 1 a 46', 'linhas 8 a 12', 'linhas 9 a 11', 'linhas 1 a 12', 'linhas 6 e 7', 'linhas 8 e 9', 'linhas 3 e 4',
      'Linhas 6 e 7', 'linhas 2 a 4', 'linhas 2 e 3', 'linhas 6 a 9', 'linhas 1 a 7', 'Linhas 1 e 2', 'itens 3 e 6',
      'itens 1 a 4', 'Grupo III', '13 pontos', '52 pontos', 'Sessão 22', 'Sessão 21', 'Sessão 24', 'Grupo II', 'versão 2',
      'linha 12', 'linha 13', 'linha 22', 'linha 25', 'linha 28', 'linha 32', 'linha 36', 'linha 21', 'linha 27', 'linha 34',
      'linha 18', 'linha 37', 'linha 41', 'linha 45', 'linha 33', 'Linha 37', 'linha 38', 'linha 39', 'linha 19', 'linha 26',
      'linha 20', 'linha 23', 'linha 29', 'linha 17', 'linha 30', 'linha 15', 'linha 14', 'linha 44', 'linha 16', 'Grupo I',
      'linha 1', 'linha 7', 'linha 8', 'linha 4', 'linha 6', 'linha 2', 'linha 3', 'linha 9', 'linha 5', 'Linha 1', 'item 1',
      'Item 1', 'item 2', 'Item 2', 'item 3', 'Item 3', 'item 4', 'Item 4', 'item 5', 'Item 5', 'item 6', 'Item 6', 'item 7',
      'Item 7', '1 (C)', '2 (B)', '3 (A)', '4 (B)', '5 (D)', '6 (C)', '7 (A)'],
 70: ['Prova 639, 2.ª fase, 2026, versão 2', 'Prova 639, 2.ª fase', 'Quadro 1, p. 2', 'Grupo III', '44 pontos', '30 pontos',
      'Sessão 24', '10 pontos', '14 pontos', '11 pontos', 'Sessão 22', 'Grupo II', 'versão 2', '5 pontos', '4 pontos',
      '0 pontos', '8 pontos', '3 pontos', 'Quadro 1', 'nível 4', 'nível 3', 'nível 2', 'nível 1', 'tipo A', 'tipo B',
      'parâmetros A, B e C', 'parâmetro A', 'parâmetro B', 'parâmetro C', 'Parâmetro B', 'Parâmetro C', 'Parâmetro A', 'Tipo A',
      'Tipo B'],
 71: ['Prova 639, 1.ª fase, 2026, Grupo I, item 1', 'Prova 639, 1.ª fase, 2026, Grupo I, item 2',
      'Prova 639, 1.ª fase, 2026, Grupo I, item 4', 'Prova 639, 1.ª fase, 2026, Grupo I, item 5',
      'Prova 639, 1.ª fase, 2026, versão 2', 'itens 1, 2, 4, 5 e 7', 'item 6, I, III e IV', 'Prova 639, 1.ª fase',
      'itens 1, 2, 4 e 5', 'versão 2, Grupo I', 'itens 3, 4 e 5', 'linhas 11 a 19', 'linhas 23 a 27', 'Linhas 11 e 12',
      'linhas 11 e 12', 'linhas 15 e 16', 'linhas 20 a 27', 'linhas 22 e 23', 'linhas 26 e 27', 'linhas 25 a 27',
      'linhas 24 e 25', 'linhas 27 a 38', 'Linhas 28 e 29', 'linhas 33 e 34', 'linhas 31 a 33', 'linhas 37 e 38',
      'linhas 34 a 36', 'linhas 32 e 33', 'linhas 35 a 38', 'linhas 35 e 36', 'linhas 34 e 35', 'linhas 1 a 10',
      'Linhas 1 a 10', 'linhas 7 a 10', 'linhas 2 a 4', 'linhas 3 e 4', 'Linhas 2 a 6', 'linhas 5 e 6', 'linhas 6 e 7',
      'itens 3 e 6', '13 pontos', '65 pontos', '10 pontos', 'Sessão 19', 'Sessão 11', 'Sessão 23', 'Grupo II', 'versão 2',
      'linha 10', '6 pontos', '3 pontos', 'linha 11', 'linha 12', 'linha 15', 'linha 23', 'linha 22', 'Linha 24', 'linha 24',
      'linha 25', 'linha 16', '8 pontos', 'linha 34', 'linha 35', 'linha 29', 'linha 33', 'linha 30', 'linha 36', 'linha 37',
      '4 pontos', 'Grupo I', 'Parte A', 'Texto 1', 'linha 3', 'linha 1', 'linha 4', 'linha 9', 'linha 6', 'linha 7', 'nível 5',
      'nível 3', 'Texto 2', 'nível 4', 'Parte B', 'Parte C', 'nível 2', 'item 3', 'item 6', 'item 2', 'Item 1', 'item 1',
      'tipo A', 'tipo B', 'Item 2', 'Item 3', 'Item 4', 'item 4', 'Item 5', 'item 5', 'Item 6', 'Item 7', 'item 7'],
 72: ['Prova 639, 2.ª fase, 2026, Grupo I, item 1', 'Prova 639, 2.ª fase, 2026, Grupo I, item 2',
      'Prova 639, 2.ª fase, 2026, Grupo I, item 4', 'Prova 639, 2.ª fase, 2026, Grupo I, item 5',
      'Prova 639, 2.ª fase, 2026, versão 2', 'Linhas 8 a 10, 15 e 16, 27 a 30', 'Linhas 8 a 10, 15 a 17, 27 a 31',
      'Linhas 1 a 7, 11 a 14, 17 a 26', 'Poema 1, versos 10 e 11', 'Poema 1, versos 8 e 9', 'itens 1, 2, 4, 5 e 7',
      'linhas 16 e 28 a 30', 'item 6, II, III e V', 'Prova 639, 2.ª fase', 'Poema 1, verso 15', 'linhas 8, 15 e 27',
      'linhas 1, 11 e 17', 'itens 1, 2, 4 e 5', 'versão 2, Grupo I', 'Poema 1, verso 8', 'Poema 2, verso 2', 'Poema 2, verso 3',
      'Poema 2, verso 5', 'Poema 2, verso 1', 'itens 2, 5 e 6', 'linhas 12 e 13', 'linhas 12 a 14', 'linhas 18 e 19',
      'linhas 17 a 36', 'Linhas 25 e 26', 'linhas 32 a 36', 'linhas 17 e 31', 'linhas 28 a 30', 'linhas 19 e 20',
      'linhas 1 a 16', 'linhas 1 a 36', 'linhas 3 e 4', 'linhas 2 e 3', 'Linhas 6 e 7', 'linhas 6 e 7', 'itens 3 e 6',
      '13 pontos', '65 pontos', '10 pontos', '36 linhas', 'Sessão 17', 'Sessão 13', 'Sessão 23', 'Grupo II', 'versão 2',
      '6 pontos', '3 pontos', 'linha 13', 'linha 12', 'linha 18', 'linha 20', 'linha 33', 'linha 25', 'linha 16', 'linha 30',
      'linha 29', 'linha 28', 'linha 32', 'linha 35', 'Linha 20', '4 pontos', 'Sessão 7', 'Sessão 4', 'Grupo I', 'Parte A',
      'Poema 1', 'nível 5', 'nível 3', 'Poema 2', 'Parte B', 'linha 3', 'linha 4', 'linha 6', 'linha 9', 'linha 5', 'linha 2',
      'Parte C', 'nível 2', 'item 3', 'item 6', 'Item 1', 'item 1', 'tipo A', 'tipo B', 'Item 2', 'item 2', 'Item 3', 'Item 4',
      'item 4', 'Item 5', 'item 5', 'Item 6', 'Item 7', 'item 7'],
 74: ['Prova 639 de 2026, 1.ª fase', 'Informação-Prova 639', '64 MiB', '8 MiB'],
 75: ['Prova 639, 2026, 1.ª fase', 'linhas 2 a 4', 'linhas 2–4', 'linha 2', 'linha 4', 'linha 1'],
 76: ['64 MiB', '8 MiB']}
# As contas da conferência foram feitas sobre o main 4bf4a053; o que mudou até à base desta camada:
# - o achado 74 (assets/exame/app.js) contava cinco pares nas células da tabela do achado 0, que já os leva presos;
# - no achado 73 (assets/exame/sessoes.json), a camada do M9 já prendeu, na sessão s19, a resposta certa («No início do
#   século XVIII») e o retorno («D. João V», «século XVIII», «século XX») da pergunta copiada da M9-F01, nas perguntas antigas e
#   na verificação «Depois da revisão»; e «v. 1» já estava preso (camada do M6). As outras quatro opções dessa pergunta mudam
#   aqui nas duas cópias (as perguntas antigas, que a página não mostra, e a verificação), para a pergunta ficar igual nas
#   duas: são as trocas literais abaixo, em vez dos pares «século XVI», «século XVII», «século XIX» e «século XX».
# - no achado 73, os pares «27:18–28:23» e «29:04–30:12» ficam de fora (revisão de 12/11/2026): estão nos rótulos dos dois trechos
#   de vídeo da sessão s27 (video.clips[].label), que assets/exame/app.js põe no <h3> do trecho e também no title do vídeo
#   (f.title=c.label+…). É o caso do data-titulo dos vídeos das obras, que vira title: o rótulo fica como estava
#   (fora_de_alcance recusa qualquer par que lá caia e RECUSADOS_TITLE guarda os dois, para o teste os conferir).
# - no achado 67 (Prova 639 de 2026, 1.ª fase, Grupo III), o par «p. 13» fica de fora: as frases que o levam em texto nosso vêm de
#   scripts/provas/dados/2026-1f/prova.json (a imagem com direitos, que o gerador põe nos cartões), que esta camada não muda.
AJUSTES = {
    74: {'refeitos': {seq: (n, 'na tabela do achado 0') for seq, n in FASES_REFEITAS.items()}},
    73: {'literais': [(f'"{o}"', f'"{o.replace("século ", "século{N}")}"',
                       'opção da pergunta da sessão s19 copiada da M9-F01, nas duas cópias (perguntas antigas e verificação)', 2)
                      for o in ('No início do século XVI', 'No fim do século XX', 'No fim do século XVII', 'No início do século XIX')],
         'ja_presos': {'século XVIII': 2, 'D. João V': 1, 'século XX': 1, 'v. 1': 1}},
}
RECUSADOS_TITLE = {73: ['27:18–28:23', '29:04–30:12']}
for _x in ACHADOS_B:
    _x.update({k: v for k, v in AJUSTES.get(_x['i'], {}).items() if k != 'ja_presos'})


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



# As provas em cartões (exame/provas/AAAA-Nf/grupo-x/, de scripts/provas/gerar.py e scripts/provas/dados/): só muda o texto nosso.
# O texto oficial (o texto e os itens da prova, as grelhas, os tópicos e as regras dos critérios, transcritos) fica como está, sem
# espaços invisíveis; as citações entre «» também, e ainda os rótulos e os títulos dos cartões (pelos quais os testes e o motor
# reconhecem os itens) e as indicações de fonte (<p class="fonte">, que os testes comparam com a transcrição).
_CADEIA = re.compile(r'"(?:[^"\\]|\\.)*"')
OFICIAL_ROT = re.compile(r'\bItem \d+ da prova\b(?! \(adaptado)')
DETALHES_OFICIAIS = ('A grelha oficial, tal como está nos critérios', 'Tipos de erro (Quadro 1 dos critérios)', 'Dos critérios oficiais',
                     'Regras dos critérios que contam na classificação', 'Critérios gerais da resposta restrita',
                     'Tópicos de resposta dos critérios', 'A tabela da correção linguística, lida por linhas',
                     'Tabela da correção linguística')
_F = r'<\\?/'   # o fecho de uma etiqueta, nos dados («</») e na página («<\/»)
BLOCOS_OFICIAIS = [re.compile(p, re.S) for p in (
    r'<div class=\\"v prova-l[^"\\]*\\">.*?' + _F + r'div>', r'<p class=\\"gl\\">.*?' + _F + r'p>', r'<p class=\\"papel-q\\">.*?' + _F + r'p>',
    r'<table class=\\"(?:empilha grelha|cl)\\">.*?' + _F + r'table>', r'<ul class=\\"(?:prova-lista|papel-l)\\">.*?' + _F + r'ul>',
    r'<ol class=\\"prova-obs\\">.*?' + _F + r'ol>', r'<p class=\\"fonte\\">.*?' + _F + r'p>', r'<p><b>(?:(?!' + _F + r'b>).)*' + _F + r'b>' + _F + r'p>',
    r'<details[^>]*><summary>(?:' + '|'.join(re.escape(s) for s in DETALHES_OFICIAIS) + r')' + _F + r'summary>.*?' + _F + r'details>')]
CAMPOS_NOSSOS = ('f', 'fe')
CAMPOS_DO_ENUNCIADO = ('p', 'p2', 'o', 'pares', 'lacunas', 'apoio')
CAMPOS_DE_QUALQUER_CARTAO = ('liga',)
PROVA = re.compile(r'(?:exame/provas|scripts/provas/dados)/\d{4}-\df/grupo-[iv]+(?:/index\.html|\.json)$')


def _cartoes_com_posicoes(texto, inicio):
    """Os cartões da lista JSON que começa em inicio («[»): para cada um, {campo: [(a, b), …]} com as posições dos textos de cada
    campo de topo (os textos das listas e dos objetos de dentro contam para o campo de topo). Devolve (fim da lista, cartões)."""
    cartoes, pilha, i, chave, espera = [], [], inicio, None, False
    while True:
        c = texto[i]
        if c in '[{':
            pilha.append(c)
            if c == '{':
                espera = True
                if len(pilha) == 2:
                    cartoes.append({})
            i += 1
        elif c in ']}':
            pilha.pop()
            i += 1
            espera = False
            if not pilha:
                return i, cartoes
        elif c == '"':
            m = _CADEIA.match(texto, i)
            if pilha[-1] == '{' and espera:
                if len(pilha) == 2:
                    chave = texto[i + 1:m.end() - 1]
                espera = False
            elif len(pilha) >= 2:
                cartoes[-1].setdefault(chave, []).append((i + 1, m.end() - 1))
            i = m.end()
        else:
            if c == ',' and pilha[-1] == '{':
                espera = True
            i += 1


_ZONAS = {}


def zonas_nossas(texto):
    """Os intervalos [a, b) de uma prova em cartões (página ou dados) onde o texto é nosso e pode levar espaços que não quebram."""
    chave = hash(texto)
    if chave in _ZONAS:
        return _ZONAS[chave]
    m = re.search(r'CARTOES=\[|"cartoes": \[', texto)
    fim, cartoes = _cartoes_com_posicoes(texto, m.end() - 1)
    nossas = []
    for c in cartoes:
        valor = lambda k: texto[c[k][0][0]:c[k][0][1]] if k in c else ''
        if valor('t') == 'ler':
            if valor('rot') != 'A prova':
                for a, b in c.get('html', []):
                    fora = sorted((a + x.start(), a + x.end()) for p in BLOCOS_OFICIAIS for x in p.finditer(texto[a:b]))
                    k = a
                    for x, y in fora:
                        if x > k:
                            nossas.append((k, x))
                        k = max(k, y)
                    nossas.append((k, b))
        else:
            campos = CAMPOS_NOSSOS + (() if OFICIAL_ROT.search(valor('rot')) else CAMPOS_DO_ENUNCIADO)
            nossas += [ab for k in campos for ab in c.get(k, [])]
        nossas += [ab for k in CAMPOS_DE_QUALQUER_CARTAO for ab in c.get(k, [])]
    # As citações entre «» ficam de fora.
    out = []
    for a, b in sorted(nossas):
        k = a
        for x in re.finditer(r'«[^«»]*»', texto[a:b]):
            if a + x.start() > k:
                out.append((k, a + x.start()))
            k = a + x.end()
        if b > k:
            out.append((k, b))
    _ZONAS[chave] = out
    return out


def _plano(s):
    """Texto simples, como tests/provas_casos.py o lê: sem etiquetas nem a marcação dos dados, espaços normalizados."""
    s = re.sub(r'<sup>\d+</sup>', '', s)
    s = re.sub(r'</?(?:i|b|em|strong|span|a|sub|small|cite)\b[^>]*>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'\[\^\d+\]', '', s).replace('**', '')
    s = re.sub(r'(?<![\w/])_([^_]+)_(?!\w)', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def _textos_da_transcricao(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from _textos_da_transcricao(y)
    elif isinstance(x, dict):
        for k, y in x.items():
            if not k.startswith('_') and 'nossa' not in k:
                yield from _textos_da_transcricao(y)


_CORPUS = {}


def corpus_oficial(rel):
    """O texto da prova e dos critérios, da transcrição conferida (tests/fixtures/prova-639-AAAA-Nf-vN.json), como
    tests/provas_casos.py o junta: o que lá está, letra a letra, é oficial."""
    pasta = re.search(r'\d{4}-\df', rel).group(0)
    if pasta not in _CORPUS:
        (fixture,) = sorted((ROOT / 'tests/fixtures').glob(f'prova-639-{pasta}-v*.json'))
        fx = json.loads(fixture.read_text('utf-8'))
        _CORPUS[pasta] = ' \n '.join(_plano(t) for t in _textos_da_transcricao({k: v for k, v in fx.items() if k != '_sobre'}))
    return _CORPUS[pasta]


def _segmento(texto, s):
    """O pedaço de texto à volta de s, entre etiquetas, aspas da cadeia JSON e «»: o que se lê de seguida."""
    a = s
    while a > 0 and texto[a - 1] not in '>«»' and not (texto[a - 1] == '"' and texto[a - 2] != '\\'):
        a -= 1
    b = s
    while b < len(texto) and texto[b] not in '<«»' and not (texto[b] == '"' and texto[b - 1] != '\\'):
        b += 1
    return texto[a:b].replace('\\"', '"').replace('\\n', ' ')


REGIOES_NOVAS = []


def fora_da_prova(texto, s):
    """Numa prova em cartões, a ocorrência em s só muda se estiver em texto nosso: num campo nosso de um cartão, fora dos blocos
    oficiais e das citações, e num pedaço que não esteja, letra a letra, na transcrição da prova e dos critérios."""
    if any(a <= s < b for a, b in REGIOES_NOVAS):
        return 'texto novo de um achado C desta página'
    if not any(a <= s < b for a, b in zonas_nossas(texto)):
        return 'texto oficial, citação, rótulo ou moldura de uma prova em cartões'
    if _plano(_segmento(texto, s)) in corpus_oficial(ATUAL):
        return 'pedaço que está, letra a letra, na transcrição da prova ou dos critérios'
    return None



# O que é próprio deste âmbito e não muda (a conferência deixou estas ocorrências de fora, com a razão em «fora»).
ATUAL = None


def _em_valor_de(texto, s, chave):
    """A posição s está no valor (texto ou lista) da última chave JSON com este nome antes de s."""
    k = texto.rfind(f'"{chave}":', 0, s)
    return k >= 0 and _fim_do_valor(texto, texto.index(':', k) + 1) > s


def _em_texto_de_apoio(texto, s):
    """A posição s está num parágrafo do texto de apoio de um aquecimento (<p class="pr">, na página e nos dados): é o texto da
    obra, ou o resumo que o acompanha, e fica como está."""
    a = texto.rfind('<p class=\\"pr\\"', 0, s)
    if a < 0:
        return False
    fins = [k for k in (texto.find('</p>', a), texto.find('<\\/p>', a)) if k >= 0]
    return bool(fins) and min(fins) > s


def fora_de_alcance(texto, s):
    """Porque é que a ocorrência em s não muda (ou None): os atributos que não se veem ou que não podem levar U+00A0 (alt,
    aria-label, href, title, src, o content da meta descrição e o data-titulo do vídeo, que vira title), o <title>, a «frase» de um
    sublinhar, as «palavras» de um cartão frase, os «passos» de um ordenar, o texto dos desenhos (SVG, que não muda de linha), os
    comentários e as notas internas dos dados («_nota»), como do M1 ao M9; e, neste âmbito, o texto de apoio dos aquecimentos
    (<p class="pr">) e, nas sessões do Exame (assets/exame/sessoes.json), as perguntas antigas («warmup», que a página não
    mostra e que tests/test_exame_alignment.py compara com as lições), o texto das obras (a chave «text») e os rótulos dos trechos
    de vídeo (video.clips[].label, que assets/exame/app.js também põe no title do vídeo); nas provas em
    cartões, tudo o que não é texto nosso (fora_da_prova)."""
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
    if _em_texto_de_apoio(texto, s):
        return 'texto de apoio de um aquecimento'
    if ATUAL and PROVA.match(ATUAL):
        return fora_da_prova(texto, s)
    if ATUAL == SESSOES:
        if _em_valor_de(texto, s, 'warmup'):
            return 'perguntas antigas da sessão (warmup), que a página não mostra'
        if _em_valor_de(texto, s, 'text'):
            return 'texto da obra (chave «text»)'
        if _em_valor_de(texto, s, 'clips') and _em_valor_de(texto, s, 'label'):
            return 'rótulo de um trecho de vídeo, que vira title'
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
        # Nas provas em cartões, as referências ligadas por vírgulas («Prova 639, 1.ª fase, 2026, versão 2») contam como uma só.
        if re.fullmatch(r'[\w\s.ºª–\-' + (',' if ATUAL and PROVA.match(ATUAL) else '') + NBSP + WJ + ']*', entre):
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
    texto = TEXTO_CAT['B'] + (' ' + x['nota_copia'] if x.get('nota_copia') else '')
    ts, final = trocas_de_janelas(rel, base_txt, pre, juntar(janelas), pares,
                                  lambda ks, i=x['i']: ACHADO.format(i=i, cat='B', texto=texto), local_b(rotulo or nome(rel)))
    return trocas + ts, final, regioes




def nome(rel):
    """O nome curto da página no manifesto."""
    m = re.match(r'exame/aquecimentos/s(\d+)/index\.html$', rel)
    if m:
        return f'Aquecimento da sessão {m.group(1)} do Exame'
    m = re.match(r'docs/pedagogia/exame-aquecimentos/s(\d+)\.json$', rel)
    if m:
        return f'Dados do aquecimento da sessão {m.group(1)} do Exame ({rel})'
    m = re.match(r'(?:exame/provas|scripts/provas/dados)/(\d{4})-(\d)f/grupo-([iv]+)(/index\.html|\.json)$', rel)
    if m:
        prova = f'Prova 639 de {m.group(1)}, {m.group(2)}.ª fase, Grupo {m.group(3).upper()}'
        return f'{prova} (cartões)' if m.group(4) != '.json' else f'Dados da {prova} ({rel})'
    if rel == 'index.html':
        return 'Entrada do Português (index.html)'
    return rel.replace('/index.html', '')


def trocas_pagina(rel, achados_ac, achados_b):
    global ATUAL
    ATUAL = rel
    base_txt = base(rel)
    pre, regioes, trocas, relatorio = base_txt, [], [], []
    for x in achados_ac:
        pre, regioes = substituir(pre, regioes, x['antigo'], x['novo'])
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}, {x["cartao"]}', 'antigo': x['antigo'], 'novo': x['novo'],
                       'ocorrencias': 1,
                       'achado': ACHADO.format(i=x['i'], cat=x['cat'], texto=TEXTO_CAT[x['cat']] + (' ' + x['nota'] if x.get('nota') else ''))})
        relatorio.append((rel, x['i'], x['cat'], 1, 1, ''))
    todos = [p for x in achados_b for p in x['pares']]
    REGIOES_NOVAS[:] = regioes if PROVA.match(rel) else []
    if PROVA.match(rel):
        achados_b = [dict(x, pares=pares_da_prova(pre, x)) for x in achados_b]
    for x in achados_b:
        ts, pre, regioes = b_da_pagina(rel, base_txt, pre, regioes, x, todos=todos)
        trocas += ts
        relatorio.append((rel, x['i'], 'B', sum(p[2] for p in x['pares']), sum(proposta(x).values()), ''))
    return base_txt, pre, trocas, relatorio


def pares_da_prova(pre, x):
    """Numa prova em cartões, cada par leva o número de ocorrências que estão em texto nosso (fora_da_prova), nunca mais do que
    as que a conferência contou: o par que desse mais fica de fora, na dúvida."""
    out = []
    for antigo, novo, n in x['pares']:
        c = len(ocorrencias(pre, antigo, novo, x['pares']))
        if 0 < c <= n:
            out.append((antigo, novo, c))
    return out


# Os aquecimentos do Exame são gerados (scripts/exame_aquecimentos.py) a partir dos bancos de docs/pedagogia/exame-aquecimentos:
# os pares de cada página mudam também no banco, com as mesmas regras, e a página sai igual do gerador (construir() confere-o).
AQUECIMENTO = re.compile(r'exame/aquecimentos/(s\d+)/index\.html$')


def dados_dos_aquecimentos():
    """Um achado por banco: os pares da página, contados no banco (o título da página e o do menu são da casca do gerador)."""
    global ATUAL
    out = []
    for x in ACHADOS_B:
        m = AQUECIMENTO.match(x['ficheiro'])
        if not m:
            continue
        rel = f'docs/pedagogia/exame-aquecimentos/{m.group(1)}.json'
        ATUAL = rel
        texto = base(rel)
        pares = [(a, n, len(ocorrencias(texto, a, n, x['pares']))) for a, n, _ in x['pares']]
        out.append(dict(i=x['i'], ficheiro=rel, pagina=x['ficheiro'], pares=[p for p in pares if p[2]],
                        nota_copia='Nos dados do gerador dos aquecimentos (scripts/exame_aquecimentos.py), que passam iguais para a página.'))
    for x in ACHADOS_B:
        if PROVA.match(x['ficheiro']):
            out.append(dict(i=x['i'], ficheiro=dados_da_prova(x['ficheiro']), pagina=x['ficheiro'], pares=x['pares'],
                            nota_copia='Nos dados do gerador das provas (scripts/provas/gerar.py), que passam iguais para a página.'))
    return out


def _por_pagina():
    por_pagina = {}
    for x in achados_ac():
        por_pagina.setdefault(x['ficheiro'], ([], []))[0].append(x)
    for x in ACHADOS_B + dados_dos_aquecimentos():
        por_pagina.setdefault(x['ficheiro'], ([], []))[1].append(x)
    return por_pagina


def construir_sem_conferir():
    for rel, (ac, bs) in sorted(_por_pagina().items()):
        try:
            trocas_pagina(rel, ac, bs)
        except SystemExit as erro:
            print('ERRO', rel, erro)


def conferir_geradores(finais):
    """As páginas geradas saem iguais dos geradores, a partir dos dados como a camada os deixa."""
    import exame_aquecimentos
    for x in dados_dos_aquecimentos():
        if PROVA.match(x['ficheiro']):
            continue
        banco = json.loads(finais[x['ficheiro']][1]) if x['ficheiro'] in finais else json.loads(base(x['ficheiro']))
        if exame_aquecimentos.pagina(banco) != finais[x['pagina']][1]:
            raise SystemExit(f'{x["pagina"]}: a página não sai igual do gerador dos aquecimentos')


def conferir_provas(finais):
    """As provas em cartões saem iguais do gerador (scripts/provas/gerar.py), a partir dos dados como a camada os deixa; as páginas
    que a camada não muda (e a secção exame/provas/) saem como estão."""
    spec = importlib.util.spec_from_file_location('provas_gerar', ROOT / 'scripts/provas/gerar.py')
    gerar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gerar)
    with tempfile.TemporaryDirectory() as tmp:
        dados = Path(tmp) / 'dados'
        shutil.copytree(ROOT / 'scripts/provas/dados', dados)
        for rel in sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'scripts/provas/dados').rglob('*.json')):
            (dados / rel.removeprefix('scripts/provas/dados/')).write_bytes((finais[rel][1] if rel in finais else base(rel)).encode('utf-8'))
        gerar.DADOS = dados
        saida, _ = gerar.gerar()
    for rel, (conteudo, _) in saida.items():
        if conteudo != (finais[rel][1] if rel in finais else base(rel)):
            raise SystemExit(f'{rel}: a página não sai igual do gerador das provas')


def construir():
    finais, relatorio = {}, []
    for rel, (ac, bs) in sorted(_por_pagina().items()):
        base_txt, final, trocas, rel_pag = trocas_pagina(rel, ac, bs)
        if trocas:
            finais[rel] = (base_txt, final, trocas)
        relatorio += rel_pag
    conferir_geradores(finais)
    conferir_provas(finais)
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
    ordem = sorted(finais, key=lambda r: (not r.startswith(('docs/', 'scripts/')), r))
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
