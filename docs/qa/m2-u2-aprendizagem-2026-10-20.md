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

## Validação efetivamente realizada

**Aprovada a inspeção programática de dados em GitHub**, confrontando os arrays CARTOES da `main` e deste ramo:

- Sete bancos lidos e comparados, sem alterações fora dos arrays.
- Contagem anterior e atual idêntica: **152 cartões / 101 atividades**; nenhum cartão adicionado, eliminado ou reordenado.
- Todos os campos alterados coincidem com a lista de intervenções prevista; campos não visados preservados.
- Feedback específico confrontado com a posição da opção correta: arrays completos nas intervenções; objetos indexados esparsos de F12/F13 preservados.
- Questões de verdadeiro/falso e escolhas existentes mantêm os índices/valores corretos.
- Correspondência integral entre os nove passos do índice do módulo e o manifesto editorial.
- F09, F12 e F13 idênticas à base quanto a conteúdo.

Os seis testes de regressão para futura execução no checkout estão em `tests/test_m2_u2_learning.py`. A inspeção de dados acima não equivale a executar Python ou o navegador; não declarar esses testes como concluídos.

## Bloqueios à publicação

1. Executar `python -m unittest discover -s tests -p test_m2_u2_learning.py` no checkout, juntamente com os auditores globais e validação de sintaxe.
2. No navegador, completar as quatro fichas e verificar novos feedbacks com escolhas corretas/incorretas, incluindo mistura de opções e tentativas sucessivas.
3. Confirmar que a seleção variável mantém disponíveis os exercícios relevantes, que o progresso persistente e os desafios da unidade não sofreram regressões.
4. Testar F06/F08/F10/F11 em 320–390 px, ecrã largo, projeção e teclado, incluindo foco e explicações longas. Leitor de ecrã real e Safari/iOS **não testados**.
5. Verificar com alunos, por observação ou respostas no papel, se o confronto de provas e a explicação de escolhas cénicas melhoram de facto. A análise automática não permite concluir aprendizagem, transferência duradoura ou retenção.

**Sem fusão ou publicação** até concluir os testes funcionais críticos. A implementação da Unidade 1 permanece separada na PR #34 para evitar dependências desnecessárias.
