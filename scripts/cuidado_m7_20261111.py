#!/usr/bin/env python3
"""11/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M7 do Português.

Constrói scripts/cuidado_m7_20261111.json, a camada literal cuidado_m7_20261111, com os achados CONFIRMADOS da varredura do M7
(refeita a 9/11 e conferida a 11/11, só leitura, sobre o main 4bf4a053): dos 66 confirmados (3 A, 60 B e 3 C) entram 61: os 3
achados A (tabelas onde há itens paralelos), 55 de referências e números que se partiam (B) e os 3 casos do mesmo tipo (C).
Ficam de fora, por decisão já tomada para todos os módulos, como do M1 ao M5, os 5 achados B dos diapositivos (4), das três
provas rápidas (56, 57 e 58) e dos questionários (59): essas páginas não mudam. Os 9 achados que a conferência recusou (0, 3, 5,
20, 28, 34, 35, 47 e 63) também não entram. A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em
tests/fixtures/cuidado-m7-edits-20261111.json:

  python3 scripts/cuidado_m7_20261111.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m7_20261111.json --manifesto tests/fixtures/cuidado-m7-edits-20261111.json \\
      --base-commit 49871e0870c666e2b33d5ce01f0779e626e29bee --nota "…"

12/11/2026: junto o ramo do M6 como ficou em 49871e08 (as reposições depois do #192 nas tarefas do M1, do M3, do M4 e do M5, e o
main c1b165fe, #193); a base passa a esse commit (era 29006166). Nenhum dos 59 ficheiros desta camada mudou entre os dois: os
resumos do manifesto e as 450 trocas são os mesmos.

Fica por cima da decisão 152 no M6 (cuidado_m6_20261108, no ramo do pedido #191 com o main 4bf4a053 já dentro, commit 29006166),
que não toca em nenhuma página do M7; as duas só partilham os dados das grelhas (o M6 nas entradas m6-u1 e m6-u2, esta na m7-u3).

Segue o modelo da camada do M6 (scripts/cuidado_m6_20261108.py), com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como na M7-F10, na M7-F15 e do M1 ao M6: class apoio-tabela, th
  scope=col no cabeçalho, th scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader,
  rowheader, cell), porque no telemóvel a tabela passa a display:block. Dentro do JSON dos cartões, as aspas vão com barra (\\").
  São três: os pesos da avaliação no índice do módulo (achado 8, como no índice do M5: o rótulo num parágrafo, a tabela
  Elemento/Peso com a coluna do peso em 5,5 rem, e «Cada tarefa tem uma grelha /20.» no p.avaliacao-tarefas), as três vidas da
  carta na dobra do «O essencial» da F01 (achado 10: Heterónimo/Vida) e os quatro termos da caixa «Recorda» da F23 (achado 25:
  Termo/O que é, com a frase final e a fonte num parágrafo a seguir). Cada página com uma tabela nova carrega
  assets/pt-lessons/apoios-tabelas.css antes de assets/appearance.css, na versão do M1 (20261106.1: a folha não muda). A F10 e
  a F15, que já tinham a sua tabela e a folha, ficam como estavam.
- B: U+00A0 (espaço que não quebra) nos espaços que a proposta final prende, e U+2060 (junção de palavras) logo a seguir ao
  traço de intervalo e ao hífen da sigla «M7-Fxx». Cada par da proposta conta-se com a palavra inteira («v. 1» não conta dentro
  de «v. 10», nem «90 min» dentro de «90 minutos») e fora das cadeias maiores dos outros pares da página («8 de março» não
  conta dentro de «8 de março de 1914», nem «80 a 120» dentro de «80 a 120 palavras»); a troca leva só os espaços que muda, com
  o mínimo de contexto que a distingue. Nas datas, a proposta do M7 prende o dia ao «de» e o ano ao «de» («13 de janeiro de
  1935» fica com U+00A0 depois de «13» e antes de «1935»), como no M5; nos pares «N e N» e «N a N» com nome antes («vv. 3 e 4»,
  «estrofes 1 a 5», «poemas II e IX»), prende o nome ao primeiro número e o «e» ou o «a» ao segundo. Ficam de fora: os «alt» (e
  aria-label, href, title, content e data-titulo, que vira o title do vídeo), o <title>, o texto dos desenhos (SVG), a «frase»
  dos cartões sublinhar, as «palavras» dos cartões frase e os «passos» dos cartões ordenar (o motor parte-os nos espaços), as
  notas internas dos dados, a casca das lições (abaixo) e o que a conferência deixou de fora com a razão: duas citações literais
  entre «» em «O leme e o retrato» (mostrengo-leme-ramos) e o título do poema no menu «Relembrar» do aquecimento da M7-U3.
- C: «Três antes de mim», no guia, em lista numerada (achado 6, o mesmo trecho, letra a letra, do guia do M5); o plano do
  texto da F10, ponto a ponto, numa lista (achado 18); e, no portefólio, os nove nomes de ficheiro que estavam em texto simples
  em <code>, como os outros nove, com <wbr> depois de «M7_», de «U1_» e de «aula_» e «td code{white-space:nowrap}» na folha da
  página (achado 54, como no portefólio do M5: os nomes só mudam de linha nos pontos marcados).
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois. Na tabela dos pesos, os números já vão com o
  espaço que não quebra (são os pares «35 %», «25 %», «10 %» e «30 %» do achado 9, que ficam em «refeitos»).

A casca das lições (migalhas «3.º ano», «Estás em: Lição M7-Fxx», o título escondido e a sigla «Lição M7-Fxx» do rodapé) não
muda aqui, ficheiro a ficheiro: muda no molde, como do M1 ao M6. Nas outras páginas (índice, guia, mapa e portefólio do módulo,
«Ler a fundo», «Olhar», «Pensar devagar» e a visita à Casa Fernando Pessoa), a proposta final conta as migalhas («não é lição:
as migalhas contam») e o «3.º ano» fica preso nas migalhas e no cabeçalho.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e das listas (cai o negrito dos nomes e dos termos que
passam a cabeçalho de linha, o ponto final de cada célula e os «1) 2) 3)» que a lista numerada substitui; os cabeçalhos
«Elemento», «Peso», «Heterónimo», «Vida», «Termo» e «O que é» são os da proposta) e os espaços invisíveis. O script calcula as
trocas sobre a base (a página com esta camada desfeita pelo manifesto, quando ele já existe): pode voltar a correr depois de a
camada estar aplicada e dá o mesmo JSON.

Páginas geradas: a tarefa da M7-U3 (scripts/tarefas_escolha.py) muda nos dados (docs/pedagogia/tarefas-escolha/m7-u3.json:
«nao_partir», como do M1 ao M6, que prende os números do molde e a meta descrição, e os achados B); os três aquecimentos
(scripts/aquecimentos.py) mudam nos dados (docs/pedagogia/aquecimentos/m7-u1.json, m7-u2.json e m7-u3.json); a grelha e a
correção da M7-U3 (scripts/grelhas_tarefas.py) mudam nos dados (docs/pedagogia/grelhas-tarefas-20261027.json, só na entrada
m7-u3). Os dados estão na mesma camada e as páginas regeneram-se sem diferenças; os geradores não mudam. As tarefas da M7-U1 e da
M7-U2 não são das de escolha (não têm dados nem gerador): mudam aqui, como nas camadas tarefas_individuais e tarefas_claras.
Nenhuma lição do M7 é gerada. Os painéis de projeção do docente (m7/painel-m7-fxx) seguem os enunciados dos cartões (a lista
CARTOES e o seletor, onde o itálico de um título vai em <i>); o material do relâmpago (MATERIAL) segue a lição antes das camadas
de cuidado (tests/test_sala_desligada.py compara-o com ela) e não muda, como do M1 ao M6: são os 12 achados dos painéis (40 a
46 e 48 a 52), e o painel da F11 (achado 47, recusado: só tinha ocorrências em MATERIAL) fica como estava. As cópias dos cartões
no banco das provas rápidas do índice (var U) mudam como as lições de onde vêm (estão nos pares do achado 9).
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m7_20261111.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m7-edits-20261111.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
CONTAR = None
ACHADO = '11/11/2026: decisão 152 (cuidado em todas as lições), varredura do M7, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como na M7-F10, na M7-F15 e do M1 ao M6).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e ao hífen da '
          'sigla).'),
    'C': 'Caso do mesmo tipo.',
}


def j(s):
    """As formas da proposta escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return s.replace('{N}', NBSP).replace('{J}', WJ)


# A folha das tabelas de apoio, antes da camada de aparência (como na M7-F10, na M7-F15 e do M1 ao M6), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
INDICE = 'm7/index.html'
COM_TABELA = {
    INDICE: ('O índice do módulo passa', [8]),
    'm7/licao-m7-f01/index.html': ('A lição passa', [10]),
    'm7/licao-m7-f23/index.html': ('A lição passa', [25]),
}
# Na tabela dos pesos do índice, a coluna do peso só leva o número (as larguras do índice do M5).
PESOS = [' style="width:auto"', ' style="width:5.5rem"']


def tabela(colunas, linhas, json_=True, larguras=None):
    """A tabela de apoio, igual às do M1 ao M6: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label com
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


def bloco(rel, inicio, fim, inclui_fim=False):
    """O trecho da base que começa em «inicio» (único na página) e acaba logo antes de «fim» (ou com ele, com inclui_fim)."""
    texto = base(rel)
    if texto.count(inicio) != 1:
        raise SystemExit(f'{rel}: «{inicio[:60]}» não aparece uma vez')
    a = texto.index(inicio)
    b = texto.index(fim, a) + (len(fim) if inclui_fim else 0)
    return texto[a:b]


# Achado 8 (A): os pesos da avaliação no índice, como no índice do M5 (um parágrafo com o rótulo, a tabela Elemento/Peso e o
# resto num p.avaliacao-tarefas). Os pesos já vão com o espaço que não quebra (os pares «35 %», «25 %», «10 %» e «30 %» do achado 9).
PESOS_ANTES = ('<p class="avaliacao-tarefas">Pesos na avaliação: tarefa da Unidade 2 («Uma ideia de heterónimo»), 35 %; tarefa da '
               'Unidade 3 («Louco, sim»), 25 %; provas rápidas, 10 %; prova escrita, 30 %. Cada tarefa tem uma grelha /20.</p>')
PESOS_LINHAS = [['Tarefa da Unidade 2 («Uma ideia de heterónimo»)', '35{N}%'], ['Tarefa da Unidade 3 («Louco, sim»)', '25{N}%'],
                ['Provas rápidas', '10{N}%'], ['Prova escrita', '30{N}%']]

# Achado 10 (A): as três vidas da carta, na dobra do «O essencial» da F01 (dentro do JSON dos cartões).
VIDAS_ANTES = ('<p><b>Caeiro</b>: Lisboa, 1889; morre em 1915; vive quase sempre no campo, sem profissão. <b>Reis</b>: Porto, 1887; '
               'médico e latinista; vive no Brasil. <b>Campos</b>: Tavira, 1890; engenheiro naval formado em Glasgow.</p>')
VIDAS_LINHAS = [['Caeiro', 'Lisboa, 1889; morre em 1915; vive quase sempre no campo, sem profissão'],
                ['Reis', 'Porto, 1887; médico e latinista; vive no Brasil'],
                ['Campos', 'Tavira, 1890; engenheiro naval formado em Glasgow']]

# Achado 25 (A): os quatro termos da caixa «Recorda» da F23 (dentro do JSON dos cartões); a frase final fica num parágrafo.
TERMOS_ANTES = ('<p><b>Ode</b>: poema de tom elevado, em estrofes regulares; Reis segue o modelo do poeta latino Horácio. '
                '<b>Epicurismo</b>: procurar a tranquilidade com prazeres simples, sem excessos, e sem temer a morte. '
                '<b>Estoicismo</b>: dominar as paixões e aceitar a ordem do mundo, incluindo a morte. <b><i>Carpe diem</i></b>: '
                'expressão latina que manda aproveitar o dia de hoje. Na lição «À beira do rio» viste esta maneira de viver; aqui '
                'dás-lhe nome. <span class=\\"sub\\">Fonte: Wikipédia, «Ricardo Reis».</span></p>')
TERMOS_LINHAS = [['Ode', 'poema de tom elevado, em estrofes regulares; Reis segue o modelo do poeta latino Horácio'],
                 ['Epicurismo', 'procurar a tranquilidade com prazeres simples, sem excessos, e sem temer a morte'],
                 ['Estoicismo', 'dominar as paixões e aceitar a ordem do mundo, incluindo a morte'],
                 ['<i>Carpe diem</i>', 'expressão latina que manda aproveitar o dia de hoje']]
TERMOS_DEPOIS = ('<p>Na lição «À beira do rio» viste esta maneira de viver; aqui dás-lhe nome. <span class=\\"sub\\">Fonte: Wikipédia, '
                 '«Ricardo Reis».</span></p>')

# Achado 6 (C): «Três antes de mim», no guia, em lista numerada (o mesmo trecho, letra a letra, do guia do M5).
REGRA_ANTES = ('Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta ao teu par de trabalho. Só depois '
               'levantas o braço.</div>')
REGRA_DEPOIS = ('Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica;</li><li>pergunta ao teu par de '
                'trabalho.</li></ol>Só depois levantas o braço.</div>')

# Achado 18 (C): o plano do texto da F10, ponto a ponto, numa lista (cada ponto com o «;» ou o «.» que tinha).
PLANO = ['A tese com condição na primeira frase;', 'um movimento que dá razão ao outro lado e vira (R ou C);',
         'mais um movimento (N, M ou P);', 'um verso exato de <i>Mensagem</i>, explicado;',
         'um facto datado separado do sentido que o poema lhe dá, ou o confronto com Garrett ou com Reis;',
         'uma conclusão que volta à tese sem a copiar;', 'as letras dos movimentos na margem.']

# Achado 54 (C): no portefólio, os nove nomes de ficheiro que estavam em texto simples passam a <code>, como os outros nove; os
# nomes compridos podem mudar de linha depois de «M7_», de «U1_» e de «aula_» (<wbr>, como no portefólio do M5), e só aí.
PORTEFOLIO = 'm7/portefolio-do-modulo-m7/index.html'
PORT_NOMES = [f'M7_U{u}_{n}' for u in (1, 2, 3) for n in ('aula_&lt;dia-mês&gt;', 'pergunta', 'o-que-aprendi')]
PORT_JA_CODE = ['M7_cartao-do-percurso', 'M7_Prova-escrita']
PORT_CSS_ANTES = 'code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
PORT_CSS_DEPOIS = PORT_CSS_ANTES + 'td code{white-space:nowrap}\n'


def com_wbr(nome_):
    """O nome com <wbr> depois de «M7_», de «U1_» e de «aula_» (onde pode mudar de linha)."""
    return re.sub(r'(M7_|U\d_|aula_)', r'\1<wbr>', nome_)


def achados_ac():
    """Os 6 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte)."""
    f01, f10, f23 = (f'm7/licao-m7-{n}/index.html' for n in ('f01', 'f10', 'f23'))
    guia = 'm7/guia-da-tarefa-m7/index.html'
    plano_antes = '<p>' + ' '.join(PLANO) + '</p>'
    out = [
        dict(i=6, cat='C', ficheiro=guia, cartao='«Três antes de mim» (div.regra)',
             nota='Os três passos numerados à mão passam a lista numerada, como no guia do M5; o texto fica igual.',
             antigo=REGRA_ANTES, novo=REGRA_DEPOIS),
        dict(i=8, cat='A', ficheiro=INDICE, cartao='«Como se cumpre uma unidade»: os pesos na avaliação',
             nota=('Como no índice do M5: o rótulo num parágrafo, a tabela Elemento/Peso (a coluna do peso com 5,5 rem) e «Cada tarefa '
                   'tem uma grelha /20.» no p.avaliacao-tarefas. Os pesos já levam o espaço que não quebra (achado 9).'),
             antigo=PESOS_ANTES,
             novo=('<p>Pesos na avaliação:</p>' + j(tabela(['Elemento', 'Peso'], PESOS_LINHAS, json_=False, larguras=PESOS))
                   + '<p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20.</p>')),
        dict(i=10, cat='A', ficheiro=f01, cartao='cartão 2, O essencial (dobra «As três vidas, segundo a carta»)',
             nota=('Duas colunas, «Heterónimo» e «Vida» (a palavra do título da dobra); cada célula leva o texto tal como está, com '
                   'os «;»; cai o ponto final e o negrito do nome (o cabeçalho da linha já o destaca), como na M5-F11.'),
             antigo=VIDAS_ANTES, novo=tabela(['Heterónimo', 'Vida'], VIDAS_LINHAS)),
        dict(i=18, cat='C', ficheiro=f10, cartao='cartão 1, O essencial (dobra «O plano do texto, ponto a ponto»)',
             nota='Os sete pontos numa lista, cada um com o «;» ou o ponto final que tinha, como os factos da M5-F08; o texto fica igual.',
             antigo=plano_antes, novo='<ul>' + ''.join(f'<li>{p}</li>' for p in PLANO) + '</ul>'),
        dict(i=25, cat='A', ficheiro=f23, cartao='cartão 14, Para entender («Recorda»)',
             nota=('Os quatro termos no cabeçalho de linha, sem negrito (o itálico de «Carpe diem» fica); cai o ponto final de cada '
                   'definição; a frase final e a fonte ficam num parágrafo a seguir, como na M5-F13.'),
             antigo=TERMOS_ANTES, novo=tabela(['Termo', 'O que é'], TERMOS_LINHAS) + TERMOS_DEPOIS),
    ]
    for nome_ in PORT_NOMES:
        out.append(dict(i=54, cat='C', ficheiro=PORTEFOLIO, cartao=f'«A lista de verificação»: o nome {html.unescape(nome_)} em <code>',
                        nota=('O nome do ficheiro, que se copia letra a letra, passa a <code>, como os outros nove da lista; pode mudar '
                              'de linha depois de «M7_», de «U1_» e de «aula_» (<wbr>), como no portefólio do M5.'),
                        antigo=f'<td>{nome_}</td>', novo=f'<td><code>{com_wbr(nome_)}</code></td>'))
    for nome_ in PORT_JA_CODE:
        out.append(dict(i=54, cat='C', ficheiro=PORTEFOLIO, cartao=f'«A lista de verificação»: o nome {nome_} pode mudar de linha depois de «M7_»',
                        nota='O nome já estava em <code>; leva <wbr> depois de «M7_», como no portefólio do M5.',
                        antigo=f'<td><code>{nome_}</code></td>', novo=f'<td><code>{com_wbr(nome_)}</code></td>'))
    out.append(dict(i=54, cat='C', ficheiro=PORTEFOLIO, cartao='a folha da página: os nomes só mudam de linha onde podem',
                    nota='Como no portefólio do M5: «td code{white-space:nowrap}», a seguir à regra do <code>.',
                    antigo=PORT_CSS_ANTES, novo=PORT_CSS_DEPOIS))
    return out


def ac_grelhas():
    """Sem achados A ou C nas grelhas do M7 (a função fica, como no M6, para os testes e para a ordem das trocas)."""
    return []


# Os 55 achados B confirmados que entram (os 12 dos painéis estão em PAINEIS). Cada par é o da proposta final, com as ocorrências
# que mudam («n»); conta-se com a palavra inteira e fora das cadeias maiores dos outros pares da página. Onde a conferência
# deixou ocorrências de fora que o detetor não conhece (a casca, uma citação literal, o menu do aquecimento), o par vai com o
# contexto que as distingue, «de» diz a que par da proposta pertence e «fora» diz o que fica e porquê; «refeitos» é o que um
# achado A já pôs com o espaço preso; «literais» são as trocas que a proposta não lista (com a razão).
PESOS_REFEITOS = 'o achado 8 (A) refaz os pesos numa tabela, já com o espaço que não quebra'
CASCA = 'está nas migalhas da casca da lição, que muda no molde'
CITACAO = 'está numa citação literal, entre «», que fica como no original'
MENU = 'está no menu «Relembrar» da casca do aquecimento, uma ligação sozinha numa linha'
ACHADOS_B = [
    dict(i=1, ficheiro='m7/caeiro-olhar/index.html',
         pares=[('poema II', 'poema{N}II', 1), ('poema IX', 'poema{N}IX', 1)]),
    dict(i=2, ficheiro='m7/campos-aniversario/index.html',
         pares=[('8 palavras', '8{N}palavras', 1)]),
    dict(i=7, ficheiro='m7/guia-da-tarefa-m7/index.html',
         pares=[('90 minutos', '90{N}minutos', 1), ('90 min', '90{N}min', 3), ('15 min', '15{N}min', 2),
                ('60 min', '60{N}min', 1), ('10 minutos', '10{N}minutos', 2),
                ('100 a 150 palavras', '100{N}a{N}150{N}palavras', 4), ('80 a 120 palavras', '80{N}a{N}120{N}palavras', 1),
                ('180 a 220 palavras', '180{N}a{N}220{N}palavras', 3), ('150 a 180 palavras', '150{N}a{N}180{N}palavras', 3),
                ('12 a 16 versos', '12{N}a{N}16{N}versos', 3), ('3.º ano', '3.º{N}ano', 2),
                ('D. Sebastião', 'D.{N}Sebastião', 2)]),
    dict(i=9, ficheiro='m7/index.html',
         pares=[('90 minutos', '90{N}minutos', 5),                 ('90 min', '90{N}min', 6), ('22 min', '22{N}min', 1),
                ('10 a 15 min', '10{N}a{N}15{N}min', 1), ('23 min', '23{N}min', 1), ('10 min', '10{N}min', 2),
                ('13 de janeiro de 1935', '13{N}de janeiro de{N}1935', 2),
                ('8 de março de 1914', '8{N}de março de{N}1914', 2), ('4 de agosto de 1578', '4{N}de agosto de{N}1578', 1),
                ('15 de outubro de 1890', '15{N}de outubro de{N}1890', 1), ('3.º ano', '3.º{N}ano', 2),
                ('2.ª estrofe', '2.ª{N}estrofe', 14), ('3.ª estrofe', '3.ª{N}estrofe', 13),
                ('5.ª estrofe', '5.ª{N}estrofe', 4), ('6.ª estrofe', '6.ª{N}estrofe', 1),
                ('4.ª estrofe', '4.ª{N}estrofe', 8), ('1.ª estrofe', '1.ª{N}estrofe', 2), ('6.º verso', '6.º{N}verso', 2),
                ('1.ª pessoa', '1.ª{N}pessoa', 3), ('3.ª estrofes', '3.ª{N}estrofes', 1), ('4.º verso', '4.º{N}verso', 1),
                ('5.º verso', '5.º{N}verso', 1), ('3.ª pessoa', '3.ª{N}pessoa', 2), ('2.ª pessoa', '2.ª{N}pessoa', 1),
                ('1.º verso', '1.º{N}verso', 2), ('poemas II e IX', 'poemas{N}II e{N}IX', 1), ('poema XX', 'poema{N}XX', 2),
                ('v. 4', 'v.{N}4', 2), ('vv. 3 e 4', 'vv.{N}3 e{N}4', 1), ('v. 2', 'v.{N}2', 1), ('poema I', 'poema{N}I', 3),
                ('poema II', 'poema{N}II', 6), ('poema IX', 'poema{N}IX', 1), ('v. 1', 'v.{N}1', 3), ('v. 8', 'v.{N}8', 4),
                ('v. 7', 'v.{N}7', 1), ('v. 10', 'v.{N}10', 1), ('v. 3', 'v.{N}3', 1), ('v. 5', 'v.{N}5', 2),
                ('D. Sebastião', 'D.{N}Sebastião', 10), ('D. João', 'D.{N}João', 3), ('M7-F10', 'M7-{J}F10', 1)],
         refeitos={s: (1, PESOS_REFEITOS) for s in ('35 %', '25 %', '10 %', '30 %')}),
    dict(i=11, ficheiro='m7/licao-m7-f01/index.html',
         pares=[('13 de janeiro de 1935', '13{N}de janeiro de{N}1935', 5), ('8 de março', '8{N}de março', 1),
                ('8 de março de 1914', '8{N}de março de{N}1914', 3)]),
    dict(i=12, ficheiro='m7/licao-m7-f02/index.html',
         pares=[('30 s', '30{N}s', 1), ('1.ª publicação', '1.ª{N}publicação', 2), ('2.ª estrofe', '2.ª{N}estrofe', 6),
                ('3.ª estrofe', '3.ª{N}estrofe', 3), ('1.ª estrofe', '1.ª{N}estrofe', 2), ('n.º 36', 'n.º{N}36', 1),
                ('v. 4', 'v.{N}4', 5), ('vv. 3 e 4', 'vv.{N}3 e{N}4', 1), ('v. 2', 'v.{N}2', 1), ('n.º 38', 'n.º{N}38', 1),
                ('v. 6', 'v.{N}6', 1), ('v. 10', 'v.{N}10', 1), ('versos 2 e 3', 'versos{N}2 e{N}3', 1)]),
    dict(i=13, ficheiro='m7/licao-m7-f04/index.html',
         pares=[('8 de março', '8{N}de março', 1), ('Poema II', 'Poema{N}II', 1), ('v. 1', 'v.{N}1', 1),
                ('verso 14', 'verso{N}14', 1), ('verso 15', 'verso{N}15', 1), ('poema IX', 'poema{N}IX', 1),
                ('poema II', 'poema{N}II', 3)]),
    dict(i=14, ficheiro='m7/licao-m7-f05/index.html',
         pares=[('1 min', '1{N}min', 1), ('12 de junho', '12{N}de junho', 1), ('1 de julho', '1{N}de julho', 1),
                ('1.ª pessoa', '1.ª{N}pessoa', 2), ('2.ª estrofe', '2.ª{N}estrofe', 2), ('3.ª estrofe', '3.ª{N}estrofe', 4),
                ('4.ª estrofe', '4.ª{N}estrofe', 3), ('5.ª estrofe', '5.ª{N}estrofe', 2),
                ('3.ª estrofes', '3.ª{N}estrofes', 1), ('1.ª estrofe', '1.ª{N}estrofe', 1), ('n.º 1', 'n.º{N}1', 1),
                ('estrofes 1 a 5', 'estrofes{N}1 a{N}5', 1), ('v. 1', 'v.{N}1', 4), ('v. 8', 'v.{N}8', 1),
                ('v. 7', 'v.{N}7', 1), ('vv. 11 e 12', 'vv.{N}11 e{N}12', 1), ('vv. 19 e 20', 'vv.{N}19 e{N}20', 1)]),
    dict(i=15, ficheiro='m7/licao-m7-f06/index.html',
         pares=[('1 min', '1{N}min', 1), ('15 de outubro', '15{N}de outubro', 1), ('15 de janeiro', '15{N}de janeiro', 1),
                ('4.º verso', '4.º{N}verso', 2), ('5.º verso', '5.º{N}verso', 1), ('n.º 39', 'n.º{N}39', 1)]),
    dict(i=16, ficheiro='m7/licao-m7-f08/index.html',
         pares=[('3 min', '3{N}min', 1), ('4 de agosto', '4{N}de agosto', 1), ('10 de dezembro', '10{N}de dezembro', 1),
                ('20 de fevereiro', '20{N}de fevereiro', 1), ('1.ª edição', '1.ª{N}edição', 1),
                ('3.º verso', '3.º{N}verso', 1), ('1.ª estrofe', '1.ª{N}estrofe', 2), ('2.ª estrofe', '2.ª{N}estrofe', 1),
                ('v. 1', 'v.{N}1', 1), ('v. 8', 'v.{N}8', 3), ('v. 10', 'v.{N}10', 1), ('D. Sebastião', 'D.{N}Sebastião', 2)]),
    dict(i=17, ficheiro='m7/licao-m7-f09/index.html',
         pares=[('4 de agosto de 1578', '4{N}de agosto de{N}1578', 2), ('1.ª pessoa', '1.ª{N}pessoa', 5),
                ('3.ª pessoa', '3.ª{N}pessoa', 2), ('2.ª pessoa', '2.ª{N}pessoa', 1), ('1.ª estrofe', '1.ª{N}estrofe', 1),
                ('2.ª estrofe', '2.ª{N}estrofe', 3), ('6.º verso', '6.º{N}verso', 1), ('2.º ano', '2.º{N}ano', 2),
                ('v. 3', 'v.{N}3', 1), ('vv. 4 e 5', 'vv.{N}4 e{N}5', 1), ('v. 4', 'v.{N}4', 2), ('v. 5', 'v.{N}5', 2),
                ('v. 11', 'v.{N}11', 1), ('v. 15', 'v.{N}15', 1), ('D. Sebastião', 'D.{N}Sebastião', 13),
                ('D. João', 'D.{N}João', 5), ('c. 1571-1574', 'c.{N}1571-1574', 1)]),
    dict(i=19, ficheiro='m7/licao-m7-f10/index.html',
         pares=[('25 %', '25{N}%', 2), ('180 a 220 palavras', '180{N}a{N}220{N}palavras', 2),
                ('1.º verso', '1.º{N}verso', 2), ('século XV', 'século{N}XV', 1), ('D. Henrique', 'D.{N}Henrique', 1),
                ('D. Sebastião', 'D.{N}Sebastião', 5), ('D. João', 'D.{N}João', 2), ('M7-F07', 'M7-{J}F07', 1)]),
    dict(i=21, ficheiro='m7/licao-m7-f11/index.html',
         pares=[('15 de outubro de 1890', '15{N}de outubro de{N}1890', 1), ('D. Sebastião', 'D.{N}Sebastião', 2)]),
    dict(i=22, ficheiro='m7/licao-m7-f13/index.html',
         pares=[('do 3.º ano de Vídeo', 'do 3.º{N}ano de Vídeo', 1), ('3.ª estrofe', '3.ª{N}estrofe', 7), ('2.ª estrofe', '2.ª{N}estrofe', 3),
                ('4.ª estrofe', '4.ª{N}estrofe', 3), ('5.ª estrofe', '5.ª{N}estrofe', 4), ('n.º 3', 'n.º{N}3', 2),
                ('n.º 2', 'n.º{N}2', 1), ('v. 2', 'v.{N}2', 1)],
         de={'do 3.º ano de Vídeo': '3.º ano'}, fora={'pt/3/">3.º ano</a>': (1, CASCA)}),
    dict(i=23, ficheiro='m7/licao-m7-f14/index.html',
         pares=[('1.ª estrofe', '1.ª{N}estrofe', 3), ('4.º verso', '4.º{N}verso', 1), ('3.ª estrofe', '3.ª{N}estrofe', 13),
                ('2.ª estrofe', '2.ª{N}estrofe', 5), ('2.º verso', '2.º{N}verso', 1), ('4.ª estrofe', '4.ª{N}estrofe', 5),
                ('6.º verso', '6.º{N}verso', 2)]),
    dict(i=24, ficheiro='m7/licao-m7-f15/index.html',
         pares=[('2.ª estrofe', '2.ª{N}estrofe', 4), ('v. 2', 'v.{N}2', 1), ('v. 9', 'v.{N}9', 1), ('v. 10', 'v.{N}10', 1),
                ('v. 11', 'v.{N}11', 2), ('vv. 9 a 11', 'vv.{N}9 a{N}11', 1)]),
    dict(i=26, ficheiro='m7/licao-m7-f23/index.html',
         pares=[('1.ª publicação', '1.ª{N}publicação', 1), ('2.ª estrofe', '2.ª{N}estrofe', 2),
                ('3.ª estrofe', '3.ª{N}estrofe', 1), ('n.º 1', 'n.º{N}1', 1), ('vv. 3 e 4', 'vv.{N}3 e{N}4', 1),
                ('v. 1', 'v.{N}1', 1), ('v. 9', 'v.{N}9', 1)]),
    dict(i=27, ficheiro='m7/licao-m7-f34/index.html',
         pares=[('n.º 2', 'n.º{N}2', 6), ('Poema I', 'Poema{N}I', 1), ('parte VI', 'parte{N}VI', 4),
                ('partes I e II', 'partes{N}I e{N}II', 2), ('poema I', 'poema{N}I', 6), ('Poema II', 'Poema{N}II', 1),
                ('poema II', 'poema{N}II', 8), ('parte I', 'parte{N}I', 1), ('parte II', 'parte{N}II', 1),
                ('Orpheu_ 2', 'Orpheu_{N}2', 1), ('Orpheu</i> 2', 'Orpheu</i>{N}2', 1)]),
    dict(i=29, ficheiro='m7/licao-m7-f35/index.html',
         pares=[('2 min', '2{N}min', 1), ('v. 3', 'v.{N}3', 2), ('verso 3', 'verso{N}3', 1), ('v. 6', 'v.{N}6', 1),
                ('v. 4', 'v.{N}4', 1), ('v. 7', 'v.{N}7', 1), ('v. 14', 'v.{N}14', 2), ('v. 21', 'v.{N}21', 1),
                ('poemas II e IX', 'poemas{N}II e{N}IX', 1), ('poema XX', 'poema{N}XX', 4), ('poema II', 'poema{N}II', 3)]),
    dict(i=30, ficheiro='m7/licao-m7-f36/index.html',
         pares=[('2 de fevereiro de 1991', '2{N}de fevereiro de{N}1991', 1), ('n.º 39', 'n.º{N}39', 2),
                ('página 2', 'página{N}2', 1), ('vv. 1 a 4', 'vv.{N}1 a{N}4', 1)]),
    dict(i=31, ficheiro='m7/lima-orpheu/index.html',
         pares=[('n.º 23621', 'n.º{N}23621', 2), ('número 2', 'número{N}2', 1), ('Orpheu 2', 'Orpheu{N}2', 4)]),
    dict(i=32, ficheiro='m7/m7-fingidor-maquina/index.html',
         pares=[('22 min', '22{N}min', 1), ('1.ª publ', '1.ª{N}publ', 4), ('n.º 36', 'n.º{N}36', 3),
                ('n.º 38', 'n.º{N}38', 1), ('estrofes 1 e 2', 'estrofes{N}1 e{N}2', 1)]),
    dict(i=33, ficheiro='m7/m7-quatro-vozes-um-problema/index.html',
         pares=[('23 min', '23{N}min', 1), ('13 de janeiro de 1935', '13{N}de janeiro de{N}1935', 2),
                ('n.º 2', 'n.º{N}2', 1), ('estrofes 1', 'estrofes{N}1', 1), ('poema X', 'poema{N}X', 2),
                ('poema IX', 'poema{N}IX', 1), ('1–3', '1–{J}3', 1)]),
    dict(i=36, ficheiro='m7/mapa-do-modulo-m7/index.html',
         pares=[('90 min', '90{N}min', 3), ('35 %', '35{N}%', 2), ('25 %', '25{N}%', 2), ('10 %', '10{N}%', 1),
                ('45 minutos', '45{N}minutos', 1), ('30 %', '30{N}%', 1),
                ('13 de junho de 1888', '13{N}de junho de{N}1888', 2),
                ('30 de novembro de 1935', '30{N}de novembro de{N}1935', 2),
                ('15 de outubro de 1890', '15{N}de outubro de{N}1890', 1),
                ('8 de março de 1914', '8{N}de março de{N}1914', 1),
                ('13 de janeiro de 1935', '13{N}de janeiro de{N}1935', 1), ('3.º ano', '3.º{N}ano', 2),
                ('1.ª edição', '1.ª{N}edição', 2), ('página 2', 'página{N}2', 2), ('século XV', 'século{N}XV', 1),
                ('D. Sebastião', 'D.{N}Sebastião', 2), ('D. Henrique', 'D.{N}Henrique', 2), ('M7-F01', 'M7-{J}F01', 4),
                ('M7-F04', 'M7-{J}F04', 3), ('M7-F06', 'M7-{J}F06', 6), ('M7-F08', 'M7-{J}F08', 4),
                ('M7-F05', 'M7-{J}F05', 3), ('M7-F11', 'M7-{J}F11', 1), ('M7-F34', 'M7-{J}F34', 1),
                ('Orpheu</i> 2', 'Orpheu</i>{N}2', 1)]),
    dict(i=37, ficheiro='m7/mensagem-mostrengo/index.html',
         pares=[('D. João II', 'D.{N}João{N}II', 1)]),
    dict(i=38, ficheiro='m7/mostrengo-leme-ramos/index.html',
         pares=[('ato III', 'ato{N}III', 1), ('século XVI', 'século{N}XVI', 1),
                ('do retrato de D. João', 'do retrato de D.{N}João', 1), ('Se D. João está vivo', 'Se D.{N}João está vivo', 1),
                ('que só D. João podia', 'que só D.{N}João podia', 1), ('mesma: D. João está vivo', 'mesma: D.{N}João está vivo', 1)],
         de={s: 'D. João' for s in ('do retrato de D. João', 'Se D. João está vivo', 'que só D. João podia', 'mesma: D. João está vivo')},
         fora={'«Sou D. João de Portugal»': (1, CITACAO), '«El-Rei D. João Segundo!»': (1, CITACAO)}),
    dict(i=39, ficheiro='m7/olhar-pessoa/index.html',
         pares=[('15 segundos', '15{N}segundos', 1), ('8 de março', '8{N}de março', 1)]),
    dict(i=53, ficheiro='m7/pessoa-ceifeira/index.html',
         pares=[('n.º 3', 'n.º{N}3', 2)]),
    dict(i=55, ficheiro='m7/portefolio-do-modulo-m7/index.html',
         pares=[('3.º ano', '3.º{N}ano', 2)]),
    dict(i=60, ficheiro='m7/santa-rita-fato/index.html',
         pares=[('n.º 46', 'n.º{N}46', 3), ('Orpheu 2', 'Orpheu{N}2', 2), ('Orpheu_ 2', 'Orpheu_{N}2', 5),
                ('1889–1918', '1889–{J}1918', 2), ('Orpheu</i> 2', 'Orpheu</i>{N}2', 1)]),
    dict(i=61, ficheiro='m7/sebastiana-nevoeiro/index.html',
         pares=[('D. Sebastião', 'D.{N}Sebastião', 1)]),
    dict(i=62, ficheiro='m7/tabacaria/index.html',
         pares=[('15 de janeiro de 1928', '15{N}de janeiro de{N}1928', 1), ('3.º ano', '3.º{N}ano', 2),
                ('2.º ano', '2.º{N}ano', 1), ('1.ª publ', '1.ª{N}publ', 1), ('século XIX', 'século{N}XIX', 2),
                ('n.º 39', 'n.º{N}39', 2)]),
    dict(i=64, ficheiro='m7/variacoes-rotulos/index.html',
         pares=[('21 de setembro de 2019', '21{N}de setembro de{N}2019', 2),
                ('10 de setembro de 2017', '10{N}de setembro de{N}2017', 2),
                ('12 de junho de 2018', '12{N}de junho de{N}2018', 3), ('1944–1984', '1944–{J}1984', 2)]),
    dict(i=65, ficheiro='m7/visita-casa-fernando-pessoa/index.html',
         pares=[('5 de novembro', '5{N}de novembro', 1), ('3.º ano', '3.º{N}ano', 2)]),
    dict(i=66, ficheiro='tarefas/m7-u1/aquecimento/index.html',
         pares=[('80 a 120 palavras', '80{N}a{N}120{N}palavras', 2), ('60 minutos', '60{N}minutos', 1),
                ('1.º verso', '1.º{N}verso', 1), ('4.ª estrofe', '4.ª{N}estrofe', 1), ('1.ª pessoa', '1.ª{N}pessoa', 1)]),
    dict(i=67, ficheiro='tarefas/m7-u1/index.html',
         pares=[('90 min', '90{N}min', 1), ('80 a 120 palavras', '80{N}a{N}120{N}palavras', 2),
                ('10 a 15 minutos', '10{N}a{N}15{N}minutos', 1)]),
    dict(i=68, ficheiro='tarefas/m7-u2/aquecimento/index.html',
         pares=[('13 de janeiro de 1935', '13{N}de janeiro de{N}1935', 3), ('M8-F01', 'M8-{J}F01', 1)]),
    dict(i=69, ficheiro='tarefas/m7-u2/index.html',
         pares=[('90 min', '90{N}min', 1), ('100 a 150 palavras', '100{N}a{N}150{N}palavras', 2),
                ('10 minutos', '10{N}minutos', 1)]),
    dict(i=70, ficheiro='tarefas/m7-u3/aquecimento/index.html',
         pares=[('180 a 220 palavras', '180{N}a{N}220{N}palavras', 1), ('1.º verso', '1.º{N}verso', 1), ('2.º ano', '2.º{N}ano', 1),
                ('verso de «D. Sebastião', 'verso de «D.{N}Sebastião', 1), ('_Mensagem_, «D. Sebastião', '_Mensagem_, «D.{N}Sebastião', 1),
                ('«Nevoeiro» e «D. Sebastião', '«Nevoeiro» e «D.{N}Sebastião', 1), ('D. João', 'D.{N}João', 2)],
         de={s: 'D. Sebastião' for s in ('verso de «D. Sebastião', '_Mensagem_, «D. Sebastião', '«Nevoeiro» e «D. Sebastião')},
         fora={'Relembrar F09, «D. Sebastião': (1, MENU)}),
    dict(i=71, ficheiro='tarefas/m7-u3/correcao/index.html',
         pares=[('180 a 220 palavras', '180{N}a{N}220{N}palavras', 1)]),
    dict(i=72, ficheiro='tarefas/m7-u3/grelha/index.html',
         pares=[('180 a 220 palavras', '180{N}a{N}220{N}palavras', 3), ('90 palavras', '90{N}palavras', 1)]),
    dict(i=73, ficheiro='tarefas/m7-u3/index.html',
         literais=[('durante 90 minutos, com entrega', 'durante 90{N}minutos, com entrega',
                    'a meta descrição muda com «nao_partir» (o gerador prende os três números do molde, como do M1 ao M6); a proposta '
                    'não a lista porque não se vê', 1)],
         pares=[('10 min', '10{N}min', 1), ('60 minutos', '60{N}minutos', 1), ('90 min', '90{N}min', 1),
                ('180 a 220 palavras', '180{N}a{N}220{N}palavras', 2), ('10 minutos', '10{N}minutos', 1),
                ('4 de agosto de 1578', '4{N}de agosto de{N}1578', 1),
                ('20 de fevereiro de 1933', '20{N}de fevereiro de{N}1933', 1), ('v. 1', 'v.{N}1', 1),
                ('D. Sebastião', 'D.{N}Sebastião', 3), ('D. João', 'D.{N}João', 1)]),
    dict(i=74, ficheiro='tarefas/m7-u1/aquecimento/index.html',
         pares=[('40 a 60', '40{N}a{N}60', 2), ('150 a 200', '150{N}a{N}200', 2), ('80 a 120', '80{N}a{N}120', 1)]),
]

# Os painéis de projeção: cada um com o seu achado.
PAINEIS = {f'm7/painel-m7-{f}/index.html': i for f, i in (
    ('f01', 40), ('f02', 41), ('f04', 42), ('f05', 43), ('f06', 44), ('f09', 45), ('f10', 46), ('f13', 48), ('f14', 49), ('f15', 50),
    ('f23', 51), ('f34', 52))}

# Sem cópias fora do módulo a mudar (as sessões do Exame não repetem nenhum dos trechos mudados) nem notas do docente geradas.
NOTAS = []

# A casca das lições fica para o molde, como do M1 ao M6: nenhuma troca. As lições com achado B.
CASCA_NO_MOLDE = sorted(x['ficheiro'] for x in ACHADOS_B if x['ficheiro'].startswith('m7/licao-'))

GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
CHAVES_TAREFA = (' "nao_partir": true,\n',
                 'Os números do molde da tarefa («90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) levam o espaço que não '
                 'quebra pelo gerador (scripts/tarefas_escolha.py), como do M1 ao M6.')
DADOS = [
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m7-u3.json', achados=(73,), chaves=('\n "unidade": 3,\n',) + CHAVES_TAREFA,
         pares=[p for p in next(x for x in ACHADOS_B if x['i'] == 73)['pares'] if p[0] not in ('10 min', '90 min')]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m7-u1.json', achados=(66,), pares=next(x for x in ACHADOS_B if x['i'] == 66)['pares']),
    dict(ficheiro='docs/pedagogia/aquecimentos/m7-u1.json', achados=(74,), pares=next(x for x in ACHADOS_B if x['i'] == 74)['pares']),
    dict(ficheiro='docs/pedagogia/aquecimentos/m7-u2.json', achados=(68,), pares=next(x for x in ACHADOS_B if x['i'] == 68)['pares']),
    dict(ficheiro='docs/pedagogia/aquecimentos/m7-u3.json', achados=(70,), pares=next(x for x in ACHADOS_B if x['i'] == 70)['pares']),
    dict(ficheiro=GRELHAS, entrada='m7-u3', achados=(71, 72), pares=next(x for x in ACHADOS_B if x['i'] == 72)['pares']),
]


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
    """O nome curto da página no manifesto. Os painéis de projeção (m7/painel-m7-fxx com CARTOES) não são notas do docente: só as
    notas editoriais (as das lições geradas, sem CARTOES) levam «(notas do docente)» (a revisão do M5 viu esse erro)."""
    m = re.match(r'm7/(?:licao|painel)-(m7-f\d+)/', rel)
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


# Os enunciados dos painéis do docente (m7/painel-m7-fxx) são os dos cartões da lição: o «p» (ou a «frase»), com ou sem os
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
    for licao in sorted(r for r in finais if r.startswith('m7/licao-')):
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
            # O seletor mostra o enunciado sem os marcadores de itálico (_…_) ou, nos painéis do M7, com o itálico em <i>.
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
