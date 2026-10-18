# M3-F18 — composição editorial e imagem

Proposta limitada à abertura de M3-F18. Não modifica o motor, a folha de estilos partilhada, a navegação ou as outras lições. Depende da integração de M3-F18, ainda em revisão no PR #10. Sem autorização de merge ou publicação deste ciclo.

## Alteração

Título com maior peso e hierarquia; imagem documental com legenda; composição em duas colunas no computador e uma faixa compacta em ecrã estreito. A linha terracota é um apontamento de cor. O CSS é exclusivo desta lição, num ficheiro de cerca de 2 KB, limitado pela classe do body. Os textos originais da abertura são mantidos.

Imagem: folha de rosto de Os Lusíadas, edição de 1572, reprodução com origem atribuída à Academia Brasileira de Letras no registo Wikimedia Commons. Autor da gravura não identificado. A página do ficheiro identifica a reprodução e o original como domínio público (PD-scan/PD-old; estatuto revisto em 2015). Não se apresenta a imagem como mapa, representação de Melinde ou documento da viagem de 1497–1499.

Fonte e licença: https://commons.wikimedia.org/wiki/File:BookFrontOsLusiadas1572.jpg

O JPEG original, sem recorte ou transformação, tem 389 × 565 px e 97 451 bytes. É servido pelo próprio repositório, com dimensões explícitas, texto alternativo, ligação à imagem integral e crédito. Não há pedido a terceiros para carregar a imagem. A leitura proposta distingue começo material do livro e começo da narração em I, 19; nenhuma resposta exige conseguir ler a gravura.

## Testes executados

- Abertura em 320×568, 390×844, 768×1024 e 1440×900: sem transbordo horizontal no documento ou no main; imagem carregada, dimensões naturais corretas.
- Botão Seguinte com 48 px de altura e inteiramente dentro da janela nas quatro dimensões.
- Percurso real de 17 cartões por teclado: 10/10, 140 pontos e sequência de dez acertos, observados após estabilizar o contador animado.
- Nova tentativa; menu por Enter, fecho por Escape e retorno do foco ao botão Menu.
- Imagem integral acessível no URL local e apresentada como imagem de 389×565. A ligação tem nome acessível e identifica a abertura numa nova aba.
- Sem avisos ou erros de consola capturados nesse percurso.
- A comparação estática preserva as dez atividades e os 16 cartões posteriores à abertura; o HTML original da abertura mantém-se dentro da nova composição.

Capturas de comparação no workspace de revisão: m3-f18-antes-computador.png, m3-f18-depois-computador.png, m3-f18-antes-telemovel.png e m3-f18-depois-telemovel.png. Não estão alojadas por este PR.

## Pendências

Leitor de ecrã real, telemóvel físico, outras fontes de sistema, impressão, ampliação de texto e condições adversas de rede não certificados. As medidas registadas cobrem a abertura, não todos os estados em cada dimensão. A integração remota do mapa continua pendente no PR #10 devido ao limite da revisão automática do ficheiro grande. Não publicar a nova lição enquanto essa integração estiver incompleta.
