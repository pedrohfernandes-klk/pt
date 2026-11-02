"""Revisão individual dos cartões: prova, retorno e sequência da leitura."""

# Índices anteriores à reordenação, depois da recuperação inicial.
ERROS = {
 'm8-f13': {
 4: ('Confundes repetição com ausência de mudança na relação. Relê a ligação entre «gastámos» e «não chega».', 'Confundes desgaste figurado com mudança de referente. Relê o que falta às palavras na relação entre as duas pessoas.'),
 11: ('Confundes a recordação de abundância com recuperação presente. Confronta as marcas de passado com o que resta agora.', 'Transferes para o passado a despedida que a voz vive agora. Relê o contraste entre a recordação e a insuficiência presente.'),
 15: ('Mudar o lugar não demonstra uma mudança do vínculo. Retoma a diferença entre conservar as palavras e perder a sua força na relação.', 'Mudar a pessoa não mostra como a mesma saudação perde força. Retoma a relação entre repetição verbal e transformação afetiva.'),
 18: ('Confundes uma leitura da voz com uma afirmação biográfica. Relê «a voz»: a expressão atribui a dimensão afetiva ao poema.', 'Confundes interpretar uma imagem com identificar a vida do autor. Relê «a imagem»: a expressão mantém a análise dentro do texto.')},
 'm8-f14': {
 4: ('Opões o incidente ao impulso de escrever, quando é ele que o desperta. Relê o que a voz tem vontade de fazer depois de a filha partir a tigela.', 'Transformas uma experiência doméstica em memória pública já confirmada. Relê a passagem da tigela para a escrita: o valor está a ser interrogado.'),
 11: ('Transferes um prestígio pronto em vez de examinar o critério. Confronta a tigela com os vestígios a que se atribui importância.', 'Confundes antiguidade com justificação de valor. Relê a diferença entre a resistência do material e a memória humana.'),
 15: ('Confundes preço com o valor que a legenda deve justificar. Relê a distinção entre valor material, afetivo e histórico.', 'Confundes raridade com uma prova de importância humana. Relê os três critérios e procura a relação concreta que sustenta a legenda.'),
 18: ('Confundes tema comum com equivalência das vozes. Regressa ao modo como cada voz transforma o objeto em pergunta.', 'Pressupões um sentido fixo antes de comparar os textos. Regressa às relações que cada poema constrói em torno do objeto.')},
 'm8-f15': {
 4: ('Confundes informação sobre a autora com identificação da voz poética. Relê a distinção entre autoria e enunciação em «O essencial».', 'Alargas a reportagem à origem de poemas que ela não documenta. Relê a apresentação de _Mundo_ e o âmbito indicado para a fonte.'),
 11: ('Pressupões um episódio biográfico em vez de o demonstrar. Relê o modelo: a aproximação não fornece uma certidão do acontecimento.', 'Pressupões que a voz reproduz uma declaração da autora. Relê a distinção entre a declaração documentada e o indício no poema.'),
 15: ('Confundes paráfrase com transcrição literal. Volta às palavras que efetivamente consultaste na apresentação da RTP.', 'Atribuis à voz poética uma síntese da reportagem. Confere a origem da formulação antes de escolher quem a enuncia.'),
 18: ('Trocar o nome do objeto não torna distintas as posições das vozes. Relê a diferença entre quem escreve e quem fala.', 'Deduzes duas vozes da biografia sem prova textual. Regressa ao modelo de confronto entre contexto e indício no poema.')},
 'm8-f16': {
 4: ('Confundes pensamento com fala pronunciada. Relê «mesmo só pensados»: a correção acontece no pensamento de George, não numa resposta dita.', 'Confundes correção interior com uma recordação comunicada. Relê a passagem da figura percebida para as palavras pensadas.'),
 11: ('Confundes recusar uma expressão com rejeitar a pessoa observada. Relê as duas maneiras de nomear a idade.', 'Introduzes uma resposta da outra mulher que o recorte não apresenta. Relê apenas o que é atribuído ao pensamento de George.'),
 15: ('Transformas pensamento em diálogo e alteras o acontecimento. Regressa ao critério: conservar apenas o que se observa de fora.', 'Mudas a pessoa que pensa em vez de restringir o acesso interior. Regressa ao critério do observável e localiza a informação mental.'),
 18: ('Transformas uma hipótese sobre a velhice numa conclusão antecipada. Relê a recusa da expressão e procura no conto o que a pode limitar.', 'Atribuis às duas mulheres uma hostilidade recíproca sem prova. Relê a assimetria: o recorte só dá acesso ao pensamento de George.')},
 'm9-f14': {
 4: ('Transformas um gesto de montagem em prova de eficácia política. Relê o contraste entre a escala do objeto e a grandeza encenada.', 'Transformas a réplica em prova da devoção pessoal. Relê o que a cena mostra do uso do objeto, sem deduzir a intenção.'),
 11: ('Apagas a diferença entre montar uma réplica e construir o edifício. Regressa aos riscos e às condições materiais de cada trabalho.', 'Reduzes as condições de trabalho à dimensão do objeto. Relê o limite da analogia: escala, risco e trabalho são relações distintas.'),
 15: ('Aumentas a dimensão sem alterar quem recebe o reconhecimento. Relê na cena B a distribuição dos louvores e do trabalho.', 'Mudas quem recebe os louvores, mantendo invisível quem trabalha. Regressa ao contraste entre autoria reconhecida e contribuição efetiva.'),
 18: ('Tratas o objeto como símbolo de significado já decidido. Relê como o uso e o contraste de escala constroem o efeito.', 'Substituis a caracterização pelo objeto por uma explicação direta. Regressa ao gesto de montagem que torna observável a autoridade.')},
 'm9-f15': {
 4: ('Transferes o modo de ler para quem recebe a sentença. Relê a quem pertence a leitura «descansada» e quem suporta as consequências.', 'Deduzes acordo do público a partir da tranquilidade descrita. Relê a diferença entre posição observável e intenção atribuída.'),
 11: ('Confundes solenidade com justiça das consequências. Regressa à distância entre a leitura tranquila e o destino dos condenados.', 'Deduzes a reação dos condenados a partir de outro grupo. Regressa às posições distintas de quem assiste e de quem recebe a sentença.'),
 15: ('Transformas tranquilidade em prova de acordo. Relê o que a descrição permite observar e o que não diz sobre cada intenção.', 'Transformas tranquilidade em prova de inocência. Relê a descrição: o modo de estar não decide a responsabilidade de quem aparece.'),
 18: ('Mudar adjetivos pode conservar o mesmo ponto de vista. Relê a diferença entre a posição de quem assiste e a de quem é exposto.', 'Conservas a posição de observação e perdes o contraste pedido. Regressa às duas experiências que a mesma praça reúne.')},
 'm9-f16': {
 4: ('Confundes ação em curso com ação apresentada como terminada. Relê a construção verbal que situa o trabalho no seu decorrer.', 'Confundes duração em curso com ação projetada no futuro. Relê o momento em que o trabalho é interrompido.'),
 11: ('Confundes o trabalho em curso com a duração tomada como um todo. Compara «estava a trabalhar» com «durante três anos».', 'Confundes repetição habitual com duração concluída. Repara no alcance de «todas as manhãs» e compara-o com «durante três anos».'),
 15: ('Mudas o agente e a ação, não apenas o modo de apresentar o tempo. Compara a pessoa que caminha nas duas formulações.', 'Introduzes um acontecimento diferente em vez de alterar o aspeto. Mantém a caminhada e confronta o seu decorrer com o seu limite.'),
 18: ('Confundes relação temporal com prova de responsabilidade. Relê a interrupção e separa o que aconteceu da explicação da causa.', 'Transformas a duração da obra em medida do valor de uma vida. Regressa ao contraste entre continuidade coletiva e interrupção individual.')}
}

# 01/11/2026 (confirmação): o terceiro elemento, quando existe, substitui o retorno do cartão.
VF = {
 'm8-f13': {1: ('Antes de reler. Na lição sobre Jorge de Sena, distinguir a testemunha do poema da presença biográfica do autor impedia ler a primeira pessoa como relato vivido?', True,
                'Confundir pessoa gramatical e identidade biográfica transforma um poema em documento sem prova. Regressa a «Jorge de Sena, poeta testemunha»: a testemunha do poema não se confunde com uma presença biográfica no acontecimento.'),
            5: ('O plural da abertura indica uma despedida vivida pelo autor e por outra pessoa real.', False),
            12: ('No poema completo, o silêncio recebe um tratamento diferente das palavras gastas.', True)},
 'm8-f14': {5: ('A referência à filha situa uma relação dentro do poema; confirmar o episódio na vida da autora exige outra fonte.', True),12: ('Reconhecer a ironia exige explicar a aproximação entre o episódio doméstico e o prestígio dos vestígios.',True)},
 'm8-f15': {1: ('Antes de reler. Na F05, «Ana Luísa Amaral: reescrever a tradição», distinguir autora e voz poética permitia usar informação biográfica sem a tomar como prova do poema?',True),12: ('Sem uma declaração da autora sobre o poema, a leitura deve pôr de parte o contexto biográfico.',False)},
 'm8-f16': {5: ('O recorte dá acesso a uma correção pensada por George, sem a apresentar como resposta dita à outra mulher.',True),12: ('Dizer que a figura fica completa na perceção de George significa que a narração já apresentou a vida da senhora observada.',False)},
 'm9-f14': {1: ('Antes de reler. Na abertura do romance, caracterizar uma figura histórica exigia distinguir a construção ficcional do registo documental?',True),12: ('A representação satírica pode explorar uma figura histórica sem documentar os seus gestos reais.',True)},
 'm9-f15': {5: ('O contraste entre a leitura tranquila e as sentenças permite questionar a solenidade da cerimónia.',True),
            12: ('A referência à multidão indica que cada pessoa teve a mesma reação à cerimónia.',False,
                 'Uma referência coletiva não individualiza as reações. Para afirmar o que sente cada pessoa, o texto teria de distinguir alguém dentro do grupo.')},
 'm9-f16': {5: ('No exemplo criado «trabalhou durante três anos», uma ação longa é apresentada como um todo concluído.',True),
            12: ('A relação entre ação em curso e interrupção ajuda a explicar o contraste entre a vida individual e a continuidade da obra.',True,
                 'Identificar as formas é só o primeiro passo. A ação em curso interrompida pelo acidente torna percetível a perda de uma vida, enquanto a obra continua.')}
}

# 01/11/2026 (confirmação): retorno de erro dos cartões de fazer que não são escolha, pelos índices anteriores à
# reordenação. Uma frase nomeia a confusão; a outra indica o sítio exato a reler, sem posição na página.
RELEITURAS = {
 'm8-f13': {
  1: 'Deixas de separar a testemunha do poema da vida do autor. Relê a linha de vida de «Jorge de Sena, poeta testemunha»: os fuzilamentos são de 1808 e Sena nasce em 1919.',
  5: 'Tomas a pessoa gramatical por prova biográfica. Relê «gastámos» e pergunta que fonte, fora do poema, diria quem viveu a despedida.',
  6: 'Trocas o nome de cada recurso pela observação de outro. Relê, em «O essencial», as definições de metáfora e de repetição e confronta-as com os dois versos citados.',
  8: 'Confundes o plano material da imagem com o plano afetivo da relação. Relê a relação descrita em «Um modelo de interpretação»: «o que era partilhado já não chega para sustentar o vínculo».',
  9: 'Pões a conclusão antes da prova que a sustenta. Relê a sequência de «Um modelo de interpretação»: observação, relação e limite, por esta ordem.',
  10: 'Escolhes os verbos em vez das palavras que os situam no tempo. Relê a frase criada e procura o que coloca cada verbo num momento diferente da relação.',
  12: 'Estendes o desgaste das palavras a tudo o que o poema apresenta. Relê o contraexemplo de «Muda uma decisão»: «o silêncio recebe um tratamento diferente».',
  14: 'Confundes o alcance de cada formulação com o tema que partilham. Relê, em «Muda uma decisão», o que separa um limite situado numa relação de uma regra universal.',
  16: 'Confundes a mudança de um vínculo com uma lei sobre o amor. Relê o limite de «Um modelo de interpretação»: «isso não demonstra que a linguagem seja inútil em todas as relações».',
  17: 'Antecipas o limite antes da imagem e do contraste que ele qualifica. Relê o modelo completo de «Um modelo de interpretação»: imagem, insuficiência atual e, só depois, o alcance da conclusão.'},
 'm8-f14': {
  1: 'Tomas a relação familiar enunciada no poema por um dado da vida da autora. Regressa à F05, à leitura de «A verdade histórica»: localiza um indício «sem o tomares como episódio biográfico».',
  5: 'Recusas a distinção entre a cena do poema e a vida da autora. Relê, em «O essencial», que esse cruzamento «não autoriza tratar cada acontecimento do poema como prova biográfica».',
  6: 'Separas os três planos da passagem que os encadeia no poema. Relê «Uma ocorrência doméstica»: os versos vão da tigela partida à vontade de escrever, e a indicação de leitura leva até à imaginação de um futuro distante.',
  8: 'Confundes o valor imaginado com uma mudança material ou com uma descoberta real. Relê, em «Do fragmento ao valor», a aproximação da tigela a objetos «a que o tempo e a história dão prestígio».',
  9: 'Começas pela pergunta crítica sem o contraste que a faz nascer. Relê o modelo de «Do fragmento ao valor»: identificar uma mudança de escala, explicar o contraste e perguntar quem atribui valor.',
  10: 'Escolhes a ação imaginada em vez da palavra que a apresenta como possibilidade. Relê a frase criada e procura o que impede de a ler como um facto comprovado.',
  12: 'Tratas o nome «ironia» como se bastasse para demonstrar a leitura. Relê, em «O essencial», a definição: a ironia põe em tensão o que parece importante e aquilo que normalmente passa despercebido.',
  14: 'Fazes de um critério a medida dos outros dois. Relê, em «O que resiste?», a pergunta sobre se durar muito e merecer memória são a mesma coisa.',
  16: 'Confundes persistência física com significado humano. Relê, em «O que resiste?», a associação entre a resistência de um material banal e o destino dos fragmentos.',
  17: 'Trocas a ordem entre o incidente, a escrita e a mudança de escala. Relê o modelo completo de «Do fragmento ao valor»: o objeto parte-se na cozinha e desencadeia a vontade de escrever.'},
 'm8-f15': {
  1: 'Lês a distinção entre autora e voz como uma proibição de usar a biografia. Regressa a «O essencial», na F05: a autora ensinou nas Letras do Porto, mas quem fala na prece é quem atravessa o mar.',
  5: 'Fazes coincidir quem assina o livro com quem fala no poema. Relê, em «O essencial», as definições de autora e de voz poética: pessoa real que escreve e instância construída no poema.',
  6: 'Trocas os planos da autoria, da enunciação e da construção jornalística. Relê, em «O essencial», as três definições: autora, voz poética e reportagem.',
  8: 'Atribuis à reportagem a função de prova ou de confissão. Relê o modelo completo de «Um modelo de confronto»: «Essa informação pode orientar uma pergunta ao poema».',
  9: 'Usas a fonte antes de saber o que ela afirma, ou esqueces o limite final. Relê «Um modelo de confronto»: a aproximação orienta uma pergunta e não fornece uma certidão do acontecimento.',
  10: 'Escolhes o que a informação faz em vez da palavra que limita esse alcance. Relê a frase criada e procura o que a apresenta como possibilidade, não como obrigação.',
  12: 'Tomas a falta de uma declaração como razão para afastar todo o contexto. Relê «Um modelo de confronto»: a atenção à vida quotidiana destacada pela reportagem permite investigar uma aproximação ao poema.',
  14: 'Atribuis a cada formulação um cuidado que não corresponde à sua natureza. Relê, em «Reconhecer uma atribuição», o que exigem as formulações A e B: conferir a apresentação e localizar a declaração exata.',
  16: 'Confundes citação e paráfrase, ou esqueces que a paráfrase também tem origem. Relê, em «Reconhecer uma atribuição», o aviso: «Não ponhas entre aspas uma paráfrase tua».',
  17: 'Pões a prova do poema antes da pergunta que o contexto permite formular. Relê o modelo completo de «Um modelo de confronto»: contexto público, pergunta ao poema e só depois a demonstração pela leitura.'},
 'm8-f16': {
  1: 'Confundes saber o que George pensa com ouvi-la falar a alguém. Relê, na F08, a definição de discurso direto em «Para entender»: as palavras da personagem, com travessão ou aspas.',
  5: 'Lês a correção como uma resposta dita à mulher observada. Relê «mesmo só pensados» e o modelo completo de «Uma correção que caracteriza»: as palavras podem ser apenas pensadas.',
  6: 'Ligas cada expressão do recorte a uma função que ela não cumpre. Relê «primeiro esboçada, finalmente completa» e «mesmo só pensados»: uma organiza a perceção, a outra situa as palavras no pensamento.',
  8: 'Confundes o que a narração dá a conhecer com uma biografia ou com uma fala. Relê, em «O essencial», que a voz narrativa pode aproximar-se do pensamento de uma personagem sem o apresentar como diálogo.',
  9: 'Trocas a ordem pela qual o recorte nomeia, recusa e volta a nomear a idade. Relê o recorte desde «uma senhora de idade» até «uma mulher velha» e segue o movimento da correção.',
  10: 'Escolhes uma palavra do retrato em vez da que nega a designação anterior. Relê a frase e procura o que recusa «de idade» antes de surgir a atitude de George.',
  12: 'Confundes a figura completa na perceção com uma vida contada. Relê «primeiro esboçada, finalmente completa»: estas palavras descrevem como a figura aparece, não a biografia da senhora.',
  14: 'Confundes um ato verbal com um pensamento ou com a falta de acesso a ele. Relê os exemplos A e B de «Experimenta uma mudança»: a mudança altera o que acontece entre as personagens e o acesso à interioridade.',
  16: 'Confundes o que o recorte permite analisar com o sentido do encontro no conto inteiro. Relê, em «As palavras confirmadas», a indicação: «As atividades seguintes usam apenas o recorte apresentado».',
  17: 'Pões a indicação de pensamento antes da correção que ela qualifica. Relê o modelo completo de «Uma correção que caracteriza»: recusa, atribuição a George e só depois as palavras apenas pensadas.'},
 'm9-f14': {
  1: 'Tratas a personagem do romance como registo direto da pessoa histórica. Relê, na F01, a definição de romance histórico em «Para entender»: ficção que se passa numa época real e usa figuras e factos dela.',
  5: 'Transformas um gesto isolado num juízo sobre a capacidade de governar. Relê, em «O essencial», a frase: «O objeto não tem um significado fixo fora do contexto».',
  6: 'Saltas do objeto para uma etiqueta sobre o rei sem passar pela relação. Relê, em «O essencial», como a caracterização indireta se faz através de ações, objetos e relações.',
  8: 'Confundes caracterização indireta com afirmação expressa, ou apagas as diferenças entre as duas obras. Relê «Comparar sem igualar»: não têm os mesmos materiais, riscos, custos humanos ou condições de execução.',
  9: 'Propões o efeito antes de observar o objeto, a ação e a escala. Relê o modelo completo de «Comparar sem igualar»: primeiro o gesto material associado à figura régia, depois a hipótese sobre a grandeza.',
  10: 'Escolhes o efeito descrito em vez da palavra que o apresenta como hipótese. Relê a frase criada e procura o que impede de a ler como conclusão automática sobre o rei.',
  12: 'Exiges que a sátira documente os gestos reais da pessoa histórica. Relê, em «O essencial», a frase: «Um romance histórico não é uma transcrição neutra do passado».',
  14: 'Atribuis a mesma pergunta a usos diferentes do objeto. Relê as cenas A e B de «Muda o enquadramento»: estudar uma estrutura não é o mesmo que receber louvores por encaixar uma peça.',
  16: 'Confundes a análise de uma representação literária com a comprovação documental de um facto. Relê, em «O essencial», que José Saramago constrói uma representação ficcional do reinado de D. João V.',
  17: 'Pões o limite da analogia antes da hipótese que ele qualifica. Relê o modelo de «Comparar sem igualar»: a escala reduzida interroga a grandeza encenada e o confronto com a obra real vem depois.'},
 'm9-f15': {
  1: 'Tomas um gesto observado como acesso direto à intenção de quem o faz. Relê, em «Um rei em miniatura», o critério de «Muda o enquadramento»: o efeito depende do enquadramento e das relações, não apenas do objeto.',
  5: 'Separas a palavra tranquila das consequências que a tornam crítica. Relê o modelo de «Dois planos em confronto»: um sinal de tranquilidade relaciona-se com as consequências da condenação.',
  6: 'Atribuis a quem assiste e a quem é condenado o mesmo problema de leitura. Relê, em «Dois planos em confronto», a aproximação entre o conforto da assistência e a vulnerabilidade dos condenados.',
  8: 'Uniformizas a experiência de quem vive a cerimónia, ou escondes o contraste que o narrador mostra. Relê o modelo completo de «Dois planos em confronto»: a diferença entre as posições produz a tensão.',
  9: 'Concluis sobre a ironia antes de mostrar a tensão que a produz. Relê, em «O essencial», a definição: a ironia pode surgir quando uma formulação tranquila entra em conflito com aquilo que está a acontecer.',
  10: 'Escolhes o que é lido em vez da palavra que qualifica o modo de ler. Relê o recorte e procura o adjetivo que sugere serenidade perante as sentenças.',
  12: 'Passas de uma referência coletiva para a reação de cada pessoa. Relê o critério de «Testa o mesmo procedimento»: uma conclusão sobre cada pessoa exige uma marca que a distinga dentro do grupo.',
  14: 'Igualas o exemplo criado ao episódio do romance. Relê, em «Testa o mesmo procedimento», o aviso: «Não é uma equivalência histórica com a Inquisição».',
  16: 'Confundes comparar um procedimento com igualar a gravidade dos acontecimentos. Relê, em «Testa o mesmo procedimento», a frase: serve apenas para observar um procedimento.',
  17: 'Pões o limite da inferência antes do contraste que ele qualifica. Relê o modelo completo de «Dois planos em confronto» e, depois, o critério de «Testa o mesmo procedimento».'},
 'm9-f16': {
  1: 'Confundes saber quem trabalha com saber durante quanto tempo trabalha. Relê, na F05, a lista de nomes de «A pedra e os nomes»: diz quem vai na viagem, não quanto tempo dura o trabalho.',
  5: 'Confundes ação concluída com ação breve. Relê, em «O essencial», a frase: «Uma situação longa pode ser apresentada como concluída».',
  6: 'Ligas cada exemplo a um valor sem observar os complementos que o acompanham. Relê, em «O essencial», os modos de apresentar uma situação: em curso, concluída, repetida.',
  8: 'Confundes a situação em curso com o seu resultado ou com uma repetição. Relê o modelo completo de «Mudar o recorte temporal»: «trabalhava» apresenta uma situação em curso e «cedeu» introduz uma ocorrência.',
  9: 'Interpretas o efeito antes de identificar as formas e os marcadores que o produzem. Relê o modelo completo de «Mudar o recorte temporal»: as formas verbais vêm antes da conclusão de que a relação produz interrupção.',
  10: 'Escolhes uma das ações em vez da palavra que as relaciona. Relê a frase e procura o que situa a ocorrência dentro da ação em curso.',
  12: 'Separas a análise das formas verbais do efeito humano da interrupção. Relê, em «A gramática não decide tudo», a frase: «A continuidade da obra não apaga essa perda».',
  14: 'Fazes do aspeto verbal a resposta a todas as perguntas sobre a cena. Relê, em «A gramática não decide tudo», a frase: «A relação temporal não demonstra, por si só, responsabilidade».',
  16: 'Isolas a forma verbal do contexto, ou a análise do efeito narrativo. Relê, em «O essencial», a frase: «A gramática participa no efeito narrativo».',
  17: 'Pões o limite da conclusão antes da interrupção e do contraste que ele qualifica. Relê «A gramática não decide tudo»: o acidente interrompe a ação de uma pessoa concreta, e a continuidade da obra não apaga essa perda.'}
}

ORDENS = {
 'm8-f13':[0,1,2,3,4,6,5,7,10,8,11,9,13,12,14,16,15,17,18,19],
 'm8-f14':[0,1,2,3,4,5,6,7,8,10,9,11,13,14,12,15,16,18,17,19],
 'm8-f15':[0,1,2,3,5,4,6,7,11,8,10,9,13,14,15,12,16,17,18,19],
 'm8-f16':[0,1,2,3,10,4,7,5,13,14,15,6,8,11,9,12,16,18,17,19],
 'm9-f14':[0,1,2,3,6,4,5,7,8,9,10,11,13,12,14,15,17,16,18,19],
 'm9-f15':[0,1,2,3,10,4,7,5,11,6,8,13,15,14,12,9,16,17,18,19],
 'm9-f16':[0,1,2,3,4,5,6,7,11,10,8,9,13,14,16,12,15,18,17,19]
}

def aplicar_confirmacao(bancos):
    for item in bancos:
        key=item['id']
        if key not in ERROS:
            continue
        cards=item['cards']
        endings={
            'm8-f13':'A recordação dá medida à perda presente. A leitura conserva a diferença entre palavras gastas e silêncio, sem transformar a despedida numa incapacidade universal de comunicar.',
            'm8-f14':'A tigela passa do incidente à escrita e à pergunta sobre a memória. A duração do material não decide o valor humano que a legenda precisa de justificar.',
            'm8-f15':'O dado biográfico abre uma pergunta, mas é o indício no poema que sustenta a resposta. Explicitar o limite impede transformar aproximação em acontecimento documentado.',
            'm8-f16':'A correção lexical revela uma atitude de George perante as palavras. Não revela uma biografia completa nem demonstra hostilidade entre as duas mulheres do encontro.',
            'm9-f14':'O gesto e a escala tornam observável uma encenação de grandeza. A comparação com a construção exige distinguir condições de trabalho e riscos, sem deduzir intenção pessoal.',
            'm9-f15':'A leitura tranquila contrasta com a gravidade das sentenças. A referência coletiva não demonstra a reação de cada pessoa, pelo que a análise distingue posições de intenções.',
            'm9-f16':'A ocorrência interrompe uma ação em curso, enquanto a obra continua. Este contraste explica um efeito humano, mas a relação temporal não demonstra a responsabilidade pelo acidente.'}
        cards[17]['f']=endings[key]
        if key=='m8-f15':
            cards[15]['o'][1]='Declaração da autora transcrita na apresentação da RTP.'
            cards[1]['f']='Confundir testemunho público e voz poética troca a natureza da fonte. Regressa a «Ana Luísa Amaral: reescrever a tradição»: a voz do poema é construída; uma declaração pública deve ser atribuída à pessoa e à ocasião em que foi feita.'
        if key=='m8-f13':
            cards[18]['f']='Afirmar que o autor viveu esta despedida é biografia sem prova. A voz e a imagem descrevem relações observáveis na construção do poema.'
        if key=='m8-f16':
            cards[18]['f']='Perguntar pela relação com o resto do conto procura relações no conjunto. Falar de rejeição da velhice ou de hostilidade recíproca pressupõe conclusões que o recorte não autoriza.'
        if key=='m9-f14':
            cards[18]['f']='Mostrar a autoridade pelo uso de um objeto testa a caracterização indireta. O objeto torna-se significativo através de ações e relações observáveis.'
            cards[11]['o']=['A escala altera os riscos e as condições de trabalho.', 'A escala muda o custo, mas conserva as condições de trabalho.', 'A escala explica o custo e as condições de trabalho.']
        if key=='m9-f15':
            cards[16]['frase']='Podemos comparar uma [1] narrativa sem tratar os acontecimentos como sendo de [2].'
        if key=='m9-f16':
            cards[15]['o'][0]='Passar de «estava a caminhar» para «caminhou até à porta».'
            cards[15]['f']='Passar de «estava a caminhar» para «caminhou até à porta» muda o recorte temporal da caminhada. Trocar a pessoa ou acrescentar uma queda muda a ação ou a personagem, e não apenas a sua apresentação.'
            cards[18]['f']='Ligar a rutura temporal à interrupção de uma vida articula forma e efeito humano. Não transforma a gramática em prova de culpa nem deixa o avanço da obra apagar a pessoa.'
        false_claims={
            'm8-f14':{1:'Antes de reler. Na F05, a referência à filha situava o acontecimento do poema na biografia da autora?'},
            'm8-f15':{5:'A primeira pessoa de um poema identifica a pessoa real que assina o livro.'},
            'm9-f14':{5:'A montagem da miniatura caracteriza o rei como incapaz de governar.'},
            'm9-f15':{1:'Antes de reler. Na cena da miniatura, o gesto de montagem dava acesso à intenção pessoal do rei?'},
            'm9-f16':{1:'Antes de reler. Na F05, identificar quem executa o trabalho permitia determinar a duração da ação?'}}
        for i,prompt in false_claims.get(key,{}).items():
            cards[i]['p']=prompt
        for i,wrong in ERROS[key].items():
            c=cards[i]
            assert c['t']=='escolha' and c['c']==0
            c['fe']=[c['f'],*wrong]
        for i,(question,value,*feedback) in VF[key].items():
            cards[i].update(p=question,v=value)
            if feedback:cards[i]['f']=feedback[0]
        # 01/11/2026 (confirmação): em cada cartão de fazer que não é escolha, o erro diz o que reler.
        for i,reread in RELEITURAS[key].items():
            assert cards[i]['t'] not in ('ler','escolha') and 'fe' not in cards[i]
            cards[i]['fe']=reread
        # Rótulos próprios das leituras: o recorte, o modelo e o contraexemplo.
        for i,label in ((3,'Lê de perto'),(7,'Para entender'),(13,'Compara')):
            assert cards[i]['t']=='ler'
            cards[i]['rot']=label
        # 01/11/2026: a sequência decorre da comparação própria de cada obra.
        item['cards']=[cards[i] for i in ORDENS[key]]
