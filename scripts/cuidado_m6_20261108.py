#!/usr/bin/env python3
"""08/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M6 do Português.

Constrói scripts/cuidado_m6_20261108.json, a camada literal cuidado_m6_20261108, com os 43 achados CONFIRMADOS da varredura
de 6/11 (só leitura, com conferência independente) no M6: 11 achados A (tabelas onde há itens paralelos), 28 de referências e
números que se partiam (B) e 4 casos do mesmo tipo (C). Os 7 achados que a conferência recusou (9, 11, 12, 13, 14, 15 e 21: os
pesos da avaliação e os tempos da aula de tarefa continuam em frase, e «Três antes de mim» do guia fica como está) não entram.
A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/cuidado-m6-edits-20261108.json:

  python3 scripts/cuidado_m6_20261108.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m6_20261108.json --manifesto tests/fixtures/cuidado-m6-edits-20261108.json \\
      --base-commit 4bf4a0538cd5f883448d179973ef016023a58f86 --nota "…"

11/11/2026 (fusão do main 4bf4a053 no pedido #191): a camada foi refeita sobre o main com a revisão dos enunciados das tarefas
(tarefas_claras_20261110, pedido #192), e fica por cima dela. As trocas das tarefas da M6-U1 e da M6-U2 (dados e páginas) são as
mesmas, agora sobre os enunciados novos; o gerador das tarefas junta «clareza» (#192) e «nao_partir_grelha» (esta camada).

11/11/2026 (reposição, no mesmo pedido #191): ao reescrever os enunciados, o #192 deixou cair espaços que não quebram (U+00A0) que a
decisão 152 já tinha posto nas tarefas do M1, do M3, do M4 e do M5 (a verificação «tables» falhava em tests/browser_cuidado_m3.py,
também no main: em «(I, 1 a 3)», o espaço a seguir à vírgula tinha voltado a ser normal). Esta camada, que fica por cima da dos enunciados, repõe-os (REPOR, abaixo;
trocas «(R)», só de espaços, sem mudar mais nenhuma letra do texto do #192): onde a mesma referência continua no texto novo, o
espaço volta («(I, 1 a 3)», «(I, 4 e 5)», «(X, 145)», «(VIII, 96)», «VIII, 96 a 99», «VIII, 98», «3 a 4 minutos», «180 a 240
palavras», «2 minutos»); onde o #192 trocou «cap.» por «capítulo» (M1-U2, M5-U1 e M5-U2), a abreviatura já não existe e a
referência nova, do mesmo tipo, fica presa como no M4 e no M5 («capítulo XII», com U+00A0). Nas tarefas geradas (M1-U2, M3-U1, M3-U2, M5-U1
e M5-U2) a troca faz-se nos dados e na página, que sai igual do gerador; as do M4 não têm gerador. Para os contratos históricos
(os testes e os geradores das camadas do M1 ao M5, que leem estas páginas como eram antes do #192), scripts/
tarefas_claras_historico.py desfaz primeiro esta camada, quando o texto ainda a traz, e só depois a dos enunciados.

Segue o modelo da camada do M5 (scripts/cuidado_m5_20261108.py), com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como na M7-F10, na M7-F15 e do M1 ao M5: class apoio-tabela, th
  scope=col no cabeçalho, th scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader,
  rowheader, cell), porque no telemóvel a tabela passa a display:block. Dentro do JSON dos cartões e do objeto E das páginas «Ler
  a fundo», as aspas vão com barra (\\"). São seis cartões «Em paralelo» (F02, F04, F05, F06, F07 e F09; o da F11 fica, como a
  varredura propôs), as caixas «Recorda» e «Para entender» com termo e definição (F02, F04, F06 e F07) e os três testes de
  «Frases da rua» (gram-oracoes-rua), dentro de um div.nota, como a de gram-modalidade no M3 (a proposta pedia uma tabela
  «testes» com estilo próprio na página). Cada página com uma tabela nova carrega assets/pt-lessons/apoios-tabelas.css antes de
  assets/appearance.css, na versão do M1 (20261106.1: a folha não muda; a proposta citava 20261105.1). Nas duas caixas de termos
  da F02 e da F06, a primeira coluna fica com 30 % (a proposta pedia a classe «termos» e uma regra na folha comum; aqui, como as
  larguras do M3 e do M5, vai no cabeçalho da coluna, e a folha não muda).
- B: U+00A0 (espaço que não quebra) nos espaços que a proposta final prende, e U+2060 (junção de palavras) logo a seguir ao
  traço de intervalo e ao hífen da sigla «M6-Fxx». Cada par conta-se no contexto da proposta (com a palavra inteira), e a troca
  leva só os espaços que muda, com o mínimo de contexto que a distingue. Nas datas, a proposta do M6 prende todos os espaços
  («19 de julho de 1886»). Os intervalos de versos escritos «(v. 1 a 4)», «(v. 1 e 2)», «(v. 9 e 10)», «(v. 13 e 14)» e
  «(v. 16 e 17)» passam à forma da M7-F10, «(vv. 1–4)», como pede a proposta (trocas literais, com a razão). Ficam de fora: os
  «alt» (e aria-label, href, title, content e data-titulo, que vira o title do vídeo), o <title>, o texto dos desenhos (SVG), a
  «frase» dos cartões sublinhar, as «palavras» dos cartões frase e os «passos» dos cartões ordenar (o motor parte-os nos espaços),
  as notas internas dos dados e a casca das lições (abaixo). O que outra camada já pôs com U+00A0 (os créditos do «i» do mapa)
  fica como está.
- C: a lista das regras de produção da F08; no portefólio, os nomes dos ficheiros todos em <code> e sem partir, a tabela com
  cabeçalho (thead, th scope=col, os role) e as células com o rótulo da coluna, que no telemóvel empilham (estilo da página, como
  na proposta); e os elementos de cada tema em listas no critério 4 das grelhas da M6-U1 e da M6-U2 (pelo gerador, com
  «max_em_listas», como no M1 e no M5).
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois.

A casca das lições (migalhas «2.º ano», «Estás em: Lição M6-Fxx» e a sigla «Lição M6-Fxx» do rodapé) não muda aqui, ficheiro a
ficheiro: muda no molde, como do M1 ao M5 (o achado 29, só da casca da F09, fica sem troca). Nas outras páginas (índice, guia,
mapa e portefólio do módulo, «Pensar devagar» e «Ler a fundo»), a proposta final e a conferência deixam as migalhas de fora (o
«2.º ano» das migalhas é uma ligação sozinha numa linha e não se parte); muda o «2.º ano» do cabeçalho, onde o achado o pede.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e das listas, as correções que a proposta final faz (as
maiúsculas e minúsculas no início das células e dos itens, os rótulos das linhas que vêm do texto, os exemplos que a proposta tira
do mesmo cartão ou do poema da lição, e a forma «vv. N–N» dos intervalos) e os espaços invisíveis. O script calcula as trocas
sobre a base (a página com esta camada desfeita pelo manifesto, quando ele já existe): pode voltar a correr depois de a camada
estar aplicada e dá o mesmo JSON.

Páginas geradas: as tarefas da M6-U1 e da M6-U2 (scripts/tarefas_escolha.py) mudam nos dados (docs/pedagogia/tarefas-escolha/
m6-u1.json e m6-u2.json: «nao_partir», como do M1 ao M5, que prende os números do molde e a meta descrição; «nao_partir_grelha»,
nova, que prende «Grelha /20» na ligação à grelha; e os achados B); os aquecimentos (scripts/aquecimentos.py) mudam nos dados
(docs/pedagogia/aquecimentos/m6-u1.json e m6-u2.json); as grelhas (scripts/grelhas_tarefas.py) mudam nos dados (docs/pedagogia/
grelhas-tarefas-20261027.json, só nas entradas m6-u1 e m6-u2: «max_em_listas» no critério 4, «nao_partir_valores», nova, que
prende «20 valores» no cabeçalho, e os achados B); a correção sai igual. Os dados estão na mesma camada e as páginas regeneram-se
sem diferenças. A lição F14 é gerada (scripts/gerar_licoes_20261101.py): a data muda na fonte (scripts/licoes_m1_m6_20261101.py,
fora da camada, como no M5), e a lição muda aqui e sai igual do gerador. Os painéis de projeção do docente (m6/painel-m6-fxx)
seguem os enunciados dos cartões (a lista e o seletor, como scripts/sync_teacher_labels.py os escreve); o material do relâmpago
(MATERIAL) segue a lição antes das camadas de cuidado (tests/test_sala_desligada.py compara-o com ela), como do M1 ao M5. As
cópias dos cartões no banco das provas rápidas do índice (var U) mudam como as lições de onde vêm, e também a cópia do retorno de
um cartão da F01 nas sessões do Exame (assets/exame/sessoes.json), que tests/test_exame_alignment.py compara com a lição.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m6_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m6-edits-20261108.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
CONTAR = None
ACHADO = '08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M6, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como na M7-F10, na M7-F15 e do M1 ao M5).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e ao hífen da '
          'sigla).'),
    'C': 'Caso do mesmo tipo.',
}


def j(s):
    """As formas da proposta escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return s.replace('{N}', NBSP).replace('{J}', WJ)


# A folha das tabelas de apoio, antes da camada de aparência (como na M7-F10, na M7-F15 e do M1 ao M5), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
COM_TABELA = {
    'm6/licao-m6-f02/index.html': ('lição', [3, 6]), 'm6/licao-m6-f04/index.html': ('lição', [4, 5]),
    'm6/licao-m6-f05/index.html': ('lição', [16]), 'm6/licao-m6-f06/index.html': ('lição', [0, 7]),
    'm6/licao-m6-f07/index.html': ('lição', [1, 8]), 'm6/licao-m6-f09/index.html': ('lição', [2]),
    'm6/gram-oracoes-rua/index.html': ('página «Ler a fundo»', [10]),
}
# Nas caixas de termos (F02 e F06), a primeira coluna fica com 30 % (o nome do recurso ou do conceito é comprido).
TERMOS = ' style="width:30%"'


def tabela(colunas, linhas, json_=True, larguras=None):
    """A tabela de apoio, igual às do M1 ao M5: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label com
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


# Os seis cartões «Em paralelo» (o liga e o que vem a seguir ficam; o div.paralelo, com os desenhos, sai).
PARALELO_INICIO, PARALELO_FIM = '<div class=\\"paralelo\\">', '<p class=\\"liga\\">'


def paralelo(rel):
    return bloco(rel, PARALELO_INICIO, PARALELO_FIM)


# As regras de produção da F08 (C), uma por item.
REGRAS_ANTES = ('<p>Pedir autorização a quem aparece reconhecível; não fotografar pessoas em situação vulnerável sem consentimento '
                '(sem-abrigo, crianças); nada de fotografar às escondidas; sair em grupo e dentro do horário combinado; música e sons '
                'próprios ou livres de direitos.</p>')
REGRAS_DEPOIS = ('<ul><li>Pedir autorização a quem aparece reconhecível.</li><li>Não fotografar pessoas em situação vulnerável sem '
                 'consentimento (sem-abrigo, crianças).</li><li>Nada de fotografar às escondidas.</li><li>Sair em grupo e dentro do '
                 'horário combinado.</li><li>Música e sons próprios ou livres de direitos.</li></ul>')

# O portefólio (C): a tabela da lista de verificação com cabeçalho, os role e o rótulo da coluna em cada célula, e todos os nomes
# em <code>; «Grelha /20.» já com o espaço que não quebra (achado 35). O estilo da página empilha as células no telemóvel.
PORTEFOLIO = 'm6/portefolio-do-modulo-m6/index.html'
PORT_CAB_ANTES = '<table><tr><th style="width:36%">Nome do ficheiro</th><th>O que é</th></tr>'
PORT_COLUNAS = ('Nome do ficheiro', 'O que é')
PORT_CSS_ANTES = 'code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n'
PORT_CSS_DEPOIS = (PORT_CSS_ANTES + 'code{white-space:nowrap}\n@media(max-width:620px){table,tbody,tr,td{display:block;width:auto}'
                   'thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}tr{border-top:2px solid var(--tinta)}'
                   'td[data-label]::before{content:attr(data-label) ": ";font-weight:700}}\n')


def portefolio():
    antigo = bloco(PORTEFOLIO, PORT_CAB_ANTES, '</table>', inclui_fim=True)
    linhas = re.findall(r'<tr><td>(.*?)</td><td>(.*?)</td></tr>', antigo)
    assert len(linhas) == 15 and antigo == PORT_CAB_ANTES + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in linhas) + '</table>'
    cab = ''.join(f'<th scope="col" role="columnheader">{c}</th>' for c in PORT_COLUNAS)
    corpo = ''
    for nome_, oque in linhas:
        nome_ = nome_ if nome_.startswith('<code>') else f'<code>{nome_}</code>'
        oque = oque.replace('Grelha /20.', 'Grelha' + NBSP + '/20.')
        corpo += (f'<tr role="row"><td role="cell" data-label="{PORT_COLUNAS[0]}">{nome_}</td>'
                  f'<td role="cell" data-label="{PORT_COLUNAS[1]}">{oque}</td></tr>')
    novo = (f'<table role="table"><thead role="rowgroup"><tr role="row">{cab}</tr></thead><tbody role="rowgroup">{corpo}</tbody></table>')
    return antigo, novo


def _grelhas():
    import grelhas_tarefas  # noqa: E402
    return grelhas_tarefas


def descritor_c4(slug):
    dados = json.loads(base('docs/pedagogia/grelhas-tarefas-20261027.json'))
    return dados['tarefas'][slug]['criterios'][3]['niveis']['max'][0]


def achados_ac():
    """Os 15 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte)."""
    f02, f04, f05, f06, f07, f09 = (f'm6/licao-m6-{n}/index.html' for n in ('f02', 'f04', 'f05', 'f06', 'f07', 'f09'))
    rua = 'm6/gram-oracoes-rua/index.html'
    port_antigo, port_novo = portefolio()
    return [
        dict(i=3, cat='A', ficheiro=f02, cartao='cartão 18, Em paralelo («Da procura ao descanso»)',
             nota=('Os dois lados passam a duas colunas, com as linhas da proposta (O Ideal, O sujeito, Recursos); o div.paralelo, com os '
                   'desenhos, sai; o liga fica.'),
             antigo=paralelo(f02),
             novo=tabela(['Aspeto', '«Ideal»', '«Na mão de Deus»'], [
                 ['O Ideal', 'visão sem nome, miragem, «Nuvem, sonho impalpavel»', '«forma transitoria e imperfeita» que o sujeito depõe'],
                 ['O sujeito', 'inquieto: «A mim mesmo pergunto, e não atino»', 'em repouso: «Descançou a final meu coração»'],
                 ['Recursos', 'anáfora e enumeração negativa: não é Vénus, Circe, Amazona',
                  'comparação da criança ao colo e apóstrofe ao coração']])),
        dict(i=6, cat='A', ficheiro=f02, cartao='cartão 20, Para entender («Recorda»)',
             nota=('O exemplo da comparação é o verso 10 de «Na mão de Deus», que está no poema da lição (a primeira frase passa a dizê-lo); '
                   'a primeira coluna fica com 30 % (a proposta pedia a classe «termos» e uma regra na folha comum).'),
             antigo=bloco(f02, '<p>Os exemplos vêm de «O Palácio da Ventura». <b>Apóstrofe</b>', '</div>'),
             novo=('<p>Os exemplos vêm de «O Palácio da Ventura»; o da comparação, de «Na mão de Deus».</p>'
                   + tabela(['Recurso', 'O que é', 'Exemplo'], [
                       ['Apóstrofe', 'chamar alguém ou alguma coisa', "«Abri-vos, portas d'ouro»"],
                       ['Metáfora', 'dizer uma coisa por outra', '«Paladino do amor»'],
                       ['Personificação', 'dar gesto ou voz de pessoa a uma coisa ou a uma ideia',
                        'as portas, a que o cavaleiro fala como se fossem pessoas'],
                       ['Comparação', 'aproximar duas coisas com «como»', '«Como criança, em lobrega jornada»'],
                       ['Anáfora', 'repetir a mesma palavra no princípio de versos ou frases', '«Por desertos, por sóes, por noite escura»']],
                       larguras=[TERMOS, '', '']))),
        dict(i=4, cat='A', ficheiro=f04, cartao='cartão 2, Em paralelo («Coordenar ou subordinar»)',
             nota='Os dois lados passam a duas colunas (O que faz, Conectores, Exemplo); o div.paralelo sai; o liga fica.',
             antigo=paralelo(f04),
             novo=tabela(['Aspeto', 'Coordenação', 'Subordinação'], [
                 ['O que faz', 'liga orações sem dependência sintática entre si', 'uma oração depende de outra, a subordinante'],
                 ['Conectores', 'e, mas, ou, pois (confirma a relação na frase)', 'que, quando, se, porque, como (decide a construção)'],
                 ['Exemplo', '«Abrem-se as portas de ouro» e «Mas dentro encontro só»',
                  '«Sonho» e «que sou um cavaleiro andante», substantiva completiva']])),
        dict(i=5, cat='A', ficheiro=f04, cartao='cartão 4, Para entender («Três relações a observar»)',
             nota='Só a lista passa a tabela; o título do painel e o details (com «M6-F07», achado 24) ficam.',
             antigo=bloco(f04, '<ul><li><b>Completiva:</b>', '<details>'),
             novo=tabela(['Relação', 'Exemplo', 'O que observar'], [
                 ['Completiva', '«Sonho que sou um cavaleiro»', 'a oração completa o verbo; «Sonho isso» ajuda a verificar.'],
                 ['Relativa com antecedente', '«os filhos que depois naufragam»', '«que» retoma «filhos» e é sujeito de «naufragam».'],
                 ['Adverbial', '«tal… que»', 'pode apresentar uma consequência; confirma-se na frase, não na palavra «que» isolada.']])),
        dict(i=16, cat='A', ficheiro=f05, cartao='cartão 2, Em paralelo («Um étimo, dois caminhos»)',
             nota=('As duas vias ficam definidas num parágrafo antes da tabela, que dá os três étimos (em itálico, como estavam) com as duas '
                   'palavras; o div.paralelo sai; o liga fica.'),
             antigo=paralelo(f05),
             novo=('<p><b>Via popular</b>: evolução fonética lenta. <b>Via erudita</b>: tomada mais tarde, próxima do latim.</p>'
                   + tabela(['Étimo', 'Via popular', 'Via erudita'], [
                       ['<i>plenu-</i>', '«cheio»', '«pleno»'], ['<i>clave-</i>', '«chave»', '«clave»'],
                       ['<i>macula-</i>', '«mancha» ou «malha»', '«mácula»']]))),
        dict(i=0, cat='A', ficheiro=f06, cartao='cartão 20, Em paralelo («O que vê e o que evoca»)',
             nota='Os dois lados passam a duas colunas (Barcos, Gente, Tempo); o div.paralelo sai; o liga e o vídeo ficam.',
             antigo=paralelo(f06),
             novo=tabela(['Elemento', 'O que vê', 'O que evoca'], [
                 ['Barcos', 'os botes atracados e os escaleres de um couraçado', '«soberbas naus que eu não verei jámais!»'],
                 ['Gente', 'calafates «enfarruscados, seccos»', '«Mouros, baixeis, heroes», Camões a nado'],
                 ['Tempo', 'o fim da tarde que «inspira» e «incommoda»', 'o passado das «chronicas navaes»']])),
        dict(i=7, cat='A', ficheiro=f06, cartao='cartão 22, Para entender («Recorda»)',
             nota='A primeira coluna fica com 30 %, como na F02; o details fica.',
             antigo=bloco(f06, '<p><b>Deambulação</b>', '</div><details>'),
             novo=tabela(['Conceito', 'O que é'], [
                 ['Deambulação', 'andar pela cidade sem destino, a ver.'],
                 ['Perceção sensorial', 'o que chega pelos sentidos (ver, ouvir, cheirar, sentir na pele).'],
                 ['Transfiguração do real', 'o que se vê torna-se outra coisa pela imaginação.'],
                 ['Tipos sociais', 'figuras que valem por um grupo inteiro, como um ofício.'],
                 ['Imaginário épico', 'as imagens que a epopeia deixou (naus, heróis, mares).']], larguras=[TERMOS, ''])),
        dict(i=1, cat='A', ficheiro=f07, cartao='cartão 28, Em paralelo («Reportagem e sonho»)',
             nota='Os dois lados passam a duas colunas (Programa, Gente, Lugar); o div.paralelo sai; os dois liga ficam.',
             antigo=paralelo(f07),
             novo=tabela(['Elemento', 'A reportagem', 'O sonho'], [
                 ['Programa', '«o real e a analyse», um livro feito do observado', '«a chimera azul de transmigrar», mudar de vida'],
                 ['Gente', 'o forjador ao torno, o ratoneiro imberbe, o cauteleiro rouco',
                  '«castissimas esposas», filhos, «mansões de vidro transparente»'],
                 ['Lugar', '«Sem arvores, no valle escuro das muralhas»', '«todos os continentes» e «as vastidões aquaticas»']])),
        dict(i=8, cat='A', ficheiro=f07, cartao='cartão 30, Para entender («Recorda»)',
             nota=('O exemplo da antítese é o do «O essencial» da lição (cartão 1), já com o espaço que não quebra em «v. 28»; o details '
                   'fica.'),
             antigo=bloco(f07, '<p><b>Antítese</b>', '</div><details>'),
             novo=tabela(['Recurso', 'O que é', 'Exemplo'], [
                 ['Antítese', 'duas ideias opostas lado a lado', '«Inflamma-se um palacio em face de um casebre» (v.' + NBSP + '28)'],
                 ['Sinestesia', 'mistura de sentidos na mesma expressão', '«um silêncio frio»'],
                 ['Hipálage', 'dar a uma coisa a qualidade que pertence a uma pessoa', '«a cadeira cansada»']])),
        dict(i=2, cat='A', ficheiro=f09, cartao='cartão 2, Em paralelo («Fora do mundo, dentro da cidade»)',
             nota='Os dois lados passam a duas colunas (Temas, Forma, Real); o div.paralelo sai; o liga e o painel ficam.',
             antigo=paralelo(f09),
             novo=tabela(['Aspeto', 'Antero', 'Cesário'], [
                 ['Temas', 'angústia existencial, o Ideal, a morte, Deus', 'a cidade, os tipos sociais, o trabalho'],
                 ['Forma', 'o soneto, com chave de ouro', 'quadras de alexandrinos e decassílabos'],
                 ['Real', 'pensado: «O palacio encantado da Ventura»', 'observado e transfigurado: «a pão no forno»']])),
        dict(i=10, cat='A', ficheiro=rua, cartao='passo 0, «Três versos, três testes» (a nota dos três testes)',
             nota=('Como a de gram-modalidade no M3: a tabela fica dentro de um div.nota, com a classe apoio-tabela e os role (a proposta '
                   'pedia uma tabela «testes» com estilo próprio na página); a folha das tabelas empilha-a no telemóvel.'),
             antigo=bloco(rua, '<p class=\\"nota\\"><b>teste do «isso»</b>', '","links"'),
             novo='<div class=\\"nota\\">' + tabela(['Teste', 'Condição', 'A oração é'], [
                 ['teste do «isso»', 'se a oração se troca por «isso»', 'substantiva'],
                 ['teste do «o qual»', 'se «que» se troca por «o qual», «os quais»', 'relativa'],
                 ['teste da pergunta', 'se responde a «quando?», «porquê?» ou «com que resultado?»', 'adverbial']]) + '</div>'),
        dict(i=17, cat='C', ficheiro='m6/licao-m6-f08/index.html', cartao='cartão 2, Para entender («Regras de produção»)',
             nota='As cinco regras numa lista, cada uma com maiúscula e ponto final; «Cada curso tem a sua encomenda» fica.',
             antigo=REGRAS_ANTES, novo=REGRAS_DEPOIS),
        dict(i=18, cat='C', ficheiro=PORTEFOLIO, cartao='«A lista de verificação»: a tabela com cabeçalho, os nomes em <code>',
             nota=('Os seis nomes que não estavam em <code> passam a estar; o cabeçalho vai num thead (com th scope=col, sem a largura de '
                   '36 %) e o resto num tbody, com os role e, em cada célula, o rótulo da sua coluna (data-label), porque no telemóvel '
                   'as células empilham. «Grelha /20.» já leva o espaço que não quebra (achado 35). Sem U+2011 nem U+2060 dentro dos '
                   'nomes (o aluno copia-os).'),
             antigo=port_antigo, novo=port_novo),
        dict(i=18, cat='C', ficheiro=PORTEFOLIO, cartao='a folha da página: os nomes não se partem e a tabela empilha no telemóvel',
             nota='O estilo da proposta: code sem mudar de linha e, até 620 px, as células umas por baixo das outras, com o rótulo.',
             antigo=PORT_CSS_ANTES, novo=PORT_CSS_DEPOIS),
    ]


def ac_grelhas():
    """Os descritores do critério 4 (nível máximo) das grelhas da M6-U1 e da M6-U2 em listas, pelo gerador, como no M1 e no M5."""
    g = _grelhas()
    out = []
    for i, slug, rel in ((19, 'm6-u1', 'tarefas/m6-u1/grelha/index.html'), (20, 'm6-u2', 'tarefas/m6-u2/grelha/index.html')):
        desc = descritor_c4(slug)
        out.append(dict(i=i, cat='C', ficheiro=rel, cartao='critério 4, nível 6 («cumprimento consistente»): os elementos de cada tema em listas',
                        nota=('Pelo gerador das grelhas, com «max_em_listas» no critério 4 (nos dados desta camada), como no M1 e no M5: na '
                              'forma do gerador («<b>Tema A</b>:», cada elemento com o «;» ou o «.» que tinha; a proposta tinha «<b>Tema A</b>» '
                              'sem os dois pontos e os elementos sem pontuação), com <ul> e o fecho de cada tema num parágrafo; a versão de '
                              'correção fica com o texto corrido (está num <small> dentro de uma célula).'),
                        antigo=f'<p>{g.ital(desc)}</p>', novo=g.em_listas(desc)))
    return out


# Os 28 achados B confirmados. Cada par é o da proposta final (no contexto que a proposta dá), com as ocorrências que mudam;
# «fora» diz quantas ficam de fora e porquê (o «alt», o data-titulo dos vídeos, o que um achado A ou C já mudou, o que outra
# camada já tinha posto, a «frase», as «palavras» e os «passos» dos exercícios), «casca» o que fica para o molde, «mais» onde o
# número que muda não é o da proposta e porquê, e «literais» as trocas que não são só de espaços (com a razão e o número).
ALT = 'o «alt» não se vê; muda a legenda'
TITULO = 'o data-titulo do vídeo vira o title do leitor; muda o botão'
VV = 'o intervalo de versos passa à forma da M7-F10 («vv.», traço de intervalo e U+2060), como pede a proposta'


def casca(n):
    return {f'Estás em: Lição M6-{n}': 1, f'Português 2026/2027. Lição M6-{n},': 1, 'pt/2/">2.º ano</a>': 1}


ACHADOS_B = [
    dict(i=22, ficheiro='m6/licao-m6-f01/index.html', casca=casca('F01'),
         pares=[('(v. 1)', '(v.{N}1)', 3), ('v. 6 corrigido', 'v.{N}6 corrigido', 1), ('(v. 7)', '(v.{N}7)', 2), ('(v. 9)', '(v.{N}9)', 3),
                ('(v. 10)', '(v.{N}10)', 1), ('(v. 11)', '(v.{N}11)', 1), ('(v. 12)', '(v.{N}12)', 1), ('(v. 14)', '(v.{N}14)', 3),
                ('(c. 1887)', '(c.{N}1887)', 1), ('(1842 a 1891)', '(1842{N}a{N}1891)', 1), ('(1842–1891)', '(1842–{J}1891)', 1),
                ('4 + 4 + 3 + 3', '4{N}+{N}4{N}+{N}3{N}+{N}3', 2)],
         fora={'Quental (fotografia, c. 1887,': (1, ALT)}),
    dict(i=23, ficheiro='m6/licao-m6-f02/index.html', casca=casca('F02'),
         literais=[('(v. 1 a 4)', '(vv.{N}1–{J}4)', VV, 1), ('(v. 1 e 2)', '(vv.{N}1–{J}2)', VV, 1), ('(v. 9 e 10)', '(vv.{N}9–{J}10)', VV, 2)],
         pares=[('(v. 4)', '(v.{N}4)', 1), ('(v. 5)', '(v.{N}5)', 1), ('(v. 6)', '(v.{N}6)', 1), ('(v. 7)', '(v.{N}7)', 1),
                ('(v. 8)', '(v.{N}8)', 1), ('v. 14 corrigido', 'v.{N}14 corrigido', 1),
                ('de Antero, com imagens (2 min)', 'de Antero, com imagens (2{N}min)', 1)],
         fora={'de Antero, com imagens (2 min)': (1, TITULO)}),
    dict(i=24, ficheiro='m6/licao-m6-f04/index.html', casca=casca('F04'),
         pares=[('>M6-F07</a>', '>M6-{J}F07</a>', 1)]),
    dict(i=25, ficheiro='m6/licao-m6-f05/index.html', casca=casca('F05'),
         pares=[('século XIX', 'século{N}XIX', 4)],
         fora={'século XIX': (1, 'está na «frase» de um cartão sublinhar, que o motor parte nos espaços')}),
    dict(i=26, ficheiro='m6/licao-m6-f06/index.html', casca=casca('F06'),
         literais=[('(v. 16 e 17)', '(vv.{N}16–{J}17)', VV, 1)],
         pares=[('(v. 3)', '(v.{N}3)', 1), ('(v. 5)', '(v.{N}5)', 2), ('(v. 7)', '(v.{N}7)', 2), ('(v. 8)', '(v.{N}8)', 1),
                ('(v. 9)', '(v.{N}9)', 1), ('(v. 10)', '(v.{N}10)', 2), ('(v. 16)', '(v.{N}16)', 1), ('(v. 17)', '(v.{N}17)', 1),
                ('(v. 20)', '(v.{N}20)', 1), ('(v. 23)', '(v.{N}23)', 1), ('(v. 24)', '(v.{N}24)', 1), ('(v. 29)', '(v.{N}29)', 1),
                ('(v. 32)', '(v.{N}32)', 1), ('(v. 44)', '(v.{N}44)', 2),
                ('os versos 27 e 28', 'os versos 27{N}e{N}28', 1), ('no verso 28', 'no verso{N}28', 1), ('parte I', 'parte{N}I', 3),
                ('S. Petersburgo', 'S.{N}Petersburgo', 3), ('Tiago Barbosa (3 min)', 'Tiago Barbosa (3{N}min)', 1)],
         fora={'Tiago Barbosa (3 min)': (1, TITULO)}),
    dict(i=27, ficheiro='m6/licao-m6-f07/index.html', casca=casca('F07'),
         pares=[('(v. 1)', '(v.{N}1)', 1), ('(v. 7)', '(v.{N}7)', 1), ('(v. 10)', '(v.{N}10)', 1), ('(v. 15)', '(v.{N}15)', 1),
                ('(v. 23)', '(v.{N}23)', 2), ('(v. 28)', '(v.{N}28)', 1), ('(v. 29)', '(v.{N}29)', 1), ('(v. 51)', '(v.{N}51)', 1),
                ('verso 36', 'verso{N}36', 1), ('verso 66', 'verso{N}66', 1), ('verso 74', 'verso{N}74', 1),
                ('parte II', 'parte{N}II', 1), ('parte IV', 'parte{N}IV', 1)]),
    dict(i=28, ficheiro='m6/licao-m6-f08/index.html', casca=casca('F08'),
         pares=[('Bárcia, c. 1900)', 'Bárcia, c.{N}1900)', 1), ('(parte I)', '(parte{N}I)', 2),
                ('Villas Boas (4 min)', 'Villas Boas (4{N}min)', 1), ('100 a 130 palavras', '100{N}a{N}130{N}palavras', 2),
                ('30 a 60 segundos', '30{N}a{N}60{N}segundos', 1), ('peça 3 min', 'peça 3{N}min', 1),
                ('curta 2 a 3 min', 'curta 2{N}a{N}3{N}min', 1), ('45 minutos', '45{N}minutos', 2), ('grelha /20', 'grelha{N}/20', 1)],
         fora={'Bárcia, c. 1900)': (1, ALT), 'Villas Boas (4 min)': (1, TITULO)}),
    dict(i=29, ficheiro='m6/licao-m6-f09/index.html', casca=casca('F09'), pares=[]),
    dict(i=30, ficheiro='m6/licao-m6-f11/index.html', casca=casca('F11'),
         pares=[('31 anos', '31{N}anos', 9), ('200 exemplares', '200{N}exemplares', 5),
                ('a 25 de fevereiro.', 'a 25{N}de{N}fevereiro.', 1), ('Morre a 19 de julho,', 'Morre a 19{N}de{N}julho,', 1),
                ('19 de julho de 1886', '19{N}de{N}julho{N}de{N}1886', 2), ('19 de julho de **1886**', '19{N}de{N}julho{N}de{N}**1886**', 1),
                ('25 de fevereiro de 1855', '25{N}de{N}fevereiro{N}de{N}1855', 2),
                ('(Lisboa, 1855 a 1886)', '(Lisboa, 1855{N}a{N}1886)', 1),
                ('Ensina RTP (1 min)', 'Ensina RTP (1{N}min)', 1), ('(54 segundos)', '(54{N}segundos)', 1)],
         fora={'Ensina RTP (1 min)': (1, TITULO)}),
    dict(i=31, ficheiro='m6/licao-m6-f14/index.html',
         pares=[('conferência de 27 de maio de 1871', 'conferência de 27{N}de{N}maio{N}de{N}1871', 1)]),
    dict(i=32, ficheiro='m6/index.html',
         literais=[('(v. 1 a 4)', '(vv.{N}1–{J}4)', VV + ' (a cópia do cartão da F02 no banco das provas rápidas)', 1),
                   ('(v. 13 e 14)', '(vv.{N}13–{J}14)', VV + ' (a cópia de um cartão da F01 no banco das provas rápidas)', 1)],
         pares=[('aula de tarefa de 90 minutos', 'aula de tarefa de 90{N}minutos', 1),
                ('Unidade 1, 90 minutos', 'Unidade 1, 90{N}minutos', 1), ('Unidade 2, 90 minutos', 'Unidade 2, 90{N}minutos', 1),
                ('tarefa 90 min</small>', 'tarefa 90{N}min</small>', 2), ('cerca de 22 min', 'cerca de 22{N}min', 2),
                ('30 %', '30{N}%', 5), ('10 %', '10{N}%', 1), ('grelha /20', 'grelha{N}/20', 2), ('Grelha /20', 'Grelha{N}/20', 2),
                ('Português, 2.º ano, percurso do módulo', 'Português, 2.º{N}ano, percurso do módulo', 1),
                # O banco das provas rápidas (var U): as mesmas trocas que nas lições de onde vêm as cópias.
                ('(v. 1)', '(v.{N}1)', 4), ('(v. 5)', '(v.{N}5)', 1), ('(v. 7)', '(v.{N}7)', 4), ('(v. 8)', '(v.{N}8)', 1),
                ('(v. 9)', '(v.{N}9)', 1), ('(v. 10)', '(v.{N}10)', 3), ('(v. 14)', '(v.{N}14)', 4), ('verso 36', 'verso{N}36', 1),
                ('4 + 4 + 3 + 3', '4{N}+{N}4{N}+{N}3{N}+{N}3', 1), ('S. Petersburgo', 'S.{N}Petersburgo', 1),
                ('parte I', 'parte{N}I', 1), ('século XIX', 'século{N}XIX', 3), ('31 anos', '31{N}anos', 4),
                ('200 exemplares', '200{N}exemplares', 4), ('25 de fevereiro de 1855', '25{N}de{N}fevereiro{N}de{N}1855', 1),
                ('19 de julho de 1886', '19{N}de{N}julho{N}de{N}1886', 1), ('45 minutos', '45{N}minutos', 1),
                ('de 100 a 130 palavras', 'de 100{N}a{N}130{N}palavras', 1)]),
    dict(i=33, ficheiro='m6/guia-da-tarefa-m6/index.html',
         pares=[('aula de tarefa de 90 minutos', 'aula de tarefa de 90{N}minutos', 1), ('(10 minutos)', '(10{N}minutos)', 1),
                ('Seguem-se 5 minutos', 'Seguem-se 5{N}minutos', 1), ('30 %', '30{N}%', 5), ('10 %', '10{N}%', 1),
                ('grelha /20', 'grelha{N}/20', 7), ('<b>Aquecer, 10 min</b>', '<b>Aquecer, 10{N}min</b>', 1),
                ('<b>Ler o enunciado, 5 min</b>', '<b>Ler o enunciado, 5{N}min</b>', 1),
                ('<b>Produzir, 60 min</b>', '<b>Produzir, 60{N}min</b>', 1),
                ('<b>Rever e entregar, 15 min</b>', '<b>Rever e entregar, 15{N}min</b>', 1),
                ('Guia da tarefa, 2.º ano', 'Guia da tarefa, 2.º{N}ano', 1)]),
    dict(i=34, ficheiro='m6/mapa-do-modulo-m6/index.html',
         pares=[('versos 1 a 3', 'versos 1{N}a{N}3', 1), ('1842–1891', '1842–{J}1891', 1), ('1855–1886', '1855–{J}1886', 1),
                ('século XX', 'século{N}XX', 1), ('30 %', '30{N}%', 5), ('10 %', '10{N}%', 1), ('90 minutos', '90{N}minutos', 3),
                ('grelha /20', 'grelha{N}/20', 3), ('Grelha /20', 'Grelha{N}/20', 2),
                ('">Lição M6-F', '">Lição M6-{J}F', 7), ('">lição M6-F', '">lição M6-{J}F', 1),
                ('Português · 2.º ano · Mapa do módulo', 'Português · 2.º{N}ano · Mapa do módulo', 1)],
         fora={'Quental (fotografia, c. 1887,': (2, 'o «alt» e o aria-label do «i» não se veem; a legenda e o crédito já têm U+00A0, '
                                                    'de outra camada'),
               'Bárcia, c. 1900)': (1, 'o «alt» não se vê; o crédito do «i» já tem U+00A0, de outra camada (em <span class="nb">)')}),
    dict(i=35, ficheiro=PORTEFOLIO,
         pares=[('aula de tarefa de 90 minutos', 'aula de tarefa de 90{N}minutos', 1), ('(40 %)', '(40{N}%)', 1),
                ('grelha /20', 'grelha{N}/20', 1), ('Português · 2.º ano · Módulo 6', 'Português · 2.º{N}ano · Módulo 6', 1)],
         fora={'Grelha /20.': (2, 'o achado 18 (C) refaz a tabela, já com o espaço que não quebra')}),
    dict(i=36, ficheiro='m6/m6-cesario-noite-inteira/index.html',
         pares=[('n.º 8698', 'n.º{N}8698', 7), ('fecham a parte I.', 'fecham a parte{N}I.', 1), ('da parte III.', 'da parte{N}III.', 1),
                ('S. Petersburgo', 'S.{N}Petersburgo', 1), ('cerca de 22 min', 'cerca de 22{N}min', 1)]),
    dict(i=37, ficheiro='m6/m6-antero-viagem-ao-nada/index.html',
         pares=[('n.º 20142', 'n.º{N}20142', 6), ('prefácio, parte I.', 'prefácio, parte{N}I.', 1),
                ('cerca de 22 min', 'cerca de 22{N}min', 1)]),
    dict(i=38, ficheiro='m6/antero-palacio/index.html',
         pares=[('(1842–1891)', '(1842–{J}1891)', 1), ('(v. 7)', '(v.{N}7)', 1), ('(v. 14)', '(v.{N}14)', 1),
                ('até 15 palavras', 'até 15{N}palavras', 1), ('n.º 20142', 'n.º{N}20142', 2)]),
    dict(i=39, ficheiro='m6/antero-deus/index.html',
         pares=[('n.º 20142', 'n.º{N}20142', 3), ('até 25 palavras', 'até 25{N}palavras', 1),
                ('menos de 25 palavras', 'menos de 25{N}palavras', 1)]),
    dict(i=40, ficheiro='m6/cesario-avemarias/index.html',
         pares=[('n.º 8698', 'n.º{N}8698', 3), ('num verso de 16 palavras', 'num verso de 16{N}palavras', 1)]),
    dict(i=41, ficheiro='m6/cesario-noite/index.html',
         pares=[('n.º 8698', 'n.º{N}8698', 3), ('os momentos da parte IV.', 'os momentos da parte{N}IV.', 1)]),
    dict(i=42, ficheiro='m6/gram-oracoes-rua/index.html',
         pares=[('n.º 8698', 'n.º{N}8698', 3), ('n.º 20142', 'n.º{N}20142', 3)]),
    dict(i=43, ficheiro='m6/sam-chelas/index.html',
         pares=[('9 de abril de 2021', '9{N}de{N}abril{N}de{N}2021', 3), ('3 de julho de 2021', '3{N}de{N}julho{N}de{N}2021', 3)]),
    dict(i=44, ficheiro='tarefas/m6-u1/index.html',
         literais=[('durante 90 minutos, com entrega', 'durante 90{N}minutos, com entrega',
                    'a meta descrição muda com «nao_partir» (o gerador prende os três números do molde, como do M1 ao M5); a proposta '
                    'não a lista porque não se vê', 1)],
         pares=[('Antes de escrever · 10 min ·', 'Antes de escrever · 10{N}min ·', 1), ('Unidade 1 · 90 min', 'Unidade 1 · 90{N}min', 1),
                ('10 minutos de cartões', '10{N}minutos de cartões', 1), ('5 minutos para', '5{N}minutos para', 1),
                ('60 minutos de', '60{N}minutos de', 1), ('15 minutos de', '15{N}minutos de', 1), ('Total: 90 minutos', 'Total: 90{N}minutos', 1),
                ('200 a 240 palavras', '200{N}a{N}240{N}palavras', 2), ('90 a 130 no tema', '90{N}a{N}130 no tema', 1),
                ('Grelha /20: como', 'Grelha{N}/20: como', 1)]),
    dict(i=45, ficheiro='tarefas/m6-u2/index.html',
         literais=[('durante 90 minutos, com entrega', 'durante 90{N}minutos, com entrega',
                    'a meta descrição muda com «nao_partir» (o gerador prende os três números do molde, como do M1 ao M5); a proposta '
                    'não a lista porque não se vê', 1)],
         pares=[('Antes de escrever · 10 min ·', 'Antes de escrever · 10{N}min ·', 1), ('Unidade 2 · 90 min', 'Unidade 2 · 90{N}min', 1),
                ('10 minutos de cartões', '10{N}minutos de cartões', 1), ('5 minutos para', '5{N}minutos para', 1),
                ('60 minutos de', '60{N}minutos de', 1), ('15 minutos de', '15{N}minutos de', 1), ('Total: 90 minutos', 'Total: 90{N}minutos', 1),
                ('200 a 240 palavras', '200{N}a{N}240{N}palavras', 2), ('90 a 130 no tema', '90{N}a{N}130 no tema', 1),
                ('grafias do século XIX', 'grafias do século{N}XIX', 1), ('Na parte II,', 'Na parte{N}II,', 2),
                ('200 exemplares', '200{N}exemplares', 1), ('aos 31 anos', 'aos 31{N}anos', 1), ('Grelha /20: como', 'Grelha{N}/20: como', 1)],
         mais={'90 a 130 no tema': (0, 'a proposta da M6-U2 remete para o modelo comum do achado 44; a frase é a mesma da M6-U1 e muda '
                                       'igual')}),
    dict(i=46, ficheiro='tarefas/m6-u1/aquecimento/index.html',
         pares=[('À mão, 200 a 240 palavras.', 'À mão, 200{N}a{N}240{N}palavras.', 1),
                ('4 + 4 + 3 + 3 (lição F01)', '4{N}+{N}4{N}+{N}3{N}+{N}3 (lição F01)', 1)],
         fora={'contas as palavras: 200 a 240': (1, 'está nos «passos» de um cartão ordenar, que não levam U+00A0')}),
    dict(i=47, ficheiro='tarefas/m6-u2/aquecimento/index.html',
         pares=[('À mão, 200 a 240 palavras.', 'À mão, 200{N}a{N}240{N}palavras.', 1)],
         fora={'contas as palavras: 200 a 240': (1, 'está nos «passos» de um cartão ordenar, que não levam U+00A0')}),
    dict(i=48, ficheiro='tarefas/m6-u1/grelha/index.html',
         pares=[('20 valores em cinco critérios', '20{N}valores em cinco critérios', 1),
                ('entre 200 e 240 palavras', 'entre 200{N}e{N}240{N}palavras', 1),
                ('das 200 a 240 palavras', 'das 200{N}a{N}240{N}palavras', 1), ('(c. 1577)', '(c.{N}1577)', 1)]),
    dict(i=49, ficheiro='tarefas/m6-u2/grelha/index.html',
         pares=[('20 valores em cinco critérios', '20{N}valores em cinco critérios', 1),
                ('entre 200 e 240 palavras', 'entre 200{N}e{N}240{N}palavras', 1),
                ('das 200 a 240 palavras', 'das 200{N}a{N}240{N}palavras', 1)]),
]

# Sem notas do docente geradas a mudar (a da F14 não tem a data). As cópias de um cartão fora do módulo seguem a lição: o retorno
# do cartão 5 da F01 está copiado (na pergunta e na verificação «Depois da revisão») nas sessões do Exame, que
# tests/test_exame_alignment.py compara com a lição, letra a letra.
NOTAS = [
    dict(i=22, ficheiro='assets/exame/sessoes.json',
         nota_copia=('Na cópia do retorno do cartão da F01 nas sessões do Exame (assets/exame/sessoes.json, sessão s10), que '
                     'tests/test_exame_alignment.py compara com a lição.'),
         pares=[('andante» (v. 1): o sujeito', 'andante» (v.{N}1): o sujeito', 2)]),
]

# 11/11/2026: os espaços que o #192 (tarefas_claras_20261110) tirou às tarefas do M1, do M3, do M4 e do M5, e que esta camada repõe
# por cima dele. Cada trecho é o texto do #192, letra a letra, com o mínimo de contexto que o distingue; só mudam espaços. «tipo»
# diz se a referência é a mesma de antes (reposta) ou se o #192 a reescreveu por extenso (nova, do mesmo tipo: «cap. XII» passou
# a «capítulo XII», e prende-se como no M4 e no M5). Nas tarefas geradas, o mesmo trecho muda nos dados e na página.
REPOSICAO = ('11/11/2026: decisão 152 (cuidado em todas as lições), reposição depois do pedido #192 (R). O #192 '
             '(tarefas_claras_20261110) reescreveu o enunciado e deixou cair o espaço que não quebra (U+00A0) que a decisão 152 no '
             '{mod} tinha posto. {texto}')
REPOR_TEXTO = {
    'reposta': 'A mesma referência continua no texto novo e volta a não se partir; só mudam espaços.',
    'nova': ('A abreviatura «cap.» passou a «capítulo» por extenso: a referência já não existe como estava, e a nova, do mesmo tipo, '
             'fica presa (como «capítulo» com o numeral no M4 e no M5); só mudam espaços.'),
}
REPOR = [
    dict(slug='m1-u2', mod='M1', gerada=True, pares=[('capítulo XII', 'capítulo{N}XII', 2, 'nova')]),
    dict(slug='m3-u1', mod='M3', gerada=True, pares=[('(I, 1{N}a{N}3)', '(I,{N}1{N}a{N}3)', 1, 'reposta')]),
    dict(slug='m3-u2', mod='M3', gerada=True,
         pares=[('(I, 4{N}e{N}5)', '(I,{N}4{N}e{N}5)', 1, 'reposta'), ('(X, 145)', '(X,{N}145)', 2, 'reposta'),
                ('curioso» (VIII, 96)', 'curioso» (VIII,{N}96)', 1, 'reposta'), ('VIII, 96{N}a{N}99', 'VIII,{N}96{N}a{N}99', 1, 'reposta'),
                ('VIII, 98 ou 99', 'VIII,{N}98 ou 99', 1, 'reposta')]),
    dict(slug='m4-u1', mod='M4', gerada=False, pares=[('<strong>3 a 4 minutos</strong>', '<strong>3{N}a{N}4{N}minutos</strong>', 1, 'reposta')]),
    dict(slug='m4-u2', mod='M4', gerada=False,
         pares=[('<strong>180 a 240 palavras</strong>', '<strong>180{N}a{N}240{N}palavras</strong>', 1, 'reposta')]),
    dict(slug='m4-u3-discurso', mod='M4', gerada=False, pares=[('<strong>2 minutos</strong>', '<strong>2{N}minutos</strong>', 1, 'reposta')]),
    dict(slug='m5-u1', mod='M5', gerada=True, pares=[('do capítulo IV em que', 'do capítulo{N}IV em que', 1, 'nova')]),
    dict(slug='m5-u2', mod='M5', gerada=True,
         pares=[('do capítulo I e outra nova', 'do capítulo{N}I e outra nova', 1, 'nova'), ('No capítulo VI,', 'No capítulo{N}VI,', 1, 'nova')]),
]


def trocas_repor():
    """As trocas «(R)»: em cada tarefa, o mesmo trecho nos dados (se a página é gerada) e na página. Devolve {ficheiro: (base,
    final, trocas)}."""
    out = {}
    for x in REPOR:
        ficheiros = ([f'docs/pedagogia/tarefas-escolha/{x["slug"]}.json'] if x['gerada'] else []) + [f'tarefas/{x["slug"]}/index.html']
        for rel in ficheiros:
            base_txt = base(rel)
            final, trocas = base_txt, []
            onde = ('Dados da tarefa ' if rel.startswith('docs/') else 'Tarefa ') + x['slug'].upper()
            for antigo, novo, n, tipo in x['pares']:
                antigo, novo = j(antigo), j(novo)
                if novo.replace(NBSP, ' ') != antigo.replace(NBSP, ' ') or novo.count(NBSP) <= antigo.count(NBSP):
                    raise SystemExit(f'{rel}: a reposição «{antigo}» muda mais do que espaços')
                if base_txt.count(antigo) != n or base_txt.count(novo) != 0:
                    raise SystemExit(f'{rel}: «{antigo}» não aparece {n} vez(es) no texto do #192')
                final = final.replace(antigo, novo)
                trocas.append({'ficheiro': rel, 'local': f'{onde}: «{novo.replace(NBSP, " ")}» que não se parte',
                               'antigo': antigo, 'novo': novo, 'ocorrencias': n,
                               'achado': REPOSICAO.format(mod=x['mod'], texto=REPOR_TEXTO[tipo])})
            out[rel] = (base_txt, final, trocas)
    return out


# A casca das lições fica para o molde, como do M1 ao M5: nenhuma troca. As lições onde a varredura a viu.
CASCA_NO_MOLDE = sorted(x['ficheiro'] for x in ACHADOS_B if x.get('casca'))

# Dados dos geradores. As trocas C («max_em_listas») e as chaves dos números do molde vão à frente; os pares B depois, com as
# mesmas sequências das páginas (sem o que vem do molde dos geradores).
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DURACOES = [('10 minutos de cartões', '10{N}minutos de cartões', 1), ('5 minutos para', '5{N}minutos para', 1),
            ('60 minutos de', '60{N}minutos de', 1), ('15 minutos de', '15{N}minutos de', 1), ('Total: 90 minutos', 'Total: 90{N}minutos', 1),
            ('200 a 240 palavras', '200{N}a{N}240{N}palavras', 2), ('90 a 130 no tema', '90{N}a{N}130 no tema', 1)]
CHAVES_TAREFA = (' "nao_partir": true,\n "nao_partir_grelha": true,\n',
                 'Os números do molde da tarefa («90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) levam o espaço que não '
                 'quebra pelo gerador (scripts/tarefas_escolha.py), como do M1 ao M5, e «Grelha /20» na ligação à grelha também '
                 '(«nao_partir_grelha», nova).')
CHAVES_GRELHA = ('   "nao_partir_valores": true,\n',
                 '«20 valores em cinco critérios», no cabeçalho da grelha, leva o espaço que não quebra pelo gerador '
                 '(scripts/grelhas_tarefas.py, «nao_partir_valores», nova).')
DADOS = [
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m6-u1.json', achados=(44,), chaves=('\n "unidade": 1,\n',) + CHAVES_TAREFA,
         pares=DURACOES),
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m6-u2.json', achados=(45,), chaves=('\n "unidade": 2,\n',) + CHAVES_TAREFA,
         pares=DURACOES + [('grafias do século XIX', 'grafias do século{N}XIX', 1), ('Na parte II,', 'Na parte{N}II,', 2),
                           ('200 exemplares', '200{N}exemplares', 1), ('aos 31 anos', 'aos 31{N}anos', 1)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m6-u1.json', achados=(46,),
         pares=[('À mão, 200 a 240 palavras.', 'À mão, 200{N}a{N}240{N}palavras.', 1),
                ('4 + 4 + 3 + 3 (lição F01)', '4{N}+{N}4{N}+{N}3{N}+{N}3 (lição F01)', 1)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m6-u2.json', achados=(47,),
         pares=[('À mão, 200 a 240 palavras.', 'À mão, 200{N}a{N}240{N}palavras.', 1)]),
    dict(ficheiro=GRELHAS, entrada='m6-u1', achados=(48,), max_em_listas=19, chaves=('   "unidade": 1,\n',) + CHAVES_GRELHA,
         pares=[('entre 200 e 240 palavras', 'entre 200{N}e{N}240{N}palavras', 1),
                ('das 200 a 240 palavras', 'das 200{N}a{N}240{N}palavras', 1), ('(c. 1577)', '(c.{N}1577)', 1)]),
    dict(ficheiro=GRELHAS, entrada='m6-u2', achados=(49,), max_em_listas=20, chaves=('   "unidade": 2,\n',) + CHAVES_GRELHA,
         pares=[('entre 200 e 240 palavras', 'entre 200{N}e{N}240{N}palavras', 1),
                ('das 200 a 240 palavras', 'das 200{N}a{N}240{N}palavras', 1)]),
]


def ler(rel):
    # 12/11/2026: por cima de todas fica a camada das tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112), que muda os
    # enunciados, as grelhas e os dados da M3-U1 e da M3-U2: desfaz-se primeiro, com contagem estrita, quando o ficheiro a traz.
    from tarefas_claras_historico import desfazer_faceis
    return desfazer_faceis(rel, (ROOT / rel).read_bytes().decode('utf-8'))


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
A_MEIO = {'">Lição M6-F', '">lição M6-F'}


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


def janelas_pares(rel, pre, pares, regioes, limite=None):
    """As janelas dos pares (antigo, novo, n) em pre (a base com as trocas A, C e literais já feitas): [início, fim, {edições},
    índice do par]. Cada par conta-se no contexto da proposta, com a palavra inteira; as ocorrências fora de alcance não contam.
    Cada par tem de aparecer exatamente n vezes. Devolve também as que ficaram de fora, com a razão."""
    janelas, fora, vistas = [], [], set()
    for k, (antigo, novo, esperado) in enumerate(pares):
        eds_rel = edicoes(antigo, j(novo))
        achadas = []
        for m in re.finditer(re.escape(antigo), pre):
            s, e = m.start(), m.end()
            if limite and not (limite[0] <= s and e <= limite[1]):
                continue
            if not _palavra_inteira(pre, s, e, antigo):
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
    """O nome curto da página no manifesto. Os painéis de projeção (m6/painel-m6-fxx com CARTOES) não são notas do docente: só as
    notas editoriais (as das lições geradas, sem CARTOES) levam «(notas do docente)» (a revisão do M5 viu esse erro)."""
    m = re.match(r'm6/(?:licao|painel)-(m6-f\d+)/', rel)
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
    """O que o achado põe na conta, par a par (para o relatório): o que muda, o que fica de fora e a casca (onde isto não dá o
    número da proposta, «mais» diz o número da proposta e porquê)."""
    out = {}
    for seq, n in ([(p[0], p[2]) for p in x['pares']] + [(s, n) for s, (n, _) in x.get('fora', {}).items()]
                   + list(x.get('casca', {}).items()) + [(a, n) for a, _, _, n in x.get('literais', [])]):
        out[seq] = out.get(seq, 0) + n
    return out


def b_da_pagina(rel, base_txt, pre, regioes, x, rotulo=None):
    """As trocas de um achado B numa página: primeiro as literais (com a razão), depois os pares."""
    trocas = []
    for antigo, novo, razao, n in x.get('literais', []):
        pre, regioes = substituir(pre, regioes, antigo, j(novo), n)
        trocas.append({'ficheiro': rel, 'local': f'{rotulo or nome(rel)}: «{antigo}»', 'antigo': antigo, 'novo': j(novo),
                       'ocorrencias': n, 'achado': ACHADO.format(i=x['i'], cat='B', texto=TEXTO_CAT['B'] + ' ' + razao[0].upper()
                                                                  + razao[1:] + '.')})
    pares = x['pares']
    janelas, _ = janelas_pares(rel, pre, pares, regioes)
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
        ts, pre, regioes = b_da_pagina(rel, base_txt, pre, regioes, x)
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
        js, _ = janelas_pares(rel, pre, spec['pares'], regioes, limite)
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


# Os enunciados dos painéis do docente (m6/painel-m6-fxx) são os dos cartões da lição: o «p» (ou a «frase»), com ou sem os
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
    for licao in sorted(r for r in finais if r.startswith('m6/licao-')):
        painel = licao.replace('/licao-', '/painel-')
        if not (ROOT / painel).is_file() or any(x['ficheiro'] == painel for x in NOTAS):
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
    # 11/11/2026: as reposições depois do #192, em ficheiros que a varredura do M6 não toca.
    repor = trocas_repor()
    if set(repor) & set(finais):
        raise SystemExit(f'reposições em ficheiros da varredura: {sorted(set(repor) & set(finais))}')
    finais.update(repor)
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
