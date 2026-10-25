# M6-F11 — Da biografia à análise do documentário

Base: main a7e16cdb5c0f84dd7a7781cea9a631493870be6b. Alteração localizada, sem sobreposição com o PR #80 (M1/M7). Nenhuma alteração ao LENTE.

## Problema e proposta aplicada

A ficha já separava factos de interpretações. Os cartões 16 e 17 verificavam sobretudo quantidades pedidas e definições de tese/prova. O pedido junto ao vídeo pressupunha que o excerto curto oferecia uma data ou um lugar biográfico para identificar: passa a pedir observação efetivamente possível no excerto.

O cartão 3 conserva os conteúdos e o vídeo, acrescentando uma comparação opcional entre dado biográfico e análise fundamentada. O modelo usa a iluminação da rua por volta de 00:05 no excerto de 54 segundos. A sensação de distância é apresentada como hipótese discutível, e não como intenção provada do realizador ou sentimento do poeta.

O cartão 16 liga iluminação e efeito possível; o 17 distingue indício, interpretação e conclusão não sustentada. O cartão final pede aplicação a outro momento, oralmente ou no caderno, com apoio opcional para revisão. Mantém-se o pedido de comentar duas escolhas, sem novos critérios de classificação. O texto de fecho original foi preservado.

Preservados: 22 definições, tipos e índices dos cartões, navegação, seleção variável, pontuação do motor, IDs e gravação. Só quatro cartões foram editados (índices 3,16,17,21). Painel do docente sincronizado. Os dois exercícios alterados não têm cópias no banco do desafio do módulo; esse ficheiro permanece intacto.

## Fontes e limites da observação

- RTP, excerto «O Livro de Cesário Verde»: https://www.youtube.com/watch?v=a5FVxpP0Pfk . Reprodução iniciada e inspeção visual dos momentos 00:00, 00:05, 00:15, 00:23, 00:35 e 00:45. O modelo analisa apenas elementos visuais observados; não depende de transcrição automática ou de uma fala atribuída.
- RTP Arquivos, ficha do programa (realização João Osório; Companhia de Ideias; emissão de 2010): https://arquivos.rtp.pt/conteudos/o-livro-de-cesario-verde/ . Ligação acrescentada na lição, mantendo o excerto existente.
- RTP Ensina: https://ensina.rtp.pt/artigo/o-livro-de-cesario-verde/ . O programa completo e o excerto curto são recursos diferentes. Não se afirma ter visionado integralmente o programa.

## Verificações executadas

- 165 testes Python aprovados; dois novos verificam estrutura pedagógica/contexto e sincronização dos controlos do docente.
- Comparação com a base: motor, estilos e código fora de CARTOES integralmente iguais; tipos de todos os cartões mantidos. git diff --check aprovado.
- Percurso real completo de uma seleção variável de 15 cartões, a 360×800, incluindo os dois exercícios revistos: emparelhamento, seleção de palavras, escolhas, verdadeiro/falso, lacunas e frase ordenada. Uma inferência errada foi introduzida propositadamente no cartão 16: feedback correto, sem bloquear a progressão. Os restantes nove exercícios foram concluídos corretamente. Após recarregar: «Já feita», melhor resultado 9 de 10 conservado.
- Apoios opcionais abertos por Enter. Leitura comparativa e tarefa final inspecionadas no navegador. Composição em computador e telemóvel; largura DOM móvel 360 sem transbordamento horizontal na leitura de apoio. Rótulos dos dois exercícios confirmados no painel real do docente; não foi aberta uma sala nem testada transmissão entre dispositivos.

## Pendências complementares

Não executados: todas as combinações da seleção variável e de distratores, leitor de ecrã, desempenho medido, transmissão de sala entre dispositivos e avaliação de benefício em turma. As operações cognitivas propostas não constituem evidência de melhoria de aprendizagem já medida. A publicação depende dos testes críticos deste lote, conforme autorização do utilizador; a execução geral de CI deve ficar identificada separadamente se ainda estiver em curso.
