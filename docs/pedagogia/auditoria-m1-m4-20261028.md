# Auditoria do M1 e do M4: correções aplicadas (28/10/2026)

Uma equipa de agentes leu as lições, os painéis, os índices, as tarefas e os guiões do M1 e do M4. Depois, um verificador cético confirmou cada achado. Este PR aplica os achados confirmados que se corrigem com texto. A ordem, os tipos, as chaves e as respostas certas dos cartões não mudam, e o progresso guardado nos aparelhos também não.

## O que mudou

**Regras de escrita**
- Saem «—», «ficha», «folha» e «feedback» do texto visível:
  - na F05 (esquema PEP e ASA) e na F28;
  - nas três aulas de tarefa do M4 e no apoio de comparação da unidade 3;
  - nos índices, guias e mapas do M4 e do M7 («trabalho em papel», como no M1);
  - no painel da F28 e nos guiões das aulas 8, 15 e 18 do M4.
- Nas tarefas do M4, o «·» que fazia de pontuação passou a dois pontos ou a «e».
- Os sublinhados de itálico em bruto saíram:
  - das opções do relâmpago dos painéis do M1 e do M4;
  - do pedido projetado e das pistas do Atlas, que agora aparecem em itálico;
  - dos guiões das aulas 1 e 12 do M1.

**Factos e citações**
- Vieira: em 1669 parte para Roma; o breve do papa que o isenta da Inquisição portuguesa é de 1675 (F01).
- Frei Luís de Sousa: «vinte e um anos» depois de Alcácer Quibir, como na peça (F08). A F28 cita Garrett à letra: «me não deixaram gozar».
- Fernão Lopes: os cortes que faltava marcar levam […] (F06, F07, F20).
- *Voz emprestada*: as legendas dizem as estrofes mostradas, em vez de «integral». O jogral é descrito como na aula 1. Os guiões deixam de mandar corrigir o ecrã oralmente.
- *A promessa do cronista*:
  - o cerco levantou-se «sobretudo» pela peste;
  - a marca «documentada / imaginada» vem explicada antes da aula 13;
  - a pergunta do Ato 3 tem uma só resposta defensável.
- Página do sermão (obras): o sermão foi pregado em 1654 e a primeira edição é de 1682. A lista de capítulos inclui o VI.

**Perguntas com mais de uma resposta defensável ou com variante errada**
- F25: a variante p2 do verdadeiro ou falso dizia o contrário da afirmação, que continua verdadeira.
- F01 do M1 (ordenar a escala): a pergunta diz agora o sentido, do mais alto para o mais baixo.
- F20 do M4 (sublinhar): «o objeto observado e o que lhe acontece».

**Coerência**
- Os painéis do M1 têm a unidade certa (o módulo tem duas).
- As tarefas do M1 e do M2 com uma só pergunta opcional deixam de a numerar «2.» (não há nenhum «1.» à vista). A mudança foi feita também nos dados. A contagem «0 de 2» fica, porque o aquecimento também conta.
- No mapa do M4:
  - as ligações vão para as aulas de tarefa (`#tarefa-unidade-N`), e não para o arquivo escondido;
  - as imagens de «Para ver» apontam para as lições onde aparecem;
  - o cabeçalho fecha com a pergunta da unidade 3.
- A tarefa da unidade 2 do M4:
  - tem o mesmo título no índice, no guia e na página;
  - relembra «Quem sabia, e quando» em vez da F27, que só vem na unidade 3.
- Créditos completos das imagens da F01, da F04 e da F11 do M4.
- A F02 do M1 deixa de citar o nome automático do canal do YouTube.
- A F01 do M4 perde o vídeo do Câmara Clara, por estar fora de contexto (regra de 28/10). O cartão compara agora os dois pregadores pela leitura, e o guião da aula 1 deixa de mandar projetar o vídeo.

## Como os testes o aceitam

As lições e as tarefas estão congeladas por hash. Cada troca está escrita, literalmente, em `tests/fixtures/auditoria-m1-m4-edits-20261028.json`. O auxiliar `tests/auditoria_20261028.py` desfaz estas trocas antes de cada comparação com o estado congelado. Se uma troca deixar de conferir, o teste falha.

Cinco testes ligam-se a ele, cada um com comentário datado:
- `test_task_routes_closure`;
- `task_source_contract`;
- `test_m1_grammar_pilot`;
- `test_module_layout`;
- `test_task_90`.

O `browser_m4_tpc` passou a comparar as opções do relâmpago sem os sublinhados de itálico.

## Fica para o PR seguinte (com a auditoria do M7)

- F10 e guião da aula 8 do M4: a lição ainda prepara a tarefa da unidade 1 como trabalho de grupo, com PDF. A tarefa atual é individual e em papel.
- Numeração antiga das tarefas do M4 (Tarefa 2 discurso, Tarefa 3 apreciação) na F14, na F20 e nos guiões das aulas 8, 11 e 16. Inclui também o bloco «As tarefas do Teams» no mapa.
- Guião da aula 9 do M4: descreve uma versão antiga da F28 e tem de ser reescrito a partir da lição.
- O «Sala —» dos painéis sai com a Sala, num PR próprio: a Sala foi desligada nas fontes a 17/10, mas continua no sítio publicado.
- Os diapositivos (.pptx e .pdf) das aulas tocadas ainda têm o texto antigo, que já lá estava antes. São eles: M1 aulas 2, 6, 7, 11 e 13; M4 aula 1, aula 12 e sessão 9. Ficam para a próxima geração dos diapositivos.
- As contagens do mapa do M4 ficam: o número conta as lições principais do plano, como o teste UX06 define.
