# M4 — auditoria operacional e proposta não aplicada

Referência publicada examinada: af75f7441bb4f28060d5672bb2c199be4ff74654 (25-10-2026). PR concorrente protegido: #80, head7902be396ddddd272a57e9c50450de74987a0a34. Esta entrega não altera lições, painéis, desafios, guiões, projeção ou progresso de M4. O último lote anterior (#91) terminou a regressão geral com sucesso.

## Resultado dos painéis

| Situação | Quantidade |
|---|---:|
| Lições examinadas |16|
| Painéis com banco desatualizado |11|
| Painel com banco alinhado (F20) |1|
| Lições sem painel dedicado (F25/F26/F27) |3|
| Painel editorial, sem banco de sala (F28) |1|

Nos 11 bancos antigos, 192 seleções:52 apontam para índices inválidos,75 para cartões de leitura e65 para perguntas/tipos diferentes. Não há uma seleção alinhada nesses 11 bancos. F20 acrescenta10 seleções alinhadas. A falta de painel dedicado e a existência de um guião editorial não são automaticamente defeitos de navegação: é necessário verificar os acessos anunciados e o papel pretendido.

Os 11 painéis estão todos alterados no PR #80. Comparados os bancos desse PR com as lições atuais, os12 painéis com banco ficam alinhados (98 seleções, incluindo F20). Isto verifica a correspondência de dados, não uma certificação pedagógica de todas as respostas ou do transporte entre aparelhos.

### Reprodução real em F07

O painel publicado usa índices antigos. Em duas páginas locais com `?local=1`, foi criada sala fictícia e usado apenas BroadcastChannel, sem envio ao ntfy.sh. O docente selecionou «Põe pela ordem da peça: o pai, a morte, a honra, as tochas» (índice4), mas o aluno recebeu «Corta tranquilamente e lê a fala aos gritos. O que se perde?», a pergunta atual desse índice. É desencontro funcional, não apenas diferença de rótulo.

Numa cópia temporária do painel do PR #80, no mesmo canal local, foi selecionada a pergunta correta. Painel e aluno mostraram o mesmo enunciado; a opção correta, feedback e retorno ao docente foram verificados. A cópia foi removida e não integra esta entrega. Não foram testados todos os98 controlos no navegador, nem ntfy.sh, redes/dispositivos distintos, QR físico, pausas, votação ou acessibilidade por leitor de ecrã.

## Desafios: diagnóstico pedagógico independente

Auditoria de leitura em paralelo:170 itens distribuídos pelas16 lições,132 questões atuais. Não há identificador de lição órfão no banco. Só7 enunciados são iguais literalmente; isso não significa que os163 restantes estejam errados. Foram lidos em profundidade F07, F28 e os casos identificados abaixo, não os170 gabaritos de forma exaustiva.

- **F07, unidade2 pool[5]:** exige que as didascálias estejam «entre parênteses», mas a lição atual ensina o exemplo junto ao nome «MANUEL, tranquilamente». Conflito concreto de conceito e gabarito.
- **F07:** os11 itens do desafio não avaliam a função de presságio do retrato nem a distinção presságio/revelação/desgraça, trabalhada em3 das7 questões atuais. Identificar de quem é o retrato não substitui interpretar a função.
- **F28, unidade2 pool[50] e [52]:** perguntas sobre «exemplo inventado» e «essas duas hipóteses» perderam os cenários ao serem copiadas. O sorteio não transporta a leitura anterior; o atributo de grupo não injeta esse contexto.
- **F20, unidade2 pool[14]:** variante refere duas horas e a principal90 minutos, ambas durações hipotéticas. Não altera a classificação, mas é uma divergência evitável.
- **F15, unidade1 pool[63]:** a inferência de «Portanto os homens falam» depende de um parágrafo que não acompanha a questão. É dependência contextual a rever, não gabarito automaticamente falso.
- **F26/F27:** lacunas de cobertura das operações de ironia dramática e comparação fundamentada; exigem segundo lote, sem declarar todas as perguntas existentes obsoletas.

Todos estes casos do desafio incidem em `m4/index.html`, também alterado no PR #80. Não foram aplicadas alterações nesse ficheiro.

## Entrega técnica de leitura

`scripts/audit_teacher_parity.py` não escreve em páginas. Compara seleções com o banco atual, distingue índice inválido, leitura e pergunta diferente, regista opções/gabarito/feedback e uma impressão SHA256 do cartão resolvido. Um ref Git local pode fornecer os painéis sem checkout ou fallback silencioso. Ausência de painel e guia editorial permanecem não certificados. Um resultado alinhado não prova validade pedagógica.

Reprodução:

    python scripts/audit_teacher_parity.py --modules m4 --output paineis-main.json
    python scripts/audit_teacher_parity.py --modules m4 --panel-ref 7902be396ddddd272a57e9c50450de74987a0a34 --output paineis-pr80.json

Ambos devolvem código1 neste snapshot: no main existem desencontros e quatro situações não certificadas; na proposta subsistem as três páginas sem painel e o painel editorial. O código1 não representa uma falha da implementação do auditor nem uma certificação de que um guião editorial esteja errado.

## Proposta concreta e conflito

O ficheiro `m4-paineis-proposta-nao-aplicada-20261025.patch` propõe apenas sincronizar bancos e seletores dos11 painéis, preservando código e estilos de main. **Não está aplicado.** A pré-visualização de navegador testou o painel completo do PR #80; o patch mínimo tem validação estática de aplicação, não certificação de todas as interações.

Antes de aplicar ou abrir outro lote de painéis, coordenar a separação dessas correções do PR #80 ou integrar o lote que as contém. Não criar duas implementações concorrentes. Não equiparar M1 preparado a M7 concluído.

Depois, um lote de desafio limitado pode corrigir a definição, acrescentar cobertura de presságio por substituição editorial justificada, restaurar dois cenários de F28 e alinhar a duração hipotética de F20. Os conteúdos preservados e o efeito de cada substituição têm de ser documentados. Ensaiar as variantes isoladas e uma tentativa normal de oito questões. Não implementar este lote sobre o mesmo ficheiro enquanto o conflito estiver aberto.

## Testes e limites

178 testes Python aprovados, incluindo quatro testes novos do auditor (identidade de resposta/feedback, índices negativos e fora do banco, alvo de leitura, rótulo/tipo desviado, painel ausente/editorial e módulo vazio). Auditor executado em main e com os painéis do PR #80; resultados completos guardados na entrega local. Nenhum ficheiro M4 alterado. A verificação real de sala foi apenas local e apenas F07. Guiões/diapositivos/projeção não foram integralmente certificados. Esta auditoria não resolve nem publica as correções P0: torna o problema, a proposta existente e os limites verificáveis.
