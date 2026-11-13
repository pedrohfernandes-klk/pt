#!/usr/bin/env python3
"""12/11/2026: as duas tarefas do M3 (m3-u1 e m3-u2) «mais fáceis de fazer», com tudo o que fala delas a usar as mesmas palavras.

Pedido do docente: «as tarefas são para manter, mas é para ser mais fácil de fazer»; «os textos estudados têm de aparecer completos
para análise». O piloto na m3-u1 foi aprovado pelo docente a 12/11/2026; esta camada regista-o e alarga-o à m3-u2. Cada tarefa é a
mesma (as mesmas perguntas, os mesmos temas A e B, o mesmo total de palavras, os mesmos critérios da grelha); muda só a forma.

Constrói scripts/tarefas_faceis_m3_20261112.json, a camada literal tarefas_faceis_m3_20261112, que se aplica com
scripts/aplicar_trocas.py; o manifesto fica em tests/fixtures/tarefas-faceis-m3-edits-20261112.json:

  python3 scripts/tarefas_faceis_m3_20261112.py
  python3 scripts/aplicar_trocas.py scripts/tarefas_faceis_m3_20261112.json \\
      --manifesto tests/fixtures/tarefas-faceis-m3-edits-20261112.json \\
      --base-commit 1471a61ab0a539719943074153f9e9647ba48e35 --nota "…"

Fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima das provas em cartões com os documentos oficiais
(exame_provas_oficial_20261112), com a qual não partilha nenhum ficheiro. Partilha ficheiros com a decisão 152 no M3
(cuidado_m3_20261108), com a revisão dos enunciados (tarefas_claras_20261110), com a decisão 152 no M6 (cuidado_m6_20261108, que
repôs espaços nas tarefas) e com as camadas mais antigas do índice, do guia e do mapa do M3: todas a desfazem primeiro.

Ficheiros (16):
- os dados: docs/pedagogia/tarefas-escolha/m3-u1.json e m3-u2.json (a chave nova «facil», de onde sai a página; as chaves antigas
  ficam como estavam, para a leitura histórica das camadas de baixo, e já não aparecem na página), docs/pedagogia/
  grelhas-tarefas-20261027.json («autoavaliacao_so_tua» e «trocas_aluno» nas duas grelhas do M3) e docs/pedagogia/aquecimentos/
  m3-u1.json e m3-u2.json («núcleo» passa a «as duas perguntas»);
- as páginas geradas: tarefas/m3-u1/ e tarefas/m3-u2/ (enunciado, grelha/, aquecimento/ e correcao/);
- as páginas do módulo que falam da aula de tarefa: m3/guia-da-tarefa-m3/ (10 e 55 minutos em vez de 5 e 60; «as duas perguntas»
  em vez de «núcleo comum»; desde 13/11/2026, sem a «Autoavaliação» que se copiava para o Teams e sem «pergunta ao teu par de
  trabalho»), m3/index.html e m3/mapa-do-modulo-m3/ («duas perguntas» em vez de «núcleo comum»).

Decisões do docente (12/11/2026), iguais nas duas tarefas: «com consulta» quer dizer lições do site, caderno e dicionário, e
diz-se uma vez, no primeiro cartão; tempos 10 (aquecimento), 10 (leitura), 55 (produção) e 15 (revisão e entrega), 90 no total;
os versos citados ou copiados não contam para as palavras; a autoavaliação da grelha é só para o aluno e não se entrega (a versão
de correção deixa de ter a coluna «Aluno» e a nota «Diferença entre a tua nota e a minha»); o aquecimento é o primeiro passo, com
uma só ligação; o vocabulário é só o que as lições já dão; de uma obra longa entra só o passo trabalhado, inteiro e contínuo,
copiado letra a letra das lições; quando o enunciado troca uma palavra por outra mais simples, a grelha, a correção, o aquecimento
e o guia usam a mesma; os textos com direitos não se copiam (bloco «Onde está o texto»); o apoio (exemplos com outro caso,
descrições, o quadro das modalidades) fica em desdobrável fechado no ecrã e não sai em papel; a verificação final tem no máximo
10 perguntas de sim ou não; em papel nenhum poema se parte.

De onde vêm os textos (cada bloco de texto dos dados traz a «origem»): m3-u1, lições F02 (I, 1 a 3 e os seis objetos do Kit),
F05 («Descalça vai para a fonte»), F09 («Alma minha gentil») e F03 (IV, 94 e 95); m3-u2, lições F10 (I, 4 e 5 e X, 145), F13
(VIII, 96 a 99), F03 (IV, 94 e 95) e F15 (o quadro das três modalidades). Nenhum texto veio de fora das lições.

Revisão de 13/11/2026 (achados de duas revisões independentes, tudo dentro desta camada): nas duas grelhas do aluno, «Duas linhas
finais» em vez de «Fecho» (mais dois pares em «trocas_aluno»); nos exemplos, «Passo» e «Alínea» presos ao número ou à letra
(U+00A0); em papel, o cabeçalho do cartão dos temas não fica sozinho no fundo de uma página (assets/task-textos.css, versão
facil-7). O tema B da m3-u2 pede dois argumentos do Velho, que fala de IV, 95 a 104, e as lições só dão IV, 94 e 95: as estâncias
96 a 104 não estão em nenhuma lição do repositório, e a edição modernizada em domínio público que se conferiu verso a verso
(oslusiadas.org, igual à do Projeto Gutenberg n.º 3333) contra a transcrição da edição de 1572 (Projeto Gutenberg n.º 27236, a
partir da Biblioteca Nacional Digital) tem gralhas («quantidades» em IV, 99; «velas» em IV, 102). Por isso não se copiaram: o
tema B diz que o Texto 3 tem as estâncias IV, 94 e 95 e que o resto da fala do Velho está no manual, sem número de página.

Decisão do docente de 13/11/2026, só no guia da tarefa do M3 (nas produções antigas sem nota): a «Autoavaliação» que se copiava para
o Teams sai, porque a autoavaliação é só para o aluno e não se entrega; e «pergunta ao teu par de trabalho» sai, porque não há
trabalho de grupo nem de pares. Sai o bloco «Autoavaliação» inteiro e o que só a ele se refere (o código que o desenhava e
guardava, a parte «AUTOAVALIAÇÃO» do texto copiado, e as duas frases que o anunciavam); a regra «Três antes de mim» fica
com os dois primeiros passos e chama-se «Dois antes de mim». Nada entra no lugar do que sai: o plano, as notas e a lista de
verificação continuam a copiar-se para o Teams. São oito trocas no guia (três em EDICOES e cinco em SAI, que tira um pedaço inteiro e
ancora nos dois vizinhos). O estilo dos níveis (.niveis) fica na folha de estilo do guia, sem uso: os nove guias da tarefa têm o
mesmo estilo, letra a letra (tests/test_tasks_m356.py), e a decisão é só para o M3.

O que NÃO muda: as outras onze tarefas, as suas grelhas, correções e aquecimentos (saem dos mesmos geradores, iguais byte a byte);
os critérios, os níveis, os exemplos e os pontos das grelhas (as trocas de palavras fazem-se só ao escrever as páginas); as lições.

Como as páginas são geradas: scripts/tarefas_escolha.py chama scripts/tarefa_facil.py quando os dados têm a chave «facil»;
scripts/grelhas_tarefas.py lê «autoavaliacao_so_tua» e «trocas_aluno»; scripts/aquecimentos.py não mudou. Sem as chaves, os três
dão byte a byte as páginas de antes: é o que as camadas de baixo conferem quando voltam a gerar as páginas com os dados como elas
os deixaram.

O script tira as trocas da diferença entre a base (cada ficheiro com esta camada desfeita pelo manifesto; antes de haver
manifesto, o ficheiro no commit de base, lido com git) e a árvore: pode voltar a correr depois de a camada estar aplicada e dá o
mesmo JSON. Para mudar uma página ou os dados por baixo desta camada (uma correção ao enunciado, por exemplo): muda-se a árvore,
voltam a gerar-se as páginas e corre-se «python3 scripts/tarefas_faceis_m3_20261112.py --base-do-commit» (a base lê-se do commit de
base, porque o manifesto antigo já não confere), e depois scripts/aplicar_trocas.py, que reescreve o manifesto. Confere, antes de
escrever: que as três páginas do módulo só mudam nas trocas de EDICOES (com as de SAI); que os geradores, com os
dados da árvore, dão as oito páginas da árvore; que, com os dados da base, dão as oito páginas da base; e cada ficheiro como
scripts/aplicar_trocas.py o vai conferir (da base para o resultado e de volta, letra a letra).

As camadas de baixo desfazem primeiro esta: scripts/verificar_camadas.py (LAYERS[0]), tests/auditoria_20261028.py,
scripts/desligar_sala.py, scripts/tarefas_claras_historico.py (a leitura histórica dos enunciados) e as bases das camadas da
decisão 152 que partilham ficheiros com ela.
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

CAMADA = ROOT / 'scripts/tarefas_faceis_m3_20261112.json'
MANIFESTO = ROOT / 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
BASE_COMMIT = '1471a61ab0a539719943074153f9e9647ba48e35'
SLUGS = ('m3-u1', 'm3-u2')
NBSP = '\xa0'

DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
DADOS_GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DADOS_AQUECIMENTOS = [f'docs/pedagogia/aquecimentos/{s}.json' for s in SLUGS]
FICHEIROS_DADOS = DADOS_TAREFAS + [DADOS_GRELHAS] + DADOS_AQUECIMENTOS
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'aquecimento/', 'correcao/')]
GUIA, INDICE, MAPA = 'm3/guia-da-tarefa-m3/index.html', 'm3/index.html', 'm3/mapa-do-modulo-m3/index.html'
MODULO = [GUIA, INDICE, MAPA]
FICHEIROS = FICHEIROS_DADOS + PAGINAS + MODULO

ACHADOS = {
    'facil': 'Pedido do docente («mais fácil de fazer», aprovado no piloto da m3-u1): a mesma tarefa no molde novo, com os textos '
             'completos junto da pergunta ou do tema que os usa, um pedido por alínea, os exemplos com outro caso em desdobrável, o '
             'primeiro cartão com o que se faz, o que se entrega e o quadro 10/10/55/15, e a verificação em perguntas de sim ou não.',
    'junto': '«Tudo junto» (decisão do docente): as mesmas palavras do enunciado novo («as duas perguntas» em vez de «núcleo»; «a letra '
             'do teu tema» em vez de «o tema escolhido»; «respostas ligadas» em vez de «articuladas»).',
    'tempos': 'Tempos decididos pelo docente: 10 minutos de aquecimento, 10 de leitura, 55 de produção e 15 de revisão e entrega (eram '
              '10, 5, 60 e 15), iguais em todos os sítios onde aparecem.',
    'auto': 'Decisão do docente: a autoavaliação da grelha é só para o aluno e não se entrega; a versão de correção fica com a nota e '
            'o comentário do docente.',
    'conta': 'Decisão do docente: os versos citados ou copiados não contam para as palavras.',
    'sem_auto': 'Decisão do docente (13/11/2026): no guia da tarefa, a «Autoavaliação» que se copiava para o Teams sai, porque a '
                'autoavaliação é só para o aluno e não se entrega. Saem o bloco, o que só a ele se refere (o código que o '
                'desenhava e guardava, a parte «AUTOAVALIAÇÃO» do texto copiado) e as duas frases que a anunciavam; o '
                'plano, as notas e a lista de verificação continuam a copiar-se.',
    'sem_par': 'Decisão do docente (13/11/2026): não há trabalho de grupo nem de pares; a regra fica com os dois primeiros passos '
               '(«Dois antes de mim»).',
}

# As três páginas do módulo não são geradas: mudam só nestas trocas (página, antigo, novo, ocorrências, categorias).
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
    (MAPA, 'com aquecimento, núcleo comum, tema A ou B e grelha /20;', 'com aquecimento, duas perguntas, tema A ou B e grelha /20;', 1,
     'junto'),
    # 13/11/2026 (decisão do docente): a «Autoavaliação» colada no Teams e «pergunta ao teu par de trabalho» saem do guia.
    (GUIA, 'verificas o trabalho com a lista da rubrica, dás-te um nível em cada parâmetro e copias tudo para a tarefa do Teams.',
     'verificas o trabalho com a lista da rubrica e copias tudo para a tarefa do Teams.', 1, 'sem_auto'),
    (GUIA, '<b>Três antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta ao teu par de '
           'trabalho. Só depois levantas o braço.',
     '<b>Dois antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica. Só depois levantas o braço.', 1,
     'sem_par'),
    (GUIA, 'O docente vê o teu plano, as notas, a lista e a autoavaliação.', 'O docente vê o teu plano, as notas e a lista.', 1,
     'sem_auto'),
]

# 13/11/2026: o que sai inteiro do guia, sem nada no lugar (página, o que fica antes, o que sai, o que fica depois, categorias). A
# troca leva os dois vizinhos, porque scripts/aplicar_trocas.py não aceita um «novo» vazio.
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
EDICOES += [(f, antes + sai + depois, antes + depois, 1, cs) for f, antes, sai, depois, cs in SAI]


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


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
    """As oito páginas que os três geradores dão com estes dados ({ficheiro de dados: texto}), numa pasta temporária."""
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
            'for s in ("m3-u1", "m3-u2"):\n'
            '    d = json.loads((te.DADOS / (s + ".json")).read_text("utf-8")); te.tarefa(d, s in grelhas, tmp / "saida")\n'
            'for s in ("m3-u1", "m3-u2"):\n'
            '    t = grelhas[s]\n'
            '    for pasta, html in (("grelha", gt.pagina_aluno(s, t)), ("correcao", gt.pagina_correcao(s, t))):\n'
            '        p = tmp / "saida/tarefas" / s / pasta / "index.html"; p.parent.mkdir(parents=True, exist_ok=True)\n'
            '        p.write_text(html, "utf-8", newline="\\n")\n'
            'sys.exit(aq.main(["--saida", str(tmp / "saida"), "--dados", str(tmp / "docs/pedagogia/aquecimentos"), "m3-u1", "m3-u2"]) or 0)\n')
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
    m = re.search(r'm3-u(\d)', rel)
    u = f'M3-U{m.group(1)}' if m else 'M3'
    if rel in DADOS_TAREFAS:
        return f'Tarefa da {u}, os dados do enunciado'
    if rel == DADOS_GRELHAS:
        return 'Grelhas das tarefas do M3, os dados'
    if rel in DADOS_AQUECIMENTOS:
        return f'Aquecimento da {u}, os dados'
    if rel == GUIA:
        return 'Guia da tarefa do M3'
    if rel == INDICE:
        return 'Índice do M3'
    if rel == MAPA:
        return 'Mapa do M3'
    return {'grelha': f'Grelha do aluno da {u}', 'aquecimento': f'Aquecimento da {u}', 'correcao': f'Versão de correção da {u}'}.get(
        rel.split('/')[2], f'Enunciado da {u}')


def categorias(rel, antigo, novo):
    cs = set()
    if rel in MODULO:
        for f, x, y, _, c in EDICOES:
            if f == rel and (y in novo or novo in y):
                cs |= set(c.split())
    elif rel in DADOS_TAREFAS or rel.endswith(('m3-u1/index.html', 'm3-u2/index.html')):
        cs |= {'facil', 'tempos', 'conta', 'auto', 'junto'} if len(novo) > 2000 else {'facil'}
    elif rel == DADOS_GRELHAS or '/grelha/' in rel or '/correcao/' in rel:
        if 'autoavalia' in novo or 'Aluno</th>' in antigo or 'Diferença entre' in antigo or '<td></td><td></td><td></td>' in antigo:
            cs.add('auto')
        if 'versos citados' in novo:
            cs.add('conta')
        if 'trocas_aluno' in novo or re.search(r'ligadas|letra do|Duas perguntas', novo):
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
                       'achado': '12/11/2026: ' + ' '.join(ACHADOS[c] for c in categorias(rel, antigo, novo))})
    return trocas


def construir():
    """Devolve (trocas, {ficheiro: (base, final)})."""
    finais = {rel: (base(rel), ler(rel)) for rel in FICHEIROS}
    if all(a == b for a, b in finais.values()):
        raise SystemExit('a camada não está aplicada nesta árvore: aplica-a com scripts/aplicar_trocas.py e o JSON que já existe')
    # As páginas do módulo mudam só nas trocas de EDICOES.
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
                       'ocorrencias': n, 'achado': '12/11/2026: ' + ' '.join(ACHADOS[c] for c in ACHADOS if c in cs.split())}
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
