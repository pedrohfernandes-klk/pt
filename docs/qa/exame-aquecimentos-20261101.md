# Aquecimentos do exame: 27 percursos em cartões

Decisão 106, 01/11/2026. Base: `main`, commit `5bf8b757bb80f4b8b0ce72aba2c48dca813b9c61`.
Ramo: `codex/exame-aquecimentos-20261101`. Integração apenas por revisão da equipa.

## O que muda

Cada sessão passa a ter 12 cartões de fazer, num total de 324. Conservam-se as 81 perguntas anteriores, com as opções reequilibradas e os títulos em itálico. Os dados antigos de `sessoes.json` mantêm-se para rastreabilidade; nesse ficheiro só muda a duração das sessões.

Os bancos ficam em `docs/pedagogia/exame-aquecimentos/s01.json` a `s27.json`. Cada cartão indica `recycledFrom` e, nos acrescentos, `sourceCard`; `adaptacao` identifica transferências para exemplos de treino. Os textos primários são consultáveis, sem glossários nem modelos de resposta. Os exemplos inventados identificam-se como treino ou caso imaginário.

As páginas próprias em `exame/aquecimentos/sNN/` usam a casca e o motor das lições, sem os alterar. A página inteira evita dois níveis de deslocamento e barras concorrentes no telemóvel e na projeção. Há regresso ao aquecimento no topo e no menu e, no fim, continuação para a leitura. O relógio, acessível no menu dos cartões, partilha o estado com a fase Aquecer.

O aquecimento passa a 10 minutos e a sessão a 50. Leitura, escrita, correção e fecho conservam os seus tempos. O catálogo, os enunciados para imprimir e a explicação dos tempos foram atualizados.

## Cartões por sessão

| Sessão | Foco | Fazer | Tipos |
|---|---|---:|---|
| s01 | Cantigas: comparar sem confundir | 12 | 2 escolha, 4 vf, 2 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s02 | Fernão Lopes: uma multidão em ação | 12 | 3 vf, 2 escolha, 3 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s03 | Gil Vicente: desejo, escolha e sátira | 12 | 3 escolha, 2 emparelhar, 1 ordenar, 3 sublinhar, 3 completar |
| s04 | Camões lírico: o que a forma faz sentir | 12 | 3 escolha, 2 sublinhar, 1 completar, 1 versos, 3 vf, 2 emparelhar |
| s05 | Os Lusíadas: celebrar e interrogar | 12 | 3 escolha, 2 versos, 2 sublinhar, 2 completar, 2 vf, 1 emparelhar |
| s06 | Vieira: os peixes são o argumento | 12 | 2 escolha, 3 vf, 3 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s07 | Frei Luís de Sousa: o que a cena revela | 12 | 2 escolha, 3 vf, 3 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s08 | Prosa romântica: paixão e condicionamento | 12 | 2 escolha, 3 vf, 2 sublinhar, 1 completar, 1 versos, 2 emparelhar, 1 ordenar |
| s09 | Eça: ver a crítica nos pormenores | 12 | 1 escolha, 3 vf, 2 completar, 4 sublinhar, 1 emparelhar, 1 ordenar |
| s10 | Antero: procurar, negar, descansar | 12 | 2 escolha, 3 vf, 2 sublinhar, 2 completar, 1 versos, 1 emparelhar, 1 ordenar |
| s11 | Cesário: uma cidade em transformação | 12 | 3 escolha, 2 versos, 1 completar, 2 sublinhar, 2 vf, 2 emparelhar |
| s12 | Pessoa: sentir e construir o poema | 12 | 3 escolha, 1 versos, 2 completar, 2 sublinhar, 2 emparelhar, 1 vf, 1 ordenar |
| s13 | Caeiro: o rio e a medida do olhar | 12 | 3 escolha, 2 sublinhar, 1 emparelhar, 3 vf, 1 completar, 1 versos, 1 ordenar |
| s14 | Reis: a disciplina do instante | 12 | 2 escolha, 3 vf, 2 emparelhar, 2 versos, 2 completar, 1 sublinhar |
| s15 | Campos: desejo e desencontro | 12 | 3 escolha, 1 versos, 1 sublinhar, 1 completar, 3 vf, 2 emparelhar, 1 ordenar |
| s16 | Mensagem: mito, história e apelo | 12 | 2 escolha, 3 vf, 2 sublinhar, 2 versos, 2 completar, 1 emparelhar |
| s17 | Poesia contemporânea: três modos de dizer | 12 | 3 escolha, 2 emparelhar, 2 completar, 2 sublinhar, 2 vf, 1 ordenar |
| s18 | Conto: o que o texto deixa por dizer | 12 | 3 escolha, 1 emparelhar, 2 sublinhar, 3 completar, 3 vf |
| s19 | Saramago: quem conta e quem faz | 12 | 3 escolha, 2 emparelhar, 1 sublinhar, 2 completar, 1 versos, 1 ordenar, 2 vf |
| s20 | Ler informação e escrever uma síntese | 12 | 3 escolha, 2 emparelhar, 2 sublinhar, 1 completar, 2 ordenar, 2 vf |
| s21 | Gramática: funções e relações entre orações | 12 | 3 escolha, 2 completar, 2 sublinhar, 1 ordenar, 2 vf, 2 emparelhar |
| s22 | Gramática: ligar, retomar e situar | 12 | 3 escolha, 2 emparelhar, 2 sublinhar, 3 completar, 1 vf, 1 ordenar |
| s23 | Exposição: explicar com uma linha clara | 12 | 3 escolha, 2 emparelhar, 2 vf, 1 completar, 2 ordenar, 2 sublinhar |
| s24 | Opinião: uma posição que resiste à revisão | 12 | 3 escolha, 2 emparelhar, 3 completar, 1 sublinhar, 2 vf, 1 ordenar |
| s25 | Apreciação crítica: julgar mostrando | 12 | 3 escolha, 2 emparelhar, 1 completar, 1 ordenar, 3 vf, 2 sublinhar |
| s26 | Oficina final: transformar uma resposta | 12 | 3 escolha, 2 vf, 2 emparelhar, 3 sublinhar, 1 completar, 1 ordenar |
| s27 | Ver, compreender, estudar melhor | 12 | 3 escolha, 2 emparelhar, 2 vf, 2 sublinhar, 1 completar, 2 ordenar |

Todos os bancos têm pelo menos cinco tipos e pelo menos um cartão de completar com várias lacunas. Os cartões de leitura não entram na contagem dos 12.

## Retorno e opções

As escolhas têm retorno alinhado com cada alternativa. Nas lacunas, o controlador fornece ao motor apenas o retorno das alternativas erradas selecionadas, conservando a explicação geral. Não foi alterado o motor partilhado.

O gerador exige diferença máxima de 20 % em caracteres visíveis, sem margem mínima de caracteres, tanto nas escolhas como nas lacunas. Exige também que a resposta certa nunca seja a única mais longa. A medição final e o resultado do teste geral serão registados após a última execução.

## Progresso e projeção

Chaves novas: `aquecimento-exame-sNN`; relógio: `pt-exame-relogio-v2-sNN-aquecer`. O motor guarda a conclusão, as tentativas e o melhor resultado como nos outros aquecimentos. Recomeçar inicia os cartões sem apagar o melhor resultado. Não migra nem apaga chaves das lições ou dos antigos aquecimentos do exame.

Com `?projetar=1`, os cartões começam do princípio, não mostram resultados privados e não gravam progresso. O relógio projetado também não lê nem grava estado. As ligações de retorno e continuação mantêm a projeção.

## Vídeos de ajuda

Escolha: `escolher`; verdadeiro ou falso: `verdadeiro-falso`; emparelhamento: `ligar-pares` ou `ligar-lados`, conforme a operação; ordenação: `ordenar`; sublinhar: `tocar-palavras`; completar: `completar`. Os ficheiros de vídeo existem e o botão de ajuda aponta para o recurso correspondente.

Versos não tem vídeo dedicado: o motor usa o vídeo de ordenar, que demonstra a mesma operação. Não foi usado mapa, que não tem ajuda associada no motor e não era necessário nestas sessões. Não se gravaram vídeos nem se alterou `/como/`.

## Verificações

A primeira passagem de navegador percorreu todos os cartões a 320, 390 e 1366 px, com respostas, ajuda, conclusão, regresso, reinício e projeção. Está em curso a passagem final após a revisão dos retornos e da tipografia.

A suite completa revelou falhas antigas em `test_sala_desligada.py`: 461 falhas de subtestes e dois erros, reproduzidos numa extração limpa do mesmo commit de base, sem as alterações deste pedido. Os testes da Sala não foram modificados. Os resultados finais dos outros testes serão acrescentados neste relatório.

No Windows, dois testes de navegador exigem uma ligação simbólica para servir `/pt/`. A execução direta dá `WinError 1314`; executam-se os mesmos testes com uma junção de diretório, sem mudar as suas asserções. O CI em Linux usa os comandos originais.

## Limites e revisão do docente

Não se alteraram as lições de origem, os exercícios das outras fases, o dossiê, os motores partilhados ou os pedidos #143 a #154. As opções foram adaptadas apenas nos bancos novos. As perguntas anteriores podem preparar aspetos da tarefa escrita, como já faziam, mas não se acrescentou qualquer resposta escrita completa.

A adequação dos 12 cartões a dez minutos deve ser confirmada em aula. O tempo não bloqueia o aluno nem avança por ele. Este pedido não publica nem funde alterações.
