# Exame — recuperação da correção local

20 de outubro de 2026. Ramo local: `work/percursos-unidades-20261020`, base `9c48a2846924378be597ec6a34b7a666be84bc3b`. Sem push, merge, publicação ou alteração do checkout antigo.

## Recuperado e corrigido

Os dois ficheiros da área de exame tinham a mesma base no checkout antigo e no atual. Foram recuperadas as alterações não commitadas de `codex/exame-cache-dados`, preservando o trabalho dos módulos deste ramo.

- O pedido de `sessoes.json` passa a acompanhar a versão de `app.js`, para que uma atualização do programa solicite também os dados dessa versão.
- Referências dos recursos do exame atualizadas para `20261019-exame-3`.
- O aquecimento consome primeiro a pergunta ainda não apresentada antes de repor o banco, mantendo dois itens distintos.
- Corrigida uma referência de versão mal formada encontrada no ficheiro antigo do lançador de projeção; preservada a versão própria desse recurso.

## Verificado

- Sintaxe de `app.js` válida.
- Catálogo: 26 sessões e 104 itens; tempos, respostas e destinos locais válidos.
- 19 verificações específicas do dossiê passaram.
- Chromium a 320 e 1440 px: pedido de dados com a mesma versão do programa, consumo prioritário dos itens restantes, dois itens distintos em rotações sucessivas, manutenção do par após recarregar, sem erros JavaScript nem transbordo horizontal.
- Teste de navegador acrescentado à integração contínua; caminhos de exame incluídos nos gatilhos.

## Limites

A verificação confirma o pedido versionado em ambiente local. Não foi publicada nem verificada a atualização numa instalação pública com cache antiga, e não se certifica o comportamento de todos os navegadores. Não foi repetido o ciclo completo de exportação/importação com fotografias no navegador neste bloco. Mantêm-se os testes específicos do dossiê e os resultados históricos documentados.

Continua pendente confrontar as 26 sessões com as fichas entretanto corrigidas. Não foi feita aqui uma revisão curricular nem confirmada a conformidade com regras de exame de 2027.
