# PT04-00/01 — verificação operacional parcial

Baseline local: 96cdb520fcf118ef555ef2e325ce93465836c9ea. A correção de teclado de M9-F03 está isolada no PR #6 e não foi publicada.

## Executado

- Índice publicado /pt/m9/ aberto em navegador real: duas unidades e ligações para as sete lições presentes.
- Abertura das sete páginas publicadas M9-F01/F02/F03/F04/F10/F05/F07: títulos esperados e controlo Seguinte disponíveis.
- Em cada uma dessas páginas: cliques reais em Seguinte do cartão 1 ao 2 e do 2 ao 3; contador chegou a 3 e novo conteúdo foi apresentado.
- Captura da terceira vista de F07 guardada no relatório local. São testes iniciais, não execução integral das lições.
- Verificação estática dos nove índices: 181 referências locais href/src com ficheiro de destino existente, sem ausências encontradas. Contagem inclui repetições, não 181 recursos únicos. Foram excluídos URLs externos, LENTE, data URIs e fragmentos sem caminho.
- A verificação de ficheiros não testa respostas HTTP, fragmentos, links gerados por JavaScript ou recursos incorporados nos dados dos exercícios.

## Observações editoriais

O índice M9 já referencia os aprofundamentos «Ver e não ver» e «De quem é o convento?». Incluí-los na análise de sobreposição de M9-C/D antes de produzir novas páginas. Não se concluiu ainda suficiência pedagógica dessas atividades.

## Pendências

PENDENTE: respostas certas/erradas em todas as mecânicas, variantes, conclusão, reposição, retoma, persistência, teclado completo, mobile, leitor de ecrã, consola, fontes e desempenho. Não se certificou equivalência byte a byte das páginas publicadas com o commit local.

As restantes 93 lições não foram abertas nesta ronda. A conclusão funcional dos nove módulos permanece pendente. Sem recomendação de publicação, merge ou início de LENTE.
