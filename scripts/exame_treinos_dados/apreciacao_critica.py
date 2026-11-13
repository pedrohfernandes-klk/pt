"""13/11/2026: treino 7, «Uma apreciação crítica, da imagem à segunda versão» (exame/treinos/apreciacao-critica/), ligado à sessão 25.

O item oficial é o Grupo III da 1.ª fase de 2026: a apreciação crítica de um cartoon de Javad Takjoo. A imagem da prova tem
direitos de autor e NÃO se reproduz: a página liga ao enunciado em eduqa.pt (p. 13) e trabalha com outra imagem, em domínio
público, que o repositório já publica com crédito completo (img/fontes/licoes-20261101/piranesi.jpg, registada em
scripts/imagens_licoes_20261101.py e usada na lição M9-F14). O enunciado, a grelha, a tabela e as regras gerais vêm da
transcrição, letra a letra. O que se diz da gravura é descrição nossa do que se vê nela.
"""
import importlib.util
from .base import *
from .escrita import oficial, R_DESC, R_80, R_CONTA, R_ZERO, R_MAI, R_UMA, R_ALT, aspetos, par_bloco, OPG

IT = F1['grupos'][2]['itens'][0]
CR = IT['criterios']
IT2 = F2['grupos'][2]['itens'][0]
assert IT['numero'] == 'III' and IT['obrigatorio'] is True and ['III', 44] in F1['cotacoes']['obrigatorios']['itens']
assert IT['cotacao'] == 44 and CR['ETD']['pontos'] == 30 and CR['CL']['pontos'] == 14
assert IT['extensao'] == {'min_palavras': 200, 'max_palavras': 350, 'minimo_para_classificar': 80} == IT2['extensao']
assert IT['imagem']['pagina_da_prova'] == 13 and IT['imagem']['autor'] == 'Javad Takjoo' and IT['imagem']['fonte'] == 'https://takjoo.com (consultado em 23/02/2026).'
assert IT['genero'] == 'texto de apreciação crítica (de um _cartoon_)' and IT2['genero'].startswith('texto de opinião')
PA, PB_, PC = CR['ETD']['parametros']
assert [p['id'] for p in (PA, PB_, PC)] == ['A', 'B', 'C'] and all(p['pontos'] == 10 for p in (PA, PB_, PC))
for _p in (PA, PB_, PC):
    assert [(n['nivel'], n['pontuacao']) for n in _p['niveis']] == [(4, 10), (3, 8), (2, 5), (1, 3)]
# o parâmetro C e a correção linguística são os mesmos nas duas fases; A e B são os do género
assert PC == IT2['criterios']['ETD']['parametros'][2] and CR['CL'] == IT2['criterios']['CL']
assert PA != IT2['criterios']['ETD']['parametros'][0] and PB_ != IT2['criterios']['ETD']['parametros'][1]
GER = json.dumps(F1['criterios']['gerais'], ensure_ascii=False)
for _s in ['erro inequívoco de pontuação', 'erro de ortografia (incluindo erro de acentuação, erro de translineação e uso indevido de letra minúscula ou de letra maiúscula)', 'erro de morfologia',
           'incumprimento das regras de citação de texto ou de referência a título de uma obra', 'erro de sintaxe', 'impropriedade lexical']:
    assert _s in GER
assert 'não descrevem a imagem nem dão tópicos de conteúdo ou exemplos de resposta' in CR['nota_nossa']

# citações do enunciado e dos critérios usadas nos passos (todas tiradas da transcrição)
E_LISTA = IT['enunciado_lista']
assert len(E_LISTA) == 3 and E_LISTA[1] == 'um comentário crítico, fundamentando a sua apreciação em, pelo menos, três aspetos relevantes e utilizando um discurso valorativo;'
A4 = PA['niveis'][0]['descritores'][0]
assert len(A4) == 4 and A4[2] == 'um comentário crítico fundamentado em, pelo menos, três aspetos distintos, recorrendo a um discurso valorativo (juízo de valor explícito ou implícito);'
A_DESC = A4[1].rstrip(';')
A_COM = A4[2].rstrip(';')
A_CONC = A4[3].rstrip('.')
A3 = PA['niveis'][1]['descritores'][0][0]
A2 = PA['niveis'][2]['descritores'][0][0]
D_DOIS = 'mas fundamenta o comentário crítico em apenas dois aspetos distintos, assegurando os restantes aspetos em avaliação neste parâmetro.'
D_UM = 'mas fundamenta o comentário crítico em apenas um aspeto, assegurando os restantes aspetos em avaliação neste parâmetro.'
assert A3.endswith(D_DOIS) and A2.endswith(D_UM) and PA['niveis'][1]['pontuacao'] == 8 and PA['niveis'][2]['pontuacao'] == 5
B4 = PB_['niveis'][0]['descritores'][0]
B_ASP = B4[1].rstrip(';')
B_REG = B4[3].rstrip('.')
assert B_ASP == 'a mobilização de aspetos diversificados e pertinentes, tanto no que diz respeito à descrição da imagem como ao comentário crítico'
C4 = PC['niveis'][0]['descritores'][0]
C_PARTES = C4[1].rstrip(';')
C_ARTIC = C4[3].rstrip(';')
assert C_PARTES == 'apresenta um texto constituído por diferentes partes, devidamente proporcionadas e articuladas entre si de modo consistente'
assert C_ARTIC == 'utiliza, adequadamente, mecanismos de articulação interfrásica'
assert PA['nota'] == '**Nota ‒** A pertinência dos argumentos e dos exemplos é avaliada no parâmetro B.'

# ---------- a imagem do treino: domínio público, com o crédito do registo das imagens das lições ----------
_spec = importlib.util.spec_from_file_location('_imagens_licoes_20261101', ROOT + '/scripts/imagens_licoes_20261101.py')
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
IMG = dict(_mod.IMAGENS['piranesi'])
assert IMG == dict(autor='Giovanni Battista Piranesi', obra='Vista interior da Basílica de São Pedro, da série Vedute di Roma', data='Cerca de 1748',
                   instituicao='The Metropolitan Museum of Art, inventário 1972.620.1. Oferta de Mrs. Otto F. Langmann, 1972.',
                   licenca='Domínio público', direitos='https://www.metmuseum.org/art/collection/search/353966',
                   fonte='https://www.metmuseum.org/art/collection/search/353966',
                   alt='Gravura do interior da Basílica de São Pedro: pequenas figuras humanas entre colunas e abóbadas monumentais.'), IMG
assert _mod.__doc__.startswith('Documentos visuais inspecionados em 01/11/2026, com direitos verificados.') and _mod.USOS['m9-f14'][0] == 'piranesi'
IMG_FICHEIRO = 'img/fontes/licoes-20261101/piranesi.jpg'
assert os.path.isfile(ROOT + '/' + IMG_FICHEIRO)
_h9 = open(ROOT + '/m9/licao-m9-f14/index.html', encoding='utf-8').read()
assert 'piranesi.jpg' in _h9 and IMG['direitos'] in _h9 and 'Giovanni Battista Piranesi' in _h9
URL_IMG_PROVA = URL['e1'] + '#page=13'
LIG_IMG_PROVA = '<a href="%s" target="_blank" rel="noopener">%s</a>'
OBRA_HTML = IMG['obra'].replace('Vedute di Roma', '<i>Vedute di Roma</i>')
assert OBRA_HTML != IMG['obra']
CREDITOS_IMG = (
    '<details class="dobra"><summary>Créditos da imagem</summary><div class="dentro"><dl class="creditos-img">'
    '<dt>Autor</dt><dd>' + IMG['autor'] + '</dd>'
    '<dt>Obra</dt><dd>' + OBRA_HTML + '</dd>'
    '<dt>Data</dt><dd>' + IMG['data'] + '</dd>'
    '<dt>Instituição ou acervo</dt><dd>' + IMG['instituicao'] + '</dd>'
    '<dt>Licença</dt><dd>' + IMG['licenca'] + '. Fonte e direitos: <a href="' + IMG['fonte'] + '" target="_blank" rel="noopener">página da obra no sítio do museu (metmuseum.org)</a>.</dd>'
    '<dt>Reprodução</dt><dd>Redimensionada, sem recorte. É a mesma reprodução da <a href="../../../m9/licao-m9-f14/">lição M9-F14</a>.</dd>'
    '</dl></div></details>')

PEDIDO_1 = md(IT['enunciado'][0]).replace('faça', 'faz').replace('do <i>cartoon</i>, da autoria de Javad Takjoo', 'da gravura, da autoria de Giovanni Battista Piranesi')
assert PEDIDO_1 == 'Num texto bem estruturado, com um mínimo de duzentas e um máximo de trezentas e cinquenta palavras, faz a apreciação crítica da gravura, da autoria de Giovanni Battista Piranesi.'
assert IT['enunciado'][1] == 'No seu texto, deve incluir:'
LISTA_HTML = '<ul class="top enun">' + ''.join('<li>%s</li>' % md(x) for x in E_LISTA) + '</ul>'
PEDIDO = '<p class="enun">' + PEDIDO_1 + '</p><p class="enun">No teu texto, deves incluir:</p>' + LISTA_HTML
MUDOU = ('<p class="pag">O que mudou em relação ao item oficial: a imagem (na prova, um <i>cartoon</i> de Javad Takjoo, que tem direitos de autor e não está nesta página) e o tratamento por «tu». '
         'Os três pontos da lista e os limites de palavras são os da prova.</p>')
CX_PEDIDO = '<div class="caixa ad">' + etq('adaptado') + PEDIDO + MUDOU + '</div>'
ENUN_OF = ''.join('<p class="enun">%s</p>' % md(x) for x in IT['enunciado']) + LISTA_HTML
CX_OFICIAL = ('<div class="caixa of">' + etq('oficial') + ENUN_OF +
              '<p class="pag">Prova 639, 2026, 1.ª fase, versão 2, Grupo III. Resposta extensa, 44 pontos; conta sempre para a classificação. Enunciado, p. 13. '
              + (LIG_IMG_PROVA % (URL_IMG_PROVA, 'Ver a imagem da prova: enunciado, p. 13 (PDF em eduqa.pt)')) + '.</p></div>')

AP_IMG = (
    '<figure class="apoio-img"><a href="../../../' + IMG_FICHEIRO + '" target="_blank" rel="noopener"><img src="../../../' + IMG_FICHEIRO + '" width="800" height="551" alt="' + html.escape(IMG['alt']) + '"></a>'
    '<figcaption>Giovanni Battista Piranesi, vista interior da Basílica de São Pedro, cerca de 1748. A licença e a fonte estão em «Créditos da imagem», mais abaixo.</figcaption></figure>'
    '<div class="apoio-pedido"><p class="notas-t">O pedido de treino</p>' + etq('adaptado') + PEDIDO + '</div>'
    '<p class="pag apoio-fim">Toca na imagem para a abrires maior, noutro separador. Na prova, a imagem é outra: um <i>cartoon</i> de Javad Takjoo, que tem direitos de autor e não está nesta página. '
    + (LIG_IMG_PROVA % (URL_IMG_PROVA, 'Vê-o no enunciado, p. 13 (PDF em eduqa.pt)')) + '.</p>'
    + CREDITOS_IMG)

obs = ''
for _o in IT['observacoes']:
    if isinstance(_o, str):
        obs += '<li>%s</li>' % md(_o)
    else:
        obs += '<li>%s<ul class="top">%s</ul></li>' % (md(_o['texto']), ''.join('<li>%s</li>' % md(x) for x in _o['lista']))
OFICIAL = (
    '<p>' + etq('oficial') + '</p>'
    '<p class="pag">Exame Final Nacional de Português, Prova 639, 2026, 1.ª fase, versão 2. Grupo III (resposta extensa, 44 pontos; conta sempre para a classificação). '
    'Item: enunciado, p. 13; critérios de classificação, pp. 2-3 e 14-16 (definitivos, atualizados a 10/07/2026). '
    + lig('e1', 'Enunciado (PDF, eduqa.pt)') + ' e ' + lig('c1', 'critérios (PDF, eduqa.pt)') + '.</p>'
    + ENUN_OF +
    '<p class="pag">A imagem do item, um <i>cartoon</i> de Javad Takjoo, tem direitos de autor e não se reproduz aqui: ' + (LIG_IMG_PROVA % (URL_IMG_PROVA, 'está no enunciado, p. 13 (PDF em eduqa.pt)')) + '. '
    'A prova indica assim a fonte da imagem: ' + esc(IT['imagem']['fonte']) + '</p>'
    '<p><b>Observações:</b></p><ol class="top menor">' + obs + '</ol>'
    '<p class="pag">Cotação: 44 pontos. Estruturação temática e discursiva, 30 (parâmetros A, B e C, 10 cada); correção linguística, 14 (critérios, pp. 14-16). A grelha completa está no passo 5.</p>'
)

SEG = E_LISTA[1]
TOK = [{'x': w} for w in SEG.split()]
assert len(TOK) == 18 and [TOK[i]['x'] for i in (8, 9, 10, 11, 12, 15)] == ['pelo', 'menos,', 'três', 'aspetos', 'relevantes', 'um']

PAR_A = 'A gravura é espetacular e gostei muito dela. As pessoas são muito pequenas e a igreja é enorme, o que é impressionante. Piranesi era um grande artista.'
PAR_B = ('O aspeto mais conseguido da gravura é a escala. Piranesi espalha pela nave figuras humanas minúsculas, que quase desaparecem ao pé dos pilares. '
         'Sem elas, não teríamos medida para a altura das abóbadas; com elas, o edifício torna-se esmagador. É uma solução eficaz, porque a grandeza não é afirmada: vê-se.')

EXC = ('<div class="caixa of">' + etq('oficial') + '<p><b>Excertos do enunciado e dos critérios</b> (a grelha completa está no passo 5).</p><ul class="top">'
       '<li>Enunciado, p. 13: «' + md(E_LISTA[1]) + '»</li>'
       '<li>Parâmetro A, nível 4 (critérios, p. 14): «' + md(A4[2]) + '»</li>'
       '<li>Parâmetro B, nível 4 (critérios, p. 15): «' + md(B4[1]) + '»</li>'
       '<li>Parâmetro B, nível 4 (critérios, p. 15): «' + md(B4[3]) + '»</li></ul></div>')

PLANO = [
    {'id': 'de', 'rotulo': 'O que vou destacar na descrição (dois ou três elementos)', 'linhas': 2},
    {'id': 'jg', 'rotulo': 'O meu juízo global (uma frase)', 'linhas': 2},
    {'id': 'a1', 'rotulo': 'Aspeto 1: o que se vê e o efeito', 'linhas': 2},
    {'id': 'a2', 'rotulo': 'Aspeto 2: o que se vê e o efeito', 'linhas': 2},
    {'id': 'a3', 'rotulo': 'Aspeto 3: o que se vê e o efeito', 'linhas': 2},
    {'id': 'co', 'rotulo': 'A ideia da conclusão', 'linhas': 2},
]

MODELO = [
    ('A gravura de Giovanni Battista Piranesi mostra o interior da Basílica de São Pedro, visto em diagonal a partir da nave. À esquerda, em primeiro plano, erguem-se pilares em sombra e arcos que abrem para uma nave lateral; '
     'por cima, uma abóbada de caixotões avança até ao fundo, onde um altar coberto por um dossel alto aparece numa zona de luz. Pelo chão, largo e claro, espalham-se pequenos grupos de figuras humanas.',
     'Parâmetro A: a descrição. Não diz tudo o que lá está: destaca o ponto de vista, os pilares, a abóbada, o altar e as figuras, que voltam no comentário.'),
    ('O aspeto mais conseguido é a escala. As figuras, minúsculas ao pé dos pilares, dão a medida do edifício: é por elas que percebemos a altura das abóbadas. A grandeza não é dita, vê-se, e essa é uma escolha muito eficaz.',
     'Primeiro aspeto: o pormenor, o efeito e um juízo de valor explícito («muito eficaz»).'),
    ('Também a perspetiva está bem resolvida. As linhas da cornija e da abóbada convergem para o fundo e conduzem o olhar até ao altar. Num espaço tão carregado de ornamentos, esta condução dá ordem à imagem e impede que o observador se perca.',
     'Segundo aspeto, distinto do primeiro. Parâmetro C: parágrafo novo para uma ideia nova; «Também» liga ao parágrafo anterior e «esta condução» retoma sem repetir as palavras.'),
    ('Por fim, o contraste entre claro e escuro, obtido apenas com traços pretos sobre o papel, dá profundidade à cena: as zonas de sombra do primeiro plano fazem recuar o fundo iluminado. '
     'Reconheço, porém, um limite: a minúcia dos ornamentos é tanta que, em alguns pontos, cansa o olhar.',
     'Terceiro aspeto e uma reserva. A reserva não é pedida pelo item: é uma proposta da sessão 25 (orientação nossa). Vem fundamentada e não desfaz o juízo favorável.'),
    ('Em suma, com figuras mínimas, linhas que guiam o olhar e um contraste seguro de luz e sombra, Piranesi faz mais do que registar um edifício: faz sentir o seu tamanho. '
     'É essa capacidade de transformar medida em impressão que torna a gravura admirável.',
     'Conclusão adequada aos pontos de vista desenvolvidos: retoma os três aspetos e fecha o juízo global.'),
]
N_MODELO = sum(len(a.split()) for a, _ in MODELO)
assert 200 <= N_MODELO <= 350, N_MODELO
modelo = ''.join('<div class="anot"><p class="c">%s</p><p class="n">%s</p></div>' % (a, b) for a, b in MODELO)

AP = {'apoio': 'img', 'apoioRot': 'A imagem e o pedido'}

TREINO = {
    'id': 'apreciacao-critica', 'viu': 'os critérios',
    'passos': [
        dict(AP, **{
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido',
            'o': 'Lê o pedido de treino e o enunciado oficial de onde ele vem. Depois responde a duas perguntas sobre o que mandam.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO + '<p>O pedido de treino vem deste item da 1.ª fase de 2026:</p>' + CX_OFICIAL},
                {'t': 'escolha', 'id': 'p7-pedido', 'etq': 'treino', 'curto': 'O que o pedido manda pôr no texto',
                 'p': 'O que tem de aparecer no teu texto para cumprires o pedido?',
                 'o': [
                     {'t': 'Um resumo de tudo o que a gravura mostra, da esquerda para a direita, sem tomares partido sobre o que lá vês.',
                      'pista': '<p>Relê o segundo ponto da lista: que palavra vem depois de «comentário»? E que discurso manda usar?</p>'},
                     {'t': 'A tua opinião sobre as grandes igrejas, com dois argumentos, um exemplo para cada argumento e uma conclusão.',
                      'pista': '<p>Isso é o que pede um texto de opinião sobre um tema. Vê qual é o objeto deste pedido: um tema ou uma imagem? Depois conta o que a lista manda incluir.</p>'},
                     {'t': 'Uma descrição que destaque elementos da imagem, um comentário crítico apoiado em três aspetos ou mais, com juízos de valor, e uma conclusão.',
                      'pista': ''},
                     {'t': 'Uma descrição completa da imagem, com tudo o que lá está, e uma frase final a dizer se gostas dela ou não.',
                      'pista': '<p>Conta, no segundo ponto da lista, em quantos aspetos se apoia o comentário. Uma frase de gosto chega para isso?</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Lê os três pontos da lista, um de cada vez. O primeiro tem um gerúndio que diz como se descreve; o segundo pede duas coisas ao comentário; o terceiro diz a que tem de se ajustar a conclusão.</p>',
                 'f': '<p>São três partes e uma maneira de dizer: a descrição, o comentário crítico (com discurso valorativo) e a conclusão. São as mesmas que o nível mais alto do parâmetro A enumera: «' + A_DESC + '»; «' + A_COM + '»; «' + A_CONC + '» '
                      '<span class="pag">(critérios, p. 14; a grelha completa está no passo 5)</span>.</p>'
                      '<p>Uma apreciação seleciona características, analisa-as e sustenta uma avaliação; não se limita a contar o que lá está.</p>'},
                {'t': 'tocar', 'id': 'p7-quantos', 'etq': 'treino', 'modo': 'palavras', 'curto': 'O número mínimo de aspetos do comentário',
                 'p': 'Neste ponto do enunciado, toca na palavra (ou nas palavras) que dizem em quantos aspetos, no mínimo, tens de apoiar o comentário. Depois toca em «Verificar».',
                 'tokens': TOK, 'nucleos': [[10]], 'permitidos': [8, 9, 10, 11, 12], 'mostra': [8, 9, 10],
                 'notas': {'8': 'Aceite com «pelo menos»: diz que três é o mínimo, não o número certo.', '9': 'Aceite com «pelo menos»: diz que três é o mínimo, não o número certo.',
                           '11': 'Aceite com «aspetos relevantes»: é aquilo que se conta.', '12': 'Aceite com «aspetos relevantes»: é aquilo que se conta.'},
                 'pistas': [
                     {'so': [8, 9], 'x': '<p>«pelo menos» diz que há um mínimo. Falta o número: vem logo a seguir.</p>'},
                     {'so': [8, 9, 11, 12], 'x': '<p>Estás no sítio certo, mas falta o número: está entre «pelo menos» e «aspetos».</p>'},
                     {'se': [0, 1, 2], 'x': '<p>«um comentário crítico» diz o que tens de escrever. A pergunta é por um número: procura mais à frente.</p>'},
                     {'se': [15], 'x': '<p>Esse «um» é um artigo, antes de «discurso valorativo»: não conta aspetos. Procura o numeral que vem antes de «aspetos».</p>'},
                     {'se': [3, 4, 5, 6, 7], 'x': '<p>Essas palavras dizem o que o comentário faz: fundamenta a apreciação. O número vem logo depois.</p>'},
                     {'se': [13, 14, 16, 17], 'x': '<p>Essas palavras pedem o discurso valorativo. O número de aspetos está antes de «e».</p>'},
                 ],
                 'falta': '<p>Procura um numeral neste ponto do enunciado.</p>',
                 'pista2': '<p>Lê só o que está entre as duas vírgulas a meio da frase e a palavra que vem logo depois. São três palavras: as duas primeiras dizem que há um mínimo; a terceira é o número.</p>',
                 'f': '<p>«três», com «pelo menos». O parâmetro A conta-os. Com três aspetos distintos ou mais, e o resto assegurado, o descritor é o do nível 4 (10 pontos). O do nível 3 (8 pontos) diz: «[…] ' + D_DOIS + '» '
                      'E o do nível 2 (5 pontos): «[…] ' + D_UM + '» <span class="pag">(critérios, p. 14)</span></p>'
                      '<p>Repara nas palavras: o enunciado diz «três aspetos relevantes» (p. 13); o parâmetro A diz «três aspetos distintos» (p. 14). Têm de ser três, têm de importar e têm de ser diferentes uns dos outros.</p>'
                      '<p>A sessão 25 pede duas características. Aqui segue-se o item, que pede pelo menos três.</p>'
                      '<p class="pag">Leitura nossa: os critérios não dizem o que conta como aspeto distinto; quem decide é o classificador.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'planear', 'curto': 'Olhar e planear', 'titulo': 'Olhar para a imagem e planear',
            'o': 'Primeiro, o que se vê e o que vale a pena destacar. Depois, o teu plano.',
            'blocos': [
                {'t': 'escolha', 'id': 'p7-descricao', 'etq': 'treino', 'curto': 'A frase que descreve destacando',
                 'p': 'Que frase descreve a gravura destacando um elemento significativo da composição?',
                 'o': [
                     {'t': 'A gravura é impressionante e muito bem feita, com imensos pormenores em toda a parte.',
                      'pista': '<p>Procura na frase uma coisa que se veja na gravura: uma forma, uma figura, um lugar. Encontras alguma?</p>'},
                     {'t': 'Junto ao chão, figuras humanas muito pequenas atravessam a nave, entre pilares que ocupam quase toda a altura da imagem.',
                      'pista': ''},
                     {'t': 'A Basílica de São Pedro é uma das maiores igrejas do mundo e recebe visitantes de muitos países.',
                      'pista': '<p>Essa frase fala do edifício real. O pedido é «a descrição da imagem apresentada»: o que se vê nesta gravura?</p>'},
                     {'t': 'Há pilares, arcos, uma abóbada, janelas, medalhões, estátuas, um altar, pessoas e uma legenda.',
                      'pista': '<p>A frase enumera tudo por igual. Relê o primeiro ponto do pedido: depois de «a descrição da imagem apresentada» vem um gerúndio. O que manda fazer?</p>'},
                 ], 'c': 1,
                 'pista2': '<p>Faz duas perguntas a cada frase. Fala do que se vê nesta gravura? Escolhe uma coisa e diz onde está e como se relaciona com o resto? Só uma responde que sim às duas.</p>',
                 'f': '<p>A frase escolhe um elemento (as figuras), diz onde está e põe-no em relação com outro (os pilares). Das outras, uma julga sem mostrar, outra fala do edifício e não da imagem, e outra faz uma lista.</p>'
                      '<p>É o que o parâmetro A pede: «' + A_DESC + '» <span class="pag">(critérios, p. 14)</span>. Uma descrição mais longa não é mais fiel: vale o pormenor certo, dito com precisão. '
                      'Primeiro registas o que observas; depois dizes o efeito, com o pormenor que o mostra.</p>'},
                {'t': 'escolha', 'id': 'p7-aspetos', 'etq': 'treino', 'curto': 'Três aspetos distintos',
                 'p': 'Que conjunto dá três aspetos distintos para o comentário desta gravura?',
                 'o': [
                     {'t': 'O tamanho reduzido das figuras humanas; a pequenez das pessoas ao pé dos pilares; as figuras minúsculas pelo chão.',
                      'pista': '<p>Diz cada um destes três por uma só palavra. Quantas palavras diferentes ficam?</p>'},
                     {'t': 'A descrição da imagem apresentada; o comentário crítico com discurso valorativo; a conclusão adequada.',
                      'pista': '<p>Essas são as três partes do texto. Os aspetos pertencem a uma delas: relê o segundo ponto da lista e vê a qual.</p>'},
                     {'t': 'É bonita; é impressionante; é uma obra-prima.',
                      'pista': '<p>São três juízos. Procura em cada um a coisa da imagem de que fala: a que característica da gravura se refere?</p>'},
                     {'t': 'A escala das figuras ao pé da arquitetura; a perspetiva, que leva o olhar ao fundo; o contraste entre sombra e luz.',
                      'pista': ''},
                 ], 'c': 3,
                 'pista2': '<p>Um aspeto é uma característica da imagem que podes apontar com o dedo e sobre a qual podes dizer um efeito. Procura o conjunto em que cada elemento aponta para uma característica diferente da gravura.</p>',
                 'f': '<p>A escala, a perspetiva e o contraste entre sombra e luz são três características diferentes da gravura, e de cada uma podes dizer o que faz a quem olha. '
                      'O parâmetro A pede um comentário fundamentado em, «pelo menos, três aspetos distintos» <span class="pag">(critérios, p. 14)</span>, e o parâmetro B valoriza «' + B_ASP + '» <span class="pag">(critérios, p. 15)</span>.</p>'
                      '<p>Dar nome ao aspeto ainda não diz o efeito. No texto, explicas o que cada um faz nesta imagem.</p>'
                      '<p class="pag">Leitura nossa: os critérios não dão uma lista de aspetos nem dizem o que conta como distinto.</p>'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). Um parágrafo de descrição; um parágrafo para cada aspeto (o que se vê, o efeito, o juízo); um parágrafo de conclusão.</p>'
                 '<p>Os critérios pedem as três partes (parâmetro A, p. 14) e um texto que «' + C_PARTES + '» (parâmetro C, p. 15). Não fixam o número de parágrafos. Outras organizações contam do mesmo modo, se cumprirem o que se pede.</p>'
                 '<p><b>E uma reserva?</b> Uma reserva é um limite que apontas à imagem. O item não a pede; quem a propõe é a sessão 25 (orientação nossa). Se a usares, fundamenta-a como o resto: '
                 'uma reserva pode tornar mais exato um juízo favorável e não te obriga a rejeitar a imagem.</p></div>'},
                {'t': 'campos', 'id': 'p7-plano', 'titulo': 'O teu plano',
                 'intro': '<p class="ajuda">Notas curtas, só para ti. Ficam guardadas neste dispositivo e podes abri-las enquanto escreves. Também podes planear no papel.</p>',
                 'campos': PLANO},
            ],
        }),
        dict(AP, **{
            'id': 'distinguir', 'curto': 'Descrever, analisar, avaliar', 'titulo': 'Distinguir gosto, análise e juízo fundamentado',
            'o': 'Quatro frases soltas e, depois, dois parágrafos de comentário sobre o mesmo aspeto: a escala.',
            'blocos': [
                {'t': 'escolha', 'id': 'p7-frases', 'etq': 'treino', 'curto': 'A frase que já avalia',
                 'p': 'Que frase já avalia a gravura: traz um juízo de valor, e não só o que se vê ou o efeito que isso tem?',
                 'o': [
                     {'t': 'Ao fundo, numa zona de luz, vê-se um altar coberto por um dossel alto.',
                      'pista': '<p>A frase diz o que está na imagem e onde. Procura nela uma palavra que diga se isso é bom, mau, eficaz ou falhado.</p>'},
                     {'t': 'As linhas da cornija e da abóbada convergem para o fundo e levam o olhar até ao altar.',
                      'pista': '<p>A frase diz um efeito: o que as linhas fazem ao olhar. Falta-lhe dizer se esse efeito vale alguma coisa. Procura a frase que dá esse passo.</p>'},
                     {'t': 'Essa condução do olhar é o maior acerto da gravura: dá ordem a um espaço que podia confundir.',
                      'pista': ''},
                     {'t': 'A legenda, por baixo da imagem, está escrita em italiano.',
                      'pista': '<p>A frase regista um facto que se vê na gravura. Procura a frase que, além de mostrar, diz quanto vale aquilo que mostra.</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Arruma as quatro frases em três gavetas: as que dizem o que se vê; a que diz o que isso faz a quem olha; a que diz quanto isso vale, com uma razão. Só uma cabe na terceira.</p>',
                 'f': '<p>Duas frases descrevem (o altar, a legenda). Uma analisa: diz um efeito, o das linhas sobre o olhar. Só uma avalia: «o maior acerto» é um juízo de valor, e a razão vem logo depois dos dois pontos.</p>'
                      '<p>O parâmetro A pede um comentário feito «recorrendo a um discurso valorativo (juízo de valor explícito ou implícito)» <span class="pag">(critérios, p. 14)</span>: sem «eu» e sem «gosto», já há juízo. '
                      'As três operações fazem falta umas às outras: sem descrição, o juízo não tem objeto; sem análise, não tem razão.</p>'},
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p><b>Parágrafo A.</b> <span class="cit">' + PAR_A + '</span></p><p><b>Parágrafo B.</b> <span class="cit">' + PAR_B + '</span></p></div>' + EXC},
                {'t': 'escolha', 'id': 'p7-distinguir', 'etq': 'treino', 'curto': 'O parágrafo que fica aquém, e porquê',
                 'p': 'Que parágrafo fica aquém do que o pedido e os critérios pedem, e porquê?',
                 'o': [
                     {'t': 'O Parágrafo A: diz que gosta e o que se vê, mas não explica o efeito do que se vê nem dá a razão do juízo.',
                      'pista': ''},
                     {'t': 'O Parágrafo B: trata um só aspeto, e o pedido exige pelo menos três aspetos no comentário.',
                      'pista': '<p>São parágrafos do comentário, não o texto inteiro. Vê, na maneira de organizar do passo 2, quantos aspetos cabem em cada parágrafo.</p>'},
                     {'t': 'O Parágrafo A: usa palavras de valor, como «espetacular» e «impressionante».',
                      'pista': '<p>Vê o segundo ponto do pedido: o discurso valorativo é um defeito ou é o que se pede? O problema está noutro sítio: procura a razão de cada juízo.</p>'},
                     {'t': 'O Parágrafo B: não está na primeira pessoa, e quem aprecia tem de dizer «eu».',
                      'pista': '<p>Procura nos excertos alguma frase que exija a primeira pessoa. O que lá está é «juízo de valor explícito ou implícito».</p>'},
                 ], 'c': 0,
                 'pista2': '<p>Em cada parágrafo, sublinha os juízos. Depois procura, logo a seguir a cada um, a razão: uma frase que diga o que aquele pormenor faz a quem olha. Num dos parágrafos, não encontras nenhuma.</p>',
                 'f': '<p>No Parágrafo A, «gostei muito» é gosto, «impressionante» fica sem porquê e a última frase fala do autor e não da imagem. No Parágrafo B estão o aspeto, o pormenor, o efeito e o juízo com a sua razão.</p>'
                      '<p>Uma frase como «A gravura é impressionante» fica fundamentada assim: «A gravura impressiona porque as figuras minúsculas dão a medida das abóbadas.»</p>'
                      '<p>O enunciado pede um comentário «fundamentando a sua apreciação» (p. 13), e o parâmetro B olha também para o registo: «' + B_REG + '» <span class="pag">(critérios, p. 15)</span>.</p>'
                      '<p class="pag">Esta comparação é leitura nossa: os critérios do Grupo III não trazem tópicos de conteúdo nem exemplos de resposta.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'escrever', 'curto': 'O teu texto', 'titulo': 'Escrever o teu texto, sem pistas',
            'o': 'Agora és tu. Tens a imagem e o pedido ao lado, e o teu plano. Os parágrafos A e B e as explicações ficam nos passos anteriores.',
            'blocos': [
                {'t': 'vercampos', 'id': 'p7-plano', 'titulo': 'Ver o meu plano', 'vazio': 'Não escreveste o plano aqui. Se o fizeste no papel, tem-no à tua frente.', 'campos': PLANO},
                {'t': 'escrever', 'id': 'p7-texto', 'curto': 'Apreciação crítica (200 a 350 palavras)', 'rotulo': 'A tua apreciação crítica', 'linhas': 18, 'conta': True,
                 'ajuda': 'Escreve aqui ou no papel, como na prova. A caixa não corrige nem classifica: só conta as palavras, pela regra dos critérios. Os limites estão no enunciado (p. 13) e a regra da extensão nos critérios (p. 3), que encontras no passo 5: és tu que a aplicas.',
                 'papel': 'Escrevi no papel (no caderno). Deixo a caixa vazia e conto as palavras à mão.'},
            ],
        }),
        dict(AP, **{
            'id': 'grelha', 'curto': 'Rever com a grelha', 'titulo': 'Rever o teu texto com a grelha oficial, critério a critério', 'precisa': 'p7-texto',
            'o': 'Lê a tua primeira versão quatro vezes, uma por critério, e marca aspeto a aspeto o que lá encontras. A página não classifica nem faz contas por ti: as regras oficiais estão à vista, com a página, para as aplicares; quem classifica é o docente.',
            'blocos': [
                {'t': 'ver1', 'de': 'p7-texto', 'conta': True, 'linhas': 18},
                {'t': 'html', 'h': '<h3>1. Género e formato (parâmetro A)</h3>' + par_bloco(PA, '14')},
                {'t': 'grelha', 'id': 'p7-gA', 'intro': '<p class="ajuda">Os três aspetos do nível 4. Para cada um, procura no teu texto as frases que o cumprem. O segundo junta duas coisas, os três aspetos distintos e o discurso valorativo: confere as duas antes de marcares. '
                 'Os descritores dos outros níveis ficam na tabela, para consultares.</p>', 'aspetos': aspetos(PA), 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>2. Tema e pertinência da informação (parâmetro B)</h3>' + par_bloco(PB_, '15')},
                {'t': 'grelha', 'id': 'p7-gB', 'intro': '<p class="ajuda">Antes dos três aspetos, a pergunta de entrada do parâmetro: o teu texto trata o tema proposto sem desvios? Por exemplo: fala sempre da imagem, ou larga-a para falar de outro assunto? (O exemplo é leitura nossa.)</p>',
                 'aspetos': ['trata o tema proposto sem desvios'] + aspetos(PB_), 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>3. Organização e coesão textuais (parâmetro C)</h3>' + par_bloco(PC, '15') +
                 '<p class="pag">O critério fala em «mecanismos de articulação interfrásica». Os conectores são um desses mecanismos; a pontuação e a retoma de palavras também ligam frases. Leitura nossa.</p>'},
                {'t': 'grelha', 'id': 'p7-gC', 'aspetos': aspetos(PC), 'opcoes': OPG},
                {'t': 'html', 'h': '<h3>4. Correção linguística (CL)</h3><div class="caixa of">' + etq('oficial') + '<p><b>' + CR['CL']['nome'] + ' (CL): 14 pontos.</b> <span class="pag">Critérios, p. 16; tipologia de erros, pp. 2-3.</span></p><p>' + md(CR['CL']['texto']) + '</p>'
                 '<p><b>Tipo A:</b> «erro inequívoco de pontuação»; «erro de ortografia (incluindo erro de acentuação, erro de translineação e uso indevido de letra minúscula ou de letra maiúscula)»; «erro de morfologia»; «incumprimento das regras de citação de texto ou de referência a título de uma obra». <b>Tipo B:</b> «erro de sintaxe»; «impropriedade lexical». <span class="pag">(Quadro 1, p. 2)</span></p>'
                 '<p>' + R_UMA + ' <span class="pag">(critérios gerais, p. 3)</span></p>'
                 + tabela_cl('CL_14') + '</div>'
                 '<p>Relê o texto devagar, só à procura de erros. Conta-os no papel, em duas colunas: os do tipo A e os do tipo B. Depois lê tu a tabela: a linha é o número de erros do tipo B e a coluna é o número de erros do tipo A. A página não faz esta leitura por ti.</p>'},
                {'t': 'html', 'h': '<h3>5. As regras que tiram pontos</h3><p class="ajuda">Conta as palavras do teu texto (a contagem da caixa segue a regra dos critérios) e aplica tu estas regras. A página não calcula descontos. '
                 'O <a href="../escrita/">treino 3</a> tem perguntas sobre estas regras, com um caso de 196 palavras.</p><div class="caixa of">' + etq('oficial') +
                 '<p><b>Extensão</b> (critérios gerais, p. 3). ' + R_DESC + ' ' + R_80 + ' ' + R_CONTA + '</p>'
                 '<p><b>Zero em A ou em B</b> (critérios gerais, p. 2). ' + R_ZERO + '</p>'
                 '<p><b>Maiúsculas</b> (critérios gerais, p. 3). ' + R_MAI + '</p></div>'
                 '<h3>Um exemplo comentado</h3><p class="ajuda">Um texto possível, escrito por nós, com ' + str(N_MODELO) + ' palavras. Não é oficial nem é um modelo para decorar: os critérios do Grupo III não trazem exemplos de resposta. Usa-o para veres onde está cada aspeto da grelha.</p>' + modelo +
                 '<div class="caixa of">' + etq('oficial') + '<p><b>Outras formulações também contam.</b> ' + R_ALT + ' <span class="pag">(critérios gerais, p. 2)</span></p></div>'},
            ],
        }),
        dict(AP, **{
            'id': 'rever', 'curto': 'Reescrever', 'titulo': 'Reescrever', 'precisa': 'p7-texto',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres os critérios, a página diz isso junto dela. Na versão revista, muda o que marcaste como «com falhas» ou «não está» e corrige os erros que contaste.',
            'blocos': [
                {'t': 'rever', 'de': 'p7-texto', 'curto': 'Versão revista da apreciação crítica', 'linhas': 18, 'conta': True},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Agora com a imagem da prova.</b> ' + (LIG_IMG_PROVA % (URL_IMG_PROVA, 'Abre o enunciado na p. 13 (PDF em eduqa.pt)')) + ' e faz o mesmo plano com o <i>cartoon</i> de Javad Takjoo: '
                 'o que destacas na descrição, três aspetos com o seu efeito, o teu juízo e a conclusão. Um <i>cartoon</i> costuma ter uma intenção crítica: pergunta também o que a imagem quer dizer e se o diz bem. '
                 'As <a href="../../provas/2026-1f/grupo-iii/">provas em cartões (1.ª fase, Grupo III)</a> trabalham esse item peça a peça.</p></div>'
                 '<div class="caixa nossa"><p><b>Sobre 2027.</b> Este item e esta grelha são de 2026. Nesse ano, a 1.ª fase pediu esta apreciação crítica de um <i>cartoon</i> e a 2.ª fase um texto de opinião, os dois no Grupo III, com 200 a 350 palavras e 44 pontos. '
                 'O género, os limites de palavras, os descontos e a grelha de 2027 estão a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        }),
    ],
}

CAB = (
    sobre('apreciacao-critica', 'Apreciação crítica') +
    '<h1>Uma apreciação crítica, da imagem à segunda versão</h1>'
    '<p class="lede">O item de resposta extensa da 1.ª fase de 2026, com outra imagem, seis passos e duas versões do teu texto. Liga-se à ' + sessao('s25', 'Apreciação crítica: julgar mostrando') + ' e ao seu ' + aquecimento('s25') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Escrever, no Grupo III, a apreciação crítica de uma imagem, de 200 a 350 palavras: descrever destacando, comentar em três aspetos com juízos fundamentados e concluir. E revê-la com os parâmetros oficiais de classificação.</dd></div>'
    '<div><dt>Item oficial a que se liga</dt><dd>Prova 639, 2026, 1.ª fase, Grupo III (resposta extensa, 44 pontos). ' + lig('e1', 'Enunciado, p. 13 (PDF em eduqa.pt)') + '; ' + lig('c1', 'critérios, pp. 2-3 e 14-16 (PDF em eduqa.pt)') + '. Critérios definitivos, atualizados a 10/07/2026.</dd></div>'
    '<div><dt>O que é igual e o que é diferente</dt><dd>Igual: o género, os três pontos da lista, os limites de palavras e a grelha. Diferente: a imagem. A sessão 25 pede duas características e uma reserva; o item de 2026 pede pelo menos três aspetos e não pede reserva. O treino segue o item.</dd></div>'
    '<div><dt>A imagem</dt><dd>A imagem da prova, um <i>cartoon</i> de Javad Takjoo, tem direitos de autor e não está nesta página: ' + (LIG_IMG_PROVA % (URL_IMG_PROVA, 'vê-a no enunciado, p. 13 (PDF em eduqa.pt)')) + '. '
    'O treino usa uma gravura de Giovanni Battista Piranesi, em domínio público, com os créditos junto dela.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<details class="dobra"><summary>Ver o item oficial: enunciado, observações e cotação</summary><div class="dentro">' + OFICIAL + '</div></details>'
)

NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB.replace(OFICIAL, '') + AP_IMG
for _s in ([R_DESC, R_80, R_CONTA, R_ZERO, R_MAI, R_ALT, R_UMA, EXC, ENUN_OF, LISTA_HTML, md(CR['CL']['texto'])] + [par_bloco(p, x) for p, x in ((PA, '14'), (PB_, '15'), (PC, '15'))]
           + aspetos(PA) + aspetos(PB_) + aspetos(PC) + [D_DOIS, D_UM, A_DESC, A_COM, A_CONC, B_ASP, B_REG, C_PARTES]):
    NOSSO = NOSSO.replace(json.dumps(_s, ensure_ascii=False)[1:-1], '').replace(_s, '')
# a única imagem da página é a gravura; o cartoon da prova só aparece como ligação ao enunciado
assert (AP_IMG + CAB + json.dumps(TREINO, ensure_ascii=False)).count('<img ') == 1 and 'takjoo.jpg' not in AP_IMG + CAB


def construir():
    lint('apreciacao-critica', NOSSO)
    return pagina_treino('apreciacao-critica', 'apreciacao-critica/', 'Apreciação crítica', 'Treino 7: uma apreciação crítica | Português',
                         'Treino da preparação de exame de Português: resposta extensa, uma apreciação crítica de uma imagem em duas versões, com a grelha oficial de 2026.', CAB, {'img': AP_IMG}, TREINO)
