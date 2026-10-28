# M1: aulas de tarefa no formato com escolha e grelhas sem soluções (28/10/2026)

## O que mudou

- **As duas aulas de tarefa do M1** (`tarefas/m1-u1/`, `tarefas/m1-u2/`) passam ao formato do piloto do M2: aquecer (15 min, em papel, sem consultar, com as duas máquinas do exame), enunciado com núcleo comum e tema A ou B, relembrar (com o dossiê do tema B) e verificar. O relógio do aluno marca o aquecimento (até 15 min) e a produção (até 60 min).
- **Texto das tarefas:** escrito por uma autora, revisto por um verificador e por uma head copy. Na integração, a unidade 2 foi encurtada para caber no limite do formato (cabeçalho e «O que conta» até 300 palavras): o lead junta os pedidos comuns da crónica, o núcleo 2 e os temas ficam mais curtos, a nota sobre as 250 a 300 palavras da aula 13 e a segunda fonte do plano dessa aula passam para «Relembrar», e o fecho diz que fica fora da contagem. Saem duas pistas que davam respostas em páginas públicas: «a síncope nomeada» em «O que conta» (unidade 2) e «(a ironia)» em «Relembrar» (unidade 1).
- **Gerador:** `scripts/tarefas_escolha.py`, com os dados em `docs/pedagogia/tarefas-escolha/<slug>.json`. Os dados guardam só o que a página publica: a grelha e a chave da correção não entram. O gerador escreve a ligação à grelha igual à de `scripts/grelhas_tarefas.py`, e os dois podem correr por qualquer ordem.
- **Grelhas /20** (`tarefas/m1-u*/grelha/` e `/correcao/`): refeitas a partir das tarefas novas, com os mesmos cinco critérios a somar 20 (unidade 1: 4 + 3 + 4 + 6 + 3; unidade 2: 3 + 3 + 5 + 5 + 4) e os três níveis. Cada página do aluno diz, numa nota, de onde vêm os exemplos.
- **Índice e guia do M1:** os cartões das tarefas dizem «trabalho em papel», como no M2, e o guia diz «Escreves em papel».
- **Testes:** `test_task_choice.py` cobre o M1 (citações do aquecimento nas lições, factos do dossiê na lição para onde apontam, nomes de «Relembrar» nas lições ligadas, gerador idempotente); o contrato compacto deixa o M1, cujo corpo novo fica autorizado em `tests/fixtures/m1-choice-tasks-20261028.json`, encadeado no corpo compacto de 27/10; `test_task_grelhas.py` proíbe nas grelhas as cadeias tiradas da chave e confere as citações dos exemplos; os testes de navegador conhecem o M1 no formato com escolha e medem as grelhas em claro, em escuro e na impressão.

## A regra das grelhas (28/10/2026)

A grelha do aluno e a versão de correção são páginas públicas. Por isso:

- **Nenhum descritor nem exemplo responde à tarefa.** Os descritores dizem o que se avalia em termos gerais (por exemplo, «dizes o som que cai, o lugar na palavra e o nome do processo»), sem a resposta.
- **Os exemplos mostram a qualidade com outro caso do mesmo tipo:** outra palavra (*luna* > lua, *lupum* > lobo), outra cantiga (D. Dinis, «Ai flores»; Mendinho), outra frase (as da lição sobre a ironia), outra imagem (a gravura de D. Dinis), outro lugar (uma manhã na escola). Nunca as palavras, as passagens, o recurso ou os factos com que a tarefa se responde, nem material que o aluno pudesse copiar para o seu tema.
- **A chave completa** (respostas esperadas, versão da grelha com as respostas, fonte de cada citação) fica fora do repositório, com o docente.
- **Teste:** cada tarefa tem, em `tests/test_task_grelhas.py`, uma lista de cadeias proibidas tiradas da chave. Quem mudar uma grelha tem de a manter limpa; quem mudar a tarefa revê a lista.

## Por validar em sala

O tempo do aquecimento, a escolha entre A e B e se a unidade 2, mais curta no enunciado, continua clara sem o docente a explicar os pedidos comuns da crónica.
