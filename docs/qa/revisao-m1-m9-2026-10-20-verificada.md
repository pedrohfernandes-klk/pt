# Português M1–M9 — revisão verificada em 20-10-2026

## Estado e âmbito

Base local e remota confirmada: `main` em `9c48a2846924378be597ec6a34b7a666be84bc3b` (fusão da PR #47, às 17:37 UTC / 18:37 em Lisboa). Ramo local: `work/auditoria-m1-m9-20261020`. Nenhum push, PR nova, merge, publicação ou deploy foi realizado nesta ronda.

- [PR #38](https://github.com/pedrohfernandes-klk/pt/pull/38): fechada e fundida; commit de fusão `0cb7b367a056300cd1ae9062b8ae34ed477f35d5`.
- [PR #39](https://github.com/pedrohfernandes-klk/pt/pull/39): fechada e fundida; commit de fusão `ccb2200183ca9d20d219f57ec21839da4a6ddc63`.
- Ambos os commits são antepassados da base local, confirmado por Git. A revisão inclui, portanto, as alterações posteriores até à #47; não parte apenas das PRs #38–#39.

Cobertura transversal dos **nove módulos e das 108 lições**: inventário, bancos reais, sintaxe, feedback presente, índices corretos, lacunas, opções repetidas, palavras selecionáveis, abertura no navegador e ligações internas das páginas. A leitura editorial aprofundada concentrou-se nos cartões identificados abaixo e em tarefas de interpretação, síntese e gramática de cada módulo. **Não se afirma uma releitura crítica exaustiva de cada alternativa dos 1802 exercícios**, nem uma certificação de aprendizagem. O inventário por lição permite distinguir cobertura estrutural de revisão semântica.

## M1-F01: verificação pedida

Executado especificamente o conjunto `tests/test_m1_f01_historical_roles.py`, incluído na execução global: os três testes originais e a regressão nova passaram.

Leitura dos cartões 3, 4, 8, 9 e 10 e das respetivas opções/feedbacks. Problema comprovado: o cartão 8 ainda afirmava, no feedback de erro, que a criação era do trovador nobre e a interpretação remunerada do jogral humilde. Isto contradizia as ressalvas já integradas nos cartões 3, 9 e 10.

**Correção:** feedback geral e duas explicações de erro do cartão 8 passam a centrar a resposta no caso de D. Dinis, reconhecendo jograis compositores. Preservadas pergunta, alternativas e resposta correta. Mantida a ordenação do cartão 10 como **esquema tradicional explicitamente limitado**, com aviso sobre o estatuto discutido do segrel; não se criou outra escala histórica.

Fundamentação consultada nesta ronda: [FCSH/Littera — Martim Codax](https://cantigas.fcsh.unl.pt/intervenientemusica.asp?cdaut=92), que o apresenta como jogral ou segrel e autor; [glossário de segrel/segrer](https://cantigas.fcsh.unl.pt/palavra.asp?cdpal=251). Estas fontes justificam evitar a exclusividade funcional, sem apagar a distinção didática tradicional.

**Navegador:** percurso normal até ao resultado, persistência e recarregamento; ensaios isolados dos cinco cartões, em 320, 390 e 1440 px. Todas as quatro opções do cartão 8 e os dois valores do cartão 9 foram exercitados. A seleção normal do motor apresenta apenas um subconjunto das opções: o ensaio repete a montagem quando a opção pretendida não surge. A associação e a ordenação tiveram correção positiva. Foram 27 cenários isolados; na execução final, as escolhas e o verdadeiro/falso foram ativados com foco e Enter.

## Continuidade M1-F11 → M2-F01

M1-F11 já confronta voz da cantiga e narrador da crónica (15–16), relaciona marcas com sofrimento individual/coletivo (18) e organiza resposta com duas provas e objeção (21). M2-F01 já distingue rubrica, fala, entrada/vestuário e aparte (16, 19–20). **Não ficou demonstrada necessidade de uma ficha, exercício ou separador de transição adicional.**

Duas formulações de M1-F11 enfraqueciam os pré-requisitos:

1. No cartão 15, «Fala um narrador, Fernão Lopes» equiparava autor e voz narrativa, apesar da distinção voz/autor ensinada nas cantigas. Agora identifica um narrador construído por Fernão Lopes; o feedback de 16 esclarece a diferença. Conservados os pares e a correção automática.
2. O feedback de 19 dizia que a conjunção, por si só, dava nome à oração. Isto contrariava F15, que pede classificação pela construção e pelo sentido contextual. A resposta do exemplo mantém-se; a explicação limita-se àquela reformulação e remete para o contexto.

Os percursos M1-F11 e M2-F01 foram concluídos normalmente e recarregados com progresso preservado. Os cartões alterados de F11 tiveram ainda testes isolados de leitura, associação e verdadeiro/falso. M2-F01 não foi editada.

## Revisão dos nove módulos

Os números seguintes contam lições, não desafios ou percursos complementares. A ordem curricular foi lida nos mapas/índices e confrontada com a documentação existente; os exemplos referem bancos atuais. Uma ausência de intervenção significa falta de erro comprovado bastante para editar, não ausência garantida de problemas.

| Módulo | Lições | Evidência editorial e progressão observada | Decisão e limite |
|---|---:|---|---|
| M1 | 12 | F01 situa produção/transmissão; F02 pede prova para natureza ameaçadora; F04 confronta escárnio/maldizer; F05 faz rever hipótese linguística; F08 liga dependência e função; F19 confronta promessa e resultado; F20 separa grito e facto; F11 sintetiza com provas e objeção. | Corrigidos F01/8 e F11/15–16,19. A associação fechada de «três leituras que não podem ser verdadeiras juntas» em F02/19 merece futura revisão interpretativa com a edição em uso; não foi automaticamente substituída. |
| M2 | 10 | F01→F02→F07 passa de rubrica/desejo à sintaxe em cena; F06/30–31 fundamenta o provérbio no desfecho; F08/16 exige dois indícios; F10/18 liga encenação e efeito; F12–F13 transferem para objeto cénico e defesa que não responde à acusação. | Conservar as melhorias das PRs anteriores. Sem nova atividade. F01 teve percurso completo nesta ronda; as restantes não foram todas percorridas integralmente de novo. |
| M3 | 12 | F02 revê ponto de vista; F03 parte de elementos observados; F15 distingue anáfora retórica/referencial; F18 separa cronologia, relato e voz; F16/16 exige pergunta com prova; F17/14–15 exige explicar versos e escrever autonomamente. | Conservar. F18, com banco externo, teve percurso completo. Os testes das revisões F02/F03/F09/F16/F17 passaram. Não se reescreveram textos acabados de integrar. |
| M4 | 15 | F04/12 trabalha o duplo valor de «comer»; F06/19 aplica critério de efeito; F11/18 distingue tipos de afirmação; F25/21 exige traço, comportamento, recurso e limite; F26 trabalha distribuição de informação; F27/15,17 recusa citação sem explicação. | Conservar os exercícios existentes. Há distratores fáceis em tarefas introdutórias; a facilidade isolada não demonstra lacuna que justifique inflacionar o banco. Necessária observação das justificações dos alunos. |
| M5 | 11 | F02 separa documento e ficção; F04/23–24 confronta discurso do pai e violência; F07 transforma a voz sintática; F10/23 compara Ramalhete inicial/final; F12 distingue vozes; F14 compara livro/ecrã; F15 sintetiza perdas. | Conservar a correção recente do indireto livre em F12/20. A regressão correspondente passou; o QA existente de associação/lacunas/feedback em M3/M5/M7 foi repetido, com 56 verificações. Não se certificam todos os contextos possíveis de indireto livre. |
| M6 | 11 | F01→F02 contrapõe procura e descanso; F04 analisa orações nos versos; F05 pede consulta lexical; F06–F07 segue as partes de «O Sentimento dum Ocidental»; F09 pede verso de cada poeta e matiz; F11 separa facto biográfico e interpretação; F12 distingue transfiguração e gesto real; F13 liga imperativo, destinatário e intervenção. | Conservar. F01/17,20 formula «soneto» como se tivesse necessariamente dez sílabas; fica sinalizada para revisão contextualizada da métrica e dos casos paralelos antes de generalizar uma alteração. Não se alterou contagem nem se acrescentou uma tarefa. |
| M7 | 17 | F02 percorre a transformação da dor; F04 observa a tensão entre olhar e argumentar; F05 segue o convite de Reis; F07 classifica orações contextualizadas; F11/5 liga causal e serenidade; F14 põe em discussão o otimismo; F34–F36 articulam planos, rio/olhar e possibilidade. | Conservar os textos e motores. A causalidade biografia→estilo em F11 já fora corrigida e a regressão passou. As sínteses por heterónimo devem continuar a ser confrontadas com versos, não tomadas como retratos universais. |
| M8 | 10 | F01 introduz lentes; F03 liga figuração da testemunha e imagem histórica; F04 faz cortes; F05 lê a transformação da prece; F06 integra aspeto e referência; F08 trabalha revisão de hipóteses em «George»; F09 delimita a regra desta tarefa; F12 exige comparar pistas diferentes. | Corrigidos cinco cartões de F03 que faziam «viu» equivaler demasiado facilmente a presença nos acontecimentos. Conservada a figuração ética, explicitada a mediação de Goya e exigida explicação autónoma no feedback final. Restante revisão semântica não é exaustiva. |
| M9 | 10 | F01 distingue época, ordem e narração; F02 distingue facto ficcional/interpretação; F03 trabalha reprodução do discurso; F05 analisa nomeação e esquecimento; F10 organiza debate; F11–F13 acrescentam ação/limite, música e revisão de hipótese com páginas da edição. | Corrigido F03/12: o procedimento com «que» fica limitado à afirmação de Blimunda e confrontado com a pergunta do cartão 11. Percursos completos de F03 e dos três bancos externos. Preservada a necessidade de ler o romance. |

### Fundamentação adicional das correções

- **M8-F03:** a própria lição data os fuzilamentos em 1808 e o nascimento de Sena em 1919. A [RTP Ensina — Metamorfoses](https://ensina.rtp.pt/explicador/metamorfoses-de-jorge-de-sena/) enquadra a «Carta» em relação à pintura. O problema é a ambiguidade do apoio didático, não a legitimidade da figuração de testemunha. Não se copiou o poema nem se inventaram citações.
- **M9-F03:** o cartão 11 já aceita «Baltasar perguntou dentro de quê», enquanto o 12 mandava ligar genericamente a fala por «que». A correção é demonstrável na própria sequência; [DGE — interrogativas indiretas](https://area.dge.mec.pt/gramatica/c12interrogperes.htm) documenta a presença de expressões interrogativas nessas construções. Não se criou um novo motor de transformação.

## Preservação e manutenção

Alterados **dez cartões de quatro lições**: M1-F01 [8]; M1-F11 [15,16,19]; M8-F03 [14,15,20,22,23]; M9-F03 [12]. Índices a partir de zero.

Comparação automática com a base: números e ordem dos cartões preservados (22/24/26/26); tipos, opções, índices e valores corretos, lacunas, pares, grupos e referências de linha sem alterações. Nos exercícios de ordenação mantém-se o número de passos e a operação. O texto exterior ao banco das quatro páginas é idêntico. Nenhuma mudança em CSS, motores, IDs, URLs ou chaves de armazenamento. Nenhuma ficha ou exercício acrescentado/eliminado.

Controlos corrigidos:

- `audit_cards.py` reconhece e valida os quatro bancos externos, sem ignorar uma lição desconhecida sem banco; verifica ainda opções duplicadas, feedback desalinhado, índices de palavras e correspondência entre marcadores/lacunas.
- `audit_learning_progression.py` reutiliza a mesma leitura de bancos. Antes acusava quatro erros inexistentes e omitia 42 atividades; agora cobre 108 lições.
- `audit_lessons.py` atualiza as contagens revistas e verifica também os sete scripts locais externos efetivamente ligados às páginas.
- Workflow M1 existente alargado ao inventário transversal, regressões e cenários de navegador. **Configurado, mas não executado remotamente nesta ronda**, pois não houve push.

## Resultados executados

| Verificação | Resultado e alcance |
|---|---|
| Testes Python | **48/48 aprovados**; inclui teste histórico pedido, continuidade, regressões anteriores e novos casos de auditoria/contexto. |
| Bancos | **108**, 2506 cartões: **704 leituras + 1802 atividades**. Sem erros nos controlos definidos. Presença de feedback não demonstra, por si só, qualidade de todas as explicações. |
| Sintaxe/inventário | **108 páginas, 706 scripts inline e 7 scripts externos** verificados; sem erros. `lang=pt-PT` e títulos verificados. |
| Ligações | **928 referências internas** em ligações HTML das lições, após normalizar o endereço publicado para a cópia local: nenhum destino em falta. Não inclui âncoras, ligações criadas dinamicamente ou disponibilidade de serviços externos. |
| Abertura em Chromium | **216 aberturas**: 108 lições × 320/1440 px, sem erro JavaScript ou transbordo horizontal inicial. Isto não equivale a 216 percursos completos. |
| Percursos completos finais | **9**: M1-F01 (29 ações), M1-F11 (27), M2-F01 (31), M8-F03 (30), M9-F03 (26), M3-F18 (27), M9-F11 (21), F12 (21), F13 (39). Total **251 ações**; conclusão e progresso preservados após recarregar. Uma tentativa normal por lição, sem esgotar combinações aleatórias. As ações podem incluir erros deliberados de navegação. |
| Cartões históricos isolados | **27 cenários**; leitura, associação, respostas certas/erradas e ordenação em 320/390/1440 px; teclado nas escolhas e verdadeiro/falso. |
| Contexto e feedback | **18 cenários**: nove cartões alterados × 320/1440 px; leitura/feedback efetivo, resposta certa, conclusão e gravação em chave de QA. |
| Regressão anterior de navegador | Repetido `browser_learning_evidence.py`: **56 verificações aprovadas** nos casos já existentes de M3/M5/M7. |
| Revisão visual | Inspecionadas capturas móveis de M1-F11/15, M8-F03/22 e M9-F03/12: hierarquia, texto e feedback legíveis; preservado o design minimalista/brutalista. |

A primeira execução Python encontrou bloqueio de permissões da pasta temporária do ambiente. Repetida com `TEMP`/`TMP` numa pasta de trabalho autorizada: sucesso. Chromium e Node foram executados com acesso aos processos locais necessário; isto não alterou o site remoto.

## Pendente, com prioridade e sem certificar o que não foi feito

1. **Revisão semântica exaustiva:** ler todas as alternativas, formulações `p2`, pistas e explicações das 1802 atividades e das restantes atividades dos desafios. Esta ronda abrange todos os módulos e bancos, com aprofundamento seletivo; não substitui essa leitura. Prioridades concretas: M1-F02/19 (leituras apresentadas como incompatíveis), M6-F01/17,20 (definição de soneto), e o par-modelo de M8-F10 (identificar o poema para conferir as afirmações sobre a luz).
2. **Acessibilidade:** o teclado foi exercitado nos cenários descritos; não foi auditada toda a ordem de foco, todos os exercícios, contraste medido, zoom a 200–400 %, leitor de ecrã real, nem Safari/iOS. Não há declaração WCAG. Verificar esses pontos antes de certificar acessibilidade.
3. **Navegadores/progresso:** não se esgotaram seleção aleatória, modo «só os que errei», projeção, sala, desafios, selos, todos os históricos antigos ou dispositivos físicos. Os históricos dos alunos não foram lidos nem alterados; QA usou contextos novos e chaves próprias nos ensaios isolados.
4. **Aprendizagem:** recolher respostas originais, confrontar inferência/prova e verificar recuperação posterior em aula. Os acertos do navegador não demonstram compreensão ou transferência efetiva.
5. **Integração:** rever o diff e executar a CI no ramo se vier a ser enviado ao GitHub. Merge, push para `main`, publicação e deploy dependem de autorização explícita.

Os restantes pontos sinalizados não foram «corrigidos» por hipótese: ficaram localizados e separados das dez intervenções efetivamente verificadas. Não se multiplicaram exercícios nem se uniformizaram as aulas num único formato.
