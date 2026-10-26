# Boia docente e tarefas finais — primeiro incremento, 26/10/2026

Decisões do docente: guiões de aula pela boia; enunciados e critérios continuam visíveis para os alunos. Todas as unidades devem terminar com Tarefa. Manter as fichas e acrescentar acesso separado à tarefa no fim da unidade. Aula de 90 minutos: 10 apresentação +10 preparação HTML +60 produção em papel +10 revisão/entrega de fotografias no Teams. O docente cria a tarefa no início da aula. Não mudar critérios ou pesos.

## O que este lote implementa

- Boia no início PT e nos nove índices, para a área conjunta LENTE/docente/#portugues. Retira só os dois atalhos de guiões docentes em M1/M4. Guias de tarefa do aluno, fontes, exercícios, URLs e progresso conservados.
- Primeira tarefa final, M4-U3: acesso depois do fecho da unidade; página própria tarefas/m4-u3/. Enunciado100–140palavras e quatro critérios copiados literalmente do cartão16 de M4-F11. A ficha original permanece. Não cria outro registo de classificação nem altera os passos digitais.
- Preparação breve: duas falas e contexto, modelo ideia/citação/explicação, quatro escolhas com feedback e possibilidade de rever. Passagens junto das duas primeiras perguntas. Produção60min e lista de verificação/fotografias. Sem armazenamento de respostas ou integração automática com Teams.
- Estilos próprios da tarefa, boia partilhada e modo noturno/projeção pelos recursos existentes. Nenhum CSS da maquete visual é integrado.

## Inventário para os próximos lotes

São 20 unidades. A tabela identifica o fecho e candidatos de reaproveitamento já observados. Não declara ausência de tarefa nas outras: falta a revisão editorial das respetivas produções/guia. Uma resposta de poucas linhas, uma ocorrência de «entregar» num texto ou um exercício longo de leitura não equivalem automaticamente a uma tarefa de 90 min.

| Unidade | Nome | Último passo atual | Próximo tratamento |
|---|---|---|---|
| M1 · U1 | Vozes da lírica medieval | m1-voz-emprestada | Rever fecho e guia do módulo |
| M1 · U2 | A cidade na crónica de Fernão Lopes | m1-f11 | Rever fecho e guia do módulo |
| M2 · U1 | Ler a Farsa: desejos, escolhas e consequências | m2-f06 | Rever fecho e guia do módulo |
| M2 · U2 | Interpretar e representar: crítica, cena e atualidade | m2-f09 | Rever m2-f08, m2-f09 |
| M3 · U1 | Camões: o mundo e a voz | m3-soneto-raciocinio | Rever fecho e guia do módulo |
| M3 · U2 | Dentro da epopeia: celebrar e questionar | m3-f17 | Rever fecho e guia do módulo |
| M4 · U1 | Pregar aos peixes | m4-f10 | Rever m4-f10 |
| M4 · U2 | O Romeiro diz «Ninguém» | m4-frei-luis-quem-sabia | Rever m4-f20 |
| M4 · U3 | Trinta dias no abrigo | m4-f11 | Piloto M4-U3 |
| M5 · U1 | Um amor contra duas famílias | m5-quem-podia-ter-feito-diferente | Rever m5-f08 |
| M5 · U2 | A casa dos Maias | m5-f15 | Rever fecho e guia do módulo |
| M6 · U1 | O ideal e a rua | m6-f04 | Rever fecho e guia do módulo |
| M6 · U2 | A cidade inteira | m6-f09 | Rever m6-f08 |
| M7 · U1 | Pessoa: fingimento, memória e identidade | m7-f15 | Rever fecho e guia do módulo |
| M7 · U2 | Heterónimos: modos de ver e de viver | m7-quatro-vozes-um-problema | Rever fecho e guia do módulo |
| M7 · U3 | Mensagem: imaginar o país e confrontar as vozes | m7-f11 | Rever m7-f10 |
| M8 · U1 | Três vozes, um século | m8-f10 | Rever m8-f10 |
| M8 · U2 | O que cabe num conto | m8-f12 | Rever fecho e guia do módulo |
| M9 · U1 | A pedra e o sonho | m9-ver-e-nao-ver | Rever fecho e guia do módulo |
| M9 · U2 | Quem fala e quem faz a obra | m9-f07 | Rever fecho e guia do módulo |

O inventário operacional está em tarefas-unidades-20261026.json. Só M4-U3 está implementada como piloto neste lote. Próximos casos económicos: M5-F08 (carta) e M6-F08 (projeto visual) já têm produções, mas não fecham as unidades. Antes de os mover, rever preparação e dependências; conservar o núcleo e os critérios. Não transformar tarefas de vídeo/defesa em escrita por simples substituição de palavras: organizar a fase de trabalho em papel preservando o que é avaliado.

## Verificação e limites

190 testes Python aprovados; cobertura de aparência em 745 páginas sem pendências. Testes novos verificam o enunciado/critérios originais, posição final em U3, contrato digital inalterado, tempos 10/10/60/10, quatro questões e guiões preservados na boia. Navegador: erro e revisão nas quatro perguntas, uma resposta ativa por grupo, contador sem duplicação; teclado; índice→tarefa; ausência do atalho docente no cabeçalho; oito observações 320/390/768/1440 claro/noite sem transbordo. Projeção conferida nos três tamanhos e QR com destino canónico; boia oculta no material projetado para não cobrir o texto. Conferir o resultado público antes de fechar. Turma, leitor de ecrã externo e projetor físico não executados. Fontes privadas indisponíveis: conservar o novo acesso e a página antes de regenerar.
