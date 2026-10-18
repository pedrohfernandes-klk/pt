# Português — reconciliação dos cartões (PT04-00/02)

Baseline: 96cdb520fcf118ef555ef2e325ce93465836c9ea. Âmbito: as 100 páginas m1–m9/licao-*/index.html.

O novo comando `python scripts/audit_cards.py` extrai o array JSON CARTOES de cada lição sem executar JavaScript da página. Verifica tipos conhecidos, presença de campo de feedback nos cartões interativos, índices de resposta em escolhas e lacunas, lacunas presentes e respostas booleanas em verdadeiro/falso. Falha explicitamente perante uma alteração da contagem baseline de 100 lições.

Resultado executado: 2382 definições de cartões; 655 de leitura; 1727 interativas. Distribuição: ler 655; emparelhar 175; escolha 429; completar 366; vf 328; ordenar 72; frase 93; versos 72; sublinhar 183; calcada 9. Zero problemas nas verificações implementadas.

Os três totais antigos de PT-01 ficam reconciliados para este âmbito exato. São definições no código, não o número mostrado numa tentativa aleatória. Os números de 18 aprofundamentos, 81 questionários e 27 provas permanecem PENDENTES de reconciliação.

Teste do próprio verificador executado: rejeitou seis casos artificiais (índice fora dos limites, índice negativo em lacuna, verdadeiro/falso com string, feedback vazio, lacunas vazias e tipo desconhecido); aceitou um caso válido. Compilação Python aprovada.

Limites: o campo de feedback existir não prova qualidade explicativa. Não valida correção factual, ambiguidades, soluções de sublinhar/ordenar/emparelhar, dados introduzidos posteriormente, todas as variantes, HTML renderizado ou interações. A expressão «zero problemas» refere-se só às verificações listadas.

Ficheiros acrescentados: scripts/audit_cards.py e docs/reconciliacao-cartoes.md. Nenhuma página do site alterada neste lote. Os scripts locais não comitados da fase zero são separados do ficheiro de M9-F03 alterado no PR #6; não foi misturado código do site no PR de auditoria.

PENDENTES e bloqueantes para publicação: validação integral em navegador, mobile, teclado/leitor de ecrã, feedback pedagógico, fontes, desempenho e regressão. PR #5 continua em draft; PR #6 continua separado. Sem merge/publicação. LENTE-03 integrado apenas documentalmente fora do repositório Português.
