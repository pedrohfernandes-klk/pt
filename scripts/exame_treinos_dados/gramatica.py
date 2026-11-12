from .base import *

G1 = F1['grupos'][1]
G2 = F2['grupos'][1]
T1 = G1['textos'][0]
T2 = G2['textos'][0]
L1 = {l['n']: l['t'] for l in T1['linhas']}
L2 = {l['n']: l['t'] for l in T2['linhas']}
I1 = G1['itens'][6]
I2 = G2['itens'][6]
assert I1['numero'] == 'II.7' and I1['chave_versao_2'] == 'D' and I1['cotacao'] == 13
assert I2['numero'] == 'II.7' and I2['chave_versao_2'] == 'A' and I2['cotacao'] == 13
assert G1['chaves_criterios_quadro']['linhas'][6] == ['7.', '(A)', '(D)', 13]
assert G2['chaves_criterios_quadro']['linhas'][6] == ['7.', '(B)', '(A)', 13]
assert ['II.7', 13] in F1['cotacoes']['obrigatorios']['itens'] and ['II.7', 13] in F2['cotacoes']['obrigatorios']['itens']


def linhas(L, grupos, realces=()):
    """grupos: lista de intervalos (a, b); entre eles marca-se o corte."""
    out = '<ol class="prosa">'
    for gi, (a, b) in enumerate(grupos):
        if gi > 0:
            out += '<li class="corte"><span class="n"></span><span>[linhas %d a %d: ver o PDF da prova]</span></li>' % (grupos[gi - 1][1] + 1, a - 1)
        for n in range(a, b + 1):
            t = md(L[n])
            for r in realces:
                t = t.replace(r, '<mark>' + r + '</mark>')
            out += '<li><span class="n">%d</span><span>%s</span></li>' % (n, t)
    return out + '</ol>'


def tem(L, a, b, s):
    j = ' '.join(L[n] for n in range(a, b + 1))
    assert s in j, (s, j)


tem(L1, 35, 36, 'pelo automóvel ou pelo avião')
tem(L1, 30, 31, 'pelo urbanismo tradicional de edifícios contínuos')
tem(L1, 21, 21, 'pelas inúmeras embarcações')
tem(L1, 20, 20, 'pela Ásia')
tem(L1, 25, 25, 'mesquitas espalhadas pelos bairros')
tem(L1, 26, 26, 'ligeiramente distorcido pelos sistemas de amplificação de áudio')
tem(L2, 1, 1, 'revela-se mais difícil mobilizar as crianças para a aprendizagem')

FONTE1 = '<p class="fonte">' + md(T1['fonte']) + ' Texto do Grupo II da Prova 639, 2026, 1.ª fase (enunciado, pp. 10-11), com a numeração de linhas da prova. Aqui estão só as linhas de que precisas; o texto completo está no ' + lig('e1', 'PDF da prova (eduqa.pt)') + '.</p>'
FONTE2 = '<p class="fonte">' + md(T2['fonte']) + ' Texto do Grupo II da Prova 639, 2026, 2.ª fase (enunciado, p. 6), com a numeração de linhas da prova. Aqui estão só as linhas 1 a 5; o texto completo está no ' + lig('e2', 'PDF da prova (eduqa.pt)') + '.</p>'

AP_OF = ('<p class="texto-t">Miguel Marcelino, «Paisagem sonora»</p><p class="texto-a">Linhas 20 a 22, 30 a 31 e 35 a 36. Os realces a amarelo são nossos: marcam as quatro expressões do item.</p>'
         + linhas(L1, [(20, 22), (30, 31), (35, 36)], ['pela Ásia', 'pelas inúmeras embarcações', 'pelo urbanismo tradicional de edifícios', 'pelo automóvel ou pelo'])
         .replace('<span>contínuos, em', '<span><mark>contínuos</mark>, em').replace('<span>avião, cuja', '<span><mark>avião</mark>, cuja')
         + FONTE1)
AP_TR = ('<p class="texto-t">Miguel Marcelino, «Paisagem sonora»</p><p class="texto-a">Linhas 23 a 26, do mesmo texto da prova. Os realces a amarelo são nossos.</p>'
         + linhas(L1, [(23, 26)], ['pelos bairros', 'pelos sistemas de amplificação de áudio']) + FONTE1)
AP_LIM = ('<p class="texto-t">Frase de treino</p><ol class="prosa"><li><span class="n"></span><span>Entrou serenamente no seu quarto.</span></li></ol>'
          '<p class="fonte">Frase de treino do aquecimento da sessão 21, feita a partir de <i>Amor de Perdição</i>, de Camilo Castelo Branco. Não é uma citação.</p>'
          '<p class="texto-t espaco">Elsa de Barros, «As virtudes do pensamento lento»</p><p class="texto-a">Linhas 1 a 5. O realce a amarelo é nosso.</p>'
          + linhas(L2, [(1, 5)], ['mobilizar as crianças para a aprendizagem']) + FONTE2)


def item_of(I, pagina, fase, extra=''):
    ops = ''.join('<li><b>(%s)</b> %s</li>' % (o['letra'], md(o['texto'])) for o in I['opcoes'])
    return ('<div class="caixa of">' + etq('oficial') +
            '<p class="enun"><b>7.</b> ' + md(I['enunciado'][0]) + '</p><ul class="top sem-marcas">' + ops + '</ul>'
            '<p class="pag">Prova 639, 2026, %s, versão 2, Grupo II, item 7. Escolha múltipla, 13 pontos; conta sempre para a classificação. Enunciado, p. %s.%s</p></div>' % (fase, pagina, extra))


OF1 = item_of(I1, '12', '1.ª fase', ' A chave oficial aparece no passo 6, depois de responderes.')
OF2 = item_of(I2, '8', '2.ª fase')

DT_AG = '«Função sintáctica desempenhada por um grupo preposicional presente numa frase passiva, que corresponde ao sujeito na frase activa com o mesmo significado.»'
DT_MOD = '«Função sintáctica desempenhada por constituintes não seleccionados por nenhum elemento do grupo sintáctico de que fazem parte. Por não serem seleccionados, a sua omissão geralmente não afecta a gramaticalidade de uma frase»'
DT_OBL = '«Complemento seleccionado pelo verbo»'
DT_SUJ = '«quando o sujeito é uma oração completiva, pode ser substituído pelo pronome demonstrativo "isso" em posição pré-verbal»'
DT_POS = '«é comum o sujeito encontrar-se em posição pós verbal»'
DT_REF = '<span class="pag">(<i>Dicionário Terminológico</i>, dt.dge.mec.pt, B.4.2, Funções sintácticas, entrada «%s»; consultado a 11/11/2026; grafia do original)</span>'
# conferência com as entradas do DT guardadas em tests/fixtures/dicionario-terminologico-20261111.json
_dt = json.load(open(ROOT + '/tests/fixtures/dicionario-terminologico-20261111.json', encoding='utf-8'))['entradas']
def _dtx(i):
    r = _dt[i]
    x = html.unescape(re.sub(r'<[^>]+>', ' ', r['definition'] + ' ' + (r.get('notes') or '')))
    return re.sub(r'\s+', ' ', x).replace(' ,', ',').replace(' .', '.').replace('( ', '(')
for cit, i in [(DT_AG, 'n297'), (DT_MOD, 'n301'), (DT_OBL, 'n296'), (DT_SUJ, 'n285'), (DT_POS, 'n285')]:
    assert re.sub(r'\s+', ' ', cit.strip('«»')) in _dtx(i), (cit, _dtx(i))

JUST_A = '«pelos bairros» e «pelos sistemas de amplificação de áudio» são complementos agentes da passiva, porque vêm depois de um particípio e começam pela preposição «por».'
JUST_B = ('«pelos sistemas de amplificação de áudio» é complemento agente da passiva: na frase ativa correspondente passa a sujeito («os sistemas de amplificação de áudio distorcem ligeiramente aquele recitar»). '
          '«pelos bairros» não é: «os bairros espalham as mesquitas» não quer dizer o mesmo. A expressão indica o lugar por onde as mesquitas estão espalhadas.')

OPS1 = ['(%s) %s' % (o['letra'], md(o['texto'])) for o in I1['opcoes']]

ANALISE = (
    '<div class="rolo" tabindex="0" role="region" aria-label="Análise das quatro opções"><table><thead><tr><th>Opção</th><th>De que depende</th><th>Frase ativa correspondente</th><th>Conclusão</th></tr></thead><tbody>'
    '<tr><td>(A) linhas 35 e 36</td><td>«causada» (particípio de «causar»)</td><td>«o automóvel ou o avião causam a poluição sonora»</td><td>Passa a sujeito: complemento agente da passiva.</td></tr>'
    '<tr><td>(B) linhas 30 e 31</td><td>«é favorecida» (passiva de «favorecer»)</td><td>«o urbanismo tradicional de edifícios contínuos favorece a acústica do instrumento-cidade»</td><td>Passa a sujeito: complemento agente da passiva.</td></tr>'
    '<tr><td>(C) linha 21</td><td>«a ser rasgada» (passiva de «rasgar»)</td><td>«as inúmeras embarcações rasgam a água»</td><td>Passa a sujeito: complemento agente da passiva.</td></tr>'
    '<tr><td>(D) linha 20</td><td>«vemos» (forma ativa, 1.ª pessoa do plural)</td><td>Não há: a frase já está na ativa, com o sujeito «nós» subentendido.</td><td>Não é complemento agente da passiva. Indica o lugar onde vemos os mercados.</td></tr>'
    '</tbody></table></div>')

TREINO = {
    'id': 'gramatica', 'viu': 'a chave oficial',
    'passos': [
        {
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido', 'apoio': 'of', 'apoioRot': 'Linhas da prova',
            'o': 'Um item de gramática da prova de 2026. Antes de olhares para as opções, vê o que o enunciado manda procurar.',
            'blocos': [
                {'t': 'html', 'h': OF1},
                {'t': 'escolha', 'id': 'p2-pedido', 'etq': 'treino', 'curto': 'O que o item oficial manda encontrar',
                 'p': 'O que é que o item te manda encontrar?',
                 'o': [
                     {'t': 'Todas as expressões que são complemento agente da passiva.',
                      'pista': '<p>Relê o enunciado até à última palavra, a que está a negro. Depois pensa em quantas letras se assinalam num item de escolha múltipla.</p>'},
                     {'t': 'A única expressão que não é complemento agente da passiva.', 'pista': ''},
                     {'t': 'A única expressão que é complemento agente da passiva.',
                      'pista': '<p>Relê o enunciado até à última palavra, a que está a negro. O que diz ela das outras três expressões?</p>'},
                     {'t': 'As expressões introduzidas pela preposição «por».',
                      'pista': '<p>Olha para a primeira palavra das quatro opções: «pelo», «pelo», «pelas», «pela». Se a preposição bastasse, quantas opções ficavam certas?</p>'},
                 ], 'c': 1,
                 'pista2': '<p>A última palavra do enunciado é «exceto». Lê a frase inteira com ela: «Todas as expressões desempenham a função…, exceto». Depois responde: de quantas expressões andas à procura, e em que é que ela difere das outras três?</p>',
                 'f': '<p>Três das quatro expressões são complemento agente da passiva. Procuras a que não é. Como as quatro começam por «por» contraído com um artigo, a forma não decide nada: tens de ir a cada linha ver de que palavra depende a expressão.</p>'},
            ],
        },
        {
            'id': 'localizar', 'curto': 'Localizar', 'titulo': 'Localizar a palavra de que a expressão depende', 'apoio': 'tr', 'apoioRot': 'Linhas da prova',
            'o': 'Treinas noutras linhas do mesmo texto, para deixares o item oficial inteiro para o passo 5.',
            'blocos': [
                {'t': 'tocar', 'id': 'p2-loc1', 'etq': 'treino', 'modo': 'palavras', 'curto': 'A palavra de que depende «pelos bairros»',
                 'p': 'Linha 25. Toca na palavra de que depende a expressão a negro, «pelos bairros». Depois toca em «Verificar».',
                 'tokens': [{'x': 'nos'}, {'x': 'minaretes'}, {'x': 'das'}, {'x': 'várias'}, {'x': 'mesquitas'}, {'x': 'espalhadas'}, {'x': '<b>pelos bairros</b>.', 'fixo': True}],
                 'nucleos': [[5]], 'permitidos': [5], 'mostra': [5],
                 'pistas': [
                     {'se': [4], 'x': '<p>«mesquitas» é o nome de que se fala. Pergunta: o que é que lhes aconteceu, «pelos bairros»? Procura a palavra que o diz.</p>'},
                     {'se': [0, 1, 2, 3], 'x': '<p>Essas palavras dizem onde estão os altifalantes e de quem são os minaretes. Pergunta: o que é que está «pelos bairros», e o que lhe aconteceu?</p>'},
                 ],
                 'falta': '<p>Pergunta: o que é que está «pelos bairros», e o que lhe aconteceu?</p>',
                 'pista2': '<p>Procura, entre as palavras da linha 25 em que podes tocar, a que vem de um verbo. É dela que a expressão a negro depende.</p>',
                 'f': '<p>«espalhadas»: é o particípio passado do verbo «espalhar».</p>'},
                {'t': 'tocar', 'id': 'p2-loc2', 'etq': 'treino', 'modo': 'palavras', 'curto': 'A forma verbal de que depende «pelos sistemas de amplificação de áudio»',
                 'p': 'Linhas 25 e 26. Toca na forma verbal de que depende a expressão a negro, «pelos sistemas de amplificação de áudio». Depois toca em «Verificar».',
                 'tokens': [{'x': 'Aquele'}, {'x': 'recitar'}, {'x': 'de'}, {'x': 'palavras'}, {'x': 'em'}, {'x': 'tom'}, {'x': 'hipnótico,'}, {'x': 'ligeiramente'}, {'x': 'distorcido'},
                            {'x': '<b>pelos sistemas de amplificação de áudio</b>.', 'fixo': True}],
                 'nucleos': [[8]], 'permitidos': [7, 8], 'mostra': [8],
                 'notas': {'7': 'Aceite com «ligeiramente», que é um advérbio a modificar «distorcido». A forma verbal é só «distorcido».'},
                 'pistas': [
                     {'se': [1], 'x': '<p>Aqui, «recitar» está usado como nome («aquele recitar»): é aquilo a que acontece alguma coisa. Procura a palavra que diz o que lhe fizeram.</p>'},
                     {'se': [0, 2, 3, 4, 5, 6], 'x': '<p>Essas palavras dizem o que se recita e em que tom. Procura a palavra que diz o que aconteceu a esse «recitar».</p>'},
                     {'so': [7], 'x': '<p>«ligeiramente» diz em que grau. Procura a palavra cujo grau ele indica.</p>'},
                 ],
                 'falta': '<p>Procura a palavra que diz o que aconteceu ao «recitar».</p>',
                 'pista2': '<p>Vai à linha 26 e procura a palavra que vem de um verbo. É ela que diz o que os sistemas de amplificação fazem àquele «recitar».</p>',
                 'f': '<p>«distorcido»: é o particípio passado do verbo «distorcer».</p><p>Até aqui, os dois casos têm a mesma forma: um particípio seguido de «por» com artigo. No passo seguinte vês que não têm a mesma função.</p>'},
            ],
        },
        {
            'id': 'distinguir', 'curto': 'Insuficiente ou adequada', 'titulo': 'Distinguir uma justificação insuficiente de uma adequada', 'apoio': 'tr', 'apoioRot': 'Linhas da prova',
            'o': 'Duas justificações para as expressões do passo 2. Uma olha só para a forma.',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') + '<p><b>Justificação A.</b> ' + JUST_A + '</p><p><b>Justificação B.</b> ' + JUST_B + '</p></div>'},
                {'t': 'escolha', 'id': 'p2-teste', 'etq': 'treino', 'curto': 'O teste que separa o agente da passiva de uma expressão de lugar',
                 'p': 'A Justificação A engana-se num dos casos. Que teste usa a Justificação B para os separar?',
                 'o': [
                     {'t': 'Ver se a expressão começa por «por» (pelo, pela, pelos, pelas).',
                      'pista': '<p>Aplica esse teste às duas expressões a negro do passo 2. Dá resultados diferentes?</p>'},
                     {'t': 'Cortar a expressão e ver se o que fica continua bem formado.',
                      'pista': '<p>Experimenta nas linhas 25 e 26: «mesquitas espalhadas» e «ligeiramente distorcido». Alguma das duas fica mal formada? Um teste que dá o mesmo resultado nos dois casos não os separa.</p>'},
                     {'t': 'Passar para a ativa e ver se a expressão passa a sujeito, com o mesmo sentido.', 'pista': ''},
                     {'t': 'Ver se a expressão vem depois de um particípio.',
                      'pista': '<p>No passo 2 tocaste em dois particípios, «espalhadas» e «distorcido». Este teste dá o mesmo resultado nos dois casos.</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Relê a Justificação B. Para cada caso, ela escreve uma frase nova: «os sistemas de amplificação de áudio distorcem…» e «os bairros espalham…». Compara cada uma com a linha da prova e vê o que mudou de lugar.</p>',
                 'f': '<p>O teste está na própria definição. Complemento agente da passiva: ' + DT_AG + ' ' + (DT_REF % 'Complemento agente da passiva') + '</p>'
                      '<p>A forma (um particípio, a preposição «por») é só o sinal que te manda fazer o teste. A Justificação A fica pelo sinal; a Justificação B faz o teste nos dois casos e mostra o resultado.</p>'
                      '<p>Quanto a «pelos bairros»: basta-te dizer que não é agente e que indica um lugar. O item oficial também só pede que separes o que é agente do que não é.</p>'},
            ],
        },
        {
            'id': 'limites', 'curto': 'Os limites dos testes', 'titulo': 'Ver até onde vai cada teste', 'apoio': 'lim', 'apoioRot': 'Frases para este passo',
            'o': 'Nenhum teste serve para tudo. Dois contrastes: um com o teste de cortar, outro com a pergunta «o quê?».',
            'blocos': [
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') +
                 '<p>O aquecimento da sessão 21 diz: «o que se corta sem estragar a frase é modificador do grupo verbal». Experimenta na mesma frase de treino.</p>'
                 '<ul class="top"><li>Sem «serenamente»: «Entrou no seu quarto.»</li><li>Sem «no seu quarto»: «Entrou serenamente.»</li></ul>'
                 '<p>As duas ficam bem formadas.</p>'
                 '<p class="pag">A frase é a do aquecimento da sessão 21 (n.º 11); a pergunta é nova. Não é um item de exame.</p></div>'},
                {'t': 'escolha', 'id': 'p2-cortar', 'curto': 'O que o teste de cortar prova e o que não prova',
                 'p': 'O que se pode concluir?',
                 'o': [
                     {'t': 'As duas expressões são modificadores do grupo verbal, porque as duas se podem cortar.',
                      'pista': '<p>Pergunta ao verbo o que ele pede. Quem entra, entra em algum sítio. O verbo «entrar» pede o lugar? E pede a maneira?</p>'},
                     {'t': 'Nenhuma das duas é modificador, porque a frase perde informação quando se cortam.',
                      'pista': '<p>Qualquer corte tira informação. A pergunta é outra: compara «entrar em algum sítio» com «entrar de alguma maneira». Qual das duas coisas faz parte do que o verbo «entrar» pede?</p>'},
                     {'t': 'Poder cortar não chega para dizer que é modificador: é preciso ver se o verbo seleciona a expressão.', 'pista': ''},
                     {'t': 'Só «serenamente» é modificador do grupo verbal, porque é a única das duas que se pode cortar.',
                      'pista': '<p>Volta às duas frases cortadas, aqui em cima. As duas ficam bem formadas. O teste de cortar deu resultados diferentes nas duas expressões?</p>'},
                 ], 'c': 2,
                 'pista2': '<p>O corte deu o mesmo resultado nas duas expressões. Deixa-o de lado e olha para o verbo: compara «entrar em algum sítio» com «entrar de alguma maneira». Vê qual das duas expressões o verbo «entrar» seleciona.</p>',
                 'f': '<p>«no seu quarto» é <b>complemento oblíquo</b>: o verbo «entrar» seleciona o lugar (entra-se em algum sítio) e a expressão não se troca por «lhe». «serenamente» é <b>modificador do grupo verbal</b>: o verbo não pede a maneira.</p>'
                      '<p>O <i>Dicionário Terminológico</i> define o modificador assim: ' + DT_MOD + ' ' + (DT_REF % 'Modificador') + ' E o complemento oblíquo como ' + DT_OBL + ' ' + (DT_REF % 'Complemento oblíquo') + '</p>'
                      '<p>Repara na ordem das ideias: o modificador pode cortar-se <b>porque</b> não é selecionado («geralmente», diz a definição). Não é modificador <b>por</b> se poder cortar. Um complemento também pode ficar por dizer, como aqui. O teste de cortar deu o mesmo resultado nas duas expressões; por isso, por si só, não as separa.</p>'},
                {'t': 'html', 'h': '<p>Agora um item da 2.ª fase de 2026, sobre a linha 1 do outro texto.</p>' + OF2},
                {'t': 'escolha', 'id': 'p2-sujeito', 'etq': 'oficial', 'curto': 'Item oficial da 2.ª fase: a função de uma oração',
                 'p': 'Que opção assinalas neste item da 2.ª fase?',
                 'o': [
                     {'t': 'sujeito.', 'pista': ''},
                     {'t': 'complemento direto.',
                      'pista': '<p>Procura o sujeito de «revela-se». Pergunta: o que é que se revela mais difícil? Depois experimenta pôr «isso» no lugar da oração, antes do verbo.</p>'},
                     {'t': 'complemento do adjetivo.',
                      'pista': '<p>O complemento do adjetivo é pedido pelo adjetivo e vem ligado a ele por uma preposição (como em «contente com a situação»). Vê se há alguma preposição entre «difícil» e «mobilizar».</p>'},
                     {'t': 'predicativo do sujeito.',
                      'pista': '<p>Na linha 1 já há uma expressão que diz como é alguma coisa: «mais difícil». Procura de que é que se diz que é «mais difícil».</p>'},
                 ], 'c': 0,
                 'pista2': '<p>Faz a experiência na linha 1: põe «isso» no lugar da oração, antes de «revela-se», e lê a frase que fica. Depois pergunta que função tem «isso» nessa frase.</p>',
                 'f': '<p>A oração é o <b>sujeito</b> de «revela-se»: «Isso revela-se mais difícil.» Chave oficial: Versão 2, (A); 13 pontos (critérios da 2.ª fase, p. 13; ' + lig('c2', 'PDF em eduqa.pt') + ').</p>'
                      '<p>Aqui falham dois testes habituais. A pergunta «o quê?» dá a mesma resposta para o sujeito e para o complemento direto. E a posição engana: a oração vem depois do verbo. O <i>Dicionário Terminológico</i> diz que, ' + DT_SUJ + ', e lembra que ' + DT_POS + ' ' + (DT_REF % 'Sujeito') + '</p>'},
            ],
        },
        {
            'id': 'responder', 'curto': 'A tua resposta', 'titulo': 'Responder ao item oficial, sem pistas', 'apoio': 'of', 'apoioRot': 'Linhas da prova',
            'o': 'Agora és tu. Tens as linhas da prova ao lado e mais nada.',
            'blocos': [
                {'t': 'html', 'h': OF1 + '<div class="caixa ad">' + etq('adaptado') + '<p class="enun">Assinala a opção e justifica a tua escolha em duas ou três frases.</p><p class="pag">O que mudou em relação ao item oficial: o enunciado, as opções e as linhas são os da prova; acrescentámos a justificação escrita. Na prova só assinalas a letra.</p></div>'},
                {'t': 'escrever', 'id': 'p2-resposta', 'curto': 'Resposta ao item oficial da 1.ª fase, com justificação escrita',
                 'opcoes': OPS1, 'opRotulo': 'A opção que assinalas',
                 'rotulo': 'A tua justificação', 'linhas': 6,
                 'ajuda': 'Em duas ou três frases: que teste usaste e o que deu, na expressão que escolheste e em pelo menos uma das outras. Escreve aqui ou no papel.'},
            ],
        },
        {
            'id': 'comparar', 'curto': 'Comparar', 'titulo': 'Comparar com a chave oficial e com uma análise comentada', 'apoio': 'of', 'apoioRot': 'Linhas da prova', 'precisa': 'p2-resposta',
            'o': 'A chave é oficial. A análise das quatro opções é nossa.',
            'blocos': [
                {'t': 'ver1', 'de': 'p2-resposta', 'opcoes': OPS1, 'linhas': 6},
                {'t': 'html', 'h': '<div class="caixa of">' + etq('oficial') + '<p><b>Chave do item 7:</b> Versão 1, (A); Versão 2, <b>(D)</b>. Pontuação: 13. <span class="pag">(critérios da 1.ª fase, p. 13: quadro do Grupo II; ' + lig('c1', 'PDF em eduqa.pt') + ')</span></p>'
                 '<p>Os critérios do Grupo II só trazem este quadro: a letra certa e os pontos. Sobre os itens de seleção classificados de forma dicotómica, os critérios gerais dizem: «a pontuação só é atribuída às respostas corretas, sendo todas as outras respostas classificadas com zero pontos» <span class="pag">(p. 1)</span>.</p></div>'
                 '<h3>Análise comentada das quatro opções</h3><p class="ajuda">Feita por nós. A classificação de «pela Ásia» como modificador do grupo verbal é análise nossa: os critérios só dizem que (D) é a opção certa.</p>' + ANALISE +
                 '<p>Em (D), o teste nem chega a aplicar-se: «vemos» não é uma forma passiva. «pela Ásia» diz onde vemos os mercados, e o verbo «ver» não pede um lugar: é modificador do grupo verbal.</p>'},
                {'t': 'lista', 'id': 'p2-conf', 'titulo': 'Confere a tua primeira versão',
                 'intro': '<p class="ajuda">Marca o que já está na tua resposta. O que ficar por marcar é o que vais rever no passo seguinte.</p>',
                 'itens': [
                     'Assinalei a opção (D).',
                     'A minha justificação diz que teste usei.',
                     'Mostra o resultado do teste na expressão que não é agente: em «que vemos pela Ásia» não há forma passiva.',
                     'Mostra o resultado em pelo menos uma das expressões que são agente: a frase ativa em que passa a sujeito.',
                     'Usei os termos da gramática: complemento agente da passiva, sujeito, frase ativa, frase passiva.',
                 ]},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). Primeiro o sinal (a forma que te faz desconfiar), depois o teste (a prova), depois a conclusão (o nome da função). O item só te pede a função; o caminho é teu.</p>'
                 '<ul class="top"><li><b>Passar à ativa</b> identifica o complemento agente da passiva. Limite: só se aplica onde há uma forma passiva.</li>'
                 '<li><b>Trocar por «o», «a» ou por «lhe»</b> identifica o complemento direto e o indireto. Limite: o predicativo do sujeito também se troca por «o» («difícil, é-o»); com verbos copulativos, a troca não prova que há complemento direto.</li>'
                 '<li><b>Cortar</b> mostra o que pode ficar por dizer. Limite: não separa o modificador de um complemento que também se pode omitir.</li>'
                 '<li><b>Perguntar «o quê?»</b> ajuda a encontrar o que o verbo pede. Limite: não separa o sujeito do complemento direto. A posição também não: uma oração que vem depois do verbo pode ser sujeito. Se não se troca por «o» e se troca por «isso» antes do verbo, é sujeito (foi o caso do passo 4).</li></ul></div>'
                 '<p class="pag"><b>Termos conferidos.</b> Os nomes das funções são os do <i>Dicionário Terminológico</i> (B.4.2), na grafia atual. Cinco deles aparecem nos itens 7 do Grupo II de 2026: complemento agente da passiva (1.ª fase); sujeito, complemento direto, complemento do adjetivo e predicativo do sujeito (2.ª fase). Os restantes (modificador, complemento oblíquo, complemento indireto) são usados na nossa análise e não vêm nesses itens. No <i>Dicionário Terminológico</i>, as entradas chamam-se «Modificador restritivo» e «Modificador apositivo». Os critérios de 2026 escrevem «modificador do nome apositivo» (p. 3); o aquecimento da sessão 21 escreve «modificador apositivo do nome».</p>'},
            ],
        },
        {
            'id': 'rever', 'curto': 'Rever', 'titulo': 'Rever a tua justificação', 'apoio': 'of', 'apoioRot': 'Linhas da prova', 'precisa': 'p2-resposta',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres a chave oficial, a página diz isso junto dela. Escreve a versão revista: diz o teste e mostra o resultado.',
            'blocos': [
                {'t': 'rever', 'de': 'p2-resposta', 'curto': 'Versão revista da justificação', 'linhas': 6, 'opcoes': OPS1},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Sobre 2027.</b> Os dois itens são de 2026. Que conteúdos de gramática podem sair em 2027, e em que tipo de item, está a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        },
    ],
}

CAB = (
    '<p class="sobre">Treino 2 de 3. Gramática</p>'
    '<h1>Que função tem, e como o sabes</h1>'
    '<p class="lede">Dois itens de gramática das provas de 2026, sete passos e uma justificação escrita por ti. Liga-se à ' + sessao('s21', 'Gramática: funções e relações entre orações') + ' e ao seu ' + aquecimento('s21') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Identificar a função sintática de uma expressão ou de uma oração no contexto, e justificar a escolha com um teste que sirva para aquele caso.</dd></div>'
    '<div><dt>Itens oficiais a que se liga</dt><dd>Prova 639, 2026, 1.ª fase, Grupo II, item 7 (complemento agente da passiva; 13 pontos): ' + lig('e1', 'enunciado, p. 12') + ', ' + lig('c1', 'critérios, p. 13') + '. '
    'Prova 639, 2026, 2.ª fase, Grupo II, item 7 (função de uma oração; 13 pontos): ' + lig('e2', 'enunciado, p. 8') + ', ' + lig('c2', 'critérios, p. 13') + '. PDF em eduqa.pt.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<p class="pag">Os dois itens oficiais aparecem inteiros nos passos 1, 4 e 5 (enunciado, quatro opções e cotação). As chaves oficiais aparecem depois de responderes, com a página dos critérios.</p>'
)

NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB + AP_LIM
for s in [OF1, OF2, DT_AG, DT_MOD, DT_OBL, DT_SUJ, DT_POS, md(I2['enunciado'][0])]:
    NOSSO = NOSSO.replace(json.dumps(s, ensure_ascii=False)[1:-1], '').replace(s, '')


def construir():
    lint('gramatica', NOSSO)
    return pagina_treino('gramatica', 'gramatica/', 'Gramática', 'Treino 2: que função tem, e como o sabes | Português',
                         'Treino da preparação de exame de Português: gramática, funções sintáticas no contexto, com dois itens oficiais de 2026 e uma justificação escrita por ti.', CAB, {'of': AP_OF, 'tr': AP_TR, 'lim': AP_LIM}, TREINO)

