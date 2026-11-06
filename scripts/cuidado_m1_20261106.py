#!/usr/bin/env python3
"""06/11/2026: decisão 152 do docente, «cuidado em todas as lições», no módulo M1 do Português.

Constrói scripts/cuidado_m1_20261106.json, a camada literal cuidado_m1_20261106, com os 48 achados CONFIRMADOS da varredura
de 6/11 (só leitura, com conferência independente) no M1: 12 tabelas (A), 34 referências e números que se partiam (B) e 2 casos
do mesmo tipo (C). A camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em
tests/fixtures/cuidado-m1-edits-20261106.json:

  python3 scripts/cuidado_m1_20261106.py
  python3 scripts/aplicar_trocas.py scripts/cuidado_m1_20261106.json --manifesto tests/fixtures/cuidado-m1-edits-20261106.json --nota "…"

Regras (as da varredura):
- A: os itens paralelos que pedem tabela passam a tabela, como na M7-F10 e na M7-F15: class apoio-tabela, th scope=col no
  cabeçalho, th scope=row na primeira coluna, td data-label, e os role (table, rowgroup, row, columnheader, rowheader, cell),
  porque no telemóvel a tabela passa a display:block. Dentro do JSON dos cartões, as aspas vão com barra (\\"), como no resto do
  JSON. Cada página com uma tabela nova carrega assets/pt-lessons/apoios-tabelas.css antes de assets/appearance.css.
- B: U+00A0 (espaço que não quebra) depois de v., vv., p., pp., cap., caps., séc., c., vol., n.º e de D./S. antes de nome; entre
  «século(s)» e o numeral, entre ordinal e nome (1.º ano, 2.º verso), entre número e unidade (min, minutos, segundos, palavras,
  %), dentro das datas («6 de dezembro», «de 1383») e em «João I»; U+2060 (junção de palavras) logo a seguir ao traço de
  intervalo (1279–1325). Em cada achado B mudam todas as ocorrências de cada trecho no ficheiro, salvo as que o próprio achado
  deixa de fora (a «casca», migalhas e menu, só muda onde o achado o diz).
- C: as três hipóteses da M1-F02 em lista; os elementos de cada tema da grelha da M1-U1 em duas listas.
- Ordem: A e C primeiro (os trechos citam o texto com espaços normais), B depois.

O texto visível fica igual, letra a letra, salvo a estrutura das tabelas e listas e os espaços invisíveis. Três achados A
(tarefas M1-U1 e M1-U2, guia da tarefa) citavam o texto de antes da decisão 154 («para o docente apresentar», «apresentação do
enunciado pelo docente»); aplicam-se ao texto de hoje: no guia, a linha da tabela é «leitura do enunciado», tal como está no
parágrafo; nas tarefas, «para leres o enunciado» passa a «lês o enunciado», a mesma reformulação mínima que o achado aceitou
(«para o docente apresentar» > «o docente apresenta»), sem reintroduzir o docente.

As trocas B não se sobrepõem: cada troca leva só os espaços que muda; quando o mesmo trecho aparece noutro sítio que não muda (a
casca, o texto de um achado A, uma ocorrência que já tinha o espaço certo), a troca leva o mínimo de contexto que a distingue.
O script calcula as trocas sobre a base (a página com esta camada desfeita pelo manifesto, quando ele já existe): pode voltar a
correr depois de a camada estar aplicada e dá o mesmo JSON.

Páginas geradas (as tarefas, o aquecimento, as grelhas e as correções da M1-U1 e da M1-U2): mudam também os dados dos
geradores (docs/pedagogia/tarefas-escolha/m1-u1.json e m1-u2.json, docs/pedagogia/aquecimentos/m1-u1.json e
docs/pedagogia/grelhas-tarefas-20261027.json, só nas entradas m1-u1 e m1-u2), que estão na mesma camada, e os geradores
(scripts/tarefas_escolha.py e scripts/grelhas_tarefas.py) ganham as chaves «tabela», «nao_partir» e «max_em_listas»; as páginas
regeneram-se sem diferenças.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m1_20261106.json'
MANIFESTO = ROOT / 'tests/fixtures/cuidado-m1-edits-20261106.json'
NBSP, WJ = '\xa0', '⁠'
ACHADO = '06/11/2026: decisão 152 (cuidado em todas as lições), varredura do M1, achado {i} ({cat}). {texto}'
TEXTO_CAT = {
    'A': 'Itens paralelos que pedem tabela passam a tabela (como na M7-F10 e na M7-F15).',
    'B': 'Referências e números que não se partem entre linhas (U+00A0; U+2060 a seguir ao traço de intervalo).',
    'C': 'Caso do mesmo tipo: itens paralelos em lista.',
}

# A folha das tabelas de apoio, antes da camada de aparência (como na M7-F10 e na M7-F15). A versão nova (20261106.1) é a da
# folha com as regras do cartão escuro e das páginas fora das lições.
FOLHA = '<link rel="stylesheet" href="{}assets/pt-lessons/apoios-tabelas.css?v=20261106.1">'
COM_TABELA = {
    'm1/licao-m1-f05/index.html': 'lição', 'm1/licao-m1-f08/index.html': 'lição', 'm1/licao-m1-f10/index.html': 'lição',
    'm1/licao-m1-f11/index.html': 'lição', 'm1/licao-m1-f15/index.html': 'lição', 'm1/licao-m1-f20/index.html': 'lição',
    'm1/gram-fonologia/index.html': 'página «Ler a fundo»', 'm1/guia-da-tarefa-m1/index.html': 'guia da tarefa',
    'tarefas/m1-u1/index.html': 'tarefa', 'tarefas/m1-u2/index.html': 'tarefa', 'm1/index.html': 'índice do módulo',
}


# Os 14 achados A e C confirmados (trecho atual e proposta final da conferência, na forma da fonte).
ACHADOS_AC = [
    dict(i=0, cat='A', ficheiro='m1/licao-m1-f05/index.html',
         cartao='5 · Conceito «Que sons apareceram, e onde?» (details «Um esquema curto e duas tentativas»)',
         antigo='<ul><li><strong>Entra (PEP):</strong> início, <strong>prótese</strong> (<i>scribere</i> &gt; escrever: vogal inicial); meio, <strong>epêntese</strong> (<i>humile</i> &gt; humilde: [d]); fim, <strong>paragoge</strong> (<i>ante</i> &gt; antes: consoante final).</li><li><strong>Desaparece (ASA):</strong> início, <strong>aférese</strong> (alevantada &gt; levantada: vogal inicial); meio, <strong>síncope</strong> (<i>malu</i> &gt; mau: [l]); fim, <strong>apócope</strong> (<i>amare</i> &gt; amar: vogal final).</li></ul>',
         novo='<table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\">Onde</th><th scope=\\"col\\" role=\\"columnheader\\">Entra (PEP)</th><th scope=\\"col\\" role=\\"columnheader\\">Desaparece (ASA)</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">início</th><td role=\\"cell\\" data-label=\\"Entra (PEP)\\"><strong>prótese</strong> (<i>scribere</i> &gt; escrever: vogal inicial)</td><td role=\\"cell\\" data-label=\\"Desaparece (ASA)\\"><strong>aférese</strong> (alevantada &gt; levantada: vogal inicial)</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">meio</th><td role=\\"cell\\" data-label=\\"Entra (PEP)\\"><strong>epêntese</strong> (<i>humile</i> &gt; humilde: [d])</td><td role=\\"cell\\" data-label=\\"Desaparece (ASA)\\"><strong>síncope</strong> (<i>malu</i> &gt; mau: [l])</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">fim</th><td role=\\"cell\\" data-label=\\"Entra (PEP)\\"><strong>paragoge</strong> (<i>ante</i> &gt; antes: consoante final)</td><td role=\\"cell\\" data-label=\\"Desaparece (ASA)\\"><strong>apócope</strong> (<i>amare</i> &gt; amar: vogal final)</td></tr></tbody></table>'),
    dict(i=1, cat='A', ficheiro='m1/gram-fonologia/index.html',
         cartao='E.passos[0] «Três palavras das cantigas» (details «Consultar o esquema PEP/ASA e experimentar»)',
         antigo='<ul><li><strong>Entra (PEP):</strong> início, <strong>prótese</strong> (<i>scribere</i> &gt; escrever: vogal inicial); interior, <strong>epêntese</strong> (<i>humile</i> &gt; humilde: [d]); fim, <strong>paragoge</strong> (<i>ante</i> &gt; antes: consoante final).</li><li><strong>Desaparece (ASA):</strong> início, <strong>aférese</strong> (alevantada &gt; levantada: vogal inicial); interior, <strong>síncope</strong> (<i>malu</i> &gt; mau: [l]); fim, <strong>apócope</strong> (<i>amare</i> &gt; amar: vogal final).</li></ul>',
         novo='<table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\">Onde</th><th scope=\\"col\\" role=\\"columnheader\\">Entra (PEP)</th><th scope=\\"col\\" role=\\"columnheader\\">Desaparece (ASA)</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">início</th><td role=\\"cell\\" data-label=\\"Entra (PEP)\\"><strong>prótese</strong> (<i>scribere</i> &gt; escrever: vogal inicial)</td><td role=\\"cell\\" data-label=\\"Desaparece (ASA)\\"><strong>aférese</strong> (alevantada &gt; levantada: vogal inicial)</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">interior</th><td role=\\"cell\\" data-label=\\"Entra (PEP)\\"><strong>epêntese</strong> (<i>humile</i> &gt; humilde: [d])</td><td role=\\"cell\\" data-label=\\"Desaparece (ASA)\\"><strong>síncope</strong> (<i>malu</i> &gt; mau: [l])</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">fim</th><td role=\\"cell\\" data-label=\\"Entra (PEP)\\"><strong>paragoge</strong> (<i>ante</i> &gt; antes: consoante final)</td><td role=\\"cell\\" data-label=\\"Desaparece (ASA)\\"><strong>apócope</strong> (<i>amare</i> &gt; amar: vogal final)</td></tr></tbody></table>'),
    dict(i=2, cat='A', ficheiro='m1/licao-m1-f08/index.html',
         cartao='18 · Agora, em papel «A resposta que entregas» (details «Um exemplo»)',
         antigo='<p>1. «Acaba a venda do trigo em Lisboa» (sublinhado: «do trigo»). Sem o grupo, «a venda»… de quê? «Venda» é nome: complemento do nome. 2. «Pobres incapazes de comprar trigo» (sublinhado: «de comprar trigo»). Sem o grupo, «incapazes»… de quê? É adjetivo: complemento do adjetivo. 3. «A cidade cercada carece de trigo» (sublinhado: «de trigo»). Sem o grupo, «carece»… de quê? É verbo, e «carece-lhe» não se diz (diz-se «carece dele»): complemento oblíquo.</p>',
         novo='<table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\">Título</th><th scope=\\"col\\" role=\\"columnheader\\">Sublinhado</th><th scope=\\"col\\" role=\\"columnheader\\">Sem o grupo</th><th scope=\\"col\\" role=\\"columnheader\\">Complemento</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">1. «Acaba a venda do trigo em Lisboa»</th><td role=\\"cell\\" data-label=\\"Sublinhado\\">«do trigo»</td><td role=\\"cell\\" data-label=\\"Sem o grupo\\">«a venda»… de quê?</td><td role=\\"cell\\" data-label=\\"Complemento\\">«Venda» é nome: complemento do nome.</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">2. «Pobres incapazes de comprar trigo»</th><td role=\\"cell\\" data-label=\\"Sublinhado\\">«de comprar trigo»</td><td role=\\"cell\\" data-label=\\"Sem o grupo\\">«incapazes»… de quê?</td><td role=\\"cell\\" data-label=\\"Complemento\\">É adjetivo: complemento do adjetivo.</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">3. «A cidade cercada carece de trigo»</th><td role=\\"cell\\" data-label=\\"Sublinhado\\">«de trigo»</td><td role=\\"cell\\" data-label=\\"Sem o grupo\\">«carece»… de quê?</td><td role=\\"cell\\" data-label=\\"Complemento\\">É verbo, e «carece-lhe» não se diz (diz-se «carece dele»): complemento oblíquo.</td></tr></tbody></table>'),
    dict(i=3, cat='A', ficheiro='m1/licao-m1-f08/index.html',
         cartao='19 · Para levar',
         antigo='<p>Tira o grupo: se a palavra fica a pedir, o grupo é complemento. Quem pede dá-lhe o nome: um nome («a guarda dos muros»), um adjetivo («amigas da natureza») ou um verbo, se o grupo tem preposição e não troca por «lhe» («chegar a ele»).</p>',
         novo='<p>Tira o grupo: se a palavra fica a pedir, o grupo é complemento. Quem pede dá-lhe o nome:</p><table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\">Quem pede</th><th scope=\\"col\\" role=\\"columnheader\\">Complemento</th><th scope=\\"col\\" role=\\"columnheader\\">Exemplo</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">um nome</th><td role=\\"cell\\" data-label=\\"Complemento\\">do nome</td><td role=\\"cell\\" data-label=\\"Exemplo\\">«a guarda dos muros»</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">um adjetivo</th><td role=\\"cell\\" data-label=\\"Complemento\\">do adjetivo</td><td role=\\"cell\\" data-label=\\"Exemplo\\">«amigas da natureza»</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">um verbo, se o grupo tem preposição e não troca por «lhe»</th><td role=\\"cell\\" data-label=\\"Complemento\\">oblíquo</td><td role=\\"cell\\" data-label=\\"Exemplo\\">«chegar a ele»</td></tr></tbody></table>'),
    dict(i=4, cat='A', ficheiro='m1/licao-m1-f11/index.html',
         cartao='14 · Recorda «Lado a lado: que diz a ligação?»',
         antigo='<p><b>Coordenação</b>: duas orações lado a lado, nenhuma parte da outra. A <b>copulativa</b> soma (e, nem); a <b>adversativa</b> contraria o que se esperava (mas); a <b>explicativa</b> justifica o que se disse ou mandou (pois, que); a <b>conclusiva</b> tira a consequência (portanto, logo, por isso).</p>',
         novo='<p><b>Coordenação</b>: duas orações lado a lado, nenhuma parte da outra.</p><table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\">Valor</th><th scope=\\"col\\" role=\\"columnheader\\">O que faz</th><th scope=\\"col\\" role=\\"columnheader\\">Conjunções</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">copulativa</th><td role=\\"cell\\" data-label=\\"O que faz\\">soma</td><td role=\\"cell\\" data-label=\\"Conjunções\\">e, nem</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">adversativa</th><td role=\\"cell\\" data-label=\\"O que faz\\">contraria o que se esperava</td><td role=\\"cell\\" data-label=\\"Conjunções\\">mas</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">explicativa</th><td role=\\"cell\\" data-label=\\"O que faz\\">justifica o que se disse ou mandou</td><td role=\\"cell\\" data-label=\\"Conjunções\\">pois, que</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">conclusiva</th><td role=\\"cell\\" data-label=\\"O que faz\\">tira a consequência</td><td role=\\"cell\\" data-label=\\"Conjunções\\">portanto, logo, por isso</td></tr></tbody></table>'),
    dict(i=8, cat='A', ficheiro='m1/licao-m1-f15/index.html',
         cartao='19 · Para levar',
         antigo='<p>Entre duas orações lado a lado, a conjunção diz a relação: o «e» soma, o «mas» contraria o que se esperava, o «pois» justifica, o «portanto» tira a consequência. Decide pelo sentido, não pela palavra: faz a troca e ouve.</p>',
         novo='<p>Entre duas orações lado a lado, a conjunção diz a relação:</p><table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\">Conjunção</th><th scope=\\"col\\" role=\\"columnheader\\">Relação</th><th scope=\\"col\\" role=\\"columnheader\\">Valor</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">«e»</th><td role=\\"cell\\" data-label=\\"Relação\\">soma</td><td role=\\"cell\\" data-label=\\"Valor\\">copulativa (e, nem)</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">«mas»</th><td role=\\"cell\\" data-label=\\"Relação\\">contraria o que se esperava</td><td role=\\"cell\\" data-label=\\"Valor\\">adversativa (mas)</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">«pois»</th><td role=\\"cell\\" data-label=\\"Relação\\">justifica</td><td role=\\"cell\\" data-label=\\"Valor\\">explicativa (pois, que)</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">«portanto»</th><td role=\\"cell\\" data-label=\\"Relação\\">tira a consequência</td><td role=\\"cell\\" data-label=\\"Valor\\">conclusiva (portanto, logo, por isso)</td></tr></tbody></table><p>Decide pelo sentido, não pela palavra: faz a troca e ouve.</p>'),
    dict(i=9, cat='A', ficheiro='m1/licao-m1-f20/index.html',
         cartao='16 · Para levar',
         antigo='<p>O grito do pajem é o que uma voz afirma; o relato mostra a cidade a correr. O que se aponta nas palavras é explícito; o que se conclui de pistas é inferência; um sentido com provas é interpretação; um juízo de valor, opinião.</p>',
         novo='<p>O grito do pajem é o que uma voz afirma; o relato mostra a cidade a correr.</p><table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\">Etiqueta</th><th scope=\\"col\\" role=\\"columnheader\\">O que é</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">explícito</th><td role=\\"cell\\" data-label=\\"O que é\\">o que se aponta nas palavras</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">inferência</th><td role=\\"cell\\" data-label=\\"O que é\\">o que se conclui de pistas</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">interpretação</th><td role=\\"cell\\" data-label=\\"O que é\\">um sentido com provas</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">opinião</th><td role=\\"cell\\" data-label=\\"O que é\\">um juízo de valor</td></tr></tbody></table>'),
    dict(i=13, cat='A', ficheiro='m1/licao-m1-f10/index.html',
         cartao='1 · A encomenda «A tua crónica» (details «Ler mais»)',
         antigo='<p><b>Figuras e fontes possíveis.</b> Álvaro Pais ou o pajem, a 6 de dezembro de 1383 (Fernão Lopes, cap. XII); Nuno Álvares Pereira em Aljubarrota (Wikipédia, «Batalha de Aljubarrota»); uma pessoa do cerco de 1384 (Fernão Lopes, caps. CXVI e CXLVIII; Wikipédia, «Cerco de Lisboa (1384)»); Inês de Castro (Wikipédia, «Inês de Castro»); ou alguém da área do teu curso, um fotógrafo, um músico, um realizador (Wikipédia e uma entrevista publicada). Sempre duas fontes, identificadas.</p>',
         novo='<p><b>Figuras e fontes possíveis.</b> Sempre duas fontes, identificadas.</p><table class=\\"apoio-tabela\\" role=\\"table\\"><thead role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"col\\" role=\\"columnheader\\" style=\\"width:50%\\">Figura</th><th scope=\\"col\\" role=\\"columnheader\\">Fontes</th></tr></thead><tbody role=\\"rowgroup\\"><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">Álvaro Pais ou o pajem, a 6\xa0de\xa0dezembro de\xa01383</th><td role=\\"cell\\" data-label=\\"Fontes\\">Fernão Lopes, cap.\xa0XII</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">Nuno Álvares Pereira em Aljubarrota</th><td role=\\"cell\\" data-label=\\"Fontes\\">Wikipédia, «Batalha de Aljubarrota»</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">uma pessoa do cerco de 1384</th><td role=\\"cell\\" data-label=\\"Fontes\\">Fernão Lopes, caps.\xa0CXVI e\xa0CXLVIII; Wikipédia, «Cerco de Lisboa (1384)»</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">Inês de Castro</th><td role=\\"cell\\" data-label=\\"Fontes\\">Wikipédia, «Inês de Castro»</td></tr><tr role=\\"row\\"><th scope=\\"row\\" role=\\"rowheader\\">alguém da área do teu curso, um fotógrafo, um músico, um realizador</th><td role=\\"cell\\" data-label=\\"Fontes\\">Wikipédia e uma entrevista publicada</td></tr></tbody></table>'),
    dict(i=16, cat='A', ficheiro='m1/index.html',
         cartao='página do módulo · «Como se cumpre uma unidade» (p.avaliacao-tarefas)',
         antigo='<p class="avaliacao-tarefas">Pesos na avaliação: tarefa da Unidade 1, 30 %; tarefa da Unidade 2, 30 %; provas rápidas, 10 %; prova escrita, 30 %. Cada tarefa tem uma grelha /20.</p>',
         novo='<p class="avaliacao-tarefas">Pesos na avaliação:</p><table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">Componente</th><th scope="col" role="columnheader">Peso</th></tr></thead><tbody role="rowgroup"><tr role="row"><th scope="row" role="rowheader">tarefa da Unidade 1</th><td role="cell" data-label="Peso">30\xa0%</td></tr><tr role="row"><th scope="row" role="rowheader">tarefa da Unidade 2</th><td role="cell" data-label="Peso">30\xa0%</td></tr><tr role="row"><th scope="row" role="rowheader">provas rápidas</th><td role="cell" data-label="Peso">10\xa0%</td></tr><tr role="row"><th scope="row" role="rowheader">prova escrita</th><td role="cell" data-label="Peso">30\xa0%</td></tr></tbody></table><p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20.</p>'),
    dict(i=17, cat='A', ficheiro='tarefas/m1-u1/index.html',
         cartao='página da tarefa · «Aquecer em cartões»',
         nota='O trecho do achado era o de antes da decisão 154; aplica-se ao de hoje: «para leres o enunciado» passa a «lês o enunciado» (a reformulação mínima que o achado aceitou) e o fim fica «depois da leitura», como está.',
         antigo='<p>No início da aula de tarefa: 10 minutos de cartões com consulta, 5 minutos para leres o enunciado, 60 minutos de produção e 15 minutos de revisão e entrega. Total: 90 minutos. O relógio de produção começa depois da leitura.</p>',
         novo='<p>No início da aula de tarefa:</p><table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">Momento</th><th scope="col" role="columnheader">Tempo</th></tr></thead><tbody role="rowgroup"><tr role="row"><th scope="row" role="rowheader">cartões com consulta</th><td role="cell" data-label="Tempo">10\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">lês o enunciado</th><td role="cell" data-label="Tempo">5\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">produção</th><td role="cell" data-label="Tempo">60\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">revisão e entrega</th><td role="cell" data-label="Tempo">15\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">Total</th><td role="cell" data-label="Tempo">90\xa0minutos</td></tr></tbody></table><p>O relógio de produção começa depois da leitura.</p>'),
    dict(i=18, cat='A', ficheiro='tarefas/m1-u2/index.html',
         cartao='página da tarefa · «Aquecer em cartões»',
         nota='O trecho do achado era o de antes da decisão 154; aplica-se ao de hoje: «para leres o enunciado» passa a «lês o enunciado» (a reformulação mínima que o achado aceitou) e o fim fica «depois da leitura», como está.',
         antigo='<p>No início da aula de tarefa: 10 minutos de cartões com consulta, 5 minutos para leres o enunciado, 60 minutos de produção e 15 minutos de revisão e entrega. Total: 90 minutos. O relógio de produção começa depois da leitura.</p>',
         novo='<p>No início da aula de tarefa:</p><table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">Momento</th><th scope="col" role="columnheader">Tempo</th></tr></thead><tbody role="rowgroup"><tr role="row"><th scope="row" role="rowheader">cartões com consulta</th><td role="cell" data-label="Tempo">10\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">lês o enunciado</th><td role="cell" data-label="Tempo">5\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">produção</th><td role="cell" data-label="Tempo">60\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">revisão e entrega</th><td role="cell" data-label="Tempo">15\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">Total</th><td role="cell" data-label="Tempo">90\xa0minutos</td></tr></tbody></table><p>O relógio de produção começa depois da leitura.</p>'),
    dict(i=19, cat='A', ficheiro='m1/guia-da-tarefa-m1/index.html',
         cartao='guia · «Aulas de tarefa das unidades»',
         nota='O trecho do achado era o de antes da decisão 154; aplica-se ao de hoje, com a linha «leitura do enunciado» tal como está no parágrafo.',
         antigo='<p>Cada aula de 90 minutos começa com 10 minutos de aquecimento em cartões, no telemóvel e com consulta. Seguem-se 5 minutos de leitura do enunciado, 60 minutos de produção com consulta e 15 minutos de revisão e entrega.',
         novo='<p>Cada aula de 90\xa0minutos:</p><table class="apoio-tabela" role="table"><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">Momento</th><th scope="col" role="columnheader">Tempo</th></tr></thead><tbody role="rowgroup"><tr role="row"><th scope="row" role="rowheader">aquecimento em cartões, no telemóvel e com consulta</th><td role="cell" data-label="Tempo">10\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">leitura do enunciado</th><td role="cell" data-label="Tempo">5\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">produção com consulta</th><td role="cell" data-label="Tempo">60\xa0minutos</td></tr><tr role="row"><th scope="row" role="rowheader">revisão e entrega</th><td role="cell" data-label="Tempo">15\xa0minutos</td></tr></tbody></table><p>'),
    dict(i=20, cat='C', ficheiro='m1/licao-m1-f02/index.html',
         cartao='15 · Explora «Três hipóteses para o final»',
         antigo='<p>O perigo é real; é a espera que exagera; ou morrer «fremosa» acusa quem não veio. Mais de uma hipótese tem apoio no texto.</p>',
         novo='<ul><li>O perigo é real.</li><li>É a espera que exagera.</li><li>Morrer «fremosa» acusa quem não veio.</li></ul><p>Mais de uma hipótese tem apoio no texto.</p>'),
    dict(i=21, cat='C', ficheiro='tarefas/m1-u1/grelha/index.html',
         cartao='critério 4 «Tema à escolha», nível 6 (dd)',
         antigo='Tema A: paralelismo; refrão que repete a promessa; o teu verso que desmente a promessa; um verso de Codax citado; uma diferença entre a tua espera e a da cantiga de Codax. Explicação: o que imitaste de Codax. Tema B: imagem em duas frases; dois factos do dossiê (contam como dois); um verso escolhido; o que o cartaz não pode prometer. Explicação: porque escolheste esse verso.</p>',
         novo='</p><p><b>Tema A</b>:</p><ul><li>paralelismo;</li><li>refrão que repete a promessa;</li><li>o teu verso que desmente a promessa;</li><li>um verso de Codax citado;</li><li>uma diferença entre a tua espera e a da cantiga de Codax.</li></ul><p>Explicação: o que imitaste de Codax.</p><p><b>Tema B</b>:</p><ul><li>imagem em duas frases;</li><li>dois factos do dossiê (contam como dois);</li><li>um verso escolhido;</li><li>o que o cartaz não pode prometer.</li></ul><p>Explicação: porque escolheste esse verso.</p>'),
]

# Os 34 achados B confirmados: pares (trecho, proposta) pela ordem do achado; «ocorrencias» é a contagem da varredura.
ACHADOS_B = [
    dict(i=22, ficheiro='m1/gram-complementos/index.html', cartao='E.subtitulo, E.passos, E.fontes e HTML', ocorrencias=11,
         pares=[('caps. CXVI e CXLVIII', 'caps.\xa0CXVI e\xa0CXLVIII'), ('cap. 148', 'cap.\xa0148'), ('cap. 115', 'cap.\xa0115'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=23, ficheiro='m1/gram-coordenadas/index.html', cartao='E.fontes e HTML', ocorrencias=9,
         pares=[('cap. XII', 'cap.\xa0XII'), ('n.º 861', 'n.º\xa0861'), ('n.º 1520', 'n.º\xa01520'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=24, ficheiro='m1/gram-fonologia/index.html', cartao='E.passos[0] e E.fontes', ocorrencias=7,
         pares=[('p. 244', 'p.\xa0244'), ('pp. 5 e 9', 'pp.\xa05 e\xa09'), ('n.º 1308', 'n.º\xa01308'), ('9.º ano', '9.º\xa0ano'), ('GTA 16', 'GTA\xa016'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=25, ficheiro='m1/guia-da-tarefa-m1/index.html', cartao='guia (HTML)', ocorrencias=10,
         pares=[('1.º ano', '1.º\xa0ano'), ('90 min', '90\xa0min'), ('250 a 300 palavras', '250 a 300\xa0palavras'), ('90 minutos', '90\xa0minutos'), ('10 minutos', '10\xa0minutos'), ('5 minutos', '5\xa0minutos'), ('60 minutos', '60\xa0minutos'), ('15 minutos', '15\xa0minutos')]),
    dict(i=26, ficheiro='m1/guilhade-dona-fea/index.html', cartao='E.subtitulo, E.passos, E.fontes e HTML', ocorrencias=9,
         pares=[('séc. XIII', 'séc.\xa0XIII'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=27, ficheiro='m1/index.html', cartao='texto estático e banco «Praticar perguntas do arquivo»', ocorrencias=48,
         pares=[('v. 14', 'v.\xa014'), ('v. 7', 'v.\xa07'), ('v. 4', 'v.\xa04'), ('Cap. XII', 'Cap.\xa0XII'), ('caps. CXVI e CXLVIII', 'caps.\xa0CXVI e\xa0CXLVIII'), ('século XVI', 'século\xa0XVI'), ('séculos XIII e XIV', 'séculos\xa0XIII e\xa0XIV'), ('1.º ano', '1.º\xa0ano'), ('6 de dezembro de 1383', '6\xa0de\xa0dezembro de\xa01383'), ('3 de setembro de 1384', '3\xa0de\xa0setembro de\xa01384'), ('14 de agosto de 1385', '14\xa0de\xa0agosto de\xa01385'), ('6 de dezembro', '6\xa0de\xa0dezembro'), ('3 de setembro', '3\xa0de\xa0setembro'), ('14 de agosto', '14\xa0de\xa0agosto'), ('30 %', '30\xa0%'), ('90 minutos', '90\xa0minutos'), ('90 min', '90\xa0min'), ('10 min', '10\xa0min'), ('10 %', '10\xa0%'), ('25 %', '25\xa0%'), ('35 %', '35\xa0%'), ('250 a 300 palavras', '250 a 300\xa0palavras'), ('160 a 200 palavras', '160 a 200\xa0palavras'), ('80 a 120 palavras', '80 a 120\xa0palavras'), ('D. Dinis', 'D.\xa0Dinis'), ('D. Pedro', 'D.\xa0Pedro')]),
    dict(i=28, ficheiro='m1/licao-m1-f01/index.html', cartao='cartões 0, 1, 4, 6, 7, 12, 13, 15, 18, 19, 20', ocorrencias=34,
         pares=[('v. 14', 'v.\xa014'), ('séculos XIII e XIV', 'séculos\xa0XIII e\xa0XIV'), ('século XVI', 'século\xa0XVI'), ('5.ª estrofe', '5.ª\xa0estrofe'), ('1 min', '1\xa0min'), ('4 min', '4\xa0min'), ('90 minutos', '90\xa0minutos'), ('fólio 21r', 'fólio\xa021r'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=29, ficheiro='m1/licao-m1-f02/index.html', cartao='cartões 0, 1, 5, 8, 9, 10, 11, 12, 13, 14', ocorrencias=39,
         pares=[('v. 2', 'v.\xa02'), ('v. 7', 'v.\xa07'), ('v. 8', 'v.\xa08'), ('v. 13', 'v.\xa013'), ('v. 5', 'v.\xa05'), ('v. 10', 'v.\xa010'), ('v. 11', 'v.\xa011'), ('v. 16', 'v.\xa016'), ('séc. XIII', 'séc.\xa0XIII'), ('século XIII', 'século\xa0XIII'), ('2.º verso', '2.º\xa0verso'), ('1.º verso', '1.º\xa0verso'), ('2.º da', '2.º\xa0da'), ('4 min', '4\xa0min'), ('90 minutos', '90\xa0minutos'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=30, ficheiro='m1/licao-m1-f04/index.html', cartao='cartões 0, 1, 2, 4, 5, 8, 9, 12, 17, 20, 21 e nota do menu', ocorrencias=38,
         pares=[('caps. V e VI', 'caps.\xa0V e\xa0VI'), ('cap. V', 'cap.\xa0V'), ('cap. VI', 'cap.\xa0VI'), ('séc. XIII', 'séc.\xa0XIII'), ('século XVI', 'século\xa0XVI'), ('n.º 544', 'n.º\xa0544'), ('n.º 1520', 'n.º\xa01520'), ('n.º 1527', 'n.º\xa01527'), ('4 min', '4\xa0min'), ('90 minutos', '90\xa0minutos'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=31, ficheiro='m1/licao-m1-f05/index.html', cartao='cartões 0 e 5', ocorrencias=5,
         pares=[('p. 244', 'p.\xa0244'), ('pp. 5 e 9', 'pp.\xa05 e\xa09'), ('9.º ano', '9.º\xa0ano'), ('90 minutos', '90\xa0minutos'), ('GTA 16', 'GTA\xa016')]),
    dict(i=32, ficheiro='m1/licao-m1-f06/index.html', cartao='cartões 0, 1, 3, 5, 7, 8, 10, 11, 13, 17, 18 e nota do menu', ocorrencias=48,
         pares=[('cap. XII', 'cap.\xa0XII'), ('cap. 11', 'cap.\xa011'), ('século XIX', 'século\xa0XIX'), ('6 de dezembro de 1383', '6\xa0de\xa0dezembro de\xa01383'), ('4 min', '4\xa0min'), ('90 minutos', '90\xa0minutos'), ('c. 1860', 'c.\xa01860'), ('1383–1385', '1383–\u20601385'), ('D. João', 'D.\xa0João'), ('D. Pedro', 'D.\xa0Pedro'), ('D. Fernando', 'D.\xa0Fernando'), ('D. Duarte', 'D.\xa0Duarte'), ('João I', 'João\xa0I')]),
    dict(i=33, ficheiro='m1/licao-m1-f07/index.html', cartao='cartões 0, 1, 4, 5, 9, 16, 20 e nota do menu', ocorrencias=28,
         pares=[('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('caps. CXVI e CXLVIII', 'caps.\xa0CXVI e\xa0CXLVIII'), ('cap. CXVI', 'cap.\xa0CXVI'), ('cap. 115', 'cap.\xa0115'), ('século XV', 'século\xa0XV'), ('3 de setembro de 1384', '3\xa0de\xa0setembro de\xa01384'), ('3 de setembro', '3\xa0de\xa0setembro'), ('90 minutos', '90\xa0minutos'), ('D. João', 'D.\xa0João'), ('S. Jorge', 'S.\xa0Jorge'), ('João I', 'João\xa0I')]),
    dict(i=34, ficheiro='m1/licao-m1-f08/index.html', cartao='cartões 0, 1, 4, 6 e nota do menu', ocorrencias=16,
         pares=[('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('cap. CXVI', 'cap.\xa0CXVI'), ('caps. XII, CXVI, CXLVIII', 'caps.\xa0XII, CXVI, CXLVIII'), ('90 minutos', '90\xa0minutos'), ('c. 1860', 'c.\xa01860'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=35, ficheiro='m1/licao-m1-f10/index.html', cartao='cartões 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13 e pistas', ocorrencias=42,
         pares=[('cap. XII', 'cap.\xa0XII'), ('cap. CXVI', 'cap.\xa0CXVI'), ('caps. CXVI e CXLVIII', 'caps.\xa0CXVI e\xa0CXLVIII'), ('cap. 11', 'cap.\xa011'), ('século XV', 'século\xa0XV'), ('6 de dezembro de 1383', '6\xa0de\xa0dezembro de\xa01383'), ('14 de agosto de 1385', '14\xa0de\xa0agosto de\xa01385'), ('250 a 300 palavras', '250 a 300\xa0palavras'), ('90 minutos', '90\xa0minutos'), ('30 %', '30\xa0%'), ('160 a 200 palavras', '160 a 200\xa0palavras'), ('c. 1860', 'c.\xa01860'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=36, ficheiro='m1/licao-m1-f11/index.html', cartao='cartões 0, 1, 4, 5, 16, 18 e nota do menu', ocorrencias=15,
         pares=[('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('cap. XII', 'cap.\xa0XII'), ('séc. XIII', 'séc.\xa0XIII'), ('século XV', 'século\xa0XV'), ('n.º 1308', 'n.º\xa01308'), ('2.º verso', '2.º\xa0verso'), ('3 de setembro de 1384', '3\xa0de\xa0setembro de\xa01384'), ('90 minutos', '90\xa0minutos'), ('180 e 240 palavras', '180 e 240\xa0palavras'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=37, ficheiro='m1/licao-m1-f15/index.html', cartao='cartões 0, 1, 8, 15, 18 e nota do menu', ocorrencias=15,
         pares=[('v. 11', 'v.\xa011'), ('cap. XII', 'cap.\xa0XII'), ('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('90 minutos', '90\xa0minutos'), ('D. João', 'D.\xa0João'), ('D. Pedro', 'D.\xa0Pedro'), ('João I', 'João\xa0I')]),
    dict(i=38, ficheiro='m1/licao-m1-f19/index.html', cartao='cartões 0, 1, 3, 6, 7, 8, 10, 14, 18, 19 e nota do menu', ocorrencias=32,
         pares=[('caps. V e VI', 'caps.\xa0V e\xa0VI'), ('séc. XIII', 'séc.\xa0XIII'), ('2.º verso', '2.º\xa0verso'), ('3.ª pessoa', '3.ª\xa0pessoa'), ('4 min', '4\xa0min'), ('90 minutos', '90\xa0minutos'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=39, ficheiro='m1/licao-m1-f20/index.html', cartao='cartões 0, 1, 3, 6, 9, 11 e nota do menu', ocorrencias=23,
         pares=[('cap. XII', 'cap.\xa0XII'), ('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('caps. XII, CXVI e CXLVIII', 'caps.\xa0XII, CXVI e\xa0CXLVIII'), ('cap. 11', 'cap.\xa011'), ('cap. CXVI', 'cap.\xa0CXVI'), ('cap. 115', 'cap.\xa0115'), ('cap. 148', 'cap.\xa0148'), ('século XV', 'século\xa0XV'), ('90 minutos', '90\xa0minutos'), ('c. 1860', 'c.\xa01860'), ('D. João', 'D.\xa0João'), ('D. Pedro', 'D.\xa0Pedro'), ('João I', 'João\xa0I')]),
    dict(i=40, ficheiro='m1/lisboa-cercada/index.html', cartao='E.subtitulo, E.passos, E.fontes e HTML', ocorrencias=10,
         pares=[('caps. CXVI e CXLVIII', 'caps.\xa0CXVI e\xa0CXLVIII'), ('cap. CXVI', 'cap.\xa0CXVI'), ('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=41, ficheiro='m1/m1-promessa-do-cronista/index.html', cartao='itens 0, 1, 6, 9, 13, 14, 28, 32', ocorrencias=35,
         pares=[('cap. XII', 'cap.\xa0XII'), ('cap. 11', 'cap.\xa011'), ('cap. CXVI', 'cap.\xa0CXVI'), ('cap. 115', 'cap.\xa0115'), ('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('cap. 148', 'cap.\xa0148'), ('6 de dezembro de 1383', '6\xa0de\xa0dezembro de\xa01383'), ('3 de setembro', '3\xa0de\xa0setembro'), ('22 min', '22\xa0min'), ('vol. I', 'vol.\xa0I'), ('D. João', 'D.\xa0João'), ('D. Pedro', 'D.\xa0Pedro'), ('João I', 'João\xa0I')]),
    dict(i=42, ficheiro='m1/m1-voz-emprestada/index.html', cartao='itens 0, 5, 8–11, 13, 16, 18, 21, 25–29', ocorrencias=24,
         pares=[('cap. V', 'cap.\xa0V'), ('século XIII', 'século\xa0XIII'), ('22 min', '22\xa0min'), ('B 1493', 'B\xa01493'), ('V 1104', 'V\xa01104'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=43, ficheiro='m1/mapa-do-modulo-m1/index.html', cartao='mapa (HTML: cabeçalho, obras, cronologia, avaliação, figuras)', ocorrencias=37,
         pares=[('século XV', 'século\xa0XV'), ('século XVI', 'século\xa0XVI'), ('1.º ano', '1.º\xa0ano'), ('6 de dezembro de 1383', '6\xa0de\xa0dezembro de\xa01383'), ('3 de setembro', '3\xa0de\xa0setembro'), ('14 de agosto de 1385', '14\xa0de\xa0agosto de\xa01385'), ('30 %', '30\xa0%'), ('90 min', '90\xa0min'), ('10 %', '10\xa0%'), ('45 minutos', '45\xa0minutos'), ('c. 1380', 'c.\xa01380'), ('c. 1460', 'c.\xa01460'), ('c. 1860', 'c.\xa01860'), ('1279–1325', '1279–\u20601325'), ('1380/1390–c. 1460', '1380/1390–\u2060c.\xa01460'), ('fólio 21r', 'fólio\xa021r'), ('D. Dinis', 'D.\xa0Dinis'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=44, ficheiro='m1/matam-o-mestre/index.html', cartao='E.subtitulo, E.passos[0] e [4], E.fontes e HTML', ocorrencias=10,
         pares=[('cap. XII', 'cap.\xa0XII'), ('6 de dezembro de 1383', '6\xa0de\xa0dezembro de\xa01383'), ('D. João', 'D.\xa0João'), ('João I', 'João\xa0I')]),
    dict(i=45, ficheiro='m1/mendinho-ermida/index.html', cartao='E.subtitulo e HTML', ocorrencias=2,
         pares=[('séc. XIII', 'séc.\xa0XIII')]),
    dict(i=46, ficheiro='m1/olhar-ajuda/index.html', cartao='E.passos[0], E.subtitulo, E.credito, E.fontes e HTML', ocorrencias=7,
         pares=[('20 segundos', '20\xa0segundos'), ('fólio 21r', 'fólio\xa021r')]),
    dict(i=47, ficheiro='m1/ondas-vigo/index.html', cartao='E.subtitulo, E.fontes e HTML', ocorrencias=4,
         pares=[('séc. XIII', 'séc.\xa0XIII'), ('n.º 1308', 'n.º\xa01308')]),
    dict(i=48, ficheiro='m1/portefolio-do-modulo-m1/index.html', cartao='cabeçalho «Português · 1.º ano · Módulo 1»', ocorrencias=1,
         pares=[('1.º ano', '1.º\xa0ano')]),
    dict(i=49, ficheiro='tarefas/m1-u1/aquecimento/index.html', cartao='cartão 10 (p2)', ocorrencias=1,
         pares=[('século XIII', 'século\xa0XIII')]),
    dict(i=50, ficheiro='tarefas/m1-u1/correcao/index.html', cartao='tabela de correção (critério 3)', ocorrencias=1,
         pares=[('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=51, ficheiro='tarefas/m1-u1/grelha/index.html', cartao='introdução, critério 5 e títulos do critério 3', ocorrencias=5,
         pares=[('200 e 240 palavras', '200 e 240\xa0palavras'), ('200 a 240 palavras', '200 a 240\xa0palavras'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=52, ficheiro='tarefas/m1-u1/index.html', cartao='página da tarefa (HTML)', ocorrencias=14,
         pares=[('90 minutos', '90\xa0minutos'), ('200 e 240 palavras', '200 e 240\xa0palavras'), ('10 min', '10\xa0min'), ('10 minutos', '10\xa0minutos'), ('5 minutos', '5\xa0minutos'), ('60 minutos', '60\xa0minutos'), ('15 minutos', '15\xa0minutos'), ('90 min', '90\xa0min'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=53, ficheiro='tarefas/m1-u2/correcao/index.html', cartao='tabela de correção', ocorrencias=3,
         pares=[('cap. XII', 'cap.\xa0XII'), ('160 a 200 palavras', '160 a 200\xa0palavras')]),
    dict(i=54, ficheiro='tarefas/m1-u2/grelha/index.html', cartao='introdução e critérios', ocorrencias=14,
         pares=[('cap. XII', 'cap.\xa0XII'), ('160 a 200 palavras', '160 a 200\xa0palavras'), ('40 palavras', '40\xa0palavras'), ('90 palavras', '90\xa0palavras'), ('D. Dinis', 'D.\xa0Dinis')]),
    dict(i=55, ficheiro='tarefas/m1-u2/index.html', cartao='página da tarefa (HTML)', ocorrencias=22,
         pares=[('cap. XII', 'cap.\xa0XII'), ('cap. CXVI', 'cap.\xa0CXVI'), ('cap. CXLVIII', 'cap.\xa0CXLVIII'), ('século XIX', 'século\xa0XIX'), ('século XV', 'século\xa0XV'), ('3 de setembro de 1384', '3\xa0de\xa0setembro de\xa01384'), ('90 minutos', '90\xa0minutos'), ('160 a 200 palavras', '160 a 200\xa0palavras'), ('10 min', '10\xa0min'), ('10 minutos', '10\xa0minutos'), ('5 minutos', '5\xa0minutos'), ('60 minutos', '60\xa0minutos'), ('15 minutos', '15\xa0minutos'), ('90 min', '90\xa0min'), ('40 palavras', '40\xa0palavras'), ('250 a 300 palavras', '250 a 300\xa0palavras'), ('D. Duarte', 'D.\xa0Duarte')]),
]


# Achados B: o que o próprio achado deixa de fora e o que já estava certo antes desta camada.
# - Mapa (43) e portefólio (48): «1.º ano» só no cabeçalho; o das migalhas é da casca e o achado não o inclui.
# - Índice (27) e guia (25): o achado conta as duas, cabeçalho e migalhas («trilho de navegação»), e as duas mudam.
# - «c. 1860» (F06, F08, F10 e F20): a camada creditos_i_20261105 já o pôs dentro do «i» com espaço que não quebra
#   (<span class="nb">c.&nbsp;1860</span>); fica como está.
EXCLUIR = {
    43: {'1.º ano': ['/pt/1/">1.º ano</a>']},
    48: {'1.º ano': ['/pt/1/">1.º ano</a>']},
}
JA_CONFORME = {32: ['c. 1860'], 34: ['c. 1860'], 35: ['c. 1860'], 39: ['c. 1860']}

# Dados dos geradores. As tarefas da M1-U1 e da M1-U2 (scripts/tarefas_escolha.py) ganham a tabela dos tempos («tabela» e
# «depois» no aquecimento) e «nao_partir» (os números do molde: «90 minutos» na descrição, «10 min» e «90 min» nos
# cabeçalhos); a grelha da M1-U1 ganha «max_em_listas» no critério 4 (scripts/grelhas_tarefas.py); os achados B entram nos
# textos dos dados, que passam iguais para as páginas.
TEMPOS_ADAPTADOS = [['cartões com consulta', '10' + NBSP + 'minutos'], ['lês o enunciado', '5' + NBSP + 'minutos'],
                    ['produção', '60' + NBSP + 'minutos'], ['revisão e entrega', '15' + NBSP + 'minutos'],
                    ['Total', '90' + NBSP + 'minutos']]
TEXTO_AQUECER = ('No início da aula de tarefa: 10 minutos de cartões com consulta, 5 minutos para leres o enunciado, 60 minutos '
                 'de produção e 15 minutos de revisão e entrega. Total: 90 minutos. O relógio de produção começa depois da leitura.')
DADOS = [
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m1-u1.json', entradas=[(None, (17, 52))], tarefa=True),
    dict(ficheiro='docs/pedagogia/tarefas-escolha/m1-u2.json', entradas=[(None, (18, 55))], tarefa=True),
    dict(ficheiro='docs/pedagogia/aquecimentos/m1-u1.json', entradas=[(None, (49,))]),
    dict(ficheiro='docs/pedagogia/grelhas-tarefas-20261027.json', entradas=[('m1-u1', (51, 50)), ('m1-u2', (54, 53))],
         listas='m1-u1'),
]


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def base(rel):
    """O texto do ficheiro sem esta camada (desfeita pelo manifesto, da última troca para a primeira)."""
    texto = ler(rel)
    if MANIFESTO.is_file():
        for edit in reversed(json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(edit['new']) != edit['occurrences']:
                raise SystemExit(f'{rel}: a camada já não confere ({edit["location"]})')
            texto = texto.replace(edit['new'], edit['old'])
    return texto


def edicoes(antigo, novo):
    """As edições atómicas que levam o trecho antigo ao novo: (posição, 'nbsp') troca o espaço nessa posição por U+00A0;
    (posição, 'wj') põe U+2060 antes do carácter nessa posição. Mais nada é permitido num achado B."""
    i = j = 0
    out = []
    while i < len(antigo) or j < len(novo):
        if j < len(novo) and novo[j] == WJ and (i >= len(antigo) or antigo[i] != WJ):
            out.append((i, 'wj'))
            j += 1
        elif i < len(antigo) and j < len(novo) and antigo[i] == novo[j]:
            i += 1
            j += 1
        elif i < len(antigo) and j < len(novo) and antigo[i] == ' ' and novo[j] == NBSP:
            out.append((i, 'nbsp'))
            i += 1
            j += 1
        else:
            raise SystemExit(f'achado B com uma mudança que não é de espaço: {antigo!r} > {novo!r}')
    return out


def aplicar_edicoes(texto, eds):
    for pos, tipo in sorted(eds, reverse=True):
        if tipo == 'nbsp':
            assert texto[pos] == ' ', (pos, texto[pos - 20:pos + 20])
            texto = texto[:pos] + NBSP + texto[pos + 1:]
        else:
            texto = texto[:pos] + WJ + texto[pos:]
    return texto


def janela_novo(pre, s, e, eds):
    """O texto da janela [s, e) de pre com as edições dela aplicadas."""
    return aplicar_edicoes(pre[s:e], [(p - s, t) for p, t in eds])


def janelas_b(rel, pre, pares, regioes, excluir=None, ja_conforme=(), cobertos=(), limite=None):
    """As janelas das ocorrências dos pares (antigo, novo) em pre (a base com as trocas A e C já feitas): [início, fim,
    {edições}, índice do par]. Conta as ocorrências de cada par (dentro do limite, se o houver)."""
    janelas, contagens = [], []
    for k, (antigo, novo) in enumerate(pares):
        eds_rel = edicoes(antigo, novo)
        n = 0
        for m in re.finditer(re.escape(antigo), pre):
            s, e = m.start(), m.end()
            if limite and not (limite[0] <= s and e <= limite[1]):
                continue
            if any(_cobre(pre, s, e, c) for c in (excluir or {}).get(antigo, [])):
                continue
            if any(a <= s < b or a < e <= b for a, b in regioes):
                raise SystemExit(f'{rel}: «{antigo}» dentro do texto novo de um achado A/C')
            janelas.append([s, e, {(s + p, t) for p, t in eds_rel}, k])
            n += 1
        if n == 0 and antigo not in ja_conforme and antigo not in cobertos:
            raise SystemExit(f'{rel}: «{antigo}» não aparece')
        contagens.append(n)
    return janelas, contagens


def juntar(janelas):
    """Junta as janelas que partilham uma edição ou em que uma tem uma edição da outra lá dentro (por exemplo «c. 1460»
    dentro de «1380/1390–c. 1460», ou «90 min» dentro de «90 minutos»): uma troca nunca leva uma edição de outra."""
    janelas = sorted(janelas)
    mudou = True
    while mudou:
        mudou = False
        for a in range(len(janelas)):
            for b in range(a + 1, len(janelas)):
                A, B = janelas[a], janelas[b]
                if A[2] & B[2] or any(A[0] <= p < A[1] for p, _ in B[2]) or any(B[0] <= p < B[1] for p, _ in A[2]):
                    janelas[a] = [min(A[0], B[0]), max(A[1], B[1]), A[2] | B[2], min(A[3], B[3])]
                    del janelas[b]
                    mudou = True
                    break
            if mudou:
                break
    return janelas


def trocas_de_janelas(rel, base_txt, pre, janelas, pares, achado, local):
    """Uma troca por texto de janela; quando esse texto aparece noutro sítio que não muda, a janela cresce para os dois lados
    (sem apanhar edições de outras janelas) até ficar única para as suas ocorrências. Devolve (trocas, texto final)."""
    todas = set().union(*[j[2] for j in janelas]) if janelas else set()
    final = aplicar_edicoes(pre, todas)
    grupos = {}
    for s, e, eds, k in janelas:
        grupos.setdefault((k, pre[s:e]), []).append((s, e, eds))
    trocas = []
    for (k, _), membros in sorted(grupos.items(), key=lambda g: (g[0][0], g[1][0][0])):
        for antigo, novo, n in _contexto(rel, base_txt, pre, final, membros, todas):
            trocas.append({'ficheiro': rel, 'local': local(k, pares[k][0], antigo), 'antigo': antigo, 'novo': novo,
                           'ocorrencias': n, 'achado': achado(k)})
    return trocas, final


def _cobre(pre, s, e, contexto):
    """A ocorrência [s, e) está dentro de uma ocorrência do contexto excluído."""
    a0 = max(0, s - len(contexto))
    for m in re.finditer(re.escape(contexto), pre[a0:e + len(contexto)]):
        if a0 + m.start() <= s and e <= a0 + m.end():
            return True
    return False


def _contexto(rel, base_txt, pre, final, membros, todas):
    # Por fim, a linha inteira (nos dados dos geradores, cada texto está numa linha).
    for L, R in [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (2, 0), (2, 2), (0, 4), (4, 0), (4, 4), (8, 8), (16, 16), (32, 32),
                 (64, 64)] + [('linhas', n) for n in range(0, 8)]:
        sub = {}
        ok = True
        for s, e, eds in membros:
            if L == 'linhas':
                # A linha e as R linhas de cada lado (nos dados, um texto repetido noutra tarefa distingue-se pelos vizinhos).
                a, b = pre.rfind('\n', 0, s) + 1, pre.find('\n', e)
                for _ in range(R):
                    a = pre.rfind('\n', 0, max(a - 1, 0)) + 1
                    b = pre.find('\n', b + 1) if pre.find('\n', b + 1) > 0 else len(pre)
            else:
                a, b = s - L, e + R
            if a < 0 or b > len(pre) or any(a <= p < b and (p, t) not in eds for p, t in todas):
                ok = False
                break
            chave = (pre[a:b], janela_novo(pre, a, b, eds))
            sub[chave] = sub.get(chave, 0) + 1
        if ok and all(base_txt.count(an) == n and pre.count(an) == n and final.count(no) == n and base_txt.count(no) == 0
                      and final.replace(no, '\0').count(an) == 0 for (an, no), n in sub.items()):
            return [(an, no, n) for (an, no), n in sub.items()]
    raise SystemExit(f'{rel}: não há contexto que distinga «{pre[membros[0][0]:membros[0][1]]}»')


def local_b(pagina):
    def f(k, par, antigo):
        if antigo == par:
            return f'{pagina}: «{par}» com espaço que não quebra'
        contexto = antigo if len(antigo) <= 60 else antigo[:57].rstrip() + '…'
        return f'{pagina}: «{par}» com espaço que não quebra (com o contexto «{contexto}»)'
    return f


def nome(rel):
    m = re.match(r'm1/licao-(m1-f\d+)/', rel)
    return m.group(1).upper() if m else rel.replace('/index.html', '')


def substituir(pre, regioes, antes, depois):
    """Troca um trecho único e atualiza as regiões de texto novo (onde nenhum par B pode cair)."""
    if pre.count(antes) != 1:
        raise SystemExit(f'trecho que não aparece uma vez: {antes[:80]!r}')
    inicio = pre.index(antes)
    delta = len(depois) - len(antes)
    regioes = [(a if a < inicio else a + delta, b if b <= inicio else b + delta) for a, b in regioes]
    return pre.replace(antes, depois), regioes + [(inicio, inicio + len(depois))]


def trocas_pagina(rel, achados_ac, achados_b):
    base_txt = base(rel)
    pre, regioes, trocas, relatorio = base_txt, [], [], []
    for x in achados_ac:
        pre, regioes = substituir(pre, regioes, x['antigo'], x['novo'])
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}, {x["cartao"]}', 'antigo': x['antigo'], 'novo': x['novo'],
                       'ocorrencias': 1,
                       'achado': ACHADO.format(i=x['i'], cat=x['cat'], texto=TEXTO_CAT[x['cat']] + (' ' + x['nota'] if x.get('nota') else ''))})
        relatorio.append((rel, x['i'], x['cat'], 1, 1, ''))
    if rel in COM_TABELA:
        ligacoes = re.findall(r'<link rel="stylesheet" href="((?:\.\./)+)assets/appearance\.css\?v=[^"]+">', pre)
        if len(ligacoes) != 1:
            raise SystemExit(f'{rel}: a ligação à camada de aparência não aparece uma vez')
        aparencia = re.search(r'<link rel="stylesheet" href="(?:\.\./)+assets/appearance\.css\?v=[^"]+">', pre).group(0)
        folha = FOLHA.format(ligacoes[0])
        pre, regioes = substituir(pre, regioes, aparencia, folha + aparencia)
        gerada = ' (a tarefa é gerada: a folha entra também pelo gerador, scripts/tarefas_escolha.py)' if rel.startswith('tarefas/') else ''
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}, cabeça: a folha das tabelas de apoio, antes da camada de aparência',
                       'antigo': aparencia, 'novo': folha + aparencia, 'ocorrencias': 1,
                       'achado': ACHADO.format(i=', '.join(str(x['i']) for x in achados_ac if x['cat'] == 'A'), cat='A',
                                               texto=f'A {COM_TABELA[rel]} passa a carregar as tabelas de apoio, antes da camada de aparência{gerada}.')})
    for x in achados_b:
        cobertos = {p for p, _ in x['pares'] if any(a['antigo'].count(p) for a in achados_ac)}
        janelas, contagens = janelas_b(rel, pre, x['pares'], regioes, EXCLUIR.get(x['i']), JA_CONFORME.get(x['i'], ()), cobertos)
        ts, final = trocas_de_janelas(rel, base_txt, pre, juntar(janelas), x['pares'],
                                      lambda k, i=x['i']: ACHADO.format(i=i, cat='B', texto=TEXTO_CAT['B']), local_b(nome(rel)))
        pre = final
        trocas += ts
        relatorio.append((rel, x['i'], 'B', sum(contagens), x['ocorrencias'],
                          ' '.join(f'{p[0]!r}x{c}' for p, c in zip(x['pares'], contagens))))
    return base_txt, pre, trocas, relatorio


def trocas_dados(spec, por_i):
    rel = spec['ficheiro']
    base_txt = base(rel)
    obj = json.loads(base_txt)
    pre, regioes, trocas = base_txt, [], []

    def limite_de(entrada):
        if entrada is None:
            return None
        inicio = pre.index(f'\n  "{entrada}": {{')
        fim = pre.find('\n  "', inicio + 5)
        return (inicio, fim if fim > 0 else len(pre))

    if spec.get('tarefa'):
        i_a, i_b = spec['entradas'][0][1]
        antigo = '  "texto": ' + json.dumps(TEXTO_AQUECER, ensure_ascii=False) + ','
        tabela = {'colunas': ['Momento', 'Tempo'], 'linhas': TEMPOS_ADAPTADOS}
        novo = ('  "texto": "No início da aula de tarefa:",\n  "tabela": '
                + json.dumps(tabela, ensure_ascii=False, indent=1).replace('\n', '\n  ')
                + ',\n  "depois": "O relógio de produção começa depois da leitura.",')
        pre, regioes = substituir(pre, regioes, antigo, novo)
        trocas.append({'ficheiro': rel, 'local': 'Dados da tarefa, aquecimento: os tempos da aula numa tabela («tabela» e «depois»)',
                       'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
                       'achado': ACHADO.format(i=i_a, cat='A', texto=TEXTO_CAT['A'] + ' ' + por_i[i_a]['nota'])})
        antes = f'\n "unidade": {obj["unidade"]},\n'
        depois_ = f'\n "unidade": {obj["unidade"]},\n "nao_partir": true,\n'
        pre, regioes = substituir(pre, regioes, antes, depois_)
        trocas.append({'ficheiro': rel, 'local': 'Dados da tarefa: «nao_partir», os números do molde com espaço que não quebra',
                       'antigo': antes, 'novo': depois_, 'ocorrencias': 1,
                       'achado': ACHADO.format(i=i_b, cat='B', texto=TEXTO_CAT['B'] + ' Os números do molde da tarefa ('
                                               '«90 minutos» na descrição, «10 min» e «90 min» nos cabeçalhos) levam o espaço pelo gerador.')})
    if spec.get('listas'):
        antes = '     "nome": "Tema à escolha (A ou B): cinco elementos e a justificação",\n     "max": 6,\n'
        lim = limite_de(spec['listas'])
        if pre[lim[0]:lim[1]].count(antes) != 1:
            raise SystemExit(f'{rel}: âncora do critério 4 não aparece uma vez na entrada {spec["listas"]}')
        pre, regioes = substituir(pre, regioes, antes, antes + '     "max_em_listas": true,\n')
        trocas.append({'ficheiro': rel, 'local': 'Grelha da M1-U1, critério 4, nível 6: os elementos de cada tema em lista («max_em_listas»)',
                       'antigo': antes, 'novo': antes + '     "max_em_listas": true,\n', 'ocorrencias': 1,
                       'achado': ACHADO.format(i=21, cat='C', texto=TEXTO_CAT['C'] + ' Só na grelha do aluno; na versão de '
                                               'correção, o texto está num <small> dentro de uma célula e fica como está.')})
    janelas, pares, nomes = [], [], []
    for entrada, achados in spec['entradas']:
        lim = limite_de(entrada)
        vistos = set()
        for i in achados:
            x = por_i.get(i)
            if not x or x['cat'] != 'B':
                continue
            for p in x['pares']:
                trecho = pre[lim[0]:lim[1]] if lim else pre
                if p[0] in vistos or not trecho.count(p[0]):
                    continue
                vistos.add(p[0])
                js, _ = janelas_b(rel, pre, [p], regioes, limite=lim)
                for j in js:
                    j[3] = len(pares)
                janelas += js
                pares.append(p)
                nomes.append((entrada, '/'.join(str(a) for a in achados if por_i.get(a, {}).get('cat') == 'B')))
    rotulo = 'Dados ' + Path(rel).stem
    ts, final = trocas_de_janelas(
        rel, base_txt, pre, juntar(janelas), pares,
        lambda k: ACHADO.format(i=nomes[k][1], cat='B', texto=TEXTO_CAT['B'] + ' Nos dados do gerador, que passam iguais para as páginas.'),
        lambda k, par, antigo: local_b(rotulo + (f', {nomes[k][0]}' if spec['entradas'][0][0] else ''))(k, par, antigo))
    return base_txt, final, trocas + ts


def main():
    por_pagina = {}
    for x in ACHADOS_AC:
        por_pagina.setdefault(x['ficheiro'], ([], []))[0].append(x)
    for x in ACHADOS_B:
        por_pagina.setdefault(x['ficheiro'], ([], []))[1].append(dict(x, cat='B'))
    por_i = {x['i']: x for x in ACHADOS_AC}
    por_i.update({x['i']: dict(x, cat='B') for x in ACHADOS_B})
    finais, relatorio = {}, []
    for rel in sorted(por_pagina):
        ac, bs = por_pagina[rel]
        base_txt, final, trocas, rel_pag = trocas_pagina(rel, ac, bs)
        finais[rel] = (base_txt, final, trocas)
        relatorio += rel_pag
    for spec in DADOS:
        finais[spec['ficheiro']] = trocas_dados(spec, por_i)
    # Confere cada ficheiro como o aplicar_trocas.py o vai conferir: a partir da base, e com tudo já aplicado.
    for rel, (base_txt, final, trocas) in finais.items():
        lista = list(enumerate(trocas, 1))
        try:
            b, depois, _ = processar(rel, lista, base_txt)
            assert b == base_txt and depois == final, rel
            b, depois, _ = processar(rel, lista, final)
            assert b == base_txt and depois == final, rel
        except (TrocaFalhou, AssertionError) as erro:
            raise SystemExit(f'{rel}: as trocas não conferem: {erro}')
    if '--relatorio' in sys.argv:
        for r in relatorio:
            print(*r)
    todas = [t for rel in finais for t in finais[rel][2]]
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {len(finais)} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
