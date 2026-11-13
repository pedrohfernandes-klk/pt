#!/usr/bin/env python3
"""13/11/2026: as duas tarefas do M1 (m1-u1 e m1-u2) «mais fáceis de fazer», com tudo o que fala delas a usar as mesmas palavras.

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201, camada tarefas_faceis_m3_20261112).
Esta camada leva o mesmo molde ao M1. Cada tarefa é a mesma (as mesmas perguntas, os mesmos temas A e B, o mesmo total de
palavras, os mesmos critérios da grelha); muda só a forma.

Constrói scripts/tarefas_faceis_m1_20261113.json, a camada literal tarefas_faceis_m1_20261113, que se aplica com
scripts/aplicar_trocas.py; o manifesto fica em tests/fixtures/tarefas-faceis-m1-edits-20261113.json:

  python3 scripts/tarefas_faceis_m1_20261113.py
  python3 scripts/aplicar_trocas.py scripts/tarefas_faceis_m1_20261113.json \\
      --manifesto tests/fixtures/tarefas-faceis-m1-edits-20261113.json \\
      --base-commit 2b343fbe53a1cd2155baf4039041fa806fd99312 --nota "…"

Fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima das tarefas do M3 mais fáceis de fazer
(tarefas_faceis_m3_20261112), com a qual partilha um ficheiro: os dados das grelhas (docs/pedagogia/grelhas-tarefas-20261027.json).
Partilha ficheiros também com a revisão dos enunciados (tarefas_claras_20261110), com a decisão 152 no M1 e no M6
(cuidado_m1_20261106 e cuidado_m6_20261108) e com as camadas mais antigas do índice e do guia do M1: todas a desfazem primeiro.

Ficheiros (12):
- os dados: docs/pedagogia/tarefas-escolha/m1-u1.json e m1-u2.json (a chave nova «facil», de onde sai a página; as chaves antigas
  ficam como estavam, para a leitura histórica das camadas de baixo, e já não aparecem na página) e docs/pedagogia/
  grelhas-tarefas-20261027.json («autoavaliacao_so_tua» e «trocas_aluno» nas duas grelhas do M1);
- as páginas geradas: tarefas/m1-u1/ e tarefas/m1-u2/ (enunciado, grelha/ e correcao/);
- as páginas do módulo que falam da aula de tarefa: m1/guia-da-tarefa-m1/ (10 e 55 minutos em vez de 5 e 60; «as duas perguntas»
  em vez de «núcleo comum»), m1/index.html («além das duas perguntas» em vez de «além do núcleo comum», no arquivo de revisão) e
  m1/portefolio-do-modulo-m1/ (sai «trabalho de equipa» da lista do que o portefólio serve para avaliar).

Decisão do docente de 13/11/2026, no portefólio do módulo: saem a autoavaliação de 0 a 20 por parâmetro e «trabalho de equipa», sem
pôr nada no lugar. O portefólio do M1 nunca teve a autoavaliação de 0 a 20; tinha «trabalho de equipa» numa lista («autonomia,
responsabilidade, trabalho de equipa, pensamento crítico, entre outros»), de onde sai. É uma troca em SAI, que tira um pedaço
inteiro e ancora nos dois vizinhos.

Revisão de 13/11/2026: a pergunta 2 da m1-u2 diz «o excerto do capítulo XII» (agora há um só, o Texto 1, contínuo), e a grelha e a
versão de correção dizem o mesmo («no excerto», três pares mais em «trocas_aluno»).

Segunda revisão de 13/11/2026: a linha de fonte do Texto 3 da m1-u1 (Guilhade) diz, como as dos Textos 1 e 2, a época do autor
(«séc. XIII», do subtítulo da lição F04) e «a cantiga inteira, com a grafia da edição» (a frase da lição F19). Na m1-u2 fica por
decidir pelo docente se a passagem copiada do tema A conta para as 160 a 200 palavras da crónica: a decisão fala em versos, e a
página continua a dizer o que dizia antes desta camada (não contam as respostas, as fontes e as duas linhas finais).

O que não foi preciso mudar: os dois aquecimentos do M1 (docs/pedagogia/aquecimentos/m1-u1.json e m1-u2.json e as suas páginas) já
dizem «Dez minutos», «o som, o lugar e o nome» e «as passagens da tarefa», e não usam «núcleo», «fecho» nem «tema escolhido»; o
mapa do M1 não descreve as partes da aula de tarefa; o guia da tarefa do M1 nunca teve a «Autoavaliação» que se copiava para o
Teams nem «pergunta ao teu par de trabalho» (isso era só do guia do M3). Os testes fixam-no.

Decisões do docente (as mesmas do M3): «com consulta» quer dizer lições do site, caderno e dicionário, e diz-se uma vez, no
primeiro cartão; tempos 10 (aquecimento), 10 (leitura), 55 (produção) e 15 (revisão e entrega), 90 no total; os versos citados ou
copiados não contam para as palavras; a autoavaliação da grelha é só para o aluno e não se entrega (a versão de correção deixa de
ter a coluna «Aluno» e a nota «Diferença entre a tua nota e a minha»); o aquecimento é o primeiro passo, com uma só ligação; o
vocabulário é só o que as lições já dão; de uma obra longa entra só o passo trabalhado, inteiro e contínuo, copiado letra a letra
das lições; quando o enunciado troca uma palavra por outra mais simples, a grelha, a correção e o guia usam a mesma; o apoio
(exemplos com outro caso) fica em desdobrável fechado no ecrã e não sai em papel; a verificação final tem no máximo 10 perguntas
de sim ou não; em papel nenhum poema, nenhuma estrofe e nenhum texto se parte. As imagens são as que já estão no repositório
(img/fontes/), em domínio público, com o crédito completo atrás do «i».

De onde vêm os textos (cada bloco de texto dos dados traz a «origem»): m1-u1, lições F19 («Ondas do mar de Vigo», inteira) e F04
(«Quer'eu em maneira de proençal», estrofes 1 e 3 do cartão e estrofe 2 de «Ler mais»; «Ai dona fea, fostes-vos queixar»,
inteira); m1-u2, lições F06 e F20 (capítulo XII, do grito do pajem até «desejando cada um de ser o primeiro», com os passos que as
lições dão em «Ler mais») e F07 (capítulo CXVI, das torres ao sino da quadrilha, e capítulo CXLVIII, do trigo aos mortos nas
praças). Nenhum texto veio de fora das lições. Os Textos 1 e 2 da m1-u2 acabam em «[…]», como nas lições: a frase continua no
capítulo, e essa continuação não está em nenhuma lição.

O molde ganhou chaves opcionais para a prosa, para as imagens numeradas e para o que serve aos dois temas (scripts/tarefa_facil.py)
e a folha assets/task-textos.css ganhou regras para elas (versão facil-8, que só a m1-u1 e a m1-u2 pedem). As páginas do M3 saem
iguais, byte a byte.

O que NÃO muda: as outras onze tarefas, as suas grelhas, correções e aquecimentos (saem dos mesmos geradores, iguais byte a byte);
os critérios, os níveis, os exemplos e os pontos das grelhas (as trocas de palavras fazem-se só ao escrever as páginas); as lições.

O script tira as trocas da diferença entre a base (cada ficheiro com esta camada desfeita pelo manifesto; antes de haver
manifesto, o ficheiro no commit de base, lido com git) e a árvore: pode voltar a correr depois de a camada estar aplicada e dá o
mesmo JSON. Para mudar uma página ou os dados por baixo desta camada (uma correção ao enunciado, por exemplo): muda-se a árvore,
voltam a gerar-se as páginas e corre-se «python3 scripts/tarefas_faceis_m1_20261113.py --base-do-commit» (a base lê-se do commit de
base, porque o manifesto antigo já não confere), e depois scripts/aplicar_trocas.py, que reescreve o manifesto. Confere, antes de
escrever: que as três páginas do módulo só mudam nas trocas de EDICOES (com a de SAI); que os geradores, com os dados da árvore, dão as seis
páginas da árvore; que, com os dados da base, dão as seis páginas da base; e cada ficheiro como scripts/aplicar_trocas.py o vai
conferir (da base para o resultado e de volta, letra a letra).

As camadas de baixo desfazem primeiro esta: scripts/verificar_camadas.py (LAYERS[0]), tests/auditoria_20261028.py,
scripts/desligar_sala.py, scripts/tarefas_claras_historico.py (a leitura histórica dos enunciados; a camada do M3 lê por ela os
dados das grelhas) e as bases das camadas da decisão 152 que partilham ficheiros com ela.
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

CAMADA = ROOT / 'scripts/tarefas_faceis_m1_20261113.json'
MANIFESTO = ROOT / 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
BASE_COMMIT = '2b343fbe53a1cd2155baf4039041fa806fd99312'
SLUGS = ('m1-u1', 'm1-u2')
NBSP = '\xa0'

DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
DADOS_GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
FICHEIROS_DADOS = DADOS_TAREFAS + [DADOS_GRELHAS]
# Os aquecimentos não mudam (já usam as mesmas palavras): não entram na camada.
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'correcao/')]
GUIA, INDICE, PORTEFOLIO = 'm1/guia-da-tarefa-m1/index.html', 'm1/index.html', 'm1/portefolio-do-modulo-m1/index.html'
MODULO = [GUIA, INDICE, PORTEFOLIO]
FICHEIROS = FICHEIROS_DADOS + PAGINAS + MODULO

ACHADOS = {
    'facil': 'O molde «mais fácil de fazer», aprovado pelo docente no M3, chega ao M1: a mesma tarefa, com os textos completos junto '
             'da pergunta ou do tema que os usa, um pedido por alínea, os exemplos com outro caso em desdobrável, o primeiro cartão '
             'com o que se faz, o que se entrega e o quadro 10/10/55/15, e a verificação em perguntas de sim ou não.',
    'junto': '«Tudo junto» (decisão do docente): as mesmas palavras do enunciado novo («as duas perguntas» em vez de «núcleo»; «a letra '
             'do teu tema» em vez de «o tema escolhido»; «respostas ligadas» em vez de «articuladas»; «duas linhas finais» em vez de '
             '«fecho»).',
    'tempos': 'Tempos decididos pelo docente: 10 minutos de aquecimento, 10 de leitura, 55 de produção e 15 de revisão e entrega (eram '
              '10, 5, 60 e 15), iguais em todos os sítios onde aparecem.',
    'auto': 'Decisão do docente: a autoavaliação da grelha é só para o aluno e não se entrega; a versão de correção fica com a nota e '
            'o comentário do docente.',
    'conta': 'Decisão do docente: os versos citados ou copiados não contam para as palavras.',
    'sem_equipa': 'Decisão do docente (13/11/2026): não há trabalho de grupo nem de pares; no portefólio do módulo, «trabalho de equipa» '
                  'sai da lista do que o portefólio serve para avaliar, sem nada no lugar.',
}

# As três páginas do módulo não são geradas: mudam só nestas trocas (página, antigo, novo, ocorrências, categorias).
EDICOES = [
    (GUIA, f'leitura do enunciado</th><td role="cell" data-label="Tempo">5{NBSP}minutos</td>',
     f'leitura do enunciado</th><td role="cell" data-label="Tempo">10{NBSP}minutos</td>', 1, 'tempos'),
    (GUIA, f'produção com consulta</th><td role="cell" data-label="Tempo">60{NBSP}minutos</td>',
     f'produção com consulta</th><td role="cell" data-label="Tempo">55{NBSP}minutos</td>', 1, 'tempos'),
    (GUIA, 'Respondes ao núcleo comum e escolhes um tema, A ou B.', 'Respondes às duas perguntas e escolhes um tema, A ou B.', 1, 'junto'),
    (INDICE, f'pede uma crónica de 160 a 200{NBSP}palavras, além do núcleo comum.',
     f'pede uma crónica de 160 a 200{NBSP}palavras, além das duas perguntas.', 1, 'junto'),
]
# O que sai sem nada no lugar (página, antes, o que sai, depois, categorias): a troca leva os dois vizinhos, para ser única.
SAI = [
    (PORTEFOLIO, 'É a base da avaliação qualitativa do módulo: autonomia, responsabilidade,', ' trabalho de equipa,',
     ' pensamento crítico, entre outros.', 'sem_equipa'),
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
    """As seis páginas que os dois geradores dão com estes dados ({ficheiro de dados: texto}), numa pasta temporária."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for rel, texto in textos.items():
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_bytes(texto.encode('utf-8'))
        codigo = (
            'import sys, json; from pathlib import Path; sys.path.insert(0, "scripts"); tmp = Path(sys.argv[1])\n'
            'import tarefas_escolha as te, grelhas_tarefas as gt\n'
            'te.DADOS = tmp / "docs/pedagogia/tarefas-escolha"; te.GRELHAS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'gt.DADOS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'grelhas = json.loads(te.GRELHAS.read_text("utf-8"))["tarefas"]\n'
            'for s in ("m1-u1", "m1-u2"):\n'
            '    d = json.loads((te.DADOS / (s + ".json")).read_text("utf-8")); te.tarefa(d, s in grelhas, tmp / "saida")\n'
            'for s in ("m1-u1", "m1-u2"):\n'
            '    t = grelhas[s]\n'
            '    for pasta, html in (("grelha", gt.pagina_aluno(s, t)), ("correcao", gt.pagina_correcao(s, t))):\n'
            '        p = tmp / "saida/tarefas" / s / pasta / "index.html"; p.parent.mkdir(parents=True, exist_ok=True)\n'
            '        p.write_text(html, "utf-8", newline="\\n")\n'
            )
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
    m = re.search(r'm1-u(\d)', rel)
    u = f'M1-U{m.group(1)}' if m else 'M1'
    if rel in DADOS_TAREFAS:
        return f'Tarefa da {u}, os dados do enunciado'
    if rel == DADOS_GRELHAS:
        return 'Grelhas das tarefas do M1, os dados'
    if rel == GUIA:
        return 'Guia da tarefa do M1'
    if rel == INDICE:
        return 'Índice do M1'
    if rel == PORTEFOLIO:
        return 'Portefólio do módulo M1'
    return {'grelha': f'Grelha do aluno da {u}', 'correcao': f'Versão de correção da {u}'}.get(rel.split('/')[2], f'Enunciado da {u}')


def categorias(rel, antigo, novo):
    cs = set()
    if rel in DADOS_TAREFAS or rel.endswith(('m1-u1/index.html', 'm1-u2/index.html')):
        cs |= {'facil', 'tempos', 'conta', 'auto', 'junto'} if len(novo) > 2000 else {'facil'}
    elif rel == DADOS_GRELHAS or '/grelha/' in rel or '/correcao/' in rel:
        if 'autoavalia' in novo or 'Aluno</th>' in antigo or 'Diferença entre' in antigo or '<td></td><td></td><td></td>' in antigo:
            cs.add('auto')
        if 'versos citados' in novo:
            cs.add('conta')
        if 'trocas_aluno' in novo or re.search(r'ligadas|letra do|[Dd]uas perguntas|Pergunta.[12]: |[Dd]uas linhas finais|[Aa]s respostas, as fontes|no excerto', novo):
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
