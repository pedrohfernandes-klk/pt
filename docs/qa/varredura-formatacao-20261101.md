# Varredura de formatação do Português, 01/11/2026

Os 361 pontos foram cruzados com os ficheiros alterados pelos pedidos #143 a #151, incluindo as dependências de cada ramo, em comparação com main. Resultado: 239 pontos corrigidos, 13 já conformes e 109 adiados. A classificação completa, os commits consultados e a lista dos ficheiros protegidos estão em `varredura-formatacao-20261101.json`.

Nenhum ficheiro com um ponto adiado recebe uma correção editorial. A infraestrutura de verificação recebe apenas o registo da camada, a comparação com os predecessores e a adaptação dos testes à apresentação corrigida e ao Windows. As camadas anteriores não são reescritas. Não há mudança de chaves de progresso, de respostas certas, de ordem ou de quantidade de cartões.

A camada é `scripts/varredura_formatacao_20261101.json`; o manifesto reversível é `tests/fixtures/varredura-formatacao-edits-20261101.json`. Os títulos do exame passam a ser apresentados em itálico com escape de HTML. Os seletores nativos mantêm texto simples; a apresentação do cartão recebe o itálico.

## Critérios e fontes conferidas

Os títulos de livros e peças levam itálico. «O Sentimento dum Ocidental» é um poema e conserva as aspas. O Largo Amor de Perdição é um lugar; em «Os Maias vieram habitar», o nome designa a família. Os separadores de glossário passam a dois pontos; nas frases de ligação usa-se a pontuação pedida pela sintaxe. As barras entre versos passam a quebras de linha; os parágrafos de estrofe mantêm-se.

Fontes consultadas para as quebras de verso e os créditos:

* [João Garcia de Guilhade, Cantigas Medievais Galego-Portuguesas](https://cantigas.fcsh.unl.pt/cantiga.asp?cdcant=1520): quebra depois de «queixar».
* [Mendinho, Cantigas Medievais Galego-Portuguesas](https://cantigas.fcsh.unl.pt/cantiga.asp?cdcant=861): versos e refrão.
* [Gil Vicente, Farsa de Inês Pereira](https://pt.wikisource.org/wiki/Farsa_de_In%C3%AAs_Pereira): pares de versos citados.
* [Gil Vicente, O Fidalgo](https://pt.wikisource.org/wiki/Auto_da_Barca_do_Inferno/O_Fidalgo) e [O Sapateiro](https://pt.wikisource.org/wiki/Auto_da_Barca_do_Inferno/O_Sapateiro): falas em verso, mantendo a grafia das citações existentes.
* Camões, [IV, 95](https://oslusiadas.org/iv/95.html), [VIII, 98](https://oslusiadas.org/viii/98.html) e [IX, 89](https://oslusiadas.org/ix/89.html): também se separaram «Honras […]» e «Estes», que pertencem a versos diferentes.
* [Cesário Verde, O Livro de Cesário Verde, Project Gutenberg 8698](https://www.gutenberg.org/cache/epub/8698/pg8698-images.html): versos e estrofes de «O Sentimento dum Ocidental».
* [Retrato de Pessoa com chapéu, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:PessoaChapeu.jpg): fotografia vista; a fonte não identifica o fotógrafo nem a instituição depositária do original. A data é apresentada como cerca de 1914, com a dúvida da descrição. A tabela declara estas lacunas e o domínio público indicado pela fonte, sem inventar uma atribuição. A mesma reprodução já estava nas três páginas corrigidas; não se acrescentam imagens.

Não se aumenta nenhum excerto protegido. As correções de versos elegíveis são de obras em domínio público.

## Aplicação por módulo

As descrições abaixo localizam o achado original. O manifesto contém o antes e depois integral de cada troca, sem abreviações. «Conforme» corrige a classificação da varredura, não o texto da página.

### M1

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V001 | `m1/gram-coordenadas/index.html`; Dados E / passos[1].html | B. «fostes-vos queixar que vos nunca louv'en[o] meu cantar; / ⟪mais⟫ ora quero fazer um cantar» (Guilhade) | Três frases de há setecentos anos, com uma palavra pequena a ligar duas orações:A. «Nom hei [eu i] barqueiro nem sei remar.» (Mendinho)B. «fostes-vos queixar ↵ … |
| V009 | `m1/flores-verde-pino/index.html`; Dados E / passos[1].html | u é? — onde está? · pino — pinheiro · pôs conmigo — combinou comigo · preguntades — perguntais · vosco — convosco · ant'o prazo saído — antes de acabar o prazo | Uma rapariga pergunta às flores do pinheiro pelo amigo. E as flores respondem.— Ai flores, ai flores do verde pino, ↵ se sabedes novas do meu amigo? ↵ Ai Deus, … |
| V010 | `m1/gram-complementos/index.html`; Dados E / passos[1].html | complemento — o que uma palavra exige para o seu sentido ficar completo · modificador — o que se junta a uma palavra sem ser exigido | Três constituintes da Crónica de D. João I, cada um a completar uma palavra diferente:A. «fosse repartida a guarda dos muros» (cap. 115)B. «outras desacostumada… |
| V011 | `m1/gram-coordenadas/index.html`; Dados E / emblemas[1][3] | Distingues somar, opor e concluir — e mostraste em cada caso que nenhuma oração está dentro da outra. | Distingues somar, opor e concluir, e mostraste em cada caso que nenhuma oração está dentro da outra. |
| V012 | `m1/gram-coordenadas/index.html`; Dados E / passos[1].html | nem — e não · mais — mas · Duas orações estão coordenadas quando se ligam sem que nenhuma esteja dentro da outra. | Três frases de há setecentos anos, com uma palavra pequena a ligar duas orações:A. «Nom hei [eu i] barqueiro nem sei remar.» (Mendinho)B. «fostes-vos queixar ↵ … |
| V013 | `m1/gram-fonologia/index.html`; Dados E / passos[1].html | Desaparece — ASA: início, aférese (alevantada > levantada: vogal inicial); interior, síncope (malu > mau: [l]); fim, apócope (amare > amar: vogal final). | Três palavras que lês nas cantigas, e de onde vêm:A. «lua» vem do latim luna («Ondas do mar de Vigo» diz «amigo»; a cantiga de D. Dinis fala das flores; a lua e… |
| V014 | `m1/gram-fonologia/index.html`; Dados E / passos[1].html | Entra — PEP: início, prótese (scribere > escrever: vogal inicial); interior, epêntese (humile > humilde: [d]); fim, paragoge (ante > antes: consoante final). | Três palavras que lês nas cantigas, e de onde vêm:A. «lua» vem do latim luna («Ondas do mar de Vigo» diz «amigo»; a cantiga de D. Dinis fala das flores; a lua e… |
| V015 | `m1/gram-fonologia/index.html`; Dados E / passos[1].html | processo fonológico — uma mudança regular de sons, do latim ao português · síncope — cai um som no meio · sonorização — um som surdo (p, t, c) passa a sonoro (b… | Três palavras que lês nas cantigas, e de onde vêm:A. «lua» vem do latim luna («Ondas do mar de Vigo» diz «amigo»; a cantiga de D. Dinis fala das flores; a lua e… |
| V016 | `m1/guilhade-dona-fea/index.html`; Dados E / passos[1].html | loar — louvar · prez — valor · nom fal — não falta · comprida de bem — cheia de qualidades · fea — feia · sandia — louca · escárnio — diz mal com palavras cober… | A — D. Dinis louva a sua senhora à maneira dos trovadores da Provença:Quer'eu em maneira de proençal ↵ fazer agora um cantar d'amor ↵ e querrei muit'i loar mia … |
| V017 | `m1/guilhade-dona-fea/index.html`; Dados E / passos[3].opcoes[1][3] | Não sabemos se é, e não é isso que faz a troça: é o jogo com o género. | Não sabemos se é, e não é isso que faz a troça: é o contraste com o género. |
| V018 | `m1/lisboa-cercada/index.html`; Dados E / passos[1].html | bacinetes — capacetes · abastaria — bastaria · esgravatando — remexendo a terra · mantimento — alimento | Em 1384 o rei de Castela cerca Lisboa. Fernão Lopes mostra a cidade duas vezes.A — preparada: «Havia mais nestas torres muitas lanças d'armas, e bacinetes, e d'… |
| V019 | `m1/matam-o-mestre/index.html`; Dados E / passos[1].html | percebido — combinado · rijamente — com força · arruído — alvoroço · em logo de — em lugar de · hu — onde · escusar — evitar | Lisboa, 6 de dezembro de 1383. O Mestre de Avis acaba de matar o conde Andeiro nos paços da rainha. Estava combinado que o pajem gritaria pela cidade:«O pajem d… |
| V020 | `m1/mendinho-ermida/index.html`; Dados E / passos[1].html | sedia-m'eu — estava eu · cercarom-mi — cercaram-me · som — são · atendendo — esperando · nom hei i — não tenho ali · fremosa — formosa | Uma cantiga de amigo: quem fala é uma rapariga, sozinha numa ermida à beira-mar, à espera do namorado. Os parênteses retos são palavras acrescentadas pelos edit… |
| V021 | `m1/ondas-vigo/index.html`; Dados E / emblemas[2][3] | Já percebeste o jogo das repetições. Volta atrás e afina. | Já percebeste o efeito das repetições. Volta atrás e afina. |
| V022 | `m1/ondas-vigo/index.html`; Dados E / passos[1].html | levado — agitado · verrá — virá · cedo — em breve | Esta é uma cantiga de amigo: quem fala é uma rapariga, à espera do namorado que foi para o mar. Lê em voz alta, devagar.Ondas do mar de Vigo, ↵ se vistes meu am… |
| V023 | `m1/tempo-da-flor/index.html`; Dados E / passos[1].html | proençaes — trovadores da Provença · soem — costumam · mais — mas · coita — sofrimento de amor · levar — suportar | D. Dinis, rei e trovador, diz que os provençais só cantam o amor na primavera. Primeira estrofe:Proençaes soem mui bem trobar ↵ e dizem eles que é com amor; ↵ m… |

### M2

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V025 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | A. «Se vos eu vejo cantar / Eu vos farei assoviar» (o Escudeiro, casado) | Para dividir e dar nome a uma oração, faz sempre o mesmo: 1) sublinha os verbos: cada verbo conjugado é uma oração; 2) procura o conector («e», «que», «se», «po… |
| V026 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | B. «Já vos preguei as janelas, / Por que não vos ponhais nelas» (o Escudeiro) | Para dividir e dar nome a uma oração, faz sempre o mesmo: 1) sublinha os verbos: cada verbo conjugado é uma oração; 2) procura o conector («e», «que», «se», «po… |
| V027 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | C. «Quero tomar por esposo / Quem se tenha por ditoso» (Inês, viúva) | Para dividir e dar nome a uma oração, faz sempre o mesmo: 1) sublinha os verbos: cada verbo conjugado é uma oração; 2) procura o conector («e», «que», «se», «po… |
| V029 | `m2/licao-m2-f12/index.html`; Cartão 4: Uma credencial recusada / html | Anjo: «Não se embarca tirania / neste batel divinal.» | Fidalgo: «Sou fidalgo de solar, ↵ é bem que me recolhais.»Anjo: «Não se embarca tirania ↵ neste batel divinal.»Mais adiante, o Anjo associa a recusa ao desprezo… |
| V030 | `m2/licao-m2-f12/index.html`; Cartão 4: Uma credencial recusada / html | Fidalgo: «Sou fidalgo de solar, / é bem que me recolhais.» | Fidalgo: «Sou fidalgo de solar, ↵ é bem que me recolhais.»Anjo: «Não se embarca tirania ↵ neste batel divinal.»Mais adiante, o Anjo associa a recusa ao desprezo… |
| V031 | `m2/licao-m2-f13/index.html`; Cartão 2: Um ofício não é uma condenação / html | Diabo: «Tu roubaste bem trint’anos / o povo com teu mester.» | No cais das duas barcas, o Sapateiro chega com avental e formas do seu ofício. Procura evitar a barca infernal. O conflito da cena não é simplesmente trabalhar … |
| V032 | `m2/licao-m2-f13/index.html`; Cartão 2: Um ofício não é uma condenação / html | Sapateiro: «Como poderá isso ser, / confessado e comungado?!...» | No cais das duas barcas, o Sapateiro chega com avental e formas do seu ofício. Procura evitar a barca infernal. O conflito da cena não é simplesmente trabalhar … |
| V033 | `m2/licao-m2-f13/index.html`; Cartão 4: A resposta que muda o critério / html | Diabo: «Ouvir missa, então roubar, / é caminho per’aqui.» | Sapateiro: «Quantas missas eu ouvi, ↵ nom me hão elas de prestar?»Diabo: «Ouvir missa, então roubar, ↵ é caminho per’aqui.»O Sapateiro invoca a participação rel… |
| V034 | `m2/licao-m2-f13/index.html`; Cartão 4: A resposta que muda o critério / html | Sapateiro: «Quantas missas eu ouvi, / nom me hão elas de prestar?» | Sapateiro: «Quantas missas eu ouvi, ↵ nom me hão elas de prestar?»Diabo: «Ouvir missa, então roubar, ↵ é caminho per’aqui.»O Sapateiro invoca a participação rel… |
| V035 | `m2/gram-formacao/index.html`; Dados E / passos[1].html | derivação — formar uma palavra a partir de outra, com um afixo · prefixo — o afixo antes da base (des-, re-, in-) · sufixo — o afixo depois da base (-mento, -ei… | Três palavras do monólogo de Inês, desmontadas:A. «Oh Jesu! que enfadamento» — enfadar + -mentoB. «Me tire do cativeiro» — cativo + -eiroC. «Em poder de desfiad… |
| V036 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | coordenada — fica ao lado da outra, ligada por «e», «mas», «ou», «logo», «pois» · subordinada — ocupa um lugar dentro da outra: de tempo, condição, causa, fim; … | Para dividir e dar nome a uma oração, faz sempre o mesmo: 1) sublinha os verbos: cada verbo conjugado é uma oração; 2) procura o conector («e», «que», «se», «po… |
| V037 | `m2/guia-da-tarefa-m2/index.html`; Guia da tarefa | 1. Apreciação crítica da *Farsa de Inês Pereira* no teatroindividual; uma aula | Título da obra em itálico; título de poema entre «». |
| V038 | `m2/ines-escolhe/index.html`; Dados E / fontes[1][1] | Gil Vicente, *Farsa de Inês Pereira*, texto integral (Wikisource) | Título da obra em itálico; título de poema entre «». |
| V039 | `m2/ines-escolhe/index.html`; Dados E / marca | Ler a fundo · *Farsa de Inês Pereira* | Título da obra em itálico; título de poema entre «». |
| V040 | `m2/ines-escolhe/index.html`; Dados E / subtitulo | Gil Vicente, *Farsa de Inês Pereira*, 1523, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V041 | `m2/ines-escolher/index.html`; Dados E / emblemas[1][3] | Apanhaste a ironia e o jogo dos provérbios. | Apanhaste a ironia e o cruzamento dos provérbios. |
| V042 | `m2/ines-escolher/index.html`; Dados E / passos[1].html | siso mero — bom senso · folão — fogoso, indomável · Nero — imperador romano, símbolo de crueldade | Inês Pereira queria um marido «discreto», que soubesse tocar e falar bem. Casou com o escudeiro Brás da Mata, que a fechou em casa e a maltratou. Viúva, escolhe… |
| V043 | `m2/ines-panela/index.html`; Dados E / passos[1].html | lavrar — bordar · aviamento — arranjo de vida (aqui, casamento) · caramujo — caracol · bugia — macaca | Inês, fechada em casa a bordar, sozinha:Renego deste lavrar ↵ E do primeiro que o usou; ↵ Ó diabo que o eu dou, ↵ Que tão mau é d'aturar. ↵ Oh Jesu! que enfadam… |
| V045 | `m2/licao-m2-f12/index.html`; #baralho | EPI · Português. Leitura complementar vicentina; *Farsa de Inês Pereira* permanece o núcleo do módulo. Contextualização e exercícios nossos; recortes identifica… | Título da obra em itálico; título de poema entre «». |
| V046 | `m2/licao-m2-f13/index.html`; #baralho | EPI · Português. Leitura complementar vicentina; *Farsa de Inês Pereira* permanece o núcleo do módulo. Contextualização e exercícios nossos; recortes identifica… | Título da obra em itálico; título de poema entre «». |
| V048 | `m2/portefolio-do-modulo-m2/index.html`; A lista de verificação | Tarefa 1, «Apreciação crítica da *Farsa de Inês Pereira* no teatro»: o produto entregue (ou a ligação) e uma linha: o que fiz, o que corrigi depois da devolução… | Título da obra em itálico; título de poema entre «». |
| V049 | `m2/visita-farsa-de-ines-pereira-no-teatro/index.html`; A farsa em cena | *Farsa de Inês Pereira*, no teatro | Título da obra em itálico; título de poema entre «». |
| V050 | `m2/visita-farsa-de-ines-pereira-no-teatro/index.html`; Abertura | A farsa em cena: *Farsa de Inês Pereira*, no teatro | Título da obra em itálico; título de poema entre «». |

### M3

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V071 | `m3/gram-anafora/index.html`; Dados E / passos[1].html | A. «Este rende munidas fortalezas, / Faz tredores e falsos os amigos» (VIII, 98). Duas estâncias antes, o Poeta falou do «vil interesse e sede inimiga / Do dinh… | Uma palavra retoma outra quando aponta para algo que já foi dito. É a anáfora como processo de retoma: pronomes, demonstrativos, repetições, sinónimos.A. «Este … |
| V072 | `m3/gram-anafora/index.html`; Dados E / passos[1].html | B. «Que as Ninfas do Oceano, tão formosas, / Tétis e a ilha angélica pintada, / Outra coisa não é que as deleitosas / Honras […] Estes são os deleites desta ilh… | Uma palavra retoma outra quando aponta para algo que já foi dito. É a anáfora como processo de retoma: pronomes, demonstrativos, repetições, sinónimos.A. «Este … |
| V073 | `m3/arte-estima/index.html`; Dados E / passos[1].html | douto e ciente — culto e sábio · prezado — estimado · troncos nobres — linhagens · zebelinos — peles de zibelina (luxo) · forjado aço — armadura | A — Canto V, 97:Enfim, não houve forte capitão, ↵ Que não fosse também douto e ciente, ↵ Da Lácia, Grega, ou Bárbara nação, ↵ Senão da Portuguesa tão somente. ↵… |
| V074 | `m3/bicho-da-terra/index.html`; Dados E / passos[1].html | apercebida — à espreita · avorrecida — detestável · rende — faz render-se · tredores — traidores · deprava — corrompe | A — Canto I, 106:No mar tanta tormenta, e tanto dano, ↵ Tantas vezes a morte apercebida! ↵ Na terra tanta guerra, tanto engano, ↵ Tanta necessidade avorrecida! … |
| V075 | `m3/camoes-alma/index.html`; Dados E / passos[1].html | gentil — nobre · assento etéreo — céu · se consente — é permitida · roga — pede | Alma minha gentil, que te partiste ↵ Tão cedo desta vida descontente, ↵ Repousa lá no céu eternamente, ↵ E viva eu cá na terra sempre triste.Se lá no assento et… |
| V076 | `m3/camoes-alma/index.html`; Dados E / passos[6].pergunta | Qual destes pares de versos faz o jogo «lá» e «cá» com algo teu, sem copiar o soneto? | Qual destes pares de versos explora o contraste entre «lá» e «cá» com algo teu, sem copiar o soneto? |
| V077 | `m3/camoes-barbara/index.html`; Dados E / passos[1].html | o povo vão — a gente comum, sem juízo · perde opinião — perde a convicção · leda — alegre · siso — juízo · bárbara — estrangeira, «selvagem» (jogo com o nome) | Aquela cativa, ↵ Que me tem cativo, ↵ Porque nela vivo, ↵ Já não quer que viva.[…]Pretos os cabelos, ↵ Onde o povo vão ↵ Perde opinião, ↵ Que os louros são belo… |
| V078 | `m3/camoes-barbara/index.html`; Dados E / passos[1].html | eda — alegre · siso — juízo · bárbara — estrangeira, «selvagem» (jogo com o nome) | Aquela cativa, ↵ Que me tem cativo, ↵ Porque nela vivo, ↵ Já não quer que viva.[…]Pretos os cabelos, ↵ Onde o povo vão ↵ Perde opinião, ↵ Que os louros são belo… |
| V079 | `m3/camoes-barbara/index.html`; Dados E / passos[4].retorno | Elogio, jogo de palavras e recusa do preconceito, tudo em versos de cinco sílabas. | Elogio, duplo sentido e recusa do preconceito, tudo em versos de cinco sílabas. |
| V080 | `m3/camoes-desconcerto/index.html`; Dados E / passos[1].html | desconcerto — desordem, falta de harmonia · sobejaram — foram demais | D — «Tanto de meu estado me acho incerto»:Tanto de meu estado me acho incerto, ↵ Que em vivo ardor tremendo estou de frio; ↵ Sem causa, juntamente choro e rio; … |
| V081 | `m3/camoes-invocacoes/index.html`; Dados E / passos[1].html | Tágides — ninfas do Tejo · grandíloquo — elevado, solene · nô mais — não mais · destemperada — desafinada | Uma epopeia começa a pedir ajuda às Musas. Esta acaba a mandá-las calar. São as duas pontas do mesmo poema.No princípio (canto I, estância 4):E vós, Tágides min… |
| V082 | `m3/camoes-leonor/index.html`; Dados E / passos[1].html | verdura — campo verde · testo — tampa · escarlata — tecido vermelho · sainho — casaco curto · vasquinha de cote — saia de uso diário | Mote:Descalça vai para a fonte ↵ Leonor pela verdura; ↵ Vai formosa, e não segura.Voltas:Leva na cabeça o pote, ↵ O testo nas mãos de prata, ↵ Cinta de fina esc… |
| V083 | `m3/camoes-perdigao/index.html`; Dados E / passos[1].html | perdigão — macho da perdiz · pena — pluma; sofrimento · desasado — sem asas · penado — que sofre | Mote:Perdigão perdeu a pena, ↵ Não há mal que lhe não venha.Voltas:Perdigão, que o pensamento ↵ Subiu a um alto lugar, ↵ Perde a pena do voar, ↵ Ganha a pena do… |
| V084 | `m3/camoes-perdigao/index.html`; Dados E / passos[2].opcoes[2][3] | Perde uma, ganha a outra: é o jogo do poema inteiro. | Perde uma, ganha a outra: é o duplo sentido do poema inteiro. |
| V085 | `m3/camoes-restelo-ramos/index.html`; Dados E / fontes[1][1] | Luís de Camões, *Os Lusíadas*, texto integral (oslusiadas.org) | Título da obra em itálico; título de poema entre «». |
| V086 | `m3/camoes-restelo-ramos/index.html`; Dados E / marca | Ler a fundo · *Os Lusíadas* | Título da obra em itálico; título de poema entre «». |
| V087 | `m3/camoes-restelo-ramos/index.html`; Dados E / subtitulo | Luís de Camões, *Os Lusíadas*, 1572, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V088 | `m3/camoes-sobolos/index.html`; Dados E / passos[1].html | sôbolos — sobre os · manado — que correu · Babilónia — o lugar do desterro · Sião — a terra de origem · despois d'acordado — depois de acordado | Sôbolos rios que vão ↵ por Babilónia, me achei, ↵ onde sentado chorei ↵ as lembranças de Sião ↵ e quanto nela passei.Ali o rio corrente ↵ de meus olhos foi mana… |
| V089 | `m3/espada-pena/index.html`; Dados E / passos[1].html | batel — barco pequeno · peregrinando — andando errante · Mavórcios — da guerra · Canace — figura mitológica que escreveu uma carta antes de morrer · ócio ignavo… | A — a segunda invocação (canto VII, 78–79):Vosso favor invoco, que navego ↵ Por alto mar, com vento tão contrário, ↵ Que, se não me ajudais, hei grande medo ↵ Q… |
| V090 | `m3/gram-anafora/index.html`; Dados E / passos[1].html | retoma — uma palavra aponta para outra que veio antes · anáfora como figura — a repetição de uma palavra no início de versos seguidos (também em VIII, 98: Este…… | Uma palavra retoma outra quando aponta para algo que já foi dito. É a anáfora como processo de retoma: pronomes, demonstrativos, repetições, sinónimos.A. «Este … |
| V091 | `m3/gram-modalidade/index.html`; Dados E / passos[1].html | epistémica — grau de certeza: talvez, deve estar, é certo que · deôntica — obrigação, permissão, pedido, ordem: tem de, pode, dai-me · apreciativa — avaliação d… | A modalidade é o que quem fala deixa ver do que pensa daquilo que diz. Três frases:A. «Dai-me agora um som alto e sublimado» (I, 4): um pedido.B. «Roga a Deus, … |
| V105 | `m3/maquina-mundo/index.html`; Dados E / passos[1].html | lume — luz · orbes — esferas · verga — vara · derredor — à volta · limada — polida · engenho — inteligência | A Deusa mostra ao Gama um modelo do universo:Aqui um globo vêm no ar, que o lume ↵ Claríssimo por ele penetrava, ↵ De modo que o seu centro está evidente, ↵ Com… |
| V106 | `m3/painel-m3-f10/index.html`; Cartão 14:  / p | No ensaio, cada citação de *Os Lusíadas* leva o canto e a estância, como «X, 145». | Título da obra em itálico; título de poema entre «». |
| V107 | `m3/questionarios/index.html`; #indice | 3Os Lusíadasfechado | Título da obra em itálico; título de poema entre «». |

### M4

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V108 | `m4/frei-luis-ramos/index.html`; Dados E / marca | Ler a fundo · *Frei Luís de Sousa* | Título da obra em itálico; título de poema entre «». |
| V109 | `m4/frei-luis-ramos/index.html`; Dados E / subtitulo | Almeida Garrett, *Frei Luís de Sousa*, 1843, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V110 | `m4/garrett-fogo/index.html`; Dados E / passos[1].html | haveres — bens, riqueza · atear — acender · o texto entre parênteses é a didascália: o que se faz em palco | Os governadores ao serviço de Castela querem instalar-se no palácio de Manuel de Sousa Coutinho. Ele responde assim:MANUEL: […] Mas fique-se aprendendo em Portu… |
| V111 | `m4/garrett-nome/index.html`; Dados E / passos[1].html | ânimo — coragem · honra — aqui, o bom nome perante os outros | No ato III, o Romeiro já disse quem é. Os pais de Maria vão entrar num convento. Ela agarra-se aos dois:MARIA: […] Que Deus é esse que está nesse altar, e quer … |
| V112 | `m4/garrett-nome/index.html`; Dados E / passos[2].retorno | O que está em jogo não é a vida: é o nome, isto é, o lugar de Maria no mundo. | O que está em causa não é a vida: é o nome, isto é, o lugar de Maria no mundo. |
| V113 | `m4/gram-atos-fala/index.html`; Dados E / passos[1].html | assertivo — afirma alguma coisa como verdadeira · diretivo — leva o outro a agir · compromissivo — compromete quem fala · expressivo — exprime um estado de quem… | Quem fala faz sempre alguma coisa a quem ouve.A. «Olhai, peixes, lá do mar para a terra.» (cap. IV)B. «os grandes comem os pequenos» (cap. IV)C. «Oh que boa dou… |
| V114 | `m4/gram-coesao/index.html`; Dados E / passos[1].html | coesão gramatical — pronomes e demonstrativos que retomam, conectores que ligam · coesão lexical — a palavra repetida, o sinónimo, a expressão equivalente · coe… | «A primeira coisa que me desedifica, peixes, de vós, é que vos comeis uns aos outros. Grande escândalo é este, mas a circunstância o faz ainda maior. Não só vos… |
| V115 | `m4/gram-deiticos/index.html`; Dados E / passos[1].html | deítico pessoal — eu, tu, vós, meu, teu · deítico espacial — aqui, ali, este, aquele · deítico temporal — hoje, agora, amanhã, este mês · referente — aquilo par… | Há palavras que só se entendem sabendo quem fala, onde e quando. São os deíticos.A. «JORGE: Romeiro, romeiro! quem és tu?» e, antes, «ROMEIRO: É aquele.» (Frei … |
| V116 | `m4/guia-da-tarefa-m4/index.html`; Guia da tarefa | 1. Um peixe de hoje2. Discurso no abrigo3. Apreciação crítica de *Frei Luís de Sousa* no teatro | Título da obra em itálico; título de poema entre «». |
| V117 | `m4/guia-da-tarefa-m4/index.html`; Tarefa 3. Apreciação crítica de Frei Luís de Sousa no teatro | Tarefa 3. Apreciação crítica de *Frei Luís de Sousa* no teatro | Título da obra em itálico; título de poema entre «». |
| V120 | `m4/licao-m4-f20/index.html`; Cartão 11: O que recordas com segurança? / html | TPC: *Frei Luís de Sousaaa*, de Raquel Castro | Título da obra em itálico; título de poema entre «». |
| V121 | `m4/mapa-do-modulo-m4/index.html`; #frase | *Frei Luís de Sousa*, lista de personagens da primeira edição (1844). Domínio público. Lição M4-F08 | Título da obra em itálico; título de poema entre «». |
| V122 | `m4/mapa-do-modulo-m4/index.html`; #frase | *Sermão de Santo António aos Peixes*, em Sermoens (Lisboa, 1682). Domínio público. Lição M4-F01 | Título da obra em itálico; título de poema entre «». |
| V123 | `m4/olhar-lupi/index.html`; Dados E / marca | Olhar · M4 *Frei Luís de Sousa* | Título da obra em itálico; título de poema entre «». |
| V124 | `m4/portefolio-do-modulo-m4/index.html`; A lista de verificação | O que se perde quando se perde o nome? Síntese de duas linhas na folha da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín | O que se perde quando se perde o nome? Síntese de duas linhas no papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín |
| V125 | `m4/portefolio-do-modulo-m4/index.html`; A lista de verificação | se defende uma regra em dois minutos? Síntese de duas linhas na folha da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín | se defende uma regra em dois minutos? Síntese de duas linhas no papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín |
| V126 | `m4/portefolio-do-modulo-m4/index.html`; A lista de verificação | zer a verdade a quem não a quer ouvir? Síntese de duas linhas na folha da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín | zer a verdade a quem não a quer ouvir? Síntese de duas linhas no papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín |
| V127 | `m4/questionarios/index.html`; #indice | 6Frei Luís de Sousafechado | Título da obra em itálico; título de poema entre «». |
| V128 | `m4/tradutor-detetive/index.html`; Dados E / passos[6].opcoes[2][3] | Reescreveu a frase inteira; o jogo era mudar uma palavra. | Reescreveu a frase inteira; o desafio era mudar uma palavra. |
| V129 | `m4/vieira-auditorio/index.html`; Dados E / passos[1].html | auditório — público · preservar dele — proteger do mal | Antes de repreender, Vieira louva os peixes. Começa assim:«Enfim, que havemos de pregar hoje aos peixes? Nunca pior auditório. Ao menos têm os peixes duas boas … |
| V130 | `m4/vieira-peixes/index.html`; Dados E / passos[1].html | costados — lados do corpo · desferram — largam · capelo — capuz · limos — algas | No capítulo V, Vieira repreende três peixes em particular:«Pegadores chamam-se estes de que agora falo, e com grande propriedade, porque sendo pequenos, não só … |
| V131 | `m4/vieira-praia/index.html`; Dados E / passos[1].html | Arimino — Rimini, cidade de Itália · hereges — os que se afastam da doutrina da Igreja · dissimular — fingir que não é nada | Vieira conta o que fez Santo António em Rimini, e é isso que ele próprio vai fazer em São Luís:«Pregava Santo António em Itália na cidade de Arimino, contra os … |
| V132 | `m4/vieira-sal/index.html`; Dados E / passos[1].html | ofício — função, dever · corrupção — aqui, o mal moral que se espalha | O sermão abre com uma frase de Cristo, «Vós sois o sal da terra», e com uma pergunta:«O efeito do sal é impedir a corrupção, mas quando a terra se vê tão corrup… |
| V133 | `m4/visita-frei-luis-de-sousa-no-teatro/index.html`; Abertura | Do texto ao palco: *Frei Luís de Sousa*, Teatro Luís de Camões | Título da obra em itálico; título de poema entre «». |
| V134 | `m4/visita-frei-luis-de-sousa-no-teatro/index.html`; Do texto ao palco | *Frei Luís de Sousa*, Teatro Luís de Camões | Título da obra em itálico; título de poema entre «». |

### M5

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V137 | `m5/camilo-assento/index.html`; Dados E / passos[1].html | assentamentos — registos · a folhas 232 — na página 232 · baetão — pano grosso de lã · pedrez — com pintas · compungia — comovia · enchutos — secos | O romance abre com um papel de arquivo:Folheando os livros de antigos assentamentos, no cartorio das cadêas da Relação do Porto, li, no das entradas dos presos … |
| V138 | `m5/camilo-carta/index.html`; Dados E / passos[1].html | consolação — conforto · degredados — condenados ao exílio · pejo — vergonha · derradeiras — últimas | Simão, na nau dos degredados, abre a última carta de Teresa:«É já o meu espirito que te falla, Simão. A tua amiga morreu. A tua pobre Thereza, á hora em que ler… |
| V139 | `m5/camilo-pai/index.html`; Dados E / passos[1].html | condescendencia — tolerância · escusada — inútil | Tadeu de Albuquerque, ao romper do dia, à filha:— Vais hoje dar a mão de esposa a teu primo Balthazar, minha filha. É preciso que te deixes cegamente levar pela… |
| V140 | `m5/camilo-seculo/index.html`; Dados E / passos[1].html | prestito — cortejo · liteiras — cadeiras cobertas levadas por homens ou animais · dama do paço — senhora da corte · chiste — piada | O pai de Simão:Domingos Botelho devia ter uma vocação qualquer; e tinha: era excellente flautista; foi a primeira flauta do seu tempo; e a tocar flauta se suste… |
| V141 | `m5/camilo-simao-ramos/index.html`; Dados E / fontes[1][1] | Camilo Castelo Branco, *Amor de Perdição*, texto integral (Project Gutenberg n.º 16425) | Título da obra em itálico; título de poema entre «». |
| V142 | `m5/camilo-simao-ramos/index.html`; Dados E / marca | Ler a fundo · *Amor de Perdição* | Título da obra em itálico; título de poema entre «». |
| V143 | `m5/camilo-simao-ramos/index.html`; Dados E / subtitulo | Camilo Castelo Branco, *Amor de Perdição*, 1862, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V144 | `m5/eca-falhamos/index.html`; Dados E / passos[1].html | phaeton — carruagem ligeira · Saint-Cloud — arredores de Paris · Figaro — jornal de Paris | Dez anos depois, Carlos e Ega, no Ramalhete:— E aqui tens tu uma existencia d'homem! Em dez annos não me tem succedido nada, a não ser quando se me quebrou o ph… |
| V145 | `m5/eca-hotel/index.html`; Dados E / passos[1].html | gastando cêra com ruins defuntos — a perder tempo com o que não merece · sole normande — linguado à normanda (francês) · banca-rota — falência · fazenda — finan… | Jantar no Hotel Central. Discute-se o realismo:— Isso é absurdo, dizia Carlos, os caracteres só se podem manifestar pela acção... ↵ — E a obra d'arte, accrescen… |
| V146 | `m5/eca-ramalhete/index.html`; Dados E / passos[1].html | renque — fila · Residencia Ecclesiastica — casa de padres · Escudo d'Armas — brasão · postigos terreos — pequenas janelas ao nível da rua | A — a primeira frase do romance:A casa que os Maias vieram habitar em Lisboa, no outono de 1875, era conhecida na visinhança da rua de S. Francisco de Paula, e … |
| V147 | `m5/eca-ramalhete/index.html`; Dados E / passos[3].opcoes[2][3] | Os Maias «vieram habitar» a casa em 1875: Carlos não nasceu lá. | Sem alteração: família Maia. |
| V148 | `m5/gram-dil/index.html`; Dados E / passos[1].html | Discurso indireto — o narrador conta o que foi dito, com um verbo como dizer e «que». | A Discurso direto «— Falhámos a vida, menino!» As palavras da personagem, com travessão ou aspas. B Discurso indireto livre «Ega mostrou-se impressionado. Olha … |
| V149 | `m5/gram-funcoes/index.html`; Dados E / passos[1].html | teste do pronome — «o», «a» dão o complemento direto; «lhe» dá o indireto · teste do corte — se a frase se aguenta sem a expressão, é modificador · predicativo … | As frases vêm do romance, em grafia atualizada.A. «Deu as cartas a Constança.»B. «Teresa ergueu-se sem lágrimas.»C. «Domingos Botelho era extremamente feio.»tes… |
| V178 | `m5/padre-amaro-rego/index.html`; Dados E / passos[6].rot | Ligação a *Os Maias* | Título da obra em itálico; título de poema entre «». |
| V179 | `m5/painel-m5-f09/index.html`; Cartão 8:  / p | A antiga cadeia fica no Largo Amor de Perdição, junto à Torre dos Clérigos. | Sem alteração: lugar. |
| V180 | `m5/questionarios/index.html`; #indice | 1Amor de Perdiçãofechado | Título da obra em itálico; título de poema entre «». |
| V181 | `m5/questionarios/index.html`; #indice | 2Os Maiasfechado | Título da obra em itálico; título de poema entre «». |
| V182 | `m5/questionarios/index.html`; #indice | 7Os espaços de Os Maiasfechado | Título da obra em itálico; título de poema entre «». |
| V183 | `m5/questionarios/index.html`; #indice | 8Os Maias: o que anuncia a tragédiafechado | Título da obra em itálico; título de poema entre «». |

### M6

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V184 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | ⟪«E mais: as costureiras, as floristas / Descem dos magasins, causam-me sobressaltos; / Custa-lhes a elevar os seus pescoços altos / E muitas delas são comparsa… | Cesário Verde atravessa Lisboa à noite e escreve o que vê. Três momentos:«E mais: as costureiras, as floristas ↵ Descem dos magasins, causam-me sobressaltos; ↵ … |
| V185 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | ⟪«Num cuteleiro, de avental, ao torno, / Um forjador maneja um malho, rubramente; / E de uma padaria exala-se, inda quente, / Um cheiro salutar e honesto a pão … | Cesário Verde atravessa Lisboa à noite e escreve o que vê. Três momentos:«E mais: as costureiras, as floristas ↵ Descem dos magasins, causam-me sobressaltos; ↵ … |
| V186 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | ⟪«“Dó da miséria!… Compaixão de mim!…” / E, nas esquinas, calvo, eterno, sem repouso, / Pede-me sempre esmola um homenzinho idoso, / Meu velho professor nas aul… | Cesário Verde atravessa Lisboa à noite e escreve o que vê. Três momentos:«E mais: as costureiras, as floristas ↵ Descem dos magasins, causam-me sobressaltos; ↵ … |
| V187 | `m6/gram-oracoes-rua/index.html`; Dados E / passos[1].html | A. «Há tal soturnidade, há tal melancolia, / Que as sombras, o bulício, o Tejo, a maresia / Despertam-me um desejo absurdo de sofrer.» | Os versos vêm dos poemas, em grafia atualizada.A. «Há tal soturnidade, há tal melancolia, ↵ Que as sombras, o bulício, o Tejo, a maresia ↵ Despertam-me um desej… |
| V189 | `m6/antero-deus/index.html`; Dados E / passos[1].html | impalpavel — que não se pode tocar · a final — por fim · despojo vão — resto inútil · depuz — pus de lado · lobrega — escura, triste | A — «Ideal», o último terceto:É como uma miragem, que entrevejo, ↵ Ideal, que nasceu na solidão, ↵ Nuvem, sonho impalpavel do Desejo...B — «Na mão de Deus»:Na m… |
| V190 | `m6/cesario-avemarias/index.html`; Dados E / fontes[1][1] | Cesário Verde, «O Sentimento dum Ocidental», O Livro de Cesário Verde (Project Gutenberg n.º 8698) | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V191 | `m6/cesario-avemarias/index.html`; Dados E / passos[1].html | soturnidade — tristeza sombria · bulicio — burburinho, ruído de gente · extravasado — que se espalha · baixeis — navios · singram — navegam · varonis — fortes | O anoitecer, junto ao rio:Nas nossas ruas, ao anoitecer, ↵ Ha tal soturnidade, ha tal melancholia, ↵ Que as sombras, o bulicio, o Tejo, a maresia ↵ Despertam-me… |
| V192 | `m6/cesario-avemarias/index.html`; Dados E / subtitulo | Cesário Verde, «O Sentimento dum Ocidental», 1887 · I, «Ave-Marias» | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V193 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | magasins — lojas · cuteleiro — oficina de facas · malho — martelo grande | Cesário Verde atravessa Lisboa à noite e escreve o que vê. Três momentos:«E mais: as costureiras, as floristas ↵ Descem dos magasins, causam-me sobressaltos; ↵ … |
| V194 | `m6/cesario-noite-ramos/index.html`; Dados E / fontes[1][1] | Cesário Verde, *O Livro de Cesário Verde* (1887), texto integral (Project Gutenberg n.º 8698) | Título da obra em itálico; título de poema entre «». |
| V195 | `m6/cesario-noite-ramos/index.html`; Dados E / marca | Ler a fundo · «O Sentimento dum Ocidental» | Título da obra em itálico; título de poema entre «». |
| V196 | `m6/cesario-noite-ramos/index.html`; Dados E / passos[1].html | Cesário Verde, o poeta deste módulo, escreveu em 1880 «O Sentimento dum Ocidental»: quatro partes, Ave-Marias, Noite Fechada, Ao Gás, Horas Mortas, uma noite in… | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V197 | `m6/cesario-noite-ramos/index.html`; Dados E / subtitulo | Cesário Verde, «O Sentimento dum Ocidental», 1880, uma história com ramos | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V198 | `m6/cesario-noite/index.html`; Dados E / fontes[1][1] | Cesário Verde, «O Sentimento dum Ocidental», O Livro de Cesário Verde (Project Gutenberg n.º 8698) | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V199 | `m6/cesario-noite/index.html`; Dados E / passos[1].html | II — «Noite Fechada»: | II: «Noite Fechada»:Toca-se as grades, nas cadeias. Som ↵ Que mortifica e deixa umas loucuras mansas! ↵ O aljube, em que hoje estão velhinhas e creanças, ↵ Bem … |
| V200 | `m6/cesario-noite/index.html`; Dados E / passos[1].html | IV — «Horas Mortas»: | II: «Noite Fechada»:Toca-se as grades, nas cadeias. Som ↵ Que mortifica e deixa umas loucuras mansas! ↵ O aljube, em que hoje estão velhinhas e creanças, ↵ Bem … |
| V201 | `m6/cesario-noite/index.html`; Dados E / passos[1].html | mortifica — atormenta · aljube — prisão · mulher de «dom» — senhora de família nobre · enfezados — raquíticos · emparedados — fechados entre paredes · fel — ama… | II: «Noite Fechada»:Toca-se as grades, nas cadeias. Som ↵ Que mortifica e deixa umas loucuras mansas! ↵ O aljube, em que hoje estão velhinhas e creanças, ↵ Bem … |
| V202 | `m6/cesario-noite/index.html`; Dados E / subtitulo | Cesário Verde, «O Sentimento dum Ocidental», 1887 · II e IV | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V203 | `m6/gram-oracoes-rua/index.html`; Dados E / passos[1].html | teste do «isso» — se a oração se troca por «isso», é substantiva · teste do «o qual» — se «que» se troca por «o qual», «os quais», é relativa · teste da pergunt… | Os versos vêm dos poemas, em grafia atualizada.A. «Há tal soturnidade, há tal melancolia, ↵ Que as sombras, o bulício, o Tejo, a maresia ↵ Despertam-me um desej… |

### M7

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V245 | `m7/licao-m7-f01/index.html`; Cartão 1: Quantos somos? / html / legenda | Fernando Pessoa (fotografia, 1914). Domínio público. Pessoa em 1914, o ano do «dia triunfal». | Fernando Pessoa, cerca de 1914.Créditos e fonte da imagemIdentificação da fotografiaAutorFotógrafo não identificado.ObraRetrato de Fernando Pessoa com chapéu.Da… |
| V246 | `m7/licao-m7-f05/index.html`; Cartão 1: À beira do rio / html / legenda | Fernando Pessoa (fotografia, 1914). Domínio público. Pessoa em 1914, o ano do «dia triunfal». | Fernando Pessoa, cerca de 1914.Créditos e fonte da imagemIdentificação da fotografiaAutorFotógrafo não identificado.ObraRetrato de Fernando Pessoa com chapéu.Da… |
| V248 | `m7/mapa-do-modulo-m7/index.html`; Blocos e legendas da página / legenda | Fernando Pessoa (fotografia, 1914). Domínio público. Lição M7-F01 | Tabela: fotógrafo não identificado; retrato com chapéu; cerca de 1914 (data incerta); reprodução no Wikimedia Commons, acervo original não indicado; domínio púb… |
| V249 | `m7/campos-aniversario/index.html`; Dados E / passos[1].html | grelado — bolor · «Pára» — grafia da edição | No tempo em que festejavam o dia dos meus anos, ↵ Eu era feliz e ninguém estava morto. ↵ Na casa antiga, até eu fazer anos era uma tradição de há séculos, ↵ E a… |
| V250 | `m7/campos-maquina/index.html`; Dados E / passos[1].html | eléctricas — grafia da edição | A — «Ode Triunfal», 1914:À dolorosa luz das grandes lâmpadas eléctricas da fábrica ↵ Tenho febre e escrevo. ↵ […] ↵ Ó rodas, ó engrenagens, r-r-r-r-r-r-r eterno… |
| V251 | `m7/gram-valores-pessoa/index.html`; Dados E / passos[1].html | aspeto — acabou (perfetivo), dura (imperfetivo), é costume (habitual), repete-se vezes contadas (iterativo), vale sempre (genérico) · modalidade — certeza ou pr… | Os versos vêm de poemas que já leste.A. «Eu era feliz e ninguém estava morto.» (Campos)B. «Cumpriu-se o Mar, e o Império se desfez.» (Mensagem)C. «Julgando-se f… |
| V252 | `m7/licao-m7-f01/index.html`; Cartão 17:  / f | **O Guardador de Rebanhos**: o primeiro título do dia triunfal, assinado por Caeiro. | Título da obra em itálico; título de poema entre «». |
| V253 | `m7/licao-m7-f01/index.html`; Cartão 17:  / frase | a começar pelo título *O Guardador de Rebanhos*. | Título da obra em itálico; título de poema entre «». |
| V254 | `m7/mensagem-mostrengo/index.html`; Dados E / passos[1].html | breu — escuridão total · reprendeu — voltou a prender | O mostrengo que está no fim do mar ↵ Na noite de breu ergueu-se a voar; ↵ À roda da nau voou três vezes, ↵ Voou três vezes a chiar, ↵ E disse: «Quem é que ousou… |
| V255 | `m7/mensagem-nevoeiro/index.html`; Dados E / passos[1].html | fulgor baço — brilho sem força · fogo-fátuo — chama fraca sobre os pântanos · derradeiro — último | O último poema da Mensagem:Nem rei nem lei, nem paz nem guerra, ↵ Define com perfil e ser ↵ Este fulgor baço da terra ↵ Que é Portugal a entristecer — ↵ Brilho … |
| V256 | `m7/painel-m7-f10/index.html`; Cartão 14:  / p | Em *Frei Luís de Sousa*, o regresso de D. João de Portugal faz renascer a família de Madalena. | Título da obra em itálico; título de poema entre «». |
| V257 | `m7/pessoa-almas/index.html`; Dados E / passos[1].html | móbil — que se move | O ortónimo, em 1930:Não sei quantas almas tenho. ↵ Cada momento mudei. ↵ Continuamente me estranho. ↵ Nunca me vi nem achei. ↵ De tanto ser, só tenho alma. ↵ Qu… |
| V258 | `m7/pessoa-ceifeira/index.html`; Dados E / passos[1].html | ceifeira — mulher que corta cereal · lida — trabalho · ciência — aqui, a consciência | Ela canta, pobre ceifeira, ↵ Julgando-se feliz talvez; ↵ Canta, e ceifa, e a sua voz, cheia ↵ De alegre e anónima viuvez,Ondula como um canto de ave ↵ No ar lim… |
| V259 | `m7/pessoa-ilha/index.html`; Dados E / passos[1].html | se olvida — se esquece · desvirtua — perde o valor | Não sei se é sonho, se realidade, ↵ Se uma mistura de sonho e vida, ↵ Aquela terra de suavidade ↵ Que na ilha extrema do sul se olvida. ↵ É a que ansiamos. Ali,… |
| V260 | `m7/reis-lidia/index.html`; Dados E / passos[1].html | fitemos — olhemos fixamente · Fado — destino | Ricardo Reis convida Lídia:Vem sentar-te comigo, Lídia, à beira do rio. ↵ Sossegadamente fitemos o seu curso e aprendamos ↵ Que a vida passa, e não estamos de m… |
| V261 | `m7/tabacaria/index.html`; #p4 | 2.º ano · Lisboa, século XIXCesário Verde, «O Sentimento dum Ocidental»: «Nas nossas ruas, ao anoitecer, / Há tal soturnidade, há tal melancolia» | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V262 | `m7/tabacaria/index.html`; #seguir | Cesário Verde, «O Sentimento dum Ocidental», in O Livro de Cesário Verde · Project Gutenberg | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V263 | `m7/tabacaria/index.html`; A minha leitura | Da janela, vejo— Hoje estou mais do lado— O Esteves, para mim, é— A minha ligação— Esta semana— | Da janela, vejo: Hoje estou mais do lado: O Esteves, para mim, é: A minha ligação: Esta semana: |
| V264 | `m7/mensagem-nevoeiro/index.html`; Dados E / passos[5].opcoes[1][1] | A turma hoje é nevoeiro: ninguém sabe o que quer. / Tudo é disperso, nada é inteiro. / Ó Portugal, hoje és nevoeiro... | A turma hoje é nevoeiro: ninguém sabe o que quer. / Tudo é disperso, nada é inteiro. / Ó Portugal, hoje és nevoeiro… |

### M9

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V268 | `m9/gram-aspeto-memorial/index.html`; Dados E / passos[1].html | aspeto — acabou (perfetivo), dura (imperfetivo), é costume (habitual), repete-se vezes contadas (iterativo), vale sempre (genérico) · coesão — anáfora (retoma o… | As frases foram escritas para este exercício, à maneira de Saramago. Não são do romance.A. Chegaram os homens a Mafra, e ali ficaram anos.B. Todas as manhãs o c… |
| V278 | `m9/painel-m9-f07/index.html`; Cartão 11:  / p | Na ponte do poder, ao lado do Memorial, estão Vieira e *Os Maias*. | Título da obra em itálico; título de poema entre «». |
| V279 | `m9/passarola-ramos/index.html`; Dados E / marca | Ler a fundo · *Memorial do Convento* | Título da obra em itálico; título de poema entre «». |
| V280 | `m9/passarola-ramos/index.html`; Dados E / subtitulo | José Saramago, *Memorial do Convento* (1982), o voo da passarola: uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V281 | `m9/questionarios/index.html`; #indice | 1Memorial do Convento: a históriafechado | Título da obra em itálico; título de poema entre «». |

### Transversal

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V024 | `tarefas/m1-u2/aquecimento/index.html`; Cartão 4:  / frase | A técnica diz: “Abre a porta.” (fala documentada) | A técnica diz: «Abre a porta.» (fala documentada) |
| V051 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 4:  / frase | A oração “para que a mesa ficasse livre” é [1]. | A oração «para que a mesa ficasse livre» é [1]. |
| V052 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 4:  / p | Frase criada: “Arrumei os livros para que a mesa ficasse livre.” Classifica a oração iniciada por para que. | Frase criada: «Arrumei os livros para que a mesa ficasse livre.» Classifica a oração iniciada por _para que_. |
| V053 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 5:  / fe[3] | A posição não classifica a oração: “Para que a mesa ficasse livre, arrumei os livros.” continua a ser final. Confirmam-na o conector e o conjuntivo. | A posição não classifica a oração: «Para que a mesa ficasse livre, arrumei os livros.» continua a ser final. Confirmam-na o conector e o conjuntivo. |
| V054 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 5:  / p | Que justificação aponta, na frase criada, os traços que confirmam a classificação de “para que a mesa ficasse livre”? | Que justificação aponta, na frase criada, os traços que confirmam a classificação de «para que a mesa ficasse livre»? |
| V055 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[1][1] | Comparação: “A notícia caiu como água gelada.” | Comparação: «A notícia caiu como água gelada.» |
| V056 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[2][1] | Antítese: “Sorrio por fora, choro por dentro.” | Antítese: «Sorrio por fora, choro por dentro.» |
| V057 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[3][1] | Enumeração: “Testes, treinos, recados, turnos.” | Enumeração: «Testes, treinos, recados, turnos.» |
| V058 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[4][1] | Interrogação retórica: “De que serve correr?” | Interrogação retórica: «De que serve correr?» |
| V059 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 10:  / apoio | Cena inventada: a Rita gaba o bolo que trouxe; o Tiago diz, à parte, para o público: “Está queimado por baixo.” | Cena inventada: a Rita gaba o bolo que trouxe; o Tiago diz, à parte, para o público: «Está queimado por baixo.» |
| V060 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 10:  / p2 | Quem diz “Está queimado por baixo”, e para quem? Escolhe a identificação certa da prova. | Quem diz «Está queimado por baixo», e para quem? Escolhe a identificação certa da prova. |
| V061 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 4:  / frase | A oração “que está na mesa” é [1]. | A oração «que está na mesa» é [1]. |
| V062 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 4:  / p | Frase criada: “O livro que está na mesa pertence à biblioteca.” Classifica a oração iniciada por que. | Frase criada: «O livro que está na mesa pertence à biblioteca.» Classifica a oração iniciada por _que_. |
| V063 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 4:  / p2 | Na frase criada “O livro que está na mesa pertence à biblioteca”, como se classifica a oração “que está na mesa”? | Na frase criada «O livro que está na mesa pertence à biblioteca», como se classifica a oração «que está na mesa»? |
| V064 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 5:  / p | Cena inventada: a Sara diz que vai subir a serra de sandálias. O guia diz, à parte: “Pés sem botas, serra sem fim.” O que anuncia o comentário? | Cena inventada: a Sara diz que vai subir a serra de sandálias. O guia diz, à parte: «Pés sem botas, serra sem fim.» O que anuncia o comentário? |
| V065 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 5:  / p2 | Numa cena inventada, a Sara quer subir a serra de sandálias e o guia diz só para o público: “Pés sem botas, serra sem fim.” Que leitura respeita o que o comentá… | Numa cena inventada, a Sara quer subir a serra de sandálias e o guia diz só para o público: «Pés sem botas, serra sem fim.» Que leitura respeita o que o comentá… |
| V066 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 7:  / pares[1][1] | Diz “Sou pontual!” e chega quando a sessão acabou. | Diz «Sou pontual!» e chega quando a sessão acabou. |
| V067 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 7:  / pares[2][1] | Diz “Trago o guião” e entrega-o logo à colega. | Diz «Trago o guião» e entrega-o logo à colega. |
| V068 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 7:  / pares[4][1] | Antes do ensaio, admite “Costumo faltar sem avisar.” | Antes do ensaio, admite «Costumo faltar sem avisar.» |
| V069 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 8:  / p | Frase criada para ensaio: “Já / cheguei.” (com alívio). A barra marca uma pausa. O que indicam os parênteses? | Frase criada para ensaio: «Já / cheguei.» (com alívio). A barra marca uma pausa. O que indicam os parênteses? |
| V070 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 8:  / p2 | Na frase criada “Já / cheguei.” (com alívio), a pausa já está na barra. Que informação acrescentam os parênteses? | Na frase criada «Já / cheguei.» (com alívio), a pausa já está na barra. Que informação acrescentam os parênteses? |
| V135 | `tarefas/m4-u3/index.html`; Blocos e legendas da página | Ilumino a minha casa para receber os muito poderosos e excelentes senhores governadores destes reinos. […] celentes senhores governadores destes reinos. | «Ilumino a minha casa para receber os muito poderosos e excelentes senhores governadores destes reinos.» |
| V136 | `tarefas/m4-u3/index.html`; Blocos e legendas da página | Oh que boa doutrina era esta para a terra, se eu não pregara para o mar! […] a para a terra, se eu não pregara para o mar! | «Oh que boa doutrina era esta para a terra, se eu não pregara para o mar!» |
| V283 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | A. «Ondas do mar de Vigo, / se vistes meu amigo?» (Martim Codax): a mesma vogal a voltar. | Três textos que já leste, com três coisas que uma estrofe de rap também faz:A. «Ondas do mar de Vigo, ↵ se vistes meu amigo?» (Martim Codax): a mesma vogal a vo… |
| V284 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | B. «Sam eu coruja ou corujo, / Ou sam algum caramujo» (Gil Vicente): sons repetidos dentro do verso. | Três textos que já leste, com três coisas que uma estrofe de rap também faz:A. «Ondas do mar de Vigo, ↵ se vistes meu amigo?» (Martim Codax): a mesma vogal a vo… |
| V285 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | C. «Que mortes, que perigos, que tormentas, / Que crueldades neles experimentas!» (Camões, IV, 95): a mesma consoante a voltar, e a mesma palavra a abrir. | Três textos que já leste, com três coisas que uma estrofe de rap também faz:A. «Ondas do mar de Vigo, ↵ se vistes meu amigo?» (Martim Codax): a mesma vogal a vo… |
| V286 | `1/todos/index.html`; Módulo 2 · Teatro vicentino | A farsa em cena: *Farsa de Inês Pereira*, no teatrocaderno de campo | Título da obra em itálico; título de poema entre «». |
| V287 | `1/todos/index.html`; Módulo 2 · Teatro vicentino | E se Inês escolhesse o asno logo?Gil Vicente, *Farsa de Inês Pereira*, 1523, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V288 | `1/todos/index.html`; Módulo 3 · Lírica e épica camonianas | E se ficasses na praia?Luís de Camões, *Os Lusíadas*, 1572, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V289 | `2/todos/index.html`; Módulo 4 · Literatura barroca e romântica | Do texto ao palco: *Frei Luís de Sousa*, Teatro Luís de Camõescaderno de campo | Título da obra em itálico; título de poema entre «». |
| V290 | `2/todos/index.html`; Módulo 4 · Literatura barroca e romântica | E se o Romeiro dissesse o nome?Almeida Garrett, *Frei Luís de Sousa*, 1843, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V291 | `2/todos/index.html`; Módulo 5 · Narrativa do século XIX | E se Simão obedecesse ao pai?Camilo Castelo Branco, *Amor de Perdição*, 1862, uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V292 | `2/todos/index.html`; Módulo 6 · Poesia Realista | Ave-MariasCesário Verde, «O Sentimento dum Ocidental», 1887 · I, «Ave-Marias» | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V293 | `2/todos/index.html`; Módulo 6 · Poesia Realista | Da «Noite Fechada» às «Horas Mortas»Cesário Verde, «O Sentimento dum Ocidental», 1887 · II e IV | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V294 | `2/todos/index.html`; Módulo 6 · Poesia Realista | Uma noite com CesárioCesário Verde, «O Sentimento dum Ocidental», 1880, uma história com ramos | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V295 | `3/index.html`; 3.º ano | Quem és quando escreves — e quem fica de fora do que contas? | Quem és quando escreves e quem fica de fora do que contas? |
| V296 | `3/todos/index.html`; Módulo 9 · Romance Saramaguiano | E se Baltasar ficasse em terra?José Saramago, *Memorial do Convento* (1982), o voo da passarola: uma história com ramos | Título da obra em itálico; título de poema entre «». |
| V297 | `assets/exame/sessoes.json`; Sessões de exame / sessions[11].writing.prompt | Explica como uma passagem de «O Sentimento dum Ocidental» transforma uma observação urbana numa reflexão. Analisa uma sensação e um contraste social ou temporal… | Título da obra em itálico; título de poema entre «». |
| V298 | `assets/exame/sessoes.json`; Sessões de exame / sessions[23].correction.model | Em *Farsa de Inês Pereira* e em *Amor de Perdição*, as escolhas individuais confrontam-se com regras sociais e relações familiares. No entanto, os textos repres… | Título da obra em itálico; título de poema entre «». |
| V299 | `assets/exame/sessoes.json`; Sessões de exame / sessions[3].focus | Interpretar o conflito na *Farsa de Inês Pereira* | Título da obra em itálico; título de poema entre «». |
| V300 | `assets/exame/sessoes.json`; Sessões de exame / sessions[3].writing.criteria[1] | Respondi ao pedido: interpretar o conflito na *Farsa de Inês Pereira*. | Título da obra em itálico; título de poema entre «». |
| V301 | `assets/exame/sessoes.json`; Sessões de exame / sessions[5].source.title | *Os Lusíadas*: celebrar e interrogar | Título da obra em itálico; título de poema entre «». |
| V302 | `assets/exame/sessoes.json`; Sessões de exame / sessions[7].source.title | *Frei Luís de Sousa*: o que a cena revela | Título da obra em itálico; título de poema entre «». |
| V303 | `assets/exame/sessoes.json`; Sessões de exame / sessions[8].writing.prompt | A partir de *Amor de Perdição*, mostra como uma escolha individual é condicionada por relações familiares ou convenções sociais. Distingue explicar uma ação de … | Título da obra em itálico; título de poema entre «». |
| V304 | `assets/exame/sessoes.json`; Sessões de exame / sessions[9].writing.prompt | Analisa dois pormenores de um espaço ou de uma cena de *Os Maias*. Explica como contribuem para caracterizar uma personagem ou para construir uma visão crítica … | Título da obra em itálico; título de poema entre «». |
| V305 | `atlas/index.html`; #atlas-lista-pessoas | Jogo de memória · opcional | Atividade de memória · opcional |
| V306 | `atlas/index.html`; #atlas-lista-pessoas | O jogo anterior continua disponível com os resultados guardados e o seu conjunto de 147 pessoas. | A atividade anterior continua disponível com os resultados guardados e o seu conjunto de 147 pessoas. |
| V307 | `atlas/index.html`; #desafio | Pessoa ou personagem?Bartolomeu de Gusmão existiu: em 1709 fez subir um pequeno balão diante da corte. No *Memorial do Convento*, o padre Bartolomeu voa na pass… | Título da obra em itálico; título de poema entre «». |
| V308 | `atlas/index.html`; #desafio | Uma data, duas versõesEunice Muñoz fez de Maria em *Frei Luís de Sousa*: a Infopédia diz 1942, o Correio da Manhã diz 1943. Quando duas fontes não batem certo, … | Título da obra em itálico; título de poema entre «». |
| V309 | `atlas/index.html`; #desafio | Uma obra, duas datasPara o *Amor de Perdição* de Manoel de Oliveira, umas fontes dão 1978 e outras 1979. Não escolhas a que dá jeito: vê o que cada data marca (… | Título da obra em itálico; título de poema entre «». |
| V310 | `atlas/index.html`; #desafio | . As fontes estão identificadas em cada perfil. Os resultados do jogo ficam só neste aparelho. Há mais 6 pessoas à espera de conferência de fontes. | . As fontes estão identificadas em cada perfil. Os resultados da atividade ficam só neste aparelho. Há mais 6 pessoas à espera de conferência de fontes. |
| V311 | `atlas/index.html`; #desafio | Passaporte do jogo | Passaporte da atividade |
| V312 | `c/candide-jardim/index.html`; Dados E / emblemas[2][3] | Já percebeste o jogo. Relê o elogio ao barão e pergunta porquê. | Já percebeste a ironia. Relê o elogio ao barão e pergunta porquê. |
| V313 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | rima pobre — duas palavras da mesma classe, quase sempre dois infinitivos · rima rica — classes diferentes, ou mais de uma sílaba a rimar · rima interna — sons … | Três textos que já leste, com três coisas que uma estrofe de rap também faz:A. «Ondas do mar de Vigo, ↵ se vistes meu amigo?» (Martim Codax): a mesma vogal a vo… |
| V314 | `c/kafka-acordar/index.html`; Dados E / passos[1].html | couraça — armadura · abaulado — curvo · caixeiro-viajante — vendedor que percorre a região com amostras · regalo — manga de peles para aquecer as mãos · flanco … | Em 1915, Franz Kafka publica A Metamorfose. Gregor Samsa, caixeiro-viajante que sustenta a família, acorda diferente. Os três primeiros parágrafos, em tradução … |
| V315 | `c/quinta-mandamentos/index.html`; Dados E / passos[1].html | Tradução nossa do inglês; o original está em domínio público na União Europeia. Garganta — o porco que fala pelos outros (Squealer, no original) · Napoleão — o … | Em 1945, George Orwell publica uma fábula: os animais de uma quinta expulsam o dono e escrevem as regras na parede do celeiro.OS SETE MANDAMENTOS. 1. Tudo o que… |
| V316 | `mapa/index.html`; 1.º ano | Abrir M1 — Literatura medieval → | Abrir M1: Literatura medieval → |
| V317 | `mapa/index.html`; 1.º ano | Abrir M2 — Teatro vicentino → | Abrir M2: Teatro vicentino → |
| V318 | `mapa/index.html`; 1.º ano | Abrir M3 — Lírica e épica camonianas → | Abrir M3: Lírica e épica camonianas → |
| V319 | `mapa/index.html`; 1.º ano | M1 — Literatura medieval12 lições+ | M1: Literatura medieval12 lições+ |
| V320 | `mapa/index.html`; 1.º ano | M2 — Teatro vicentino10 lições+ | M2: Teatro vicentino10 lições+ |
| V321 | `mapa/index.html`; 1.º ano | M3 — Lírica e épica camonianas12 lições+ | M3: Lírica e épica camonianas12 lições+ |
| V322 | `mapa/index.html`; 2.º ano | Abrir M4 — Literatura barroca e romântica → | Abrir M4: Literatura barroca e romântica → |
| V323 | `mapa/index.html`; 2.º ano | Abrir M5 — Narrativa do século XIX → | Abrir M5: Narrativa do século XIX → |
| V324 | `mapa/index.html`; 2.º ano | Abrir M6 — Poesia Realista → | Abrir M6: Poesia Realista → |
| V325 | `mapa/index.html`; 2.º ano | M4 — Literatura barroca e romântica16 lições+ | M4: Literatura barroca e romântica16 lições+ |
| V326 | `mapa/index.html`; 2.º ano | M5 — Narrativa do século XIX11 lições+ | M5: Narrativa do século XIX11 lições+ |
| V327 | `mapa/index.html`; 2.º ano | M6 — Poesia Realista11 lições+ | M6: Poesia Realista11 lições+ |
| V328 | `mapa/index.html`; 3.º ano | Abrir M7 — Lírica pessoana → | Abrir M7: Lírica pessoana → |
| V329 | `mapa/index.html`; 3.º ano | Abrir M8 — Poesia e conto do século XX → | Abrir M8: Poesia e conto do século XX → |
| V330 | `mapa/index.html`; 3.º ano | Abrir M9 — Romance Saramaguiano → | Abrir M9: Romance Saramaguiano → |
| V331 | `mapa/index.html`; 3.º ano | M7 — Lírica pessoana17 lições+ | M7: Lírica pessoana17 lições+ |
| V332 | `mapa/index.html`; 3.º ano | M8 — Poesia e conto do século XX10 lições+ | M8: Poesia e conto do século XX10 lições+ |
| V333 | `mapa/index.html`; 3.º ano | M9 — Romance Saramaguiano10 lições+ | M9: Romance Saramaguiano10 lições+ |
| V334 | `obras/amor-perdicao/index.html`; Abertura | *Amor de Perdição* | Título da obra em itálico; título de poema entre «». |
| V335 | `obras/amor-perdicao/index.html`; Conhecer o autor | *Amor de Perdição*, de Camilo Castelo BrancoRTP Ensina (Grandes Livros, 2009), 48 min. Documentário sobre o romance de Simão, Teresa e Mariana. | Título da obra em itálico; título de poema entre «». |
| V336 | `obras/amor-perdicao/index.html`; Ler | *Amor de Perdição* (Projeto Gutenberg, n.º 16425) | Título da obra em itálico; título de poema entre «». |
| V337 | `obras/cesario/index.html`; Abertura | «O Sentimento dum Ocidental» | Título da obra em itálico; título de poema entre «». |
| V338 | `obras/cesario/index.html`; Conhecer o autor | O Livro de Cesário VerdeRTP Ensina (Grandes Livros, 2010), cópia no Arquivo da Internet, 31 min. Documentário sobre o poeta do concreto. | Título da obra em itálico; título de poema entre «». |
| V339 | `obras/cesario/index.html`; Ler | «O Sentimento dum Ocidental» (Biblioteca) | Título da obra em itálico; título de poema entre «». |
| V340 | `obras/frei-luis/index.html`; Abertura | *Frei Luís de Sousa* | Título da obra em itálico; título de poema entre «». |
| V341 | `obras/frei-luis/index.html`; Frei Luís de Sousa, outra encenação para Garrett | *Frei Luís de Sousa*, outra encenação para Garrett | Título da obra em itálico; título de poema entre «». |
| V342 | `obras/frei-luis/index.html`; Ler | *Frei Luís de Sousa* (Biblioteca) | Título da obra em itálico; título de poema entre «». |
| V343 | `obras/index.html`; As obras | «O Sentimento dum Ocidental»M6, Cesário Verde. 2 leituras. | Título da obra em itálico; título de poema entre «». |
| V344 | `obras/ines/index.html`; Abertura | *Farsa de Inês Pereira* | Título da obra em itálico; título de poema entre «». |
| V345 | `obras/ines/index.html`; Auto da Barca do Inferno (2022) | *Auto da Barca do Inferno* (2022) | Título da obra em itálico; título de poema entre «». |
| V346 | `obras/ines/index.html`; Auto da Barca do Inferno (2022) | Não é a *Farsa de Inês Pereira*: é outra peça do mesmo autor, numa montagem que a própria companhia diz desconstruída. Serve para comparar. | Título da obra em itálico; título de poema entre «». |
| V347 | `obras/ines/index.html`; Conhecer o autor | *Auto da Barca do Inferno*, de Gil VicenteRTP Ensina (Grandes Livros, 2009), 32 min. Documentário sobre outra peça de Gil Vicente e a crítica à sociedade do seu… | Título da obra em itálico; título de poema entre «». |
| V348 | `obras/lusiadas/index.html`; Abertura | *Os Lusíadas* | Título da obra em itálico; título de poema entre «». |
| V349 | `obras/lusiadas/index.html`; Conhecer o autor | *Os Lusíadas*: um poema épico e críticoRTP Ensina (Câmara Clara, 2007), 4 min. Helder Macedo sobre a exaltação e a crítica no poema. | Título da obra em itálico; título de poema entre «». |
| V350 | `obras/lusiadas/index.html`; Ler | *Os Lusíadas* (Projeto Gutenberg, n.º 3333) | Título da obra em itálico; título de poema entre «». |
| V351 | `obras/maias/index.html`; Abertura | *Os Maias* | Título da obra em itálico; título de poema entre «». |
| V352 | `obras/maias/index.html`; Conhecer o autor | A sátira de Eça de Queirós em *Os Maias*»RTP Ensina (Grandes Livros, 2009), 6 min. Carlos Reis sobre a caricatura da sociedade. | Título da obra em itálico; título de poema entre «». |
| V353 | `obras/maias/index.html`; Conhecer o autor | *Os Maias*, de Eça de QueirósRTP Ensina (Grandes Livros, 2009), 49 min. Documentário sobre três gerações da família Maia. | Título da obra em itálico; título de poema entre «». |
| V354 | `obras/maias/index.html`; Ler | *Os Maias* (Projeto Gutenberg, n.º 40409) | Título da obra em itálico; título de poema entre «». |
| V355 | `obras/memorial/index.html`; Abertura | *Memorial do Convento* | Título da obra em itálico; título de poema entre «». |
| V356 | `obras/memorial/index.html`; Conhecer o autor | *Memorial do Convento*, de José SaramagoRTP Ensina (Grandes Livros, 2011), cópia no Arquivo da Internet, 35 min. O convento de Mafra, a passarola, Baltasar e Bl… | Título da obra em itálico; título de poema entre «». |
| V357 | `obras/memorial/index.html`; Um excerto do romance | Ao tocar, o vídeo carrega a partir do YouTube (Rota *Memorial do Convento*). Também podes abri-lo no YouTube. | Título da obra em itálico; título de poema entre «». |
| V358 | `obras/pessoa/index.html`; Ler | *O Guardador de Rebanhos*, XX, de Alberto Caeiro (Biblioteca) | Título da obra em itálico; título de poema entre «». |
| V359 | `obras/pessoa/index.html`; Ler | Os poemas das lições estão no Arquivo Pessoa. *O Guardador de Rebanhos*, XX, e «Tabacaria» estão também na Biblioteca. | Título da obra em itálico; título de poema entre «». |
| V360 | `obras/sermao/index.html`; Abertura | *Sermão de Santo António aos Peixes* | Título da obra em itálico; título de poema entre «». |
| V361 | `obras/sermao/index.html`; Conhecer o autor | *Sermão de Santo António aos Peixes*, de padre António VieiraRTP Ensina (Grandes Livros, 2009), 48 min. Documentário sobre o sermão pregado no Maranhão a 13 de … | Título da obra em itálico; título de poema entre «». |

## Depois de os pedidos entrarem

Um ponto associado a vários pedidos espera pela integração ou conciliação de todos os ramos que alteram o ficheiro. A revisão confirma então o texto que estiver no main.

| Ponto | Depois de entrar | Ficheiro | Correção proposta |
|---|---|---|---|
| V002 | #150 | `m1/licao-m1-f01/index.html` | Acrescentar a instituição depositária e a referência do manuscrito/reprodução. A indicação de domínio público não identifica a proveniência da imagem. Local: Cartão 1: A língua que se canta / html / legenda |
| V003 | #150 | `m1/licao-m1-f01/index.html` | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. Local: Cartão 4: Tocar e cantar chega para trovar? / html |
| V004 | #150 | `m1/licao-m1-f04/index.html` | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. Local: Cartão 13: Que faz Guilhade com «loar»? / html |
| V005 | #150 | `m1/licao-m1-f04/index.html` | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. Local: Cartão 2: Quem fala, e quem é a «senhor»? / html |
| V006 | #150 | `m1/licao-m1-f04/index.html` | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. Local: Cartão 2: Quem fala, e quem é a «senhor»? / html |
| V007 | #150 | `m1/licao-m1-f04/index.html` | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. Local: Cartão 6: Quanto vale a senhora de D. Dinis? / html |
| V008 | #150 | `m1/licao-m1-f11/index.html` | Acrescentar a instituição depositária e a referência do manuscrito/reprodução. A indicação de domínio público não identifica a proveniência da imagem. Local: Cartão 1: Ondas, gritos e grãos de trigo / html / legenda |
| V028 | #150 | `m2/licao-m2-f07/index.html` | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. Local: Cartão 8: Para entender / html |
| V044 | #150 | `m2/licao-m2-f01/index.html` | Aplicar itálico a «Farsa de Inês Pereira» no texto corrido. Local: Cartão 19: Para entender / html |
| V047 | #150 | `m2/mapa-do-modulo-m2/index.html` | Aplicar itálico a «Farsa de Inês Pereira» no texto corrido. Local: #frase |
| V092 | #144, #145, #148, #150 | `m3/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: Lírica e épica camonianas |
| V093 | #150 | `m3/licao-m3-f05/index.html` | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». Local: Cartão 14:  / p2 |
| V094 | #150 | `m3/licao-m3-f05/index.html` | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». Local: Cartão 18:  / f |
| V095 | #150 | `m3/licao-m3-f05/index.html` | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». Local: Cartão 19: Leonor e o perdigão / html |
| V096 | #150 | `m3/licao-m3-f13/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: Cartão 1: Um bicho da terra tão pequeno / html |
| V097 | #150 | `m3/licao-m3-f13/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: Cartão 27: A calçada do verso / f |
| V098 | #144, #145, #148, #150 | `m3/licao-m3-f16/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: Cartão 1: Quem disse este verso? / html |
| V099 | #144, #145, #148, #150 | `m3/licao-m3-f16/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: Cartão 2: O essencial / html |
| V100 | #144, #145, #148, #150 | `m3/licao-m3-f16/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: Cartão 2: O essencial / html |
| V101 | #150 | `m3/licao-m3-f18/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: #baralho |
| V102 | #150 | `m3/licao-m3-f18/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: Cartão 11: Quatro funções / html |
| V103 | #150 | `m3/licao-m3-f18/index.html` | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». Local: Cartão 1: Uma epopeia por dentro / html |
| V104 | #144, #145, #148, #150 | `m3/mapa-do-modulo-m3/index.html` | Aplicar itálico a «Os Lusíadas» no texto corrido. Local: #frase |
| V118 | #149 | `m4/index.html` | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». Local: Dados U / [2].pool[37].f |
| V119 | #149 | `m4/index.html` | Aplicar itálico a «Sermão de Santo António aos Peixes» no texto corrido. Local: Literatura barroca e romântica |
| V150 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Dados U / [1].pool[40].f |
| V151 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Dados U / [1].pool[40].fe[3] |
| V152 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Dados U / [1].pool[47].f |
| V153 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Dados U / [1].pool[47].o[3] |
| V154 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Dados U / [1].pool[48].pares[3][1] |
| V155 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Dados U / [2].pool[1].frase |
| V156 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Dados U / [2].pool[74].passos[3] |
| V157 | #144, #145, #148, #150 | `m5/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Narrativa do século XIX |
| V158 | #150 | `m5/licao-m5-f02/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 20: Para entender / html |
| V159 | #150 | `m5/licao-m5-f02/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 4: Introdução / html |
| V160 | #144, #145, #148, #150 | `m5/licao-m5-f08/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 3: Para entender / html |
| V161 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 10:  / f |
| V162 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 10:  / fe |
| V163 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 10:  / p |
| V164 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 2: O essencial / html |
| V165 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 3:  / f |
| V166 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html` | Aplicar itálico a «Amor de Perdição» no texto corrido. Local: Cartão 3:  / fe[3] |
| V167 | #150 | `m5/licao-m5-f10/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 1: Sombrio casarão / html |
| V168 | #150 | `m5/licao-m5-f10/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 21: O Ramalhete, no início e no fim / html |
| V169 | #150 | `m5/licao-m5-f10/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 22:  / pares[1][1] |
| V170 | #150 | `m5/licao-m5-f10/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 3: O essencial / html |
| V171 | #150 | `m5/licao-m5-f10/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 5:  / frase |
| V172 | #150 | `m5/licao-m5-f14/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 21: Para levar / html |
| V173 | #150 | `m5/licao-m5-f14/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 2: O essencial / html |
| V174 | #150 | `m5/licao-m5-f14/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 2: O essencial / html |
| V175 | #144, #145, #148, #150 | `m5/licao-m5-f15/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 12:  / passos[3] |
| V176 | #144, #145, #148, #150 | `m5/licao-m5-f15/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: Cartão 2: O essencial / html |
| V177 | #144, #145, #148, #150 | `m5/mapa-do-modulo-m5/index.html` | Aplicar itálico a «Os Maias» no texto corrido. Local: #frase |
| V188 | #149, #150 | `m6/licao-m6-f01/index.html` | Identificar a autoria da fotografia, ou declarar autoria não identificada após conferir a fonte; indicar a instituição ou reprodução consultada. Não atribuir um nome por suposição. Local: Cartão 1: O cavaleiro que encontra o nada / html / legenda |
| V204 | #144, #145, #148, #150 | `m6/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #m6-cesario-noite-inteira |
| V205 | #144, #145, #148, #150 | `m6/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Dados U / [2].pool[38].fe[3] |
| V206 | #144, #145, #148, #150 | `m6/index.html` | Aplicar itálico a «O Livro de Cesário Verde» no texto corrido. Local: Poesia Realista |
| V207 | #144, #145, #148, #150 | `m6/licao-m6-f04/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #baralho |
| V208 | #144, #145, #148, #150 | `m6/licao-m6-f04/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 5: Para entender / html |
| V209 | #150 | `m6/licao-m6-f05/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #baralho |
| V210 | #150 | `m6/licao-m6-f05/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 15:  / frase |
| V211 | #150 | `m6/licao-m6-f05/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 1: Palavras com passado / html |
| V212 | #150 | `m6/licao-m6-f06/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 16:  / html |
| V213 | #150 | `m6/licao-m6-f06/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 1: «Ave-Marias» / html |
| V214 | #150 | `m6/licao-m6-f06/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 21: O que vê e o que evoca / html |
| V215 | #150 | `m6/licao-m6-f06/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 2: O essencial / html |
| V216 | #150 | `m6/licao-m6-f06/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 3: I: «Ave-Marias» (na íntegra) / html |
| V217 | #150 | `m6/licao-m6-f07/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #baralho |
| V218 | #150 | `m6/licao-m6-f07/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 1: Da «Noite Fechada» às «Horas Mortas» / html |
| V219 | #150 | `m6/licao-m6-f07/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 26:  / html |
| V220 | #144, #145, #148, #150 | `m6/licao-m6-f08/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #baralho |
| V221 | #144, #145, #148, #150 | `m6/licao-m6-f08/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 2: O essencial / html |
| V222 | #144, #145, #148, #150 | `m6/licao-m6-f09/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #baralho |
| V223 | #144, #145, #148, #150 | `m6/licao-m6-f09/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 5:  / fe[3] |
| V224 | #144, #145, #148, #150 | `m6/licao-m6-f11/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 6:  / f |
| V225 | #144, #145, #148, #150 | `m6/licao-m6-f11/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 7:  / f |
| V226 | #144, #145, #148, #150 | `m6/licao-m6-f11/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 9:  / f |
| V227 | #150 | `m6/licao-m6-f12/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 2: Manhã e contraste / html |
| V228 | #150 | `m6/licao-m6-f12/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 2: Manhã e contraste / html |
| V229 | #150 | `m6/licao-m6-f12/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 5: A hipótese do artista / html |
| V230 | #150 | `m6/licao-m6-f12/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 5: A hipótese do artista / html |
| V231 | #150 | `m6/licao-m6-f12/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 9: Do olhar às mãos / html |
| V232 | #150 | `m6/licao-m6-f12/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 9: Do olhar às mãos / html |
| V233 | #150 | `m6/licao-m6-f13/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 2: Quem é chamado? / html |
| V234 | #150 | `m6/licao-m6-f13/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 5: A mudança de tom / html |
| V235 | #150 | `m6/licao-m6-f13/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 5: A mudança de tom / html |
| V236 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #frase |
| V237 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html` | Aplicar itálico a «O Livro de Cesário Verde» no texto corrido. Local: #frase |
| V238 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #frase |
| V239 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: #frase |
| V240 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html` | Aplicar itálico a «O Livro de Cesário Verde» no texto corrido. Local: #frase |
| V241 | #144, #145, #148, #150 | `tarefas/m6-u2/aquecimento/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Cartão 1: A cidade que Cesário viu / html |
| V242 | #144, #145, #148, #150 | `tarefas/m6-u2/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Dossiê do tema B |
| V243 | #144, #145, #148, #150 | `tarefas/m6-u2/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Dossiê do tema B |
| V244 | #144, #145, #148, #150 | `tarefas/m6-u2/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Tema B Cesário nos dias de hoje |
| V247 | #149 | `m7/licao-m7-f34/index.html` | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. Local: Cartão 32: Muda o lugar, mantém a técnica / html |
| V265 | #145, #148, #150 | `m8/licao-m8-f04/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 25: Adeus / html |
| V266 | #145, #148, #150 | `m8/licao-m8-f05/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 24: A verdade histórica / html |
| V267 | #145, #148, #150 | `m8/licao-m8-f10/index.html` | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. Local: Cartão 3: Da cena pintada à palavra dirigida aos filhos / html |
| V269 | #143, #145, #148, #150 | `m9/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Dados U / [2].pool[45].f |
| V270 | #143, #145, #148, #150 | `m9/index.html` | Aplicar itálico a «O Sentimento dum Ocidental» no texto corrido. Local: Dados U / [2].pool[45].pares[3][1] |
| V271 | #148, #150 | `m9/licao-m9-f01/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Cartão 1: Um convento, uma promessa / html |
| V272 | #148, #150 | `m9/licao-m9-f03/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Cartão 5: Para entender / html |
| V273 | #148, #150 | `m9/licao-m9-f03/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Cartão 5: Para entender / html |
| V274 | #145, #148, #150 | `m9/licao-m9-f05/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Cartão 2: O essencial / html |
| V275 | #148, #150 | `m9/licao-m9-f11/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Cartão 13: Para levar / html |
| V276 | #148, #150 | `m9/licao-m9-f12/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Cartão 13: Para levar / html |
| V277 | #148, #150 | `m9/licao-m9-f13/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Cartão 23: Para levar / html |
| V282 | #145, #148, #150 | `tarefas/m9-u2/index.html` | Aplicar itálico a «Memorial do Convento» no texto corrido. Local: Textos e condições de consulta |

## Validação

Resultados finais a preencher depois da bateria completa.
