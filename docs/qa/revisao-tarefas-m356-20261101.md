# Revisão do pedido 144, 01/11/2026

## Âmbito

Aplicação da parte 1 da revisão de arte, português europeu, factos e qualidade. Os achados repetidos entre revisores recebem uma única correção. O pedido continua em rascunho. A revisão dos ramos seguintes recebe este trabalho por merge.

## Correções

| Grupo de achados | Aplicação |
|---|---|
| Abertura dos três índices e pesos | Avaliação dentro de «Como se cumpre uma unidade», depois da abertura; conserva os pesos e a informação sobre recuperação. Teste impede a sua presença antes do título. |
| Linhas T e «Neste módulo» | Título sem o prefixo repetido; apoio identifica a unidade, os 90 minutos, o processo e os 30 %. Índice conta as aulas de leitura/preparação e termina na aula de tarefa. |
| CSS dos guias | Repostos os quatro valores alterados indevidamente pela substituição de 55 por 60. A revisão trabalha por campo e por trecho exato, sem substituições numéricas gerais. |
| Guias e portefólios | Ligações da tarefa e da grelha separadas; títulos entre aspas nas entregas; extras para rever a matéria, sem os confundir com a recuperação avaliada. |
| Dobra dos extras | Alvo com 88 px no telemóvel e 44 px acima, com sinal de abertura. |
| Grelhas e correções | Ligações com cor do sistema e alvos de 44 px; rótulo a 13 px; observações reservadas ao papel em ecrãs estreitos; regras de impressão para manter título e comentário juntos. Regeneração também do M1 e M7-U3. |
| Aquecimentos | Bebas Neue no molde e títulos equilibrados; regeneração dos 16 aquecimentos existentes neste ramo. Os quatro seguintes serão regenerados no 145. |
| Retornos dependentes da ordem | Identificação por conteúdo na tese do M3-U2, antítese, planos e comparação do M6-U1 e fotografia do M6-U2. |
| Metalinguagem e modalidade | Marcas de itálico nos pronomes e formas citadas; probabilidade no M3-U2; explicações da função dos pronomes, discurso direto e indireto livre revistas. |
| Enunciados | Voz que suspende a ação; voz off; tese com citações explicadas; partida como projeto ou viagem; duas fotografias no M6-U2, uma por parte. Ajustes concisos mantêm o limite de 300 palavras do enunciado. |
| Pontuação e referências | Referência da Musa, ensaio extra, «Pois bem», dois pontos antes da citação, síntese do M3-U2 e nomes metalinguísticos corrigidos. |
| Fontes | Camilo tinha 56 anos na fotografia datada de 7 de março de 1882. A antiga Cadeia da Relação é o edifício referido na F09. «O Sentimento dum Ocidental» conserva aspas na F11. |
| Progresso | M5 e M6 voltam a ler e gravar nas chaves históricas `desafio-M5-uN` e `desafio-M6-uN`. Teste de execução carrega uma tentativa anterior do M5, verifica o resultado e proíbe gravações durante a leitura. |
| Texto justificado | Cobertura acrescentada para os pesos e para a prosa de apresentação das tarefas; conserva os casos anteriores. |
| Citações consecutivas | O teste exige versos adjacentes. A barra com espaços é lida como separador de versos, sem omitir palavras entre eles. |
| Fins de linha | O teste exige LF no resultado do gerador. Foi necessário corrigir `scripts/provas/gerar.py`, que ainda escrevia sem `newline`, ao contrário do pressuposto da revisão. Só se normaliza CRLF na cópia de trabalho. |

## Escolhas entre propostas de revisão

* Os pesos ficam dentro da dobra de regras, uma das alternativas expressamente propostas pelo diretor de arte. Evita tanto o bloco no topo como um parágrafo solto depois do rodapé; mantém a informação já testada.
* Escolheu-se «A voz que suspende a ação», em vez de «interrompe», conforme a proposta completa do enunciado.
* Os itálicos metalinguísticos foram aplicados mesmo quando o texto colado da revisão perdeu a formatação e mostrava antes e depois aparentemente iguais.
* O exemplo de discurso direto passa a `A mãe perguntou: «E agora?»`. A decisão sobre permitir travessão em produções do aluno continua reservada ao docente; não foi criado um novo sinal proibido no exemplo público.
* A etiqueta curta das aulas conserva o separador já usado pelos módulos-modelo. A mudança deste separador nos nove módulos fica para uma intervenção conjunta, como solicitado.

## Fonte conferida

[Fotografia de Camilo, ficha do Commons](https://commons.wikimedia.org/wiki/File:Camilo_Castelo_Branco_(1882)_-_Uni%C3%A3o_%E2%80%93_Photographia_da_Casa_Real-Porto.png): a inscrição no verso data a fotografia de 7 de março de 1882; autor União, Photographia da Casa Real, Porto.

## Coordenação e validação

M1 e M7: uniformização futura do texto da linha T, sem alterar agora os seus percursos congelados. Os casos do molde de grelhas e aquecimentos explicitamente pedidos foram corrigidos pelo gerador.

O 152 fica fora desta revisão. A ordem de integração e o registo das camadas serão conferidos depois da revisão humana, sem fusão automática. Os números finais dos testes e as ligações às verificações ficam na descrição do pedido.
