# Apresentações de M5 integradas nas lições — 25/10/2026

## Âmbito

As onze lições que já têm uma apresentação de M5 recebem no menu dois acessos diretos: PDF e PowerPoint. Os ficheiros continuam nos endereços existentes. Não se alteram bancos, respostas, critérios, progresso, motor, navegação entre cartões nem recursos partilhados de projeção.

Primeiro lote de versões finais: M5-F09 (11 diapositivos) e M5-F12 (13). As restantes nove apresentações ficam acessíveis, mas não são apresentadas como revistas nesta ronda. Os outros módulos e Cidadania continuam no inventário seguinte.

## Alterações pedagógicas

- M5-F09 conserva os nove diapositivos e acrescenta um modelo de observação/interpretação e produção de 12 minutos no caderno com revisão de 5 minutos. Os exemplos novos estão identificados como inventados. As fontes de contexto ficam nas notas.
- M5-F12 conserva os dez diapositivos, com explicações revistas: os ajustes do relato dependem do contexto, e a pontuação isolada não prova o indireto livre. Acrescenta modelo, produção de 12 minutos e correção comentada de 5 minutos. São versões possíveis, não uma fórmula única de resposta.
- Nos dois ficheiros, as atividades no site/Sala tornam-se opcionais, preservando os QR. Os endereços junto aos QR passam também a ser ligações clicáveis.
- Conservam-se imagens, créditos, formato 16:9, tipografia Arial/Georgia e tabela nativa. O texto do PowerPoint continua editável.

## Verificação e limites

O lote passa os 178 testes Python do repositório. A primeira tentativa teve erros de acesso à pasta temporária do ambiente; repetida com uma pasta temporária no espaço de trabalho, passou integralmente.

Os dois PowerPoint passam integridade do pacote, geometria, contagem de diapositivos, política tipográfica, presença da tabela nativa e reimportação pela ferramenta de apresentações. São verificações estruturais, não abertura no Microsoft PowerPoint. Esta verificação nativa e leitor de ecrã ficam como complementares pendentes.

Todos os diapositivos são renderizados e revistos visualmente antes da publicação. As ligações de ficheiros, menu móvel e versão pública são verificadas no navegador e registadas no relatório do PR.

A exportação PDF direta da ferramenta falhou por uma dependência tipográfica ausente (`#standard-fonts/Helvetica`). Os PDF deste lote reproduzem as imagens dos diapositivos verificados e conservam as ligações clicáveis. O texto nesses PDF não é selecionável. O PowerPoint associado conserva texto e tabela editáveis. Não se alterou a instalação nem a ferramenta para contornar o erro. Atributos locais impedem que o Git transforme os bytes dos dois PDF.

## Fontes preservadas/verificadas

- Centro Português de Fotografia: https://cpf.pt/documento-mes-fundos-e-colecoes-36/
- Centro Nacional de Cultura / Patrimatic, Casa de Camilo: https://www.e-cultura.pt/patrimonio_item/4910
- Eça de Queirós, *Os Maias*, Project Gutenberg 40409: https://www.gutenberg.org/ebooks/40409

## Coordenação

Branch própria `work/pt-apresentacoes-m5-20261025`, separada dos pilotos noturnos. Sem ficheiros do PR LENTE #38, geradores do Claude ou áreas protegidas de Cidadania. O Claude deverá avaliar o lote publicado e os limites documentados; não depende da sua implementação.
