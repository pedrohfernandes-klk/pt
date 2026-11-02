"""Revisão individual dos cartões: prova, retorno e sequência da leitura."""

# Índices anteriores à reordenação, depois da recuperação inicial.
ERROS = {
 'm8-f13': {
 4: ('Confundes repetição com ausência de mudança na relação. Relê a ligação entre «gastámos» e «não chega».', 'Confundes desgaste figurado com mudança de referente. Relê o que falta às palavras na relação entre as duas pessoas.'),
 11: ('Confundes a recordação de abundância com recuperação presente. Confronta as marcas de passado com o que resta agora.', 'Transferes para o passado a despedida que a voz vive agora. Relê o contraste entre a recordação e a insuficiência presente.'),
 15: ('Mudar o lugar não demonstra uma mudança do vínculo. Retoma a diferença entre conservar as palavras e perder a sua força na relação.', 'Mudar a pessoa não mostra como a mesma saudação perde força. Retoma a relação entre repetição verbal e transformação afetiva.'),
 18: ('Confundes uma leitura da voz com uma afirmação biográfica. Relê «a voz»: a expressão atribui a dimensão afetiva ao poema.', 'Confundes interpretar uma imagem com identificar a vida do autor. Relê «a imagem»: a expressão mantém a análise dentro do texto.')},
 'm8-f14': {
 4: ('Invertem-se o incidente e o impulso de escrever. Relê o que a voz decide fazer depois de a tigela cair.', 'Transformas uma experiência doméstica em memória pública já confirmada. Relê a passagem da tigela para a escrita: o valor está a ser interrogado.'),
 11: ('Transferes um prestígio pronto em vez de examinar o critério. Confronta a tigela com os vestígios a que se atribui importância.', 'Confundes antiguidade com justificação de valor. Relê a diferença entre a resistência do material e a memória humana.'),
 15: ('Confundes preço com o valor que a legenda deve justificar. Relê a distinção entre valor material, afetivo e histórico.', 'Confundes raridade com uma prova de importância humana. Relê os três critérios e procura a relação concreta que sustenta a legenda.'),
 18: ('Confundes tema comum com equivalência das vozes. Regressa ao modo como cada voz transforma o objeto em pergunta.', 'Pressupões um sentido fixo antes de comparar os textos. Regressa às relações que cada poema constrói em torno do objeto.')},
 'm8-f15': {
 4: ('Confundes informação sobre a autora com identificação da voz poética. Relê a distinção entre autoria e enunciação em «O essencial».', 'Alargas a reportagem à origem de poemas que ela não documenta. Relê a apresentação de «Mundo» e o âmbito indicado para a fonte.'),
 11: ('Pressupões um episódio biográfico em vez de o demonstrar. Relê o modelo: a aproximação não fornece uma certidão do acontecimento.', 'Pressupões que a voz reproduz uma declaração da autora. Relê a distinção entre a declaração documentada e o indício no poema.'),
 15: ('Confundes paráfrase com transcrição literal. Volta às palavras que efetivamente consultaste na apresentação da RTP.', 'Atribuis à voz poética uma síntese da reportagem. Confere a origem da formulação antes de escolher quem a enuncia.'),
 18: ('Trocar o nome do objeto não torna distintas as posições das vozes. Relê a diferença entre quem escreve e quem fala.', 'Deduzes duas vozes da biografia sem prova textual. Regressa ao modelo de confronto entre contexto e indício no poema.')},
 'm8-f16': {
 4: ('Confundes pensamento com fala pronunciada. Relê a indicação de que George não se disse aquilo.', 'Confundes correção interior com uma recordação comunicada. Relê a passagem da figura percebida para as palavras pensadas.'),
 11: ('Confundes recusar uma expressão com rejeitar a pessoa observada. Relê as duas maneiras de nomear a idade.', 'Introduzes uma resposta da outra mulher que o recorte não apresenta. Relê apenas o que é atribuído ao pensamento de George.'),
 15: ('Transformas pensamento em diálogo e alteras o acontecimento. Regressa ao critério: conservar apenas o que se observa de fora.', 'Mudas a pessoa que pensa em vez de restringir o acesso interior. Regressa ao critério do observável e localiza a informação mental.'),
 18: ('Transformas uma hipótese sobre a velhice numa conclusão antecipada. Relê a recusa da expressão e procura no conto o que a pode limitar.', 'Atribuis hostilidade às duas mulheres sem prova recíproca. Relê a assimetria: o recorte dá acesso ao pensamento de George.')},
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

VF = {
 'm8-f13': {1: ('Antes de reler. Na leitura anterior, distinguir voz poética e autor impedia transformar a primeira pessoa em prova biográfica?', True), 5: ('O plural da abertura indica uma despedida vivida pelo autor e por outra pessoa real.', False)},
 'm8-f14': {5: ('A referência à filha situa uma relação dentro do poema; confirmar o episódio na vida da autora exige outra fonte.', True),12: ('Reconhecer a ironia exige explicar a aproximação entre o episódio doméstico e o prestígio dos vestígios.',True)},
 'm8-f15': {1: ('Antes de reler. Na F05, «Ana Luísa Amaral: reescrever a tradição», distinguir autora e voz poética permitia usar informação biográfica sem a tomar como prova do poema?',True),12: ('Distinguir autora e voz poética torna inútil o contexto biográfico na interpretação.',False)},
 'm8-f16': {5: ('O recorte dá acesso a uma correção pensada por George, sem a apresentar como resposta dita à outra mulher.',True),12: ('A figura completar-se na perceção de George significa que a narração já apresentou a sua biografia.',False)},
 'm9-f14': {1: ('Antes de reler. Na abertura do romance, caracterizar uma figura histórica exigia distinguir a construção ficcional do registo documental?',True),12: ('A representação satírica pode explorar uma figura histórica sem documentar os seus gestos reais.',True)},
 'm9-f15': {5: ('O contraste entre a leitura tranquila e as sentenças permite questionar a solenidade da cerimónia.',True),12: ('A referência à multidão indica que cada pessoa teve a mesma reação à cerimónia.',False)},
 'm9-f16': {5: ('Uma ação longa pode ser apresentada como um todo concluído, como no exemplo «trabalhou durante três anos».',True),12: ('A relação entre ação em curso e interrupção ajuda a explicar o contraste entre a vida individual e a continuidade da obra.',True)}
}

ORDENS = {
 'm8-f13':[0,1,2,3,4,6,5,7,10,8,11,9,13,12,14,16,15,17,18,19],
 'm8-f14':[0,1,2,3,4,5,6,7,8,10,9,11,13,14,12,15,16,18,17,19],
 'm8-f15':[0,1,2,3,5,4,6,7,11,8,10,9,13,14,15,12,16,17,18,19],
 'm8-f16':[0,1,2,3,4,5,7,6,8,11,10,9,13,12,15,14,16,18,17,19],
 'm9-f14':[0,1,2,3,6,4,5,7,8,9,10,11,13,12,14,15,17,16,18,19],
 'm9-f15':[0,1,2,3,4,6,5,7,10,11,8,9,13,15,14,12,16,17,18,19],
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
            'm8-f14':{1:'Antes de reler. Na F05, a referência à filha confirmava que o acontecimento do poema pertencia à biografia da autora?'},
            'm8-f15':{5:'A primeira pessoa de um poema identifica a pessoa real que assina o livro.'},
            'm9-f14':{5:'A montagem da miniatura demonstra a incapacidade do rei para governar.'},
            'm9-f15':{1:'Antes de reler. Na cena da miniatura, o gesto de montagem demonstrava a intenção pessoal do rei?'},
            'm9-f16':{1:'Antes de reler. Na F05, identificar quem executa o trabalho permitia determinar a duração da ação?'}}
        for i,prompt in false_claims.get(key,{}).items():
            cards[i]['p']=prompt
        for i,wrong in ERROS[key].items():
            c=cards[i]
            assert c['t']=='escolha' and c['c']==0
            c['fe']=[c['f'],*wrong]
        for i,(question,value) in VF[key].items():
            cards[i].update(p=question,v=value)
        # 01/11/2026: a sequência decorre da comparação própria de cada obra.
        item['cards']=[cards[i] for i in ORDENS[key]]
