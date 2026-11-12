from .base import *

# ---------- o poema (texto do banco docs/pedagogia/exame-aquecimentos/s14.json) ----------
banco = json.load(open(ROOT + '/docs/pedagogia/exame-aquecimentos/s14.json', encoding='utf-8'))
VERSOS = [html.unescape(v) for v in re.findall(r'<span class="ln" data-l="[^"]+">(.*?)</span>', banco['cartoes'][1]['html'])]
assert len(VERSOS) == 12, VERSOS
ESPERADO = ["As rosas amo dos jardins de Adónis,", "Essas volucres amo, Lídia, rosas,", "Que em o dia em que nascem,", "Em esse dia morrem.",
            "A luz para elas é eterna, porque", "Nascem nascido já o Sol, e acabam", "Antes que Apolo deixe", "O seu curso visível.",
            "Assim façamos nossa vida um dia,", "Inscientes, Lídia, voluntariamente", "Que há noite antes e após", "O pouco que duramos."]
assert VERSOS == ESPERADO


def cita_ok(texto):
    """Confere que cada citação «…» com (v. n) ou (vv. n-m) existe no poema."""
    junto = ' / '.join(VERSOS)
    for m in re.finditer(r'«([^«»]+)»\s*\((vv?\.) (\d+)(?:-(\d+))?\)', texto):
        c = m.group(1)
        a = int(m.group(3)); b = int(m.group(4) or a)
        tre = ' / '.join(VERSOS[a - 1:b])
        c0 = c[0].upper() + c[1:]
        ok = (c in tre) or (c0 in tre) or (c.lower() in tre.lower())
        assert ok, ('citação não conferida', c, tre)


poema = '<ol class="poema">' + ''.join(
    '<li%s><span class="n">%d</span><span>%s</span></li>' % (' class="e"' if i in (4, 8) else '', i + 1, esc(v)) for i, v in enumerate(VERSOS)) + '</ol>'

APOIO_POEMA = (
    '<p class="texto-t">«As rosas amo dos jardins de Adónis»</p>'
    '<p class="texto-a">Fernando Pessoa, ode assinada pelo heterónimo Ricardo Reis. Quem fala no poema é o sujeito poético, que se dirige a Lídia.</p>'
    + poema +
    '<p class="notas-t">Notas nossas (não são de nenhuma prova)</p>'
    '<ul class="notas"><li><b>jardins de Adónis</b> (v. 1): na Grécia antiga, vasos de plantas que cresciam depressa e murchavam em poucos dias, preparados para as festas de Adónis.</li>'
    '<li><b>volucres</b> (v. 2): passageiras, que duram pouco.</li>'
    '<li><b>Apolo</b> (v. 7): aqui, o Sol; «o seu curso visível» é o caminho do Sol durante o dia.</li>'
    '<li><b>Inscientes</b> (v. 10): que não sabem.</li></ul>'
    '<p class="fonte">Ricardo Reis, «As rosas amo dos jardins de Adónis» (11-7-1914); 1.ª publicação na <i>Athena</i>, n.º 1, Lisboa, outubro de 1924; <i>Odes de Ricardo Reis</i>, Ática, 1946; Arquivo Pessoa. Texto conferido com o banco do aquecimento s14 e com a lição de origem (M7-F23). O poema não saiu nas provas de 2026.</p>'
)

# ---------- item oficial: 1.ª fase, Grupo I, Parte B, item 5 ----------
PB = F1['grupos'][0]['partes'][1]
IT = PB['itens'][1]
assert IT['numero'] == 'I.5' and IT['cotacao'] == 13
tx = PB['textos'][0]
est = ''
for e_i, e in enumerate(tx['estrofes']):
    for v_i, v in enumerate(e):
        est += '<li%s><span class="n">%s</span><span>%s</span></li>' % (
            ' class="e"' if (v_i == 0 and e_i > 0) else '', v['v'] if v['v'] % 5 == 0 else '', md(v['t']))
notas = ''.join('<li value="%d">%s</li>' % (n['n'], md(n['texto'])) for n in PB['notas'])
cr = IT['criterios']
top = ''
for t in cr['topicos']:
    top += '<li>%s<ul class="top">%s</ul></li>' % (md(t['rotulo']), ''.join('<li>%s</li>' % md(p) for p in t['pontos']))
ced, cl = cr['parametros']
assert ced['pontos'] == 10 and cl['pontos'] == 3

OFICIAL = (
    '<p>' + etq('oficial') + '</p>'
    '<p class="pag">Exame Final Nacional de Português, Prova 639, 2026, 1.ª fase, versão 2. Grupo I, Parte B, item 5. '
    'Texto: enunciado, p. 6; item: enunciado, p. 7; critério: critérios de classificação, pp. 10-11 (definitivos, atualizados a 10/07/2026). '
    + lig('e1', 'Enunciado (PDF, eduqa.pt)') + ' e ' + lig('c1', 'critérios (PDF, eduqa.pt)') + '.</p>'
    '<h3>Parte B</h3><p class="instr"><span class="pag">Instrução da prova:</span> ' + md(PB['instrucao']) + '</p>'
    '<ol class="poema">' + est + '</ol>'
    '<p class="fonte">' + md(tx['fonte']) + '</p>'
    '<p class="notas-t">Notas (da prova)</p><ol class="notas">' + notas + '</ol>'
    '<p class="pag">Na prova, só os versos 5, 10, 15 e 20 trazem o número à margem.</p>'
    '<h3>Item 5 (13 pontos; conta sempre para a classificação)</h3>'
    '<p class="enun"><b>5.</b> ' + md(IT['enunciado'][0]) + '</p>'
    '<h3>Critério específico (critérios, pp. 10-11)</h3>'
    '<p>' + md(cr['instrucao']) + '</p><ul class="top">' + top + '</ul>'
    '<p class="pag">Regra de leitura dos tópicos (critérios, p. 4): «Nos tópicos de resposta de cada item, as expressões separadas por barras oblíquas ‒ à exceção das utilizadas no interior de cada uma das transcrições ‒ correspondem a exemplos de formulações possíveis, apresentadas em alternativa. As ideias apresentadas entre parênteses não têm de ser obrigatoriamente mobilizadas para que as respostas sejam consideradas adequadas.»</p>'
    '<h3>' + ced['nome'] + ' (C-ED): ' + str(ced['pontos']) + ' pontos</h3>'
    + tabela_niveis(ced['niveis'], 'Níveis de desempenho do parâmetro C-ED, item 5') +
    '<p class="pag">' + md(ced['nota_de_rodape']) + '</p>'
    '<h3>' + cl['nome'] + ' (CL): ' + str(cl['pontos']) + ' pontos</h3>'
    '<p>' + md(cl['texto']) + '</p>' + tabela_cl('CL_3') +
    '<p class="pag">' + md(cl['nota_de_rodape']) + '</p>'
)

REGRA_P2 = '«As respostas que não apresentem exatamente os termos ou interpretações constantes nos critérios específicos são classificadas em igualdade de circunstâncias com aquelas que os apresentem, desde que o seu conteúdo seja cientificamente válido, adequado ao solicitado e enquadrado pelos documentos curriculares de referência.»'
# conferir com a transcrição
_g = json.dumps(F1['criterios']['gerais'], ensure_ascii=False)
assert REGRA_P2.strip('«»') in _g
assert 'exceto quando tal é expressamente requerido no item, as respostas não têm de apresentar um parágrafo introdutório nem um parágrafo conclusivo' in _g
assert 'sem recurso obrigatório a conectores interfrásicos' in _g
assert 'incumprimento das regras de citação de texto ou de referência a título de uma obra' in _g

PEDIDO = ('Explicita a relação entre a imagem das rosas (versos 1 a 8) e a proposta de vida que o sujeito poético faz a Lídia (versos 9 a 12). '
          'Fundamenta a tua resposta com dois elementos textuais, um de cada parte do poema.')
CX_PEDIDO = '<div class="caixa tr">' + etq('treino') + '<p class="enun">' + PEDIDO + '</p></div>'

RESP_A = 'As rosas dos jardins de Adónis são passageiras: «em o dia em que nascem, / Em esse dia morrem» (vv. 3-4). Com esta imagem, o sujeito poético mostra que a vida é breve.'
RESP_B = ('As rosas vivem um só dia (vv. 3-4), mas o sujeito poético não as lamenta: diz duas vezes que as ama (vv. 1-2). A razão está na segunda estrofe: como acabam '
          '«Antes que Apolo deixe / O seu curso visível» (vv. 7-8), nunca veem a noite, e por isso «A luz para elas é eterna» (v. 5). '
          'A imagem mostra uma vida breve que se vive inteira na luz, sem conhecer o fim.')
EX = [
    ('As rosas dos jardins de Adónis vivem um só dia: «em o dia em que nascem, / Em esse dia morrem» (vv. 3-4).',
     'Começa pela imagem e prova-a logo. Não tem parágrafo de introdução: este item não o pede e, sem pedido expresso, os critérios não o exigem (p. 2).'),
    ('Como acabam «Antes que Apolo deixe / O seu curso visível» (vv. 7-8), nunca veem a noite, e por isso, para elas, a luz «é eterna» (v. 5).',
     'Explica o que a imagem mostra, com a razão que o próprio poema dá («porque», v. 5). É o passo que faltava à Resposta A.'),
    ('É esta maneira de viver que o sujeito poético propõe a Lídia: «Assim façamos nossa vida um dia» (v. 9).',
     'Faz a ligação. «Assim» é a palavra do poema que une as duas partes: a resposta diz o que se imita.'),
    ('Há, porém, uma diferença. As rosas não sabem da noite; o sujeito poético e Lídia sabem que «há noite antes e após / O pouco que duramos» (vv. 11-12) e terão de a ignorar por escolha, «voluntariamente» (v. 10). O que nas rosas é natureza, neles é uma decisão.',
     'Diz até onde vai a comparação, com a palavra que tocaste no passo 2. Não atribui ao poema medo nem desespero: os versos não o dizem.'),
]
for t in [RESP_A, RESP_B] + [a for a, _ in EX]:
    cita_ok(t)
assert '«é eterna»' in EX[1][0] and 'é eterna' in VERSOS[4]

exemplo = ''.join('<div class="anot"><p class="c">%s</p><p class="n">%s</p></div>' % (a, b) for a, b in EX)

TOK2 = [
    {'x': 'v. 10', 'fixo': True}, {'x': 'Inscientes,'}, {'x': 'Lídia,'}, {'x': 'voluntariamente'}, {'nl': True},
    {'x': 'v. 11', 'fixo': True}, {'x': 'Que'}, {'x': 'há'}, {'x': 'noite'}, {'x': 'antes'}, {'x': 'e'}, {'x': 'após'}, {'nl': True},
    {'x': 'v. 12', 'fixo': True}, {'x': 'O'}, {'x': 'pouco'}, {'x': 'que'}, {'x': 'duramos.'},
]
assert ' '.join(t['x'] for t in TOK2[1:4]) == VERSOS[9] and ' '.join(t['x'] for t in TOK2[6:12]) == VERSOS[10] and ' '.join(t['x'] for t in TOK2[14:18]) == VERSOS[11]

TREINO = {
    'id': 'interpretacao', 'viu': 'os critérios',
    'passos': [
        {
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido', 'apoio': 'poema',
            'o': 'Antes de leres o poema à procura de respostas, lê o que te pedem: quantas coisas e com que condições.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO +
                 '<p>Este pedido foi escrito por nós, à maneira do item 5 da 1.ª fase de 2026, que diz assim:</p>'
                 '<div class="caixa of">' + etq('oficial') + '<p class="enun">' + md(IT['enunciado'][0]) + '</p>'
                 '<p class="pag">Prova 639, 2026, 1.ª fase, Grupo I, Parte B, item 5 (13 pontos). Enunciado, p. 7. O item completo, com o texto e o critério, está no cimo desta página.</p></div>'
                 '<p>Nos dois casos há dois verbos de instrução: um manda dizer («Explicite», «Explicita»), o outro manda provar («Fundamente», «Fundamenta»).</p>'},
                {'t': 'escolha', 'id': 'p1-pedido', 'etq': 'treino', 'curto': 'O que o pedido de treino manda fazer',
                 'p': 'O que tem de aparecer na tua resposta para o pedido de treino ficar cumprido?',
                 'o': [
                     {'t': 'O nome do recurso expressivo usado nos versos 1 a 8 e o nome da filosofia de Ricardo Reis.',
                      'pista': '<p>Relê os dois verbos do pedido de treino: «Explicita» e «Fundamenta». Vê se algum deles manda dar um nome.</p>'},
                     {'t': 'Um resumo do poema, estrofe a estrofe, por palavras tuas.',
                      'pista': '<p>Procura no pedido a palavra que une as duas partes do poema. Um resumo diz o que está em cada estrofe. Diz de que maneira uma se liga à outra?</p>'},
                     {'t': 'A relação entre a imagem das rosas e a proposta de vida, com um elemento textual dos versos 1 a 8 e outro dos versos 9 a 12.',
                      'pista': ''},
                     {'t': 'A tua opinião sobre a proposta de vida, com exemplos da tua experiência.',
                      'pista': '<p>Vê em que é que o pedido manda apoiar a resposta: procura a expressão que vem depois de «Fundamenta a tua resposta com».</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Lê o pedido de treino aos bocados. Primeiro, o nome que vem logo depois de «Explicita a». Depois, o que vem a seguir a «Fundamenta a tua resposta com», até ao ponto final. A opção adequada traz essas duas partes e mais nada.</p>',
                 'f': '<p>O pedido tem duas tarefas e uma condição. Tarefa 1: explicitar uma <b>relação</b> (o que une a imagem das rosas à proposta de vida). Tarefa 2: <b>fundamentar</b>. Condição: dois elementos textuais, um de cada parte do poema.</p>'
                      '<p>O item oficial funciona da mesma maneira: pede <b>dois</b> sentimentos e, para <b>cada um</b>, um recurso expressivo ilustrado com um elemento textual. Quem conta primeiro o que lhe pedem sabe quando a resposta está completa.</p>'},
            ],
        },
        {
            'id': 'localizar', 'curto': 'Localizar', 'titulo': 'Localizar no poema', 'apoio': 'poema',
            'o': 'Duas buscas no texto: os versos que fazem a imagem e a palavra que decide o sentido da proposta.',
            'blocos': [
                {'t': 'tocar', 'id': 'p1-versos', 'etq': 'treino', 'modo': 'versos', 'curto': 'Os versos que dizem que as rosas nascem e morrem no mesmo dia',
                 'p': 'Nas duas primeiras estrofes (versos 1 a 8), toca nos versos que dizem que as rosas nascem e morrem no mesmo dia. Toca só nos versos de que precisas e depois em «Verificar».',
                 'tokens': [{'x': esc(v), 'n': i + 1} for i, v in enumerate(VERSOS[:8])],
                 'nucleos': [[2, 3], [5, 6, 7]], 'permitidos': [2, 3, 4, 5, 6, 7], 'mostra': [2, 3],
                 'notas': {'4': 'O verso 5 também é aceite: é nele que começa a frase que continua nos versos 6 a 8.'},
                 'pistas': [
                     {'se': [0, 1], 'x': '<p>Os versos 1 e 2 dizem que o sujeito poético ama as rosas e a quem fala (Lídia). Não dizem quando nascem nem quando morrem. Procura os versos com os verbos de nascer e de morrer (ou acabar) e deixa só esses.</p>'},
                     {'so': [2], 'x': '<p>O verso 3 diz em que dia nascem. Falta o que acontece nesse mesmo dia: lê o verso que completa a frase.</p>'},
                     {'so': [3], 'x': '<p>O verso 4 diz «Em esse dia morrem». Que dia é «esse»? Junta o verso que o diz.</p>'},
                     {'so': [4], 'x': '<p>O verso 5 diz o que a luz é para as rosas e anuncia uma razão («porque»). Procura os versos onde se diz quando nascem e quando acabam.</p>'},
                 ],
                 'falta': '<p>A tua seleção ainda não junta o nascer e o morrer (ou acabar). Vê onde começa e onde termina a frase que diz as duas coisas.</p>',
                 'pista2': '<p>Procura, nos versos 3 a 8, as formas dos verbos «nascer», «morrer» e «acabar». A tua seleção tem de juntar um verso que fale do nascer com outro que fale do morrer ou do acabar. Os versos 1 e 2 ficam de fora.</p>',
                 'f': '<p>«Que em o dia em que nascem, / Em esse dia morrem» (vv. 3-4) di-lo diretamente. Os versos 6 a 8 dizem o mesmo por outras palavras: as rosas nascem com o Sol já nascido e acabam antes de «Apolo» (o Sol) deixar «O seu curso visível», isto é, antes de anoitecer. As duas seleções, ou as duas juntas, são aceites.</p>'},
                {'t': 'tocar', 'id': 'p1-palavra', 'etq': 'treino', 'modo': 'palavras', 'curto': 'A palavra que mostra que não saber da noite é uma escolha',
                 'p': 'Nos versos 10 a 12, toca na palavra (ou nas palavras) que mostram que não saber da noite é uma escolha do sujeito poético e de Lídia. Depois toca em «Verificar».',
                 'tokens': TOK2,
                 'nucleos': [[3]], 'permitidos': [1, 3], 'mostra': [3],
                 'notas': {'1': 'Aceite com «Inscientes»: as duas palavras leem-se juntas (não saber, por vontade).'},
                 'pistas': [
                     {'se': [2], 'x': '<p>«Lídia» é a pessoa a quem o sujeito poético fala. Procura a palavra que diz de que maneira os dois ficam «Inscientes».</p>'},
                     {'se': [6, 7, 8, 9, 10, 11], 'x': '<p>As palavras do verso 11 dizem o que existe à volta da vida: a noite. A pergunta é sobre a atitude perante ela. Procura no verso 10.</p>'},
                     {'se': [14, 15, 16, 17], 'x': '<p>O verso 12 fala do tempo que a vida dura. Procura, no verso 10, a palavra que diz que essa atitude é por querer.</p>'},
                     {'so': [1], 'x': '<p>«Inscientes» diz que não sabem (vê a nota junto do poema). Ainda não diz que é por querer: procura, no mesmo verso, a palavra que o diz.</p>'},
                 ],
                 'falta': '<p>Procura, no verso 10, a palavra que diz que essa atitude é por querer.</p>',
                 'pista2': '<p>Fica só no verso 10. Uma das palavras é o nome da pessoa a quem o sujeito poético fala. Das outras, procura a que diz de que maneira se faz uma coisa: aqui, de que maneira os dois ficam sem saber.</p>',
                 'f': '<p>«voluntariamente» (v. 10): o sujeito poético e Lídia não ignoram a noite por acaso; decidem não pensar nela. As rosas não precisam de decidir, porque nunca chegam a vê-la. Guarda esta palavra: vais precisar dela na tua resposta.</p>'},
            ],
        },
        {
            'id': 'distinguir', 'curto': 'Insuficiente ou adequada', 'titulo': 'Distinguir uma resposta insuficiente de uma adequada', 'apoio': 'poema',
            'o': 'Duas maneiras de explicar a imagem das rosas, que é a primeira metade do que te pedem. As duas citam o poema e nenhuma diz nada de errado.',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') +
                 '<p><b>Resposta A.</b> <span class="cit">' + RESP_A + '</span></p>'
                 '<p><b>Resposta B.</b> <span class="cit">' + RESP_B + '</span></p></div>'},
                {'t': 'escolha', 'id': 'p1-distinguir', 'etq': 'treino', 'curto': 'A resposta que fica aquém, e porquê',
                 'p': 'Que resposta fica aquém do pedido, e porquê?',
                 'o': [
                     {'t': 'A Resposta B: afasta-se do pedido, porque fala da luz e de Apolo em vez de falar das rosas.',
                      'pista': '<p>Vai à segunda estrofe do poema. A quem se refere «elas», no verso 5? Quem «nasce» e «acaba», nos versos 6 a 8?</p>'},
                     {'t': 'A Resposta A: não diz o nome do recurso expressivo.',
                      'pista': '<p>Relê o pedido de treino (está no passo 1): os verbos são «Explicita» e «Fundamenta». Vê se algum deles pede um nome.</p>'},
                     {'t': 'A Resposta B: usa citações a mais.',
                      'pista': '<p>Conta as citações da Resposta B e vê se cada uma vem acompanhada do que mostra. O pedido fixa um mínimo de elementos textuais. Procura se fixa um máximo.</p>'},
                     {'t': 'A Resposta A: diz que as rosas duram pouco, mas não explica o que nelas se admira.',
                      'pista': ''},
                 ], 'c': 3,
                 'pista2': '<p>Põe as duas respostas ao lado dos versos 5 a 8 do poema. Vê qual das duas usa esses versos e o que a outra deixa por dizer sobre as rosas.</p>',
                 'f': '<p>A Resposta A fica pela ideia que serve para qualquer poema com flores: a vida é breve. Não usa os versos 5 a 8, onde está o que é próprio desta ode: as rosas nunca veem a noite e, para elas, a luz é eterna.</p>'
                      '<p>Nos critérios do item oficial 5, cada tópico junta três coisas: o recurso, o elemento textual e <b>o que ele sugere</b> (por exemplo: «através da qual se sugere o destino cruel que condena os seus filhos desde a nascença», critérios, p. 10). E os níveis separam o tópico abordado «adequadamente» do tópico abordado «com pequenas imprecisões e/ou omissões» (pp. 10-11). A Resposta A não erra: omite.</p>'
                      '<p class="pag">Usar estes descritores num poema que não saiu na prova é leitura nossa.</p>'},
            ],
        },
        {
            'id': 'escrever', 'curto': 'A tua resposta', 'titulo': 'Escrever a tua resposta, sem pistas', 'apoio': 'poema',
            'o': 'Agora és tu. O poema fica contigo; as respostas A e B e as explicações ficam nos passos anteriores.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO +
                 '<p class="pag">Na prova, os itens deste tipo valem 13 pontos e não têm limite de palavras: o desconto por extensão só existe no item de resposta extensa (critérios, p. 3). Escreve o que for preciso para cumprires o pedido.</p>'},
                {'t': 'escrever', 'id': 'p1-resposta', 'curto': 'Resposta escrita sobre a relação entre a imagem e a proposta',
                 'rotulo': 'A tua resposta', 'linhas': 9,
                 'ajuda': 'Escreve aqui ou no papel. Quando acabares, guarda: só depois aparecem os critérios e o exemplo comentado.'},
            ],
        },
        {
            'id': 'comparar', 'curto': 'Comparar', 'titulo': 'Comparar com os critérios e com um exemplo comentado', 'apoio': 'poema', 'precisa': 'p1-resposta',
            'o': 'Lê a tua primeira versão ao lado dos tópicos e do exemplo. Não há classificação automática: quem decide o que falta és tu, e depois o docente.',
            'blocos': [
                {'t': 'ver1', 'de': 'p1-resposta'},
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') +
                 '<p><b>Tópicos de resposta</b> (feitos por nós, à maneira dos critérios oficiais).</p><ul class="top">'
                 '<li><b>A imagem.</b> As rosas dos jardins de Adónis nascem e morrem no mesmo dia (vv. 3-4). Como acabam antes de o Sol se pôr (vv. 6-8), não chegam a ver a noite: «A luz para elas é eterna» (v. 5).</li>'
                 '<li><b>A proposta.</b> O sujeito poético propõe a Lídia que vivam do mesmo modo: «Assim façamos nossa vida um dia» (v. 9). Mas sabem que «há noite antes e após / O pouco que duramos» (vv. 11-12) e têm de escolher não pensar nela: «Inscientes, Lídia, voluntariamente» (v. 10).</li>'
                 '<li><b>A relação.</b> As rosas são o modelo: vivem o seu tempo breve como se fosse o tempo todo. A diferença é que nelas isso é natureza e, no sujeito poético e em Lídia, é uma decisão.</li></ul></div>'
                 '<div class="caixa of">' + etq('oficial') + '<p><b>Outras formulações também contam.</b> ' + REGRA_P2 + ' <span class="pag">(critérios gerais, p. 2)</span></p>'
                 '<p>E os tópicos de cada item são dados com a fórmula «ou outros igualmente relevantes» <span class="pag">(critérios, p. 10, para o item 5)</span>.</p></div>'},
                {'t': 'lista', 'id': 'p1-conf', 'titulo': 'Confere a tua primeira versão',
                 'intro': '<p class="ajuda">Marca o que já está na tua resposta. O que ficar por marcar é o que vais rever no passo seguinte.</p>',
                 'itens': [
                     'Disse o que a imagem das rosas mostra, e fui além de «a vida é breve».',
                     'Disse o que o sujeito poético propõe a Lídia.',
                     'Liguei as duas partes: disse em que é que a proposta imita as rosas.',
                     'Disse o que separa as rosas de «nós» (saber da noite e escolher não pensar nela), ou outra ideia igualmente apoiada no texto.',
                     'Usei um elemento textual dos versos 1 a 8 e outro dos versos 9 a 12, entre aspas e com o número do verso.',
                     'Cada citação vem acompanhada do que ela mostra.',
                     'Não atribuí ao poema o que ele não diz (por exemplo, medo ou desespero).',
                     'Escrevi «o sujeito poético» para quem fala no poema. O autor é Fernando Pessoa; Ricardo Reis é o heterónimo que assina a ode.',
                     'Reli a ortografia, a pontuação e as aspas das citações.',
                 ]},
                {'t': 'html', 'h': '<h3>Um exemplo comentado</h3><p class="ajuda">Uma resposta possível, escrita por nós. Não é a única e não é oficial.</p>' + exemplo +
                 '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). Em cada parte: a ideia, a prova (a citação com o número do verso) e a explicação do que a prova mostra. O exemplo faz isto duas vezes e junta uma frase de ligação.</p>'
                 '<p>Os critérios não impõem esta ordem nem conectores certos: «exceto quando tal é expressamente requerido no item, as respostas não têm de apresentar um parágrafo introdutório nem um parágrafo conclusivo» e a clareza pode ser assegurada «sem recurso obrigatório a conectores interfrásicos» <span class="pag">(critérios gerais, p. 2)</span>.</p></div>'
                 '<p class="pag">Correção linguística: no item oficial vale 3 dos 13 pontos (tabela no item oficial, no cimo da página; critérios, p. 11). Entre os erros do tipo A está o «incumprimento das regras de citação de texto ou de referência a título de uma obra» (critérios, p. 2).</p>'},
            ],
        },
        {
            'id': 'rever', 'curto': 'Rever', 'titulo': 'Rever a tua resposta', 'apoio': 'poema', 'precisa': 'p1-resposta',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres os critérios, a página diz isso junto dela. Escreve a versão revista: muda só o que os critérios e o exemplo te mostraram que faltava.',
            'blocos': [
                {'t': 'rever', 'de': 'p1-resposta', 'curto': 'Versão revista da resposta', 'linhas': 9},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Sobre 2027.</b> O item oficial e os critérios citados são de 2026. A estrutura da prova de 2027, incluindo os poetas e os tipos de item do Grupo I, está a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        },
    ],
}

CAB = (
    '<p class="sobre">Treino 1 de 3. Interpretação literária</p>'
    '<h1>Da imagem à proposta de vida</h1>'
    '<p class="lede">Uma ode de Ricardo Reis, seis passos e uma resposta escrita por ti. Trabalha a mesma ode que o ' + aquecimento('s14') + ' da ' + sessao('s14', 'Reis: a disciplina do instante') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Explicar a relação entre uma imagem do poema e uma ideia (aqui, a proposta de vida), com apoio em elementos textuais.</dd></div>'
    '<div><dt>Item oficial a que se liga</dt><dd>Prova 639, 2026, 1.ª fase, Grupo I, Parte B, item 5 (resposta restrita, 13 pontos): explicitar sentimentos e fundamentar cada um com um recurso expressivo e um elemento textual. '
    + lig('e1', 'Enunciado, p. 7 (PDF em eduqa.pt)') + '; ' + lig('c1', 'critérios, pp. 10-11 (PDF em eduqa.pt)') + '.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<details class="dobra"><summary>Ver o item oficial completo: texto, item, cotação e critério</summary><div class="dentro">' + OFICIAL + '</div></details>'
)

cita_ok(json.dumps(TREINO, ensure_ascii=False))
NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB.replace(OFICIAL, '') + APOIO_POEMA


def construir():
    lint('interpretacao', re.sub(re.escape(md(IT['enunciado'][0])), '', NOSSO))
    return pagina_treino('interpretacao', 'interpretacao/', 'Interpretação', 'Treino 1: da imagem à proposta de vida | Português',
                         'Treino da preparação de exame de Português: interpretação literária, com uma ode de Ricardo Reis, seis passos e uma resposta escrita por ti.', CAB, {'poema': APOIO_POEMA}, TREINO)

