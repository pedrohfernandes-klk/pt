#!/usr/bin/env python3
"""13/11/2026: as três tarefas do M7 (m7-u1, m7-u2 e m7-u3) «mais fáceis de fazer», com tudo o que fala delas a usar as mesmas palavras.

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201, camada tarefas_faceis_m3_20261112) e
levado ao M1 (#203), ao M5 (#204) e ao M6 (#205, camada tarefas_faceis_m6_20261113). Esta camada leva o mesmo molde ao M7. Cada
tarefa é a mesma (as mesmas ordens, os mesmos temas A e B na m7-u3, o mesmo total de palavras, os mesmos critérios da grelha); muda
só a forma.

Constrói scripts/tarefas_faceis_m7_20261113.json, a camada literal tarefas_faceis_m7_20261113, que se aplica com
scripts/aplicar_trocas.py; o manifesto fica em tests/fixtures/tarefas-faceis-m7-edits-20261113.json:

  python3 scripts/tarefas_faceis_m7_20261113.py
  python3 scripts/aplicar_trocas.py scripts/tarefas_faceis_m7_20261113.json \\
      --manifesto tests/fixtures/tarefas-faceis-m7-edits-20261113.json \\
      --base-commit fe614d6750b7c4b93fd58f739415f6a250310552 --nota "…"

Fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima das tarefas do M6 mais fáceis de fazer
(tarefas_faceis_m6_20261113), com a qual partilha um ficheiro: os dados das grelhas (docs/pedagogia/grelhas-tarefas-20261027.json),
que também partilha com as camadas das tarefas do M5, do M1 e do M3. Partilha ficheiros também com a revisão dos enunciados
(tarefas_claras_20261110), com a decisão 152 no M7 (cuidado_m7_20261111) e com as camadas mais antigas do guia e do portefólio:
todas a desfazem primeiro.

Ficheiros (13):
- os dados: docs/pedagogia/tarefas-escolha/m7-u3.json (a chave nova «facil», de onde sai a página; as chaves antigas ficam como
  estavam, para a leitura histórica das camadas de baixo), docs/pedagogia/grelhas-tarefas-20261027.json («autoavaliacao_so_tua»,
  «correcao_estreita» e «trocas_aluno» na grelha da m7-u3: «opinião» onde dizia «tese», «comparação» onde dizia «outra voz» e
  «confronto», «duas linhas finais» onde dizia «fecho») e docs/pedagogia/aquecimentos/m7-u1.json e m7-u3.json (os tempos e as palavras
  do enunciado novo; na m7-u3, os dois temas com as palavras do enunciado);
- as páginas: tarefas/m7-u1/ (enunciado e aquecimento/), tarefas/m7-u2/ (enunciado) e tarefas/m7-u3/ (enunciado, grelha/,
  aquecimento/ e correcao/);
- as páginas do módulo que falam da aula de tarefa: m7/guia-da-tarefa-m7/ (quatro blocos de 10, 10, 55 e 15 minutos em vez de três
  de 15, 60 e 15; «opinião» e «comparação» na tarefa da unidade 3; sem a «Autoavaliação» que se copiava para o Teams e sem «pergunta
  ao teu par de trabalho»: a regra passa a chamar-se «Dois antes de mim») e m7/portefolio-do-modulo-m7/ (sai «trabalho de equipa»,
  sem nada no lugar; este portefólio não tinha a autoavaliação de 0 a 20 por parâmetro). O índice e o mapa do M7 não dizem «núcleo
  comum» nem os tempos da aula de tarefa: ficam como estavam.

A m7-u1 e a m7-u2 não são tarefas de escolha (não têm temas A e B nem grelha /20: a rubrica está no guia da tarefa) e as suas páginas
eram escritas à mão. Passam a sair de dados novos (docs/pedagogia/tarefas-individuais/m7-u1.json e m7-u2.json, que não são da camada:
são ficheiros novos) por scripts/tarefas_individuais_faceis.py e pelo mesmo molde (scripts/tarefa_facil.py, pagina_individual). A
camada guarda a troca da página antiga pela nova, para as camadas de baixo a lerem como era.

Decisões do docente (as mesmas do M3, do M1, do M5 e do M6): «com consulta» quer dizer lições do site, caderno e dicionário, e diz-se
uma vez, no primeiro cartão; tempos 10 (aquecimento), 10 (leitura), 55 (produção) e 15 (revisão e entrega), 90 no total; os versos
citados ou copiados não contam para as palavras; a autoavaliação da grelha é só para o aluno e não se entrega; o aquecimento é o
primeiro passo, com uma só ligação; o vocabulário é só o que as lições já dão; os poemas vêm das lições, letra a letra; quando o
enunciado troca uma palavra por outra mais simples, a grelha, a correção, o aquecimento e o guia usam a mesma; o apoio (exemplos com
outro caso) fica em desdobrável fechado no ecrã e não sai em papel; a verificação final tem no máximo 10 perguntas de sim ou não. Só
do M7: na m7-u3 só entram completos «Mar Português» e «D. Sebastião, Rei de Portugal».

De onde vêm os textos (cada bloco de texto dos dados traz a «origem»): m7-u1, lições F14 («Não sei se é sonho, se realidade», os 24
versos dos cartões «O texto, 1 de 2» e «O texto, 2 de 2», com o vocabulário e a linha de fonte) e F15 («Quando as crianças brincam»,
os 12 versos do cartão «O texto»); m7-u2, nenhum (o texto é do aluno); m7-u3, lições F08 («Mar Português», os 12 versos do cartão «O
texto, 2 de 2», com o vocabulário e a linha de fonte) e F09 («D. Sebastião, Rei de Portugal», os 10 versos do cartão «O texto, 1 de
3», com a linha de fonte; o vocabulário de «areal» vem do cartão «O texto, 3 de 3»). Nenhum texto veio de fora das lições e nada
ficou por dar. Não há imagens.

Os exemplos (regra do docente: sempre com outro caso, sem frases dos textos da tarefa). Na m7-u1, outro par de poemas («Autopsicografia»
e «Ela canta, pobre ceifeira», com as frases do aquecimento e versos das lições F02 e F13). Na m7-u2, o perfil e o texto de Augusto
Pires (o exemplo do guia da tarefa), um verso de Caeiro (lição F35) e duas lições sobre Campos (F01 e F11), como no aquecimento. Na
m7-u3, o texto «Ensaiar vale a pena?», o verso de «O Infante» e a data da «Tabacaria», que são os exemplos da grelha; o exemplo antigo
«Descobre o movimento (resolvido)» usava o verso 1 de «D. Sebastião, Rei de Portugal» (o Texto 2) e não entra; o quadro dos seis
movimentos mostra-os com o tema do ensaio e com a frase da lição F07, e não com os versos dos dois poemas (o quadro da lição F10, que
os usa, continua na lição).

O molde ganhou chaves opcionais (scripts/tarefa_facil.py): «perguntas» vazia com «temas_relogio» e «depois» (a tarefa em que se escolhe
primeiro e se escreve um só texto), «opcional» (a pergunta opcional com «opinião»), um apoio com «html», e pagina_individual(). A folha
assets/task-textos.css ganhou as regras das tarefas individuais (versão facil-11, que só as três páginas do M7 pedem). As páginas do
M3, do M1, do M5 e do M6 saem iguais, byte a byte.

O que NÃO muda: as outras tarefas, as suas grelhas, correções e aquecimentos (saem dos mesmos geradores, iguais byte a byte); os
critérios, os níveis, os exemplos e os pontos da grelha da m7-u3 (as trocas de palavras fazem-se só ao escrever as páginas); a rubrica
da m7-u1 e da m7-u2 no guia; as lições.

O script tira as trocas da diferença entre a base (cada ficheiro com esta camada desfeita pelo manifesto; antes de haver manifesto,
o ficheiro no commit de base, lido com git) e a árvore: pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.
Para mudar uma página ou os dados por baixo desta camada: muda-se a árvore, voltam a gerar-se as páginas e corre-se «python3
scripts/tarefas_faceis_m7_20261113.py --base-do-commit» (a base lê-se do commit de base, porque o manifesto antigo já não confere), e
depois scripts/aplicar_trocas.py, que reescreve o manifesto. Confere, antes de escrever: que os geradores, com os dados da árvore,
dão as páginas da árvore (as sete geradas das tarefas de escolha e dos aquecimentos, e as duas individuais); que, com os dados da
base, dão as páginas da base (as quatro da m7-u3; o aquecimento da m7-u1 cita o enunciado antigo da m7-u1, que era escrito à mão, e por isso só se confere com os dados da árvore); e cada ficheiro como scripts/aplicar_trocas.py o vai conferir (da base
para o resultado e de volta, letra a letra).

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

CAMADA = ROOT / 'scripts/tarefas_faceis_m7_20261113.json'
MANIFESTO = ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'
BASE_COMMIT = 'fe614d6750b7c4b93fd58f739415f6a250310552'
NBSP = '\xa0'

DADOS_TAREFAS = ['docs/pedagogia/tarefas-escolha/m7-u3.json']
DADOS_GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DADOS_AQUECIMENTOS = ['docs/pedagogia/aquecimentos/m7-u1.json', 'docs/pedagogia/aquecimentos/m7-u3.json']
FICHEIROS_DADOS = DADOS_TAREFAS + [DADOS_GRELHAS] + DADOS_AQUECIMENTOS
# As páginas que já saíam dos geradores (com os dados da base dão a página da base) e as duas que eram escritas à mão.
PAGINAS = ['tarefas/m7-u1/aquecimento/index.html'] + [f'tarefas/m7-u3/{p}index.html' for p in ('', 'grelha/', 'aquecimento/', 'correcao/')]
INDIVIDUAIS = ['tarefas/m7-u1/index.html', 'tarefas/m7-u2/index.html']
GUIA, PORTEFOLIO = 'm7/guia-da-tarefa-m7/index.html', 'm7/portefolio-do-modulo-m7/index.html'
MODULO = [GUIA, PORTEFOLIO]
FICHEIROS = FICHEIROS_DADOS + INDIVIDUAIS + PAGINAS + MODULO

ACHADOS = {
    'facil': 'O molde «mais fácil de fazer», aprovado pelo docente no M3, chega ao M7: a mesma tarefa, com os textos das lições junto '
             'do pedido ou do tema que os usa, um pedido por alínea, os exemplos com outro caso em desdobrável, o primeiro cartão '
             'com o que se faz, o que se entrega e o quadro 10/10/55/15, e a verificação em perguntas de sim ou não.',
    'junto': '«Tudo junto» (decisão do docente): as mesmas palavras do enunciado novo («opinião» em vez de «tese»; «comparação» em vez '
             'de «outra voz» e «confronto»; «duas linhas finais» em vez de «fecho» e «síntese»; os dois temas da m7-u3 ditos como no '
             'enunciado).',
    'tempos': 'Tempos decididos pelo docente: 10 minutos de aquecimento, 10 de leitura, 55 de produção e 15 de revisão e entrega, '
              'iguais em todos os sítios onde aparecem.',
    'auto': 'Decisão do docente: a autoavaliação da grelha é só para o aluno e não se entrega; a versão de correção fica com a nota e '
            'o comentário do docente.',
    'sem_auto': 'Decisão do docente (13/11/2026): no guia da tarefa, a «Autoavaliação» que se copiava para o Teams sai, porque a '
                'autoavaliação é só para o aluno e não se entrega; o plano, as notas e a lista de verificação continuam a copiar-se.',
    'sem_par': 'Decisão do docente (13/11/2026): não há trabalho de grupo nem de pares; a regra fica com os dois primeiros passos '
               '(«Dois antes de mim»).',
    'sem_equipa': 'Decisão do docente (13/11/2026): não há trabalho de grupo nem de pares; no portefólio do módulo, «trabalho de equipa» '
                  'sai da lista do que o portefólio serve para avaliar, sem nada no lugar.',
}


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


def gerar_com(textos, individuais=False):
    """As páginas que os geradores dão com estes dados ({ficheiro de dados: texto}), numa pasta temporária: as cinco das tarefas de
    escolha e dos aquecimentos e, com «individuais», as duas das tarefas individuais (dos dados da árvore, que não são da camada)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for rel, texto in textos.items():
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_bytes(texto.encode('utf-8'))
        codigo = (
            'import sys, json; from pathlib import Path; sys.path.insert(0, "scripts"); tmp = Path(sys.argv[1])\n'
            'import tarefas_escolha as te, grelhas_tarefas as gt, aquecimentos as aq, tarefas_individuais_faceis as ti\n'
            'te.DADOS = tmp / "docs/pedagogia/tarefas-escolha"; te.GRELHAS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'gt.DADOS = tmp / "docs/pedagogia/grelhas-tarefas-20261027.json"\n'
            'grelhas = json.loads(te.GRELHAS.read_text("utf-8"))["tarefas"]\n'
            's = "m7-u3"\n'
            'd = json.loads((te.DADOS / (s + ".json")).read_text("utf-8")); te.tarefa(d, s in grelhas, tmp / "saida")\n'
            't = grelhas[s]\n'
            'for pasta, html in (("grelha", gt.pagina_aluno(s, t)), ("correcao", gt.pagina_correcao(s, t))):\n'
            '    p = tmp / "saida/tarefas" / s / pasta / "index.html"; p.parent.mkdir(parents=True, exist_ok=True)\n'
            '    p.write_text(html, "utf-8", newline="\\n")\n'
            'ti.main(["--saida", str(tmp / "saida")])\n'
            'sys.exit(aq.main(["--saida", str(tmp / "saida"), "--dados", str(tmp / "docs/pedagogia/aquecimentos")] + sys.argv[2:]) or 0)\n')
        r = subprocess.run([sys.executable, '-c', codigo, str(tmp)] + (['m7-u1', 'm7-u3'] if individuais else ['m7-u3']), cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if r.returncode:
            raise SystemExit('os geradores falharam: ' + r.stdout + r.stderr)
        # O aquecimento da m7-u1 cita o enunciado da m7-u1, que na base era outra página, escrita à mão: com os dados da base não se gera.
        return {rel: (tmp / 'saida' / rel).read_bytes().decode('utf-8') for rel in (PAGINAS + INDIVIDUAIS if individuais else PAGINAS[1:])}

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
    m = re.search(r'm7-u(\d)', rel)
    u = f'M7-U{m.group(1)}' if m else 'M7'
    if rel in DADOS_TAREFAS:
        return f'Tarefa da {u}, os dados do enunciado'
    if rel == DADOS_GRELHAS:
        return 'Grelha da tarefa da M7-U3, os dados'
    if rel in DADOS_AQUECIMENTOS:
        return f'Aquecimento da {u}, os dados'
    if rel == GUIA:
        return 'Guia da tarefa do M7'
    if rel == PORTEFOLIO:
        return 'Portefólio do módulo M7'
    return {'grelha': f'Grelha do aluno da {u}', 'aquecimento': f'Aquecimento da {u}', 'correcao': f'Versão de correção da {u}'}.get(
        rel.split('/')[2], f'Enunciado da {u}')


def categorias(rel, antigo, novo):
    cs = set()
    if rel in DADOS_TAREFAS or rel in INDIVIDUAIS or rel == 'tarefas/m7-u3/index.html':
        cs |= {'facil', 'tempos', 'junto'} | ({'auto'} if 'm7-u3' in rel else set())
    elif rel == DADOS_GRELHAS or '/grelha/' in rel or '/correcao/' in rel:
        if 'autoavalia' in novo or 'Aluno</th>' in antigo or 'Diferença entre' in antigo or '<td></td><td></td><td></td>' in antigo:
            cs.add('auto')
        if 'trocas_aluno' in novo or not cs:
            cs.add('junto')
    elif rel == GUIA:
        if 'Autoavaliação' in antigo or 'AUTOAVALIAÇÃO' in antigo or 'autoavaliação' in antigo or 'dataset.auto' in antigo or 'r-auto' in antigo or 'dás-te um nível' in antigo:
            cs.add('sem_auto')
        if 'par de trabalho' in antigo:
            cs.add('sem_par')
        if re.search(r'(15|60|10|55)(' + NBSP + r'| )min|BLOCOS|15:00', antigo + novo):
            cs.add('tempos')
        if 'opinião' in novo or 'comparação' in novo or not cs:
            cs.add('junto')
    elif rel == PORTEFOLIO:
        cs.add('sem_equipa')
    else:  # os aquecimentos e os seus dados
        cs.add('junto')
        if re.search(r'(55|Dez)' + NBSP + 'minutos', novo):
            cs.add('tempos')
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
    # Os geradores dão as páginas da árvore com os dados da árvore, e as da base com os dados da base.
    for k, quando in ((1, 'da árvore'), (0, 'da base')):
        geradas = gerar_com({rel: finais[rel][k] for rel in FICHEIROS_DADOS}, individuais=bool(k))
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
