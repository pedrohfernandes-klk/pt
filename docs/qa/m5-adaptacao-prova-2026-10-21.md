# M5-F14 — observar antes de avaliar a adaptação

Revisão local em 21 de outubro de 2026, após a publicação de M6/M8 pela PR #53. Base: main 2290c8e1. Ramo próprio work/m5-adaptacao-com-prova-20261021. Sem publicação deste bloco.

## Problema e intervenção

A ficha apresentava a conservação da ironia como ganho certo da voz narrativa e a perda de ritmo como possibilidade genérica, sem localizar um excerto. O desafio repetia a conservação da ironia como resposta fechada. Esses efeitos precisam de prova na relação entre texto, leitura vocal, imagem e montagem.

A revisão distingue observação, interpretação e avaliação. Identificar uma voz narrativa não equivale a comprovar ironia; uma pausa não prova, sozinha, perda de ritmo. O aluno regista versão e marca temporal e fundamenta o efeito. A coluna de avaliação mantém a comparação entre ganhos e perdas, mas esclarece que não é necessário inventar uma perda para obter simetria.

O modelo contém duas hipóteses inventadas: mesmo plano da fachada sem voz ou com a expressão «sombrio casarão de paredes severas» e uma pausa. Estão explicitamente identificadas como exercício de encenação, não como descrição de cenas reais de Botelho. O trecho do romance já se encontra em M5-F10, para onde se liga. A experiência oral prepara a observação do filme e permite rever a previsão depois de ver um excerto.

Duas escolhas com alternativas plausíveis distinguem o indício da inferência precipitada. Uma associação organiza dimensões de observação em vez de impor efeitos. As formulações alternativas p2, as variantes do desafio e o painel foram sincronizados. O exemplo no desafio explicita as hipóteses para funcionar sem depender de um cartão de leitura ausente.

## Fontes efetivamente consultadas

A RTP confirma a emissão em dezembro de 2015 de uma versão alargada em quatro episódios, com cenas inéditas: https://media.rtp.pt/extra/ficcao/estreia-os-maias-minisserie/ . A ficha técnica da Cinemateca confirma filme de 2014, argumento e realização de João Botelho e Jorge Vaz de Carvalho como voz do narrador: https://www.cinemateca.pt/CinematecaSite/media/Documentos/2022-09-21_OS-MAIAS-CENAS-DA-VIDA-ROMANTICA.pdf . Ambas abertas e consultadas nesta ronda. Não foi visionado integralmente o filme ou um episódio, nem verificada reprodução ou disponibilidade audiovisual. Não se atribui às fontes a interpretação das hipóteses didáticas inventadas.

## Preservação

Mantidos 21 cartões, tipos, ordem, imagem e cartão de abertura integralmente iguais à base, textos literários existentes, URLs, motores e chaves de progresso. Alterados os cartões 1,2,5,6,7,8,11,12,13,14,15,16,18,20 (índices a partir de zero). Sem novas fichas ou aumento de exercícios. Os desafios mantêm o número de itens; uma variante de verdadeiro/falso redundante foi substituída pela escolha fundamentada e autónoma. Não houve reordenação de índices da lição, pelo que não se criou migração do progresso.

## QA realizado

99 testes Python aprovados, incluindo cinco regressões de M5. Auditorias das 108 lições e bancos sem erros; evidências bancos.json e sintaxe.json. Globalmente, 2509 cartões: 710 de leitura e 1799 interativos.

Chromium a 320/1440: uma tentativa normal por largura, conclusão preservada após recarregar, percurso pelos 21 cartões do banco e nenhum erro JavaScript ou transbordo horizontal nos estados percorridos. As três alternativas erradas de cada uma das duas escolhas revistas foram exercitadas por teclado, com feedback específico conferido. Como o motor seleciona dois distratores, cada par de resposta correta e distrator foi isolado para cobrir todas as explicações sem alterar a produção. Pista do modelo aberta e fechada por teclado. Captura móvel inspecionada. Teste reproduzível tests/browser_m5_adaptacao.py integrado no fluxo de regressão.

## Limites e continuação

Não se comprova aprendizagem por estes acertos nem se certifica revisão integral de M5. Não foram testados Safari, leitor de ecrã real, todas as rotações, projeção física ou respostas de alunos. Apresentações PDF/PPTX arquivadas não foram revistas. Não foi integrado vídeo novo sem revisão audiovisual.

Próxima revisão concreta sugerida: M6-F09, onde a associação de recursos a cada poeta pode ser lida como exclusividade e «hipálage ou sinestesia» pede distinção contextual. Conferir primeiro versos e exemplos; não generalizar a alteração a todo o módulo.
