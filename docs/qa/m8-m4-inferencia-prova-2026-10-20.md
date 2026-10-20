# Português — M8 e M4: inferir, rever, provar

Data: 20-10-2026. Ramo independente a partir de `main`. PR em rascunho; sem publicação. Esta ronda dá continuidade às PR #34–#36, sem depender das suas alterações.

## Porque intervir

**M8 — unidade «O que cabe num conto».** A F08 apresenta distinções entre facto, inferência e interpretação, mas os cartões 8 e 13 pediam apenas recuperar adjetivos ou identificar uma opinião. O aluno podia acertar sem justificar nem corrigir uma hipótese. As fichas F09 e F12 recuperavam regras de uma encomenda e slogans sobre «sugerir em vez de explicar», sem aplicar consistentemente essas distinções a situações novas.

**M4 — unidade «Trinta dias no abrigo».** A F27 faz bem a ligação entre a ideia, o indício e a explicação, mas os distratores dos cartões 3, 6 e 12 continham respostas quase elimináveis sem reler Vieira ou Garrett («porque sim», generalização sobre a idade, nome da obra). Melhorar a plausibilidade das alternativas é prioritário face a acrescentar cartões.

## Alterações executadas

| Ficha | Intervenção concreta | Aprendizagem que procura tornar observável |
| --- | --- | --- |
| M8-F08, cartões 8 e 13 | Um exemplo **expressamente inventado**, distinto de «George»: Rita encontra a carta que julgava queimada e não a abre; mais tarde, um ano escrito no verso obriga a **rever** a hipótese sobre quem a guardou | Distinguir ação observável, inferência possível e conclusão que os indícios não autorizam; reavaliar a hipótese com um novo pormenor |
| M8-F08, leituras 1 e 21 | Instruções para regressar à narrativa de «George» com hipótese, indício e dúvida não resolvida | A sinopse ajuda a entrar na leitura, mas não substitui uma passagem do texto literário |
| M8-F09, cartão 10 | Pequena cena **inventada** sobre Teresa e a chave, com quatro versões de continuação; comparar tensão sustentada pelos gestos e explicação psicológica prematura | Aplicar a noção de sugestão na revisão de um conto |
| M8-F09, cartão 15 | A unidade de ação é exigência **desta tarefa de escrita**, não uma lei absoluta de todos os contos | Distinguir o contrato de avaliação de uma definição universal do género |
| M8-F12, leituras 0 e 2, cartão 6 | A hipótese de que poesia e conto «não explicam» deixa de ser conclusão obrigatória; comparar pergunta poética e encontro narrado quanto à função do que fica em aberto | Identificar analogia e diferença; não presumir mensagem idêntica a partir de técnica parecida |
| M4-F27, cartões 3, 6 e 12 | Distratores plausíveis e feedback por erro específico; respostas corretas mantidas | Usar a passagem sobre os grandes e pequenos, a direção da apóstrofe e fala + didascália para sustentar a resposta |

Não houve alterações de texto a obras de terceiros. Os cenários de Rita e Teresa estão identificados como **exemplos inventados**, não passagens de «George». A apreciação literária do conto exige consulta efetiva à obra; a atividade não a dispensa.

## Preservação — verificação estrutural realizada

Confronto programático dos quatro bancos `CARTOES` de `main` com o ramo de trabalho, com resultado **PASS**:

- **85 cartões no total**, sem novos nem eliminados: F08 22, F09 19, F12 22, M4-F27 22. **67 atividades** (17 + 16 + 18 + 16); nenhuma alterou o tipo.
- HTML e JavaScript **exteriores** aos bancos `CARTOES` integralmente idênticos aos da base.
- Alterações limitadas aos campos editoriais identificados; valor/índice de cada resposta certa original preservado.
- Feedback `fe` por opção incorreta compatível com os índices originais; instruções de leitura anteriores mantidas, salvo substituições pontuais em M8-F12.
- Sem novas dependências de produção, CSS, imagens, IDs, URLs, grupos, temporizadores, componentes ou chaves de progresso.

Os seis testes de regressão editorial foram adicionados em `tests/test_inferencia_m8_m4.py`. Foi também preparado `tests/browser_inferencia_m8_m4.py`, que deverá exercitar o motor real em Chromium, abrir as quatro fichas em 320/390/1440 píxeis, concluir uma tentativa por ficha, recarregar para verificar o progresso e provocar erros específicos nas escolhas revistas. O GitHub Actions responsável encontra-se em `.github/workflows/pt-m8-m4-qa.yml`.

**Estado de execução atualizado:** a validação funcional automatizada terminou com **success** em [GitHub Actions #39387441373](https://github.com/pedrohfernandes-klk/pt/actions/runs/39387441373), a 20-10-2026. Foram aprovados **6/6 testes Python** e **125 verificações de Chromium** em quatro fichas, incluindo carregamento sem erros JavaScript nos cenários exercitados, larguras de 320/390/1440 píxeis, feedback específico associado ao índice de cada opção errada, conclusão de cada ficha e recuperação do progresso local após recarregar.

**Percursos completos:** M8-F08, **29 ações**; M8-F09, **25 ações**; M8-F12, **28 ações**; M4-F27, **28 ações**. Total: **110 ações de navegação**. Os exercícios foram concluídos com o motor das páginas, sem saltar os cartões apresentados nessa tentativa. A suite também exerceu isoladamente as alternativas erradas nas escolhas revistas.

**Limite da aprovação:** uma tentativa integral por ficha e alternativas específicas no motor real, não todas as seleções e formulações possíveis, nem Safari/iOS, leitor de ecrã real, projeção física ou aquisição de competências pelos alunos.

## Antes de publicar

- Concluir e aprovar os testes Python e Chromium, corrigindo falhas reais e distinguindo bugs de testes de bugs de produção.
- Testar Safari/iOS, leitor de ecrã real, teclado, zoom, projeção e mobilidade em dispositivos físicos; não alegar estes testes com base na execução do Chromium.
- Usar dois trabalhos curtos de alunos para avaliar se conseguem localizar indícios, defender uma hipótese e revisá-la depois de outro indício. Repetir a operação noutro conto, sem copiar a situação inventada.
- Confirmar que alterações textuais não tornam rígidos os esquemas de resposta e que as quatro fichas são utilizáveis com o professor e autonomamente.

## Próximo foco editorial

M8: observar a leitura integral de «George» e se existem momentos suficientes de prova textual genuína, pois o baralho atual depende bastante da síntese do conto. M4: observar em aula se os distratores mais plausíveis obrigam efetivamente a reler a passagem, sem avaliar a competência apenas pelo acerto.
