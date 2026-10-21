# M6-F04 — analisar relações, não decorar senhas

Revisão local de 21 de outubro de 2026, base f9076936. Main remota confirmada em 2290c8e1. Ramo work/m6-oracoes-contexto-20261021. Não publicado; conserva os blocos locais anteriores de M5, critérios, revisão transversal e M6-F09.

## Falhas verificadas

A ficha propunha substituir mecanicamente «que» por «o qual» para reconhecer relativas, inclusive restritivas em que o pronome é sujeito ou complemento direto. Os próprios exemplos produzidos eram inadequados: «os filhos os quais…» e «o qual dê…». O contexto anterior de «Pois sobem…» estava ausente na classificação. O feedback da causal «bate à porta porque está exausto» indicava-a como modelo para ligar «entra no palácio» a «não encontra nada», sem justificar causalidade. Havia ainda uma definição de assíndeto excessivamente geral e uma explicação de ordem direta que esquecia o sujeito subentendido no imperativo.

## Ensino e exercícios

A leitura explica primeiro o complemento e o antecedente. O modelo inventado «Penso que escolheste o poema» / «Leio o poema que escolheste» mantém a palavra «que» e muda a sua relação: complemento do verbo ou relativo que retoma «poema». «Isso» fica limitado às completivas trabalhadas; não é uma senha para todas as substantivas. A análise identifica também a função do relativo.

Retomou-se o contexto de «Pois sobem…» da estrofe já presente em M6-F07. O apoio permite relacionar música e comparação com uma pauta. A classificação explicativa fica associada à leitura contextual trabalhada, sem se afirmar que a palavra, isolada, basta. O exercício de seleção e a sua formulação alternativa fornecem esse contexto.

As associações passam a destacar as partes classificadas, mantendo as frases que as enquadram. As lacunas aplicam duas operações diferentes: reconhecer o complemento e localizar o antecedente. A retoma oral/no caderno pede recuperar a distinção sem o modelo e experimentar «mas» e «porque» nas duas frases didáticas, explicando a relação introduzida e a prova de que necessita. A experiência de mudar um conector dá uma consequência de sentido à ação; não se acrescentaram pontos ou novos mecanismos.

Corrigiram-se também variantes antigas do desafio, incluindo uma escolha cuja resposta certa era a troca inadequada por «o qual». Em M6-F09, a revisão complementar deixa de repetir esse atalho; a associação destaca as subordinadas e identifica um exemplo didático que antes podia parecer citação literal de um poeta. Painéis sincronizados.

## Preservação

M6-F04 mantém 24 cartões e M6-F09 mantém 21. Tipos, ordem, cartões de abertura, imagens, URLs, motores, CSS e chaves de progresso preservados. Sem novas fichas ou aumento de exercícios. F04: cartões 1,2,3,4,8,10,12,13,15,18,19,21,22,23; F09: cartões 1 e 13 (índices a partir de zero). Sem deslocação de índices, não foi criada migração.

A estrofe de Cesário foi retomada da grafia já apresentada em M6-F07, sem nova colação editorial. Não se alterou o texto dessa ficha. As frases didáticas e a citação de Antero são distinguidas no material.

## Fontes consultadas

Ciberdúvidas, «A diferença entre que e o qual», página aberta e consultada: https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/a-diferenca-entre-que-e-o-qual/28632 . Sustenta a limitação da substituição nas restritivas com as funções referidas.

Ciberdúvidas, «Oração subordinada causal / oração coordenada explicativa», página aberta e consultada: https://ciberduvidas-ql.iscte-iul.pt/consultorio/perguntas/oracao-subordinada-causal--oracao-coordenada-explicativa/6148 . Usada para o contraste entre dependência causal e justificação. A interpretação específica da pauta/flauta é a leitura didática do contexto do poema, não uma conclusão atribuída a essa página.

## Verificação realizada

112 testes Python aprovados, incluindo quatro regressões novas. Auditorias dos 108 bancos e da sintaxe sem erros: 2509 cartões, 710 de leitura e 1799 interativos.

Chromium a 320/1440: tentativa normal de cada ficha, conclusão recuperada após recarregar e passagem pelos bancos completos de 24 e 21 cartões. Sem erros JavaScript ou transbordo horizontal nos estados percorridos. Abertura e fecho do contexto de «pois» por teclado; feedback de erros na causal e na identificação do antecedente conferido. Captura móvel do modelo inspecionada. Teste reproduzível tests/browser_m6_oracoes.py integrado no fluxo de regressão.

Um primeiro ensaio dos cartões isolados reabria os resultados porque reutilizava uma chave de QA concluída. O teste passou a pedir explicitamente uma montagem nova para esses cenários; o percurso normal continua a testar o comportamento real de conclusão e persistência. Nenhuma alteração ao motor foi necessária.

## Limites e continuidade

Não é uma revisão integral da gramática dos nove módulos. Não se certificam todas as análises possíveis dos versos nem se afirma que todos os conectores têm uma única leitura em qualquer contexto. Não houve revisão audiovisual, Safari/iOS, leitor de ecrã real, teste de todas as rotações ou observação da aprendizagem com alunos. PDF/PPTX arquivados não foram revistos. Mantêm-se os critérios e o plano de integração de vídeo com função pedagógica comprovada.
