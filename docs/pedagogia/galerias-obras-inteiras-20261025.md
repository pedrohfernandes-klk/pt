# Galerias: preservar a obra na miniatura

Base 90895d610dd77335f2231ca57a0e94e279e53f95, já com #92, #93 e #95 integrados. Lote limitado aos mapas M3/M5/M8/M9, sem PR PT concorrente observado antes de editar e no fecho dos ensaios.

## Alteração

Cinco figuras recebem `obra-completa`: Rimas (1595), página de rosto de Os Maias (1888), Os fuzilamentos de 3 de maio, D. João V e Passarola. Só estas miniaturas usam `object-fit:contain;object-position:center` e fundo de papel. A galeria conserva grelha, altura, navegação e ampliação. As restantes fotografias e recortes mantêm-se.

Conserva ficheiros e bytes das imagens, texto alternativo, legendas, fontes, licenças, URLs, âncoras, conteúdos, progresso e código funcional. Remover as cinco classes e quatro regras locais restitui exatamente os quatro HTML anteriores; comparação executada. Não modifica fontes/geradores do Claude; a regra deve ser preservada ao regenerar estes quatro mapas.

## Verificação própria

- 178 testes Python aprovados após a alteração; `git diff --check` aprovado.
- Comparações antes/depois das cinco imagens em navegador real, 1280×720 e 390×844; imagens carregadas, quadro 168×170/167,5×170, fonte/licença/ligação conservadas. Capturas externas em outputs/enquadramentos-20261025 e medições em qa-galerias-pt.json. As primeiras capturas tinham nomes móveis mas dimensões efetivas de computador; foram renomeadas e o ensaio móvel foi repetido após confirmar o viewport real.
- A 320×740: cinco ampliações por Enter, Escape e retorno do foco à imagem; imagens carregadas, contain e sem transbordamento horizontal. qa-galerias-320-teclado.json.
- Projeção real dos quatro mapas: abrir a galeria dentro da moldura, ampliar as cinco obras e fechar; alternar 18/22/28 px, com estado selecionado, galeria e QR presentes. Doze estados guardados em qa-galerias-projecao.json. Inspeção visual da galeria M9 projetada em tamanho grande confirma a obra inteira. A grelha existente mantém legendas estreitas neste tamanho; melhorar a grelha de projeção é proposta separada, não alteração deste lote.

## Limites

Não foram repetidos percursos completos das lições, impressão, leitor de ecrã, QR físico, projetor da escola, desempenho ou modo noturno. O CSS mantém a miniatura pequena: a informação editorial fina deve ser lida ampliando, não prometida como legível em 170 px. Não se alteram projeção partilhada, Cidadania, Cartaz ou critérios pedagógicos.

Publicação automática autorizada após os testes críticos, em lote pequeno. CI do head final e resultado público devem ficar registados no PR, distinguindo testes específicos e regressão geral complementar.
