# Português — primeira auditoria transversal orientada pela aprendizagem

Data: 20-10-2026. Estado: revisão editorial; nenhuma alteração publicada.

## Critério

O objetivo não é aumentar o número de atividades. Para identificar uma lacuna, é necessário localizar um **enunciado, estímulo, resposta ou feedback concreto** que confunda um indício com uma conclusão, transforme uma hipótese interpretativa em regra, ensine uma generalização incorreta ou impeça a transferência. A quantidade de cartões e o facto de uma ficha ter variação desativada são indícios estruturais, nunca prova de deficiência pedagógica.

## Evidência consultada

- `docs/qa/2026-10-19-inventario-fichas.csv`: inventário anterior das 108 fichas, categorias, variação e sinais automáticos; não garante qualidade do raciocínio.
- `docs/pedagogia/referencias-de-atividades.md`: leitura detalhada de seis sequências em M1, M3, M4, M5, M7 e M9. A conclusão aí expressa distingue boas atividades de reconhecimentos e generalizações.
- `docs/qa/auditoria-unidades-m1-m9-2026-10-19.md`: 20 unidades, correspondência curricular e limitações.
- Inspeção direta nesta ronda: F17/M3, F12/M5, F11/M7, F01/M8, F12/M6 e os índices dos percursos do M2. Esta **não é** uma revisão exaustiva de todos os cartões dos nove módulos.

## Decisões por módulo

| Módulo | Evidência relevante | Decisão presente |
| --- | --- | --- |
| **M1**, Literatura Medieval | F19 distingue intenção literal, voz e autor; feedback explica confusões com prova textual | Preservar como referência. Procurar melhoria apenas se uma nova análise revelar falha específica |
| **M3**, Camões | F17, cartão 11, equiparava textos e «quem fica de fora» como associação fechada | **Corrigido.** Perspetivas passam a hipóteses a comprovar com passagem; rótulos dos pares contextualizados |
| **M4**, Barroco/Romantismo | F27 trabalha tese, indício, revisão de afirmações e função de deíticos | Preservar como referência; rever futuramente distratores artificiais amostralmente identificados |
| **M5**, Narrativa do séc. XIX | F12, cartão 20, apresentava 3.ª pessoa e imperfeito como regra necessária do discurso indireto livre | **Corrigido.** Questão limita-se à forma «era» no excerto de Carlos; feedback esclarece a variedade do discurso indireto livre |
| **M6**, Poesia Realista | F12 exige distinguir hipótese imaginativa de ação real em Cesário; banco fixo de oito atividades é intencional | Preservar; a ausência de seleção aleatória não justifica novas perguntas |
| **M7**, Pessoa | F11, cartão 9, sugeria «engenheiro naval, daí máquinas e verso livre»; ligação de oração causal e interpretação de Reis pouco explícita | **Corrigido.** Biografia ficcional não substitui prova poética; explicada a relação entre causal e proposta de serenidade |
| **M8**, Poesia/Conto | F01 apresenta as «lentes» de leitura e afirma que são apenas portas para a análise do poema; não se encontrou, nesta amostra, erro bastante para alterar | Sem intervenção. Priorizar futuramente observação da revisão de hipóteses nos contos |
| **M9**, Saramago | Revisão anterior M9-F01 distinguiu tempo histórico, ordem do relato e momento de narração; M9-F13 articula investigação e interpretação | Preservar correção recente. Exigir verificação de transferência antes de multiplicar lições |

O M2 é tratado separadamente nas PR #34 (U1) e #35 (U2), ambas com execução automatizada de testes de navegador. Esta PR não modifica o M2.

## Preservação e testes

Alterações apenas nos arrays `CARTOES` de três ficheiros HTML: M3-F17 (cartão 11), M5-F12 (cartão 20), M7-F11 (cartões 5, 9, 20, 21). Conservados número e ordem dos cartões, operações, IDs, URLs, motores, chaves de armazenamento e propriedades não intervencionadas. M5 conserva as mesmas alternativas e índices corretos; M3 altera texto de pares mas não a quantidade nem o sistema de associação.

A verificação estática inicial dos ficheiros foi aprovada no momento da edição. A execução dos cinco testes de regressão e dos cenários Chromium depende do workflow incluído nesta PR; o seu resultado deve ser consultado antes de aprovar. Não foram efetuados testes em Safari/iOS, leitor de ecrã real ou aula com alunos. A retenção e a transferência real exigem observação posterior.

## Próxima ronda após testes

1. **M8:** tomar uma sequência de conto com inferências sucessivas, testar distinção entre hipótese, evidência e revisão; só adicionar atividade se faltar operação essencial.
2. **M4:** rever as alternativas manifestamente fáceis em atividades de argumentação, sem uniformizar a diversidade dos exercícios.
3. **M3/M5/M7:** fazer aplicação curta com alunos dos casos aqui corrigidos, procurando explicações autónomas em vez de acertos de reconhecimento.
4. **M1/M6/M9:** conservar os pontos fortes, auditando transferências apenas quando a observação ou dados de exercícios apontarem para confusões concretas.

**Esta é uma primeira revisão transversal com intervenções comprovadas, não uma certificação pedagógica integral das 108 fichas.**
