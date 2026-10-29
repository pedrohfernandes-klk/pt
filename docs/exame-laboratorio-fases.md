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

## Redesenho «Oficina da palavra» (27/10/2026, para validação)

Decisões do docente (27/10): a identidade fica só no laboratório; fontes livres em ficheiros locais. O nome público continua «Laboratório de respostas».

- **Fontes:** Fraunces (leitura e títulos; eixos de tamanho ótico e peso) e IBM Plex Sans (orientação e ferramentas). Ambas SIL Open Font License 1.1, com a licença ao lado dos ficheiros (`assets/exame/fontes/`). Subconjunto latino com todos os glifos do português, cerca de 194 KB no total. Sem serviço externo; recurso a Georgia e Arial.
- **Tokens:** só em `body.oficina` (prefixo `--of-`), em claro e escuro. O contraste foi medido: texto ≥ 4,5:1 nos dois temas. O amarelo serve só de fundo, com texto escuro.
- **Assinatura:**
  - os quatro verbos do título passam a ser o índice das máquinas (Pensa, Prova, Responde, Revê), com o número de oficina;
  - o rótulo «Instrução» como recorte;
  - o traço de anotação.
- **Quatro máquinas, quatro composições:**
  - **01:** a instrução é anotada (verbo de comando, objeto, condição) só depois de verificares.
  - **02:** as linhas do texto são as próprias escolhas, com «Verificar» logo a seguir.
  - **03:** caderno pautado com margem e relógio.
  - **04:** a resposta em revisão fica no campo de leitura, com marcas de corretor e conteúdo (C-ED) separado de língua (CL).
- **Estado:** o relógio é estado de cada exercício. Revelar apoios não o reinicia nem apaga o rascunho. Mudar de máquina ou de texto põe-no em pausa, e a pausa é anunciada. As atualizações são parciais e conservam o foco: ao revelar, o foco vai para o título do apoio.
- **Projeção:** em 1366×768, o texto, a instrução, as escolhas e «Verificar» cabem no primeiro ecrã. Em 1920×1080, o texto principal fica perto de 30 px. Os campos pessoais continuam ocultos.
- **Papel:** A4 a preto e branco, com:
  - cabeçalho com o número da oficina;
  - linhas com referência;
  - instrução em caixa;
  - linhas de escrita que saem sem a opção de imprimir fundos;
  - origem no fim.
- **Testes novos** (`tests/browser_exame_laboratorio.cjs`): contraste nos dois temas, relógio e rascunho conservados, pausa ao mudar de máquina, foco, teclado, anotações só depois de verificar, papel e primeiro ecrã da projeção.

Por validar em sala: legibilidade à distância, ritmo dos dois minutos e clareza das anotações.

## Percurso e revisão da própria resposta (28/10/2026, para validação)

Mantém-se a identidade «Oficina da palavra» e o banco de dois textos autorais. Esta intervenção melhora a ligação entre operações e a observação da aprendizagem:

- Navegação anterior/seguinte no mesmo texto; depois de «Sê o corretor», regresso à própria resposta. A indicação de etapa é navegação, não conclusão ou classificação.
- Na escrita, consulta dos critérios antes de produzir a resposta, sem revelar o modelo nem saltar a sequência dos apoios.
- Ação explícita para conservar uma primeira versão imutável e trabalhar a revisão; campo para justificar o que mudou e que critério orientou a alteração.
- Primeira versão, versão revista e reflexão mantidas separadamente por texto, em memória, ao alternar de máquina. Não há persistência após recarga nem integração no dossiê. A interface explica que é necessário copiar o trabalho antes de sair.
- Textos pessoais ocultos na projeção e excluídos de ambas as impressões; escape de conteúdo mantido. Recomeçar com texto escrito exige confirmação para evitar perda acidental.
- Feedback específico para cada linha escolhida. Em «O regresso», o contrato é reconhecido como evidência relevante mas incompleta, a relacionar com os gestos da despedida; não é marcado como simplesmente errado.
- Testes adicionais: percurso ligado, critérios sem modelo, conservação de versões/reflexão, texto tratado como texto, privacidade, cancelamento/confirmação do reinício e composição móvel.

Não foram acrescentados itens oficiais nem notas automáticas. Próxima validação pedagógica: verificar se a segunda versão melhora nos tópicos concretos de C-ED e se o aluno consegue explicar essa melhoria. A expansão do banco deve preservar a identificação da origem e a correspondência com critérios específicos.

## Textos compostos, identidade nas sessões e relógio do aluno (27–28/10/2026)

Pedido do docente (27/10): uma cantiga não pode parecer um relatório; subir um degrau na tipografia, nas cores e na identidade, com princípios de Gestalt, sem perder a matriz.

- **Textos das sessões:** os 15 recortes literários deixam de ser texto achatado. Cada um é reconstruído a partir da lição de onde vem (`source.passages`): versos e estrofes, omissões marcadas com «[…]», parágrafos numerados, falas de teatro com o nome da figura e as didascálias em itálico, palavras explicadas com nota numerada (como no exame nacional) e crédito com os títulos em itálico. Três referências antigas foram corrigidas pelo caminho: a lição da cantiga de Codax («As cantigas lado a lado»), a estância «Nas naus estar se deixa vagaroso» (VIII, 96) e a parte «Noite Fechada» do poema de Cesário. Cada verso e cada parágrafo guarda a referência à linha da lição; `tests/test_exame_textos.py` falha se a lição mudar e o exame ficar desalinhado.
- **Identidade:** `assets/exame/oficina.css` reúne as fontes (Fraunces e IBM Plex Sans, locais, OFL) e os tokens claros e escuros, comuns ao laboratório e às sessões. Nas sessões, os tokens antigos passam a ler a Oficina; cada fase tem a sua cor (aquecer amarelo, ler azul, escrever óxido, corrigir verde, fechar tinta) e cada ano do catálogo também.
- **Relógio do aluno** (`assets/relogio.js`, comum às aulas de tarefa): o aluno escolhe a duração até ao máximo; pode pausar duas vezes; depois disso, parar recomeça do início. Sessões: o máximo é o tempo da fase (5, 8, 10 a 20, 7 a 17 e 5 min). Laboratório: um relógio por exercício, com máximos de 1, 2, 2 e 3 min (máquinas 01 a 04, a validar em sala); mudar de máquina com o relógio a contar conta como pausa e é anunciado.
- **Texto do sítio:** sem «ficha» nem «folha» nas sessões (os dois casos que ficam são citações de Camilo e de Álvaro de Campos).

Por validar em sala: leitura das notas à distância, os máximos do laboratório e a regra das duas pausas.

Ao juntar as duas linhas (29/10/2026), o relógio do aluno passou a servir também o percurso: um relógio por exercício, com os mesmos máximos, e «Recomeçar esta máquina» pede confirmação antes de repor o texto, a revisão e o relógio.
