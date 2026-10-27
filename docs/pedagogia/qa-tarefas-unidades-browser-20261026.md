# QA das aulas de tarefa — M1, M4 e M7 — 26/10/2026

## Decisão de contrato

Uma tarefa é a aula de encerramento da unidade. A síntese de duas linhas integra o trabalho dessa aula. Não há um desafio obrigatório, uma síntese a registar ou um cartão do percurso depois da tarefa. As lições anteriores, a sua ordem, os enunciados e as chaves de progresso mantêm-se.

Os desafios antigos continuam disponíveis apenas no arquivo facultativo, acessível pela boia de materiais do docente. A prática do arquivo usa as chaves anteriores: `desafio-M4-uN` em M4 e `desafio-unidade-v2-M1-uN` / `desafio-unidade-v2-M7-uN` nos outros dois módulos. Não conclui nem avalia a aula de tarefa.

A boia também reúne os guiões, as tarefas e critérios e o portefólio. Os blocos de ligações opcionais e os slots do carrossel foram deslocados integralmente para o arquivo. Os slots têm `data-cartaz-archive`: a navegação normal não os monta. A ativação só ocorre na abertura expressa do arquivo.

## Testes browser da CI auditados

Foram identificados os 29 ficheiros distintos invocados como testes browser em `.github/workflows/pt-m1-qa.yml`. As chamadas repetidas de revisão continuam na workflow. A workflow não foi reduzida nem foram retirados testes.

Os contratos alterados são:

- `browser_unit_routes.py`: verifica as oito aulas de tarefa por navegação real, a posição no fim da unidade, a ordem das lições, os quatro exercícios de preparação e o feedback de cada opção. Verifica também o arquivo opcional, as chaves antigas e a cobertura das lições nos pools. Os contratos dos outros seis módulos permanecem.
- `browser_task_contract.py`: auxiliar partilhado sem lançamento de browser. Valida os relógios 10/10/60/10, a consulta, a síntese na mesma aula, a entrega no Teams, o acesso por teclado, o estado dos botões, a correspondência entre feedback e opção e a ausência de escritas de avaliação no armazenamento.
- `browser_unit_synthesis.py`: conserva os testes completos de M2. Em M1/M4/M7 verifica a ausência do registo separado e de migração automática para avaliação; lê respostas e sínteses históricas sem alterar os valores. Inclui o registo da antiga quinta etapa de M7 e a exibição segura de texto semelhante a HTML.
- `browser_unit_support.py`: mantém o inventário de mapas, guias e portefólios dos nove módulos. Nos três guias alterados verifica as ligações atuais, o arquivo fechado e a sua abertura pelo teclado.
- `browser_ux06_pt.py`: mantém os percursos reais início → módulo → primeira lição → segunda lição → unidade, o modo escuro, o foco e a ampliação do texto. Aceita a ação de continuação correta nos módulos com adaptador, retira a expectativa de passaporte em M7 e substitui os antigos gates de M1 pela navegação para a lição seguinte e para a tarefa.
- `browser_m4_tpc.py`: mantém a sequência original de dezoito entradas numeradas de leitura/preparação e acrescenta a verificação das três linhas de tarefa. O destino da unidade 3 é «Discurso no abrigo». O percurso posterior das lições e respetivo feedback mantém-se integral.

`browser_m1_and_inventory.py` não precisava de alteração: continua a verificar as 109 páginas de lições a duas larguras, os percursos completos, recarregamento, chaves e feedback específico. Os restantes testes ligados a lições de M1/M4/M7 também não dependem dos controlos de fecho retirados e foram mantidos.

## Fixtures e portabilidade entre Windows e Linux

`task-route-lesson-content-before.json` conserva o contrato anterior à integração: ordem e configuração das lições, pools e conteúdos de todas as páginas de lição e exercícios longos abrangidos. Os hashes dos ficheiros foram derivados diretamente dos blobs de `7163b603`, nunca regenerados a partir das páginas atuais.

A única normalização dos conteúdos é a conversão das terminações de linha para LF. O teste lê o texto em UTF-8 com a conversão universal de novas linhas e volta a codificá-lo em UTF-8 para o hash. Assim, o checkout CRLF do Windows e o checkout LF da CI Linux produzem o mesmo resultado. Não se remove espaço, não se altera a grafia e não se analisa ou minifica o HTML para esse cálculo.

A minificação e a formatação dos documentos de lição permanecem inalteradas. Não é preciso reformatar ficheiros para corrigir um contrato de navegação. Os pools mantêm o seu hash estrutural de JSON, com ordenação das chaves apenas para a comparação, sem reescrever o objeto original.

`module-layout-before.json` é a fixture de apresentação dos índices. Apenas as expectativas de M1/M4/M7 foram atualizadas para as alterações expressamente autorizadas: aulas de tarefa no percurso, fecho sem gates separados, arquivo e boia. Imagens, lições e restantes módulos continuam cobertos. Esta atualização não substitui a fixture independente do conteúdo original das lições.

## Validação executada nesta revisão

Foi analisada a sintaxe dos 29 pontos de entrada browser e do novo auxiliar, sem executar Playwright nem lançar um browser. Verificou-se também a estrutura HTML e unicidade de identificadores dos três índices, o estado inerte dos slots de carrossel e o teste de execução isolado do adaptador JavaScript.

Os testes browser serão executados pela plataforma de CI. Esta revisão não apresenta a inspeção de sintaxe como execução dos percursos browser.

A suite Python completa passou: 213 testes. O teste isolado de execução do adaptador também passou. Os cenários de browser novos foram apenas inspecionados e analisados sintaticamente nesta frente, conforme a separação de trabalho com a revisão visual.

## Complemento: paleta e contrato responsivo

A paleta autorizada foi integrada apenas nos dois CSS de módulo e tarefa. As ligações a esses CSS nos nove índices e nas nove páginas de tarefa (incluindo o apoio comparativo antigo) usam a versão de cache `20261026-mostarda-1`. O corpo de cada documento foi comparado antes/depois e mantém-se idêntico nesta atualização. Os scripts e os assets de aparência não mudam.

A fixture de apresentação não precisou de atualização por causa da versão de cache: já compara o texto visível, as ligações de navegação, as imagens, os identificadores e os scripts; as queries de `<link rel="stylesheet">` não fazem parte desses valores. Não se alteraram hashes para fazer passar uma alteração de cores.

A CI executará a matriz das oito tarefas com larguras reais de 390 e 1366 px, em claro e noturno: 32 combinações. O teste exige que `innerWidth` seja exatamente a largura pedida, confirma o esquema em `matchMedia`, exercita todas as opções e respetivo feedback, as âncoras por teclado, a boia e o lançamento real de projeção com a tarefa dentro do iframe. Também verifica a ausência de overflow e de escritas de avaliação automática.

A revisão visual do pai confirmou o funcionamento das oito tarefas no desktop. A tentativa de reduzir a largura na ferramenta de revisão visual manteve `innerWidth` em 1280 px; por isso não certifica o comportamento mobile. A certificação mobile fica dependente da execução efetiva desta matriz na CI. Nesta frente não foi executado Playwright localmente.

Após este complemento, a suite Python completa passou com 214 testes. A continuidade dos dois rótulos de tarefa foi corrigida por instrução da revisão: M1-U2 «Crónica “Estar lá”» e M4-U1 «Um peixe de hoje», sem alterar os títulos nem os enunciados das lições. Apenas os hashes de texto e scripts dos índices M1/M4 foram ajustados para estes rótulos autorizados; a fixture do conteúdo original das lições mantém-se.
