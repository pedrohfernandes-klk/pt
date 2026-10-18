# M3-F18 — registo de validação

Lição nova: **Uma epopeia por dentro**, 17 cartões e 10 atividades. Este registo compila os resultados de navegador comunicados pelo agente principal; o autor deste documento não repetiu esses testes. Não representa publicação nem aprovação de merge.

## Resultados funcionais comunicados

| Cenário | Resultado observado pelo agente principal |
|---|---|
| Percurso com respostas corretas | 17 cartões percorridos; resultado **10/10**, **140 pontos** |
| Percurso com respostas incorretas | **10 erros** disponibilizados para revisão |
| Nova tentativa | Execução da repetição confirmada |
| Melhor resultado | Preservação do melhor resultado confirmada |
| Progresso da unidade | Indicador **1/8** observado |

Estes resultados cobrem os cenários indicados, não todas as combinações de resposta, transições possíveis ou condições de armazenamento. O valor 1/8 refere-se ao indicador observado, não ao número total de lições do módulo.

## Larguras de apresentação

O ficheiro `outputs/m3-f18-responsive.json` contém as medidas recolhidas pelo agente principal:

| Janela | Largura do conteúdo medida | Largura de deslocação |
|---|---:|---:|
| 320 × 568 | 320 | 320 |
| 390 × 844 | 390 | 390 |
| 768 × 1024 | 768 | 768 |
| 1440 × 900 | 1440 | 1440 |

Não foi detetado transbordo horizontal nas medições registadas. Isso não certifica todos os cartões em todas as larguras, legibilidade com ampliação de texto nem comportamento em dispositivos físicos. Evidência visual disponível: `outputs/m3-f18-nova-licao-mobile.png`.

## Verificações estáticas e editoriais

- Extração dos motores partilhados comparada com M3-F13 na baseline `96cdb520fcf118ef555ef2e325ce93465836c9ea`: casca idêntica; jogo idêntico exceto a remoção do limite de seis itens na revisão. Detalhes em `outputs/pt-paridade-estatica.json`.
- Os 100 arrays CARTOES originais permanecem textualmente preservados, totalizando 2382 cartões; não foram migrados para os motores partilhados.
- A nova lição usa tipos nativos do motor, com índices e feedback consistentes na auditoria estática.
- A referência aos preparativos/despedida foi precisada para IV, 84–93. A revisão editorial independente não encontrou erro bloqueante nos dez exercícios.
- O registo técnico `outputs/m3-f18-implementacao.json` documenta verificação de sintaxe de 14 scripts e ausência de destinos HTML locais em falta na combinação staging + repositório preservado. Os seus campos antigos de testes pendentes não devem ser lidos como se os testes de navegador acima não tivessem ocorrido; este documento acrescenta esses resultados sem reescrever a evidência original.

## Pendências e limites

Continuam sem certificação neste registo: leitor de ecrã; auditoria integral de teclado/foco/menu/som; todos os estados interativos em todas as larguras; métricas de desempenho; falhas de rede ou armazenamento; comportamento em dispositivo físico; ligações e progresso após integração final da branch. Sala, zoom de imagens, animações de símbolos e missões opcionais legadas não fazem parte da prova de paridade desta página nova.

Os testes não executados permanecem explícitos e bloqueantes para a respetiva aprovação de publicação. O êxito dos cenários descritos não autoriza migração em massa, merge ou publicação. LENTE não foi alterado.


Integração final: entrada pelo índice local abre F18; menu por Enter, fecho Escape e retorno do foco ao botão Menu confirmados. Configuração remota de preview não confirmada; endpoint Pages indisponível no conector. Sem deployment público.
