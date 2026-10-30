# Passagem ao Claude: aquecimentos do M1

## 1. Ramo, commit e pedido de integração

- Ramo: `codex/tarefas-m1-aquecimentos-20261030`, criado a partir de `origin/main` em `88af7ff2e353514620b1fcb7cb2bd51f3d28daf3`.
- Último commit de implementação à redação deste relatório: `0cd84c46b3b041512c791b55166a3555edd3cac5`. Este relatório entra num commit documental posterior; o SHA final do ramo está no cabeçalho do [PR #134](https://github.com/pedrohfernandes-klk/pt/pull/134).
- PR **em rascunho**, para `main`: **M1: aquecimentos em cartões nas tarefas das unidades 1 e 2**.
- Autor dos commits: Terra Firme, `terra-firme@epi.local`. Sem merge, sem deploy e sem execução de `publicar.mjs`.
- Estado: implementação funcional, testes específicos aprovados, integração impedida pelos contratos literais por reconciliar e pela suite de base já vermelha. Não apresentar a suite completa como aprovada.

## 2. Ficheiros criados e alterados

Cada caminho é relativo à raiz do repositório.

- `docs/pedagogia/aquecimentos/m1-u1.json`: Novo baralho da lírica, com exemplos de Mendinho e casos inventados.
- `docs/pedagogia/aquecimentos/m1-u2.json`: Novo baralho da crónica, com casos inventados e operações das lições.
- `tarefas/m1-u1/aquecimento/index.html`: Página gerada pelo gerador existente, sem motor novo.
- `tarefas/m1-u2/aquecimento/index.html`: Página gerada com o mesmo formato e a chave própria de progresso.
- `docs/pedagogia/tarefas-escolha/m1-u1.json`: Substitui o aquecimento em papel pelo esquema de cartões; cerca de passa a aproximadamente no lead.
- `docs/pedagogia/tarefas-escolha/m1-u2.json`: Substitui apenas o objeto aquecer, mantendo o restante conteúdo.
- `tarefas/m1-u1/index.html`: Tarefa regenerada com ligação aos cartões e relógios de 10 e 60 minutos.
- `tarefas/m1-u2/index.html`: Tarefa regenerada com os mesmos acessos e distribuição temporal.
- `m1/index.html`: Acrescenta exclusivamente duas linhas A, imediatamente antes das linhas T.
- `m1/guia-da-tarefa-m1/index.html`: Atualiza apenas o parágrafo atual de abertura; preserva o arquivo das produções antigas.
- `scripts/auditar_aquecimentos_m1.py`: Mede todas as opções redigidas, incluindo lacunas, e recusa pistas de comprimento acima dos limites.
- `tests/test_task_aquecimentos.py`: Alarga o contrato existente aos dois baralhos do M1 e generaliza a identificação do módulo.
- `tests/browser_task_aquecimentos.py`: Percorre também o M1, as ligações às tarefas, a projeção e as linhas A do percurso.
- `tests/test_task_choice.py`: Reconhece os dois aquecimentos em cartões, mantendo as mesmas exigências de conteúdo e extensão.
- `tests/test_m1_unit_tasks.py`: Acrescenta a verificação da interface atual; conserva as asserções sobre os predecessores históricos.
- `tests/test_aquecimentos_m1_opcoes.py`: Verifica variedade, momento, todas as citações e distribuição das opções, incluindo empates.
- `tests/browser_aquecimentos_m1_feedback.py`: Experimenta certo e errado em todos os dez cartões ativos de cada baralho a 390 px.
- `.github/workflows/pt-tarefas-qa.yml`: Acrescenta os novos testes e auditoria à validação contínua, sem retirar testes existentes.
- `docs/pedagogia/relatorios/2026-10-30-m1-aquecimentos/RELATORIO-CLAUDE.md`: Este relatório de passagem e as decisões para revisão.
- `docs/pedagogia/relatorios/2026-10-30-m1-aquecimentos/OPCOES.json`: Resultados por escolha, com comprimentos e indicadores dos limites.
- `docs/pedagogia/relatorios/2026-10-30-m1-aquecimentos/RESULTADOS-TESTES.txt`: Saídas dos testes específicos e de navegador, falhas adicionais por inteiro e identificação das falhas da base.

Não foram alterados o exame, os seus recursos, o CSS das lições, `jogo.js`, qualquer lição ou qualquer manifesto literal. O guia da tarefa foi tratado como guia, explicitamente referido na instrução dos tempos; não foi alterada uma lição.

## 3. Resumo dos dois baralhos

Ambos têm 12 cartões: abertura, dez cartões ativos e fecho. Há seis tipos ativos: emparelhar, escolha, completar, ordenar, rever e V/F. Os exemplos criados são assinalados como inventados e escritos sem guillemets. As respostas abaixo pertencem apenas aos aquecimentos, não às tarefas avaliadas.

### M1-U1: Voz, repetição e prova

| N.º | Tipo | Operação treinada | Resposta certa |
|---|---|---|---|
| 1 | ler | Orientação, consulta e separação da tarefa | Sem resposta; dez minutos, sem nota. |
| 2 | emparelhar | Distinguir identificar, citar, classificar e explicar | Identificar: indicar quem fala; citar: copiar palavras exatas; classificar: dar o nome ao recurso; explicar: ligar recurso e efeito. |
| 3 | escolha | Distinguir autor e voz através de uma marca textual | Uma voz feminina que espera o amigo; fremosa marca o feminino. |
| 4 | completar | Classificar a repetição no fim das estrofes | Refrão fixo. |
| 5 | escolha | Limitar uma conclusão pelo tempo verbal | A voz anuncia uma morte ainda futura; não conta uma morte consumada nem uma salvação. |
| 6 | ordenar | Construir uma resposta fundamentada | Leitura da espera → citação → nome e localização do refrão → explicação da persistência perante o perigo. |
| 7 | emparelhar | Identificar um processo no segmento selecionado | luna/lua: síncope; ante/antes: paragoge; semper/sempre: metátese; p/b em lupum/lobo: sonorização. |
| 8 | completar | Justificar o nome do processo com a posição | No meio da palavra. |
| 9 | escolha | Encontrar uma contradição num texto criado | A terceira linha nega a discrição prometida. |
| 10 | rever | Corrigir uma atribuição biográfica indevida | Na cantiga, a rapariga anuncia a sua morte no mar. |
| 11 | vf | Controlar uma promessa sobre o conteúdo da obra | Falso: não se pode anunciar um resgate que a cantiga não narra. |
| 12 | ler | Transferir operações para a tarefa | Sem resposta; escolher provas próprias e explicar os efeitos. |

### M1-U2: Da pista à cena

| N.º | Tipo | Operação treinada | Resposta certa |
|---|---|---|---|
| 1 | ler | Assinalar a natureza dos casos | Sem resposta; cinema e biblioteca são casos inventados. |
| 2 | emparelhar | Separar informação, inferência, interpretação e opinião | Porta fechada: explícita; querer entrar: inferência; obstáculo: interpretação; magnífica: opinião. |
| 3 | escolha | Distinguir aviso e acontecimento confirmado | O porteiro lançou um aviso de fogo. |
| 4 | completar | Relacionar pormenor sensorial e efeito | Pôr o leitor na cena. |
| 5 | escolha | Confrontar fontes que divergem | Indicar cada versão e a sua origem. |
| 6 | ordenar | Rever com fontes e mostrar a alteração | Voltar às fontes → conferir factos/citações → assinalar falas criadas/coerência → riscar e justificar. |
| 7 | emparelhar | Reconhecer operações de escrita e gramática | da biblioteca: completa um nome; range: som; Para/escuta/corre: gradação; grupo inteiro: ação conjunta. |
| 8 | completar | Comparar o que imagem e relato permitem mostrar | A reação de quem vê. |
| 9 | escolha | Explicar o efeito de uma gradação | As ordens aumentam a urgência da ação. |
| 10 | rever | Declarar a origem de uma fala criada | A técnica diz Abre a porta (fala imaginada). |
| 11 | vf | Limitar a liberdade de criação pelas fontes | Falso: a fala imaginada não pode contradizer os factos das fontes. |
| 12 | ler | Transferir o treino para a tarefa | Sem resposta; provas próprias, fontes identificadas e criação assinalada. |

## 4. Passagens reservadas e exclusão

**U1:** ficam fora dos cartões as passagens de Codax usadas na tarefa, as cantigas de louvor/contralouvor de D. Dinis e Guilhade, os exemplos mare, malu, amicum e acume e a promessa Chega já. O treino literário usa Mendinho e um texto de segredo inteiramente criado. Os processos fonológicos usam outros segmentos de F05.

**U2:** ficam reservados o grito do pajem, a reação da cidade no capítulo XII, o sino e a defesa do capítulo CXVI e a fome/grão de trigo do capítulo CXLVIII, bem como a fala adulterada da tarefa e a forma pra. O treino usa só casos novos, claramente inventados. Não publica uma leitura resolvida destes episódios.

Além das âncoras identificadas manualmente, `reservadas` inclui todas as citações de 12 ou mais caracteres dos dados públicos de cada tarefa. A lista exata está nos dois JSON. O gerador recusa a presença das cadeias reservadas em qualquer cartão ativo, sem distinguir maiúsculas. Os testes repetem essa verificação. Esta é uma proteção literal, não um detetor de paráfrases: a revisão pedagógica adicional confirmou a separação dos textos e episódios.

As citações de Mendinho conferem nas lições F01/F02, incluindo pontuação e parênteses retos. Os processos selecionados conferem em F05. A U2 aplica as distinções de F20, as operações de F08/F10 e a gradação de F07, sem importar os excertos reservados. O novo teste confere também citações com menos de 12 caracteres, embora o gerador só exija as maiores.

## 5. Equilíbrio das opções

Comando: `python scripts/auditar_aquecimentos_m1.py`. Resultado integral: [OPCOES.json](OPCOES.json).

Conta caracteres visíveis, remove HTML/negrito e normaliza espaços. Usa a amplitude conservadora `(maior - menor) / menor`. Inclui as duas lacunas e as quatro perguntas de escolha/revisão de cada baralho. Conta os empates como certa mais longa.

| Medida | M1-U1 | M1-U2 |
|---|---:|---:|
| Grupos com três opções | 6 | 6 |
| Maior amplitude | 10,00% | 5,72% |
| Certa entre as mais longas, contando empates | 2/6 | 2/6 |
| Certa pelo menos 25% maior do que a maior errada | 0 | 0 |
| Violações | 0 | 0 |

V/F usa os dois rótulos fixos do motor, não opções redigidas para estes baralhos. Emparelhar e ordenar não têm uma alternativa correta concorrente com distratores; as respetivas sequências têm extensão controlada para leitura móvel. A revisão manual verificou pormenor comparável nas alternativas e ausência de uma citação exclusiva na opção certa. As opções da pergunta opcional já existente nas tarefas não foram reescritas nem entram nesta medição.

## 6. Distribuição dos 90 minutos

Nas duas unidades: **10 minutos de cartões com consulta + 5 de apresentação pelo docente + 60 de produção + 15 de revisão e entrega = 90**.

O relógio do aquecimento começa em 10; o da produção e a sua representação no topo começam em 60. Os cinco minutos de apresentação e os quinze finais são orientados pelo docente; não se criou um relógio global novo. O texto do aquecimento e a abertura atual do guia dizem a mesma coisa. As durações antigas dentro do arquivo do guia permanecem documentadas como arquivo, não como instrução da aula atual. As linhas A indicam 10 min; as linhas T mantêm 90 min.

## 7. Testes e resultados

Executados com Python 3.12 em Windows. As dependências de navegador foram instaladas apenas na pasta de trabalho. Um lançador externo ao repositório escolheu o Chromium 149 já instalado; não alterou seletores, asserções, testes percorridos ou comportamento do produto.

| Comando | Resultado |
|---|---|
| `python scripts/aquecimentos.py m1-u1 m1-u2` | Validação e geração aprovadas. |
| `python scripts/tarefas_escolha.py m1-u1 m1-u2` | Duas tarefas regeneradas. |
| `python scripts/auditar_aquecimentos_m1.py` | Código 0; nenhuma violação. |
| `python -m unittest discover -s tests -p test_task_aquecimentos.py` | 13 testes, OK. |
| `python -m unittest discover -s tests -p test_task_choice.py` | 7 testes, OK; o limite de 300 palavras foi mantido. |
| `python -m unittest discover -s tests -p test_aquecimentos_m1_opcoes.py` | 2 testes, OK. |
| `python -m unittest discover -s tests` antes | 308 testes; 461 falhas e 2 erros em test_sala_desligada. |
| O mesmo comando numa cópia limpa de origin/main | Repete 308 testes, 461 falhas e 2 erros. |
| `python -m unittest discover -s tests` depois | 311 testes; 476 falhas e 2 erros. Não aprovado. |
| `python tests/browser_task_aquecimentos.py` | Aprovado: cinco baralhos completos em 390/claro e 1366/escuro; projeção sem gravação; tarefas, percursos e verificações M7 existentes. |
| `python tests/browser_aquecimentos_m1_feedback.py` | Aprovado: os dez cartões ativos de cada baralho, certos e errados, com a explicação esperada visível e sem deslize horizontal a 390 px. |
| `python tests/browser_task_lesson_matrix.py` | Interrompido por timeout de 30 segundos em Page.reload, M7-U1, #apoios; as duas tarefas M1 tinham passado em 390/claro. Não é aprovação da matriz completa. |
| `git diff --check` | Sem erros. |

Saídas: [RESULTADOS-TESTES.txt](RESULTADOS-TESTES.txt). Contém as 15 falhas adicionais completas, todos os identificadores da base e os registos integrais dos três testes de navegador. Os logs completos da suite antes/depois foram conservados na pasta de trabalho, fora do site.

As **15 falhas adicionais** distribuem-se assim: cinco em `test_m1_grammar_pilot`, cinco em `test_m1_unit_tasks`, três em `test_module_layout` e duas em `test_task_reader`. Doze são impedidas pelos hashes dos dados públicos da tarefa; três pelo contrato congelado de texto, ligações e IDs do índice. A camada literal foi conservada. Não se ignorou nenhuma asserção nem se mudou um limite para obter aprovação.

Exemplos da saída:

```text
AssertionError: Public task data differs from its authorization: docs/pedagogia/tarefas-escolha/m1-u1.json
AssertionError: Public task data differs from its authorization: docs/pedagogia/tarefas-escolha/m1-u2.json
FAILED (failures=476, errors=2)
playwright._impl._errors.TimeoutError: Page.reload: Timeout 30000ms exceeded.
```

## 8. Decisões, dúvidas e trabalho por concluir

**Decisões tomadas:** dez minutos para manter o modelo M7-U3; Mendinho como outro texto da U1; casos inventados na U2 para não antecipar os capítulos avaliados; uma única palavra na ligação do enunciado (Aquecer), com duração e explicação no primeiro cartão da tarefa; microedição equivalente cerca de → aproximadamente na U1 para conservar o contrato de 300 palavras. O restante enunciado, temas, dossiê, apoios e critérios foram preservados. As asserções de máquinas em papel que verificam predecessores históricos foram mantidas; acrescentou-se um teste da interface atual em vez de falsificar o passado.

**Revisão dos três júris:**

- Factos: citações literais verificadas; nenhum novo facto histórico; ficções assinaladas; remissão da gradação corrigida para F07.
- Aprendizagem: cartões exercitam identificação, prova, classificação, efeito, inferência, confronto de fontes, criação delimitada e revisão; os textos avaliados ficam para a tarefa.
- Viabilidade: doze cartões, dez ativos, feedback certo/errado e ecrã de 390 px verificados. Dez minutos é uma estimativa pedagógica, não uma duração medida com alunos; confirmar em aula e ajustar a 10–15 minutos se necessário, redistribuindo explicitamente os 90.

**Pedido de decisão ao Claude/docente:** autorizas e assumes a atualização encadeada dos contratos literais para esta alteração já autorizada? Em particular, `tests/fixtures/m1-choice-tasks-20261028.json`, os contratos usados por `tests/task_source_contract.py` e o contrato de índice em `tests/fixtures/module-layout-before.json` / `tests/test_module_layout.py` precisam de tratamento explícito. Não os alterei porque a instrução exclui as camadas literais. A atualização deve preservar os predecessores e conferir o diff exato, sem regenerar cegamente hashes.

É ainda necessário resolver ou reconciliar as 461 falhas e dois erros de base ligados à Sala, diagnosticar o timeout da matriz M7-U1 e voltar a correr a suite e a matriz completas. Estes pontos impedem recomendar merge. A ausência de alterações na M7 não demonstra, por si, que o timeout se reproduz na base; essa comparação não foi executada.

O ramo fica entregue ao Claude para revisão. Não há alteração em produção.
