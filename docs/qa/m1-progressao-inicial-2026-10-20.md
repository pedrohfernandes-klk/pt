# M1 — auditoria inicial da progressão real entre lições

Data: 20-10-2026. Estado: diagnóstico editorial fundamentado em amostras de cartões reais; **nenhum conteúdo de aluno alterado**.

## Base examinada
- Organização curricular do M1: unidade lírica com cinco fichas (F01 → F02 → F05 → F04 → F19) e unidade de crónica com sete (F06 → F08 → F07 → F20 → F15 → F10 → F11), segundo `docs/qa/auditoria-unidades-m1-m9-2026-10-19.md`.
- Bancos `CARTOES` de todas as 12 fichas de M1: amostra inicial de enunciados de cada uma, mais a referência editorial aprofundada já existente para F19.
- Inventário estrutural (19-10-2026): 12 fichas, com variação ativa nas doze. As contagens e tipos do inventário são históricos e não substituem a leitura do código.

## Progressão que já existe e deve ser preservada
1. **F01 → F02:** contexto da produção/transmissão das cantigas → leitura de Mendinho, paralelismo, refrão e indícios de isolamento da voz.
2. **F02 → F05:** da língua medieval presente no poema para as mudanças de sons; esta ligação pode apoiar a interpretação, mas o inventário de processos fonológicos não prova sozinho compreensão da cantiga.
3. **F05 → F04 → F19:** regresso a cantigas de louvor e troça → comparação de versos e análise do desfasamento entre promessa e resultado; F19 já contém transferência da ironia para uma situação inventada.
4. **F06 → F08:** a crónica encena vozes, gestos e ações; F08 aproxima a gramática dos grupos nominais e preposicionais das formulações históricas e da ação.
5. **F08 → F07 → F20:** análise da cidade sitiada → regresso ao grito e à construção narrativa de Fernão Lopes; o importante é discriminar informação do narrador, fala e efeitos na multidão.
6. **F20 → F15 → F10 → F11:** coordenação/subordinação e efeito no sentido → produção contextualizada de uma crónica, com distinção entre fonte e fala imaginada → confronto final das estratégias da cantiga e da crónica.

## Dois focos de auditoria detalhada — não são erros certificados
### A. F01, cartões 9–10 (índices zero): estatuto e ofícios
**Problema editorial observado:** o cartão 9 afirma categoricamente «o trovador é nobre e cria; o jogral, humilde, interpreta por paga» e o cartão 10 transforma trovador, segrel e jogral numa escala social fixa, «da mais alta para a mais humilde». Estas formulações ensinam uma tipologia escolar sem assinalar que se trata de uma generalização histórica e confundem estatuto social e atividade. Não alterar automaticamente a resposta correta: verificar bibliografia medievalística e escolher uma redação que mantenha a distinção funcional sem sugerir fronteiras universais. O cartão 10 requer cuidado especial, pois modificar a ordem imposta altera o mecanismo de correção; melhor substituir a afirmação categórica apenas depois da revisão historiográfica.

### B. F08 → F07/F20: gramática ao serviço do relato
**Verificação adicional:** F08, cartões 17–20, já apresenta transferência para frases novas e análise de uma frase do cerco. F20, cartões 18–20, retoma com clareza a distinção entre afirmação, ação, prova e interpretação. Logo, **não há lacuna demonstrada que justifique inserir um exercício digital novo**. Em aula pode pedir-se uma reformulação oral («O pajem gritou» → «O grito do pajem»), contrastando o foco da construção, mas a continuidade central entre gramática e relato já está representada nas fichas.

## Limites e decisões
- **Manter F19 como referência**: mar com funções distintas, voz autoral vs voz textual, ironia demonstrada pelo confronto entre promessa e realização.
- **Sem novas fichas por quota.** O M1 já tem 5+7 fichas nas suas duas unidades.
- Não se alegam testes de navegador nesta ronda nem leitura exaustiva de todos os cartões.
- Antes de editar uma ficha: ler estímulo, alternativas, índice correto e feedback do cartão-alvo, identificar a confusão demonstrável, preservar o motor e verificar progressão/progresso em navegador.
- Em sala, a evidência mínima de transferência será uma justificação original com um indício preciso, não apenas um acerto de escolha múltipla.

## Próxima ação concreta
Submeter a revisão historiográfica da tipologia de F01 e, caso confirme o risco de categorização excessiva, propor alteração pontual dos cartões 9–10 com regressões. **F08/F07/F20: conservar**, sem acrescentar cartões nesta ronda.

## Intervenção editorial efetuada no ramo (20-10-2026)
O estudo especializado confirma que a tripartição é uma convenção útil, mas historicamente permeável, e que a posição de «segrel» é discutida. O portal **Cantigas Medievais Galego-Portuguesas** regista Pero da Ponte como exemplo de estatuto social de segrel «algo fluido» e Martim Codax como jogral ou segrel e autor de cantigas. A *Enciclopedia Galega Universal* adverte contra a separação simplista entre trovador compositor e jogral mero intérprete.

**Referências de consulta:**
- https://cantigas.fcsh.unl.pt/cfautorgp.asp?cdaut=121
- https://cantigas.fcsh.unl.pt/intervenientemusica.asp?cdaut=92
- https://cantigas.fcsh.unl.pt/palavra.asp?cdpal=251
- https://egu.xunta.gal/gl/termo/121485/escola-galego-portuguesa

**Alteração circunscrita à F01:** explicações de leitura, feedback dos cartões 9 e 10 e respetivos enunciados passam a distinguir esquema didático tradicional e descrição histórica universal. Não foram modificadas as respostas, a ordem dos passos nem o motor. Regressão editorial acrescentada em `tests/test_m1_f01_historical_roles.py`. **A execução desse teste e a validação funcional em navegador permanecem por confirmar.**
