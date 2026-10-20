# M2 — Unidade 1: aprendizagem com evidência, retoma e transferência

**Data:** 20-10-2026. **Âmbito:** M2-F01, F02 e F07. **Estado:** ramo de revisão, sem integração nem publicação.
Referência estrutural: docs/pedagogia/arquitetura-aprendizagem.md e m2-u1-progressao.json.

## Hipótese pedagógica

A unidade parte da rubrica inicial (quem fala e em que situação), atravessa a fala de Inês e o juízo da Mãe (o que o texto confirma, o que é interpretação de uma personagem) e chega à relação entre orações (o que os conectores fazem num contexto). O aluno deve apontar uma prova, rever uma inferência e transportar o procedimento para frases que não pertençam à farsa.

Não se criou outra unidade nem se substituíram as lições por «fichas de ligação». Os conteúdos e o design existentes continuam a ser a estrutura principal. Retomas e projeções para a ficha seguinte são breves e integradas no texto dos cartões.

## Alterações editoriais

| Ficha | Alteração | Operação visada |
| --- | --- | --- |
| F01 | Feedback específico para as três alternativas erradas em «este motivo» (cartão 10) | separar ocasião, acusação e motivo textual |
| F01 | Feedback para confusões entre aparte, monólogo, rubrica e fala coletiva (cartão 20) | distinguir função pelo destinatário |
| F01 | Nota curta no fecho a anunciar a passagem do provérbio à experiência de Inês | conservar a pergunta para F02 |
| F02 | Feedback de verdadeiro/falso sobre «Inês é preguiçosa» (cartão 17) | separar facto observável de juízo de uma personagem |
| F02 | Feedback por opção sobre «aviamento» (cartão 25) | inferir sentido lexical a partir das falas |
| F02 | Retoma final sobre «Todas vêm e todas vão» e «Praza a Deos...» | preparar a passagem da leitura para a sintaxe |
| F07 | Retoma sucinta da fala «Praza a Deos que...» antes da análise (cartão 1) | passar do que Inês pede à função da oração |
| F07 | Feedback específico para «quem se tenha por ditoso» e para os diferentes «que» (cartões 8, 9 e 15) | evitar regras baseadas apenas no conector |
| F07 | Exercício com frase explicitamente inventada, «A jovem quer sair, mas a família pede que fique» (novo cartão 23) | distinguir coordenação adversativa e subordinada completiva em caso novo |
| F07 | Comparação de causa e finalidade em duas frases igualmente identificadas como inventadas, com resposta revelada voluntariamente (cartão final) | justificar e rever a resposta antes de a consultar |

As notas de continuidade não têm temporizador ou pontuação extra. A transferência escrita/oral não é corrigida artificialmente por uma máquina. A explicação é revelável para permitir autorrevisão e mediação docente.

**Contagens:** F01 24 cartões; F02 28; F07 25 (anteriormente 24). F07 passou de 18 para 19 atividades; todas as leituras anteriores permanecem. A questão nova não substitui perguntas da obra, nem passa a integrar o banco dos desafios do módulo sem uma decisão específica.

## Preservação

- Conteúdo exterior ao array CARTOES sem alterações; títulos, URLs, módulos, IDs, progresso, motores e estilos preservados.
- Não se eliminaram nem reordenaram cartões preexistentes. Inseriu-se um único cartão de escolha antes da leitura final de F07; não há alteração nas chaves de armazenamento.
- Mantidas as opções, respostas corretas, feedback geral e restantes operações dos exercícios existentes. Melhorias limitadas ao feedback específico e à continuidade das leituras.
- Frases criadas para aplicação claramente marcadas como tal: não se atribuem a Gil Vicente.
- Não foi alterado o LENTE.

## Validação efetivamente executada — estado atualizado

**Estrutural:** 9/9 verificações programáticas da revisão original, incluindo contagens, compatibilidade do banco, seleção simulada do grupo de transferência e comparação com a versão de base. Os dados das fichas e os motores de exercícios anteriores foram preservados, exceto os acréscimos identificados.

**GitHub Actions / Chromium:** execução de 20-10-2026, [run 39354266402](https://github.com/pedrohfernandes-klk/pt/actions/runs/39354266402), conclusão **success**. No checkout do ramo:

- **10/10** testes Python concluídos, incluindo contratos de continuidade e formato dos cartões.
- **138 verificações de navegador** sobre M2-F01, F02 e F07, executadas em Chromium, com larguras de 320, 390 e 1440 px; abertura das páginas, ausência de erros JavaScript nos casos testados, navegação inicial, apresentação de erros específicos em opções efetivamente escolhidas, acertos, resultados e persistência de conclusão num identificador de QA isolado.
- Os testes usaram o motor real das páginas; os cartões editoriais alterados foram exercitados também em sobreposições isoladas com o mesmo motor. Não constituem uma passagem integral por todas as combinações possíveis das fichas.

## Pendências e critérios para publicação

1. Percorrer integralmente cada ficha na sequência e confirmar que a nova atividade F07 não compromete a contagem do melhor resultado anterior nem os desafios do módulo. Os testes confirmam persistência em chave de QA, **não migração de dados reais preexistentes**.
2. Verificar a projeção, foco/teclado e navegação integral de cada ficha, incluindo situações de erro repetido. A navegação inicial foi exercitada; não se certificou a totalidade do percurso no navegador.
3. Inspecionar Safari/iOS e pelo menos um leitor de ecrã real; comparar telemóvel físico e zoom sem transbordo. Estes testes **não foram realizados**.
4. Observar com alunos se justificam interpretações autonomamente, revêm erros e transferem procedimentos para excertos novos. Não há ainda evidência de retenção posterior.

**Estado: validação automatizada dos percursos-alvo aprovada; validação integral, acessibilidade real e eficácia pedagógica pendentes.** PR #34 permanece em rascunho, sem fusão/publicação.
