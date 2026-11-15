#!/usr/bin/env python3
"""15/11/2026: a tarefa m4-u2 no molde «mais fácil de fazer», com «Tema A ou B», e «tudo junto» no M4; no mesmo pedido, um acerto
do M8 (os quatro poemas da m8-u1 estão no manual).

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201, camada tarefas_faceis_m3_20261112) e
levado ao M1, ao M5, ao M6, ao M7, ao M8 e ao M9 (#208, camada tarefas_faceis_m9_20261114). Esta camada leva-o à tarefa da
unidade 2 do M4, que era escrita à mão e não estava nos dados das tarefas de escolha.

DECISÕES DO DOCENTE (15/11/2026) para a m4-u2:
- a tarefa passa a «Tema A ou B» na mesma tarefa. Tema A: a apreciação crítica do espetáculo que já existia (o mesmo pedido, com
  título, 180 a 240 palavras, o mesmo espetáculo: <i>TPC: Frei Luís de Sousaaa</i>, de Raquel Castro, visto no LU.CA). Tema B: um
  texto de opinião sobre a pergunta escolhida pelo docente, letra a letra: «Que juízo merece Telmo, quando cala o nome do retrato no
  ato II de <i>Frei Luís de Sousa</i>: cumpre a palavra dada ou engana Maria?». A mesma extensão e os mesmos critérios nos dois;
- sai a opção «Se não foste ao teatro» (o desdobrável do enunciado, a frase do guia e a do aquecimento);
- as falas do tema B são só as que as lições do M4 citam, conferidas letra a letra: o diálogo do retrato (ato II, cena I), inteiro
  e contínuo, das lições F26 (cartão 13 e o seu «Ler mais»), F08 (cartões 2 e 4) e «Quem sabia, e quando» (cartão 10); e, no
  Texto 2, as falas curtas das lições F27 (cartão 16), «Quem sabia, e quando» (cartão 2) e F08 (cartão 4, «Ler mais»). A razão da
  promessa de Telmo só está parafraseada na lição F27 (cartão 16): a página dá o resumo da lição, dito como resumo. A peça inteira
  lê-se no livro (nenhuma lição do M4 diz «no manual»).

A página da m4-u2 passa a sair de dados novos, docs/pedagogia/tarefas-escolha/m4-u2.json (não são da camada: é um ficheiro novo,
como os das tarefas individuais do M7), por scripts/tarefas_escolha.py e pelo molde (scripts/tarefa_facil.py, que ganha uma chave
opcional, «opcionais», para guardar as duas perguntas opcionais de antes). A camada guarda a troca da página antiga pela nova, para
as camadas de baixo a lerem como era.

Constrói scripts/tarefa_m4u2_tema_b_20261115.json, a camada literal, que se aplica com scripts/aplicar_trocas.py; o manifesto fica em
tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json:

  python3 scripts/tarefa_m4u2_tema_b_20261115.py
  python3 scripts/aplicar_trocas.py scripts/tarefa_m4u2_tema_b_20261115.json \\
      --manifesto tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json \\
      --base-commit 015ee060613875e1b1377a905a8d5f4c2dbc0ad0 --nota "…"

Fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima das tarefas do M9 mais fáceis de fazer
(tarefas_faceis_m9_20261114), com a qual partilha os dados das grelhas (docs/pedagogia/grelhas-tarefas-20261027.json), que também
partilha com as camadas das tarefas do M8, do M7, do M6, do M5, do M1 e do M3. Partilha ficheiros com camadas mais antigas (a
decisão 152 no M4 e no M8, os aquecimentos do M4, a autonomia 154, o índice da decisão 148 e as camadas do índice, do mapa, do guia e
do portefólio): todas a desfazem primeiro.

Ficheiros (14):
- os dados: docs/pedagogia/aquecimentos/m4-u2.json (no aquecimento, «no teu texto» onde dizia «na tua apreciação», duas vezes; o
  cartão «Para levar» serve os dois temas e perde a frase da alternativa de leitura; as falas novas da tarefa entram nas
  «reservadas», que nenhum cartão pode usar), docs/pedagogia/tarefas-escolha/m8-u1.json e docs/pedagogia/grelhas-tarefas-20261027.json
  (o acerto do M8);
- as páginas: tarefas/m4-u2/ (o enunciado, a página nova no lugar da escrita à mão, e o aquecimento) e tarefas/m8-u1/ (o enunciado
  e a grelha; a versão de correção não diz onde se leu e não muda);
- as páginas do M4 que falam da aula de tarefa: m4/guia-da-tarefa-m4/ (a unidade 2 com o novo título, o tema A ou B, os tempos
  10/10/55/15 e a frase do que não conta para as palavras; «escreves duas linhas finais» onde dizia «fazes uma síntese simples
  integrada»; sai «Se faltaste à ida ao teatro»), m4/index.html, m4/mapa-do-modulo-m4/ e m4/portefolio-do-modulo-m4/ (o novo título;
  «duas linhas finais» onde dizia «síntese»; no portefólio sai «trabalho de equipa», sem nada no lugar; no índice, o cartão da
  apreciação crítica diz «180 a 240 palavras», como a tarefa; no mapa, o segundo critério da tarefa 2 é «Relação com Garrett», que
  serve os dois temas, onde dizia «Do texto ao palco»);
- a lição F20 (cartão «O fogo de Manuel», «Ler mais») e o plano da aula 11 deixam de dizer que a cena do incêndio é a da tarefa
  para quem faltou ao teatro (sai a opção «Se não foste ao teatro»); a frase que fica pede só a comparação da leitura em voz alta
  com a leitura em silêncio. O cartão «Agora, em papel» da F20 (e a sua cópia no plano da aula 11) é o exercício da própria lição e
  não muda: fica como dúvida para o docente;
- ACERTO DO M8: m8/guia-da-tarefa-m8/ («lê os dois poemas de cada tema antes da aula, no manual» e «dizem também onde ler»).

ACERTO DO M8 (decisão do docente, 15/11/2026): «Adeus», «Prece no Mediterrâneo» e «A verdade histórica» estão no manual. Na m8-u1,
as linhas de fonte dos Textos 2, 3 e 4 voltam a dizer «O poema completo lê-se no manual.», com o cartão da lição, como a do Texto 1;
a alínea de onde se leu e a grelha dizem «o manual, a publicação que a lição indica ou outra edição»; o cartão «Rever a matéria» diz
que os poemas se leem no manual. As camadas já publicadas não mudam.

Os exemplos (regra do docente: outro caso, sem frases da peça nem do espetáculo, sem dar feita nenhuma alínea, sem repetir o
aquecimento e sem inventar factos): dois casos inventados, ditos como inventados (uma récita da escola, com o figurino, que o
aquecimento não usa; a bibliotecária da escola, um juízo com um só lado, um critério e um pormenor, que não tem a forma da pergunta do
tema B).

O script tira as trocas da diferença entre a base (cada ficheiro com esta camada desfeita pelo manifesto; antes de haver manifesto,
ou com --base-do-commit, o ficheiro no commit de base, lido com git) e a árvore: pode voltar a correr depois de a camada estar
aplicada e dá o mesmo JSON. Para mudar uma página ou os dados por baixo desta camada: muda-se a árvore, voltam a gerar-se as páginas
e corre-se «python3 scripts/tarefa_m4u2_tema_b_20261115.py --base-do-commit», e depois scripts/aplicar_trocas.py, que reescreve o
manifesto. Confere, antes de escrever: que os geradores, com os dados da árvore, dão as páginas da árvore e, com os dados da base, as
páginas da base (a m4-u2 só com os dados da árvore, porque na base era escrita à mão); e cada ficheiro como scripts/aplicar_trocas.py
o vai conferir (da base para o resultado e de volta, letra a letra).

As camadas de baixo desfazem primeiro esta: scripts/verificar_camadas.py (LAYERS[0]), tests/auditoria_20261028.py,
scripts/desligar_sala.py, scripts/tarefas_claras_historico.py e as bases das camadas que partilham ficheiros com ela.
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

CAMADA = ROOT / 'scripts/tarefa_m4u2_tema_b_20261115.json'
MANIFESTO = ROOT / 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json'
BASE_COMMIT = '015ee060613875e1b1377a905a8d5f4c2dbc0ad0'
NBSP = '\xa0'

DADOS_AQUECIMENTO = 'docs/pedagogia/aquecimentos/m4-u2.json'
DADOS_M8 = 'docs/pedagogia/tarefas-escolha/m8-u1.json'
DADOS_GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
FICHEIROS_DADOS = [DADOS_AQUECIMENTO, DADOS_M8, DADOS_GRELHAS]
# 15/11/2026: os dados novos da m4-u2 (não são da camada: ficheiro novo, como os das tarefas individuais do M7).
DADOS_M4U2 = 'docs/pedagogia/tarefas-escolha/m4-u2.json'
ENUNCIADO = 'tarefas/m4-u2/index.html'
AQUECIMENTO = 'tarefas/m4-u2/aquecimento/index.html'
PAGINAS_M8 = ['tarefas/m8-u1/index.html', 'tarefas/m8-u1/grelha/index.html']
# As páginas que saem dos geradores com os dados da base e com os da árvore (a m4-u2 só com os da árvore).
PAGINAS = [AQUECIMENTO] + PAGINAS_M8
GUIA, INDICE, MAPA = 'm4/guia-da-tarefa-m4/index.html', 'm4/index.html', 'm4/mapa-do-modulo-m4/index.html'
PORTEFOLIO = 'm4/portefolio-do-modulo-m4/index.html'
# 15/11/2026 (revisão): a lição F20 e o plano da aula 11 ligavam a cena do incêndio à opção «Se não foste ao teatro» da tarefa.
LICAO_F20, AULA_11 = 'm4/licao-m4-f20/index.html', 'm4/aulas/aula-11/index.html'
GUIA_M8 = 'm8/guia-da-tarefa-m8/index.html'
MODULO = [GUIA, INDICE, MAPA, PORTEFOLIO, LICAO_F20, AULA_11]
FICHEIROS = FICHEIROS_DADOS + [ENUNCIADO] + PAGINAS + MODULO + [GUIA_M8]

ACHADOS = {
    'facil': 'O molde «mais fácil de fazer», aprovado pelo docente no M3, chega à tarefa da unidade 2 do M4: a mesma tarefa, com o '
             'tema A (a apreciação crítica do espetáculo) e o tema B (o texto de opinião sobre Telmo, decisão do docente de '
             '15/11/2026), um pedido por alínea, as falas de Garrett que as lições citam, letra a letra, os exemplos com outro caso em '
             'desdobrável, o primeiro cartão com o que se faz, o que se entrega e o quadro 10/10/55/15, e a verificação em perguntas de '
             'sim ou não.',
    'teatro': 'Decisão do docente (15/11/2026): sai a opção «Se não foste ao teatro».',
    'aquecimento': 'Decisão do docente (15/11/2026): o aquecimento serve os dois temas; muda pouco e no molde.',
    'junto': '«Tudo junto» (decisão do docente): as mesmas palavras do enunciado novo (o título novo da tarefa; «duas linhas finais» '
             'em vez de «síntese»; «tema A ou B»; a mesma frase do que não conta para as palavras; os tempos 10/10/55/15).',
    'sem_equipa': 'Decisão do docente: não há trabalho de grupo nem de pares; no portefólio do módulo sai «trabalho de equipa», sem '
                  'nada no lugar.',
    'manual': 'Acerto do M8 (decisão do docente, 15/11/2026): «Adeus», «Prece no Mediterrâneo» e «A verdade histórica» estão no '
              'manual, como «As Palavras»; onde se diz onde se leu, «o manual, a publicação que a lição indica ou outra edição».',
}


def ler(rel):
    # 15/11/2026: por cima desta camada fica a das duas linhas finais em vez da síntese integrada (sintese_duas_linhas_20261115), que
    # não partilha ficheiros com esta: desfaz-se primeiro, com contagem estrita, quando o ficheiro a traz (a «árvore» desta camada é o
    # ficheiro como ela o deixou).
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 15/11/2026: e, antes dessa, a fila final (fila_final_20261115), que muda o portefólio do M4 (partilha-o com esta camada): desfaz-se
    # primeiro, com contagem estrita.
    fila_final = ROOT / 'tests/fixtures/fila-final-edits-20261115.json'
    if fila_final.is_file():
        for e in reversed(json.loads(fila_final.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: a fila final já não confere ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
    sintese = ROOT / 'tests/fixtures/sintese-duas-linhas-edits-20261115.json'
    if sintese.is_file():
        for e in reversed(json.loads(sintese.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: as duas linhas finais em vez da síntese integrada já não conferem ({e["location"]})')
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


def gerar_com(textos, com_m4u2):
    """As páginas que os geradores dão com estes dados ({ficheiro de dados: texto}), numa pasta temporária: o aquecimento da m4-u2,
    o enunciado e a grelha da m8-u1 e, com «com_m4u2», o enunciado da m4-u2 (dos dados novos da árvore, que não são da camada)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for rel, texto in textos.items():
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_bytes(texto.encode('utf-8'))
        if com_m4u2:
            (tmp / DADOS_M4U2).write_bytes((ROOT / DADOS_M4U2).read_bytes())
        codigo = (
            'import sys, json; from pathlib import Path; sys.path.insert(0, "scripts"); tmp = Path(sys.argv[1])\n'
            'import tarefas_escolha as te, grelhas_tarefas as gt, aquecimentos as aq\n'
            'te.DADOS = tmp / "docs/pedagogia/tarefas-escolha"; te.GRELHAS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'gt.DADOS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'grelhas = json.loads(te.GRELHAS.read_text("utf-8"))["tarefas"]\n'
            'for s in sys.argv[2:]:\n'
            '    d = json.loads((te.DADOS / (s + ".json")).read_text("utf-8")); te.tarefa(d, s in grelhas, tmp / "saida")\n'
            'html = gt.pagina_aluno("m8-u1", grelhas["m8-u1"])\n'
            'p = tmp / "saida/tarefas/m8-u1/grelha/index.html"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(html, "utf-8", newline="\\n")\n'
            'sys.exit(aq.main(["--saida", str(tmp / "saida"), "--dados", str(tmp / "docs/pedagogia/aquecimentos"), "m4-u2"]) or 0)\n')
        slugs = ['m8-u1'] + (['m4-u2'] if com_m4u2 else [])
        r = subprocess.run([sys.executable, '-c', codigo, str(tmp)] + slugs, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if r.returncode:
            raise SystemExit('os geradores falharam: ' + r.stdout + r.stderr)
        return {rel: (tmp / 'saida' / rel).read_bytes().decode('utf-8') for rel in PAGINAS + ([ENUNCIADO] if com_m4u2 else [])}

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
    return {DADOS_AQUECIMENTO: 'Aquecimento da M4-U2, os dados', DADOS_M8: 'Tarefa da M8-U1, os dados do enunciado',
            DADOS_GRELHAS: 'Grelhas das tarefas (M8-U1), os dados', ENUNCIADO: 'Enunciado da M4-U2', AQUECIMENTO: 'Aquecimento da M4-U2',
            'tarefas/m8-u1/index.html': 'Enunciado da M8-U1', 'tarefas/m8-u1/grelha/index.html': 'Grelha do aluno da M8-U1',
            GUIA: 'Guia da tarefa do M4', INDICE: 'Índice do M4', MAPA: 'Mapa do módulo M4', PORTEFOLIO: 'Portefólio do módulo M4',
            GUIA_M8: 'Guia da tarefa do M8', LICAO_F20: 'Lição F20 do M4', AULA_11: 'Plano da aula 11 do M4'}[rel]


def categorias(rel, antigo, novo):
    if rel in (DADOS_M8, DADOS_GRELHAS, GUIA_M8) or rel.startswith('tarefas/m8-u1/'):
        return ['manual']
    if rel == ENUNCIADO:
        return ['facil', 'teatro', 'junto']
    cs = set()
    if rel in (DADOS_AQUECIMENTO, AQUECIMENTO):
        cs.add('aquecimento')
        if 'alternativa de leitura' in antigo:
            cs.add('teatro')
    if 'faltaste' in antigo or 'não foste' in antigo or 'faltou ao teatro' in antigo:
        cs.add('teatro')
    if 'trabalho de equipa' in antigo:
        cs.add('sem_equipa')
    if rel in (LICAO_F20, AULA_11):
        return [c for c in ACHADOS if c in cs]
    if not cs or 'síntese' in antigo or 'Apreciação crítica do espetáculo' in antigo:
        cs.add('junto')
    return [c for c in ACHADOS if c in cs]


def trocas_do_ficheiro(rel, a, b):
    trocas = []
    for antigo, novo in trocas_do_texto(a, b):
        trecho = _visivel(novo)
        trecho = trecho if len(trecho) <= 90 else trecho[:88].rstrip() + '…'
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}: «{trecho}»', 'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
                       'achado': '15/11/2026: ' + ' '.join(ACHADOS[c] for c in categorias(rel, antigo, novo))})
    return trocas


def construir():
    """Devolve (trocas, {ficheiro: (base, final)})."""
    finais = {rel: (base(rel), ler(rel)) for rel in FICHEIROS}
    if all(a == b for a, b in finais.values()):
        raise SystemExit('a camada não está aplicada nesta árvore: aplica-a com scripts/aplicar_trocas.py e o JSON que já existe')
    # Os geradores dão as páginas da árvore com os dados da árvore, e as da base com os dados da base (a m4-u2 só da árvore).
    for k, quando in ((1, 'da árvore'), (0, 'da base')):
        geradas = gerar_com({rel: finais[rel][k] for rel in FICHEIROS_DADOS}, com_m4u2=bool(k))
        for rel in geradas:
            if geradas[rel] != finais[rel][k]:
                raise SystemExit(f'{rel}: com os dados {quando}, os geradores não dão a página {quando}')
    todas = []
    for rel in FICHEIROS:
        a, b = finais[rel]
        if a == b:
            raise SystemExit(f'{rel}: nada muda')
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
