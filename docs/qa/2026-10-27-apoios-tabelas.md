# Apoios de leitura — auditoria M1–M9 e primeiro lote

Referência: main `9b1b9e05740b730ec4484de6e91c460779c6a2cd`, 27 de outubro de 2026. Primeiro lote: M7-F15, cartão 12 do banco completo (a posição apresentada pode variar).

## Cobertura confirmada

Leitura e validação estrutural dos bancos de 109 lições, 2411 cartões: M1 12/244; M2 10/232; M3 12/286; M4 16/282; M5 11/259; M6 11/248; M7 17/409; M8 10/228; M9 10/223. Nenhum erro estrutural encontrado. Também foram examinados 29 painéis de M1–M3 e seis bancos suplementares (191 cartões); estes não estão somados aos 2411 cartões das lições.

Procuraram-se referências a tabelas, esquemas, imagens, passagens e exemplos, confrontando-as com cartões vizinhos, campos auxiliares e os grupos sujeitos a baralhamento. Não se confundiu um texto repartido, uma glosa ou uma leitura explicitamente pedida no livro com um apoio prometido e inexistente.

Esta é uma auditoria de código e contexto, não uma certificação visual de todos os cartões ou da disponibilidade de vídeos e livros externos.

## Correção deste lote

M7-F15 apresentava sete processos num único parágrafo. O cartão passa a conter uma tabela com conceito, definição e exemplo, cabeçalhos semânticos e os sete processos originais. No telemóvel, as linhas ficam empilhadas com rótulos de definição/exemplo. A primeira linha de dados não fica escondida por uma regra destinada ao cabeçalho.

O estilo é opt-in, carregado só nesta lição. Não se alteram motor, ordem/tipos de cartões, perguntas, opções, feedback, chaves ou progresso. O manifesto literal permite reverter só esta alteração e verificar o hash congelado anterior; os novos testes verificam a tabela atual e os 20 outros cartões intactos.

## Fila de correções comprovadas, fora deste lote

| Prioridade | Local | Problema | Próximo incremento mínimo |
|---|---|---|---|
| P1 | M8-F09, cartão 7 | Pede um resumo-modelo chave/cão/escada que não aparece na lição; o guia ligado tem outro modelo. | Dar o modelo didático no próprio apoio, identificado como inventado; preservar os pares e as respostas. |
| P1 | M8-F08, cartão 14 | Depende do exemplo de Rita de outra pergunta; ambas podem ser baralhadas. | Repetir a cena-base junto da pergunta e retirar a dependência de «anterior». |
| P2 | M2-F02/F07 e M3-F10, painéis | Índices antigos enviam leituras ou perguntas diferentes para o relâmpago. | Reconciliar índice, tipo, enunciado e seletor com cada pergunta atual; testar envio real. |
| P2 | M8-F09, cartão 18 | Remete para uma «lista final» ausente, embora as palavras necessárias estejam no exercício. | Tornar o enunciado autossuficiente, sem criar nova lista obrigatória. |
| P3 | M3-F17 e M2-F10, painéis | Rótulos e quantidades antigos não correspondem à pergunta. | Corrigir após confronto com o banco atual. |

## Verificações visuais ainda necessárias fora deste lote

Tabelas existentes: M2-F09, M6-F08, M8-F10 e M9-F05; paralelos de M6-F07/F09 e dois SVG de M1. O código prevê adaptações, mas a auditoria não confirmou a legibilidade real a 390 px nos dois temas. Não estão classificados como tabelas ausentes ou comprovadamente ilegíveis. Disponibilidade dos vídeos externos e do manual continua uma verificação separada.

## Testes do lote

Executados localmente: três testes de estrutura, conteúdo e preservação do cartão; quatro testes de continuidade das tarefas/arquivo. Verificação visual local do cartão isolado em computador e num iframe real de 390 px: tabela com sete linhas, rótulos e primeira linha visíveis; legenda móvel ajustada; tipografia dos conceitos recuperada da formatação minúscula do estilo antigo. Estas capturas são pré-visualizações isoladas, não um percurso completo publicado.

Obrigatório antes de publicar: suite completa, CI de revisão/telemóvel/projeção nos três tamanhos e regressão no head final. O percurso completo do banco M7-F15 continua no CI geral existente. Não se declara publicação ou QA transversal completa enquanto estas verificações não terminarem.
