"""11/11/2026: a entrada dos treinos (exame/treinos/).
12/11/2026: quatro cartões, com o treino da sessão 17; a contagem do título vem de base.TREINOS."""
from .base import *

CARTOES = [
    ('interpretacao', 'Treino 1. Interpretação literária', 'Da imagem à proposta de vida',
     'Ricardo Reis, «As rosas amo dos jardins de Adónis». Explicas a relação entre a imagem das rosas e a proposta de vida, com apoio no texto.',
     'Trabalha a mesma ode que o aquecimento da ' + sessao('s14', 'Reis: a disciplina do instante', '../') + '. Liga-se ao item 5 do Grupo I da 1.ª fase de 2026 (13 pontos).', 6),
    ('gramatica', 'Treino 2. Gramática', 'Que função tem, e como o sabes',
     'Identificas e justificas uma função sintática no contexto, com contraste entre casos e os limites de cada teste.',
     'Liga-se à ' + sessao('s21', 'Gramática: funções e relações entre orações', '../') + ' e aos itens 7 do Grupo II das duas fases de 2026 (13 pontos cada).', 7),
    ('escrita', 'Treino 3. Escrita com correção', 'Um texto de opinião, do pedido à segunda versão',
     'Planeias, escreves e revês um texto de 200 a 350 palavras com a grelha oficial, aspeto a aspeto.',
     'Liga-se à ' + sessao('s24', 'Opinião: uma posição que resiste à revisão', '../') + ' e ao Grupo III da 2.ª fase de 2026 (44 pontos).', 6),
    ('poesia-contemporanea', 'Treino 4. Poesia contemporânea', 'Dois poemas, um eixo',
     'Jorge de Sena, «Uma pequenina luz», e Eugénio de Andrade, «As Palavras». Comparas o modo como cada poema apresenta uma coisa frágil, com uma transcrição de cada um.',
     'Liga-se à ' + sessao('s17', 'Poesia contemporânea: três modos de dizer', '../') + ' e ao item 2 do Grupo I da 2.ª fase de 2026 (13 pontos). Os poemas têm direitos de autor: a página traz duas citações curtas e manda ler os poemas inteiros no manual.', 6),
]
assert [c[0] for c in CARTOES] == [p for p, _ in TREINOS]
CAPITAL = POR_EXTENSO.capitalize()
cart = ''
for pid, num, tit, o, liga, n in CARTOES:
    cart += ('<article class="cartao-p"><p class="num">%s</p><h2>%s</h2><p>%s</p><p class="pag">%s %d passos.</p>'
             '<a class="btn forte" href="%s/">Abrir o treino<span class="so-leitor">: %s</span></a><p class="est" data-estado="%s" data-n="%d"></p></article>') % (num, tit, o, liga, n, pid, tit, pid, n)

CORPO = (
    '<main id="conteudo" tabindex="-1"><p class="sobre">Preparação de exame</p>'
    '<h1>' + CAPITAL + ' treinos de exame</h1>'
    '<p class="lede">' + CAPITAL + ' treinos curtos para a preparação da prova 639. Cada um parte de um item oficial de 2026, mantém o texto ao lado da pergunta, dá duas pistas antes da explicação e acaba numa resposta escrita por ti, que revês com os critérios.</p>'
    '<div class="cartoes">' + cart + '</div>'
    '<h2>Como funciona cada treino</h2>'
    '<ul class="top">'
    '<li><b>O pedido primeiro.</b> Começas por ver o que o item manda fazer, quantas coisas e com que condições.</li>'
    '<li><b>O texto fica contigo.</b> O poema, as linhas da prova ou o enunciado estão sempre ao lado da pergunta (em ecrãs estreitos, por cima, e podem recolher-se). Quando o texto tem direitos de autor, ficam ao lado as citações curtas e a indicação de onde o ler inteiro.</li>'
    '<li><b>Três tentativas, duas pistas.</b> Se erras, recebes uma pista feita para o erro que cometeste e tentas outra vez. Se voltas a errar, recebes uma segunda pista, que te leva ao sítio do texto onde está a resposta, sem a dizer. A explicação só aparece à terceira falha. Verificar duas vezes seguidas a mesma seleção errada não gasta tentativa.</li>'
    '<li><b>Uma resposta tua.</b> Escreves sem pistas à vista, na caixa ou no papel. A caixa não é enviada para lado nenhum e nada classifica o teu texto.</li>'
    '<li><b>Duas versões.</b> A primeira versão fica ao lado da versão revista. Podes alterá-la em qualquer altura; se a alterares depois de veres os critérios, a página diz isso junto dela, para a comparação continuar honesta.</li>'
    '<li><b>Registo.</b> No fim, vês o que fizeste por ti, à primeira, o que fizeste com pista (à segunda ou à terceira) e o que precisou de explicação.</li></ul>'
    '<h2>O que é de quem</h2>' + LEGENDA +
    '<div class="caixa nossa espaco"><p><b>Sobre 2027.</b> Os itens e os critérios são os de 2026: enunciados e critérios definitivos das duas fases, em eduqa.pt. Onde uma regra pode mudar, a página diz «a confirmar na Informação-Prova de 2027», que ainda não temos.</p></div>'
    '<p class="pag">Os 27 aquecimentos das sessões continuam na <a href="../">entrada da preparação de exame</a>, cada um na sua sessão.</p>'
    '</main>\n'
)


def construir():
    lint('indice', CORPO)
    out = (cabeca('../../', CAPITAL + ' treinos de exame | Português',
                  CAPITAL + ' treinos da preparação de exame de Português: interpretação literária, gramática, escrita e comparação de poemas, cada um a partir de um item oficial de 2026.', True) +
           topo('../', './', '', None) + CORPO +
           rodape('../', './', '../../', '<span>As respostas ficam só neste dispositivo. Nada é enviado.</span>') + '</body></html>\n')
    return 'exame/treinos/index.html', out
