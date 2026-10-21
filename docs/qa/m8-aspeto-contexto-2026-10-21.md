# M8-F06 — Aspeto com contexto

## Estado
Incremento local, sem publicação. Main confirmada em d83920a6. O ramo conserva também a melhoria local anterior de M8-F05; esta etapa altera apenas M8-F06 e as entradas correspondentes no painel e no desafio.

## Problemas demonstrados
- A explicação de iterativo exigia um número exato de ocorrências. A repetição pode ser indicada sem contagem exata. A nova tarefa pede identificar a expressão que marca repetição, evitando opor automaticamente iterativo e perfetivo como classificações incompatíveis.
- «Pintava quando a campainha tocou» era apresentado como prova de uma interrupção. O toque localiza a pintura em curso, mas não prova que a pintora tenha parado. Corrigidos feedback e formulação alternativa.
- «Lia» aparecia isolado; a relação entre tempo passado e conclusão podia ficar reduzida a uma etiqueta morfológica. O ensino e a pergunta usam agora uma frase completa e contrastam leitura em curso com leitura explicitamente concluída.
- O fecho pedia imitar um modelo sem apresentar o parágrafo completo. Passa a incluir o modelo didático, as retomas explicadas e uma tarefa oral ou no caderno. O desafio deixa de depender de uma referência ausente a «Sena escreveu-o longe».

## Intervenção
Mantidos os 24 cartões, ordem, tipos de exercício, imagem de abertura, URLs e motores. Alterados os cartões 1, 4, 6, 7, 10, 11 e 23. Painel sincronizado; seis entradas do desafio corrigidas. Sem novas fichas, campos obrigatórios ou vídeos sem função demonstrada.

O esquema inicial organiza os cinco valores com exemplos completos. A escolha sobre repetição conserva o motor existente e oferece feedback sobre os indícios e os limites da conclusão. O modelo final articula gramática e escrita sem classificar uma interpretação pessoal como certa ou errada.

## Fundamentação
[Ângela Costa, Ciberdúvidas — habitual e iterativo](https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/aspeto-habitual-e-aspeto-iterativo/32201): repetição num intervalo e comportamento habitual. Foram usados apenas os esclarecimentos pertinentes à repetição; não se transpõem todas as análises do artigo.

[Dicionário Terminológico da DGE — valor aspetual](https://dt.dge.mec.pt/index.php?id=n398): enquadramento lexical e gramatical e distinção entre conclusão e ausência de informação sobre a culminação. A página depende de JavaScript; o extrato indexado foi consultado, não uma leitura integral da interface.

## Validação
128 testes Python passaram, incluindo quatro regressões novas. Chromium a 320 e 1440 px: tentativa normal, banco completo de 24 cartões, conclusão e progresso após recarregar; três distratores da escolha nova testados por teclado em pares controlados e feedback visível. Sem erros JavaScript nem transbordo horizontal. Captura móvel inspecionada: esquema legível, com deslocação vertical. Teste incluído na CI para futura integração.

Inventário: 108 lições e 2509 cartões, sem aumento. O relatório de sintaxe acompanha esta entrega. Diferenças desta etapa em diff.patch.

## Limites e próximo foco
Não houve publicação, ensaio com alunos ou teste com leitores de ecrã. Não se esgotam as análises possíveis de todas as frases nem se certificam todas as tarefas de anáfora e catáfora. A distinção entre repetição e hábito exige contexto; não é substituída por uma nova regra mecânica. Os testes de distratores usam pares controlados porque o motor sorteia apenas parte das opções.
