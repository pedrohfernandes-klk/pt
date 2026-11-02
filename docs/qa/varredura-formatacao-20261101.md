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

## Contagem

| Tipo | Corrigidos | Conformes | Adiados |
|---|---:|---:|---:|
| Versos em linha corrida | 19 | 0 | 7 |
| Crédito de imagem incompleto | 3 | 0 | 3 |
| Travessão | 88 | 0 | 0 |
| Vocabulário da casa | 17 | 0 | 5 |
| Aspas não angulares | 21 | 0 | 0 |
| Título sem itálico | 88 | 13 | 81 |
| Citação em bloco sem aspas | 2 | 0 | 13 |
| Reticências | 1 | 0 | 0 |

## Aplicação por módulo

O manifesto conserva o antes e depois integral de cada troca. As tabelas usam os excertos da varredura original. ↵ representa uma quebra de verso. «Conforme» corrige a classificação do achado, sem alterar a passagem.

### M1

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V001 | `m1/gram-coordenadas/index.html`; Dados E / passos[1].html | B. «fostes-vos queixar que vos nunca louv'en[o] meu cantar; / ⟪mais⟫ ora quero fazer um cantar» (Guilhade) | B. «fostes-vos queixar ↵ que vos nunca louv'en[o] meu cantar; ↵ mais ora quero fazer um cantar» (Guilhade) |
| V009 | `m1/flores-verde-pino/index.html`; Dados E / passos[1].html | u é? — onde está? · pino — pinheiro · pôs conmigo — combinou comigo · preguntades — perguntais · vosco — convosco · ant'o prazo saído — antes de acabar o prazo | u é: onde está ↵ pino: pinheiro ↵ pôs conmigo: combinou comigo ↵ preguntades: perguntais ↵ vosco: convosco ↵ ant'o prazo saído: antes de acabar o prazo |
| V010 | `m1/gram-complementos/index.html`; Dados E / passos[1].html | complemento — o que uma palavra exige para o seu sentido ficar completo · modificador — o que se junta a uma palavra sem ser exigido | complemento: o que uma palavra exige para o seu sentido ficar completo ↵ modificador: o que se junta a uma palavra sem ser exigido |
| V011 | `m1/gram-coordenadas/index.html`; Dados E / emblemas[1][3] | Distingues somar, opor e concluir — e mostraste em cada caso que nenhuma oração está dentro da outra. | Distingues somar, opor e concluir, e mostraste em cada caso que nenhuma oração está dentro da outra. |
| V012 | `m1/gram-coordenadas/index.html`; Dados E / passos[1].html | nem — e não · mais — mas · Duas orações estão coordenadas quando se ligam sem que nenhuma esteja dentro da outra. | nem: e não ↵ mais: mas. Duas orações estão coordenadas quando se ligam sem que nenhuma esteja dentro da outra. |
| V013 | `m1/gram-fonologia/index.html`; Dados E / passos[1].html | Desaparece — ASA: início, aférese (alevantada > levantada: vogal inicial); interior, síncope (malu > mau: [l]); fim, apócope (amare > amar: vogal final). | Desaparece (ASA): início, aférese (alevantada > levantada: vogal inicial); interior, síncope (*malu* > mau: [l]); fim, apócope (*amare* > amar: vogal final). |
| V014 | `m1/gram-fonologia/index.html`; Dados E / passos[1].html | Entra — PEP: início, prótese (scribere > escrever: vogal inicial); interior, epêntese (humile > humilde: [d]); fim, paragoge (ante > antes: consoante final). | Entra (PEP): início, prótese (*scribere* > escrever: vogal inicial); interior, epêntese (*humile* > humilde: [d]); fim, paragoge (*ante* > antes: consoante final). |
| V015 | `m1/gram-fonologia/index.html`; Dados E / passos[1].html | processo fonológico — uma mudança regular de sons, do latim ao português · síncope — cai um som no meio · sonorização — um som surdo (p, t, c) passa a sonoro (b, d, g) · prótese — entra um som no início · apócope — cai um som no fim · parag | processo fonológico: uma mudança regular de sons, do latim ao português ↵ síncope: cai um som no meio ↵ sonorização: um som surdo (p, t, c) passa a sonoro (b, d, g) ↵ prótese: entra um som no início ↵ apócope: cai um som no fim |
| V016 | `m1/guilhade-dona-fea/index.html`; Dados E / passos[1].html | loar — louvar · prez — valor · nom fal — não falta · comprida de bem — cheia de qualidades · fea — feia · sandia — louca · escárnio — diz mal com palavras cobertas (duplo sentido) · maldizer — diz mal descobertamente, muitas vezes nomeando | loar: louvar ↵ prez: valor ↵ nom fal: não falta ↵ comprida de bem: cheia de qualidades ↵ fea: feia ↵ sandia: louca ↵ escárnio: diz mal com palavras cobertas (duplo sentido) ↵ maldizer: diz mal descobertamente, muitas vezes nomeando o visado |
| V017 | `m1/guilhade-dona-fea/index.html`; Dados E / passos[3].opcoes[1][3] | Não sabemos se é, e não é isso que faz a troça: é o jogo com o género. | Não sabemos se é, e não é isso que faz a troça: é o contraste com o género. |
| V018 | `m1/lisboa-cercada/index.html`; Dados E / passos[1].html | bacinetes — capacetes · abastaria — bastaria · esgravatando — remexendo a terra · mantimento — alimento | bacinetes: capacetes ↵ abastaria: bastaria ↵ esgravatando: remexendo a terra ↵ mantimento: alimento |
| V019 | `m1/matam-o-mestre/index.html`; Dados E / passos[1].html | percebido — combinado · rijamente — com força · arruído — alvoroço · em logo de — em lugar de · hu — onde · escusar — evitar | percebido: combinado ↵ rijamente: com força ↵ arruído: alvoroço ↵ em logo de: em lugar de ↵ hu: onde ↵ escusar: evitar |
| V020 | `m1/mendinho-ermida/index.html`; Dados E / passos[1].html | sedia-m'eu — estava eu · cercarom-mi — cercaram-me · som — são · atendendo — esperando · nom hei i — não tenho ali · fremosa — formosa | sedia-m'eu: estava eu ↵ cercarom-mi: cercaram-me ↵ som: são ↵ atendendo: esperando ↵ nom hei i: não tenho ali ↵ fremosa: formosa |
| V021 | `m1/ondas-vigo/index.html`; Dados E / emblemas[2][3] | Já percebeste o jogo das repetições. Volta atrás e afina. | Já percebeste o efeito das repetições. Volta atrás e afina. |
| V022 | `m1/ondas-vigo/index.html`; Dados E / passos[1].html | levado — agitado · verrá — virá · cedo — em breve | levado: agitado ↵ verrá: virá ↵ cedo: em breve |
| V023 | `m1/tempo-da-flor/index.html`; Dados E / passos[1].html | proençaes — trovadores da Provença · soem — costumam · mais — mas · coita — sofrimento de amor · levar — suportar | proençaes: trovadores da Provença ↵ soem: costumam ↵ mais: mas ↵ coita: sofrimento de amor ↵ levar: suportar |
| V024 | `tarefas/m1-u2/aquecimento/index.html`; Cartão 4:  / frase | A técnica diz: “Abre a porta.” (fala documentada) | A técnica diz: «Abre a porta.» (fala documentada) |

### M2

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V025 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | A. «Se vos eu vejo cantar / Eu vos farei assoviar» (o Escudeiro, casado) | A. «Se vos eu vejo cantar ↵ Eu vos farei assoviar» (o Escudeiro, casado) |
| V026 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | B. «Já vos preguei as janelas, / Por que não vos ponhais nelas» (o Escudeiro) | B. «Já vos preguei as janelas, ↵ Por que não vos ponhais nelas» (o Escudeiro) |
| V027 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | C. «Quero tomar por esposo / Quem se tenha por ditoso» (Inês, viúva) | C. «Quero tomar por esposo ↵ Quem se tenha por ditoso» (Inês, viúva) |
| V029 | `m2/licao-m2-f12/index.html`; Cartão 4: Uma credencial recusada / html | Anjo: «Não se embarca tirania / neste batel divinal.» | Anjo: «Não se embarca tirania ↵ neste batel divinal.» |
| V030 | `m2/licao-m2-f12/index.html`; Cartão 4: Uma credencial recusada / html | Fidalgo: «Sou fidalgo de solar, / é bem que me recolhais.» | Fidalgo: «Sou fidalgo de solar, ↵ é bem que me recolhais.» |
| V031 | `m2/licao-m2-f13/index.html`; Cartão 2: Um ofício não é uma condenação / html | Diabo: «Tu roubaste bem trint’anos / o povo com teu mester.» | Diabo: «Tu roubaste bem trint’anos ↵ o povo com teu mester.» |
| V032 | `m2/licao-m2-f13/index.html`; Cartão 2: Um ofício não é uma condenação / html | Sapateiro: «Como poderá isso ser, / confessado e comungado?!...» | Sapateiro: «Como poderá isso ser, ↵ confessado e comungado?!...» |
| V033 | `m2/licao-m2-f13/index.html`; Cartão 4: A resposta que muda o critério / html | Diabo: «Ouvir missa, então roubar, / é caminho per’aqui.» | Diabo: «Ouvir missa, então roubar, ↵ é caminho per’aqui.» |
| V034 | `m2/licao-m2-f13/index.html`; Cartão 4: A resposta que muda o critério / html | Sapateiro: «Quantas missas eu ouvi, / nom me hão elas de prestar?» | Sapateiro: «Quantas missas eu ouvi, ↵ nom me hão elas de prestar?» |
| V035 | `m2/gram-formacao/index.html`; Dados E / passos[1].html | derivação — formar uma palavra a partir de outra, com um afixo · prefixo — o afixo antes da base (des-, re-, in-) · sufixo — o afixo depois da base (-mento, -eiro, -oso) · teste — tira o afixo: a base tem de existir sozinha | derivação: formar uma palavra a partir de outra, com um afixo ↵ prefixo: o afixo antes da base (des-, re-, in-) ↵ sufixo: o afixo depois da base (-mento, -eiro, -oso) ↵ teste: tira o afixo, e a base tem de existir sozinha |
| V036 | `m2/gram-oracoes-farsa/index.html`; Dados E / passos[1].html | coordenada — fica ao lado da outra, ligada por «e», «mas», «ou», «logo», «pois» · subordinada — ocupa um lugar dentro da outra: de tempo, condição, causa, fim; de nome (relativa); de complemento (completiva, ou relativa sem nome antes, com | coordenada: fica ao lado da outra, ligada por «e», «mas», «ou», «logo», «pois» ↵ subordinada: ocupa um lugar dentro da outra, com valor de tempo, condição, causa ou fim, de nome (relativa), de complemento (completiva, ou relativa sem nome antes, com «quem»: |
| V037 | `m2/guia-da-tarefa-m2/index.html`; Guia da tarefa | 1. Apreciação crítica da Farsa de Inês Pereira no teatroindividual; uma aula | 1. Apreciação crítica da *Farsa de Inês Pereira* no teatroindividual; uma aula |
| V038 | `m2/ines-escolhe/index.html`; Dados E / fontes[1][1] | Gil Vicente, Farsa de Inês Pereira, texto integral (Wikisource) | Gil Vicente, *Farsa de Inês Pereira*, texto integral (Wikisource) |
| V039 | `m2/ines-escolhe/index.html`; Dados E / marca | Ler a fundo · Farsa de Inês Pereira | Ler a fundo · *Farsa de Inês Pereira* |
| V040 | `m2/ines-escolhe/index.html`; Dados E / subtitulo | Gil Vicente, Farsa de Inês Pereira, 1523, uma história com ramos | Gil Vicente, *Farsa de Inês Pereira*, 1523, uma história com ramos |
| V041 | `m2/ines-escolher/index.html`; Dados E / emblemas[1][3] | Apanhaste a ironia e o jogo dos provérbios. | Apanhaste a ironia e a oposição dentro dos provérbios. |
| V042 | `m2/ines-escolher/index.html`; Dados E / passos[1].html | siso mero — bom senso · folão — fogoso, indomável · Nero — imperador romano, símbolo de crueldade | siso mero: bom senso ↵ folão: fogoso, indomável ↵ Nero: imperador romano, símbolo de crueldade |
| V043 | `m2/ines-panela/index.html`; Dados E / passos[1].html | lavrar — bordar · aviamento — arranjo de vida (aqui, casamento) · caramujo — caracol · bugia — macaca | lavrar: bordar ↵ aviamento: arranjo de vida (aqui, casamento) ↵ caramujo: caracol ↵ bugia: macaca |
| V045 | `m2/licao-m2-f12/index.html`; #baralho | EPI · Português. Leitura complementar vicentina; Farsa de Inês Pereira permanece o núcleo do módulo. Contextualização e exercícios nossos; recortes identificados. O progresso fica neste aparelho. | EPI · Português. Leitura complementar vicentina; *Farsa de Inês Pereira* permanece o núcleo do módulo. Contextualização e exercícios nossos; recortes identificados. O progresso fica neste aparelho. |
| V046 | `m2/licao-m2-f13/index.html`; #baralho | EPI · Português. Leitura complementar vicentina; Farsa de Inês Pereira permanece o núcleo do módulo. Contextualização e exercícios nossos; recortes identificados. O progresso fica neste aparelho. | EPI · Português. Leitura complementar vicentina; *Farsa de Inês Pereira* permanece o núcleo do módulo. Contextualização e exercícios nossos; recortes identificados. O progresso fica neste aparelho. |
| V048 | `m2/portefolio-do-modulo-m2/index.html`; A lista de verificação | Tarefa 1, «Apreciação crítica da Farsa de Inês Pereira no teatro»: o produto entregue (ou a ligação) e uma linha: o que fiz, o que corrigi depois da devolução. | Tarefa 1, «Apreciação crítica da *Farsa de Inês Pereira* no teatro»: o produto entregue (ou a ligação) e uma linha: o que fiz, o que corrigi depois da devolução. |
| V049 | `m2/visita-farsa-de-ines-pereira-no-teatro/index.html`; A farsa em cena | Farsa de Inês Pereira, no teatro | *Farsa de Inês Pereira*, no teatro |
| V050 | `m2/visita-farsa-de-ines-pereira-no-teatro/index.html`; Abertura | A farsa em cena: Farsa de Inês Pereira, no teatro | A farsa em cena: *Farsa de Inês Pereira*, no teatro |
| V051 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 4:  / frase | A oração “para que a mesa ficasse livre” é [1]. | A oração *para que a mesa ficasse livre* é [1]. |
| V052 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 4:  / p | Frase criada: “Arrumei os livros para que a mesa ficasse livre.” Classifica a oração iniciada por para que. | Frase criada: *Arrumei os livros para que a mesa ficasse livre.* Classifica a oração iniciada por *para que*. |
| V053 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 5:  / fe[3] | A posição não classifica a oração: “Para que a mesa ficasse livre, arrumei os livros.” continua a ser final. Confirmam-na o conector e o conjuntivo. | A posição não classifica a oração: *Para que a mesa ficasse livre, arrumei os livros.* continua a ser final. Confirmam-na o conector e o conjuntivo. |
| V054 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 5:  / p | Que justificação aponta, na frase criada, os traços que confirmam a classificação de “para que a mesa ficasse livre”? | Que justificação aponta, na frase criada, os traços que confirmam a classificação de *para que a mesa ficasse livre*? |
| V055 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[1][1] | Comparação: “A notícia caiu como água gelada.” | Comparação: *A notícia caiu como água gelada.* |
| V056 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[2][1] | Antítese: “Sorrio por fora, choro por dentro.” | Antítese: *Sorrio por fora, choro por dentro.* |
| V057 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[3][1] | Enumeração: “Testes, treinos, recados, turnos.” | Enumeração: *Testes, treinos, recados, turnos.* |
| V058 | `tarefas/m2-u1/aquecimento/index.html`; Cartão 7:  / pares[4][1] | Interrogação retórica: “De que serve correr?” | Interrogação retórica: *De que serve correr?* |
| V059 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 10:  / apoio | Cena inventada: a Rita gaba o bolo que trouxe; o Tiago diz, à parte, para o público: “Está queimado por baixo.” | Cena inventada: a Rita gaba o bolo que trouxe; o Tiago diz, à parte, para o público: «Está queimado por baixo.» |
| V060 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 10:  / p2 | Quem diz “Está queimado por baixo”, e para quem? Escolhe a identificação certa da prova. | Quem diz «Está queimado por baixo», e para quem? Escolhe a identificação certa da prova. |
| V061 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 4:  / frase | A oração “que está na mesa” é [1]. | A oração *que está na mesa* é [1]. |
| V062 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 4:  / p | Frase criada: “O livro que está na mesa pertence à biblioteca.” Classifica a oração iniciada por que. | Frase criada: *O livro que está na mesa pertence à biblioteca.* Classifica a oração iniciada por *que*. |
| V063 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 4:  / p2 | Na frase criada “O livro que está na mesa pertence à biblioteca”, como se classifica a oração “que está na mesa”? | Na frase criada *O livro que está na mesa pertence à biblioteca*, como se classifica a oração *que está na mesa*? |
| V064 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 5:  / p | Cena inventada: a Sara diz que vai subir a serra de sandálias. O guia diz, à parte: “Pés sem botas, serra sem fim.” O que anuncia o comentário? | Cena inventada: a Sara diz que vai subir a serra de sandálias. O guia diz, à parte: «Pés sem botas, serra sem fim.» O que anuncia o comentário? |
| V065 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 5:  / p2 | Numa cena inventada, a Sara quer subir a serra de sandálias e o guia diz só para o público: “Pés sem botas, serra sem fim.” Que leitura respeita o que o comentário anuncia? | Numa cena inventada, a Sara quer subir a serra de sandálias e o guia diz só para o público: «Pés sem botas, serra sem fim.» Que leitura respeita o que o comentário anuncia? |
| V066 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 7:  / pares[1][1] | Diz “Sou pontual!” e chega quando a sessão acabou. | Diz «Sou pontual!» e chega quando a sessão acabou. |
| V067 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 7:  / pares[2][1] | Diz “Trago o guião” e entrega-o logo à colega. | Diz «Trago o guião» e entrega-o logo à colega. |
| V068 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 7:  / pares[4][1] | Antes do ensaio, admite “Costumo faltar sem avisar.” | Antes do ensaio, admite «Costumo faltar sem avisar.» |
| V069 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 8:  / p | Frase criada para ensaio: “Já / cheguei.” (com alívio). A barra marca uma pausa. O que indicam os parênteses? | Frase criada para ensaio: *Já / cheguei.* (com alívio). A barra marca uma pausa. O que indicam os parênteses? |
| V070 | `tarefas/m2-u2/aquecimento/index.html`; Cartão 8:  / p2 | Na frase criada “Já / cheguei.” (com alívio), a pausa já está na barra. Que informação acrescentam os parênteses? | Na frase criada *Já / cheguei.* (com alívio), a pausa já está na barra. Que informação acrescentam os parênteses? |

### M3

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V071 | `m3/gram-anafora/index.html`; Dados E / passos[1].html | A. «Este rende munidas fortalezas, / Faz tredores e falsos os amigos» (VIII, 98). Duas estâncias antes, o Poeta falou do «vil interesse e sede inimiga / Do dinheiro». | A. «Este rende munidas fortalezas, ↵ Faz tredores e falsos os amigos» (VIII, 98). Duas estâncias antes, o Poeta falou do «vil interesse e sede inimiga ↵ Do dinheiro». |
| V072 | `m3/gram-anafora/index.html`; Dados E / passos[1].html | B. «Que as Ninfas do Oceano, tão formosas, / Tétis e a ilha angélica pintada, / Outra coisa não é que as deleitosas / Honras […] Estes são os deleites desta ilha» (IX, 89). | B. «Que as Ninfas do Oceano tão formosas, ↵ Tethys, e a ilha angélica pintada, ↵ Outra coisa não é que as deleitosas ↵ Honras […] ↵ Estes são os deleites desta ilha» (IX, 89). |
| V073 | `m3/arte-estima/index.html`; Dados E / passos[1].html | douto e ciente — culto e sábio · prezado — estimado · troncos nobres — linhagens · zebelinos — peles de zibelina (luxo) · forjado aço — armadura | douto e ciente: culto e sábio ↵ prezado: estimado ↵ troncos nobres: linhagens ↵ zebelinos: peles de zibelina (luxo) ↵ forjado aço: armadura |
| V074 | `m3/bicho-da-terra/index.html`; Dados E / passos[1].html | apercebida — à espreita · avorrecida — detestável · rende — faz render-se · tredores — traidores · deprava — corrompe | apercebida: à espreita ↵ avorrecida: detestável ↵ rende: faz render-se ↵ tredores: traidores ↵ deprava: corrompe |
| V075 | `m3/camoes-alma/index.html`; Dados E / passos[1].html | gentil — nobre · assento etéreo — céu · se consente — é permitida · roga — pede | gentil: nobre ↵ assento etéreo: céu ↵ se consente: é permitida ↵ roga: pede |
| V076 | `m3/camoes-alma/index.html`; Dados E / passos[6].pergunta | Qual destes pares de versos faz o jogo «lá» e «cá» com algo teu, sem copiar o soneto? | Qual destes pares de versos usa o contraste entre «lá» e «cá» para falar de algo teu, sem copiar o soneto? |
| V077 | `m3/camoes-barbara/index.html`; Dados E / passos[1].html | o povo vão — a gente comum, sem juízo · perde opinião — perde a convicção · leda — alegre · siso — juízo · bárbara — estrangeira, «selvagem» (jogo com o nome) | o povo vão: a gente comum, sem juízo ↵ perde opinião: perde a convicção ↵ leda: alegre ↵ siso: juízo ↵ bárbara: estrangeira, «selvagem» (duplo sentido do nome) |
| V078 | `m3/camoes-barbara/index.html`; Dados E / passos[1].html | eda — alegre · siso — juízo · bárbara — estrangeira, «selvagem» (jogo com o nome) | leda: alegre ↵ siso: juízo ↵ bárbara: estrangeira, «selvagem» (duplo sentido do nome) |
| V079 | `m3/camoes-barbara/index.html`; Dados E / passos[4].retorno | Elogio, jogo de palavras e recusa do preconceito, tudo em versos de cinco sílabas. | Elogio, duplo sentido e recusa do preconceito, tudo em versos de cinco sílabas. |
| V080 | `m3/camoes-desconcerto/index.html`; Dados E / passos[1].html | desconcerto — desordem, falta de harmonia · sobejaram — foram demais | desconcerto: desordem, falta de harmonia ↵ sobejaram: foram demais |
| V081 | `m3/camoes-invocacoes/index.html`; Dados E / passos[1].html | Tágides — ninfas do Tejo · grandíloquo — elevado, solene · nô mais — não mais · destemperada — desafinada | Tágides: ninfas do Tejo ↵ grandíloquo: elevado, solene ↵ nô mais: não mais ↵ destemperada: desafinada |
| V082 | `m3/camoes-leonor/index.html`; Dados E / passos[1].html | verdura — campo verde · testo — tampa · escarlata — tecido vermelho · sainho — casaco curto · vasquinha de cote — saia de uso diário | verdura: campo verde ↵ testo: tampa ↵ escarlata: tecido vermelho ↵ sainho: casaco curto ↵ vasquinha de cote: saia de uso diário |
| V083 | `m3/camoes-perdigao/index.html`; Dados E / passos[1].html | perdigão — macho da perdiz · pena — pluma; sofrimento · desasado — sem asas · penado — que sofre | perdigão: macho da perdiz ↵ pena: pluma e sofrimento (duplo sentido) ↵ desasado: sem asas ↵ penado: que sofre |
| V084 | `m3/camoes-perdigao/index.html`; Dados E / passos[2].opcoes[2][3] | Perde uma, ganha a outra: é o jogo do poema inteiro. | Perde uma, ganha a outra: é o duplo sentido do poema inteiro. |
| V085 | `m3/camoes-restelo-ramos/index.html`; Dados E / fontes[1][1] | Luís de Camões, Os Lusíadas, texto integral (oslusiadas.org) | Luís de Camões, *Os Lusíadas*, texto integral (oslusiadas.org) |
| V086 | `m3/camoes-restelo-ramos/index.html`; Dados E / marca | Ler a fundo · Os Lusíadas | Ler a fundo · *Os Lusíadas* |
| V087 | `m3/camoes-restelo-ramos/index.html`; Dados E / subtitulo | Luís de Camões, Os Lusíadas, 1572, uma história com ramos | Luís de Camões, *Os Lusíadas*, 1572, uma história com ramos |
| V088 | `m3/camoes-sobolos/index.html`; Dados E / passos[1].html | sôbolos — sobre os · manado — que correu · Babilónia — o lugar do desterro · Sião — a terra de origem · despois d'acordado — depois de acordado | sôbolos: sobre os ↵ manado: que correu ↵ Babilónia: o lugar do desterro ↵ Sião: a terra de origem ↵ despois d'acordado: depois de acordado |
| V089 | `m3/espada-pena/index.html`; Dados E / passos[1].html | batel — barco pequeno · peregrinando — andando errante · Mavórcios — da guerra · Canace — figura mitológica que escreveu uma carta antes de morrer · ócio ignavo — preguiça | batel: barco pequeno ↵ peregrinando: andando errante ↵ Mavórcios: da guerra ↵ Canace: figura mitológica que escreveu uma carta antes de morrer ↵ ócio ignavo: preguiça |
| V090 | `m3/gram-anafora/index.html`; Dados E / passos[1].html | retoma — uma palavra aponta para outra que veio antes · anáfora como figura — a repetição de uma palavra no início de versos seguidos (também em VIII, 98: Este… Este… Este…) | retoma: uma palavra aponta para outra que veio antes ↵ anáfora como figura: a repetição de uma palavra no início de versos seguidos (também em VIII, 98: Este… Este… Este…) |
| V091 | `m3/gram-modalidade/index.html`; Dados E / passos[1].html | epistémica — grau de certeza: talvez, deve estar, é certo que · deôntica — obrigação, permissão, pedido, ordem: tem de, pode, dai-me · apreciativa — avaliação de quem fala: infelizmente, que belo! | epistémica: grau de certeza (talvez, deve estar, é certo que) ↵ deôntica: obrigação, permissão, pedido, ordem (tem de, pode, dai-me) ↵ apreciativa: avaliação de quem fala (infelizmente, que belo!) |
| V105 | `m3/maquina-mundo/index.html`; Dados E / passos[1].html | lume — luz · orbes — esferas · verga — vara · derredor — à volta · limada — polida · engenho — inteligência | lume: luz ↵ orbes: esferas ↵ verga: vara ↵ derredor: à volta ↵ limada: polida ↵ engenho: inteligência |
| V106 | `m3/painel-m3-f10/index.html`; Cartão 14:  / p | No ensaio, cada citação de Os Lusíadas leva o canto e a estância, como «X, 145». | No ensaio, cada citação de *Os Lusíadas* leva o canto e a estância, como «X, 145». |
| V107 | `m3/questionarios/index.html`; #indice | 3Os Lusíadasfechado | 3*Os Lusíadas*fechado |

### M4

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V108 | `m4/frei-luis-ramos/index.html`; Dados E / marca | Ler a fundo · Frei Luís de Sousa | Ler a fundo · *Frei Luís de Sousa* |
| V109 | `m4/frei-luis-ramos/index.html`; Dados E / subtitulo | Almeida Garrett, Frei Luís de Sousa, 1843, uma história com ramos | Almeida Garrett, *Frei Luís de Sousa*, 1843, uma história com ramos |
| V110 | `m4/garrett-fogo/index.html`; Dados E / passos[1].html | haveres — bens, riqueza · atear — acender · o texto entre parênteses é a didascália: o que se faz em palco | haveres: bens, riqueza ↵ atear: acender. O texto entre parênteses é a didascália: o que se faz em palco. |
| V111 | `m4/garrett-nome/index.html`; Dados E / passos[1].html | ânimo — coragem · honra — aqui, o bom nome perante os outros | ânimo: coragem ↵ honra: aqui, o bom nome perante os outros |
| V112 | `m4/garrett-nome/index.html`; Dados E / passos[2].retorno | O que está em jogo não é a vida: é o nome, isto é, o lugar de Maria no mundo. | O que está em causa não é a vida: é o nome, isto é, o lugar de Maria no mundo. |
| V113 | `m4/gram-atos-fala/index.html`; Dados E / passos[1].html | assertivo — afirma alguma coisa como verdadeira · diretivo — leva o outro a agir · compromissivo — compromete quem fala · expressivo — exprime um estado de quem fala · declarativo — muda a realidade ao ser dito por quem pode | assertivo: afirma alguma coisa como verdadeira ↵ diretivo: leva o outro a agir ↵ compromissivo: compromete quem fala ↵ expressivo: exprime um estado de quem fala ↵ declarativo: muda a realidade ao ser dito por quem pode |
| V114 | `m4/gram-coesao/index.html`; Dados E / passos[1].html | coesão gramatical — pronomes e demonstrativos que retomam, conectores que ligam · coesão lexical — a palavra repetida, o sinónimo, a expressão equivalente · coerência — o texto faz sentido e avança | coesão gramatical: pronomes e demonstrativos que retomam, conectores que ligam ↵ coesão lexical: a palavra repetida, o sinónimo, a expressão equivalente ↵ coerência: o texto faz sentido e avança |
| V115 | `m4/gram-deiticos/index.html`; Dados E / passos[1].html | deítico pessoal — eu, tu, vós, meu, teu · deítico espacial — aqui, ali, este, aquele · deítico temporal — hoje, agora, amanhã, este mês · referente — aquilo para que a palavra aponta | deítico pessoal: eu, tu, vós, meu, teu ↵ deítico espacial: aqui, ali, este, aquele ↵ deítico temporal: hoje, agora, amanhã, este mês ↵ referente: aquilo para que a palavra aponta |
| V116 | `m4/guia-da-tarefa-m4/index.html`; Guia da tarefa | 1. Um peixe de hoje2. Discurso no abrigo3. Apreciação crítica de Frei Luís de Sousa no teatro | 1. Um peixe de hoje2. Discurso no abrigo3. Apreciação crítica de *Frei Luís de Sousa* no teatro |
| V117 | `m4/guia-da-tarefa-m4/index.html`; Tarefa 3. Apreciação crítica de Frei Luís de Sousa no teatro | Tarefa 3. Apreciação crítica de Frei Luís de Sousa no teatro | Tarefa 3. Apreciação crítica de *Frei Luís de Sousa* no teatro |
| V120 | `m4/licao-m4-f20/index.html`; Cartão 11: O que recordas com segurança? / html | TPC: Frei Luís de Sousaaa, de Raquel Castro | TPC: *Frei Luís de Sousaaa*, de Raquel Castro |
| V121 | `m4/mapa-do-modulo-m4/index.html`; #frase | Frei Luís de Sousa, lista de personagens da primeira edição (1844). Domínio público. Lição M4-F08 | *Frei Luís de Sousa*, lista de personagens da primeira edição (1844). Domínio público. Lição M4-F08 |
| V122 | `m4/mapa-do-modulo-m4/index.html`; #frase | Sermão de Santo António aos Peixes, em Sermoens (Lisboa, 1682). Domínio público. Lição M4-F01 | *Sermão de Santo António aos Peixes*, em Sermoens (Lisboa, 1682). Domínio público. Lição M4-F01 |
| V123 | `m4/olhar-lupi/index.html`; Dados E / marca | Olhar · M4 Frei Luís de Sousa | Olhar · M4 *Frei Luís de Sousa* |
| V124 | `m4/portefolio-do-modulo-m4/index.html`; A lista de verificação | O que se perde quando se perde o nome? Síntese de duas linhas na folha da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín | O que se perde quando se perde o nome? Síntese de duas linhas no papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín |
| V125 | `m4/portefolio-do-modulo-m4/index.html`; A lista de verificação | se defende uma regra em dois minutos? Síntese de duas linhas na folha da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín | se defende uma regra em dois minutos? Síntese de duas linhas no papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín |
| V126 | `m4/portefolio-do-modulo-m4/index.html`; A lista de verificação | zer a verdade a quem não a quer ouvir? Síntese de duas linhas na folha da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín | zer a verdade a quem não a quer ouvir? Síntese de duas linhas no papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra sín |
| V127 | `m4/questionarios/index.html`; #indice | 6Frei Luís de Sousafechado | 6*Frei Luís de Sousa*fechado |
| V128 | `m4/tradutor-detetive/index.html`; Dados E / passos[6].opcoes[2][3] | Reescreveu a frase inteira; o jogo era mudar uma palavra. | Reescreveu a frase inteira; o desafio era mudar uma palavra. |
| V129 | `m4/vieira-auditorio/index.html`; Dados E / passos[1].html | auditório — público · preservar dele — proteger do mal | auditório: público ↵ preservar dele: proteger do mal |
| V130 | `m4/vieira-peixes/index.html`; Dados E / passos[1].html | costados — lados do corpo · desferram — largam · capelo — capuz · limos — algas | costados: lados do corpo ↵ desferram: largam ↵ capelo: capuz ↵ limos: algas |
| V131 | `m4/vieira-praia/index.html`; Dados E / passos[1].html | Arimino — Rimini, cidade de Itália · hereges — os que se afastam da doutrina da Igreja · dissimular — fingir que não é nada | Arimino: Rimini, cidade de Itália ↵ hereges: os que se afastam da doutrina da Igreja ↵ dissimular: fingir que não é nada |
| V132 | `m4/vieira-sal/index.html`; Dados E / passos[1].html | ofício — função, dever · corrupção — aqui, o mal moral que se espalha | ofício: função, dever ↵ corrupção: aqui, o mal moral que se espalha |
| V133 | `m4/visita-frei-luis-de-sousa-no-teatro/index.html`; Abertura | Do texto ao palco: Frei Luís de Sousa, Teatro Luís de Camões | Do texto ao palco: *Frei Luís de Sousa*, Teatro Luís de Camões |
| V134 | `m4/visita-frei-luis-de-sousa-no-teatro/index.html`; Do texto ao palco | Frei Luís de Sousa, Teatro Luís de Camões | *Frei Luís de Sousa*, Teatro Luís de Camões |
| V135 | `tarefas/m4-u3/index.html`; Blocos e legendas da página | Ilumino a minha casa para receber os muito poderosos e excelentes senhores governadores destes reinos. […] celentes senhores governadores destes reinos. | «Ilumino a minha casa para receber os muito poderosos e excelentes senhores governadores destes reinos.» |
| V136 | `tarefas/m4-u3/index.html`; Blocos e legendas da página | Oh que boa doutrina era esta para a terra, se eu não pregara para o mar! […] a para a terra, se eu não pregara para o mar! | «Oh que boa doutrina era esta para a terra, se eu não pregara para o mar!» |

### M5

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V137 | `m5/camilo-assento/index.html`; Dados E / passos[1].html | assentamentos — registos · a folhas 232 — na página 232 · baetão — pano grosso de lã · pedrez — com pintas · compungia — comovia · enchutos — secos | assentamentos: registos ↵ a folhas 232: na página 232 ↵ baetão: pano grosso de lã ↵ pedrez: com pintas ↵ compungia: comovia ↵ enchutos: secos |
| V138 | `m5/camilo-carta/index.html`; Dados E / passos[1].html | consolação — conforto · degredados — condenados ao exílio · pejo — vergonha · derradeiras — últimas | consolação: conforto ↵ degredados: condenados ao exílio ↵ pejo: vergonha ↵ derradeiras: últimas |
| V139 | `m5/camilo-pai/index.html`; Dados E / passos[1].html | condescendencia — tolerância · escusada — inútil | condescendencia: tolerância ↵ escusada: inútil |
| V140 | `m5/camilo-seculo/index.html`; Dados E / passos[1].html | prestito — cortejo · liteiras — cadeiras cobertas levadas por homens ou animais · dama do paço — senhora da corte · chiste — piada | prestito: cortejo ↵ liteiras: cadeiras cobertas levadas por homens ou animais ↵ dama do paço: senhora da corte ↵ chiste: piada |
| V141 | `m5/camilo-simao-ramos/index.html`; Dados E / fontes[1][1] | Camilo Castelo Branco, Amor de Perdição, texto integral (Project Gutenberg n.º 16425) | Camilo Castelo Branco, *Amor de Perdição*, texto integral (Project Gutenberg n.º 16425) |
| V142 | `m5/camilo-simao-ramos/index.html`; Dados E / marca | Ler a fundo · Amor de Perdição | Ler a fundo · *Amor de Perdição* |
| V143 | `m5/camilo-simao-ramos/index.html`; Dados E / subtitulo | Camilo Castelo Branco, Amor de Perdição, 1862, uma história com ramos | Camilo Castelo Branco, *Amor de Perdição*, 1862, uma história com ramos |
| V144 | `m5/eca-falhamos/index.html`; Dados E / passos[1].html | phaeton — carruagem ligeira · Saint-Cloud — arredores de Paris · Figaro — jornal de Paris | phaeton: carruagem ligeira ↵ Saint-Cloud: arredores de Paris ↵ *Figaro*: jornal de Paris |
| V145 | `m5/eca-hotel/index.html`; Dados E / passos[1].html | gastando cêra com ruins defuntos — a perder tempo com o que não merece · sole normande — linguado à normanda (francês) · banca-rota — falência · fazenda — finanças | gastando cêra com ruins defuntos: a perder tempo com o que não merece ↵ *sole normande*: linguado à normanda (francês) ↵ banca-rota: falência ↵ fazenda: finanças |
| V146 | `m5/eca-ramalhete/index.html`; Dados E / passos[1].html | renque — fila · Residencia Ecclesiastica — casa de padres · Escudo d'Armas — brasão · postigos terreos — pequenas janelas ao nível da rua | renque: fila ↵ Residencia Ecclesiastica: casa de padres ↵ Escudo d'Armas: brasão ↵ postigos terreos: pequenas janelas ao nível da rua |
| V147 | `m5/eca-ramalhete/index.html`; Dados E / passos[3].opcoes[2][3] | Os Maias «vieram habitar» a casa em 1875: Carlos não nasceu lá. | Sem alteração: família Maia. |
| V148 | `m5/gram-dil/index.html`; Dados E / passos[1].html | Discurso indireto — o narrador conta o que foi dito, com um verbo como dizer e «que». | Discurso indireto: o narrador conta o que foi dito, com um verbo como dizer e «que». |
| V149 | `m5/gram-funcoes/index.html`; Dados E / passos[1].html | teste do pronome — «o», «a» dão o complemento direto; «lhe» dá o indireto · teste do corte — se a frase se aguenta sem a expressão, é modificador · predicativo do sujeito — vem com verbos como ser, estar, parecer, ficar | teste do pronome: «o», «a» dão o complemento direto, «lhe» dá o indireto ↵ teste do corte: se a frase se aguenta sem a expressão, é modificador ↵ predicativo do sujeito: vem com verbos como ser, estar, parecer, ficar |
| V178 | `m5/padre-amaro-rego/index.html`; Dados E / passos[6].rot | Ligação a Os Maias | Ligação a *Os Maias* |
| V179 | `m5/painel-m5-f09/index.html`; Cartão 8:  / p | A antiga cadeia fica no Largo Amor de Perdição, junto à Torre dos Clérigos. | Sem alteração: lugar. |
| V180 | `m5/questionarios/index.html`; #indice | 1Amor de Perdiçãofechado | 1*Amor de Perdição*fechado |
| V181 | `m5/questionarios/index.html`; #indice | 2Os Maiasfechado | 2*Os Maias*fechado |
| V182 | `m5/questionarios/index.html`; #indice | 7Os espaços de Os Maiasfechado | 7Os espaços de *Os Maias*fechado |
| V183 | `m5/questionarios/index.html`; #indice | 8Os Maias: o que anuncia a tragédiafechado | 8*Os Maias*: o que anuncia a tragédiafechado |

### M6

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V184 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | ⟪«E mais: as costureiras, as floristas / Descem dos magasins, causam-me sobressaltos; / Custa-lhes a elevar os seus pescoços altos / E muitas delas são comparsas ou coristas.»⟫ | «E mais: as costureiras, as floristas ↵ Descem dos magasins, causam-me sobressaltos; ↵ Custa-lhes a elevar os seus pescoços altos ↵ E muitas delas são comparsas ou coristas.» |
| V185 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | ⟪«Num cuteleiro, de avental, ao torno, / Um forjador maneja um malho, rubramente; / E de uma padaria exala-se, inda quente, / Um cheiro salutar e honesto a pão no forno.»⟫ | «Num cuteleiro, de avental, ao torno, ↵ Um forjador maneja um malho, rubramente; ↵ E de uma padaria exala-se, inda quente, ↵ Um cheiro salutar e honesto a pão no forno.» |
| V186 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | ⟪«“Dó da miséria!… Compaixão de mim!…” / E, nas esquinas, calvo, eterno, sem repouso, / Pede-me sempre esmola um homenzinho idoso, / Meu velho professor nas aulas de latim!»⟫ | «“Dó da miséria!… Compaixão de mim!…” ↵ E, nas esquinas, calvo, eterno, sem repouso, ↵ Pede-me sempre esmola um homenzinho idoso, ↵ Meu velho professor nas aulas de latim!» |
| V187 | `m6/gram-oracoes-rua/index.html`; Dados E / passos[1].html | A. «Há tal soturnidade, há tal melancolia, / Que as sombras, o bulício, o Tejo, a maresia / Despertam-me um desejo absurdo de sofrer.» | A. «Há tal soturnidade, há tal melancolia, ↵ Que as sombras, o bulício, o Tejo, a maresia ↵ Despertam-me um desejo absurdo de sofrer.» |
| V189 | `m6/antero-deus/index.html`; Dados E / passos[1].html | impalpavel — que não se pode tocar · a final — por fim · despojo vão — resto inútil · depuz — pus de lado · lobrega — escura, triste | impalpavel: que não se pode tocar ↵ a final: por fim ↵ despojo vão: resto inútil ↵ depuz: pus de lado ↵ lobrega: escura, triste |
| V190 | `m6/cesario-avemarias/index.html`; Dados E / fontes[1][1] | Cesário Verde, «O Sentimento dum Ocidental», O Livro de Cesário Verde (Project Gutenberg n.º 8698) | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V191 | `m6/cesario-avemarias/index.html`; Dados E / passos[1].html | soturnidade — tristeza sombria · bulicio — burburinho, ruído de gente · extravasado — que se espalha · baixeis — navios · singram — navegam · varonis — fortes | soturnidade: tristeza sombria ↵ bulicio: burburinho, ruído de gente ↵ extravasado: que se espalha ↵ baixeis: navios ↵ singram: navegam ↵ varonis: fortes |
| V192 | `m6/cesario-avemarias/index.html`; Dados E / subtitulo | Cesário Verde, «O Sentimento dum Ocidental», 1887 · I, «Ave-Marias» | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V193 | `m6/cesario-gas/index.html`; Dados E / passos[1].html | magasins — lojas · cuteleiro — oficina de facas · malho — martelo grande | *magasins*: lojas ↵ cuteleiro: oficina de facas ↵ malho: martelo grande |
| V194 | `m6/cesario-noite-ramos/index.html`; Dados E / fontes[1][1] | Cesário Verde, O Livro de Cesário Verde (1887), texto integral (Project Gutenberg n.º 8698) | Cesário Verde, *O Livro de Cesário Verde* (1887), texto integral (Project Gutenberg n.º 8698) |
| V195 | `m6/cesario-noite-ramos/index.html`; Dados E / marca | Ler a fundo · O Sentimento dum Ocidental | Ler a fundo · «O Sentimento dum Ocidental» |
| V196 | `m6/cesario-noite-ramos/index.html`; Dados E / passos[1].html | Cesário Verde, o poeta deste módulo, escreveu em 1880 «O Sentimento dum Ocidental»: quatro partes, Ave-Marias, Noite Fechada, Ao Gás, Horas Mortas, uma noite inteira a andar por Lisboa. Começa assim (grafia de 1887): | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V197 | `m6/cesario-noite-ramos/index.html`; Dados E / subtitulo | Cesário Verde, «O Sentimento dum Ocidental», 1880, uma história com ramos | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V198 | `m6/cesario-noite/index.html`; Dados E / fontes[1][1] | Cesário Verde, «O Sentimento dum Ocidental», O Livro de Cesário Verde (Project Gutenberg n.º 8698) | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V199 | `m6/cesario-noite/index.html`; Dados E / passos[1].html | II — «Noite Fechada»: | II. «Noite Fechada»: |
| V200 | `m6/cesario-noite/index.html`; Dados E / passos[1].html | IV — «Horas Mortas»: | IV. «Horas Mortas»: |
| V201 | `m6/cesario-noite/index.html`; Dados E / passos[1].html | mortifica — atormenta · aljube — prisão · mulher de «dom» — senhora de família nobre · enfezados — raquíticos · emparedados — fechados entre paredes · fel — amargura · imagina — assim na edição de 1887; muitas edições corrigem para «imagino | mortifica: atormenta ↵ aljube: prisão ↵ mulher de «dom»: senhora de família nobre ↵ enfezados: raquíticos ↵ emparedados: fechados entre paredes ↵ fel: amargura ↵ imagina: assim na edição de 1887 (muitas edições corrigem para «imagino») |
| V202 | `m6/cesario-noite/index.html`; Dados E / subtitulo | Cesário Verde, «O Sentimento dum Ocidental», 1887 · II e IV | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V203 | `m6/gram-oracoes-rua/index.html`; Dados E / passos[1].html | teste do «isso» — se a oração se troca por «isso», é substantiva · teste do «o qual» — se «que» se troca por «o qual», «os quais», é relativa · teste da pergunta — quando, porquê, com que resultado: é adverbial | teste do «isso»: se a oração se troca por «isso», é substantiva ↵ teste do «o qual»: se «que» se troca por «o qual», «os quais», é relativa ↵ teste da pergunta: se responde a «quando?», «porquê?» ou «com que resultado?», é adverbial |

### M7

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V245 | `m7/licao-m7-f01/index.html`; Cartão 1: Quantos somos? / html / legenda | Fernando Pessoa (fotografia, 1914). Domínio público. Pessoa em 1914, o ano do «dia triunfal». | Fotógrafo não identificado; retrato de Fernando Pessoa com chapéu; cerca de 1914 (data incerta); reprodução no Wikimedia Commons, original sem instituição indicada; domínio público. |
| V246 | `m7/licao-m7-f05/index.html`; Cartão 1: À beira do rio / html / legenda | Fernando Pessoa (fotografia, 1914). Domínio público. Pessoa em 1914, o ano do «dia triunfal». | Fotógrafo não identificado; retrato de Fernando Pessoa com chapéu; cerca de 1914 (data incerta); reprodução no Wikimedia Commons, original sem instituição indicada; domínio público. |
| V248 | `m7/mapa-do-modulo-m7/index.html`; Blocos e legendas da página / legenda | Fernando Pessoa (fotografia, 1914). Domínio público. Lição M7-F01 | Fotógrafo não identificado; retrato de Fernando Pessoa com chapéu; cerca de 1914 (data incerta); reprodução no Wikimedia Commons, original sem instituição indicada; domínio público. |
| V249 | `m7/campos-aniversario/index.html`; Dados E / passos[1].html | grelado — bolor · «Pára» — grafia da edição | grelado: bolor ↵ «Pára»: grafia da edição |
| V250 | `m7/campos-maquina/index.html`; Dados E / passos[1].html | eléctricas — grafia da edição | eléctricas: grafia da edição |
| V251 | `m7/gram-valores-pessoa/index.html`; Dados E / passos[1].html | aspeto — acabou (perfetivo), dura (imperfetivo), é costume (habitual), repete-se vezes contadas (iterativo), vale sempre (genérico) · modalidade — certeza ou probabilidade (epistémica), dever ou conselho (deôntica), avaliação (apreciativa) | aspeto: acabou (perfetivo), dura (imperfetivo), é costume (habitual), repete-se vezes contadas (iterativo), vale sempre (genérico) ↵ modalidade: certeza ou probabilidade (epistémica), dever ou conselho (deôntica), avaliação (apreciativa) |
| V252 | `m7/licao-m7-f01/index.html`; Cartão 17:  / f | **O Guardador de Rebanhos**: o primeiro título do dia triunfal, assinado por Caeiro. | ***O Guardador de Rebanhos***: o primeiro título do dia triunfal, assinado por Caeiro. |
| V253 | `m7/licao-m7-f01/index.html`; Cartão 17:  / frase | a começar pelo título O Guardador de Rebanhos. | a começar pelo título *O* *Guardador* *de* *Rebanhos*. |
| V254 | `m7/mensagem-mostrengo/index.html`; Dados E / passos[1].html | breu — escuridão total · reprendeu — voltou a prender | breu: escuridão total ↵ reprendeu: voltou a prender |
| V255 | `m7/mensagem-nevoeiro/index.html`; Dados E / passos[1].html | fulgor baço — brilho sem força · fogo-fátuo — chama fraca sobre os pântanos · derradeiro — último | fulgor baço: brilho sem força ↵ fogo-fátuo: chama fraca sobre os pântanos ↵ derradeiro: último |
| V256 | `m7/painel-m7-f10/index.html`; Cartão 14:  / p | Em Frei Luís de Sousa, o regresso de D. João de Portugal faz renascer a família de Madalena. | Em *Frei Luís de Sousa*, o regresso de D. João de Portugal faz renascer a família de Madalena. |
| V257 | `m7/pessoa-almas/index.html`; Dados E / passos[1].html | móbil — que se move | móbil: que se move |
| V258 | `m7/pessoa-ceifeira/index.html`; Dados E / passos[1].html | ceifeira — mulher que corta cereal · lida — trabalho · ciência — aqui, a consciência | ceifeira: mulher que corta cereal ↵ lida: trabalho ↵ ciência: aqui, a consciência |
| V259 | `m7/pessoa-ilha/index.html`; Dados E / passos[1].html | se olvida — se esquece · desvirtua — perde o valor | se olvida: se esquece ↵ desvirtua: perde o valor |
| V260 | `m7/reis-lidia/index.html`; Dados E / passos[1].html | fitemos — olhemos fixamente · Fado — destino | fitemos: olhemos fixamente ↵ Fado: destino |
| V261 | `m7/tabacaria/index.html`; #p4 | 2.º ano · Lisboa, século XIXCesário Verde, «O Sentimento dum Ocidental»: «Nas nossas ruas, ao anoitecer, / Há tal soturnidade, há tal melancolia» | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V262 | `m7/tabacaria/index.html`; #seguir | Cesário Verde, «O Sentimento dum Ocidental», in O Livro de Cesário Verde · Project Gutenberg | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V263 | `m7/tabacaria/index.html`; A minha leitura | Da janela, vejo— Hoje estou mais do lado— O Esteves, para mim, é— A minha ligação— Esta semana— | Da janela, vejo ↵ Hoje estou mais do lado ↵ O Esteves, para mim, é ↵ A minha ligação ↵ Esta semana |
| V264 | `m7/mensagem-nevoeiro/index.html`; Dados E / passos[5].opcoes[1][1] | A turma hoje é nevoeiro: ninguém sabe o que quer. / Tudo é disperso, nada é inteiro. / Ó Portugal, hoje és nevoeiro... | A turma hoje é nevoeiro: ninguém sabe o que quer. / Tudo é disperso, nada é inteiro. / Ó Portugal, hoje és nevoeiro… |

### M9

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V268 | `m9/gram-aspeto-memorial/index.html`; Dados E / passos[1].html | aspeto — acabou (perfetivo), dura (imperfetivo), é costume (habitual), repete-se vezes contadas (iterativo), vale sempre (genérico) · coesão — anáfora (retoma o que já foi dito), catáfora (anuncia o que vem), conector (liga e diz a relação) | aspeto: acabou (perfetivo), dura (imperfetivo), é costume (habitual), repete-se vezes contadas (iterativo), vale sempre (genérico) ↵ coesão: anáfora (retoma o que já foi dito), catáfora (anuncia o que vem), conector (liga e diz a relação) |
| V278 | `m9/painel-m9-f07/index.html`; Cartão 11:  / p | Na ponte do poder, ao lado do Memorial, estão Vieira e Os Maias. | Na ponte do poder, ao lado do Memorial, estão Vieira e *Os Maias*. |
| V279 | `m9/passarola-ramos/index.html`; Dados E / marca | Ler a fundo · Memorial do Convento | Ler a fundo · *Memorial do Convento* |
| V280 | `m9/passarola-ramos/index.html`; Dados E / subtitulo | José Saramago, Memorial do Convento (1982), o voo da passarola: uma história com ramos | José Saramago, *Memorial do Convento* (1982), o voo da passarola: uma história com ramos |
| V281 | `m9/questionarios/index.html`; #indice | 1Memorial do Convento: a históriafechado | 1*Memorial do Convento*: a históriafechado |

### Transversal

| Ponto | Ficheiro e local | Antes | Depois |
|---|---|---|---|
| V283 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | A. «Ondas do mar de Vigo, / se vistes meu amigo?» (Martim Codax): a mesma vogal a voltar. | A. «Ondas do mar de Vigo, ↵ se vistes meu amigo?» (Martim Codax): a mesma vogal a voltar. |
| V284 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | B. «Sam eu coruja ou corujo, / Ou sam algum caramujo» (Gil Vicente): sons repetidos dentro do verso. | B. «Sam eu coruja ou corujo, ↵ Ou sam algum caramujo» (Gil Vicente): sons repetidos dentro do verso. |
| V285 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | C. «Que mortes, que perigos, que tormentas, / Que crueldades neles experimentas!» (Camões, IV, 95): a mesma consoante a voltar, e a mesma palavra a abrir. | C. «Que mortes, que perigos, que tormentas, ↵ Que crueldades neles experimentas!» (Camões, IV, 95): a mesma consoante a voltar, e a mesma palavra a abrir. |
| V286 | `1/todos/index.html`; Módulo 2 · Teatro vicentino | A farsa em cena: Farsa de Inês Pereira, no teatrocaderno de campo | A farsa em cena: *Farsa de Inês Pereira*, no teatrocaderno de campo |
| V287 | `1/todos/index.html`; Módulo 2 · Teatro vicentino | E se Inês escolhesse o asno logo?Gil Vicente, Farsa de Inês Pereira, 1523, uma história com ramos | E se Inês escolhesse o asno logo?Gil Vicente, *Farsa de Inês Pereira*, 1523, uma história com ramos |
| V288 | `1/todos/index.html`; Módulo 3 · Lírica e épica camonianas | E se ficasses na praia?Luís de Camões, Os Lusíadas, 1572, uma história com ramos | E se ficasses na praia?Luís de Camões, *Os Lusíadas*, 1572, uma história com ramos |
| V289 | `2/todos/index.html`; Módulo 4 · Literatura barroca e romântica | Do texto ao palco: Frei Luís de Sousa, Teatro Luís de Camõescaderno de campo | Do texto ao palco: *Frei Luís de Sousa*, Teatro Luís de Camõescaderno de campo |
| V290 | `2/todos/index.html`; Módulo 4 · Literatura barroca e romântica | E se o Romeiro dissesse o nome?Almeida Garrett, Frei Luís de Sousa, 1843, uma história com ramos | E se o Romeiro dissesse o nome?Almeida Garrett, *Frei Luís de Sousa*, 1843, uma história com ramos |
| V291 | `2/todos/index.html`; Módulo 5 · Narrativa do século XIX | E se Simão obedecesse ao pai?Camilo Castelo Branco, Amor de Perdição, 1862, uma história com ramos | E se Simão obedecesse ao pai?Camilo Castelo Branco, *Amor de Perdição*, 1862, uma história com ramos |
| V292 | `2/todos/index.html`; Módulo 6 · Poesia Realista | Ave-MariasCesário Verde, «O Sentimento dum Ocidental», 1887 · I, «Ave-Marias» | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V293 | `2/todos/index.html`; Módulo 6 · Poesia Realista | Da «Noite Fechada» às «Horas Mortas»Cesário Verde, «O Sentimento dum Ocidental», 1887 · II e IV | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V294 | `2/todos/index.html`; Módulo 6 · Poesia Realista | Uma noite com CesárioCesário Verde, «O Sentimento dum Ocidental», 1880, uma história com ramos | Sem alteração: o poema já tem aspas; o livro, quando citado, já tem itálico. |
| V295 | `3/index.html`; 3.º ano | Quem és quando escreves — e quem fica de fora do que contas? | Quem és quando escreves e quem fica de fora do que contas? |
| V296 | `3/todos/index.html`; Módulo 9 · Romance Saramaguiano | E se Baltasar ficasse em terra?José Saramago, Memorial do Convento (1982), o voo da passarola: uma história com ramos | E se Baltasar ficasse em terra?José Saramago, *Memorial do Convento* (1982), o voo da passarola: uma história com ramos |
| V297 | `assets/exame/sessoes.json`; Sessões de exame / sessions[11].writing.prompt | Explica como uma passagem de O Sentimento dum Ocidental transforma uma observação urbana numa reflexão. Analisa uma sensação e um contraste social ou temporal. | Explica como uma passagem de «O Sentimento dum Ocidental» transforma uma observação urbana numa reflexão. Analisa uma sensação e um contraste social ou temporal. |
| V298 | `assets/exame/sessoes.json`; Sessões de exame / sessions[23].correction.model | Em Farsa de Inês Pereira e em Amor de Perdição, as escolhas individuais confrontam-se com regras sociais e relações familiares. No entanto, os textos representam esse confronto de modos diferentes: a farsa expõe interesses através do cómico | Na *Farsa de Inês Pereira* e em *Amor de Perdição*, as escolhas individuais confrontam-se com regras sociais e relações familiares. No entanto, os textos representam esse confronto de modos diferentes: a farsa expõe interesses através do cómico, enquanto a |
| V299 | `assets/exame/sessoes.json`; Sessões de exame / sessions[3].focus | Interpretar o conflito na Farsa de Inês Pereira | Interpretar o conflito na *Farsa de Inês Pereira* |
| V300 | `assets/exame/sessoes.json`; Sessões de exame / sessions[3].writing.criteria[1] | Respondi ao pedido: interpretar o conflito na Farsa de Inês Pereira. | Respondi ao pedido: interpretar o conflito na *Farsa de Inês Pereira*. |
| V301 | `assets/exame/sessoes.json`; Sessões de exame / sessions[5].source.title | Os Lusíadas: celebrar e interrogar | *Os Lusíadas*: celebrar e interrogar |
| V302 | `assets/exame/sessoes.json`; Sessões de exame / sessions[7].source.title | Frei Luís de Sousa: o que a cena revela | *Frei Luís de Sousa*: o que a cena revela |
| V303 | `assets/exame/sessoes.json`; Sessões de exame / sessions[8].writing.prompt | A partir de Amor de Perdição, mostra como uma escolha individual é condicionada por relações familiares ou convenções sociais. Distingue explicar uma ação de a justificar. | A partir de *Amor de Perdição*, mostra como uma escolha individual é condicionada por relações familiares ou convenções sociais. Distingue explicar uma ação de a justificar. |
| V304 | `assets/exame/sessoes.json`; Sessões de exame / sessions[9].writing.prompt | Analisa dois pormenores de um espaço ou de uma cena de Os Maias. Explica como contribuem para caracterizar uma personagem ou para construir uma visão crítica da sociedade. | Analisa dois pormenores de um espaço ou de uma cena de *Os Maias*. Explica como contribuem para caracterizar uma personagem ou para construir uma visão crítica da sociedade. |
| V305 | `atlas/index.html`; #atlas-lista-pessoas | Jogo de memória · opcional | Atividade de memória · opcional |
| V306 | `atlas/index.html`; #atlas-lista-pessoas | O jogo anterior continua disponível com os resultados guardados e o seu conjunto de 147 pessoas. | A atividade anterior continua disponível com os resultados guardados e o seu conjunto de 147 pessoas. |
| V307 | `atlas/index.html`; #desafio | Pessoa ou personagem?Bartolomeu de Gusmão existiu: em 1709 fez subir um pequeno balão diante da corte. No Memorial do Convento, o padre Bartolomeu voa na passarola com Baltasar e Blimunda, mas esse voo é ficção. Num romance histórico, separ | Pessoa ou personagem?Bartolomeu de Gusmão existiu: em 1709 fez subir um pequeno balão diante da corte. No *Memorial do Convento*, o padre Bartolomeu voa na passarola com Baltasar e Blimunda, mas esse voo é ficção. Num romance histórico, separ |
| V308 | `atlas/index.html`; #desafio | Uma data, duas versõesEunice Muñoz fez de Maria em Frei Luís de Sousa: a Infopédia diz 1942, o Correio da Manhã diz 1943. Quando duas fontes não batem certo, escreve só o que ambas confirmam («nos anos 40», «ainda adolescente») e regista a | Uma data, duas versõesEunice Muñoz fez de Maria em *Frei Luís de Sousa*: a Infopédia diz 1942, o Correio da Manhã diz 1943. Quando duas fontes não batem certo, escreve só o que ambas confirmam («nos anos 40», «ainda adolescente») e regista a |
| V309 | `atlas/index.html`; #desafio | Uma obra, duas datasPara o Amor de Perdição de Manoel de Oliveira, umas fontes dão 1978 e outras 1979. Não escolhas a que dá jeito: vê o que cada data marca (a rodagem, a primeira exibição na televisão, a estreia em sala) e escreve qual usa | Uma obra, duas datasPara o *Amor de Perdição* de Manoel de Oliveira, umas fontes dão 1978 e outras 1979. Não escolhas a que dá jeito: vê o que cada data marca (a rodagem, a primeira exibição na televisão, a estreia em sala) e escreve qual usa |
| V310 | `atlas/index.html`; #desafio | . As fontes estão identificadas em cada perfil. Os resultados do jogo ficam só neste aparelho. Há mais 6 pessoas à espera de conferência de fontes. | . As fontes estão identificadas em cada perfil. Os resultados da atividade ficam só neste aparelho. Há mais 6 pessoas à espera de conferência de fontes. |
| V311 | `atlas/index.html`; #desafio | Passaporte do jogo | Passaporte da atividade |
| V312 | `c/candide-jardim/index.html`; Dados E / emblemas[2][3] | Já percebeste o jogo. Relê o elogio ao barão e pergunta porquê. | Já desconfias do narrador. Relê o elogio ao barão e pergunta porquê. |
| V313 | `c/compasso-rimas/index.html`; Dados E / passos[1].html | rima pobre — duas palavras da mesma classe, quase sempre dois infinitivos · rima rica — classes diferentes, ou mais de uma sílaba a rimar · rima interna — sons que voltam dentro do verso · assonância — a vogal que volta · aliteração — a con | rima pobre: duas palavras da mesma classe, quase sempre dois infinitivos ↵ rima rica: classes diferentes, ou mais de uma sílaba a rimar ↵ rima interna: sons que voltam dentro do verso ↵ assonância: a vogal que volta ↵ aliteração: a consoante que volta |
| V314 | `c/kafka-acordar/index.html`; Dados E / passos[1].html | couraça — armadura · abaulado — curvo · caixeiro-viajante — vendedor que percorre a região com amostras · regalo — manga de peles para aquecer as mãos · flanco — lado do corpo | couraça: armadura ↵ abaulado: curvo ↵ caixeiro-viajante: vendedor que percorre a região com amostras ↵ regalo: manga de peles para aquecer as mãos ↵ flanco: lado do corpo |
| V315 | `c/quinta-mandamentos/index.html`; Dados E / passos[1].html | Tradução nossa do inglês; o original está em domínio público na União Europeia. Garganta — o porco que fala pelos outros (Squealer, no original) · Napoleão — o porco que governa | Tradução nossa do inglês; o original está em domínio público na União Europeia. ↵ Garganta: o porco que fala pelos outros (Squealer, no original) ↵ Napoleão: o porco que governa |
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
| V334 | `obras/amor-perdicao/index.html`; Abertura | Amor de Perdição | *Amor de Perdição* |
| V335 | `obras/amor-perdicao/index.html`; Conhecer o autor | «Amor de Perdição», de Camilo Castelo BrancoRTP Ensina (Grandes Livros, 2009), 48 min. Documentário sobre o romance de Simão, Teresa e Mariana. | *Amor de Perdição*, de Camilo Castelo BrancoRTP Ensina (Grandes Livros, 2009), 48 min. Documentário sobre o romance de Simão, Teresa e Mariana. |
| V336 | `obras/amor-perdicao/index.html`; Ler | Amor de Perdição (Projeto Gutenberg, n.º 16425) | *Amor de Perdição* (Projeto Gutenberg, n.º 16425) |
| V337 | `obras/cesario/index.html`; Abertura | O Sentimento dum Ocidental | «O Sentimento dum Ocidental» |
| V338 | `obras/cesario/index.html`; Conhecer o autor | O Livro de Cesário VerdeRTP Ensina (Grandes Livros, 2010), cópia no Arquivo da Internet, 31 min. Documentário sobre o poeta do concreto. | *O Livro de Cesário Verde*RTP Ensina (Grandes Livros, 2010), cópia no Arquivo da Internet, 31 min. Documentário sobre o poeta do concreto. |
| V339 | `obras/cesario/index.html`; Ler | O Sentimento dum Ocidental (Biblioteca) | «O Sentimento dum Ocidental» (Biblioteca) |
| V340 | `obras/frei-luis/index.html`; Abertura | Frei Luís de Sousa | *Frei Luís de Sousa* |
| V341 | `obras/frei-luis/index.html`; Frei Luís de Sousa, outra encenação para Garrett | Frei Luís de Sousa, outra encenação para Garrett | *Frei Luís de Sousa*, outra encenação para Garrett |
| V342 | `obras/frei-luis/index.html`; Ler | Frei Luís de Sousa (Biblioteca) | *Frei Luís de Sousa* (Biblioteca) |
| V343 | `obras/index.html`; As obras | O Sentimento dum OcidentalM6, Cesário Verde. 2 leituras. | «O Sentimento dum Ocidental»M6, Cesário Verde. 2 leituras. |
| V344 | `obras/ines/index.html`; Abertura | Farsa de Inês Pereira | *Farsa de Inês Pereira* |
| V345 | `obras/ines/index.html`; Auto da Barca do Inferno (2022) | Auto da Barca do Inferno (2022) | *Auto da Barca do Inferno* (2022) |
| V346 | `obras/ines/index.html`; Auto da Barca do Inferno (2022) | Não é a Farsa de Inês Pereira: é outra peça do mesmo autor, numa montagem que a própria companhia diz desconstruída. Serve para comparar. | Não é a *Farsa de Inês Pereira*: é outra peça do mesmo autor, numa montagem que a própria companhia diz desconstruída. Serve para comparar. |
| V347 | `obras/ines/index.html`; Conhecer o autor | «Auto da Barca do Inferno», de Gil VicenteRTP Ensina (Grandes Livros, 2009), 32 min. Documentário sobre outra peça de Gil Vicente e a crítica à sociedade do seu tempo. | *Auto da Barca do Inferno*, de Gil VicenteRTP Ensina (Grandes Livros, 2009), 32 min. Documentário sobre outra peça de Gil Vicente e a crítica à sociedade do seu tempo. |
| V348 | `obras/lusiadas/index.html`; Abertura | Os Lusíadas | *Os Lusíadas* |
| V349 | `obras/lusiadas/index.html`; Conhecer o autor | Os Lusíadas: um poema épico e críticoRTP Ensina (Câmara Clara, 2007), 4 min. Helder Macedo sobre a exaltação e a crítica no poema. | *Os Lusíadas*: um poema épico e críticoRTP Ensina (Câmara Clara, 2007), 4 min. Helder Macedo sobre a exaltação e a crítica no poema. |
| V350 | `obras/lusiadas/index.html`; Ler | Os Lusíadas (Projeto Gutenberg, n.º 3333) | *Os Lusíadas* (Projeto Gutenberg, n.º 3333) |
| V351 | `obras/maias/index.html`; Abertura | Os Maias | *Os Maias* |
| V352 | `obras/maias/index.html`; Conhecer o autor | A sátira de Eça de Queirós em «Os Maias»RTP Ensina (Grandes Livros, 2009), 6 min. Carlos Reis sobre a caricatura da sociedade. | A sátira de Eça de Queirós em *Os Maias*RTP Ensina (Grandes Livros, 2009), 6 min. Carlos Reis sobre a caricatura da sociedade. |
| V353 | `obras/maias/index.html`; Conhecer o autor | Os Maias, de Eça de QueirósRTP Ensina (Grandes Livros, 2009), 49 min. Documentário sobre três gerações da família Maia. | *Os Maias*, de Eça de QueirósRTP Ensina (Grandes Livros, 2009), 49 min. Documentário sobre três gerações da família Maia. |
| V354 | `obras/maias/index.html`; Ler | Os Maias (Projeto Gutenberg, n.º 40409) | *Os Maias* (Projeto Gutenberg, n.º 40409) |
| V355 | `obras/memorial/index.html`; Abertura | Memorial do Convento | *Memorial do Convento* |
| V356 | `obras/memorial/index.html`; Conhecer o autor | «Memorial do Convento», de José SaramagoRTP Ensina (Grandes Livros, 2011), cópia no Arquivo da Internet, 35 min. O convento de Mafra, a passarola, Baltasar e Blimunda. | *Memorial do Convento*, de José SaramagoRTP Ensina (Grandes Livros, 2011), cópia no Arquivo da Internet, 35 min. O convento de Mafra, a passarola, Baltasar e Blimunda. |
| V357 | `obras/memorial/index.html`; Um excerto do romance | Ao tocar, o vídeo carrega a partir do YouTube (Rota Memorial do Convento). Também podes abri-lo no YouTube. | Ao tocar, o vídeo carrega a partir do YouTube (Rota *Memorial do Convento*). Também podes abri-lo no YouTube. |
| V358 | `obras/pessoa/index.html`; Ler | O Guardador de Rebanhos, XX, de Alberto Caeiro (Biblioteca) | *O Guardador de Rebanhos*, XX, de Alberto Caeiro (Biblioteca) |
| V359 | `obras/pessoa/index.html`; Ler | Os poemas das lições estão no Arquivo Pessoa. «O Guardador de Rebanhos», XX, e «Tabacaria» estão também na Biblioteca. | Os poemas das lições estão no Arquivo Pessoa. *O Guardador de Rebanhos*, XX, e «Tabacaria» estão também na Biblioteca. |
| V360 | `obras/sermao/index.html`; Abertura | Sermão de Santo António aos Peixes | *Sermão de Santo António aos Peixes* |
| V361 | `obras/sermao/index.html`; Conhecer o autor | «Sermão de Santo António aos Peixes», de padre António VieiraRTP Ensina (Grandes Livros, 2009), 48 min. Documentário sobre o sermão pregado no Maranhão a 13 de junho de 1654. | *Sermão de Santo António aos Peixes*, de padre António VieiraRTP Ensina (Grandes Livros, 2009), 48 min. Documentário sobre o sermão pregado no Maranhão a 13 de junho de 1654. |

## Depois de os pedidos entrarem

02/11/2026: os pedidos #144 a #151 já estão no main (o #143 continua aberto). Os pontos desta lista ficam para a volta seguinte da varredura, num pedido próprio sobre o main; esta camada não lhes mexe.

Os ficheiros com pontos adiados não recebem correções editoriais. Quando vários pedidos alteram o mesmo ficheiro, é necessário conciliar as suas alterações antes de rever o ponto no main.

| Ponto | Depois de entrar | Ficheiro e local | Correção proposta |
|---|---|---|---|
| V002 | #150 | `m1/licao-m1-f01/index.html`; Cartão 1: A língua que se canta / html / legenda | Acrescentar a instituição depositária e a referência do manuscrito/reprodução. A indicação de domínio público não identifica a proveniência da imagem. |
| V003 | #150 | `m1/licao-m1-f01/index.html`; Cartão 4: Tocar e cantar chega para trovar? / html | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. |
| V004 | #150 | `m1/licao-m1-f04/index.html`; Cartão 13: Que faz Guilhade com «loar»? / html | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. |
| V005 | #150 | `m1/licao-m1-f04/index.html`; Cartão 2: Quem fala, e quem é a «senhor»? / html | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. |
| V006 | #150 | `m1/licao-m1-f04/index.html`; Cartão 2: Quem fala, e quem é a «senhor»? / html | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. |
| V007 | #150 | `m1/licao-m1-f04/index.html`; Cartão 6: Quanto vale a senhora de D. Dinis? / html | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. |
| V008 | #150 | `m1/licao-m1-f11/index.html`; Cartão 1: Ondas, gritos e grãos de trigo / html / legenda | Acrescentar a instituição depositária e a referência do manuscrito/reprodução. A indicação de domínio público não identifica a proveniência da imagem. |
| V028 | #150 | `m2/licao-m2-f07/index.html`; Cartão 8: Para entender / html | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. |
| V044 | #150 | `m2/licao-m2-f01/index.html`; Cartão 19: Para entender / html | Aplicar itálico a «Farsa de Inês Pereira» no texto corrido. |
| V047 | #150 | `m2/mapa-do-modulo-m2/index.html`; #frase | Aplicar itálico a «Farsa de Inês Pereira» no texto corrido. |
| V092 | #144, #145, #148, #150 | `m3/index.html`; Lírica e épica camonianas | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V093 | #150 | `m3/licao-m3-f05/index.html`; Cartão 14:  / p2 | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». |
| V094 | #150 | `m3/licao-m3-f05/index.html`; Cartão 18:  / f | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». |
| V095 | #150 | `m3/licao-m3-f05/index.html`; Cartão 19: Leonor e o perdigão / html | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». |
| V096 | #150 | `m3/licao-m3-f13/index.html`; Cartão 1: Um bicho da terra tão pequeno / html | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V097 | #150 | `m3/licao-m3-f13/index.html`; Cartão 27: A calçada do verso / f | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V098 | #144, #145, #148, #150 | `m3/licao-m3-f16/index.html`; Cartão 1: Quem disse este verso? / html | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V099 | #144, #145, #148, #150 | `m3/licao-m3-f16/index.html`; Cartão 2: O essencial / html | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V100 | #144, #145, #148, #150 | `m3/licao-m3-f16/index.html`; Cartão 2: O essencial / html | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V101 | #150 | `m3/licao-m3-f18/index.html`; #baralho | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V102 | #150 | `m3/licao-m3-f18/index.html`; Cartão 11: Quatro funções / html | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V103 | #150 | `m3/licao-m3-f18/index.html`; Cartão 1: Uma epopeia por dentro / html | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». |
| V104 | #144, #145, #148, #150 | `m3/mapa-do-modulo-m3/index.html`; #frase | Aplicar itálico a «Os Lusíadas» no texto corrido. |
| V118 | #149 | `m4/index.html`; Dados U / [2].pool[37].f | Reformular apenas o texto editorial: «contraste», «duplo sentido», «atividade» ou «documento da aula», conforme o caso; no crédito da edição, «página de rosto». |
| V119 | #149 | `m4/index.html`; Literatura barroca e romântica | Aplicar itálico a «Sermão de Santo António aos Peixes» no texto corrido. |
| V150 | #144, #145, #148, #150 | `m5/index.html`; Dados U / [1].pool[40].f | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V151 | #144, #145, #148, #150 | `m5/index.html`; Dados U / [1].pool[40].fe[3] | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V152 | #144, #145, #148, #150 | `m5/index.html`; Dados U / [1].pool[47].f | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V153 | #144, #145, #148, #150 | `m5/index.html`; Dados U / [1].pool[47].o[3] | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V154 | #144, #145, #148, #150 | `m5/index.html`; Dados U / [1].pool[48].pares[3][1] | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V155 | #144, #145, #148, #150 | `m5/index.html`; Dados U / [2].pool[1].frase | Aplicar itálico a «Os Maias» no texto corrido. |
| V156 | #144, #145, #148, #150 | `m5/index.html`; Dados U / [2].pool[74].passos[3] | Aplicar itálico a «Os Maias» no texto corrido. |
| V157 | #144, #145, #148, #150 | `m5/index.html`; Narrativa do século XIX | Aplicar itálico a «Os Maias» no texto corrido. |
| V158 | #150 | `m5/licao-m5-f02/index.html`; Cartão 20: Para entender / html | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V159 | #150 | `m5/licao-m5-f02/index.html`; Cartão 4: Introdução / html | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V160 | #144, #145, #148, #150 | `m5/licao-m5-f08/index.html`; Cartão 3: Para entender / html | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V161 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html`; Cartão 10:  / f | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V162 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html`; Cartão 10:  / fe | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V163 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html`; Cartão 10:  / p | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V164 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html`; Cartão 2: O essencial / html | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V165 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html`; Cartão 3:  / f | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V166 | #144, #145, #148, #150 | `m5/licao-m5-f09/index.html`; Cartão 3:  / fe[3] | Aplicar itálico a «Amor de Perdição» no texto corrido. |
| V167 | #150 | `m5/licao-m5-f10/index.html`; Cartão 1: Sombrio casarão / html | Aplicar itálico a «Os Maias» no texto corrido. |
| V168 | #150 | `m5/licao-m5-f10/index.html`; Cartão 21: O Ramalhete, no início e no fim / html | Aplicar itálico a «Os Maias» no texto corrido. |
| V169 | #150 | `m5/licao-m5-f10/index.html`; Cartão 22:  / pares[1][1] | Aplicar itálico a «Os Maias» no texto corrido. |
| V170 | #150 | `m5/licao-m5-f10/index.html`; Cartão 3: O essencial / html | Aplicar itálico a «Os Maias» no texto corrido. |
| V171 | #150 | `m5/licao-m5-f10/index.html`; Cartão 5:  / frase | Aplicar itálico a «Os Maias» no texto corrido. |
| V172 | #150 | `m5/licao-m5-f14/index.html`; Cartão 21: Para levar / html | Aplicar itálico a «Os Maias» no texto corrido. |
| V173 | #150 | `m5/licao-m5-f14/index.html`; Cartão 2: O essencial / html | Aplicar itálico a «Os Maias» no texto corrido. |
| V174 | #150 | `m5/licao-m5-f14/index.html`; Cartão 2: O essencial / html | Aplicar itálico a «Os Maias» no texto corrido. |
| V175 | #144, #145, #148, #150 | `m5/licao-m5-f15/index.html`; Cartão 12:  / passos[3] | Aplicar itálico a «Os Maias» no texto corrido. |
| V176 | #144, #145, #148, #150 | `m5/licao-m5-f15/index.html`; Cartão 2: O essencial / html | Aplicar itálico a «Os Maias» no texto corrido. |
| V177 | #144, #145, #148, #150 | `m5/mapa-do-modulo-m5/index.html`; #frase | Aplicar itálico a «Os Maias» no texto corrido. |
| V188 | #149, #150 | `m6/licao-m6-f01/index.html`; Cartão 1: O cavaleiro que encontra o nada / html / legenda | Identificar a autoria da fotografia, ou declarar autoria não identificada após conferir a fonte; indicar a instituição ou reprodução consultada. Não atribuir um nome por suposição. |
| V204 | #144, #145, #148, #150 | `m6/index.html`; #m6-cesario-noite-inteira | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V205 | #144, #145, #148, #150 | `m6/index.html`; Dados U / [2].pool[38].fe[3] | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V206 | #144, #145, #148, #150 | `m6/index.html`; Poesia Realista | Aplicar itálico a «O Livro de Cesário Verde» no texto corrido. |
| V207 | #144, #145, #148, #150 | `m6/licao-m6-f04/index.html`; #baralho | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V208 | #144, #145, #148, #150 | `m6/licao-m6-f04/index.html`; Cartão 5: Para entender / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V209 | #150 | `m6/licao-m6-f05/index.html`; #baralho | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V210 | #150 | `m6/licao-m6-f05/index.html`; Cartão 15:  / frase | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V211 | #150 | `m6/licao-m6-f05/index.html`; Cartão 1: Palavras com passado / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V212 | #150 | `m6/licao-m6-f06/index.html`; Cartão 16:  / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V213 | #150 | `m6/licao-m6-f06/index.html`; Cartão 1: «Ave-Marias» / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V214 | #150 | `m6/licao-m6-f06/index.html`; Cartão 21: O que vê e o que evoca / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V215 | #150 | `m6/licao-m6-f06/index.html`; Cartão 2: O essencial / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V216 | #150 | `m6/licao-m6-f06/index.html`; Cartão 3: I: «Ave-Marias» (na íntegra) / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V217 | #150 | `m6/licao-m6-f07/index.html`; #baralho | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V218 | #150 | `m6/licao-m6-f07/index.html`; Cartão 1: Da «Noite Fechada» às «Horas Mortas» / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V219 | #150 | `m6/licao-m6-f07/index.html`; Cartão 26:  / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V220 | #144, #145, #148, #150 | `m6/licao-m6-f08/index.html`; #baralho | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V221 | #144, #145, #148, #150 | `m6/licao-m6-f08/index.html`; Cartão 2: O essencial / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V222 | #144, #145, #148, #150 | `m6/licao-m6-f09/index.html`; #baralho | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V223 | #144, #145, #148, #150 | `m6/licao-m6-f09/index.html`; Cartão 5:  / fe[3] | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V224 | #144, #145, #148, #150 | `m6/licao-m6-f11/index.html`; Cartão 6:  / f | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V225 | #144, #145, #148, #150 | `m6/licao-m6-f11/index.html`; Cartão 7:  / f | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V226 | #144, #145, #148, #150 | `m6/licao-m6-f11/index.html`; Cartão 9:  / f | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V227 | #150 | `m6/licao-m6-f12/index.html`; Cartão 2: Manhã e contraste / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V228 | #150 | `m6/licao-m6-f12/index.html`; Cartão 2: Manhã e contraste / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V229 | #150 | `m6/licao-m6-f12/index.html`; Cartão 5: A hipótese do artista / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V230 | #150 | `m6/licao-m6-f12/index.html`; Cartão 5: A hipótese do artista / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V231 | #150 | `m6/licao-m6-f12/index.html`; Cartão 9: Do olhar às mãos / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V232 | #150 | `m6/licao-m6-f12/index.html`; Cartão 9: Do olhar às mãos / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V233 | #150 | `m6/licao-m6-f13/index.html`; Cartão 2: Quem é chamado? / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V234 | #150 | `m6/licao-m6-f13/index.html`; Cartão 5: A mudança de tom / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V235 | #150 | `m6/licao-m6-f13/index.html`; Cartão 5: A mudança de tom / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V236 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html`; #frase | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V237 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html`; #frase | Aplicar itálico a «O Livro de Cesário Verde» no texto corrido. |
| V238 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html`; #frase | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V239 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html`; #frase | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V240 | #144, #145, #148, #150 | `m6/mapa-do-modulo-m6/index.html`; #frase | Aplicar itálico a «O Livro de Cesário Verde» no texto corrido. |
| V241 | #144, #145, #148, #150 | `tarefas/m6-u2/aquecimento/index.html`; Cartão 1: A cidade que Cesário viu / html | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V242 | #144, #145, #148, #150 | `tarefas/m6-u2/index.html`; Dossiê do tema B | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V243 | #144, #145, #148, #150 | `tarefas/m6-u2/index.html`; Dossiê do tema B | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V244 | #144, #145, #148, #150 | `tarefas/m6-u2/index.html`; Tema B Cesário nos dias de hoje | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V247 | #149 | `m7/licao-m7-f34/index.html`; Cartão 32: Muda o lugar, mantém a técnica / html | Dispor cada verso numa linha e conservar as estrofes; retirar as barras usadas como separadores. |
| V265 | #145, #148, #150 | `m8/licao-m8-f04/index.html`; Cartão 25: Adeus / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V266 | #145, #148, #150 | `m8/licao-m8-f05/index.html`; Cartão 24: A verdade histórica / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V267 | #145, #148, #150 | `m8/licao-m8-f10/index.html`; Cartão 3: Da cena pintada à palavra dirigida aos filhos / html | Acrescentar a delimitação «…» segundo a regra editorial, mantendo o bloco, as quebras e o crédito. Não alterar o texto citado. |
| V269 | #143, #145, #148, #150 | `m9/index.html`; Dados U / [2].pool[45].f | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V270 | #143, #145, #148, #150 | `m9/index.html`; Dados U / [2].pool[45].pares[3][1] | Rever a delimitação de «O Sentimento dum Ocidental»: é um poema e leva aspas, nunca itálico. Conservar se já estiver conforme. |
| V271 | #148, #150 | `m9/licao-m9-f01/index.html`; Cartão 1: Um convento, uma promessa / html | Aplicar itálico a «Memorial do Convento» no texto corrido. |
| V272 | #148, #150 | `m9/licao-m9-f03/index.html`; Cartão 5: Para entender / html | Aplicar itálico a «Memorial do Convento» no texto corrido. |
| V273 | #148, #150 | `m9/licao-m9-f03/index.html`; Cartão 5: Para entender / html | Aplicar itálico a «Memorial do Convento» no texto corrido. |
| V274 | #145, #148, #150 | `m9/licao-m9-f05/index.html`; Cartão 2: O essencial / html | Aplicar itálico a «Memorial do Convento» no texto corrido. |
| V275 | #148, #150 | `m9/licao-m9-f11/index.html`; Cartão 13: Para levar / html | Aplicar itálico a «Memorial do Convento» no texto corrido. |
| V276 | #148, #150 | `m9/licao-m9-f12/index.html`; Cartão 13: Para levar / html | Aplicar itálico a «Memorial do Convento» no texto corrido. |
| V277 | #148, #150 | `m9/licao-m9-f13/index.html`; Cartão 23: Para levar / html | Aplicar itálico a «Memorial do Convento» no texto corrido. |
| V282 | #145, #148, #150 | `tarefas/m9-u2/index.html`; Textos e condições de consulta | Aplicar itálico a «Memorial do Convento» no texto corrido. |

## Validação

02/11/2026: os números desta secção são os da volta de 01/11. Os atuais estão em «Volta sobre o main de 02/11/2026», no fim.

* Bateria unitária completa: 387 testes, todos aprovados, incluindo a língua e os cinco testes novos de âmbito e integridade.
* Nove camadas verificadas por `scripts/verificar_camadas.py`, sem reescrever manifestos anteriores. A nova camada tem 151 trocas em 122 ficheiros. A exceção histórica da página regenerada M7-U3 conserva o seu contrato de predecessor e sucessor nos testes.
* Opções: 2848 perguntas na regra; zero respostas denunciadoras; 730 grupos fora dos 20 % e 741 com a certa estritamente mais longa, exatamente como na base. Esta revisão não aumenta nenhuma destas contagens.
* Hierarquia: 545 páginas, a 390 e 1366 px, 1090 medições. Base e revisão têm os mesmos totais: R1 35, R2 4, R3 8, R5 0. Zero erros de abertura e nenhum aumento por página e largura. Os casos anteriores ficam fora desta intervenção de formatação.
* Navegador específico: 230 aberturas das 115 páginas HTML corrigidas, a 390 e 1366 px, com verificação do itálico do exame, créditos e escape de HTML. Acrescenta o lançamento dos cartões dos três painéis com títulos corrigidos, nas duas larguras.
* Painéis: 69 perguntas lançadas nos quatro painéis da verificação existente. Aquecimentos do M2: seis percursos completos, com respostas certas e as duas alternativas erradas.
* A bateria integral de navegador contém 53 comandos distintos: 51 em Python e dois em Node. A execução local e a integração contínua, incluindo as repetições das verificações adaptadas, são acompanhadas no [pedido #152](https://github.com/pedrohfernandes-klk/pt/pull/152). A descrição do pedido regista o estado final e as ligações às execuções.

As adaptações dos testes têm comentário de 01/11/2026. Não se retiram testes nem se reduzem os limiares. As alterações da infraestrutura que também aparece noutros pedidos limitam-se ao registo da camada, à reversão antes dos contratos congelados, à comparação do texto visível e à execução equivalente no Windows.


## Volta de confirmação da revisão de 01/11/2026

Revista a cabeça ba36cf2c, que já restringia a normalização aos marcadores de itálico. Os 361 pontos originais conservam os seus destinos: 239 corrigidos, 13 conformes e 109 adiados. As correções seguintes respondem aos achados adicionais, sem os contar como pontos novos da varredura original.

| Grupo de achados | Correção aplicada | Verificação |
|---|---|---|
| Foco, perguntas, opções e retornos do exame | Os dois usos de focus e os três campos de question() usam o formatador seguro f(). | Todas as sessões e cinco fases, nas duas larguras; retorno revelado e ausência de marcadores visíveis. |
| Exportação do dossiê | A cópia legível retira apenas os marcadores de itálico dos dados de estudo; a cópia JSON de reposição conserva os originais. | Exportação com todas as sessões, sem marcadores no texto visível; conteúdo de reposição igual aos dados iniciais. |
| Palavras tocáveis da M7-F01 | Itálico em cada uma das quatro palavras, mantendo oito peças e certas [4,5,6,7]. O painel M7-F01 tem a mesma frase e retorno. | Teste de marcadores por palavra em todos os cartões sublinhar/riscar; navegador: oito peças, quatro itálicos e nenhum sublinhado visível. Igualdades estritas repostas. |
| Crédito de Pessoa, três páginas | Peça .tabela visível, 0,8125 rem/1,4; autor desconhecido, obra, data incerta, origem e licença explícitos. Texto alternativo coerente. Ligação M7-F01 reposta no mapa. | Verificação da legenda e da ligação, tamanho da letra e ausência de deslocamento horizontal. Inspeção a 320 px. |
| Fontes de Lupi | Aspas equilibradas e título em itálico no HTML e nos dados E.fontes. | Conferência da camada reversível e abertura da página. |
| Migalhas das duas visitas | Texto e itálico dentro de um único elemento em linha. | Texto visível contém «cena: Farsa» e «palco: Frei». |
| Versos e rótulos | Cada verso num span.vl, com recolhido na continuação; rótulo em coluna própria. A citação breve de prosa em gram-anafora conserva a barra. | Seis leituras a 320 px, sem deslocamento e com estilos de bloco/recolhido; teste anterior conserva o mínimo de 20 exemplos. |
| Fonte de Camões | A estância IX, 89 segue «Que as Ninfas do Oceano tão formosas,» e «Tethys, e a ilha angélica pintada,». | [Fonte aberta e conferida](https://oslusiadas.org/ix/89.html); grafia da fonte mantida. |
| Notas de vocabulário | Entradas em linhas distintas, termos iniciais a negrito; eliminadas as colisões entre separadores e definições, incluindo pena, pronomes, modalidades, subordinadas e PEP/ASA. | Inspeção dos oito casos apontados e das notas de flores-verde-pino, eca-hotel e quinta-mandamentos. |
| Travessões e rótulos restantes | Rótulos A./B./C./D., II./IV.; análise de formação de palavras com dois pontos; Cândido com dois pontos; retorno de questionários com vírgula. | Camada e aberturas do navegador. O texto citado das obras não foi reformulado. |
| Resumo de Tabacaria | Campos estáticos vazios; quatro valores de recurso do JavaScript passam a «(sem resposta)». | Não há travessão no ficheiro; inclui o valor usado na cópia do texto. |
| Títulos e formulações | Título completo de TPC em itálico, Sermoens em itálico, regência «Na Farsa», contraste «lá/cá», emblemas de Cândido e dos provérbios clarificados. | Conferência editorial e fonte/página na camada. |
| Aquecimentos M1-U2, M2-U1 e M2-U2 | Fontes JSON e páginas iguais; exemplos criados em itálico, discurso direto com aspas portuguesas. | Comparação direta com o gerador e com o baralho publicado; teste de navegador não converte aspas esperadas. |
| Falas criadas e citações | Lista literal fechada de quatro casos já identificados como inventados, anteriormente em aspas curvas. Nenhuma frase nova se aceita por ser apenas marcada «inventada». | Teste exige todas as falas presentes e identificadas; rejeita alteração, atribuição a obra e citação fabricada. As citações literárias continuam conferidas nas fontes. |
| Servidor de provas | Conserva o funcionamento no Windows, mas devolve 404 fora de /pt/. | Teste de provas intacto; comentário datado no transporte local. |
| Terminações de linha | Gerador de aquecimentos escreve LF; quatro contratos exigem ausência de CR nas páginas publicadas. | Verificação de bytes em todos os sistemas, além das comparações de geração. |
| Relatório | V012, V078, V253 e V295 alinhados com o conteúdo aplicado. | Não há pontos dos 361 adiados exclusivamente pelo #147; o registo de pedidos preserva a fotografia da classificação inicial. |

### Divergências fundamentadas

A V253 mantém o itálico palavra a palavra, conforme três pareceres, em vez de o adiar: o navegador confirma quatro elementos i nas oito peças e nenhum marcador visível. O motor suporta esta solução sem alteração dos índices.

Nas notas, as propostas alternativas de pontuação foram conciliadas com uma entrada por linha. Adotaram-se «pena: pluma e sofrimento (duplo sentido)», parênteses nas modalidades e ponto final antes de comentários explicativos. As divisões automáticas não criam entradas novas.

A lista literal de falas criadas cobre apenas o discurso direto que já existia em casos explicitamente inventados. A mudança de aspas tornava essas falas falsos candidatos a citações literárias. O teste novo passa a conferir o que antes estava em aspas curvas e não era verificado, mantendo o controlo das citações genuínas e das passagens reservadas.

### Ordem de integração

02/11/2026: feito. A cadeia entrou no main antes deste pedido, que juntou o main por merge e pôs a camada no topo (ver a secção seguinte).

Propõe-se confirmar e integrar primeiro a cadeia #144, #145, #148, #150 e os pedidos #149/#154, e só depois integrar o #152. A equipa deve trazer as bases aprovadas por merge, nunca por rebase, conforme a instrução do docente. A varredura ficará no topo de LAYERS e das cadeias de desfazer após esse merge, com nova execução integral dos testes. Não se resolveu esta dependência fundindo pedidos ainda em revisão nem alterando os seus ramos.

### Resultados desta volta

387 testes unitários aprovados; nove camadas conferidas; 2848 perguntas, zero incumprimentos; 230 aberturas das páginas corrigidas, duas larguras, além de todas as fases do exame e da exportação; seis leituras em verso a 320 px inspecionadas. Os seis percursos dos aquecimentos M2 passaram, com respostas certas e duas alternativas erradas. A hierarquia teve 1090 medições: R1 35, R2 4, R3 8 e R5 0, sem aumento por página e largura face à cabeça anterior. Os resultados dos fluxos longos do GitHub são registados na descrição do pedido, com a cabeça efetivamente enviada.

Fora desta camada: o rótulo de m7/caeiro-olhar, identificado pelo parecer como exterior ao pedido, mantém-se para a volta própria.

## Volta sobre o main de 02/11/2026

O ramo juntou o main `fe2d829e` por merge, já com os pedidos #144 a #151, #154, #161 (tarefas individuais) e #162 (calçada). Nada foi reescrito nos ramos dos outros pedidos.

| Peça | O que mudou | Verificação |
|---|---|---|
| Camada | Refeita em trocas mínimas sobre o main: 647 trocas em 119 ficheiros (112 páginas, 4 JSON, 2 JS e 1 CSS); a maior troca tem 278 carateres. Cada troca tem o «antigo» no main e o «novo» uma só vez no fim. | Aplicada sobre o main, reproduz os ficheiros finais sem nenhuma diferença; desfeita, volta ao main. |
| Cadeia | `varredura_formatacao_20261101` no topo de LAYERS, das cadeias de desfazer dos testes, de `scripts/desligar_sala.py` e dos `--desfazer-antes` dos quatro fluxos. | `scripts/verificar_camadas.py`: 17 de 17 camadas conferidas. |
| Aquecimentos M1-U2, M2-U1 e M2-U2 | As páginas passam a vir só do gerador (`scripts/aquecimentos.py`), a partir dos JSON corrigidos; saem da camada. | Página gerada igual à do ficheiro, nos três casos. |
| Conflitos | Oito páginas com mudanças no main e na varredura ficaram com as duas: o texto do main e a formatação da varredura (m6/antero-deus incluída). | Comparação troca a troca com a intenção registada. |
| Rótulos | «A.», «B.», «C.», «D.», «II.» e «IV.» a negrito, sem travessão nem dois pontos encadeados, em dez páginas; Cândido com nota em linha própria. | Teste novo de rótulos; o rótulo de m7/caeiro-olhar fica para a volta própria, como já estava dito. |
| Versos com rótulo | Regra geral de `lesson.css` reduzida ao recolhido do verso (`.verso .vl`); a coluna do rótulo fica só nas quatro páginas que a pedem, com estilo próprio. Os rótulos de fala das lições («Fidalgo:», «Sapateiro:») deixam de ficar por cima do verso. | Navegador, M2-F12 e M2-F13 a 390 e 1366 px: o texto do rótulo acaba antes do primeiro caráter do verso. Com a regra antiga, o teste falha (33 px sobrepostos). |
| Painel M9-F07 | Itálico igual ao da lição nos cartões 12 e 13. | Teste novo: o itálico de cada cartão do painel é igual ao da lição; navegador conta os itálicos. |
| Relatório | Os 89 «Depois» que mudaram foram regenerados a partir dos ficheiros atuais. | Teste novo: o «Depois» de cada um dos 239 pontos corrigidos está no texto visível, pela ordem. |

### Resultados de 02/11/2026

443 testes unitários aprovados; 17 camadas conferidas; opções com 2991 perguntas, zero denunciadoras, 730 grupos fora dos 20 % e 741 com a certa mais longa, exatamente como no main. Os testes de navegador e os fluxos do GitHub ficam registados na descrição do pedido, com a cabeça enviada.
