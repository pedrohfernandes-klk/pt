from .base import *

IT = F2['grupos'][2]['itens'][0]
CR = IT['criterios']
assert IT['cotacao'] == 44 and CR['ETD']['pontos'] == 30 and CR['CL']['pontos'] == 14
assert IT['extensao'] == {'min_palavras': 200, 'max_palavras': 350, 'minimo_para_classificar': 80}
GER = json.dumps(F2['criterios']['gerais'], ensure_ascii=False)
GER1 = json.dumps(F1['criterios']['gerais'], ensure_ascii=False)


def oficial(s):
    """Devolve a citação depois de conferir que está nos critérios gerais das duas fases."""
    assert s in GER and s in GER1, s
    return '«' + s + '»'


R_DESC = oficial('Sempre que não sejam respeitados os limites relativos ao número de palavras indicados na instrução do item de resposta extensa, desconta-se um ponto por cada palavra (a mais ou a menos), até ao máximo de cinco (1 × 5) pontos, depois de aplicados todos os critérios definidos para o item.')
R_80 = oficial('Caso a resposta apresente uma extensão inferior a oitenta palavras, é classificada com zero pontos.')
R_CONTA = oficial('Para efeitos de contagem, considera-se uma palavra qualquer sequência delimitada por espaços em branco, mesmo quando esta integre elementos ligados por hífen (ex.: /dir-se-ia/). Qualquer número conta como uma única palavra, independentemente do número de algarismos que o constituam (ex.: /2026/).')
R_ZERO = oficial('A atribuição da classificação de zero pontos no parâmetro A (Género/Formato Textual) ou no parâmetro B (Tema e Pertinência da Informação) implica a atribuição de zero pontos nos restantes parâmetros da ETD, bem como na CL.')
R_MAI = oficial('As provas em que se apresente, pelo menos, uma resposta restrita ou extensa escrita integralmente em maiúsculas são sujeitas a uma desvalorização de cinco pontos na classificação total.')
R_UMA = oficial('Em cada resposta, contabiliza-se como uma única ocorrência quer a repetição de uma palavra com o mesmo erro ortográfico, quer a presença de mais de um erro na mesma palavra (incluindo erro de acentuação, erro de translineação e uso indevido de letra minúscula ou de letra maiúscula).')
R_ALT = oficial('As respostas que não apresentem exatamente os termos ou interpretações constantes nos critérios específicos são classificadas em igualdade de circunstâncias com aquelas que os apresentem, desde que o seu conteúdo seja cientificamente válido, adequado ao solicitado e enquadrado pelos documentos curriculares de referência.')
for s in ['erro inequívoco de pontuação', 'erro de ortografia (incluindo erro de acentuação, erro de translineação e uso indevido de letra minúscula ou de letra maiúscula)', 'erro de morfologia',
          'incumprimento das regras de citação de texto ou de referência a título de uma obra', 'erro de sintaxe', 'impropriedade lexical']:
    assert s in GER

obs = ''
for i, o in enumerate(IT['observacoes']):
    if isinstance(o, str):
        obs += '<li>%s</li>' % md(o)
    else:
        obs += '<li>%s<ul class="top">%s</ul></li>' % (md(o['texto']), ''.join('<li>%s</li>' % md(x) for x in o['lista']))
ENUN = (''.join('<p class="enun">%s</p>' % md(x) for x in IT['enunciado']) +
        '<ul class="top enun">' + ''.join('<li>%s</li>' % md(x) for x in IT['enunciado_lista']) + '</ul>'
        '<p><b>Observações:</b></p><ol class="top menor">' + obs + '</ol>')
AP_ITEM = ('<p>' + etq('oficial') + '</p><p class="texto-a">Prova 639, 2026, 2.ª fase, versão 2, Grupo III. Resposta extensa, 44 pontos; conta sempre para a classificação. Enunciado, p. 8 (' + lig('e2', 'PDF em eduqa.pt') + ').</p>'
           + ENUN +
           '<p class="pag">Cotação: 44 pontos. Estruturação temática e discursiva, 30 (parâmetros A, B e C, 10 cada); correção linguística, 14 (critérios, pp. 14-16).</p>')

PA, PB_, PC = CR['ETD']['parametros']
assert [p['id'] for p in (PA, PB_, PC)] == ['A', 'B', 'C'] and all(p['pontos'] == 10 for p in (PA, PB_, PC))


def aspetos(p):
    d = p['niveis'][0]['descritores'][0]
    assert p['niveis'][0]['nivel'] == 4
    return [md(x).rstrip(';.') for x in d[1:]]


def par_bloco(p, pag):
    return ('<div class="caixa of">' + etq('oficial') + '<p><b>Parâmetro %s: %s</b> (%d pontos). <span class="pag">Critérios, p. %s.</span></p>' % (p['id'], p['nome'], p['pontos'], pag)
            + tabela_niveis(p['niveis'], 'Níveis de desempenho do parâmetro ' + p['id']) + (('<p class="pag">' + md(p['nota']) + '</p>') if p.get('nota') else '') + '</div>')


for p in (PA, PB_, PC):
    assert [(n['nivel'], n['pontuacao']) for n in p['niveis']] == [(4, 10), (3, 8), (2, 5), (1, 3)]
OPG = ['Está no meu texto', 'Está, com falhas', 'Não está']

PAR_A = 'As experiências pessoais são muito importantes para a visão do mundo de cada um. Por exemplo, viajar é uma experiência muito enriquecedora e toda a gente devia viajar mais.'
PAR_B = ('As experiências pessoais dão-nos o que nenhum manual consegue dar: o encontro com pessoas concretas. Quando fiz voluntariado num lar, a solidão dos idosos, que eu só conhecia dos números estudados nas aulas, '
         'passou a ter rostos e nomes. Desde então, olho para o envelhecimento do país como um problema que também é meu.')

MODELO = [
    ('Costuma dizer-se que a escola ensina e a vida educa, como se fossem dois caminhos separados. Na minha opinião, a visão que cada pessoa tem do mundo só fica rica quando os dois se cruzam: as experiências pessoais dão sentido ao que se aprende, e o que se aprende dá palavras ao que se vive.',
     'Parâmetro A: o ponto de vista está dito («Na minha opinião…»). Parâmetro B: o texto pega nas duas partes do tema, experiências e escola. Há discurso valorativo («só fica rica»).'),
    ('Em primeiro lugar, as experiências pessoais mostram-nos o mundo de perto. Quando fiz voluntariado num lar, a solidão dos idosos, que eu só conhecia dos números estudados nas aulas, passou a ter rostos e nomes. Nenhum gráfico me tinha feito sentir que o envelhecimento do país também é um problema meu.',
     'Primeiro argumento (o que as experiências dão) e um exemplo que o ilustra: mostra o que mudou em quem escreve.'),
    ('Por outro lado, sem os conhecimentos adquiridos na escola, a experiência fica presa ao que cada um vê. Foi nas aulas de História que percebi por que razão o meu avô emigrou para França nos anos sessenta: aquilo que em casa era apenas uma memória de família passou a fazer parte da história de um país pobre e fechado. O conhecimento alargou, assim, uma experiência que eu julgava só nossa.',
     'Segundo argumento, distinto do primeiro, com o seu exemplo. Parâmetro C: parágrafo novo para uma ideia nova; «Por outro lado» e «assim» ligam as frases; «aquilo que em casa era apenas uma memória» retoma a emigração do avô sem repetir as palavras.'),
    ('Em suma, opor a escola à vida é um erro que empobrece as duas. Quem só confia no que viveu vê pouco; quem só repete o que estudou vê de longe. É do encontro entre ambas que nasce um olhar mais largo e mais justo sobre o mundo.',
     'Conclusão ligada à argumentação: volta ao ponto de vista e fecha com um juízo de valor («é um erro»).'),
]
N_MODELO = sum(len(a.split()) for a, _ in MODELO)
assert 200 <= N_MODELO <= 350, N_MODELO
modelo = ''.join('<div class="anot"><p class="c">%s</p><p class="n">%s</p></div>' % (a, b) for a, b in MODELO)

SEG = 'defenda uma perspetiva pessoal sobre o contributo das experiências pessoais e dos conhecimentos adquiridos na escola para o enriquecimento da visão que cada indivíduo constrói do mundo.'
assert SEG in IT['enunciado'][1]
TOK = [{'x': w} for w in SEG.split()]
assert TOK[8]['x'] == 'experiências' and TOK[12]['x'] == 'conhecimentos' and TOK[15]['x'] == 'escola' and len(TOK) == 27

PLANO = [
    {'id': 'pv', 'rotulo': 'O meu ponto de vista (uma frase)', 'linhas': 2},
    {'id': 'a1', 'rotulo': 'Argumento 1', 'linhas': 2},
    {'id': 'e1', 'rotulo': 'Exemplo que ilustra o argumento 1', 'linhas': 2},
    {'id': 'a2', 'rotulo': 'Argumento 2', 'linhas': 2},
    {'id': 'e2', 'rotulo': 'Exemplo que ilustra o argumento 2', 'linhas': 2},
    {'id': 'co', 'rotulo': 'A ideia da conclusão', 'linhas': 2},
]

EXC = ('<div class="caixa of">' + etq('oficial') + '<p><b>Excertos do enunciado e dos critérios</b> (a grelha completa está no passo 5).</p><ul class="top">'
       '<li>Enunciado, p. 8: «' + md(IT['enunciado_lista'][0]) + '»</li>'
       '<li>Enunciado, p. 8: «' + md(IT['enunciado_lista'][1]) + '»</li>'
       '<li>Parâmetro B, nível 4 (critérios, p. 15): «' + md(PB_['niveis'][0]['descritores'][0][1]) + '»</li>'
       '<li>Parâmetro C, nível 4 (critérios, p. 15): «' + md(PC['niveis'][0]['descritores'][0][3]) + '»</li>'
       '<li>Critérios, p. 14: «' + md(PA['nota']).replace('<b>', '').replace('</b>', '') + '»</li></ul></div>')
assert 'argumentos e de exemplos diversificados e pertinentes' in PB_['niveis'][0]['descritores'][0][1]
assert 'mecanismos de articulação interfrásica' in PC['niveis'][0]['descritores'][0][3]

TREINO = {
    'id': 'escrita', 'viu': 'os critérios',
    'passos': [
        {
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido', 'apoio': 'item', 'apoioRot': 'O item oficial',
            'o': 'Lê o enunciado inteiro, incluindo a lista e as observações. Depois responde a duas perguntas sobre o que ele manda.',
            'blocos': [
                {'t': 'escolha', 'id': 'p3-pedido', 'etq': 'treino', 'curto': 'O que o enunciado manda pôr no texto',
                 'p': 'O que tem de aparecer no teu texto para cumprires o enunciado?',
                 'o': [
                     {'t': 'Uma descrição das experiências pessoais e dos conhecimentos da escola, sem tomar partido.',
                      'pista': '<p>Procura no enunciado o verbo que te diz o que fazer e o que vem logo a seguir a ele.</p>'},
                     {'t': 'Um ponto de vista claro, dois argumentos, um exemplo para cada argumento, um discurso valorativo e uma conclusão.', 'pista': ''},
                     {'t': 'Um ponto de vista, três argumentos e uma conclusão que resuma o texto.',
                      'pista': '<p>Conta no primeiro ponto da lista do enunciado: quantos argumentos? E o que acompanha cada um deles?</p>'},
                     {'t': 'Uma opinião sobre o que devia mudar na escola de hoje.',
                      'pista': '<p>Relê o tema: fala do contributo de duas coisas para a visão do mundo. Que duas coisas são? As mudanças na escola são uma delas?</p>'},
                 ], 'c': 1,
                 'pista2': '<p>Lê os três pontos da lista do enunciado, um de cada vez, e conta o que cada um pede. O primeiro ponto pede mais do que uma coisa: separa-as.</p>',
                 'f': '<p>A lista do enunciado tem três pontos, mas são cinco coisas: o ponto de vista, dois argumentos, um exemplo significativo para cada um, um discurso valorativo e uma conclusão. São as mesmas cinco que o nível mais alto do parâmetro A enumera (critérios, p. 14; a grelha completa está no passo 5).</p>'},
                {'t': 'html', 'h': '<div class="caixa of">' + etq('oficial') + '<p><b>Limites de extensão</b> (critérios gerais, p. 3; ' + lig('c2', 'PDF em eduqa.pt') + ').</p><p>' + R_DESC + '</p><p>' + R_80 + '</p><p>' + R_CONTA + '</p></div>'},
                {'t': 'escolha', 'id': 'p3-limites', 'etq': 'treino', 'curto': 'O que acontece a um texto com 196 palavras',
                 'p': 'Imagina que o teu texto tem 196 palavras. O que dizem os critérios?',
                 'o': [
                     {'t': 'É classificado com zero pontos, porque não chega às duzentas palavras.',
                      'pista': '<p>Procura, na regra da p. 3, o número de palavras abaixo do qual o texto tem zero pontos. É duzentas?</p>'},
                     {'t': 'Descontam-se 5 pontos: qualquer desvio custa o máximo.',
                      'pista': '<p>Relê a primeira frase da regra: quanto se desconta por cada palavra? Depois conta quantas palavras faltam a 196 para chegar a 200.</p>'},
                     {'t': 'Não acontece nada: 196 arredonda para 200.',
                      'pista': '<p>Procura na regra da p. 3 alguma margem ou arredondamento. Depois conta quantas palavras faltam.</p>'},
                     {'t': 'Descontam-se 4 pontos: um por cada palavra em falta.', 'pista': ''},
                 ], 'c': 3,
                 'pista2': '<p>A regra tem duas frases. A primeira fala de um desconto por cada palavra, com um máximo; a segunda fala de oitenta palavras. Vê em qual das duas cabe um texto de 196 palavras e faz a conta.</p>',
                 'f': '<p>Faltam 4 palavras para as 200: descontam-se 4 pontos, «depois de aplicados todos os critérios definidos para o item». Com 353 palavras, descontam-se 3. Com 150, o desconto fica no máximo, que é 5. Abaixo de 80, o texto tem zero pontos.</p><p>A contagem é por sequências entre espaços: «dir-se-ia» conta como uma palavra e «2026» também.</p>'},
            ],
        },
        {
            'id': 'planear', 'curto': 'Localizar e planear', 'titulo': 'Localizar o tema e planear', 'apoio': 'item', 'apoioRot': 'O item oficial',
            'o': 'Primeiro, o tema exato. Depois, o teu plano.',
            'blocos': [
                {'t': 'tocar', 'id': 'p3-tema', 'etq': 'treino', 'modo': 'palavras', 'curto': 'As duas coisas cujo contributo o tema manda discutir',
                 'p': 'Nesta parte do enunciado, toca nas palavras que dizem as duas coisas cujo contributo tens de discutir. Podes tocar só no nome principal de cada uma ou no grupo inteiro. Depois toca em «Verificar».',
                 'tokens': TOK, 'nucleos': [[8, 12]], 'permitidos': [7, 8, 9, 10, 11, 12, 13, 14, 15], 'mostra': [8, 9, 12, 13, 14, 15],
                 'pistas': [
                     {'se': list(range(16, 27)), 'x': '<p>Tocaste naquilo para que as duas coisas contribuem: o enriquecimento da visão do mundo. Procura o que contribui: vem logo depois de «o contributo».</p>'},
                     {'se': list(range(0, 7)), 'x': '<p>Essas palavras dizem o que tens de fazer (defender uma perspetiva) e anunciam o assunto. Procura as duas coisas que vêm depois de «o contributo», ligadas por «e».</p>'},
                 ],
                 'falta': '<p>Estás no sítio certo, mas falta uma das duas coisas: o enunciado liga-as com «e».</p>',
                 'pista2': '<p>Lê só o que está entre «o contributo» e «para o enriquecimento». São dois grupos de palavras ligados por «e»: toca no nome principal de cada um.</p>',
                 'f': '<p>«experiências pessoais» e «conhecimentos adquiridos na escola». O tema junta as duas coisas. Um texto que só fale de uma arrisca-se a ser lido como tratando o tema com desvios, o que pesa no parâmetro B (critérios, p. 15).</p><p class="pag">Leitura nossa: os critérios não dizem o que conta como desvio; quem decide é o classificador.</p>'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). Um parágrafo para dizer o ponto de vista; um parágrafo para cada argumento, com o seu exemplo; um parágrafo para concluir.</p>'
                 '<p>Os critérios pedem os cinco elementos (parâmetro A, p. 14) e um texto com «diferentes partes, devidamente proporcionadas e articuladas entre si», com os parágrafos bem marcados (parâmetro C, p. 15). Não fixam o número de parágrafos nem o sítio onde fica o ponto de vista. Outras organizações contam do mesmo modo, se cumprirem o que se pede.</p></div>'},
                {'t': 'campos', 'id': 'p3-plano', 'titulo': 'O teu plano',
                 'intro': '<p class="ajuda">Notas curtas, só para ti. Ficam guardadas neste dispositivo e podes abri-las enquanto escreves. Também podes planear no papel.</p>',
                 'campos': PLANO},
            ],
        },
        {
            'id': 'distinguir', 'curto': 'Insuficiente ou adequado', 'titulo': 'Distinguir um parágrafo insuficiente de um adequado', 'apoio': 'item', 'apoioRot': 'O item oficial',
            'o': 'Dois parágrafos de desenvolvimento para este tema. Os dois têm um argumento e um exemplo.',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p><b>Parágrafo A.</b> <span class="cit">' + PAR_A + '</span></p><p><b>Parágrafo B.</b> <span class="cit">' + PAR_B + '</span></p></div>' + EXC},
                {'t': 'escolha', 'id': 'p3-distinguir', 'etq': 'treino', 'curto': 'O parágrafo que fica aquém, e porquê',
                 'p': 'Que parágrafo fica aquém do que o enunciado e os critérios pedem, e porquê?',
                 'o': [
                     {'t': 'O Parágrafo A: não começa por um conector.',
                      'pista': '<p>Procura a palavra «conector» nos excertos dos critérios, aqui em cima. O que lá está é «mecanismos de articulação interfrásica». Vê se o Parágrafo A tem algum.</p>'},
                     {'t': 'O Parágrafo B: está na primeira pessoa e conta um caso da vida de quem escreve.',
                      'pista': '<p>Relê o enunciado: pede uma «perspetiva pessoal» e, para cada argumento, «um exemplo significativo». Procura nos excertos alguma frase que proíba a primeira pessoa ou os casos vividos.</p>'},
                     {'t': 'O Parágrafo A: o exemplo é geral e não mostra de que maneira a experiência muda a visão do mundo.', 'pista': ''},
                     {'t': 'O Parágrafo A: dá uma opinião («toda a gente devia viajar mais»).',
                      'pista': '<p>Vê o segundo ponto da lista do enunciado. Um juízo de valor é um defeito ou é o que se pede?</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Põe lado a lado os exemplos dos dois parágrafos: as viagens, no A; o voluntariado num lar, no B. Procura em cada um a frase que diz o que mudou na maneira de ver de quem escreve.</p>',
                 'f': '<p>No Parágrafo A, o argumento repete o tema por outras palavras e o exemplo («viajar») não diz o que muda em quem viaja. No Parágrafo B, o argumento diz o que as experiências dão (o encontro com pessoas concretas) e o exemplo mostra uma mudança na maneira de ver, ligando a experiência ao que se estudou nas aulas.</p>'
                      '<p>O enunciado pede um «exemplo significativo» para cada argumento, e o parâmetro B valoriza «a mobilização de argumentos e de exemplos diversificados e pertinentes» (critérios, p. 15).</p>'
                      '<p class="pag">Esta comparação é leitura nossa: os critérios do Grupo III não trazem tópicos de conteúdo nem exemplos de resposta.</p>'},
            ],
        },
        {
            'id': 'escrever', 'curto': 'O teu texto', 'titulo': 'Escrever o teu texto, sem pistas', 'apoio': 'item', 'apoioRot': 'O item oficial',
            'o': 'Agora és tu. Tens o enunciado ao lado e o teu plano. Os parágrafos A e B e as explicações ficam nos passos anteriores.',
            'blocos': [
                {'t': 'vercampos', 'id': 'p3-plano', 'titulo': 'Ver o meu plano', 'vazio': 'Não escreveste o plano aqui. Se o fizeste no papel, tem-no à tua frente.', 'campos': PLANO},
                {'t': 'escrever', 'id': 'p3-texto', 'curto': 'Texto de opinião (200 a 350 palavras)', 'rotulo': 'O teu texto de opinião', 'linhas': 18, 'conta': True,
                 'ajuda': 'Escreve aqui ou no papel, como na prova. A caixa não corrige nem classifica: só conta as palavras, pela regra dos critérios. Os limites estão no enunciado (p. 8) e a regra da extensão no passo 1 (critérios, p. 3): és tu que a aplicas.',
                 'papel': 'Escrevi no papel (no caderno). Deixo a caixa vazia e conto as palavras à mão.'},
            ],
        },
        {
            'id': 'grelha', 'curto': 'Rever com a grelha', 'titulo': 'Rever o teu texto com a grelha oficial, critério a critério', 'apoio': 'item', 'apoioRot': 'O item oficial', 'precisa': 'p3-texto',
            'o': 'Lê a tua primeira versão quatro vezes, uma por critério, e marca aspeto a aspeto o que lá encontras. A página não classifica nem faz contas por ti: as regras oficiais estão à vista, com a página, para as aplicares; quem classifica é o docente.',
            'blocos': [
                {'t': 'ver1', 'de': 'p3-texto', 'conta': True, 'linhas': 18},
                {'t': 'html', 'h': '<h3>1. Género e formato (parâmetro A)</h3>' + par_bloco(PA, '14')},
                {'t': 'grelha', 'id': 'p3-gA', 'intro': '<p class="ajuda">Os cinco aspetos do nível 4. Para cada um, procura no teu texto a frase que o cumpre. Os descritores dos outros níveis ficam na tabela, para consultares.</p>', 'aspetos': aspetos(PA), 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>2. Tema e pertinência da informação (parâmetro B)</h3>' + par_bloco(PB_, '15')},
                {'t': 'grelha', 'id': 'p3-gB', 'intro': '<p class="ajuda">Antes dos três aspetos, a pergunta de entrada do parâmetro: o teu texto trata o tema proposto sem desvios? Por exemplo: fala das duas coisas que o enunciado junta? (O exemplo é leitura nossa.)</p>',
                 'aspetos': ['trata o tema proposto sem desvios'] + aspetos(PB_), 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>3. Organização e coesão textuais (parâmetro C)</h3>' + par_bloco(PC, '15') +
                 '<p class="pag">O critério fala em «mecanismos de articulação interfrásica». Os conectores são um desses mecanismos; a pontuação e a retoma de palavras também ligam frases. Leitura nossa.</p>'},
                {'t': 'grelha', 'id': 'p3-gC', 'aspetos': aspetos(PC), 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>4. Correção linguística (CL)</h3><div class="caixa of">' + etq('oficial') + '<p><b>' + CR['CL']['nome'] + ' (CL): 14 pontos.</b> <span class="pag">Critérios, p. 16; tipologia de erros, pp. 2-3.</span></p><p>' + md(CR['CL']['texto']) + '</p>'
                 '<p><b>Tipo A:</b> «erro inequívoco de pontuação»; «erro de ortografia (incluindo erro de acentuação, erro de translineação e uso indevido de letra minúscula ou de letra maiúscula)»; «erro de morfologia»; «incumprimento das regras de citação de texto ou de referência a título de uma obra». <b>Tipo B:</b> «erro de sintaxe»; «impropriedade lexical». <span class="pag">(Quadro 1, p. 2)</span></p>'
                 '<p>' + R_UMA + ' <span class="pag">(critérios gerais, p. 3)</span></p>'
                 + tabela_cl('CL_14') + '</div>'
                 '<p>Relê o texto devagar, só à procura de erros. Conta-os no papel, em duas colunas: os do tipo A e os do tipo B. A mesma palavra repetida com o mesmo erro de ortografia conta uma vez, e vários erros na mesma palavra também contam uma vez. Os outros erros contam sempre que aparecem.</p>'
                 '<p>Depois lê tu a tabela: a linha é o número de erros do tipo B e a coluna é o número de erros do tipo A. A página não faz esta leitura por ti.</p>'},
                {'t': 'html', 'h': '<h3>5. As regras que tiram pontos</h3><p class="ajuda">Conta as palavras do teu texto (a contagem da caixa segue a regra dos critérios) e aplica tu estas regras. A página não calcula descontos.</p><div class="caixa of">' + etq('oficial') +
                 '<p><b>Extensão</b> (critérios gerais, p. 3). ' + R_DESC + ' ' + R_80 + ' ' + R_CONTA + '</p>'
                 '<p><b>Zero em A ou em B</b> (critérios gerais, p. 2). ' + R_ZERO + '</p>'
                 '<p><b>Maiúsculas</b> (critérios gerais, p. 3). ' + R_MAI + '</p></div>'
                 '<h3>Um exemplo comentado</h3><p class="ajuda">Um texto possível, escrito por nós, com ' + str(N_MODELO) + ' palavras. Não é oficial nem é um modelo para decorar: os critérios do Grupo III não trazem exemplos de resposta. Usa-o para veres onde está cada aspeto da grelha.</p>' + modelo +
                 '<div class="caixa of">' + etq('oficial') + '<p><b>Outras formulações também contam.</b> ' + R_ALT + ' <span class="pag">(critérios gerais, p. 2)</span></p></div>'},
            ],
        },
        {
            'id': 'rever', 'curto': 'Reescrever', 'titulo': 'Reescrever', 'apoio': 'item', 'apoioRot': 'O item oficial', 'precisa': 'p3-texto',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres os critérios, a página diz isso junto dela. Na versão revista, muda o que marcaste como «com falhas» ou «não está» e corrige os erros que contaste.',
            'blocos': [
                {'t': 'rever', 'de': 'p3-texto', 'curto': 'Versão revista do texto de opinião', 'linhas': 18, 'conta': True},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Sobre 2027.</b> Este item e esta grelha são de 2026. Nesse ano, a 1.ª fase pediu uma apreciação crítica de um <i>cartoon</i> e a 2.ª fase este texto de opinião, as duas com 200 a 350 palavras e 44 pontos. O género, os limites de palavras, os descontos e a grelha de 2027 estão a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        },
    ],
}

CAB = (
    '<p class="sobre">Treino 3 de 3. Escrita com correção</p>'
    '<h1>Um texto de opinião, da leitura do pedido à segunda versão</h1>'
    '<p class="lede">O item de resposta extensa da 2.ª fase de 2026, seis passos e duas versões do teu texto. Liga-se à ' + sessao('s24', 'Opinião: uma posição que resiste à revisão') + ' e ao seu ' + aquecimento('s24') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Escrever um texto de opinião de 200 a 350 palavras que cumpra o enunciado, e revê-lo com os parâmetros oficiais de classificação.</dd></div>'
    '<div><dt>Item oficial a que se liga</dt><dd>Prova 639, 2026, 2.ª fase, Grupo III (resposta extensa, 44 pontos). ' + lig('e2', 'Enunciado, p. 8 (PDF em eduqa.pt)') + '; ' + lig('c2', 'critérios, pp. 2-3 e 14-16 (PDF em eduqa.pt)') + '. Critérios definitivos, publicados a 31/07/2026.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<p class="pag">O enunciado oficial fica sempre ao lado dos passos, inteiro. A grelha oficial completa (parâmetros A, B e C, tabela de correção linguística e regras gerais) está no passo 5, com a página de cada parte.</p>'
)

NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB
for s in [R_DESC, R_80, R_CONTA, R_ZERO, R_MAI, R_ALT, R_UMA, EXC, md(CR['CL']['texto'])] + [par_bloco(p, x) for p, x in ((PA, '14'), (PB_, '15'), (PC, '15'))] + aspetos(PA) + aspetos(PB_) + aspetos(PC):
    NOSSO = NOSSO.replace(json.dumps(s, ensure_ascii=False)[1:-1], '').replace(s, '')


def construir():
    lint('escrita', NOSSO)
    return pagina_treino('escrita', 'escrita/', 'Escrita', 'Treino 3: um texto de opinião | Português',
                         'Treino da preparação de exame de Português: resposta extensa, um texto de opinião em duas versões, com a grelha oficial de 2026.', CAB, {'item': AP_ITEM}, TREINO)

