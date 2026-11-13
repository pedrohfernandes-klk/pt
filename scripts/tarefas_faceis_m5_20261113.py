#!/usr/bin/env python3
"""13/11/2026: as duas tarefas do M5 (m5-u1 e m5-u2) «mais fáceis de fazer», com tudo o que fala delas a usar as mesmas palavras, e
dois acertos do M3 decididos pelo docente no mesmo dia.

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201, camada tarefas_faceis_m3_20261112) e
levado ao M1 (pedido #203, camada tarefas_faceis_m1_20261113). Esta camada leva o mesmo molde ao M5. Cada tarefa é a mesma (as mesmas
perguntas, os mesmos temas A e B, o mesmo total de palavras, os mesmos critérios da grelha); muda só a forma.

Constrói scripts/tarefas_faceis_m5_20261113.json, a camada literal tarefas_faceis_m5_20261113, que se aplica com
scripts/aplicar_trocas.py; o manifesto fica em tests/fixtures/tarefas-faceis-m5-edits-20261113.json:

  python3 scripts/tarefas_faceis_m5_20261113.py
  python3 scripts/aplicar_trocas.py scripts/tarefas_faceis_m5_20261113.json \\
      --manifesto tests/fixtures/tarefas-faceis-m5-edits-20261113.json \\
      --base-commit e2e73379e75fd5dd4bc68009e63071c836333356 --nota "…"

Fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima das tarefas do M1 mais fáceis de fazer
(tarefas_faceis_m1_20261113), com a qual partilha um ficheiro: os dados das grelhas (docs/pedagogia/grelhas-tarefas-20261027.json).
Com a camada das tarefas do M3 (tarefas_faceis_m3_20261112) partilha três: os dados das grelhas, os dados da m3-u2 e o enunciado da
m3-u2. Partilha ficheiros também com a revisão dos enunciados (tarefas_claras_20261110), com a decisão 152 no M3, no M5 e no M6
(cuidado_m3_20261108, cuidado_m5_20261108 e cuidado_m6_20261108) e com as camadas mais antigas do índice, do guia, do mapa e do
portefólio: todas a desfazem primeiro.

Ficheiros (20):
- os dados: docs/pedagogia/tarefas-escolha/m5-u1.json e m5-u2.json (a chave nova «facil», de onde sai a página; as chaves antigas
  ficam como estavam, para a leitura histórica das camadas de baixo, e já não aparecem na página), docs/pedagogia/
  grelhas-tarefas-20261027.json («autoavaliacao_so_tua» e «trocas_aluno» nas duas grelhas do M5, e os exemplos de dois critérios
  de cada grelha, que deixam de usar passagens dos textos da tarefa: ver «Os exemplos», mais abaixo) e docs/pedagogia/aquecimentos/
  m5-u1.json e m5-u2.json («núcleo» passa a «as duas perguntas»; «o tema» no topo passa a «a letra do tema»; «o que o narrador
  quer» passa a «o efeito em quem lê»);
- as páginas geradas: tarefas/m5-u1/ e tarefas/m5-u2/ (enunciado, grelha/, aquecimento/ e correcao/);
- as páginas do módulo que falam da aula de tarefa: m5/guia-da-tarefa-m5/ (10 e 55 minutos em vez de 5 e 60; «as duas perguntas»
  em vez de «núcleo comum»; sem a «Autoavaliação» que se copiava para o Teams e sem «pergunta ao teu par de trabalho»: a regra passa
  a chamar-se «Dois antes de mim»), m5/index.html e m5/mapa-do-modulo-m5/ («duas perguntas» em vez de «núcleo comum») e
  m5/portefolio-do-modulo-m5/ (saem a autoavaliação de 0 a 20 por parâmetro e «trabalho de equipa», sem nada no lugar);
- os dois acertos do M3 (decisão do docente de 13/11/2026): m3/portefolio-do-modulo-m3/ (saem a autoavaliação de 0 a 20 por parâmetro
  e «trabalho de equipa», sem nada no lugar) e o tema B da m3-u2 (docs/pedagogia/tarefas-escolha/m3-u2.json e tarefas/m3-u2/): a
  página diz que os argumentos de IV, 94 e 95 chegam, em vez de remeter para o manual para IV, 96 a 104.

Decisões do docente (as mesmas do M3 e do M1): «com consulta» quer dizer lições do site, caderno e dicionário, e diz-se uma vez, no
primeiro cartão; tempos 10 (aquecimento), 10 (leitura), 55 (produção) e 15 (revisão e entrega), 90 no total; a autoavaliação da
grelha é só para o aluno e não se entrega (a versão de correção deixa de ter a coluna «Aluno» e a nota «Diferença entre a tua nota e
a minha»); o aquecimento é o primeiro passo, com uma só ligação; o vocabulário é só o que as lições já dão; de uma obra longa entra
só o passo trabalhado, copiado letra a letra das lições, na grafia das lições; quando o enunciado troca uma palavra por outra mais
simples, a grelha, a correção, o aquecimento e o guia usam a mesma; o apoio (exemplos com outro caso) fica em desdobrável fechado no
ecrã e não sai em papel; a verificação final tem no máximo 10 perguntas de sim ou não. Só do M5: o tema B da m5-u2 tem 100 a 150
palavras (o enunciado de antes dizia «100 a 150 no tema» em cima e «100 a 130» no tema B).

De onde vêm os textos (cada bloco de texto dos dados traz a «origem»): m5-u1, lições F02 (a Introdução de Amor de Perdição, os sete
parágrafos das lições), F04 (o capítulo IV, do início à fala de Tadeu ao sobrinho, parágrafos [1] a [18], com o corte «[3] […]» que
a lição tem) e F08 (as três perguntas de Teresa, os factos e as marcas de uma carta, como a lição os dá, em português atual);
m5-u2, lições F10 (o Ramalhete no capítulo I, parágrafos [1] e [2], e no último capítulo, parágrafos [1] a [3]), F11 (o capítulo
VI: o parágrafo [1], de Alencar, e os parágrafos [3] a [9], a discussão e a interrupção) e F13 (o balanço final, parágrafos [1] a
[13]). Nenhum texto veio de fora das lições. O que as lições não dão não se copiou de fontes externas: o último parágrafo da
Introdução, a parte do capítulo IV que a lição salta (o fim do parágrafo [2] e o que a lição marca com «[3] […]») e a parte do
capítulo VI que a lição marca com «[2] […]» (o Texto 4 da m5-u2 começa por essa marca, como a lição). A página di-lo na linha de
fonte de cada texto e não remete para o manual, porque os passos das lições chegam para o que a tarefa pede. Na m5-u1, a Introdução
e o capítulo IV ficam os dois no cartão da pergunta 1, que pede uma passagem de cada um; a pergunta 2 só usa a fala de Tadeu, que
o próprio pedido cita.

Os exemplos (revisão de 13/11/2026): com os textos inteiros na página, quatro exemplos «com outro caso» usavam passagens dos textos
da tarefa (três vinham da grelha do main: «Teu primo é um composto de todas as virtudes», a carta inventada de Tadeu com «a
violencia de um pae é sempre amor», o painel com «Thereza ergueu-se sem lagrimas…», todos do capítulo IV, e a pergunta de Ega, do
balanço final). A regra do docente é «exemplos sempre com outro caso, sem as passagens da tarefa»; por isso os exemplos da página e
os da grelha (que são os mesmos) passam a usar frases que as lições dão e que não estão nos textos da tarefa: «Domingos Botelho era
extremamente feio» e «Simão, adeus até à eternidade!» (lição F07), «não recebia resposta» (lição F17, numa carta inventada da mãe
de Simão) e «Simão disse que estava ali» (o exemplo inventado da lição F12). Os critérios, os níveis e os pontos não mudam.

O molde ganhou três chaves opcionais (scripts/tarefa_facil.py): «html» num parágrafo (os itálicos da lição), «longo» num texto em
prosa (pode passar de uma página em papel, sem partir parágrafos) e «nao_partir_dossie». A folha assets/task-textos.css ganhou a
regra dos itálicos na prosa (vale para todas as páginas do molde) e as regras de impressão de «.tt-longo» (versão facil-9, que só a
m5-u1 e a m5-u2 pedem). As páginas do M3 e do M1 saem iguais, byte a byte, salvo a
frase do tema B da m3-u2.

O que NÃO muda: as outras tarefas, as suas grelhas, correções e aquecimentos (saem dos mesmos geradores, iguais byte a byte); os
critérios, os níveis e os pontos das grelhas (as trocas de palavras fazem-se só ao escrever as páginas; dos exemplos mudam só os
de dois critérios de cada grelha do M5, como se diz acima); as lições.

O script tira as trocas da diferença entre a base (cada ficheiro com esta camada desfeita pelo manifesto; antes de haver
manifesto, o ficheiro no commit de base, lido com git) e a árvore: pode voltar a correr depois de a camada estar aplicada e dá o
mesmo JSON. Para mudar uma página ou os dados por baixo desta camada (uma correção ao enunciado, por exemplo): muda-se a árvore,
voltam a gerar-se as páginas e corre-se «python3 scripts/tarefas_faceis_m5_20261113.py --base-do-commit» (a base lê-se do commit de
base, porque o manifesto antigo já não confere), e depois scripts/aplicar_trocas.py, que reescreve o manifesto. Confere, antes de
escrever: que as cinco páginas dos módulos só mudam nas trocas de EDICOES (com as de SAI); que os geradores, com os dados da árvore,
dão as nove páginas da árvore; que, com os dados da base, dão as nove páginas da base; e cada ficheiro como scripts/aplicar_trocas.py
o vai conferir (da base para o resultado e de volta, letra a letra).

As camadas de baixo desfazem primeiro esta: scripts/verificar_camadas.py (LAYERS[0]), tests/auditoria_20261028.py,
scripts/desligar_sala.py, scripts/tarefas_claras_historico.py (a leitura histórica dos enunciados; as camadas do M1 e do M3 leem por
ela ou pelo seu próprio «ler») e as bases das camadas que partilham ficheiros com ela.
"""
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/tarefas_faceis_m5_20261113.json'
MANIFESTO = ROOT / 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
BASE_COMMIT = 'e2e73379e75fd5dd4bc68009e63071c836333356'
SLUGS = ('m5-u1', 'm5-u2')
M3U2 = 'm3-u2'  # o acerto do tema B (13/11/2026)
NBSP = '\xa0'

DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS + (M3U2,)]
DADOS_GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DADOS_AQUECIMENTOS = [f'docs/pedagogia/aquecimentos/{s}.json' for s in SLUGS]
FICHEIROS_DADOS = DADOS_TAREFAS + [DADOS_GRELHAS] + DADOS_AQUECIMENTOS
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'aquecimento/', 'correcao/')] + [f'tarefas/{M3U2}/index.html']
GUIA, INDICE, MAPA = 'm5/guia-da-tarefa-m5/index.html', 'm5/index.html', 'm5/mapa-do-modulo-m5/index.html'
PORTEFOLIO, PORTEFOLIO_M3 = 'm5/portefolio-do-modulo-m5/index.html', 'm3/portefolio-do-modulo-m3/index.html'
MODULO = [GUIA, INDICE, MAPA, PORTEFOLIO, PORTEFOLIO_M3]
FICHEIROS = FICHEIROS_DADOS + PAGINAS + MODULO

ACHADOS = {
    'facil': 'O molde «mais fácil de fazer», aprovado pelo docente no M3, chega ao M5: a mesma tarefa, com os textos das lições junto '
             'da pergunta ou do tema que os usa, um pedido por alínea, os exemplos com outro caso em desdobrável, o primeiro cartão '
             'com o que se faz, o que se entrega e o quadro 10/10/55/15, e a verificação em perguntas de sim ou não.',
    'junto': '«Tudo junto» (decisão do docente): as mesmas palavras do enunciado novo («as duas perguntas» em vez de «núcleo»; «a letra '
             'do teu tema» em vez de «o tema escolhido»; «respostas ligadas» em vez de «articuladas»; «duas linhas finais» em vez de '
             '«fecho»; «o efeito em quem lê» e «uma expressão do romance», como no enunciado).',
    'tempos': 'Tempos decididos pelo docente: 10 minutos de aquecimento, 10 de leitura, 55 de produção e 15 de revisão e entrega (eram '
              '10, 5, 60 e 15), iguais em todos os sítios onde aparecem.',
    'auto': 'Decisão do docente: a autoavaliação da grelha é só para o aluno e não se entrega; a versão de correção fica com a nota e '
            'o comentário do docente.',
    'tema_b': 'Decisão do docente (13/11/2026): o tema B da m5-u2 tem 100 a 150 palavras.',
    'sem_auto': 'Decisão do docente (13/11/2026): no guia da tarefa, a «Autoavaliação» que se copiava para o Teams sai, porque a '
                'autoavaliação é só para o aluno e não se entrega. Saem o bloco, o que só a ele se refere (o código que o '
                'desenhava e guardava, a parte «AUTOAVALIAÇÃO» do texto copiado) e as duas frases que a anunciavam; o '
                'plano, as notas e a lista de verificação continuam a copiar-se.',
    'sem_par': 'Decisão do docente (13/11/2026): não há trabalho de grupo nem de pares; a regra fica com os dois primeiros passos '
               '(«Dois antes de mim»).',
    'sem_020': 'Decisão do docente (13/11/2026): no portefólio do módulo, a autoavaliação de 0 a 20 por parâmetro sai, sem nada no '
               'lugar.',
    'sem_equipa': 'Decisão do docente (13/11/2026): não há trabalho de grupo nem de pares; no portefólio do módulo, «trabalho de equipa» '
                  'sai da lista do que o portefólio serve para avaliar, sem nada no lugar.',
    'exemplos': 'Regra do docente: os exemplos mostram sempre outro caso, sem as passagens da tarefa. Com os textos inteiros na página, '
                'os exemplos da grelha que usavam frases desses textos passam a usar frases que as lições dão e que não estão nos '
                'textos da tarefa (os mesmos exemplos do enunciado).',
    'velho': 'Decisão do docente (13/11/2026): no tema B da m3-u2, a página diz que os argumentos de IV, 94 e 95 chegam, em vez de '
             'remeter para o manual para IV, 96 a 104.',
}

# As cinco páginas dos módulos não são geradas: mudam só nestas trocas (página, antigo, novo, ocorrências, categorias).
EDICOES = [
    (GUIA, f'Seguem-se 5{NBSP}minutos de leitura, 60 de produção e 15 de revisão e entrega.',
     f'Seguem-se 10{NBSP}minutos de leitura, 55 de produção e 15 de revisão e entrega.', 1, 'tempos'),
    (GUIA, f'<b>Ler o enunciado, 5{NBSP}min</b><span>Lê o núcleo comum e os temas A e B.</span>',
     f'<b>Ler o enunciado, 10{NBSP}min</b><span>Lê as duas perguntas e os temas A e B.</span>', 1, 'tempos junto'),
    (GUIA, f'<b>Produzir, 60{NBSP}min</b>', f'<b>Produzir, 55{NBSP}min</b>', 1, 'tempos'),
    (GUIA, '[5, "Ler o enunciado", "Lê o núcleo comum e os temas A e B."], [60, "Produzir",',
     '[10, "Ler o enunciado", "Lê as duas perguntas e os temas A e B."], [55, "Produzir",', 1, 'tempos junto'),
    (INDICE, 'aquecimento em cartões, núcleo comum, tema A ou B, revisão e fotografias no Teams.',
     'aquecimento em cartões, duas perguntas, tema A ou B, revisão e fotografias no Teams.', 1, 'junto'),
    (INDICE, 'com consulta: aquecimento, núcleo comum, tema A ou B, revisão e fotografias no Teams.',
     'com consulta: aquecimento, duas perguntas, tema A ou B, revisão e fotografias no Teams.', 2, 'junto'),
    (INDICE, 'preparação para a tarefa desta unidade, com núcleo comum e tema A ou B.',
     'preparação para a tarefa desta unidade, com duas perguntas e tema A ou B.', 2, 'junto'),
    (MAPA, 'com aquecimento, núcleo comum, tema A ou B e grelha /20;', 'com aquecimento, duas perguntas, tema A ou B e grelha /20;', 1,
     'junto'),
    # A «Autoavaliação» colada no Teams e «pergunta ao teu par de trabalho» saem do guia (como no guia do M3).
    (GUIA, 'verificas o trabalho com a lista da rubrica, dás-te um nível em cada parâmetro e copias tudo para a tarefa do Teams.',
     'verificas o trabalho com a lista da rubrica e copias tudo para a tarefa do Teams.', 1, 'sem_auto'),
    (GUIA, '<b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica;</li><li>pergunta ao '
           'teu par de trabalho.</li></ol>Só depois levantas o braço.',
     '<b>Dois antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica.</li></ol>Só depois levantas '
     'o braço.', 1, 'sem_par'),
    (GUIA, 'O docente vê o teu plano, as notas, a lista e a autoavaliação.', 'O docente vê o teu plano, as notas e a lista.', 1,
     'sem_auto'),
]

# O que sai inteiro, sem nada no lugar (página, o que fica antes, o que sai, o que fica depois, categorias). A troca leva os dois
# vizinhos, porque scripts/aplicar_trocas.py não aceita um «novo» vazio. No guia, são as mesmas cinco saídas do guia do M3.
SAI = [
    # o bloco «Autoavaliação»
    (GUIA, '<ul class="lista" id="r-verificar"></ul>\n',
     '<h2>Autoavaliação</h2>\n<p class="pequeno">Em cada parâmetro, toca no nível que achas que tens. O 4 é o melhor. Escreve uma '
     'linha a dizer porquê.</p>\n<div id="r-auto"></div>\n',
     '<div class="fila"><button class="btn" id="copiar">', 'sem_auto'),
    # o código que desenhava o bloco
    (GUIA, r'''+esc(p.niveis[0])+'.</label></li>'}).join("");''' + '\n',
     r'''  $("#r-auto").innerHTML=atual.rubrica.map(function(p,i){var a=D.auto[i]||{};return '<p style="margin:10px 0 4px"><b>'+esc(p.nome)+'</b> <span class="pequeno">(extra sem nota)</span></p><div class="niveis" data-p="'+i+'">'+[4,3,2,1].map(function(n){return '<button aria-pressed="'+(a.n===n?"true":"false")+'" data-n="'+n+'">'+n+'</button>'}).join("")+'</div><textarea data-auto="'+i+'" placeholder="Porquê, numa linha." style="min-height:56px">'+esc(a.j||"")+'</textarea>'}).join("");''' + '\n',
     '  $("#escolha").hidden=true;', 'sem_auto'),
    # o código que guardava a linha «porquê» e o nível tocado
    (GUIA, 'if(t.dataset.k){d().campos[t.dataset.k]=t.value;guardar()}',
     'if(t.dataset.auto!=null){var a=d().auto;a[t.dataset.auto]=a[t.dataset.auto]||{};a[t.dataset.auto].j=t.value;guardar()}',
     '});\ndocument.addEventListener("change"', 'sem_auto'),
    (GUIA, 'filter(function(j){return j>=0});guardar()}});\n',
     r'''document.addEventListener("click",function(ev){var b=ev.target.closest(".niveis button");if(!b||!atual)return;var p=b.parentNode.dataset.p;b.parentNode.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-pressed","false")});b.setAttribute("aria-pressed","true");var a=d().auto;a[p]=a[p]||{};a[p].n=Number(b.dataset.n);guardar()});''' + '\n',
     'function texto(){', 'sem_auto'),
    # a parte «AUTOAVALIAÇÃO» do texto que se copia para o Teams
    (GUIA, 'l.push((D.feito.indexOf(i)>=0?"[x] ":"[ ] ")+p.nome)});',
     r'''l.push("","AUTOAVALIAÇÃO");''' + '\n' + r'''  atual.rubrica.forEach(function(p,i){var a=D.auto[i]||{};l.push(p.nome+": nível "+(a.n||"-")+(a.j?" · "+a.j:""))});''',
     r'''return l.join("\n")}''', 'sem_auto'),
]
SAI += [
    # o portefólio do M5 e o do M3: a autoavaliação de 0 a 20 por parâmetro e «trabalho de equipa»
    (PORTEFOLIO, 'copiado do Percurso do módulo', ', e a tua autoavaliação de 0 a 20 por parâmetro, com razões', '.</td></tr></table>',
     'sem_020'),
    (PORTEFOLIO, f'do módulo (40{NBSP}%): autonomia, responsabilidade,', ' trabalho de equipa,', ' pensamento crítico, entre outros.',
     'sem_equipa'),
    (PORTEFOLIO_M3, 'copiado do Percurso do módulo', f', e a tua autoavaliação de 0{NBSP}a{NBSP}20 por parâmetro, com razões',
     '.</td></tr></table>', 'sem_020'),
    (PORTEFOLIO_M3, f'do módulo (40{NBSP}%): autonomia, responsabilidade,', ' trabalho de equipa,', ' pensamento crítico, entre outros.',
     'sem_equipa'),
]
EDICOES += [(f, antes + sai + depois, antes + depois, 1, cs) for f, antes, sai, depois, cs in SAI]


def ler(rel):
    # 13/11/2026: por cima desta camada fica a das tarefas do M6 mais fáceis de fazer (tarefas_faceis_m6_20261113), que também muda
    # os dados das grelhas: desfaz-se primeiro, com contagem estrita, quando o ficheiro a traz (a «árvore» desta camada é o
    # ficheiro como ela o deixou).
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 13/11/2026: e por cima de todas fica a das tarefas do M7 (tarefas_faceis_m7_20261113), que também muda os dados das grelhas:
    # desfaz-se antes da do M6, com contagem estrita.
    m7 = ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'
    if m7.is_file():
        for e in reversed(json.loads(m7.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: as tarefas do M7 mais fáceis de fazer já não conferem ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
    m6 = ROOT / 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json'
    if m6.is_file():
        for e in reversed(json.loads(m6.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: as tarefas do M6 mais fáceis de fazer já não conferem ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
    return texto


DO_COMMIT = False  # com --base-do-commit: a base lê-se do commit de base (para refazer a camada depois de mudar as páginas)


def base(rel):
    """O texto do ficheiro sem esta camada: desfeita pelo manifesto (da última troca para a primeira, com contagem estrita); se a
    camada estiver por aplicar nesse ficheiro, o ficheiro já é a base. Antes de haver manifesto (ou com --base-do-commit), o
    ficheiro no commit de base."""
    texto = ler(rel)
    if MANIFESTO.is_file() and not DO_COMMIT:
        edits = json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])
        if edits and all(texto.count(e['new']) == 0 and texto.count(e['old']) == e['occurrences'] for e in edits):
            return texto
        for e in reversed(edits):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: o manifesto desta camada já não confere ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
        return texto
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    if r.returncode:
        raise SystemExit(f'{rel}: sem manifesto e sem o commit de base {BASE_COMMIT[:8]}')
    return r.stdout.decode('utf-8')


def gerar_com(textos):
    """As nove páginas que os três geradores dão com estes dados ({ficheiro de dados: texto}), numa pasta temporária."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for rel, texto in textos.items():
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_bytes(texto.encode('utf-8'))
        codigo = (
            'import sys, json; from pathlib import Path; sys.path.insert(0, "scripts"); tmp = Path(sys.argv[1])\n'
            'import tarefas_escolha as te, grelhas_tarefas as gt, aquecimentos as aq\n'
            'te.DADOS = tmp / "docs/pedagogia/tarefas-escolha"; te.GRELHAS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'gt.DADOS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'grelhas = json.loads(te.GRELHAS.read_text("utf-8"))["tarefas"]\n'
            'for s in ("m5-u1", "m5-u2", "m3-u2"):\n'
            '    d = json.loads((te.DADOS / (s + ".json")).read_text("utf-8")); te.tarefa(d, s in grelhas, tmp / "saida")\n'
            'for s in ("m5-u1", "m5-u2"):\n'
            '    t = grelhas[s]\n'
            '    for pasta, html in (("grelha", gt.pagina_aluno(s, t)), ("correcao", gt.pagina_correcao(s, t))):\n'
            '        p = tmp / "saida/tarefas" / s / pasta / "index.html"; p.parent.mkdir(parents=True, exist_ok=True)\n'
            '        p.write_text(html, "utf-8", newline="\\n")\n'
            'sys.exit(aq.main(["--saida", str(tmp / "saida"), "--dados", str(tmp / "docs/pedagogia/aquecimentos"), "m5-u1", "m5-u2"]) or 0)\n')
        r = subprocess.run([sys.executable, '-c', codigo, str(tmp)], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if r.returncode:
            raise SystemExit('os geradores falharam: ' + r.stdout + r.stderr)
        return {rel: (tmp / 'saida' / rel).read_bytes().decode('utf-8') for rel in PAGINAS}


# ---------- da diferença às trocas ----------

_PEDACOS = re.compile(r'<[^<>]*>|[^<>\s]+\s*|\s+|.', re.S)
_FRONTEIRA = ' \n<>"'
_JUNTAR = 160  # diferenças a menos desta distância ficam na mesma troca (uma página refeita dá poucas trocas, grandes)


def diferencas(a, b):
    """Os intervalos que mudam, [(a0, a1, b0, b1)], pela ordem do texto. O princípio e o fim iguais ficam de fora antes de comparar."""
    p = 0
    while p < len(a) and p < len(b) and a[p] == b[p]:
        p += 1
    s = 0
    while s < len(a) - p and s < len(b) - p and a[len(a) - 1 - s] == b[len(b) - 1 - s]:
        s += 1
    # recua até uma fronteira, para os pedaços do meio começarem e acabarem em palavras inteiras
    while p > 0 and a[p - 1] not in _FRONTEIRA:
        p -= 1
    while s > 0 and a[len(a) - s] not in _FRONTEIRA:
        s -= 1
    ma, mb = a[p:len(a) - s], b[p:len(b) - s]
    pa, pb = _PEDACOS.findall(ma), _PEDACOS.findall(mb)
    assert ''.join(pa) == ma and ''.join(pb) == mb
    ia, ib = [p], [p]
    for x in pa:
        ia.append(ia[-1] + len(x))
    for x in pb:
        ib.append(ib[-1] + len(x))
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pa, pb, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        a0, a1, b0, b1 = ia[i1], ia[i2], ib[j1], ib[j2]
        while a0 < a1 and b0 < b1 and a[a0] == b[b0]:
            a0, b0 = a0 + 1, b0 + 1
        while a1 > a0 and b1 > b0 and a[a1 - 1] == b[b1 - 1]:
            a1, b1 = a1 - 1, b1 - 1
        if out and a0 - out[-1][1] < _JUNTAR:
            out[-1] = (out[-1][0], a1, out[-1][2], b1)
        else:
            out.append((a0, a1, b0, b1))
    return out


def trocas_do_texto(a, b):
    """[(antigo, novo)]: cada diferença alargada, dos dois lados, até à fronteira seguinte de palavra ou de etiqueta, até o antigo
    ser único na base e o novo único no resultado, sem se sobrepor a outra."""
    hs = diferencas(a, b)

    def alargar(h):
        a0, a1, b0, b1 = h
        k = 1
        while a0 - k > 0 and a[a0 - k] not in _FRONTEIRA:
            k += 1
        k = min(k, a0)
        a0, b0 = a0 - k, b0 - k
        k = 1
        while a1 + k < len(a) and a[a1 + k - 1] not in _FRONTEIRA:
            k += 1
        k = min(k, len(a) - a1)
        return a0, a1 + k, b0, b1 + k

    def serve(h):
        antigo, novo = a[h[0]:h[1]], b[h[2]:h[3]]
        return (bool(antigo) and bool(novo) and a.count(antigo) == 1 and a.count(novo) == 0 and b.count(novo) == 1
                and b.replace(novo, '\0').count(antigo) == 0)

    def juntar(hs):
        out = []
        for h in sorted(hs):
            if out and h[0] <= out[-1][1]:
                o = out[-1]
                out[-1] = (o[0], max(o[1], h[1]), o[2], max(o[3], h[3]))
            else:
                out.append(h)
        return out

    hs = [alargar(h) for h in hs]
    for _ in range(2000):
        hs = juntar(hs)
        maus = [k for k, h in enumerate(hs) if not serve(h)]
        if not maus:
            for h in hs:
                assert a[:h[0]].endswith(b[max(0, h[2] - 20):h[2]][-10:]) or h[0] < 10
            return [(a[h[0]:h[1]], b[h[2]:h[3]]) for h in hs]
        for k in maus:
            hs[k] = alargar(hs[k])
    raise SystemExit('não encontrei contexto que torne as trocas únicas')


def _visivel(s):
    s = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', '…', s)
    s = s.replace('\\"', '"').replace('<\\/', '</').replace('\\n', ' ')
    s = re.sub(r'^[^<>]*>|<[^<>]*$', ' ', s)
    s = re.sub(r'<[^<>]*>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def nome(rel):
    m = re.search(r'm([35])-u(\d)', rel)
    u = f'M{m.group(1)}-U{m.group(2)}' if m else ('M3' if rel.startswith('m3/') else 'M5')
    if rel in DADOS_TAREFAS:
        return f'Tarefa da {u}, os dados do enunciado'
    if rel == DADOS_GRELHAS:
        return 'Grelhas das tarefas do M5, os dados'
    if rel in DADOS_AQUECIMENTOS:
        return f'Aquecimento da {u}, os dados'
    if rel == GUIA:
        return 'Guia da tarefa do M5'
    if rel == INDICE:
        return 'Índice do M5'
    if rel == MAPA:
        return 'Mapa do M5'
    if rel in (PORTEFOLIO, PORTEFOLIO_M3):
        return f'Portefólio do módulo {u}'
    return {'grelha': f'Grelha do aluno da {u}', 'aquecimento': f'Aquecimento da {u}', 'correcao': f'Versão de correção da {u}'}.get(
        rel.split('/')[2], f'Enunciado da {u}')


EXEMPLOS_NOVOS = ('Domingos Botelho era extremamente feio', 'Simão disse que estava ali', 'mãe de Simão', 'adeus até à eternidade',
                  'Numa carta inventada de Tadeu', 'fala relatada de Simão', 'aqui está tudo como deixaste')


def categorias(rel, antigo, novo):
    cs = set()
    if M3U2 in rel:
        cs.add('velho')
    elif rel in DADOS_TAREFAS or rel.endswith(('m5-u1/index.html', 'm5-u2/index.html')):
        cs |= {'facil', 'tempos', 'auto', 'junto'} if len(novo) > 2000 else {'facil'}
        if 'm5-u2' in rel and len(novo) > 2000:
            cs.add('tema_b')
    elif rel == DADOS_GRELHAS or '/grelha/' in rel or '/correcao/' in rel:
        if 'autoavalia' in novo or 'Aluno</th>' in antigo or 'Diferença entre' in antigo or '<td></td><td></td><td></td>' in antigo:
            cs.add('auto')
        # o resto são as palavras do enunciado novo («trocas_aluno»: ligadas, a letra do tema, duas perguntas, duas linhas finais,
        # o efeito em quem lê, uma expressão do romance)
        # os exemplos que deixaram de usar passagens dos textos da tarefa (revisão de 13/11/2026)
        if any(m in novo for m in EXEMPLOS_NOVOS):
            cs.add('exemplos')
        if 'trocas_aluno' in novo or not cs:
            cs.add('junto')
    else:
        cs.add('junto')
    if not cs:
        raise SystemExit(f'{rel}: troca sem categoria: «{antigo[:120]}» para «{novo[:120]}»')
    return [c for c in ACHADOS if c in cs]


def trocas_do_ficheiro(rel, a, b):
    trocas = []
    for antigo, novo in trocas_do_texto(a, b):
        trecho = _visivel(novo)
        trecho = trecho if len(trecho) <= 90 else trecho[:88].rstrip() + '…'
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}: «{trecho}»', 'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
                       'achado': '13/11/2026: ' + ' '.join(ACHADOS[c] for c in categorias(rel, antigo, novo))})
    return trocas


def construir():
    """Devolve (trocas, {ficheiro: (base, final)})."""
    finais = {rel: (base(rel), ler(rel)) for rel in FICHEIROS}
    if all(a == b for a, b in finais.values()):
        raise SystemExit('a camada não está aplicada nesta árvore: aplica-a com scripts/aplicar_trocas.py e o JSON que já existe')
    # As páginas dos módulos mudam só nas trocas de EDICOES.
    for rel in MODULO:
        texto = finais[rel][0]
        for f, antigo, novo, n, _ in EDICOES:
            if f == rel:
                if texto.count(antigo) != n:
                    raise SystemExit(f'{rel}: «{antigo[:60]}…» aparece {texto.count(antigo)} vez(es) na base, não {n}')
                texto = texto.replace(antigo, novo)
        if texto != finais[rel][1]:
            raise SystemExit(f'{rel}: a página não é a base com as trocas de EDICOES')
    # Os geradores dão as páginas da árvore com os dados da árvore, e as da base com os dados da base.
    for k, quando in ((1, 'da árvore'), (0, 'da base')):
        geradas = gerar_com({rel: finais[rel][k] for rel in FICHEIROS_DADOS})
        for rel in PAGINAS:
            if geradas[rel] != finais[rel][k]:
                raise SystemExit(f'{rel}: com os dados {quando}, os geradores não dão a página {quando}')
    todas = []
    for rel in FICHEIROS:
        a, b = finais[rel]
        if a == b:
            raise SystemExit(f'{rel}: nada muda')
        if rel in MODULO:
            trocas = [{'ficheiro': rel, 'local': f'{nome(rel)}: «{_visivel(novo)[:88]}»', 'antigo': antigo, 'novo': novo,
                       'ocorrencias': n, 'achado': '13/11/2026: ' + ' '.join(ACHADOS[c] for c in ACHADOS if c in cs.split())}
                      for f, antigo, novo, n, cs in EDICOES if f == rel]
        else:
            trocas = trocas_do_ficheiro(rel, a, b)
        lista = list(enumerate(trocas, 1))
        try:
            for texto in (a, b):
                x, y, _ = processar(rel, lista, texto)
                assert x == a and y == b
        except (TrocaFalhou, AssertionError) as erro:
            raise SystemExit(f'{rel}: as trocas não conferem: {erro}')
        todas += trocas
    return todas, finais


def main():
    global DO_COMMIT
    DO_COMMIT = '--base-do-commit' in sys.argv[1:]
    todas, finais = construir()
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {len(finais)} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
