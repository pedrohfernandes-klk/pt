"""12/11/2026: treino 5, «Uma inferência, dois apoios, um limite» (exame/treinos/conto/), ligado à sessão 18.

O conto do treino, «George», de Maria Judite de Carvalho, tem direitos de autor. A página mostra só um recorte de duas
frases, o que a lição M8-F16 já publica, e remete para o manual. O recorte confere-se aqui, letra a letra, com o cartão
da lição de onde vem; o que se diz do conto além do recorte é resumo das lições M8-F08 e M8-F16, e as frases em que se
apoia também se conferem. Nenhuma frase do conto é reconstituída de memória.
"""
from .base import *

# ---------- as lições do M8 de onde vêm o recorte e o que se diz do conto ----------
L8, H8 = licao('f08')
L16, H16 = licao('f16')
H3I = open(ROOT + '/m8/m8-george-tres-idades/index.html', encoding='utf-8').read()

# o recorte: as únicas palavras do conto que a página mostra
RECORTE = 'À sua frente uma senhora de idade, primeiro esboçada, finalmente completa, olha-a atentamente. De idade não, George detesta eufemismos, mesmo só pensados, uma mulher velha.'
FRASE1, FRASE2 = RECORTE.split('. ')[0] + '.', RECORTE.split('. ')[1]
assert FRASE1 + ' ' + FRASE2 == RECORTE
CITACOES = {RECORTE: ('m8/licao-m8-f16/', L16)}
assert '«%s»' % RECORTE in L16, 'recorte que a lição não publica'
# tal e qual no ficheiro publicado, dentro da citação em bloco do cartão «As palavras confirmadas»
assert '<blockquote class=\\"prosa\\">«%s»<\\/blockquote>' % RECORTE in H16
assert '"titulo":"As palavras confirmadas","rot":"Lê de perto"' in H16

# o que se diz do conto e do recorte além das duas frases é resumo das lições: as frases de apoio têm de lá estar
for _s in ('Maria Judite de Carvalho, «George», em Seta Despedida, Mem Martins, Europa-América, 1995', 'A fonte não indica a página da edição',
           'O resto do conto lê-se na edição da turma', 'No conto, a narração cruza perceção e vida interior', 'A palavra «não» marca a recusa',
           'Um eufemismo atenua uma expressão potencialmente dura', 'a designação mais atenuada da idade é recusada e substituída por uma nomeação direta',
           'A narração atribui a recusa a George e acrescenta que as palavras podem ser apenas pensadas',
           'Não concluas que já conheces todos os sentimentos de George sobre o envelhecimento',
           'A referência a palavras apenas pensadas impede tomar a passagem por diálogo pronunciado',
           'Confundir a rejeição da palavra com rejeição da pessoa acrescenta uma atitude que o recorte não comprova',
           'Não revela uma biografia completa nem demonstra hostilidade entre as duas mulheres do encontro',
           'O papel do encontro na estrutura da obra exige ler além dele'):
    assert _s in L16, ('lição M8-F16', _s)
for _s in ('Uma mulher encontra a rapariga que foi e a velha que vai ser.', 'Chamam-se Gi, George, Georgina', 'três nomes para uma só pessoa',
           '«George» é de Seta Despedida (1995)'):
    assert _s in L8, ('lição M8-F08', _s)
assert '<title>Lição M8-F08: «George», uma mulher em três idades</title>' in H8 and '<i>Novo Sentidos 12</i>, ASA, 2023' in H8
assert '<title>Recorte de «George» | Português</title>' in H16
# as lições não dão a página do manual
assert not re.search(r'(?i)manual[^.<]*\bp(p|ág)?\. ?\d', L8 + L16)
for _s in ('<title>Três idades, uma mulher, um leitor ', 'Abre o manual em «George», de Maria Judite de Carvalho', '"titulo":"Passagem, leitura, limite"',
           'Inclui a tua interpretação, uma passagem que a apoie e algo que essa passagem não esclareça', 'Podes começar pela passagem ou pela ideia'):
    assert _s in H3I, ('exercício longo do M8', _s)
# o pedido de escrita da sessão 18 também manda sustentar a leitura em pistas e separar inferência de invenção
assert 'distingue inferência de invenção' in SESSOES['s18']['writing']['prompt']
# e o aquecimento da sessão tem o mesmo título e o mesmo objetivo
_s18 = json.load(open(ROOT + '/docs/pedagogia/exame-aquecimentos/s18.json', encoding='utf-8'))
assert _s18['titulo'] == SESSOES['s18']['title'] and 'fundamentar inferências em «George»' in _s18['cartoes'][0]['html']

M8 = '../../../m8/'
LIG8 = '<a href="%slicao-m8-f08/">lição M8-F08 («George», uma mulher em três idades)</a>' % M8
LIG16 = '<a href="%slicao-m8-f16/">lição M8-F16 (Recorte de «George»)</a>' % M8
LIG3I = '<a href="%sm8-george-tres-idades/">«Três idades, uma mulher, um leitor»</a>' % M8
MANUAL = '<i>Novo Sentidos 12</i> (ASA, 2023)'

# o que pode vir entre «» no texto nosso sem ser bocado do recorte: títulos, palavras dos enunciados e nomes de partes da página
ENTRE_ASPAS = {
    'George', 'Três idades, uma mulher, um leitor', 'Passagem, leitura, limite', 'As palavras confirmadas', 'Conto: o que o texto deixa por dizer',
    'Infira', 'Explicite', 'Compare', 'Verificar', 'evidenciado no recorte', 'fundamentando a tua resposta com', 'frontal',
}


def cita_ok(texto):
    """Tudo o que o texto nosso põe entre «» é um bocado do recorte, uma citação oficial conferida ou está em ENTRE_ASPAS."""
    for m in re.finditer(r'«([^«»]+)»', texto):
        c = m.group(1)
        if c in ENTRE_ASPAS or c in OFICIAIS or any(c in cit or c.rstrip('.,') in cit for cit in CITACOES):
            continue
        raise AssertionError(('entre aspas e não conferido', c))


# ---------- item oficial: 2.ª fase, Grupo I, Parte B, item 4 ----------
PB = F2['grupos'][0]['partes'][1]
IT = PB['itens'][0]
assert IT['numero'] == 'I.4' and IT['cotacao'] == 13 and IT['obrigatorio'] is True and IT['verbo_instrucional'] == 'Infira'
TX = PB['textos'][0]
assert (TX['autor'], TX['obra'], TX['genero']) == ('Almeida Garrett', '_Frei Luís de Sousa_', 'texto dramático (excerto)')
assert [l['n'] for l in TX['linhas']] == list(range(1, 37))
excerto = '<ol class="prosa">' + ''.join(
    '<li><span class="n">%d</span><span>%s</span></li>' % (l['n'], ('<b>%s</b>' % md(l['t'])) if l.get('personagem') else md(l['t'])) for l in TX['linhas']) + '</ol>'
notas = ''.join('<li value="%d">%s</li>' % (n['n'], md(n['texto'])) for n in PB['notas'])
cr = IT['criterios']
assert all(list(t) == ['pontos'] and len(t['pontos']) == 1 for t in cr['topicos']) and len(cr['topicos']) == 5
top = ''.join('<li>%s</li>' % md(t['pontos'][0]) for t in cr['topicos'])
ced, cl = cr['parametros']
assert ced['pontos'] == 10 and cl['pontos'] == 3 and cl['tabela'] == 'CL_3'
BARRAS = F2['grupos'][0]['nota_dos_criterios']
assert BARRAS == F1['grupos'][0]['nota_dos_criterios']
assert 'os critérios dão «ll. 1-2»' in cr['nota_nossa'] and 'estão nas linhas 2 e 3' in cr['nota_nossa']
assert 'Órfã de pai e de' in TX['linhas'][1]['t'] and TX['linhas'][2]['t'].startswith('mãe...') and 'e de família e de nome' in TX['linhas'][2]['t']

# o verbo «Infira» só aparece neste item, em todo o Grupo I das duas fases; os textos narrativos de 2026 estão na Parte A da 1.ª fase
_infira = [(f, i['numero']) for f, F in (('1f', F1), ('2f', F2)) for p in F['grupos'][0]['partes'] for i in p['itens']
           if re.search(r'\bInfir', ' '.join(i['enunciado']))]
assert _infira == [('2f', 'I.4')], _infira
_generos = {(f, p['id']): [t['genero'] for t in p.get('textos', [])] for f, F in (('1f', F1), ('2f', F2)) for p in F['grupos'][0]['partes']}
assert _generos == {('1f', 'A'): ['romance (excerto)', 'romance (excerto)'], ('1f', 'B'): ['poema'], ('1f', 'C'): [],
                    ('2f', 'A'): ['poema', 'poema'], ('2f', 'B'): ['texto dramático (excerto)'], ('2f', 'C'): []}, _generos
PA1 = F1['grupos'][0]['partes'][0]
assert [(i['numero'], i['verbo_instrucional'], i['tipo']) for i in PA1['itens'][:2]] == [
    ('I.1', 'Explicite', 'construção: resposta restrita'), ('I.2', 'Compare', 'construção: resposta restrita')]
assert PA1['itens'][2]['tipo'].startswith('seleção')
assert [t['autor'] for t in PA1['textos']] == ['José Saramago', 'José Saramago']
# 12/11/2026 (revisão): o item 7 da 1.ª fase também é de resposta restrita e trata de romances, mas sem excerto dado na prova
PC1 = F1['grupos'][0]['partes'][2]
assert [(i['numero'], i['tipo']) for i in PC1['itens']] == [('I.7', 'construção: resposta restrita (breve exposição)')] and not PC1.get('textos')
assert 'obras de José Saramago' in PC1['itens'][0]['enunciado'][0] and '_Memorial do Convento_' in ' '.join(PC1['itens'][0]['enunciado'])
IT1 = PA1['itens'][0]
assert IT1['cotacao'] == 13 and len(IT1['enunciado']) == 2

# citações dos critérios usadas nos passos
D_DOIS = 'Infere dois traços da personalidade de Manuel, abordando, adequadamente, dois tópicos de resposta.'
D_UM = 'Infere um traço da personalidade de Manuel, abordando, adequadamente, um tópico de resposta.'
_n5 = [n for n in ced['niveis'] if n['nivel'] == 5][0]
_n3 = [n for n in ced['niveis'] if n['nivel'] == 3][0]
assert _n5['pontuacao'] == 10 and _n5['descritores'][0][0] == D_DOIS
assert _n3['pontuacao'] == 6 and D_UM in _n3['descritores'][2]
assert all(D_UM not in json.dumps(n['descritores'], ensure_ascii=False) for n in ced['niveis'] if n['nivel'] > 3)
T_RAC = 'racionalidade, pois, apesar do intenso sofrimento que o dilacera, ouve os argumentos do seu interlocutor e reformula o seu raciocínio'
assert cr['topicos'][2]['pontos'][0].startswith(T_RAC + ' («É verdade.') and cr['topicos'][2]['pontos'][0].endswith('– l. 18);')
I_DOIS = 'dois dos tópicos seguintes, ou outros igualmente relevantes'
assert cr['instrucao'] == 'Devem ser abordados **dois** dos tópicos seguintes, ou outros igualmente relevantes:'

REGRA_P2 = '«As respostas que não apresentem exatamente os termos ou interpretações constantes nos critérios específicos são classificadas em igualdade de circunstâncias com aquelas que os apresentem, desde que o seu conteúdo seja cientificamente válido, adequado ao solicitado e enquadrado pelos documentos curriculares de referência.»'
R_INTRO = 'exceto quando tal é expressamente requerido no item, as respostas não têm de apresentar um parágrafo introdutório nem um parágrafo conclusivo'
R_CONECT = 'sem recurso obrigatório a conectores interfrásicos'
R_CITAR = 'incumprimento das regras de citação de texto ou de referência a título de uma obra'
for _g in (json.dumps(F1['criterios']['gerais'], ensure_ascii=False), json.dumps(F2['criterios']['gerais'], ensure_ascii=False)):
    for _s in (REGRA_P2.strip('«»'), R_INTRO, R_CONECT, R_CITAR):
        assert _s in _g, _s
OFICIAIS = {REGRA_P2.strip('«»'), R_INTRO, R_CONECT, R_CITAR, D_DOIS, D_UM, T_RAC, I_DOIS, 'ou outros igualmente relevantes'}

OFICIAL = (
    '<p>' + etq('oficial') + '</p>'
    '<p class="pag">Exame Final Nacional de Português, Prova 639, 2026, 2.ª fase, versão 2. Grupo I, Parte B, item 4. '
    'Texto: enunciado, p. 4; item: enunciado, p. 5; critério: critérios de classificação, pp. 8-9 (definitivos, publicados a 31/07/2026). '
    + lig('e2', 'Enunciado (PDF, eduqa.pt)') + ' e ' + lig('c2', 'critérios (PDF, eduqa.pt)') + '.</p>'
    '<h3>Parte B</h3><p class="instr"><span class="pag">Instrução da prova:</span> ' + md(PB['instrucao']) + '</p>'
    + excerto +
    '<p class="fonte">' + md(TX['fonte']) + '</p>'
    '<p class="notas-t">Notas (da prova)</p><ol class="notas">' + notas + '</ol>'
    '<p class="pag">Na prova, o número das linhas vem à margem de 5 em 5; as linhas com o nome da personagem contam na numeração.</p>'
    '<h3>Item 4 (13 pontos; conta sempre para a classificação)</h3>'
    '<p class="enun"><b>4.</b> ' + md(IT['enunciado'][0]) + '</p>'
    '<h3>Critério específico (critérios, pp. 8-9)</h3>'
    '<p>' + md(cr['instrucao']) + '</p><ul class="top">' + top + '</ul>'
    '<p class="pag">Nota nossa: no primeiro tópico, os critérios dão as linhas 1 e 2; na numeração impressa da prova, essas palavras estão nas linhas 2 e 3.</p>'
    '<p class="pag">Regra de leitura dos tópicos (critérios, p. 4): «' + md(BARRAS) + '»</p>'
    '<h3>' + ced['nome'] + ' (C-ED): ' + str(ced['pontos']) + ' pontos</h3>'
    + tabela_niveis(ced['niveis'], 'Níveis de desempenho do parâmetro C-ED, item 4') +
    '<p class="pag">' + md(ced['nota_de_rodape']) + '</p>'
    '<h3>' + cl['nome'] + ' (CL): ' + str(cl['pontos']) + ' pontos</h3>'
    '<p>' + md(cl['texto']) + '</p>' + tabela_cl('CL_3') +
    '<p class="pag">' + md(cl['nota_de_rodape']) + '</p>'
)

# ---------- texto de apoio: o recorte e onde ler o conto inteiro ----------
APOIO = (
    '<p class="texto-t">«George»: um recorte de duas frases</p>'
    '<p class="texto-a">O conto tem direitos de autor. Aqui fica só o recorte que a lição M8-F16 já traz. O conto inteiro está no manual.</p>'
    '<p class="cit">«' + RECORTE + '»</p>'
    '<p class="fonte">Maria Judite de Carvalho, «George», em <i>Seta Despedida</i>, Mem Martins, Europa-América, 1995. Recorte da ' + LIG16 + ', cartão «As palavras confirmadas». '
    'A lição não dá a página nem as linhas.</p>'
    '<ul class="notas"><li><b>O que as lições dizem do conto</b> (resumo, não são frases do conto): uma mulher encontra a rapariga que foi e a velha que vai ser; '
    'chamam-se Gi, George e Georgina, três nomes para uma só pessoa; a narração cruza o que George vê com o que George pensa.</li>'
    '<li><b>eufemismos</b>: um eufemismo atenua uma expressão que podia soar dura.</li>'
    '<li><b>O que o recorte não diz</b>: quem é a mulher, nem o que acontece antes e depois. Para o saberes, lê o conto.</li></ul>'
    '<p class="notas-t">Onde ler o conto inteiro</p>'
    '<ul class="notas"><li><b>Abre o manual</b>, ' + MANUAL + ', em «George», de Maria Judite de Carvalho. As lições não dão a página: procura o título no índice do manual.</li>'
    '<li><b>Ou abre a lição</b> que acompanha a leitura do conto, a ' + LIG8 + ', e a lição do recorte, na ligação de cima.</li></ul>'
)

PEDIDO = ('Infere um traço da personalidade de George evidenciado no recorte, fundamentando a tua resposta com dois elementos textuais. '
          'Indica ainda uma conclusão que o recorte não permite tirar.')
CX_PEDIDO = '<div class="caixa tr">' + etq('treino') + '<p class="enun">' + PEDIDO + '</p></div>'

RESP_A = ('George detesta eufemismos, como diz o recorte: «George detesta eufemismos». Vê à sua frente uma mulher velha e fica com medo de envelhecer. '
          'Por isso não gosta dela.')
RESP_B = ('George é frontal na maneira de nomear as coisas. A mulher que tem à frente é apresentada como «uma senhora de idade», mas a expressão é logo recusada, «De idade não», '
          'e trocada por outra, direta: «uma mulher velha». Esta exigência vale até para o que não chega a ser dito: os eufemismos são recusados «mesmo só pensados». '
          'O recorte não permite concluir o que George sente pela mulher nem pela velhice: mostra apenas a relação dela com uma maneira de dizer.')
EX = [
    ('George é frontal na maneira de nomear o que vê.',
     'Começa pelo traço. É uma inferência porque passa de uma atitude perante as palavras, que o recorte mostra, para uma maneira de ser, que o recorte não escreve. Trocar uma palavra por um sinónimo não chegava. Não tem parágrafo de introdução: este pedido não o exige e, sem pedido expresso, os critérios também não (p. 2).'),
    ('A mulher que tem à frente é apresentada como «uma senhora de idade», mas a expressão é logo recusada, «De idade não», e trocada por uma designação direta: «uma mulher velha».',
     'Primeiro elemento textual e o que ele mostra. Usa a palavra em que tocaste no passo 2. Falta o número da linha, que a lição não dá. Juntá-lo é um hábito nosso (os critérios oficiais dão a linha nos tópicos, mas os níveis não a exigem): se tiveres o manual, indica-o.'),
    ('Esta exigência não vale só para o que se diz em voz alta: segundo a narração, George detesta eufemismos «mesmo só pensados».',
     'Segundo elemento, pela mesma ordem. Separa quem conta (a narração) de quem pensa (George): a correção não é uma fala.'),
    ('O recorte mostra, assim, a relação de George com uma maneira de dizer; não permite concluir o que ela sente pela mulher que a olha, nem pela velhice.',
     'O limite: o que o recorte deixa por dizer. Sem esta frase, a resposta podia passar por uma certeza sobre os sentimentos de George, como na Resposta A.'),
]
exemplo = ''.join('<div class="anot"><p class="c">%s</p><p class="n">%s</p></div>' % (a, b) for a, b in EX)

TOK_R = [{'x': x} for x in RECORTE.split(' ')]
TOK_2 = [{'x': x} for x in FRASE2.split(' ')]
assert len(TOK_R) == 25 and len(TOK_2) == 12 and ' '.join(t['x'] for t in TOK_R) == RECORTE and ' '.join(t['x'] for t in TOK_2) == FRASE2
assert [TOK_R[i]['x'] for i in (13, 14, 15)] == ['De', 'idade', 'não,'] and [TOK_2[i]['x'] for i in (6, 7, 8)] == ['mesmo', 'só', 'pensados,']

AP = {'apoio': 'cit', 'apoioRot': 'O recorte e onde ler o conto'}

TREINO = {
    'id': 'conto', 'viu': 'os critérios',
    'passos': [
        dict(AP, **{
            'id': 'pedido', 'curto': 'O pedido', 'titulo': 'Compreender o pedido',
            'o': 'Antes de ires ao recorte, lê o que te pedem: que verbo, com que condição e com que limite.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO +
                 '<p>Este pedido foi escrito por nós. O item oficial de 2026 mais próximo é o item 4 da 2.ª fase, que diz assim:</p>'
                 '<div class="caixa of">' + etq('oficial') + '<p class="enun">' + md(IT['enunciado'][0]) + '</p>'
                 '<p class="pag">Prova 639, 2026, 2.ª fase, Grupo I, Parte B, item 4 (13 pontos). Enunciado, p. 5. O item, com o excerto e o critério, está no cimo desta página.</p></div>'
                 '<p><b>O que é igual.</b> O verbo, que é inferir; uma personagem; o apoio em elementos textuais; uma resposta restrita.</p>'
                 '<p><b>O que é diferente.</b> O texto da prova é dramático, um excerto de <i>Frei Luís de Sousa</i>, de Almeida Garrett: só tem falas e didascálias, e é delas que se infere. '
                 '«George» é um conto: há um narrador, e é pela narração que ficas a saber o que George pensa. A prova pede dois traços. O pedido de treino pede um, porque o recorte só tem duas frases, '
                 'e junta-lhe um limite, que a prova não pede.</p>'
                 '<p>Em 2026, os itens de resposta restrita sobre um excerto narrativo dado na prova são os itens 1 e 2 da 1.ª fase, com dois excertos de romances de José Saramago. Usam outros verbos, «Explicite» e «Compare». '
                 'O item 7 da mesma fase pede uma breve exposição sobre um romance do mesmo autor, sem excerto. O item 1 diz assim:</p>'
                 '<div class="caixa of">' + etq('oficial') + '<p class="enun">' + md(IT1['enunciado'][0]) + '</p><p class="enun">' + md(IT1['enunciado'][1]) + '</p>'
                 '<p class="pag">Prova 639, 2026, 1.ª fase, Grupo I, Parte A, item 1 (13 pontos). ' + lig('e1', 'Enunciado, p. 3 (PDF em eduqa.pt)') + '; ' + lig('c1', 'critérios, pp. 4-5 (PDF em eduqa.pt)') + '.</p></div>'
                 '<p>No Grupo I das duas fases, o verbo «Infira» só aparece no item 4 da 2.ª fase. Nenhum item de 2026 manda inferir a partir de um conto.</p>'},
                {'t': 'escolha', 'id': 'p5-pedido', 'etq': 'treino', 'curto': 'O que o pedido de treino manda fazer',
                 'p': 'O que tem de aparecer na tua resposta para o pedido de treino ficar cumprido?',
                 'o': [
                     {'t': 'Um resumo do conto «George», do princípio ao fim, com tudo o que acontece às três figuras.',
                      'pista': '<p>Relê o primeiro verbo do pedido de treino e o que vem logo a seguir. Um resumo conta o que acontece. Vê se o pedido fala do que acontece ou de como George é.</p>'},
                     {'t': 'Um traço de George que o recorte sustenta, dois elementos textuais que o apoiem e uma conclusão que o recorte não permite.',
                      'pista': ''},
                     {'t': 'A tua opinião sobre George: se gostas dela ou não, e porquê, com dois exemplos do que tu farias no lugar dela.',
                      'pista': '<p>Procura no pedido de treino as palavras que dizem onde tem de estar o traço: «evidenciado no recorte». Vê se uma opinião tua está no recorte.</p>'},
                     {'t': 'Dois traços da personalidade de George, cada um com a sua transcrição do recorte, e mais nada.',
                      'pista': '<p>Estás a responder ao item oficial, que pede dois traços de Manuel. Relê o pedido de treino e conta: quantos traços, quantos elementos textuais, e o que pede a segunda frase.</p>'},
                 ], 'c': 1,
                 'pista2': '<p>Lê o pedido de treino aos bocados. Primeiro, o verbo e o que ele pede. Depois, o que vem a seguir a «fundamentando a tua resposta com». Por fim, a segunda frase. A opção adequada traz as três partes e mais nada.</p>',
                 'f': '<p>O pedido tem um verbo, uma condição e um limite. O verbo é <b>inferir</b>: chegar a uma ideia que o texto não escreve, a partir do que ele escreve. A condição são <b>dois elementos textuais</b>. '
                      'O limite é <b>uma conclusão que o recorte não permite tirar</b>.</p>'
                      '<p>Nos critérios do item oficial, o descritor do nível mais alto repete o verbo do enunciado: «' + D_DOIS + '» <span class="pag">(critérios, p. 8)</span>. '
                      'Lê sempre o verbo primeiro: é por ele que a resposta é medida.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'localizar', 'curto': 'Localizar', 'titulo': 'Localizar no recorte',
            'o': 'Duas buscas no recorte: a palavra que recusa uma maneira de dizer e as palavras que dizem onde essa recusa se passa.',
            'blocos': [
                {'t': 'tocar', 'id': 'p5-recusa', 'etq': 'treino', 'modo': 'palavras', 'curto': 'A palavra que recusa a primeira maneira de dizer a idade',
                 'p': 'No recorte, toca na palavra que recusa a primeira maneira de dizer a idade da mulher. Depois toca em «Verificar».',
                 'tokens': TOK_R,
                 'nucleos': [[15]], 'permitidos': [13, 14, 15], 'mostra': [15],
                 'notas': {'13': 'Aceite com «De idade»: são as palavras recusadas, e leem-se juntas com a que as recusa.',
                           '14': 'Aceite com «De idade»: são as palavras recusadas, e leem-se juntas com a que as recusa.'},
                 'pistas': [
                     {'so': [13, 14], 'x': '<p>«De idade» repete a expressão da primeira frase. Falta a palavra que a recusa: vem logo a seguir.</p>'},
                     {'se': [3, 4, 5, 6], 'x': '<p>«uma senhora de idade» é a primeira maneira de dizer a idade. A pergunta é pela palavra que a afasta: procura na segunda frase.</p>'},
                     {'se': [22, 23, 24], 'x': '<p>«uma mulher velha» é a maneira de dizer que fica no fim. Antes dela, há uma palavra que afasta a primeira: procura no início da segunda frase.</p>'},
                     {'se': [16, 17, 18], 'x': '<p>«George detesta eufemismos» dá a razão da troca. A pergunta é pela palavra que faz a recusa, antes da razão.</p>'},
                     {'se': [19, 20, 21], 'x': '<p>Essas palavras não recusam nenhuma expressão. A pergunta é pela palavra que afasta a primeira maneira de dizer a idade: procura no início da segunda frase.</p>'},
                     {'se': [0, 1, 2, 7, 8, 9, 10, 11, 12], 'x': '<p>Essas palavras são da primeira frase, que apresenta a mulher. A recusa está na segunda frase.</p>'},
                 ],
                 'falta': '<p>Procura, no início da segunda frase, a palavra que recusa a expressão da primeira.</p>',
                 'pista2': '<p>Fica só no início da segunda frase, antes do nome de George. São três palavras: duas repetem a expressão da primeira frase; a terceira é um advérbio de negação.</p>',
                 'f': '<p>«não» recusa «de idade», a expressão com que a primeira frase apresentou a mulher. Segundo a lição M8-F16, é uma correção: a designação atenuada é recusada e trocada por uma direta, «uma mulher velha». '
                      'Guarda esta correção: é o primeiro elemento textual da tua resposta.</p>'},
                {'t': 'tocar', 'id': 'p5-pensados', 'etq': 'treino', 'modo': 'palavras', 'curto': 'As palavras que mostram que a correção não é dita',
                 'p': 'Na segunda frase do recorte, toca na palavra (ou nas palavras) que mostram que esta correção não é dita em voz alta. Depois toca em «Verificar».',
                 'tokens': TOK_2,
                 'nucleos': [[8]], 'permitidos': [6, 7, 8], 'mostra': [8],
                 'notas': {'6': 'Aceite com «mesmo só»: as três palavras leem-se juntas.', '7': 'Aceite com «mesmo só»: as três palavras leem-se juntas.'},
                 'pistas': [
                     {'so': [6, 7], 'x': '<p>«mesmo» e «só» reforçam a palavra que vem a seguir. Falta essa palavra, que diz onde ficam os eufemismos.</p>'},
                     {'se': [0, 1, 2], 'x': '<p>«De idade não» faz a recusa, mas não diz se ela é falada ou pensada. Procura mais à frente.</p>'},
                     {'se': [3, 4, 5], 'x': '<p>«George detesta eufemismos» diz de quem é a atitude. Não diz se a correção sai em voz alta. Procura o que vem logo depois.</p>'},
                     {'se': [9, 10, 11], 'x': '<p>«uma mulher velha» é a designação que fica. A pergunta é por outra coisa: onde se passa a correção, na fala ou no pensamento.</p>'},
                 ],
                 'falta': '<p>Procura as palavras que dizem onde ficam os eufemismos de que a frase fala.</p>',
                 'pista2': '<p>Procura entre as duas últimas vírgulas da frase. São três palavras. A última é um particípio e diz onde ficam os eufemismos de que a frase fala: não chegam à boca.</p>',
                 'f': '<p>«pensados»: os eufemismos de que a frase fala nem chegam a ser ditos. A lição M8-F16 tira daqui duas coisas: a narração atribui a recusa a George, e a recusa passa-se no pensamento. '
                      'Não é uma resposta dita à mulher. É o segundo elemento textual da tua resposta.</p>'
                      '<p class="pag">Duas frases não são o conto. Para saberes quem é a mulher e o que acontece antes e depois, lê o conto inteiro no manual.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'separar', 'curto': 'Diz, sugere, acrescentas', 'titulo': 'Separar o que o recorte diz, o que sugere e o que lhe acrescentas',
            'o': 'Quatro afirmações sobre George. Uma está escrita no recorte, uma tem apoio nele, uma não tem apoio nenhum e uma vai contra ele.',
            'blocos': [
                {'t': 'escolha', 'id': 'p5-separar', 'etq': 'treino', 'curto': 'A afirmação que é uma inferência com apoio',
                 'p': 'Que afirmação é uma inferência com apoio no recorte: não está lá escrita, mas há palavras do recorte que a sustentam?',
                 'o': [
                     {'t': 'George detesta eufemismos.',
                      'pista': '<p>Procura estas palavras no recorte. Se lá estão, o texto di-lo: não precisas de inferir. Inferir é dar um passo a partir do que está escrito.</p>'},
                     {'t': 'George tem medo de envelhecer.',
                      'pista': '<p>Procura no recorte uma palavra de medo, ou um gesto que o mostre. Vê se o que encontras é sobre a velhice ou sobre uma maneira de a nomear.</p>'},
                     {'t': 'George é frontal na maneira de nomear as coisas.',
                      'pista': ''},
                     {'t': 'George diz à mulher, em voz alta, que ela é velha.',
                      'pista': '<p>Volta às palavras em que tocaste no passo 2, entre as duas últimas vírgulas. Vê se a correção chega a sair em voz alta.</p>'},
                 ], 'c': 2,
                 'pista2': '<p>Faz duas perguntas a cada afirmação. Primeira: está escrita no recorte, com estas palavras? Se está, o texto di-lo. Segunda: que palavras do recorte a sustentam? '
                           'Se não encontras nenhuma, és tu que a acrescentas. Sobra uma afirmação: a que não está escrita e tem palavras que a sustentam.</p>',
                 'f': '<ul class="top"><li><b>O recorte diz.</b> «George detesta eufemismos» está lá, com todas as letras. Copiar não é inferir.</li>'
                      '<li><b>O recorte sugere.</b> O recorte escreve uma atitude perante as palavras («George detesta eufemismos») e mostra um gesto: a correção («De idade não», «uma mulher velha»), que se passa no pensamento («mesmo só pensados»). '
                      'Daí a uma maneira de ser, a de quem é frontal, vai um passo que o recorte não escreve mas sustenta. É uma inferência com apoio. Dizer o mesmo por outras palavras não chegava.</li>'
                      '<li><b>Tu acrescentas.</b> O medo de envelhecer não tem nenhuma palavra do recorte a sustentá-lo. A lição M8-F16 avisa: o recorte mostra a relação de George com uma palavra, e não dá a conhecer tudo o que ela sente sobre o envelhecimento.</li>'
                      '<li><b>O recorte contraria.</b> A correção não é dita em voz alta: os eufemismos são recusados «mesmo só pensados».</li></ul>'
                      '<p>Os critérios do item oficial fazem o mesmo caminho: dão o nome de um traço que o excerto não escreve e, logo a seguir, o que no texto o mostra. Um dos tópicos começa assim: «' + T_RAC + '», '
                      'e segue-se a transcrição, com a linha <span class="pag">(critérios, p. 8)</span>.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'distinguir', 'curto': 'Insuficiente ou adequada', 'titulo': 'Distinguir uma resposta insuficiente de uma adequada',
            'o': 'Duas respostas ao pedido de treino. As duas falam de George e as duas usam palavras do recorte.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO + '<div class="caixa tr">' + etq('treino') +
                 '<p><b>Resposta A.</b> <span class="cit">' + RESP_A + '</span></p>'
                 '<p><b>Resposta B.</b> <span class="cit">' + RESP_B + '</span></p></div>'},
                {'t': 'escolha', 'id': 'p5-distinguir', 'etq': 'treino', 'curto': 'A resposta que fica aquém, e porquê',
                 'p': 'Que resposta fica aquém do pedido, e porquê?',
                 'o': [
                     {'t': 'A Resposta B: fala de palavras, e o pedido é sobre a personalidade de George.',
                      'pista': '<p>Relê o pedido: o traço tem de estar «evidenciado no recorte». Vê o que o recorte mostra George a fazer, e com quê.</p>'},
                     {'t': 'A Resposta A: repete o que o recorte já diz e junta-lhe um sentimento que nenhuma palavra do recorte mostra.',
                      'pista': ''},
                     {'t': 'A Resposta A: só tem três frases, e uma resposta destas precisa de mais.',
                      'pista': '<p>Procura no pedido um número de frases ou de palavras. Depois conta outra coisa na Resposta A: quantas afirmações têm apoio numa passagem do recorte.</p>'},
                     {'t': 'A Resposta B: acaba a dizer o que o recorte não permite concluir, e isso tira força à inferência.',
                      'pista': '<p>Relê a segunda frase do pedido. Vê se dizer o limite é uma fraqueza da resposta ou uma parte do que se pede.</p>'},
                 ], 'c': 1,
                 'pista2': '<p>Procura, em cada resposta, o que vem entre aspas. Depois pergunta, afirmação a afirmação: que palavras do recorte a sustentam? Numa das respostas, há duas afirmações que ficam sem nenhuma.</p>',
                 'f': '<p>A Resposta A começa por copiar: «George detesta eufemismos» está escrito, não é inferência. Depois salta para o medo de envelhecer e para a antipatia pela mulher, e nenhuma palavra do recorte sustenta nem um nem outra. '
                      'A Resposta B dá um nome ao traço, apoia-o em dois elementos textuais e diz onde o recorte para.</p>'
                      '<p>No item oficial, os critérios dão cinco traços possíveis de Manuel e pedem dois: «' + I_DOIS + '» <span class="pag">(critérios, p. 8)</span>. Há mais de uma inferência válida, desde que o texto a sustente.</p>'
                      '<p>Lá, quem infere um só traço não passa do nível 3, que vale 6 dos 10 pontos: «' + D_UM + '» <span class="pag">(critérios, pp. 8-9)</span>. '
                      'Este treino trabalha um traço de cada vez; na prova, repetes o mesmo caminho para o segundo.</p>'
                      '<p class="pag">Usar estes critérios num recorte que não saiu na prova é leitura nossa.</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'escrever', 'curto': 'A tua resposta', 'titulo': 'Escrever a tua resposta, sem pistas',
            'o': 'Agora és tu. Fica contigo o recorte; as respostas A e B e as explicações ficam nos passos anteriores.',
            'blocos': [
                {'t': 'html', 'h': CX_PEDIDO +
                 '<p>A tua resposta trata só do recorte. Podes inferir o traço dos passos anteriores ou outro, desde que duas passagens do recorte o sustentem. '
                 'Se tiveres o manual à mão, lê primeiro o conto inteiro: ajuda-te a ver o que o recorte, por si, não permite concluir.</p>'
                 '<p class="pag">Na prova, os itens deste tipo valem 13 pontos e não têm limite de palavras: o desconto por extensão só existe no item de resposta extensa (critérios, p. 3). Escreve o que for preciso para cumprires o pedido.</p>'},
                {'t': 'escrever', 'id': 'p5-resposta', 'curto': 'Resposta escrita: a inferência sobre George',
                 'rotulo': 'A tua resposta', 'linhas': 9,
                 'ajuda': 'Escreve aqui ou no papel. Quando acabares, guarda: só depois aparecem os critérios e o exemplo comentado.'},
            ],
        }),
        dict(AP, **{
            'id': 'comparar', 'curto': 'Conferir', 'titulo': 'Conferir com os critérios e com um exemplo comentado', 'precisa': 'p5-resposta',
            'o': 'Lê a tua primeira versão ao lado dos tópicos e do exemplo. Não há classificação automática: quem decide o que falta és tu, e depois o docente.',
            'blocos': [
                {'t': 'ver1', 'de': 'p5-resposta'},
                {'t': 'html', 'h': '<div class="caixa tr">' + etq('treino') +
                 '<p><b>Tópicos de resposta</b> (feitos por nós, à maneira dos critérios oficiais).</p><ul class="top">'
                 '<li><b>O traço.</b> Exigência com as palavras, até consigo mesma; frontalidade na maneira de nomear; ou recusa de atenuar o que vê. Vale outro nome, se o recorte o sustentar.</li>'
                 '<li><b>Primeiro elemento.</b> A correção: «uma senhora de idade» é recusada, «De idade não», e trocada por «uma mulher velha».</li>'
                 '<li><b>Segundo elemento.</b> «mesmo só pensados»: a exigência vale até no pensamento, e a correção não é dita à mulher. Em alternativa, «George detesta eufemismos», que atribui a atitude a George.</li>'
                 '<li><b>O limite.</b> O recorte não permite concluir, por exemplo, o que George sente pela velhice, o que sente pela mulher que a olha, quem é essa mulher, ou que haja hostilidade entre as duas.</li></ul>'
                 '<p class="pag">Estes tópicos apoiam-se no recorte e na lição M8-F16. Confere-os com o conto inteiro, no manual: se o texto te mostrar outra coisa, vale o texto.</p></div>'
                 '<div class="caixa of">' + etq('oficial') + '<p><b>Outras formulações também contam.</b> ' + REGRA_P2 + ' <span class="pag">(critérios gerais, p. 2)</span></p>'
                 '<p>E os tópicos de cada item são dados com a fórmula «ou outros igualmente relevantes» <span class="pag">(critérios da 2.ª fase, p. 8, para o item 4)</span>.</p></div>'},
                {'t': 'lista', 'id': 'p5-conf', 'titulo': 'Confere a tua primeira versão',
                 'intro': '<p class="ajuda">Marca o que já está na tua resposta. O que ficar por marcar é o que vais rever no passo seguinte.</p>',
                 'itens': [
                     'Dei um nome ao traço de George: uma maneira de ser que o recorte não escreve, e não só outra palavra para o que lá está.',
                     'Apoiei o traço em dois elementos textuais, entre aspas, copiados letra a letra.',
                     'Cada elemento vem acompanhado do que ele mostra.',
                     'Não dei como inferência o que o recorte já diz com todas as letras.',
                     'Indiquei uma conclusão que o recorte não permite tirar.',
                     'Não atribuí a George sentimentos, falas ou gestos que o recorte não mostra.',
                     'Separei quem conta (o narrador) de quem pensa (George): não escrevi que George disse o que só pensou.',
                     'Escrevi o título do conto entre aspas e o nome da autora sem erros.',
                     'Reli a ortografia, a pontuação e as aspas das transcrições.',
                 ]},
                {'t': 'html', 'h': '<h3>Um exemplo comentado</h3><p class="ajuda">Uma resposta possível, escrita por nós só com o recorte desta página. Não é a única e não é oficial.</p>' + exemplo +
                 '<div class="caixa nossa"><p><b>Uma maneira de organizar</b> (é nossa, não é exigência do exame). O traço; o primeiro elemento textual e o que ele mostra; o segundo, pela mesma ordem; o limite. '
                 'O exercício ' + LIG3I + ', do módulo 8, propõe o mesmo no cartão «Passagem, leitura, limite», e lembra que podes começar pela passagem ou pela ideia.</p>'
                 '<p>Os critérios não impõem esta ordem nem conectores certos: «' + R_INTRO + '» e a clareza pode ser assegurada «' + R_CONECT + '» <span class="pag">(critérios gerais, p. 2)</span>.</p></div>'
                 '<p class="pag">Correção linguística: no item oficial vale 3 dos 13 pontos (tabela no item oficial, no cimo da página; critérios, p. 9). Entre os erros do tipo A está o «' + R_CITAR + '» (critérios, p. 2).</p>'},
            ],
        }),
        dict(AP, **{
            'id': 'rever', 'curto': 'Rever', 'titulo': 'Rever a tua resposta', 'precisa': 'p5-resposta',
            'o': 'A primeira versão fica ao lado. Podes alterá-la; se o fizeres depois de veres os critérios, a página diz isso junto dela. Escreve a versão revista: muda só o que os critérios e o exemplo te mostraram que faltava.',
            'blocos': [
                {'t': 'rever', 'de': 'p5-resposta', 'curto': 'Versão revista da resposta', 'linhas': 9},
                {'t': 'registo'},
                {'t': 'html', 'h': '<div class="caixa nossa"><p><b>Outra passagem.</b> O mesmo plano serve para qualquer passagem de «George». Abre o manual, escolhe uma passagem sobre uma das três figuras e faz o mesmo: um traço, dois elementos textuais, um limite. '
                 'A ' + LIG8 + ' e o exercício ' + LIG3I + ' acompanham essa leitura.</p></div>'
                 '<div class="caixa nossa"><p><b>Sobre 2027.</b> Os itens oficiais e os critérios citados são de 2026. A estrutura da prova de 2027, incluindo as obras e os tipos de item do Grupo I, está a confirmar na Informação-Prova de 2027, que ainda não temos.</p></div>'},
            ],
        }),
    ],
}

CAB = (
    sobre('conto', 'Conto') +
    '<h1>Uma inferência, dois apoios, um limite</h1>'
    '<p class="lede">Um recorte de «George», de Maria Judite de Carvalho, sete passos e uma inferência escrita por ti. Liga-se à ' + sessao('s18', 'Conto: o que o texto deixa por dizer') + ' e ao seu ' + aquecimento('s18') + '.</p>'
    '<dl class="liga">'
    '<div><dt>Operação do exame que treinas</dt><dd>Fundamentar uma inferência sobre uma personagem com elementos do texto, numa resposta restrita: separar o que o texto diz, o que sugere e o que o leitor acrescenta sem apoio.</dd></div>'
    '<div><dt>Item oficial a que se liga</dt><dd>Prova 639, 2026, 2.ª fase, Grupo I, Parte B, item 4 (resposta restrita, 13 pontos): inferir dois traços da personalidade de uma personagem, com elementos textuais. '
    + lig('e2', 'Enunciado, pp. 4-5 (PDF em eduqa.pt)') + '; ' + lig('c2', 'critérios, pp. 8-9 (PDF em eduqa.pt)') + '. Critérios definitivos, publicados a 31/07/2026.</dd></div>'
    '<div><dt>O que é igual e o que é diferente</dt><dd>Igual: o verbo «Infira», uma personagem, o apoio em elementos textuais. Diferente: o texto da prova é dramático (um excerto de <i>Frei Luís de Sousa</i>), não narrativo; a prova pede dois traços e o treino pede um, com um limite. '
    'Em 2026, os itens de resposta restrita sobre um excerto narrativo dado na prova são os itens 1 e 2 da 1.ª fase (' + lig('e1', 'enunciado, p. 3') + '; ' + lig('c1', 'critérios, pp. 4-7') + '), com os verbos «Explicite» e «Compare». Nenhum item de 2026 manda inferir a partir de um conto.</dd></div>'
    '<div><dt>O texto</dt><dd>O conto tem direitos de autor. A página mostra só um recorte de duas frases, o que a lição M8-F16 já traz, e indica onde ler o conto inteiro: no manual.</dd></div>'
    '<div><dt>O que é de quem</dt><dd>' + LEGENDA + '</dd></div>'
    '</dl>'
    '<details class="dobra"><summary>Ver o item oficial: texto, item, cotação e critério</summary><div class="dentro">' + OFICIAL + '</div></details>'
)

NOSSO = json.dumps(TREINO, ensure_ascii=False) + CAB.replace(OFICIAL, '') + APOIO
for _s in [md(IT['enunciado'][0]), md(IT1['enunciado'][0]), md(IT1['enunciado'][1])]:
    assert _s in NOSSO
    NOSSO = NOSSO.replace(json.dumps(_s, ensure_ascii=False)[1:-1], '').replace(_s, '')
cita_ok(NOSSO)
# a Resposta A, que é a insuficiente, só põe entre aspas o que o recorte tem; o que inventa vem sem aspas
assert re.findall(r'«([^«»]+)»', RESP_A) == ['George detesta eufemismos']


def construir():
    lint('conto', NOSSO)
    return pagina_treino('conto', 'conto/', 'Conto', 'Treino 5: uma inferência, dois apoios, um limite | Português',
                         'Treino da preparação de exame de Português: fundamentar uma inferência sobre uma personagem de um conto, com um recorte curto, sete passos e uma resposta escrita por ti.', CAB, {'cit': APOIO}, TREINO)
