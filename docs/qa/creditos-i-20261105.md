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

## Testes

- Novos: `tests/test_creditos_i.py` (peça igual nos dois sítios, estrutura de cada «i», nenhum crédito longo à vista fora da lista fechada `tests/fixtures/creditos-a-vista-20261105.json`, «Parar o desenho» fora do «i») e `tests/browser_creditos_i.cjs` (ensaio e uma amostra de P7 e P9, no CI das lições).
- Mudam, com comentário datado e a mesma exigência no sítio novo: `tests/browser_documentos_lote2.py`, `tests/test_texto_justificado.py` e `tests/browser_texto_justificado.py`.
- A camada entra em todas as cadeias: `scripts/verificar_camadas.py`, `tests/auditoria_20261028.py` (`undo_creditos_i_0511` no início de `undo_contexto_0511`), `scripts/desligar_sala.py`, os testes das cadeias e os workflows.
