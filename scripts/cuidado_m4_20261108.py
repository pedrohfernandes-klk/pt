#!/usr/bin/env python3
"""08/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M4 do Português.

Constrói scripts/cuidado_m4_20261108.json, a camada literal cuidado_m4_20261108, com os 38 achados CONFIRMADOS da varredura
de 6/11 (só leitura, com conferência independente) no M4: 6 achados A (tabelas onde há itens paralelos), 29 de referências e
números que se partiam (B) e 3 casos do mesmo tipo (C). Os 9 achados que a conferência recusou (5, 6, 7, 8, 9, 10, 11, 12 e 17)
não entram. A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/cuidado-m4-edits-20261108.json:

  python3 scripts/cuidado_m4_20261108.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m4_20261108.json --manifesto tests/fixtures/cuidado-m4-edits-20261108.json --nota "…"

Segue o modelo das camadas do M1, do M2 e do M3 (scripts/cuidado_m1_20261106.py, cuidado_m2_20261108.py e cuidado_m3_20261108.py),
com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como na M7-F10, na M7-F15, no M1, no M2 e no M3: class apoio-tabela, th
  scope=col no cabeçalho, th scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader, rowheader,
  cell), porque no telemóvel a tabela passa a display:block. Dentro do JSON dos cartões, as aspas vão com barra (\\"). Cada página
  com uma tabela nova carrega assets/pt-lessons/apoios-tabelas.css antes de assets/appearance.css, na versão do M1 (20261106.1: a
  folha não muda; as regras do cartão escuro «Para levar», que a varredura pedia para a F06 e a F25, e as de fora das lições já lá
  estão desde o M1). Nas duas listas «As frases da aula» (F06 e F25), a lista fecha antes da tabela e reabre a seguir com start, e
  a tabela leva a legenda da proposta (nas lições, a folha dá estilo à <caption>). No guia da tarefa (fora das lições), a tabela do
  guião de exemplo fica dentro de um div.ex, para guardar a letra do exemplo, e a primeira coluna (a parte do guião, uma palavra)
  fica estreita; a proposta da conferência pedia uma tabela sem a classe apoio-tabela e com estilo próprio na página: usa-se a
  classe, como nas outras tabelas novas, porque a folha das tabelas já tem as regras de fora das lições (desde o M1).
- B: U+00A0 (espaço que não quebra) nos espaços que a proposta final prende (capítulo, ato e cena com o número romano, «séc.»,
  «c.», «n.º», «§», ordinal e nome, número e unidade, datas, intervalos «N a M palavras», «aula» e «aulas» com o número);
  U+2060 (junção de palavras) logo a seguir ao traço de intervalo e ao hífen da sigla «M4-Fxx», e o hífen entre anos passa a traço
  de intervalo («c. 1535-1540» > «c. 1535–1540»). Como na proposta, há espaços que ficam: nas datas, entre o mês e o «de» do ano
  («13 de junho de 1654»), nas listas, à volta das vírgulas e antes do «e» («caps. II e III», «cenas I, XIV e XV»), e em «aulas 1
  a 8», antes do «a». Conta-se como a varredura: cada ocorrência uma vez, das sequências mais longas para as mais curtas, com a
  palavra inteira («ato I» não conta dentro de «ato II», nem «aula 1» dentro de «aula 10»). Mudam todas as ocorrências que se veem,
  também na linha «Hoje» do cartão de abertura, no cartão extra do fim, nas pistas («Pista») e nas fontes do rodapé
  (c-menu-extra), que a varredura às vezes contou à parte. Ficam de fora: os «alt» (e aria-label, href, title, content e
  data-titulo), o <title>, o texto dos desenhos (SVG, que não muda de linha), a «frase» dos cartões sublinhar (as palavras contam-se
  por espaços) e a casca das lições (abaixo). O que outra camada já pôs com U+00A0 (os créditos do «i») fica como está; nos que
  estão em <span class="nb">, só o hífen passa a traço de intervalo, com a junção. No vídeo da F01 e da F10, além do botão, muda
  o data-dur, de onde assets/pt-lessons/aula-clara.js refaz o botão depois de se ver o vídeo.
- C: na F10, «O que conta» do cartão 3 passa a lista, como nos outros cartões; no mapa, cada termo fica junto da sua definição; no
  portefólio, os nomes dos ficheiros vão todos em <code>, sem partir, e os cabeçalhos ganham scope.
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois.

A casca das lições (migalhas «2.º ano», «Estás em: Lição M4-Fxx», o título escondido «Lição M4-Fxx» e a sigla «Lição M4-Fxx» do
rodapé) não muda aqui, ficheiro a ficheiro: muda no molde, como no M1, no M2 e no M3. As fontes do rodapé (c-menu-extra) mudam,
como no M1. Nas outras páginas (índice do módulo, guia, mapa, portefólio e os dois exercícios longos «Pensar devagar»), as
migalhas mudam porque o achado da página as inclui, como no M2 e no M3.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e das listas, as correções que a proposta final faz
(achados 0, 1, 2, 3, 13, 14 e 15) e os espaços invisíveis. As trocas B não se sobrepõem: cada troca leva só os espaços que muda;
quando o mesmo trecho aparece noutro sítio que não muda, a troca leva o mínimo de contexto que a distingue. O script calcula as
trocas sobre a base (a página com esta camada desfeita pelo manifesto, quando ele já existe): pode voltar a correr depois de a
camada estar aplicada e dá o mesmo JSON.

Páginas geradas: os aquecimentos da M4-U1, da M4-U2 e da M4-U3 (discurso) (scripts/aquecimentos.py) mudam nos dados
(docs/pedagogia/aquecimentos/m4-u1.json, m4-u2.json e m4-u3-discurso.json), na mesma camada, e regeneram-se sem diferenças. Os
painéis do docente (m4/painel-m4-fxx) seguem os enunciados dos cartões das lições. As tarefas das unidades do M4 (tarefas/m4-u*)
não têm gerador (não estão em docs/pedagogia/tarefas-escolha) e mudam na página.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m4_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m4-edits-20261108.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
CONTAR = None
ACHADO = '08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M4, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como na M7-F10, na M7-F15, no M1, no M2 e no M3).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e ao hífen da sigla, '
          'e o hífen entre anos passa a traço de intervalo).'),
    'C': 'Caso do mesmo tipo.',
}

# A folha das tabelas de apoio, antes da camada de aparência (como na M7-F10, na M7-F15, no M1, no M2 e no M3), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
COM_TABELA = {
    'm4/licao-m4-f06/index.html': ('lição', [2]), 'm4/licao-m4-f10/index.html': ('lição', [0, 3]),
    'm4/licao-m4-f14/index.html': ('lição', [4]), 'm4/licao-m4-f25/index.html': ('lição', [1]),
    'm4/guia-da-tarefa-m4/index.html': ('guia da tarefa', [13]),
}
# No guia (fora das lições), a regra da folha dava 60 % à primeira de duas colunas (a dos pesos do M1); a parte do guião é uma
# palavra e fica estreita, e o texto fica com o resto.
ESTREITA = ' style="width:25%"'
LARGA = ' style="width:auto"'
# Na F06, o nome do ato mais comprido («Compromissivo») não cabia nos 25 % da primeira coluna e partia-se a meio no ecrã largo (as
# lições trazem th,td{overflow-wrap:anywhere}): a coluna leva uma largura em em, que cresce com a letra (também na projeção).
ATO = ' style="width:11em"'


def tabela(colunas, linhas, json_=True, caption=None, larguras=None):
    """A tabela de apoio, igual às do M1, do M2 e do M3: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label
    com o nome da coluna, e os role. Com json_, as aspas vão escapadas como no JSON dos cartões."""
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


# As linhas das tabelas novas (o texto de cada célula, na forma da fonte, com U+00A0 onde o achado B da página o pede).
PEIXES_F10 = [['Roncadores', 'pequenos e barulhentos, «as roncas do mar»', 'fazer mais ruído do que se vale'],
              ['Pegadores', '«nunca os desferram»', 'viver à custa de quem tem poder'],
              ['Voadores', '«porque vos quereis ser aves?»', 'querer ser mais do que se é'],
              ['Polvo', '«parece» manso e ataca de emboscada', 'trair com cara de bondade']]
PEIXES_F25 = [['Roncadores', 'pequenos e barulhentos, «as roncas do mar»', 'barulho sem valor'],
              ['Pegadores', '«nunca os desferram» e vivem à custa do maior', 'viver à custa dos poderosos'],
              ['Voadores', 'querem ser aves, e ao voador «mata-o a vaidade de voar»', 'presunção'],
              ['Polvo', '«parece um monge» e ataca de emboscada', 'traição com cara mansa']]
ATOS_F06 = [['Assertivo', 'afirma, e pode ser verdadeiro ou falso', '«os grandes comem os pequenos»'],
            ['Diretivo', 'leva quem ouve a fazer alguma coisa; obriga quem ouve', '«Olhai, peixes»; «traz-me»'],
            ['Expressivo', 'mostra o que sente quem fala', '«Oh…!»; «Quem me dera…»'],
            ['Compromissivo', 'obriga quem fala', '«trago-te»'],
            ['Declarativo', 'muda a realidade quando o diz quem tem autoridade; não é o mesmo que frase declarativa',
             '«Declaro eleita delegada de turma a Marta.»']]
AULAS_F10 = [['aula' + NBSP + '1', '«Mudou somente o púlpito e o auditório, mas não desistiu da doutrina»; «faltou pouco, para que lhe '
              'não tirassem a vida»'],
             ['aulas' + NBSP + '2 e' + NBSP + '4', '«os ouvintes, sendo verdadeira a doutrina que lhes dão, a não querem receber»'],
             ['aula' + NBSP + '3', '«para a cidade é que haveis de olhar»'],
             ['aula' + NBSP + '4', '«Ao menos têm os peixes duas boas qualidades de ouvintes: ouvem e não falam»'],
             ['aula' + NBSP + '5', '«A vossa bruteza é melhor que a minha razão»'],
             ['aulas' + NBSP + '5 e' + NBSP + '6', '«Oh que boa doutrina era esta para a terra, se eu não pregara para o mar!»']]
PLANO_F14 = [['Regra', 'comemos todos à mesma mesa, três vezes por dia, à mesma hora.'],
             ['Argumento' + NBSP + '1', 'a comida chega para todos se for repartida às claras; ontem à noite a caixa das bolachas ficou '
              'vazia e hoje de manhã ninguém sabia quem as tinha comido.'],
             ['Argumento' + NBSP + '2', 'à mesa fala-se; a discussão de terça sobre o gerador acabou ao jantar, com toda a gente sentada.'],
             ['Objeção', '«E quem tem fome fora de horas?»'],
             ['Resposta', 'cada um guarda uma peça de fruta com o seu nome na prateleira; ninguém passa fome, só não se come o que é '
              'dos outros.'],
             ['Apelo', 'votem a mesa comum.']]
GUIAO_GUIA = [['Abertura', '«Quem aqui já viu alguém subir agarrado a outro?»'],
              ['Vieira', 'no capítulo' + NBSP + 'V, repreende os pegadores: peixes pequenos que se colam aos grandes e vivem do que eles '
               'comem; o recurso é a antítese entre o grande que trabalha e o pequeno que só se agarra.'],
              ['Hoje', 'a conta que cresce a repetir o que outra conta diz, sem fazer nada de seu.'],
              ['Objeção', '«mas partilhar também é trabalho».'],
              ['Resposta', 'Vieira distingue quem nada ao lado de quem se cola; partilhar com nome e ideia própria é nadar ao lado.'],
              ['Fecho', 'a pergunta do princípio, agora com o peixe à vista.'],
              ['Imagens', 'a gravura do peixe, uma captura de ecrã sem nomes, a frase de Vieira.']]
# Os nove nomes de ficheiro do portefólio que não estavam em <code> (o registo da aula, a pergunta e o «o que aprendi» das três
# unidades).
NOMES_SEM_CODE = [f'M4_U{u}_{n}' for u in (1, 2, 3) for n in ('folha_&lt;dia-mês&gt;', 'pergunta', 'o-que-aprendi')]

# Os 9 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte).
ACHADOS_AC = [
    dict(i=0, cat='A', ficheiro='m4/licao-m4-f10/index.html', cartao='cartão 13, Recorda («Quatro peixes, quatro traços»)',
         nota='O «Antes de ler» diz «na tabela» em vez de «na lista». Sem legenda: o título do cartão já a nomeia.',
         antigo='Procura na lista a frase em que Vieira lhe pergunta porquê.</p><ul><li><b>Roncadores</b>: pequenos e barulhentos, '
                '«as roncas do mar»; fazer mais ruído do que se vale.</li><li><b>Pegadores</b>: «nunca os desferram»; viver à custa de '
                'quem tem poder.</li><li><b>Voadores</b>: «porque vos quereis ser aves?»; querer ser mais do que se é.</li><li><b>Polvo'
                '</b>: «parece» manso e ataca de emboscada; trair com cara de bondade.</li></ul>',
         novo='Procura na tabela a frase em que Vieira lhe pergunta porquê.</p>' + tabela(['Peixe', 'No texto', 'Traço'], PEIXES_F10)),
    dict(i=1, cat='A', ficheiro='m4/licao-m4-f25/index.html', cartao='cartão 17, Para levar (As frases da aula, itens 3 e 4)',
         nota=('Os vícios vêm do cartão 16 («O que conta», item 2) e a legenda do cartão 15; a lista fecha antes da tabela e reabre a '
               'seguir com start=3 (o item «Uma comparação de hoje…» fica o terceiro). O cartão é escuro: as regras do cartão escuro já '
               'estão na folha desde o M1.'),
         antigo='<li>Roncadores: pequenos e barulhentos, «as roncas do mar». Pegadores: «nunca os desferram» e vivem à custa do maior.</li>'
                '<li>Voadores: querem ser aves, e ao voador «mata-o a vaidade de voar». Polvo: «parece um monge» e ataca de emboscada.</li>',
         novo=('</ol>' + tabela(['Peixe', 'Traço e palavras', 'Vício dos homens'], PEIXES_F25,
                               caption='Quatro peixes repreendidos, quatro vícios') + '<ol start=\\"3\\">')),
    dict(i=2, cat='A', ficheiro='m4/licao-m4-f06/index.html', cartao='cartão 16, Para levar (As frases da aula, itens 2 a 5)',
         nota=('Os exemplos vêm do parágrafo do cartão e do cartão 8 (a frase da diretora de turma); o diretivo junta as duas '
               'explicações que a lista dava. A lista fecha antes da tabela e reabre a seguir com start=2 (o item «A forma não decide '
               'o ato» fica o segundo). O cartão é escuro: as regras do cartão escuro já estão na folha desde o M1. A primeira coluna '
               'leva 11em, para «Compromissivo» não se partir a meio no ecrã largo.'),
         antigo='<li>Assertivo: afirma, e pode ser verdadeiro ou falso. Diretivo: leva quem ouve a fazer alguma coisa.</li><li>Expressivo: '
                'mostra o que sente quem fala, como «Oh…!» ou «Quem me dera…».</li><li>Compromissivo: obriga quem fala («trago-te»); o '
                'diretivo obriga quem ouve («traz-me»).</li><li>Declarativo: muda a realidade quando o diz quem tem autoridade; não é o '
                'mesmo que frase declarativa.</li>',
         novo='</ol>' + tabela(['Ato', 'O que faz', 'Exemplo'], ATOS_F06, caption='Os cinco atos de fala', larguras=[ATO, '', ''])
              + '<ol start=\\"2\\">'),
    dict(i=3, cat='A', ficheiro='m4/licao-m4-f10/index.html', cartao='cartão 8, Decide (Ler mais: as passagens das aulas)',
         nota=('As duas passagens da aula 1 ficam na mesma célula, separadas por «;». «aula 1», «aulas 2 e 4»… já levam o espaço que '
               'não quebra (achado 25).'),
         antigo='<p>Passagens das aulas da unidade que servem a resposta: aula 1, «Mudou somente o púlpito e o auditório, mas não '
                'desistiu da doutrina» e «faltou pouco, para que lhe não tirassem a vida»; aulas 2 e 4, «os ouvintes, sendo verdadeira a '
                'doutrina que lhes dão, a não querem receber»; aula 3, «para a cidade é que haveis de olhar»; aula 4, «Ao menos têm os '
                'peixes duas boas qualidades de ouvintes: ouvem e não falam»; aula 5, «A vossa bruteza é melhor que a minha razão»; '
                'aulas 5 e 6, «Oh que boa doutrina era esta para a terra, se eu não pregara para o mar!».</p>',
         novo='<p>Passagens das aulas da unidade que servem a resposta:</p>' + tabela(['Aula', 'Passagem'], AULAS_F10)),
    dict(i=4, cat='A', ficheiro='m4/licao-m4-f14/index.html', cartao='cartão 16, Agora, em papel (Um exemplo)',
         nota='O enunciado pede o plano «em seis linhas, uma por peça»: cada peça numa linha; o texto fica igual, sem os rótulos.',
         antigo='<p>Regra: comemos todos à mesma mesa, três vezes por dia, à mesma hora. Argumento 1: a comida chega para todos se for '
                'repartida às claras; ontem à noite a caixa das bolachas ficou vazia e hoje de manhã ninguém sabia quem as tinha comido. '
                'Argumento 2: à mesa fala-se; a discussão de terça sobre o gerador acabou ao jantar, com toda a gente sentada. Objeção: «E '
                'quem tem fome fora de horas?» Resposta: cada um guarda uma peça de fruta com o seu nome na prateleira; ninguém passa '
                'fome, só não se come o que é dos outros. Apelo: votem a mesa comum.</p>',
         novo=tabela(['Peça', 'No exemplo'], PLANO_F14)),
    dict(i=13, cat='A', ficheiro='m4/guia-da-tarefa-m4/index.html',
         cartao='Tarefa 1 (arquivo), «Um exemplo: Os pegadores» (o guião da apresentação)',
         nota=('A tabela fica dentro de um div.ex, para guardar a letra do exemplo, e leva a classe apoio-tabela e os role, como as '
               'outras tabelas novas (a folha já tem as regras de fora das lições); a proposta pedia uma tabela sem a classe, com '
               'estilo próprio na página. A parte do guião é uma palavra e fica numa coluna estreita. A única mudança de texto da '
               'proposta: «Objeção que a turma pode fazer» passa a «Objeção». «capítulo V» já leva o espaço que não quebra (achado 42).'),
         antigo='<p class="ex">Abertura: «Quem aqui já viu alguém subir agarrado a outro?» Vieira, no capítulo V, repreende os pegadores: '
                'peixes pequenos que se colam aos grandes e vivem do que eles comem; o recurso é a antítese entre o grande que trabalha e '
                'o pequeno que só se agarra. Hoje: a conta que cresce a repetir o que outra conta diz, sem fazer nada de seu. Objeção que '
                'a turma pode fazer: «mas partilhar também é trabalho». Resposta: Vieira distingue quem nada ao lado de quem se cola; '
                'partilhar com nome e ideia própria é nadar ao lado. Fecho: a pergunta do princípio, agora com o peixe à vista. Imagens: '
                'a gravura do peixe, uma captura de ecrã sem nomes, a frase de Vieira.</p>',
         novo=('<div class="ex">' + tabela(['Parte', 'No guião'], GUIAO_GUIA, json_=False, larguras=[ESTREITA, LARGA]) + '</div>')),
    dict(i=14, cat='C', ficheiro='m4/licao-m4-f10/index.html', cartao='cartão 3, A encomenda (Ler mais, 2.º parágrafo)',
         nota=('«O que conta» passa a lista numerada, como nos outros cartões do M4 (todos <ol>); «20 segundos» já leva o espaço que '
               'não quebra (achado 25). O resto do parágrafo fica igual.'),
         antigo='<p>O que conta: a citação certa e localizada, o recurso nomeado e explicado, o comportamento de hoje sem visar ninguém, '
                'a objeção respondida com prova no texto, três a quatro minutos, imagens com crédito. Conta também o processo: três '
                'aberturas de 20 segundos',
         novo='<p>O que conta:</p><ol><li>A citação certa e localizada.</li><li>O recurso nomeado e explicado.</li><li>O comportamento de '
              'hoje sem visar ninguém.</li><li>A objeção respondida com prova no texto.</li><li>Três a quatro minutos.</li><li>Imagens '
              'com crédito.</li></ol><p>Conta também o processo: três aberturas de 20' + NBSP + 'segundos'),
    dict(i=15, cat='C', ficheiro='m4/mapa-do-modulo-m4/index.html',
         cartao='«Palavras que tens de saber»: a entrada «apóstrofe, anáfora, antítese, gradação»',
         nota='Cada termo fica junto da sua definição, no formato do vocabulário das lições, sem linhas novas (o mapa imprime-se).',
         antigo='<dd>chamar («irmãos peixes»); repetir no início; opor contrários; subir degrau a degrau.</dd>',
         novo='<dd>apóstrofe, chamar («irmãos peixes»); anáfora, repetir no início; antítese, opor contrários; gradação, subir degrau a '
              'degrau.</dd>'),
    dict(i=15, cat='C', ficheiro='m4/mapa-do-modulo-m4/index.html',
         cartao='«Palavras que tens de saber»: a entrada «presságio, revelação, catástrofe»',
         antigo='<dd>os passos da tragédia: os sinais, a verdade que se descobre, a queda.</dd>',
         novo='<dd>os passos da tragédia: presságio, os sinais; revelação, a verdade que se descobre; catástrofe, a queda.</dd>'),
    dict(i=16, cat='C', ficheiro='m4/portefolio-do-modulo-m4/index.html', cartao='«A lista de verificação»: os cabeçalhos',
         nota='Sem a largura fixa de 36 % (os nomes, sem partir, dão a largura da coluna) e com scope nos cabeçalhos.',
         antigo='<th style="width:36%">Nome do ficheiro</th><th>O que é</th>',
         novo='<th scope="col">Nome do ficheiro</th><th scope="col">O que é</th>'),
] + [
    dict(i=16, cat='C', ficheiro='m4/portefolio-do-modulo-m4/index.html', cartao=f'«A lista de verificação»: {n} em <code>',
         nota='Como nas outras linhas da lista.' if k == 0 else None,
         antigo=f'<td>{n}</td>', novo=f'<td><code>{n}</code></td>') for k, n in enumerate(NOMES_SEM_CODE)
] + [
    dict(i=16, cat='C', ficheiro='m4/portefolio-do-modulo-m4/index.html', cartao='a folha da página: os nomes em <code> não se partem',
         nota='O aluno copia estes nomes à letra: na tabela, não partem nos hífenes.',
         antigo='code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n',
         novo='code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\ntd code{white-space:nowrap}\n'),
]

# Os 29 achados B confirmados. Para cada um: as sequências da proposta final, com as ocorrências que se mudam (cada ocorrência
# contada uma vez, das mais longas para as mais curtas). «nb» são os créditos que outra camada já tinha posto em <span class="nb">
# com U+00A0: só o hífen passa a traço de intervalo, com a junção. «fora» diz o que fica de fora, e porquê: a casca das lições (que
# fica para o molde), o que um achado A ou C já mudou, ou o que outra camada já tinha posto (os «alt», o <title>, os desenhos e a
# «frase» dos sublinhar ficam sempre de fora e não se contam). «mais» diz, onde o número que se muda não é o da proposta, o número
# da proposta e porquê (ocorrências que também se veem e que a varredura contou à parte, ou não contou).
CASCA = 'a casca das lições (migalhas, «Estás em» e sigla do rodapé) fica para o molde'
JA = 'já com U+00A0, de outra camada (os créditos do «i»)'
VIDEO = 'o data-dur, de onde aula-clara.js refaz o botão do vídeo, muda com o botão'
ACHADOS_B = [
    dict(i=18, ficheiro='m4/licao-m4-f01/index.html',
         pares=[('cap. I', 12), ('cap. VI', 2), ('caps. II e III', 1), ('caps. IV e V', 2), ('13 de junho de 1654', 2), ('90 minutos', 1),
                ('1 min', 2), ('1.º sermão', 1), ('1.º tomo', 1), ('Mateus 5,13', 1), ('aula 2', 1)],
         nb=[('c.\xa01535-1540', 1)],
         mais={'1 min': (1, VIDEO)},
         fora={'2.º ano': (1, CASCA), 'M4-F01': (2, CASCA), 'séc. XVIII': (1, JA)}),
    dict(i=19, ficheiro='m4/licao-m4-f02/index.html',
         pares=[('cap. I', 13), ('cap. VI', 1), ('caps. II e III', 1), ('13 de junho de 1654', 1), ('13 de junho', 1), ('90 minutos', 1),
                ('Mateus 5, 13', 3), ('§ I', 3), ('(IV e V)', 1), ('aula 1', 4)],
         nb=[('c.\xa01535-1540', 1)],
         fora={'2.º ano': (1, CASCA), 'M4-F02': (2, CASCA), 'séc. XVIII': (1, JA)}),
    dict(i=20, ficheiro='m4/licao-m4-f04/index.html',
         pares=[('cap. IV', 11), ('caps. II e III', 1), ('cap. V', 2), ('caps. I e V', 1), ('cap. I', 1), ('90 minutos', 1)],
         mais={'cap. IV': (10, 'mais uma nas pistas («Pista»), que também se veem')},
         fora={'2.º ano': (1, CASCA), 'M4-F04': (2, CASCA)}),
    dict(i=21, ficheiro='m4/licao-m4-f06/index.html',
         pares=[('caps. II, IV, V e VI', 1), ('cap. V', 1), ('cap. IV', 3), ('90 minutos', 1)],
         fora={'2.º ano': (1, CASCA), 'M4-F06': (2, CASCA)}),
    dict(i=22, ficheiro='m4/licao-m4-f07/index.html',
         pares=[('século XVI', 1), ('ato I', 10), ('cenas XI e XII', 3), ('cena XI', 3), ('cena V', 2), ('cenas VII e VIII', 1), ('cena IX', 1),
                ('Ato I', 2), ('cena XII', 1), ('cena VIII', 5), ('cena VII', 3), ('Cena XII', 1), ('Ato II', 1), ('cena I', 3), ('cena IV', 1),
                ('ato II', 2), ('90 minutos', 1), ('aula 4', 1)],
         mais={'ato I': (8, 'a proposta conta 8 visíveis, ou 10 com o cartão extra do fim e as pistas («Pista»), que também se veem')},
         fora={'2.º ano': (1, CASCA), 'M4-F07': (2, CASCA)}),
    dict(i=23, ficheiro='m4/licao-m4-f08/index.html',
         pares=[('ato II', 10), ('cenas I, XIV e XV', 1), ('cena I', 5), ('Ato II', 2), ('cena II', 1), ('ato I', 1), ('cenas XIV e XV', 3),
                ('cena XV', 1), ('Cena XIV', 1), ('Cena XV', 1), ('cenas I e XIV', 1), ('ato III', 2), ('cena V', 1), ('90 minutos', 1)],
         mais={'ato II': (8, 'mais o cartão extra do fim e as pistas («Pista»), que também se veem'),
               'cenas XIV e XV': (2, 'mais o cartão extra do fim, que também se vê')},
         fora={'2.º ano': (1, CASCA), 'M4-F08': (2, CASCA)}),
    dict(i=24, ficheiro='m4/licao-m4-f09/index.html',
         pares=[('ato III', 14), ('cena XI', 14), ('ato II', 16), ('cenas X e XI', 1), ('cena I', 7), ('Ato III', 4), ('ato I', 2), ('cena VIII', 1),
                ('cenas I e VIII', 1), ('cena XII', 3), ('cena V', 2), ('90 minutos', 1), ('aula 1', 1), ('aula 4', 3), ('aula 10', 2),
                ('aula 12', 1)],
         mais={'ato III': (13, 'mais o cartão extra do fim, que também se vê')},
         fora={'2.º ano': (1, CASCA), 'M4-F09': (2, CASCA)}),
    dict(i=25, ficheiro='m4/licao-m4-f10/index.html',
         pares=[('cap. V', 5), ('cap. IV', 2), ('cap. I', 2), ('cap. VI', 1), ('capítulo V', 2), ('90 minutos', 1), ('20 segundos', 2),
                ('150 a 200 palavras', 1), ('1 min', 2), ('aula 1', 2), ('aula 4', 1)],
         mais={'cap. V': (4, 'a proposta conta 4 visíveis, ou 5 com as fontes do rodapé, que mudam, como no M1'), '1 min': (1, VIDEO),
               '20 segundos': (2, 'a proposta conta 2 nos cartões, ou 3 com as pistas («Pista»), que também se veem; o do cartão 3 vai '
                               'com o achado 14 (C)')},
         fora={'2.º ano': (1, CASCA), 'M4-F10': (2, CASCA),
               '20 segundos': (1, 'o achado 14 (C) passa «O que conta» do cartão 3 a lista, já com o espaço que não quebra'),
               'aula 1': (1, 'o achado 3 (A) passa as passagens do cartão 8 à tabela, já com o espaço que não quebra'),
               'aula 3': (1, 'só no cartão 8, que o achado 3 (A) passa à tabela, já com o espaço que não quebra'),
               'aula 4': (1, 'o achado 3 (A) passa as passagens do cartão 8 à tabela, já com o espaço que não quebra'),
               'aula 5': (1, 'só no cartão 8, que o achado 3 (A) passa à tabela, já com o espaço que não quebra')}),
    dict(i=26, ficheiro='m4/licao-m4-f11/index.html',
         pares=[('cap. I', 4), ('caps. II e III', 1), ('caps. IV e V', 1), ('cap. VI', 1), ('ato I', 2), ('cenas XI e XII', 2), ('cena XI', 2),
                ('cena XII', 1), ('ato III', 3), ('cena V', 1), ('13 de junho de 1654', 1), ('90 minutos', 1), ('100 a 140 palavras', 4),
                ('140 palavras', 1), ('131 palavras', 1)],
         fora={'2.º ano': (1, CASCA), 'M4-F11': (2, CASCA), 'séc. XVIII': (1, JA)}),
    dict(i=27, ficheiro='m4/licao-m4-f14/index.html',
         pares=[('5 de outubro de 1915', 4), ('5 de outubro de 1910', 1), ('14 de maio', 1), ('9 de março de 1916', 1), ('90 minutos', 1),
                ('3.º parágrafo', 2), ('5.º aniversário', 1), ('1.ª frase', 1), ('2.ª frase', 1), ('n.º 7', 1), ('aula 8', 1)],
         fora={'2.º ano': (1, CASCA), 'M4-F14': (2, CASCA)}),
    dict(i=28, ficheiro='m4/licao-m4-f15/index.html',
         pares=[('cap. IV', 11), ('90 minutos', 1), ('aula 3', 2), ('aula 12', 1)],
         fora={'2.º ano': (1, CASCA), 'M4-F15': (2, CASCA)}),
    dict(i=29, ficheiro='m4/licao-m4-f20/index.html',
         pares=[('Cena XI', 1), ('Cena XII', 1), ('ato I', 5), ('cena XI', 2), ('cena XII', 5), ('90 minutos', 2)],
         fora={'2.º ano': (1, CASCA), 'M4-F20': (2, CASCA)}),
    dict(i=30, ficheiro='m4/licao-m4-f25/index.html',
         pares=[('caps. I, II e V', 1), ('cap. IV', 1), ('caps. I e II', 1), ('cap. I', 1), ('cap. II', 3), ('caps. II e III', 1),
                ('caps. IV e V', 1), ('cap. V', 6), ('90 minutos', 1), ('aula 1', 2), ('aula 2', 1), ('aula 6', 1)],
         fora={'2.º ano': (1, CASCA), 'M4-F25': (2, CASCA)}),
    dict(i=31, ficheiro='m4/licao-m4-f26/index.html',
         pares=[('ato I', 3), ('cenas XI e XII', 3), ('ato II', 12), ('cenas I, XIV e XV', 1), ('ato III', 6), ('cena XI', 4), ('cena VIII', 1),
                ('cena XII', 1), ('cena I', 2), ('cena II', 5), ('cenas XIV e XV', 1), ('cena XV', 3), ('cena XIV', 1), ('90 minutos', 1)],
         nb=[('c.\xa01571-1574', 1)],
         mais={'ato II': (11, 'mais uma nas pistas («Pista»), que também se veem'),
               'ato III': (5, 'mais uma nas pistas («Pista»), que também se veem'),
               'cena XV': (2, 'mais uma nas pistas («Pista»), que também se veem')},
         fora={'2.º ano': (1, CASCA), 'M4-F26': (2, CASCA)}),
    dict(i=32, ficheiro='m4/licao-m4-f27/index.html',
         pares=[('cap. IV', 2), ('ato II', 5), ('cena I', 4), ('ato I', 2), ('cena II', 2), ('90 minutos', 1), ('aula 3', 1)],
         fora={'2.º ano': (1, CASCA), 'M4-F27': (2, CASCA)}),
    dict(i=33, ficheiro='m4/recursos/tpc-entrada.js',
         pares=[('ato I', 4), ('cena II', 1), ('cena I', 3), ('5 min', 1), ('45 minutos', 3), ('15 minutos', 1), ('8 min', 2), ('7 min', 1),
                ('15 min', 1), ('3 min', 1), ('80 a 120 palavras', 1), ('60 segundos', 1), ('4 min', 1), ('10 min', 1), ('1799–1854', 1)]),
    dict(i=34, ficheiro='m4/index.html',
         pares=[('cap. I', 5), ('ato I', 2), ('ato II', 8), ('cena XI', 1), ('ato III', 2), ('cena I', 1), ('cena XV', 2), ('13 de junho de 1654', 2),
                ('5 de outubro de 1915', 1), ('90 minutos', 6), ('25 %', 1), ('10 %', 1), ('15 %', 1), ('90 min', 6), ('10 min', 3),
                ('150 a 200 palavras', 1), ('100 a 140 palavras', 1), ('2.º ano', 2), ('1665–1667', 1), ('Mateus 5, 13', 1)]),
    dict(i=35, ficheiro='tarefas/m4-u1/index.html',
         pares=[('90 min', 1), ('10 minutos', 1), ('150 a 200 palavras', 1), ('3 a 4 minutos', 1)]),
    dict(i=36, ficheiro='tarefas/m4-u2/index.html',
         pares=[('Ato I', 1), ('ato I', 1), ('90 min', 1), ('10 minutos', 1), ('180 a 240 palavras', 1)]),
    dict(i=37, ficheiro='tarefas/m4-u3-discurso/index.html',
         pares=[('90 min', 1), ('10 minutos', 1), ('220 a 280 palavras', 1), ('2 minutos', 1)]),
    dict(i=38, ficheiro='tarefas/m4-u3/index.html',
         pares=[('ato I', 1), ('cena XII', 1), ('100 a 140 palavras', 2), ('10 min', 4), ('60 min', 1), ('30 min', 1), ('15 min', 1), ('5 min', 1),
                ('140 palavras', 2), ('M4-F11', 3)]),
    dict(i=39, ficheiro='tarefas/m4-u1/aquecimento/index.html', pares=[('cap. I', 4), ('cap. V', 2)]),
    dict(i=40, ficheiro='tarefas/m4-u2/aquecimento/index.html', pares=[('ato III', 1), ('ato II', 7), ('cena IV', 8)]),
    dict(i=41, ficheiro='tarefas/m4-u3-discurso/aquecimento/index.html', pares=[('350 palavras', 1), ('220 a 280 palavras', 2), ('7.º B', 1)]),
    dict(i=42, ficheiro='m4/guia-da-tarefa-m4/index.html',
         pares=[('ato I', 1), ('ato II', 1), ('90 min', 3), ('150 a 200 palavras', 1), ('3 minutos', 1), ('220 a 280 palavras', 2),
                ('180 a 240 palavras', 2), ('2.º ano', 2), ('aulas 1 a 8', 1), ('aulas 9 a 15', 1), ('aulas 16 a 18', 1)],
         fora={'capítulo V': (1, 'o achado 13 (A) passa o guião de exemplo à tabela, já com o espaço que não quebra')}),
    dict(i=43, ficheiro='m4/m4-frei-luis-quem-sabia/index.html',
         pares=[('ato I', 12), ('Ato I', 1), ('cena II', 1), ('ato II', 7), ('cena I', 3), ('cena VIII', 2), ('Ato II', 1), ('cena XIV', 2),
                ('cenas XIV e XV', 1), ('cena XV', 1), ('ato III', 6), ('Ato III', 1), ('cena XI', 1), ('25 min', 1), ('2.º ano', 1),
                ('n.º 17591', 6)]),
    dict(i=44, ficheiro='m4/m4-sermao-tribunal/index.html',
         pares=[('Cap. I', 1), ('Cap. IV', 1), ('cap. V', 1), ('Cap. V', 1), ('Cap. VI', 1), ('capítulo IV', 3), ('capítulo V', 2),
                ('13 de junho de 1654', 1), ('25 min', 1), ('2.º ano', 1), ('a objeção do Ato 4', 1)]),
    dict(i=45, ficheiro='m4/mapa-do-modulo-m4/index.html',
         pares=[('cap. I', 1), ('caps. II e III', 1), ('caps. IV e V', 1), ('século II d.C.', 1), ('13 de junho de 1654', 2),
                ('4 de agosto de 1578', 1), ('90 min', 3), ('25 %', 4), ('10 %', 1), ('45 minutos', 1), ('15 %', 1), ('2.º ano', 2),
                ('1608 – Bahia', 1), ('1799 – Lisboa', 1), ('aulas 1 a 8', 1), ('aulas 9 a 15', 1), ('aulas 16 a 18', 1), ('M4-F01', 5),
                ('M4-F08', 3), ('M4-F07', 1), ('M4-F14', 1), ('M4-F10', 1), ('M4-F26', 1)],
         nb=[('c.\xa01535-1540', 1), ('c.\xa01571-1574', 1)],
         fora={'séc. XVIII': (1, JA + '; o do «alt» não se vê')}),
    dict(i=46, ficheiro='m4/portefolio-do-modulo-m4/index.html',
         pares=[('2.º ano', 2), ('aulas 1 a 8', 1), ('aulas 9 a 15', 1), ('aulas 16 a 18', 1)]),
]

# A casca das lições fica para o molde, como no M1, no M2 e no M3: nenhuma troca. As lições onde a varredura a viu.
CASCA_NO_MOLDE = sorted(x['ficheiro'] for x in ACHADOS_B if x['ficheiro'].startswith('m4/licao-'))

# Dados dos geradores, com as sequências que lá estão (as das páginas, sem o que vem do molde dos geradores).
DADOS = [
    dict(ficheiro='docs/pedagogia/aquecimentos/m4-u1.json', achados=(39,), pares=[('cap. I', 4), ('cap. V', 2)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m4-u2.json', achados=(40,), pares=[('ato III', 1), ('ato II', 7), ('cena IV', 8)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m4-u3-discurso.json', achados=(41,),
         pares=[('350 palavras', 1), ('220 a 280 palavras', 2), ('7.º B', 1)]),
]

# As formas da proposta final que não prendem todos os espaços (as outras prendem cada espaço; o traço de intervalo leva a junção
# a seguir, e o hífen entre anos passa a traço de intervalo).
MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'


def alvo(seq):
    """A forma que não se parte, como na proposta final: nas datas com ano, o espaço entre o mês e o «de» do ano fica; nas listas
    («caps. II e III», «cenas I, XIV e XV», «(IV e V)»), só se prendem o primeiro espaço e o que vem a seguir ao «e»; em «aulas
    1 a 8», o primeiro e o que vem a seguir ao «a»; em «a objeção do Ato 4», só «Ato 4»; em «1608 – Bahia», o ano ao traço; na sigla
    «M4-Fxx», a junção a seguir ao hífen. O resto prende cada espaço, e o traço de intervalo leva a junção a seguir."""
    m = re.fullmatch(r'(\d+) de (' + MESES + r') de (\d{4})', seq)
    if m:
        return f'{m[1]}{NBSP}de{NBSP}{m[2]} de{NBSP}{m[3]}'
    m = re.fullmatch(r'((?:caps|cenas)\.?) (.+) e (\S+)', seq)
    if m:
        return f'{m[1]}{NBSP}{m[2]} e{NBSP}{m[3]}'
    m = re.fullmatch(r'\((\S+) e (\S+)\)', seq)
    if m:
        return f'({m[1]} e{NBSP}{m[2]})'
    m = re.fullmatch(r'aulas (\d+) a (\d+)', seq)
    if m:
        return f'aulas{NBSP}{m[1]} a{NBSP}{m[2]}'
    if seq == 'a objeção do Ato 4':
        return 'a objeção do Ato' + NBSP + '4'
    m = re.fullmatch(r'(\d{4}) – (\w+)', seq)
    if m:
        return f'{m[1]}{NBSP}– {m[2]}'
    if re.fullmatch(r'M4-F\d+', seq):
        return seq.replace('-', '-' + WJ)
    out = seq.replace(' ', NBSP)
    out = re.sub(r'(?<=\d)[-–](?=\d)', TRACO + WJ, out)
    return out


nao_parte = alvo

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
    sublinhar, o texto dos desenhos (SVG, que não muda de linha), os comentários e as notas internas dos dados («_nota»)."""
    if _nota_interna(texto, s):
        return 'nota interna dos dados'
    attr = _atributo(texto, s)
    if attr in ('alt', 'aria-label', 'href', 'title', 'src', 'content', 'data-titulo'):
        return 'atributo ' + attr
    if texto.rfind('<title>', 0, s) > texto.rfind('</title>', 0, s):
        return '<title>'
    if _frase_de_sublinhar(texto, s):
        return 'frase de um sublinhar'
    if _em_desenho(texto, s):
        return 'texto de um desenho (SVG)'
    if _em_comentario(texto, s):
        return 'comentário'
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
            if CONTAR is not None:
                CONTAR.append((rel, antigo, len(lista), esperado))
            else:
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
    m = re.match(r'm4/licao-(m4-f\d+)/', rel)
    if m:
        return m.group(1).upper()
    if rel == 'm4/recursos/tpc-entrada.js':
        return 'M4-F28 (banco de cartões)'
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
    return [(p[0], alvo(p[0]), p[1]) for p in x['pares']]


def proposta(x):
    """O que o achado põe na conta, sequência a sequência (para o relatório): o que muda, o que fica de fora e os créditos em «nb»
    (onde isto não dá o número da proposta, «mais» diz o número da proposta e porquê)."""
    out = {}
    for seq, n in list(x['pares']) + [(s, n) for s, (n, _) in x.get('fora', {}).items()] + [(s.replace(NBSP, ' '), n) for s, n in x.get('nb', [])]:
        out[seq] = out.get(seq, 0) + n
    return out


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
        relatorio.append((rel, x['i'], 'B', sum(n for _, _, n in pares), sum(proposta(x).values()), ''))
    return base_txt, pre, trocas, relatorio


def trocas_dados(specs):
    """As trocas de um ficheiro de dados: os achados B nos textos (os aquecimentos do M4 não levam «nao_partir»: o molde do
    gerador não tem números que se partam)."""
    rel = specs[0]['ficheiro']
    base_txt = base(rel)
    pre, regioes, trocas = base_txt, [], []
    janelas, pares, nomes = [], [], []
    for spec in specs:
        limite = None
        if 'entrada' in spec:
            inicio = pre.index(f'\n  "{spec["entrada"]}": {{')
            fim = pre.find('\n  "', inicio + 5)
            limite = (inicio, fim if fim > 0 else len(pre))
        ps = pares_de(spec)
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


# Os enunciados dos painéis do docente (m4/painel-m4-fxx) são os dos cartões da lição: o «p» (ou a «frase»), com ou sem os
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
    for licao in sorted(r for r in finais if r.startswith('m4/licao-')):
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


def construir_sem_conferir():
    por_pagina = {}
    for x in ACHADOS_AC:
        por_pagina.setdefault(x['ficheiro'], ([], []))[0].append(x)
    for x in ACHADOS_B:
        por_pagina.setdefault(x['ficheiro'], ([], []))[1].append(x)
    for rel in sorted(set(por_pagina) | set(COM_TABELA)):
        ac, bs = por_pagina.get(rel, ([], []))
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
