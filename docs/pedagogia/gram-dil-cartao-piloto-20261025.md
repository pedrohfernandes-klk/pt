# Discurso indireto livre — piloto de composição

Base: af75f7441bb4f28060d5672bb2c199be4ff74654. Apenas `m5/gram-dil/index.html`, fora dos ficheiros dos PRs #80 e #92 e das alterações locais observadas nos outros checkouts. O utilizador apreciou o piloto e autorizou aplicação/publicação em 25/10. Replicação transversal continua sujeita a pequenos lotes e verificação de conflitos.

## Composição

- Proximidade: excerto e explicação pertencem à mesma região. Em computador ficam lado a lado; em telemóvel, a explicação segue imediatamente o excerto.
- Hierarquia: o excerto tem serifa e maior dimensão; os rótulos e as explicações usam a tipografia corrente. As letras A/B/C e a margem da tarefa recebem um apontamento de terracota discreto.
- Região comum: o relato de João e a produção no caderno ficam num grupo próprio. O conteúdo anteriormente dentro de um detalhe passa a estar visível; isto aumenta a extensão vertical do cartão.
- Fonte: mantém destino, texto, indicação de abertura externa e área de interação de pelo menos 44 px, com aspeto de ligação bibliográfica em vez de grande botão preto.

Os três excertos, a definição de indireto, a contextualização do relato e a encomenda no caderno foram preservados. A explicação de indireto livre foi distribuída junto de B e C. Os nove passos mantêm ordem estrutural e dados; questões, alternativas, gabaritos, feedback, fontes, identificadores e progresso não mudaram. Além da composição, o controlo local de navegação recebeu a correção descrita abaixo; o motor partilhado não foi alterado. A variação já existente entre tentativas permanece.

## Verificações executadas

- 174 testes Python aprovados, correspondentes à base deste piloto. Os quatro testes do auditor M4 pertencem ao PR #92 e não foram misturados nesta branch.
- Comparação programática antes/depois: todos os campos de dados fora do HTML da primeira leitura iguais; código de execução e estrutura da página iguais fora do novo estilo; excertos e tarefa conservados.
- Navegador, 1280 × 720 e 390 × 844: capturas antes/depois; sem transbordo horizontal na página normal; explicações empilhadas no telemóvel. A tarefa e a fonte foram inspecionadas após deslocação vertical.
- Fonte alcançável por teclado; Tab passa para o controlo seguinte. Área da fonte: 44 px na verificação de computador.
- Passagem da leitura ao exercício, resposta correta numa tentativa nova, feedback e retoma após recarregar: observados. A ordem pode variar numa nova tentativa, conforme o comportamento existente.
- Projeção local com QR visível e ligação pública correta; controlos pequeno/médio/grande e ocultação do QR responderam. Capturas da projeção anterior e do piloto. Não houve leitura física do QR.
- `git diff --check` sem problemas.

## Falha funcional reproduzida e corrigida

Depois de uma resposta corrigida, a faixa de feedback sobrepunha-se ao rodapé e tapava «Voltar ao passo anterior». O teste de posição confirmou que o centro do botão atingia a faixa, nas duas versões. A correção local move os dois controlos para um grupo dentro do feedback. O centro passa a atingir o próprio botão. Regresso confirmado por clique em computador e por Enter no telemóvel, sem transbordo horizontal. Reentrada no exercício mantém a resposta guardada. Não foi necessário alterar recursos partilhados ou ficheiros de outros PRs.

Depois da correção, foi percorrido o conjunto dos nove passos no navegador até ao cartão final (90/90): leitura, duas escolhas, classificação dos quatro excertos, seleção de pistas, transformação contextualizada, verbo declarativo, mudança de referências e síntese. Feedback e avanço observados. Não foram executados todas as alternativas erradas, leitor de ecrã, aparelho físico, impressão, verificação visual do modo escuro ou medição de desempenho. O novo CSS contém adaptações para modo escuro e impressão, mas isso não equivale a teste real. Capturas são evidência de composição, não de benefício comprovado em turma.

## Próximo passo

Publicar o piloto aprovado depois dos testes e verificar o site público. O crescimento vertical foi apresentado na comparação: o cartão exige mais deslocação, mas não esconde a tarefa. Preparar o modo noturno PT+LENTE em incrementos separados e voltar a cruzar ficheiros com trabalhos ativos antes de editar; não misturar alterações globais neste PR.
