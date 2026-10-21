# M8-F10 — comparar com prova

21 de outubro de 2026. Ramo local work/m8-comparar-com-prova-20261021, após 320876f4 (revisão local de M6). Main remota confirmada em a7faa64c. Nenhuma publicação realizada nesta ronda; M6 e este bloco de M8 continuam locais.

## Problemas demonstráveis

A ficha classificava como certas afirmações sobre a luz exterior e de verão de um poema de Eugénio de Andrade sem identificar o poema, fornecer passagem ou permitir conferir essas afirmações. O modelo também decretava que o melhor par era o mais contrastante, excluindo semelhanças como base legítima de comparação. Vários exercícios apenas repetiam essa classificação sem prova. A imagem inicial, de Goya, já remetia para Sena, mas não para o modelo de luz proposto.

## Correção

O modelo usa agora «Carta a meus filhos sobre os fuzilamentos de Goya», de Jorge de Sena, em Metamorfoses (1963), e O 3 de Maio de 1808 em Madrid, de Goya (1814), a imagem já existente. Um breve verso, já presente em M8-F03, identifica os destinatários e permite observar o futuro verbal. A referência explícita à leitura integral impede tomar o recorte como prova de todas as ideias do poema.

A relação entre destinatários, mundo futuro e violência representada é apresentada como hipótese a desenvolver, não resposta interpretativa única. Os exercícios distinguem indícios conferíveis, enumeração de recursos e argumento. A escolha final compara uma hipótese sustentada com erros plausíveis: intenção idêntica presumida, datas tomadas como impedimento ou lista de recursos sem ligação. Cada erro tem explicação específica. O vocativo e o futuro entram na leitura; não se acrescenta uma lista gramatical desligada.

Hammershøi permanece numa proposta opcional de investigação. Escolher Eugénio requer identificar um poema e localizar a prova. O modelo anterior não foi tratado como validado. Semelhança, contraste e transformação passam a relações possíveis, sujeitas a fundamentação. Mantidos os requisitos de entrega já definidos na encomenda, incluindo cursos, tempos e créditos; não são apresentados no relatório como normas gerais de citação.

## Design e preservação

Conservados 22 cartões, tipos e ordem, URL, chaves de progresso, motores, figura de abertura e encomendas por curso. Alterados os cartões 0,1,2,3,7,8,10,11,12,18,20,21 (índices a partir de zero). Não se acrescentaram fichas ou exercícios. Desafios e painel sincronizados, incluindo duas variantes antigas do desafio que ainda reproduziam a luz não demonstrada.

Na inspeção visual, a retirada do separador decorativo expôs uma grelha antiga de três colunas: o segundo bloco ficava na coluna de 14 píxeis. Corrigido neste modelo com estilo restrito: duas colunas largas, uma abaixo de 600 píxeis, separação por linha e citação com margem curta. Não se alterou o CSS dos restantes módulos.

## Validação

- 94 testes Python aprovados, incluindo quatro regressões novas deste bloco e as três da revisão local de M6.
- Auditorias dos 108 bancos e da sintaxe sem erros; evidências bancos.json e sintaxe.json. Conservadas as contagens globais: 2509 cartões, 710 de leitura e 1799 interativos.
- Chromium a 320/1440: uma tentativa normal por largura, conclusão recuperada após recarregar, percurso forçado pelos 22 cartões do banco, sem erro JavaScript ou transbordo horizontal.
- Todas as três alternativas erradas da comparação final testadas por teclado e respetivo feedback conferido. O motor seleciona dois distratores por tentativa; o ensaio isolou cada par autêntico para garantir cobertura, sem alterar o motor.
- Capturas do modelo inspecionadas após a correção da grelha. O teste reproduzível tests/browser_m8_comparacao.py inclui limite mínimo de largura dos blocos e está integrado no fluxo de regressão.
- Verificação automática de preservação integral da figura de abertura, quantidade, ordem e tipos dos cartões. Sem alteração de índices, não foi criada migração do progresso.

## Fontes e limites

A relação da Carta com Goya foi confrontada com a RTP Ensina: https://ensina.rtp.pt/explicador/metamorfoses-de-jorge-de-sena/ . O resultado de pesquisa foi consultado; a abertura integral dessa página falhou nesta sessão. Não se afirma leitura integral dessa fonte nem do poema nesta ronda. O recorte citado foi retomado da ficha M8-F03 existente.

Identificação da pintura e data: Museo del Prado, https://www.museodelprado.es/coleccion/obra-de-arte/el-3-de-mayo-en-madrid-o-los-fusilamientos/5e177409-2993-4240-97fb-847a02c6496c . Contexto noturno e função do farol: https://www.museodelprado.es/actualidad/actividad/2-y-3-de-mayo-de-1808/37deee43-09d5-4570-9769-b2148f0549aa . A interpretação proposta não é atribuída ao museu como conclusão obrigatória.

Não houve revisão audiovisual, leitor de ecrã real, Safari/iOS, prova com alunos, revisão exaustiva de M8 ou teste de todas as rotações. As antigas apresentações PDF/PPTX arquivadas no repositório não foram revistas; não estão ligadas diretamente na ficha HTML inspecionada. Esta revisão cobre o percurso interativo e o seu desafio, não certifica esses arquivos.
