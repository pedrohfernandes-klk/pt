# Revisão transversal curta — clareza, ensino e desenho

21 de outubro de 2026. Base local 40b2250a, sobre main remota 2290c8e1. Ramo work/pt-transversal-clareza-20261021. Sem publicação. O ramo conserva a revisão local anterior de M5-F14 e os critérios de ensino, consolidação, jogo, design e vídeo.

## Cobertura efetiva

Triagem das instruções e respostas assinaladas nos exercícios de seleção de palavras dos bancos inline dos nove módulos; procura de comparações cujo número de blocos não corresponde à grelha. Confronto de 188 cópias de escolhas nos desafios com as respetivas fichas, quando coincidem a pergunta e o texto da resposta correta. Auditorias automáticas dos 108 bancos, incluindo os externos, e da sintaxe.

Leitura editorial aprofundada de M3-F11 e amostras de M6-F04 e M8-F06. Esta ronda não é uma nova revisão semântica integral de todos os exercícios, nem garante a coerência das variantes que não puderam ser emparelhadas automaticamente. Os casos abaixo justificaram intervenção concreta; os restantes módulos não receberam alterações por analogia.

## 1. M7 — três comparações ilegíveis

M7-F02/15, M7-F13/18 e M7-F14/16 tinham dois blocos numa grelha de três colunas, sendo a central reservada a um separador já ausente. O navegador mediu 14 píxeis na segunda coluna, tanto em 320 como em 1440 píxeis de janela. O conteúdo estava presente, mas a apresentação prejudicava a leitura.

Correção: classe explícita para duas colunas e uma pequena folha de estilos partilhada apenas entre estas três páginas. Duas colunas no ecrã largo, blocos empilhados com separação no móvel. Depois: 272/272 píxeis no móvel e 310/310 no ecrã largo. Os textos das comparações mantêm-se integralmente iguais; mudaram apenas a classe e a ligação ao CSS. Poemas, imagens e motores preservados.

## 2. M3-F11 — ensinar antes de perguntar

A tarefa de escuta pedia tese, argumentos, notas seletivas e perguntas sem mostrar suficientemente essas operações. Um excerto didático explicitamente inventado permite agora distinguir assunto, posição defendida, razão e exemplos; mostra uma nota fiel e seletiva e formas de pedir esclarecimento, justificação ou exemplo. A síntese pede recuperar tema/tese sem voltar ao modelo, conferir e transferir para uma intervenção real.

O exercício de associação misturava três exemplos lexicais do português com o tétum, fechando com «a mesma língua, palavras diferentes». Corrigido: o tétum é apresentado como língua distinta, cooficial com o português em Timor-Leste. A Constituição, artigo 13.º, foi consultada na página oficial do Parlamento: https://www.parlamento.tl/legislasaun . O exemplo de cooficialidade é distinguido da variação lexical, sem sugerir uma variedade única por país ou exclusividade geográfica de cada palavra.

A pergunta sobre os adjetivos passa a identificar «registo», com que «fiel» e «seletivo» concordam, e liga a seleção ao exemplo explicado. O modelo de pergunta deixa de ser validado apenas pelo tamanho e pelo registo: o exercício analisa a posição pressuposta por «deve mandar». Removidas variantes antigas do desafio que declaravam a norma de Portugal dominante, confundiam línguas e variedades ou afirmavam que o modelo tinha vinte palavras. Mantidos os limites desta tarefa, sem os transformar em regras universais.

## 3. Três índices de respostas errados em desafios

As próprias fichas e os feedbacks permitem demonstrar os erros, sem nova interpretação literária:

- M3-F05: «Descalça vai para a fonte» tinha no desafio a resposta marcada «Cinco, redondilha menor», em vez de «Sete, redondilha maior».
- M3-F11: a pergunta sobre os registos adicionais do guião marcava idade/profissão, em vez de palavra de outra variedade e surpresa.
- M6-F02: «Ideal» marcava a força da Amazona, em vez da série de negações que define a figura.

Corrigidos apenas esses índices; opções, perguntas e feedbacks dessas três cópias mantidos. O novo teste compara textos de respostas, respeitando a possibilidade de ordens diferentes entre ficha e desafio. Não presume que as posições numéricas tenham de coincidir.

## Preservação

Sem novas fichas ou aumento do número de cartões. Quantidades, tipos e ordem preservados nas quatro lições editadas; cartões de abertura e imagens integralmente iguais à base local. M3-F11 conserva vinte cartões e os seus tipos; os índices mantêm-se. Desafios conservam o número de itens e o painel de M3 foi sincronizado. Nenhuma alteração ao motor, pontuação, URLs ou chaves de progresso; não foi necessária migração.

## Testes e evidências

104 testes Python aprovados, incluindo cinco regressões novas. Auditorias das 108 lições sem erros: 2509 cartões, 710 de leitura e 1799 interativos. As correções dos índices não alteram estas contagens.

Chromium: seis comparações (três páginas × 320/1440) medidas antes e depois, sem erros JavaScript ou transbordo horizontal. M3-F11: tentativa normal, conclusão após recarregar e passagem por todos os vinte cartões a 320/1440. As três respostas corrigidas foram confirmadas no contexto real das páginas de módulo, com cartões efetivos do desafio; não se afirma conclusão de todos os desafios. Feedback da pergunta sobre pressupostos exercitado com uma resposta errada. Comparação corrigida de M7-F13 verificada em projeção com texto grande. Captura móvel de M7-F13 inspecionada.

Evidências: baseline.json, qa.json, indices-desafios.json, preservacao.json, bancos.json, sintaxe.json e capturas. Rotina reproduzível tests/browser_transversal_clareza.py, incluída no fluxo de regressão. O modo --baseline destina-se a registar medidas; as capturas anteriores preservadas nesta pasta mostram a versão antes da correção.

## Limites e plano mantido

Não houve sessão com alunos, Safari/iOS, leitor de ecrã real, ensaio físico de projeção, medição de retenção ou exploração de todas as rotações. As apresentações PDF/PPTX arquivadas não foram revistas. Os testes funcionais não demonstram aprendizagem.

Não se integrou vídeo sem um excerto efetivamente verificado e uma tarefa definida. A seleção e integração pedagógica de vídeos mantém-se no plano. Também permanece a revisão contextual de M6-F09 e a observação de transferências nos restantes módulos. M6-F04 contém classificações cuja fundamentação depende do contexto completo dos versos; esta ronda não as reescreveu por suspeita nem certifica a suficiência de todos os testes simplificados da ficha.
