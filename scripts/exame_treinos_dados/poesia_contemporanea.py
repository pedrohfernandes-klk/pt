"""12/11/2026: treino 4, «Dois poemas, um eixo» (exame/treinos/poesia-contemporanea/), ligado à sessão 17.

Os dois poemas do treino têm direitos de autor (Jorge de Sena, Eugénio de Andrade). A página mostra só duas citações
curtas, as que as lições M8-F03 e M8-F04 já publicam, e remete para o manual. Cada citação confere-se aqui, letra a
letra, com os cartões da lição de onde vem; o que se diz dos poemas além das citações é resumo dessas lições, e as
frases em que se apoia também se conferem. Nenhum verso é reconstituído de memória.
"""
from .base import *


# ---------- as lições do M8 de onde vêm as citações (licao() está em base.py desde 12/11/2026) ----------
L3, H3 = licao('f03')
L4, H4 = licao('f04')
L5, H5 = licao('f05')

# as duas citações: as únicas palavras dos poemas que a página mostra
C_SENA = 'Apenas como elas. / Mas brilha.'
C_EUG = 'São como um cristal, / as palavras.'
CITACOES = {C_SENA: ('m8/licao-m8-f03/', L3), C_EUG: ('m8/licao-m8-f04/', L4)}
for _c, (_p, _l) in CITACOES.items():
    assert '«%s»' % _c in _l, ('citação que a lição não publica', _c, _p)

# o que se diz dos poemas além das citações é resumo das lições: as frases de apoio têm de lá estar
for _s in ('Uma luz pequena e trémula, no meio das pessoas', 'Há quem sopre com raiva para a apagar', 'A luz não aquece, não ilumina os rostos, não custa dinheiro',
           'No fim de «Uma pequenina luz», «Apenas como elas. / Mas brilha.»', 'A luz é comparada à **exatidão, à firmeza e à justiça**',
           'Jorge de Sena, «Uma pequenina luz», Fidelidade (1958)', '«Uma pequenina luz»: no manual', '«Mas brilha», como «elas»: a que é comparada a luz no fim do poema?'):
    assert _s in L3, ('lição M8-F03', _s)
for _s in ('O poema abre com uma comparação: «São como um cristal, / as palavras.»', 'navegam sem segurança', 'São frágeis e inocentes',
           'O poema acaba com duas perguntas, que ficam sem resposta: quem as ouve, e quem as recolhe', 'as palavras podem perder-se, e o poema pergunta quem as recolhe',
           '«As Palavras» é uma arte poética', 'Coisa frágil: palavras de cristal', 'Coisa frágil: uma luz pequena que brilha',
           'Os dois guardam uma coisa frágil, palavras de cristal ou uma luz pequena', 'a edição do manual', 'cada palavra é um cristal, e pode ferir', 'O poeta como testemunha'):
    assert _s in L4, ('lição M8-F04', _s)
assert 'A prece e o cristal' in L5 and 'Ana Luísa Amaral' in L5 and 'Abre com uma comparação: «São como um cristal»' in L5
for _h, _t in ((H3, 'Lição M8-F03: Jorge de Sena, poeta testemunha'), (H4, 'Lição M8-F04: Eugénio de Andrade: a palavra essencial'), (H5, 'Lição M8-F05: Ana Luísa Amaral: reescrever a tradição')):
    assert _t in _h and '<i>Novo Sentidos 12</i>, ASA, 2023' in _h, _t
# o plano da comparação é o do cartão 11 do aquecimento da sessão 17
_s17 = json.load(open(ROOT + '/docs/pedagogia/exame-aquecimentos/s17.json', encoding='utf-8'))
assert _s17['cartoes'][11]['p'] == 'Para comparar dois poemas, por ordem:'

M8 = '../../../m8/'
LIG3 = '<a href="%slicao-m8-f03/">lição M8-F03 («Jorge de Sena, poeta testemunha»)</a>' % M8
LIG4 = '<a href="%slicao-m8-f04/">lição M8-F04 («Eugénio de Andrade: a palavra essencial»)</a>' % M8
LIG5 = '<a href="%slicao-m8-f05/">lição M8-F05 («Ana Luísa Amaral: reescrever a tradição»)</a>' % M8
MANUAL = '<i>Novo Sentidos 12</i> (ASA, 2023)'

# o que pode vir entre «» no texto nosso sem ser bocado de uma das duas citações: títulos, palavras dos enunciados e nomes de partes da página
ENTRE_ASPAS = {
    'Uma pequenina luz', 'As Palavras', 'Prece no Mediterrâneo', 'Jorge de Sena, poeta testemunha', 'Eugénio de Andrade: a palavra essencial',
    'Ana Luísa Amaral: reescrever a tradição', 'Poesia contemporânea: três modos de dizer', 'Para comparar dois poemas, por ordem',
    'Compara', 'Compare', 'Explique', 'Fundamenta', 'fundamentando', 'o modo como', 'fundamentando a tua resposta com', 'o modo como cada poema apresenta uma coisa frágil',
    'os dois', 'nos dois', 'mas só', 'mas não', 'enquanto', 'já', 'Verificar', 'o sujeito poético', 'o poema', 'a confirmar na Informação-Prova de 2027',
    'um relativo ao poema de Eugénio de Andrade e outro relativo ao poema de Alberto Caeiro', 'ou outros igualmente relevantes',
}


def cita_ok(texto):
    """Tudo o que o texto nosso põe entre «» é um bocado de uma das duas citações, uma citação oficial conferida ou está em ENTRE_ASPAS."""
    for m in re.finditer(r'«([^«»]+)»', texto):
        c = m.group(1)
        if c in ENTRE_ASPAS or c in OFICIAIS or any(c in cit or c.rstrip('.,') in cit for cit in CITACOES):
            continue
        raise AssertionError(('entre aspas e não conferido', c))


# ---------- item oficial: 2.ª fase, Grupo I, Parte A, item 2 ----------
PA = F2['grupos'][0]['partes'][0]
IT = PA['itens'][1]
assert IT['numero'] == 'I.2' and IT['cotacao'] == 13 and IT['obrigatorio'] is True and IT['verbo_instrucional'] == 'Explique'
P1, P2 = PA['textos']
assert (P1['rotulo'], P1['autor'], P2['rotulo'], P2['heteronimo']) == ('Poema 1', 'Eugénio de Andrade', 'Poema 2', 'Alberto Caeiro')
cr = IT['criterios']
top = ''
for t in cr['topicos']:
    top += '<li>%s<ul class="top">%s</ul></li>' % (md(t['rotulo']), ''.join('<li>%s</li>' % md(p) for p in t['pontos']))
ced, cl = cr['parametros']
assert ced['pontos'] == 10 and cl['pontos'] == 3 and cl['tabela'] == 'CL_3'
BARRAS = F2['grupos'][0]['nota_dos_criterios']
assert BARRAS == F1['grupos'][0]['nota_dos_criterios']
assert os.path.isfile(ROOT + '/exame/provas/2026-2f/grupo-i/index.html')

# o item de 2026 com o verbo «Compare»: 1.ª fase, Grupo I, Parte A, item 2 (dois excertos de romances)
IT1 = F1['grupos'][0]['partes'][0]['itens'][1]
assert IT1['numero'] == 'I.2' and IT1['cotacao'] == 13 and IT1['verbo_instrucional'] == 'Compare'
T_AMBOS = 'trata-se, em ambos os casos, de ambientes ruidosos (embora a intensidade dos sons seja diferente)'
assert IT1['criterios']['topicos'][0]['pontos'][0].startswith(T_AMBOS + ', pois, no mercado do peixe,') and ', enquanto, no mercado da Praça da Figueira,' in IT1['criterios']['topicos'][0]['pontos'][0]
D_UM = 'Explica o modo como um dos sujeitos poéticos perspetiva a escrita, abordando, adequadamente, um tópico de resposta.'
_n3 = [n for n in ced['niveis'] if n['nivel'] == 3][0]
assert _n3['pontuacao'] == 6 and D_UM in _n3['descritores'][2]
assert all(D_UM not in json.dumps(n['descritores'], ensure_ascii=False) for n in ced['niveis'] if n['nivel'] > 3)

REGRA_P2 = '«As respostas que não apresentem exatamente os termos ou interpretações constantes nos critérios específicos são classificadas em igualdade de circunstâncias com aquelas que os apresentem, desde que o seu conteúdo seja cientificamente válido, adequado ao solicitado e enquadrado pelos documentos curriculares de referência.»'
R_INTRO = 'exceto quando tal é expressamente requerido no item, as respostas não têm de apresentar um parágrafo introdutório nem um parágrafo conclusivo'
R_CONECT = 'sem recurso obrigatório a conectores interfrásicos'
R_CITAR = 'incumprimento das regras de citação de texto ou de referência a título de uma obra'
for _g in (json.dumps(F1['criterios']['gerais'], ensure_ascii=False), json.dumps(F2['criterios']['gerais'], ensure_ascii=False)):
    for _s in (REGRA_P2.strip('«»'), R_INTRO, R_CONECT, R_CITAR):
        assert _s in _g, _s
assert 'um relativo ao poema de Eugénio de Andrade e outro relativo ao poema de Alberto Caeiro' in cr['instrucao'] and 'ou outros igualmente relevantes' in cr['instrucao']
OFICIAIS = {REGRA_P2.strip('«»'), R_INTRO, R_CONECT, R_CITAR, T_AMBOS, D_UM, 'no mercado do peixe', 'enquanto, no mercado da Praça da Figueira'}

OFICIAL = (
    '<p>' + etq('oficial') + '</p>'
    '<p class="pag">Exame Final Nacional de Português, Prova 639, 2026, 2.ª fase, versão 2. Grupo I, Parte A, item 2. '
    'Poemas: enunciado, pp. 2-3; item: enunciado, p. 3; critério: critérios de classificação, pp. 6-7 (definitivos, publicados a 31/07/2026). '
    + lig('e2', 'Enunciado (PDF, eduqa.pt)') + ' e ' + lig('c2', 'critérios (PDF, eduqa.pt)') + '.</p>'
    '<h3>Parte A</h3><p class="instr"><span class="pag">Instrução da prova:</span> ' + md(PA['instrucao']) + '</p>'
    '<p class="pag">Os dois poemas da prova não se repetem aqui. Lê-os, com as notas, nas <a href="../../provas/2026-2f/grupo-i/">provas em cartões (2.ª fase, Grupo I)</a> ou no enunciado. As fontes que a prova indica são estas:</p>'
    '<p class="fonte">Poema 1: ' + md(P1['fonte']) + '</p>'
    '<p class="fonte">Poema 2: ' + md(P2['fonte']) + '</p>'
    '<h3>Item 2 (13 pontos; conta sempre para a classificação)</h3>'
    '<p class="enun"><b>2.</b> ' + md(IT['enunciado'][0]) + '</p>'
    '<h3>Critério específico (critérios, pp. 6-7)</h3>'
    '<p>' + md(cr['instrucao']) + '</p><ul class="top">' + top + '</ul>'
    '<p class="pag">Regra de leitura dos tópicos (critérios, p. 4): «' + md(BARRAS) + '»</p>'
    '<h3>' + ced['nome'] + ' (C-ED): ' + str(ced['pontos']) + ' pontos</h3>'
    + tabela_niveis(ced['niveis'], 'Níveis de desempenho do parâmetro C-ED, item 2') +
    '<p class="pag">' + md(ced['nota_de_rodape']) + '</p>'
    '<h3>' + cl['nome'] + ' (CL): ' + str(cl['pontos']) + ' pontos</h3>'
    '<p>' + md(cl['texto']) + '</p>' + tabela_cl('CL_3') +
    '<p class="pag">' + md(cl['nota_de_rodape']) + '</p>'
)

# ---------- texto de apoio: as citações curtas e onde ler os poemas inteiros ----------
APOIO = (
    '<p class="texto-t">Dois poemas, duas citações curtas</p>'
    '<p class="texto-a">Os dois poemas têm direitos de autor. Aqui ficam só as duas citações que as lições do módulo 8 já trazem. Os poemas inteiros estão no manual.</p>'
    '<p class="notas-t">Jorge de Sena, «Uma pequenina luz»</p>'
    '<p class="cit">«' + C_SENA + '»</p>'
    '<p class="fonte">Vem no fim do poema, segundo a ' + LIG3 + ', de onde é a citação. A barra separa dois versos.</p>'
    '<ul class="notas"><li><b>O que a lição diz do poema</b> (resumo, não são versos): a luz é pequena e trémula e está no meio das pessoas; não aquece, não ilumina os rostos, não custa dinheiro; há quem sopre com raiva para a apagar.</li>'
    '<li><b>elas</b>: segundo a lição, a exatidão, a firmeza e a justiça, a que a luz é comparada.</li></ul>'
    '<p class="notas-t">Eugénio de Andrade, «As Palavras»</p>'
    '<p class="cit">«' + C_EUG + '»</p>'
    '<p class="fonte">É a abertura do poema. Citação da ' + LIG4 + '. A barra separa dois versos.</p>'
    '<ul class="notas"><li><b>O que a lição diz do poema</b> (resumo, não são versos): as palavras são frágeis e navegam sem segurança; o poema acaba com duas perguntas que ficam sem resposta, quem as ouve e quem as recolhe.</li></ul>'
    '<p class="notas-t">Onde ler os poemas inteiros</p>'
    '<ul class="notas"><li><b>Abre o manual</b>, ' + MANUAL + ', em «Uma pequenina luz», de Jorge de Sena, e em «As Palavras», de Eugénio de Andrade. As lições não dão a página: procura os títulos no índice do manual.</li>'
    '<li><b>Ou abre a lição</b> de cada poema, que diz onde o podes ler: a lição M8-F03 e a lição M8-F04, nas ligações de cima.</li></ul>'
)

PEDIDO = ('Compara o modo como cada poema apresenta uma coisa frágil (a luz, em «Uma pequenina luz», de Jorge de Sena; as palavras, em «As Palavras», de Eugénio de Andrade), '
          'fundamentando a tua resposta com uma transcrição de cada poema.')
CX_PEDIDO = '<div class="caixa tr">' + etq('treino') + '<p class="enun">' + PEDIDO + '</p></div>'

RESP_A = ('Em «As Palavras», de Eugénio de Andrade, as palavras são frágeis: «São como um cristal, / as palavras.» '
          'Em «Uma pequenina luz», de Jorge de Sena, a luz é pequena, mas não se apaga: «Mas brilha.»')
RESP_B = ('Os dois poemas apresentam uma coisa frágil e os dois a comparam a outra. Em «As Palavras», a comparação vem na abertura, «São como um cristal, / as palavras.», '
          'e o poema acaba em perguntas que ficam sem resposta. Em «Uma pequenina luz», a comparação vem no fim, «Apenas como elas.», e é seguida de uma afirmação: «Mas brilha.» '
          'Nos dois a coisa frágil corre perigo, mas só o poema de Jorge de Sena acaba a dizer que ela resiste.')
EX = [
    ('«As Palavras», de Eugénio de Andrade, e «Uma pequenina luz», de Jorge de Sena, dão valor a uma coisa frágil, e os dois a dizem por comparação.',
     'Começa pelo eixo: diz logo o que os dois poemas têm em comum. Não tem parágrafo de introdução: este pedido não o exige e, sem pedido expresso, os critérios também não (p. 2).'),
    ('No poema de Eugénio de Andrade, a comparação abre o texto, «São como um cristal, / as palavras.», e a fragilidade fica em aberto: o poema termina com duas perguntas a que ninguém responde.',
     'Primeiro poema: a ideia, a transcrição e o que ela mostra. Falta o número dos versos, que as lições não dão. Juntá-lo é um hábito nosso, que os níveis dos critérios não exigem: se copiares do manual, indica-o.'),
    ('No poema de Jorge de Sena, a comparação vem no fim, «Apenas como elas.», e é logo seguida de uma oposição: «Mas brilha.»',
     'Segundo poema, pela mesma ordem. Usa a palavra em que tocaste no passo 2 e diz o que ela faz: opõe.'),
    ('Assim, os dois poemas mostram uma coisa frágil, mas não a deixam no mesmo ponto: em «As Palavras», não se sabe se alguém a recolhe; em «Uma pequenina luz», ela resiste.',
     'Diz o que se mantém e o que muda. É esta frase que faz da resposta uma comparação: sem ela, ficavam duas descrições, como na Resposta A.'),
]
exemplo = ''.join('<div class="anot"><p class="c">%s</p><p class="n">%s</p></div>' % (a, b) for a, b in EX)

TOK_S = [{'x': 'Apenas'}, {'x': 'como'}, {'x': 'elas.'}, {'x': '/', 'fixo': True}, {'x': 'Mas'}, {'x': 'brilha.'}]
TOK_E = [{'x': 'São'}, {'x': 'como'}, {'x': 'um'}, {'x': 'cristal,'}, {'x': '/', 'fixo': True}, {'x': 'as'}, {'x': 'palavras.'}]
assert ' '.join(t['x'] for t in TOK_S) == C_SENA and ' '.join(t['x'] for t in TOK_E) == C_EUG

AP = {'apoio': 'cit', 'apoioRot': 'Citações e onde ler os poemas'}

TREINO = {
    'id': 'poesia-contemporanea', 'viu': 'os critérios',
    'passos': [
        dict(AP, **{
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido',
            'o': 'Antes de ires aos poemas, lê o que te pedem: que verbo, sobre quê e com que condição.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO +
                 '<p>Este pedido foi escrito por nós. O item oficial de 2026 mais próximo é o item 2 da 2.ª fase, que diz assim:</p>'
                 '<div class="caixa of">' + etq('oficial') + '<p class="enun">' + md(IT['enunciado'][0]) + '</p>'
                 '<p class="pag">Prova 639, 2026, 2.ª fase, Grupo I, Parte A, item 2 (13 pontos). Enunciado, p. 3. O item, com o critério, está no cimo desta página.</p></div>'
                 '<p><b>O que é igual.</b> Dois poemas (na prova, um deles é de Eugénio de Andrade), um eixo dado no enunciado (lá, a escrita; aqui, uma coisa frágil) e transcrições de cada poema.</p>'
                 '<p><b>O que é diferente.</b> O verbo do item oficial é «Explique», e os critérios dão os tópicos poema a poema: «um relativo ao poema de Eugénio de Andrade e outro relativo ao poema de Alberto Caeiro» <span class="pag">(critérios, p. 6)</span>. '
                 'O pedido de treino usa «Compara»: tens de dizer também o que um poema tem a ver com o outro.</p>'
                 '<p>Em 2026, o verbo «Compare» aparece noutro item, sobre dois excertos de romances de José Saramago:</p>'
                 '<div class="caixa of">' + etq('oficial') + '<p class="enun">' + md(IT1['enunciado'][0]) + '</p><p class="enun">' + md(IT1['enunciado'][1]) + '</p>'
                 '<p class="pag">Prova 639, 2026, 1.ª fase, Grupo I, Parte A, item 2 (13 pontos). ' + lig('e1', 'Enunciado, p. 3 (PDF em eduqa.pt)') + '; ' + lig('c1', 'critérios, pp. 6-7 (PDF em eduqa.pt)') + '.</p></div>'},
                {'t': 'escolha', 'id': 'p4-pedido', 'etq': 'treino', 'curto': 'O que o pedido de treino manda fazer',
                 'p': 'O que tem de aparecer na tua resposta para o pedido de treino ficar cumprido?',
                 'o': [
                     {'t': 'Um resumo de «Uma pequenina luz» e, a seguir, um resumo de «As Palavras».',
                      'pista': '<p>Relê o primeiro verbo do pedido de treino. Um resumo diz o que está em cada poema. Diz o que um poema tem a ver com o outro?</p>'},
                     {'t': 'A vida de Jorge de Sena e a de Eugénio de Andrade, com as datas e os livros de cada um.',
                      'pista': '<p>Procura no pedido de treino o que se compara: vem logo depois de «Compara». Vê se o pedido fala dos poemas ou dos poetas.</p>'},
                     {'t': 'O que os dois poemas fazem com uma coisa frágil, com o que têm em comum e o que os separa, e uma transcrição de cada um.',
                      'pista': ''},
                     {'t': 'O nome do recurso expressivo de cada uma das duas citações.',
                      'pista': '<p>Relê as duas formas verbais do pedido de treino: «Compara» e «fundamentando». Vê se alguma delas manda dar um nome.</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Lê o pedido de treino aos bocados. Primeiro, o verbo. Depois, o que vem a seguir a «o modo como», até ao parêntese. Por fim, o que vem depois de «fundamentando a tua resposta com». A opção adequada traz as três partes e mais nada.</p>',
                 'f': '<p>O pedido tem um verbo, um eixo e uma condição. O verbo é <b>comparar</b>: dizer o que se mantém e o que muda de um poema para o outro. O eixo é a <b>coisa frágil</b> que cada poema apresenta. A condição é <b>uma transcrição de cada poema</b>.</p>'
                      '<p>O eixo vem no enunciado, como nos dois itens oficiais de cima (a escrita, num; as sensações, no outro). Não tens de o inventar: tens de o seguir nos dois textos.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'localizar', 'curto': 'Localizar', 'titulo': 'Localizar nas citações',
            'o': 'Duas buscas, uma em cada citação: a palavra que mostra o que o poema faz com a coisa frágil.',
            'blocos': [
                {'t': 'tocar', 'id': 'p4-sena', 'etq': 'treino', 'modo': 'palavras', 'curto': 'A palavra que mostra que a luz resiste',
                 'p': 'Na citação de «Uma pequenina luz», toca na palavra (ou nas palavras) que mostram que a luz resiste, apesar de tudo o que o poema disse dela. Depois toca em «Verificar».',
                 'tokens': TOK_S,
                 'nucleos': [[4]], 'permitidos': [4, 5], 'mostra': [4],
                 'notas': {'5': 'Aceite com «brilha»: as duas palavras leem-se juntas (apesar de tudo, a luz brilha).'},
                 'pistas': [
                     {'se': [0], 'x': '<p>«Apenas» limita: diz que a luz é só como «elas», e mais nada. A pergunta é pela palavra que vira a frase para o outro lado. Procura no segundo verso da citação.</p>'},
                     {'se': [1, 2], 'x': '<p>«como elas» faz a comparação (o texto de apoio diz quem são «elas»). A pergunta é por outra coisa: a palavra que opõe o que vem depois ao que vem antes.</p>'},
                     {'so': [5], 'x': '<p>«brilha» diz o que a luz faz. Ainda não diz que o faz apesar de tudo: procura, no mesmo verso, a palavra que marca essa oposição.</p>'},
                 ],
                 'falta': '<p>Procura, no segundo verso da citação, a palavra que marca uma oposição.</p>',
                 'pista2': '<p>Fica só no segundo verso da citação, que tem duas palavras. Uma diz o que a luz faz. A outra é uma conjunção: liga este verso ao que vem antes e opõe-no a ele.</p>',
                 'f': '<p>«Mas» é uma conjunção coordenativa adversativa: opõe o brilho a tudo o que vem antes. Segundo a lição M8-F03, a luz é pequena e trémula, não aquece, não ilumina os rostos, e há quem sopre com raiva para a apagar. No fim, o poema afirma, em duas palavras: «Mas brilha.» Guarda esta palavra: vais precisar dela na tua resposta.</p>'},
                {'t': 'tocar', 'id': 'p4-eugenio', 'etq': 'treino', 'modo': 'palavras', 'curto': 'A palavra que diz a que são comparadas as palavras',
                 'p': 'Na citação de «As Palavras», toca na palavra que diz a que são comparadas as palavras. Depois toca em «Verificar».',
                 'tokens': TOK_E,
                 'nucleos': [[3]], 'permitidos': [2, 3], 'mostra': [3],
                 'notas': {'2': 'Aceite com «um»: o artigo e o nome leem-se juntos («um cristal»).'},
                 'pistas': [
                     {'se': [5, 6], 'x': '<p>«as palavras» é aquilo de que o poema fala: o primeiro termo da comparação. A pergunta é pelo segundo termo, que vem depois de «como».</p>'},
                     {'se': [1], 'x': '<p>«como» é a palavra que faz a comparação. A pergunta é pelo que vem a seguir: aquilo a que as palavras são comparadas.</p>'},
                     {'se': [0], 'x': '<p>«São» é o verbo. Procura o nome que vem depois de «como».</p>'},
                     {'so': [2], 'x': '<p>«um» é o artigo. Falta o nome que ele acompanha.</p>'},
                 ],
                 'falta': '<p>Procura o nome que vem depois de «como».</p>',
                 'pista2': '<p>Fica no primeiro verso da citação. Uma comparação tem dois termos e uma palavra que os liga. O primeiro termo está no segundo verso; a palavra que liga é «como». Toca no que sobra: o nome do segundo termo.</p>',
                 'f': '<p>«cristal»: a lição M8-F04 lê nesta comparação uma coisa frágil, que também pode ferir. Repara que as duas citações têm «como»: os dois poemas comparam. Em «As Palavras», a comparação abre o poema; em «Uma pequenina luz», segundo a lição M8-F03, a comparação vem no fim.</p>'
                      '<p class="pag">Duas citações não são dois poemas. Antes de escreveres, lê os poemas inteiros no manual.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'distinguir', 'curto': 'Insuficiente ou adequada', 'titulo': 'Distinguir uma resposta insuficiente de uma adequada',
            'o': 'Duas respostas ao pedido de treino. As duas usam transcrições e nenhuma diz nada de errado sobre os poemas.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO + '<div class="caixa tr">' + etq('treino') +
                 '<p><b>Resposta A.</b> <span class="cit">' + RESP_A + '</span></p>'
                 '<p><b>Resposta B.</b> <span class="cit">' + RESP_B + '</span></p></div>'},
                {'t': 'escolha', 'id': 'p4-distinguir', 'etq': 'treino', 'curto': 'A resposta que fica aquém, e porquê',
                 'p': 'Que resposta fica aquém do pedido, e porquê?',
                 'o': [
                     {'t': 'A Resposta B: fala de como cada poema acaba, e o pedido só fala de uma coisa frágil.',
                      'pista': '<p>Relê o pedido: «o modo como cada poema apresenta uma coisa frágil». Vê se o que o poema diz dela no fim faz parte da maneira de a apresentar.</p>'},
                     {'t': 'A Resposta A: põe um poema a seguir ao outro e não diz o que têm em comum nem o que os separa.',
                      'pista': ''},
                     {'t': 'A Resposta A: as transcrições que usa são curtas de mais.',
                      'pista': '<p>Vê o que o pedido diz sobre as transcrições: pede uma de cada poema. Procura se fixa um tamanho.</p>'},
                     {'t': 'A Resposta B: trata os dois poemas no mesmo parágrafo, e cada poema devia ter o seu.',
                      'pista': '<p>Procura no pedido alguma regra sobre parágrafos. Depois vê o que o verbo «Compara» obriga a fazer com os dois poemas.</p>'},
                 ], 'c': 1,
                 'pista2': '<p>Procura, em cada resposta, as palavras que ligam um poema ao outro: «os dois», «nos dois», «mas só». Vê qual das respostas as tem e qual fala de um poema e depois do outro, sem ligação.</p>',
                 'f': '<p>A Resposta A não erra: cada frase traz a sua transcrição. Mas são duas descrições lado a lado. Falta dizer o que se mantém e o que muda de um poema para o outro, e é isso que «Compara» pede.</p>'
                      '<p>No item oficial com o verbo «Compare» (1.ª fase, item 2), os tópicos dos critérios juntam sempre os dois textos na mesma frase. O primeiro começa assim: «' + T_AMBOS + '», e continua com «no mercado do peixe» de um lado e «enquanto, no mercado da Praça da Figueira» do outro <span class="pag">(critérios da 1.ª fase, p. 6)</span>.</p>'
                      '<p>No item oficial dos dois poemas (2.ª fase, item 2), o verbo é «Explique» e os critérios pedem um tópico por poema: lá, uma resposta como a A cumpria a estrutura pedida. É o verbo «Compara», do pedido de treino, que a deixa aquém.</p>'
                      '<p>Nos dois casos, os dois poemas têm de ser tratados. Lá, quem só trata um não passa do nível 3, que vale 6 dos 10 pontos: «' + D_UM + '» <span class="pag">(critérios da 2.ª fase, p. 7)</span>.</p>'
                      '<p class="pag">Usar estes critérios em dois poemas que não saíram na prova é leitura nossa.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'escrever', 'curto': 'A tua resposta', 'titulo': 'Escrever a tua resposta, sem pistas',
            'o': 'Agora és tu. Ficam contigo as duas citações e o manual; as respostas A e B e as explicações ficam nos passos anteriores.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO +
                 '<p><b>Abre o manual</b> e lê os dois poemas inteiros antes de escreveres. Podes usar as duas citações desta página ou outras transcrições, copiadas do manual com o número do verso.</p>'
                 '<p class="pag">Na prova, os itens deste tipo valem 13 pontos e não têm limite de palavras: o desconto por extensão só existe no item de resposta extensa (critérios, p. 3). Escreve o que for preciso para cumprires o pedido.</p>'},
                {'t': 'escrever', 'id': 'p4-resposta', 'curto': 'Resposta escrita: a comparação dos dois poemas',
                 'rotulo': 'A tua resposta', 'linhas': 9,
                 'ajuda': 'Escreve aqui ou no papel. Quando acabares, guarda: só depois aparecem os critérios e o exemplo comentado.'},
            ],
        }),
        dict(AP, **{
            'id': 'comparar', 'curto': 'Conferir', 'titulo': 'Conferir com os critérios e com um exemplo comentado', 'precisa': 'p4-resposta',
            'o': 'Lê a tua primeira versão ao lado dos tópicos e do exemplo. Não há classificação automática: quem decide o que falta és tu, e depois o docente.',
            'blocos': [
                {'t': 'ver1', 'de': 'p4-resposta'},
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') +
                 '<p><b>Tópicos de resposta</b> (feitos por nós, à maneira dos critérios oficiais).</p><ul class="top">'
                 '<li><b>O eixo.</b> Os dois poemas apresentam uma coisa frágil e dão-lhe valor: as palavras, em «As Palavras»; uma luz pequena, em «Uma pequenina luz».</li>'
                 '<li><b>«As Palavras».</b> As palavras são comparadas a um cristal logo na abertura: «São como um cristal, / as palavras.» Segundo a lição M8-F04, são frágeis, navegam sem segurança e podem perder-se: o poema acaba com duas perguntas que ficam sem resposta.</li>'
                 '<li><b>«Uma pequenina luz».</b> Segundo a lição M8-F03, a luz é pequena e trémula, e há quem sopre com raiva para a apagar. No fim do poema, segundo a mesma lição, vem «Apenas como elas. / Mas brilha.»: a luz é comparada à exatidão, à firmeza e à justiça e, apesar de tudo, brilha.</li>'
                 '<li><b>O que se mantém e o que muda.</b> Mantém-se a coisa frágil, dita por comparação e em perigo. Muda o fim: «As Palavras» acaba em pergunta; «Uma pequenina luz» acaba a afirmar que a luz brilha. '
                 'Muda também aquilo de que se fala: da própria poesia, num caso (a lição chama-lhe arte poética); de uma luz posta ao lado da justiça, no outro (a lição vê aí o poeta como testemunha).</li></ul>'
                 '<p class="pag">Estes tópicos apoiam-se nas lições M8-F03 e M8-F04 e nas duas citações. Confere-os com os poemas inteiros, no manual: se o texto te mostrar outra coisa, vale o texto.</p></div>'
                 '<div class="caixa of">' + etq('oficial') + '<p><b>Outras formulações também contam.</b> ' + REGRA_P2 + ' <span class="pag">(critérios gerais, p. 2)</span></p>'
                 '<p>E os tópicos de cada item são dados com a fórmula «ou outros igualmente relevantes» <span class="pag">(critérios da 2.ª fase, p. 6, para o item 2)</span>.</p></div>'},
                {'t': 'lista', 'id': 'p4-conf', 'titulo': 'Confere a tua primeira versão',
                 'intro': '<p class="ajuda">Marca o que já está na tua resposta. O que ficar por marcar é o que vais rever no passo seguinte.</p>',
                 'itens': [
                     'Disse o eixo: o que os dois poemas têm em comum.',
                     'Disse o que cada poema faz com a coisa frágil (a luz, num; as palavras, no outro).',
                     'Disse pelo menos uma diferença entre os dois poemas, e não só duas descrições seguidas.',
                     'Usei uma transcrição de cada poema, entre aspas, copiada letra a letra.',
                     'Se copiei do manual, juntei o número do verso (hábito nosso, não é exigência dos critérios).',
                     'Cada transcrição vem acompanhada do que ela mostra.',
                     'Não atribuí aos poemas o que eles não dizem: o que afirmei confere com o texto do manual.',
                     'Escrevi «o sujeito poético» ou «o poema» para quem fala, sem confundir a voz do poema com a vida do poeta.',
                     'Escrevi os títulos dos poemas entre aspas e os nomes dos dois poetas sem erros.',
                     'Reli a ortografia, a pontuação e as aspas das transcrições.',
                 ]},
                {'t': 'html', 'h': '<h3>Um exemplo comentado</h3><p class="ajuda">Uma resposta possível, escrita por nós só com as duas citações desta página. Não é a única e não é oficial.</p>' + exemplo +
                 '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). O eixo; o primeiro poema (a ideia, a transcrição e o que ela mostra); o segundo poema, pela mesma ordem; o que se mantém e o que muda. '
                 'É a ordem do cartão «Para comparar dois poemas, por ordem», do aquecimento da sessão 17.</p>'
                 '<p>Os critérios não impõem esta ordem nem conectores certos: «' + R_INTRO + '» e a clareza pode ser assegurada «' + R_CONECT + '» <span class="pag">(critérios gerais, p. 2)</span>. '
                 'Para passar de um poema ao outro, «enquanto» ou «já» servem tão bem como «mas não».</p></div>'
                 '<p class="pag">Correção linguística: no item oficial vale 3 dos 13 pontos (tabela no item oficial, no cimo da página; critérios, p. 7). Entre os erros do tipo A está o «' + R_CITAR + '» (critérios, p. 2).</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'rever', 'curto': 'Rever', 'titulo': 'Rever a tua resposta', 'precisa': 'p4-resposta',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres os critérios, a página diz isso junto dela. Escreve a versão revista: muda só o que os critérios e o exemplo te mostraram que faltava.',
            'blocos': [
                {'t': 'rever', 'de': 'p4-resposta', 'curto': 'Versão revista da resposta', 'linhas': 9},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Outro par.</b> O mesmo plano serve para outros dois poemas do módulo 8. A ' + LIG5 + ' põe em paralelo «Prece no Mediterrâneo», de Ana Luísa Amaral, e «As Palavras».</p></div>'
                 '<div class="caixa nossa"><p><b>Sobre 2027.</b> Os itens oficiais e os critérios citados são de 2026. A estrutura da prova de 2027, incluindo os poetas e os tipos de item do Grupo I, está a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        }),
    ],
}

CAB = (
    sobre('poesia-contemporanea', 'Poesia contemporânea') +
    '<h1>Dois poemas, um eixo</h1>'
    '<p class="lede">Dois poemas do módulo 8, seis passos e uma comparação escrita por ti. Liga-se à ' + sessao('s17', 'Poesia contemporânea: três modos de dizer') + ' e ao seu ' + aquecimento('s17') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Comparar dois poemas a partir de um eixo dado no pedido, com apoio numa transcrição de cada um, numa resposta restrita.</dd></div>'
    '<div><dt>Item oficial a que se liga</dt><dd>Prova 639, 2026, 2.ª fase, Grupo I, Parte A, item 2 (resposta restrita, 13 pontos): explicar o modo como, em cada um de dois poemas, o sujeito poético perspetiva a escrita, com transcrições. '
    + lig('e2', 'Enunciado, pp. 2-3 (PDF em eduqa.pt)') + '; ' + lig('c2', 'critérios, pp. 6-7 (PDF em eduqa.pt)') + '. Critérios definitivos, publicados a 31/07/2026.</dd></div>'
    '<div><dt>O que é igual e o que é diferente</dt><dd>Igual: dois poemas, um eixo dado no enunciado, transcrições de cada poema. Diferente: o item oficial manda explicar cada poema e não usa o verbo «Compare». '
    'Em 2026, esse verbo só aparece no Grupo I no item 2 da 1.ª fase, sobre dois excertos de romances (' + lig('e1', 'enunciado, p. 3') + '; ' + lig('c1', 'critérios, pp. 6-7') + '). Nenhum item de 2026 manda comparar dois poemas com esse verbo.</dd></div>'
    '<div><dt>Os textos</dt><dd>Os dois poemas do treino têm direitos de autor. A página mostra só duas citações curtas, as que as lições do módulo 8 já trazem, e indica onde ler os poemas inteiros: no manual.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<details class="dobra"><summary>Ver o item oficial: item, cotação e critério</summary><div class="dentro">' + OFICIAL + '</div></details>'
)

# o verbo «Compare» não aparece em mais nenhum item do Grupo I das duas fases
_verbos = [(f, i['numero']) for f, F in (('1f', F1), ('2f', F2)) for p in F['grupos'][0]['partes'] for i in p['itens']
           if re.search(r'\bCompar', ' '.join(i['enunciado']))]
assert _verbos == [('1f', 'I.2')], _verbos

NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB.replace(OFICIAL, '') + APOIO
for _s in [md(IT['enunciado'][0]), md(IT1['enunciado'][0]), md(IT1['enunciado'][1])]:
    assert _s in NOSSO
    NOSSO = NOSSO.replace(json.dumps(_s, ensure_ascii=False)[1:-1], '').replace(_s, '')
cita_ok(NOSSO)
# 12/11/2026 (revisão): a lição M8-F03 põe a citação «no fim» do poema; a página não diz por conta própria que é o último verso
assert not re.search(r'(?i)\bfech(o|a)\b', NOSSO), 'a página não afirma que a citação fecha o poema'


def construir():
    lint('poesia-contemporanea', NOSSO)
    return pagina_treino('poesia-contemporanea', 'poesia-contemporanea/', 'Poesia contemporânea', 'Treino 4: dois poemas, um eixo | Português',
                         'Treino da preparação de exame de Português: comparar dois poemas a partir de um eixo, com duas citações curtas, seis passos e uma resposta escrita por ti.', CAB, {'cit': APOIO}, TREINO)
