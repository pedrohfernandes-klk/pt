# M8 — Revisão coerente e fontes de leitura

Base: `c95bee7b82cdbcd30e043a2a608f6d57a80ec874` (PR #57 publicado). Âmbito: M8-F12, seu painel, desafios da unidade 2 e acesso às leituras F03/F04/F05. Sem alterações ao LENTE, aos motores, estilos, imagens, chaves de progresso ou unidades.

## Decisões pedagógicas e de utilização

Três auditorias paralelas de leitura, integração sequencial. Na F12 e no desafio, o hábito deixa de ser apresentado como incompatível com repetição; os pares explicam situações completas, incluindo o limite da inferência sobre «pintava». Mantêm-se respostas e pares.

A comparação deixa de impor uma preferência universal por sugerir. A hipótese é identificada como tal na tarefa de sublinhar; os desafios retomam o critério de comparação com diferenças sustentadas da própria ficha. Uma escolha de vocabulário trabalha inferência sustentada. Dos dois emparelhamentos autor/obra iguais no desafio, conserva-se um; o outro passa a trabalhar quatro retomadas em exemplos inventados. Não se elimina a cobertura dos quatro autores.

O essencial recupera o antecedente de «Ele»; a ajuda correspondente acompanha-o. O modelo e a leitura comparativa continuam disponíveis; há recuperação nos desafios e transferência para novos exemplos e aplicação oral/no caderno.

O painel docente tinha rótulos antigos nos índices 6/7/14/18/19 e oferecia o índice 10, agora leitura, como pergunta de completar. O seletor e o índice foram derivados dos interativos atuais da F12. O lançamento por índice mantém o protocolo existente. Não foi feita emissão para uma turma real.

## Fontes de leitura consultadas

Pedido adicional do utilizador integrado neste lote: ligar a publicação consultada e identificar separadamente a obra primária, sem acrescentar transcrições integrais.

- **M8-F05:** Ana Luísa Amaral, «Prece no Mediterrâneo», *Ágora*, Assírio & Alvim, 2019, segundo a reprodução na [Seara Nova, 07-08-2023](https://searanova.publ.pt/2023/08/07/poesia-prece-no-mediterraneo/). A página associa-se ao n.º 1760, Outono de 2022; a data da publicação web é distinta. Maria João Milhano é a assinatura da rubrica, não a autora do poema.
- **M8-F03:** [RTP Ensina — «Uma Pequenina Luz»](https://ensina.rtp.pt/artigo/jorge-sena-poesia/), de Jorge de Sena; programa *Voz*, 2005, leitura de Carmen Dolores. A RTP não identifica o livro. A referência a *Fidelidade* (1958) foi confirmada em Augusto Santos Silva, *Se numa noite de inverno uma estudante* (FLUP, 2022), [p. 5, nota 2](https://ler.letras.up.pt/uploads/ficheiros/19616.pdf#page=5), que remete para Sena, 1978, pp. 52–53.
- **M8-F04:** [RTP Ensina — «As Palavras»](https://ensina.rtp.pt/artigo/as-palavras-de-eugenio-de-andrade/), de Eugénio de Andrade; *Voz*, 2005, leitura de Beatriz Batarda. Já existia acesso associado ao vídeo; a referência de leitura foi reformulada para identificar a publicação efetivamente consultada. A página RTP atribui o poema a *Até Amanhã*, enquanto o registo indexado da [Poetry International](https://www.poetryinternational.com/en/poets-poems/poems/poem/103-4834_WORDS) aponta *Coração do Dia*, 1958, e apresenta uma variante de concordância. A abertura direta desta última fonte devolveu 403. Retirou-se da referência desta leitura a atribuição categórica a *Até Amanhã*; a colação de edição fica pendente. Não se alterou o poema nem se escolheu uma variante por palpite.

As três publicações textuais foram abertas e lidas. Os acessos ficam junto dos cartões de leitura e numa ajuda expansível da comparação F12. Para «George» e para a «Carta a meus filhos», mantém-se a remissão para o manual: não foi localizada/verificada neste lote uma reprodução alternativa. A pesquisa cobre estas leituras do M8, não o corpus inteiro de M1–M9.

## Verificações executadas antes do envio

- 144 testes Python aprovados (seis regressões novas); sintaxe de 35 scripts nos seis HTML alterados aprovada.
- Navegador real: quatro novos pares de referência, feedback e ausência visual de corte horizontal a 320 px; pares aspetuais e escolha habitual por Enter; resultado guardado após recarregar em fixture isolada com chave QA; seletor docente escolhendo o índice 8 correto; ajuda das fontes aberta por teclado; fonte Seara Nova junto da leitura a 390 px; essencial normal da F12 em projeção grande a 1440 px com QR.
- Fixtures locais copiam dados autênticos e usam chaves QA fora do repositório. Não representam uma tentativa normal completa do módulo.
- Novo `browser_m8_f12_revisao.py`: renderização de fontes, itens alterados e novo desafio em 320/1440; teclado, conclusão de itens, painel e projeção. O workflow M8/M4 já percorre a F12 completa a 390 px. Execução remota e publicação devem ser confirmadas na entrega do PR; configuração de um teste não significa execução aprovada.

## Limites

Não executados: leitor de ecrã, outros motores, todas as combinações de seleção, turma real, visionamento/áudio dos leitores externos, estudo de desempenho global e observação de aprendizagem. Os testes funcionais não demonstram aprendizagem. A divergência bibliográfica de Eugénio fica explicitamente pendente; o acesso ao texto e a atribuição de autoria estão identificados, sem apresentar uma edição duvidosa como certa.
