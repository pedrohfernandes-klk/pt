# M7 compacto e adaptador partilhado — 27/10/2026

Base exata: `13ce769c65e74340b8edf72bbb6aea85aef86f53`. Esta frente altera apenas os três corpos de M7, o adaptador e feedback partilhados e os contratos browser. Não modifica os corpos de M1/M4, índices, workflow, motores, paleta ou lições.

As três tarefas de M7 são individuais. Cada uma tem enunciado e critérios com menos de 180 palavras, ligações precisas a duas ou três lições, duas perguntas opcionais num detalhe fechado e uma verificação breve com síntese de duas linhas e fotografias no Teams. O aluno vê três cartões: Enunciado, Relembrar e Verificar. Não há relógio por fases, rondas, pré-trabalho ou procedimentos de aplicação.

Produtos preservados:
- U1: comparação de 80 a 120 palavras, com uma passagem de cada poema, leitura própria e dúvida fundamentada.
- U2: perfil ficcional, texto de 100 a 150 palavras, duas escolhas justificadas, três fontes com data e diferenças, apresentação de dois minutos e resposta a pergunta.
- U3: objeto individual, memória de 150 a 200 palavras, três propostas antes da escolha, três mudanças justificadas e defesa de três minutos com perguntas.

O modo `data-task-compact` do adaptador não extrai as duas perguntas para cartões autónomos, não esconde o quiz e não desloca o seu estado para fora do detalhe opcional. Mantém a casca existente, o índice livre, teclado, hashes, detalhes, deslocação própria, impressão e alternativa sem JavaScript. O feedback conta o número real de grupos: dois nos novos compactos; quatro no apoio comparativo antigo.

M7 carrega os dois scripts com `v=20261027-compact-1`. Depois de integrar os corpos compactos de M1/M4, o integrador deve atualizar também essas cinco páginas para esta versão dos scripts. Os seus corpos e heads não foram alterados nesta frente.

## Evidência de migração

`tests/fixtures/task-compact-m7-before-after.json` contém, para cada caminho, `before_source`, `before_sha256`, `after_source`, `after_sha256`, `before_body` e `after_body_sha256`, em UTF-8/LF. O original foi obtido da base exata por Git. Permite restaurar literalmente a página anterior nos contratos históricos, sem regenerar as fixtures dos conteúdos literários.

Os quatro testes novos de compacto M7 passam: forma de três cartões, concisão, perguntas opcionais, produtos, fontes e manifesto literal. O teste Node verifica o mesmo feedback com dois e quatro grupos. Ambos os scripts passam a verificação de sintaxe Node; os helpers browser foram analisados sintaticamente.

Na suite parcial desta frente foram executados 236 testes: as oito falhas e três erros pertencem exclusivamente aos contratos históricos de M7 que ainda exigem o corpo anterior, quatro perguntas ou relógio por fases. Esses contratos não foram alterados, por instrução do integrador; a reconciliação será feita com os três manifestos depois de reunir M1/M4/M7. Não houve falhas de M1/M4 nem do feedback partilhado.

A matriz browser mantém 32 combinações e as oito alternativas sem adaptador, agora compatíveis com os compactos de duas perguntas e três cartões. Não foi executado Playwright localmente. A validação visual e mobile depende da CUA do pai e da CI.
