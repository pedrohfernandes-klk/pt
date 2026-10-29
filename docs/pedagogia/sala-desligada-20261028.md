# A Sala de aula desligada no sítio publicado (28/10/2026)

A 17/10/2026, o docente decidiu desligar a «Sala de aula em tempo real» (ponto 22 de DECISOES). A Sala enviava a alcunha, a lição e os pontos de cada aluno para tópicos públicos do ntfy.sh, que qualquer pessoa com o código de cinco caracteres podia ler e escrever. Nas fontes, a mudança fez-se nesse dia (`_interno/modelo/sala.mjs`; a história e o código antigo estão em `_interno/arquivo/sala-desligada-2026-10-17.md`). No sítio publicado, as 204 páginas que ainda falavam com o ntfy.sh mudam agora. Este PR também fecha o ponto que a auditoria do M1 e do M4 deixou em aberto: o código da sala no cabeçalho dos painéis.

## O que saiu

- **Lições (100):** o botão «Sala» do menu, o formulário (código e alcunha), a faixa da pausa, o cartão que interrompia a lição (relâmpago, votação, fecho) e o envio do estado a cada 15 segundos. Sai também o modo de código que aparecia quando a rede falhava. A nota do menu, «O que marcas fica só neste aparelho», passa a ser verdade sem exceções.
- **Desafio da unidade (índices do M3, M5, M6, M8 e M9):** o envio do resultado para o placar. O Desafio continua igual e grava no aparelho.
- **Atlas:** o botão «Sala de aula», o formulário e o envio da parte acesa de cada país para o «mapa da turma».
- **Mapa da turma (`atlas/sala/`):** passa a uma página curta que leva ao Atlas, como nas fontes.
- **Canal:** o `window.EPISala` sai das 204 páginas (`fetch` e `EventSource` para o ntfy.sh, `BroadcastChannel` com `?local`).

## O que fica nos painéis do docente

Ao contrário das fontes, os 93 painéis (`/pt/<m>/painel-<id>/`) continuam a servir a aula no projetor e funcionam sem rede:

- o pedido em letra de cartaz (com itálico no M1 e no M4) e o cronómetro;
- o QR da lição, que já vem embutido na página; no ecrã de abertura cresce e ocupa o lugar do placar;
- a pausa cronometrada, com os cartões a fazer;
- o relâmpago e, de M3 a M9, o «Quem sou eu?» do Atlas (ver abaixo);
- as teclas P, R, F e Esc, e ainda A («Quem sou eu?», que o botão já anunciava) e I («Voltar ao início», que repõe o ecrã de abertura com as instruções e o QR).

Saem o código da sala, o placar com alcunhas, o sorteio, a votação, o campo «Código do aluno» e todos os envios para os telemóveis. A grelha passa a uma coluna. As instruções e os textos que falavam da Sala foram reescritos:

- «Abre a lição no telemóvel pelo QR»;
- «Responde no caderno; depois, em voz alta»;
- «Pousa o telemóvel e olha para o projetor»;
- «Parar o cronómetro» e «Voltar ao início».

### O relâmpago e o «Quem sou eu?» só no projetor

Antes, o painel mandava para os telemóveis o cartão inteiro da lição; o projetor mostrava só o enunciado. Sem telemóveis do outro lado, um enunciado como «Toca nas duas palavras…» ou «Põe os três últimos versos pela ordem» deixava de se poder responder (532 dos 1445 relâmpagos). Agora:

- o projetor mostra, por baixo do enunciado, o material do cartão da lição, baralhado e sem a solução: as opções (A, B, C…), os pares em duas colunas, os itens a ordenar, as palavras da frase, a frase com as lacunas numeradas e as opções de cada uma, a frase onde se procura a palavra, a citação e a imagem quando o cartão as tem;
- uma linha diz o que se escreve no caderno («No caderno, escreve a letra», «escreve os pares: 1 A, 2 B…»…);
- quando o tempo acaba, aparece a correção do próprio cartão (o texto que a lição mostrava depois de responder);
- nos 33 painéis em que a lição tinha mudado e o painel não, os 127 enunciados que tinham ficado para trás passam aos cartões atuais da lição, para o enunciado e o material serem do mesmo cartão;
- o «Quem sou eu?» mostra «Quem sou eu?» em grande, as três hipóteses e uma pista por cada terço do tempo; no fim, o nome e a frase de remate.

Os oito painéis estáticos (notas do docente, prolongamentos) nunca tiveram a Sala e não mudam.

## A limpeza

Em todas as páginas onde a Sala existia, o canal dá lugar a uma limpeza que corre uma vez. É uma cópia literal de `SALA_LIMPAR_JS` de `sala.mjs` e apaga o que a Sala deixou no aparelho:

- `epi-sala` (código e alcunha);
- `epi-sala-atlas`;
- as chaves `painel-sala-*`;
- `epi-atlas-sala`, em `sessionStorage`.

A página inicial corre a mesma limpeza antes de «Guardar num ficheiro» e de «Repor», por isso o ficheiro do progresso deixa de levar a alcunha.

## Lições e índices congelados

52 lições (M1, M2, M4 e M7) e os nove índices estão congelados por hash ou por digest nos testes. As trocas destas 61 páginas estão em `tests/fixtures/sala-desligada-edits-20261028.json`. Cada troca é literal (`location`, `old`, `new`, `occurrences`) e tem sempre texto novo. Os testes desfazem este manifesto primeiro e depois o da auditoria (`tests/auditoria_20261028.py` e `test_task_routes_closure.py`).

## Como voltar a correr o script

```
python3 scripts/desligar_sala.py              # aplica, ou confirma que já está aplicado
python3 scripts/desligar_sala.py --verificar  # não escreve; sai com 1 se houver alguma coisa por fazer
```

O script só faz trocas literais de blocos conhecidos. Se um bloco não aparecer como se conhece, ou se depois das trocas ficar alguma marca da Sala, avisa, não escreve nada e sai com erro. Corrido outra vez, não muda nada. Nas páginas congeladas, desfaz o manifesto da Sala, volta a aplicar as trocas e confere que dá a página atual; o resto da página pode mudar depois (outras trocas literais, outros manifestos) sem estragar o script. Só uma mudança num bloco que as trocas tocam dá aviso, e esse aviso diz que o manifesto já não se desfaz, não que a forma da Sala é desconhecida. Os painéis não estão congelados: para refazer o material do relâmpago depois de mudar o script, repõem-se a partir do último commit e corre-se o script outra vez.

`tests/test_sala_desligada.py` corre `--verificar` e confere o material de cada um dos 1445 relâmpagos (sem a solução). Corre em todos os PR, sem filtro de caminhos (`.github/workflows/pt-sala-qa.yml`), porque a garantia vale para toda a árvore publicada. `tests/browser_sala_desligada.py` abre lições, painéis, dois índices, o Atlas e a página inicial e falha se houver pedidos para fora da origem local. A lista dos pedidos aceites é por página e só tem o que essas páginas pedem de facto: o CSS dos tipos de letra do Google, o estilo do Lente na página inicial e uma imagem com endereço absoluto no índice do M1 (já antes da Sala), e a navegação da página curta `atlas/sala/` para o Atlas publicado (pedido novo, igual ao das fontes).

## Fica por fazer

- Os diapositivos (104 PPTX e 102 PDF) ainda têm o diapositivo «Pausa: cartões no telemóvel», que manda tocar em «Sala». São binários e mudam na próxima geração completa nas fontes.
- Ainda há CSS morta da Sala, que não se vê no ecrã, em `assets/pt-lessons/lesson.css` e na regra `.casca-menu .sala` de 144 páginas que nunca tiveram a Sala.
- Em 22 relâmpagos de painéis sem itálico (M2, M3, M5 a M9), o enunciado guarda ainda os sublinhados do itálico (`_Os Lusíadas_`) e o projetor mostra-os tal como estão. Já era assim antes desta mudança.
