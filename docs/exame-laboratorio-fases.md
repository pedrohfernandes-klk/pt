# Apoio ao exame — auditoria e protótipo

Data: 27/10/2026. Base auditada: `2fbca39d538b467f37f72e276731412267bfe657`.

## Fase 0 — auditoria

O endereço público `/pt/` corresponde ao repositório `pedrohfernandes-klk/pt`, branch `main`. Não existe um repositório acessível com o nome `pedrohfernandes-klk.github.io` na ligação utilizada.

O site é estático, sem pacote de construção. `exame/index.html` carrega `assets/exame/app.js`, `dossier.js`, `sessoes.json` e `exame.css`. O catálogo tem 27 sessões, cinco fases, temporizador, pesquisa, filtros, impressão, correção revelada manualmente e dossiê local com fotografias, importação e exportação. O modo `?projetar=1` oculta dados pessoais. As fontes e as limitações do treino autoral já aparecem na vista de cobertura.

Os estilos usam papel claro, tinta escura, acento terracota, linhas e tipografia sem ornamentos. A implementação reutiliza esses estilos e a aparência universal. Nenhuma sessão, dado, chave de armazenamento, correção, fotografia ou função do dossiê é alterada. A única alteração na página existente é a ligação para o laboratório.

Não foram encontrados ficheiros AGENTS.md na árvore do repositório. Os workflows existentes executam QA por áreas em pull requests; nenhum workflow versionado publica o site. Esta proposta só acrescenta QA em PR. Não altera a configuração do GitHub Pages, não faz merge nem publica.

## Fontes verificadas

- [Página oficial da 1.ª fase de 2026](https://eduqa.pt/exames-nacionais-2026-divulgacao-de-enunciados-e-criterios-1-a-fase/), com critérios definitivos atualizados em 10/07/2026.
- [Critérios definitivos, Português 639, 2026, 1.ª fase](https://eduqa.pt/wp-content/uploads/2026/07/portugues_prova_639_cc.pdf), pp. 1–3: articulação entre critérios gerais e específicos, C-ED e CL, aceitação de formulações válidas alternativas e estruturação da resposta restrita.

Utiliza-se o documento definitivo, em vez da versão de trabalho adaptada encontrada inicialmente. O protótipo não reproduz itens oficiais nem atribui os seus níveis/pontos a textos autorais. A lista de revisão é uma adaptação didática dos parâmetros gerais, com tópicos próprios de cada texto. O campo de escrita não faz avaliação semântica automática. A validação automática refere-se apenas às escolhas fechadas, com explicação contextual.

## Fase 1 — protótipo para validação

Rota proposta: `exame/laboratorio/`.

- Quatro máquinas: interpretação da instrução, seleção de prova textual, resposta breve e avaliação fundamentada de uma resposta insuficiente.
- Dois textos autorais com quatro tarefas cada. São amostras simples para validar a dinâmica, não uma cobertura do programa ou uma simulação da dificuldade integral do exame.
- Escolha livre de texto/máquina; resposta, escolhas e autoavaliação mantidas em memória ao alternar, até fechar/recarregar a página. O protótipo não integra estes registos no dossiê.
- Pista, resposta possível e critérios revelados em três passos manuais. As escolhas dão feedback fundamentado ao pedir verificação.
- Projeção por botão ou `?projetar=1`, campos pessoais ocultos, temporizador de dois minutos, papel sem soluções e impressão apenas dos apoios já revelados.
- Distinção explícita oficial/adaptado/formativo. Todas as amostras são formativas. Quatro linhas é uma meta didática, sem imposição no campo e sem alegação de regra oficial.

## Validação antes de avançar

Verificar em sala a legibilidade, o ritmo de dois minutos, a utilidade das pistas e a clareza dos critérios por texto. Comparar a primeira resposta com a revisão. Rever a qualidade e a exigência das amostras antes de aumentar o banco.

## Fase 2 — após validação do protótipo

Adicionar itens oficiais identificados por ano, fase, versão e número; ligar cada item ao enunciado e aos critérios específicos definitivos. Registar qualquer alteração como adaptação, incluindo o que mudou. Atribuir pontos apenas segundo a grelha correspondente, sem converter a lista didática numa suposta escala oficial universal. Expandir os contextos para educação literária e leitura, com revisão docente de cada modelo e distrator.

## Fase 3 — após validação pedagógica

Integrar o registo no dossiê, se aprovado; testar migração, exportação e privacidade em projeção. Só depois de aprovação explícita fazer merge/publicação. Não ativar classificação automática de texto livre sem um processo próprio de validação.

## Verificação reproduzível

`node --check assets/exame/laboratorio.js`

`python -m unittest discover -s tests -p 'test_exame*.py' -v`

`node tests/browser_exame_laboratorio.cjs` (Playwright instalado; opcionalmente `PT_BROWSER_CHANNEL=msedge` para usar Edge local).

O teste de navegador cobre as oito combinações, respostas certas/erradas, apoios ocultos/revelados, autoavaliação, impressão sem soluções/dados pessoais, projeção, reinício, temporizador e preservação do catálogo com 27 sessões, a 390 e 1366 px. O workflow de PR também executa os testes existentes de cache e alinhamento das sessões.
