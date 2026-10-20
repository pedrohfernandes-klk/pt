# M2, Unidade 1 — aprendizagem e continuidade (20-10-2026)

## Âmbito

Piloto sobre M2-F01, F02 e F07, partindo da versão de `main` anterior ao lote. Sem alteração dos motores partilhados, estilos, identificadores, chaves de armazenamento ou URLs. Não há publicação nem fusão com `main`. O manifesto editorial e o contrato geral estão em `docs/pedagogia/`.

## Alterações pedagógicas

- **F01:** feedback por opção incorreta em «este motivo» (rubrica, provérbio e encomenda) e na distinção entre aparte, monólogo e rubrica; preparação da cena de Inês.
- **F02:** uma retoma breve do provérbio, feedback específico da distinção entre juízo da Mãe e facto narrado e da interpretação de «aviamento», com fecho que prepara a análise de orações. Uma segunda retoma concorrente, redundante, foi retirada.
- **F07:** retoma de uma fala de Inês e da função de «que», feedback específico em dois casos de interpretação sintática, uma nova questão de aplicação com frases expressamente inventadas («mas» e «que»), e tarefa complementar oral ou escrita que distingue causa de finalidade. Foi eliminada uma segunda retoma redundante.
- Na transferência nova, o grupo `transfer` é distinto; confirmar no navegador que aparece corretamente em tentativas normais e na revisão de erros. `p2` constitui formulação alternativa, não prova de variação cognitiva.

## Inventário e invariantes

| Ficha | Cartões antes | Cartões no ramo | Atividades antes | Atividades no ramo |
| --- | ---: | ---: | ---: | ---: |
| F01 | 24 | 24 | 17 | 17 |
| F02 | 28 | 28 | 17 | 17 |
| F07 | 24 | 25 | 18 | 19 |
| **Total** | **76** | **77** | **52** | **53** |

Verificação estrutural de leitura das três fontes no ramo e em `main`: **aprovada**. Todos os cartões anteriores mantêm os seus campos e conteúdos, com exceção dos acréscimos identificados de `fe` e `html`; a nova atividade insere-se antes do cartão final da F07. Os valores de resposta correta, perguntas anteriores e tipos dos cartões já existentes permanecem iguais. Índices de `fe` das escolhas confrontados com as respetivas opções; feedback específico para respostas incorretas não está associado à opção correta. A correspondência com a ordem do manifesto M2-U1 foi confirmada.

A verificação acima foi executada sobre os conteúdos obtidos do GitHub; não equivale a executar o código JavaScript numa interface real.

## Verificações obrigatórias antes de publicar

- Executar no checkout completo o auditor `python scripts/audit_learning_progression.py` e os testes de regressão.
- Abrir as três páginas no navegador e percorrê-las, incluindo todas as novas retomas, cada alternativa errada com `fe`, a atividade de transferência e o cartão final da F07.
- Testar acerto e erro, sequência de cartões, seleção com `g: "transfer"`, repetição de tentativa, variação `p2`, recuperação de progresso e de melhor resultado anteriores (incluindo o aumento de um cartão na F07).
- Verificar apresentação em ecrãs estreitos, projeção, teclado, `details/summary` e contraste. Leitor de ecrã real e Safari/iOS ficam assinalados como **não realizados**.
- Observar numa aula se o aluno justifica com indícios, revê uma interpretação e aplica a distinção a um caso diferente. O acerto em escolhas automáticas não constitui por si só evidência de retenção.

**Estado:** revisão estrutural aprovada; validação funcional e pedagógica real **pendente**. Ramo/PR em rascunho; não publicar até concluir os testes críticos.
