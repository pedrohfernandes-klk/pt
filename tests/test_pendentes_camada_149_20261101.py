"""01/11/2026: correções do #149 reservadas para depois do #144 e do #145.

Não aplica trocas, não regista camadas e não dispensa nenhum contrato publicado.
Retirar cada entrada quando for integrada numa camada própria. A lista só diminui.
"""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

# 01/11/2026: para depois do #144 e do #145.
PENDENTES_CAMADA_149_20261101 = [{'ficheiro': 'm1/licao-m1-f20/index.html',
  'local': 'M1-F20 C14',
  'antigo': '{"t":"escolha","rot":"O nome do homem de barrete","tipo":"transferir","g":"c-interpretacao-opiniao","mais":true,"ver":"<img '
            'src=\\"../../img/fontes/fernao-lopes-painel.jpg\\" alt=\\"Rosto de um homem velho, de rugas fundas, com um barrete alto '
            'escuro e roupa escura, num pormenor dos Painéis de São Vicente.\\" loading=\\"lazy\\" style=\\"object-position:50% '
            '38%\\">","p":"Só com esta pintura, que é a frase «Este homem é Fernão Lopes»?","p2":"Para quem só tem este painel, «É Fernão '
            'Lopes» é que tipo de frase?","o":["Sem apoio na pintura, e nem por isso uma opinião","Informação explícita: a pintura '
            'mostra-o","Uma opinião: um juízo de quem olha","Uma interpretação: o rosto prova o nome"],"c":0,"fe":["","A pintura mostra um '
            'rosto, um barrete e uma roupa escura, e nenhum nome: nada nela diz quem é.","Não há juízo de valor: dizer quem é não é dizer '
            'se é bom ou mau. O que falta é apoio.","Uma interpretação defende-se com o que se vê, e um rosto não prova um nome: era '
            'precisa outra fonte."],"f":"A pintura não traz nome: «é Fernão Lopes» é o que a tradição afirma. Sem apoio na pintura, não '
            'passa por isso a opinião; para o provar, era precisa outra fonte."}',
  'novo': '{"t":"escolha","rot":"O nome do homem de barrete","tipo":"transferir","g":"c-interpretacao-opiniao","ver":"<img '
          'src=\\"../../img/fontes/fernao-lopes-painel.jpg\\" alt=\\"Rosto de um homem velho, de rugas fundas, com um barrete alto escuro '
          'e roupa escura, num pormenor dos Painéis de São Vicente.\\" loading=\\"lazy\\" style=\\"object-position:50% 38%\\">","p":"Só '
          'com esta pintura, que é a frase «Este homem é Fernão Lopes»?","p2":"Para quem só tem este painel, «É Fernão Lopes» é que tipo '
          'de frase?","o":["Identificação sem prova: o rosto não revela o nome","Informação explícita: a pintura mostra o nome '
          'escrito","Juízo prudente: o rosto talvez permita dar-lhe nome","Inferência apoiada: o rosto permite dar-lhe um '
          'nome"],"c":0,"fe":[null,"Confundes uma figura visível com a sua identificação. Procura no painel uma inscrição que dê o nome: '
          'não há nenhuma.","Confundes uma afirmação com uma hipótese. Relê a frase: «Este homem é Fernão Lopes» não traz «talvez»; afirma '
          'um nome que a pintura, sozinha, não sustenta.","Confundes semelhança com prova de identidade. Volta ao rosto: que fonte '
          'permitiria ligar-lhe um nome?"],"f":"A pintura não traz nome: «é Fernão Lopes» é o que a tradição afirma. Sem apoio na pintura, '
          'não passa por isso a opinião; para o provar, era precisa outra fonte.","mais":true}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm4/licao-m4-f01/index.html',
  'local': 'M4-F01 C11',
  'antigo': '{"t":"escolha","rot":"Os peixes em ordem","g":1,"l":"1-1","mais":true,"cita":"postos todos por sua ordem com as cabeças de '
            'fora da água, António pregava, e eles ouviam.","p":"Porque conta Vieira que os peixes ouviam assim?","p2":"Que efeito tem a '
            'imagem dos peixes em ordem, de cabeça fora de água?","o":["Mostra-os como um auditório atento, o contrário dos '
            'homens","Descreve as espécies do mar de Arimino","Mostra que os peixes pequenos ficavam à frente","Prova que os peixes '
            'entendiam a doutrina melhor que os homens"],"c":0,"fe":["","Aqui, Vieira não nomeia espécies: diz só «os grandes, os maiores, '
            'os pequenos». O que importa é que todos ouvem.","O texto diz «por sua ordem», sem dizer quem fica à frente: o que conta é '
            'estarem todos a ouvir.","O texto diz que «ouviam», não que entendiam. O que se opõe aos homens é ouvir: eles não '
            'querem."],"f":"«António pregava, e eles ouviam»: em ordem e de cabeça fora de água, os peixes são o auditório que os homens '
            'recusaram ser. A frase opõe-se em silêncio aos homens, que não ouviam."}',
  'novo': '{"t":"escolha","rot":"Os peixes em ordem","g":1,"l":"1-1","cita":"postos todos por sua ordem com as cabeças de fora da água, '
          'António pregava, e eles ouviam.","p":"Que contraste responde melhor à pergunta de abertura: por que razão fala Vieira aos '
          'peixes?","fe":["A cena não demonstra uma capacidade superior dos peixes nem dispensa os homens como destinatários da crítica. A '
          'alegoria faz o que se diz de uns chegar aos outros. Relê «António pregava, e eles ouviam»: o verbo é ouvir, não entender.","A '
          'ordem dos peixes participa na imagem do auditório atento. Não é uma descrição naturalista da vida marinha: tem uma função no '
          'argumento. Relê «com as cabeças de fora da água»: que atitude assume o auditório perante quem prega?",null],"f":"A atenção dos '
          'peixes faz sobressair a recusa dos homens. Assim, falar aos peixes continua a ser uma forma de interpelar os homens. No texto, '
          'procura a ação que mostra essa atenção.","o":["Os peixes entendem; essa capacidade torna desnecessário pregar aos homens.","Os '
          'peixes reúnem-se; essa ordem explica como vivem longe dos homens.","Os peixes escutam atentos; essa atenção põe em causa a '
          'recusa dos homens."],"c":2}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm4/licao-m4-f01/index.html',
  'local': 'M4-F01 C18',
  'antigo': '{"t":"ler","rot":"Para levar","escuro":true,"html":"<p class=\\"levar\\"><span class=\\"ch\\" style=\\"--i:0\\">A</span><span '
            'class=\\"ch\\" style=\\"--i:1\\">n</span><span class=\\"ch\\" style=\\"--i:2\\">t</span><span class=\\"ch\\" '
            'style=\\"--i:3\\">ó</span><span class=\\"ch\\" style=\\"--i:4\\">n</span><span class=\\"ch\\" style=\\"--i:5\\">i</span><span '
            'class=\\"ch\\" style=\\"--i:6\\">o</span><span class=\\"ch\\" style=\\"--i:7\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:8\\">m</span><span class=\\"ch\\" style=\\"--i:9\\">u</span><span class=\\"ch\\" '
            'style=\\"--i:10\\">d</span><span class=\\"ch\\" style=\\"--i:11\\">o</span><span class=\\"ch\\" '
            'style=\\"--i:12\\">u</span><span class=\\"ch\\" style=\\"--i:13\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:14\\">o</span><span class=\\"ch\\" style=\\"--i:15\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:16\\">a</span><span class=\\"ch\\" style=\\"--i:17\\">u</span><span class=\\"ch\\" '
            'style=\\"--i:18\\">d</span><span class=\\"ch\\" style=\\"--i:19\\">i</span><span class=\\"ch\\" '
            'style=\\"--i:20\\">t</span><span class=\\"ch\\" style=\\"--i:21\\">ó</span><span class=\\"ch\\" '
            'style=\\"--i:22\\">r</span><span class=\\"ch\\" style=\\"--i:23\\">i</span><span class=\\"ch\\" '
            'style=\\"--i:24\\">o</span><span class=\\"ch\\" style=\\"--i:25\\">,</span><span class=\\"ch\\" style=\\"--i:26\\"> '
            '</span><span class=\\"ch\\" style=\\"--i:27\\">n</span><span class=\\"ch\\" style=\\"--i:28\\">ã</span><span class=\\"ch\\" '
            'style=\\"--i:29\\">o</span><span class=\\"ch\\" style=\\"--i:30\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:31\\">a</span><span class=\\"ch\\" style=\\"--i:32\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:33\\">d</span><span class=\\"ch\\" style=\\"--i:34\\">o</span><span class=\\"ch\\" '
            'style=\\"--i:35\\">u</span><span class=\\"ch\\" style=\\"--i:36\\">t</span><span class=\\"ch\\" '
            'style=\\"--i:37\\">r</span><span class=\\"ch\\" style=\\"--i:38\\">i</span><span class=\\"ch\\" '
            'style=\\"--i:39\\">n</span><span class=\\"ch\\" style=\\"--i:40\\">a</span><span class=\\"ch\\" '
            'style=\\"--i:41\\">.</span></p><p>Santo António deixou as praças pelas praias, sem mudar o que pregava. Vieira, em São Luís, '
            'fala aos peixes para que os homens ouçam: é a alegoria, que diz uma coisa para significar outra, do princípio ao fim do '
            'sermão.</p><details class=\\"mais\\"><summary>As frases da aula</summary><div><ol><li>Em São Luís, em 1654, os colonos '
            'escravizavam os indígenas e não queriam ouvir Vieira.</li><li>Vieira conta o que fez Santo António em Arimino para mostrar o '
            'que ele próprio vai fazer.</li><li>Calar-se, retirar-se ou dissimular seria prudência ou covardia; o zelo não se '
            'rende.</li><li>Para Vieira, mudar de auditório não é desistir: a doutrina fica, muda quem a ouve.</li><li>Alegoria: o que se '
            'diz aos peixes vale para os homens, do princípio ao fim do sermão.</li></ol></div></details>"}',
  'novo': '{"t":"ler","rot":"Para levar","escuro":true,"html":"<p class=\\"levar\\"><span class=\\"ch\\" style=\\"--i:0\\">A</span><span '
          'class=\\"ch\\" style=\\"--i:1\\">n</span><span class=\\"ch\\" style=\\"--i:2\\">t</span><span class=\\"ch\\" '
          'style=\\"--i:3\\">ó</span><span class=\\"ch\\" style=\\"--i:4\\">n</span><span class=\\"ch\\" style=\\"--i:5\\">i</span><span '
          'class=\\"ch\\" style=\\"--i:6\\">o</span><span class=\\"ch\\" style=\\"--i:7\\"> </span><span class=\\"ch\\" '
          'style=\\"--i:8\\">m</span><span class=\\"ch\\" style=\\"--i:9\\">u</span><span class=\\"ch\\" style=\\"--i:10\\">d</span><span '
          'class=\\"ch\\" style=\\"--i:11\\">o</span><span class=\\"ch\\" style=\\"--i:12\\">u</span><span class=\\"ch\\" '
          'style=\\"--i:13\\"> </span><span class=\\"ch\\" style=\\"--i:14\\">o</span><span class=\\"ch\\" style=\\"--i:15\\"> '
          '</span><span class=\\"ch\\" style=\\"--i:16\\">a</span><span class=\\"ch\\" style=\\"--i:17\\">u</span><span class=\\"ch\\" '
          'style=\\"--i:18\\">d</span><span class=\\"ch\\" style=\\"--i:19\\">i</span><span class=\\"ch\\" '
          'style=\\"--i:20\\">t</span><span class=\\"ch\\" style=\\"--i:21\\">ó</span><span class=\\"ch\\" '
          'style=\\"--i:22\\">r</span><span class=\\"ch\\" style=\\"--i:23\\">i</span><span class=\\"ch\\" '
          'style=\\"--i:24\\">o</span><span class=\\"ch\\" style=\\"--i:25\\">,</span><span class=\\"ch\\" style=\\"--i:26\\"> '
          '</span><span class=\\"ch\\" style=\\"--i:27\\">n</span><span class=\\"ch\\" style=\\"--i:28\\">ã</span><span class=\\"ch\\" '
          'style=\\"--i:29\\">o</span><span class=\\"ch\\" style=\\"--i:30\\"> </span><span class=\\"ch\\" '
          'style=\\"--i:31\\">a</span><span class=\\"ch\\" style=\\"--i:32\\"> </span><span class=\\"ch\\" '
          'style=\\"--i:33\\">d</span><span class=\\"ch\\" style=\\"--i:34\\">o</span><span class=\\"ch\\" '
          'style=\\"--i:35\\">u</span><span class=\\"ch\\" style=\\"--i:36\\">t</span><span class=\\"ch\\" '
          'style=\\"--i:37\\">r</span><span class=\\"ch\\" style=\\"--i:38\\">i</span><span class=\\"ch\\" '
          'style=\\"--i:39\\">n</span><span class=\\"ch\\" style=\\"--i:40\\">a</span><span class=\\"ch\\" '
          'style=\\"--i:41\\">.</span></p><p>Santo António deixou as praças pelas praias, sem mudar o que pregava. Vieira, em São Luís, '
          'fala aos peixes para que os homens ouçam: é a alegoria, que diz uma coisa para significar outra, do princípio ao fim do '
          'sermão.</p><details class=\\"mais\\"><summary>As frases da aula</summary><div><ol><li>Em São Luís, em 1654, os colonos '
          'escravizavam os indígenas e não queriam ouvir Vieira.</li><li>Vieira conta o que fez Santo António em Arimino para mostrar o '
          'que ele próprio vai fazer.</li><li>Calar-se, retirar-se ou dissimular seria prudência ou covardia; o zelo não se '
          'rende.</li><li>Para Vieira, mudar de auditório não é desistir: a doutrina fica, muda quem a ouve.</li><li>Alegoria: o que se '
          'diz aos peixes vale para os homens, do princípio ao fim do sermão.</li></ol></div></details><p>Volta à pergunta do início. '
          'Explica oralmente como a atenção dos peixes responde à recusa dos homens e aponta uma expressão que sustente a tua '
          'leitura.</p>"}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm4/recursos/tpc-entrada.js',
  'local': 'M4-F28 C03',
  'antigo': '{"t":"escolha","p":"Laura e Tiago têm de trabalhar juntos; Madalena teme um passado que julgava encerrado. Que pergunta ajuda '
            'a comparar os conflitos?","o":["As duas obras apresentam exatamente a mesma história?","Como condiciona uma relação anterior '
            'o que as personagens podem fazer agora?","Que personagem de TPC corresponde obrigatoriamente a Madalena?"],"c":1,"f":"A '
            'comparação procura uma **relação entre conflitos**, sem apagar diferenças. No TPC, os ex-namorados partilham um trabalho; em '
            'Garrett, a dúvida sobre um primeiro marido ameaça a segurança da família.","g":"m4-tpc","fe":["A sinopse apresenta uma '
            'recriação a partir de Garrett, não uma transcrição integral nem a mesma história.",null,"Aproximar conflitos não obriga a '
            'emparelhar personagens: as situações e as suas consequências são diferentes."]}',
  'novo': '{"t":"escolha","p":"Laura e Tiago têm de trabalhar juntos; Madalena teme um passado que julgava encerrado. Que pergunta ajuda a '
          'comparar os conflitos?","o":["Que sequência de acontecimentos se repete nas duas histórias?","Que relação anterior limita o que '
          'podem fazer no presente?","Que personagem de cada obra ocupa o mesmo lugar na família?"],"c":1,"f":"A comparação procura uma '
          '**relação entre conflitos**, sem apagar diferenças. No TPC, os ex-namorados partilham um trabalho; em Garrett, a dúvida sobre '
          'um primeiro marido ameaça a segurança da família.","g":"m4-tpc","fe":["Confundes relação temática com repetição do enredo. Relê '
          'as duas situações: um namoro terminado e um marido desaparecido.",null,"Confundes comparação de conflitos com correspondência '
          'entre personagens. Relê quem integra cada grupo antes de procurar pares."]}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm4/recursos/tpc-entrada.js',
  'local': 'M4-F28 C05',
  'antigo': '{"t":"escolha","p":"Madalena fala de «imensa felicidade», mas diz que os «contínuos terrores» não a deixam gozá-la. Que '
            'leitura explica melhor a tensão?","o":["Madalena já não sente amor pelo marido atual","O amor existe, mas o medo impede-a de '
            'o viver em segurança","A felicidade só existiu antes de conhecer Manuel"],"c":1,"f":"O contraste está **dentro da mesma '
            'experiência**: há amor e felicidade, mas o medo impede que sejam vividos plenamente. A hipótese liga a interpretação a '
            'palavras concretas da fala.","g":"m4-tpc","fe":["O texto fala em «imensa felicidade» dada pelo amor; o problema é não '
            'conseguir gozá-la sem medo.",null,"A fala liga a felicidade ao amor presente. Não a localiza apenas num tempo anterior a '
            'Manuel."]}',
  'novo': '{"t":"escolha","p":"Madalena fala de «imensa felicidade», mas diz que os «contínuos terrores» não a deixam gozá-la. Que leitura '
          'explica melhor a tensão?","o":["O medo mostra que o amor pelo marido deixou de existir","O amor existe, mas o medo impede-a de '
          'o viver em paz","A felicidade pertence ao tempo anterior ao amor atual"],"c":1,"f":"O contraste está **dentro da mesma '
          'experiência**: há amor e felicidade, mas o medo impede que sejam vividos plenamente. A hipótese liga a interpretação a palavras '
          'concretas da fala.","g":"m4-tpc","fe":["Confundes impedimento de gozar com ausência de amor. Relê «imensa felicidade» e quem a '
          'dava.",null,"Deslocas a felicidade para outro tempo. Relê «que me dava o seu amor»: a tensão está dentro dessa relação."]}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm6/licao-m6-f01/index.html',
  'local': 'M6-F01 C16',
  'antigo': '{"t":"escolha","p":"O que encontra o cavaleiro quando as portas de ouro se abrem?","p2":"Que há dentro do palácio, depois do '
            'fragor das portas?","o":["Silêncio e escuridão, e nada mais","Uma sala de ouro, sem ninguém à espera","A Ventura, que o '
            'recebe em silêncio","A luz fulgurante que tinha visto de fora"],"c":0,"f":"Lá dentro há só «Silencio e escuridão» e, diz o '
            'último verso, «nada mais!» (v. 14): a promessa de luz dá em **vazio**.","cita":"Silencio e escuridão — e nada '
            'mais!","l":"0-16","g":2,"fe":[null,"O ouro é das portas, vistas de fora («portas d\'ouro»); dentro não há sala descrita, só '
            '«Silencio e escuridão» (v. 14).","A Ventura não aparece: dentro, o cavaleiro encontra «só» (apenas) «Silencio e escuridão» '
            '(v. 13 e 14); ninguém o recebe.","A luz era a do palácio visto de fora, «fulgurante» (v. 7); ao abrir as portas encontra o '
            'contrário, «escuridão» (v. 14)."]}',
  'novo': '{"t":"escolha","p":"O cavaleiro vê abrirem-se as portas de ouro, mas encontra o vazio. Que pergunta ajuda a explicar esta '
          'mudança?","f":"A promessa de riqueza não coincide com o que o cavaleiro encontra. Procura uma palavra do exterior e outra do '
          'interior: a relação entre elas sustenta a interpretação.","cita":"Silencio e escuridão — e nada '
          'mais!","l":"0-16","g":2,"fe":[null,"Confundes a duração da viagem com o contraste do desfecho. Relê o que o poema diz das '
          'portas e do que há dentro.","O poema não identifica quem construiu o palácio. Essa informação não pode servir de prova. Compara '
          'o exterior e o interior antes de acrescentares uma causa."],"o":["Que contraste liga a promessa exterior ao que encontra '
          'dentro?","Que distância percorreu o cavaleiro antes de chegar à porta?","Que pessoa mandou construir o palácio para receber o '
          'cavaleiro?"],"c":0}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm7/licao-m7-f34/index.html',
  'local': 'M7-F34 C09',
  'antigo': '{"t":"escolha","p":"No cinema, a «dupla exposição» mostra duas imagens no mesmo sítio, uma através da outra. Que verso faz '
            'isso com palavras?","p2":"Que verso põe duas imagens no mesmo lugar, como dois fotogramas sobrepostos?","o":["«os navios '
            'passam por dentro dos troncos das árvores»","«O porto que sonho é sombrio e pálido»","«Liberto em duplo, abandonei-me da '
            'paisagem abaixo...»","«E esta paisagem é cheia de sol deste lado...»"],"c":0,"f":"**Navios e troncos ocupam o mesmo lugar** '
            'da imagem. Os outros versos falam de um só plano, ou de nenhuma imagem.","cita":"E os navios passam por dentro dos troncos '
            'das árvores","l":"0-13","g":2,"fe":[null,"Este verso fica só no sonho: o porto «sombrio e pálido» não se mistura aqui com a '
            'paisagem.","«Em duplo» é o poeta desdobrado, não uma imagem; aqui não há duas coisas a ocupar o mesmo lugar.","Este verso '
            'fica só na paisagem, ao sol; nenhuma coisa sonhada entra nele."]}',
  'novo': '{"t":"escolha","p":"No verso «os navios passam por dentro dos troncos das árvores», que leitura justifica a aproximação à dupla '
          'exposição?","f":"Os navios pertencem a um plano e os troncos a outro. A expressão «por dentro» põe-nos no mesmo espaço '
          'imaginado, em vez de apenas alternar duas cenas.","cita":"E os navios passam por dentro dos troncos das '
          'árvores","l":"0-13","g":"dupla-exposicao","fe":["Alternar cenas seria apresentar uma e depois outra. Aqui, uma atravessa a '
          'outra: é essa relação espacial que deves explicar. Relê «por dentro dos troncos»: os espaços sucedem-se ou cruzam-se?","O verso '
          'não descreve uma rota navegável entre árvores. O cruzamento entre planos cria a imagem; tratá-lo como itinerário literal perde '
          'esse efeito. Relê «navios» e «troncos»: a expressão põe elementos dos dois planos no mesmo lugar.",null],"o":["Dois espaços '
          'aparecem um depois do outro; a passagem separa os momentos.","Dois espaços pertencem à mesma viagem; a passagem descreve uma '
          'rota real e possível.","Dois espaços ocupam a mesma imagem; atravessar os troncos aproxima os planos."],"c":2}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm7/licao-m7-f34/index.html',
  'local': 'M7-F34 C31',
  'antigo': '{"t":"escolha","g":"escuta-vi-transferencia","p":"Compara I e VI: «os navios […] são estas árvores» e «Todo o teatro é o meu '
            'quintal». O que aproxima estes versos?","p2":"I: «os navios […] são estas árvores»; VI: «Todo o teatro é o meu quintal». O '
            'que fazem os dois versos?","o":["Identificam elementos de dois planos, em vez de apenas os colocarem lado a lado","Narram '
            'duas viagens reais, primeiro de barco e depois de comboio","Apagam o presente para contar só acontecimentos da '
            'infância","Usam uma comparação explícita introduzida por «como»"],"c":0,"f":"Em I, **navios e árvores**; em VI, **teatro e '
            'quintal**. As formas de «ser» fundem os planos. A VI transporta a mesma técnica para outra relação: presente e '
            'memória.","fe":[null,"Os versos não contam duas viagens: sobrepõem lugares na experiência do sujeito.","A infância é central '
            'em VI, mas não constitui um dos planos de I. Procura uma operação comum aos dois versos.","Nestes dois versos não aparece '
            '«como»: «são» e «é» constroem uma identificação."]}',
  'novo': '{"t":"escolha","g":"escuta-vi-transferencia","p":"Compara I e VI: «os navios […] são estas árvores» e «Todo o teatro é o meu '
          'quintal». O que aproxima estes versos?","p2":"I: «os navios […] são estas árvores»; VI: «Todo o teatro é o meu quintal». O que '
          'fazem os dois versos?","o":["Identificam dois planos distintos, fazendo um passar pelo outro","Alternam dois planos, '
          'descrevendo um lugar depois do outro","Substituem o presente, deixando no verso apenas o lugar da memória"],"c":0,"f":"Em I, '
          '**navios e árvores**; em VI, **teatro e quintal**. As formas de «ser» fundem os planos. A VI transporta a mesma técnica para '
          'outra relação: presente e memória.","fe":[null,"Confundes fusão com alternância. Relê «são» e «é»: cada verbo identifica '
          'elementos, sem narrar uma passagem entre lugares.","Confundes cruzamento com apagamento. Relê os dois pares: navios e árvores, '
          'teatro e quintal. Os dois planos permanecem reconhecíveis."]}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm8/licao-m8-f12/index.html',
  'local': 'M8-F12 C09',
  'antigo': '{"t":"escolha","p":"Que leitura se destaca em «Todas as manhãs, relia a carta»?","p2":"Que valor é destacado por «todas as '
            'manhãs» nesta frase?","o":["iterativo","perfetivo","habitual","genérico"],"c":2,"f":"**Habitual**: «todas as manhãs» '
            'apresenta a releitura como um costume. Um hábito também envolve repetição. Em «Naquela revisão, releu a carta várias vezes», '
            'destaca-se a repetição num episódio; não é necessária uma contagem exata.","g":"fim","fe":["Há repetição, mas «todas as '
            'manhãs» apresenta-a como costume, não como um episódio delimitado.","«Relia», no imperfeito, não apresenta uma releitura '
            'concluída; e «todas as manhãs» marca regularidade.",null,"O genérico fala de uma classe em geral («Os contos são narrativas '
            'breves»); aqui é o costume de alguém."]}',
  'novo': '{"t":"escolha","p":"Exemplo criado: Todas as manhãs, relia a carta. Que valor aspetual destaca a expressão '
          'inicial?","g":"fim","o":["habitual","perfetivo","genérico"],"c":0,"f":"Habitual: «todas as manhãs» apresenta a releitura como '
          'um costume. Um hábito também envolve repetição: habitual e iterativo não são rótulos sempre '
          'incompatíveis.","fe":[null,"Confundes a regularidade de alguém com a conclusão de um ato. Relê «todas as manhãs» e «relia»: que '
          'costume apresentam?","Confundes um costume de alguém com uma verdade geral. Relê «todas as manhãs» e «relia»: a frase descreve '
          'uma situação particular."]}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm8/licao-m8-f12/index.html',
  'local': 'M8-F12 C17',
  'antigo': '{"t":"vf","p":"A revisão do módulo vem antes da prova de recuperação e das tarefas.","p2":"Esta lição de revisão antecede a '
            'prova e as tarefas.","v":true,"f":"Verdadeiro: poesia e conto, valor aspetual, anáfora e catáfora, numa só '
            'lição.","g":"fim","fe":"É verdadeiro: esta lição junta poesia, conto e gramática antes da prova; «Abre» diz: antes da prova, '
            'volta a tudo o que leste."}',
  'novo': '{"t":"escolha","p":"Exemplo criado: um poema retoma uma oração e muda o pedido final. Que pergunta recupera a lente da '
          'tradição?","f":"A lente da tradição pergunta pelo que o texto retoma e transforma. As palavras conservadas e a mudança final '
          'permitem testar essa relação.","g":"fim","fe":["Esta pergunta usa as figurações de quem escreve. Não é uma pergunta errada em '
          'geral; é uma pergunta diferente da que o caso pede. Relê o que o caso diz: o poema retoma uma oração e muda o pedido '
          'final.",null,"Esta pergunta usa a lente do contemporâneo. Pode ser útil noutra leitura, mas não identifica por si o diálogo com '
          'a oração. Relê a relação indicada entre a oração e o poema: que palavras e que mudança permitem compará-los?"],"o":["Que imagem '
          'de quem escreve surge e como se mostra essa voz?","Que palavras conserva da oração e que efeito produz a mudança?","Que '
          'problema do seu tempo aparece e que pessoas ficam afetadas?"],"c":1}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm8/licao-m8-f12/index.html',
  'local': 'M8-F12 C22',
  'antigo': '{"t":"ler","rot":"Para levar","escuro":true,"html":"<h2>Experimenta a outra leitura</h2><p>No exemplo inventado da poeta e da '
            'editora, muda a frase para deixar claro que foi <b>a poeta</b> a levar o manuscrito. Diz a nova versão ou anota-a no '
            'caderno.</p><details><summary>Rever a reformulação</summary><p>«A poeta conversou com a editora. A poeta levou o manuscrito.» '
            'Aqui, a repetição resolve a ambiguidade. Também podes reorganizar a informação, desde que conserves quem conversou e quem '
            'levou o manuscrito.</p><p>Num texto teu, procura uma retoma: o leitor tem informação para perceber a quem se refere? Se '
            'deixaste uma dúvida de propósito, explica a sua função e o indício que a sustenta.</p></details><svg class=\\"simbolo '
            'tracar\\" viewBox=\\"0 0 48 48\\" aria-hidden=\\"true\\" data-ico=\\"maquina\\" data-gesto=\\"tecla\\"><path d=\\"M8 40V28a4 '
            '4 0 0 1 4-4h24a4 4 0 0 1 4 4v12z\\"/><path d=\\"M12 24v-8h24v8\\"/><path d=\\"M16 12h16\\"/><path d=\\"M14 32h20M16 '
            '36h16\\"/><path d=\\"M20 20h8\\"/></svg><svg class=\\"simbolo azulejo canto\\" viewBox=\\"0 0 48 48\\" aria-hidden=\\"true\\" '
            'data-ico=\\"azulejo\\"><path d=\\"M4 4h40v40H4z\\"/><path d=\\"M24 4v40M4 24h40\\"/><path d=\\"M24 10l6 14-6 '
            '14-6-14z\\"/><path d=\\"M10 24l14-6 14 6-14 6z\\"/><circle cx=\\"24\\" cy=\\"24\\" r=\\"3\\"/><path d=\\"M4 4l8 8M44 4l-8 8M4 '
            '44l8-8M44 44l-8-8\\"/></svg><p class=\\"levar\\"><span class=\\"ch\\" style=\\"--i:0\\">Q</span><span class=\\"ch\\" '
            'style=\\"--i:1\\">u</span><span class=\\"ch\\" style=\\"--i:2\\">e</span><span class=\\"ch\\" style=\\"--i:3\\"> </span><span '
            'class=\\"ch\\" style=\\"--i:4\\">t</span><span class=\\"ch\\" style=\\"--i:5\\">e</span><span class=\\"ch\\" '
            'style=\\"--i:6\\">x</span><span class=\\"ch\\" style=\\"--i:7\\">t</span><span class=\\"ch\\" style=\\"--i:8\\">o</span><span '
            'class=\\"ch\\" style=\\"--i:9\\"> </span><span class=\\"ch\\" style=\\"--i:10\\">d</span><span class=\\"ch\\" '
            'style=\\"--i:11\\">o</span><span class=\\"ch\\" style=\\"--i:12\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:13\\">m</span><span class=\\"ch\\" style=\\"--i:14\\">ó</span><span class=\\"ch\\" '
            'style=\\"--i:15\\">d</span><span class=\\"ch\\" style=\\"--i:16\\">u</span><span class=\\"ch\\" '
            'style=\\"--i:17\\">l</span><span class=\\"ch\\" style=\\"--i:18\\">o</span><span class=\\"ch\\" style=\\"--i:19\\"> '
            '</span><span class=\\"ch\\" style=\\"--i:20\\">v</span><span class=\\"ch\\" style=\\"--i:21\\">a</span><span class=\\"ch\\" '
            'style=\\"--i:22\\">i</span><span class=\\"ch\\" style=\\"--i:23\\">s</span><span class=\\"ch\\" style=\\"--i:24\\"> '
            '</span><span class=\\"ch\\" style=\\"--i:25\\">r</span><span class=\\"ch\\" style=\\"--i:26\\">e</span><span class=\\"ch\\" '
            'style=\\"--i:27\\">l</span><span class=\\"ch\\" style=\\"--i:28\\">e</span><span class=\\"ch\\" '
            'style=\\"--i:29\\">r</span><span class=\\"ch\\" style=\\"--i:30\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:31\\">p</span><span class=\\"ch\\" style=\\"--i:32\\">o</span><span class=\\"ch\\" '
            'style=\\"--i:33\\">r</span><span class=\\"ch\\" style=\\"--i:34\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:35\\">v</span><span class=\\"ch\\" style=\\"--i:36\\">o</span><span class=\\"ch\\" '
            'style=\\"--i:37\\">n</span><span class=\\"ch\\" style=\\"--i:38\\">t</span><span class=\\"ch\\" '
            'style=\\"--i:39\\">a</span><span class=\\"ch\\" style=\\"--i:40\\">d</span><span class=\\"ch\\" '
            'style=\\"--i:41\\">e</span><span class=\\"ch\\" style=\\"--i:42\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:43\\">p</span><span class=\\"ch\\" style=\\"--i:44\\">r</span><span class=\\"ch\\" '
            'style=\\"--i:45\\">ó</span><span class=\\"ch\\" style=\\"--i:46\\">p</span><span class=\\"ch\\" '
            'style=\\"--i:47\\">r</span><span class=\\"ch\\" style=\\"--i:48\\">i</span><span class=\\"ch\\" '
            'style=\\"--i:49\\">a</span><span class=\\"ch\\" style=\\"--i:50\\">?</span><span class=\\"ch\\" style=\\"--i:51\\"> '
            '</span><span class=\\"ch\\" style=\\"--i:52\\">S</span><span class=\\"ch\\" style=\\"--i:53\\">e</span><span class=\\"ch\\" '
            'style=\\"--i:54\\"> </span><span class=\\"ch\\" style=\\"--i:55\\">a</span><span class=\\"ch\\" style=\\"--i:56\\"> '
            '</span><span class=\\"ch\\" style=\\"--i:57\\">r</span><span class=\\"ch\\" style=\\"--i:58\\">e</span><span class=\\"ch\\" '
            'style=\\"--i:59\\">s</span><span class=\\"ch\\" style=\\"--i:60\\">p</span><span class=\\"ch\\" '
            'style=\\"--i:61\\">o</span><span class=\\"ch\\" style=\\"--i:62\\">s</span><span class=\\"ch\\" '
            'style=\\"--i:63\\">t</span><span class=\\"ch\\" style=\\"--i:64\\">a</span><span class=\\"ch\\" style=\\"--i:65\\"> '
            '</span><span class=\\"ch\\" style=\\"--i:66\\">f</span><span class=\\"ch\\" style=\\"--i:67\\">o</span><span class=\\"ch\\" '
            'style=\\"--i:68\\">r</span><span class=\\"ch\\" style=\\"--i:69\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:70\\">n</span><span class=\\"ch\\" style=\\"--i:71\\">e</span><span class=\\"ch\\" '
            'style=\\"--i:72\\">n</span><span class=\\"ch\\" style=\\"--i:73\\">h</span><span class=\\"ch\\" '
            'style=\\"--i:74\\">u</span><span class=\\"ch\\" style=\\"--i:75\\">m</span><span class=\\"ch\\" '
            'style=\\"--i:76\\">,</span><span class=\\"ch\\" style=\\"--i:77\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:78\\">o</span><span class=\\"ch\\" style=\\"--i:79\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:80\\">m</span><span class=\\"ch\\" style=\\"--i:81\\">ó</span><span class=\\"ch\\" '
            'style=\\"--i:82\\">d</span><span class=\\"ch\\" style=\\"--i:83\\">u</span><span class=\\"ch\\" '
            'style=\\"--i:84\\">l</span><span class=\\"ch\\" style=\\"--i:85\\">o</span><span class=\\"ch\\" style=\\"--i:86\\"> '
            '</span><span class=\\"ch\\" style=\\"--i:87\\">a</span><span class=\\"ch\\" style=\\"--i:88\\">i</span><span class=\\"ch\\" '
            'style=\\"--i:89\\">n</span><span class=\\"ch\\" style=\\"--i:90\\">d</span><span class=\\"ch\\" '
            'style=\\"--i:91\\">a</span><span class=\\"ch\\" style=\\"--i:92\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:93\\">n</span><span class=\\"ch\\" style=\\"--i:94\\">ã</span><span class=\\"ch\\" '
            'style=\\"--i:95\\">o</span><span class=\\"ch\\" style=\\"--i:96\\"> </span><span class=\\"ch\\" '
            'style=\\"--i:97\\">a</span><span class=\\"ch\\" style=\\"--i:98\\">c</span><span class=\\"ch\\" '
            'style=\\"--i:99\\">a</span><span class=\\"ch\\" style=\\"--i:100\\">b</span><span class=\\"ch\\" '
            'style=\\"--i:101\\">o</span><span class=\\"ch\\" style=\\"--i:102\\">u</span><span class=\\"ch\\" '
            'style=\\"--i:103\\">.</span></p>"}',
  'novo': '{"t":"ler","rot":"Para levar","escuro":true,"html":"<h2>Experimenta a outra leitura</h2><p>No exemplo inventado da poeta e da '
          'editora, muda a frase para deixar claro que foi <b>a poeta</b> a levar o manuscrito. Diz a nova versão ou anota-a no '
          'caderno.</p><details><summary>Rever a reformulação</summary><p>«A poeta conversou com a editora. A poeta levou o manuscrito.» '
          'Aqui, a repetição resolve a ambiguidade. Também podes reorganizar a informação, desde que conserves quem conversou e quem levou '
          'o manuscrito.</p><p>Num texto teu, procura uma retoma: o leitor tem informação para perceber a quem se refere? Se deixaste uma '
          'dúvida de propósito, explica a sua função e o indício que a sustenta.</p></details><svg class=\\"simbolo tracar\\" viewBox=\\"0 '
          '0 48 48\\" aria-hidden=\\"true\\" data-ico=\\"maquina\\" data-gesto=\\"tecla\\"><path d=\\"M8 40V28a4 4 0 0 1 4-4h24a4 4 0 0 1 '
          '4 4v12z\\"/><path d=\\"M12 24v-8h24v8\\"/><path d=\\"M16 12h16\\"/><path d=\\"M14 32h20M16 36h16\\"/><path d=\\"M20 '
          '20h8\\"/></svg><svg class=\\"simbolo azulejo canto\\" viewBox=\\"0 0 48 48\\" aria-hidden=\\"true\\" '
          'data-ico=\\"azulejo\\"><path d=\\"M4 4h40v40H4z\\"/><path d=\\"M24 4v40M4 24h40\\"/><path d=\\"M24 10l6 14-6 14-6-14z\\"/><path '
          'd=\\"M10 24l14-6 14 6-14 6z\\"/><circle cx=\\"24\\" cy=\\"24\\" r=\\"3\\"/><path d=\\"M4 4l8 8M44 4l-8 8M4 44l8-8M44 '
          '44l-8-8\\"/></svg><p class=\\"levar\\">Que texto compreendes agora de outra maneira? Mostra a passagem que mudou a tua '
          'leitura.</p>"}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm9/recursos/f13.js',
  'local': 'M9-F13 C02',
  'antigo': '{"t":"ler","rot":"Lê e confronta","titulo":"Caderno de leitura: quatro estações","html":"<p>Oficina longa, com o livro '
            'aberto, em quatro estações: hipótese inicial; confronto de episódios; contraexemplo e revisão; síntese fundamentada. Entre '
            'estações, discute a leitura com um colega e anota a página da edição.</p><p>Hipótese a testar: a liberdade no romance '
            'consiste em escapar ao mundo do poder. Não a aceites como resposta final: confronta-a com o voo da passarola (XVI), a '
            'violência e a memória dos trabalhadores (XIX) e o reencontro final (XXV).</p>"}',
  'novo': '{"t":"ler","rot":"Lê e confronta","titulo":"Caderno de leitura: quatro estações","html":"<p>Oficina longa, com o livro aberto, '
          'em quatro estações: hipótese inicial; confronto de episódios; contraexemplo e revisão; síntese fundamentada. Entre estações, '
          'discute a leitura com um colega e anota a página da edição.</p><p>Hipótese a testar: a liberdade no romance consiste em escapar '
          'ao mundo do poder. Não a aceites como resposta final: confronta-a com o voo da passarola (XVI), a violência e a memória dos '
          'trabalhadores (XIX) e o reencontro final (XXV).</p><p>O voo prova uma liberdade completa, ou o final obriga-te a mudar essa '
          'leitura? Escolhe uma resposta provisória. No fim, vais voltar a ela com duas passagens do livro.</p>"}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm9/recursos/f13.js',
  'local': 'M9-F13 C10',
  'antigo': '{"t":"escolha","p":"O nome desconhecido da viúva invalida todo o gesto de memória?","o":["Sim: uma narrativa só vale se '
            'conseguir dizer tudo sobre todos","Não: mostra um limite que o próprio gesto de recordar admite","Sim: prova que a dor da '
            'viúva não interessa nada à obra","Não: autoriza inventar-lhe uma biografia e apresentá-la como facto"],"c":1,"f":"O limite é '
            '**reconhecido**, não escondido. Recordar pode ser necessário sem ser total. Nem a impossibilidade de contar tudo torna inútil '
            'a memória, nem autoriza preencher a falta com uma biografia falsamente atribuída ao romance.","g":"m9-f13-6","fe":["Nenhuma '
            'narrativa diz tudo; o romance recupera muito e confessa o nome que lhe falta («Estação 2: a pedra e a viúva»).",null,"O '
            'narrador detém-se na viúva para dizer que não lhe sabe o nome: é um limite assumido, não desinteresse («Estação 2»).","A '
            'falta não autoriza inventar: preencher o nome com uma biografia seria atribuir ao romance o que ele não diz."]}',
  'novo': '{"t":"escolha","p":"O narrador recupera trabalhadores esquecidos, mas não sabe o nome da viúva. Que revisão explica os dois '
          'dados?","f":"A revisão conserva o gesto de recordar e reconhece a falta. Confronta-a com a passagem: recuperar uma vida não '
          'implica conhecer todos os seus dados.","g":"m9-f13-6","fe":["Uma lacuna não autoriza apresentar uma invenção como informação do '
          'romance. Podes formular uma pergunta sobre a falta; não podes preenchê-la como facto. Relê na Estação 2 a frase em que o '
          'narrador diz que não sabe o nome.",null,"A falta do nome não torna dispensável a passagem. O próprio limite faz parte do que a '
          'narrativa mostra sobre recordar quem foi esquecido. Relê na Estação 2 a frase em que o narrador diz que não sabe o '
          'nome."],"o":["A memória recupera vidas, por isso permite completar os nomes que faltam.","A memória recupera vidas, embora '
          'deixe parte do seu percurso por conhecer.","A memória recupera vidas, por isso o anonimato torna o episódio '
          'dispensável."],"c":1}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm9/recursos/f13.js',
  'local': 'M9-F13 C21',
  'antigo': '{"t":"escolha","p":"Que síntese explica melhor os confrontos realizados?","o":["A liberdade é fuga definitiva: no final, o '
            'poder desaparece","Junta liberdade e vínculo à violência e aos limites da memória","A memória só conta se reproduzir todas as '
            'vidas por inteiro","Como há elementos extraordinários, nenhuma cena apoia uma leitura"],"c":1,"f":"A segunda síntese consegue '
            'explicar **possibilidades e limites** sem reduzir o romance a um slogan. O voo e o vínculo não apagam a violência; os limites '
            'da memória não anulam a tentativa de recordar. A interpretação ganha força por suportar o confronto, não por prometer '
            'explicar tudo.","g":"m9-f13-15","fe":["O final não mostra o poder a desaparecer: Baltasar morre num auto de fé («Estação '
            '3»).",null,"A memória pode ter limites e contar: o romance recorda muitos sem saber o nome da viúva («Estação 2»).","O '
            'extraordinário pertence ao mundo ficcional e lê-se com as regras dele; o voo e as vontades apoiam leituras («Estação 1», '
            '«Estação 3»)."]}',
  'novo': '{"t":"escolha","p":"Que revisão da hipótese explica o voo e o reencontro final?","f":"O voo e o vínculo abrem possibilidades, '
          'mas não eliminam a morte de Baltasar. Uma hipótese mais precisa explica tanto a ação de Blimunda como o auto de '
          'fé.","g":"m9-f13-15","fe":[null,"Confundes persistência do vínculo com vitória sobre a violência. Relê na Estação 3 onde '
          'Baltasar morre e o que Blimunda recolhe.","Confundes a perda com a anulação do que foi vivido. Relê na Estação 3 o gesto de '
          'Blimunda: o que conserva apesar da morte?"],"o":["O voo afirma liberdade partilhada; o final conserva o vínculo sem apagar a '
          'violência.","O voo afirma liberdade partilhada; o final mostra que ela acaba por vencer a violência.","O voo afirma liberdade '
          'partilhada; o final torna sem valor tudo o que a construiu."],"c":0}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'm9/recursos/f13.js',
  'local': 'M9-F13 C23',
  'antigo': '{"t":"ler","rot":"Para levar","html":"<p class=\\"levar\\">Uma interpretação melhora quando explica também o que a obriga a '
            'mudar.</p><p>No caderno, escreve uma síntese tua: hipótese revista, dois episódios em confronto e uma limitação reconhecida. '
            'Revê-a com o livro antes de a usares no comentário ou no debate.</p><p>Fonte da obra e contexto editorial: <a '
            'href=\\"https://www.josesaramago.org/livro/memorial-do-convento/\\" target=\\"_blank\\" rel=\\"noopener\\">Fundação José '
            'Saramago, Memorial do Convento</a>. As passagens literárias leem-se no livro; a paginação varia entre edições.</p>"}',
  'novo': '{"t":"ler","rot":"Para levar","html":"<p class=\\"levar\\">Uma interpretação melhora quando explica também o que a obriga a '
          'mudar.</p><p>No caderno, escreve quatro a seis linhas. Retoma a hipótese inicial sobre a liberdade: apresenta a tua leitura '
          'agora, uma passagem que a apoia e outra que a limita, com as páginas da tua edição. Explica o que mudou. Se manténs a hipótese, '
          'mostra como ela resiste ao contraexemplo. Revê a síntese com o livro.</p><p>Fonte da obra e contexto editorial: <a '
          'href=\\"https://www.josesaramago.org/livro/memorial-do-convento/\\" target=\\"_blank\\" rel=\\"noopener\\">Fundação José '
          'Saramago, <i>Memorial do Convento</i></a>. As passagens literárias leem-se no livro; a paginação varia entre edições.</p>"}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'tarefas/m4-u1/aquecimento/index.html',
  'local': 'A-M4 C05',
  'antigo': '{"t": "escolha", "p": "No ensaio com relógio, a tua apresentação chega aos cinco minutos. O que fazes?", "p2": "A '
            'apresentação tem de durar três a quatro minutos, e o ensaio deu cinco. Qual é a boa decisão?", "o": ["Cortas o que se repete '
            'e voltas a ensaiar.", "Falas mais depressa, para caber tudo no tempo.", "Deixas assim: um minuto a mais não conta."], "c": 0, '
            '"f": "Três a quatro minutos é um critério, e o ensaio com relógio serve para mudares alguma coisa (F10). Corta o que se '
            'repete, não a citação, o recurso ou a resposta à objeção.", "fe": [null, "Falar depressa tira clareza: quem ouve não pode '
            'voltar atrás. Ganha tempo a cortar, não a acelerar.", "O tempo conta: são três a quatro minutos. Um ensaio que passa do '
            'limite pede uma mudança."], "g": 4}',
  'novo': '{"t": "escolha", "p": "Caso criado: o teu ensaio dura cinco minutos. Repetes a mesma ideia, citas Vieira e explicas o efeito da '
          'citação. Que revisão conserva o essencial?", "f": "A repetição ocupa tempo sem acrescentar prova. Depois do corte, confirma se '
          'ainda explicas a relação entre a citação e a ideia e se cumpres o tempo pedido.", "fe": ["Confundes uma prova com uma repetição '
          'dispensável. Relê a citação de Vieira e a frase que repete a ideia: qual delas sustenta a interpretação?", "Confundes a '
          'explicação da prova com a repetição da ideia. Relê a ligação entre a citação e o efeito: sem ela, como se percebe o '
          'raciocínio?", null], "g": 4, "o": ["Cortas a citação de Vieira, manténs a repetição e voltas a medir o tempo.", "Cortas a '
          'explicação do efeito, manténs a repetição e voltas a medir o tempo.", "Cortas a ideia repetida, manténs a prova e a sua '
          'explicação e medes o tempo."], "c": 2}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'exame/provas/2026-1f/grupo-i/index.html',
  'local': 'E-2026-I C34',
  'antigo': '{"t": "vf", "g": "3c", "l": "29", "p": "As frontarias da Rua dos Douradores são descritas como grandiosas e ricas.", "p2": '
            '"Ricardo Reis vê na rua prédios imponentes e cheios de ornamentos.", "v": false, "f": "Falso. São altas, mas «de cinza parda» '
            '(linha 29), com «monótonas cantarias» (linha 30), e os prédios estão «porejando sombra e humidade» (linha 34). Altura não é '
            'grandeza: a rua é parda e húmida. Por isso, no espaço (a), a opção (3), «monumentalidade», não serve.", "fe": "As frontarias '
            'são «de cinza parda» (linha 29) e as cantarias, «monótonas» (linha 30). Nada de riqueza: a opção (3), «monumentalidade», não '
            'serve.", "rot": "Porquê? Verdadeiro ou falso"}',
  'novo': '{"t": "sublinhar", "g": "3c", "l": "29", "p": "Toca nas duas palavras que caracterizam a cor das frontarias e limitam a leitura '
          'de riqueza.", "f": "«Cinza parda» caracteriza a cor; «altas» indica dimensão. Na linha 29, a altura não basta para defender a '
          'monumentalidade, sobretudo quando a linha 30 acrescenta a monotonia.", "fe": "Confundes altura com riqueza. Relê a linha 29: '
          'depois de «frontarias de», que duas palavras descrevem a cor?", "rot": "Porquê? Toca nas palavras", "frase": "e ver as altas '
          'frontarias de cinza parda,", "certas": [6, 7]}',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145; revisão curta do #149'},
 {'ficheiro': 'docs/pedagogia/aquecimentos/m4-u1.json',
  'local': 'A-M4 fonte do gerador',
  'antigo': '{\n'
            '   "t": "escolha",\n'
            '   "p": "No ensaio com relógio, a tua apresentação chega aos cinco minutos. O que fazes?",\n'
            '   "p2": "A apresentação tem de durar três a quatro minutos, e o ensaio deu cinco. Qual é a boa decisão?",\n'
            '   "o": [\n'
            '    "Cortas o que se repete e voltas a ensaiar.",\n'
            '    "Falas mais depressa, para caber tudo no tempo.",\n'
            '    "Deixas assim: um minuto a mais não conta."\n'
            '   ],\n'
            '   "c": 0,\n'
            '   "f": "Três a quatro minutos é um critério, e o ensaio com relógio serve para mudares alguma coisa (F10). Corta o que se '
            'repete, não a citação, o recurso ou a resposta à objeção.",\n'
            '   "fe": [\n'
            '    null,\n'
            '    "Falar depressa tira clareza: quem ouve não pode voltar atrás. Ganha tempo a cortar, não a acelerar.",\n'
            '    "O tempo conta: são três a quatro minutos. Um ensaio que passa do limite pede uma mudança."\n'
            '   ],\n'
            '   "g": 4\n'
            '  }',
  'novo': '{\n'
          '   "t": "escolha",\n'
          '   "p": "Caso criado: o teu ensaio dura cinco minutos. Repetes a mesma ideia, citas Vieira e explicas o efeito da citação. Que '
          'revisão conserva o essencial?",\n'
          '   "f": "A repetição ocupa tempo sem acrescentar prova. Depois do corte, confirma se ainda explicas a relação entre a citação e '
          'a ideia e se cumpres o tempo pedido.",\n'
          '   "fe": [\n'
          '    "Confundes uma prova com uma repetição dispensável. Relê a citação de Vieira e a frase que repete a ideia: qual delas '
          'sustenta a interpretação?",\n'
          '    "Confundes a explicação da prova com a repetição da ideia. Relê a ligação entre a citação e o efeito: sem ela, como se '
          'percebe o raciocínio?",\n'
          '    null\n'
          '   ],\n'
          '   "g": 4,\n'
          '   "o": [\n'
          '    "Cortas a citação de Vieira, manténs a repetição e voltas a medir o tempo.",\n'
          '    "Cortas a explicação do efeito, manténs a repetição e voltas a medir o tempo.",\n'
          '    "Cortas a ideia repetida, manténs a prova e a sua explicação e medes o tempo."\n'
          '   ],\n'
          '   "c": 2\n'
          '  }',
  'ocorrencias': 1,
  'achado': '01/11/2026: primeiro lote de conteúdos aprovado'},
 {'ficheiro': 'scripts/provas/dados/2026-1f/grupo-i.json',
  'local': 'E-2026-I fonte do gerador',
  'antigo': '{\n'
            '   "t": "vf",\n'
            '   "g": "3c",\n'
            '   "l": "29",\n'
            '   "p": "As frontarias da Rua dos Douradores são descritas como grandiosas e ricas.",\n'
            '   "p2": "Ricardo Reis vê na rua prédios imponentes e cheios de ornamentos.",\n'
            '   "v": false,\n'
            '   "f": "Falso. São altas, mas «de cinza parda» (linha 29), com «monótonas cantarias» (linha 30), e os prédios estão '
            '«porejando sombra e humidade» (linha 34). Altura não é grandeza: a rua é parda e húmida. Por isso, no espaço (a), a opção '
            '(3), «monumentalidade», não serve.",\n'
            '   "fe": "As frontarias são «de cinza parda» (linha 29) e as cantarias, «monótonas» (linha 30). Nada de riqueza: a opção (3), '
            '«monumentalidade», não serve.",\n'
            '   "rot": "Porquê? Verdadeiro ou falso"\n'
            '  }',
  'novo': '{\n'
          '   "t": "sublinhar",\n'
          '   "g": "3c",\n'
          '   "l": "29",\n'
          '   "p": "Toca nas duas palavras que caracterizam a cor das frontarias e limitam a leitura de riqueza.",\n'
          '   "f": "«Cinza parda» caracteriza a cor; «altas» indica dimensão. Na linha 29, a altura não basta para defender a '
          'monumentalidade, sobretudo quando a linha 30 acrescenta a monotonia.",\n'
          '   "fe": "Confundes altura com riqueza. Relê a linha 29: depois de «frontarias de», que duas palavras descrevem a cor?",\n'
          '   "rot": "Porquê? Toca nas palavras",\n'
          '   "frase": "e ver as altas frontarias de cinza parda,",\n'
          '   "certas": [\n'
          '    6,\n'
          '    7\n'
          '   ]\n'
          '  }',
  'ocorrencias': 1,
  'achado': '01/11/2026: primeiro lote de conteúdos aprovado'},
 {'ficheiro': 'm4/index.html',
  'local': 'M4 unidade 1: prova esperada',
  'antigo': 'id="tarefa-unidade-1"><a href="../tarefas/m4-u1/"><span class="n">T</span><span><span class="t">Tarefa da Unidade 1 · Um '
            'peixe de hoje</span><span class="f">Aula de 90 minutos com consulta: aquecimento em cartões, guião em papel, apresentações em '
            'pequenos grupos ao mesmo tempo e fotografias no Teams.</span></span><span class="chip">90 '
            'min</span></a></li></ol></section></section>',
  'novo': 'id="tarefa-unidade-1"><a href="../tarefas/m4-u1/"><span class="n">T</span><span><span class="t">Tarefa da Unidade 1 · Um peixe '
          'de hoje</span><span class="f">Aula de 90 minutos com consulta: aquecimento em cartões, guião em papel, apresentações em '
          'pequenos grupos ao mesmo tempo e fotografias no Teams.</span></span><span class="chip">90 min</span></a></li></ol><p '
          'class="prova-esperada">No fim, explicas uma alegoria, mostras a passagem que a sustenta e respondes a uma '
          'objeção.</p></section></section>',
  'ocorrencias': 1,
  'achado': '01/11/2026: primeiro lote de conteúdos aprovado'},
 {'ficheiro': 'm4/index.html',
  'local': 'M4 unidade 2: prova esperada',
  'antigo': 'id="tarefa-unidade-2"><a href="../tarefas/m4-u2/"><span class="n">T</span><span><span class="t">Tarefa da Unidade 2 · '
            'Apreciação crítica do espetáculo</span><span class="f">Aula de 90 minutos com consulta: aquecimento em cartões, apreciação '
            'crítica em papel, síntese integrada e fotografias no Teams.</span></span><span class="chip">90 '
            'min</span></a></li></ol></section></section>',
  'novo': 'id="tarefa-unidade-2"><a href="../tarefas/m4-u2/"><span class="n">T</span><span><span class="t">Tarefa da Unidade 2 · '
          'Apreciação crítica do espetáculo</span><span class="f">Aula de 90 minutos com consulta: aquecimento em cartões, apreciação '
          'crítica em papel, síntese integrada e fotografias no Teams.</span></span><span class="chip">90 min</span></a></li></ol><p '
          'class="prova-esperada">No fim, explicas um conflito, relacionas uma fala com uma indicação de cena e justificas uma escolha de '
          'representação.</p></section></section>',
  'ocorrencias': 1,
  'achado': '01/11/2026: primeiro lote de conteúdos aprovado'},
 {'ficheiro': 'm4/index.html',
  'local': 'M4 unidade 3: prova esperada',
  'antigo': 'id="tarefa-unidade-3"><a href="../tarefas/m4-u3-discurso/"><span class="n">T</span><span><span class="t">Tarefa da Unidade 3 '
            '· Discurso no abrigo</span><span class="f">Aula de 90 minutos com consulta: aquecimento em cartões, discurso em papel, '
            'apresentações em pequenos grupos ao mesmo tempo e fotografias no Teams.</span></span><span class="chip">90 '
            'min</span></a></li></ol></section></section>',
  'novo': 'id="tarefa-unidade-3"><a href="../tarefas/m4-u3-discurso/"><span class="n">T</span><span><span class="t">Tarefa da Unidade 3 · '
          'Discurso no abrigo</span><span class="f">Aula de 90 minutos com consulta: aquecimento em cartões, discurso em papel, '
          'apresentações em pequenos grupos ao mesmo tempo e fotografias no Teams.</span></span><span class="chip">90 '
          'min</span></a></li></ol><p class="prova-esperada">No fim, sustentas com uma passagem a tua leitura da relação entre personagens '
          'e confrontas uma interpretação diferente.</p></section></section>',
  'ocorrencias': 1,
  'achado': '01/11/2026: primeiro lote de conteúdos aprovado'},
 {'ficheiro': 'm4/index.html',
  'local': 'M4 prova: peça de fecho',
  'antigo': '</head>',
  'novo': '<style>.unidade>.prova-esperada{text-wrap:pretty;margin:8px 0 0;padding-left:43px;max-width:calc(70ch + 43px);font:400 1rem/1.5 '
          'Georgia,serif;color:var(--suave)}@media(min-width:601px){.unidade>.prova-esperada{padding-left:64px;max-width:calc(70ch + '
          '64px)}}.unidade>.prova-esperada::before{content:"Prova da unidade";display:block;margin:0 0 4px;font:700 .8125rem/1.3 '
          'Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--tinta)}</style></head>',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145'},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: contagem',
  'antigo': '12 cartões na aula',
  'novo': '13 cartões na aula',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145'},
 {'ficheiro': 'm9/painel-m9-f13/index.html',
  'local': 'M9 medição: procedimento e rubrica',
  'antigo': '</main>',
  'novo': '<section id="medicao-piloto"><h2>Medição em papel: quatro critérios</h2><p>Os três casos criados estão no anexo privado, fora '
          'do sítio. Aplicação individual, sem classificação pública nem registo no aparelho.</p><h3>Procedimento</h3><ol><li>Antes da '
          'oficina, dá o primeiro caso durante oito minutos, sem consulta nem discussão prévia.</li><li>Depois da oficina, aplica o '
          'segundo caso nas mesmas condições. Uma semana depois, aplica o terceiro, sem preparação adicional.</li><li>Em cada momento, '
          'pede a mesma resposta em quatro a seis linhas: uma hipótese, um detalhe que a apoie, outro que a limite e uma revisão que '
          'explique ambos.</li><li>Aplica os quatro critérios, cada um com 0 ou 1, com as notas de correção guardadas fora do sítio. '
          'Regista apenas os totais da turma na tabela impressa. Compara também o número de participantes: não atribuas diferenças à '
          'oficina sem considerar ausências e diferenças entre casos.</li></ol><p>Antes de usar, dois revisores classificam o mesmo '
          'pequeno conjunto de respostas de exemplo e resolvem as divergências.</p><p>Os resultados leem-se como indícios de transferência '
          'e de usabilidade, nunca como prova de eficácia.</p><h3>Grelha comum</h3><div '
          'class="medicao-tabela"><table><thead><tr><th>Critério</th><th>1 ponto</th><th>0 pontos</th></tr></thead><tbody><tr><th>Responde '
          'à pergunta</th><td>Apresenta uma resposta pertinente à pergunta.</td><td>Não responde à pergunta.</td></tr><tr><th>Usa um '
          'indício pertinente</th><td>Seleciona um detalhe pertinente do caso.</td><td>Não seleciona um indício '
          'pertinente.</td></tr><tr><th>Explica a ligação entre o indício e a conclusão</th><td>Explica como o detalhe sustenta a '
          'conclusão.</td><td>Não explica a ligação.</td></tr><tr><th>Reconhece um limite ou distingue uma alternativa '
          'próxima</th><td>Delimita a conclusão ou distingue uma leitura próxima.</td><td>Não reconhece um limite nem distingue uma '
          'alternativa.</td></tr></tbody></table></div><h3>Totais da turma</h3><p>Em cada critério, indica quantas respostas obtiveram 1 '
          'ponto. Na distribuição, conta as respostas com cada total. Não inscrevas nomes nem transcrevas respostas individuais.</p><div '
          'class="medicao-tabela"><table><thead><tr><th>Total da turma</th><th>Antes</th><th>Depois</th><th>Uma semana '
          'depois</th></tr></thead><tbody><tr><th>Participantes</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Responde à '
          'pergunta: 1 ponto</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Usa um indício pertinente: 1 '
          'ponto</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Explica a ligação entre o indício e a conclusão: 1 '
          'ponto</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Reconhece um limite ou distingue uma alternativa próxima: 1 '
          'ponto</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Respostas com '
          '0/4</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Respostas com '
          '1/4</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Respostas com '
          '2/4</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Respostas com '
          '3/4</th><td>_____</td><td>_____</td><td>_____</td></tr><tr><th>Respostas com '
          '4/4</th><td>_____</td><td>_____</td><td>_____</td></tr></tbody></table></div></section></main>',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145'},
 {'ficheiro': 'm9/painel-m9-f13/index.html',
  'local': 'M9 medição: impressão e noindex',
  'antigo': '</head>',
  'novo': '<style '
          'id="conteudos-medicao">h1{font-size:39px}h2{font-size:31px}h3{font-size:25px}h1,h2,h3{text-wrap:balance}h2,h3{line-height:1.2}.medicao-tabela{max-width:100%;overflow-x:auto}#medicao-piloto '
          'table{width:100%;border-collapse:collapse;font:13px/1.5 Arial,sans-serif}#medicao-piloto th,#medicao-piloto td{border:1px solid '
          'currentColor;padding:8px;text-align:left;vertical-align:top}@media print{#medicao-piloto{break-before:page}#medicao-piloto '
          'h3,#medicao-piloto h3+p{break-after:avoid}#medicao-piloto ol,#medicao-piloto '
          '.medicao-tabela{break-inside:avoid}.medicao-tabela{overflow:visible}}</style><meta name="robots" content="noindex"></head>',
  'ocorrencias': 1,
  'achado': '01/11/2026: para depois do #144 e do #145'},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: complementos',
  'antigo': '4 cartões de pergunta e 2 de leitura',
  'novo': '3 cartões de pergunta e 2 de leitura',
  'ocorrencias': 1},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: C11 no núcleo',
  'antigo': '<li><span class="t">ler</span>Agora, em papel: A resposta que entregas</li>',
  'novo': '<li><span class="t">escolhe</span>Que contraste responde melhor à pergunta de abertura: por que razão fala Vieira aos '
          'peixes?</li><li><span class="t">ler</span>Agora, em papel: A resposta que entregas</li>',
  'ocorrencias': 1},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: C11 sai do complemento',
  'antigo': 'Os peixes em ordem (a segunda parte do texto), alegoria ou comparação',
  'novo': 'Alegoria ou comparação',
  'ocorrencias': 1},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: lista de 13',
  'antigo': 'Os 12 cartões da aula',
  'novo': 'Os 13 cartões da aula',
  'ocorrencias': 1},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: fecho 13',
  'antigo': 'Fechar</small><small>cartão 12',
  'novo': 'Fechar</small><small>cartão 13',
  'ocorrencias': 1},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: leitura e produção',
  'antigo': 'Escrever</small><small>cartão 11',
  'novo': 'Escrever</small><small>cartões 11 e 12',
  'ocorrencias': 1},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: pergunta do arco',
  'antigo': '«Agora, em papel»:',
  'novo': 'A pergunta sobre a atenção dos peixes e «Agora, em papel»:',
  'ocorrencias': 1},
 {'ficheiro': 'm4/aulas/aula-01/index.html',
  'local': 'M4 guião: turma no cartão 11',
  'antigo': 'Escrever sozinho, sem telemóvel.',
  'novo': 'Responder no telemóvel à pergunta sobre a atenção dos peixes e só então mostrar a resposta (tecla R). Depois, escrever sozinho, '
          'sem telemóvel.',
  'ocorrencias': 1},
 {'ficheiro': 'm4/painel-m4-f01/index.html',
  'local': 'M4-F01 painel: CARTOES',
  'antigo': '[{"k":2,"t":"escolha","p":"Porque não escolhe António nenhuma destas saídas?"},{"k":4,"t":"escolha","p":"Caso imaginário: a '
            'direção ignora as queixas da delegada de turma. Que faria António?"},{"k":7,"t":"escolha","p":"Mais à frente, Vieira '
            'repreende o peixe-voador, de barbatanas como asas. Lido como alegoria, que homem pode ele '
            'ser?"},{"k":9,"t":"emparelhar","p":"Que papel tem cada coisa, na história de António e na de '
            'Vieira?"},{"k":10,"t":"escolha","p":"Porque conta Vieira que os peixes ouviam assim?"},{"k":11,"t":"escolha","p":"Caso '
            'imaginário: o jornal da escola só fala de um aquário, mas todos percebem que é a escola. Que '
            'é?"},{"k":13,"t":"escolha","p":"Caso imaginário: um discurso de fim de curso abre com uma história do primeiro dia. Que parte '
            'é essa?"},{"k":15,"t":"emparelhar","p":"Que fim serve cada passo do cap. I: ensinar, deleitar ou comover?"}]',
  'novo': '[{"k":2,"t":"escolha","p":"Porque não escolhe António nenhuma destas saídas?"},{"k":4,"t":"escolha","p":"Caso imaginário: a '
          'direção ignora as queixas da delegada de turma. Que faria António?"},{"k":7,"t":"escolha","p":"Mais à frente, Vieira repreende '
          'o peixe-voador, de barbatanas como asas. Lido como alegoria, que homem pode ele ser?"},{"k":9,"t":"emparelhar","p":"Que papel '
          'tem cada coisa, na história de António e na de Vieira?"},{"k":10,"t":"escolha","p":"Que contraste responde melhor à pergunta de '
          'abertura: por que razão fala Vieira aos peixes?"},{"k":11,"t":"escolha","p":"Caso imaginário: o jornal da escola só fala de um '
          'aquário, mas todos percebem que é a escola. Que é?"},{"k":13,"t":"escolha","p":"Caso imaginário: um discurso de fim de curso '
          'abre com uma história do primeiro dia. Que parte é essa?"},{"k":15,"t":"emparelhar","p":"Que fim serve cada passo do cap. I: '
          'ensinar, deleitar ou comover?"}]',
  'ocorrencias': 1,
  'achado': '01/11/2026: sincronizar com a camada, depois do #144 e do #145'},
 {'ficheiro': 'm6/painel-m6-f01/index.html',
  'local': 'M6-F01 painel: CARTOES',
  'antigo': '[{"k":4,"t":"escolha","p":"Quem fala em «O Palacio da Ventura» e o que se sonha?"},{"k":5,"t":"sublinhar","p":"Toca nas três '
            'palavras repetidas que fazem a anáfora do verso."},{"k":6,"t":"completar","p":"Que palavra do soneto quer dizer '
            '«ansioso»?"},{"k":7,"t":"vf","p":"A primeira quadra termina com «O palacio encantado da '
            'Ventura!»."},{"k":8,"t":"sublinhar","p":"Toca nos dois adjetivos que dizem o estado do '
            'cavaleiro."},{"k":9,"t":"completar","p":"Que armas do cavaleiro estão desfeitas na segunda '
            'quadra?"},{"k":10,"t":"escolha","p":"«E eis que subito o avisto, fulgurante»: o que avista o '
            'cavaleiro?"},{"k":11,"t":"versos","p":"Põe os versos do primeiro terceto pela ordem do '
            'soneto."},{"k":12,"t":"escolha","p":"«Eu sou o Vagabundo, o Desherdado...»: quem o brada e a quem?"},{"k":14,"t":"vf","p":"As '
            'portas de ouro abrem-se devagar e em silêncio."},{"k":15,"t":"escolha","p":"O que encontra o cavaleiro quando as portas de '
            'ouro se abrem?"},{"k":16,"t":"completar","p":"Que recurso opõe «fulgurante» (v. 7) a «Silencio e escuridão» (v. '
            '14)?"},{"k":18,"t":"vf","p":"A chave de ouro deste soneto está na primeira quadra, em «busco '
            'anhelante»."},{"k":19,"t":"emparelhar","p":"Liga cada elemento da alegoria ao que '
            'representa."},{"k":20,"t":"completar","p":"Como se organizam as estrofes de «O Palacio da '
            'Ventura»?"},{"k":21,"t":"ordenar","p":"Os quatro tempos do soneto, por ordem:"},{"k":22,"t":"frase","p":"Põe por ordem o '
            'primeiro verso do último terceto."}]',
  'novo': '[{"k":4,"t":"escolha","p":"Quem fala em «O Palacio da Ventura» e o que se sonha?"},{"k":5,"t":"sublinhar","p":"Toca nas três '
          'palavras repetidas que fazem a anáfora do verso."},{"k":6,"t":"completar","p":"Que palavra do soneto quer dizer '
          '«ansioso»?"},{"k":7,"t":"vf","p":"A primeira quadra termina com «O palacio encantado da '
          'Ventura!»."},{"k":8,"t":"sublinhar","p":"Toca nos dois adjetivos que dizem o estado do '
          'cavaleiro."},{"k":9,"t":"completar","p":"Que armas do cavaleiro estão desfeitas na segunda '
          'quadra?"},{"k":10,"t":"escolha","p":"«E eis que subito o avisto, fulgurante»: o que avista o '
          'cavaleiro?"},{"k":11,"t":"versos","p":"Põe os versos do primeiro terceto pela ordem do soneto."},{"k":12,"t":"escolha","p":"«Eu '
          'sou o Vagabundo, o Desherdado...»: quem o brada e a quem?"},{"k":14,"t":"vf","p":"As portas de ouro abrem-se devagar e em '
          'silêncio."},{"k":15,"t":"escolha","p":"O cavaleiro vê abrirem-se as portas de ouro, mas encontra o vazio. Que pergunta ajuda a '
          'explicar esta mudança?"},{"k":16,"t":"completar","p":"Que recurso opõe «fulgurante» (v. 7) a «Silencio e escuridão» (v. '
          '14)?"},{"k":18,"t":"vf","p":"A chave de ouro deste soneto está na primeira quadra, em «busco '
          'anhelante»."},{"k":19,"t":"emparelhar","p":"Liga cada elemento da alegoria ao que '
          'representa."},{"k":20,"t":"completar","p":"Como se organizam as estrofes de «O Palacio da '
          'Ventura»?"},{"k":21,"t":"ordenar","p":"Os quatro tempos do soneto, por ordem:"},{"k":22,"t":"frase","p":"Põe por ordem o '
          'primeiro verso do último terceto."}]',
  'ocorrencias': 1,
  'achado': '01/11/2026: sincronizar com a camada, depois do #144 e do #145'},
 {'ficheiro': 'm7/painel-m7-f34/index.html',
  'local': 'M7-F34 painel: CARTOES',
  'antigo': '[{"k":3,"t":"versos","p":"Põe os versos da primeira estrofe do poema I pela ordem do '
            'poema."},{"k":4,"t":"sublinhar","p":"Toca na palavra que nomeia o lugar que o poeta vê e na que nomeia o lugar que ele '
            'sonha."},{"k":5,"t":"emparelhar","p":"Liga cada verso ao plano em que está."},{"k":7,"t":"completar","p":"«Liberto em duplo»: '
            'como se sente o poeta, e em que se torna o cais?"},{"k":8,"t":"escolha","p":"No cinema, a «dupla exposição» mostra duas '
            'imagens no mesmo sítio, uma através da outra. Que verso faz isso com palavras?"},{"k":9,"t":"vf","p":"Em «Com uma '
            'horizontalidade vertical», o poeta engana-se nas palavras."},{"k":11,"t":"escolha","p":"Que palavra do poema I quer dizer '
            '«fila, fileira»?"},{"k":13,"t":"completar","p":"No poema II, a vela de dentro diz-se com uma coisa de fora. '
            'Completa."},{"k":14,"t":"emparelhar","p":"Liga cada pedaço do poema II ao lugar de onde vem."},{"k":15,"t":"escolha","p":"Em '
            '«as vidraças da igreja vistas de fora são o som da chuva ouvido por dentro», o que separa e junta o dentro e o fora da '
            'igreja?"},{"k":16,"t":"sublinhar","p":"Toca na forma do verbo «ver» e na forma do verbo '
            '«ouvir»."},{"k":18,"t":"escolha","p":"«A missa é um automóvel que passa»: que dois planos se cruzam neste '
            'verso?"},{"k":19,"t":"versos","p":"Ordena o final do poema II, do vento à chuva que '
            'cessa."},{"k":21,"t":"emparelhar","p":"Liga cada coisa ao plano onde nasce."},{"k":23,"t":"vf","p":"«Chuva Oblíqua» foi '
            'publicada no segundo número da revista _Orpheu_, em 1915."},{"k":24,"t":"vf","p":"«Poemas interseccionistas» são poemas em '
            'que duas realidades se cruzam no mesmo verso."},{"k":25,"t":"ordenar","p":"O percurso de «Chuva Oblíqua», I e II, pela ordem '
            'do texto:"},{"k":26,"t":"frase","p":"Põe por ordem o verso em que os navios atravessam as '
            'árvores."},{"k":28,"t":"escolha","p":"Na parte VI ouvida no vídeo, que dois planos se '
            'cruzam?"},{"k":29,"t":"escolha","p":"«Todo o teatro é o meu quintal»: qual é a interpretação mais bem apoiada pelo '
            'verso?"},{"k":30,"t":"escolha","p":"Compara I e VI: «os navios […] são estas árvores» e «Todo o teatro é o meu quintal». O '
            'que aproxima estes versos?"}]',
  'novo': '[{"k":3,"t":"versos","p":"Põe os versos da primeira estrofe do poema I pela ordem do poema."},{"k":4,"t":"sublinhar","p":"Toca '
          'na palavra que nomeia o lugar que o poeta vê e na que nomeia o lugar que ele sonha."},{"k":5,"t":"emparelhar","p":"Liga cada '
          'verso ao plano em que está."},{"k":7,"t":"completar","p":"«Liberto em duplo»: como se sente o poeta, e em que se torna o '
          'cais?"},{"k":8,"t":"escolha","p":"No verso «os navios passam por dentro dos troncos das árvores», que leitura justifica a '
          'aproximação à dupla exposição?"},{"k":9,"t":"vf","p":"Em «Com uma horizontalidade vertical», o poeta engana-se nas '
          'palavras."},{"k":11,"t":"escolha","p":"Que palavra do poema I quer dizer «fila, fileira»?"},{"k":13,"t":"completar","p":"No '
          'poema II, a vela de dentro diz-se com uma coisa de fora. Completa."},{"k":14,"t":"emparelhar","p":"Liga cada pedaço do poema II '
          'ao lugar de onde vem."},{"k":15,"t":"escolha","p":"Em «as vidraças da igreja vistas de fora são o som da chuva ouvido por '
          'dentro», o que separa e junta o dentro e o fora da igreja?"},{"k":16,"t":"sublinhar","p":"Toca na forma do verbo «ver» e na '
          'forma do verbo «ouvir»."},{"k":18,"t":"escolha","p":"«A missa é um automóvel que passa»: que dois planos se cruzam neste '
          'verso?"},{"k":19,"t":"versos","p":"Ordena o final do poema II, do vento à chuva que cessa."},{"k":21,"t":"emparelhar","p":"Liga '
          'cada coisa ao plano onde nasce."},{"k":23,"t":"vf","p":"«Chuva Oblíqua» foi publicada no segundo número da revista _Orpheu_, em '
          '1915."},{"k":24,"t":"vf","p":"«Poemas interseccionistas» são poemas em que duas realidades se cruzam no mesmo '
          'verso."},{"k":25,"t":"ordenar","p":"O percurso de «Chuva Oblíqua», I e II, pela ordem do texto:"},{"k":26,"t":"frase","p":"Põe '
          'por ordem o verso em que os navios atravessam as árvores."},{"k":28,"t":"escolha","p":"Na parte VI ouvida no vídeo, que dois '
          'planos se cruzam?"},{"k":29,"t":"escolha","p":"«Todo o teatro é o meu quintal»: qual é a interpretação mais bem apoiada pelo '
          'verso?"},{"k":30,"t":"escolha","p":"Compara I e VI: «os navios […] são estas árvores» e «Todo o teatro é o meu quintal». O que '
          'aproxima estes versos?"}]',
  'ocorrencias': 1,
  'achado': '01/11/2026: sincronizar com a camada, depois do #144 e do #145'},
 {'ficheiro': 'm8/painel-m8-f12/index.html',
  'local': 'M8-F12 painel: CARTOES',
  'antigo': '[{"k":3,"t":"emparelhar","p":"Liga cada traço ao género a que pertence."},{"k":4,"t":"completar","p":"O que perguntam as '
            'lentes do contemporâneo e da tradição?"},{"k":5,"t":"completar","p":"O que perguntam as lentes das figurações e da arte '
            'poética?"},{"k":6,"t":"escolha","p":"«As Palavras» termina com perguntas sem resposta; «George» apresenta o encontro com '
            'outras idades da protagonista. Qual das comparações respeita os dois textos?"},{"k":7,"t":"escolha","p":"Que lente usas para '
            'perguntar o que «Prece no Mediterrâneo» vai buscar aos Evangelhos?"},{"k":8,"t":"escolha","p":"Que leitura se destaca em '
            '«Todas as manhãs, relia a carta»?"},{"k":9,"t":"vf","p":"Em «A poeta conversou com a editora. Ela levou o manuscrito», «Ela» '
            'identifica com certeza qual das duas levou o manuscrito."},{"k":11,"t":"sublinhar","p":"Na hipótese «preferem sugerir a '
            'explicar», toca nas três palavras que indicam o que fica por interpretar."},{"k":12,"t":"ordenar","p":"Como se constrói a '
            'resposta de desenvolvimento, por ordem:"},{"k":13,"t":"escolha","p":"Que termo nomeia a característica do conto de ser '
            'curto?"},{"k":14,"t":"emparelhar","p":"Liga cada autor ao texto que leste no módulo."},{"k":15,"t":"vf","p":"A resposta de '
            'desenvolvimento da revisão tem 60 a 80 palavras."},{"k":16,"t":"vf","p":"A revisão do módulo vem antes da prova de '
            'recuperação e das tarefas."},{"k":17,"t":"emparelhar","p":"Liga cada frase à leitura aspetual que nela se '
            'destaca."},{"k":18,"t":"vf","p":"A lente da arte poética pergunta se o poema fala da própria '
            'poesia."},{"k":19,"t":"completar","p":"Como tornas claro que foi a editora a levar o '
            'manuscrito?"},{"k":20,"t":"frase","p":"Põe por ordem a pergunta da lente do contemporâneo."}]',
  'novo': '[{"k":3,"t":"emparelhar","p":"Liga cada traço ao género a que pertence."},{"k":4,"t":"completar","p":"O que perguntam as lentes '
          'do contemporâneo e da tradição?"},{"k":5,"t":"completar","p":"O que perguntam as lentes das figurações e da arte '
          'poética?"},{"k":6,"t":"escolha","p":"«As Palavras» termina com perguntas sem resposta; «George» apresenta o encontro com outras '
          'idades da protagonista. Qual das comparações respeita os dois textos?"},{"k":7,"t":"escolha","p":"Que lente usas para perguntar '
          'o que «Prece no Mediterrâneo» vai buscar aos Evangelhos?"},{"k":8,"t":"escolha","p":"Exemplo criado: Todas as manhãs, relia a '
          'carta. Que valor aspetual destaca a expressão inicial?"},{"k":9,"t":"vf","p":"Em «A poeta conversou com a editora. Ela levou o '
          'manuscrito», «Ela» identifica com certeza qual das duas levou o manuscrito."},{"k":11,"t":"sublinhar","p":"Na hipótese '
          '«preferem sugerir a explicar», toca nas três palavras que indicam o que fica por interpretar."},{"k":12,"t":"ordenar","p":"Como '
          'se constrói a resposta de desenvolvimento, por ordem:"},{"k":13,"t":"escolha","p":"Que termo nomeia a característica do conto '
          'de ser curto?"},{"k":14,"t":"emparelhar","p":"Liga cada autor ao texto que leste no módulo."},{"k":15,"t":"vf","p":"A resposta '
          'de desenvolvimento da revisão tem 60 a 80 palavras."},{"k":16,"t":"escolha","p":"Exemplo criado: um poema retoma uma oração e '
          'muda o pedido final. Que pergunta recupera a lente da tradição?"},{"k":17,"t":"emparelhar","p":"Liga cada frase à leitura '
          'aspetual que nela se destaca."},{"k":18,"t":"vf","p":"A lente da arte poética pergunta se o poema fala da própria '
          'poesia."},{"k":19,"t":"completar","p":"Como tornas claro que foi a editora a levar o manuscrito?"},{"k":20,"t":"frase","p":"Põe '
          'por ordem a pergunta da lente do contemporâneo."}]',
  'ocorrencias': 1,
  'achado': '01/11/2026: sincronizar com a camada, depois do #144 e do #145'},
 {'ficheiro': 'm4/painel-m4-f01/index.html',
  'local': 'M4-F01 painel: seletor',
  'antigo': '<select data-r-k><option value="2">Porque não escolhe António nenhuma destas saídas?</option><option value="4">Caso '
            'imaginário: a direção ignora as queixas da delegada de turma. Que faria António?</option><option value="7">Mais à frente, '
            'Vieira repreende o peixe-voador, de barbatanas como asas. Lido como alegoria, que homem pode ele ser?</option><option '
            'value="9">Que papel tem cada coisa, na história de António e na de Vieira?</option><option value="10">Porque conta Vieira que '
            'os peixes ouviam assim?</option><option value="11">Caso imaginário: o jornal da escola só fala de um aquário, mas todos '
            'percebem que é a escola. Que é?</option><option value="13">Caso imaginário: um discurso de fim de curso abre com uma história '
            'do primeiro dia. Que parte é essa?</option><option value="15">Que fim serve cada passo do cap. I: ensinar, deleitar ou '
            'comover?</option></select>',
  'novo': '<select data-r-k><option value="2">Porque não escolhe António nenhuma destas saídas?</option><option value="4">Caso imaginário: '
          'a direção ignora as queixas da delegada de turma. Que faria António?</option><option value="7">Mais à frente, Vieira repreende '
          'o peixe-voador, de barbatanas como asas. Lido como alegoria, que homem pode ele ser?</option><option value="9">Que papel tem '
          'cada coisa, na história de António e na de Vieira?</option><option value="10">Que contraste responde melhor à pergunta de '
          'abertura: por que razão fala Vieira aos peixes?</option><option value="11">Caso imaginário: o jornal da escola só fala de um '
          'aquário, mas todos percebem que é a escola. Que é?</option><option value="13">Caso imaginário: um discurso de fim de curso abre '
          'com uma história do primeiro dia. Que parte é essa?</option><option value="15">Que fim serve cada passo do cap. I: ensinar, '
          'deleitar ou comover?</option></select>',
  'ocorrencias': 1,
  'achado': '01/11/2026: manter o seletor do painel coerente com CARTOES'},
 {'ficheiro': 'm6/painel-m6-f01/index.html',
  'local': 'M6-F01 painel: seletor',
  'antigo': '<select data-r-k><option value="4">Quem fala em «O Palacio da Ventura» e o que se sonha?</option><option value="5">Toca nas '
            'três palavras repetidas que fazem a anáfora do verso.</option><option value="6">Que palavra do soneto quer dizer '
            '«ansioso»?</option><option value="7">A primeira quadra termina com «O palacio encantado da Ventura!».</option><option '
            'value="8">Toca nos dois adjetivos que dizem o estado do cavaleiro.</option><option value="9">Que armas do cavaleiro estão '
            'desfeitas na segunda quadra?</option><option value="10">«E eis que subito o avisto, fulgurante»: o que avista o '
            'cavaleiro?</option><option value="11">Põe os versos do primeiro terceto pela ordem do soneto.</option><option value="12">«Eu '
            'sou o Vagabundo, o Desherdado...»: quem o brada e a quem?</option><option value="14">As portas de ouro abrem-se devagar e em '
            'silêncio.</option><option value="15">O que encontra o cavaleiro quando as portas de ouro se abrem?</option><option '
            'value="16">Que recurso opõe «fulgurante» (v. 7) a «Silencio e escuridão» (v. 14)?</option><option value="18">A chave de ouro '
            'deste soneto está na primeira quadra, em «busco anhelante».</option><option value="19">Liga cada elemento da alegoria ao que '
            'representa.</option><option value="20">Como se organizam as estrofes de «O Palacio da Ventura»?</option><option value="21">Os '
            'quatro tempos do soneto, por ordem:</option><option value="22">Põe por ordem o primeiro verso do último '
            'terceto.</option></select>',
  'novo': '<select data-r-k><option value="4">Quem fala em «O Palacio da Ventura» e o que se sonha?</option><option value="5">Toca nas '
          'três palavras repetidas que fazem a anáfora do verso.</option><option value="6">Que palavra do soneto quer dizer '
          '«ansioso»?</option><option value="7">A primeira quadra termina com «O palacio encantado da Ventura!».</option><option '
          'value="8">Toca nos dois adjetivos que dizem o estado do cavaleiro.</option><option value="9">Que armas do cavaleiro estão '
          'desfeitas na segunda quadra?</option><option value="10">«E eis que subito o avisto, fulgurante»: o que avista o '
          'cavaleiro?</option><option value="11">Põe os versos do primeiro terceto pela ordem do soneto.</option><option value="12">«Eu '
          'sou o Vagabundo, o Desherdado...»: quem o brada e a quem?</option><option value="14">As portas de ouro abrem-se devagar e em '
          'silêncio.</option><option value="15">O cavaleiro vê abrirem-se as portas de ouro, mas encontra o vazio. Que pergunta ajuda a '
          'explicar esta mudança?</option><option value="16">Que recurso opõe «fulgurante» (v. 7) a «Silencio e escuridão» (v. '
          '14)?</option><option value="18">A chave de ouro deste soneto está na primeira quadra, em «busco anhelante».</option><option '
          'value="19">Liga cada elemento da alegoria ao que representa.</option><option value="20">Como se organizam as estrofes de «O '
          'Palacio da Ventura»?</option><option value="21">Os quatro tempos do soneto, por ordem:</option><option value="22">Põe por ordem '
          'o primeiro verso do último terceto.</option></select>',
  'ocorrencias': 1,
  'achado': '01/11/2026: manter o seletor do painel coerente com CARTOES'},
 {'ficheiro': 'm7/painel-m7-f34/index.html',
  'local': 'M7-F34 painel: seletor',
  'antigo': '<select data-r-k><option value="3">Põe os versos da primeira estrofe do poema I pela ordem do poema.</option><option '
            'value="4">Toca na palavra que nomeia o lugar que o poeta vê e na que nomeia o lu</option><option value="5">Liga cada verso ao '
            'plano em que está.</option><option value="7">«Liberto em duplo»: como se sente o poeta, e em que se torna o '
            'cais?</option><option value="8">No cinema, a «dupla exposição» mostra duas imagens no mesmo sítio, uma</option><option '
            'value="9">Em «Com uma horizontalidade vertical», o poeta engana-se nas palavras.</option><option value="11">Que palavra do '
            'poema I quer dizer «fila, fileira»?</option><option value="13">No poema II, a vela de dentro diz-se com uma coisa de fora. '
            'Completa.</option><option value="14">Liga cada pedaço do poema II ao lugar de onde vem.</option><option value="15">Em «as '
            'vidraças da igreja vistas de fora são o som da chuva ouvido por</option><option value="16">Toca na forma do verbo «ver» e na '
            'forma do verbo «ouvir».</option><option value="18">«A missa é um automóvel que passa»: que dois planos se cruzam neste '
            've</option><option value="19">Ordena o final do poema II, do vento à chuva que cessa.</option><option value="21">Liga cada '
            'coisa ao plano onde nasce.</option><option value="23">«Chuva Oblíqua» foi publicada no segundo número da revista '
            '<i>Orpheu</i>, e</option><option value="24">«Poemas interseccionistas» são poemas em que duas realidades se '
            'cruzam</option><option value="25">O percurso de «Chuva Oblíqua», I e II, pela ordem do texto:</option><option value="26">Põe '
            'por ordem o verso em que os navios atravessam as árvores.</option><option value="28">Na parte VI ouvida no vídeo, que dois '
            'planos se cruzam?</option><option value="29">«Todo o teatro é o meu quintal»: qual é a interpretação mais bem '
            'apoia</option><option value="30">Compara I e VI: «os navios […] são estas árvores» e «Todo o teatro é o</option></select>',
  'novo': '<select data-r-k><option value="3">Põe os versos da primeira estrofe do poema I pela ordem do poema.</option><option '
          'value="4">Toca na palavra que nomeia o lugar que o poeta vê e na que nomeia o lugar que ele sonha.</option><option '
          'value="5">Liga cada verso ao plano em que está.</option><option value="7">«Liberto em duplo»: como se sente o poeta, e em que '
          'se torna o cais?</option><option value="8">No verso «os navios passam por dentro dos troncos das árvores», que leitura '
          'justifica a aproximação à dupla exposição?</option><option value="9">Em «Com uma horizontalidade vertical», o poeta engana-se '
          'nas palavras.</option><option value="11">Que palavra do poema I quer dizer «fila, fileira»?</option><option value="13">No poema '
          'II, a vela de dentro diz-se com uma coisa de fora. Completa.</option><option value="14">Liga cada pedaço do poema II ao lugar '
          'de onde vem.</option><option value="15">Em «as vidraças da igreja vistas de fora são o som da chuva ouvido por dentro», o que '
          'separa e junta o dentro e o fora da igreja?</option><option value="16">Toca na forma do verbo «ver» e na forma do verbo '
          '«ouvir».</option><option value="18">«A missa é um automóvel que passa»: que dois planos se cruzam neste verso?</option><option '
          'value="19">Ordena o final do poema II, do vento à chuva que cessa.</option><option value="21">Liga cada coisa ao plano onde '
          'nasce.</option><option value="23">«Chuva Oblíqua» foi publicada no segundo número da revista _Orpheu_, em 1915.</option><option '
          'value="24">«Poemas interseccionistas» são poemas em que duas realidades se cruzam no mesmo verso.</option><option value="25">O '
          'percurso de «Chuva Oblíqua», I e II, pela ordem do texto:</option><option value="26">Põe por ordem o verso em que os navios '
          'atravessam as árvores.</option><option value="28">Na parte VI ouvida no vídeo, que dois planos se cruzam?</option><option '
          'value="29">«Todo o teatro é o meu quintal»: qual é a interpretação mais bem apoiada pelo verso?</option><option '
          'value="30">Compara I e VI: «os navios […] são estas árvores» e «Todo o teatro é o meu quintal». O que aproxima estes '
          'versos?</option></select>',
  'ocorrencias': 1,
  'achado': '01/11/2026: manter o seletor do painel coerente com CARTOES'},
 {'ficheiro': 'm8/painel-m8-f12/index.html',
  'local': 'M8-F12 painel: seletor',
  'antigo': '<select data-r-k><option value="3">Liga cada traço ao género a que pertence.</option><option value="4">O que perguntam as '
            'lentes do contemporâneo e da tradição?</option><option value="5">O que perguntam as lentes das figurações e da arte '
            'poética?</option><option value="6">«As Palavras» termina com perguntas sem resposta; «George» apresenta o encontro com outras '
            'idades da protagonista. Qual das comparações respeita os dois textos?</option><option value="7">Que lente usas para perguntar '
            'o que «Prece no Mediterrâneo» vai buscar aos Evangelhos?</option><option value="8">Que leitura se destaca em «Todas as '
            'manhãs, relia a carta»?</option><option value="9">Em «A poeta conversou com a editora. Ela levou o manuscrito», «Ela» '
            'identifica com certeza qual das duas levou o manuscrito.</option><option value="11">Na hipótese «preferem sugerir a '
            'explicar», toca nas três palavras que indicam o que fica por interpretar.</option><option value="12">Como se constrói a '
            'resposta de desenvolvimento, por ordem:</option><option value="13">Que termo nomeia a característica do conto de ser '
            'curto?</option><option value="14">Liga cada autor ao texto que leste no módulo.</option><option value="15">A resposta de '
            'desenvolvimento da revisão tem 60 a 80 palavras.</option><option value="16">A revisão do módulo vem antes da prova de '
            'recuperação e das tarefas.</option><option value="17">Liga cada frase à leitura aspetual que nela se destaca.</option><option '
            'value="18">A lente da arte poética pergunta se o poema fala da própria poesia.</option><option value="19">Como tornas claro '
            'que foi a editora a levar o manuscrito?</option><option value="20">Põe por ordem a pergunta da lente do '
            'contemporâneo.</option></select>',
  'novo': '<select data-r-k><option value="3">Liga cada traço ao género a que pertence.</option><option value="4">O que perguntam as '
          'lentes do contemporâneo e da tradição?</option><option value="5">O que perguntam as lentes das figurações e da arte '
          'poética?</option><option value="6">«As Palavras» termina com perguntas sem resposta; «George» apresenta o encontro com outras '
          'idades da protagonista. Qual das comparações respeita os dois textos?</option><option value="7">Que lente usas para perguntar o '
          'que «Prece no Mediterrâneo» vai buscar aos Evangelhos?</option><option value="8">Exemplo criado: Todas as manhãs, relia a '
          'carta. Que valor aspetual destaca a expressão inicial?</option><option value="9">Em «A poeta conversou com a editora. Ela levou '
          'o manuscrito», «Ela» identifica com certeza qual das duas levou o manuscrito.</option><option value="11">Na hipótese «preferem '
          'sugerir a explicar», toca nas três palavras que indicam o que fica por interpretar.</option><option value="12">Como se constrói '
          'a resposta de desenvolvimento, por ordem:</option><option value="13">Que termo nomeia a característica do conto de ser '
          'curto?</option><option value="14">Liga cada autor ao texto que leste no módulo.</option><option value="15">A resposta de '
          'desenvolvimento da revisão tem 60 a 80 palavras.</option><option value="16">Exemplo criado: um poema retoma uma oração e muda o '
          'pedido final. Que pergunta recupera a lente da tradição?</option><option value="17">Liga cada frase à leitura aspetual que nela '
          'se destaca.</option><option value="18">A lente da arte poética pergunta se o poema fala da própria poesia.</option><option '
          'value="19">Como tornas claro que foi a editora a levar o manuscrito?</option><option value="20">Põe por ordem a pergunta da '
          'lente do contemporâneo.</option></select>',
  'ocorrencias': 1,
  'achado': '01/11/2026: manter o seletor do painel coerente com CARTOES'}]

# 01/11/2026: P1 passa do C08 para o C16, depois da segunda parte do poema.
LIMITE_149_20261101 = frozenset([('docs/pedagogia/aquecimentos/m4-u1.json', 'A-M4 fonte do gerador'), ('exame/provas/2026-1f/grupo-i/index.html', 'E-2026-I C34'), ('m1/licao-m1-f20/index.html', 'M1-F20 C14'), ('m4/aulas/aula-01/index.html', 'M4 guião: C11 no núcleo'), ('m4/aulas/aula-01/index.html', 'M4 guião: C11 sai do complemento'), ('m4/aulas/aula-01/index.html', 'M4 guião: complementos'), ('m4/aulas/aula-01/index.html', 'M4 guião: contagem'), ('m4/aulas/aula-01/index.html', 'M4 guião: fecho 13'), ('m4/aulas/aula-01/index.html', 'M4 guião: leitura e produção'), ('m4/aulas/aula-01/index.html', 'M4 guião: lista de 13'), ('m4/aulas/aula-01/index.html', 'M4 guião: pergunta do arco'), ('m4/aulas/aula-01/index.html', 'M4 guião: turma no cartão 11'), ('m4/index.html', 'M4 prova: peça de fecho'), ('m4/index.html', 'M4 unidade 1: prova esperada'), ('m4/index.html', 'M4 unidade 2: prova esperada'), ('m4/index.html', 'M4 unidade 3: prova esperada'), ('m4/licao-m4-f01/index.html', 'M4-F01 C11'), ('m4/licao-m4-f01/index.html', 'M4-F01 C18'), ('m4/painel-m4-f01/index.html', 'M4-F01 painel: CARTOES'), ('m4/painel-m4-f01/index.html', 'M4-F01 painel: seletor'), ('m4/recursos/tpc-entrada.js', 'M4-F28 C03'), ('m4/recursos/tpc-entrada.js', 'M4-F28 C05'), ('m6/licao-m6-f01/index.html', 'M6-F01 C16'), ('m6/painel-m6-f01/index.html', 'M6-F01 painel: CARTOES'), ('m6/painel-m6-f01/index.html', 'M6-F01 painel: seletor'), ('m7/licao-m7-f34/index.html', 'M7-F34 C09'), ('m7/licao-m7-f34/index.html', 'M7-F34 C31'), ('m7/painel-m7-f34/index.html', 'M7-F34 painel: CARTOES'), ('m7/painel-m7-f34/index.html', 'M7-F34 painel: seletor'), ('m8/licao-m8-f12/index.html', 'M8-F12 C09'), ('m8/licao-m8-f12/index.html', 'M8-F12 C17'), ('m8/licao-m8-f12/index.html', 'M8-F12 C22'), ('m8/painel-m8-f12/index.html', 'M8-F12 painel: CARTOES'), ('m8/painel-m8-f12/index.html', 'M8-F12 painel: seletor'), ('m9/painel-m9-f13/index.html', 'M9 medição: impressão e noindex'), ('m9/painel-m9-f13/index.html', 'M9 medição: procedimento e rubrica'), ('m9/recursos/f13.js', 'M9-F13 C02'), ('m9/recursos/f13.js', 'M9-F13 C10'), ('m9/recursos/f13.js', 'M9-F13 C21'), ('m9/recursos/f13.js', 'M9-F13 C23'), ('scripts/provas/dados/2026-1f/grupo-i.json', 'E-2026-I fonte do gerador'), ('tarefas/m4-u1/aquecimento/index.html', 'A-M4 C05')])

# 01/11/2026: as cópias serão atualizadas juntamente com a lição, sem dispensar a comparação atual.
PENDENTES_DESAFIO_M8_20261101 = [
    ('m8/index.html', 'desafio U2: cópia de M8-F12 C09'),
]

# 01/11/2026: materiais gerados a refazer com a camada do #149 (não aceitam troca literal).
# 02/11/2026: reúne os achados 5/14/21; regenerar nas fontes quando C11 entrar no núcleo.
PENDENTES_MATERIAIS_149_20261101 = [
    ('m4/diapositivos/aula-01-f01.pdf', 'aula 1: 13 cartões; diapositivo do C11 «Que contraste responde melhor…» antes de «Agora, em papel»; «Para ir mais longe»: 3 cartões de pergunta e 2 de leitura, sem «Os peixes em ordem»'),
    ('m4/diapositivos/aula-01-f01.pptx', 'o mesmo que o PDF'),
    ('m4/aulas/guioes-m4.pdf', 'aula 1: «13 cartões na aula», lista de 13 e «Para ir mais longe: 3 cartões de pergunta e 2 de leitura», sem «Os peixes em ordem»'),
]

class Pendentes149(unittest.TestCase):
    def test_lista_apenas_diminui_e_trocas_nao_estao_aplicadas(self):
        ids=[(e['ficheiro'],e['local']) for e in PENDENTES_CAMADA_149_20261101]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(set(ids)<=LIMITE_149_20261101)
        texts={}
        for e in PENDENTES_CAMADA_149_20261101:
            with self.subTest(local=e['local']):
                s=texts.setdefault(e['ficheiro'],(ROOT/e['ficheiro']).read_text('utf-8'))
                self.assertNotEqual(e['antigo'],e['novo'])
                self.assertEqual(s.count(e['antigo']),e['ocorrencias'])
                self.assertNotIn(e['novo'],s,'Troca aplicada: retirar da lista pendente')
                texts[e['ficheiro']]=s.replace(e['antigo'],e['novo'])
        self.assertFalse((ROOT/'scripts/conteudos_lote1_20261101.json').exists())
        self.assertFalse((ROOT/'tests/fixtures/conteudos-lote1-edits-20261101.json').exists())

    def test_cartoes_corrigidos_sem_extras_e_opcoes_equilibradas(self):
        # 01/11/2026: contar também as certas mais longas, incluindo empates.
        shortest=0;longest=0;three=0
        for e in PENDENTES_CAMADA_149_20261101:
            if not re.fullmatch(r'(?:M[1-9]-F[0-9]+|A-M4|E-2026-I) C[0-9]+',e['local']):continue
            c=json.loads(e['novo']);before=json.loads(e['antigo'])
            self.assertNotEqual(c.get('p2',''),c.get('p','!'))
            if c['t']=='escolha':
                lengths=[len(re.sub('<[^>]+>','',s)) for s in c['o']]
                self.assertLessEqual(max(lengths),1.2*min(lengths),e['local'])
                self.assertEqual(len(c['fe']),len(c['o']))
                for i,f in enumerate(c['fe']):
                    if i!=c['c']:self.assertRegex(f,r'Relê|Revê|Volta|Procura|Compara')
                if len(lengths)==3:
                    three+=1;shortest+=lengths[c['c']]==min(lengths)
                    longest+=lengths[c['c']]==max(lengths)
            if c['t']!='ler':self.assertTrue(c.get('f'))
            self.assertEqual(c.get('mais'),before.get('mais')) if e['local']!='M4-F01 C11' else self.assertFalse(c.get('mais'))
        self.assertLessEqual(shortest*3,three)
        self.assertLessEqual(longest*3,three)

    def test_copias_m8_sem_isenções(self):
        # 01/11/2026: a cópia alterada é C09; C18 é a outra cópia e não muda.
        self.assertTrue(set(PENDENTES_DESAFIO_M8_20261101)<= {
            ('m8/index.html','desafio U2: cópia de M8-F12 C09')})
        source=(ROOT/'m8/index.html').read_text('utf-8')
        pool=[c for c in json.JSONDecoder().raw_decode(source.split('var U=',1)[1])[0][1]['pool'] if c.get('_l')=='m8-f12']
        for _,label in PENDENTES_DESAFIO_M8_20261101:
            local=label.split('cópia de ')[1]
            e=next(e for e in PENDENTES_CAMADA_149_20261101 if e['local']==local)
            self.assertTrue(any(c['p']==json.loads(e['antigo'])['p'] for c in pool),'Cópia inexistente no desafio: retirar o pendente')
            self.assertNotIn(json.loads(e['novo'])['p'],source,'Cópia corrigida: retirar o pendente')

    # 01/11/2026: proteger a serialização dos geradores e os materiais ainda por regenerar.
    def test_json_das_paginas_geradas(self):
        for e in PENDENTES_CAMADA_149_20261101:
            if '/aquecimento/' in e['ficheiro'] or e['ficheiro'].startswith('exame/provas/'):
                self.assertEqual(e['novo'],json.dumps(json.loads(e['novo']),ensure_ascii=False),e['local'])

    def test_materiais_pendentes_apenas_diminuem_e_existem(self):
        limite=frozenset([
            ('m4/diapositivos/aula-01-f01.pdf', 'aula 1: 13 cartões; diapositivo do C11 «Que contraste responde melhor…» antes de «Agora, em papel»; «Para ir mais longe»: 3 cartões de pergunta e 2 de leitura, sem «Os peixes em ordem»'),
            ('m4/diapositivos/aula-01-f01.pptx', 'o mesmo que o PDF'),
            ('m4/aulas/guioes-m4.pdf', 'aula 1: «13 cartões na aula», lista de 13 e «Para ir mais longe: 3 cartões de pergunta e 2 de leitura», sem «Os peixes em ordem»'),
        ])
        self.assertEqual(len(PENDENTES_MATERIAIS_149_20261101),len(set(PENDENTES_MATERIAIS_149_20261101)))
        self.assertTrue(set(PENDENTES_MATERIAIS_149_20261101)<=limite)
        for path,_ in PENDENTES_MATERIAIS_149_20261101:self.assertTrue((ROOT/path).is_file(),path)

    # 01/11/2026: a aplicação futura conserva os seletores k/t/p dos painéis e a ordem de leitura do M6.
    def test_paineis_pendentes_correspondem_as_licoes(self):
        for e in PENDENTES_CAMADA_149_20261101:
            if not e['local'].endswith('painel: CARTOES'):continue
            lesson=e['local'].split()[0];cards=json.loads(e['novo'])
            for change in PENDENTES_CAMADA_149_20261101:
                if re.fullmatch(lesson+r' C\d+',change['local']):
                    c=json.loads(change['novo']);k=int(change['local'].split(' C')[1])-1
                    if c['t']=='ler':continue
                    self.assertEqual(next(x for x in cards if x['k']==k),{'k':k,'t':c['t'],'p':c['p']})
        e=next(e for e in PENDENTES_CAMADA_149_20261101 if e['local']=='M6-F01 C16')
        before=json.loads(e['antigo']);after=json.loads(e['novo'])
        self.assertEqual(after['g'],2)
        self.assertEqual((after['cita'],after['l']),(before['cita'],before['l']))
        self.assertFalse(any(e['local']=='M6-F01 C08' for e in PENDENTES_CAMADA_149_20261101))

if __name__=='__main__':unittest.main()
