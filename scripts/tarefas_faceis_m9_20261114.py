#!/usr/bin/env python3
"""14/11/2026: as duas tarefas do M9 (m9-u1 e m9-u2) «mais fáceis de fazer», com tudo o que fala delas a usar as mesmas palavras, e
dois acertos: o guia da tarefa do M2 e o índice do M7. 15/11/2026: «no livro» onde as páginas diziam «na edição da turma».

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201, camada tarefas_faceis_m3_20261112) e
levado ao M1, ao M5, ao M6, ao M7 e ao M8 (#207, camada tarefas_faceis_m8_20261113). Esta camada leva o mesmo molde ao M9. Cada
tarefa é a mesma (as mesmas ordens, os mesmos temas A e B, o mesmo total de palavras, os mesmos critérios da grelha); muda só a forma.

Constrói scripts/tarefas_faceis_m9_20261114.json, a camada literal tarefas_faceis_m9_20261114, que se aplica com
scripts/aplicar_trocas.py; o manifesto fica em tests/fixtures/tarefas-faceis-m9-edits-20261114.json:

  python3 scripts/tarefas_faceis_m9_20261114.py
  python3 scripts/aplicar_trocas.py scripts/tarefas_faceis_m9_20261114.json \\
      --manifesto tests/fixtures/tarefas-faceis-m9-edits-20261114.json \\
      --base-commit 85c4b50420a00513d252a9da09e4901a4c3f4a49 --nota "…"

Fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima das tarefas do M8 mais fáceis de fazer
(tarefas_faceis_m8_20261113), com a qual partilha um ficheiro: os dados das grelhas (docs/pedagogia/grelhas-tarefas-20261027.json),
que também partilha com as camadas das tarefas do M7, do M6, do M5, do M1 e do M3. Com a do M7 partilha também o índice do M7. Partilha
ficheiros também com a revisão dos enunciados (tarefas_claras_20261110), com a decisão 152 no M9 e no M2 (cuidado_m9_20261112,
cuidado_m2_20261108), com o índice da decisão 148 e com as camadas mais antigas do índice, do mapa, do guia e do portefólio: todas a
desfazem primeiro.

Ficheiros (21; 15 até 15/11/2026):
- os dados: docs/pedagogia/tarefas-escolha/m9-u1.json e m9-u2.json (a chave nova «facil», de onde sai a página; as chaves antigas
  ficam como estavam, para a leitura histórica das camadas de baixo) e docs/pedagogia/grelhas-tarefas-20261027.json
  («autoavaliacao_so_tua», «correcao_estreita» e «trocas_aluno» nas grelhas da m9-u1 e da m9-u2: «plano» onde dizia «núcleo» e
  «núcleo de planificação», «duas linhas finais» onde dizia «síntese», «a letra do tema», «a edição que usaste (a editora e o ano)»
  onde dizia «a edição consultada», «decisão» onde a grelha da m9-u2 dizia «tese», e a frase do que não conta para as palavras);
- as páginas: tarefas/m9-u1/ e tarefas/m9-u2/ (enunciado, grelha/ e correcao/);
- as páginas do módulo que falam da aula de tarefa: m9/guia-da-tarefa-m9/ (10 minutos de leitura e 55 de produção em vez de 5 e 60,
  no texto e nos quatro blocos; «plano» em vez de «núcleo»; a frase do que não conta para as palavras; sem a «Autoavaliação» que se
  copiava para o Teams e sem «pergunta ao teu par de trabalho»: a regra passa a chamar-se «Dois antes de mim»),
  m9/portefolio-do-modulo-m9/ (saem «autoavaliação /20» e «trabalho de equipa», sem nada no lugar; «plano» e «duas linhas finais»
  onde dizia «núcleo» e «duas linhas»; 15/11/2026, revisão: «duas linhas finais» onde dizia «síntese», três vezes), m9/index.html
  («tema A ou B, plano, texto» onde dizia «planificação, tema A ou B», três vezes; 15/11/2026, revisão: «as duas linhas finais
  fazem parte da entrega» onde dizia «a síntese integra a produção» e «com a síntese integrada») e m9/mapa-do-modulo-m9/ («As duas
  linhas finais fazem parte da entrega» onde dizia «A síntese faz parte da entrega»): nenhuma das quatro páginas diz «síntese»;
- ACERTO DO M2: m2/guia-da-tarefa-m2/ (só as frases do guia, como nos guias do M3 ao M8: sai o bloco «Autoavaliação» que se copiava
  para o Teams, com o código e o texto copiado que lhe pertencem; sai «pergunta ao teu par de trabalho»; a regra passa a «Dois antes
  de mim», com dois passos, também nos dois blocos que a nomeiam; os tempos e as tarefas do M2 não mudam);
- ACERTO DO M7: m7/index.html («No fim, defendes uma opinião com um verso de Mensagem», onde dizia «tese»: a m7-u3 diz «opinião» em
  todo o lado).
- 15/11/2026, A EDIÇÃO DA TURMA NÃO EXISTE (decisão do docente): o romance e o conto leem-se no livro. Sai «edição da turma» de todo o
  sítio, com frases que tratam o aluno por «tu»: nos dados e nos enunciados da m9-u1 e da m9-u2 («lê os capítulos I e V de
  <i>Memorial do Convento</i>, no livro»; «Lê o episódio no livro» e «Lê o capítulo no livro», como dizem as lições F14 e F15; «Lê a
  passagem no livro.»; «o excerto da Porto Editora ou o livro»; «O romance não está nesta página: lê-o no livro.»), nas lições do M9
  que as tarefas citam letra a letra (m9/licao-m9-f14/, m9/licao-m9-f15/ e m9/licao-m9-f16/, no JSON dos cartões: «Lê o episódio no
  livro», «A leitura integral do capítulo faz-se no livro», «Lê o capítulo no livro.», «lê a passagem no livro.»), na página da obra
  (obras/memorial/: «Ainda não identificámos o capítulo e a página do excerto no livro.») e na lição e no painel da F16 do M8, que
  são de um conto (m8/licao-m8-f16/ e m8/painel-m8-f16/: «O resto do conto lê-se no livro.» e, nos dois, com o mesmo texto, «Que
  pergunta permite prosseguir a leitura do conto?»). Estas páginas estavam congeladas: as trocas entram nesta camada, que ainda não
  está no main; as camadas já publicadas não mudam.

Os aquecimentos da m9-u1 e da m9-u2 (dados e páginas) não mudam: já diziam «Dez minutos», não falam do núcleo nem dos 60 minutos, e
os seus casos inventados (o diretor que inaugura a biblioteca; a exposição escolar) são os que os exemplos do enunciado novo usam.

DIREITOS DE AUTOR (decisão do docente para todo o M9): <i>Memorial do Convento</i> ainda tem direitos de autor (José Saramago morre em
2010: o mapa do módulo M9 diz «Azinhaga, 1922–Lanzarote, 2010»; nenhuma lição do M9 dá o ano) e não se copia para a página. Os
excertos longos das lições F01, F02 e F05 ficam nas lições e não se copiam. Cada passagem tem um bloco «Onde está o texto» com as
citações curtas que as lições do M9 já publicam, letra a letra, e a linha de fonte, sem número de página. As lições do M9 dizem «na
edição da turma» ou «no livro», nunca «no manual»: a página diz o mesmo e o cartão da lição que diz onde ler. 15/11/2026: a edição
da turma não existe (decisão do docente); as lições e a página dizem «no livro».
- m9-u1, Texto 1, capítulo I (a miniatura): nenhuma lição cita a passagem; a lição F14 («Lê de perto») dá um resumo e manda ler o
  episódio no livro;
- m9-u1, Texto 2, capítulo V (o primeiro auto de fé): «a descansada leitura das sentenças» (lição F15, «Lê de perto»);
- m9-u2, Texto 1, os nomes dos trabalhadores: a citação do cartão 16 da lição F05; o excerto fica no cartão «O texto, 1 de 3»;
- m9-u2, Texto 2, capítulo XIX (Francisco Marques): «está a fazer bem o trabalho» (lição F16, «Lê de perto») e a citação da viúva
  (lição F05, cartão 24);
- m9-u2, Texto 3, Blimunda: «por obra também dos olhos de Blimunda» (lição F02, cartão 22); a lição F11 aponta os capítulos XVI e XXV;
- m9-u2, Texto 4, Scarlatti: nenhuma lição cita a passagem nem diz o capítulo; a lição F12 diz como a procurar no livro.
Nada veio de fora das lições e não há imagens.

Decisões do docente (as mesmas do M3 ao M8): «com consulta» quer dizer lições do site, caderno e dicionário, e diz-se uma vez, no
primeiro cartão; tempos 10 (aquecimento), 10 (leitura), 55 (produção) e 15 (revisão e entrega), 90 no total; as passagens citadas
ou copiadas não contam para as palavras (a mesma frase no enunciado, na grelha e no guia); a autoavaliação da grelha é só para o aluno
e não se entrega; o aquecimento é o primeiro passo, com uma só ligação; quando o enunciado troca uma palavra por outra mais simples, a
grelha, a correção, o guia, o índice e o mapa usam a mesma; o apoio (exemplos com outro caso) fica em desdobrável fechado no ecrã e não
sai em papel; a verificação final tem no máximo 10 perguntas de sim ou não.

Os exemplos (regra do docente: sempre com outro caso, sem frases dos textos da tarefa, sem dar feita nenhuma alínea, sem repetir
respostas do aquecimento): na m9-u1, o caso inventado do aquecimento (o diretor que elogia o silêncio); na m9-u2, o caso inventado do
aquecimento (a exposição escolar), com uma decisão que não é a do aquecimento (as fotografias lado a lado, não as datas).
15/11/2026 (revisão): os exemplos da m9-u1 diziam, por outras palavras, o que o aquecimento ensina (a solenidade que se perde, o
ruído por cima da fala, o que o diretor pensa) e escolhiam a fita como pormenor, que o aquecimento diz que não serve de indício.
Agora a opinião é outra (a cena tem graça: a biblioteca abre com uma máquina de obras atrás do diretor), os pormenores são
«inaugura a biblioteca» e «uma máquina de obras», e o procedimento é a ordem das frases (a máquina só aparece na segunda), que o
aquecimento não trabalha. Na m9-u2, a linha «O teu texto» do cartão «Se precisares de rever» usa as palavras do enunciado
(«objeção», «resposta») e diz as da lição F10 entre parênteses.

O molde não ganhou chaves: as páginas do M9 usam as do M8 (scripts/tarefa_facil.py) e a folha assets/task-textos.css na versão
facil-12. As páginas dos outros módulos saem iguais, byte a byte.

O que NÃO muda: as outras tarefas, as suas grelhas, correções e aquecimentos (saem dos mesmos geradores, iguais byte a byte); os
critérios, os níveis, os exemplos e os pontos das grelhas da m9-u1 e da m9-u2 (as trocas de palavras fazem-se só ao escrever as
páginas); os aquecimentos do M9; as lições (15/11/2026: só as frases da edição da turma, nas F14, F15 e F16 do M9 e na F16 do M8);
as tarefas e os tempos do M2.

O script tira as trocas da diferença entre a base (cada ficheiro com esta camada desfeita pelo manifesto; antes de haver manifesto,
o ficheiro no commit de base, lido com git) e a árvore: pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.
Para mudar uma página ou os dados por baixo desta camada: muda-se a árvore, voltam a gerar-se as páginas e corre-se «python3
scripts/tarefas_faceis_m9_20261114.py --base-do-commit» (a base lê-se do commit de base, porque o manifesto antigo já não confere), e
depois scripts/aplicar_trocas.py, que reescreve o manifesto. Confere, antes de escrever: que os geradores, com os dados da árvore,
dão as páginas da árvore e, com os dados da base, as páginas da base (as seis: enunciado, grelha e versão de correção de cada
tarefa); e cada ficheiro como scripts/aplicar_trocas.py o vai conferir (da base para o resultado e de volta, letra a letra).

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

CAMADA = ROOT / 'scripts/tarefas_faceis_m9_20261114.json'
MANIFESTO = ROOT / 'tests/fixtures/tarefas-faceis-m9-edits-20261114.json'
BASE_COMMIT = '85c4b50420a00513d252a9da09e4901a4c3f4a49'
NBSP = '\xa0'
SLUGS = ('m9-u1', 'm9-u2')

DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
DADOS_GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
FICHEIROS_DADOS = DADOS_TAREFAS + [DADOS_GRELHAS]
# As páginas que saem dos geradores: com os dados da base dão a página da base; com os da árvore, a da árvore.
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'correcao/')]
GUIA, PORTEFOLIO = 'm9/guia-da-tarefa-m9/index.html', 'm9/portefolio-do-modulo-m9/index.html'
INDICE, MAPA = 'm9/index.html', 'm9/mapa-do-modulo-m9/index.html'
# 14/11/2026: os dois acertos (o guia da tarefa do M2 e o índice do M7).
GUIA_M2, INDICE_M7 = 'm2/guia-da-tarefa-m2/index.html', 'm7/index.html'
MODULO = [GUIA, PORTEFOLIO, INDICE, MAPA, GUIA_M2, INDICE_M7]
# 15/11/2026: a edição da turma não existe (decisão do docente); lê-se no livro. As lições do M9 que as tarefas citam, a página da
# obra e a lição e o painel da F16 do M8 (um conto).
LICOES_M9 = [f'm9/licao-m9-f{n}/index.html' for n in ('14', '15', '16')]
OBRA = 'obras/memorial/index.html'
CONTO_M8 = ['m8/licao-m8-f16/index.html', 'm8/painel-m8-f16/index.html']
LIVRO = LICOES_M9 + [OBRA] + CONTO_M8
FICHEIROS = FICHEIROS_DADOS + PAGINAS + MODULO + LIVRO

ACHADOS = {
    'facil': 'O molde «mais fácil de fazer», aprovado pelo docente no M3, chega ao M9: a mesma tarefa, com um pedido por alínea, os '
             'exemplos com outro caso em desdobrável, o primeiro cartão com o que se faz, o que se entrega e o quadro 10/10/55/15, e a '
             'verificação em perguntas de sim ou não.',
    'direitos': 'Decisão do docente para o M9: <i>Memorial do Convento</i> ainda tem direitos de autor e não se copia; cada passagem tem '
                'um bloco «Onde está o texto», só com as citações curtas que as lições do M9 já publicam, letra a letra, e a remissão '
                'para o livro ou para o cartão da lição que diz onde a ler, sem número de página.',
    'junto': '«Tudo junto» (decisão do docente): as mesmas palavras do enunciado novo («plano» em vez de «núcleo» e de «planificação»; '
             '«duas linhas finais» em vez de «síntese»; «a letra do tema»; «a edição que usaste (a editora e o ano)» em vez de «a '
             'edição consultada»; «decisão» em vez de «tese»; a mesma frase do que não conta para as palavras).',
    'tempos': 'Tempos decididos pelo docente: 10 minutos de aquecimento, 10 de leitura, 55 de produção e 15 de revisão e entrega, '
              'iguais em todos os sítios onde aparecem.',
    'auto': 'Decisão do docente: a autoavaliação da grelha é só para o aluno e não se entrega; a versão de correção fica com a nota e '
            'o comentário do docente.',
    'sem_auto': 'Decisão do docente: no guia da tarefa, a «Autoavaliação» que se copiava para o Teams sai, porque a autoavaliação é '
                'só para o aluno e não se entrega; o plano, as notas e a lista de verificação continuam a copiar-se.',
    'sem_par': 'Decisão do docente: não há trabalho de grupo nem de pares; a regra fica com os dois primeiros passos («Dois antes de '
               'mim»).',
    'sem_equipa': 'Decisão do docente: não há trabalho de grupo nem de pares, e a autoavaliação não se entrega; no portefólio do '
                  'módulo saem «trabalho de equipa» e «autoavaliação /20», sem nada no lugar.',
    'acerto_m2': 'Acerto do M2 (decisão do docente, 14/11/2026): o guia da tarefa do M2 fica como os do M3 ao M9; só mudam estas '
                 'frases do guia, não as tarefas nem os tempos do M2.',
    'acerto_m7': 'Acerto do M7 (decisão do docente, 14/11/2026): «opinião» em vez de «tese», como a m7-u3 diz em todo o lado.',
    'livro': '15/11/2026: a edição da turma não existe (decisão do docente); lê-se no livro. Sai «edição da turma» de todo o sítio, '
             'com frases que tratam o aluno por «tu».',
}


def ler(rel):
    # 15/11/2026: por cima desta camada fica a da tarefa m4-u2 com «Tema A ou B» e o acerto do M8 (tarefa_m4u2_tema_b_20261115), que
    # também muda os dados das grelhas: desfaz-se primeiro, com contagem estrita, quando o ficheiro a traz (a «árvore» desta camada é o
    # ficheiro como ela o deixou).
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    m4u2 = ROOT / 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json'
    if m4u2.is_file():
        for e in reversed(json.loads(m4u2.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: a tarefa m4-u2 com «Tema A ou B» já não confere ({e["location"]})')
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
    """As páginas que os geradores dão com estes dados ({ficheiro de dados: texto}), numa pasta temporária: o enunciado, a grelha e a
    versão de correção de cada uma das duas tarefas."""
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
            'for s in ("m9-u1", "m9-u2"):\n'
            '    d = json.loads((te.DADOS / (s + ".json")).read_text("utf-8")); te.tarefa(d, s in grelhas, tmp / "saida")\n'
            '    t = grelhas[s]\n'
            '    for pasta in ("grelha", "correcao"):\n'
            '        html = gt.pagina_aluno(s, t) if pasta == "grelha" else gt.pagina_correcao(s, t)\n'
            '        p = tmp / "saida/tarefas" / s / pasta / "index.html"; p.parent.mkdir(parents=True, exist_ok=True)\n'
            '        p.write_text(html, "utf-8", newline="\\n")\n')
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
    # 15/11/2026: os ficheiros da edição da turma.
    if rel in LICOES_M9:
        return f'Lição F{rel.split("-f")[1][:2]} do M9'
    if rel == OBRA:
        return 'Página da obra Memorial do Convento'
    if rel in CONTO_M8:
        return ('Lição' if '/licao-' in rel else 'Painel') + ' F16 do M8'
    m = re.search(r'm(\d)-u(\d)', rel)
    u = f'M{m.group(1)}-U{m.group(2)}' if m else 'M9'
    if rel in DADOS_TAREFAS:
        return f'Tarefa da {u}, os dados do enunciado'
    if rel == DADOS_GRELHAS:
        return 'Grelhas das tarefas (M9-U1 e M9-U2), os dados'
    if rel == INDICE:
        return 'Índice do M9'
    if rel == INDICE_M7:
        return 'Índice do M7'
    if rel == GUIA_M2:
        return 'Guia da tarefa do M2'
    if rel == MAPA:
        return 'Mapa do módulo M9'
    if rel == GUIA:
        return 'Guia da tarefa do M9'
    if rel == PORTEFOLIO:
        return 'Portefólio do módulo M9'
    return {'grelha': f'Grelha do aluno da {u}', 'correcao': f'Versão de correção da {u}'}.get(rel.split('/')[2], f'Enunciado da {u}')


def categorias(rel, antigo, novo):
    cs = set()
    if rel in LIVRO:
        return ['livro']
    if rel in (INDICE, MAPA):
        return ['junto']
    if rel == INDICE_M7:
        return ['acerto_m7']
    if rel == GUIA_M2:
        return [c for c in ACHADOS if c in {'acerto_m2', 'sem_auto', 'sem_par'}]
    if rel in DADOS_TAREFAS or rel in ('tarefas/m9-u1/index.html', 'tarefas/m9-u2/index.html'):
        cs |= {'facil', 'direitos', 'tempos', 'junto', 'auto'}
        if 'edição da turma' in antigo:
            cs.add('livro')
    elif rel == DADOS_GRELHAS or '/grelha/' in rel or '/correcao/' in rel:
        if 'autoavalia' in novo or 'Aluno</th>' in antigo or 'Diferença entre' in antigo or '<td></td><td></td><td></td>' in antigo:
            cs.add('auto')
        if 'trocas_aluno' in novo or not cs:
            cs.add('junto')
    elif rel == GUIA:
        if 'Autoavaliação' in antigo or 'AUTOAVALIAÇÃO' in antigo or 'autoavaliação' in antigo or 'dataset.auto' in antigo or 'r-auto' in antigo:
            cs.add('sem_auto')
        if 'par de trabalho' in antigo:
            cs.add('sem_par')
        if re.search(r'(5|60|10|55)(' + NBSP + r'| )min|BLOCOS|\[5, |\[60, ', antigo + novo):
            cs.add('tempos')
        if 'núcleo' in antigo or 'Não contam para as palavras' in novo or not cs:
            cs.add('junto')
    elif rel == PORTEFOLIO:
        if 'trabalho de equipa' in antigo or 'autoavaliação' in antigo:
            cs.add('sem_equipa')
        if 'núcleo' in antigo or 'síntese' in antigo or not cs:
            cs.add('junto')
    assert cs, rel
    return [c for c in ACHADOS if c in cs]


def trocas_do_ficheiro(rel, a, b):
    trocas = []
    for antigo, novo in trocas_do_texto(a, b):
        trecho = _visivel(novo)
        trecho = trecho if len(trecho) <= 90 else trecho[:88].rstrip() + '…'
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}: «{trecho}»', 'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
                       'achado': ('' if rel in LIVRO else '14/11/2026: ') + ' '.join(ACHADOS[c] for c in categorias(rel, antigo, novo))})
    return trocas


def construir():
    """Devolve (trocas, {ficheiro: (base, final)})."""
    finais = {rel: (base(rel), ler(rel)) for rel in FICHEIROS}
    if all(a == b for a, b in finais.values()):
        raise SystemExit('a camada não está aplicada nesta árvore: aplica-a com scripts/aplicar_trocas.py e o JSON que já existe')
    # Os geradores dão as páginas da árvore com os dados da árvore, e as da base com os dados da base.
    for k, quando in ((1, 'da árvore'), (0, 'da base')):
        geradas = gerar_com({rel: finais[rel][k] for rel in FICHEIROS_DADOS})
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
