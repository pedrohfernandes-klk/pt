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

## Validação funcional — execução final

**Estrutural:** confronto dos sete bancos CARTOES com a versão de base: **152 cartões e 101 atividades**, sem alterações imprevistas fora dos bancos; IDs, URLs, chaves de progresso e motores preservados. Nove passos do manifesto conformes ao índice.

**GitHub Actions / Chromium:** [run 39356390392](https://github.com/pedrohfernandes-klk/pt/actions/runs/39356390392), **success** em 20-10-2026:

- **6/6 testes Python** aprovados.
- **228 verificações de navegador** nas sete lições F06, F08, F09, F10, F11, F12 e F13, com larguras de 320, 390 e 1440 px. Nos cartões-alvo, verificaram-se opções realmente apresentadas, resposta errada e certa, feedback contextualizado, resultado e progresso isolado.
- **24 verificações complementares** nos dois percursos longos: abertura, avanço inicial, menu, Escape e responsividade.
- **Nove percursos completos** através do motor real, sem saltar cartões: F06 **41** ações, «Inês escolhe duas vezes» **50**, F10 **29**, «A máquina de rir» **46**, F08 **27**, F09 **28**, F11 **28**, F12 **23**, F13 **23**; no total, **295 ações** até ao ecrã final. Os resultados guardados foram recuperados após recarregar.
- Os dois percursos longos incluíram escolhas de posição, abertura de todas as perspetivas, seleção múltipla e associação, além dos formatos normais. Não surgiram erros JavaScript nos percursos exercitados.

**Âmbito e limites:** uma tentativa completa por percurso, com seleção normal dos cartões, e testes adicionais isolados para feedback específico. Não foram exploradas exaustivamente todas as variantes aleatórias ou todas as opções de cada ficha, nem dados reais históricos.

## Verificações adicionais, fora da aprovação Chromium

1. **Acessibilidade e ambiente:** Safari/iOS, leitor de ecrã real, ecrãs/dispositivos físicos, zoom elevado, foco ao longo de todas as combinações e projeção em sala — por realizar.
2. **Regressões com dados anteriores:** confirmar em ambiente controlado a recuperação de estados antigos e os selos/desafios das unidades, além dos progressos locais de QA.
3. **Aprendizagem:** recolher fundamentações autênticas dos alunos, observar se corrigem hipóteses e medir recuperação posterior e transferência para outro texto; não comprovado pelo navegador.

**Estado:** validação funcional automatizada de **uma tentativa integral por cada um dos nove percursos aprovada**. Acessibilidade real, históricos antigos e eficácia pedagógica permanecem por validar. PR #35 continua em rascunho, sem fusão ou publicação.
