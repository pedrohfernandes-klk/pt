#!/usr/bin/env python3
"""15/11/2026: revisão geral antes de publicar, com as decisões do utilizador de 15/11/2026 («decide tu mesmo isso tudo já»): sem
«ficha» nem «sozinho» no texto dirigido ao aluno, sem tarefas de pares, sem retratos de pessoas identificáveis e só vídeos oficiais.

O que muda (os achados confirmados da revisão geral, conferidos um a um na árvore antes de entrar):
- «ficha» (decisão f): no Atlas, «Faz uma pequena ficha de escuta» passa a «Faz um pequeno registo de escuta» (assets/atlas-editorial.js,
  achado 4) e a «ficha técnica» passa a «informação técnica» (assets/atlas-explorar.js, achado 5). Na segunda frase do achado 5, a
  proposta «a informação técnica indica sobre os materiais» não se diz em português; fica «a informação técnica descreve os
  materiais», com o mesmo sentido. As versões dos dois ficheiros mudam em atlas/index.html, para os navegadores não usarem a cópia
  antiga, como a decisão 154 fez (autonomia_154_20261105);
- tarefas de pares (decisão e): na M9-F12, «Com um colega, prepara duas frases» passa a «Prepara por escrito duas frases»
  (m9/recursos/f12.js, achado 6); nas notas para a aula da M9-F11 e da M9-F12, «explica a um colega uma escolha e o seu limite»
  passa a «explica por escrito, em duas frases, uma escolha e o seu limite» (achado 7; as duas lições pedem duas frases: «Testa duas
  frases» na F11, «prepara duas frases» na F12);
- «sozinho» (decisão f, marca de género de quem lê): nas provas em cartões, «tentas primeiro sozinho» passa a «tentas primeiro por
  ti» (achado 8), na secção exame/provas/index.html, nas lições do Grupo I e do Grupo II das duas provas de 2026 e nos dados de onde
  essas lições saem (scripts/provas/dados/AAAA-Nf/grupo-x.json). A frase da secção está no molde do gerador (scripts/provas/gerar.py):
  o gerador passa a lê-la de seccao.json («entrada», chave nova que entra nesta camada, com os dados) e, sem a chave, dá a frase de
  antes, byte a byte, para as camadas de baixo (cuidado_exame_20261112 e exame_provas_oficial_20261112) continuarem a gerar a secção
  como a deixaram, como fez a camada exame_provas_oficial_20261112 com «nao_partir». O gerador muda fora da camada (é código, como
  nessa camada);
- retratos de pessoas identificáveis (decisão a): sai a imagem, com o crédito e a legenda; o texto do cartão fica. José Saramago no
  primeiro cartão da M9-F11 (m9/recursos/f11.js, achado 11), Eugénio de Andrade no da M8-F13 (achado 22) e Ana Luísa Amaral no da
  M8-F14 (achado 23). As duas lições do M8 são geradas (scripts/gerar_licoes_20261101.py): o registo das imagens
  (scripts/imagens_licoes_20261101.py, IMAGENS e USOS) perde os dois retratos fora da camada (fonte do gerador, como nas camadas do
  cuidado do M5 e do M8), e as páginas mudam aqui e saem iguais do gerador. A lista fechada dos créditos longos à vista
  (tests/fixtures/creditos-a-vista-20261105.json) perde a entrada do retrato da M9-F11, que fica a zero. Os três ficheiros de imagem,
  sem uso, saem do repositório (não são trocas);
- vídeos que não são do canal do titular (decisão b): sai o vídeo, com o botão, o crédito e o «No caderno» que dependia só dele. Na
  M5-F14, o trailer do filme (canal «Alexandre Oliveira») do «O essencial» e o bailado da Companhia Nacional de Bailado (canal «Teatro
  Micaelense») do «Para levar» (achado 10); na M5-F15, Teresa Pinto Coelho na RTP1 (canal «Instituto de História Contemporânea»)
  do «O essencial» (achado 9). Os cartões ficam com o texto que já tinham. O dossiê do tema B da tarefa M5-U2 tinha um facto cuja
  única fonte no sítio era o crédito desse vídeo («A 8 de janeiro de 2025, Eça recebe honras de Panteão.», com a fonte «o vídeo de
  Teresa Pinto Coelho»): sai, sem inventar outra fonte, dos dados (docs/pedagogia/tarefas-escolha/m5-u2.json) e da página
  (tarefas/m5-u2/index.html), que sai igual do gerador; o tema B continua a pedir um facto datado do dossiê, que fica com quatro;
- Exame, sessão 27 (decisão b, achado 13): sai o objeto «video» (a masterclass da «Academia X», os dois trechos, as perguntas
  s27-video1 a s27-video4, a nota e o playbackNote) e as etiquetas «vídeo» e «compreensão oral». A sessão fica com a alternativa em
  texto: o antigo video.fallback, palavra por palavra, abre o contexto do texto (source.context), que o motor mostra na fase Ler, antes
  dos dois casos, e em «Consultar o texto» no aquecimento; a nota do texto guarda a indicação da Informação-Prova que estava em
  video.note; a instrução e o critério da escrita deixam de remeter para os trechos. assets/exame/app.js não muda: o vídeo já era
  opcional (phaseLabel, currentQuestions e phaseContent testam session.video) e a s27 segue o caminho das outras 26 sessões.

Fica de fora (e porquê):
- a crónica do M1 (achado 19): não é um problema (decisão c);
- a legenda «Grafismo gerado com recurso a IA, EPI, 2026.» (decisão d, achados 0, 12, 20 e 21): nos índices, lições, painéis,
  atividades e mapas do M2, do M3, do M6 e do M9 não há grafismo ilustrativo feito por código (os SVG são ícones de interface
  aria-hidden, emblemas dos cartões, divisórias de calçada e as formas de 16 px que marcam os pares ligados; não há canvas; os PNG
  embutidos são códigos QR e os JPEG são reproduções de obras): nenhuma página leva a legenda, que continua só na entrada (o «i» do
  fundo da calçada). As imagens embutidas de origem por confirmar (as galerias «Para ver» dos mapas do M6 e do M9 e as figuras das
  lições do M6 e do M9) não se legendam: ficam na nota do relatório;
- o mesmo retrato de José Saramago (fotografia de Mario Antonio Pena), embutido em base64 na M9-F10 e no mapa do M9, e os retratos de
  Camilo (M5-F17), de Antero (M6-F14) e de Cesário Verde (desenho de Columbano): a decisão (a) nomeia os três retratos desta camada;
  os outros ficam para o docente;
- a pergunta do aquecimento da sessão 27 («Como usar uma proposta de estudo apresentada num vídeo?») e o título da sessão («Ver,
  compreender, estudar melhor»): são genéricos e não dependem do vídeo que sai;
- os registos históricos (docs/qa/) e os manifestos das camadas de baixo, que guardam os textos antigos de propósito.

A camada é literal e fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima da fila final (fila_final_20261115),
com a qual partilha assets/exame/sessoes.json. Partilha ficheiros com 23 camadas de baixo, que a desfazem primeiro: a fila final, as
tarefas do M5 mais fáceis de fazer (a tarefa M5-U2), as provas em cartões com os documentos oficiais, a decisão 152 no Exame, no M9, no
M8, no M6 e no M5, a revisão dos enunciados das tarefas, a cidade do cartaz, os créditos atrás de um «i» do pedido pt-1, o lote 3 do
Atlas, a autonomia 154, o contexto e a lição do Laboratório do exame, o lote 2, a varredura de formatação, as tarefas individuais, as
lições do M1 ao M6, as tarefas do M3, do M5 e do M6, a língua das perguntas, as opções equilibradas e o texto justificado
(tests/test_revisao_geral_20261115.py confere cada uma com esta desfeita primeiro).

Constrói scripts/revisao_geral_20261115.json, que se aplica com scripts/aplicar_trocas.py; o manifesto fica em
tests/fixtures/revisao-geral-edits-20261115.json:

  python3 scripts/revisao_geral_20261115.py
  python3 scripts/aplicar_trocas.py scripts/revisao_geral_20261115.json \\
      --manifesto tests/fixtures/revisao-geral-edits-20261115.json \\
      --base-commit 2ee5309baa209e3d2497e8a244819b17f2c0de4f --nota "…"

Sem argumentos, o script confere que as trocas dão da base (a árvore com esta camada desfeita pelo manifesto, se o houver) o estado
da árvore, e escreve o JSON. Os blocos que saem (as figuras, os vídeos e o objeto «video» da s27) leem-se da base, entre o seu
início e o seu fim, e cada troca ancora-se no texto vizinho (o aplicar_trocas.py não aceita um «novo» vazio). Pode voltar a correr
depois de a camada estar aplicada e dá o mesmo JSON.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/revisao_geral_20261115.json'
MANIFESTO = ROOT / 'tests/fixtures/revisao-geral-edits-20261115.json'


def base(rel):
    """O ficheiro sem esta camada (desfeita pelo manifesto, se o houver e a camada estiver aplicada)."""
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    if MANIFESTO.is_file():
        edits = json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])
        if edits and all(texto.count(e['new']) == e['occurrences'] for e in edits):
            for e in reversed(edits):
                texto = texto.replace(e['new'], e['old'])
    return texto


def bloco(rel, inicio, fim):
    """O bloco da base de rel que começa em «inicio» (uma só vez na base) e acaba no primeiro «fim» a seguir (inclusive)."""
    texto = base(rel)
    if texto.count(inicio) != 1:
        raise SystemExit(f'{rel}: «{inicio[:60]}» aparece {texto.count(inicio)} vezes na base')
    i = texto.index(inicio)
    return texto[i:texto.index(fim, i) + len(fim)]


def tirar(rel, antes, inicio, fim, depois):
    """A troca que tira o bloco (de «inicio» a «fim»), ancorada no texto que acaba logo antes dele e no que começa logo a seguir:
    o antigo é antes + bloco + depois e o novo é antes + depois (o novo nunca está dentro do antigo)."""
    b = bloco(rel, inicio, fim)
    texto = base(rel)
    if texto.count(antes + b + depois) != 1:
        raise SystemExit(f'{rel}: o bloco «{inicio[:60]}» não está entre as âncoras')
    return antes + b + depois, antes + depois


ACHADO_FICHA = ('15/11/2026: revisão geral: «ficha» é palavra proibida no texto dirigido ao aluno (decisão f do utilizador): passa a '
                '«registo» e a «informação técnica», com o mesmo sentido.')
ACHADO_VERSOES = ('15/11/2026: revisão geral: as versões do atlas-editorial.js e do atlas-explorar.js mudam com o texto, para os '
                  'navegadores não usarem a cópia antiga (como fez a decisão 154).')
ACHADO_PARES = ('15/11/2026: revisão geral: não há tarefas de pares (decisão e do utilizador): o que se fazia com um colega passa a '
                'trabalho individual, por escrito, com o mesmo objetivo.')
ACHADO_SOZINHO = ('15/11/2026: revisão geral: «sozinho» marca o género de quem lê (decisão f do utilizador): «tentas primeiro sozinho» '
                  'passa a «tentas primeiro por ti».')
ACHADO_RETRATOS = ('15/11/2026: revisão geral: nas imagens, nenhuma pessoa identificável (decisão a do utilizador): sai o retrato, com '
                   'o crédito e a legenda; o texto do cartão fica.')
ACHADO_VIDEOS = ('15/11/2026: revisão geral: só vídeos oficiais (decisão b do utilizador): sai o vídeo que não é do canal do titular, '
                 'com o crédito e o que dependia só dele; o cartão fica com o que já estava na página, sem nada inventado.')
ACHADO_S27 = ('15/11/2026: revisão geral: só vídeos oficiais (decisão b do utilizador): a sessão 27 perde a masterclass da «Academia X» '
              '(canal privado), com os trechos e as perguntas que dependiam só dela, e fica com a alternativa em texto.')

EDITORIAL, EXPLORAR, ATLAS = 'assets/atlas-editorial.js', 'assets/atlas-explorar.js', 'atlas/index.html'
F12, P11, P12 = 'm9/recursos/f12.js', 'm9/painel-m9-f11/index.html', 'm9/painel-m9-f12/index.html'
SECCAO, SECCAO_DADOS = 'exame/provas/index.html', 'scripts/provas/dados/seccao.json'
GRUPOS = [(f'exame/provas/{p}/{g}/index.html', f'scripts/provas/dados/{p}/{g}.json', f'{fase}, {nome}')
          for p, fase in (('2026-1f', '1.ª fase de 2026'), ('2026-2f', '2.ª fase de 2026'))
          for g, nome in (('grupo-i', 'Grupo I'), ('grupo-ii', 'Grupo II'))]
F11, M8F13, M8F14 = 'm9/recursos/f11.js', 'm8/licao-m8-f13/index.html', 'm8/licao-m8-f14/index.html'
M5F14, M5F15 = 'm5/licao-m5-f14/index.html', 'm5/licao-m5-f15/index.html'
U2_DADOS, U2 = 'docs/pedagogia/tarefas-escolha/m5-u2.json', 'tarefas/m5-u2/index.html'
SESSOES = 'assets/exame/sessoes.json'

ENTRADA = ('Os exames nacionais de Português, grupo a grupo. Lês o texto da prova com a numeração da prova e, a seguir a cada parte, '
           'fazes os cartões: o que pede o verbo, que linhas provam, o plano da resposta. A resposta completa escreve-se no caderno, '
           'com a grelha oficial à vista, e só depois a comparas com exemplos e com os critérios. Nos itens de escolha, tentas '
           'primeiro por ti e depois vês porquê.')

TROCAS = [
    (EDITORIAL, 'Atlas, José Carlos Schwarz («Ouvir»): «Faz um pequeno registo de escuta com três campos»',
     'Faz uma pequena ficha de escuta com três campos', 'Faz um pequeno registo de escuta com três campos', ACHADO_FICHA),
    (EXPLORAR, 'Atlas, explorar Almada e Amadeo («Material»): «Consulta a informação técnica.»',
     'Consulta a ficha técnica.', 'Consulta a informação técnica.', ACHADO_FICHA),
    (EXPLORAR, 'Atlas, explorar Almada e Amadeo («Rever»): «a informação técnica descreve os materiais»',
     'a ficha técnica informa sobre os materiais', 'a informação técnica descreve os materiais', ACHADO_FICHA),
    (ATLAS, 'Versão do atlas-editorial.js, para os navegadores não usarem a cópia antiga',
     'atlas-editorial.js?v=20261105-autonomia-1', 'atlas-editorial.js?v=20261115-revisao-geral-1', ACHADO_VERSOES),
    (ATLAS, 'Versão do atlas-explorar.js, para os navegadores não usarem a cópia antiga',
     'atlas-explorar.js?v=20261105-autonomia-1', 'atlas-explorar.js?v=20261115-revisao-geral-1', ACHADO_VERSOES),
    (F12, 'M9-F12, «Uma defesa com limites»: «Prepara por escrito duas frases», sem colega',
     '<p>Com um colega, prepara duas frases:', '<p>Prepara por escrito duas frases:', ACHADO_PARES),
    (P11, 'Notas para a aula da M9-F11: «explica por escrito, em duas frases, uma escolha e o seu limite»',
     'explica a um colega uma escolha e o seu limite.', 'explica por escrito, em duas frases, uma escolha e o seu limite.', ACHADO_PARES),
    (P12, 'Notas para a aula da M9-F12: «explica por escrito, em duas frases, uma escolha e o seu limite»',
     'explica a um colega uma escolha e o seu limite.', 'explica por escrito, em duas frases, uma escolha e o seu limite.', ACHADO_PARES),
    (SECCAO_DADOS, 'Secção das provas em cartões: a frase de entrada passa aos dados («entrada»), com «tentas primeiro por ti»',
     ' "nao_partir": true,\n "seguir":',
     ' "nao_partir": true,\n "_entrada": "15/11/2026: a frase de entrada da secção (o parágrafo of-entrada), sem marca de género para '
     'quem lê («tentas primeiro por ti»). Sem esta chave, scripts/provas/gerar.py escreve a frase de antes.",\n "entrada": '
     + json.dumps(ENTRADA, ensure_ascii=False) + ',\n "seguir":', ACHADO_SOZINHO),
    (SECCAO, 'Secção das provas em cartões: «Nos itens de escolha, tentas primeiro por ti e depois vês porquê.»',
     'tentas primeiro sozinho e depois vês porquê.', 'tentas primeiro por ti e depois vês porquê.', ACHADO_SOZINHO),
]
for _pagina, _dados, _nome in GRUPOS:
    TROCAS.append((_dados, f'Dados da prova da {_nome}, cartão «Abre»: «tentas primeiro por ti»', 'tentas primeiro sozinho',
                   'tentas primeiro por ti', ACHADO_SOZINHO))
    TROCAS.append((_pagina, f'Lição da prova da {_nome}, cartão «Abre»: «tentas primeiro por ti»', 'tentas primeiro sozinho',
                   'tentas primeiro por ti', ACHADO_SOZINHO))

TROCAS.append((F11, 'M9-F11, «O cuidado também é ação»: sai o retrato de José Saramago, com o crédito e a legenda',
               *tirar(F11, '"html":"', '<figure class=\\"fig\\"><img src=\\"../../img/fontes/saramago-2005.jpg\\"', '</figure>',
                      '<p class=\\"abre\\">Construir, ver, procurar'), ACHADO_RETRATOS))
TROCAS.append((M8F13, 'M8-F13, «Quando as palavras se gastam»: sai o retrato de Eugénio de Andrade (a figura, o «i» dos créditos e a legenda)',
               *tirar(M8F13, '"html":"', '<figure class=\\"fig documento\\"><a href=\\"../../img/fontes/licoes-20261101/eugenio.jpg\\"',
                      '<\\/figure>', '<p class=\\"abre\\"><strong>Como pode um poema'), ACHADO_RETRATOS))
TROCAS.append((M8F14, 'M8-F14, «A história de uma tigela»: sai o retrato de Ana Luísa Amaral (a figura, o «i» dos créditos e a legenda)',
               *tirar(M8F14, '"html":"', '<figure class=\\"fig documento\\"><a href=\\"../../img/fontes/licoes-20261101/amaral.jpg\\"',
                      '<\\/figure>', '<p class=\\"abre\\"><strong>Quem decide o que merece'), ACHADO_RETRATOS))

TROCAS.append((M5F14, 'M5-F14, «O essencial»: sai o trailer do filme do canal «Alexandre Oliveira» (o botão, o «No caderno» e o crédito)',
               *tirar(M5F14, 'e o que a escolha ganha e perde.</span></li></ol>', '<div class=\\"yt\\" data-yt=\\"S_hGdGKAkv8\\"', '</div>',
                      '"},{"t":"ler","rot":"Em paralelo","titulo":"O livro e o filme"'), ACHADO_VIDEOS))
TROCAS.append((M5F14, 'M5-F14, «Para levar»: sai o bailado do canal «Teatro Micaelense» (o botão, o «No caderno» e o crédito)',
               *tirar(M5F14, 'Não uses o exemplo inventado como prova sobre o filme.</p></details>', '<div class=\\"yt\\" data-yt=\\"UVrhS1QOQyw\\"',
                      '</div>', '"}],A2ID=null;'), ACHADO_VIDEOS))
TROCAS.append((M5F15, 'M5-F15, «O essencial»: sai o vídeo da RTP1 do canal «Instituto de História Contemporânea» (o botão, o «No caderno» e o crédito)',
               *tirar(M5F15, 'revês também o indireto livre e a estrutura circular.</span></li></ol>', '<div class=\\"yt\\" data-yt=\\"VjSVmIj8CbI\\"',
                      '</div>', '"},{"t":"ler","rot":"Em paralelo","titulo":"Romantismo e Realismo"'), ACHADO_VIDEOS))
TROCAS.append((U2_DADOS, 'Dados da tarefa M5-U2, dossiê do tema B: sai o facto de 2025, cuja única fonte era o vídeo que sai da M5-F15',
               *tirar(U2_DADOS, '«Linha de vida»"\n  }', ',\n  {\n   "facto": "A 8', '(o vídeo de Teresa Pinto Coelho)"\n  }', '\n ],\n "opcional"'),
               ACHADO_VIDEOS))
TROCAS.append((U2, 'Tarefa M5-U2, dossiê do tema B: sai o facto de 2025, cuja única fonte era o vídeo que sai da M5-F15',
               *tirar(U2, '«Linha de vida»</a></span></li>', '<li>A 8', '(o vídeo de Teresa Pinto Coelho)</a></span></li>', '</ol></section>'),
               ACHADO_VIDEOS))

_VIDEO = bloco(SESSOES, '\n      "video": {\n        "title": "Masterclass Exame Nacional de Português"', '\n      },')
_FALLBACK = json.loads('{' + _VIDEO.strip().rstrip(',') + '}')['video']['fallback']
TROCAS += [
    (SESSOES, 'Sessão 27, etiquetas: saem «vídeo» e «compreensão oral»',
     '"tags": [\n        "vídeo",\n        "compreensão oral",\n        "método de estudo",', '"tags": [\n        "método de estudo",',
     ACHADO_S27),
    (SESSOES, 'Sessão 27, contexto do texto: a alternativa em texto (o antigo video.fallback, palavra por palavra) antes dos dois casos',
     '"context": "Lê os dois casos. O que permite verificar a aprendizagem de cada aluno?"',
     '"context": ' + json.dumps(_FALLBACK + ' Lê os dois casos. O que permite verificar a aprendizagem de cada aluno?', ensure_ascii=False),
     ACHADO_S27),
    (SESSOES, 'Sessão 27, nota do texto: sem o vídeo, com a indicação da Informação-Prova que estava em video.note',
     '"note": "Casos fictícios. O vídeo é uma fonte de propostas de estudo, não uma previsão do exame."',
     '"note": "Casos fictícios. A proposta de estudo não é uma previsão do exame. Para a estrutura, a duração e as regras da prova, '
     'consulta a Informação-Prova da tua época em «Programa e fontes»."', ACHADO_S27),
    (SESSOES, 'Sessão 27: sai o objeto «video» (a masterclass da «Academia X», os dois trechos e as perguntas s27-video1 a s27-video4)',
     'do resultado do ensaio."\n        }\n      ],' + _VIDEO + '\n      "writing": {',
     'do resultado do ensaio."\n        }\n      ],\n      "writing": {', ACHADO_S27),
    (SESSOES, 'Sessão 27, instrução da escrita: «volta à proposta de estudo»',
     '"Consulta os casos e volta aos trechos ou à alternativa em texto quando precisares."',
     '"Consulta os casos e volta à proposta de estudo quando precisares."', ACHADO_S27),
    (SESSOES, 'Sessão 27, critério da escrita: «Usei uma ideia da proposta de estudo»',
     '"Usei uma ideia dos trechos ou da alternativa em texto, sem a tomar como garantia de resultado."',
     '"Usei uma ideia da proposta de estudo, sem a tomar como garantia de resultado."', ACHADO_S27),
]

FICHEIROS = []
for _t in TROCAS:
    if _t[0] not in FICHEIROS:
        FICHEIROS.append(_t[0])


def trocas():
    return [{'ficheiro': f, 'local': l, 'antigo': a, 'novo': n, 'ocorrencias': 1, 'achado': ach} for f, l, a, n, ach in TROCAS]


def main():
    todas = trocas()
    for rel in FICHEIROS:
        lista = [(i, t) for i, t in enumerate(todas, 1) if t['ficheiro'] == rel]
        try:
            processar(rel, lista, base(rel))
        except TrocaFalhou as erro:
            raise SystemExit(f'{rel}: as trocas não conferem: {erro}')
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {len(FICHEIROS)} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
