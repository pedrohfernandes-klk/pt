# Créditos atrás de um botão «i» (pedido pt-2)

05/11/2026. Decisões 153 e 162. O docente: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir». Plano: `plano-creditos-i-20261105.md` (secções 1, 2.1, 2.3, 3 e 4). Sobre o main `b3ee0f9c`.

Regra de fundo: o crédito acompanha a imagem, fechado; o que diz o que se vê e serve a pergunta fica à vista. Os créditos não se encurtam: cada palavra passa para dentro do «i». As licenças CC ganham a ligação para o texto da licença (`rel="license"`), que a impressão escreve por extenso.

## A peça comum

| Ficheiro | Função |
| --- | --- |
| `assets/info-i.css` | A peça: variante «canto» (no canto inferior direito da imagem, dentro de um `.com-i`) e variante «linha» (`.info-i--linha`, logo por baixo); foco desenhado para dentro; temas pelas variáveis de cada casa; cores forçadas; projeção discreta; impressão por extenso com o endereço da licença, sem o «i»; a linha `.fundo-acoes` dos fundos animados (o botão «Parar o desenho» ao lado do «i», fora dele) e a sua regra de impressão. |
| `assets/info-i.js` | Escape fecha e devolve o foco ao «i» (cede o Escape a um diálogo aberto, como o ampliador); um clique fora fecha; um aberto de cada vez (o `name="info-i"` já o faz nos navegadores atuais); fecha tudo quando a projeção começa e marca `data-ii-projecao` nas lições com `?projetar=1`. Não grava nada. |
| `tests/fixtures/info-i-sha256.json` | O sha256 dos dois ficheiros, igual no Português e no Lente. |
| `tests/fixtures/info-i.html` | Página de ensaio: canto, linha, imagem pequena, imagem dentro de ligação, cartão, ficha de documento visual e linha de um fundo animado. |

## Família P7: crédito puro nas lições M1 e M4 (27 páginas, 47 figuras)

Camada literal `creditos_i_20261105` (no topo da cadeia, por cima de `exame_contexto_20261105`), construída por `scripts/creditos_i_20261105.py`. A `span.moldura` passa a `div.moldura.com-i`; o «i» («Créditos da imagem») fica depois da imagem; cada página carrega a peça comum. As imagens com menos de 240 px de largura no cartão (a gravura de D. Dinis e a cantiga de Codax) levam a variante «linha». As datas aproximadas e os intervalos de anos não partem (`span.nb`), nem «cap. I» (espaço inseparável), pela decisão 152.

Fica à vista o que vem depois dos dois pontos e diz o que se vê; o resto sai inteiro para o «i». As outras legendas eram só crédito: o `figcaption` sai e o `alt` de cada imagem já diz o que se vê.

| Lições | Fica à vista | Vai para o «i» |
| --- | --- | --- |
| M1-F04 | Cantigas de D. Dinis. | *Cancioneiro da Biblioteca Nacional*, cópia do século XVI. Domínio público. |
| M1-F07 | Pormenor: as muralhas. | *Crónicas* de Froissart, século XV (pormenor). Domínio público. |
| M1-F07 | Pormenor: o arraial. | *Crónicas* de Froissart, século XV (pormenor). Domínio público. |
| M4-F01, M4-F02, M4-F15 | A primeira página do sermão. | *Sermoens* de Vieira, Lisboa, 1682. Domínio público. |
| M4-F01, M4-F02 | O começo do cap. I. | *Sermoens*, Lisboa, 1682. Domínio público. |
| M4-F11 | A nota por baixo do título. | *Sermoens* de Vieira, Lisboa, 1682. Domínio público. |
| M4-F08 | A lista de personagens. | *Frei Luiz de Sousa*, primeira edição, 1844. Domínio público. |
| M4-F09, M4-F26 | A lista das pessoas. | *Frei Luiz de Sousa*, primeira edição, 1844. Domínio público. |
| as outras 35 figuras | nada (sai o `figcaption`) | a legenda inteira, letra a letra; «CC BY-SA 4.0» com a ligação para a licença |

O montante (`aulas-claras/licao_v2.py`, `fig()`, nas fontes) ainda escreve a legenda longa: muda no mesmo pedido, nas fontes.

## Família P9: documento visual (6 lições geradas)

`scripts/imagens_licoes_20261101.py` e `scripts/templates/licao-20261101.html.tpl`, regenerados com `scripts/gerar_licoes_20261101.py` (M3-F19, M5-F17, M6-F14, M8-F13, M8-F14, M9-F14). A linha da licença com «Fonte ↗», a ficha («Identificação do documento visual») e «Consultar a fonte e os direitos ↗» passam inteiras para o «i» (variante «linha», num `div.info-i-texto`, porque a ficha é uma tabela). O «i» fica logo por baixo do canto direito da imagem centrada; aberta, a ficha ocupa a largura da coluna (até 34rem) sem deslocar a imagem. A legenda que diz o que se vê fica à vista e «Abrir a imagem inteira» fica igual, filha da figura. O molde passa a carregar a peça comum (as 16 lições geradas).

## Família P10: Pessoa, cerca de 1914 (3 páginas)

M7-F01, M7-F05 e a galeria «Para ver» do mapa M7. A decisão 153 substitui a regra de 01/11 da varredura de formatação («crédito visível na peça `.tabela`, sem controlo de abertura»): os seis campos passam, letra a letra, para o «i». Variante «linha»: nas lições, a fotografia tem 220 a 253 px de largura no cartão (medida a 320, 390, 852 e 1366 px); na galeria, as miniaturas têm 150 px ou pouco mais. Nas lições, a `span.moldura` passa a `div.moldura.com-i`; na galeria, o «i» fica entre a imagem e a legenda («Créditos da imagem: Fernando Pessoa», porque a galeria terá vários «i» depois da P16).

| Fica à vista | Vai para o «i» |
| --- | --- |
| Fernando Pessoa, cerca de 1914. (e, no mapa, a ligação «Lição M7-F01») | Fotógrafo não identificado; retrato de Fernando Pessoa com chapéu; cerca de 1914 (data incerta); reprodução no Wikimedia Commons, original sem instituição indicada; domínio público (ligação para File:PessoaChapeu.jpg). |

## Família P11: dupla exposição de «Chuva Oblíqua» (M7-F34)

O «i» não pode viver dentro do `div.dupla-foto`, que tem `role="img"`: a fotografia e o «i» ficam juntos num `div.com-i`, que toma a largura da fotografia (até 560 px, centrada; um `<style>` na cabeça da página, com a peça). Variante «canto».

| Fica à vista | Vai para o «i» |
| --- | --- |
| Os botões dos versos e «Toca num pedaço do verso: acende-se o seu plano.» | Duas fotografias sobrepostas: um jardim de Lisboa em 1907 e o Tejo diante da Praça do Comércio, cerca de 1910 (H. C. White Co. e National Photo Company; Biblioteca do Congresso dos EUA, sem restrições conhecidas). |

## Família P12: retratos do «Em paralelo» (4 lições, 8 retratos)

O `p.rosto-c` sai inteiro para um «i» da variante «linha», logo por baixo do retrato redondo de 76 px e alinhado à direita dele; aberto, o crédito ocupa a largura da coluna e o «i» não muda de sítio (regra em `assets/pt-lessons/aula-clara.css`). Cada parágrafo era só crédito: o `alt` do retrato e o título da coluna dizem o que se vê. Com dois retratos no cartão, o nome acessível junta a identificação: «Créditos da imagem: Santo António», «… António Vieira», «… Almeida Garrett», «… ilha de San Simón», «… Pergaminho Vindel».

| Lições | Vai para o «i» (nada fica à vista) |
| --- | --- |
| M1-F19 | Ilha de San Simón, ria de Vigo (Iago Pillado, 2024). CC BY-SA 4.0 (com a ligação para a licença). |
| M1-F19 | Pergaminho Vindel, com «Ondas do mar de Vigo». Domínio público. |
| M4-F01, M4-F02 | Garcia Fernandes (pormenor) |
| M4-F01, M4-F02, M4-F11 | Retrato, séc. XVIII (pormenor) (com espaço inseparável em «séc. XVIII», decisão 152) |
| M4-F11 | José Malhoa, 1881 |

## Família P13: crédito colado à explicação (3 lições e 3 painéis)

A frase do crédito no fim do campo `f` (a explicação que aparece depois de responder) sai da explicação e vai, letra a letra, para o «i» da imagem do campo `ver` da mesma pergunta; o itálico do motor (`_…_`) passa a `<i>`. Nas lições, a imagem ocupa a largura do cartão: variante «canto». O motor (`assets/pt-lessons/jogo.js`, `corpo()`) põe o «i» fora da figura que amplia, que é um botão (`figure.ver-fig[role=button]`), num `div.com-i.ver-com-i`; tocar no «i» abre os créditos e não amplia, e tocar na imagem continua a ampliar (a margem passa para a moldura, em `aula-clara.css`). Nos painéis, a imagem do material tem 154 a 346 px de largura (30vh de altura): variante «linha», com a moldura ajustada à imagem (um `<style>` na cabeça de cada painel).

| Lição e painel | Fica na explicação | Vai para o «i» da imagem |
| --- | --- | --- |
| M4-F01 | … quer ser mais do que é. | Cromolitografia: Allen & Ginter, *Peixe-voador* (série *Fish from American Waters*), 1889, The Met. Domínio público. |
| M4-F04 | … «como hão de comer, e como se hão de comer». | Pintura: Umberto Boccioni, *A cidade que sobe*, 1910, MoMA. Domínio público. |
| M4-F11 | … «O mais forte» julga: opinião. | Imagem: *Frei Luiz de Sousa*, primeira edição, 1844. Domínio público. |

A peça comum mudou numa coisa: um «i» aberto dentro de um diálogo (um cartão montado num ecrã sobreposto, `[aria-modal="true"]`) fecha-se primeiro com o Escape; o diálogo só se fecha com o Escape seguinte. O ampliador, que fica por cima do «i», continua a receber o Escape. O sha256 de `assets/info-i.js` foi atualizado no registo comum, que vai igual para o Lente.

O montante, nas fontes, fica por fazer como na P7: `aulas-claras/licao_v2.py` (o `rosto-c` do «Em paralelo») e os dados das lições M4 (o campo `f`).

## Família P14: «Pensar devagar» (17 páginas)

Uma figura por página, no primeiro cartão (`figure.fig-rev`, com a imagem pelo endereço publicado). Só sai o `span.fr-cred`: passa letra a letra para um «i» da variante «canto», dentro da moldura (a `span.fr-moldura` passa a `div.fr-moldura.com-i`; a imagem tem 272 px de largura ou mais nas quatro larguras medidas). A primeira letra sobe a maiúscula, porque o crédito abre o «i» sozinho («impressão de João Álvares…» passa a «Impressão de João Álvares…»). O `span.fr-leg`, que diz o que se vê e serve a pergunta, fica à vista, sozinho no `figcaption`; o ampliador mostra só essa legenda. A licença CC de Mafra ganha a ligação (`rel="license"`), também quando o crédito já traz a ligação para o Commons.

| Página | Fica à vista (fr-leg, igual) | Vai para o «i» (fr-cred) |
| --- | --- | --- |
| m1-promessa-do-cronista | O cerco de Lisboa de 1384 numa iluminura francesa: … | Crónicas de Jean Froissart (iluminura). Domínio público. commons.wikimedia.org |
| m1-voz-emprestada | Pergaminho Vindel: as cantigas de Martim Codax com a música. … | Domínio público. commons.wikimedia.org |
| m2-ines-escolhe-duas-vezes | Copilaçam de todalas obras de Gil Vicente, 1562: … | Impressão de João Álvares, 1562 (reprodução de Victorcouto). Domínio público. commons.wikimedia.org |
| m2-maquina-de-rir | Hogarth, O público a rir, 1733: … | CC0. commons.wikimedia.org |
| m3-soneto-raciocinio | Rimas de Camões, 1595: … | Página impressa de 1595. Domínio público. commons.wikimedia.org |
| m3-velho-restelo-juri | Os Lusíadas, 1572: … | Luís de Camões. Academia Brasileira de Letras, via Wikimedia Commons. Domínio público. commons.wikimedia.org |
| m4-frei-luis-quem-sabia | Frei Luís de Sousa, 1844: … | Almeida Garrett (edição de 1844, BNP). Domínio público. commons.wikimedia.org |
| m4-sermao-tribunal | Santo António a pregar aos peixes, Garcia Fernandes, cerca de 1535: … | Domínio público. commons.wikimedia.org |
| m5-o-pais-ou-eles | O Hotel Central, cerca de 1910: … | Domínio público. commons.wikimedia.org |
| m5-quem-podia-ter-feito-diferente | A Cadeia da Relação do Porto, 1850: … | Lucas de Almeida Marrão (BNP). Domínio público. commons.wikimedia.org |
| m6-antero-viagem-ao-nada | Antero de Quental por Columbano, 1889: … | Domínio público. commons.wikimedia.org |
| m6-cesario-noite-inteira | Varinas na Ribeira Nova, cerca de 1900: … | José Artur Leitão Bárcia (Arquivo Municipal de Lisboa). Domínio público. commons.wikimedia.org |
| m7-fingidor-maquina | Fernando Pessoa em 1929: o fingidor, fotografado. | Autor não identificado (fotografia de 1929). Domínio público. commons.wikimedia.org |
| m7-quatro-vozes-um-problema | Orpheu, n.º 2, 1915: … | Revista Orpheu. Domínio público. commons.wikimedia.org |
| m8-poema-testemunha | Goya, 3 de maio de 1808: … | Domínio público. commons.wikimedia.org |
| m9-de-quem-e-o-convento | O Palácio-Convento de Mafra: de quem é esta pedra? | Fotografia de Alvesgaspar, 2013. CC BY-SA 3.0 (com a ligação para a licença). commons.wikimedia.org |
| m9-ver-e-nao-ver | A Passarola: o que uns viram voar e outros não viram. | Bartolomeu de Gusmão (fac-símile). Domínio público. commons.wikimedia.org |

A atribuição CC BY-SA 3.0 de Mafra não trazia o nome do fotógrafo no `fr-cred` de origem. 06/11/2026 (revisão): confirmado no Commons (File:Mafra_May_2013-2.jpg: autor e carregamento de Alvesgaspar, 8 de maio de 2013, CC BY-SA 3.0), o mesmo crédito da galeria do mapa M9; o «i» abre com «Fotografia de Alvesgaspar, 2013.». Falta corrigir o crédito nas fontes (`imagens-comuns.mjs`). O montante (`imagens-comuns.mjs`, nas fontes) ainda escreve o `fr-cred` à vista.

## Família P15: exercícios «Olhar» (4 páginas)

M1 `olhar-ajuda` e `olhar-andeiro`, M4 `olhar-lupi`, M7 `olhar-pessoa`. O crédito é montado pelo motor de cada página (`imagem()`), a partir dos campos `credito` e `creditoUrl`; o varrimento estático não o vê, e `tests/test_creditos_i.py` e `tests/browser_creditos_i.cjs` conferem-no à parte. O motor passa a pôr a imagem e o «i» num `div.com-i.olhar-com-i`, que toma a largura da imagem, centrada (um `<style>` na cabeça, com a peça), e o crédito dentro do «i», com o itálico (`_…_`) em `<i>` e as palavras «Wikimedia Commons» a ligar ao `creditoUrl`: a ligação, que não se via, passa a viver no «i». O `p.credito` deixa de existir. No campo `credito`, os pontos médios passam a pontos finais (as regras da casa não os querem dentro de frases) e «c. 1860» ganha espaço inseparável; nenhuma palavra sai. Variante «canto», salvo o retrato de Pessoa (220 a 229 px de largura): «linha».

| Exercício | Antes (p.credito, à vista) | No «i» (com a ligação creditoUrl) |
| --- | --- | --- |
| olhar-ajuda | _Cancioneiro da Ajuda_, fólio 21r · domínio público · Wikimedia Commons | *Cancioneiro da Ajuda*, fólio 21r. Domínio público. Wikimedia Commons. |
| olhar-andeiro | José de Sousa Azevedo, _Morte do Conde Andeiro_ (c. 1860), Museu Nacional de Soares dos Reis, Porto · domínio público · Wikimedia Commons | José de Sousa Azevedo, *Morte do Conde Andeiro* (c. 1860), Museu Nacional de Soares dos Reis, Porto. Domínio público. Wikimedia Commons. |
| olhar-lupi | Miguel Ângelo Lupi, _D. João de Portugal_ (1863) · domínio público · Wikimedia Commons | Miguel Ângelo Lupi, *D. João de Portugal* (1863). Domínio público. Wikimedia Commons. |
| olhar-pessoa | Fernando Pessoa, fotografia de 1914 · domínio público · Wikimedia Commons | Fernando Pessoa, fotografia de 1914. Domínio público. Wikimedia Commons. |

O montante (`interativos.mjs`, nas fontes) ainda escreve o `p.credito` e os pontos médios.

## Família P16: galeria «Para ver» dos mapas do módulo (9 páginas, 78 figuras)

Cada figura ganha um «i» da variante «linha» entre a imagem e a legenda (as miniaturas têm 150 px ou pouco mais), como o de Pessoa (P10). O «i» leva o crédito inteiro, letra a letra: a identificação, a licença (as CC com a ligação para o texto da licença) e, quando há, a ligação «Fonte: …». À vista ficam o que se vê e a ligação «Lição Mx-Fyy»: a identificação sem o parêntese final, que traz o autor, a data, o acervo e o fotógrafo (secção 1.1 do plano, legendas mistas); sem parêntese final, a identificação inteira. O nome de cada «i» junta a identificação que fica à vista («Créditos da imagem: D. João III»); quando duas legendas à vista coincidem no mesmo mapa (dois retratos de Almeida Garrett no M4, dois de Antero de Quental no M6), junta a identificação inteira. As datas aproximadas e os intervalos de anos não partem (`span.nb`), nem «séc. XVIII» e «n.º 39» (espaço inseparável). As duas figuras do M4 sem ligação para uma lição (Almeida Garrett por Guglielmi e a cabeça de Demóstenes) ficam só com a legenda curta.

| Mapa | Fica à vista | Vai para o «i» |
| --- | --- | --- |
| M1 | Pergaminho Vindel: cantigas de Martim Codax. (e «Lição M1-F01») | Pergaminho Vindel: cantigas de Martim Codax. Domínio público. |
| M1 | *Cancioneiro da Ajuda*, fólio 21r. (e «Lição M1-F04») | *Cancioneiro da Ajuda*, fólio 21r. Domínio público. |
| M1 | *Morte do Conde Andeiro*. (e «Lição M1-F06») | *Morte do Conde Andeiro* (José de Sousa Azevedo, c. 1860). Domínio público. |
| M1 | Fernão Lopes (retrato imaginado). (e «Lição M1-F06») | Fernão Lopes (retrato imaginado, Pollini). Domínio público. |
| M1 | Pergaminho Vindel exposto. (e «Lição M1-F01») | Pergaminho Vindel exposto (fotografia de Luis Miguel Bugallo Sánchez, 2017). CC BY-SA 4.0. |
| M1 | «Ondas do mar de Vigo», transcrição de Pedro Vindel. (e «Lição M1-F01») | «Ondas do mar de Vigo», transcrição de Pedro Vindel (1915). Domínio público. |
| M1 | Ilha de San Simón, ria de Vigo. (e «Lição M1-F01») | Ilha de San Simón, ria de Vigo (fotografia de Iago Pillado, 2024). CC BY-SA 4.0. |
| M1 | Uma página do *Cancioneiro da Biblioteca Nacional*. (e «Lição M1-F01») | *Cancioneiro da Biblioteca Nacional*, página (cópia do século XVI). Domínio público. |
| M1 | D. Dinis, gravura em *Diálogos de Vária História*. (e «Lição M1-F04») | D. Dinis, gravura em *Diálogos de Vária História* (Pedro de Mariz, 1594). Domínio público. |
| M1 | Figura identificada como Fernão Lopes, Painéis de São Vicente. (e «Lição M1-F06») | Figura identificada como Fernão Lopes, Painéis de São Vicente (Nuno Gonçalves, século XV). Domínio público. |
| M1 | O cerco de Lisboa de 1384, iluminura das Crónicas de Froissart. (e «Lição M1-F06») | O cerco de Lisboa de 1384, iluminura das Crónicas de Froissart (século XV). Domínio público. |
| M2 | *Copilaçam de todalas obras de Gil Vicente* (Lisboa, 1562), frontispício. (e «Lição M2-F01») | *Copilaçam de todalas obras de Gil Vicente* (Lisboa, 1562), frontispício. Domínio público. |
| M2 | Convento de Cristo, Tomar. (e «Lição M2-F01») | Convento de Cristo, Tomar (fotografia de Ingo Mehling, 2022). CC BY-SA 4.0. |
| M2 | D. João III. (e «Lição M2-F01») | D. João III (Anthonis Mor, 1552). Domínio público. |
| M2 | Trajes de portugueses, *Trachtenbuch*. (e «Lição M2-F01») | Trajes de portugueses, *Trachtenbuch* (Christoph Weiditz, década de 1530). Domínio público. |
| M3 | Luís de Camões. (e «Lição M3-F02») | Luís de Camões (Fernão Gomes, c. 1577). Domínio público. |
| M3 | *Rimas* de Luís de Camões, primeira edição (1595), página de rosto. (e «Lição M3-F02») | *Rimas* de Luís de Camões, primeira edição (1595), página de rosto. Domínio público. |
| M3 | Túmulo de Luís de Camões, Mosteiro dos Jerónimos. (e «Lição M3-F02») | Túmulo de Luís de Camões, Mosteiro dos Jerónimos (fotografia de ProtoplasmaKid, 2019). CC BY-SA 4.0. |
| M3 | Lavadeiras portuguesas, *Costume of Portugal*. (e «Lição M3-F02») | Lavadeiras portuguesas, *Costume of Portugal* (Henri L'Evêque, 1814). Domínio público. |
| M3 | *Os Lusíadas*, primeira edição (1572), frontispício. (e «Lição M3-F05») | *Os Lusíadas*, primeira edição (1572), frontispício. Domínio público. Fonte: Academia Brasileira de Letras, via Wikimedia Commons. |
| M3 | Vasco da Gama, *Livro de Lisuarte de Abreu*. (e «Lição M3-F05») | Vasco da Gama, *Livro de Lisuarte de Abreu* (c. 1560). Domínio público. |
| M3 | Nau São Bento, *Livro de Lisuarte de Abreu*. (e «Lição M3-F05») | Nau São Bento, *Livro de Lisuarte de Abreu* (século XVI). Domínio público. |
| M3 | Prato com esfera armilar e armas de Portugal, porcelana chinesa. (e «Lição M3-F05») | Prato com esfera armilar e armas de Portugal, porcelana chinesa (c. 1520-1540, The Met). Domínio público (The Met, Open Access). |
| M4 | *Sermão de Santo António aos Peixes*, em *Sermoens*. (e «Lição M4-F01») | *Sermão de Santo António aos Peixes*, em *Sermoens* (Lisboa, 1682). Domínio público. |
| M4 | Padre António Vieira. (e «Lição M4-F01») | Padre António Vieira (retrato, início do séc. XVIII). Domínio público. |
| M4 | D. João de Portugal. (e «Lição M4-F08») | D. João de Portugal (Miguel Ângelo Lupi, 1863). Domínio público. |
| M4 | Almeida Garrett (Pedro Augusto Guglielmi, 1844). | Almeida Garrett (Pedro Augusto Guglielmi, 1844). Domínio público. |
| M4 | Santo António a pregar aos peixes. (e «Lição M4-F01») | Santo António a pregar aos peixes (Garcia Fernandes, c. 1535-1540, MNAA). Domínio público. |
| M4 | Peixe-voador, cromolitografia da série *Fish from American Waters*. (e «Lição M4-F01») | Peixe-voador, cromolitografia da série *Fish from American Waters* (Allen & Ginter, 1889, The Met). Domínio público (The Met, Open Access). |
| M4 | Almeida Garrett (José Malhoa, 1881). (e «Lição M4-F07») | Almeida Garrett (José Malhoa, 1881). Domínio público. |
| M4 | *Frei Luís de Sousa*, lista de personagens da primeira edição. (e «Lição M4-F08») | *Frei Luís de Sousa*, lista de personagens da primeira edição (1844). Domínio público. |
| M4 | Sala das sessões da Câmara dos Deputados, São Bento. (e «Lição M4-F14») | Sala das sessões da Câmara dos Deputados, São Bento (fotografia de José Artur Leitão Bárcia, 1909). Domínio público. |
| M4 | Cícero denuncia Catilina no Senado. (e «Lição M4-F10») | Cícero denuncia Catilina no Senado (Cesare Maccari, 1889). Domínio público. |
| M4 | Cabeça de Demóstenes, mármore, cópia romana. | Cabeça de Demóstenes, mármore, cópia romana (século II d.C., The Met). Domínio público (The Met, Open Access). |
| M4 | D. Sebastião. (e «Lição M4-F26») | D. Sebastião (Cristóvão de Morais, c. 1571-1574, MNAA). Domínio público. |
| M5 | Camilo Castelo Branco. (e «Lição M5-F02») | Camilo Castelo Branco (fotografia da União, Photographia da Casa Real, Porto, 1882). Domínio público. |
| M5 | Interior da Cadeia da Relação do Porto. (e «Lição M5-F02») | Interior da Cadeia da Relação do Porto (Lucas de Almeida Marrão, c. 1850). Domínio público. |
| M5 | Cadeia da Relação do Porto, hoje Centro Português de Fotografia. (e «Lição M5-F02») | Cadeia da Relação do Porto, hoje Centro Português de Fotografia (fotografia de Reis Quarteu, 2021). CC BY-SA 4.0. |
| M5 | Eça de Queirós. (e «Lição M5-F10») | Eça de Queirós (Fotografia Guedes, Porto, c. 1895). Domínio público. |
| M5 | *Os Maias*, primeira edição (1888), volume 1, página de rosto. (e «Lição M5-F10») | *Os Maias*, primeira edição (1888), volume 1, página de rosto. Domínio público. Fonte: Wikimedia Commons. |
| M5 | Praça dos Remolares, Lisboa, gravura do *Archivo Pittoresco*. (e «Lição M5-F10») | Praça dos Remolares, Lisboa, gravura do *Archivo Pittoresco* (Francisco Augusto Nogueira da Silva, 1860). Domínio público. |
| M5 | Hotel Central, Lisboa. (e «Lição M5-F10») | Hotel Central, Lisboa (fotografia de Joshua Benoliel, c. 1910). Domínio público. |
| M6 | Antero de Quental (fotografia, c. 1887). (e «Lição M6-F01») | Antero de Quental (fotografia, c. 1887, publicada em In Memoriam, 1896). Domínio público. |
| M6 | Antero de Quental (Columbano Bordalo Pinheiro, 1889). (e «Lição M6-F01») | Antero de Quental (Columbano Bordalo Pinheiro, 1889, MNAC). Domínio público. |
| M6 | Jardim Botânico de Coimbra. (e «Lição M6-F01») | Jardim Botânico de Coimbra (fotografia de J. Lévy & Co, década de 1880). Domínio público. |
| M6 | Cesário Verde. (e «Lição M6-F07») | Cesário Verde (retrato de Columbano Bordalo Pinheiro em *O Livro de Cesário Verde*, 1887). Domínio público. |
| M6 | «O Sentimento dum Ocidental» em *O Livro de Cesário Verde* (1887), primeira página. (e «Lição M6-F07») | «O Sentimento dum Ocidental» em *O Livro de Cesário Verde* (1887), primeira página. Domínio público. |
| M6 | Mercado de peixe na Ribeira Nova, Lisboa. (e «Lição M6-F07») | Mercado de peixe na Ribeira Nova, Lisboa (fotografia de José Artur Leitão Bárcia, c. 1900). Domínio público. |
| M6 | Estação original do Cais do Sodré. (e «Lição M6-F07») | Estação original do Cais do Sodré (fotografia da década de 1890, publicada pela CP em 1996). Domínio público. |
| M7 | Casa Fernando Pessoa. (e «Lição M7-F04») | Casa Fernando Pessoa (fotografia de Lijealso, 2008). CC BY 3.0. |
| M7 | «Tabacaria» na *Presença*, n.º 39, julho de 1933. (e «Lição M7-F06») | «Tabacaria» na *Presença*, n.º 39, julho de 1933 (fotografia de Pmms2005). CC BY-SA 4.0. |
| M7 | *Mensagem*, 1.ª edição. (e «Lição M7-F08») | *Mensagem*, 1.ª edição (1934). Domínio público. |
| M7 | Fernando Pessoa em 1929. (e «Lição M7-F01») | Fernando Pessoa em 1929 (fotografia, autor não identificado). Domínio público. |
| M7 | Revista *Orpheu*, n.º 2 (1915), capa. (e «Lição M7-F01») | Revista *Orpheu*, n.º 2 (1915), capa. Domínio público. |
| M7 | «Tabacaria» na revista *Presença*, n.º 39 (julho de 1933), página 2. (e «Lição M7-F06») | «Tabacaria» na revista *Presença*, n.º 39 (julho de 1933), página 2. Domínio público. |
| M7 | Café A Brasileira, Chiado. (e «Lição M7-F01») | Café A Brasileira, Chiado (fotografia de dirk.olbertz, 2010). CC BY 2.0. |
| M7 | *Condução do rebanho*. (e «Lição M7-F04») | *Condução do rebanho* (Silva Porto, 1893, Museu Soares dos Reis; fotografia de Joseolgon, 2016). CC BY-SA 4.0. |
| M7 | *Passagem de gado*. (e «Lição M7-F04») | *Passagem de gado* (João Cristino da Silva, 1867, MNAC; fotografia de Pedro Ribeiro Simões, 2019). CC BY 2.0. |
| M7 | Horácio, gravura no frontispício das *Oeuvres*. (e «Lição M7-F05») | Horácio, gravura no frontispício das *Oeuvres* (1735, Rijksmuseum). CC0. |
| M7 | Busto de Epicuro, Altes Museum, Berlim. (e «Lição M7-F05») | Busto de Epicuro, Altes Museum, Berlim (fotografia de Yair Haklai, 2019). Domínio público. |
| M7 | Busto do «Pseudo-Séneca», British Museum. (e «Lição M7-F05») | Busto do «Pseudo-Séneca», British Museum (fotografia de Marie-Lan Nguyen, 2011). Domínio público. |
| M7 | Tavira, ponte sobre o Gilão. (e «Lição M7-F06») | Tavira, ponte sobre o Gilão (fotografia de Marc Ryckaert, 2007). CC BY-SA 4.0. |
| M7 | *A cidade que sobe*. (e «Lição M7-F06») | *A cidade que sobe* (Umberto Boccioni, 1910, MoMA). Domínio público. |
| M7 | Casa Havaneza, tabacaria do Chiado desde 1864. (e «Lição M7-F06») | Casa Havaneza, tabacaria do Chiado desde 1864 (fotografia de Martapgoncalves, 2020). CC BY-SA 4.0. |
| M7 | D. Sebastião. (e «Lição M7-F08») | D. Sebastião (Cristóvão de Morais, c. 1571-1574, MNAA). Domínio público. |
| M7 | Figura identificada como o Infante D. Henrique, Painéis de São Vicente. (e «Lição M7-F08») | Figura identificada como o Infante D. Henrique, Painéis de São Vicente (Nuno Gonçalves, século XV). Domínio público. |
| M7 | *Aparição do Adamastor*. (e «Lição M7-F08») | *Aparição do Adamastor* (Carlos Reis, antes de 1940). Domínio público. |
| M8 | *Os fuzilamentos de 3 de maio de 1808*. (e «Lição M8-F01») | *Os fuzilamentos de 3 de maio de 1808* (Francisco de Goya, 1814, Museo del Prado). Domínio público. |
| M8 | Rua do Alecrim, Lisboa. (e «Lição M8-F08») | Rua do Alecrim, Lisboa (fotografia de Roger Wollstadt, 1968). CC BY-SA 2.0. |
| M8 | Estação do Rossio, Lisboa. (e «Lição M8-F08») | Estação do Rossio, Lisboa (fotografia de Jorge Franganillo, 2024). CC BY 2.0. |
| M8 | Relógio de bolso. (e «Lição M8-F08») | Relógio de bolso (Robert Roskell, 1820-1821, The Met). Domínio público (The Met, Open Access). |
| M9 | Palácio-Convento de Mafra, fachada. (e «Lição M9-F01») | Palácio-Convento de Mafra, fachada (fotografia de Alvesgaspar, 2013). CC BY-SA 3.0. |
| M9 | Biblioteca do Palácio Nacional de Mafra. (e «Lição M9-F01») | Biblioteca do Palácio Nacional de Mafra (fotografia de Hipersyl, 2026). CC BY 4.0. |
| M9 | D. João V. (e «Lição M9-F01») | D. João V (Domenico Duprà, 1725, Biblioteca Joanina). Domínio público. |
| M9 | A Passarola de Bartolomeu de Gusmão, desenho do século XVIII. (e «Lição M9-F01») | A Passarola de Bartolomeu de Gusmão, desenho do século XVIII (fac-símile, BNP). Domínio público. |
| M9 | Casa dos Bicos, Lisboa, sede da Fundação José Saramago. (e «Lição M9-F04») | Casa dos Bicos, Lisboa, sede da Fundação José Saramago (fotografia de Ingo Mehling, 2022). CC BY-SA 4.0. |
| M9 | José Saramago em 2005. (e «Lição M9-F04») | José Saramago em 2005 (fotografia de Mario Antonio Pena). CC BY-SA 2.0. |
| M9 | Oliveira milenar, Constância. (e «Lição M9-F04») | Oliveira milenar, Constância (fotografia de GualdimG, 2025). CC BY-SA 4.0. |

A peça comum mudou em duas coisas, as duas vistas nas galerias. Na impressão, o endereço da licença pode partir onde for preciso (numa coluna de 168 px, o endereço inteiro invadia a coluna do lado); o nome da licença continua inteiro. E as ligações dentro do crédito são sempre texto corrido (`display:inline`), mesmo quando a página dá outra caixa às suas ligações: as galerias põem as ligações em `inline-block` (para a ligação «Lição» ter área de toque), e, na impressão, o ponto final depois da licença ficava sozinho numa linha. O sha256 de `assets/info-i.css` mudou em `tests/fixtures/info-i-sha256.json` (a mesma peça vai para o Lente).

## Correções da revisão (06/11/2026)

- Projeção (bloqueante): o «i» «canto» guarda o fundo de papel e o halo de 2 px; só a «linha», sobre o papel da página, perde o fundo. Sem eles, o círculo descia a 1,29:1 contra a fotografia. Proposta de emenda ao plano, secção 1.3: «Projeção: sem fundo cheio» passa a valer só para a variante «linha». O bloco 3 de `tests/browser_creditos_i.cjs` exige fundo e 3:1 do círculo contra o halo no «canto» projetado.
- Proximidade (variante «linha» seguida de legenda): no ecrã, com o «i» fechado, a legenda sobe para a faixa do «i», à esquerda dele, junto da imagem (galerias «Para ver», na peça comum; P10 nas lições M7-F01 e M7-F05, num estilo da página, só enquanto a legenda fica por baixo da imagem, porque a partir de 1024 × 560 px a casca põe a legenda ao lado; P9, no molde). Aberto, o crédito abre entre a imagem e a legenda e o «i» não muda de sítio. Na impressão nada muda. O bloco 8 do teste de navegador mede-o nas quatro larguras.
- Legendas à vista: «Fernão Lopes (retrato imaginado).»; os dois retratos de Almeida Garrett (M4) e os dois de Antero de Quental (M6) com o autor e a data à vista; «Uma página do *Cancioneiro da Biblioteca Nacional*.»; os títulos de obras em itálico nas legendas da P16 e nos seus «i». O «i» leva sempre a identificação inteira.
- Mafra (P14): o autor que a CC BY-SA 3.0 exige, confirmado no Commons (ver acima).
- Decisão 152: espaço inseparável em «c. 1860» e nas outras datas aproximadas dentro dos «i» (já em `span.nb`) e em «H. C. White Co.» (P11). Nenhuma palavra muda.
- P11 (dupla exposição): o «i» passa a 8 px da fotografia (9 px da caixa, por causa do 1 px de borda da moldura). Aberto, o crédito cobre boa parte da fotografia a 320 px (87 %); tocar num verso é um clique fora e fecha o crédito, por isso o exercício não fica preso.

## Testes

- Novos: `tests/test_creditos_i.py` (peça igual nos dois sítios, estrutura de cada «i», nenhum crédito longo à vista fora da lista fechada `tests/fixtures/creditos-a-vista-20261105.json`, «Parar o desenho» fora do «i») e `tests/browser_creditos_i.cjs` (ensaio e uma amostra de P7 e P9, no CI das lições).
- Mudam, com comentário datado e a mesma exigência no sítio novo: `tests/browser_documentos_lote2.py`, `tests/test_texto_justificado.py` e `tests/browser_texto_justificado.py`.
- Fatia 2: mudam `tests/test_varredura_formatacao.py` (`test_creditos_declaram_as_lacunas_da_fonte`: os seis campos dentro do «i» de M7-F01, M7-F05 e do mapa M7, nenhum fora; continua a proibir `credito-imagem`) e `tests/browser_varredura_formatacao.py` (o «i» vê-se; aberto, os seis campos com 13,1 px ou menos; «Lição M7-F01» à vista fora do «i»). `tests/test_creditos_i.py` ganha três testes (a instrução da dupla exposição à vista; os oito retratos letra a letra; nenhum crédito no texto de uma explicação em todo o sítio, e o da P13 no «i» da imagem) e `tests/browser_creditos_i.cjs` ganha as amostras de P10 e P11 e os casos montados de P12 e P13 (lição e painel) e a galeria do mapa M7.
- A camada entra em todas as cadeias: `scripts/verificar_camadas.py`, `tests/auditoria_20261028.py` (`undo_creditos_i_0511` no início de `undo_contexto_0511`; 06/11/2026, depois de juntar o main: no início de `undo_atlas_lote3_0511`, por cima do lote 3 do Atlas e da decisão 154), `scripts/desligar_sala.py`, os testes das cadeias e os workflows.
- Fatia 3: `tests/test_creditos_i.py` sobe o mínimo de «i» para 173 e ganha três testes (P14: o `fr-cred` letra a letra no «i» da moldura e só o `fr-leg` no `figcaption`; P15: o campo `credito` sem pontos médios, o `creditoUrl` e o motor que monta o «i»; P16: em cada galeria, imagem, «i» e legenda, por esta ordem, o crédito a começar pela legenda à vista e a acabar na licença, nenhuma licença na legenda, as ligações «Lição Mx-Fyy» contadas e um nome único por «i»). A lista fechada perde as entradas de P14 e P16 (ficam 88 entradas e 88 créditos: P1 1, P2 9, P3 1, P8 77). `tests/browser_creditos_i.cjs` ganha a amostra da P14 (com o ampliador) e os casos da P15 (M4 «canto» e M7 «linha», com a ligação `creditoUrl`) e da P16 (mapa M8, com as quatro ligações «Lição» à vista, fora do «i»); o caso do mapa M7 passa a olhar só para a figura de Pessoa (a galeria tem agora 19 «i»); as imagens pelo endereço publicado servem-se da árvore local. Na impressão, em todos os casos montados, as ligações do crédito ficam em linha com o texto (`display:inline`).
