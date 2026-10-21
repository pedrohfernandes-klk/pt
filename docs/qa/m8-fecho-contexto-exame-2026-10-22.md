# M8-F05/F06 — fecho de contexto, complemento e exame

## Âmbito e base
Main confirmada: d83920a684e382f8ce3d53edb4ce9ef03d98c430 (PR #55). Este lote conserva os incrementos locais de ironia e aspeto, anteriormente em 3f259b58, e completa as suas dependências. Não altera o LENTE, os motores, URLs, chaves de progresso ou imagens de abertura. Não constitui revisão integral de M8 ou das 26 sessões de exame.

O utilizador escolheu auditorias paralelas de pedagogia, UX e testes, integração sequencial, e publicação por lote coerente com resumo e evidências antes da integração. As três auditorias foram realizadas sem edições concorrentes; a revisão semântica final do complemento não identificou contradição bloqueante.

## O que mudou e porquê
- F05: os contextos A/B passam a acompanhar as duas perguntas que deles dependem. São exemplos didáticos explicitamente distintos do poema. O apoio apresenta indícios, sem fornecer a classificação. Os rótulos do painel foram encurtados com sentido; metadados e perguntas estão sincronizados. Mantidos 24 cartões.
- F06: o exemplo com «Nele» inclui o antecedente, também na abertura e no desafio autónomo. A pergunta distingue mecanismo de coesão de função sintática. A árvore e o emparelhamento identificam a personagem como sujeito de «viu», em vez de atribuírem a visão ao espelho. «Em geral» delimita a leitura genérica no exemplo de emparelhamento. Mantidos 24 cartões.
- Complemento diretamente ligado «gramatica-aspeto»: seis passos conservados. Ensino e aplicações deixam de exigir contagem exata da repetição e de deduzir interrupção. A tarefa de escrita distingue o que a frase sustenta de interpretações sobre calma ou insistência. Os valores são tratados no contexto, sem exclusividade universal.
- Exame s17: o pedido já solicitava dois poemas de autores diferentes; o foco, o primeiro critério e a correção deixaram de exigir os três autores disponíveis. Os três apoios continuam acessíveis. A s22 remete para F06, mas não reproduz as regras antigas de aspeto: não foi reescrita sem necessidade demonstrada. Atualizada a versão dos recursos para 20261021-exame-5, seguindo o mecanismo de cache já existente.

## Ensino, recuperação, transferência e design
Preservados os modelos analisados antes das aplicações. As perguntas de ironia recuperam a relação entre palavras e situação, com os indícios junto da tarefa. O complemento de aspeto aplica a distinção a escolhas narrativas e pede limites da interpretação. Os fechos continuam a permitir síntese oral/no caderno, sem campos obrigatórios.

Design: proximidade real entre prova e pergunta; controlos, foco e estilos existentes preservados. Os esquemas continuam a exigir deslocação vertical no móvel e no tamanho grande. Não se tratou essa deslocação como transbordo horizontal nem se tentou reduzir o texto com tipografia ilegível. Sem novo vídeo ou decoração.

## Validação executada localmente
- 134 testes Python aprovados, incluindo seis regressões novas deste fecho. A primeira execução geral usou a pasta temporária restrita e falhou por permissões; com TEMP/TMP em work/tmp, os 134 passaram. Um teste novo também detetou uma cópia sem antecedente no desafio; foi corrigida antes da execução aprovada.
- Catálogo de exame: 26 sessões, 104 itens contando verificações finais; tempos, respostas e destinos locais válidos.
- Inventário: 108 lições, 2509 cartões (710 leituras e 1799 interativos), sem erros de banco. Sintaxe de 29 scripts internos nos sete HTML modificados aprovada; motores não alterados.
- Navegador, prévia exata em 127.0.0.1:8779: percurso normal das duas fichas até ao resultado e recuperação do estado após recarregar, a 1440 px. A seleção normal não apresenta todos os 24 cartões de cada banco.
- Prévia focada com o mesmo HTML e motor: perguntas 15/18 de F05 com os apoios, resposta certa na lacuna e resposta errada por Enter, com feedback. Capturas a 390 px, sem transbordo horizontal no caso ensaiado. As prévias focadas são ficheiros locais fora do repositório, não novos conteúdos a publicar.
- Projeção real de F06: controlo Grande (28 px), avanço para o modelo de aspeto, texto e QR visíveis. Captura inspecionada; modelo vertical com deslocação. Não se executou nesta ronda uma passagem integral das duas fichas em projeção grande.
- Complemento: seis passos, classificação 6/6, feedback de erro sobre interrupção, repetição sem contagem exata, transferência por teclado, conclusão e resultado recuperado após recarregar.
- Exame s17: pedido e critério de dois poemas conferidos no navegador. O teste automático acrescentado à CI cobre ainda correção revelada manualmente e o percurso do complemento a 320/1440 px; a sua execução remota deve ser confirmada antes da integração.

As primeiras visitas na porta 8766 não foram usadas para certificar os novos ficheiros: essa prévia não expunha os ficheiros focados. A porta 8779 foi criada para a versão exata. A tentativa de prévia em 8778 também não ficou acessível no navegador. Não se extrapola o que não foi confirmado.

## Fontes e limites
Critérios permanentes: docs/pedagogia/criterios-qualidade-licoes.md. Fundamentação: DGE, referência anafórica (https://area.dge.mec.pt/gramatica/anafora5.html); Dicionário Terminológico, ironia e valor aspetual, nas referências dos relatórios originais. A página de aspeto depende de JavaScript; não se declara leitura integral dessa interface.

Pendentes complementares: leitor de ecrã, Safari/Firefox, aula com alunos e todas as combinações de rotação/erro. Não se ensaiou uma sala docente com participantes remotos nem se revalidou o dossiê fotográfico, cujo código não mudou. Testes demonstram os casos executados, não aprendizagem ou cobertura curricular integral.

Próximo lote: auditar exemplos ambíguos do complemento anafora-catafora (terrina/poeta, «o encontrei» e carta/Teresa), confirmando primeiro os seus acessos; considerar um novo contexto de transferência para ironia se houver necessidade real. As imagens de Goya em F05/F06 foram preservadas; a pertinência específica pode ser revista separadamente. Não apresentar estas pendências como resolvidas.
