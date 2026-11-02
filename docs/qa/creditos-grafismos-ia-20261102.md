# Atribuição dos grafismos gerados com recurso a IA

02/11/2026. Correção editorial separada do #156, sobre o main `d1f343535901b0bb0045032196f3f09c398a8c4e`. Não altera os pedidos fechados #152/#163 nem as imagens documentais de terceiros.

## Inventário transversal

A pesquisa percorreu as páginas publicadas, SVG, CSS, JavaScript e geradores Python do Português, procurando «desenho nosso», variantes de género e número, «grafismo nosso», «ilustração nossa» e atribuições análogas próximas de «EPI». Foi confirmada uma atribuição publicada deste tipo: o grafismo da calçada na entrada.

| Ficheiro | Função | Tratamento |
| --- | --- | --- |
| `index.html`, `.cf-credito` | Legenda visível da calçada | «Desenho nosso, pedra a pedra» passa a «Grafismo gerado com recurso a IA». Mantêm-se EPI, 2026, padrão de ondas, «mar largo», Rossio e Lisboa, bem como o botão de movimento. |
| `scripts/creditos_grafismos_ia_20261102.json` | Fonte atual da alteração da legenda | Nova camada literal, aplicada pelo gerador existente, por cima da varredura. |
| `scripts/gerar_calcada_mar.py` | Gerador determinístico do SVG | Crédito do comentário gerado atualizado. |
| `assets/calcada-mar.svg` | Saída do gerador | Regenerada e conferida; só o comentário de atribuição muda. |
| `assets/fundo-calcada.css` | Comentário de identificação do grafismo | Atribuição de IA explícita; a descrição já não usa «pedra a pedra». As regras CSS ficam iguais. |
| `scripts/calcada_mar_20261102.py` e camadas/manifestos anteriores | Construção e registo histórico da versão publicada | Conservados para reproduzir e desfazer essa versão. A camada nova aplica a instrução posterior; não se reescrevem as alterações históricas. |
| `m9/licao-m9-f05/index.html` | Encomenda de uma animação ao aluno, «pedra a pedra» | Conservada: é uma proposta de produção, não uma atribuição de autoria do grafismo. |

A pesquisa não confirmou outras legendas publicadas com estas atribuições. Não se presume que imagens documentais sejam feitas com IA por terem sido incluídas no sítio com apoio de ferramentas de programação.

## Correspondência entre fonte e saída

A legenda HTML resulta de `scripts/aplicar_trocas.py scripts/creditos_grafismos_ia_20261102.json`. O manifesto guarda os textos exatos, a ocorrência única e os hashes antes/depois. O SVG foi regenerado por `scripts/gerar_calcada_mar.py`; a opção `--verificar` confere a saída byte a byte. Removendo apenas o comentário XML, o SVG anterior e o novo são idênticos: geometria, dimensões, cores e ordem dos elementos não mudam.

O script que construiu a camada antiga da calçada é um registo histórico, não a fonte atual do crédito. Uma reconstrução completa aplica primeiro essa camada e depois a nova atribuição de IA. Esta distinção evita alterar a intenção da camada já publicada.

## Validação

444 testes unitários aprovados; 18 de 18 camadas conferidas. SVG regenerado e verificado pelo gerador. Conferência visual aprovada a 390 e 1366 px: legenda e referência legíveis, botão de pausa conservado, sem deslocamento horizontal. O pedido fica em rascunho e aguarda revisão e lugar na fila de publicação.


## Integração depois da publicação do #156

Main `bd9ec1ba3e82e0a2e76ab9aac674b0154310d908` integrado por merge, depois da publicação do #156. A camada de créditos fica acima de `conteudos_lote2_20261101`, com o manifesto regenerado sobre esta base. As verificações desfazem primeiro os créditos e depois o lote 2; conservam as asserções e os hashes históricos. Não há alterações ao conteúdo aprovado do #156.

Validação desta integração: 449 testes unitários aprovados; 19/19 camadas; SVG conferido pelo gerador; crédito visto novamente a 390 e 1366 px, sem deslocamento horizontal. Não foram alteradas a geometria nem as regras visuais. Pedido em rascunho, para confirmação da nova cabeça e atribuição da vez de publicação.
