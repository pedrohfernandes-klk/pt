# M8-F12 — Da identificação à clareza das retomas

Base: main cca9d288070b54e736f571ee2607e1a04f7018f2. Sem sobreposição com PR #80. M8-F06 preservada e nenhum ficheiro de LENTE alterado.

## Diagnóstico e alteração

A mesma pergunta verdadeiro/falso de identificação («Li o conto. Ele surpreendeu-me») aparecia em F06 e F12. Em F06 serve a aprendizagem inicial; F12 já repete o mesmo modelo na leitura essencial e nas lacunas. Mantém-se a recuperação em F06 e no apoio de F12; dois exercícios de F12 passam a aplicar a noção a um problema de escrita.

Exemplo explicitamente inventado: «A poeta conversou com a editora. Ela levou o manuscrito.» O modelo opcional mostra que o pronome pode retomar ambas as pessoas; apontar para trás não resolve por si só a ambiguidade. O cartão9 pede reconhecer o limite da informação. O cartão19 pede explicitar a editora como pessoa pretendida. A tarefa final transfere para a outra leitura, identificando a poeta, e para revisão de uma retoma num texto do aluno.

Apoio distingue clareza num relato informativo de uma incerteza literária a interpretar. Não transforma toda a ambiguidade em erro, nem impõe que os contos expliquem tudo. Os conteúdos e exemplos anteriores da leitura essencial e o fecho foram preservados.

Quatro cartões editados (1,9,19,21), mantendo 22 definições, tipos, índices, resposta falsa do VF, duas lacunas e motor de pontos. Uma cópia do VF no desafio do módulo e rótulos do painel sincronizados. Motor, estilos, IDs, navegação, gravação, encomenda de desenvolvimento e critérios mantidos.

## Fonte de verificação

Luís Filipe Cunha, «Coesão, anáfora», Ciberdúvidas, 24-10-2008: https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/coesao-anafora/24762 . Explica a possibilidade de o antecedente não ser o sujeito anterior e a compatibilidade de género/número. O exemplo de poeta/editora foi criado para esta atividade, não é transcrição da fonte ou de «George».

## Testes

172 testes Python aprovados; validação das estruturas, contexto, conservação da recuperação em F06, paridade com desafio e painel. Código fora dos bancos e tipos dos cartões comparados com a base, sem alterações. git diff --check aprovado.

Percurso normal completo de M8-F12 a 360×800: seleção de 17 cartões, 12 interações. Novo VF incluído; resposta errada intencional recebeu explicação sobre as duas pessoas possíveis. Conclusão e recarregamento conservaram 11/12. Apoios opcionais abertos por Enter e transferência inspecionada.

A seleção normal não incluiu o cartão19. Foi por isso testado numa pré-visualização local temporária, com os mesmos cartões/modelo/motor, apenas três cartões e chave QA separada: duas lacunas respondidas corretamente, feedback e progressão verificados. Isto é teste focalizado e não um segundo percurso integral. A pré-visualização foi removida e não integra a publicação. Modelo inspecionado em computador e telemóvel; largura DOM móvel360 sem transbordamento horizontal.

Pendências complementares: todas as seleções aleatórias e distratores, leitor de ecrã, desempenho medido, transmissão da sala e avaliação de aprendizagem em turma. Estado de CI/publicação registado na entrega. Publicação segue a autorização de testes proporcionais.
