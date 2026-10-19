# Unidades com pelo menos três fichas — Português

Baseline: `b280e1975a4f9027eb6e214f8b7b85f19b85b7bc`.

Regra do utilizador: cada unidade deve conter pelo menos três fichas. Os percursos longos são preservados, mas não entram nesta contagem.

| Módulo | Fichas por unidade após reorganização |
|---|---|
| M1 | 5, 7 |
| M2 | 3, 7 |
| M3 | 5, 7 |
| M4 | 7, 5, 3 |
| M5 | 5, 6 |
| M6 | 6, 5 |
| M7 | 6, 7, 4 |
| M8 | 6, 4 |
| M9 | 5, 5 |

As 108 fichas mantêm-se. A reorganização corrige sete unidades abaixo do mínimo em M1, M2, M3 e M7. Os restantes módulos não necessitam de alterações para cumprir esta regra.

## Arquitetura pedagógica

M1: vozes da lírica medieval; cidade na crónica de Fernão Lopes. M2: entrada na Farsa; escolhas, representação e sátira. M3: contexto e lírica; interpretação da epopeia. M7: Pessoa; confronto entre heterónimos; Mensagem e síntese.

Cada nova unidade tem uma pergunta orientadora, uma composição com hierarquia própria e uma lista explícita de fichas no mapa. As antigas sequências passam a etapas internas: conservam desafios, respostas escritas, selos, parâmetros de avaliação e identificadores. Isto permite integrar aprendizagens sem invalidar trabalhos e progresso guardados. Os guias e portefólios apresentam a correspondência; os códigos dos nomes de ficheiro das entregas mantêm-se.

Os índices e mapas distinguem unidades de etapas. A contagem de fichas exclui percursos longos e exercícios soltos. A definição das novas unidades acompanha as páginas dos módulos em dados JSON identificados por `epi-unidades-pedagogicas`; os registos antigos continuam a suportar os pontos de controlo para compatibilidade.

## Verificações executadas

- Todos os grupos propostos cumprem o mínimo de três fichas e preservam exatamente as fichas do módulo.
- Preservação dos IDs e ligações anteriores nas páginas alteradas; ausência de novos IDs duplicados.
- 60 scripts passaram na verificação de sintaxe.
- Navegador real: quatro índices e quatro mapas; contagens e etapas correspondentes visíveis.
- Navegador real: oito guias/portefólios, com acesso à organização das unidades.
- Quatro desafios completos, um por módulo alterado: 32 respostas confirmadas corretas, 8/8 por desafio. A seleção apresentada cobriu escolha, verdadeiro/falso, completar, ordenar, sublinhar e ordenar versos. Não incluiu emparelhar nesta execução.
- Progresso, selo e síntese anteriormente guardados na etapa 4 de M2 continuam visíveis.
- Índices testados em 1058, 320 e 390 px CSS, sem transbordo horizontal.

## Limites e publicação

Não foram repetidas todas as atividades de todas as fichas: estas não foram alteradas neste lote. Não executados leitor de ecrã real, dispositivos físicos ou desempenho formal. A preservação de avaliação incide nos parâmetros e conteúdos existentes; a eficácia pedagógica da nova organização requer acompanhamento em aula.

O PR #24 é independente e altera apenas a integração de M6 e a documentação de auditoria. A publicação anterior do PR #23 continuava em fila na última consulta. Este lote fica verificável em PR próprio; não declarar publicação concluída enquanto o workflow do SHA correspondente e o site público não forem confirmados.

