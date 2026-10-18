# M3-F18 — verificação deste incremento

Base local do PR: `c607ba2075bdcfb49d8cb6c8109328c95aead94e`. Escopo verificado: página inicial, primeiro ano, mapa M3, índice M3 e bootstrap F18. O design e a imagem em preparação não fazem parte desta prova.

## Executado: verificações estáticas

- 21 scripts nos cinco ficheiros passaram a sintaxe.
- Os 100 arrays de lições anteriores coincidem com a baseline `96cdb520fcf118ef555ef2e325ce93465836c9ea`, obtida diretamente de Git.
- Existem 101 lições; M3 tem 12 entradas coerentes no índice, mapa, página inicial e primeiro ano. F18 aparece uma vez em cada conjunto de dados.
- F18 mantém 17 cartões e dez atividades. Atividades 4 e 10 continuam com resposta correta no índice 1, sem alteração de mecânica.
- A conclusão do motor grava `licao-m3-f18.lida`; o callback grava `licao-m3-f18-a1.lida`. Índice e mapa leem essas mesmas chaves. Verificação do contrato estático, sem simular execução no navegador.
- A atividade 10 usa `_in medias res_`, notação suportada pelo formatador, e já não pressupõe que uma resposta errada demonstra domínio.

Hashes e resultados individuais: `outputs/m3-f18-cycle-static.json` no workspace de trabalho.

## PENDENTE: navegador do candidato exato

**Atividade 4, cartão 7, `epopeia-4`.** Enunciado: «Porque aparece a partida num canto posterior ao começo da navegação?»

- Teste certo: escolher «O relato de Gama recupera acontecimentos anteriores»; esperar acerto e explicação do recuo temporal.
- Teste errado: escolher «O número do canto indica a data de cada acontecimento»; esperar erro e feedback que distingue posição de leitura e data.
- Conferir que a explicação não menciona distratores antigos, como «segunda partida» ou «defeito da edição». Avançar e voltar a rever o feedback, sem alterar a resposta da tentativa.

**Atividade 10, cartão 16, `epopeia-10`.** Enunciado: «Qual síntese usa os três recortes para explicar a organização do poema?»

- Teste certo: escolher «A narração começa durante a viagem e recupera a partida através do relato de Gama»; esperar acerto.
- Teste errado: escolher «O poema segue a cronologia porque os cantos estão numerados»; esperar erro.
- Nos dois percursos, confirmar que o feedback mostra «in medias res» em itálico, sem asteriscos/sublinhados visíveis, e não declara que o aluno já domina a matéria.

Usar duas tentativas distintas para certo/errado: a resposta fica bloqueada após a escolha. Não presumir a posição visual das alternativas, pois o motor pode baralhá-las mesmo com sequência fixa. Usar o texto das opções.

**Integração final:** terminar F18; regressar ao módulo; conferir conclusão e indicador da unidade. Abrir mapa, raiz e primeiro ano; conferir total 12 e entrada F18; recarregar e confirmar persistência. Verificar a navegação do menu, Escape e retorno de foco no layout final. Não confundir ligações absolutas para o site público com o candidato local.

Leitor de ecrã real, dispositivo físico e desempenho permanecem não executados neste registo. Nenhuma chamada remota, merge ou publicação foi realizada nesta revisão.

## Executado no navegador neste ciclo

Na cópia exata da integração, 17 cartões percorridos duas vezes por teclado: dez respostas certas deram 10/10 e 140 pontos; dez respostas erradas deram 0/10 e dez entradas de revisão. O contador animado foi observado depois de estabilizar. Os feedbacks das atividades 4 e 10 foram lidos nos dois estados, sem referências aos distratores antigos nem marcas de formatação expostas; a revisão contém «in medias res» num elemento i.

A conclusão apareceu como 1 de 8 passos na unidade. A entrada mostrou M3 com 1 de 12 lições e propôs continuar em F13, lição 7 de 12. Isto confirma gravação, leitura e articulação do novo identificador. Permanecem complementares: leitor de ecrã real, telemóvel físico, todas as variantes de resposta e condições adversas de rede/armazenamento. Não houve merge ou publicação deste ciclo.


## Limite do envio remoto

O mapa corrigido foi testado na cópia local, mas ainda não foi enviado ao GitHub: a revisão automática não conseguiu analisar o ficheiro grande por limite de entrada. O conector não executou a ação. A autenticação do Git local também falhou. Este PR inclui as restantes correções; o mapa remoto continua pendente e isso bloqueia a integração/publicação da nova lição. Não confundir os testes locais do conjunto completo com o estado remoto parcial.
