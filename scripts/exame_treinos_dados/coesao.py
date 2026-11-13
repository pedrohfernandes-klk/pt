"""13/11/2026: treino 6, «O que retoma, o que situa, o que liga» (exame/treinos/coesao/), ligado à sessão 22.

Dois itens de gramática do Grupo II da 2.ª fase de 2026 sobre o mesmo texto (Elsa de Barros, «As virtudes do pensamento
lento»): o item 5 (coesão gramatical referencial) e o item 6 (modalidade). Os dois são opcionais (contam os três melhores de
cinco). Os critérios do Grupo II só trazem o quadro das chaves: tudo o que explica porquê é leitura nossa e vem dito como tal.
As definições vêm do Dicionário Terminológico (entradas guardadas em tests/fixtures/dicionario-terminologico-20261113.json).
As linhas do texto da prova vêm da transcrição, com a numeração da prova e os cortes marcados; a linha 24 não entra.
"""
from .base import *
from .gramatica import linhas, tem

G1 = F1['grupos'][1]
G2 = F2['grupos'][1]
TX = G2['textos'][0]
L2 = {l['n']: l['t'] for l in TX['linhas']}
assert TX['titulo'] == '«As virtudes do pensamento lento»' and sorted(L2) == list(range(1, 47))
I5, I6 = G2['itens'][4], G2['itens'][5]
assert (I5['numero'], I5['chave_versao_2'], I5['cotacao'], I5['obrigatorio']) == ('II.5', 'D', 13, False)
assert (I6['numero'], I6['chave_versao_2'], I6['cotacao'], I6['obrigatorio']) == ('II.6', 'C', 13, False)
assert G2['chaves_criterios_quadro']['linhas'][4] == ['5.', '(C)', '(D)', 13]
assert G2['chaves_criterios_quadro']['linhas'][5] == ['6.', '(A)', '(C)', 13]
OPC = 'Destes 5 itens, contribuem para a classificação final da prova os 3 itens cujas respostas obtenham melhor pontuação.'
assert F2['cotacoes']['opcionais']['texto'] == OPC == F1['cotacoes']['opcionais']['texto']
assert F2['cotacoes']['opcionais']['itens'] == ['I.3', 'I.6', 'II.2', 'II.5', 'II.6']
# a mesma operação na 1.ª fase: itens 5 (opcional) e 6 (conta sempre), só referidos
J5, J6 = G1['itens'][4], G1['itens'][5]
assert (J5['numero'], J5['chave_versao_2'], J5['obrigatorio']) == ('II.5', 'B', False) and 'II.5' in F1['cotacoes']['opcionais']['itens']
assert (J6['numero'], J6['chave_versao_2'], J6['obrigatorio']) == ('II.6', 'C', True) and ['II.6', 13] in F1['cotacoes']['obrigatorios']['itens']
assert J5['enunciado'][0] == 'Entre as linhas 6 e 22, a coesão lexical e a coesão gramatical referencial são asseguradas por mecanismos como'
assert J5['opcoes'][1]['texto'].endswith('e o uso dos vocábulos «cujos» e «onde», no segundo caso.')
assert 'o predomínio de verbos no presente do indicativo' in J5['opcoes'][0]['texto']
assert J6['enunciado'][0].startswith('O vocábulo «como» está associado a uma ideia de exemplificação e a uma ideia de comparação')

# ---------- citações dos critérios (iguais nas duas fases) ----------
GER1 = json.dumps(F1['criterios']['gerais'], ensure_ascii=False)
GER2 = json.dumps(F2['criterios']['gerais'], ensure_ascii=False)
R_DICO = 'a pontuação só é atribuída às respostas corretas, sendo todas as outras respostas classificadas com zero pontos'
R_CONECT = 'a progressão e a clareza das ideias podem ser asseguradas através de diversos mecanismos (nomeadamente a pontuação e a repetição lexical), sem recurso obrigatório a conectores interfrásicos'
R_COES = 'avalia-se a capacidade de assegurar a progressão e o encadeamento da informação através do recurso a mecanismos de coesão textual adequados'
for _s in (R_DICO, R_CONECT, R_COES):
    assert _s in GER1 and _s in GER2, _s
PC = F2['grupos'][2]['itens'][0]['criterios']['ETD']['parametros'][2]
assert PC == F1['grupos'][2]['itens'][0]['criterios']['ETD']['parametros'][2]
assert (PC['id'], PC['nome'], PC['pontos']) == ('C', 'Organização e Coesão Textuais', 10) and PC['niveis'][0]['nivel'] == 4
C_LIGAR, C_RETOMAR, C_SITUAR = [x.rstrip(';.') for x in PC['niveis'][0]['descritores'][0][3:6]]
assert C_LIGAR == 'utiliza, adequadamente, mecanismos de articulação interfrásica'
assert C_RETOMAR == 'mantém, de forma sistemática, cadeias de referência através de substituições nominais e pronominais adequadas'
assert C_SITUAR == 'estabelece conexões adequadas entre coordenadas de enunciação (pessoa, tempo, espaço) ao longo do texto'

# ---------- Dicionário Terminológico: citações conferidas com as entradas guardadas a 13/11/2026 ----------
_dt = json.load(open(ROOT + '/tests/fixtures/dicionario-terminologico-20261113.json', encoding='utf-8'))['entradas']


def dtx(i):
    """Texto da entrada (definição, exemplos e notas), sem marcas e com os espaços normalizados."""
    r = _dt[i]
    x = html.unescape(re.sub(r'<[^>]+>', ' ', r['definition'] + ' ' + (r.get('examples') or '') + ' ' + (r.get('notes') or '')))
    return re.sub(r'\s+', ' ', x).replace(' ,', ',').replace(' .', '.').replace('( ', '(').replace(' )', ')')


DT_MODAL = '«A modalidade permite expressar apreciações sobre o conteúdo de um enunciado (i) ou representar valores de probabilidade ou certeza (modalidade epistémica) (ii), ou de permissão ou obrigação (valor deôntico) (iii).»'
DT_EX_EPI = '«Talvez esteja a chover.»'
DT_EX_DEO = '«Tens de trabalhar mais!»'
DT_REFV = '«variável (por exemplo "eu", "hoje", "isso"), sendo, neste caso, fixada através de processos de deixis ou anáfora»'
DT_ANA = '«Expressão linguística (termo anafórico) cuja interpretação depende da relação de co-referência ou da relação sinedóquica ou meronímica que mantém com outra expressão (o antecedente) que figura anteriormente na linearidade do texto.»'
DT_DEI = '«“agora” é o momento em que o “eu” fala»'
DT_DEI_ADJ = '«alguns adjectivos (actual, contemporâneo, futuro, etc.)»'
DT_DEI_TXT = '«Merece particular menção a deixis textual»'
DT_COE = '«as cadeias de referência, as reiterações e substituições lexicais (coesão lexical), os conectores interfrásicos (coesão interfrásica) e a ordenação correlativa dos tempos verbais»'
DT_CITA = [(DT_MODAL, 'n402'), (DT_EX_EPI, 'n402'), (DT_EX_DEO, 'n402'), (DT_REFV, 'n390'), (DT_ANA, 'n463'), (DT_DEI, 'n420'), (DT_DEI_ADJ, 'n420'), (DT_DEI_TXT, 'n420'), (DT_COE, 'n462')]
for _c, _i in DT_CITA:
    assert _c.strip('«»') in dtx(_i), (_c, dtx(_i))
assert [_dt[i]['title'] for i in ('n402', 'n390', 'n463', 'n420', 'n462')] == ['Modalidade', 'Referência', 'Anáfora', 'Deixis', 'Coesão textual']
DT_REF = '<span class="pag">(<i>Dicionário Terminológico</i>, dt.dge.mec.pt, entrada «%s»; consultado a 13/11/2026; grafia do original)</span>'

# ---------- as linhas da prova que ficam ao lado dos passos ----------
for _a, _b, _s in [(1, 1, 'Hoje em dia'), (23, 23, 'um tipo de atenção'), (29, 29, 'no livro'), (5, 5, 'dos alunos'), (17, 17, 'diante'), (19, 19, 'este tipo'),
                   (18, 18, 'atrás'), (21, 21, 'na obra _Sociedade do Cansaço_'), (30, 30, 'dois tipos'), (6, 6, 'estes'), (31, 31, 'os primeiros'), (31, 32, 'os segundos'),
                   (6, 6, 'os desafios escolares, quando estes contrariam'), (30, 30, 'dois tipos de mecanismos'), (16, 17, 'naquilo que tem diante de si'), (17, 18, 'àquilo que está atrás de si'),
                   (11, 12, 'será que esta visão é correta e está a ser favorável para a própria sociedade que a criou?'), (13, 13, 'Antes de responder a esta questão'),
                   (13, 13, 'podemos fazer o seguinte exercício'), (13, 14, 'imaginemo-nos a regressar ao cenário da vida selvagem, na qual um animal tem de dividir a sua atenção'),
                   (14, 15, 'um animal tem de dividir a sua atenção por diversas atividades para que, enquanto come, não acabe por ser comido.'),
                   (17, 17, 'pois tem de estar permanentemente alerta'), (18, 18, 'muitas das atividades mais valorizadas na atualidade'),
                   (19, 19, 'privilegiam este tipo de mecanismos'), (44, 44, 'Mas esta revolução tem os seus riscos.'), (45, 45, 'pode implicar soluções'), (1, 1, 'as crianças')]:
    tem(L2, _a, _b, _s)
assert '—' in L2[24] and all('—' not in L2[n] for n in L2 if n != 24)
MOSTRADAS = [1, 5, 6] + list(range(11, 24)) + [29, 30, 31, 32, 44, 45, 46]

FONTE = ('<p class="fonte">' + md(TX['fonte']) + ' Texto do Grupo II da Prova 639, 2026, 2.ª fase (enunciado, p. 6), com a numeração de linhas da prova. '
         'Aqui estão só as linhas de que precisas; o texto completo está no ' + lig('e2', 'PDF da prova (eduqa.pt)') + '.</p>')
TIT = '<p class="texto-t">Elsa de Barros, «As virtudes do pensamento lento»</p>'


def _uma(h, velho, novo):
    assert h.count(velho) == 1, (velho, h.count(velho))
    return h.replace(velho, novo)


AP_OF = _uma(_uma(linhas(L2, [(1, 1), (5, 6), (16, 23), (29, 32)],
                         ['Hoje em dia', 'um tipo de atenção', 'no livro', 'dos alunos', 'diante', 'este tipo', 'atrás', 'na obra <i>Sociedade do Cansaço</i>', 'dois tipos', 'estes', 'os primeiros']),
                  'enquanto os</span>', 'enquanto <mark>os</mark></span>'), '<span>segundos, de', '<span><mark>segundos</mark>, de')
assert AP_OF.count('<mark>') == 13
AP_OF = (TIT + '<p class="texto-a">Linhas 1, 5 e 6, 16 a 23 e 29 a 32. Os realces a amarelo são nossos: marcam as doze expressões do item 5.</p>' + AP_OF + FONTE)
AP_TR = _uma(linhas(L2, [(11, 20)], ['na qual', 'esta questão', 'na atualidade']), 'sociedade que a criou?', 'sociedade que <mark>a</mark> criou?')
assert AP_TR.count('<mark>') == 4
AP_TR = (TIT + '<p class="texto-a">Linhas 11 a 20, do mesmo texto da prova. Os realces a amarelo são nossos.</p>' + AP_TR + FONTE)
AP_MOD = linhas(L2, [(13, 18), (44, 46)], ['podemos fazer', 'para que', ', pois', 'tem de estar', 'pode implicar']).replace('<mark>, pois</mark>', ', <mark>pois</mark>')
assert AP_MOD.count('<mark>') == 5
AP_MOD = (TIT + '<p class="texto-a">Linhas 13 a 18 e 44 a 46. Os realces a amarelo são nossos.</p>' + AP_MOD + FONTE)
LINHAS_HTML = [AP_OF, AP_TR, AP_MOD]


def item_of(I, n, pagina, extra=''):
    ops = ''.join('<li><b>(%s)</b> %s</li>' % (o['letra'], md(o['texto'])) for o in I['opcoes'])
    return ('<div class="caixa of">' + etq('oficial') +
            '<p class="enun"><b>%d.</b> ' % n + md(I['enunciado'][0]) + '</p><ul class="top sem-marcas">' + ops + '</ul>'
            '<p class="pag">Prova 639, 2026, 2.ª fase, versão 2, Grupo II, item %d. Escolha múltipla, 13 pontos; é um dos cinco itens de que contam os três melhores. Enunciado, p. %s.%s</p></div>' % (n, pagina, extra))


OF5 = item_of(I5, 5, '7', ' A chave oficial aparece no passo 6, depois de responderes.')
OF6 = item_of(I6, 6, '8')
OPS5 = ['(%s) %s' % (o['letra'], md(o['texto'])) for o in I5['opcoes']]

# frases de treino que vêm do aquecimento e da sessão 22
_s22 = json.load(open(ROOT + '/docs/pedagogia/exame-aquecimentos/s22.json', encoding='utf-8'))
_j22 = json.dumps(_s22, ensure_ascii=False)
F_INES = 'Inês viu a mãe quando ela entrou'
F_TALVEZ = 'Talvez a personagem reconheça o erro'
F_TEMDE = 'Para ser perdoada, a personagem tem de reconhecer o erro.'
for _f in (F_INES, F_TALVEZ):
    assert '_%s_' % _f in _j22 and any('_%s_' % _f in q['q'] for q in SESSOES['s22']['warmup']), _f
assert _s22['titulo'] == SESSOES['s22']['title']

JUST_A = '«esta questão» (linha 13) e «na atualidade» (linha 18) fazem as duas coesão referencial, porque nenhuma se percebe só pelas palavras que tem.'
JUST_B = ('«esta questão» só se percebe indo atrás no texto: retoma a pergunta das linhas 11 e 12. «na atualidade» percebe-se sem ir a nenhuma outra expressão do texto: '
          'aponta para o tempo em que a autora escreve. A primeira retoma; a segunda situa.')

TOK_QUAL = [{'x': w} for w in 'imaginemo-nos a regressar ao cenário da vida selvagem,'.split()] + [{'x': '<b>na qual</b> um animal tem de dividir a sua atenção', 'fixo': True}]
assert [TOK_QUAL[i]['x'] for i in (4, 5, 6, 7)] == ['cenário', 'da', 'vida', 'selvagem,'] and len(TOK_QUAL) == 9
TOK_A = [{'x': w} for w in 'será que esta visão é correta e está a ser favorável para a própria sociedade que'.split()] + [{'x': '<b>a</b> criou?', 'fixo': True}]
assert [TOK_A[i]['x'] for i in (2, 3, 8, 12, 14, 15)] == ['esta', 'visão', 'a', 'a', 'sociedade', 'que'] and len(TOK_A) == 17
TOK_MODO = [{'x': w} for w in 'um animal tem de dividir a sua atenção por diversas atividades para que, enquanto come, não acabe por ser comido.'.split()]
assert [TOK_MODO[i]['x'] for i in (2, 4, 14, 15, 16, 17, 18, 19)] == ['tem', 'dividir', 'come,', 'não', 'acabe', 'por', 'ser', 'comido.'] and len(TOK_MODO) == 20

ANALISE = (
    '<div class="rolo" tabindex="0" role="region" aria-label="Análise das quatro opções"><table><thead><tr><th>Opção</th><th>Expressão</th><th>Para onde aponta</th><th>Conclusão</th></tr></thead><tbody>'
    '<tr><td>(D)</td><td>«estes» (linha 6); «os primeiros» (linha 31); «os segundos» (linhas 31 e 32)</td>'
    '<td>«estes» retoma «os desafios escolares» (linha 6), com que concorda no masculino plural. «os primeiros» e «os segundos» retomam, um de cada vez, os «dois tipos de mecanismos» da linha 30.</td>'
    '<td>As três vão buscar o sentido a uma expressão dita antes: as três retomam.</td></tr>'
    '<tr><td>(A)</td><td>«Hoje em dia» (linha 1); «um tipo de atenção» (linha 23); «no livro» (linha 29)</td>'
    '<td>«Hoje em dia» aponta para o tempo de quem escreve. «um tipo de atenção» e «no livro» apresentam o que ainda não tinha sido dito; o texto explica-o a seguir.</td>'
    '<td>Nenhuma vai buscar o sentido a uma expressão anterior.</td></tr>'
    '<tr><td>(B)</td><td>«dos alunos» (linha 5); «diante» (linha 17); «este tipo» (linha 19)</td>'
    '<td>«este tipo» retoma os mecanismos descritos nas linhas 14 a 18. «diante» diz um lugar em relação ao animal; quem retoma o animal é «si», em «diante de si». «dos alunos» dá outro nome a quem a linha 1 chamou «as crianças».</td>'
    '<td>«diante» não retoma nenhuma expressão: uma que falhe chega para afastar a opção.</td></tr>'
    '<tr><td>(C)</td><td>«atrás» (linha 18); «na obra <i>Sociedade do Cansaço</i>» (linha 21); «dois tipos» (linha 30)</td>'
    '<td>«atrás» diz um lugar em relação ao animal («atrás de si»). «na obra <i>Sociedade do Cansaço</i>» e «dois tipos» apresentam o que ainda não tinha sido dito; «dois tipos» é o antecedente de «os primeiros» e de «os segundos».</td>'
    '<td>Nenhuma vai buscar o sentido a uma expressão anterior.</td></tr>'
    '</tbody></table></div>')

AP = {'apoioRot': 'Linhas da prova'}

TREINO = {
    'id': 'coesao', 'viu': 'a chave oficial',
    'passos': [
        dict(AP, **{
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido', 'apoio': 'of',
            'o': 'Um item de gramática da 2.ª fase de 2026. Antes de escolheres uma opção, vê o que o enunciado manda procurar e quantas expressões traz cada opção.',
            'blocos': [
                {'t': 'html', 'h': OF5},
                {'t': 'escolha', 'id': 'p6-pedido', 'etq': 'treino', 'curto': 'O que tem de acontecer para uma opção estar certa',
                 'p': 'O que tem de acontecer para uma opção deste item estar certa?',
                 'o': [
                     {'t': 'Basta que uma das três expressões remeta para outra expressão do texto.',
                      'pista': '<p>Conta as expressões de cada opção e relê o fim do enunciado: «elementos textuais como». O item fala de uma expressão ou do conjunto que vem em cada opção?</p>'},
                     {'t': 'As três expressões têm de situar o texto no tempo ou no espaço.',
                      'pista': '<p>Relê o nome do mecanismo no enunciado. A palavra «referencial» fala de situar no tempo e no espaço, ou de referir o que o texto já disse?</p>'},
                     {'t': 'As três expressões têm de ir buscar o sentido a outra expressão do texto.', 'pista': ''},
                     {'t': 'As três expressões têm de pertencer ao mesmo campo lexical.',
                      'pista': '<p>Repetir ou variar o vocabulário é outro tipo de coesão. Relê o enunciado: diz «coesão gramatical referencial», não diz «coesão lexical».</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Lê o enunciado até «referencial». Depois faz a cada expressão a mesma pergunta: sei de que fala sem ir a outro sítio do texto? E vê quantas expressões de cada opção têm de passar nessa pergunta.</p>',
                 'f': '<p>Cada opção traz três expressões, e as três têm de servir: uma que falhe chega para afastar a opção. Há coesão referencial quando uma expressão vai buscar o sentido a outra, dita antes, a que se chama antecedente.</p>'
                      '<p>O <i>Dicionário Terminológico</i> chama anáfora a essa expressão: ' + DT_ANA + ' ' + (DT_REF % 'Anáfora') + '</p>'
                      '<p class="pag">Os critérios só dão a letra certa. Dizer o que o item quer com «coesão gramatical referencial» é leitura nossa, apoiada na definição.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'localizar', 'curto': 'Localizar', 'titulo': 'Localizar o que cada palavra retoma', 'apoio': 'tr',
            'o': 'Treinas noutras linhas do mesmo texto, para deixares o item oficial inteiro para o passo 5.',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p>Na frase «' + F_INES + '», «ela» tanto pode ser Inês como a mãe. Quando há dois antecedentes possíveis, é a concordância ou o sentido que decide. '
                 'Nas duas buscas que se seguem, decide uma vez a concordância e outra vez o sentido.</p>'
                 '<p class="pag">Frase de treino do aquecimento da sessão 22. Não é uma citação.</p></div>'},
                {'t': 'tocar', 'id': 'p6-qual', 'etq': 'treino', 'modo': 'palavras', 'curto': 'O que «na qual» retoma',
                 'p': 'Linhas 13 e 14. Toca na palavra (ou nas palavras) que a expressão a negro, «na qual», retoma. Depois toca em «Verificar».',
                 'tokens': TOK_QUAL, 'nucleos': [[6]], 'permitidos': [5, 6, 7], 'mostra': [6, 7],
                 'notas': {'5': 'Aceite com «da»: o grupo inteiro é «a vida selvagem», aqui com a preposição «de».',
                           '7': 'Aceite com «selvagem»: o nome é «vida»; o grupo inteiro é «a vida selvagem».'},
                 'pistas': [
                     {'se': [4], 'x': '<p>«na qual» está no feminino. Vê o género de «cenário» e procura, ali ao lado, um nome que concorde com «a qual».</p>'},
                     {'so': [5, 7], 'x': '<p>Estás no grupo certo, mas falta o nome: a palavra que diz onde é que um animal tem de dividir a atenção.</p>'},
                     {'se': [0, 1, 2, 3], 'x': '<p>Essas palavras dizem o que se imagina: um regresso. Pergunta: onde é que um animal tem de dividir a atenção? Procura um nome.</p>'},
                 ],
                 'falta': '<p>Pergunta: onde é que um animal tem de dividir a atenção? Procura um nome.</p>',
                 'pista2': '<p>Procura, antes da vírgula, um nome feminino no singular: só esse pode concordar com «a qual».</p>',
                 'f': '<p>«na qual» retoma «a vida selvagem». Aqui decide a concordância: «a qual» é feminino e «cenário» é masculino. A proximidade, por si, não chegava.</p>'
                      '<p>Os relativos também contam para a coesão referencial. Na 1.ª fase de 2026, a opção certa do item 5 do Grupo II dá como mecanismo de coesão gramatical referencial o uso dos vocábulos «cujos» e «onde» '
                      '<span class="pag">(' + lig('e1', 'enunciado, p. 12') + '; chave: Versão 2, (B), ' + lig('c1', 'critérios, p. 13') + ')</span>.</p>'},
                {'t': 'tocar', 'id': 'p6-a', 'etq': 'treino', 'modo': 'palavras', 'curto': 'O que o pronome «a» retoma',
                 'p': 'Linhas 11 e 12. Toca na palavra (ou nas palavras) que o pronome a negro, «a», retoma. Depois toca em «Verificar».',
                 'tokens': TOK_A, 'nucleos': [[3]], 'permitidos': [2, 3], 'mostra': [2, 3],
                 'notas': {'2': 'Aceite com «esta»: o grupo inteiro é «esta visão».'},
                 'pistas': [
                     {'so': [2], 'x': '<p>«esta» acompanha um nome. É esse nome que o pronome retoma: vem logo a seguir.</p>'},
                     {'se': [12, 13, 14], 'x': '<p>A sociedade é quem cria. O pronome é aquilo que foi criado. Pergunta: o que é que a sociedade criou?</p>'},
                     {'se': [8], 'x': '<p>Esse «a» faz parte de «está a ser». Procura um nome, mais atrás, que diga o que a sociedade criou.</p>'},
                     {'se': [15], 'x': '<p>Esse «que» retoma «sociedade». O pronome a negro é outro: diz aquilo que a sociedade criou.</p>'},
                     {'se': [0, 1, 4, 5, 6, 7, 9, 10, 11], 'x': '<p>Essas palavras não dizem o que foi criado. Pergunta: o que é que a sociedade criou? Procura um nome feminino no singular.</p>'},
                 ],
                 'falta': '<p>Pergunta: o que é que a sociedade criou? Procura um nome feminino no singular.</p>',
                 'pista2': '<p>Faz a pergunta «a sociedade criou o quê?» e procura a resposta antes de «é correta».</p>',
                 'f': '<p>«a» retoma «esta visão». Aqui o género não chega, porque «sociedade» também é um nome feminino no singular: decide o sentido. A sociedade é quem cria; a visão é o que foi criado.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'distinguir', 'curto': 'Retomar ou situar', 'titulo': 'Distinguir uma justificação insuficiente de uma adequada', 'apoio': 'tr',
            'o': 'Duas justificações sobre duas expressões das linhas 13 e 18. Uma trata as duas da mesma maneira.',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p><b>Justificação A.</b> ' + JUST_A + '</p><p><b>Justificação B.</b> ' + JUST_B + '</p></div>'},
                {'t': 'escolha', 'id': 'p6-teste', 'etq': 'treino', 'curto': 'O teste que separa retomar de situar',
                 'p': 'A Justificação A junta dois casos diferentes. Que teste usa a Justificação B para os separar?',
                 'o': [
                     {'t': 'Ver se a expressão começa por um demonstrativo, como «este» ou «esta».',
                      'pista': '<p>Relê a Justificação B: fala da forma da expressão ou do sítio onde se vai buscar o sentido? Lembra-te do pronome «a» da linha 12: retoma «esta visão» e não é um demonstrativo.</p>'},
                     {'t': 'Ver onde se vai buscar o sentido: a outra expressão do texto ou ao momento de quem escreve.', 'pista': ''},
                     {'t': 'Ver se a expressão se pode retirar sem a frase ficar mal formada.',
                      'pista': '<p>Experimenta retirar cada uma das duas expressões. O resultado é diferente nos dois casos? Um teste que dá o mesmo resultado não os separa.</p>'},
                     {'t': 'Ver se a expressão indica um tempo ou indica um lugar.',
                      'pista': '<p>«na atualidade» indica um tempo. E «esta questão»? O teste da Justificação B aplica-se às duas expressões: procura o gesto que ela repete.</p>'},
                 ], 'c': 1,
                 'pista2': '<p>A Justificação B faz duas vezes o mesmo gesto: procura no texto a expressão de que a outra depende. Num caso encontra-a, no outro não.</p>',
                 'f': '<p>O teste é perguntar onde se vai buscar o sentido. Se é a uma expressão dita antes, a expressão <b>retoma</b>: é uma anáfora. Se é ao momento, ao lugar ou à pessoa de quem escreve, a expressão <b>situa</b>: é um caso de deixis.</p>'
                      '<p>O <i>Dicionário Terminológico</i> diz que a referência de uma expressão pode ser ' + DT_REFV + ' ' + (DT_REF % 'Referência') + '. '
                      'Sobre a deixis, lembra que ' + DT_DEI + ' e conta entre as palavras com este valor ' + DT_DEI_ADJ + ' ' + (DT_REF % 'Deixis') + '.</p>'
                      '<p>A forma é só um sinal. Um demonstrativo tanto pode retomar («esta questão») como apontar para fora do texto; e um pronome pessoal retoma sem demonstrativo nenhum.</p>'
                      '<p class="pag">«Retomar» e «situar» são palavras nossas para anáfora e deixis. A mesma entrada fala ainda da deixis textual (' + DT_DEI_TXT + '), que este treino não trabalha.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'situar', 'curto': 'Ligar e situar', 'titulo': 'Ligar e situar: o conector, o modo do verbo e a modalidade', 'apoio': 'mod',
            'o': 'O mesmo conector, o mesmo verbo ou o mesmo tempo podem ter valores diferentes. Decide sempre no contexto.',
            'blocos': [
                {'t': 'escolha', 'id': 'p6-ligar', 'etq': 'treino', 'curto': 'O conector que pode ficar no lugar de «pois»',
                 'p': 'Linha 17: «pois tem de estar permanentemente alerta». Que conector pode ficar no lugar de «pois» sem mudar a relação entre as duas ideias?',
                 'o': [
                     {'t': 'portanto', 'pista': '<p>Vê qual das duas ideias é a razão da outra. Depois lê as linhas 16 e 17 com «portanto» e vê se a razão continua do mesmo lado.</p>'},
                     {'t': 'embora', 'pista': '<p>Estar sempre alerta é um obstáculo que não chega para impedir a concentração, ou é aquilo que a impede?</p>'},
                     {'t': 'porque', 'pista': ''},
                     {'t': 'contudo', 'pista': '<p>As duas ideias opõem-se, ou uma explica a outra? Lê as linhas 16 e 17 e pergunta «porquê?» depois de «diante de si».</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Lê as linhas 16 e 17 e pergunta «porquê?» depois de «diante de si». O que vem a seguir a «pois» responde a essa pergunta: procura o conector que introduz uma razão.</p>',
                 'f': '<p>Aqui, «pois» introduz a razão: o animal não se concentra no que tem à frente porque tem de estar alerta. «porque» mantém essa relação. Os outros três mudam-na: «portanto» faria da razão uma consequência, e «embora» e «contudo» fariam dela um contraste.</p>'
                      '<p>Conhecer o valor de um conector serve para ler e para escolher bem. Não te obriga a usá-los: nas respostas restritas, os critérios dizem que «' + R_CONECT + '» <span class="pag">(critérios gerais, p. 2)</span>.</p>'
                      '<p class="pag">Frase da prova; a pergunta é nossa. O valor de «pois» nesta linha é leitura nossa.</p>'},
                {'t': 'tocar', 'id': 'p6-modo', 'etq': 'treino', 'modo': 'palavras', 'curto': 'A forma verbal no presente do conjuntivo',
                 'p': 'Linhas 14 e 15. Toca na forma verbal que está no presente do conjuntivo. Depois toca em «Verificar».',
                 'tokens': TOK_MODO, 'nucleos': [[16]], 'permitidos': [15, 16, 17, 18, 19], 'mostra': [16],
                 'notas': {'15': 'Aceite com «não»: a forma verbal é só «acabe».',
                           '17': 'Aceite com «por ser comido»: as palavras leem-se juntas, mas a forma que está no conjuntivo é só «acabe».',
                           '18': 'Aceite com «por ser comido»: as palavras leem-se juntas, mas a forma que está no conjuntivo é só «acabe».',
                           '19': 'Aceite com «por ser comido»: as palavras leem-se juntas, mas a forma que está no conjuntivo é só «acabe».'},
                 'pistas': [
                     {'so': [15, 17, 18, 19], 'x': '<p>Essas palavras acompanham a forma que procuras, mas nenhuma delas está no conjuntivo. Falta a forma verbal que depende de «para que».</p>'},
                     {'se': [2, 14], 'x': '<p>«tem» e «come» estão no presente do indicativo: dão a ação como um facto. Procura a forma que depende de «para que».</p>'},
                     {'se': [4], 'x': '<p>«dividir» está no infinitivo. Procura uma forma com pessoa e tempo, que dependa de «para que».</p>'},
                     {'se': [0, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13], 'x': '<p>Essas palavras não são formas verbais. Procura o verbo que depende de «para que».</p>'},
                 ],
                 'falta': '<p>Procura o verbo que depende de «para que».</p>',
                 'pista2': '<p>«para que» introduz uma finalidade: aquilo que se quer conseguir ou, aqui, evitar. O verbo que depende dele não dá a ação como um facto. Procura-o depois de «enquanto come».</p>',
                 'f': '<p>«acabe»: presente do conjuntivo do verbo «acabar», pedido por «para que», que introduz uma finalidade. O indicativo («tem», «come») dá a ação como um facto; o conjuntivo dá-a como algo que se quer evitar.</p>'
                      '<p>A prova conta que reconheças o tempo e o modo: no item 5 do Grupo II da 1.ª fase, duas das opções falam de «o predomínio de verbos no presente do indicativo» <span class="pag">(' + lig('e1', 'enunciado, p. 12') + ')</span>.</p>'},
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p><b>Primeira frase.</b> ' + F_TALVEZ + '.</p><p><b>Segunda frase.</b> ' + F_TEMDE + '</p>'
                 '<p class="pag">A primeira é uma frase de treino do aquecimento da sessão 22; a segunda é nova. Não são citações.</p></div>'},
                {'t': 'escolha', 'id': 'p6-modal', 'etq': 'treino', 'curto': 'Os valores de «talvez» e de «tem de»',
                 'p': 'Que valores exprimem a primeira e a segunda frase, por esta ordem?',
                 'o': [
                     {'t': 'probabilidade (modalidade epistémica) e permissão (modalidade deôntica)',
                      'pista': '<p>A primeira metade serve. Na segunda frase, alguém dá licença à personagem, ou diz-se o que ela é obrigada a fazer para ser perdoada? Troca «tem de» por «é obrigatório que» e por «é permitido que».</p>'},
                     {'t': 'probabilidade (modalidade epistémica) e obrigação (modalidade deôntica)', 'pista': ''},
                     {'t': 'certeza (modalidade epistémica) e obrigação (modalidade deôntica)',
                      'pista': '<p>A segunda metade serve. Na primeira frase, troca «talvez» por «é certo que» e por «é provável que». Qual das duas mantém o sentido?</p>'},
                     {'t': 'permissão (modalidade deôntica) e certeza (modalidade epistémica)',
                      'pista': '<p>Nenhuma das metades serve. Troca «talvez» por «é provável que» e «tem de» por «é obrigatório que», e vê se o sentido se mantém.</p>'},
                 ], 'c': 1,
                 'pista2': '<p>Tens quatro paráfrases: «é provável que», «é certo que», «é obrigatório que», «é permitido que». Experimenta-as em cada frase e fica com a que mantém o sentido.</p>',
                 'f': '<p>«Talvez» apresenta o reconhecimento do erro como provável, sem o dar por certo: valor de probabilidade. «tem de» diz o que a personagem é obrigada a fazer para ser perdoada: valor de obrigação.</p>'
                      '<p>O <i>Dicionário Terminológico</i> define assim: ' + DT_MODAL + ' Dá como exemplo do segundo caso ' + DT_EX_EPI + ' e do terceiro ' + DT_EX_DEO + ' ' + (DT_REF % 'Modalidade') + '</p>'},
                {'t': 'html', 'h': '<p>Agora o item 6 da mesma prova, sobre duas expressões das linhas 17 e 45.</p>' + OF6},
                {'t': 'escolha', 'id': 'p6-item6', 'etq': 'oficial', 'curto': 'Item oficial da 2.ª fase: a modalidade de duas expressões',
                 'p': 'Que opção assinalas neste item da 2.ª fase?',
                 'o': [
                     {'t': md(I6['opcoes'][0]['texto']),
                      'pista': '<p>O primeiro caso serve. No segundo, vai à linha 44 e vê de que fala a frase. Alguém dá licença para haver erros, ou diz-se o que pode vir a acontecer?</p>'},
                     {'t': md(I6['opcoes'][1]['texto']),
                      'pista': '<p>O segundo caso serve. No primeiro, vê nas linhas 15 a 17 o que acontece ao animal se não estiver alerta. A frase dá uma certeza de quem escreve, ou diz o que o animal é forçado a fazer?</p>'},
                     {'t': md(I6['opcoes'][2]['texto']), 'pista': ''},
                     {'t': md(I6['opcoes'][3]['texto']),
                      'pista': '<p>Experimenta as paráfrases nos dois casos: «é obrigatório que» e «é certo que», na linha 17; «é provável que» e «é permitido que», na linha 45.</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Troca cada expressão pelas quatro paráfrases («é obrigatório que», «é permitido que», «é certo que», «é provável que») e vê qual mantém o sentido, primeiro na linha 17 e depois na linha 45.</p>',
                 'f': '<p>Chave oficial: Versão 2, (C); 13 pontos (critérios da 2.ª fase, p. 13; ' + lig('c2', 'PDF em eduqa.pt') + ').</p>'
                      '<p>A chave só dá a letra; o porquê é leitura nossa. Na linha 17, o animal é forçado a estar alerta, para não acabar comido (linha 15): obrigação. Na linha 45, a frase vem depois de «Mas esta revolução tem os seus riscos» (linha 44): diz o que é provável que aconteça, não dá licença a ninguém.</p>'
                      '<p>A forma não decide. Na linha 13, «podemos fazer o seguinte exercício» tem o mesmo verbo «poder» e lê-se como permissão: quem escreve propõe um exercício que nos é permitido fazer (leitura nossa, a mesma das provas em cartões). Só o contexto diz que valor tem o verbo.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'responder', 'curto': 'A tua resposta', 'titulo': 'Responder ao item oficial, sem pistas', 'apoio': 'of',
            'o': 'Agora és tu. Tens as linhas da prova ao lado e mais nada.',
            'blocos': [
                {'t': 'html', 'h': OF5 + '<div class="caixa ad">' + etq('adaptado') + '<p class="enun">Assinala a opção e justifica a tua escolha em três ou quatro frases: diz o que retoma cada uma das três expressões da opção que escolheste '
                 'e mostra, numa das outras opções, uma expressão que não retoma nada.</p>'
                 '<p class="pag">O que mudou em relação ao item oficial: o enunciado, as opções e as linhas são os da prova; acrescentámos a justificação escrita. Na prova só assinalas a letra.</p></div>'},
                {'t': 'escrever', 'id': 'p6-resposta', 'curto': 'Resposta ao item 5 da 2.ª fase, com justificação escrita',
                 'opcoes': OPS5, 'opRotulo': 'A opção que assinalas',
                 'rotulo': 'A tua justificação', 'linhas': 7,
                 'ajuda': 'Para cada expressão: a linha e a expressão que ela retoma. Escreve aqui ou no papel.'},
            ],
        }),
        dict(AP, **{
            'id': 'comparar', 'curto': 'Comparar', 'titulo': 'Comparar com a chave oficial e com uma análise comentada', 'apoio': 'of', 'precisa': 'p6-resposta',
            'o': 'A chave é oficial. A análise das quatro opções é nossa.',
            'blocos': [
                {'t': 'ver1', 'de': 'p6-resposta', 'opcoes': OPS5, 'linhas': 7},
                {'t': 'html', 'h': '<div class="caixa of">' + etq('oficial') + '<p><b>Chave do item 5:</b> Versão 1, (C); Versão 2, <b>(D)</b>. Pontuação: 13. <span class="pag">(critérios da 2.ª fase, p. 13: quadro do Grupo II; ' + lig('c2', 'PDF em eduqa.pt') + ')</span></p>'
                 '<p>Os critérios do Grupo II só trazem este quadro: a letra certa e os pontos. Sobre os itens de seleção classificados de forma dicotómica, os critérios gerais dizem: «' + R_DICO + '» <span class="pag">(p. 1)</span>.</p>'
                 '<p>O item 5 é um dos cinco itens de que só contam os três melhores: «' + OPC + '» <span class="pag">(enunciado, p. 8; critérios, p. 16)</span>.</p></div>'
                 '<h3>Análise comentada das quatro opções</h3><p class="ajuda">Feita por nós. Os critérios só dizem que (D) é a opção certa; o que cada expressão faz no texto é leitura nossa.</p>' + ANALISE +
                 '<p>Sobre «dos alunos» (linha 5): é um nome diferente para as mesmas pessoas. As provas em cartões leem esta troca como coesão lexical; a chave não se pronuncia sobre a expressão, e a opção (B) já fica afastada por «diante».</p>'},
                {'t': 'lista', 'id': 'p6-conf', 'titulo': 'Confere a tua primeira versão',
                 'intro': '<p class="ajuda">Marca o que já está na tua resposta. O que ficar por marcar é o que vais rever no passo seguinte.</p>',
                 'itens': [
                     'Assinalei a opção (D).',
                     'Disse o que «estes» retoma, com a linha.',
                     'Disse o que «os primeiros» e «os segundos» retomam, com a linha.',
                     'Mostrei, numa das outras opções, uma expressão que não retoma nada e disse o que ela faz: situa ou apresenta.',
                     'Usei os termos da gramática: coesão referencial, retomar, antecedente.',
                     'Copiei as expressões do texto entre aspas, letra a letra.',
                 ]},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). Uma pergunta para cada operação, e o limite de cada uma.</p>'
                 '<ul class="top"><li><b>Retomar.</b> De que expressão dita antes depende o sentido? Limite: a mais próxima nem sempre é o antecedente; decide a concordância ou o sentido.</li>'
                 '<li><b>Situar.</b> O sentido depende do momento, do lugar ou da pessoa de quem escreve? Limite: a forma não decide; um demonstrativo tanto retoma como situa.</li>'
                 '<li><b>Ligar.</b> Que relação há entre as duas ideias, e que conector a mantém? Limite: o mesmo conector pode ter mais de um valor; lê as duas ideias antes de decidir.</li>'
                 '<li><b>Modalidade.</b> Que paráfrase mantém o sentido: «é provável que», «é certo que», «é obrigatório que» ou «é permitido que»? Limite: o mesmo verbo («poder», «dever») pode ter valores diferentes; decide o contexto.</li></ul></div>'
                 '<p class="pag"><b>Termos conferidos.</b> «Coesão gramatical referencial», «modalidade deôntica» e «modalidade epistémica», com os valores de obrigação, permissão, certeza e probabilidade, são os termos dos próprios itens (enunciado, pp. 7 e 8). '
                 '«Anáfora», «antecedente» e «deixis» são os do <i>Dicionário Terminológico</i>, que conta entre os mecanismos de coesão textual ' + DT_COE + ' ' + (DT_REF % 'Coesão textual') + '. '
                 'Nas citações do dicionário fica a grafia do original.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'rever', 'curto': 'Rever', 'titulo': 'Rever a tua justificação', 'apoio': 'of', 'precisa': 'p6-resposta',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres a chave oficial, a página diz isso junto dela. Escreve a versão revista: para cada expressão, a linha e o antecedente.',
            'blocos': [
                {'t': 'rever', 'de': 'p6-resposta', 'curto': 'Versão revista da justificação', 'linhas': 7, 'opcoes': OPS5},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa of">' + etq('oficial') + '<p><b>Leva isto para a tua escrita.</b> No Grupo III, o nível mais alto do parâmetro C (Organização e Coesão Textuais, 10 pontos) pede, entre outros aspetos, um texto que: '
                 '«' + C_LIGAR + '»; «' + C_RETOMAR + '»; «' + C_SITUAR + '» <span class="pag">(critérios, p. 15, nas duas fases)</span>.</p>'
                 '<p>Nas respostas restritas, «' + R_COES + '» <span class="pag">(critérios gerais, p. 2)</span>.</p></div>'
                 '<div class="caixa nossa"><p>Ligar, retomar e situar: é a nossa maneira de ler estes três aspetos, pela ordem em que os critérios os dão, e é o título da sessão 22. '
                 'Relê um parágrafo teu e faz-lhe as perguntas do passo 6: cada pronome tem um só antecedente possível? Cada conector diz a relação que querias? Os tempos verbais situam tudo no mesmo momento?</p></div>'
                 '<div class="caixa nossa"><p><b>Na outra prova.</b> Na 1.ª fase de 2026, os itens 5 e 6 do Grupo II pedem operações vizinhas: o item 5, a coesão lexical e a coesão gramatical referencial; o item 6, os valores de «como» '
                 '(' + lig('e1', 'enunciado, p. 12') + '). Este treino não os trabalha. Estão, com os da 2.ª fase, nas provas em cartões: <a href="../../provas/2026-1f/grupo-ii/">1.ª fase, Grupo II</a> e <a href="../../provas/2026-2f/grupo-ii/">2.ª fase, Grupo II</a>.</p></div>'
                 '<div class="caixa nossa"><p><b>Sobre 2027.</b> Os itens são de 2026. Que conteúdos de gramática podem sair em 2027, e em que tipo de item, está a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        }),
    ],
}

CAB = (
    sobre('coesao', 'Gramática do texto') +
    '<h1>O que retoma, o que situa, o que liga</h1>'
    '<p class="lede">Dois itens de gramática da prova de 2026 (2.ª fase), sete passos e uma justificação escrita por ti. Liga-se à ' + sessao('s22', 'Gramática: ligar, retomar e situar') + ' e ao seu ' + aquecimento('s22') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Dizer, no contexto, para onde aponta uma expressão (se retoma ou se situa), que relação um conector estabelece e que valor modal tem um verbo, e justificar com um teste.</dd></div>'
    '<div><dt>Itens oficiais a que se liga</dt><dd>Prova 639, 2026, 2.ª fase, Grupo II, item 5 (coesão gramatical referencial; 13 pontos): ' + lig('e2', 'enunciado, p. 7') + ', ' + lig('c2', 'critérios, p. 13') + '. '
    'Item 6 (modalidade; 13 pontos): enunciado, p. 8; critérios, p. 13. Os dois estão entre os cinco itens de que só contam os três melhores (enunciado, p. 8). '
    'Na 1.ª fase, os itens 5 e 6 do Grupo II pedem operações vizinhas (' + lig('e1', 'enunciado, p. 12') + '; ' + lig('c1', 'critérios, p. 13') + ') e não são trabalhados aqui. PDF em eduqa.pt.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<p class="pag">Os dois itens oficiais aparecem inteiros nos passos 1, 4 e 5 (enunciado, quatro opções e cotação). As chaves oficiais aparecem depois de responderes, com a página dos critérios. '
    'Os critérios do Grupo II só dão a letra certa: as explicações são nossas e vêm ditas como tal.</p>'
)

NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB + ''.join(LINHAS_HTML)
for _s in [OF5, OF6] + LINHAS_HTML + [c for c, _ in DT_CITA] + [md(o['texto']) for o in I5['opcoes'] + I6['opcoes']] + [OPC, R_DICO, R_CONECT, R_COES, C_LIGAR, C_RETOMAR, C_SITUAR]:
    NOSSO = NOSSO.replace(json.dumps(_s, ensure_ascii=False)[1:-1], '').replace(_s, '')


def construir():
    lint('coesao', NOSSO)
    return pagina_treino('coesao', 'coesao/', 'Coesão e modalidade', 'Treino 6: o que retoma, o que situa, o que liga | Português',
                         'Treino da preparação de exame de Português: coesão referencial, conectores, modo verbal e modalidade no contexto, com dois itens oficiais de 2026 e uma justificação escrita por ti.',
                         CAB, {'of': AP_OF, 'tr': AP_TR, 'mod': AP_MOD}, TREINO)
