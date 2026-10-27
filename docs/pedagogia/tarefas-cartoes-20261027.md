# Aulas de tarefa em cartões — 27/10/2026

Base exata: `68958382`. Trabalho isolado em `work/pt-tarefas-cartoes-20261027`.

## Implementação

As oito tarefas canónicas carregam `assets/pt-lessons/lesson.css`, o controlador existente `EPICasca.pagina` de `casca.js` e o novo adaptador `task-reader.js`. O CSS do adaptador limita-se à composição desta página; não introduz cores nem altera os motores ou os tokens de aparência.

A página HTML completa permanece no documento como alternativa sem JavaScript. Quando o adaptador carrega, cria a estrutura normal da casca e desloca os nós existentes para cartões: abertura, eventuais pré-requisitos, preparação e modelo, quatro perguntas separadas, apoios, produção e entrega. Não se reescrevem as perguntas ou o feedback com `innerHTML`, nem se clonam botões. Os listeners de `task-90.js` ficam nos mesmos nós.

O adaptador usa `C.num`, `C.barra`, `C.acoes`, `C.menu`, `C.rolarTopo` e `C.sombra`. A barra é um índice de consulta, sem pontuação, bloqueio ou avaliação. Todos os cartões são acessíveis logo no início pelo menu. Ações de anterior/seguinte e teclas de navegação permitem mudar de cartão; as perguntas não condicionam a passagem.

Só um cartão se apresenta de cada vez. O corpo da casca permite deslocação interna quando a leitura é longa. Não há uma segunda página infinita por trás. Ligações como `#apoios`, `#criterios` e os identificadores existentes de cada apoio revelam o respetivo cartão e abrem os detalhes necessários. Nas perguntas, «Consultar apoios» e «Voltar à pergunta» conservam a escolha e o feedback já explorados.

A impressão apresenta todos os cartões e abre os detalhes temporariamente, restaurando o estado de leitura no regresso. Se o adaptador não carregar, a página original permanece legível; se a inicialização falhar depois de mover nós, o registo das posições permite repor os mesmos nós no documento original.

Não se acrescentam chaves de armazenamento, notas nem conclusão automática. O conteúdo, identificadores, URLs, critérios, quatro perguntas, tempo de 90 minutos e consulta mantêm-se.

## Tratamento por tu

Apenas M4-U1 precisava de correção de imperativos instrucionais. Agora usa «Com o teu grupo de 2 ou 3, escolhe…», «Compara…», «Abre este apoio apenas se precisares…» e equivalentes no restante guião. Conserva o trabalho de grupo, todos os participantes na fala, os produtos, a duração, as citações e os critérios transcritos.

A fixture `tests/fixtures/task-reader-before.json` foi derivada da base exata. Nos outros sete documentos, o corpo original tem de permanecer idêntico. Em M4-U1, a comparação aplica exclusivamente a lista explícita de correções para tu. Critérios, citações, identificadores e ligações são conferidos separadamente.

## Validação e CI

A matriz completa está no driver independente `tests/browser_task_lesson_matrix.py`, preparado para o job paralelo da CI. A workflow não foi alterada nesta frente. O percurso geral continua a verificar os três índices, arquivo e progresso, mas abre apenas uma tarefa por módulo; não executa adicionalmente os 32 estados responsivos.

O driver dedicado cobre as oito tarefas em 390 e 1366 px, nos dois temas, exigindo a largura real. Navega pelo índice com teclado antes das quatro perguntas; explora as três opções de cada uma; testa consulta e regresso à pergunta sem perder feedback; verifica hashes, detalhes, deslocação própria da leitura, impressão completa, boia, projeção e ausência de escritas de avaliação. Inclui ainda as oito páginas com o carregamento do adaptador bloqueado para verificar a alternativa legível e o feedback original.

Foram executados os testes Python e a verificação de sintaxe Node, sem executar Playwright localmente. A validação visual e a matriz browser dependem da revisão do pai e da CI; este documento não certifica mobile sem essa execução.
