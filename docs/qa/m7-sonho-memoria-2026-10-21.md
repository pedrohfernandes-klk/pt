# M7 — sonho, memória e prova textual

Revisão local de M7-F14 e M7-F15, em 21 de outubro de 2026. Base local: 348ea300. A main remota foi confirmada em bc8bd6232f08f25a765a2091748d20d9fee89716. Este bloco não foi publicado; também permanecem locais as alterações anteriores de M2-F06/F11, no commit 348ea300.

## Problemas verificados e correções

- **F14: contexto e progressão.** A imagem inicial documenta outro poema, «Tabacaria»; uma nota torna explícita essa função. O esquema acompanha agora a passagem da ilha desejada à dúvida, ao desencanto e à formulação «em nós». Evita classificar automaticamente «nesta terra», na terceira estrofe, como interior do sujeito. A síntese admite leituras sustentadas e pede um indício que dificulte a hipótese escolhida.
- **F15: perceção e interpretação.** Ouvir as crianças não demonstra que o sujeito não as vê. A explicação e o feedback distinguem a perceção nomeada dessa inferência. «Que não tive» é uma formulação da voz do poema, não prova documental da infância de Fernando Pessoa. O presente surge como desejo em «sinta», sem se impor uma felicidade já alcançada.
- **Prova e revisão.** Cada ficha substitui uma pergunta por uma atividade de revisão de frase: comparar alternativas, observar a mudança e confirmar depois. Os distratores têm feedback específico; a tentativa pode ser repetida através do motor existente. As atividades estão também nos desafios do módulo e nos painéis do professor.
- **Gramática com função.** F15 distingue a imagem «onda de alegria» de um exemplo expressamente inventado de imitação sonora, «tiquetaque». Mantém as definições e os exemplos de formação de palavras existentes.

## Preservação

F14 conserva 23 cartões e F15 conserva 21. Os cartões dos poemas mantêm-se integralmente iguais à base local; as imagens de abertura permanecem visíveis e conservam as mesmas fontes. Não foram criadas lições nem alterados os motores partilhados. Não foi necessária migração dos índices de progresso.

## Verificação realizada

- 87 testes Python aprovados, incluindo cinco regressões específicas deste bloco.
- Auditoria de 108 lições: 2509 cartões, dos quais 710 de leitura e 1799 interativos; sem erros reportados.
- Navegador a 320 e 1280 píxeis: percurso pelos 44 cartões, feedback de todas as opções erradas das novas atividades, alteração reversível antes de confirmar e repetição dos erros com resposta correta.
- Duas tentativas normais por ficha e largura, com verificação de conclusão e persistência do progresso após recarregar.
- Verificação do exercício no contexto dos desafios e em projeção; sem transbordo horizontal nos cenários ensaiados.
- Verificações existentes de rotação e do catálogo de exame aprovadas. Comparação automática dos poemas e imagens com a base local.
- A última afinação do esquema de F14 foi validada pelos testes estáticos; a bateria de navegador antecede essa afinação textual, que não alterou a mecânica.

Evidências nesta pasta: qa.json, preservacao.json, diff-conteudos.json, progressao.txt e capturas. A rotina de navegador foi integrada no fluxo de testes do repositório.

## Limites e pendências

Esta revisão cobre duas fichas, não constitui uma nova auditoria integral de M1–M9. Não foram medidos resultados de aprendizagem nem feitas sessões com alunos, revisão com leitor de ecrã, comparação de edições dos poemas ou revisão audiovisual. Os conteúdos foram confrontados com os poemas já presentes nas fichas. Não foram acrescentados vídeos ou alteradas sessões de exame neste bloco. Publicação pendente de autorização para estas alterações locais.
