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

## Validação efetivamente executada

**9/9 verificações programáticas de dados**, sobre os ficheiros reais do ramo: contagens; presença de feedback geral nas atividades; três explicações para cada escolha errada nas opções selecionadas; feedback específico de verdadeiro/falso; continuidade entre as fichas; existência de uma única atividade no grupo «transfer»; ausência de enunciados «p» repetidos; compatibilidade dos tipos com o motor; seleção do grupo de transferência nas **1 000 amostras simuladas** do algoritmo (não no navegador).

Além disso, confronto dos arrays com a baseline da main confirmou estabilidade de todas as partes exteriores aos arrays. O motor atribui «data-j» ao índice original da opção quando a apresenta baralhada; o campo «fe» usa esse índice. Essa correspondência permite o feedback específico após baralhamento, mas falta observá-la na interface real.

O ficheiro tests/test_m2_u1_learning.py acrescenta cinco testes de regressão ao repositório. **Ainda não foi executado por um runner Python no checkout completo**; não confundir a verificação de dados deste lote com a execução da suite nem com um teste de navegador.

## Verificações ainda obrigatórias antes de publicar

1. Executar a suite Python, a auditoria geral e a verificação de sintaxe em checkout completo.
2. Abrir F01, F02 e F07 num navegador real; testar escolha errada e certa, mensagens por alternativa, navegação entre cartões, retoma e leitura final; repetir tentativa com outras opções.
3. Verificar resposta e regresso no percurso F07, estado após recarregar e se a introdução do cartão afeta o melhor resultado pré-existente; confirmar desafios de M2 intactos.
4. Inspecionar ecrãs estreitos, projeção, teclado, foco, leitor de ecrã, Safari/iOS e desempenho.
5. Realizar uma aplicação com alunos: recolher exemplos anonimizados de justificações, confrontar reconhecimento imediato com aplicação posterior e rever distratores que se revelem artificiais ou ambíguos.

**Não declarar aprendizagem real comprovada:** existe agora um percurso melhor sustentado e observável, mas compreensão, retenção e efeito da intervenção exigem provas em aula.
