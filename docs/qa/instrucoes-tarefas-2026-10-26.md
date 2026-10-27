# Instruções de preparação e fecho — 26/10/2026

Base exata: `65f786c3bfeaaec6ddb754acd81d3bcf44c726af`. Lote local, sem publicação.

As aulas preparatórias de M1/M4 deixam de anunciar desafios digitais finais, sínteses autónomas ou a obrigação de repetir uma produção. As três aberturas são curtas e remetem para a Tarefa da Unidade correspondente. Cinco guiões recuperam provas e respostas existentes no tempo antes ocupado pelos fechos antigos. A síntese simples e a entrega pertencem à aula de tarefa.

Mapas e portefólios de M1/M4/M7 passam a orientar para esse fecho. Os portefólios recuperam trabalhos e reflexões já entregues: não exigem gerar um cartão do percurso, escrever outra síntese ou repetir uma reflexão. As linhas de ficheiros anteriores permanecem identificadas como registos facultativos. Parâmetros, ponderações e critérios não foram alterados.

## Preservação verificável

- `tests/fixtures/task-instruction-edits-20261026.json` regista nove pares exatos de texto antigo/novo em três lições, com contagem e localização. São strings UX, substituídas literalmente no HTML; não se reserializaram motores.
- `original_lesson_text`, no teste de percurso, reverte apenas esses pares, pela ordem inversa. O hash do ficheiro inteiro normalizado para LF tem de coincidir com a fixture original de conteúdo, baseada em `7163b603`. A fixture antiga e os seus hashes não foram atualizados.
- As perguntas literárias e as listas de critérios dos cinco guiões têm contratos separados, capturados da base exata deste lote. Permanecem iguais.
- O teste do apoio de comparação M4 continua a verificar o enunciado e a rubrica originais, recuperados pelo restauro explícito. O cartão de F11 conserva a pergunta de 100–140 palavras, o exemplo e os quatro critérios; só a orientação de entrega passa a treino com consulta, sem nova entrega.
- Os desafios que são atividades de leitura permanecem. «Desafio» no comentário à ironia de Manuel é conteúdo literário e não foi substituído. Os arquivos de bancos/registos dos índices, as propostas anteriores dos guias e os relatórios históricos não foram alterados.

## Limites e remissões

Dois resumos de `m1/index.html` ainda anunciam o fecho antigo: «Cinco atos, o desafio e a síntese da unidade 1» e «uma multidão sem nome; desafio e síntese». Ficaram fora deste lote por instrução expressa de não editar os índices frontais; as duas substituições constam da auditoria entregue ao integrador. Devem ser aplicadas pelo lote responsável pelos índices.

Não foram alterados CSS/JS partilhados, exame, páginas das tarefas ou o índice frontal de qualquer módulo. Sem browser partilhado ou inspeção visual: a alteração é textual e conserva a estrutura das páginas, salvo os blocos locais de orientação dos guiões. As caixas com os exercícios e critérios anteriores mantêm-se, agora rotuladas como consulta opcional.

## Validação

O teste próprio orquestra o restauro das nove strings, a brevidade das três aberturas, a ausência de fechos autónomos nos mapas/portefólios/guiões, a recuperação de produções e a igualdade das perguntas/rubricas dos guiões. A suíte Python completa corre com `TEMP` e `TMP` dentro desta worktree. Resultado: 218 testes passaram, incluindo os cinco testes próprios e os contratos de preservação.
