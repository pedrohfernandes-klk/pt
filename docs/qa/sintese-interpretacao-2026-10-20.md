# Síntese e interpretação — revisão local de Português

Data: 20 de outubro de 2026. Ramo: `work/percursos-unidades-20261020`. Alterações locais; sem push, merge ou publicação.

## O que mudou neste bloco

- Nas 20 unidades dos nove módulos, a síntese é feita oralmente ou no caderno. O registo explícito indica realização, sem classificar a qualidade da resposta. O campo de notas no ecrã é opcional; deixou de existir uma contagem mínima como condição de conclusão.
- A conclusão mantém os restantes requisitos do percurso: lições, atividades e desafio. O registo da síntese pode ser revisto; essa revisão atualiza a conclusão. Notas novas, mesmo longas, não concluem automaticamente a unidade.
- As notas e os registos anteriores são preservados. Uma síntese que já satisfazia o anterior critério local de 80 palavras é reconhecida como registo anterior; esse limiar só serve a migração, não as atividades novas. Os históricos da organização anterior continuam separados.
- Mapas, guias e portefólios foram alinhados com a síntese oral/no caderno. Mantêm-se as tarefas autónomas de escrita que têm uma finalidade própria.
- Quatro cartões passaram de resposta automaticamente classificada a comparação aberta de hipóteses, com prova textual e explicação consultável: M1-F02/19 (final da cantiga), M8-F12/10 (sugerir/explicar), M9-F10/14 e /15 (inferência e posição do narrador). Índices indicados a partir de zero. Foram também retirados dos bancos dos desafios.
- Em M7-F14/18, manteve-se a distinção objetiva entre facto e interpretação. O feedback esclarece que uma interpretação exige sustentação textual; não é uma opinião arbitrária.
- O motor comum das atividades não foi alterado. Mantiveram-se as lições e o número total de cartões: 2506, agora com 708 cartões de leitura/exploração e 1798 atividades interativas.

## Verificação efetiva

- 55 testes automáticos passaram, incluindo a regressão específica M1-F01, a continuidade M1–M2, a organização das unidades e os novos critérios da síntese.
- Auditoria das 108 lições: 706 scripts incorporados e sete ficheiros de scripts externos verificados; nenhum erro de sintaxe/inventário reportado. Auditorias de cartões e progressão sem problemas estruturais.
- Chromium: nove módulos a 320 e 1440 px; desafios e cobertura das unidades; os dois desafios de M2 concluídos; persistência de notas, histórico anterior e acesso direto aos complementos.
- Chromium: síntese oral e no caderno sem notas; conclusão com os restantes requisitos preenchidos; foco de teclado após registo; persistência após reabrir; revisão do registo; notas longas sem conclusão automática; migração da síntese anterior.
- Chromium: os quatro cartões abertos mostram a explicação e não oferecem botões de classificação. Captura móvel da síntese inspecionada visualmente.

## Limites e pendentes

Esta é uma correção de casos demonstráveis, não uma certificação de todas as interpretações presentes nas 1798 atividades. A verificação estrutural não demonstra retenção, transferência ou aprendizagem dos alunos. A indisponibilidade de armazenamento recebe mensagem própria, mas não foi simulada neste bloco. Os resultados antigos das lições não foram apagados nem recalculados.

Vídeos e Lente não foram alterados neste bloco. O relatório antigo já incluía recursos existentes: as leituras de Adília Lopes, Cesariny e Tabacaria, Matriz, Justiça/Sandel e as duas experiências de ficção. Mantêm-se pendentes a confirmação audiovisual/atribuições dos três vídeos em reserva e a verificação da reprodução de Sandel depois de iniciada. Não se afirma revisão audiovisual integral.

Os relatórios anteriores descrevem fases anteriores; a exigência de escrever uma síntese no ecrã aí documentada foi substituída por esta alteração.

## Ficheiros para revisão

`alteracoes-acumuladas.patch` contém o diff local acumulado face a HEAD, incluindo as fases anteriores. `sintese-oral-320.png` mostra o registo móvel. Os testes novos estão em `tests/test_unit_synthesis.py` e `tests/browser_unit_synthesis.py`; a execução em Chromium foi acrescentada à integração contínua.
