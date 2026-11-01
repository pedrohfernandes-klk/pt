# Aquecimentos do exame: 27 percursos em cartões

Decisão 106, 01/11/2026. Base: `main`, commit `5bf8b757bb80f4b8b0ce72aba2c48dca813b9c61`.
Ramo: `codex/exame-aquecimentos-20261101`. Integração apenas por revisão da equipa.

## O que muda

Cada sessão passa a ter 12 cartões de fazer, num total de 324. Conservam-se as 81 perguntas anteriores, com as opções reequilibradas e os títulos em itálico. Os dados antigos de `sessoes.json` mantêm-se para rastreabilidade; nesse ficheiro só muda a duração das sessões.

Os bancos ficam em `docs/pedagogia/exame-aquecimentos/s01.json` a `s27.json`. Cada cartão indica `recycledFrom` e, nos acrescentos, `sourceCard`; `adaptacao` identifica transferências para exemplos de treino. Os textos primários são consultáveis, sem glossários nem modelos de resposta. Os exemplos inventados identificam-se como treino ou caso imaginário.

As páginas próprias em `exame/aquecimentos/sNN/` usam a casca e o motor das lições, sem os alterar. A página inteira evita dois níveis de deslocamento e barras concorrentes no telemóvel e na projeção. Há regresso ao aquecimento no topo e no menu e, no fim, continuação para a leitura. O relógio, acessível no menu dos cartões, partilha o estado com a fase Aquecer.

O aquecimento passa a 10 minutos e a sessão a 50. Leitura, escrita, correção e fecho conservam os seus tempos. O catálogo, os enunciados para imprimir e a explicação dos tempos foram atualizados.

## Cartões por sessão

| Sessão | Foco | Fazer | Tipos |
|---|---|---:|---|
| s01 | Cantigas: comparar sem confundir | 12 | 2 escolha, 4 vf, 2 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s02 | Fernão Lopes: uma multidão em ação | 12 | 3 vf, 2 escolha, 3 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s03 | Gil Vicente: desejo, escolha e sátira | 12 | 3 escolha, 2 emparelhar, 1 ordenar, 3 sublinhar, 3 completar |
| s04 | Camões lírico: o que a forma faz sentir | 12 | 3 escolha, 2 sublinhar, 1 completar, 1 versos, 3 vf, 2 emparelhar |
| s05 | Os Lusíadas: celebrar e interrogar | 12 | 3 escolha, 2 versos, 2 sublinhar, 2 completar, 2 vf, 1 emparelhar |
| s06 | Vieira: os peixes são o argumento | 12 | 2 escolha, 3 vf, 3 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s07 | Frei Luís de Sousa: o que a cena revela | 12 | 2 escolha, 3 vf, 3 emparelhar, 2 sublinhar, 1 completar, 1 ordenar |
| s08 | Prosa romântica: paixão e condicionamento | 12 | 2 escolha, 3 vf, 2 sublinhar, 1 completar, 1 versos, 2 emparelhar, 1 ordenar |
| s09 | Eça: ver a crítica nos pormenores | 12 | 1 escolha, 3 vf, 2 completar, 4 sublinhar, 1 emparelhar, 1 ordenar |
| s10 | Antero: procurar, negar, descansar | 12 | 2 escolha, 3 vf, 2 sublinhar, 2 completar, 1 versos, 1 emparelhar, 1 ordenar |
| s11 | Cesário: uma cidade em transformação | 12 | 3 escolha, 2 versos, 1 completar, 2 sublinhar, 2 vf, 2 emparelhar |
| s12 | Pessoa: sentir e construir o poema | 12 | 3 escolha, 1 versos, 2 completar, 2 sublinhar, 2 emparelhar, 1 vf, 1 ordenar |
| s13 | Caeiro: o rio e a medida do olhar | 12 | 3 escolha, 2 sublinhar, 1 emparelhar, 3 vf, 1 completar, 1 versos, 1 ordenar |
| s14 | Reis: a disciplina do instante | 12 | 2 escolha, 3 vf, 2 emparelhar, 2 versos, 2 completar, 1 sublinhar |
| s15 | Campos: desejo e desencontro | 12 | 3 escolha, 1 versos, 1 sublinhar, 1 completar, 3 vf, 2 emparelhar, 1 ordenar |
| s16 | Mensagem: mito, história e apelo | 12 | 2 escolha, 3 vf, 2 sublinhar, 2 versos, 2 completar, 1 emparelhar |
| s17 | Poesia contemporânea: três modos de dizer | 12 | 3 escolha, 2 emparelhar, 2 completar, 2 sublinhar, 2 vf, 1 ordenar |
| s18 | Conto: o que o texto deixa por dizer | 12 | 3 escolha, 1 emparelhar, 2 sublinhar, 3 completar, 3 vf |
| s19 | Saramago: quem conta e quem faz | 12 | 3 escolha, 2 emparelhar, 1 sublinhar, 2 completar, 1 versos, 1 ordenar, 2 vf |
| s20 | Ler informação e escrever uma síntese | 12 | 3 escolha, 2 emparelhar, 2 sublinhar, 1 completar, 2 ordenar, 2 vf |
| s21 | Gramática: funções e relações entre orações | 12 | 3 escolha, 2 completar, 2 sublinhar, 1 ordenar, 2 vf, 2 emparelhar |
| s22 | Gramática: ligar, retomar e situar | 12 | 3 escolha, 2 emparelhar, 2 sublinhar, 3 completar, 1 vf, 1 ordenar |
| s23 | Exposição: explicar com uma linha clara | 12 | 3 escolha, 2 emparelhar, 2 vf, 1 completar, 2 ordenar, 2 sublinhar |
| s24 | Opinião: uma posição que resiste à revisão | 12 | 3 escolha, 2 emparelhar, 3 completar, 1 sublinhar, 2 vf, 1 ordenar |
| s25 | Apreciação crítica: julgar mostrando | 12 | 3 escolha, 2 emparelhar, 1 completar, 1 ordenar, 3 vf, 2 sublinhar |
| s26 | Oficina final: transformar uma resposta | 12 | 3 escolha, 2 vf, 2 emparelhar, 3 sublinhar, 1 completar, 1 ordenar |
| s27 | Ver, compreender, estudar melhor | 12 | 3 escolha, 2 emparelhar, 2 vf, 2 sublinhar, 1 completar, 2 ordenar |

Todos os bancos têm pelo menos cinco tipos e pelo menos um cartão de completar com várias lacunas. Os cartões de leitura não entram na contagem dos 12.

## Retorno e opções

As escolhas têm retorno alinhado com cada alternativa. Nas lacunas, o controlador fornece ao motor apenas o retorno das alternativas erradas selecionadas, conservando a explicação geral. Não foi alterado o motor partilhado.

O gerador exige diferença máxima de 20 % em caracteres visíveis, sem margem mínima de caracteres, tanto nas escolhas como nas lacunas. Exige também que a resposta certa nunca seja a única mais longa. Resultado: 156 conjuntos (71 escolhas e 85 lacunas), amplitude máxima de 20 %, zero conjuntos fora dos 20 %, zero certas como única opção mais longa. Há 44 cartões de completar, 41 com várias lacunas. Os tipos por sessão variam entre cinco e sete. `tests/test_opcoes_equilibradas.py`: cinco testes aprovados, também no CI.

## Progresso e projeção

Chaves novas: `aquecimento-exame-sNN`; relógio: `pt-exame-relogio-v2-sNN-aquecer`. O motor guarda a conclusão, as tentativas e o melhor resultado como nos outros aquecimentos. Recomeçar inicia os cartões sem apagar o melhor resultado. Não migra nem apaga chaves das lições ou dos antigos aquecimentos do exame.

Com `?projetar=1`, os cartões começam do princípio, não mostram resultados privados e não gravam progresso. O relógio projetado também não lê nem grava estado. As ligações de retorno e continuação mantêm a projeção.

## Vídeos de ajuda

Escolha: `escolher`; verdadeiro ou falso: `verdadeiro-falso`; emparelhamento: `ligar-pares` ou `ligar-lados`, conforme a operação; ordenação: `ordenar`; sublinhar: `tocar-palavras`; completar: `completar`. Os ficheiros de vídeo existem e o botão de ajuda aponta para o recurso correspondente.

Versos não tem vídeo dedicado: o motor usa o vídeo de ordenar, que demonstra a mesma operação. Não foi usado mapa, que não tem ajuda associada no motor e não era necessário nestas sessões. Não se gravaram vídeos nem se alterou `/como/`.

## Verificações

A passagem final de `python tests/browser_exame_aquecimentos.py` percorreu os 324 cartões nas três larguras: 320, 390 e 1366 px. Todas as respostas certas foram aceites; verificaram-se ajuda, ausência de deslocamento horizontal, conclusão, melhor resultado, reinício, retorno por alternativa, retorno de uma só lacuna errada e projeção sem gravações nem exposição de resultados privados.

| Comando | Resultado |
|---|---|
| `python scripts/exame_aquecimentos.py --check` | 27 páginas atuais; bancos válidos e opções dentro dos limites |
| `python -m unittest discover -s tests -p 'test_exame*.py' -v` | 16 testes aprovados |
| `node tests/exame-catalogo.cjs` | 27 sessões; 108 itens anteriores preservados; tempos e destinos válidos |
| `python tests/browser_exame_aquecimentos.py` | 81 percursos completos, mais os casos de erro e projeção |
| `node tests/browser_exame_laboratorio.cjs` | Aprovado |
| `node tests/browser_exame_oficina_revisao.cjs` | Aprovado, incluindo impressão e relógio sem armazenamento |
| `python tests/browser_exame_cache.py` | Aprovado a 320 e 1440 px |
| `python tests/browser_exame_alignment.py` | Aprovado |
| `python tests/browser_relogio.py` | Aprovado |
| `python tests/browser_exame_hierarquia.py` | Aprovado: três páginas, 390 e 1366 px |
| `python tests/browser_provas_cartoes.py` | Aprovado: duas provas, todos os grupos, três larguras e projeção |
| `python -m unittest discover -s tests -p 'test_*.py'` | 381 testes executados; ver ressalva de Windows abaixo |
| `git diff --check` | Sem erros |

A suite completa no Windows termina com 461 falhas de subtestes e dois erros, todos em `test_sala_desligada.py`. O mesmo resultado reproduz-se numa extração limpa do commit de base. No CI Linux deste pedido, a verificação da Sala passou. Não se alteraram esses testes nem se apresenta a execução local como aprovada.

No Windows, a execução direta de dois testes de navegador (`browser_exame_hierarquia.py` e `browser_provas_cartoes.py`) deu `WinError 1314` ao criar uma ligação simbólica para servir `/pt/`. Os mesmos testes passaram usando uma junção de diretório, sem mudar qualquer asserção. No CI Linux correm pelos comandos originais.

O primeiro CI aprovou os testes de opções e de língua, mas os dois trabalhos falharam depois com `manifesto desatualizado`: a duração de `sessoes.json` mudou. Foram regenerados apenas os resumos desse ficheiro nos dois manifestos, com a nota `01/11/2026`, sem alterar trocas, ocorrências ou os registos dos outros ficheiros. Reprodução: `python scripts/exame_aquecimentos.py --atualizar-contratos`. As verificações completas dos manifestos confirmam 68/68 e 425/425 trocas aplicadas, zero por aplicar, zero ficheiros excluídos.

O pedido de integração é [#155, em rascunho](https://github.com/pedrohfernandes-klk/pt/pull/155). O estado final do CI consulta-se nesse pedido.

## Capturas e revisão visual

A 390 px, foram vistos o cartão de escolha e o de lacunas: pergunta e controlos legíveis, sem deslocamento horizontal. As colunas de emparelhamento receberam uma regra local de largura para palavras longas a 320 px. Não se alterou o alinhamento do texto corrido.

- [Consulta inicial](exame-aquecimentos-20261101/01-consulta-390.png)
- [Escolha](exame-aquecimentos-20261101/02-escolha-390.png)
- [Várias lacunas](exame-aquecimentos-20261101/03-lacunas-390.png)
- [Projeção](exame-aquecimentos-20261101/04-projecao-390.png)

Foi também verificado o relógio: começa em 10:00, continua na abertura dos cartões e conserva o estado no regresso à fase Aquecer.

## Limites e revisão do docente

Não se alteraram as lições de origem, os exercícios das outras fases, o dossiê, os motores partilhados ou os pedidos #143 a #154. As opções foram adaptadas apenas nos bancos novos. As perguntas anteriores podem preparar aspetos da tarefa escrita, como já faziam, mas não se acrescentou qualquer resposta escrita completa.

A adequação dos 12 cartões a dez minutos deve ser confirmada em aula. O tempo não bloqueia o aluno nem avança por ele. Este pedido não publica nem funde alterações.
