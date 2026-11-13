"""13/11/2026: treino 8, «Uma afirmação, duas reflexões, três partes» (exame/treinos/exposicao/), ligado à sessão 23.

O item oficial é o item 7 do Grupo I da 2.ª fase de 2026 (Parte C): uma «breve exposição» sobre a lírica de Camões, 13 pontos,
sem número de palavras marcado, com introdução e conclusão pedidas pelo próprio item. Os limites de 200 a 350 palavras só
existem no Grupo III; a meta da sessão 23 (200 a 350 palavras, duas obras) vem dita como orientação nossa da sessão.
Os dois sonetos do treino estão em domínio público e vêm, verso a verso, de páginas já publicadas: «Alma minha gentil, que te
partiste», do banco do aquecimento s04 (igual à lição M3-F09); «Amor é fogo que arde sem se ver», do exercício longo do
módulo 3 «O soneto que acaba numa pergunta». Tudo o que o texto nosso põe entre «» é verso destes sonetos, citação oficial
conferida ou está na lista ENTRE_ASPAS.
"""
from .base import *
from .escrita import R_DESC, OPG

# ---------- os dois sonetos (domínio público), das páginas onde já estão publicados ----------
_b04 = json.load(open(ROOT + '/docs/pedagogia/exame-aquecimentos/s04.json', encoding='utf-8'))
ALMA = [html.unescape(v) for v in re.findall(r'<span class="ln" data-l="0-\d+">(.*?)</span>', _b04['cartoes'][1]['html'])]
ALMA_ESPERADO = ['Alma minha gentil, que te partiste', 'Tão cedo desta vida descontente,', 'Repousa lá no céu eternamente,', 'E viva eu cá na terra sempre triste.',
                 'Se lá no assento etéreo, onde subiste,', 'Memória desta vida se consente,', 'Não te esqueças daquele amor ardente', 'Que já nos olhos meus tão puro viste.',
                 'E se vires que pode merecer-te', 'Alguma cousa a dor que me ficou', 'Da mágoa, sem remédio, de perder-te,',
                 'Roga a Deus, que teus anos encurtou,', 'Que tão cedo de cá me leve a ver-te,', 'Quão cedo de meus olhos te levou.']
assert ALMA == ALMA_ESPERADO, ALMA
FONTE_ALMA = 'Luís de Camões, <i>Rhythmas</i> (1595), soneto XIII (grafia modernizada).'
assert '<p class="fonte">' + FONTE_ALMA + '</p>' in _b04['cartoes'][1]['html'].replace('\xa0', ' ')
H9 = open(ROOT + '/m3/licao-m3-f09/index.html', encoding='utf-8').read()
assert '<title>Lição M3-F09: Uma alma gentil, um «não sei quê»</title>' in H9
for _s in ('Repousa lá no céu eternamente,', 'E viva eu cá na terra sempre triste.', 'a antítese separa-os: «lá no céu», «cá na terra».', 'Luís de Camões, _Rhythmas_ (1595), soneto XIII (grafia modernizada).'):
    assert _s in H9.replace('\xa0', ' '), ('lição M3-F09', _s)
assert [st for st in SESSOES['s04']['source']['passages'][0]['stanzas']][0][2:] == ALMA[2:4]

H3 = open(ROOT + '/m3/m3-soneto-raciocinio/index.html', encoding='utf-8').read()
_bq = [m for m in re.findall(r'<blockquote class=\\"cit\\">(.*?)</blockquote>', H3, re.S) if 'Amor é fogo' in m]
AMOR = [html.unescape(v) for v in re.findall(r'<p>(.*?)</p>', _bq[0])]
AMOR_ESPERADO = ['Amor é fogo que arde sem se ver;', 'É ferida que dói e não se sente;', 'É um contentamento descontente;', 'É dor que desatina sem doer;',
                 'É um não querer mais que bem querer;', 'É solitário andar por entre a gente;', 'É um não contentar-se de contente;', 'É cuidar que se ganha em se perder;',
                 'É um estar-se preso por vontade;', 'É servir a quem vence o vencedor;', 'É um ter com quem nos mata lealdade.',
                 'Mas como causar pode o seu favor', 'Nos mortais corações conformidade,', 'Sendo a si tão contrário o mesmo Amor?']
assert AMOR == AMOR_ESPERADO, AMOR
FONTE_AMOR = 'Luís de Camões, <i>Rimas (sonetos)</i>, «Amor é fogo que arde sem se ver», soneto integral. Obras Completas, tomo II (transcrição do Project Gutenberg n.º 31509); aqui moderniza-se a grafia'
assert FONTE_AMOR in H3.replace('\xa0', ' ')
for _s in ('O soneto que acaba numa pergunta', 'o soneto acaba no ponto de interrogação', 'Como causa «conformidade» algo tão contrário a si mesmo', 'Procura a primeira palavra que não é «É» nem «Amor».'):
    assert _s in H3, ('exercício longo do M3', _s)
# a pergunta única do passo 2: antes do verso 12, todos os versos abrem por «Amor é» ou por «É»; a única oposição lá/cá da primeira quadra está nos versos 3 e 4
assert all(v.startswith(('Amor é', 'É ')) for v in AMOR[:11]) and AMOR[11].startswith('Mas como') and AMOR[13].endswith('?')
assert [i for i, v in enumerate(ALMA[:4]) if re.search(r'\b(lá|cá)\b', v)] == [2, 3]
VERSOS = ' / '.join(ALMA) + ' // ' + ' / '.join(AMOR)


def poema(versos):
    return '<ol class="poema">' + ''.join('<li%s><span class="n">%d</span><span>%s</span></li>' % (' class="e"' if i in (4, 8, 11) else '', i + 1, esc(v)) for i, v in enumerate(versos)) + '</ol>'


M3 = '../../../m3/'
LIG9 = '<a href="%slicao-m3-f09/">lição M3-F09 (Uma alma gentil, um «não sei quê»)</a>' % M3
LIG3 = '<a href="%sm3-soneto-raciocinio/">«O soneto que acaba numa pergunta»</a>' % M3
AP_POEMAS = (
    '<p class="texto-t">«Alma minha gentil, que te partiste»</p>' + poema(ALMA) +
    '<p class="fonte">' + FONTE_ALMA + ' Texto conferido com o banco do aquecimento da sessão 4 e com a ' + LIG9 + '.</p>'
    '<p class="texto-t espaco">«Amor é fogo que arde sem se ver»</p>' + poema(AMOR) +
    '<p class="fonte">' + FONTE_AMOR + '. Texto conferido com o exercício ' + LIG3 + ', do módulo 3.</p>'
    '<p class="pag">Os dois sonetos estão em domínio público. Nenhum dos dois saiu impresso nas provas de 2026: o item 7 não traz texto.</p>'
)

# ---------- item oficial: 2.ª fase, Grupo I, Parte C, item 7 ----------
IT = F2['grupos'][0]['partes'][2]['itens'][0]
assert (IT['numero'], IT['cotacao'], IT['obrigatorio'], IT['tipo']) == ('I.7', 13, True, 'construção: resposta restrita (breve exposição)')
assert ['I.7', 13] in F2['cotacoes']['obrigatorios']['itens'] and not F2['grupos'][0]['partes'][2].get('textos')
assert len(IT['enunciado']) == 3 and len(IT['enunciado_lista']) == 3 and 'extensao' not in IT
assert not re.search(r'palavras|\d', ' '.join(IT['enunciado'] + IT['enunciado_lista']))  # o item não marca número de palavras
E_INTRO, E_DES, E_CONC = [x.rstrip(';.') for x in IT['enunciado_lista']]
assert E_INTRO == 'uma introdução ao tema' and E_CONC == 'uma conclusão adequada ao desenvolvimento do tema'
assert E_DES == 'um desenvolvimento no qual explicite duas reflexões sobre a existência humana, presentes na lírica de Camões, fundamentando cada uma delas com referência a poemas lidos'
cr = IT['criterios']
PC_, PED, PCL = cr['parametros']
assert [(p['sigla'], p['pontos']) for p in (PC_, PED, PCL)] == [('C', 8), ('ED', 3), ('CL', 2)] and PCL['tabela'] == 'CL_2' and cr['pontos'] == 13
assert [(n['nivel'], n['pontuacao']) for n in PC_['niveis']] == [(4, 8), (3, 6), (2, 4), (1, 2)]
assert [(n['nivel'], n['pontuacao']) for n in PED['niveis']] == [(3, 3), (2, 2), (1, 1)]
assert F2['criterios']['tabelas_CL']['CL_2']['erros_B'] == {'0': {'A0': 2, 'A1': 2, 'A2': 1, 'A3': 1}, '1': {'A0': 1}}
I_DOIS = 'Devem ser abordados dois dos tópicos seguintes, ou outros igualmente relevantes.'
assert cr['instrucao'] == 'Devem ser abordados **dois** dos tópicos seguintes, ou outros igualmente relevantes.' and cr['introducao_topicos'] == 'Por exemplo, reflexão sobre:'
assert len(cr['topicos']) == 7 and all(list(t) == ['pontos'] and len(t['pontos']) == 1 for t in cr['topicos'])
D_C4 = 'Explicita, adequadamente, duas reflexões sobre a existência humana, presentes na poesia lírica de Camões.'
D_C2B = 'Explicita, adequadamente, apenas uma reflexão sobre a existência humana, presente na poesia lírica de Camões.'
assert PC_['niveis'][0]['descritores'] == [[D_C4]] and PC_['niveis'][2]['descritores'][1] == [D_C2B] and PC_['niveis'][2]['pontuacao'] == 4
D_ED3 = PED['niveis'][0]['descritores'][0][0]
D_ED2 = PED['niveis'][1]['descritores'][0][0]
ED_PARTES = 'três partes (introdução, desenvolvimento e conclusão), devidamente proporcionadas'
ED_COES = 'mecanismos de coesão textual que asseguram de modo global a progressão e o encadeamento das ideias'
ED_DESEQ = 'desequilíbrios de proporção'
assert ED_PARTES in D_ED3 and ED_COES in D_ED3 and ED_DESEQ in D_ED2 and D_ED3.startswith('Escreve um texto bem estruturado constituído por três partes')
N_ED = 'Além dos descritores de desempenho relativos à estruturação temática e discursiva, há que atender aos Critérios Gerais (p. 2).'
assert PED['nota_de_rodape'] == N_ED
T_AMOR = 'a experiência amorosa, nomeadamente sobre as emoções contraditórias geradas pelo amor'
T_AMOR_V = 'ferida que dói, e não se sente'
T_MORTE = 'a dor provocada pela saudade da amada que morreu no mar, nomeadamente sobre a crueldade da morte que a levou prematuramente e de forma inesperada, condenando o poeta a viver em profunda tristeza'
T_MORTE_V = 'cá na terra sempre triste'
assert cr['topicos'][0]['pontos'][0].startswith(T_AMOR + ' (') and '(a «%s»)' % T_AMOR_V in cr['topicos'][0]['pontos'][0]
assert cr['topicos'][1]['pontos'][0] == T_MORTE + ' («%s»);' % T_MORTE_V
assert T_MORTE_V in ALMA[3] and T_AMOR_V not in VERSOS and T_AMOR_V.replace(',', '') in AMOR[1]
assert 'adequadamente, num dos casos' in PC_['niveis'][1]['descritores'][0][0] and PC_['niveis'][1]['descritores'][0][0].startswith('Explicita, adequadamente, duas reflexões')

GER1 = json.dumps(F1['criterios']['gerais'], ensure_ascii=False)
GER2 = json.dumps(F2['criterios']['gerais'], ensure_ascii=False)
REGRA_P2 = 'As respostas que não apresentem exatamente os termos ou interpretações constantes nos critérios específicos são classificadas em igualdade de circunstâncias com aquelas que os apresentem, desde que o seu conteúdo seja cientificamente válido, adequado ao solicitado e enquadrado pelos documentos curriculares de referência.'
R_INTRO = 'exceto quando tal é expressamente requerido no item, as respostas não têm de apresentar um parágrafo introdutório nem um parágrafo conclusivo'
R_PARAG = 'apenas deve ser penalizada a ausência dos parágrafos inequivocamente necessários, ou seja, aqueles que decorrem da introdução de unidades de sentido claramente distintas das anteriores'
R_CONECT = 'a progressão e a clareza das ideias podem ser asseguradas através de diversos mecanismos (nomeadamente a pontuação e a repetição lexical), sem recurso obrigatório a conectores interfrásicos'
R_CITAR = 'incumprimento das regras de citação de texto ou de referência a título de uma obra'
for _s in (REGRA_P2, R_INTRO, R_PARAG, R_CONECT, R_CITAR, R_DESC.strip('«»')):
    assert _s in GER1 and _s in GER2, _s
assert 'item de resposta extensa' in R_DESC
# a regra dos limites de palavras é do Grupo III: só esse item tem extensão marcada, nas duas fases
for _F in (F1, F2):
    assert _F['grupos'][2]['itens'][0]['extensao']['min_palavras'] == 200 and _F['grupos'][2]['itens'][0]['extensao']['max_palavras'] == 350
    assert all('extensao' not in i for p in _F['grupos'][0]['partes'] for i in p['itens'])

# a mesma «breve exposição» na 1.ª fase (só se compara; o enunciado não se reproduz)
IT1 = F1['grupos'][0]['partes'][2]['itens'][0]
cr1 = IT1['criterios']
assert (IT1['numero'], IT1['cotacao'], IT1['tipo'], IT1['obrigatorio']) == ('I.7', 13, IT['tipo'], True)
assert IT1['enunciado_lista'][0] == IT['enunciado_lista'][0] and IT1['enunciado_lista'][2] == IT['enunciado_lista'][2]
assert 'duas situações ou dois momentos' in IT1['enunciado_lista'][1] and IT1['obras_a_escolha'] == ['_Memorial do Convento_', '_O Ano da Morte de Ricardo Reis_']
assert [(p['sigla'], p['pontos']) for p in cr1['parametros']] == [('C', 8), ('ED', 3), ('CL', 2)] and cr1['parametros'][1]['niveis'] == PED['niveis'] and cr1['parametros'][2]['tabela'] == 'CL_2'
assert 'Escreva uma breve exposição na qual comprove' in IT['enunciado'][1] and 'Escreva uma breve exposição na qual comprove' in IT1['enunciado'][1]

# a sessão 23 pede outra coisa: 200 a 350 palavras, duas obras (meta de treino da sessão, não regra do item 7)
_p23 = SESSOES['s23']['writing']['prompt'].replace('\xa0', ' ')
assert 'texto expositivo de 200 a 350 palavras' in _p23 and 'em duas obras estudadas' in _p23

ENUN = (''.join('<p class="enun">%s</p>' % md(x) for x in IT['enunciado']) +
        '<ul class="top enun">' + ''.join('<li>%s</li>' % md(x) for x in IT['enunciado_lista']) + '</ul>')
AP_ITEM = ('<p>' + etq('oficial') + '</p><p class="texto-a">Prova 639, 2026, 2.ª fase, versão 2, Grupo I, Parte C, item 7. Resposta restrita (breve exposição), 13 pontos; conta sempre para a classificação. Enunciado, p. 5 (' + lig('e2', 'PDF em eduqa.pt') + ').</p>'
           + ENUN +
           '<p class="pag">Cotação: 13 pontos. Aspetos de conteúdo, 8; aspetos de estruturação do discurso, 3; aspetos de correção linguística, 2 (critérios, pp. 12-13).</p>'
           '<p class="pag">O item não traz texto: escreves a partir dos poemas que leste.</p>')

topicos = '<ul class="top">' + ''.join('<li>%s</li>' % md(t['pontos'][0]) for t in cr['topicos']) + '</ul>'
TOPICOS_OF = ('<div class="caixa of">' + etq('oficial') + '<p><b>Tópicos de resposta</b> <span class="pag">(critérios, p. 12; ' + lig('c2', 'PDF em eduqa.pt') + ')</span></p>'
              '<p>' + md(cr['instrucao']) + '</p><p>' + md(cr['introducao_topicos']) + '</p>' + topicos + '</div>')
TAB_C = ('<div class="caixa of">' + etq('oficial') + '<p><b>' + PC_['nome'] + ' (C): ' + str(PC_['pontos']) + ' pontos.</b> <span class="pag">Critérios, p. 12.</span></p>'
         + tabela_niveis(PC_['niveis'], 'Níveis de desempenho dos aspetos de conteúdo, item 7') + '</div>')
TAB_ED = ('<div class="caixa of">' + etq('oficial') + '<p><b>' + PED['nome'] + ' (ED): ' + str(PED['pontos']) + ' pontos.</b> <span class="pag">Critérios, p. 13.</span></p>'
          + tabela_niveis(PED['niveis'], 'Níveis de desempenho dos aspetos de estruturação do discurso, item 7') + '<p class="pag">' + md(N_ED) + '</p></div>')
TAB_CL = ('<div class="caixa of">' + etq('oficial') + '<p><b>' + PCL['nome'] + ' (CL): ' + str(PCL['pontos']) + ' pontos.</b> <span class="pag">Critérios, p. 13; tipologia de erros, pp. 2-3.</span></p>'
          '<p>' + md(PCL['texto']) + '</p>' + tabela_cl('CL_2') + '<p class="pag">' + md(PCL['nota_de_rodape']) + '</p></div>')
OFICIAIS_HTML = [ENUN, TOPICOS_OF, TAB_C, TAB_ED, TAB_CL]

# ---------- textos nossos ----------
PARAGRAFO = ('Uma das reflexões presentes na lírica de Camões é sobre a morte de quem se ama. Em «Alma minha gentil, que te partiste», o sujeito poético dirige-se à amada morta e opõe o lugar dela ao seu: '
             '«Repousa lá no céu eternamente, / E viva eu cá na terra sempre triste.»')
INTRO_B = 'Na lírica de Camões, o sujeito poético não diz só o que sente: pensa sobre o que é amar e sobre o que é perder quem se ama.'
CONC_B = 'Do amor que se contradiz à perda de quem se ama, estes poemas mostram que a lírica de Camões pensa a existência humana.'
EXP_A = [
    'Luís de Camões é um dos maiores poetas portugueses e a sua lírica fala de muitos aspetos da existência humana, como os sentimentos e as experiências pessoais.',
    'Uma reflexão é sobre o amor. Em «Amor é fogo que arde sem se ver», o amor é «um contentamento descontente» e «dor que desatina sem doer», o que mostra que amar é viver sentimentos contrários ao mesmo tempo.',
    'Outra reflexão é sobre a mudança, porque na vida tudo muda e nada fica igual.',
    'Em conclusão, Camões reflete sobre a existência humana.',
]
EXP_B = [
    (INTRO_B,
     'Introdução ao tema: a lírica de Camões como reflexão sobre a existência humana. Anuncia as duas reflexões; anunciá-las é um hábito nosso, não é exigência do item.'),
    ('A primeira reflexão é sobre a natureza contraditória do amor. Em «Amor é fogo que arde sem se ver», o amor é definido por contrários, como «um contentamento descontente», e o soneto acaba numa pergunta: '
     'como pode causar «conformidade» nos corações o que é «tão contrário» a si mesmo? Amar é, assim, viver num conflito que a razão não resolve.',
     'Primeira reflexão: diz-se a reflexão, refere-se o poema e diz-se o que ele mostra. As palavras entre aspas estão no soneto, letra a letra.'),
    ('A segunda é sobre a morte de quem se ama. Em «Alma minha gentil, que te partiste», o sujeito poético dirige-se à amada morta e opõe o lugar dela ao seu: ela repousa «lá no céu», ele fica «cá na terra sempre triste». '
     'A morte é pensada como uma separação que deixa a quem fica uma vida reduzida à tristeza.',
     'Segunda reflexão, pelo mesmo caminho. «A segunda» retoma o parágrafo anterior sem repetir as palavras: é um mecanismo de coesão, e não é um conector.'),
    (CONC_B,
     'Conclusão adequada ao desenvolvimento: volta às duas reflexões e à afirmação que o item manda comprovar, sem trazer nada de novo.'),
]
N_EXP_B = sum(len(a.split()) for a, _ in EXP_B)
exemplo = ''.join('<div class="anot"><p class="c">%s</p><p class="n">%s</p></div>' % (a, b) for a, b in EXP_B)


def exp_html(pars):
    return ''.join('<p class="cit">%s</p>' % x for x in pars)


# o que pode vir entre «» no texto nosso sem ser verso dos dois sonetos: títulos, palavras dos enunciados e nomes de partes da página
ENTRE_ASPAS = {
    'Exposição: explicar com uma linha clara', 'Camões lírico: o que a forma faz sentir', 'O soneto que acaba numa pergunta', 'não sei quê',
    'Verificar', 'breve', 'breve exposição', 'comprove', 'explicite', 'Comprovar', 'na qual', 'exceto quando', 'três partes', 'parágrafos', 'conector', 'transcrição', 'resumo',
    'lá', 'cá', 'Mas', 'Amor é', 'É', 'A segunda', 'adequadamente', 'duas obras', '200 a 350 palavras', 'poemas lidos', 'tu', 'com falhas', 'não está', 'Explicitar',
}
OFICIAIS = {REGRA_P2, R_INTRO, R_PARAG, R_CONECT, R_CITAR, R_DESC.strip('«»'), D_C4, D_C2B, D_ED3, D_ED2, ED_PARTES, ED_COES, ED_DESEQ, I_DOIS, T_AMOR, T_AMOR_V, T_MORTE, T_MORTE_V, E_INTRO, E_DES, E_CONC,
            'fundamentando cada uma delas com referência a poemas lidos', 'referência a poemas lidos', 'com referência a poemas lidos', 'mecanismos de coesão textual', 'ou outros igualmente relevantes', 'adequada ao desenvolvimento do tema', 'devidamente proporcionadas'}
assert 'adequada ao desenvolvimento do tema' in E_CONC and 'devidamente proporcionadas' in D_ED3
for _s in ('fundamentando cada uma delas com referência a poemas lidos',):
    assert _s in E_DES
assert 'mecanismos de coesão textual' in D_ED3 and 'ou outros igualmente relevantes' in I_DOIS


def cita_ok(texto):
    """Tudo o que o texto nosso põe entre «» é verso (ou bocado de verso) dos dois sonetos, citação oficial conferida ou está em ENTRE_ASPAS."""
    for m in re.finditer(r'«([^«»]+)»', re.sub(r'<[^>]+>', '', texto)):
        c = m.group(1)
        if c in ENTRE_ASPAS or c in OFICIAIS or c in VERSOS or c.rstrip('.,') in VERSOS:
            continue
        raise AssertionError(('entre aspas e não conferido', c))


AP_I = {'apoio': 'item', 'apoioRot': 'O item oficial'}
AP_P = {'apoio': 'poemas', 'apoioRot': 'Os dois sonetos'}
TOK_ALMA = [{'x': esc(v), 'n': i + 1} for i, v in enumerate(ALMA[:4])]
TOK_AMOR = [{'x': esc(v), 'n': i + 1} for i, v in enumerate(AMOR)]

PLANO = [
    {'id': 'tema', 'rotulo': 'A introdução: o tema, numa frase', 'linhas': 2},
    {'id': 'r1', 'rotulo': 'Primeira reflexão', 'linhas': 2},
    {'id': 'p1', 'rotulo': 'Poema que a fundamenta, e o que nele o mostra', 'linhas': 2},
    {'id': 'r2', 'rotulo': 'Segunda reflexão', 'linhas': 2},
    {'id': 'p2', 'rotulo': 'Poema que a fundamenta, e o que nele o mostra', 'linhas': 2},
    {'id': 'co', 'rotulo': 'A ideia da conclusão', 'linhas': 2},
]

TREINO = {
    'id': 'exposicao', 'viu': 'os critérios',
    'passos': [
        dict(AP_I, **{
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido',
            'o': 'Lê o enunciado inteiro, com a lista. Depois responde a duas perguntas sobre o que ele manda.',
            'blocos': [
                {'t': 'escolha', 'id': 'p8-pedido', 'etq': 'treino', 'curto': 'O que o item manda pôr na exposição',
                 'p': 'O que tem de aparecer na tua exposição para o item ficar cumprido?',
                 'o': [
                     {'t': 'A tua opinião sobre a afirmação, com dois argumentos e um exemplo para cada um.',
                      'pista': '<p>Procura no enunciado o verbo que vem depois de «na qual». A afirmação já vem dada: vê se o item te pede que a discutas ou que a comproves.</p>'},
                     {'t': 'Um resumo de dois poemas de Camões, verso a verso, pela ordem em que os leste.',
                      'pista': '<p>Relê o segundo ponto da lista e procura lá a palavra «resumo». Depois vê o que tens de explicitar, e quantas vezes.</p>'},
                     {'t': 'Uma introdução ao tema, duas reflexões sobre a existência humana, cada uma fundamentada com referência a poemas lidos, e uma conclusão.',
                      'pista': ''},
                     {'t': 'Uma introdução, a análise formal de um soneto (rima, métrica e recursos expressivos) e uma conclusão.',
                      'pista': '<p>Conta no segundo ponto da lista: quantas reflexões? E sobre quê: sobre a forma dos poemas ou sobre a existência humana?</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Lê a lista do enunciado, um ponto de cada vez, e conta o que cada um pede. O segundo ponto pede mais do que uma coisa: separa-as.</p>',
                 'f': '<p>A lista tem três pontos, mas o segundo pede mais do que uma coisa: duas reflexões, e cada uma fundamentada com referência a poemas lidos. O nível mais alto dos aspetos de conteúdo repete o verbo do enunciado: «' + D_C4 + '» <span class="pag">(critérios, p. 12)</span>.</p>'
                      '<p>«Comprovar» não é opinar nem resumir: é mostrar, com poemas, que a afirmação é verdadeira. «Explicitar» é dizer por palavras tuas, com clareza, que reflexão lá está.</p>'
                      '<p class="pag">O sentido que damos aos dois verbos é leitura nossa.</p>'},
                {'t': 'html', 'h': '<div class="caixa of">' + etq('oficial') + '<p><b>O que os critérios dizem sobre as partes e sobre o número de palavras</b> (' + lig('c2', 'PDF em eduqa.pt') + ').</p>'
                 '<p>Critérios gerais, p. 2, sobre as respostas restritas: «' + R_INTRO + '».</p>'
                 '<p>Item 7, estruturação do discurso, nível 3 (3 pontos), p. 13: «' + D_ED3 + '»</p>'
                 '<p>Critérios gerais, p. 3, limites de extensão: ' + R_DESC + '</p></div>'
                 '<div class="caixa nossa"><p><b>O que é igual nas duas fases de 2026.</b> Na 1.ª fase, o item 7 também pediu uma breve exposição, com a mesma lista de três pontos (introdução, desenvolvimento com dois elementos fundamentados, conclusão), '
                 'os mesmos 13 pontos e a mesma divisão: 8 para o conteúdo, 3 para a estruturação do discurso e 2 para a correção linguística (' + lig('e1', 'enunciado, p. 8') + '; ' + lig('c1', 'critérios, pp. 12-13') + '). '
                 'Mudou a obra: um romance de José Saramago, em vez da lírica de Camões.</p></div>'},
                {'t': 'escolha', 'id': 'p8-regras', 'etq': 'treino', 'curto': 'O tamanho e as partes da exposição',
                 'p': 'O que dizem o item e os critérios sobre o tamanho e as partes desta exposição?',
                 'o': [
                     {'t': 'De 200 a 350 palavras; por cada palavra a mais ou a menos, desconta-se um ponto.',
                      'pista': '<p>Relê a regra da p. 3, aqui em cima: de que item fala? Depois procura um número de palavras no enunciado do item 7.</p>'},
                     {'t': 'O item não marca um número de palavras; pede três partes, e a proporção entre elas conta na estruturação do discurso.',
                      'pista': ''},
                     {'t': 'Como nas outras respostas restritas, a introdução e a conclusão são dispensáveis.',
                      'pista': '<p>Relê a regra da p. 2: começa por «exceto quando». Vê se a lista do item 7 pede uma introdução e uma conclusão.</p>'},
                     {'t': 'A exposição tem de ter exatamente quatro parágrafos: um de introdução, dois de desenvolvimento e um de conclusão.',
                      'pista': '<p>Procura a palavra «parágrafos» no item e no descritor da p. 13. O que lá está é «três partes». Vê se uma parte tem de ser um só parágrafo.</p>'},
                 ], 'c': 1,
                 'pista2': '<p>São três textos oficiais: o enunciado (p. 5), a regra da introdução e da conclusão (p. 2) e o descritor da estruturação (p. 13). Procura em cada um o que diz sobre palavras, sobre partes e sobre proporção.</p>',
                 'f': '<p>O enunciado só diz «breve». Os limites de 200 a 350 palavras e o desconto por palavra são do item de resposta extensa, o Grupo III (enunciado, p. 8; critérios, p. 3).</p>'
                      '<p>As três partes são pedidas pelo item (p. 5) e avaliadas: o nível 3 da estruturação fala em «' + ED_PARTES + '»; com «' + ED_DESEQ + '», o descritor é o do nível 2, 2 pontos (p. 13). '
                      'Os critérios falam em partes, não em número de parágrafos: «' + R_PARAG + '» <span class="pag">(critérios gerais, p. 2)</span>.</p>'
                      '<p class="pag">No pedido de escrita da sessão 23 aparecem «200 a 350 palavras» e «duas obras»: é uma meta de treino da sessão (orientação nossa), não é uma regra do item 7.</p>'},
            ],
        }),
        dict(AP_P, **{
            'id': 'localizar', 'curto': 'Localizar', 'titulo': 'Localizar nos poemas',
            'o': 'Dois sonetos que o módulo 3 já te deu a ler. Em cada um, procura o sítio onde o poema deixa de só sentir e passa a pensar.',
            'blocos': [
                {'t': 'tocar', 'id': 'p8-alma', 'etq': 'treino', 'modo': 'versos', 'curto': 'Os dois versos que opõem o lugar dela ao lugar dele',
                 'p': 'Na primeira quadra de «Alma minha gentil, que te partiste», toca nos dois versos que opõem o lugar onde ela repousa ao lugar onde ele fica a viver. Depois toca em «Verificar».',
                 'tokens': TOK_ALMA, 'nucleos': [[2, 3]], 'permitidos': [2, 3], 'mostra': [2, 3],
                 'pistas': [
                     {'se': [0, 1], 'x': '<p>Os versos 1 e 2 dizem que ela partiu, e quando. A pergunta é pelos dois lugares: procura duas palavras pequenas, uma que aponta para longe e outra que aponta para perto.</p>'},
                 ],
                 'falta': '<p>Estás no sítio certo, mas a oposição precisa dos dois lados: falta um verso.</p>',
                 'pista2': '<p>Procura os advérbios «lá» e «cá». Cada um está num verso, e os dois versos vêm seguidos.</p>',
                 'f': '<p>«Repousa lá no céu eternamente, / E viva eu cá na terra sempre triste.» A lição M3-F09 chama antítese a esta oposição: «lá no céu», «cá na terra». '
                      'Daqui sai uma reflexão: a morte de quem se ama separa, e quem fica vive na tristeza.</p>'
                      '<p>Os critérios dão uma reflexão destas como exemplo: «' + T_MORTE + '», e citam «' + T_MORTE_V + '» <span class="pag">(critérios, p. 12)</span>.</p>'
                      '<p class="pag">Nota nossa: os critérios não dizem de que poema tiram o verso, e este soneto, tal como aqui está, não fala do mar. Não precisas de o dizer.</p>'},
                {'t': 'tocar', 'id': 'p8-amor', 'etq': 'treino', 'modo': 'versos', 'curto': 'O verso em que o soneto passa a perguntar',
                 'p': '«Amor é fogo que arde sem se ver» começa por definir o amor, verso a verso. Toca no verso em que deixa de definir e passa a perguntar. Depois toca em «Verificar».',
                 'tokens': TOK_AMOR, 'nucleos': [[11]], 'permitidos': [11, 12, 13], 'mostra': [11],
                 'notas': {'12': 'Aceite com os versos 13 e 14: a pergunta ocupa o terceto inteiro, mas começa no verso 12.', '13': 'Aceite com os versos 13 e 14: a pergunta ocupa o terceto inteiro, mas começa no verso 12.'},
                 'pistas': [
                     {'so': [12, 13], 'x': '<p>Esses versos já fazem parte da pergunta. Falta o verso onde ela começa.</p>'},
                     {'se': list(range(0, 11)), 'x': '<p>Esse verso ainda diz o que o amor é. Procura o primeiro verso que não começa por «Amor é» nem por «É».</p>'},
                 ],
                 'falta': '<p>Procura o verso onde a pergunta começa.</p>',
                 'pista2': '<p>Fica só no último terceto. O primeiro verso dele começa por uma conjunção que anuncia uma viragem.</p>',
                 'f': '<p>«Mas como causar pode o seu favor»: até ao verso 11, o soneto define o amor por contrários; no verso 12, pergunta como pode causar «conformidade» nos corações o que é «tão contrário» a si mesmo. '
                      'É a leitura do exercício ' + LIG3 + ', do módulo 3. Aqui está outra reflexão: a experiência amorosa como contradição que não se resolve.</p>'
                      '<p>Os critérios também a dão como exemplo: «' + T_AMOR + '» <span class="pag">(critérios, p. 12)</span>.</p>'
                      '<p class="pag">Nota nossa: nesse tópico, os critérios citam «' + T_AMOR_V + '», com vírgula; nesta página, o verso 2 vem sem ela. São edições diferentes, e as duas servem. Se citares, cita como leste.</p>'},
            ],
        }),
        dict(AP_P, **{
            'id': 'explicitar', 'curto': 'Da referência à reflexão', 'titulo': 'Passar da referência à reflexão',
            'o': 'Um parágrafo de desenvolvimento que para na citação. Quatro maneiras de o continuar.',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p class="cit">' + PARAGRAFO + '</p></div>'},
                {'t': 'escolha', 'id': 'p8-explicitar', 'etq': 'treino', 'curto': 'A frase que explicita a reflexão',
                 'p': 'Que frase continua o parágrafo de modo a explicitar a reflexão?',
                 'o': [
                     {'t': 'Ou seja, ela repousa no céu para sempre e ele vive na terra sempre triste.',
                      'pista': '<p>Compara esta frase com os dois versos, palavra a palavra. Vê o que ela diz que os versos ainda não tinham dito.</p>'},
                     {'t': 'No mesmo soneto, mais abaixo, o sujeito poético fala ainda da «mágoa, sem remédio, de perder-te».',
                      'pista': '<p>É mais uma transcrição. Conta quantas frases do parágrafo dizem o que as transcrições mostram sobre a morte de quem se ama.</p>'},
                     {'t': 'Este soneto é um dos mais conhecidos de Camões e mostra bem a qualidade da sua poesia.',
                      'pista': '<p>Esta frase avalia o poema. Relê o segundo ponto da lista do item: pede uma avaliação ou uma reflexão sobre a existência humana?</p>'},
                     {'t': 'A oposição entre «lá» e «cá» mostra a morte de quem se ama como uma separação: quem fica continua vivo, mas na tristeza.',
                      'pista': ''},
                 ], 'c': 3,
                 'pista2': '<p>Faz a mesma pergunta às quatro frases: diz o que os versos mostram sobre a vida de quem perde alguém? Só uma responde; as outras repetem, acrescentam ou elogiam.</p>',
                 'f': '<p>Três frases, três funções: a primeira diz a reflexão, a segunda refere o poema, a terceira diz o que os versos mostram. Sem a terceira, a citação fica solta, e o tamanho da citação não muda isso.</p>'
                      '<p>O item pede um desenvolvimento em que explicites as reflexões, «fundamentando cada uma delas com referência a poemas lidos» (enunciado, p. 5), e o descritor mede isso mesmo: «' + D_C4 + '» <span class="pag">(critérios, p. 12)</span>. '
                      'Os tópicos dos critérios fazem o mesmo caminho: dizem a reflexão e juntam-lhe palavras dos poemas, várias vezes entre parênteses (p. 12).</p>'
                      '<p class="pag">Leitura nossa: o que o item pede é a referência a poemas; a transcrição de versos não é exigida. Se citares, cita letra a letra: entre os erros do tipo A está o «' + R_CITAR + '» (critérios, p. 2).</p>'},
            ],
        }),
        dict(AP_I, **{
            'id': 'partes', 'curto': 'Abrir e fechar', 'titulo': 'Abrir e fechar a exposição',
            'o': 'Imagina que o desenvolvimento trata o amor feito de contrários e a morte de quem se ama. Faltam a primeira parte e a última.',
            'blocos': [
                {'t': 'escolha', 'id': 'p8-intro', 'etq': 'treino', 'curto': 'A introdução ao tema',
                 'p': 'Que frase serve de introdução ao tema desta exposição?',
                 'o': [
                     {'t': 'Em «Amor é fogo que arde sem se ver», o amor é definido por contrários.',
                      'pista': '<p>Esta frase já é desenvolvimento: entra num poema. Procura a frase que apresenta o tema antes de chegar aos poemas.</p>'},
                     {'t': INTRO_B, 'pista': ''},
                     {'t': 'Luís de Camões é o autor de <i>Os Lusíadas</i>, a epopeia que narra a viagem de Vasco da Gama à Índia.',
                      'pista': '<p>Relê a primeira linha do item: de que parte da obra de Camões fala?</p>'},
                     {'t': 'Sempre gostei de poesia, e os sonetos de Camões são os meus preferidos desde o 10.º ano.',
                      'pista': '<p>Procura no item o tema: é o teu gosto, ou a reflexão sobre a existência humana na lírica de Camões?</p>'},
                 ], 'c': 1,
                 'pista2': '<p>O tema está na primeira frase do item: a lírica de Camões e a reflexão sobre a existência humana. Só uma opção fala das duas coisas sem entrar ainda num poema.</p>',
                 'f': '<p>A introdução apresenta o tema: a lírica de Camões como reflexão sobre a existência humana. Esta anuncia também as duas reflexões que vêm a seguir. '
                      'O item pede «' + E_INTRO + '» (enunciado, p. 5) e não diz como tem de ser.</p>'
                      '<p class="pag">Anunciar as reflexões é uma maneira nossa de abrir, não é uma exigência.</p>'},
                {'t': 'escolha', 'id': 'p8-conclusao', 'etq': 'treino', 'curto': 'A conclusão adequada ao desenvolvimento',
                 'p': 'Que frase serve de conclusão a este desenvolvimento?',
                 'o': [
                     {'t': CONC_B, 'pista': ''},
                     {'t': 'Além disso, Camões reflete também sobre a mudança, porque no mundo nada fica igual ao que era antes.',
                      'pista': '<p>Vê se esta frase fecha o que foi tratado ou abre uma reflexão nova, que o desenvolvimento não fundamentou.</p>'},
                     {'t': 'Em suma, são dois sonetos muito bonitos, que recomendo a quem gosta de poesia.',
                      'pista': '<p>Relê o terceiro ponto da lista: a conclusão é «adequada ao desenvolvimento do tema». Procura o tema nesta frase.</p>'},
                     {'t': 'Em conclusão, o primeiro soneto tem catorze versos e o segundo também.',
                      'pista': '<p>A frase é verdadeira. Vê se retoma as duas reflexões do desenvolvimento.</p>'},
                 ], 'c': 0,
                 'pista2': '<p>Procura a frase que volta às duas reflexões do desenvolvimento e à afirmação que o item manda comprovar, sem trazer nada de novo.</p>',
                 'f': '<p>A conclusão retoma as duas reflexões e fecha a comprovação. O item pede «' + E_CONC + '» (enunciado, p. 5), e as três partes, «devidamente proporcionadas», fazem parte do descritor do nível 3 da estruturação do discurso (critérios, p. 13).</p>'},
            ],
        }),
        dict(AP_I, **{
            'id': 'distinguir', 'curto': 'Insuficiente ou adequada', 'titulo': 'Distinguir uma exposição insuficiente de uma adequada',
            'o': 'Duas exposições para o item 7. As duas têm introdução, desenvolvimento e conclusão.',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p><b>Exposição A.</b></p>' + exp_html(EXP_A) + '<p><b>Exposição B.</b></p>' + exp_html([a for a, _ in EXP_B]) + '</div>'},
                {'t': 'escolha', 'id': 'p8-distinguir', 'etq': 'treino', 'curto': 'A exposição que fica aquém, e porquê',
                 'p': 'Que exposição fica aquém do que o item pede, e porquê?',
                 'o': [
                     {'t': 'A Exposição A: os parágrafos não começam todos por um conector.',
                      'pista': '<p>Procura a palavra «conector» no item e no descritor da p. 13, no passo 1. O que lá está é «mecanismos de coesão textual». Vê se a Exposição A tem algum.</p>'},
                     {'t': 'A Exposição A: só uma das duas reflexões vem fundamentada num poema; a outra fica sem referência a nenhum.',
                      'pista': ''},
                     {'t': 'A Exposição B: transcreve só bocados de versos; devia transcrever as quadras inteiras.',
                      'pista': '<p>Procura no item a palavra «transcrição». O que ele pede é «referência a poemas lidos».</p>'},
                     {'t': 'A Exposição B: não chega às duzentas palavras que uma resposta escrita tem de ter.',
                      'pista': '<p>Procura um número de palavras no enunciado do item 7. Depois relê, no passo 1, de que item fala a regra do desconto.</p>'},
                 ], 'c': 1,
                 'pista2': '<p>Em cada exposição, conta duas coisas: quantas reflexões há e, para cada uma, que poema a fundamenta. Numa delas, a conta não fecha.</p>',
                 'f': '<p>Na Exposição A, a reflexão sobre a mudança não refere nenhum poema, e o item pede que cada reflexão venha fundamentada «com referência a poemas lidos» (enunciado, p. 5). '
                      'Além disso, a introdução repete o enunciado e a conclusão não retoma as reflexões. Na Exposição B, cada reflexão tem o seu poema e uma frase que diz o que ele mostra.</p>'
                      '<p>Nos critérios, um dos descritores do nível 2 dos aspetos de conteúdo (4 dos 8 pontos) é este: «' + D_C2B + '» <span class="pag">(critérios, p. 12)</span>.</p>'
                      '<p>E os conectores não são obrigatórios: «' + R_CONECT + '» <span class="pag">(critérios gerais, p. 2)</span>.</p>'
                      '<p class="pag">Pôr estes descritores ao lado de uma exposição feita por nós é leitura nossa: quem classifica é o docente.</p>'},
            ],
        }),
        dict(AP_I, **{
            'id': 'escrever', 'curto': 'A tua exposição', 'titulo': 'Planear e escrever a tua exposição, sem pistas',
            'o': 'Agora és tu. Fica contigo o item, como na prova. As exposições A e B e as explicações ficam nos passos anteriores.',
            'blocos': [
                {'t': 'html', 'h': '<p>Podes usar os dois sonetos dos passos anteriores ou outros poemas de Camões que tenhas lido: o item diz «poemas lidos». Na prova não tens os poemas à frente. '
                 'Se citares, cita letra a letra; se não tens a certeza das palavras, refere o poema sem aspas.</p>'
                 '<p class="pag">O item vale 13 pontos e não marca um número de palavras: o desconto por extensão só existe no item de resposta extensa (critérios, p. 3). A caixa conta as palavras só para saberes o tamanho do que escreveste.</p>'},
                {'t': 'campos', 'id': 'p8-plano', 'titulo': 'O teu plano',
                 'intro': '<p class="ajuda">Notas curtas, só para ti. Ficam guardadas neste dispositivo. Também podes planear no papel.</p>',
                 'campos': PLANO},
                {'t': 'escrever', 'id': 'p8-resposta', 'curto': 'Breve exposição sobre a lírica de Camões', 'rotulo': 'A tua exposição', 'linhas': 14, 'conta': True,
                 'ajuda': 'Escreve aqui ou no papel. Quando acabares, guarda: só depois aparecem os critérios e o exemplo comentado.'},
            ],
        }),
        dict(AP_I, **{
            'id': 'comparar', 'curto': 'Conferir', 'titulo': 'Conferir com os critérios, aspeto a aspeto', 'precisa': 'p8-resposta',
            'o': 'Lê a tua primeira versão ao lado da grelha oficial. Não há classificação automática: marcas tu, aspeto a aspeto, e quem classifica é o docente.',
            'blocos': [
                {'t': 'ver1', 'de': 'p8-resposta', 'conta': True, 'linhas': 14},
                {'t': 'html', 'h': '<h3>1. Os tópicos de resposta</h3>' + TOPICOS_OF +
                 '<p class="pag">Nota nossa: os critérios citam versos sem dizer de que poemas são. Os tópicos são exemplos: valem outras reflexões, se as fundamentares em poemas lidos.</p>'
                 '<div class="caixa of">' + etq('oficial') + '<p><b>Outras formulações também contam.</b> «' + REGRA_P2 + '» <span class="pag">(critérios gerais, p. 2)</span></p></div>'},
                {'t': 'html', 'h': '<h3>2. Aspetos de conteúdo (8 pontos)</h3>' + TAB_C +
                 '<p class="pag">Nota nossa: nos níveis 3 e 2, o descritor repete «adequadamente» também onde fala de imprecisões. Está assim no PDF; transcrevemos sem corrigir.</p>'},
                {'t': 'grelha', 'id': 'p8-gC', 'intro': '<p class="ajuda">Para cada aspeto, procura na tua exposição a frase que o cumpre. O item diz «com referência a poemas lidos»: não exige um poema diferente para cada reflexão.</p>',
                 'aspetos': ['primeira reflexão sobre a existência humana, explicitada', 'primeira reflexão fundamentada com referência a poemas lidos',
                             'segunda reflexão, diferente da primeira, explicitada', 'segunda reflexão fundamentada com referência a poemas lidos'], 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>3. Aspetos de estruturação do discurso (3 pontos)</h3>' + TAB_ED +
                 '<div class="caixa of">' + etq('oficial') + '<p><b>Critérios gerais, p. 2.</b> «' + R_INTRO + '»; «' + R_PARAG + '»; «' + R_CONECT + '».</p></div>'
                 '<p class="pag">O descritor fala em «mecanismos de coesão textual». Os conectores são um deles; a pontuação e a repetição de palavras também ligam frases. Neste item, a introdução e a conclusão são pedidas pelo enunciado.</p>'},
                {'t': 'grelha', 'id': 'p8-gED',
                 'aspetos': [E_INTRO, 'um desenvolvimento', E_CONC, 'três partes devidamente proporcionadas', ED_COES], 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>4. Aspetos de correção linguística (2 pontos)</h3>' + TAB_CL +
                 '<p>Relê a exposição devagar, só à procura de erros. Conta-os no papel, em duas colunas: os do tipo A (pontuação, ortografia, morfologia, regras de citação) e os do tipo B (sintaxe, impropriedade lexical); a lista está no Quadro 1 dos critérios, p. 2. '
                 'Depois lê tu a tabela: a linha é o número de erros do tipo B e a coluna é o número de erros do tipo A. A página não faz esta leitura por ti.</p>'},
                {'t': 'html', 'h': '<h3>Um exemplo comentado</h3><p class="ajuda">É a Exposição B do passo 5, escrita por nós, com ' + str(N_EXP_B) + ' palavras. Não é oficial nem é para decorar: os critérios dão tópicos, não exemplos de resposta. '
                 'O número de palavras também não é uma meta: o item só diz «breve».</p>' + exemplo +
                 '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). A introdução ao tema; para cada reflexão, a reflexão, o poema e o que ele mostra; a conclusão, que volta às duas reflexões. '
                 'Outras organizações contam do mesmo modo, se tiverem as três partes e as duas reflexões fundamentadas.</p></div>'},
            ],
        }),
        dict(AP_I, **{
            'id': 'rever', 'curto': 'Rever', 'titulo': 'Rever a tua exposição', 'precisa': 'p8-resposta',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres os critérios, a página diz isso junto dela. Na versão revista, muda o que marcaste como «com falhas» ou «não está».',
            'blocos': [
                {'t': 'rever', 'de': 'p8-resposta', 'curto': 'Versão revista da exposição', 'linhas': 14, 'conta': True},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Outra obra.</b> Na 1.ª fase de 2026, o item 7 pediu o mesmo sobre um romance de José Saramago, <i>Memorial do Convento</i> ou <i>O Ano da Morte de Ricardo Reis</i> '
                 '(' + lig('e1', 'enunciado, p. 8') + '; ' + lig('c1', 'critérios, pp. 12-13') + '). O plano é o mesmo: introdução, dois elementos fundamentados, conclusão.</p>'
                 '<p>Para voltares à lírica de Camões: a ' + sessao('s04', 'Camões lírico: o que a forma faz sentir') + ', a ' + LIG9 + ' e as <a href="../../provas/2026-2f/grupo-i/">provas em cartões (2.ª fase, Grupo I)</a>, que trabalham este mesmo item 7.</p></div>'
                 '<div class="caixa nossa"><p><b>Sobre 2027.</b> O item e os critérios são de 2026. Se a prova de 2027 mantém uma breve exposição, sobre que obras e com que critérios, está a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        }),
    ],
}

CAB = (
    sobre('exposicao', 'Exposição') +
    '<h1>Uma afirmação, duas reflexões, três partes</h1>'
    '<p class="lede">O item 7 do Grupo I da 2.ª fase de 2026, dois sonetos de Camões, oito passos e duas versões da tua exposição. Liga-se à ' + sessao('s23', 'Exposição: explicar com uma linha clara') + ' e ao seu ' + aquecimento('s23') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Escrever uma breve exposição sobre uma obra: comprovar uma afirmação com dois elementos fundamentados, em introdução, desenvolvimento e conclusão.</dd></div>'
    '<div><dt>Item oficial a que se liga</dt><dd>Prova 639, 2026, 2.ª fase, Grupo I, Parte C, item 7 (resposta restrita, 13 pontos; conta sempre). ' + lig('e2', 'Enunciado, p. 5 (PDF em eduqa.pt)') + '; ' + lig('c2', 'critérios, pp. 12-13 (PDF em eduqa.pt)') + '. Critérios definitivos, publicados a 31/07/2026.</dd></div>'
    '<div><dt>O que é igual e o que é diferente da sessão</dt><dd>A sessão 23 pede um texto de 200 a 350 palavras sobre duas obras: é uma meta de treino da sessão (orientação nossa). Na prova de 2026, a exposição é o item 7: breve, sem número de palavras marcado, sobre uma obra. '
    'Os limites de 200 a 350 palavras só existem no Grupo III (enunciado, p. 8; critérios, p. 3). O treino segue o item.</dd></div>'
    '<div><dt>Os textos</dt><dd>Os dois sonetos estão em domínio público e vêm das páginas do módulo 3, com a fonte.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<p class="pag">O enunciado oficial fica ao lado dos passos, inteiro. Os tópicos, os níveis e a tabela dos critérios estão no passo 7, com a página de cada parte.</p>'
)

NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB + AP_POEMAS + AP_ITEM
for _s in OFICIAIS_HTML + [R_DESC]:
    assert _s in NOSSO or json.dumps(_s, ensure_ascii=False)[1:-1] in NOSSO, _s[:60]
    NOSSO = NOSSO.replace(json.dumps(_s, ensure_ascii=False)[1:-1], '').replace(_s, '')
cita_ok(NOSSO)
# o que as exposições A e B põem entre aspas é título (primeiro verso) ou bocado de um verso dos dois sonetos
for _t in EXP_A + [a for a, _ in EXP_B] + [PARAGRAFO]:
    for _c in re.findall(r'«([^«»]+)»', _t):
        assert _c in VERSOS or _c.rstrip('.,;') in VERSOS, _c


def construir():
    lint('exposicao', NOSSO)
    return pagina_treino('exposicao', 'exposicao/', 'Exposição', 'Treino 8: uma breve exposição | Português',
                         'Treino da preparação de exame de Português: uma breve exposição sobre a lírica de Camões, a partir do item 7 do Grupo I da 2.ª fase de 2026, em oito passos e duas versões.',
                         CAB, {'item': AP_ITEM, 'poemas': AP_POEMAS}, TREINO)
