# Português — jogabilidade, repetição e critérios pedagógicos

20 de outubro de 2026. Ramo: `work/jogabilidade-rotacao-20261020`, a partir de `089435c34444b1131e5c51ea9c7f6326290b374f`. Incremento local, sem nova publicação.

## Corrigido e verificado

1. **Cobertura nas novas tentativas.** Um teste determinístico reproduziu uma falha: para evitar repetir o conjunto anterior, o motor podia retirar o único exercício de um grupo pedagógico. A troca só pode agora retirar um item de um grupo ainda representado. Vocabulário obrigatório preservado.
2. **Prioridade aos itens menos apresentados.** Nos bancos com mais de 12 atividades e variação ativa, o motor dá prioridade aos itens menos apresentados nas tentativas concluídas. As leituras permanecem todas, pela ordem original. O contador é local e acrescenta informação aos registos existentes; não elimina notas nem resultados. Abrir apenas o resumo de uma lição já feita não gera um novo baralho.
3. **Teclado e nomes acessíveis.** As palavras do glossário e as etapas clicáveis da linha do tempo respondem a Enter e Espaço, com estado expandido exposto. As lacunas têm nomes como «Lacuna 1 de 2». Aspeto visual preservado.
4. **Revisão completa.** Uma variante anunciava o número total de erros mas mostrava apenas seis. A lista passa a mostrar todos e chama-se «O que rever», evitando afirmar que o aluno aprendeu automaticamente.
5. **Uma versão do motor nas lições e desafios.** Foram encontradas 100 cópias incorporadas nas lições, com apenas duas variantes, e nove cópias nos índices de módulo. Substituídas por referências ao motor comum já existente, na mesma posição e sem alterar a ordem de carregamento. As oito lições que já usavam o ficheiro comum receberam a mesma referência versionada. Não foram alterados os motores específicos das experiências complementares autónomas.

## Conteúdos e pedagogia

Os bancos das 108 lições foram comparados antes e depois: todos os 2506 cartões foram preservados. Nenhum exercício foi acrescentado para aumentar a contagem. O inventário contém 708 cartões de leitura/exploração e 1798 atividades interativas.

Foram formalizados critérios de orientação, esquema, exemplo analisado, prova textual, prática, feedback e transferência, articulados com proximidade, semelhança, continuidade, região comum e figura/fundo. O documento distingue utilização em aula de estudo autónomo e variedade de interface de variedade cognitiva. Não certifica o cumprimento integral desses critérios em cada lição.

O levantamento encontrou 100 cartões com o rótulo «O essencial», 74 «Em paralelo» e 61 «Para entender». A ausência desses rótulos nas experiências com estrutura diferente não demonstra, por si só, uma lacuna. Não foi feita neste incremento uma reescrita dos esquemas ou uma nova revisão interpretativa integral.

## Evidência

- 60 testes Python passaram.
- Teste determinístico da rotação: falha reproduzida antes da correção; cobertura dos grupos, seleção diferente, prioridade aos itens não apresentados e respeito por bancos fixos verificados depois.
- Chromium a 320 e 1440 px: duas tentativas concluídas; conservação dos grupos e acesso aos 13 itens do banco de teste nas duas tentativas; contadores locais; lista completa de erros; teclado no glossário e na linha do tempo; nomes das lacunas.
- Chromium: as 108 lições abrem a 320 e 1440 px; nove percursos completos prioritários com recuperação do progresso; cartões trovador/jogral/segrel e feedback contextual corrigido.
- Chromium: índices dos nove módulos, cobertura dos desafios, ambos os desafios de M2 concluídos, registos anteriores e complementos preservados.
- Projeção de M1-F01: carregamento pelo painel existente, passagem ao cartão seguinte e tamanho grande confirmados.
- Auditorias de sintaxe, cartões e progressão sem erros reportados. Testes novos incluídos na integração contínua para futura PR.

## Limites e próximos pontos editoriais

Há sete bancos pequenos em que a seleção de itens não roda: M2-F12/F13, M3-F18, M6-F12/F13 e M9-F11/F12. Mantêm os seus itens. Reformular a pergunta ou baralhar opções não equivale a introduzir um exemplo novo; não foi prometido um problema inédito em todas as tentativas.

A seleção por grupos e frequência não modela todas as dependências semânticas entre exercícios. Os bancos explicitamente fixos continuam fixos. A necessidade de novas situações, exemplos e formatos deve ser confirmada pela leitura pedagógica, não deduzida apenas das contagens.

Não foi feita uma certificação de ausência de falhas em todos os dispositivos, revisão integral com leitor de ecrã ou demonstração de aprendizagem com alunos. A revisão qualitativa dos 1798 exercícios, das ambiguidades e da autonomia dos materiais continua a ser trabalho contextual, por lotes. Os motores das páginas complementares autónomas continuam por confrontar com estas melhorias. Nada foi publicado neste incremento.

## Ficheiros de apoio

- `inventario-108-licoes.csv`: tipos, variantes de pergunta e campos de feedback por lição; são sinais estruturais, não classificações de qualidade.
- `cartoes-preservados.json`: comparação dos bancos e impressão digital dos cartões.
- `criterios-pedagogicos.md`: critérios editoriais e de interação.
- `alteracoes.patch`: diff do incremento.
