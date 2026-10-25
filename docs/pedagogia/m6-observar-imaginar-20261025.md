# M6-F07 — Observar, transformar e justificar

Base: main ed9440f4092e77b0b772b320df47cc7cb65ee341. Lote isolado, sem sobreposição com o PR #80 (M1/M7). Nenhum ficheiro do LENTE alterado.

## Problemas observados e correções

O feedback do cartão 16 opunha o programa realista à imaginação («não da imaginação»), embora os próprios versos transformem montras em «mausoléos». O cartão 32 dizia que a hipálage «está na ordem», confundindo ordenação do verso com transferência de uma qualidade. A distinção reportagem/sonho podia reforçar a ideia de que os elementos observados são linguagem neutra.

O cartão 15 acrescenta um modelo opcional junto dos versos: descrição das luzes que se apagam → transformação das montras → efeito possível de opressão. O cartão 16 passa a pedir uma leitura sustentada nos dois versos, com feedback específico por distrator. Mantém tipo e posição da resposta correta.

O quadro reportagem/sonho e o respetivo feedback passam a explicitar que o ponto de partida observado já pode ser transformado pela linguagem. Um apoio opcional sobre «honesto» compara a transferência moral com uma alteração de ordem e uma descrição sem essa transferência. A explicação depois da ordenação do verso foi corrigida.

A aplicação final retoma os «olhos» do caleche e propõe duas representações da mesma carruagem: descrição neutra e ameaçadora, oralmente, no caderno ou com dois desenhos. Exige manter um pormenor reconhecível e explicar a escolha. O fecho original e os textos poéticos foram preservados.

## Âmbito

Sete cartões editados (índices 15,16,28,29,30,32,33). Mantidas 34 definições, tipos, índices, pontos do motor, navegação, seleção variável e gravação. Uma cópia do exercício no desafio do módulo e os rótulos do painel do docente foram sincronizados. Motor, estilos e código fora dos bancos de dados inalterados.

## Fontes consultadas

- Cesário Verde, O Livro de Cesario Verde, edição de 1887, transcrição do Project Gutenberg n.º 8698: https://www.gutenberg.org/cache/epub/8698/pg8698-images.html . Conferidos os versos da padaria, «o real e a analyse», «mausoléos» e «olhos» do caleche. A leitura sobre a transformação das montras é inferência fundamentada no texto, não uma afirmação biográfica.
- Carla Marques, «Uma hipálage de O sentimento de um ocidental (Cesário Verde)», Ciberdúvidas, 15-10-2024: https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/uma-hipalage-de-o-sentimento-de-um-ocidental-cesario-verde/38225 . Sustenta a transferência da qualidade moral e a valorização do trabalho. Ligação acrescentada no apoio; não se reproduz a resposta integral.

## Testes executados

168 testes Python aprovados. Novos testes verificam a articulação entre observação e imaginação, o efeito da hipálage, o contexto das variantes e a paridade com o desafio e painel. Comparação com a base: só os sete cartões e uma cópia no desafio alterados; tipos de todos os cartões mantidos. git diff --check aprovado.

Percurso real completo no navegador a 360×800: 30 cartões selecionados, incluindo as duas interações revistas. Escolha errada intencional no cartão 16 recebeu feedback específico. Ordenação do verso da padaria mostrou a explicação corrigida. Apoios opcionais abertos por Enter; tarefa final com desenho visível. Conclusão e recarregamento conservaram o melhor resultado 13/14. Largura DOM 360 sem transbordamento horizontal na leitura do modelo.

Pendências complementares: todas as seleções aleatórias e distratores, leitor de ecrã, desempenho medido, transmissão de sala entre dispositivos e avaliação de eficácia em turma. O lote não altera o serviço de sala nem critérios de classificação. Estado de CI e publicação registado na entrega.

Verificação adicional em computador: segunda tentativa percorrida até ao exercício revisto; resposta correta na variante p2 e respetivo feedback confirmados. Capturas móvel e computador do modelo guardadas. Uma repetição da suite falhou por usar a pasta temporária restrita do ambiente (11 erros de permissões); repetida com a pasta temporária do trabalho, voltou a passar os 168 testes. Não foi removido nem dispensado nenhum teste.
