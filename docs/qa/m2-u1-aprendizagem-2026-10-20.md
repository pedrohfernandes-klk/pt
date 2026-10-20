# M2 — Unidade 1: aprendizagem com evidência, retoma e transferência

**Data:** 20-10-2026. **Âmbito:** M2-F01, F02 e F07. **Estado:** ramo de revisão, sem integração nem publicação.
Referência estrutural: docs/pedagogia/arquitetura-aprendizagem.md e m2-u1-progressao.json.

## Hipótese pedagógica

A unidade parte da rubrica inicial (quem fala e em que situação), atravessa a fala de Inês e o juízo da Mãe (o que o texto confirma, o que é interpretação de uma personagem) e chega à relação entre orações (o que os conectores fazem num contexto). O aluno deve apontar uma prova, rever uma inferência e transportar o procedimento para frases que não pertençam à farsa.

Não se criou outra unidade nem se substituíram as lições por «fichas de ligação». Os conteúdos e o design existentes continuam a ser a estrutura principal. Retomas e projeções para a ficha seguinte são breves e integradas no texto dos cartões.

## Alterações editoriais

| Ficha | Alteração | Operação visada |
| --- | --- | --- |
| F01 | Feedback específico para as três alternativas erradas em «este motivo» (cartão 10) | separar ocasião, acusação e motivo textual |
| F01 | Feedback para confusões entre aparte, monólogo, rubrica e fala coletiva (cartão 20) | distinguir função pelo destinatário |
| F01 | Nota curta no fecho a anunciar a passagem do provérbio à experiência de Inês | conservar a pergunta para F02 |
| F02 | Feedback de verdadeiro/falso sobre «Inês é preguiçosa» (cartão 17) | separar facto observável de juízo de uma personagem |
| F02 | Feedback por opção sobre «aviamento» (cartão 25) | inferir sentido lexical a partir das falas |
| F02 | Retoma final sobre «Todas vêm e todas vão» e «Praza a Deos...» | preparar a passagem da leitura para a sintaxe |
| F07 | Retoma sucinta da fala «Praza a Deos que...» antes da análise (cartão 1) | passar do que Inês pede à função da oração |
| F07 | Feedback específico para «quem se tenha por ditoso» e para os diferentes «que» (cartões 8, 9 e 15) | evitar regras baseadas apenas no conector |
| F07 | Exercício com frase explicitamente inventada, «A jovem quer sair, mas a família pede que fique» (novo cartão 23) | distinguir coordenação adversativa e subordinada completiva em caso novo |
| F07 | Comparação de causa e finalidade em duas frases igualmente identificadas como inventadas, com resposta revelada voluntariamente (cartão final) | justificar e rever a resposta antes de a consultar |

As notas de continuidade não têm temporizador ou pontuação extra. A transferência escrita/oral não é corrigida artificialmente por uma máquina. A explicação é revelável para permitir autorrevisão e mediação docente.

**Contagens:** F01 24 cartões; F02 28; F07 25 (anteriormente 24). F07 passou de 18 para 19 atividades; todas as leituras anteriores permanecem. A questão nova não substitui perguntas da obra, nem passa a integrar o banco dos desafios do módulo sem uma decisão específica.

## Preservação

- Conteúdo exterior ao array CARTOES sem alterações; títulos, URLs, módulos, IDs, progresso, motores e estilos preservados.
- Não se eliminaram nem reordenaram cartões preexistentes. Inseriu-se um único cartão de escolha antes da leitura final de F07; não há alteração nas chaves de armazenamento.
- Mantidas as opções, respostas corretas, feedback geral e restantes operações dos exercícios existentes. Melhorias limitadas ao feedback específico e à continuidade das leituras.
- Frases criadas para aplicação claramente marcadas como tal: não se atribuem a Gil Vicente.
- Não foi alterado o LENTE.

## Validação funcional — execução final

**Verificação estrutural:** 9/9 controlos iniciais de dados e comparação com a baseline, sem mudanças imprevistas nos bancos ou motores.

**GitHub Actions / Chromium:** [run 39357131084](https://github.com/pedrohfernandes-klk/pt/actions/runs/39357131084), **success** em 20-10-2026:

- **10/10 testes Python** aprovados.
- **144 verificações de navegador** nas três lições F01/F02/F07: 320, 390 e 1440 px, navegação, feedback específico após erro, escolha correta, leitura, conclusão e progresso em chave local de QA.
- **Três percursos completos**, com seleção normal de cartões e interação em todas as etapas apresentadas pelo motor: F01 31 ações, F02 33, F07 30, **94 ações de navegação** no total. Os resultados guardados foram recuperados após recarregar.
- **Regressão adicional de histórico:** F07 iniciou com um histórico sintético que representava três tentativas e melhor classificação **12/12**. O ecrã «Já feita» apresentou a classificação anterior; o botão «Nova tentativa» iniciou novo percurso completo (30 ações), preservou a melhor pontuação e incrementou o número de tentativas. **PASS**. Esta verificação não modifica o progresso dos alunos.
- Formatos de escolha, classificação, associação, lacunas, ordenação e sublinhado exercitados; sem erros JavaScript nos percursos testados.

**Âmbito:** uma tentativa integral por ficha, uma repetição integral com histórico de QA para F07 e ensaios isolados de feedback por alternativa. Não se verificaram todas as combinações aleatórias possíveis nem os históricos reais dos alunos.

## Verificações adicionais, fora da aprovação Chromium

1. **Navegadores e acessibilidade:** Safari/iOS, leitores de ecrã reais, dispositivo móvel físico, foco em todos os percursos e utilização efetiva da projeção em sala — por executar.
2. **Dados anteriores:** compatibilidade do caso sintético F07 **aprovada**; outros formatos históricos e selos/desafios das etapas do módulo não foram ensaiados integralmente.
3. **Aprendizagem:** testar compreensão, fundamentação e transferência com respostas autênticas dos alunos, incluindo recuperação posterior — não demonstrado pelos testes automáticos.

**Estado:** validação funcional automatizada dos três percursos e preservação de melhor resultado antigo em F07 **aprovadas**; acessibilidade real, variantes adicionais, desafio do módulo e eficácia pedagógica permanecem pendentes. PR #34 continua em rascunho, sem fusão nem publicação.
