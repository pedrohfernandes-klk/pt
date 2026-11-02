#!/usr/bin/env python3
"""02/11/2026: o docente — «não há tarefas de grupo». Todas as tarefas passam a individuais, sem mudar o resto.

Constrói scripts/tarefas_individuais_20261102.json (trocas literais mínimas) a partir da lista abaixo, conferindo que cada
«antigo» aparece nas páginas atuais o número de vezes declarado. A camada aplica-se depois com scripts/aplicar_trocas.py.
Mudanças:
- tarefas de produção dos guias (M1, M2, M3, M4, M6, M7 extra, M9 extra): «em grupo» passa a «individual», os verbos passam
  do plural ao singular (tu), «Uma entrega por grupo» passa a «Entrega individual», saem os créditos de «quem fez o quê» e as
  linhas das rubricas que avaliavam a parte de cada membro do grupo;
- mapas do M1 e do M2 e portefólios: sem trabalhos de grupo nem «o responsável carrega o produto»;
- tarefas de unidade M4-U1, M4-U3 (discurso) e M7-U2: a apresentação continua individual, mas já não é feita «ao teu grupo»;
  os guias do M4 e do M7 dizem «apresentação individual» em vez de «apresentações em pequenos grupos».
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACHADO = 'Pedido do docente de 02/11/2026: não há tarefas de grupo; a tarefa fica igual, mas individual.'

# o «novo» leva o fim do bloco: sem ele, seria o princípio do «antigo» e a troca contar-se-ia como já aplicada
PORTEFOLIO_GERAL = ('O produto, ou a ligação, e uma linha: o que fiz, o que corrigi depois da devolução. Nos trabalhos de grupo, '
                    'o responsável carrega o produto; os outros põem a ligação e os créditos próprios.</div>',
                    'O produto, ou a ligação, e uma linha: o que fiz, o que corrigi depois da devolução.</div>')


def portefolio_tarefa(nome):
    return (f'{nome}: a ligação para o produto do grupo (só o responsável carrega o ficheiro) e os teus créditos, assinados: '
            'o que fizeste tu.', f'{nome}: o teu produto, ou a ligação para ele.')


G1 = 'Uma entrega por grupo.'
TROCAS = {
    'm1/guia-da-tarefa-m1/index.html': [
        ('<p class="quem">Em grupo de 2 ou 3.</p><p class="enc">Escrevam, à maneira de Guilhade e com palavras cobertas, uma cantiga de '
         'escárnio sobre um alvo de hoje que não seja ninguém da escola, e gravem a leitura.',
         '<p class="quem">Individual.</p><p class="enc">Escreve, à maneira de Guilhade e com palavras cobertas, uma cantiga de '
         'escárnio sobre um alvo de hoje que não seja ninguém da escola, e grava a leitura.'),
        ('M1_Tarefa2_Escarnio.m4a. ' + G1, 'M1_Tarefa2_Escarnio.m4a. Entrega individual.'),
        ('O alvo é um costume ou uma figura pública, nunca alguém da escola; os créditos dizem quem fez o quê.',
         'O alvo é um costume ou uma figura pública, nunca alguém da escola.'),
    ],
    'm1/mapa-do-modulo-m1/index.html': [
        ('<b>Cantiga de escárnio de 2026</b><span class="peso">25 %, em grupo de 2 ou 3</span>',
         '<b>Cantiga de escárnio de 2026</b><span class="peso">25 %, individual</span>'),
    ],
    'm1/portefolio-do-modulo-m1/index.html': [PORTEFOLIO_GERAL, portefolio_tarefa('Tarefa 2, «Cantiga de escárnio de 2026»')],
    'm2/guia-da-tarefa-m2/index.html': [
        ('<b>2. Recontagem contemporânea da farsa em vídeo</b><span>em grupo; duas aulas</span>', '<b>2. Recontagem contemporânea da farsa em vídeo</b><span>individual; duas aulas</span>'),
        ('<b>3. Dois anúncios de casamento</b><span>em grupo de 2 ou 3; duas aulas</span>', '<b>3. Dois anúncios de casamento</b><span>individual; duas aulas</span>'),
        ('"titulo":"Recontagem contemporânea da farsa em vídeo","quem":"em grupo","grupo":true', '"titulo":"Recontagem contemporânea da farsa em vídeo","quem":"individual","grupo":false'),
        ('"titulo":"Dois anúncios de casamento","quem":"em grupo de 2 ou 3","grupo":true', '"titulo":"Dois anúncios de casamento","quem":"individual","grupo":false'),
        ('Dividam a farsa em cinco momentos', 'Divide a farsa em cinco momentos'),
        ('a segunda escolha) e decidam o equivalente de hoje', 'a segunda escolha) e decide o equivalente de hoje'),
        ('"Escrevam o guião: cada personagem', '"Escreve o guião: cada personagem'),
        ('Filmem só quem autorizou; cumpram as regras de imagem da escola.', 'Filma só quem autorizou; cumpre as regras de imagem da escola.'),
        ('Nos créditos, cada mudança tem uma razão escrita; digam quem fez o quê.',
         'Nos créditos, cada mudança tem uma razão escrita; diz quem aparece no vídeo.'),
        ('o guião e os créditos. ' + G1, 'o guião e os créditos. Entrega individual.'),
        ('Recontem a Farsa de Inês Pereira nos dias de hoje', 'Reconta a Farsa de Inês Pereira nos dias de hoje'),
        ('M2_Tarefa2_FichaTecnica.pdf. ' + G1, 'M2_Tarefa2_FichaTecnica.pdf. Entrega individual.'),
        ('{"nome":"A cena assinada","niveis":["cada aluno assina uma cena com função clara; os apartes resolvidos",'
         '"cena assinada; aparte pouco claro","cena sem função na história","sem cena própria"]',
         '{"nome":"Cenas e apartes","niveis":["cada cena tem função clara na história; os apartes resolvidos",'
         '"cenas com função; um aparte pouco claro","uma cena sem função na história","cenas sem função na história"]'),
        ('Fizemos um vídeo em que a Inês escolhe um namorado. Mudámos tudo porque assim era mais engraçado.',
         'Fiz um vídeo em que a Inês escolhe um namorado. Mudei tudo porque assim era mais engraçado.'),
        ('Releiam as cenas de Pêro Marques e do Escudeiro e copiem três marcas', 'Relê as cenas de Pêro Marques e do Escudeiro e copia três marcas'),
        ('"Escrevam cada anúncio como Lianor Vaz o faria', '"Escreve cada anúncio como Lianor Vaz o faria'),
        ('Gravem a leitura dos dois anúncios num minuto', 'Grava a leitura dos dois anúncios num minuto'),
        ('com a voz da casamenteira.","Créditos: quem fez o quê."',
         'com a voz da casamenteira.","Confere os limites: 100 a 130 palavras em cada anúncio e um minuto de áudio."'),
        ('Os dois anúncios com as marcas citadas, o áudio e os créditos, num só envio por grupo.',
         'Os dois anúncios com as marcas citadas e o áudio, num só envio.'),
        ('Escrevam os dois anúncios que Lianor Vaz publicaria hoje', 'Escreve os dois anúncios que Lianor Vaz publicaria hoje'),
        ('M2_Tarefa3_Anuncios.m4a. ' + G1, 'M2_Tarefa3_Anuncios.m4a. Entrega individual.'),
        ('{"nome":"Limite, áudio e grupo","niveis":["100 a 130 palavras cada; áudio de um minuto, percetível, na voz da casamenteira; créditos",'
         '"limite ou áudio com um desvio","sem áudio, ou limite muito falhado","sem áudio nem créditos"]',
         '{"nome":"Limite e áudio","niveis":["100 a 130 palavras cada; áudio de um minuto, percetível, na voz da casamenteira",'
         '"limite ou áudio com um desvio","sem áudio, ou limite muito falhado","sem áudio nem limite cumprido"]'),
    ],
    'm2/mapa-do-modulo-m2/index.html': [
        ('<b>Recontagem contemporânea da farsa em vídeo</b><span class="peso">25 %, em grupo</span>',
         '<b>Recontagem contemporânea da farsa em vídeo</b><span class="peso">25 %, individual</span>'),
        ('<b>Dois anúncios de casamento</b><span class="peso">25 %, em grupo de 2 ou 3</span>',
         '<b>Dois anúncios de casamento</b><span class="peso">25 %, individual</span>'),
    ],
    'm2/portefolio-do-modulo-m2/index.html': [PORTEFOLIO_GERAL,
        portefolio_tarefa('Tarefa 2, «Recontagem contemporânea da farsa em vídeo»'),
        portefolio_tarefa('Tarefa 3, «Dois anúncios de casamento»')],
    'm3/guia-da-tarefa-m3/index.html': [
        ('<b>2. Objeto crítico das Descobertas</b><span>em grupo; duas aulas</span>', '<b>2. Objeto crítico das Descobertas</b><span>individual; duas aulas</span>'),
        ('<b>3. O Velho do Restelo em 2026</b><span>em grupo de 2 ou 3; duas aulas</span>', '<b>3. O Velho do Restelo em 2026</b><span>individual; duas aulas</span>'),
        ('"titulo":"Objeto crítico das Descobertas","quem":"em grupo","grupo":true', '"titulo":"Objeto crítico das Descobertas","quem":"individual","grupo":false'),
        ('"titulo":"O Velho do Restelo em 2026","quem":"em grupo de 2 ou 3","grupo":true', '"titulo":"O Velho do Restelo em 2026","quem":"individual","grupo":false'),
        ('"Escolham o objeto (astrolábio, padrão, mapa, caixa de especiarias) e decidam a mudança que o critica',
         '"Escolhe o objeto (astrolábio, padrão, mapa, caixa de especiarias) e decide a mudança que o critica'),
        ('Construam ou desenhem o objeto; fotografem-no sobre fundo liso.', 'Constrói ou desenha o objeto; fotografa-o sobre fundo liso.'),
        ('"Escrevam a legenda (o que é, o que mudou, porquê)', '"Escreve a legenda (o que é, o que mudou, porquê)'),
        ('"Registem duas fontes', '"Regista duas fontes'),
        ('o manual, com as duas fontes. ' + G1, 'o manual, com as duas fontes. Entrega individual.'),
        ('Recriem um objeto das Descobertas', 'Recria um objeto das Descobertas'),
        ('M3_Tarefa2_Legenda.pdf. ' + G1, 'M3_Tarefa2_Legenda.pdf. Entrega individual.'),
        ('Releiam o Velho do Restelo (canto IV) e resumam os três argumentos dele em três frases vossas',
         'Relê o Velho do Restelo (canto IV) e resume os três argumentos dele em três frases tuas'),
        ('"Escolham a «partida» de hoje', '"Escolhe a «partida» de hoje'),
        ('Escrevam o discurso de um minuto, transpondo os três argumentos; digam-no ao vivo, um de cada vez ou a várias vozes.',
         'Escreve o discurso de um minuto, transpondo os três argumentos; di-lo ao vivo.'),
        ('Escrevam, em três linhas, o que responderia quem parte. Créditos: quem fez o quê.',
         'Escreve, em três linhas, o que responderia quem parte.'),
        ('O texto com as estâncias, o áudio, a resposta de quem parte e os créditos, num só envio por grupo.',
         'O texto com as estâncias, o áudio e a resposta de quem parte, num só envio.'),
        ('Deem voz a um Velho do Restelo de hoje', 'Dá voz a um Velho do Restelo de hoje'),
        ('M3_Tarefa3_Restelo.m4a. ' + G1, 'M3_Tarefa3_Restelo.m4a. Entrega individual.'),
        ('{"nome":"Discurso ao vivo e grupo","niveis":["um minuto, dito ao vivo com voz e olhar; 150 a 200 palavras; créditos"',
         '{"nome":"Discurso ao vivo","niveis":["um minuto, dito ao vivo com voz e olhar; 150 a 200 palavras"'),
    ],
    'm3/portefolio-do-modulo-m3/index.html': [PORTEFOLIO_GERAL],
    'm4/guia-da-tarefa-m4/index.html': [
        ('aquecimento em cartões no início e apresentações em pequenos grupos, ao mesmo tempo',
         'aquecimento em cartões no início e apresentação individual'),
        ('<p class="quem">Em grupo de 2 ou 3.</p><p class="enc">Escolham um peixe das repreensões de Vieira e apresentem-no à turma',
         '<p class="quem">Individual.</p><p class="enc">Escolhe um peixe das repreensões de Vieira e apresenta-o à turma'),
        ('M4_Tarefa1_Peixe.mp4. ' + G1, 'M4_Tarefa1_Peixe.mp4. Entrega individual.'),
        ('Três a quatro minutos, todos falam, no máximo três imagens com crédito.', 'Três a quatro minutos, no máximo três imagens com crédito.'),
    ],
    'm5/portefolio-do-modulo-m5/index.html': [PORTEFOLIO_GERAL],
    'm6/guia-da-tarefa-m6/index.html': [
        ('<b>2. Cesário Verde nos dias de hoje</b><span>em grupo; duas aulas</span>', '<b>2. Cesário Verde nos dias de hoje</b><span>individual; duas aulas</span>'),
        ('"titulo":"Cesário Verde nos dias de hoje","quem":"em grupo","grupo":true', '"titulo":"Cesário Verde nos dias de hoje","quem":"individual","grupo":false'),
        ('Horas Mortas) escolham um lugar da Lisboa ribeirinha', 'Horas Mortas) escolhe um lugar da Lisboa ribeirinha'),
        ('"Fotografem ou filmem a pensar nos cinco sentidos', '"Fotografa ou filma a pensar nos cinco sentidos'),
        ('"Legendem cada imagem', '"Legenda cada imagem'),
        ('Apresentem à turma em três minutos e entreguem os créditos, com quem fez o quê.',
         'Apresenta à turma em três minutos e entrega os créditos.'),
        ('(ou a ligação) e os créditos. ' + G1, '(ou a ligação) e os créditos. Entrega individual.'),
        ('Refaçam o percurso de «O Sentimento dum Ocidental»', 'Refaz o percurso de «O Sentimento dum Ocidental»'),
        ('M6_Tarefa2_FichaTecnica.pdf. ' + G1, 'M6_Tarefa2_FichaTecnica.pdf. Entrega individual.'),
        ('"todos falam; versos ditos de cor ou bem lidos;', '"versos ditos de cor ou bem lidos;'),
    ],
    'm6/portefolio-do-modulo-m6/index.html': [PORTEFOLIO_GERAL],
    'm7/guia-da-tarefa-m7/index.html': [
        ('aquecimento em cartões no início e apresentações em pequenos grupos, ao mesmo tempo',
         'aquecimento em cartões no início e apresentação individual'),
        ('<b>Extra. Mensagem para 2026</b><span>em grupo de 2 ou 3; sem nota, por gosto ou para recuperação</span>',
         '<b>Extra. Mensagem para 2026</b><span>individual; sem nota, por gosto ou para recuperação</span>'),
        ('na unidade 2, a apresentação ao grupo.', 'na unidade 2, a apresentação individual.'),
        ('Apresenta-o ao teu grupo de 4 ou 5 colegas em dois minutos, com os grupos ao mesmo tempo, e lê uma frase dele.',
         'Apresenta-o em dois minutos e lê uma frase dele.'),
        ('"titulo":"Mensagem para 2026","quem":"em grupo de 2 ou 3","grupo":true', '"titulo":"Mensagem para 2026","quem":"individual","grupo":false'),
        ('"Escolham o poema («O Infante»', '"Escolhe o poema («O Infante»'),
        ('«Nevoeiro») e digam, em duas linhas, a estrutura dele', '«Nevoeiro») e diz, em duas linhas, a estrutura dele'),
        ('"Decidam o símbolo de hoje', '"Decide o símbolo de hoje'),
        ('Escrevam a versão com a mesma estrutura; citem dois versos do original como modelo.',
         'Escreve a versão com a mesma estrutura; cita dois versos do original como modelo.'),
        ('Gravem a leitura num minuto; registem os créditos (quem fez o quê).', 'Grava a leitura num minuto.'),
        ('O texto com os versos de modelo, o áudio e os créditos, num só envio por grupo.', 'O texto com os versos de modelo e o áudio, num só envio.'),
        ('Escolham um poema da Mensagem e façam a sua versão para hoje', 'Escolhe um poema da Mensagem e faz a tua versão para hoje'),
        ('dois versos dele citados como modelo, a gravação da leitura (um minuto) e os créditos (quem fez o quê).',
         'dois versos dele citados como modelo e a gravação da leitura (um minuto).'),
        ('M7_Extra_Mensagem.m4a. ' + G1, 'M7_Extra_Mensagem.m4a. Entrega individual.'),
        ('são símbolos, não pessoas; o texto é vosso.', 'são símbolos, não pessoas; o texto é teu.'),
        ('{"nome":"Forma, leitura e grupo","niveis":["12 a 16 versos ou 150 a 180 palavras; leitura de um minuto, percetível; créditos",'
         '"limite ou leitura com um desvio","sem leitura, ou limite muito falhado","sem áudio nem créditos"]',
         '{"nome":"Forma e leitura","niveis":["12 a 16 versos ou 150 a 180 palavras; leitura de um minuto, percetível",'
         '"limite ou leitura com um desvio","sem leitura, ou limite muito falhado","sem leitura nem texto completo"]'),
    ],
    'm8/portefolio-do-modulo-m8/index.html': [PORTEFOLIO_GERAL],
    'm9/guia-da-tarefa-m9/index.html': [
        ('<b>Extra. Os que carregaram a pedra</b><span>em grupo; duas aulas</span>', '<b>Extra. Os que carregaram a pedra</b><span>individual; duas aulas</span>'),
        ('"titulo":"Os que carregaram a pedra","quem":"em grupo","grupo":true', '"titulo":"Os que carregaram a pedra","quem":"individual","grupo":false'),
        ('"Releiam o capítulo da pedra e copiem os nomes', '"Relê o capítulo da pedra e copia os nomes'),
        ('"Decidam o produto e o que vai mostrar', '"Decide o produto e o que vai mostrar'),
        ('"Façam o produto; cada escolha de forma', '"Faz o produto; cada escolha de forma'),
        ('Apresentem à turma e entreguem os créditos, com quem fez o quê.', 'Apresenta à turma e entrega os créditos.'),
        ('a fundamentação e os créditos. ' + G1, 'a fundamentação e os créditos. Entrega individual.'),
        ('Deem nome aos anónimos do Memorial do Convento num produto do vosso curso', 'Dá nome aos anónimos do Memorial do Convento num produto do teu curso'),
        ('M9_Tarefa1_Fundamentacao.pdf. ' + G1, 'M9_Tarefa1_Fundamentacao.pdf. Entrega individual.'),
        ('Apresentação à turma; créditos; todos fizeram alguma coisa.', 'Apresentação à turma; créditos.'),
        ('"7 minutos; todos falam; uma objeção prevista e respondida"', '"7 minutos; uma objeção prevista e respondida"'),
        ('"lê-se do papel; fala um só"', '"lê-se do papel"'),
        ('{"nome":"Processo e parte de cada um","niveis":["três grupos testados, crítica de outro grupo registada, memória descritiva individual com 100 a 150 palavras"',
         '{"nome":"Processo e memória descritiva","niveis":["três grupos de anónimos testados, crítica de um colega registada, memória descritiva com 100 a 150 palavras"'),
    ],
    'm9/portefolio-do-modulo-m9/index.html': [PORTEFOLIO_GERAL],
    'tarefas/m4-u1/index.html': [
        ('apresentação individual de 3 a 4 minutos, ao teu grupo de quatro, com os grupos ao mesmo tempo.',
         'apresentação individual de 3 a 4 minutos.'),
    ],
    'tarefas/m4-u3-discurso/index.html': [
        ('apresentação individual de 2 minutos, ao teu grupo de quatro ou cinco, com os grupos ao mesmo tempo.',
         'apresentação individual de 2 minutos.'),
    ],
    'tarefas/m7-u2/index.html': [
        ('Apresenta a voz ao teu grupo em dois minutos, lê uma frase e responde a uma pergunta.',
         'Apresenta a voz em dois minutos, lê uma frase e responde a uma pergunta.'),
        ('As apresentações fazem-se em pequenos grupos de 4 ou 5, todos ao mesmo tempo, com o docente a circular. Cada um regista no '
         'seu papel, numa linha, a pergunta que lhe fizeram e o que respondeu; essa linha entra nas fotografias.',
         'A apresentação é individual. Regista no teu papel, numa linha, a pergunta que te fizeram e o que respondeste; essa linha '
         'entra nas fotografias.'),
    ],
    # índices: a linha da aula de tarefa e a descrição das lições da tarefa
    'm3/index.html': [
        ('<span class="f">Em grupo, recria um objeto das navegações com duas histórias',
         '<span class="f">Recria um objeto das navegações com duas histórias'),
    ],
    'm4/index.html': [
        ('guião em papel, apresentações em pequenos grupos ao mesmo tempo e fotografias no Teams.',
         'guião em papel, apresentação individual e fotografias no Teams.'),
        ('discurso em papel, apresentações em pequenos grupos ao mesmo tempo e fotografias no Teams.',
         'discurso em papel, apresentação individual e fotografias no Teams.'),
    ],
    'm6/index.html': [
        ('<span class="f">Em grupo, refaz o percurso do poema a partir do Cais do Sodré',
         '<span class="f">Refaz o percurso do poema a partir do Cais do Sodré'),
    ],
    'm7/index.html': [
        ('síntese integrada, apresentações em pequenos grupos ao mesmo tempo e fotografias no Teams.',
         'síntese integrada, apresentação individual e fotografias no Teams.'),
    ],
}

# Lições das tarefas e os seus painéis: o mesmo texto nos dois (o painel repete a pergunta e as opções da lição).
# As regras de segurança da saída à rua do M6 («sair em grupo e dentro do horário combinado») não são uma tarefa de grupo:
# ficam como estão.
LICOES = {
    'm2-f09': (
        [  # só na lição
            ('O provérbio e o par asno/cavalo que escolheram (meio minuto). 2) O mapa: em que se transformou cada momento da farsa, e uma '
             'escolha de que se orgulham (dois minutos). 3) Uma dificuldade e como a resolveram (um minuto). 4) A resposta do grupo à '
             'pergunta do módulo: <b>o que é que escolheram mudar na vossa recontagem, e porquê?</b> (um minuto). Sobra meio minuto para '
             'uma pergunta da turma. Decidam antes quem fala em cada passo.</p>',
             'O provérbio e o par asno/cavalo que escolheste (meio minuto). 2) O mapa: em que se transformou cada momento da farsa, e uma '
             'escolha de que te orgulhas (dois minutos). 3) Uma dificuldade e como a resolveste (um minuto). 4) A tua resposta à pergunta '
             'do módulo: <b>o que é que escolheste mudar na tua recontagem, e porquê?</b> (um minuto). Sobra meio minuto para uma pergunta '
             'da turma.</p>'),
            ('o efeito que o grupo se propôs conservar.', 'o efeito que te propuseste conservar.'),
            ('ordena a apresentação oral do grupo.', 'ordena a tua apresentação oral.'),
        ],
        [  # na lição e no painel
            ('"Uma dificuldade e como a resolveram"', '"Uma dificuldade e como a resolveste"'),
            ('O grupo escolheu uma aplicação de encontros', 'Escolheste uma aplicação de encontros'),
            ('Neste ensaio, o grupo quer comparar duas marcações', 'Neste ensaio, queres comparar duas marcações'),
            ('"Um tema do grupo, creditado"', '"Um tema próprio, creditado"'),
        ],
    ),
    'm3-f04': (
        [
            ('protótipo mostrado a outro grupo, etiqueta revista duas vezes.', 'protótipo mostrado a um colega, etiqueta revista duas vezes.'),
            ('"A divisão do trabalho não é a pergunta; a reflexão olha', '"A ajuda de um colega não é a pergunta; a reflexão olha'),
        ],
        [
            ('Recriem-no com olhar crítico', 'Recria-o com olhar crítico'),
            ('Como o grupo trabalha, por ordem:', 'Como trabalhas, por ordem:'),
            ('"Mostrar o protótipo a outro grupo"', '"Mostrar o protótipo a um colega"'),
            ('"Que parte não conseguimos confirmar"', '"Que parte não consegui confirmar"'),
            ('"Que parte ficou entregue a outro grupo"', '"Que parte ficou entregue a um colega"'),
            ('**O que não conseguimos confirmar**, e o que fizemos com isso.', '**O que não consegui confirmar**, e o que fiz com isso.'),
        ],
    ),
    'm6-f08': (
        [
            ('Extra sem nota, em grupo: quatro fotografias, uma por parte do poema,', 'Extra sem nota, individual: quatro fotografias, uma por parte do poema,'),
            ('Extra sem nota, em grupo, sete horas:', 'Extra sem nota, individual, sete horas:'),
            ('o corredor e o som são escolhas do grupo.', 'o corredor e o som são escolhas tuas.'),
            ('"p2":"O que faz o grupo antes de filmar alguém que se reconhece?"', '"p2":"O que fazes antes de filmar alguém que se reconhece?"'),
            ('Que nome tem o texto em que cada um explica o verso, a imagem e a ligação?', 'Que nome tem o texto em que explicas o verso, a imagem e a ligação?'),
            ('aqui explica-se uma escolha do próprio grupo: verso, imagem e ligação.', 'aqui explicas uma escolha tua: verso, imagem e ligação.'),
            ('(I), o grupo inventa um corredor apertado e som irregular. Como distingue a sua proposta da informação do verso?',
             '(I), inventas um corredor apertado e som irregular. Como distingues a tua proposta da informação do verso?'),
            ('Em vez das quatro fotografias ou da curta, o grupo pode usar o formato do seu curso.',
             'Em vez das quatro fotografias ou da curta, podes usar o formato do teu curso.'),
            ('Que colunas tem o guião que o grupo preenche parte a parte?', 'Que colunas tem o guião que preenches parte a parte?'),
            ('Toca na condição para usar música que não é do grupo.', 'Toca na condição para usar música que não é tua.'),
            ('Um grupo escolhe uma fotografia «bonita», mas não explica', 'Um aluno escolhe uma fotografia «bonita», mas não explica'),
        ],
        [
            ('O percurso pode demorar o tempo que o grupo quiser, desde que seja seguro.', 'O percurso pode demorar o tempo que quiseres, desde que seja seguro.'),
            ('que explica uma escolha do grupo?', 'que explica uma escolha tua?'),
            ('(I): o grupo quer criar incómodo sem mostrar gás.', '(I): queres criar incómodo sem mostrar gás.'),
            ('Em cada parte do guião registam o [1] escolhido, o que mostram hoje e [2].', 'Em cada parte do guião registas o [1] escolhido, o que mostras hoje e [2].'),
            ('o que mostramos hoje, **luz, hora e som**.', 'o que mostras hoje, **luz, hora e som**.'),
            ('os sons que não são do teu grupo.', 'os sons que não são teus.'),
            ('«Livres de direitos»: ou são do grupo, ou podem usar-se sem autorização.', '«Livres de direitos»: ou são teus, ou podem usar-se sem autorização.'),
            ('Exemplo inventado: o grupo escolhe uma fotografia', 'Exemplo inventado: escolhes uma fotografia'),
        ],
    ),
    'm9-f05': (
        [
            ('E vocês, com as ferramentas do curso?', 'E tu, com as ferramentas do curso?'),
            ('Em grupo, um produto do vosso curso faz o mesmo por anónimos,', 'Um produto do teu curso faz o mesmo por anónimos,'),
            ('Em grupo, um produto do vosso curso faz o mesmo por um grupo de anónimos,', 'Um produto do teu curso faz o mesmo por um grupo de anónimos,'),
            ('o vosso produto faz o mesmo.</p>', 'o teu produto faz o mesmo.</p>'),
            ('Como o _Memorial_, o vosso produto dá nome e voz', 'Como o _Memorial_, o teu produto dá nome e voz'),
            ('Além do produto do grupo, há um texto curto.', 'Além do produto, há um texto curto.'),
            ('"A memória descritiva não é do grupo: é individual, e cada um conta o que fez («O essencial»)."',
             '"A crítica de um colega ajuda a rever o produto; a memória descritiva é tua e conta o que fizeste («O essencial»)."'),
            ('A memória descritiva, que é tua e não do grupo, tem que extensão?', 'A memória descritiva que acompanha o produto tem que extensão?'),
            ('no produto do teu grupo, e o que o permitiria?', 'no teu produto, e o que o permitiria?'),
            ('os que o romance e o vosso produto querem lembrar?', 'os que o romance e o teu produto querem lembrar?'),
            ('"palavras":["O","produto","é do","grupo;","a","memória","descritiva","é tua."],"f":"«O produto é do grupo; a memória '
             'descritiva é tua»: duas frases paralelas, o ponto e vírgula ao meio, e «tua» a fechar."',
             '"palavras":["O","produto","dá nome","e voz;","a","memória","descritiva","explica-o."],"f":"«O produto dá nome e voz; a '
             'memória descritiva explica-o»: duas frases paralelas, o ponto e vírgula ao meio, e «explica-o» a fechar."'),
        ],
        [
            ('O produto do grupo faz por um grupo de anónimos', 'O teu produto faz por um grupo de anónimos'),
            ('O produto do grupo tem [1] citações', 'O teu produto tem [1] citações'),
            ('de apresentação; cronometra com o teu grupo.', 'de apresentação; cronometra o teu ensaio.'),
            ('"Um texto individual sobre o que cada um fez"', '"Um texto teu sobre o que fizeste no produto"'),
            ('"Um texto escrito pelo grupo sobre o produto"', '"A crítica que um colega fez ao teu produto"'),
            ('É tua, não do grupo: **100 a 150 palavras**', 'É tua: **100 a 150 palavras**'),
            ('**100 a 150 palavras**: a memória é individual; o produto é do grupo.', '**100 a 150 palavras**: a memória descritiva é curta e acompanha o produto.'),
            ('o narrador e o vosso produto lembram.', 'o narrador e o teu produto lembram.'),
            ('"O vosso produto"', '"O teu produto"'),
        ],
    ),
    'm9-f07': (
        [],
        [('"À memória descritiva do grupo"', '"À memória descritiva da tarefa"')],
    ),
}
PAINEL_ESPECIFICO = {
    'm9-f05': [
        ('"25":{"f":"«O produto é do grupo; a memória descritiva é tua»: duas frases paralelas, o ponto e vírgula ao meio, e «tua» a '
         'fechar.","palavras":["produto","memória","grupo;","é do","é tua.","a","O","descritiva"]}',
         '"25":{"f":"«O produto dá nome e voz; a memória descritiva explica-o»: duas frases paralelas, o ponto e vírgula ao meio, e '
         '«explica-o» a fechar.","palavras":["produto","memória","e voz;","dá nome","explica-o.","a","O","descritiva"]}'),
    ],
}
# Índices dos módulos: a «retoma» guarda cópias dos cartões das lições (com "_l"); levam as mesmas trocas, mais as cópias
# antigas que já não têm par na lição e as diferenças de formatação.
INDICE_ESPECIFICO = {
    'm2': [
        ('{"t":"vf","p":"Quem não aparece no vídeo não precisa de função registada no grupo.","v":false,"f":"Falso: todos os '
         'elementos têm função registada; é regra de produção e entra no diário de grupo.","_l":"m2-f09"}',
         '{"t":"vf","p":"Quem aparece no vídeo não precisa de ter autorizado a filmagem.","v":false,"f":"Falso: filma só quem '
         'autorizou; é regra de produção da escola.","_l":"m2-f09"}'),
    ],
    'm3': [
        ('"p":"Quantos objetos candidatos investiga o grupo antes de escolher um?","frase":"O grupo investiga [1] objetos candidatos',
         '"p":"Quantos objetos candidatos investigas antes de escolher um?","frase":"Investigas [1] objetos candidatos'),
        ('"o":["Ao docente","Aos autores de um manual","A outro grupo"],"c":2,"f":"A outro grupo: «Protótipo mostrado a outro grupo» '
         'é o terceiro passo do processo."',
         '"o":["Ao docente","Aos autores de um manual","A um colega"],"c":2,"f":"A um colega: «Protótipo mostrado a um colega» '
         'é o terceiro passo do processo."'),
    ],
    'm9': [
        ('<span class="f">Com o teu grupo, dá forma e voz a anónimos num produto do teu curso',
         '<span class="f">Dá forma e voz a anónimos num produto do teu curso'),
        ('"f":"É tua, não do grupo: 100 a 150 palavras', '"f":"É tua: 100 a 150 palavras'),
    ],
}
for _lic, (_so, _ambos) in LICOES.items():
    _m = _lic.split('-')[0]
    TROCAS[f'{_m}/licao-{_lic}/index.html'] = _so + _ambos
    TROCAS[f'{_m}/painel-{_lic}/index.html'] = _ambos + PAINEL_ESPECIFICO.get(_lic, [])
    _indice = (ROOT / f'{_m}/index.html').read_text('utf-8')
    TROCAS.setdefault(f'{_m}/index.html', []).extend(par for par in _so + _ambos if par[0] in _indice)
for _m, _pares in INDICE_ESPECIFICO.items():
    TROCAS.setdefault(f'{_m}/index.html', []).extend(_pares)

# Mapas (nomes dos critérios renomeados nos guias), nota do guião da aula 8 do M4, exemplo do exercício longo do M6 e
# desafio do Atlas.
TROCAS['m1/mapa-do-modulo-m1/index.html'].append(('Forma e leitura; Alvo, língua e grupo</span>', 'Forma e leitura; Alvo e língua</span>'))
TROCAS['m2/mapa-do-modulo-m2/index.html'] += [
    ('Fidelidade e escolha; A cena assinada; Produção', 'Fidelidade e escolha; Cenas e apartes; Produção'),
    ('Registo e contraste; Limite, áudio e grupo</span>', 'Registo e contraste; Limite e áudio</span>'),
]
TROCAS['m4/aulas/aula-08/index.html'] = [
    ('guarda a versão anterior da encomenda, em grupo e com PDF: não se projeta', 'guarda a versão anterior da encomenda, com PDF: não se projeta'),
]
TROCAS['m6/m6-cesario-noite-inteira/index.html'] = [
    ('<p>Imagina um grupo que refaz o percurso do poema com uma câmara', '<p>Imagina alguém que refaz o percurso do poema com uma câmara'),
]
TROCAS['assets/atlas-editorial.js'] = [
    ('Em grupo, inventem uma saudação breve com palavras ou gestos e expliquem uma escolha coletiva.',
     'Inventa uma saudação breve com palavras ou gestos e explica uma das tuas escolhas.'),
]


def main():
    trocas = []
    falhas = []
    for ficheiro, pares in TROCAS.items():
        texto = (ROOT / ficheiro).read_text('utf-8')
        for n, (antigo, novo) in enumerate(pares, 1):
            k = texto.count(antigo)
            if k == 0:
                falhas.append(f'{ficheiro}: troca {n} não encontrada: {antigo[:90]}')
                continue
            if texto.replace(antigo, novo).count(novo) != k:
                falhas.append(f'{ficheiro}: troca {n}: o novo não fica único: {novo[:90]}')
                continue
            trocas.append({'ficheiro': ficheiro, 'local': f'Tarefas individuais, troca {n}', 'antigo': antigo, 'novo': novo,
                           'ocorrencias': k, 'achado': ACHADO})
            texto = texto.replace(antigo, novo)
    if falhas:
        raise SystemExit('\n'.join(falhas))
    destino = ROOT / 'scripts/tarefas_individuais_20261102.json'
    destino.write_text(json.dumps(trocas, ensure_ascii=False, indent=2) + '\n', 'utf-8', newline='\n')
    print(len(trocas), 'trocas em', len({t['ficheiro'] for t in trocas}), 'ficheiros')


if __name__ == '__main__':
    main()
