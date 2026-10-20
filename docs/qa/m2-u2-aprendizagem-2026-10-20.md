# M2 · Unidade 2 — revisão pedagógica e QA (20-10-2026)

**Estado:** primeiro lote editorial pronto para revisão; não publicado. **Base:** `main`. **Âmbito:** Unidade 2 de Teatro Vicentino. Sem alterar motores, folhas de estilo, catálogos, índices, URLs, IDs ou chaves de progresso. O trabalho da Unidade 1 permanece na PR #34, independente deste ramo.

## Percurso preservado

F06 → percurso longo «Inês escolhe duas vezes» → F10 → percurso longo «A máquina de rir» → F08 → F09 → F11 → F12 → F13. São **sete lições normais e dois percursos longos**. As sete fichas têm **152 cartões** (101 exercícios e 51 leituras). O mapa pedagógico em `docs/pedagogia/m2-u2-progressao.json` reproduz exatamente a ordem e os IDs do índice do módulo; não é carregado pelo navegador.

## Intervenções cirúrgicas

| Ficha | Campos modificados | Razão |
| --- | --- | --- |
| F06 | feedback específico em 25; nota de conclusão em 33 | Evitar literalizar a cantiga e preparar uma tese sustentada por cenas diferentes |
| F10 | nota explicativa em 4; reformulação de 9, 12, 14 e 18 | Corrigir generalizações: uma reportagem pode recorrer a fontes indiretas e à primeira pessoa; a terceira pessoa e a observação direta são opções **desta encomenda**, não leis do género; exigir um juízo sobre escolhas cénicas ligado a efeitos verificáveis |
| F08 | explicação inicial em 1; exercício 16; conclusão 21 | Apresentar o plano de escrita como apoio e substituir a identificação fácil de uma «tese dupla» por confronto de dois versos e revisão de conclusão |
| F11 | abertura 0; resumo 1; exercício 15; feedback 19 | Tratar «ninguém é poupado» como hipótese a discutir e separar crítica à ambição de Inês de justificação do controlo exercido pelo Escudeiro |
| F09, F12, F13 | **nenhum** | Recontagem e exercícios complementares já oferecem operações de transferência e análise contextual que interessa conservar |

Não se criaram cartões, pontos, mecanismos ou novos ecrãs. As quatro fichas revistas mantêm as opções corretas do respetivo motor; onde se alteraram distratores, as respostas certas continuam no mesmo índice. Os feedbacks específicos usam o formato compatível com o motor existente. Foram preservados os textos de todas as outras atividades.

## Validação efetivamente realizada — estado atualizado

**Inspeção estática:** confronto dos sete bancos CARTOES de M2-U2 com `main`: **152 cartões e 101 atividades**, sem remoções ou reordenações; alterações limitadas a campos editoriais identificados; HTML/JavaScript exterior aos bancos, chaves de progresso, URLs e motores preservados. Controlo de índices de feedback, respostas e correspondência dos nove passos com o manifesto aprovado.

**GitHub Actions / Chromium:** [run 39354626094](https://github.com/pedrohfernandes-klk/pt/actions/runs/39354626094), de 20-10-2026, conclusão **success**:

- **6/6 testes Python** no checkout.
- **224 verificações de navegador** nas sete lições F06, F08, F09, F10, F11, F12 e F13; larguras de 320, 390 e 1440 px, abertura, navegação inicial e ausência de erros JavaScript nos percursos exercitados. Nos cartões-alvo, respostas incorretas e certas, feedback em opções realmente apresentadas, resultados e progresso local isolado. As escolhas com feedback por objeto indexado de F12/F13 foram exercitadas no motor real.
- **24 verificações adicionais** nos dois percursos longos «Inês escolhe duas vezes» e «A máquina de rir»: abertura, responsividade, avanço inicial e menu com fecho por Escape.

Os cartões-alvo foram testados em sobreposições isoladas com o mesmo motor das lições. Não se realizaram percursos completos nem se cobriram todas as combinações da seleção variável. A persistência observada pertence a dados de QA, não a históricos reais preexistentes.

## Pendências obrigatórias antes da publicação

1. Percursos integrais das nove páginas, desafios de etapa e continuidade entre fichas, incluindo verificação do histórico de progressos anterior às mudanças.
2. Projeção em aula, teclado/foco nos percursos completos, leitor de ecrã real e Safari/iOS; testes físicos e medição formal de desempenho **ainda não efetuados**.
3. Observação pedagógica: discutir e justificar interpretações com textos, voz ou caderno, rever uma conclusão e aplicar o procedimento semanas depois. A eficácia e a retenção não se inferem dos acertos automáticos.

**Estado: intervenção funcionalmente aprovada nos casos automatizados; certificação integral, acessibilidade e eficácia pedagógica pendentes.** PR #35 continua em rascunho, sem fusão ou publicação.
