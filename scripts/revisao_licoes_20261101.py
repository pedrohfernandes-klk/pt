"""01/11/2026: revisão da sequência efetiva segundo a adenda pedagógica.

Os bancos são integrais: não há seleção variável nem variantes p2. Cada tentativa
contém 14 respostas automáticas e uma produção oral explícita no Para levar.
"""
from html import escape

REVISOES = {
 'm8-f13': dict(
  recuperar=('Recupera a distinção da leitura anterior: uma voz em primeira pessoa identifica necessariamente o autor real?', False,
             'Confundir pessoa gramatical e identidade biográfica transforma um poema em documento sem prova. Na lição anterior, regressa à distinção entre a voz do poema e Eugénio de Andrade.'),
  modelo='A imagem inicial apresenta palavras como matéria que se gasta. A insuficiência atual relaciona essa imagem com o vínculo. A conclusão aplica-se a esta relação, não a toda a comunicação.',
  limite='Contraexemplo à ideia de que tudo no poema perdeu valor: o silêncio recebe um tratamento diferente. Critério: uma conclusão sobre todos os elementos só resiste se explicar também esse contraste.',
  pista='Compara o alcance da primeira formulação criada com o da segunda: a relação concreta passou a regra universal?',
  prova='Que duas palavras distinguem uma mudança na relação de uma impossibilidade sem história?',
  ordem=['As palavras surgem como matéria que se gasta','A insuficiência atual afeta o vínculo','A abundância passada torna a perda mais intensa','O tratamento do silêncio limita a generalização'],
  ordem_p='Ordena esta reconstrução da leitura, da imagem inicial ao limite da conclusão.',
  escolhas={3:['Perderam força dentro desta relação.','Ficaram repetidas sem alterar o vínculo.','Passaram a designar objetos diferentes.'],
            10:['Realça a perda sentida no presente.','Sugere que o vínculo está a recuperar.','Desloca a despedida para o passado.'],
            14:['Um encontro em que a saudação muda de efeito.','Um encontro em que muda apenas o lugar da saudação.','Um encontro em que muda só a pessoa que saúda.'],
            17:['O autor viveu exatamente esta despedida.','A voz dá à despedida uma dimensão afetiva.','A imagem liga a linguagem à perda do vínculo.']}),
 'm8-f14': dict(
  recuperar=('Recupera a leitura da F05: a referência a uma filha no poema basta para comprovar um episódio da vida da autora?',False,
             'Confundir uma cena enunciada com um facto biográfico apaga a construção poética. Relê, na F05, a atribuição da voz e a abertura do poema: a relação familiar está no texto, mas a comprovação pede outra fonte.'),
  modelo='O objeto parte-se na cozinha e desencadeia a vontade de escrever. O contraste faz do incidente matéria poética. A dimensão doméstica não o torna automaticamente um acontecimento público.',
  limite='Contraexemplo a uma celebração solene do objeto: a sua origem e o seu uso quotidiano persistem no poema. Critério: a leitura da grandeza tem de explicar os sinais que a fazem descer de escala.',
  pista='Distingue a mudança de valor imaginada de uma mudança material do objeto. A projeção no futuro é uma descoberta comprovada?',
  prova='Que marca do exemplo criado distingue atribuir valor de descobrir uma propriedade física?',
  ordem=['Um incidente doméstico chama a atenção da voz','O desejo de escrever transforma-o em matéria poética','O futuro imaginado altera a escala do valor','O uso quotidiano impede uma grandeza sem contraste'],
  ordem_p='Ordena a transformação do incidente numa reflexão sobre valor e história.'),
 'm8-f15': dict(
  recuperar=('Recupera a distinção das leituras anteriores: uma declaração da autora e uma fala do sujeito poético pertencem ao mesmo plano de prova?',False,
             'Confundir testemunho público e voz poética troca a natureza da fonte. Regressa à F05: a voz do poema é construída; uma declaração pública deve ser atribuída à pessoa e à ocasião em que foi feita.'),
  modelo='A reportagem apresenta uma autora e uma obra em contexto público. Essa informação pode orientar uma pergunta ao poema. Só a leitura do poema permite demonstrar o funcionamento de uma imagem.',
  limite='Contraexemplo à equivalência entre reportagem e poema: um texto jornalístico pode informar sobre uma publicação sem conter a voz que fala no poema. Critério: cada afirmação precisa de uma fonte que possa sustentá-la.',
  pista='Pergunta se a afirmação diz respeito à pessoa, à publicação ou à construção de uma voz. Procura a fonte adequada a esse plano.',
  prova='Que palavra neste exemplo impede identificar automaticamente uma pessoa e a voz que a obra constrói?',
  ordem=['A reportagem fornece um contexto público','Esse contexto permite formular uma pergunta','O poema oferece a prova da leitura literária','A atribuição distingue os dois planos'],
  ordem_p='Ordena a relação entre informação jornalística e interpretação, sem substituir uma pela outra.'),
 'm8-f16': dict(
  recuperar=('Recupera a leitura da F08: conhecer um pensamento de George é o mesmo que ouvi-la dizer esse pensamento a outra personagem?',False,
             'Confundir interioridade e diálogo acrescenta uma ação à narrativa. Na F08, recupera a distinção entre o que George pensa e o que é apresentado como fala dirigida a alguém.'),
  modelo='A correção lexical recusa uma designação atenuada. A narração atribui a recusa a George e acrescenta que as palavras podem ser apenas pensadas. Isso caracteriza uma atitude sem a transformar numa fala pronunciada.',
  limite='Contraexemplo à ideia de que uma designação direta é necessariamente dita em voz alta: o próprio recorte inclui palavras apenas pensadas. Critério: só atribuis uma fala pronunciada se o texto fornecer uma marca desse ato.',
  pista='Compara a informação disponível em chamar e em pensar sem dizer. O leitor pode saber algo que a outra personagem não ouviu.',
  prova='Que palavra distingue uma recusa da primeira designação de uma simples continuação do retrato?',
  ordem=['Uma designação atenuada apresenta a idade','A correção recusa essa designação','A recusa é atribuída à atitude de George','A indicação de pensamento limita a leitura como diálogo'],
  ordem_p='Ordena a relação entre nomeação, correção e acesso à interioridade.'),
 'm9-f14': dict(
  recuperar=('Recupera a abertura do romance: uma personagem histórica representada em ficção equivale a um registo documental dos seus atos?',False,
             'Confundir personagem e documento transforma uma construção literária em prova histórica. Regressa à abertura da F01 e distingue a pessoa histórica da forma como o narrador apresenta o poder.'),
  modelo='A montagem da miniatura associa um gesto material à figura régia. A mudança de escala pode diminuir a grandeza encenada. O objeto isolado não comprova incapacidade de governo.',
  limite='Contraexemplo ao juízo de que montar miniaturas prova incapacidade: a cena criada de estudo de uma estrutura atribui outra função à montagem. Critério: o efeito depende do enquadramento e das relações, não apenas do objeto.',
  pista='Compara quem executa o trabalho e quem recebe os louvores. A crítica nasce da miniatura ou da distribuição do reconhecimento?',
  prova='Que palavra distingue uma hipótese sobre o efeito da cena de uma conclusão automática sobre o rei?',
  ordem=['O gesto de montagem torna o poder observável','A escala reduzida contrasta com a grandeza régia','A comparação abre uma hipótese satírica','As diferenças de risco e de trabalho limitam a analogia'],
  ordem_p='Ordena uma interpretação da miniatura que preserve o limite da comparação.'),
 'm9-f15': dict(
  recuperar=('Recupera a miniatura da lição anterior: observar um gesto basta para provar a intenção de quem o faz?',False,
             'Confundir gesto e intenção transforma um indício numa certeza. Regressa à comparação da miniatura: a interpretação precisa das relações e do enquadramento, não apenas do objeto.'),
  modelo='Uma leitura apresentada como descansada pode ser confrontada com a gravidade das sentenças. A diferença entre as posições produz a tensão. Não é necessário atribuir o mesmo sentimento a cada pessoa do público.',
  limite='Contraexemplo à conclusão de que o público inteiro sente o mesmo: a referência coletiva não individualiza todas as reações. Critério: uma conclusão sobre cada pessoa exige uma marca que a distinga dentro do grupo.',
  pista='Identifica a quem pertence o conforto e sobre quem recai a sentença. A descrição de um gesto permite deduzir a intenção de toda a multidão?',
  prova='Que marca do exemplo criado distingue uma posição observável de uma intenção atribuída?',
  ordem=['A cerimónia reúne posições desiguais','A solenidade enquadra a exposição dos condenados','A leitura descansada contrasta com as sentenças','A referência coletiva não prova cada reação individual'],
  ordem_p='Ordena a construção do contraste e o limite da inferência sobre a multidão.'),
 'm9-f16': dict(
  recuperar=('Recupera a leitura do trabalho na F05: identificar quem executa uma ação permite, por si só, determinar a duração dessa ação?',False,
             'Confundir o agente com o recorte temporal mistura perguntas diferentes. Regressa à F05 para identificar quem trabalha; agora será necessário observar as formas verbais e os marcadores para estudar a duração.'),
  modelo='No exemplo criado, trabalhava apresenta uma situação em curso e cedeu introduz uma ocorrência. A relação produz interrupção. O tempo verbal, sozinho, não determina a responsabilidade pelo acontecimento.',
  limite='Contraexemplo à regra de que uma ação concluída é breve: trabalhou durante três anos apresenta uma longa duração como um todo. Critério: duração e modo de apresentar a ação são dimensões diferentes.',
  pista='Conserva o acontecimento e compara apenas a maneira de o apresentar. Os complementos delimitam a ação ou indicam repetição?',
  prova='Que palavra distingue uma ocorrência situada dentro da ação de duas ações sem relação explicitada?',
  ordem=['O trabalho é apresentado enquanto decorre','Uma ocorrência interrompe a ação individual','A continuidade da obra contrasta com a perda','A relação temporal não demonstra responsabilidade'],
  ordem_p='Ordena a articulação entre tempo narrativo, efeito humano e limite da conclusão.'),
}


# Distratores próximos: cada alternativa conserva o objeto e altera a inferência.
REVISOES['m8-f14']['prova']='Que palavra distingue uma hipótese sobre o futuro de uma descoberta já comprovada?'
REVISOES['m8-f15']['prova']='Que palavra distingue uma orientação possível de uma prova que decidiria a leitura?'
REVISOES['m9-f15']['prova']='Que palavra permite confrontar o modo de ler com a gravidade das sentenças?'
REVISOES['m9-f14']['escolhas']={
 3:['Como liga a escala reduzida à grandeza encenada?', 'Como prova a montagem a eficácia do governo?', 'Como confirma a réplica a devoção da pessoa real?'],
 10:['A escala altera os riscos e as condições de trabalho.', 'A escala conserva os riscos e as condições de trabalho.', 'A escala basta para explicar as condições de trabalho.'],
 14:['Reconhecer o contributo das pessoas que fazem a obra.', 'Aumentar o tamanho da peça que recebe os louvores.', 'Transferir os louvores para quem escolheu a miniatura.'],
 17:['Mostrar a autoridade através do uso de um objeto.', 'Apresentar o objeto como símbolo de sentido fixo.', 'Trocar o objeto por uma descrição direta do poder.']}
REVISOES['m9-f15']['escolhas']={
 3:['Tranquilidade da leitura perante consequências violentas.', 'Tranquilidade dos condenados perante a leitura das penas.', 'Tranquilidade do público como prova de acordo com as penas.'],
 10:['Observar o efeito da cerimónia na vida dos condenados.', 'Deduzir a justiça da cerimónia da sua ordem e solenidade.', 'Deduzir a reação dos condenados do comportamento público.'],
 14:['Que experiência falta na tranquilidade apresentada?', 'Que acordo se comprova na tranquilidade apresentada?', 'Que inocência se prova na tranquilidade apresentada?'],
 17:['Criar duas legendas da praça, de posições distintas.', 'Criar duas legendas da praça, mudando só os adjetivos.', 'Criar duas legendas da praça, mantendo a mesma posição.']}
REVISOES['m8-f16']['escolhas']={
 3:['Da perceção da figura para uma correção interior.', 'Da perceção da figura para uma resposta pronunciada.', 'Da perceção da figura para uma recordação partilhada.'],
 10:['George recusa a expressão atenuada sobre a idade.', 'George recusa a presença da mulher idosa que a observa.', 'George recusa ouvir uma resposta da mulher idosa.'],
 14:['Retirar a informação sobre o pensamento de George.', 'Transformar em fala a informação pensada por George.', 'Atribuir à mulher o pensamento apresentado de George.'],
 17:['Como se relaciona este encontro com o resto do conto?', 'Como confirma este encontro uma rejeição da velhice?', 'Como comprova este encontro uma hostilidade recíproca?']}
REVISOES['m8-f14']['escolhas']={
 3:['O incidente doméstico torna-se matéria de escrita.', 'O incidente doméstico impede a vontade de escrever.', 'O incidente doméstico confirma uma memória pública.'],
 10:['Interrogar o prestígio dado aos vestígios.', 'Transferir para a tigela o prestígio antigo.', 'Confirmar o prestígio pela idade do objeto.'],
 14:['Comparar objetos e explicar o efeito das suas legendas.', 'Comparar objetos e fazer do preço a medida das legendas.', 'Comparar objetos e deduzir da raridade o valor das legendas.'],
 17:['Explicar como cada voz transforma um objeto em pergunta.', 'Explicar como o tema comum torna equivalentes as duas vozes.', 'Explicar como o mesmo objeto recebe um sentido já definido.']}
REVISOES['m8-f15']['escolhas']={
 3:['A reportagem situa a atenção da autora ao mundo.', 'A reportagem identifica a autora com a voz de um poema.', 'A reportagem explica a origem doméstica de cada poema.'],
 10:['Como se constrói a atenção ao quotidiano neste poema?', 'Como confirma este poema o episódio vivido pela autora?', 'Como reproduz a voz do poema a declaração da autora?'],
 14:['Síntese da apresentação publicada pela RTP Ensina.', 'Declaração da autora transcrita na apresentação RTP.', 'Comentário do sujeito poético à apresentação da RTP.'],
 17:['Criar duas vozes distintas para observar o mesmo objeto.', 'Criar duas vozes equivalentes, trocando o nome do objeto.', 'Criar duas vozes biográficas a partir do nome da autora.']}


# 01/11/2026: o retorno acompanha os distratores revistos, sem referências a opções retiradas.
REVISOES['m9-f14']['retornos']={
 3:'Relacionar a escala reduzida com a grandeza encenada permite interpretar a caracterização. Confundir o gesto com prova de eficácia ou devoção atribui-lhe uma conclusão que o objeto não demonstra.',
 14:'Reconhecer quem faz a obra altera a desigualdade do reconhecimento. Confundir dimensão do objeto ou escolha da peça com contributo para a construção deixa essa desigualdade por explicar.'}
REVISOES['m8-f16']['retornos']={10:'George recusa explicitamente uma expressão atenuada. Confundir a rejeição da palavra com rejeição da pessoa acrescenta uma atitude que o recorte não comprova.'}
REVISOES['m9-f15']['retornos']={14:'A pergunta pela experiência excluída confronta o conforto com as consequências. Confundir tranquilidade com acordo ou inocência transforma uma aparência em prova de um juízo.'}

def aplicar(bancos, revisoes=REVISOES):
    for item in bancos:
        if item['id'] not in revisoes:
            continue
        d=revisoes[item['id']];cards=item['cards']
        # Todos os cartões permanecem no núcleo integral, incluindo a recuperação.
        cards[0]['html']='<p class="abre">'+escape(item['question'])+'</p>'+cards[0]['html']
        cards[6]['html'] += '<p><strong>Modelo completo.</strong> '+d['modelo']+'</p>'
        cards[12]['html'] += '<p>'+d['limite']+'</p><details class="apoio"><summary>Uma pista, se precisares</summary><p>'+d['pista']+'</p><p>Consultar esta ajuda não altera o teu progresso.</p></details>'
        cards[9]['p']=d['prova']
        cards[16]['p']=d['ordem_p'];cards[16]['passos']=d['ordem']
        cards[16]['f']='A sequência liga os pormenores à interpretação e conserva o seu limite. Relê o modelo e o contraexemplo: '+d['pista']
        for index,options in d.get('escolhas',{}).items():
            cards[index]['o']=options
        for index,feedback in d.get('retornos',{}).items():
            cards[index]['f']=feedback
        for index,prompt in d.get('perguntas',{}).items():
            cards[index]['p']=prompt
        # O retorno identifica a confusão já descrita no banco e delimita a releitura.
        for i,c in enumerate(cards):
            if c['t']=='ler':continue
            anchor=2 if i<6 else 6 if i<12 else 12
            c['f']+=' Relê o cartão «'+cards[anchor]['titulo']+'» e confronta a pista com a tua resposta.'
        p,value,feedback=d['recuperar']
        recall=cards.pop(18)
        recall.update(p='Antes de reler. '+p,v=value,f=feedback+' Relê essa distinção na lição anterior depois de tentares responder.')
        cards.insert(1,recall)
        cards[-1]['html']='<p class="levar">'+escape(item['question'])+'</p><p>Responde oralmente com uma passagem que sustente a tua leitura e outra que a limite. Explica o critério que te permite distingui-las. Podes manter a leitura inicial, se mostrares por que razão resiste ao confronto.</p>'
        item['tentativa']=dict(automaticas=14,producao_oral=1,escrita_livre=0,selecionadas=0,variantes_p2=0)
        for i,c in enumerate(cards):
            if c['t']!='ler':c['g']=item['id']+'-'+str(i)
