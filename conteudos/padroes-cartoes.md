# Tipos adicionais: contrato para as equipas

Preparação F2, 03/11/2026. Estes tipos ainda não estão publicados. A inserção em lições espera pela aprovação da fase, pelos vídeos e pela fila das camadas. Os exemplos de `tests/fixtures/tipos-mais-ensaio.json` são dados técnicos de ensaio, não conteúdo pedagógico aprovado.

## Regras comuns

Cada cartão novo tem `id` único, `p` e `f`. Não se atribuem identificadores retroativos aos bancos antigos. O identificador acompanha a variante e serve para recuperar, em memória, o que ficou por resolver. A pergunta inicial, a viragem e o fecho de uma lição pertencem ao núcleo, não apenas à seleção variável.

Os distratores representam confusões próximas. Não se usa o comprimento, a concordância óbvia ou uma formulação excepcionalmente prudente para denunciar a resposta. O retorno de erro nomeia a confusão e delimita uma pista; o retorno de acerto explica a prova. Os textos criados são identificados como tal. As citações mantêm a fonte e respeitam os limites de reprodução.

O aluno é tratado por «tu». Usam-se português europeu e AO90. As perguntas que escolhem entre opções dizem «Que…», «Qual das…» ou «Qual é…». Os títulos de livros ficam em itálico e os títulos de poemas entre aspas «». A extração `textos_de` inclui os retornos, as variantes e os materiais, para que a revisão não se limite ao enunciado.

## Escolher o tipo pela operação

| Tipo | Operação que justifica a escolha | Campos específicos |
| --- | --- | --- |
| `lacunas` | Decidir relações num texto, com alternativas que também parecem possíveis | `texto`, `espacos`, `distratores`, `fe_bloco`; opcionais `fe_espaco` e `aceita` |
| `varias` | Julgar todas as afirmações de um conjunto | `o`, `certas`, `fe`; opcional `diz_quantas` |
| `montar` | Experimentar a ordem e observar a relação gramatical | `blocos`, `fim`, `proprios`, `fe_ordem`; opcionais `aceita`, `distratores`, `fe_bloco` |
| `intruso` | Encontrar e testar um critério de classificação | `itens`, `razoes`, `certos`, `fe_item`, `fe_razao` |
| `razao` | Distinguir leituras pela prova que só sustenta uma delas | Os mesmos campos do intruso, com duas ou três leituras e pelo menos três indícios |
| `corrigir` | Localizar um erro antes de conhecer as alternativas de correção | `texto` ou `partes`, `erros`; opcional `armadilhas` |

## Limites

| Tipo | Lição | Núcleo e projeção | Aquecimento |
| --- | --- | --- | --- |
| `lacunas` | Até 70 palavras; até 6 espaços | Até 50 palavras e 5 espaços | Até 40 palavras e 4 espaços |
| Banco de `lacunas` | Até 8 blocos, incluindo 2 a 4 distratores; cada bloco até 2 palavras e 14 carateres | Igual | Igual |
| `varias` | 4 a 6 opções; 2 a n menos 1 certas | Igual | 4 opções |
| `montar` | 3 a 8 blocos, até 4 palavras por bloco; 0 a 2 distratores | 3 a 6 blocos | 3 a 6 blocos |
| `intruso` | 4 a 6 itens de texto; 3 razões; imagens até 4 | Igual | Igual |
| `corrigir` | Até 40 partes e 3 erros | Até 30 partes e 2 erros | Até 30 partes e 2 erros |

Os limites não garantem que um cartão concreto caiba. Mede-se o banco de lacunas a 320 px: até 150 px de altura. Se ultrapassar esse valor, divide-se o cartão. Mede-se também a projeção, o contraste e a legibilidade. Não se reduz a letra para fazer caber conteúdo excessivo.

## Cuidados por tipo

**Lacunas.** Os marcadores `[1]` a `[n]` aparecem uma vez e por ordem. Cada distrator tem retorno válido em todos os espaços, ou um mapa por espaço com recurso `*`. O revisor experimenta cada bloco em cada espaço. Se também servir, regista-o em `aceita` ou altera o texto. Pelo menos metade dos espaços pede uma relação ou um conceito aplicado a um caso novo. Não se copia o resumo que acabou de ser mostrado.

**Várias afirmações.** Todas têm retorno, incluindo as certas que podem ficar esquecidas. Não se usam «todas» nem «nenhuma das anteriores». O cartão não fica junto de um verdadeiro ou falso sobre a mesma distinção.

**Montar.** Os blocos começam por minúscula, exceto os nomes declarados em `proprios`, e não trazem pontuação final. `fim` é obrigatório. As ordens alternativas aceites são permutações dos índices; quando a escrita muda, usa-se `[índices, "frase escrita"]`. O banco inicial não apresenta uma ordem aceite. O texto de erro diz que relação a ordem alterou.

**Intruso.** A pergunta não oferece o critério que o aluno deve encontrar. Cada razão errada é plausível, mas outro elemento do conjunto permite refutá-la. As imagens exigem `img`, `alt`, `autor`, `obra`, `data`, `origem` e `licenca`, com fonte aberta e verificada. Só se admitem domínio público, CC0, CC BY e CC BY-SA. A imagem entra apenas numa página que carregue o visor comum; a fotografia livre de uma obra protegida não resolve os direitos da obra.

**Razão.** Os indícios não são paráfrases das leituras. Pelo menos um é verdadeiro, mas serve às duas leituras, e o retorno explica por que motivo não decide. A verificação automática de palavras repetidas é um alerta estrutural, não substitui esta leitura crítica.

**Corrigir.** As alternativas só aparecem depois da identificação dos erros. Cada erro tem três formas distintas, sem repetir a forma errada, e um retorno. As palavras corretas que parecem erradas podem ter uma explicação em `armadilhas`. A correção conserva a pontuação.

A contagem distingue duas operações: classificar cada palavra como correta ou incorreta e escolher a forma que corrige cada erro. O retorno mostra os dois totais. Na repetição, uma palavra correta marcada por engano volta como decisão de identificação, sem obrigar a corrigir outra palavra que já estava resolvida.

## Integração e revisão

O gerador valida pelo contexto e carrega `tipos-mais.js` e `tipos-mais.css` apenas quando há tipos adicionais. A versão de entrada F2 é `20261102-f2`. O validador estático recusa recursos ausentes ou anteriores à entrada do tipo. Não se muda a versão do motor para apagar o progresso: a F0 fornece a migração explícita por lote.

O material inicial do painel e de papel não inclui índices certos, modelos resolvidos ou retornos. O campo `f` do painel fica separado e só aparece na ação de correção. Um fragmento HTML aprovado não equivale a um documento final impresso aprovado.

`cita` é uma citação, apresentada uma vez pelo cabeçalho do motor. Para frases ou textos criados, usa-se `apoio`, com a indicação «Frase criada» ou «Texto criado»: não recebe aspas automáticas. Ambos acompanham o material para papel e passam pela verificação de língua.

O documento final é gerado por `scripts/cartoes_papel.py`: recebe um JSON com `cartoes` e `titulo`, ou uma lista de cartões, e escreve um HTML autónomo através de `--saida`. Conserva o pedido, a instrução e o material público, sem incluir o banco de respostas. A impressão usa esse documento, não a fotografia da resposta do aluno. As extensões registadas em `tipos_regras` usam o mesmo consumidor.

Antes de inserir cartões, as equipas verificam o raciocínio, a língua, as fontes, as opções, as variantes, o teclado, o telemóvel, a projeção, a impressão e os vídeos. Os primeiros cartões de cada tipo recebem revisão pedagógica. O tempo e os pontos não são prova de aprendizagem: a prova é a resposta sustentada por indícios e capaz de enfrentar uma objeção.
