# Variedade F0: ajuda e progresso compatível

## Integração incremental do main publicado, 03/11/2026

O main `123335cf9804a493c003ea03b6806196833d91ef`, com os créditos aprovados do #164, entra por merge sobre a cabeça em revisão `c87d871d2653f68e0c6e31a0bf50201cd6dd44da`. Não entra código da F2. Esta integração não equivale a aprovação da migração nem a autorização de publicação.

Os dez conflitos eram nas listas e funções de reversão. A ordem fica F0, créditos de IA, lote 2 e camadas anteriores. Mantêm-se todas as contagens e asserções estritas; os testes alterados levam comentário de 03/11/2026. O manifesto F0 foi regenerado sobre `123335cf`, com as mesmas 24 trocas e os mesmos 21 destinos. O código de migração, o JSON da camada F0 e os vinte aquecimentos são idênticos, byte a byte, à cabeça anterior: 22 ficheiros conferidos. No índice, a única diferença visível para essa cabeça é o crédito aprovado do #164.

Validação desta integração: 453 testes unitários aprovados, 20/20 camadas, oito ensaios de navegador da migração, 60 casos de ajuda e sete casos de importação. Os registos locais são `f0-pos164-unitarios.log`, `f0-pos164-camadas.log` e `f0-pos164-browser.log`, junto às cópias de trabalho. A confirmação incremental e o CI da nova cabeça ficam a cargo da revisão antes de seguir para a F2.

02/11/2026. Primeiro passo da variedade, antes dos tipos F2/F3. Ramo separado `codex/variedade-f0-20261102`, com a correção PT156-01 integrada por merge. Não inclui o adaptador F2 nem os tipos do GPT2. A publicação depende da revisão e da ordem da fila, incluindo #156 e #164.

## O que muda

O gerador `scripts/aquecimentos.py` acrescenta o botão «Como se faz» ao cabeçalho. Foram regenerados os vinte aquecimentos atuais, não apenas os dez que o plano antigo contava. Cada página é igual ao resultado anterior, byte a byte, exceto pelo botão. Cartões, respostas, versões, chaves e ligações ficam intactos. O botão usa a ajuda já existente na casca; esta fase não regrava nem certifica o conteúdo dos vídeos.

`assets/pt-lessons/acrescentos.js` fornece a migração dos índices quando um lote posterior inserir cartões. Ainda não há inserções de cartões nesta fase. O recurso só migra uma lição quando carrega com `data-chave`, `data-lote` e `data-novos` explícitos. Sem esses atributos, apenas disponibiliza as funções de compatibilidade da importação.

Na entrada do sítio, a importação do progresso guarda primeiro uma fotografia das marcas de lote do aparelho. Assim, a ordem das chaves do ficheiro importado não altera o resultado. Quando uma versão tem lotes que a outra não tem, não se misturam as suas `exposicoes` e `ult`. Conservam-se os restantes campos e as regras de fusão anteriores, incluindo melhores resultados, tentativas e conclusão. Se os conjuntos de lotes forem incomparáveis, os índices ficam por reconstruir nas tentativas seguintes; não se inventa uma correspondência entre cartões. As marcas dos lotes continuam a acompanhar o progresso exportado.

## Contrato de migração

```html
<script src="../../assets/pt-lessons/acrescentos.js?v=20261102-f0"
        data-chave="licao-m4-f01" data-lote="n106-m4" data-novos="5,9"></script>
```

As posições são base zero, no banco final depois das inserções. A linha entra depois das migrações antigas do banco e antes da chamada a `EPIJogo.montar`. Não se altera o `?v` do motor. Um lote entra uma vez; vários lotes entram pela ordem das suas linhas.

Fora da projeção, marca-se o lote em `K-acrescentos`, mesmo quando não há progresso. Só se escreve em `K` quando já existem tentativas ou exposições. A marca externa sobrevive à regra de `versao` do motor. Os campos `versao`, `banco`, `lida`, `melhor`, `totalMelhor`, `tentativas`, `xp` e `mais` não são alterados pela migração. `ult` mantém a ordenação textual do motor. Em projeção não se lê nem escreve o armazenamento. Falhas de armazenamento não impedem a leitura; uma falha ao escrever o estado repõe a marca anterior.

Não se devem voltar a inserir as mesmas posições com outro identificador de lote. Os manifestos das futuras camadas têm de ligar cada lote à sua inserção, com painéis e guiões coerentes, como determina o plano F6.

## Camada literal e testes históricos

`scripts/variedade_f0_20261102.json` contém 24 trocas em 21 ficheiros: vinte cabeçalhos gerados e quatro mudanças na importação da entrada. O manifesto é `tests/fixtures/variedade-f0-edits-20261102.json`. A reversão F0 entra antes do lote 2; as ocorrências e os hashes continuam estritos. Não se reescreveram camadas antigas.

Os testes históricos mudam apenas para desfazer a camada nova antes das anteriores, com comentário datado. Os testes dos aquecimentos continuam a comparar diretamente a página com o gerador. O novo fluxo `pt-variedade-f0-qa.yml` executa os testes de migração, a camada e os navegadores específicos.

## Provas já concluídas

- Migração: 600 correspondências de índices verificadas pelo teste unitário, com preservação dos restantes campos e rejeição de entradas inválidas.
- Oito cenários Chromium da migração: ausência de progresso; primeira tentativa e recarregamento; dois lotes e repetição; versão conservada; ordem textual; migrações anteriores M2-F06/F07; importação incompatível; projeção sem leitura/escrita; armazenamento inválido e falha de escrita. Alguns cenários incluem mais de um caso.
- Três testes da camada F0: âmbito exato, hashes reversíveis e vinte bancos/chaves/versões intactos.
- Os 14 testes existentes dos aquecimentos passaram sem alteração.
- Sessenta casos de ajuda: vinte páginas em 320 escuro, 390 claro e 1366 com projeção. Abertura por teclado, ligação do vídeo, fecho por Escape, sem transbordo ou alteração de progresso. A reprodução integral dos vídeos não foi certificada por estes testes.
- Sete importações reais pela interface da entrada: aparelho mais recente, ficheiro mais recente, lotes iguais, lotes incomparáveis, primeira importação, marca local sem registo e marca recebida sem tentativa. Conferidos índices, melhores resultados, tentativas, versão e conclusão.

Bateria final: 453 testes unitários aprovados e 19/19 camadas conferidas. A primeira execução encontrou uma regressão na posição do recurso da entrada: separava os blocos de limpeza e importação. A camada coloca agora o recurso antes de ambos, conservando a adjacência exigida pelo teste original. Nenhum limite nem asserção foi alterado. Os 60 casos de ajuda e as sete importações passaram novamente com esta correção. O CI será registado no pedido antes da confirmação. Não há autorização de publicação neste documento.

## Ligação com as fases seguintes

F2 recebe esta fase por merge. O contrato F2/F3 está preparado noutro ramo, com adaptador em ensaio; não faz parte da publicação F0. Os aquecimentos do exame do #155 continuam no ramo da sua equipa. Quando integrarem o gerador comum, devem regenerar as páginas e conservar esta ajuda, sem alterações nas respostas ou nas chaves. As cópias e os motores do Lente permanecem com a equipa que detém esses caminhos.
