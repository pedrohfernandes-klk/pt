# Discurso indireto livre — piloto de composição

Base: af75f7441bb4f28060d5672bb2c199be4ff74654. Apenas `m5/gram-dil/index.html`, fora dos ficheiros dos PRs #80 e #92 e das alterações locais observadas nos outros checkouts. Não publicado: o utilizador pediu comparação e apreciação do piloto antes de publicar ou replicar.

## Composição

- Proximidade: excerto e explicação pertencem à mesma região. Em computador ficam lado a lado; em telemóvel, a explicação segue imediatamente o excerto.
- Hierarquia: o excerto tem serifa e maior dimensão; os rótulos e as explicações usam a tipografia corrente. As letras A/B/C e a margem da tarefa recebem um apontamento de terracota discreto.
- Região comum: o relato de João e a produção no caderno ficam num grupo próprio. O conteúdo anteriormente dentro de um detalhe passa a estar visível; isto aumenta a extensão vertical do cartão.
- Fonte: mantém destino, texto, indicação de abertura externa e área de interação de pelo menos 44 px, com aspeto de ligação bibliográfica em vez de grande botão preto.

Os três excertos, a definição de indireto, a contextualização do relato e a encomenda no caderno foram preservados. A explicação de indireto livre foi distribuída junto de B e C. Os nove passos mantêm ordem estrutural e dados; questões, alternativas, gabaritos, feedback, fontes, identificadores, progresso e código de execução não mudaram. A variação já existente entre tentativas permanece.

## Verificações executadas

- 174 testes Python aprovados, correspondentes à base deste piloto. Os quatro testes do auditor M4 pertencem ao PR #92 e não foram misturados nesta branch.
- Comparação programática antes/depois: todos os campos de dados fora do HTML da primeira leitura iguais; código de execução e estrutura da página iguais fora do novo estilo; excertos e tarefa conservados.
- Navegador, 1280 × 720 e 390 × 844: capturas antes/depois; sem transbordo horizontal na página normal; explicações empilhadas no telemóvel. A tarefa e a fonte foram inspecionadas após deslocação vertical.
- Fonte alcançável por teclado; Tab passa para o controlo seguinte. Área da fonte: 44 px na verificação de computador.
- Passagem da leitura ao exercício, resposta correta numa tentativa nova, feedback e retoma após recarregar: observados. A ordem pode variar numa nova tentativa, conforme o comportamento existente.
- Projeção local com QR visível e ligação pública correta; controlos pequeno/médio/grande e ocultação do QR responderam. Capturas da projeção anterior e do piloto. Não houve leitura física do QR.
- `git diff --check` sem problemas.

## Pendência funcional observada

Depois de uma resposta corrigida, o botão «Voltar ao passo anterior» não recuou no ensaio. O mesmo comportamento foi reproduzido na cópia anterior, com o mesmo estado guardado. Não foi introduzido pelo piloto (código de execução comprovadamente igual), mas não deve ser declarado aprovado: diagnosticar e corrigir num lote próprio antes de certificar o percurso completo. A retoma da resposta e o avanço funcionaram.

Não foram executados percurso integral dos nove passos nesta ronda, leitor de ecrã, aparelho físico, impressão, verificação visual do modo escuro ou medição de desempenho. O novo CSS contém adaptações para modo escuro e impressão, mas isso não equivale a teste real. Capturas são evidência de composição, não de benefício comprovado em turma.

## Próximo passo

Apreciar o piloto com as comparações. Manter a alteração isolada; não publicar nem replicar antes dessa apreciação. Tratar o regresso num lote separado, sem interferir com trabalhos concorrentes. O crescimento vertical é a principal contrapartida a avaliar: o cartão exige mais deslocação, mas não esconde a tarefa.
