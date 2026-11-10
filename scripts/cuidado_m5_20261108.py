#!/usr/bin/env python3
"""08/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M5 do Português.

Constrói scripts/cuidado_m5_20261108.json, a camada literal cuidado_m5_20261108, com os 52 achados CONFIRMADOS da varredura
de 6/11 (só leitura, com conferência independente) no M5: 7 achados A (tabelas onde há itens paralelos), 35 de referências e
números que se partiam (B) e 10 casos do mesmo tipo (C). Os 11 achados que a conferência recusou (2, 3, 4, 5, 7, 8, 10, 11, 16,
17 e 19) não entram. A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em
tests/fixtures/cuidado-m5-edits-20261108.json:

  python3 scripts/cuidado_m5_20261108.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m5_20261108.json --manifesto tests/fixtures/cuidado-m5-edits-20261108.json --nota "…"

Segue o modelo das camadas do M1 ao M4 (scripts/cuidado_m1_20261106.py e cuidado_m2/m3/m4_20261108.py), com as mesmas regras:
- A: os itens paralelos que pedem tabela passam a tabela, como na M7-F10, na M7-F15 e do M1 ao M4: class apoio-tabela, th
  scope=col no cabeçalho, th scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader,
  rowheader, cell), porque no telemóvel a tabela passa a display:block. Dentro do JSON dos cartões, as aspas vão com barra (\\").
  Cada página com uma tabela nova carrega assets/pt-lessons/apoios-tabelas.css antes de assets/appearance.css, na versão do M1
  (20261106.1: a folha não muda; as regras de fora das lições já lá estão desde o M1). Nas tabelas dos pesos (índice, guia e
  mapa), como no M3: a coluna do peso só leva um número e fica estreita (5,5 rem; a primeira fica com o resto), e o rótulo
  («Pesos na avaliação:», «Avaliação:») fica num parágrafo antes da tabela, e não numa <caption> (fora das lições a folha comum
  não dá estilo à legenda e, no telemóvel, ela ficava espremida); a proposta pedia também a classe avaliacao-pesos com estilo
  próprio nos nove guias: usa-se só a classe apoio-tabela, como no M3. Os tempos da aula de tarefa (M5-U1 e M5-U2) passam à
  tabela pelo gerador das tarefas, como no M1 («tabela» e «depois» no aquecimento), com o total numa linha do corpo da tabela
  (a folha comum só empilha o corpo; a proposta punha-o num <tfoot>).
- B: U+00A0 (espaço que não quebra) nos espaços que a proposta final prende, e U+2060 (junção de palavras) logo a seguir ao
  traço de intervalo e ao hífen da sigla «M5-Fxx». A proposta do M5 dá cada troca com o seu contexto («A 17 de março, Simão
  parte»): cada par conta-se no contexto da proposta (com a palavra inteira), e a troca leva só os espaços que muda, com o
  mínimo de contexto que a distingue. Nas datas, o espaço entre o mês e o «de» do ano fica; nas listas, à volta das vírgulas
  e antes do «e». Ficam de fora: os «alt» (e aria-label, href, title, content e data-titulo, que vira o title do vídeo), o
  <title>, o texto dos desenhos (SVG), a «frase» dos cartões sublinhar e a casca das lições (abaixo). O que outra camada já pôs
  com U+00A0 (os créditos do «i», em <span class="nb">) fica como está. «Séc. XIX» do guia passa a «século XIX», como na
  proposta (é a única forma abreviada do M5).
- C: as listas (F08, «Três antes de mim» do guia e os temas A da M5-U1 e B da M5-U2), os nomes do vocabulário a negrito (F11,
  F12 e F13), os nomes do portefólio em <code> e sem partir, e os descritores do critério 3 das grelhas em listas (pelo
  gerador, com «max_em_listas», como no M1).
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois.

A casca das lições (migalhas «2.º ano» e «Narrativa do século XIX», «Estás em: Lição M5-Fxx» e a sigla «Lição M5-Fxx» do
rodapé) não muda aqui, ficheiro a ficheiro: muda no molde, como do M1 ao M4. As fontes do rodapé (c-menu-extra) mudam, como no
M1. Nas outras páginas (índice do módulo, guia, mapa e portefólio), as migalhas mudam porque o achado da página as inclui.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e das listas, as correções que a proposta final faz
(os nomes a negrito ligados com «e», «Séc.» > «século», as maiúsculas no início das linhas das tabelas e das listas) e os
espaços invisíveis. O script calcula as trocas sobre a base (a página com esta camada desfeita pelo manifesto, quando ele já
existe): pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.

Páginas geradas: as tarefas da M5-U1 e da M5-U2 (scripts/tarefas_escolha.py) mudam nos dados (docs/pedagogia/tarefas-escolha/
m5-u1.json e m5-u2.json: «nao_partir», como no M1 e no M3, a tabela dos tempos, a lista do tema e os achados B); os aquecimentos
(scripts/aquecimentos.py) mudam nos dados (docs/pedagogia/aquecimentos/m5-u1.json e m5-u2.json); as grelhas e a correção
(scripts/grelhas_tarefas.py) mudam nos dados (docs/pedagogia/grelhas-tarefas-20261027.json, só nas entradas m5-u1 e m5-u2:
«max_em_listas» no critério 3 e os achados B). Os dados estão na mesma camada e as páginas regeneram-se sem diferenças. As
lições F16 e F17 são geradas (scripts/gerar_licoes_20261101.py): os textos mudam nas fontes (scripts/licoes_m1_m6_20261101.py,
revisao_confirmacao_m16_20261101.py e imagens_licoes_20261101.py, fora da camada, como no M2), e a lição e as notas do docente
(m5/painel-m5-f16 e f17) mudam aqui e saem iguais do gerador. Os painéis do docente das outras lições (m5/painel-m5-fxx) seguem
os enunciados dos cartões.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
from tarefas_claras_historico import desfazer as desfazer_enunciados
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m5_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m5-edits-20261108.json'
NBSP, WJ, TRACO = '\xa0', '⁠', '–'
CONTAR = None
ACHADO = '08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M5, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como na M7-F10, na M7-F15 e do M1 ao M4).',
    'B': ('Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo e ao hífen da '
          'sigla).'),
    'C': 'Caso do mesmo tipo.',
}


def j(s):
    """As formas da proposta escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return s.replace('{N}', NBSP).replace('{J}', WJ)


# A folha das tabelas de apoio, antes da camada de aparência (como na M7-F10, na M7-F15 e do M1 ao M4), na versão do M1.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
COM_TABELA = {
    'm5/licao-m5-f11/index.html': ('lição', [6]), 'm5/licao-m5-f13/index.html': ('lição', [9]),
    'm5/index.html': ('índice do módulo', [1]), 'm5/guia-da-tarefa-m5/index.html': ('guia da tarefa', [0]),
    'm5/mapa-do-modulo-m5/index.html': ('mapa do módulo', [12]),
    'tarefas/m5-u1/index.html': ('tarefa da unidade (gerada, como no M1)', [13]),
    'tarefas/m5-u2/index.html': ('tarefa da unidade (gerada, como no M1)', [14]),
}
# A coluna que só leva um número (o peso) fica estreita; a primeira fica com o resto (a regra da folha dava-lhe 60 %), como no M3.
ESTREITA = ' style="width:5.5rem"'
LARGA = ' style="width:auto"'


def tabela(colunas, linhas, json_=True, caption=None, larguras=None):
    """A tabela de apoio, igual às do M1 ao M4: cabeçalho com th scope=col, primeira coluna com th scope=row, td data-label com
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
    html_ = (f'<table class="apoio-tabela" role="table">{legenda}<thead role="rowgroup"><tr role="row">{cab}</tr></thead>'
             f'<tbody role="rowgroup">{corpo}</tbody></table>')
    return html_.replace('"', '\\"') if json_ else html_


# Os pesos da avaliação (índice, guia e mapa), com o cabeçalho da proposta («Elemento», «Peso»); o parágrafo fica, sem a
# enumeração, a seguir à tabela.
PESOS = [['Tarefa da Unidade 1', '30' + NBSP + '%'], ['Tarefa da Unidade 2', '30' + NBSP + '%'], ['Provas rápidas', '10' + NBSP + '%'],
         ['Prova escrita', '30' + NBSP + '%']]
PESOS_ANTES = ' tarefa da Unidade 1, 30 %; tarefa da Unidade 2, 30 %; provas rápidas, 10 %; prova escrita, 30 %. '


def pesos(rotulo):
    # Como no M3: o rótulo fica num parágrafo antes da tabela; o parágrafo a seguir não leva a classe avaliacao-tarefas, que
    # continua a ser de um só parágrafo (tests/browser_revisao_tarefas_20261101.py).
    antigo = f'<p class="avaliacao-tarefas">{rotulo}:{PESOS_ANTES}'
    novo = (f'<p>{rotulo}:</p>' + tabela(['Elemento', 'Peso'], PESOS, json_=False, larguras=[LARGA, ESTREITA])
            + '<p class="avaliacao-tarefas">')
    return antigo, novo


# Os tempos da aula de tarefa (M5-U1 e M5-U2), pelo gerador das tarefas (como no M1). O texto atual diz «5 minutos para leres o
# enunciado» e «depois da leitura» (a proposta citava o texto antigo, «para o docente apresentar o enunciado»).
TEMPOS = {'colunas': ['Momento', 'Tempo'],
          'linhas': [['Cartões com consulta', '10' + NBSP + 'minutos'], ['Lês o enunciado', '5' + NBSP + 'minutos'],
                     ['Produção', '60' + NBSP + 'minutos'], ['Revisão e entrega', '15' + NBSP + 'minutos'],
                     ['Total', '90' + NBSP + 'minutos']]}
TEMPOS_TEXTO = ('No início da aula de tarefa: 10 minutos de cartões com consulta, 5 minutos para leres o enunciado, 60 minutos de '
                'produção e 15 minutos de revisão e entrega. Total: 90 minutos. O relógio de produção começa depois da leitura.')
TEMPOS_ANTES, TEMPOS_DEPOIS = 'No início da aula de tarefa:', 'O relógio de produção começa depois da leitura.'
TEMPOS_PAGINA = ('<p>' + TEMPOS_ANTES + '</p>' + tabela(TEMPOS['colunas'], TEMPOS['linhas'], json_=False)
                 + '<p>' + TEMPOS_DEPOIS + '</p>')


def tempos_json():
    """O aquecimento nos dados, como o da M1-U1: «texto», «tabela» e «depois» (indentação de json.dumps com indent=1)."""
    corpo = json.dumps({'texto': TEMPOS_ANTES, 'tabela': TEMPOS, 'depois': TEMPOS_DEPOIS}, ensure_ascii=False, indent=1)
    linhas = corpo.split('\n')[1:-1]
    return '\n'.join(' ' + l for l in linhas) + ',\n'


# As listas dos temas (C): o tema A da M5-U1 e o tema B da M5-U2, nos dados e na página.
TEMA_A_ANTES = ('Escreve a carta (90 a 120 palavras): local e data, vocativo, despedida e assinatura; resposta a uma pergunta dela; '
                'uma memória dos dois; um recurso expressivo teu; um eco do romance, entre «». Depois,')
TEMA_A_DEPOIS = ('Escreve a carta (90 a 120 palavras):</p><ol><li>local e data, vocativo, despedida e assinatura;</li><li>resposta a '
                 'uma pergunta dela;</li><li>uma memória dos dois;</li><li>um recurso expressivo teu;</li><li>um eco do romance, entre '
                 '«».</li></ol><p>Depois,')
TEMA_B_ITENS = ('Num parágrafo de opinião (100 a 130 palavras):</p><ol><li>tese na primeira frase;</li><li>outra citação do último '
                'capítulo, explicada;</li><li>um facto datado do dossiê, ligado à tese;</li><li>contra-argumento e refutação;</li>'
                '<li>conclusão.</li></ol>')
TEMA_B_ANTES = ('Num parágrafo de opinião (100 a 130 palavras): tese na primeira frase; outra citação do último capítulo, explicada; '
                'um facto datado do dossiê, ligado à tese; contra-argumento e refutação; conclusão.')

# Os nomes do portefólio que não estavam em <code> (o registo, a pergunta e o «o que aprendi» das duas unidades) e os longos, com
# um ponto onde podem mudar de linha (<wbr>, depois de cada «_»), como na proposta.
NOMES_SEM_CODE = [(f'M5_U{u}_{n}', f'M5_<wbr>U{u}_<wbr>{n}'.replace('registo_&lt;', 'registo_<wbr>&lt;'))
                  for u in (1, 2) for n in ('registo_&lt;dia-mês&gt;', 'pergunta', 'o-que-aprendi')]
NOMES_COM_CODE = [('M5_cartao-do-percurso', 'M5_<wbr>cartao-do-percurso'), ('M5_Prova-escrita', 'M5_<wbr>Prova-escrita')]


def _grelhas():
    import grelhas_tarefas  # noqa: E402
    return grelhas_tarefas


def descritor_c3(slug):
    dados = json.loads(base('docs/pedagogia/grelhas-tarefas-20261027.json'))
    return dados['tarefas'][slug]['criterios'][2]['niveis']['max'][0]


# Os 17 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte).
ACHADOS_AC = [
    dict(i=0, cat='A', ficheiro='m5/guia-da-tarefa-m5/index.html', cartao='secção «Tarefas das unidades» (p.avaliacao-tarefas)',
         nota=('Como no M3: o rótulo «Avaliação:» num parágrafo antes da tabela (sem <caption>), a coluna do peso estreita e só a classe '
               'apoio-tabela (a proposta pedia também avaliacao-pesos, com estilo próprio nos nove guias); o resto do parágrafo fica no '
               'mesmo p.avaliacao-tarefas. Só no M5 (este pedido é do M5).'),
         antigo=pesos('Avaliação')[0], novo=pesos('Avaliação')[1]),
    dict(i=1, cat='A', ficheiro='m5/index.html', cartao='secção «Como se cumpre uma unidade» (p.avaliacao-tarefas)',
         nota=('Como no M3 e no achado 0; o resto do parágrafo fica no mesmo p.avaliacao-tarefas, que continua a ser um só dentro de '
               'details.regra.'),
         antigo=pesos('Pesos na avaliação')[0], novo=pesos('Pesos na avaliação')[1]),
    dict(i=12, cat='A', ficheiro='m5/mapa-do-modulo-m5/index.html', cartao='secção «As tarefas do Teams» (p.avaliacao-tarefas)',
         nota='Como no M3 e no achado 0; o resto do parágrafo fica no mesmo p.avaliacao-tarefas.',
         antigo=pesos('Avaliação')[0], novo=pesos('Avaliação')[1]),
    dict(i=6, cat='A', ficheiro='m5/licao-m5-f11/index.html', cartao='cartão 23, Para entender («Quem está à mesa»)',
         nota='As células usam o texto do cartão, sem o verbo «é»; o parágrafo do realismo e do naturalismo fica.',
         antigo='<p><b>Ega</b>, amigo de Carlos, defende o naturalismo. <b>Alencar</b> é um poeta romântico, mais velho. <b>Craft</b> é um '
                'inglês rico, colecionador de arte. <b>Cohen</b> é um homem das finanças. <b>Dâmaso</b> imita o que lhe parece elegante.</p>',
         novo=tabela(['Personagem', 'Quem é'], [
             ['Ega', 'amigo de Carlos, defende o naturalismo'], ['Alencar', 'um poeta romântico, mais velho'],
             ['Craft', 'um inglês rico, colecionador de arte'], ['Cohen', 'um homem das finanças'],
             ['Dâmaso', 'imita o que lhe parece elegante']])),
    dict(i=9, cat='A', ficheiro='m5/licao-m5-f13/index.html', cartao='cartão 19, Para entender («Recorda: as peças de um texto de opinião»)',
         nota='«refutação» passa a ter maiúscula por abrir linha; a última frase fica num parágrafo a seguir à tabela.',
         antigo='<p><b>Tese</b>: a tua posição, numa frase. <b>Argumento</b>: uma razão que a prova, com um exemplo. <b>Contra-argumento</b>: '
                'o que dirá quem discorda; <b>refutação</b>: a tua resposta. <b>Modalização</b>: as palavras que mostram o grau de certeza '
                '(«talvez», «sem dúvida», «parece-me»). Para a crítica social, junta a este excerto o jantar do Hotel Central: uma elite que '
                'sabe que o país vai falir e muda de assunto.</p>',
         novo=tabela(['Peça', 'O que é'], [
             ['Tese', 'a tua posição, numa frase'], ['Argumento', 'uma razão que a prova, com um exemplo'],
             ['Contra-argumento', 'o que dirá quem discorda'], ['Refutação', 'a tua resposta'],
             ['Modalização', 'as palavras que mostram o grau de certeza («talvez», «sem dúvida», «parece-me»)']])
              + '<p>Para a crítica social, junta a este excerto o jantar do Hotel Central: uma elite que sabe que o país vai falir e muda '
                'de assunto.</p>'),
    dict(i=13, cat='A', ficheiro='tarefas/m5-u1/index.html', cartao='«Aquecer em cartões» (os tempos da aula de tarefa)',
         nota=('Pelo gerador das tarefas, como no M1 («tabela» e «depois» nos dados, que estão nesta camada). O texto atual diz «para '
               'leres o enunciado» e «depois da leitura»: a linha é «Lês o enunciado» (a proposta citava o texto antigo, «O docente '
               'apresenta o enunciado»). O total fica numa linha do corpo da tabela (a proposta punha-o num <tfoot>, que a folha comum '
               'não empilha no telemóvel), e o estilo é o da folha comum (a proposta pedia regras próprias em task-90.css).'),
         antigo='<p>' + TEMPOS_TEXTO + '</p>', novo=TEMPOS_PAGINA),
    dict(i=14, cat='A', ficheiro='tarefas/m5-u2/index.html', cartao='«Aquecer em cartões» (os tempos da aula de tarefa)',
         nota='Como no achado 13, pelo gerador das tarefas.',
         antigo='<p>' + TEMPOS_TEXTO + '</p>', novo=TEMPOS_PAGINA),
    dict(i=15, cat='C', ficheiro='m5/guia-da-tarefa-m5/index.html', cartao='«Três antes de mim» (div.regra)',
         nota='Os três passos numa lista ordenada, só no M5 (este pedido é do M5).',
         antigo='<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta '
                'ao teu par de trabalho. Só depois levantas o braço.</div>',
         novo='<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica;</li>'
              '<li>pergunta ao teu par de trabalho.</li></ol>Só depois levantas o braço.</div>'),
    dict(i=18, cat='C', ficheiro='m5/licao-m5-f08/index.html', cartao='cartão 2, Para entender («Recorda: o que Simão sabe nesta noite»)',
         nota=('As três perguntas e os quatro factos em listas; «Podias» passa a ter maiúscula por abrir item. A data dos factos já leva '
               'os espaços que não quebram (achado 31). «As marcas de uma carta» fica em linha.'),
         antigo='<p><b>As perguntas de Teresa:</b> podias tu com a desesperança e com a vida? Que farias da vida sem a tua companheira? Nunca '
                'hás de amar outra vez?</p><p><b>Os factos:</b> Simão matou Baltasar e vai degredado para a Índia; a nau saiu do Porto a 17 de '
                'março de 1807; Teresa morreu no convento de Monchique; Mariana, a filha do ferrador, vai a bordo com ele.</p>',
         novo=j('<p><b>As perguntas de Teresa:</b></p><ul><li>Podias tu com a desesperança e com a vida?</li><li>Que farias da vida sem a tua '
                'companheira?</li><li>Nunca hás de amar outra vez?</li></ul><p><b>Os factos:</b></p><ul><li>Simão matou Baltasar e vai '
                'degredado para a Índia;</li><li>a nau saiu do Porto a 17{N}de março de{N}1807;</li><li>Teresa morreu no convento de '
                'Monchique;</li><li>Mariana, a filha do ferrador, vai a bordo com ele.</li></ul>')),
    dict(i=20, cat='C', ficheiro='m5/licao-m5-f11/index.html', cartao='cartão 20, O texto, 6 de 6 (vocabulário: a entrada «Claude Bernard»)',
         nota='A conferência recusou a lista (achado 16): os três nomes a negrito, o último ligado com «e», como no M3.',
         antigo='<b>Claude Bernard</b>, Stuart Mill, Darwin, cientistas',
         novo='<b>Claude Bernard</b>, <b>Stuart Mill</b> e <b>Darwin</b>, cientistas'),
    dict(i=21, cat='C', ficheiro='m5/licao-m5-f12/index.html', cartao='cartão 2, O texto (vocabulário: a entrada «Gremio»)',
         nota='Os dois nomes a negrito, ligados com «e».',
         antigo='<b>Gremio</b>, Casa Havaneza, locais de convívio', novo='<b>Gremio</b> e <b>Casa Havaneza</b>, locais de convívio'),
    dict(i=22, cat='C', ficheiro='m5/licao-m5-f13/index.html', cartao='cartão 15, O texto, 5 de 5 (vocabulário: a entrada «Gremio»)',
         nota='Os nomes a negrito, o último ligado com «e».',
         antigo='<b>Gremio</b>, Casa Havaneza, clube e tabacaria do Chiado', novo='<b>Gremio</b> e <b>Casa Havaneza</b>, clube e tabacaria do Chiado'),
    dict(i=22, cat='C', ficheiro='m5/licao-m5-f13/index.html', cartao='cartão 15, O texto, 5 de 5 (vocabulário: a entrada «Bois»)',
         antigo='<b>Bois</b>, Bignon, Trouville, Saint-Cloud, lugares', novo='<b>Bois</b>, <b>Bignon</b>, <b>Trouville</b> e <b>Saint-Cloud</b>, lugares'),
] + [
    dict(i=23, cat='C', ficheiro='m5/portefolio-do-modulo-m5/index.html', cartao=f'«A lista de verificação»: {n} em <code>',
         nota='Como nas outras linhas da lista, com um ponto onde o nome pode mudar de linha (<wbr>) depois de cada «_».' if k == 0 else None,
         antigo=f'<td>{n}</td>', novo=f'<td><code>{w}</code></td>') for k, (n, w) in enumerate(NOMES_SEM_CODE)
] + [
    dict(i=23, cat='C', ficheiro='m5/portefolio-do-modulo-m5/index.html', cartao=f'«A lista de verificação»: {n}, um ponto para mudar de linha',
         antigo=f'<td><code>{n}</code></td>', novo=f'<td><code>{w}</code></td>') for n, w in NOMES_COM_CODE
] + [
    dict(i=23, cat='C', ficheiro='m5/portefolio-do-modulo-m5/index.html', cartao='a folha da página: os nomes em <code> não se partem',
         nota='O aluno copia estes nomes à letra: na tabela, não partem nos hífenes (só nos <wbr>).',
         antigo='code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\n',
         novo='code{font:.85rem Consolas,"Courier New",monospace;border:1px solid var(--tinta);padding:1px 4px}\ntd code{white-space:nowrap}\n'),
    dict(i=25, cat='C', ficheiro='tarefas/m5-u1/index.html', cartao='tema A, «A voz de Simão»: os cinco elementos da carta',
         nota='Pelo gerador das tarefas (temas[0].texto, nos dados desta camada): os cinco elementos numa lista numerada.',
         antigo=TEMA_A_ANTES, novo=TEMA_A_DEPOIS),
    dict(i=27, cat='C', ficheiro='tarefas/m5-u2/index.html', cartao='tema B, «Falhámos a vida, hoje?»: os cinco elementos do parágrafo',
         nota=('Pelo gerador das tarefas (temas[1].texto, nos dados desta camada); o gerador tira o parágrafo vazio que sobrava no fim '
               '(scripts/tarefas_escolha.py, 08/11/2026).'),
         antigo=TEMA_B_ANTES + '</p>', novo=TEMA_B_ITENS),
]


def ac_grelhas():
    """Os descritores do critério 3 (nível máximo) das grelhas da M5-U1 e da M5-U2 em listas, pelo gerador, como no M1."""
    g = _grelhas()
    out = []
    for i, slug, rel in ((24, 'm5-u1', 'tarefas/m5-u1/grelha/index.html'), (26, 'm5-u2', 'tarefas/m5-u2/grelha/index.html')):
        desc = descritor_c3(slug)
        depois = desc.replace('narrada na 3.ª pessoa;', 'narrada na 3.ª' + NBSP + 'pessoa;')
        out.append(dict(i=i, cat='C', ficheiro=rel, cartao='critério 3, nível 6 («cumprimento consistente»): os elementos de cada tema em listas',
                        nota=('Pelo gerador das grelhas, com «max_em_listas» no critério 3 (nos dados desta camada), como no M1: na forma do '
                              'gerador («<b>Tema A</b>:», a proposta tinha «<b>Tema A:</b>»), com <ul> e o fecho de cada tema num parágrafo; '
                              'a versão de correção fica com o texto corrido (está num <small> dentro de uma célula).'
                              + (' O tema B fecha com «Conclusão:» (o gerador passa a aceitá-la). «3.ª pessoa» já leva o espaço que não quebra '
                                 '(achado 50).' if slug == 'm5-u2' else '')),
                        antigo=f'<p>{g.ital(desc)}</p>', novo=g.em_listas(depois)))
    return out


# Os 35 achados B confirmados. Cada par é o da proposta final (no contexto que a proposta dá), com as ocorrências que mudam;
# «fora» diz quantas ficam de fora e porquê (o «alt», o data-titulo dos vídeos, o que um achado A ou C já mudou, o que outra
# camada já tinha posto), «casca» o que fica para o molde, «mais» onde o número que muda não é o da proposta e porquê, e
# «literais» as trocas que não são só de espaços (com a razão).
CASCA = 'a casca das lições (migalhas, «Estás em» e sigla do rodapé) fica para o molde'
ALT = 'o «alt» não se vê; muda a legenda'
TITULO = 'o data-titulo do vídeo vira o title do leitor; muda o botão'
JA = 'já com U+00A0, de outra camada (os créditos do «i», em <span class="nb">)'


def casca(n):
    return {f'Estás em: Lição M5-{n}': 1, f'Português 2026/2027. Lição M5-{n},': 1, 'pt/2/">2.º ano</a>': 1, 'Narrativa do século XIX</a>': 1}


ACHADOS_B = [
    dict(i=28, ficheiro='m5/licao-m5-f02/index.html', casca=casca('F02'),
         pares=[('A 17 de março, Simão parte', 'A 17{N}de março, Simão parte', 1),
                ('>a folhas 232</b>, o seguinte', '>a folhas{N}232</b>, o seguinte', 1),
                ('<b>a folhas 232</b>, na página 232', '<b>a folhas{N}232</b>, na página{N}232', 1),
                ('lida por Sónia Pedro (5 min)', 'lida por Sónia Pedro (5{N}min)', 1),
                ('<i>Foi para a India em 17 de Março de 1807</i>', '<i>Foi para a India em 17{N}de Março de{N}1807</i>', 1),
                ('«Foi para a India em 17 de Março de 1807» fecha', '«Foi para a India em 17{N}de Março de{N}1807» fecha', 1),
                ('escripto: Foi para a India em 17 de Março de 1807.', 'escripto: Foi para a India em 17{N}de Março de{N}1807.', 1),
                ('Ensina RTP (1 min)', 'Ensina RTP (1{N}min)', 1)],
         fora={'lida por Sónia Pedro (5 min)': (1, TITULO), 'Ensina RTP (1 min)': (1, TITULO)}),
    dict(i=29, ficheiro='m5/licao-m5-f04/index.html', casca=casca('F04'),
         pares=[('primeira parte, cap. IV.', 'primeira parte, cap.{N}IV.', 1),
                ('Lucas de Almeida Marrão, c. 1850)', 'Lucas de Almeida Marrão, c.{N}1850)', 1),
                ('"titulo":"Capítulo IV"', '"titulo":"Capítulo{N}IV"', 1),
                ('_Amor de Perdição_ (1862), cap. IV (grafia', '_Amor de Perdição_ (1862), cap.{N}IV (grafia', 1),
                ('Ler o capítulo IV na Wikisource', 'Ler o capítulo{N}IV na Wikisource', 1),
                ('_Amor de Perdição_, 1862, cap. IV</p>', '_Amor de Perdição_, 1862, cap.{N}IV</p>', 1)],
         fora={'Lucas de Almeida Marrão, c. 1850)': (1, ALT)}),
    dict(i=30, ficheiro='m5/licao-m5-f07/index.html', casca=casca('F07'), pares=[]),
    dict(i=31, ficheiro='m5/licao-m5-f08/index.html', casca=casca('F08'),
         pares=[('Lucas de Almeida Marrão, c. 1850)', 'Lucas de Almeida Marrão, c.{N}1850)', 1),
                ('17 de março de 1807', '17{N}de março de{N}1807', 6),
                ('26 de setembro de 1861', '26{N}de setembro de{N}1861', 2),
                ('A 28 de dezembro de 1815', 'A 28{N}de dezembro de{N}1815', 1),
                ('(primeiros 4 min)', '(primeiros 4{N}min)', 1)],
         fora={'Lucas de Almeida Marrão, c. 1850)': (1, ALT), '(primeiros 4 min)': (1, TITULO),
               '17 de março de 1807': (1, 'a de «Os factos»: o achado 18 (C) passa-os a lista, já com o espaço que não quebra')}),
    dict(i=32, ficheiro='m5/licao-m5-f09/index.html', casca=casca('F09'),
         pares=[('(3 min)', '(3{N}min)', 1), ('(2 min)', '(2{N}min)', 1),
                ('aos 26 de Setembro de 1861', 'aos 26{N}de Setembro de{N}1861', 1)],
         fora={'(3 min)': (1, TITULO), '(2 min)': (1, TITULO)}),
    dict(i=33, ficheiro='m5/licao-m5-f10/index.html', casca=casca('F10'),
         pares=[('(1888), cap. I e último', '(1888), cap.{N}I e último', 1),
                ('(1888), volume 1, página', '(1888), volume{N}1, página', 1),
                ('aparece logo no capítulo I.', 'aparece logo no capítulo{N}I.', 1),
                ('A 28 de dezembro, a RTP1', 'A 28{N}de dezembro, a RTP1', 1),
                ('Ensina RTP (1 min)', 'Ensina RTP (1{N}min)', 1),
                ('"A: Início (cap. I)"', '"A: Início (cap.{N}I)"', 1),
                ('sr.ª</b> D. Maria I:', 'sr.ª</b> D.{N}Maria{N}I:', 1),
                ('papa rico do século XVI\\">Leão X</b>', 'papa rico do século{N}XVI\\">Leão{N}X</b>', 1),
                ('sr. D. João V.', 'sr.{N}D.{N}João{N}V.', 1),
                ('<b>Leão X</b>, papa rico do século XVI</p>', '<b>Leão{N}X</b>, papa rico do século{N}XVI</p>', 1),
                ('(1888), cap. I (grafia', '(1888), cap.{N}I (grafia', 1),
                ('Sónia Pedro (3 min)', 'Sónia Pedro (3{N}min)', 1),
                ('do segundo parágrafo do cap. I.', 'do segundo parágrafo do cap.{N}I.', 1),
                ('1888, cap. I e último', '1888, cap.{N}I e último', 1)],
         fora={'Ensina RTP (1 min)': (1, TITULO), 'Sónia Pedro (3 min)': (1, TITULO)}),
    dict(i=34, ficheiro='m5/licao-m5-f11/index.html', casca=casca('F11'),
         pares=[('(cap. VI). O que marcas', '(cap.{N}VI). O que marcas', 1), ('Benoliel, c. 1910)', 'Benoliel, c.{N}1910)', 1),
                ('O hotel do capítulo VI,', 'O hotel do capítulo{N}VI,', 1), ('(1888), cap. VI (grafia', '(1888), cap.{N}VI (grafia', 1),
                ('1888, cap. VI</p>', '1888, cap.{N}VI</p>', 1)]),
    dict(i=35, ficheiro='m5/licao-m5-f12/index.html', casca=casca('F12'),
         pares=[('(1888), cap. VI e último', '(1888), cap.{N}VI e último', 1), ('1.ª pessoa', '1.ª{N}pessoa', 3),
                ('3.ª pessoa', '3.ª{N}pessoa', 7)]),
    dict(i=36, ficheiro='m5/licao-m5-f13/index.html', casca=casca('F13'),
         pares=[('Porto, c. 1895)', 'Porto, c.{N}1895)', 1)], fora={'Porto, c. 1895)': (1, ALT)}),
    dict(i=37, ficheiro='m5/licao-m5-f14/index.html', casca=casca('F14'),
         pares=[('Benoliel, c. 1910)', 'Benoliel, c.{N}1910)', 1), ('O hotel do capítulo VI,', 'O hotel do capítulo{N}VI,', 1),
                ('(2 min)', '(2{N}min)', 2), ('(capítulo I; retoma', '(capítulo{N}I; retoma', 1), ('>M5-F10</a>', '>M5-{J}F10</a>', 1)],
         fora={'Benoliel, c. 1910)': (1, ALT), '(2 min)': (2, TITULO)}),
    dict(i=38, ficheiro='m5/licao-m5-f15/index.html', casca=casca('F15'),
         pares=[('(1888), volume 1, página', '(1888), volume{N}1, página', 1), ('(primeiros 4 min)', '(primeiros 4{N}min)', 1),
                ('(8 de janeiro de 2025)', '(8{N}de janeiro de{N}2025)', 1)],
         fora={'(1888), volume 1, página': (1, ALT), '(primeiros 4 min)': (1, TITULO)}),
    dict(i=39, ficheiro='m5/licao-m5-f16/index.html',
         pares=[('No capítulo I, o padre', 'No capítulo{N}I, o padre', 1), ('No capítulo III, Brown', 'No capítulo{N}III, Brown', 1),
                ('vol. I, Porto', 'vol.{N}I, Porto', 1), ('do capítulo I (pp. 18–19)', 'do capítulo{N}I (pp.{N}18–{J}19)', 1),
                ('do capítulo III (pp. 82–83)', 'do capítulo{N}III (pp.{N}82–{J}83)', 1), ('capítulos I e III', 'capítulos{N}I e{N}III', 1),
                ('resumo do capítulo III:', 'resumo do capítulo{N}III:', 1), ('capítulo III, p. 90.', 'capítulo{N}III, p.{N}90.', 1),
                ('No mesmo capítulo III,', 'No mesmo capítulo{N}III,', 1)]),
    dict(i=40, ficheiro='m5/licao-m5-f17/index.html',
         pares=[('7 de março de 1882', '7{N}de março de{N}1882', 1),
                ('capítulo XII, edição de Ivo Castro', 'capítulo{N}XII, edição de Ivo Castro', 1),
                ('2020, p. 120.', '2020, p.{N}120.', 1),
                ('Procura o capítulo XII e a página impressa 120.', 'Procura o capítulo{N}XII e a página impressa{N}120.', 1),
                ('recorte do capítulo XII.', 'recorte do capítulo{N}XII.', 1),
                ('Relê o recorte do capítulo XII e', 'Relê o recorte do capítulo{N}XII e', 1)]),
    dict(i=41, ficheiro='m5/index.html',
         pares=[('aula de tarefa de 90 minutos: aquecimento', 'aula de tarefa de 90{N}minutos: aquecimento', 1),
                ('tarefa 90 min</small>', 'tarefa 90{N}min</small>', 2), ('cerca de 25 min, sem nada', 'cerca de 25{N}min, sem nada', 2),
                ('<span class="chip">10 min</span>', '<span class="chip">10{N}min</span>', 2),
                ('<span class="chip">90 min</span>', '<span class="chip">90{N}min</span>', 2),
                ('90 minutos com consulta', '90{N}minutos com consulta', 2), ('Grelha /20; 30 %.', 'Grelha /20; 30{N}%.', 2),
                ('Narrativa do século XIX</span></h1>', 'Narrativa do século{N}XIX</span></h1>', 1),
                ('Módulo 5, Narrativa do século XIX. Nada', 'Módulo 5, Narrativa do século{N}XIX. Nada', 1), ('2.º ano', '2.º{N}ano', 2),
                ('a folhas 232.', 'a folhas{N}232.', 1), ('17 de Março de 1807', '17{N}de Março de{N}1807', 2),
                ('26 de Setembro de 1861', '26{N}de Setembro de{N}1861', 2), ('capítulo IV', 'capítulo{N}IV', 3),
                ('17 de março de 1807', '17{N}de março de{N}1807', 6), ('26 de setembro de 1861', '26{N}de setembro de{N}1861', 2),
                ('28 de dezembro de 1815', '28{N}de dezembro de{N}1815', 1), ('no capítulo VI?', 'no capítulo{N}VI?', 1),
                ('.ª pessoa', '.ª{N}pessoa', 12), ('28 de dezembro de 2015', '28{N}de dezembro de{N}2015', 1)]),
    dict(i=42, ficheiro='m5/guia-da-tarefa-m5/index.html',
         literais=[('Narrativa do Séc. XIX', 'Narrativa do século{N}XIX',
                    '«Séc. XIX» passa a «século XIX», como na proposta (é a única forma abreviada do M5), já com o espaço que não quebra')],
         pares=[('tarefa de 90 minutos, com aquecimento', 'tarefa de 90{N}minutos, com aquecimento', 1),
                ('em cartões (10 minutos). Seguem-se 5 minutos de', 'em cartões (10{N}minutos). Seguem-se 5{N}minutos de', 1),
                ('</a><br>30 %, individual', '</a><br>30{N}%, individual', 2),
                ('<b>Aquecer, 10 min</b>', '<b>Aquecer, 10{N}min</b>', 1), ('<b>Ler o enunciado, 5 min</b>', '<b>Ler o enunciado, 5{N}min</b>', 1),
                ('<b>Produzir, 60 min</b>', '<b>Produzir, 60{N}min</b>', 1),
                ('<b>Rever e entregar, 15 min</b>', '<b>Rever e entregar, 15{N}min</b>', 1), ('2.º ano', '2.º{N}ano', 2)]),
    dict(i=43, ficheiro='m5/mapa-do-modulo-m5/index.html',
         pares=[('Camilo Castelo Branco (1825–1890)', 'Camilo Castelo Branco (1825–{J}1890)', 1),
                ('Eça de Queirós (1845–1900)', 'Eça de Queirós (1845–{J}1900)', 1),
                ('individual, 90 minutos, 30 %.', 'individual, 90{N}minutos, 30{N}%.', 2),
                ('tarefa de 90 minutos, com aquecimento', 'tarefa de 90{N}minutos, com aquecimento', 1),
                ('(1888), volume 1, página', '(1888), volume{N}1, página', 2),
                ('">Lição M5-F', '">Lição M5-{J}F', 7), ('">lição M5-F', '">lição M5-{J}F', 4),
                ('<h1>Narrativa do século XIX</h1>', '<h1>Narrativa do século{N}XIX</h1>', 1), ('2.º ano', '2.º{N}ano', 2)],
         fora={'Marrão, c. 1850)': (2, 'o «alt»; o crédito do «i» já tem U+00A0, de outra camada (em <span class="nb">)'),
               'Porto, c. 1895)': (2, 'o «alt»; o crédito do «i» já tem U+00A0, de outra camada (em <span class="nb">)'),
               'Benoliel, c. 1910)': (2, 'o «alt»; o crédito do «i» já tem U+00A0, de outra camada (em <span class="nb">)'),
               '(1888), volume 1, página': (2, 'o «alt» e o aria-label do «i» não se veem')},
         mais={'(1888), volume 1, página': (2, 'a varredura contou o «alt» e a legenda; o crédito do «i» (camada de 7/11, depois da '
                                              'varredura) também se vê e muda com a legenda')}),
    dict(i=44, ficheiro='m5/portefolio-do-modulo-m5/index.html',
         pares=[('tarefa de 90 minutos, com grelha', 'tarefa de 90{N}minutos, com grelha', 1), ('(40 %)', '(40{N}%)', 1),
                ('2.º ano', '2.º{N}ano', 2), ('Narrativa do século XIX.</p>', 'Narrativa do século{N}XIX.</p>', 1)]),
    dict(i=45, ficheiro='tarefas/m5-u1/index.html',
         literais=[('durante 90 minutos, com entrega', 'durante 90{N}minutos, com entrega',
                    'a meta descrição muda com «nao_partir» (o gerador prende os três números do molde, como no M1 e no M3); a conferência '
                    'tirou-a da lista porque não se vê')],
         pares=[('Antes de escrever · 10 min ·', 'Antes de escrever · 10{N}min ·', 1), ('Unidade 1 · 90 min', 'Unidade 1 · 90{N}min', 1),
                ('outra do cap. IV em que', 'outra do cap.{N}IV em que', 1),
                ('virtudes» (cap. IV), «Teu primo»', 'virtudes» (cap.{N}IV), «Teu primo»', 1),
                ('a 17 de março de 1807;', 'a 17{N}de março de{N}1807;', 1)]),
    dict(i=46, ficheiro='tarefas/m5-u2/index.html',
         literais=[('durante 90 minutos, com entrega', 'durante 90{N}minutos, com entrega',
                    'a meta descrição muda com «nao_partir» (o gerador prende os três números do molde, como no M1 e no M3); a conferência '
                    'tirou-a da lista porque não se vê')],
         pares=[('Antes de escrever · 10 min ·', 'Antes de escrever · 10{N}min ·', 1), ('Unidade 2 · 90 min', 'Unidade 2 · 90{N}min', 1),
                ('que vem do cap. I e outra nova.', 'que vem do cap.{N}I e outra nova.', 1), ('No cap. VI, Alencar', 'No cap.{N}VI, Alencar', 1),
                ('Narra na 3.ª pessoa', 'Narra na 3.ª{N}pessoa', 1), ('o hotel do cap. VI, trinta', 'o hotel do cap.{N}VI, trinta', 1),
                ('A 28 de dezembro de 2015, a RTP1', 'A 28{N}de dezembro de{N}2015, a RTP1', 1),
                ('A 8 de janeiro de 2025, Eça', 'A 8{N}de janeiro de{N}2025, Eça', 1)]),
    dict(i=47, ficheiro='tarefas/m5-u1/aquecimento/index.html', pares=[('na Introdução e no cap. IV;', 'na Introdução e no cap.{N}IV;', 1)]),
    dict(i=48, ficheiro='tarefas/m5-u2/aquecimento/index.html', pares=[('no cap. I, há uma', 'no cap.{N}I, há uma', 1)]),
    dict(i=49, ficheiro='tarefas/m5-u1/grelha/index.html',
         pares=[('outra do cap. IV em que', 'outra do cap.{N}IV em que', 1),
                ('virtudes» (cap. IV), «Teu primo»', 'virtudes» (cap.{N}IV), «Teu primo»', 1),
                ('amor» (cap. IV): copio', 'amor» (cap.{N}IV): copio', 1)]),
    dict(i=50, ficheiro='tarefas/m5-u2/grelha/index.html',
         pares=[('o que vem do cap. I e o que é novo', 'o que vem do cap.{N}I e o que é novo', 1),
                ('já estava no cap. I e outra', 'já estava no cap.{N}I e outra', 1),
                ('narrada na 3.ª pessoa;', 'narrada na 3.ª{N}pessoa;', 0), ('primo!» (cap. IV de', 'primo!» (cap.{N}IV de', 1)],
         fora={'narrada na 3.ª pessoa;': (1, 'o achado 26 (C) passa o descritor a listas, já com o espaço que não quebra')}),
    dict(i=51, ficheiro='tarefas/m5-u1/correcao/index.html', pares=[('outra do cap. IV em que', 'outra do cap.{N}IV em que', 1)]),
    dict(i=52, ficheiro='tarefas/m5-u2/correcao/index.html',
         pares=[('já estava no cap. I e outra', 'já estava no cap.{N}I e outra', 1), ('narrada na 3.ª pessoa;', 'narrada na 3.ª{N}pessoa;', 1)]),
    dict(i=53, ficheiro='m5/camilo-assento/index.html',
         pares=[('Gutenberg n.º 16425)', 'Gutenberg n.º{N}16425)', 2), ('folhas 232', 'folhas{N}232', 3), ('na página 232', 'na página{N}232', 1),
                ('17 de Março de 1807', '17{N}de Março de{N}1807', 2)]),
    dict(i=54, ficheiro='m5/camilo-carta/index.html', pares=[('Gutenberg n.º 16425)', 'Gutenberg n.º{N}16425)', 2)]),
    dict(i=55, ficheiro='m5/camilo-pai/index.html',
         pares=[('Gutenberg n.º 16425)', 'Gutenberg n.º{N}16425)', 2), ('1862, cap. IV', '1862, cap.{N}IV', 2)]),
    dict(i=56, ficheiro='m5/gram-funcoes/index.html', pares=[('Gutenberg n.º 16425)', 'Gutenberg n.º{N}16425)', 3)]),
    dict(i=57, ficheiro='m5/eca-falhamos/index.html', pares=[('Gutenberg n.º 40409)', 'Gutenberg n.º{N}40409)', 2)]),
    dict(i=58, ficheiro='m5/eca-hotel/index.html',
         pares=[('Gutenberg n.º 40409)', 'Gutenberg n.º{N}40409)', 2), ('1888, cap. VI', '1888, cap.{N}VI', 2)]),
    dict(i=59, ficheiro='m5/eca-ramalhete/index.html',
         pares=[('Gutenberg n.º 40409)', 'Gutenberg n.º{N}40409)', 2), ('1888, cap. I e último', '1888, cap.{N}I e último', 2),
                ('sr.ª D. Maria I:', 'sr.ª{N}D.{N}Maria{N}I:', 1)]),
    dict(i=60, ficheiro='m5/gram-dil/index.html', pares=[('Gutenberg n.º 40409)', 'Gutenberg n.º{N}40409)', 3)]),
    dict(i=61, ficheiro='m5/m5-quem-podia-ter-feito-diferente/index.html',
         pares=[('cerca de 25 min</p>', 'cerca de 25{N}min</p>', 1), ('a folhas 232, o seguinte', 'a folhas{N}232, o seguinte', 1),
                ('em 17 de Março de 1807', 'em 17{N}de Março de{N}1807', 1),
                ('</i>, Capítulo IV (o retrato', '</i>, Capítulo{N}IV (o retrato', 2), ('Gutenberg n.º 16425', 'Gutenberg n.º{N}16425', 5)]),
    dict(i=62, ficheiro='m5/m5-o-pais-ou-eles/index.html',
         pares=[('cerca de 25 min</p>', 'cerca de 25{N}min</p>', 1), ('O hotel do capítulo VI,', 'O hotel do capítulo{N}VI,', 0),
                ('</i>, cap. VI, o jantar', '</i>, cap.{N}VI, o jantar', 2), ('</i>, cap. IV, uma vida', '</i>, cap.{N}IV, uma vida', 1),
                ('Gutenberg n.º 40409', 'Gutenberg n.º{N}40409', 5), ('no capítulo IV: resoluções', 'no capítulo{N}IV: resoluções', 1),
                ('O diletante do capítulo IV e', 'O diletante do capítulo{N}IV e', 1)],
         fora={'O hotel do capítulo VI,': (1, 'só no «alt» desta página, que não se vê')}),
]

# As notas do docente das lições geradas F16 e F17 (m5/painel-m5-f16 e f17, de scripts/gerar_licoes_20261101.py, render_notes)
# repetem os retornos dos cartões: os pares do achado da lição que lá estão mudam também, e as notas saem iguais do gerador.
NOTAS = [
    dict(i=39, ficheiro='m5/painel-m5-f16/index.html',
         pares=[('capítulos I e III', 'capítulos{N}I e{N}III', 1), ('resumo do capítulo III:', 'resumo do capítulo{N}III:', 1)]),
    dict(i=40, ficheiro='m5/painel-m5-f17/index.html',
         pares=[('recorte do capítulo XII.', 'recorte do capítulo{N}XII.', 1),
                ('Relê o recorte do capítulo XII e', 'Relê o recorte do capítulo{N}XII e', 1)]),
]

# A casca das lições fica para o molde, como do M1 ao M4: nenhuma troca. As lições onde a varredura a viu.
CASCA_NO_MOLDE = sorted(x['ficheiro'] for x in ACHADOS_B if x.get('casca'))

# Dados dos geradores. As trocas A e C (a tabela dos tempos, as listas dos temas e «max_em_listas») e «nao_partir» vão à frente;
# os pares B depois, com as mesmas sequências das páginas (sem o que vem do molde dos geradores).
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DADOS = [
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m5-u1.json', achados=(45,), nao_partir='\n "unidade": 1,\n',
         ac=[(13, 'A', 'Dados da tarefa: o aquecimento com a tabela dos tempos («texto», «tabela» e «depois», como na M1-U1)',
              f'  "texto": {json.dumps(TEMPOS_TEXTO, ensure_ascii=False)},\n', None),
             (25, 'C', 'Dados da tarefa: o tema A com os cinco elementos da carta numa lista numerada', TEMA_A_ANTES, TEMA_A_DEPOIS)],
         pares=[('outra do cap. IV em que', 'outra do cap.{N}IV em que', 1),
                ('virtudes» (cap. IV), «Teu primo»', 'virtudes» (cap.{N}IV), «Teu primo»', 1),
                ('a 17 de março de 1807;', 'a 17{N}de março de{N}1807;', 1)]),
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m5-u2.json', achados=(46,), nao_partir='\n "unidade": 2,\n',
         ac=[(14, 'A', 'Dados da tarefa: o aquecimento com a tabela dos tempos («texto», «tabela» e «depois», como na M1-U1)',
              f'  "texto": {json.dumps(TEMPOS_TEXTO, ensure_ascii=False)},\n', None),
             (27, 'C', 'Dados da tarefa: o tema B com os cinco elementos do parágrafo numa lista numerada (o texto acaba em «<p>»)',
              TEMA_B_ANTES + '"', TEMA_B_ITENS + '<p>"')],
         pares=[('que vem do cap. I e outra nova.', 'que vem do cap.{N}I e outra nova.', 1), ('No cap. VI, Alencar', 'No cap.{N}VI, Alencar', 1),
                ('Narra na 3.ª pessoa', 'Narra na 3.ª{N}pessoa', 1), ('o hotel do cap. VI, trinta', 'o hotel do cap.{N}VI, trinta', 1),
                ('A 28 de dezembro de 2015, a RTP1', 'A 28{N}de dezembro de{N}2015, a RTP1', 1),
                ('A 8 de janeiro de 2025, Eça', 'A 8{N}de janeiro de{N}2025, Eça', 1)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m5-u1.json', achados=(47,), pares=[('na Introdução e no cap. IV;', 'na Introdução e no cap.{N}IV;', 1)]),
    dict(ficheiro='docs/pedagogia/aquecimentos/m5-u2.json', achados=(48,), pares=[('no cap. I, há uma', 'no cap.{N}I, há uma', 1)]),
    dict(ficheiro=GRELHAS, entrada='m5-u1', achados=(49, 51), max_em_listas=24,
         pares=[('outra do cap. IV em que', 'outra do cap.{N}IV em que', 1),
                ('virtudes» (cap. IV), «Teu primo»', 'virtudes» (cap.{N}IV), «Teu primo»', 1),
                ('amor» (cap. IV): copio', 'amor» (cap.{N}IV): copio', 1)]),
    dict(ficheiro=GRELHAS, entrada='m5-u2', achados=(50, 52), max_em_listas=26,
         pares=[('o que vem do cap. I e o que é novo', 'o que vem do cap.{N}I e o que é novo', 1),
                ('já estava no cap. I e outra', 'já estava no cap.{N}I e outra', 1),
                ('narrada na 3.ª pessoa;', 'narrada na 3.ª{N}pessoa;', 1), ('primo!» (cap. IV de', 'primo!» (cap.{N}IV de', 1)]),
]


def ler(rel):
    return desfazer_enunciados(rel, (ROOT / rel).read_bytes().decode('utf-8'))


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


# Os pares da proposta que acabam a meio de uma palavra (a sigla da lição, antes do número): à direita não se exige a palavra inteira.
A_MEIO = {'">Lição M5-F', '">lição M5-F'}


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
    m = re.match(r'm5/(?:licao|painel)-(m5-f\d+)/', rel)
    if m:
        return m.group(1).upper() + (' (notas do docente)' if '/painel-' in rel else '')
    return rel.replace('/index.html', '')


def substituir(pre, regioes, antes, depois):
    """Troca um trecho único e atualiza as regiões de texto novo (onde nenhum par B pode cair)."""
    if pre.count(antes) != 1:
        raise SystemExit(f'trecho que não aparece uma vez: {antes[:80]!r}')
    inicio = pre.index(antes)
    delta = len(depois) - len(antes)
    regioes = [(a if a < inicio else a + delta, b if b <= inicio else b + delta) for a, b in regioes]
    return pre.replace(antes, depois), regioes + [(inicio, inicio + len(depois))]


def proposta(x):
    """O que o achado põe na conta, par a par (para o relatório): o que muda, o que fica de fora e a casca (onde isto não dá o
    número da proposta, «mais» diz o número da proposta e porquê)."""
    out = {}
    for seq, n in ([(p[0], p[2]) for p in x['pares']] + [(s, n) for s, (n, _) in x.get('fora', {}).items()]
                   + list(x.get('casca', {}).items()) + [(a, 1) for a, _, _ in x.get('literais', [])]):
        out[seq] = out.get(seq, 0) + n
    return out


def b_da_pagina(rel, base_txt, pre, regioes, x, rotulo=None):
    """As trocas de um achado B numa página: primeiro as literais (com a razão), depois os pares."""
    trocas = []
    for antigo, novo, razao in x.get('literais', []):
        pre, regioes = substituir(pre, regioes, antigo, j(novo))
        trocas.append({'ficheiro': rel, 'local': f'{rotulo or nome(rel)}: «{antigo}»', 'antigo': antigo, 'novo': j(novo),
                       'ocorrencias': 1, 'achado': ACHADO.format(i=x['i'], cat='B', texto=TEXTO_CAT['B'] + ' ' + razao[0].upper()
                                                                  + razao[1:] + '.')})
    pares = x['pares']
    janelas, _ = janelas_pares(rel, pre, pares, regioes)
    texto = TEXTO_CAT['B'] + (' Nas notas do docente, geradas a partir dos cartões da lição (scripts/gerar_licoes_20261101.py).'
                              if '/painel-' in rel else '')
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
        relatorio.append((rel, x['i'], 'B', sum(p[2] for p in x['pares']) + len(x.get('literais', [])), sum(proposta(x).values()), ''))
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
        if spec.get('nao_partir'):
            antes = spec['nao_partir']
            depois = antes + ' "nao_partir": true,\n'
            pre, regioes = substituir(pre, regioes, antes, depois)
            trocas.append({'ficheiro': rel, 'local': 'Dados da tarefa: «nao_partir», os números do molde com espaço que não quebra',
                           'antigo': antes, 'novo': depois, 'ocorrencias': 1,
                           'achado': ACHADO.format(i='/'.join(map(str, spec['achados'])), cat='B', texto=TEXTO_CAT['B'] + (
                               ' Os números do molde da tarefa («90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) levam o '
                               'espaço que não quebra pelo gerador (scripts/tarefas_escolha.py), como no M1 e no M3.'))})
        for i, cat, local, antes, depois in spec.get('ac', []):
            if depois is None:
                depois = tempos_json()
            pre, regioes = substituir(pre, regioes, antes, depois)
            trocas.append({'ficheiro': rel, 'local': local, 'antigo': antes, 'novo': depois, 'ocorrencias': 1,
                           'achado': ACHADO.format(i=i, cat=cat, texto=TEXTO_CAT[cat] + ' Nos dados do gerador das tarefas, que '
                                                   'passam iguais para a página.')})
        if spec.get('max_em_listas'):
            # O critério 3 desta entrada: «"max": 6,» passa a levar «"max_em_listas": true,» a seguir, como no M1. O trecho cresce
            # para a direita até ser único no ficheiro.
            a, b = _limite(pre, spec['entrada'])
            k = pre.index('"nome": "Tema à escolha (A ou B)', a, b)
            k = pre.index('"max": 6,\n', k) + len('"max": 6,\n')
            fim = k + 1
            while pre.count(pre[k - len('"max": 6,\n'):fim]) != 1:
                fim += 1
            antes = pre[k - len('"max": 6,\n'):fim]
            depois = '"max": 6,\n     "max_em_listas": true,\n' + pre[k:fim]
            pre, regioes = substituir(pre, regioes, antes, depois)
            trocas.append({'ficheiro': rel, 'local': f'Dados das grelhas, {spec["entrada"]}: «max_em_listas» no critério 3',
                           'antigo': antes, 'novo': depois, 'ocorrencias': 1,
                           'achado': ACHADO.format(i=spec['max_em_listas'], cat='C', texto=TEXTO_CAT['C'] + (
                               ' O descritor do nível máximo do critério 3 abre os elementos de cada tema em listas, pelo gerador das '
                               'grelhas (scripts/grelhas_tarefas.py), como no M1; a versão de correção fica com o texto corrido.'))})
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


# Os enunciados dos painéis do docente (m5/painel-m5-fxx) são os dos cartões da lição: o «p» (ou a «frase»), com ou sem os
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
    for licao in sorted(r for r in finais if r.startswith('m5/licao-')):
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
    for x in ACHADOS_AC + ac_grelhas():
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
