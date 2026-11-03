# F2: preparação para revisão

03/11/2026. A F0 está no #165, com 15 verificações aprovadas na cabeça `c87d871d`. A F2 recebeu essa fase por merge e permanece num ramo separado, sem páginas publicadas que carreguem os novos tipos.

## O que já pode ser ensaiado

As peças `lacunas`, `varias`, `montar`, `intruso`, `razao` e `corrigir` usam o adaptador comum. Há barra de ações, pista, revelação em projeção, fotografia com controlos desativados e variantes na repetição. O banco original não é modificado. A escolha de várias afirmações conta classificações corretas, incluindo a rejeição das falsas; a razão avalia o par elemento/indício. O relatório final terá de explicitar estes universos de contagem.

As imagens usam o visor comum do sítio. O crédito compacto fica junto à miniatura e a fonte/licença ficam também no cartão. A impressão tem material inicial próprio, independente da resposta dada no ecrã. Não se usa a fotografia de uma resposta como material inicial para papel.

`scripts/tipos_regras.py` fornece validação, extração dos textos visíveis, conjuntos de opções, dicas e material sem soluções. Os consumidores são `audit_cards.py`, `aquecimentos.py`, `desligar_sala.py`, `medir_opcoes.py` e `opcoes_equilibradas.py`. Os aquecimentos antigos continuam idênticos ao gerador: recursos adicionais só entram quando há um tipo novo.

O painel recebe `f` separado do material inicial, como já acontecia. O documento final é produzido por `scripts/cartoes_papel.py`, função `pagina(cartoes, titulo, base_url=None)` e CLI `dados.json --saida atividade.html`. Inclui enunciado, instrução e material público. Não serializa o banco nem transporta respostas escondidas. O GPT2 confirma a integração F3 através deste consumidor real, não de uma página de substituição construída pelo teste.

No tipo `corrigir`, a contagem distingue a identificação de cada palavra da escolha de cada correção. Um falso positivo volta como decisão de identificação; as formas corretamente escolhidas não são repetidas por causa desse erro.

## Provas executadas

- 72 cenários dos seis tipos: quatro larguras, resposta certa, erro deliberado, projeção, teclado a 390 px, revisão e variante.
- 19 testes dos validadores e consumidores, incluindo dados malformados, retorno por espaço, índices, crédito/licença, pergunta que denuncia o critério, versão de recurso e extração sem soluções.
- 14 testes dos aquecimentos existentes, sem alterar as comparações do gerador.
- 11 casos limite: seis comparações de impressão inicial/final, duas verificações de miniaturas e zoom, texto projetado com 70 palavras, ordem alternativa com pontuação própria e banco num ecrã baixo com Escape.
- Dois cenários adicionais: seis tipos em sequência com sete confirmações exatas; falso positivo em `corrigir`, repetindo só a decisão falhada.
- Quatro testes do gerador final para papel: documento completo sem respostas, recusa de dados inválidos, escape com itálico e CLI idêntica à função.
- Três larguras do documento final, 320, 390 e 1366 px, com enunciados e instruções exatos, impressão, ausência de transbordo e de controlos ou soluções escondidas.

Estas provas não constituem ainda autorização de publicação. A bateria integral da versão candidata passou: 477 testes em 228,025 segundos. As provas locais estão nos ficheiros `f2-unitarios-candidato.log`, `f2-browser-candidato.log` e `f2-limites-candidato.log`, junto às cópias de trabalho. As capturas são atualizadas em `f2-provas-visuais-20261103`, incluindo o documento final para papel.

O primeiro CI confirmou os 477 testes e as 19 camadas, mas revelou uma falha comum a três verificações: o import dos tipos precedia a docstring de `medir_opcoes.py`, usada por `argparse`. A correção repõe a docstring no início, sem alterar limiares. Acrescentou-se uma prova da interface de linha de comandos. A medição `--regra` voltou a verificar 2993 escolhas, com zero denunciadoras. Não se alterou nenhum teste existente para aceitar a falha.

## O que falta para a entrega completa

1. Rever os casos limite e a qualidade visual das seis peças, incluindo os maiores bancos, as variantes e os estados parciais. Os limites de dados não substituem medir um cartão concreto.
2. Fechar a integração com o Lente pela equipa que detém os seus motores, incluindo cor calculada e cópias conferidas. Este ramo não altera esses caminhos.
3. Depois do parecer visual, gravar os seis vídeos no motor real, com passos, código de gravação e hashes. Não há vídeos finais nesta preparação.
4. Fechar com o GPT2 os sete contratos da página final de papel F3, usando `cartoes_papel.pagina`. O limite de 14 versos usa a marca explícita `unidade_partes: "verso"`, já confirmada pelo GPT2. A cobertura anterior dos 72 cartões F3 diz respeito ao fragmento e ao painel, não fecha por si estes sete contratos.
5. Rever e confirmar a fase antes de publicar, depois da F0 e respeitando a prioridade do #164.

A revisão visual do cabeçalho e a nova composição do M4 pertencem ao GPT3. Não há alterações concorrentes a essas páginas neste ramo.
