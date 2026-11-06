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

## Testes

- Novos: `tests/test_creditos_i.py` (peça igual nos dois sítios, estrutura de cada «i», nenhum crédito longo à vista fora da lista fechada `tests/fixtures/creditos-a-vista-20261105.json`, «Parar o desenho» fora do «i») e `tests/browser_creditos_i.cjs` (ensaio e uma amostra de P7 e P9, no CI das lições).
- Mudam, com comentário datado e a mesma exigência no sítio novo: `tests/browser_documentos_lote2.py`, `tests/test_texto_justificado.py` e `tests/browser_texto_justificado.py`.
- Fatia 2: mudam `tests/test_varredura_formatacao.py` (`test_creditos_declaram_as_lacunas_da_fonte`: os seis campos dentro do «i» de M7-F01, M7-F05 e do mapa M7, nenhum fora; continua a proibir `credito-imagem`) e `tests/browser_varredura_formatacao.py` (o «i» vê-se; aberto, os seis campos com 13,1 px ou menos; «Lição M7-F01» à vista fora do «i»). `tests/test_creditos_i.py` ganha três testes (a instrução da dupla exposição à vista; os oito retratos letra a letra; nenhum crédito no texto de uma explicação em todo o sítio, e o da P13 no «i» da imagem) e `tests/browser_creditos_i.cjs` ganha as amostras de P10 e P11 e os casos montados de P12 e P13 (lição e painel) e a galeria do mapa M7.
- A camada entra em todas as cadeias: `scripts/verificar_camadas.py`, `tests/auditoria_20261028.py` (`undo_creditos_i_0511` no início de `undo_contexto_0511`), `scripts/desligar_sala.py`, os testes das cadeias e os workflows.
