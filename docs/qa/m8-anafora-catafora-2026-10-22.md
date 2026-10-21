# M8 — Referência anafórica e catafórica

Base: `16663af469c94df317f61a57efe687068a44e5cb` (main, PR #56). Âmbito: apoio existente `m8/anafora-catafora/` e acesso opcional pela M8-F06. Sem alterações ao LENTE.

## Diagnóstico e decisões

Três auditorias paralelas de leitura (pedagogia, acesso/UX e testes), seguidas de integração sequencial. O apoio era acessível pelo catálogo «Tudo o que há no ano», mas não diretamente pela M8-F06.

- A classificação tinha vários pronomes por frase sem indicar o alvo. Cada caso identifica agora a expressão analisada.
- «Ela» pode retomar a poeta ou a terrina. Conservou-se o exemplo: ambas as leituras são anafóricas. O retorno distingue ambiguidade do referente de direção da referência.
- A lacuna pede expressamente a retoma de «a carta»; as alternativas contrastam género/número. Deixa de avaliar como errada uma retoma demonstrativa defensável. O feedback relaciona as expressões concretas e abandona a falsa regra baseada em pontuação.
- Modelo com substituição e explicação → identificação sem modelo à vista → aplicação oral/no caderno, no retorno da escolha final. Ajuda nativa expansível, acionável por teclado. A produção própria não é corrigida automaticamente nem obrigatória para concluir.
- Ligação opcional no menu e no final da M8-F06; regresso à ficha no menu do apoio. Mantêm-se o complemento obrigatório de aspeto, os seis passos, a ordem das chaves certas, os níveis e a chave `epi-pt-anafora-catafora`. Sem alteração ao motor, imagens ou estilos.

A revisão apoia-se na distinção entre expressão e antecedente apresentada na [referência gramatical disponibilizada pela DGE](https://area.dge.mec.pt/gramatica/anafora5.html). Não se concluiu que todas as frases anteriores estavam erradas.

## Verificação executada antes do envio

- 138 testes Python aprovados, incluindo quatro regressões focadas novas.
- Sintaxe dos dez scripts embutidos dos dois HTML aprovados.
- Navegador real, pré-visualização própria em `127.0.0.1:8779/pt/`: seis passos do apoio a 320 px; ajuda por teclado; classificação 4/4; escolha do referente por Enter; erro deliberado na lacuna com correção 1/2; juízos 4/4; escolha final com proposta de aplicação; resultado 45/50 preservado após recarregar.
- Projeção a 1440 px, tamanho grande (28 px), com QR e modelo revisto; acesso opcional visível no menu e no final da M8-F06, retorno visível no menu do apoio. Capturas guardadas na pasta de entrega fora do repositório.

`tests/browser_m8_anafora.py` acrescenta o percurso completo em contextos novos a 320/1440 px, erro deliberado, teclado, retoma, ligações, ausência de transbordo e projeção. Está integrado no workflow geral; a execução remota e a publicação serão confirmadas na entrega associada ao PR. Não considerar a mera presença do teste prova de execução.

## Limites e pendências

Leitor de ecrã, outros motores de navegador, todas as combinações da nova tentativa e observação com alunos não foram executados nesta ronda. Os testes funcionais não demonstram aprendizagem. O rótulo genérico legado «como o poeta» nas lacunas continua a não ser ideal neste apoio de gramática; a revisão desse rótulo deve ser consistente com os restantes complementos, num lote próprio. Não se certificou novamente todo o conteúdo de M1–M9 nem desempenho global.
