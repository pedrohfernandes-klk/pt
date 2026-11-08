#!/usr/bin/env python3
"""08/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M2 do Português.

Constrói scripts/cuidado_m2_20261108.json, a camada literal cuidado_m2_20261108, com os 29 achados CONFIRMADOS da varredura
de 6/11 (só leitura, com conferência independente) no M2: 5 achados de tabela (A), 20 de referências e números que se partiam
(B) e 4 casos do mesmo tipo (C). Os 7 achados que a conferência recusou (4, 5, 6, 7, 9, 10 e 13) não entram. A camada aplica-se
com scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/cuidado-m2-edits-20261108.json:

  python3 scripts/cuidado_m2_20261108.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m2_20261108.json --manifesto tests/fixtures/cuidado-m2-edits-20261108.json --nota "…"

Segue o modelo da camada do M1 (scripts/cuidado_m1_20261106.py), com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como na M7-F10, na M7-F15 e no M1: class apoio-tabela, th scope=col no
  cabeçalho, th scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader, rowheader, cell),
  porque no telemóvel a tabela passa a display:block. Dentro do JSON dos cartões (e dos itens da página «Pensar devagar»), as
  aspas vão com barra (\\"), como no resto do JSON. Cada página com uma tabela nova carrega assets/pt-lessons/apoios-tabelas.css
  antes de assets/appearance.css (a versão da folha é a do M1, 20261106.1: a folha não muda).
- B: U+00A0 (espaço que não quebra) depois de D. antes de nome e entre o nome e o numeral («D. João III», «D. Maria II»), depois de
  «c.» antes do ano, entre ordinal e nome (1.º ano), entre número e unidade (min, minutos, segundos, s, palavras, %, «por
  cento»), dentro dos intervalos «N a M palavras» e «N e M palavras» e dentro das datas («3 de março», «17 de janeiro de 2023»);
  U+2060 (junção de palavras) logo a seguir ao traço de intervalo («180–240», «1465–c. 1536») e no hífen das siglas de lição
  («M2-F01»). Em cada achado B mudam todas as ocorrências de cada trecho no ficheiro, salvo as que o próprio achado deixa de
  fora: a «frase» dos cartões sublinhar (as palavras contam-se por espaços, com índices em «certas») e os «alt» das imagens.
- C: o vocabulário da F06 com o termo inteiro a negrito (e a glosa do verso certa); a lista dos ficheiros do portefólio com
  cabeçalho, nomes inteiros e empilhada no telemóvel; os exemplos A, B e C da F14 em lista; os versos da F07 com a marcação de
  verso das outras lições do M2 (p.v, um span.ln com span.n por verso, sem itálico).
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois.

A casca das lições (migalhas, «Estás em», rodapé: achado 16) não muda aqui, ficheiro a ficheiro: muda no molde, como no M1 (a
camada cuidado_m1_20261106 não mexeu na casca das lições, e a proposta final do achado 16 é para o gerador da casca). Nas outras
páginas (índice do módulo, guia, mapa, portefólio e as duas páginas «Pensar devagar»), as migalhas mudam porque o achado da página
as inclui, como no índice e no guia do M1.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e listas e os espaços invisíveis. As trocas B não se
sobrepõem: cada troca leva só os espaços que muda; quando o mesmo trecho aparece noutro sítio que não muda, a troca leva o mínimo
de contexto que a distingue. O script calcula as trocas sobre a base (a página com esta camada desfeita pelo manifesto, quando ele
já existe): pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.

Páginas geradas: os aquecimentos da M2-U1 e da M2-U2 (scripts/aquecimentos.py) mudam também nos dados
(docs/pedagogia/aquecimentos/m2-u1.json e m2-u2.json), que estão na mesma camada, e regeneram-se sem diferenças. As páginas das
tarefas tarefas/m2-u1/ e m2-u2/ não são geradas (são o piloto de scripts/tarefas_escolha.py) e mudam só na página.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m2_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m2-edits-20261108.json'
NBSP, WJ = '\xa0', '⁠'
ACHADO = '08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M2, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como na M7-F10, na M7-F15 e no M1).',
    'B': 'Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e no hífen das siglas).',
    'C': 'Caso do mesmo tipo.',
}

# A folha das tabelas de apoio, antes da camada de aparência (como na M7-F10, na M7-F15 e no M1), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
COM_TABELA = {
    'm2/licao-m2-f02/index.html': 'lição', 'm2/licao-m2-f06/index.html': 'lição', 'm2/licao-m2-f07/index.html': 'lição',
    'm2/licao-m2-f09/index.html': 'lição', 'm2/m2-maquina-de-rir/index.html': 'página «Pensar devagar»',
}


def tabela(colunas, linhas):
    """A tabela de apoio, igual às do M1 (e às de scripts/tarefas_escolha.py), com as aspas escapadas como no JSON dos cartões.
    Uma célula None fica vazia e sem data-label (no telemóvel, um rótulo sem nada a seguir não serve)."""
    cab = ''.join(f'<th scope="col" role="columnheader">{c}</th>' for c in colunas)
    corpo = ''
    for linha in linhas:
        corpo += '<tr role="row"><th scope="row" role="rowheader">' + linha[0] + '</th>'
        for k, v in enumerate(linha[1:], 1):
            corpo += '<td role="cell"></td>' if v is None else f'<td role="cell" data-label="{colunas[k]}">{v}</td>'
        corpo += '</tr>'
    html = (f'<table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row">{cab}</tr></thead>'
            f'<tbody role="rowgroup">{corpo}</tbody></table>')
    return html.replace('"', '\\"')


def versos(linhas):
    """Os versos com a marcação das outras lições do M2 (F02, F06, F11): p.v, um span.ln por verso, com o span.n vazio que recua o
    verso (sem data-l, para não ligar as marcas de linha a meio da lição), separados pela quebra escapada do JSON (\\n)."""
    return ('<p class=\\"v\\">' + '\\n'.join('<span class=\\"ln\\"><span class=\\"n\\"></span>' + l + '</span>' for l in linhas)
            + '</p>')


# Os versos da F07 (achado 15): cada bloco <p><i>…<br>…</i></p> dos cartões 2, 3 e 4, a rubrica e a fala de um verso.
VERSOS_F07 = [
    (2, ['Mãe: Tomai aquela cadeira.', 'Pêro Marques: E que val aqui uma destas?', 'Inês (à parte): Ó Jesu! que João das bestas!',
         'Olhai aquela canseira!']),
    (2, ['Rubrica: Assentou-se com as costas pera elas, e diz:']),
    (2, ['Pêro Marques: Eu cuido que não estou bem...']),
    (2, ['Cuido que lhe trago aqui', 'Pêras da minha pereira...', 'Hão-de estar na derradeira.', 'Tende ora, Inês, per i.',
         'Inês: E isso hei-de ter na mão?', 'Pêro Marques: Deitae as peas no chão.', 'Inês: As perlas pera enfiar..',
         'Três chocalhos e um novelo...', 'E as peias no capelo...', 'E as pêras? Onde estão?', 'Pêro Marques: Nunca tal me aconteceu!',
         "Algum rapaz m'as comeu..."]),
    (3, ['Vidal: Esperai, aguardai ora!', 'Soubemos dum escudeiro', "De feição d'atafoneiro", 'Que virá logo essora,',
         "Que fala... e com' ora fala!", 'Estrugirá esta sala.', "E tange... e com' ora tange!"]),
    (3, ['Escudeiro: E se me vires mentir', 'Gabando-me de privado,', 'Está tu dissimulado,', 'Ou sai-te pera fora a rir',
         'Isto te aviso daqui,', 'Faze-o por amor de mi.', 'Moço: Porém, senhor digo eu', 'Que mau calçado é o meu',
         'Pera estas vistas assi.', 'Escudeiro: Que farei, que o sapateiro', 'Não tem solas nem tem pele?',
         'Moço: Sapatos me daria ele,', 'Se me vós désseis dinheiro...', 'Escudeiro: Eu o haverei agora.',
         'E mais calças te prometo.', 'Moço (à parte): Homem que não tem nem preto,', 'Casa muito na má hora.']),
    (4, ['Escudeiro: Vós cantais, Inês Pereira?', "Em vodas m'andáveis vós?", 'Juro ao corpo de Deus',
         'Que esta seja a derradeira!']),
    (4, ['Vós não haveis de falar', 'Com homem nem mulher que seja;', 'Nem somente ir à igreja', 'Não vos quero eu leixar',
         'Já vos preguei as janelas,', 'Por que não vos ponhais nelas.', 'Estareis aqui encerrada', 'Nesta casa, tão fechada',
         "Como freira d'Oudivelas."]),
    (4, ['Inês: Que pecado foi o meu?', 'Porque me dais tal prisão?', 'Escudeiro: Vós buscastes discrição,',
         'Que culpa vos tenho eu?', 'Pode ser maior aviso,', 'Maior discrição e siso', 'Que guardar o meu tisouro?',
         'Não sois vós, mulher meu ouro?', 'Que mal faço em guardar isso?']),
]

# A lista dos ficheiros do portefólio (achado 12): as 15 linhas de hoje, todos os nomes em <code>.
FICHEIROS = [
    ('M2_capa', 'Capa: nome, turma, módulo, data de início e de fim.', True),
    ('M2_cartao-do-percurso', 'Registo anterior, facultativo. Se já o guardaste, conserva-o; não é preciso gerar outro cartão.', True),
    ('M2_U1_folha_&lt;dia-mês&gt;', 'Unidade 1, «Ler a Farsa: desejos, escolhas e consequências»: registo da aula, com nome e data.', False),
    ('M2_U1_pergunta', 'Como transformam as escolhas de Inês o seu desejo de liberdade? Síntese de duas linhas no papel da aula de '
     'tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra síntese.', False),
    ('M2_U1_o-que-aprendi', 'Recupera a síntese da aula de tarefa. Conserva outras reflexões já feitas, sem produzir uma nova.', False),
    ('M2_U2_folha_&lt;dia-mês&gt;', 'Unidade 2, «Interpretar e representar: crítica, cena e atualidade»: registo da aula, com nome e data.', False),
    ('M2_U2_pergunta', 'Como sustentar uma leitura da Farsa e transformá-la numa proposta de representação? Síntese de duas linhas no '
     'papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra síntese.', False),
    ('M2_U2_o-que-aprendi', 'Recupera a síntese da aula de tarefa. Conserva outras reflexões já feitas, sem produzir uma nova.', False),
    ('M2_Tarefa1', 'Tarefa 1, «Apreciação crítica da <i>Farsa de Inês Pereira</i> no teatro»: o produto entregue (ou a ligação) e uma '
     'linha: o que fiz, o que corrigi depois da devolução.', True),
    ('M2_Tarefa2', 'Tarefa 2, «Recontagem contemporânea da farsa em vídeo»: o teu produto, ou a ligação para ele.', True),
    ('M2_Tarefa3', 'Tarefa 3, «Dois anúncios de casamento»: o teu produto, ou a ligação para ele.', True),
    ('M2_Revisao1', 'A Revisão 1, corrigida e somada, fotografada na própria aula.', True),
    ('M2_Revisao2', 'A Revisão 2, corrigida e somada, fotografada na própria aula.', True),
    ('M2_Prova-escrita', 'A prova escrita, corrigida, fotografada quando te for devolvida.', True),
    ('M2_balanco', 'Usa os trabalhos já entregues se o docente pedir o balanço previsto. Os registos anteriores são facultativos; '
     'mantêm-se os parâmetros e as ponderações.', True),
]
LISTA_ANTES = ('<table><tr><th style="width:36%">Nome do ficheiro</th><th>O que é</th></tr>'
               + ''.join(f'<tr><td>{f"<code>{n}</code>" if code else n}</td><td>{d}</td></tr>' for n, d, code in FICHEIROS)
               + '</table>')
LISTA_DEPOIS = ('<table class="lista-ficheiros"><thead><tr><th scope="col">Nome do ficheiro</th><th scope="col">O que é</th></tr>'
                '</thead><tbody>'
                + ''.join(f'<tr><td data-th="Nome do ficheiro"><code>{n}</code></td><td data-th="O que é">{d}</td></tr>'
                          for n, d, _ in FICHEIROS)
                + '</tbody></table>')
# As regras da lista, no <style> da própria página (fora das lições não há folha comum para ela): os nomes não se partem no
# hífen, e até 560 px cada linha empilha (o nome e, por baixo, o que é).
CSS_ANCORA = 'code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
CSS_LISTA = ('.lista-ficheiros code{white-space:nowrap}@media (max-width:560px){.lista-ficheiros,.lista-ficheiros tbody,'
             '.lista-ficheiros tr,.lista-ficheiros td{display:block;width:auto}.lista-ficheiros thead{position:absolute;width:1px;'
             'height:1px;overflow:hidden;clip-path:inset(50%)}.lista-ficheiros tr{border-top:2px solid currentColor;padding:6px 0}'
             '.lista-ficheiros td{border:0;padding:2px 0}}\n')


def bloco_f07(linhas):
    return '<p><i>' + '<br>'.join(linhas) + '</i></p>'


# Os achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte).
ACHADOS_AC = [
    dict(i=0, cat='A', ficheiro='m2/licao-m2-f02/index.html',
         cartao='cartão 23, Para entender (caixa «Recorda: cinco recursos»)',
         antigo='<p><b>Comparação</b>: aproxima duas coisas com «como» («Licença, como a bugia»). <b>Metáfora</b>: dá a uma coisa o '
                'nome de outra, sem «como» («cativa / Em poder de desfiados»). <b>Enumeração</b>: acumula termos numa lista («Rico, '
                'honrado, conhecido», diz Lianor Vaz). <b>Antítese</b>: põe frente a frente dois opostos («sam aguçosa / E vós '
                'dais-vos de vagar»). <b>Interrogação retórica</b>: pergunta que não espera resposta («Ou cuidas que é dia santo?»).</p>',
         novo=tabela(['Recurso', 'O que faz', 'Exemplo'], [
             ['Comparação', 'aproxima duas coisas com «como»', '«Licença, como a bugia»'],
             ['Metáfora', 'dá a uma coisa o nome de outra, sem «como»', '«cativa / Em poder de desfiados»'],
             ['Enumeração', 'acumula termos numa lista', '«Rico, honrado, conhecido», diz Lianor Vaz'],
             ['Antítese', 'põe frente a frente dois opostos', '«sam aguçosa / E vós dais-vos de vagar»'],
             ['Interrogação retórica', 'pergunta que não espera resposta', '«Ou cuidas que é dia santo?»']])),
    dict(i=1, cat='A', ficheiro='m2/licao-m2-f07/index.html',
         cartao='cartão 7, Para entender (detalhe «Consultar os tipos de orações e os conectores», caixa «Coordenadas»)',
         antigo='<p><b>Coordenadas</b> (as orações ligam-se sem que nenhuma esteja dentro da outra): copulativas (e, nem), adversativas '
                '(mas; também porém, contudo, todavia, que são advérbios de ligação), disjuntivas (ou), conclusivas (logo; também '
                'portanto e por isso, advérbios de ligação), explicativas (pois, que).</p>',
         novo='<p><b>Coordenadas</b> (as orações ligam-se sem que nenhuma esteja dentro da outra):</p>' + tabela(['Tipo', 'Conectores'], [
             ['copulativas', 'e, nem'], ['adversativas', 'mas; também porém, contudo, todavia, que são advérbios de ligação'],
             ['disjuntivas', 'ou'], ['conclusivas', 'logo; também portanto e por isso, advérbios de ligação'],
             ['explicativas', 'pois, que']])),
    dict(i=1, cat='A', ficheiro='m2/licao-m2-f07/index.html',
         cartao='cartão 7, Para entender (detalhe «Consultar os tipos de orações e os conectores», caixa «Subordinadas»)',
         antigo='<p><b>Subordinadas</b> (uma ocupa um lugar dentro da outra): <b>substantivas</b> completivas (que, se) ou relativas sem '
                'antecedente; <b>adjetivas relativas</b> restritivas ou explicativas; <b>adverbiais</b> causais (porque), temporais '
                '(quando), condicionais (se), finais (para que), concessivas (embora), consecutivas (tão… que), comparativas (como).</p>',
         novo='<p><b>Subordinadas</b> (uma ocupa um lugar dentro da outra): <b>substantivas</b> completivas (que, se) ou relativas sem '
              'antecedente; <b>adjetivas relativas</b> restritivas ou explicativas; <b>adverbiais</b>:</p>' + tabela(['Tipo', 'Conector'], [
                  ['causais', 'porque'], ['temporais', 'quando'], ['condicionais', 'se'], ['finais', 'para que'],
                  ['concessivas', 'embora'], ['consecutivas', 'tão… que'], ['comparativas', 'como']])),
    dict(i=2, cat='A', ficheiro='m2/licao-m2-f09/index.html',
         cartao='cartão 2, Para entender (detalhe «Desenvolver a proposta no projeto de turma», caixa «Roteiro da apresentação oral»)',
         antigo='<p><b>Cinco minutos, quatro passos.</b> 1) O provérbio e o par asno/cavalo que escolheste (meio minuto). 2) O mapa: em '
                'que se transformou cada momento da farsa, e uma escolha de que te orgulhas (dois minutos). 3) Uma dificuldade e como '
                'a resolveste (um minuto). 4) A tua resposta à pergunta do módulo: <b>o que é que escolheste mudar na tua recontagem, '
                'e porquê?</b> (um minuto). Sobra meio minuto para uma pergunta da turma.</p>',
         novo='<p><b>Cinco minutos, quatro passos.</b></p>' + tabela(['Passo', 'Conteúdo', 'Tempo'], [
             ['1', 'O provérbio e o par asno/cavalo que escolheste', 'meio minuto'],
             ['2', 'O mapa: em que se transformou cada momento da farsa, e uma escolha de que te orgulhas', 'dois minutos'],
             ['3', 'Uma dificuldade e como a resolveste', 'um minuto'],
             ['4', 'A tua resposta à pergunta do módulo: <b>o que é que escolheste mudar na tua recontagem, e porquê?</b>', 'um minuto']])
              + '<p>Sobra meio minuto para uma pergunta da turma.</p>'),
    dict(i=3, cat='A', ficheiro='m2/m2-maquina-de-rir/index.html',
         cartao='item 6, Ato 2 «As peças da máquina»',
         nota='A célula do exemplo do monólogo fica vazia e sem data-label (o texto não traz exemplo, e um rótulo sem nada não serve no '
              'telemóvel); sai a vírgula de «tipo social, e entra», que só separava a enumeração que passa à coluna Exemplo.',
         antigo='<p>As peças têm nome nas lições. A personagem-tipo: cada figura é um tipo social, o lavrador rico e simples, o fidalgo '
                'pobre que se gaba, a alcoviteira que vende, o falso religioso, e entra vestida do que é. A rubrica, texto secundário, '
                'manda o gesto: «Assentou-se com as costas pera elas».</p><p>O aparte: a fala que só a sala ouve, «Ó Jesu! que João '
                'das bestas!». O monólogo: a fala de quem está só em cena. O duplo sentido: a palavra que uma personagem ouve de uma '
                'maneira e a sala de outra, como «mor gado» e «morgado». Lê a fala de Pêro com estas peças na cabeça.</p>',
         novo='<p>As peças têm nome nas lições.</p>' + tabela(['Peça', 'O que faz', 'Exemplo'], [
             ['A personagem-tipo', 'cada figura é um tipo social e entra vestida do que é',
              'o lavrador rico e simples, o fidalgo pobre que se gaba, a alcoviteira que vende, o falso religioso'],
             ['A rubrica', 'texto secundário, manda o gesto', '«Assentou-se com as costas pera elas»'],
             ['O aparte', 'a fala que só a sala ouve', '«Ó Jesu! que João das bestas!»'],
             ['O monólogo', 'a fala de quem está só em cena', None],
             ['O duplo sentido', 'a palavra que uma personagem ouve de uma maneira e a sala de outra', '«mor gado» e «morgado»']])
              + '<p>Lê a fala de Pêro com estas peças na cabeça.</p>'),
    dict(i=8, cat='A', ficheiro='m2/licao-m2-f06/index.html',
         cartao='cartão 28, Para entender (caixa «Recorda»)',
         antigo='<p><b>Anáfora</b>: a mesma palavra a abrir versos seguidos. <b>Antítese</b>: duas ideias opostas lado a lado. '
                '<b>Provérbio</b>: frase feita que guarda um saber comum. <b>Duplo sentido</b>: a frase diz uma coisa a quem está em '
                'cena e outra ao público.</p>',
         novo=tabela(['Recurso', 'O que é'], [
             ['Anáfora', 'a mesma palavra a abrir versos seguidos.'], ['Antítese', 'duas ideias opostas lado a lado.'],
             ['Provérbio', 'frase feita que guarda um saber comum.'],
             ['Duplo sentido', 'a frase diz uma coisa a quem está em cena e outra ao público.']])),
    dict(i=11, cat='C', ficheiro='m2/licao-m2-f06/index.html',
         cartao='cartão 15, o verso 80 («Señores, por caridad»): a glosa ao toque cobre o termo inteiro',
         nota='Os outros vocabulários do M2 ficam como estão (o termo vai sempre a negrito); só se acerta o defeito real da F06.',
         antigo='<b class=\\"gt\\" data-s=\\"por caridad, senhores, por caridade\\">Señores</b>, por caridad</span>',
         novo='<b class=\\"gt\\" data-s=\\"senhores, por caridade\\">Señores, por caridad</b></span>'),
    dict(i=11, cat='C', ficheiro='m2/licao-m2-f06/index.html',
         cartao='cartão 18, Vocabulário: o termo «Señores, por caridad» inteiro a negrito',
         nota='Os outros vocabulários do M2 ficam como estão (o termo vai sempre a negrito); só se acerta o defeito real da F06.',
         antigo='<b>Señores</b>, por caridad, senhores, por caridade;',
         novo='<b>Señores, por caridad</b>, senhores, por caridade;'),
    dict(i=11, cat='C', ficheiro='m2/licao-m2-f06/index.html',
         cartao='cartão 18, Vocabulário: o termo «haced que el tiempo pasado no se cuente por perdido» a negrito, como os outros',
         nota='Os outros vocabulários do M2 ficam como estão (o termo vai sempre a negrito); só se acerta o defeito real da F06.',
         antigo='; haced que el tiempo pasado no se cuente por perdido, fazei',
         novo='; <b>haced que el tiempo pasado no se cuente por perdido</b>, fazei'),
    dict(i=12, cat='C', ficheiro='m2/portefolio-do-modulo-m2/index.html',
         cartao='secção «A lista de verificação»: a tabela dos ficheiros com cabeçalho, nomes inteiros e linhas que empilham no telemóvel',
         nota='Todos os nomes em <code>; sem U+2011 nem junção dentro dos nomes, que mudariam o que se copia.',
         antigo=LISTA_ANTES, novo=LISTA_DEPOIS),
    dict(i=12, cat='C', ficheiro='m2/portefolio-do-modulo-m2/index.html',
         cartao='cabeça (<style> da página): as regras da lista dos ficheiros',
         nota='As regras ficam no <style> da própria página.',
         antigo=CSS_ANCORA, novo=CSS_ANCORA + CSS_LISTA),
    dict(i=14, cat='C', ficheiro='m2/licao-m2-f14/index.html',
         cartao='cartão 12, Compara «A mesma forma, outros efeitos»: os exemplos A, B e C em lista',
         nota='Sem o valor de cada exemplo, que daria a resposta do cartão seguinte; as barras dos fechos ficam escapadas (<\\/p>), '
              'como no resto da fonte.',
         antigo='<p>Exemplos criados para esta lição. A: Guardei a casinha de madeira da maqueta. B: A nossa casinha acolheu toda a '
                'família. C: É só uma casinha, não merece atenção.<\\/p>',
         novo='<p>Exemplos criados para esta lição.<\\/p><ul><li><b>A:<\\/b> Guardei a casinha de madeira da maqueta.<\\/li><li><b>B:'
              '<\\/b> A nossa casinha acolheu toda a família.<\\/li><li><b>C:<\\/b> É só uma casinha, não merece atenção.<\\/li><\\/ul>'),
] + [
    dict(i=15, cat='C', ficheiro='m2/licao-m2-f07/index.html',
         cartao=f'cartão {c}, Ler a cena: o bloco «{linhas[0]}» com a marcação de verso',
         nota='A marcação das outras lições do M2 (p.v, span.ln, span.n vazio, sem data-l), sem itálico; a rubrica fica numa linha '
              '«Rubrica: …», como na F02; os […], as notas e as fontes ficam.',
         antigo=bloco_f07(linhas), novo=versos(linhas))
    for c, linhas in VERSOS_F07
]

# Os 20 achados B confirmados: (trecho, proposta, ocorrências do trecho na base, sem as que o achado deixa de fora). As contagens
# são as da conferência; onde um trecho está dentro de outro do mesmo achado («90 min» em «90 minutos», «5 minutos» em «15
# minutos»), conta-se cada ocorrência do trecho, como na conferência.
D_JOAO = ('D. João III', 'D.\xa0João\xa0III')
D_MARIA = ('D. Maria II', 'D.\xa0Maria\xa0II')
ANO = ('1.º ano', '1.º\xa0ano')
ACHADOS_B = [
    dict(i=16, ficheiro=None, cartao='casca das lições (migalhas, «Estás em», rodapé)', ocorrencias=34, pares=[]),
    dict(i=17, ficheiro='m2/licao-m2-f01/index.html', cartao='cartões 1, 3, 6 (f), 7 e 10', ocorrencias=7,
         pares=[('(4 min)', '(4\xa0min)', 2), D_JOAO + (5,)]),
    dict(i=18, ficheiro='m2/licao-m2-f08/index.html', cartao='cartões 0, 1, 2 e 4 e pistas', ocorrencias=9,
         pares=[('180 a 240 palavras', '180\xa0a\xa0240\xa0palavras', 1), ('25 %', '25\xa0%', 1), D_MARIA + (3,), ('(5 min)', '(5\xa0min)', 2),
                ('180–240 palavras', '180–⁠240\xa0palavras', 1), ('25 por cento', '25\xa0por cento', 1)]),
    dict(i=19, ficheiro='m2/licao-m2-f09/index.html', cartao='cartões 0 (legenda), 2 (tabela, vídeo e créditos) e 3 (f)', ocorrencias=7,
         pares=[('30 segundos', '30\xa0segundos', 1), ('(30 s)', '(30\xa0s)', 2), D_MARIA + (2,),
                ('<figcaption>D. João III', '<figcaption>D.\xa0João\xa0III', 1), ('25 por cento', '25\xa0por cento', 1)]),
    dict(i=20, ficheiro='m2/licao-m2-f10/index.html', cartao='cartão 16, sublinhar (só no campo f)', ocorrencias=1,
         pares=[('3 de março', '3\xa0de\xa0março', 1)]),
    dict(i=21, ficheiro='m2/licao-m2-f11/index.html', cartao='cartão 1 e pistas', ocorrencias=2,
         pares=[('100 a 130 palavras', '100\xa0a\xa0130\xa0palavras', 2)]),
    dict(i=22, ficheiro='m2/licao-m2-f12/index.html', cartao='cartões 1 e 8 (vídeos)', ocorrencias=4,
         pares=[('(3 min)', '(3\xa0min)', 2), ('(1 min)', '(1\xa0min)', 2)]),
    dict(i=23, ficheiro='m2/licao-m2-f13/index.html', cartao='cartão 8 (vídeo)', ocorrencias=2,
         pares=[('(1 min)', '(1\xa0min)', 2)]),
    dict(i=24, ficheiro='m2/licao-m2-f15/index.html', cartao='cartão 3 (referência ao Ciberdúvidas)', ocorrencias=1,
         pares=[('17 de janeiro de 2023', '17\xa0de\xa0janeiro\xa0de\xa02023', 1)]),
    dict(i=25, ficheiro='m2/licao-m2-f07/index.html', cartao='cartão 0 (legenda da imagem)', ocorrencias=1,
         pares=[('<figcaption>D. João III', '<figcaption>D.\xa0João\xa0III', 1)]),
    dict(i=26, ficheiro='m2/index.html', cartao='página do módulo e arquivo de perguntas', ocorrencias=24,
         pares=[('90 minutos', '90\xa0minutos', 4), ('90 min', '90\xa0min', 8), ('10 min', '10\xa0min', 2), ('25 por cento', '25\xa0por cento', 1),
                ('30 segundos', '30\xa0segundos', 1), ANO + (3,), D_JOAO + (3,), ('3 de março', '3\xa0de\xa0março', 2),
                ('30 %', '30\xa0%', 3), ('10 %', '10\xa0%', 1)]),
    dict(i=27, ficheiro='m2/guia-da-tarefa-m2/index.html', cartao='guia e dados T das tarefas de arquivo', ocorrencias=21,
         pares=[('90 minutos', '90\xa0minutos', 1), ('90 min', '90\xa0min', 3), ('10 minutos', '10\xa0minutos', 1),
                ('5 minutos', '5\xa0minutos', 3), ('15 min', '15\xa0min', 2), ('60 min', '60\xa0min', 1),
                ('220 a 280 palavras', '220\xa0a\xa0280\xa0palavras', 2), ('180 a 240 palavras', '180\xa0a\xa0240\xa0palavras', 1),
                ('80 a 120 palavras', '80\xa0a\xa0120\xa0palavras', 1), ('3 a 5 minutos', '3\xa0a\xa05\xa0minutos', 2),
                ('100 a 130 palavras', '100\xa0a\xa0130\xa0palavras', 4), ANO + (2,)]),
    dict(i=28, ficheiro='m2/mapa-do-modulo-m2/index.html', cartao='mapa (cabeçalho, caminho, obras, «Quando», tarefas, «Para ver»)',
         ocorrencias=19,
         pares=[('90 min', '90\xa0min', 2), ('45 minutos', '45\xa0minutos', 1), ('30 %', '30\xa0%', 4), ('10 %', '10\xa0%', 1), ANO + (2,),
                ('Lição M2-F01</a>', 'Lição M2-⁠F01</a>', 4), ('perante D. João III', 'perante D.\xa0João\xa0III', 2),
                ('<p class="info-i-texto">D. João III', '<p class="info-i-texto">D.\xa0João\xa0III', 1),
                ('<figcaption>D. João III', '<figcaption>D.\xa0João\xa0III', 1),
                ('c. 1465–c. 1536', 'c.\xa01465–⁠c.\xa01536', 2)]),
    dict(i=29, ficheiro='m2/portefolio-do-modulo-m2/index.html', cartao='migalhas e cabeçalho', ocorrencias=2, pares=[ANO + (2,)]),
    dict(i=30, ficheiro='tarefas/m2-u1/index.html', cartao='aquecer, cabeçalho, enunciado, critérios e dossiê do tema B', ocorrencias=12,
         pares=[('10 min', '10\xa0min', 2), ('10 minutos', '10\xa0minutos', 1), ('5 minutos', '5\xa0minutos', 2), ('60 minutos', '60\xa0minutos', 1),
                ('15 minutos', '15\xa0minutos', 1), ('90 minutos', '90\xa0minutos', 2), ('90 min', '90\xa0min', 3),
                ('180 a 240 palavras', '180\xa0a\xa0240\xa0palavras', 1), ('80 a 140', '80\xa0a\xa0140', 1),
                ('180 e 240 palavras', '180\xa0e\xa0240\xa0palavras', 1), D_JOAO + (1,), D_MARIA + (1,)]),
    dict(i=31, ficheiro='tarefas/m2-u2/index.html', cartao='aquecer, cabeçalho, enunciado, critérios e dossiê do tema B', ocorrencias=14,
         pares=[('10 min', '10\xa0min', 2), ('10 minutos', '10\xa0minutos', 1), ('5 minutos', '5\xa0minutos', 2), ('60 minutos', '60\xa0minutos', 1),
                ('15 minutos', '15\xa0minutos', 1), ('90 minutos', '90\xa0minutos', 2), ('90 min', '90\xa0min', 3),
                ('200 a 260 palavras', '200\xa0a\xa0260\xa0palavras', 1), ('100 a 160', '100\xa0a\xa0160', 1),
                ('50 a 80 palavras', '50\xa0a\xa080\xa0palavras', 1), ('200 e 260 palavras', '200\xa0e\xa0260\xa0palavras', 1),
                D_JOAO + (1,), D_MARIA + (2,)]),
    dict(i=32, ficheiro='tarefas/m2-u1/aquecimento/index.html', cartao='cartão 5, ordenar (campo p)', ocorrencias=1,
         pares=[('180 a 240 palavras', '180\xa0a\xa0240\xa0palavras', 1)]),
    dict(i=33, ficheiro='tarefas/m2-u2/aquecimento/index.html', cartao='cartão 10, vf (p e p2), e cartão 11, Para levar', ocorrencias=6,
         pares=[('230 palavras', '230\xa0palavras', 1), ('70 palavras', '70\xa0palavras', 1),
                ('200 a 260 palavras', '200\xa0a\xa0260\xa0palavras', 2), ('50 a 80', '50\xa0a\xa080', 2)]),
    dict(i=34, ficheiro='m2/m2-maquina-de-rir/index.html', cartao='item 0, item 17 e migalhas', ocorrencias=3,
         pares=[('20 min', '20\xa0min', 1), ANO + (1,), D_JOAO + (1,)]),
    dict(i=35, ficheiro='m2/m2-ines-escolhe-duas-vezes/index.html', cartao='item 0 e migalhas', ocorrencias=2,
         pares=[('22 min', '22\xa0min', 1), ANO + (1,)]),
]

# Achados B: o que o próprio achado deixa de fora.
# - A «frase» do cartão sublinhar do lead (F10 e o mesmo cartão no arquivo do índice): as palavras contam-se por espaços e
#   «certas» guarda os índices [6, 7, 8, 9]; o «f» e o «p» do escolha mudam.
# - Os «alt» das imagens de D. João III (F07 e F09): o alt não se vê; muda a legenda.
FRASE_LEAD = '"frase":"Trinta alunos do 1.º ano viram, no Teatro da Escola, a 3 de março,"'
ALT_D_JOAO = 'alt=\\"D. João III (Anthonis Mor, 1552)\\"'
EXCLUIR = {
    20: {'3 de março': [FRASE_LEAD]},
    26: {'3 de março': [FRASE_LEAD], '1.º ano': [FRASE_LEAD]},
}
# A casca das lições (achado 16) fica para o molde, como no M1: nenhuma troca. As lições onde a conferência a viu.
CASCA_NO_MOLDE = {16: ['m2/licao-m2-f01/index.html', 'm2/licao-m2-f02/index.html', 'm2/licao-m2-f06/index.html',
                       'm2/licao-m2-f07/index.html', 'm2/licao-m2-f08/index.html', 'm2/licao-m2-f09/index.html',
                       'm2/licao-m2-f10/index.html', 'm2/licao-m2-f11/index.html']}

# Dados dos geradores: os aquecimentos da M2-U1 e da M2-U2 (scripts/aquecimentos.py); os achados B entram nos textos dos dados,
# que passam iguais para as páginas.
DADOS = [
    dict(ficheiro='docs/pedagogia/aquecimentos/m2-u1.json', entradas=[(None, (32,))]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m2-u2.json', entradas=[(None, (33,))]),
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
    (posição, 'wj') põe U+2060 antes do carácter nessa posição. Mais nada é permitido num achado B."""
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
        else:
            raise SystemExit(f'achado B com uma mudança que não é de espaço: {antigo!r} > {novo!r}')
    return out


def aplicar_edicoes(texto, eds):
    for pos, tipo in sorted(eds, reverse=True):
        if tipo == 'nbsp':
            assert texto[pos] == ' ', (pos, texto[pos - 20:pos + 20])
            texto = texto[:pos] + NBSP + texto[pos + 1:]
        else:
            texto = texto[:pos] + WJ + texto[pos:]
    return texto


def janela_novo(pre, s, e, eds):
    """O texto da janela [s, e) de pre com as edições dela aplicadas."""
    return aplicar_edicoes(pre[s:e], [(p - s, t) for p, t in eds])


def janelas_b(rel, pre, pares, regioes, excluir=None, limite=None):
    """As janelas das ocorrências dos pares (antigo, novo, n) em pre (a base com as trocas A e C já feitas): [início, fim,
    {edições}, índice do par]. Cada par tem de aparecer exatamente n vezes (fora do que o achado deixa de fora)."""
    janelas, contagens = [], []
    for k, (antigo, novo, esperado) in enumerate(pares):
        eds_rel = edicoes(antigo, novo)
        n = 0
        for m in re.finditer(re.escape(antigo), pre):
            s, e = m.start(), m.end()
            if limite and not (limite[0] <= s and e <= limite[1]):
                continue
            if any(_cobre(pre, s, e, c) for c in (excluir or {}).get(antigo, [])):
                continue
            if any(a <= s < b or a < e <= b for a, b in regioes):
                raise SystemExit(f'{rel}: «{antigo}» dentro do texto novo de um achado A/C')
            janelas.append([s, e, {(s + p, t) for p, t in eds_rel}, k])
            n += 1
        if esperado is not None and n != esperado:
            raise SystemExit(f'{rel}: «{antigo}» aparece {n} vez(es), e o achado conta {esperado}')
        contagens.append(n)
    return janelas, contagens


def juntar(janelas):
    """Junta as janelas que partilham uma edição ou em que uma tem uma edição da outra lá dentro (por exemplo «90 min» dentro de
    «90 minutos», ou «5 minutos» dentro de «3 a 5 minutos»): uma troca nunca leva uma edição de outra."""
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


def _cobre(pre, s, e, contexto):
    """A ocorrência [s, e) está dentro de uma ocorrência do contexto excluído."""
    a0 = max(0, s - len(contexto))
    for m in re.finditer(re.escape(contexto), pre[a0:e + len(contexto)]):
        if a0 + m.start() <= s and e <= a0 + m.end():
            return True
    return False


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
            return f'{pagina}: «{par}» com espaço que não quebra'
        contexto = antigo if len(antigo) <= 60 else antigo[:57].rstrip() + '…'
        return f'{pagina}: «{par}» com espaço que não quebra (com o contexto «{contexto}»)'
    return f


def nome(rel):
    m = re.match(r'm2/licao-(m2-f\d+)/', rel)
    return m.group(1).upper() if m else rel.replace('/index.html', '')


def substituir(pre, regioes, antes, depois):
    """Troca um trecho único e atualiza as regiões de texto novo (onde nenhum par B pode cair)."""
    if pre.count(antes) != 1:
        raise SystemExit(f'trecho que não aparece uma vez: {antes[:80]!r}')
    inicio = pre.index(antes)
    delta = len(depois) - len(antes)
    regioes = [(a if a < inicio else a + delta, b if b <= inicio else b + delta) for a, b in regioes]
    return pre.replace(antes, depois), regioes + [(inicio, inicio + len(depois))]


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
        ligacoes = re.findall(r'<link rel="stylesheet" href="((?:\.\./)+)assets/appearance\.css\?v=[^"]+">', pre)
        if len(ligacoes) != 1:
            raise SystemExit(f'{rel}: a ligação à camada de aparência não aparece uma vez')
        aparencia = re.search(r'<link rel="stylesheet" href="(?:\.\./)+assets/appearance\.css\?v=[^"]+">', pre).group(0)
        folha = FOLHA.format(ligacoes[0])
        pre, regioes = substituir(pre, regioes, aparencia, folha + aparencia)
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}, cabeça: a folha das tabelas de apoio, antes da camada de aparência',
                       'antigo': aparencia, 'novo': folha + aparencia, 'ocorrencias': 1,
                       'achado': ACHADO.format(i=', '.join(str(i) for i in dict.fromkeys(x['i'] for x in achados_ac if x['cat'] == 'A')), cat='A',
                                               texto=f'A {COM_TABELA[rel]} passa a carregar as tabelas de apoio, antes da camada de aparência.')})
    for x in achados_b:
        janelas, contagens = janelas_b(rel, pre, x['pares'], regioes, EXCLUIR.get(x['i']))
        ts, final = trocas_de_janelas(rel, base_txt, pre, juntar(janelas), x['pares'],
                                      lambda k, i=x['i']: ACHADO.format(i=i, cat='B', texto=TEXTO_CAT['B']), local_b(nome(rel)))
        pre = final
        trocas += ts
        relatorio.append((rel, x['i'], 'B', sum(contagens), x['ocorrencias'],
                          ' '.join(f'{p[0]!r}x{c}' for p, c in zip(x['pares'], contagens))))
    return base_txt, pre, trocas, relatorio


def trocas_dados(spec, por_i):
    rel = spec['ficheiro']
    base_txt = base(rel)
    pre, regioes = base_txt, []
    janelas, pares, nomes = [], [], []
    for entrada, achados in spec['entradas']:
        for i in achados:
            for p in por_i[i]['pares']:
                js, _ = janelas_b(rel, pre, [p], regioes)
                for j in js:
                    j[3] = len(pares)
                janelas += js
                pares.append(p)
                nomes.append('/'.join(str(a) for a in achados))
    rotulo = 'Dados ' + '/'.join(Path(rel).parts[-2:])
    ts, final = trocas_de_janelas(
        rel, base_txt, pre, juntar(janelas), pares,
        lambda k: ACHADO.format(i=nomes[k], cat='B', texto=TEXTO_CAT['B'] + ' Nos dados do gerador, que passam iguais para a página.'),
        local_b(rotulo))
    return base_txt, final, ts


def construir():
    por_pagina = {}
    for x in ACHADOS_AC:
        por_pagina.setdefault(x['ficheiro'], ([], []))[0].append(x)
    for x in ACHADOS_B:
        if x['ficheiro']:
            por_pagina.setdefault(x['ficheiro'], ([], []))[1].append(x)
    por_i = {x['i']: x for x in ACHADOS_B}
    finais, relatorio = {}, []
    for rel in sorted(por_pagina):
        ac, bs = por_pagina[rel]
        base_txt, final, trocas, rel_pag = trocas_pagina(rel, ac, bs)
        finais[rel] = (base_txt, final, trocas)
        relatorio += rel_pag
    for spec in DADOS:
        finais[spec['ficheiro']] = trocas_dados(spec, por_i)
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
