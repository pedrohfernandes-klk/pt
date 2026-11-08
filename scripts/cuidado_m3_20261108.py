#!/usr/bin/env python3
"""08/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M3 do Português.

Constrói scripts/cuidado_m3_20261108.json, a camada literal cuidado_m3_20261108, com os 44 achados CONFIRMADOS da varredura
de 6/11 (só leitura, com conferência independente) no M3: 10 achados A (9 tabelas onde há itens paralelos e a entrada ambígua do
vocabulário da F13), 31 de referências e números que se partiam (B) e 3 casos do mesmo tipo (C). Os 9 achados que a conferência
recusou (4, 6, 7, 8, 9, 10, 12, 13 e 21) não entram. A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em
tests/fixtures/cuidado-m3-edits-20261108.json:

  python3 scripts/cuidado_m3_20261108.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m3_20261108.json --manifesto tests/fixtures/cuidado-m3-edits-20261108.json --nota "…"

Segue o modelo das camadas do M1 e do M2 (scripts/cuidado_m1_20261106.py e scripts/cuidado_m2_20261108.py), com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como na M7-F10, na M7-F15, no M1 e no M2: class apoio-tabela, th scope=col
  no cabeçalho, th scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader, rowheader, cell),
  porque no telemóvel a tabela passa a display:block. Dentro do JSON dos cartões (e do baralho da F18, em
  assets/pt-lessons/m3-f18.js), as aspas vão com barra (\\"). Cada página com uma tabela nova carrega
  assets/pt-lessons/apoios-tabelas.css antes de assets/appearance.css, na versão do M1 (20261106.1: a folha não muda; fora das
  lições valem as regras que o M1 lá pôs). A F18 tem o baralho num ficheiro à parte, que só a lição M3-F18 carrega: a tabela entra
  no baralho e a folha na página da lição. Nas tabelas dos pesos (índice, guia e mapa), a coluna do peso só leva um número e fica
  estreita (5,5 rem; a primeira fica com o resto), e o rótulo («Pesos na avaliação:», «Avaliação:») fica num parágrafo antes da
  tabela, como no índice do M1 (a <caption> da proposta não tem estilo fora das lições e, no telemóvel, ficava espremida).
- B: U+00A0 (espaço que não quebra) em cada espaço de cada trecho do achado (canto e estância, «c.», «séc.», «t.», «n.º», «est.»,
  «vv.», «D.» e o nome, ordinal e nome, número e unidade, datas, intervalos «N a M» e «N e M»); U+2060 (junção de palavras) logo a
  seguir ao traço de intervalo, e o hífen entre anos passa a traço de intervalo («c. 1520-1540» > «c. 1520–1540»). Conta-se como a
  varredura: cada ocorrência uma vez, das sequências mais longas para as mais curtas, com a palavra inteira («I, 4» não conta
  dentro de «I, 4 e 5», de «VIII, 4…» nem de «I, 45»). Em «até 25 palavras» só se prende «25 palavras». Ficam de fora, mesmo
  quando a varredura os contou: os «alt» (e aria-label, href e <title>), a «frase» dos cartões sublinhar (as palavras contam-se por
  espaços) e a casca das lições (abaixo). O que outra camada já pôs dentro de <span class="nb"> com U+00A0 fica como está.
- C: na F05, os dois sentidos de «pena» na mesma entrada do vocabulário; na F10, a referência da estância sai do primeiro verso e
  do «cita» e passa ao título do cartão; na F13, os cartões das estâncias 97, 98 e 99 dizem a estância que mostram.
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois.

A casca das lições (migalhas «1.º ano», «Estás em: Lição M3-Fxx» e a sigla «Lição M3-Fxx» do rodapé) não muda aqui, ficheiro a
ficheiro: muda no molde, como no M1 e no M2. As fontes do rodapé (c-menu-extra) mudam, como no M1. Nas outras páginas (índice do
módulo, guia, mapa, portefólio, as páginas «Ler a fundo» e os dois exercícios longos «Pensar devagar»), as migalhas mudam porque
o achado da página as inclui, como no M2.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas, as correções dos achados C e da entrada da F13 (achado
11) e os espaços invisíveis. As trocas B não se sobrepõem: cada troca leva só os espaços que muda; quando o mesmo trecho aparece
noutro sítio que não muda, a troca leva o mínimo de contexto que a distingue. O script calcula as trocas sobre a base (a página
com esta camada desfeita pelo manifesto, quando ele já existe): pode voltar a correr depois de a camada estar aplicada e dá o
mesmo JSON.

Páginas geradas: as tarefas da M3-U1 e da M3-U2 (scripts/tarefas_escolha.py) ganham «nao_partir» nos dados (os números do molde:
«90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) e os achados B nos textos dos dados
(docs/pedagogia/tarefas-escolha/m3-u1.json e m3-u2.json); os aquecimentos (scripts/aquecimentos.py) mudam nos dados
(docs/pedagogia/aquecimentos/m3-u1.json e m3-u2.json); as grelhas e a correção (scripts/grelhas_tarefas.py) mudam nos dados
(docs/pedagogia/grelhas-tarefas-20261027.json, só nas entradas m3-u1 e m3-u2), e o gerador ganha a chave «nao_partir» (os
intervalos dos níveis, «1 a 3», com espaço que não quebra). Os dados estão na mesma camada e as páginas regeneram-se sem diferenças.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m3_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m3-edits-20261108.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
ACHADO = '08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M3, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como na M7-F10, na M7-F15, no M1 e no M2).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo, e o hífen entre '
          'anos passa a traço de intervalo).'),
    'C': 'Caso do mesmo tipo.',
}

# A folha das tabelas de apoio, antes da camada de aparência (como na M7-F10, na M7-F15, no M1 e no M2), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
COM_TABELA = {
    'm3/licao-m3-f05/index.html': ('lição', [1]), 'm3/licao-m3-f09/index.html': ('lição', [2]),
    'm3/licao-m3-f13/index.html': ('lição', [3]), 'm3/licao-m3-f15/index.html': ('lição', [0]),
    'm3/licao-m3-f18/index.html': ('lição (a tabela está no baralho, assets/pt-lessons/m3-f18.js)', [5]),
    'm3/gram-modalidade/index.html': ('página «Ler a fundo»', [17]), 'm3/index.html': ('índice do módulo', [18]),
    'm3/guia-da-tarefa-m3/index.html': ('guia da tarefa', [19]), 'm3/mapa-do-modulo-m3/index.html': ('mapa do módulo', [20]),
}
# A coluna que só leva um número (o peso) fica estreita; a primeira fica com o resto (a regra da folha dava-lhe 60 %).
ESTREITA = ' style="width:5.5rem"'
LARGA = ' style="width:auto"'


def tabela(colunas, linhas, json_=True, caption=None, larguras=None):
    """A tabela de apoio, igual às do M1 e do M2: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label com
    o nome da coluna, e os role. Com json_, as aspas vão escapadas como no JSON dos cartões."""
    larguras = larguras or [''] * len(colunas)
    cab = ''.join(f'<th scope="col" role="columnheader"{w}>{c}</th>' for c, w in zip(colunas, larguras))
    corpo = ''
    for linha in linhas:
        corpo += '<tr role="row"><th scope="row" role="rowheader">' + linha[0] + '</th>'
        for k, v in enumerate(linha[1:], 1):
            corpo += f'<td role="cell" data-label="{colunas[k]}">{v}</td>'
        corpo += '</tr>'
    legenda = f'<caption>{caption}</caption>' if caption else ''
    html = (f'<table class="apoio-tabela" role="table">{legenda}<thead role="rowgroup"><tr role="row">{cab}</tr></thead>'
            f'<tbody role="rowgroup">{corpo}</tbody></table>')
    return html.replace('"', '\\"') if json_ else html


# Os pesos da avaliação (índice, guia e mapa): o parágrafo fica, sem a enumeração, a seguir à tabela.
PESOS = [['Tarefa da Unidade 1', '30' + NBSP + '%'], ['Tarefa da Unidade 2', '30' + NBSP + '%'], ['Provas rápidas', '10' + NBSP + '%'],
         ['Prova escrita', '30' + NBSP + '%']]
PESOS_ANTES = ' tarefa da Unidade 1, 30 %; tarefa da Unidade 2, 30 %; provas rápidas, 10 %; prova escrita, 30 %. '


def pesos(rotulo):
    # O rótulo fica num parágrafo antes da tabela, como no índice do M1, e não numa <caption>: fora das lições a folha comum não dá
    # estilo à legenda, e no telemóvel (tabela em bloco) ela ficava espremida numa coluna estreita. O parágrafo não leva a classe
    # avaliacao-tarefas, que continua a ser de um só parágrafo (tests/browser_revisao_tarefas_20261101.py).
    antigo = f'<p class="avaliacao-tarefas">{rotulo}:{PESOS_ANTES}'
    novo = (f'<p>{rotulo}:</p>' + tabela(['Componente', 'Peso'], PESOS, json_=False, larguras=[LARGA, ESTREITA])
            + '<p class="avaliacao-tarefas">')
    return antigo, novo


# Os 13 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte).
ACHADOS_AC = [
    dict(i=0, cat='A', ficheiro='m3/licao-m3-f15/index.html', cartao='cartão 4, Para entender («As três modalidades»)',
         nota='«Modalidade» passa ao cabeçalho da coluna; «Marcas: …» fica num parágrafo a seguir.',
         antigo='<p><b>Modalidade epistémica</b>: grau de certeza (valor de certeza ou probabilidade: «talvez», «deve estar», «é certo '
                'que»). <b>Deôntica</b>: obrigação ou permissão («tem de», «pode sair»); o pedido e a ordem também são deônticos. '
                '<b>Apreciativa</b>: avaliação ou emoção do locutor («Infelizmente», «Que belo!»). Marcas: verbos modais, advérbios, '
                'adjetivos, modos verbais, tipos de frase.</p>',
         novo=tabela(['Modalidade', 'O que exprime', 'Exemplos'], [
             ['Epistémica', 'grau de certeza (valor de certeza ou probabilidade)', '«talvez», «deve estar», «é certo que»'],
             ['Deôntica', 'obrigação ou permissão; o pedido e a ordem também são deônticos', '«tem de», «pode sair»'],
             ['Apreciativa', 'avaliação ou emoção do locutor', '«Infelizmente», «Que belo!»']])
              + '<p>Marcas: verbos modais, advérbios, adjetivos, modos verbais, tipos de frase.</p>'),
    dict(i=1, cat='A', ficheiro='m3/licao-m3-f05/index.html', cartao='cartão 20, Para entender («Recorda»)',
         nota='«menor, de cinco» passa a «Redondilha menor» e «verso de cinco sílabas», só com palavras do próprio parágrafo.',
         antigo='<p><b>Medida velha</b>: os versos curtos da tradição peninsular. <b>Redondilha maior</b>: verso de sete sílabas; '
                '<b>menor</b>, de cinco. <b>Mote</b>: os versos de abertura, que dão o tema. <b>Voltas</b>: as estrofes que desenvolvem '
                'o mote e voltam ao seu último verso. <b>Hipérbole</b>: exagero que engrandece.</p>',
         novo=tabela(['Termo', 'O que é'], [
             ['Medida velha', 'os versos curtos da tradição peninsular'], ['Redondilha maior', 'verso de sete sílabas'],
             ['Redondilha menor', 'verso de cinco sílabas'], ['Mote', 'os versos de abertura, que dão o tema'],
             ['Voltas', 'as estrofes que desenvolvem o mote e voltam ao seu último verso'], ['Hipérbole', 'exagero que engrandece']])),
    dict(i=2, cat='A', ficheiro='m3/licao-m3-f09/index.html', cartao='cartão 20, Para entender («Recorda», primeira caixa)',
         nota='A segunda caixa («Como se representa a amada») é prosa e fica.',
         antigo='<p><b>Apóstrofe</b>: chamar alguém e falar-lhe, mesmo que não possa ouvir. <b>Antítese</b>: duas ideias opostas lado a '
                'lado. <b>Paralelismo</b>: a mesma construção repetida em dois versos. <b>Sujeito poético</b>: a voz que fala no poema.</p>',
         novo=tabela(['Termo', 'O que é'], [
             ['Apóstrofe', 'chamar alguém e falar-lhe, mesmo que não possa ouvir'], ['Antítese', 'duas ideias opostas lado a lado'],
             ['Paralelismo', 'a mesma construção repetida em dois versos'], ['Sujeito poético', 'a voz que fala no poema']])),
    dict(i=3, cat='A', ficheiro='m3/licao-m3-f13/index.html', cartao='cartão 22, Para entender («Recorda»)',
         antigo='<p><b>Reflexão do Poeta</b>: o narrador para a ação e fala em nome próprio. <b>Interrogação retórica</b>: pergunta que '
                'não espera resposta. <b>Metáfora</b>: dá a uma coisa o nome de outra. <b>Anáfora</b>: a mesma palavra a abrir versos '
                'seguidos.</p>',
         novo=tabela(['Termo', 'O que é'], [
             ['Reflexão do Poeta', 'o narrador para a ação e fala em nome próprio'], ['Interrogação retórica', 'pergunta que não espera resposta'],
             ['Metáfora', 'dá a uma coisa o nome de outra'], ['Anáfora', 'a mesma palavra a abrir versos seguidos']])),
    dict(i=5, cat='A', ficheiro='assets/pt-lessons/m3-f18.js', cartao='cartão 10, Quatro funções («Planos que se articulam»)',
         nota=('O baralho da F18 está neste ficheiro, que só a lição M3-F18 carrega; a folha das tabelas entra na página da lição. O <h3> '
               'e o parágrafo «Compara I, 19–20…» ficam.'),
         antigo='<p>A <b>viagem</b> acompanha os navegantes. A <b>história de Portugal</b> alarga o relato ao passado do povo. A '
                '<b>mitologia</b> introduz deuses e conflitos divinos. As <b>reflexões do Poeta</b> interrompem a ação para julgar.</p>',
         novo=tabela(['Plano', 'O que faz'], [
             ['Viagem', 'acompanha os navegantes'], ['História de Portugal', 'alarga o relato ao passado do povo'],
             ['Mitologia', 'introduz deuses e conflitos divinos'], ['Reflexões do Poeta', 'interrompem a ação para julgar']])),
    dict(i=11, cat='A', ficheiro='m3/licao-m3-f13/index.html', cartao='cartão 17, O texto, 5 de 5 (vocabulário: a entrada «Polidoro»)',
         nota=('A conferência recusou a tabela do vocabulário (é a convenção de todo o sítio) e aceitou a correção mínima da entrada '
               'ambígua: os quatro nomes a negrito e a lista fechada com «e».'),
         antigo='<b>Polidoro</b>, Rei Treício, Acriso, Tarpeia, exemplos antigos de crimes por dinheiro;',
         novo='<b>Polidoro</b>, <b>Rei Treício</b>, <b>Acriso</b> e <b>Tarpeia</b>, exemplos antigos de crimes por dinheiro;'),
    dict(i=14, cat='C', ficheiro='m3/licao-m3-f05/index.html', cartao='cartão 15, O texto, 4 de 4 (vocabulário: a entrada «pena»)',
         nota=('Os dois sentidos de «pena» na mesma entrada, na forma que o sítio já usa na página de estudo m3/camoes-perdigao, '
               'adaptada à vírgula do vocabulário em linha.'),
         antigo='<b>pena</b>, pluma; sofrimento;', novo='<b>pena</b>, pluma e sofrimento (duplo sentido);'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 2, O texto, 1 de 3: a referência sai do primeiro verso',
         antigo='<span class=\\"n\\"></span>I, 4 · E vós,', novo='<span class=\\"n\\"></span>E vós,'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 6, O texto, 2 de 3: a referência sai do primeiro verso',
         nota='Com «uma», para a troca ser única (há outro verso que começa por «Dai-me»).',
         antigo='<span class=\\"n\\"></span>I, 5 · Dai-me uma', novo='<span class=\\"n\\"></span>Dai-me uma'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 10, O texto, 3 de 3: a referência sai do primeiro verso',
         nota='Com o início do verso, para a troca ser única (o old_str da proposta acabava no espaço depois de «·»).',
         antigo='<span class=\\"n\\"></span>X, 145 · <b class=\\"gt\\" data-s=\\"não mais\\">Nô mais</b>',
         novo='<span class=\\"n\\"></span><b class=\\"gt\\" data-s=\\"não mais\\">Nô mais</b>'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 3, sublinhar: o «cita» sem a referência',
         antigo='"cita":"I, 4 · E vós, Tágides minhas, pois criado"', novo='"cita":"E vós, Tágides minhas, pois criado"'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 11, versos: o «cita» sem a referência',
         antigo='"cita":"X, 145 · Nô mais, Musa, nô mais, que a Lira tenho"', novo='"cita":"Nô mais, Musa, nô mais, que a Lira tenho"'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 2, O texto, 1 de 3: a estância no título',
         nota='O título «Duas invocações, dois tons» continua no cartão 14, «Em paralelo».',
         antigo='"rot":"O texto, 1 de 3","titulo":"Duas invocações, dois tons"',
         novo='"rot":"O texto, 1 de 3","titulo":"Canto' + NBSP + 'I,' + NBSP + '4"'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 6, O texto, 2 de 3: a estância no título',
         antigo='"rot":"O texto, 2 de 3","titulo":""', novo='"rot":"O texto, 2 de 3","titulo":"Canto' + NBSP + 'I,' + NBSP + '5"'),
    dict(i=15, cat='C', ficheiro='m3/licao-m3-f10/index.html', cartao='cartão 10, O texto, 3 de 3: a estância no título',
         antigo='"rot":"O texto, 3 de 3","titulo":""', novo='"rot":"O texto, 3 de 3","titulo":"Canto' + NBSP + 'X,' + NBSP + '145"'),
    dict(i=16, cat='C', ficheiro='m3/licao-m3-f13/index.html', cartao='cartão 12, O texto, 3 de 5: a estância no título',
         antigo='"rot":"O texto, 3 de 5","titulo":""', novo='"rot":"O texto, 3 de 5","titulo":"Canto' + NBSP + 'VIII,' + NBSP + '97"'),
    dict(i=16, cat='C', ficheiro='m3/licao-m3-f13/index.html', cartao='cartão 14, O texto, 4 de 5: a estância no título',
         antigo='"rot":"O texto, 4 de 5","titulo":""', novo='"rot":"O texto, 4 de 5","titulo":"Canto' + NBSP + 'VIII,' + NBSP + '98"'),
    dict(i=16, cat='C', ficheiro='m3/licao-m3-f13/index.html', cartao='cartão 17, O texto, 5 de 5: a estância no título',
         antigo='"rot":"O texto, 5 de 5","titulo":""', novo='"rot":"O texto, 5 de 5","titulo":"Canto' + NBSP + 'VIII,' + NBSP + '99"'),
    dict(i=17, cat='A', ficheiro='m3/gram-modalidade/index.html', cartao='passo 0, «Três frases, três tons» (a nota das três modalidades)',
         nota=('A tabela fica dentro de um div.nota, para guardar a letra pequena e o filete da nota; leva os role, como as do M1 fora '
               'das lições, porque a folha das tabelas a empilha no telemóvel.'),
         antigo='<p class=\\"nota\\"><b>epistémica</b>: grau de certeza (talvez, deve estar, é certo que)<br><b>deôntica</b>: obrigação, '
                'permissão, pedido, ordem (tem de, pode, dai-me)<br><b>apreciativa</b>: avaliação de quem fala (infelizmente, que '
                'belo!)</p>',
         novo='<div class=\\"nota\\">' + tabela(['Modalidade', 'O que marca', 'Exemplos'], [
             ['epistémica', 'grau de certeza', 'talvez, deve estar, é certo que'],
             ['deôntica', 'obrigação, permissão, pedido, ordem', 'tem de, pode, dai-me'],
             ['apreciativa', 'avaliação de quem fala', 'infelizmente, que belo!']]) + '</div>'),
    dict(i=18, cat='A', ficheiro='m3/index.html', cartao='secção «Como se cumpre uma unidade» (p.avaliacao-tarefas)',
         nota=('Só no M3 (este pedido é do M3); o resto do parágrafo fica no mesmo p.avaliacao-tarefas, que continua a ser um só dentro '
               'de details.regra.'),
         antigo=pesos('Pesos na avaliação')[0], novo=pesos('Pesos na avaliação')[1]),
    dict(i=19, cat='A', ficheiro='m3/guia-da-tarefa-m3/index.html', cartao='secção «Tarefas das unidades» (p.avaliacao-tarefas)',
         nota='Só no M3 (este pedido é do M3); o resto do parágrafo fica no mesmo p.avaliacao-tarefas.',
         antigo=pesos('Avaliação')[0], novo=pesos('Avaliação')[1]),
    dict(i=20, cat='A', ficheiro='m3/mapa-do-modulo-m3/index.html', cartao='secção «As tarefas do Teams» (p.avaliacao-tarefas)',
         nota='Só no M3 (este pedido é do M3); o resto do parágrafo fica no mesmo p.avaliacao-tarefas.',
         antigo=pesos('Avaliação')[0], novo=pesos('Avaliação')[1]),
]

# Os 31 achados B confirmados. Para cada um: as sequências da varredura, com as ocorrências que se mudam (cada ocorrência contada
# uma vez, das mais longas para as mais curtas). Onde o número não é o da varredura, «fora» diz porquê: o «alt», a «frase» de um
# sublinhar, a casca das lições (que fica para o molde), o que um achado A ou C já mudou, ou o que outra camada já tinha posto.
CASCA = 'a casca das lições (migalhas e sigla do «Estás em» e do rodapé) fica para o molde'
ALT = 'o «alt» não se vê; muda a legenda'
ACHADOS_B = [
    dict(i=22, ficheiro='m3/licao-m3-f02/index.html', ocorrencias=19,
         pares=[('I, 1 a 3', 5), ('D. Sebastião', 1), ('estância 3', 1), ('D. Manuel', 1), ('120 a 150', 1), ('c. 1577', 1), ('verso 6', 1),
                ('3 min', 2), ('1 min', 2)],
         fora={'1.º ano': (1, CASCA), 'M3-F02': (2, CASCA), 'c. 1577': (1, ALT)}),
    dict(i=23, ficheiro='m3/licao-m3-f03/index.html', ocorrencias=37,
         pares=[('estâncias 94 e 95', 1), ('estâncias 94', 2), ('D. Sebastião', 2), ('IV, 94 e 95', 6), ('D. Manuel I', 9), ('estância 95', 1),
                ('século XVI', 3), ('séc. XVI', 1), ('verso 2', 1), ('IV, 95', 3), ('IV, 94', 1), ('3 min', 4)],
         fora={'1.º ano': (1, CASCA), 'M3-F03': (2, CASCA)}),
    dict(i=24, ficheiro='m3/licao-m3-f04/index.html', ocorrencias=13,
         pares=[('120 a 150 palavras', 2), ('300 a 400 palavras', 2), ('80 a 100 palavras', 5), ('60 a 90 palavras', 1)],
         fora={'1.º ano': (1, CASCA), 'M3-F04': (2, CASCA)}),
    dict(i=25, ficheiro='m3/licao-m3-f05/index.html', ocorrencias=11,
         pares=[('versos 3 e 4', 1), ('t. III', 3), ('1 min', 4)],
         fora={'1.º ano': (1, CASCA), 'M3-F05': (2, CASCA)}),
    dict(i=26, ficheiro='m3/licao-m3-f09/index.html', ocorrencias=6,
         pares=[('soneto XIII', 1), ('c. 1577', 1)],
         fora={'1.º ano': (1, CASCA), 'M3-F09': (2, CASCA), 'c. 1577': (1, ALT)}),
    dict(i=27, ficheiro='m3/licao-m3-f10/index.html', ocorrencias=58,
         pares=[('300 a 400 palavras', 1), ('estâncias 4 e 5', 1), ('Canto I, 4 e 5', 3), ('canto VII, 78', 1), ('c. 1520-1540', 1),
                ('Canto X, 145', 3), ('D. Sebastião', 1), ('canto V, 97', 1), ('estância 5', 1), ('I, 4 e 5', 4), ('canto I', 5),
                ('canto X', 4), ('Canto I', 1), ('verso 7', 1), ('I, 4–5', 1), ('X, 145', 10), ('4 min', 2), ('I, 4', 5), ('I, 5', 3)],
         fora={'1.º ano': (1, CASCA), 'M3-F10': (2, CASCA), 'c. 1520-1540': (1, ALT),
               'X, 145': (2, 'o achado 15 (C) tira a referência do primeiro verso e do «cita» do cartão 11'),
               'I, 4': (2, 'o achado 15 (C) tira a referência do primeiro verso e do «cita» do cartão 3'),
               'I, 5': (1, 'o achado 15 (C) tira a referência do primeiro verso')}),
    dict(i=28, ficheiro='m3/licao-m3-f11/index.html', ocorrencias=22,
         pares=[('25 de novembro de 2019', 1), ('até 25 palavras', 3), ('25 de novembro', 1), ('artigo 13.º', 1), ('século XVI', 1),
                ('5 de maio', 7), ('1 min', 2), ('2 min', 2)],
         fora={'1.º ano': (1, CASCA), 'M3-F11': (2, CASCA), 'século XVI': (1, ALT)}),
    dict(i=29, ficheiro='m3/licao-m3-f13/index.html', ocorrencias=60,
         pares=[('estâncias 100 a 106', 2), ('Canto VIII, 96 a 99', 4), ('VIII, 96 a 99', 6), ('Canto I, 106', 4), ('estância 106', 2),
                ('estância 96', 1), ('estância 97', 1), ('estância 99', 1), ('canto VIII', 3), ('VIII, 96', 2), ('VIII, 97', 1),
                ('VIII, 98', 4), ('VIII, 99', 3), ('Canto I', 1), ('canto I', 3), ('I, 106', 15), ('4 min', 2), ('2 min', 2)],
         fora={'1.º ano': (1, CASCA), 'M3-F13': (2, CASCA)}),
    dict(i=30, ficheiro='m3/licao-m3-f15/index.html', ocorrencias=21,
         pares=[('estância 98', 2), ('estância 96', 1), ('VIII, 98', 4), ('c. 1560', 1), ('I, 106', 1), ('X, 145', 2), ('IX, 89', 1),
                ('V, 97', 1), ('2 min', 4)],
         fora={'1.º ano': (1, CASCA), 'M3-F15': (2, CASCA), 'c. 1560': (1, ALT)}),
    dict(i=31, ficheiro='m3/licao-m3-f16/index.html', ocorrencias=12,
         pares=[('30 segundos', 5), ('2 min', 2), ('4 min', 2)],
         fora={'1.º ano': (1, CASCA), 'M3-F16': (2, CASCA)}),
    dict(i=32, ficheiro='m3/licao-m3-f17/index.html', ocorrencias=21,
         pares=[('120 a 150 palavras', 4), ('300 a 400 palavras', 2), ('D. Sebastião', 1), ('300 a 400', 1), ('120 a 150', 1), ('c. 1560', 1),
                ('120–150', 1), ('t. III', 1), ('4 min', 2), ('2 min', 2), ('30 %', 1)],
         fora={'1.º ano': (1, CASCA), 'M3-F17': (2, CASCA), 'c. 1560': (1, ALT)}),
    dict(i=33, ficheiro='assets/pt-lessons/m3-f18.js', ocorrencias=32,
         pares=[('II, 109–110', 2), ('IV, 84–93', 2), ('canto III', 5), ('I, 19–20', 3), ('III, 3–5', 2), ('canto IV', 2), ('III, 1–5', 3),
                ('verso 1', 1), ('canto I', 1), ('III, 3', 1), ('I, 106', 1), ('I, 19', 5), ('4 min', 2), ('2 min', 2)]),
    dict(i=34, ficheiro='m3/index.html', ocorrencias=95,
         pares=[('25 de novembro de 2019', 3), ('300 a 400 palavras', 2), ('120 a 150 palavras', 1), ('80 a 100 palavras', 2),
                ('estâncias 98 e 99', 1), ('até 25 palavras', 2), ('VIII, 96 a 99', 2), ('VIII, 98 e 99', 1), ('D. Sebastião', 6),
                ('IV, 94 a 104', 1), ('IV, 94 e 95', 2), ('D. Manuel I', 4), ('90 segundos', 1), ('estância 96', 1), ('estância 99', 1),
                ('30 segundos', 3), ('90 minutos', 3), ('120 a 150', 1), ('vv. 3 e 4', 1), ('5 de maio', 4), ('I, 1 a 3', 2),
                ('I, 4 e 5', 2), ('VIII, 96', 1), ('VIII, 98', 1), ('1.º ano', 2), ('canto I', 1), ('canto X', 1), ('90 min', 4),
                ('20 min', 2), ('10 min', 2), ('I, 106', 4), ('X, 145', 9), ('IV, 94', 2), ('IV, 95', 4), ('IX, 89', 1), ('V, 97', 1),
                ('30 %', 2), ('I, 1', 2), ('I, 4', 2), ('I, 5', 4)],
         fora={'30 %': (3, 'o achado 18 (A) passa os pesos à tabela, já com o espaço que não quebra'),
               '10 %': (1, 'o achado 18 (A) passa os pesos à tabela, já com o espaço que não quebra')}),
    dict(i=35, ficheiro='m3/camoes-alma/index.html', ocorrencias=4, pares=[('soneto XIII', 3), ('1.º ano', 1)]),
    dict(i=36, ficheiro='m3/camoes-invocacoes/index.html', ocorrencias=15,
         pares=[('estância X, 145', 1), ('estância I, 4', 1), ('estância 145', 1), ('estância 4', 1), ('est. 145', 2), ('1.º ano', 1),
                ('canto I', 3), ('canto X', 3), ('est. 4', 2)]),
    dict(i=37, ficheiro='m3/camoes-leonor/index.html', ocorrencias=7, pares=[('n.º 37192', 3), ('1.º ano', 1), ('t. III', 3)]),
    dict(i=38, ficheiro='m3/camoes-mudanca/index.html', ocorrencias=3, pares=[('1.º ano', 1), ('t. II', 2)]),
    dict(i=39, ficheiro='m3/bicho-da-terra/index.html', ocorrencias=15,
         pares=[('Canto VIII, 98', 2), ('Canto I, 106', 2), ('VIII, 98', 5), ('1.º ano', 1), ('I, 106', 5)]),
    dict(i=40, ficheiro='m3/gram-modalidade/index.html', ocorrencias=5, pares=[('1.º ano', 1), ('I, 4', 4)]),
    dict(i=41, ficheiro='m3/m3-soneto-raciocinio/index.html', ocorrencias=12,
         pares=[('n.º 31509', 2), ('n.º 37192', 1), ('verso 12', 1), ('verso 11', 1), ('1.º ano', 1), ('verso 1', 3), ('verso 5', 1),
                ('verso 9', 1), ('20 min', 1)]),
    dict(i=42, ficheiro='m3/m3-velho-restelo-juri/index.html', ocorrencias=69,
         pares=[('estâncias 95 a 104', 1), ('estância IX, 92', 1), ('IV, 95 a 104', 1), ('estância 106', 1), ('estância 145', 1),
                ('estância 95', 2), ('estância 94', 1), ('estância 96', 1), ('estância 92', 1), ('estância 1', 1), ('canto VIII', 1),
                ('Canto IV', 1), ('canto IV', 7), ('est. 145', 1), ('VIII, 96', 2), ('canto IX', 3), ('1.º ano', 1), ('est. 94', 1),
                ('est. 95', 1), ('canto X', 8), ('canto I', 3), ('est. 92', 1), ('20 min', 1), ('IV, 95', 7), ('X, 145', 9), ('I, 106', 2),
                ('IV, 94', 2), ('IX, 92', 7)]),
    dict(i=43, ficheiro='m3/guia-da-tarefa-m3/index.html', ocorrencias=26,
         pares=[('300 a 400 palavras', 3), ('150 a 200 palavras', 2), ('80 a 120 palavras', 4), ('90 minutos', 1), ('10 minutos', 1),
                ('5 minutos', 1), ('300 a 400', 1), ('canto IV', 1), ('1.º ano', 2), ('10 min', 1), ('60 min', 1), ('15 min', 1), ('5 min', 1),
                ('30 %', 2)],
         fora={'30 %': (3, 'o achado 19 (A) passa os pesos à tabela, já com o espaço que não quebra'),
               '10 %': (1, 'o achado 19 (A) passa os pesos à tabela, já com o espaço que não quebra')}),
    dict(i=44, ficheiro='m3/portefolio-do-modulo-m3/index.html', ocorrencias=5,
         pares=[('90 minutos', 1), ('1.º ano', 2), ('0 a 20', 1), ('40 %', 1)]),
    dict(i=45, ficheiro='m3/mapa-do-modulo-m3/index.html', ocorrencias=26,
         pares=[('versos 1 e 2', 1), ('c. 1524–1580', 1), ('90 minutos', 3), ('século XVI', 1), ('1497–1499', 2), ('1.º ano', 2),
                ('canto I', 1), ('c. 1524', 1), ('canto X', 1), ('30 %', 2)],
         # O crédito do prato (no «i» da galeria) já está em <span class="nb"> com U+00A0 (camada creditos_i_20261105): só o hífen
         # passa a traço de intervalo, com a junção.
         nb=[('c.\xa01520-1540', 1)],
         fora={'30 %': (3, 'o achado 20 (A) passa os pesos à tabela, já com o espaço que não quebra'),
               '10 %': (1, 'o achado 20 (A) passa os pesos à tabela, já com o espaço que não quebra'),
               'século XVI': (1, ALT), 'c. 1520-1540': (1, ALT + '; o crédito do «i» já tinha U+00A0 e só muda o hífen (em «nb»)'),
               'c. 1577': (2, ALT + '; o crédito do «i» já tinha U+00A0 (camada creditos_i_20261105)'),
               'c. 1560': (2, ALT + '; o crédito do «i» já tinha U+00A0 (camada creditos_i_20261105)')}),
    dict(i=46, ficheiro='tarefas/m3-u1/index.html', ocorrencias=17,
         pares=[('200 a 240 palavras', 3), ('IV, 94 e 95', 1), ('D. Manuel I', 1), ('90 minutos', 2), ('10 minutos', 1), ('60 minutos', 1),
                ('15 minutos', 1), ('século XVI', 1), ('5 minutos', 1), ('80 a 120', 1), ('I, 1 a 3', 1), ('verso 3', 1), ('10 min', 1),
                ('90 min', 1)]),
    dict(i=47, ficheiro='tarefas/m3-u2/index.html', ocorrencias=27,
         pares=[('200 a 250 palavras', 2), ('VIII, 96 a 99', 1), ('VIII, 98 e 99', 1), ('IV, 95 a 104', 1), ('IV, 94 e 95', 1),
                ('90 minutos', 2), ('10 minutos', 1), ('60 minutos', 1), ('15 minutos', 1), ('5 minutos', 1), ('90 a 140', 1),
                ('I, 4 e 5', 2), ('VIII, 96', 2), ('VIII, 98', 1), ('VIII, 97', 2), ('verso 12', 1), ('10 min', 1), ('90 min', 1),
                ('X, 145', 3), ('IV, 94', 1)]),
    dict(i=48, ficheiro='tarefas/m3-u1/aquecimento/index.html', ocorrencias=2, pares=[('200 a 240 palavras', 1), ('200 a 240', 1)]),
    dict(i=49, ficheiro='tarefas/m3-u1/grelha/index.html', ocorrencias=7,
         pares=[('200 a 240 palavras', 1), ('I, 106', 1), ('1 a 3', 2), ('1 a 2', 2), ('1 a 5', 1)]),
    dict(i=50, ficheiro='tarefas/m3-u2/aquecimento/index.html', ocorrencias=17,
         pares=[('200 a 250 palavras', 1), ('estância I, 106', 1), ('I, 4 e 5', 1), ('VIII, 99', 1), ('canto I', 4), ('X, 145', 1),
                ('I, 106', 8)]),
    dict(i=51, ficheiro='tarefas/m3-u2/correcao/index.html', ocorrencias=1, pares=[('VIII, 98', 1)]),
    dict(i=52, ficheiro='tarefas/m3-u2/grelha/index.html', ocorrencias=20,
         pares=[('200 a 250 palavras', 1), ('VIII, 98', 2), ('I, 106', 9), ('IX, 92', 3), ('1 a 2', 2), ('1 a 3', 2), ('1 a 5', 1)]),
]

# A casca das lições fica para o molde, como no M1 e no M2: nenhuma troca. As lições onde a varredura a viu.
CASCA_NO_MOLDE = sorted(x['ficheiro'] for x in ACHADOS_B if x['ficheiro'].startswith('m3/licao-'))

# Dados dos geradores, com as sequências que lá estão (as das páginas, sem o que vem do molde dos geradores).
DADOS = [
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m3-u1.json', achados=(46,), nao_partir='\n "unidade": 1,\n',
         pares=[('200 a 240 palavras', 3), ('IV, 94 e 95', 1), ('D. Manuel I', 1), ('90 minutos', 1), ('10 minutos', 1), ('60 minutos', 1),
                ('15 minutos', 1), ('século XVI', 1), ('5 minutos', 1), ('80 a 120', 1), ('I, 1 a 3', 1), ('verso 3', 1)]),
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m3-u2.json', achados=(47,), nao_partir='\n "unidade": 2,\n',
         pares=[('200 a 250 palavras', 2), ('VIII, 96 a 99', 1), ('VIII, 98 e 99', 1), ('IV, 95 a 104', 1), ('IV, 94 e 95', 1),
                ('90 minutos', 1), ('10 minutos', 1), ('60 minutos', 1), ('15 minutos', 1), ('5 minutos', 1), ('90 a 140', 1),
                ('I, 4 e 5', 2), ('VIII, 96', 2), ('VIII, 98', 1), ('VIII, 97', 2), ('verso 12', 1), ('X, 145', 3), ('IV, 94', 1)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m3-u1.json', achados=(48,), pares=[('200 a 240 palavras', 1), ('200 a 240', 1)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m3-u2.json', achados=(50,),
         pares=[('200 a 250 palavras', 1), ('estância I, 106', 1), ('I, 4 e 5', 1), ('VIII, 99', 1), ('canto I', 4), ('X, 145', 1),
                ('I, 106', 8)]),
    dict(ficheiro='docs/pedagogia/grelhas-tarefas-20261027.json', entrada='m3-u1', achados=(49,),
         nao_partir='\n   "modulo": "M3",\n   "unidade": 1,\n', pares=[('200 a 240 palavras', 1), ('I, 106', 1)]),
    dict(ficheiro='docs/pedagogia/grelhas-tarefas-20261027.json', entrada='m3-u2', achados=(51, 52),
         nao_partir='\n   "modulo": "M3",\n   "unidade": 2,\n', pares=[('200 a 250 palavras', 1), ('VIII, 98', 2), ('I, 106', 9), ('IX, 92', 3)]),
    # O vídeo de Sá de Miranda da F17 (achado 32) vem de scripts/videos_escolhidos_pt.py: o título e o botão mudam nos dados (é o
    # único vídeo desses dados), e o script confere que a lição fica igual.
    dict(ficheiro='docs/pedagogia/videos-escolhidos-pt-20261028.json', achados=(32,), pares=[('2 min', 2)]),
]


def nao_parte(seq):
    """A forma que não se parte: cada espaço passa a U+00A0, o traço de intervalo leva U+2060 a seguir, e o hífen entre dois
    números passa a traço de intervalo, com a junção. Em «até 25 palavras», só se prende «25 palavras» (o «até» pode partir)."""
    if seq == 'até 25 palavras':
        return 'até 25' + NBSP + 'palavras'
    out = seq.replace(' ', NBSP)
    out = re.sub(r'(?<=\d)[-–](?=\d)', TRACO + WJ, out)
    return out


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
    intervalo. Mais nada é permitido num achado B."""
    i = j = 0
    out = []
    while i < len(antigo) or j < len(novo):
        if j < len(novo) and novo[j] == WJ and (i >= len(antigo) or antigo[i] != WJ):
            out.append((i, 'wj'))
            j += 1
        elif i < len(antigo) and j < len(novo) and antigo[i] == novo[j]:
            i += 1
            j += 1
        elif i < len(antigo) and j < len(novo) and antigo[i] == ' ' and novo[j] == NBSP:
            out.append((i, 'nbsp'))
            i += 1
            j += 1
        elif i < len(antigo) and j < len(novo) and antigo[i] == '-' and novo[j] == TRACO:
            out.append((i, 'traco'))
            i += 1
            j += 1
        else:
            raise SystemExit(f'achado B com uma mudança que não é de espaço nem de traço: {antigo!r} > {novo!r}')
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


def _frase_de_sublinhar(texto, s):
    """A posição s está no valor de «frase» de um cartão sublinhar (as palavras contam-se por espaços)."""
    k = texto.rfind('"frase":', 0, s)
    if k < 0:
        return False
    inicio = texto.index('"', k + len('"frase":')) + 1
    m = re.compile(r'(?<!\\)"').search(texto, inicio)
    if not m or m.start() < s:
        return False
    t = list(re.finditer(r'\{\s*"t":\s*"(\w+)"', texto[:k]))
    return bool(t) and t[-1].group(1) == 'sublinhar'


def _nota_interna(texto, s):
    """A posição s está no valor de uma chave JSON que começa por «_» (as notas internas dos dados, que não se publicam)."""
    i = s
    while i > 0:
        i -= 1
        if texto[i] == '"' and texto[i - 1] != '\\':
            break
    return re.search(r'"_\w+"\s*:\s*$', texto[max(0, i - 40):i]) is not None


def fora_de_alcance(texto, s):
    """Porque é que a ocorrência em s não muda (ou None): os atributos que não se veem ou que não podem levar U+00A0, o <title>,
    a «frase» de um sublinhar e as notas internas dos dados («_nota»)."""
    if _nota_interna(texto, s):
        return 'nota interna dos dados'
    attr = _atributo(texto, s)
    if attr in ('alt', 'aria-label', 'href', 'title', 'src'):
        return 'atributo ' + attr
    if texto.rfind('<title>', 0, s) > texto.rfind('</title>', 0, s):
        return '<title>'
    if _frase_de_sublinhar(texto, s):
        return 'frase de um sublinhar'
    return None


def _palavra_inteira(texto, s, e, seq):
    antes, depois = texto[s - 1:s], texto[e:e + 1]
    return not ((seq[0].isalnum() and antes.isalnum()) or (seq[-1].isalnum() and depois.isalnum()))


def ocorrencias(rel, texto, pares, regioes, limite=None):
    """As ocorrências de cada sequência em texto, das mais longas para as mais curtas, com a palavra inteira, sem as que estão
    dentro de uma ocorrência já contada nem as que estão fora de alcance. Devolve {sequência: [(início, fim)]} e as que ficaram de
    fora, com a razão."""
    usados, achadas, fora = [], {}, []
    for seq in sorted(dict.fromkeys(pares), key=lambda x: -len(x)):
        achadas[seq] = []
        for m in re.finditer(re.escape(seq), texto):
            s, e = m.start(), m.end()
            if limite and not (limite[0] <= s and e <= limite[1]):
                continue
            if not _palavra_inteira(texto, s, e, seq) or any(a <= s < b or a < e <= b for a, b in usados):
                continue
            razao = fora_de_alcance(texto, s)
            if razao:
                fora.append((seq, s, razao))
                usados.append((s, e))
                continue
            if any(a <= s < b or a < e <= b for a, b in regioes):
                raise SystemExit(f'{rel}: «{seq}» dentro do texto novo de um achado A/C')
            achadas[seq].append((s, e))
            usados.append((s, e))
    return achadas, fora


def janelas_b(rel, pre, pares, regioes, limite=None):
    """As janelas das ocorrências dos pares (sequência, nova, n) em pre (a base com as trocas A e C já feitas): [início, fim,
    {edições}, índice do par]. Cada sequência tem de aparecer exatamente n vezes (contadas como a varredura, sem o que fica de
    fora)."""
    achadas, _ = ocorrencias(rel, pre, [p[0] for p in pares], regioes, limite)
    janelas = []
    for k, (antigo, novo, esperado) in enumerate(pares):
        eds_rel = edicoes(antigo, novo)
        lista = achadas[antigo]
        if len(lista) != esperado:
            raise SystemExit(f'{rel}: «{antigo}» aparece {len(lista)} vez(es), e o achado conta {esperado}')
        for s, e in lista:
            janelas.append([s, e, {(s + p, t) for p, t in eds_rel}, k])
    return janelas


def juntar(janelas):
    """Junta as janelas que partilham uma edição ou em que uma tem uma edição da outra lá dentro: uma troca nunca leva uma edição
    de outra."""
    janelas = sorted(janelas)
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
    """Uma troca por texto de janela; quando esse texto aparece noutro sítio que não muda, a janela cresce para os dois lados
    (sem apanhar edições de outras janelas) até ficar única para as suas ocorrências. Devolve (trocas, texto final)."""
    todas = set().union(*[j[2] for j in janelas]) if janelas else set()
    final = aplicar_edicoes(pre, todas)
    grupos = {}
    for s, e, eds, k in janelas:
        grupos.setdefault((k, pre[s:e]), []).append((s, e, eds))
    trocas = []
    for (k, _), membros in sorted(grupos.items(), key=lambda g: (g[0][0], g[1][0][0])):
        for antigo, novo, n in _contexto(rel, base_txt, pre, final, membros, todas):
            trocas.append({'ficheiro': rel, 'local': local(k, pares[k][0], antigo), 'antigo': antigo, 'novo': novo,
                           'ocorrencias': n, 'achado': achado(k)})
    return trocas, final


def _contexto(rel, base_txt, pre, final, membros, todas):
    # Por fim, a linha inteira (nos dados dos geradores, cada texto está numa linha).
    for L, R in [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (2, 0), (2, 2), (0, 4), (4, 0), (4, 4), (8, 8), (16, 16), (32, 32),
                 (64, 64)] + [('linhas', n) for n in range(0, 8)]:
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
    m = re.match(r'(?:m3/licao-(m3-f\d+)/|assets/pt-lessons/(m3-f\d+)\.js)', rel)
    if m:
        return (m.group(1) or m.group(2)).upper() + (' (baralho)' if rel.startswith('assets/') else '')
    return rel.replace('/index.html', '')


def substituir(pre, regioes, antes, depois):
    """Troca um trecho único e atualiza as regiões de texto novo (onde nenhum par B pode cair)."""
    if pre.count(antes) != 1:
        raise SystemExit(f'trecho que não aparece uma vez: {antes[:80]!r}')
    inicio = pre.index(antes)
    delta = len(depois) - len(antes)
    regioes = [(a if a < inicio else a + delta, b if b <= inicio else b + delta) for a, b in regioes]
    return pre.replace(antes, depois), regioes + [(inicio, inicio + len(depois))]


def pares_de(x):
    return [(seq, nao_parte(seq), n) for seq, n in x['pares']]


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
        tipo, quais = COM_TABELA[rel]
        ligacoes = re.findall(r'<link rel="stylesheet" href="((?:\.\./)+)assets/appearance\.css\?v=[^"]+">', pre)
        if len(ligacoes) != 1:
            raise SystemExit(f'{rel}: a ligação à camada de aparência não aparece uma vez')
        aparencia = re.search(r'<link rel="stylesheet" href="(?:\.\./)+assets/appearance\.css\?v=[^"]+">', pre).group(0)
        folha = FOLHA.format(ligacoes[0])
        pre, regioes = substituir(pre, regioes, aparencia, folha + aparencia)
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}, cabeça: a folha das tabelas de apoio, antes da camada de aparência',
                       'antigo': aparencia, 'novo': folha + aparencia, 'ocorrencias': 1,
                       'achado': ACHADO.format(i=', '.join(map(str, quais)), cat='A',
                                               texto=f'A {tipo} passa a carregar as tabelas de apoio, antes da camada de aparência.')})
    for x in achados_b:
        pares = pares_de(x) + [(seq, seq.replace('-', TRACO + WJ), n) for seq, n in x.get('nb', [])]
        janelas = janelas_b(rel, pre, pares, regioes)
        ts, final = trocas_de_janelas(rel, base_txt, pre, juntar(janelas), pares,
                                      lambda k, i=x['i']: ACHADO.format(i=i, cat='B', texto=TEXTO_CAT['B']), local_b(nome(rel)))
        pre = final
        trocas += ts
        relatorio.append((rel, x['i'], 'B', sum(n for _, _, n in pares), x['ocorrencias'], ''))
    return base_txt, pre, trocas, relatorio


def trocas_dados(specs):
    """As trocas de um ficheiro de dados (uma ou mais entradas): «nao_partir» onde o gerador o lê, e os achados B nos textos."""
    rel = specs[0]['ficheiro']
    base_txt = base(rel)
    pre, regioes, trocas = base_txt, [], []
    for spec in specs:
        if spec.get('nao_partir'):
            antes = spec['nao_partir']
            depois = antes + (' "nao_partir": true,\n' if 'entrada' not in spec else '   "nao_partir": true,\n')
            pre, regioes = substituir(pre, regioes, antes, depois)
            if 'entrada' in spec:
                o_que = ('Os intervalos dos níveis da grelha («1 a 3») levam o espaço que não quebra pelo gerador '
                         '(scripts/grelhas_tarefas.py).')
                local = f'Dados das grelhas, {spec["entrada"]}: «nao_partir», os intervalos dos níveis com espaço que não quebra'
            else:
                o_que = ('Os números do molde da tarefa («90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) levam o '
                         'espaço que não quebra pelo gerador (scripts/tarefas_escolha.py).')
                local = 'Dados da tarefa: «nao_partir», os números do molde com espaço que não quebra'
            trocas.append({'ficheiro': rel, 'local': local, 'antigo': antes, 'novo': depois, 'ocorrencias': 1,
                           'achado': ACHADO.format(i='/'.join(map(str, spec['achados'])), cat='B', texto=TEXTO_CAT['B'] + ' ' + o_que)})
    janelas, pares, nomes = [], [], []
    for spec in specs:
        limite = None
        if 'entrada' in spec:
            inicio = pre.index(f'\n  "{spec["entrada"]}": {{')
            fim = pre.find('\n  "', inicio + 5)
            limite = (inicio, fim if fim > 0 else len(pre))
        ps = [(seq, nao_parte(seq), n) for seq, n in spec['pares']]
        js = janelas_b(rel, pre, ps, regioes, limite)
        for j in js:
            j[3] += len(pares)
        janelas += js
        pares += ps
        nomes += [(spec.get('entrada'), '/'.join(map(str, spec['achados'])))] * len(ps)
    rotulo = 'Dados ' + '/'.join(Path(rel).parts[-2:])
    ts, final = trocas_de_janelas(
        rel, base_txt, pre, juntar(janelas), pares,
        lambda k: ACHADO.format(i=nomes[k][1], cat='B', texto=TEXTO_CAT['B'] + ' Nos dados do gerador, que passam iguais para as páginas.'),
        lambda k, par, antigo: local_b(rotulo + (f', {nomes[k][0]}' if nomes[k][0] else ''))(k, par, antigo))
    return base_txt, final, trocas + ts


def cartoes_de(texto):
    """Os cartões de uma lição (CARTOES=[…])."""
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0] if m else None


# Os enunciados dos painéis do docente (m3/painel-m3-fxx) são os dos cartões da lição: o «p» (ou a «frase»), com ou sem os
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
    for licao in sorted(r for r in finais if r.startswith('m3/licao-')):
        painel = licao.replace('/licao-', '/painel-')
        if not (ROOT / painel).is_file():
            continue
        base_txt = base(painel)
        itens = cartoes_de(base_txt)
        if itens is None:
            continue
        antes, depois = cartoes_de(finais[licao][0]), cartoes_de(finais[licao][1])
        i = next(x['i'] for x in ACHADOS_B if x['ficheiro'] == licao)
        pre, trocas = base_txt, []
        for item in itens:
            k = item['k']
            f = next((f for f in ENUNCIADOS if f(antes[k]) == item['p']), None)
            if f is None or f(depois[k]) == item['p']:
                continue
            novo = dict(item, p=f(depois[k]))
            # No seletor, alguns enunciados estão cortados: o corte fica no mesmo sítio do texto.
            # O seletor mostra o enunciado sem os marcadores de itálico (_…_), quando os há.
            opcao = re.search(r'<option value="%d">([^<]*)</option>' % k, pre).group(1)
            g = next((g for g in (lambda x: x, lambda x: re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', x))
                      if html.escape(g(item['p']), quote=False).startswith(opcao)), None)
            if g is None:
                raise SystemExit(f'{painel}: o seletor do cartão {k} não é o enunciado do painel')
            novo_esc = html.escape(g(novo['p']), quote=False)
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
            out[painel] = (base_txt, pre, trocas)
    return out


def construir():
    por_pagina = {}
    for x in ACHADOS_AC:
        por_pagina.setdefault(x['ficheiro'], ([], []))[0].append(x)
    for x in ACHADOS_B:
        por_pagina.setdefault(x['ficheiro'], ([], []))[1].append(x)
    for rel in COM_TABELA:
        por_pagina.setdefault(rel, ([], []))
    finais, relatorio = {}, []
    for rel in sorted(por_pagina):
        ac, bs = por_pagina[rel]
        base_txt, final, trocas, rel_pag = trocas_pagina(rel, ac, bs)
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
    return [t for rel in finais for t in finais[rel][2]], relatorio, len(finais)


def main():
    todas, relatorio, n = construir()
    if '--relatorio' in sys.argv:
        for r in relatorio:
            print(*r)
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {n} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
