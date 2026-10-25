# M4 — auditoria de paridade após integração do PR #80

25-10-2026. Main atual verificado: `b72521542aa06c261708e3f6034438f97cdd5723`, após integração do #80 e do Atlas #94. Pages desse main terminou com sucesso. Esta entrega não altera lições, painéis, desafios, guiões, projeção ou progresso de M4.

## Estado atual confirmado

Foi recolhido um snapshot dos treze painéis no SHA indicado, por leitura do GitHub. Os blobs das dezasseis páginas de lição foram comparados com a árvore desse main e coincidem com as páginas locais usadas como fonte dos cartões. O auditor executado no snapshot confirmou **12 bancos/98 seleções alinhados**. F25/F26/F27 continuam sem painel dedicado e F28 é um guião editorial: são quatro situações não certificadas pelo auditor, não defeitos automaticamente demonstrados.

O patch mínimo anexado na primeira versão do #92 foi retirado depois de o #80 integrar as correções. Não reaplicar esse patch: os onze painéis já estão corrigidos no main. O #92 passa a conter só auditor, testes e relatório. O envio desta atualização ainda aguarda disponibilidade da revisão de aprovação; não se declara integrado no GitHub.

## Diagnóstico histórico dos painéis — base af75f744

| Situação | Quantidade |
|---|---:|
| Lições examinadas |16|
| Painéis com banco desatualizado |11|
| Painel com banco alinhado (F20) |1|
| Lições sem painel dedicado (F25/F26/F27) |3|
| Painel editorial, sem banco de sala (F28) |1|

Nos 11 bancos antigos, 192 seleções:52 apontam para índices inválidos,75 para cartões de leitura e65 para perguntas/tipos diferentes. Não há uma seleção alinhada nesses 11 bancos. F20 acrescenta10 seleções alinhadas. A falta de painel dedicado e a existência de um guião editorial não são automaticamente defeitos de navegação: é necessário verificar os acessos anunciados e o papel pretendido.

Os onze painéis foram corrigidos pelo responsável por M1/M4 no PR #80. A comparação depois da integração confirma os doze bancos alinhados (98 seleções, incluindo F20). Os números da tabela e os 192 desencontros acima pertencem à base anterior. Isto verifica correspondência de dados, não certificação pedagógica de todas as respostas nem do transporte entre aparelhos.

### Reprodução real em F07

O painel publicado usa índices antigos. Em duas páginas locais com `?local=1`, foi criada sala fictícia e usado apenas BroadcastChannel, sem envio ao ntfy.sh. O docente selecionou «Põe pela ordem da peça: o pai, a morte, a honra, as tochas» (índice4), mas o aluno recebeu «Corta tranquilamente e lê a fala aos gritos. O que se perde?», a pergunta atual desse índice. É desencontro funcional, não apenas diferença de rótulo.

Numa cópia temporária do painel do PR #80, no mesmo canal local, foi selecionada a pergunta correta. Painel e aluno mostraram o mesmo enunciado; a opção correta, feedback e retorno ao docente foram verificados. A cópia foi removida e não integra esta entrega. Não foram testados todos os98 controlos no navegador, nem ntfy.sh, redes/dispositivos distintos, QR físico, pausas, votação ou acessibilidade por leitor de ecrã.

## Desafios: diagnóstico pedagógico independente, não encerrado pela paridade

Auditoria de leitura em paralelo:170 itens distribuídos pelas16 lições,132 questões atuais. Não há identificador de lição órfão no banco. Só7 enunciados são iguais literalmente; isso não significa que os163 restantes estejam errados. Foram lidos em profundidade F07, F28 e os casos identificados abaixo, não os170 gabaritos de forma exaustiva.

- **F07, unidade2 pool[5]:** exige que as didascálias estejam «entre parênteses», mas a lição atual ensina o exemplo junto ao nome «MANUEL, tranquilamente». Conflito concreto de conceito e gabarito.
- **F07:** os11 itens do desafio não avaliam a função de presságio do retrato nem a distinção presságio/revelação/desgraça, trabalhada em3 das7 questões atuais. Identificar de quem é o retrato não substitui interpretar a função.
- **F28, unidade2 pool[50] e [52]:** perguntas sobre «exemplo inventado» e «essas duas hipóteses» perderam os cenários ao serem copiadas. O sorteio não transporta a leitura anterior; o atributo de grupo não injeta esse contexto.
- **F20, unidade2 pool[14]:** variante refere duas horas e a principal90 minutos, ambas durações hipotéticas. Não altera a classificação, mas é uma divergência evitável.
- **F15, unidade1 pool[63]:** a inferência de «Portanto os homens falam» depende de um parágrafo que não acompanha a questão. É dependência contextual a rever, não gabarito automaticamente falso.
- **F26/F27:** lacunas de cobertura das operações de ironia dramática e comparação fundamentada; exigem segundo lote, sem declarar todas as perguntas existentes obsoletas.

Estes casos incidem em `m4/index.html`. Não foram alterados por esta auditoria, nem foi repetida integralmente a revisão pedagógica após o #80. O responsável por M4 deve reconfirmar o desafio atual e tratar os casos em lote próprio. Não os declarar resolvidos só porque os painéis alinham.

## Entrega técnica de leitura

`scripts/audit_teacher_parity.py` não escreve em páginas. Compara seleções com o banco atual, distingue índice inválido, leitura e pergunta diferente, regista opções/gabarito/feedback e uma impressão SHA256 do cartão resolvido. Um ref Git local pode fornecer os painéis sem checkout ou fallback silencioso. Ausência de painel e guia editorial permanecem não certificados. Um resultado alinhado não prova validade pedagógica.

Reprodução:

    python scripts/audit_teacher_parity.py --modules m4 --output paineis-main.json
    python scripts/audit_teacher_parity.py --modules m4 --panel-ref 7902be396ddddd272a57e9c50450de74987a0a34 --output paineis-pr80.json

Na base histórica, ambos devolviam código 1: no main havia desencontros e quatro situações não certificadas; na proposta subsistiam as três páginas sem painel e o guião editorial. No main posterior ao #80, o primeiro comando continua a devolver 1 só pelas quatro situações não certificadas. O código não significa falha dos testes do auditor nem obrigação de substituir o guião por um painel. Executar o primeiro comando numa base que já inclua o #80; o segundo conserva apenas valor de comparação histórica.

## Integração delimitada após coordenação

O patch `m4-paineis-proposta-nao-aplicada-20261025.patch` foi retirado desta entrega porque a correção já veio pelo #80. Era um artefacto de engenharia, não conteúdo pedagógico. Não criar outra implementação concorrente dos painéis. O #92 integra apenas ferramenta, quatro testes e relatório atualizado.

M1 foi integrado pelo responsável. M7 continua reservado ao Claude; não equiparar a conclusão do M1 à do M7. A cobertura pedagógica dos desafios M4 também permanece com o responsável por M4.

Um lote próprio de desafio pode confirmar/corrigir a definição, cobertura de presságio, cenários de F28 e duração hipotética de F20. Documentar conteúdos preservados e efeito das substituições; ensaiar variantes isoladas e uma tentativa normal de oito questões. Não implementar por esta conversa sobre ficheiros reservados ao Claude.

## Testes e limites

178 testes Python aprovados na branch desta auditoria, incluindo quatro do auditor (identidade de resposta/feedback, índices negativos e fora do banco, alvo de leitura, rótulo/tipo desviado, painel ausente/editorial e módulo vazio). Comparação adicional do snapshot posterior ao #80 executada com 12 bancos/98 seleções alinhados. Resultados completos e identidade do snapshot guardados na entrega local. Nenhum ficheiro M4 alterado por esta entrega. O CI final deve verificar a combinação com o main atual; a suite local anterior não é esse ensaio combinado. A sessão real foi apenas local/F07 antes da integração; não foi repetida em sala pública depois do #80. Guiões/diapositivos/projeção não foram integralmente certificados. O #92 não é uma nova publicação funcional: as correções dos painéis vieram pelo #80 e as pendências pedagógicas continuam separadas.
