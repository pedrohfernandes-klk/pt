# M3: piloto do polimento (perguntas, feedback, leitura e página do módulo)

Base: `90d2f3b1` (main, PR #65). Âmbito: as 11 lições do M3 com o banco no próprio HTML (F02, F03, F04, F05, F09, F10, F11, F13, F15, F16, F17), a página do módulo `m3/` e uma pergunta do portal de exame que recicla a M3-F13. A M3-F18 (banco externo, já revista em lote próprio) fica de fora. Sem alterações ao motor, ao LENTE nem às chaves de progresso.

Decisões do docente aplicadas (avaliação de 22/10/2026, cinco rondas): explicação por cada opção errada («porque falha e onde ver»); distratores que são erros que um aluno comete, do mesmo campo, do mesmo comprimento e nunca verdadeiros à letra; cartão de leitura até cerca de 80 palavras visíveis; «O essencial» em esquema curto com um exemplo; fora o texto de bastidor; sem travessão, sem «ficha»; palavra do módulo abaixo do título; contagens só em passos.

## O que mudou

| Medida (11 lições) | Antes | Depois |
|---|---|---|
| Escolhas com explicação por opção errada (`fe`) | 0 de 44 | 44 de 44 |
| Verdadeiro/falso com explicação do erro (`fe`) | 0 de 31 | 31 de 31 |
| Escolhas em que a certa é a opção mais longa | 22 (50 %) | 5 (11 %) |
| Cartões de leitura em prosa com mais de 80 palavras visíveis | 15 | 0 |
| Travessões «—» nos cartões | 7 | 0 |
| «ficha» no texto dos cartões | 3 | 0 |

- **Feedback.** O motor partilhado já mostrava `fe` antes da explicação geral (`fb()` em `assets/pt-lessons/jogo.js`). Cada explicação diz o que a opção confunde e aponta o verso, a estância ou a passagem que mostra o certo, sem dar outra resposta. Exemplo (M3-F02, «Cessem do sábio Grego e do Troiano»): quem escolhe «Alexandro e Trajano» lê «Alexandro e Trajano vêm no verso seguinte ("Cale-se de Alexandro e de Trajano"): são conquistadores, não os heróis de Homero e de Virgílio».
- **Opções.** Reescritas em 19 escolhas para igualar comprimentos e tirar distratores fora do campo (por exemplo, M3-F17: «Paradoxo ou antítese» contra «Metonímia», «Anástrofe», «Apóstrofe» passou a pares do mesmo tamanho; M3-F13: «Que o dinheiro leva a crimes desde sempre» contra distratores que agora também são leituras plausíveis). A ordem das opções e o índice da certa mantêm-se; o motor continua a baralhar.
- **Leitura.** «O essencial», «Em paralelo», «Linha de vida» e «Para entender» ficam até cerca de 80 palavras visíveis. O que excedia (os seis objetos do _Kit_ em F02, as outras invocações em F10, o exemplo registado em F11, a anáfora em F15) passou para um «Ler mais» que se abre (`<details>`, com teclado), dentro do mesmo cartão. Não se acrescentaram cartões: o número de cartões por lição, os índices e o progresso guardado ficam iguais. Os cartões com o texto do poema (F02, F03, F10, F13) não se cortaram.
- **Bastidor e regras.** Saem «Não o transcrevemos aqui» (F02) e «Excerto didático inventado, não transcrição de uma conferência» (F11), que passa a «Exemplo escrito para esta lição»; «na ficha» passa a «no exercício» ou «na página»; os títulos «A — …» e «B — …» passam a «A: …»; `_Kit_` sem itálico renderizado passa a `<i>Kit</i>`; retirada de F11 a afirmação, sem fonte, de que o português foi «a primeira língua com um dia oficial da UNESCO».
- **Página do módulo.** A palavra do módulo («fama») passa para uma linha própria abaixo do título, sem o tapar (a 390 e a 1280 px); «5 lições principais» e «7 lições principais» passam a «6 passos» e «8 passos», o mesmo número do contador; o «+» de «Como se cumpre uma unidade» ganha espaço.

## O que o aluno aprende, recupera ou transfere

O conteúdo ensinado é o mesmo. Muda o que acontece no erro: em vez de ver só a resposta certa, o aluno lê porque a sua escolha não serve e onde o texto o mostra, o que o devolve ao verso antes de seguir. Com opções do mesmo comprimento, deixa de ser possível acertar pela forma.

## Verificação executada

- `python -m unittest discover -s tests -p 'test_*.py'`: 149 testes aprovados.
- `scripts/audit_cards.py`, `audit_lessons.py`, `audit_learning_progression.py`, `tests/jogo-rotacao.cjs`, `tests/exame-catalogo.cjs`, `tests/exame-dossie.cjs`: aprovados.
- Duas alterações deliberadas em dados de teste: `assets/exame/sessoes.json` (s05-q3 recicla a pergunta do dinheiro da M3-F13 e acompanha as opções novas) e `tests/test_transversal_clareza.py` (a marca de exemplo não real passa a «Exemplo escrito para esta lição»; a intenção do teste, marcar o exemplo como não autêntico, mantém-se).
- Navegador (Chromium, 390 px): cartões de escolha com erro deliberado mostram a explicação própria antes da explicação geral; «Ler mais» abre e fecha; página do módulo a 390 e 1280 px sem sobreposição. Capturas antes e depois em `docs/qa/capturas/m3-piloto-2026-10-22/`.

## Limites

Não se reescreveram as perguntas de logística (por exemplo, a percentagem do torneio ou a etapa do Projeto do ano), que pedem memória de instruções; ficam assinaladas para decisão. Leitor de ecrã, outros navegadores e observação com alunos não foram feitos nesta ronda. Os testes funcionais não demonstram aprendizagem.
