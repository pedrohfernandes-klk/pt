"""12/11/2026: as duas tarefas do M3 (m3-u1 e m3-u2) «mais fáceis de fazer» e «tudo junto» no M3 (camada tarefas_faceis_m3_20261112).

Pedido do docente: «as tarefas são para manter, mas é para ser mais fácil de fazer»; «os textos estudados têm de aparecer completos
para análise». O piloto na m3-u1 foi aprovado a 12/11/2026. O que este ficheiro fixa:

* a tarefa pede o mesmo: os títulos, os nomes e as letras dos temas, o total de palavras e a orientação de cada parte, as
  passagens e as expressões que o enunciado de antes citava, o dossiê e a pergunta opcional, e os critérios, níveis, exemplos e
  pontos da grelha, iguais aos de antes da camada (a base do manifesto, que é o main 1471a61a);
* os textos para análise são os das lições do M3, letra a letra (versos, estrofes, vocabulário e linha de fonte), e a página
  mostra-os inteiros e pela ordem, junto da pergunta ou do tema que os usa;
* as decisões do docente, em todos os sítios: tempos 10/10/55/15 (quadro, relógios, guia), nenhum «5 min» nem «60 min» antigos
  nas páginas do M3 ligadas à tarefa; «com consulta» dito uma vez, no primeiro cartão; os versos citados ou copiados não contam;
  a autoavaliação da grelha não se entrega (enunciado, grelha e correção); o aquecimento com uma só ligação; no máximo 10 perguntas
  de sim ou não na verificação; as mesmas palavras no enunciado, na grelha, na correção, no aquecimento, no guia, no índice e no
  mapa;
* a decisão do docente de 13/11/2026, no guia da tarefa do M3: a «Autoavaliação» que se copiava para o Teams e «pergunta ao teu
  par de trabalho» saíram, e o resto do guia é o do main de partida, letra a letra, salvo as trocas da camada;
* as regras do texto: sem as palavras proibidas, sem «·» nem «—» nas nossas frases, «Que + nome» ou «Qual das…», referências que
  não se partem, exemplos com outro caso (nunca as passagens reservadas da tarefa);
* o contrato da página, que substitui o de tests/test_task_choice.py nestas duas tarefas: seis cartões com nome, dois temas, uma
  pergunta opcional com três opções, os dois relógios, os factos do dossiê com fonte e ligação que existe, as citações e os
  números de cada facto na lição para onde aponta, os nomes das secções tal como estão nas lições ligadas;
* as outras onze tarefas geradas não mudam: não estão na camada, não usam o molde novo e saem iguais dos geradores;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base, gerador que dá o mesmo JSON, registada na
  auditoria (desfazer), em scripts/desligar_sala.py, na leitura histórica dos enunciados e nas cadeias e caminhos dos fluxos.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em
tests/browser_tarefas_faceis_m3.py."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import html
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'scripts'))
from auditoria_20261028 import undo_tarefas_faceis_m3_1112, undo_exame_provas_oficial_1112, undo_tarefas_faceis_m1_1113  # noqa: E402
import verificar_camadas  # noqa: E402

CAMADA_REL = 'scripts/tarefas_faceis_m3_20261112.json'
MANIFESTO_REL = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
PO = 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
# 13/11/2026: por cima desta camada ficam as duas tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113, o mesmo molde), que
# se desfazem primeiro em todas as cadeias e partilham com ela um ficheiro, os dados das grelhas.
M1 = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
BASE_COMMIT = '1471a61ab0a539719943074153f9e9647ba48e35'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
TROCAS = json.loads((ROOT / CAMADA_REL).read_text('utf-8'))
SLUGS = ('m3-u1', 'm3-u2')
N = '\xa0'
DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
DADOS_AQUECIMENTOS = [f'docs/pedagogia/aquecimentos/{s}.json' for s in SLUGS]
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'aquecimento/', 'correcao/')]
GUIA, INDICE, MAPA = 'm3/guia-da-tarefa-m3/index.html', 'm3/index.html', 'm3/mapa-do-modulo-m3/index.html'
FICHEIROS = DADOS_TAREFAS + [GRELHAS] + DADOS_AQUECIMENTOS + PAGINAS + [GUIA, INDICE, MAPA]
# As outras tarefas que saem de scripts/tarefas_escolha.py.
# 13/11/2026: eram onze. A m1-u1 e a m1-u2 passaram ao mesmo molde (camada tarefas_faceis_m1_20261113), com o seu teste
# (tests/test_tarefas_faceis_m1.py, que exige delas o mesmo que este exige das do M3); as que não usam o molde são agora nove, e a
# exigência sobre elas é a mesma. As treze páginas continuam a sair dos geradores, byte a byte.
OUTRAS = ('m5-u1', 'm5-u2', 'm6-u1', 'm6-u2', 'm7-u3', 'm8-u1', 'm8-u2', 'm9-u1', 'm9-u2')
NO_MOLDE_M1 = ('m1-u1', 'm1-u2')
# O que cada tarefa pede, em números (iguais aos do enunciado de antes): total, orientação das perguntas e do tema.
NUMEROS = {'m3-u1': ('200 a 240', 'cerca de 60', '80 a 120'), 'm3-u2': ('200 a 250', '110', '90 a 140')}
# As lições de onde vem cada texto (a «origem» de cada bloco nos dados tem de ser esta).
ORIGENS = {
    'm3-u1': {'texto-1': ('m3/licao-m3-f02/index.html', 24), 'texto-2': ('m3/licao-m3-f05/index.html', 17),
              'texto-3': ('m3/licao-m3-f09/index.html', 14), 'texto-4': ('m3/licao-m3-f03/index.html', 16)},
    'm3-u2': {'texto-1': ('m3/licao-m3-f10/index.html', 24), 'texto-2': ('m3/licao-m3-f13/index.html', 32),
              'texto-3': ('m3/licao-m3-f03/index.html', 16)},
}
CARTOES_NOMES = ['Começar', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Fechar e entregar', 'Rever a matéria']


def ler(rel):
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 13/11/2026: os dados das grelhas levam agora por cima a camada das tarefas do M1 (duas chaves novas nas grelhas do M1). Este
    # teste lê-os como a camada do M3 os deixou: com a do M1 desfeita pela auditoria, com contagem estrita. Nos outros quinze ficheiros
    # a árvore é o «after» desta camada, como antes.
    if rel == GRELHAS:
        texto = undo_tarefas_faceis_m1_1113(rel, texto)
    return texto


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def antes(rel):
    """O ficheiro como estava por baixo desta camada (desfeita pelo manifesto, com contagem estrita): o main de partida."""
    texto = ler(rel)
    for e in reversed(MANIFESTO['files'].get(rel, {}).get('edits', [])):
        assert texto.count(e['new']) == e['occurrences'], (rel, e['location'])
        texto = texto.replace(e['new'], e['old'])
    return texto


def visivel(fonte, so_main=True, sem_nav=True):
    """O texto que se lê numa página: sem scripts, estilos nem etiquetas, com os espaços normais juntos (U+00A0 fica)."""
    if so_main and '<main' in fonte:
        fonte = fonte[fonte.index('<main'):fonte.index('</main>')]
    fonte = re.sub(r'<(script|style)\b.*?</\1>', ' ', fonte, flags=re.S)
    if sem_nav:
        fonte = re.sub(r'<nav\b.*?</nav>', ' ', fonte, flags=re.S)
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fonte))).strip()


def solto(texto):
    return texto.replace(N, ' ')


def cartoes(rel):
    """Os cartões de uma lição (CARTOES=[…], numa só linha do ficheiro)."""
    fonte = ler(rel)
    i = fonte.index('CARTOES=[')
    return json.JSONDecoder().raw_decode(fonte[i + 8:])[0]


def da_licao(rel, numeros):
    """Os versos (por estrofe, com os rótulos «Mote» e «Voltas» à parte), o vocabulário e a linha de fonte dos cartões «O texto» de uma
    lição, tal como lá estão: (estrofes, vocabulário, fonte)."""
    arr = cartoes(rel)
    linhas, gloss, fonte = [], [], None
    for k in numeros:
        c = arr[k - 1]
        assert c['t'] == 'ler' and c['rot'].startswith('O texto, '), (rel, k)
        v = re.search(r'<p class="v">(.*?)</p>', c['html'], re.S).group(1)
        for m in re.finditer(r'<span class="ln" data-l="\d+-(\d+)"><span class="n">\d*</span>(.*?)</span>(?=\n|$)', v, re.S):
            linhas.append((int(m.group(1)), html.unescape(re.sub(r'<[^>]+>', '', m.group(2)))))
        g = re.search(r'<p class="gl"><b>Vocabulário:</b> (.*?)</p>', c['html'], re.S)
        if g:
            gloss += [re.fullmatch(r'<b>(.*)</b>, (.*?)', item, re.S).groups() for item in g.group(1).split('; ')]
        f = re.search(r'<p class="fonte">(.*?)</p>', c['html'], re.S)
        if f:
            fonte = re.sub(r'_([^_]+)_', r'<i>\1</i>', f.group(1))
    estrofes, anterior = [], None
    for i, t in linhas:
        if t in ('Mote', 'Voltas'):
            estrofes.append({'rotulo': t, 'versos': []})
        else:
            if not estrofes or (anterior is not None and i != anterior + 1 and estrofes[-1]['versos']):
                estrofes.append({'rotulo': None, 'versos': []})
            estrofes[-1]['versos'].append(t)
        anterior = i
    return estrofes, [list(x) for x in gloss], fonte


class Pagina(HTMLParser):
    """A estrutura de uma página de tarefa: os filhos de <main>, os temas, as perguntas com opções e as ligações."""

    def __init__(self, fonte):
        super().__init__()
        self.pilha, self.raiz, self.ids, self.ligacoes, self.temas, self.perguntas, self.opcoes = [], [], [], [], [], [], []
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.pilha and self.pilha[-1][0] == 'main':
            self.raiz.append((tag, a.get('id'), a.get('data-task-card-name')))
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a':
            self.ligacoes.append(a.get('href', ''))
        if 'data-task-theme' in a:
            self.temas.append(a['data-task-theme'])
        if 'data-task-question' in a:
            self.perguntas.append((a['data-task-question'], any(x[0] == 'details' for x in self.pilha)))
        if tag == 'button' and 'data-response' in a:
            self.opcoes.append(a)
        if tag not in ('meta', 'link', 'br', 'img', 'input'):
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        if any(x[0] == tag for x in self.pilha):
            self.pilha = self.pilha[:max(i for i, x in enumerate(self.pilha) if x[0] == tag)]


def plana(rel):
    """Texto de uma página do sítio, sem marcas nem entidades, com os espaços juntos (como tests/test_task_choice.py)."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', ler(rel))))


class TarefasFaceisM3(unittest.TestCase):
    maxDiff = None

    # ---------- a tarefa pede o mesmo ----------

    def test_a_tarefa_pede_o_mesmo(self):
        for slug in SLUGS:
            rel = f'docs/pedagogia/tarefas-escolha/{slug}.json'
            d, a = json.loads(ler(rel)), json.loads(antes(rel))
            f = d['facil']
            with self.subTest(tarefa=slug):
                # As chaves de antes ficam todas, iguais: a camada só acrescenta «facil».
                self.assertNotIn('facil', a)
                self.assertEqual({k: v for k, v in d.items() if k != 'facil'}, a)
                self.assertEqual(list(d)[-1], 'facil')
                # O título, os títulos das duas perguntas, as letras e os nomes dos dois temas.
                self.assertEqual(d['titulo'], a['titulo'])
                self.assertEqual([p['titulo'] for p in f['perguntas']], [re.match(r'<strong>(.*?)</strong>', n).group(1) for n in a['nucleo']])
                self.assertEqual([(t['letra'], t['nome']) for t in f['temas']], [(t['letra'], t['nome']) for t in a['temas']])
                self.assertEqual(len(f['perguntas']), 2)
                # Os números: o total e a orientação de cada parte, os do «lead» de antes.
                total, perguntas, tema = NUMEROS[slug]
                lead = solto(a['lead'])
                self.assertIn(f'<strong>{total} palavras no total</strong>', lead)
                self.assertIn(perguntas, lead)
                self.assertIn(f'{tema} no tema', lead)
                quadro = f['quadro']['linhas']
                self.assertEqual(solto(quadro[-1][2]), total)
                self.assertEqual(solto(quadro[4][2]), f'orientação: {tema}')
                self.assertIn(perguntas, solto(quadro[2][2]['t'] if isinstance(quadro[2][2], dict) else quadro[2][2]))
                self.assertEqual(solto(f['temas_nota']), f'Orientação: {tema} palavras.')
                self.assertIn(f'Tenho {total} palavras?', [solto(x) for x in f['verificar']])
                # Tudo o que o enunciado de antes citava entre «» ou localizava por canto e estância continua pedido.
                # (os poemas e as estâncias que o enunciado de antes nomeava são agora os textos numerados: conta o título e a fonte de cada um)
                pedido = solto(json.dumps([f['perguntas'], f['temas'], f['finais'], [(t['titulo'], t['fonte']) for t in f['textos']]], ensure_ascii=False))
                velho = solto(' '.join(a['nucleo'] + [t['texto'] for t in a['temas']]))
                for citado in re.findall(r'«([^»]+)»', velho):
                    # (o soneto «Alma minha gentil» vem agora com o primeiro verso inteiro no título: confere-se o princípio da citação)
                    self.assertIn(f'«{citado}', pedido, citado)
                for ref in re.findall(r'\b[IVX]+, \d+(?: (?:a|e|ou) \d+)?', velho):
                    self.assertIn(ref, pedido, ref)
                # A pergunta das duas linhas finais é a de antes.
                pergunta = re.search(r'palavras: (.*?\?)', a['fecho']).group(1)
                self.assertIn(pergunta[0].upper() + pergunta[1:], re.sub(r'^Responde: (.)', lambda m: m.group(1).upper(), f['finais']['passos'][0]))
                # O dossiê e a pergunta opcional são os de antes (a página lê-os das chaves antigas).
                self.assertEqual(d['dossie'], a['dossie'])
                self.assertEqual(d['opcional'], a['opcional'])

    def test_criterios_da_grelha_iguais(self):
        agora, base = json.loads(ler(GRELHAS))['tarefas'], json.loads(antes(GRELHAS))['tarefas']
        self.assertEqual(list(agora), list(base))
        for slug, t in agora.items():
            with self.subTest(grelha=slug):
                novas = {'autoavaliacao_so_tua', 'trocas_aluno'} if slug in SLUGS else set()
                self.assertEqual(set(t) - set(base[slug]), novas)
                self.assertEqual({k: v for k, v in t.items() if k not in novas}, base[slug])
                self.assertEqual(sum(c['max'] for c in t['criterios']), 20)
        for slug in SLUGS:
            t = agora[slug]
            self.assertIs(t['autoavaliacao_so_tua'], True)
            # As trocas são só as palavras que o enunciado novo trocou; cada uma ocorre nos textos da grelha.
            antigos = [a for a, _ in t['trocas_aluno']]
            self.assertEqual(antigos[:5], ['Núcleo comum (duas respostas) e um tema à escolha (A ou B)', 'Respostas articuladas', 'o tema no topo',
                                           'o tema escolhido está no topo', 'Não escrever no topo o tema escolhido (A ou B).'])
            self.assertEqual(antigos[5], 'mais duas linhas finais que não contam para as palavras.')
            # 13/11/2026: o enunciado diz «Duas linhas finais» e já não diz «Fecho»; a grelha do aluno usa a mesma palavra nos exemplos e
            # em «Custa pontos» (achado de uma revisão; «tudo junto»). Passam a ser oito trocas, e as duas novas são estas, exatas.
            self.assertEqual(t['trocas_aluno'][6:], [['Fecho: ', 'Duas linhas finais: '],
                                                     ['Fecho genérico, sem verso.', 'Duas linhas finais genéricas, sem verso.']])
            self.assertEqual(len(antigos), 8)
            grelha = visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False, sem_nav=False)
            self.assertNotRegex(grelha, r'[Ff]echo')
            self.assertEqual(grelha.count('Duas linhas finais: '), 2)
            self.assertEqual(grelha.count('Duas linhas finais genéricas, sem verso.'), 1)
            self.assertNotRegex(visivel(ler(f'tarefas/{slug}/index.html')), r'[Ff]echo')
            fonte = json.dumps({k: v for k, v in t.items() if k != 'trocas_aluno'}, ensure_ascii=False)
            for a in antigos:
                self.assertIn(a, fonte)

    # ---------- os textos são os das lições, letra a letra ----------

    def test_textos_letra_a_letra_das_licoes(self):
        for slug in SLUGS:
            f = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))['facil']
            pagina = ler(f'tarefas/{slug}/index.html')
            self.assertEqual([t['id'] for t in f['textos']], list(ORIGENS[slug]))
            for t in f['textos']:
                rel, n_versos = ORIGENS[slug][t['id']]
                with self.subTest(tarefa=slug, texto=t['id']):
                    m = re.fullmatch(re.escape(rel) + r', linha \d+, cartões ([\d, ]+) \(copiado letra a letra\)', t['origem'])
                    self.assertIsNotNone(m, t['origem'])
                    estrofes, gloss, fonte = da_licao(rel, [int(x) for x in m.group(1).split(', ')])
                    # Os versos, estrofe a estrofe; os rótulos «Mote» e «Voltas» são os da lição (os outros dizem o canto e a estância).
                    self.assertEqual([e['versos'] for e in t['estrofes']], [e['versos'] for e in estrofes])
                    self.assertEqual(sum(len(e['versos']) for e in t['estrofes']), n_versos)
                    for e, l in zip(t['estrofes'], estrofes):
                        if l['rotulo']:
                            self.assertEqual(e.get('rotulo'), l['rotulo'])
                        elif e.get('rotulo'):
                            self.assertRegex(solto(e['rotulo']), r'^Canto [IVX]+, estância \d+$')
                    self.assertEqual(t['glossario'], gloss)
                    self.assertEqual(t['fonte'], fonte)
                    # Na página, o texto está inteiro e contínuo, pela ordem, com os versos numerados de 5 em 5.
                    bloco = re.search(r'<section class="tt-texto[^"]*" id="' + t['id'] + r'".*?</section>', pagina, re.S).group(0)
                    versos = [html.unescape(v) for v in re.findall(r'<span class="tt-l">(.*?)</span></span>', bloco)]
                    self.assertEqual(versos, [v for e in estrofes for v in e['versos']])
                    numeros = re.findall(r'<span class="tt-n">(\d*)</span>', bloco)
                    self.assertEqual(numeros, [str(k) if k % 5 == 0 else '' for k in range(1, n_versos + 1)])
                    self.assertEqual(bloco.count('<p class="tt-estrofe">'), len(estrofes))
                    for palavra, sentido in gloss:
                        self.assertIn(f'<li><b>{palavra}</b>: {sentido}</li>', bloco)
                    self.assertIn(f'<p class="tt-fonte">{t["fonte"]}</p>', bloco)
                    self.assertEqual(pagina.count(f'id="{t["id"]}"'), 1)
            # Cada texto fica no cartão da pergunta ou do tema que o usa, uma só vez.
            usados = [i for p in f['perguntas'] for i in p['textos']] + [i for t in f['temas'] for i in t['material'].get('textos', [])]
            self.assertEqual(sorted(usados), sorted(ORIGENS[slug]))
        # O Kit de Patrícia Lino tem direitos: não se copia; diz-se onde está, sem número de página, com os seis nomes da lição F02.
        f1 = json.loads(ler(DADOS_TAREFAS[0]))['facil']
        kit = f1['perguntas'][0]['onde_esta']
        para_entender = next(c for c in cartoes('m3/licao-m3-f02/index.html') if c.get('rot') == 'Para entender')['html']
        nomes = re.findall(r'<li><b>(.*?):</b>', para_entender)
        self.assertEqual(len(nomes), 6)
        self.assertEqual([n.rstrip(';.') for n in kit['nomes']], nomes)
        self.assertEqual(kit['titulo'], 'Onde está o texto: o <i>Kit</i> de Patrícia Lino')
        self.assertIn('direitos de autor', kit['frases'][0])
        bloco = re.search(r'<section class="tt-onde" id="kit".*?</section>', ler('tarefas/m3-u1/index.html'), re.S).group(0)
        self.assertNotRegex(visivel(bloco, so_main=False), r'\bp(?:ág)?\.\s*\d|página\s+\d')
        # 13/11/2026: o tema B da m3-u2 pede dois argumentos do Velho, e o Velho fala de IV, 95 a 104 (dossiê). Das lições só vêm IV, 94
        # e 95 (lição F03): nenhuma lição do M3 tem as estâncias 96 a 104, e a edição modernizada em domínio público que se conferiu
        # contra a de 1572 tem gralhas. Por isso não se copiam: o tema diz o que o Texto 3 tem e que o resto da fala está no manual,
        # sem número de página (achado de uma revisão).
        f2 = json.loads(ler(DADOS_TAREFAS[1]))['facil']
        tema_b = f2['temas'][1]
        self.assertEqual(tema_b['antes'], [
            f'O Velho do Restelo de Camões está no <a href="#texto-3">Texto{N}3</a>.',
            f'O Texto{N}3 tem as estâncias{N}IV,{N}94{N}e{N}95, as mesmas das lições. O resto da fala do Velho (IV,{N}96{N}a{N}104) está no manual.'])
        u2 = ler('tarefas/m3-u2/index.html')
        for frase in tema_b['antes']:
            self.assertEqual(u2.count(f'<p class="tf-p tf-antes">{frase}</p>'), 1)
        self.assertEqual([e['rotulo'] for e in next(x for x in f2['textos'] if x['id'] == 'texto-3')['estrofes']],
                         [f'Canto{N}IV, estância{N}94', f'Canto{N}IV, estância{N}95'])
        for incipit in ('Dura inquietação', 'A que novos desastres', 'geração daquele insano', 'nesta gostosa', 'Ismaelita',
                        'Deixas criar', 'maldito o primeiro', 'filho de Jápeto', 'moço miserando'):
            self.assertNotIn(incipit, u2)
            for licao in sorted((ROOT / 'm3').glob('licao-m3-f*/index.html')):
                self.assertNotIn(incipit, licao.read_text('utf-8'), licao.parent.name)
        self.assertNotRegex(visivel(u2), r'manual[^.]*\bp(?:ág)?\.\s*\d|manual[^.]*página\s+\d')
        self.assertEqual(f2['rever_texto'], f'Os Textos{N}1, 2{N}e{N}3 já estão nesta página. As lições servem para rever a matéria.')
        self.assertEqual(u2.count(f'<p class="tf-p">{f2["rever_texto"]}</p>'), 1)
        # O quadro das modalidades da m3-u2 é o da lição F15, letra a letra.
        f2 = json.loads(ler(DADOS_TAREFAS[1]))['facil']
        apoio = f2['perguntas'][1]['apoios'][0]
        f15 = next(c for c in cartoes('m3/licao-m3-f15/index.html') if c.get('rot') == 'Para entender')['html']
        self.assertEqual(apoio['quadro']['colunas'], re.findall(r'<th scope="col" role="columnheader">(.*?)</th>', f15))
        self.assertEqual(apoio['quadro']['linhas'], [list(x) for x in re.findall(
            r'<tr role="row"><th scope="row" role="rowheader">(.*?)</th><td role="cell" data-label="[^"]*">(.*?)</td><td role="cell" data-label="[^"]*">(.*?)</td></tr>', f15)])
        self.assertEqual(len(apoio['quadro']['linhas']), 3)
        self.assertIn(f'</table><p>{apoio["notas"][0]}</p>', f15)
        paralelo = next(c for c in cartoes('m3/licao-m3-f15/index.html') if c.get('rot') == 'Em paralelo')['html']
        self.assertIn('<li>' + f2['perguntas'][1]['ajudas'][1].rstrip('.') + '</li>', paralelo)

    def test_exemplos_com_outro_caso(self):
        # Os exemplos mostram como se faz com outro caso: vêm da grelha pública (ou do exemplo que a página já tinha) e nunca usam as
        # passagens reservadas da tarefa (a lista «reservadas» do aquecimento).
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in SLUGS:
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            f = d['facil']
            reservadas = json.loads(ler(f'docs/pedagogia/aquecimentos/{slug}.json'))['reservadas']
            self.assertGreater(len(reservadas), 30)
            publico = solto(json.dumps(grelhas[slug], ensure_ascii=False) + json.dumps(d['exemplos'], ensure_ascii=False))
            exemplos = [x for p in f['perguntas'] for x in p['exemplos']] + [x for t in f['temas'] for x in t['material'].get('exemplos', [])]
            self.assertGreaterEqual(len(exemplos), 4)
            for x in exemplos:
                for p in x.get('paragrafos', []):
                    texto = p if isinstance(p, str) else p['t']
                    with self.subTest(tarefa=slug, exemplo=texto[:50]):
                        for r in reservadas:
                            self.assertNotIn(r, texto)
                        # 13/11/2026: «Passo» e «Alínea» ficam presos ao número ou à letra (U+00A0), como as outras referências.
                        if isinstance(p, dict):
                            self.assertRegex(p['al'], rf'^(?:Passos?|Alíneas?){N}')
                            self.assertNotRegex(p['al'], r'(?:Passos?|Alíneas?) |\d (?:a|e) \d|\) (?:a|e) [a-f]\)')
                        if slug == 'm3-u1' and isinstance(p, dict) and p['al'].startswith(f'Passo{N}4'):
                            # A única linha que não vem da grelha: um verso das voltas de «Perdigão perdeu a pena», da lição F05.
                            self.assertIn('</span>Subiu a um alto lugar,</span>', ler('m3/licao-m3-f05/index.html'))
                            continue
                        sem_marcas = solto(re.sub(r'</?i>', '_', texto))
                        # (um exemplo da m3-u2 começa a frase onde a grelha a continua: só muda a maiúscula inicial)
                        if sem_marcas.startswith('Em «Respondo'):
                            sem_marcas = 'e' + sem_marcas[1:]
                        self.assertIn(sem_marcas, publico)
            pagina = ler(f'tarefas/{slug}/index.html')
            # Em desdobrável fechado no ecrã, que não sai em papel.
            self.assertEqual(pagina.count('<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>'), len(f['perguntas']) + 2)
            self.assertEqual(len(re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>Ver (?:um exemplo com outro caso|dois exemplos com outros casos)</summary>', pagina)),
                             len(f['perguntas']) + 2)
            self.assertNotRegex(pagina, r'<details[^>]*tf-so-ecra[^>]* open')
        css = ler('assets/task-textos.css')
        impressao = css[css.index('@media print{'):]
        self.assertIn('[data-task-facil] .tf-so-ecra{display:none!important}', impressao)
        self.assertIn('[data-task-facil] .tt-texto{break-inside:avoid}', impressao)
        # 13/11/2026: em papel, o cabeçalho do cartão dos temas (título, orientação e «Escreve a letra do teu tema») não fica sozinho no
        # fundo de uma página (achado de uma revisão; tests/browser_tarefas_faceis_m3.py confere-o na impressão).
        self.assertIn('[data-task-facil] :is(h2,h3,h4,summary,.tt-rotulo,.tf-meta,.tf-antes,.tf-fig){break-after:avoid}', impressao)
        self.assertIn('[data-task-facil] .tf-topo{break-after:avoid}', impressao)
        self.assertIn('[data-task-facil] .tt-estrofe{margin:0 0 14px;max-width:none;break-inside:avoid}', css)

    # ---------- as decisões do docente, em todos os sítios ----------

    def test_tempos_10_10_55_15_em_todos_os_sitios(self):
        for slug in SLUGS:
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            f = d['facil']
            pagina = ler(f'tarefas/{slug}/index.html')
            with self.subTest(tarefa=slug):
                tempos = [solto(l[0]['t'] if isinstance(l[0], dict) else l[0]) for l in f['quadro']['linhas'] if l[0]]
                self.assertEqual(tempos, ['10 min', '10 min', '55 min', '15 min', '90 min'])
                self.assertEqual([solto(l[1]) for l in f['quadro']['linhas']],
                                 ['Aquecimento em cartões', 'Leitura do enunciado', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Revisão e entrega', 'Total'])
                self.assertEqual(f['quadro']['linhas'][2][0], {'t': f'55{N}min', 'linhas': 3})
                self.assertEqual(f['producao_minutos'], 55)
                self.assertEqual(d['aquecer']['minutos'], 10)
                # Na página: o quadro, e os dois relógios (10 e 55 minutos).
                quadro = re.search(r'<table class="tf-quadro">.*?</table>', pagina, re.S).group(0)
                self.assertEqual(re.findall(r'<th scope="row(?:group)?"(?: rowspan="3")?>(\d+)\xa0min</th>', quadro), ['10', '10', '55', '15', '90'])
                self.assertIn(f'<th scope="rowgroup" rowspan="3">55{N}min</th><td>Pergunta{N}1</td>', quadro)
                self.assertEqual(re.findall(r'data-relogio data-max="(\d+)" data-passo="(\d)" data-rotulo="([^"]+)" data-chave="pt-relogio:tarefas/' + slug + r':(\w+)"', pagina),
                                 [('10', '1', 'Aquecimento', 'aquecimento'), ('55', '5', 'Produção em papel', 'producao')])
                self.assertEqual(pagina.count('data-relogio'), 2)
                self.assertIn(f'Faz o aquecimento (10{N}minutos).', pagina)
                self.assertIn(f'Nos 10{N}minutos de leitura, lê as duas perguntas e os passos dos dois temas.', pagina)
                self.assertIn(f'<p class="task-kicker">Tarefa individual, 90{N}minutos</p>', pagina)
        # O aquecimento diz «Dez minutos»; o guia da tarefa tem os mesmos quatro blocos.
        for slug in SLUGS:
            self.assertEqual(ler(f'tarefas/{slug}/aquecimento/index.html').count('Dez minutos, com consulta.'), 1)
        guia = ler(GUIA)
        blocos = json.JSONDecoder().raw_decode(guia.split('BLOCOS=', 1)[1])[0]
        self.assertEqual(blocos, [[10, 'Aquecer', 'Faz os cartões com consulta.'], [10, 'Ler o enunciado', 'Lê as duas perguntas e os temas A e B.'],
                                  [55, 'Produzir', 'Escreve individualmente, em papel, com consulta.'],
                                  [15, 'Rever e entregar', 'Confere a grelha /20 e entrega fotografias legíveis no Teams.']])
        self.assertEqual(re.findall(r'<div class="t"><b>([^<]+)</b>', guia),
                         [f'Aquecer, 10{N}min', f'Ler o enunciado, 10{N}min', f'Produzir, 55{N}min', f'Rever e entregar, 15{N}min'])
        self.assertIn(f'faz o aquecimento em cartões (10{N}minutos). Seguem-se 10{N}minutos de leitura, 55 de produção e 15 de revisão e entrega.', guia)
        # Nenhum «5 min» nem «60 min» antigos (nem «5 minutos», «60 minutos», «60 de produção») nas páginas do M3 ligadas à tarefa.
        for rel in PAGINAS + [GUIA, INDICE, MAPA, 'm3/portefolio-do-modulo-m3/index.html']:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                self.assertNotRegex(fonte, r'(?<![\d,.])(?:5|60)[ \xa0]min')
                self.assertNotRegex(fonte, r'\b60 de produção|\b5 de leitura')
                self.assertNotIn('10/5/60/15', fonte)

    def test_consulta_versos_autoavaliacao_e_aquecimento(self):
        for slug in SLUGS:
            pagina = ler(f'tarefas/{slug}/index.html')
            texto = visivel(pagina)
            cabeca = pagina.split('<header>', 1)[1].split('</header>', 1)[0]
            with self.subTest(tarefa=slug):
                # «Com consulta» diz-se uma vez, no primeiro cartão, e diz o que é.
                frase = 'Trabalhas à mão. O aquecimento e a tarefa são com consulta: podes usar as lições do site, o caderno e o dicionário.'
                self.assertIn(f'<p class="tf-p">{frase}</p>', cabeca)
                self.assertEqual(texto.count('com consulta'), 1)
                self.assertEqual(len(re.findall(r'\bconsulta\b', texto)), 1)
                # Os versos citados ou copiados não contam: uma vez no enunciado, por baixo do quadro, e igual na grelha do aluno.
                conta = ('Não contam para as palavras: os versos citados ou copiados, as divisões em sílabas e as duas linhas finais.' if slug == 'm3-u1'
                         else 'Não contam para as palavras: os versos citados ou copiados e as duas linhas finais.')
                self.assertIn(f'<p class="tf-nota">{conta}</p>', cabeca)
                self.assertEqual(texto.count('Não contam para as palavras'), 1)
                grelha = ler(f'tarefas/{slug}/grelha/index.html')
                self.assertEqual(grelha.count(conta), 1)
                self.assertNotIn('que não contam para as palavras', grelha)
                # A autoavaliação é só para o aluno: não se entrega (enunciado, grelha e correção).
                self.assertIn('<p class="tf-nota tf-grelha-nota">A autoavaliação da grelha é só para ti: não se entrega.</p>', cabeca)
                self.assertEqual(texto.count('autoavaliação'), 2)
                entrega = pagina[pagina.index('<h2>Entrega no Teams</h2>'):pagina.index('</section>', pagina.index('<h2>Entrega no Teams</h2>'))]
                self.assertEqual(re.findall(r'<li>(.*?)</li>', entrega), ['Fotografa as respostas, o texto do teu tema e as duas linhas finais.',
                                                                          'Confirma que as fotografias mostram o trabalho completo.',
                                                                          'Entrega as fotografias na tarefa do Teams.'])
                self.assertEqual(grelha.count('Esta autoavaliação é só para ti: não se entrega.'), 1)
                self.assertNotIn('Entrega esta autoavaliação', grelha)
                self.assertNotIn('comenta a diferença', grelha)
                correcao = ler(f'tarefas/{slug}/correcao/index.html')
                self.assertIn('<thead><tr><th>Critério</th><th class="n">Máx.</th><th class="n">Docente</th><th>Observações</th></tr></thead>', correcao)
                self.assertNotIn('Aluno</th>', correcao)
                self.assertNotIn('Diferença entre a tua nota e a minha', correcao)
                self.assertNotIn('Onde nos afastámos', correcao)
                # Cada linha da tabela de notas tem quatro células (critério, máximo, docente, observações); antes tinha cinco.
                linhas = re.findall(r'<tr(?: class="total")?>(.*?)</tr>', correcao[correcao.index('<tbody>'):correcao.index('</tbody>')])
                self.assertEqual(len(linhas), 6)
                for l in linhas:
                    self.assertEqual(len(re.findall(r'<t[dh][ >]', l)), 4, l[:80])
                for parte in ('<h2 class="g-fb-t">Comentário ao aluno</h2>', '<h3>O que funciona</h3>', '<h3>O que te custa pontos</h3>', '<h3>Próximo passo</h3>'):
                    self.assertEqual(correcao.count(parte), 1)
                # O aquecimento é o primeiro passo, com uma só ligação.
                self.assertEqual(pagina.count('href="aquecimento/"'), 1)
                self.assertIn(f'<ol class="tf-fazer"><li>Faz o aquecimento (10{N}minutos).<span class="task-aquecer tf-abrir"><a href="aquecimento/">Abrir o aquecimento em cartões</a></span></li>', cabeca)
                self.assertLess(cabeca.index('href="aquecimento/"'), cabeca.index('O que entregas'))
                # A verificação final: no máximo 10 perguntas de sim ou não, numa só lista.
                lista = re.search(r'<fieldset class="task-checklist" aria-labelledby="entregar-title">(.*?)</fieldset>', pagina, re.S).group(1)
                perguntas = re.findall(r'<label><input type="checkbox"> <span>(.*?)</span></label>', lista)
                self.assertEqual(lista.count('<label>'), len(perguntas))
                self.assertLessEqual(len(perguntas), 10)
                self.assertGreaterEqual(len(perguntas), 9)
                self.assertTrue(all(p.endswith('?') for p in perguntas), perguntas)
                self.assertEqual(pagina.count('class="task-checklist"'), 1)
                self.assertIn('<p class="tf-p" id="criterios">Responde sim ou não. Se for não, completa o teu trabalho.</p>', pagina)
                # Um pedido por alínea ou passo: cada um é uma frase só, salvo o último passo do tema B da m3-u2 (duas frases curtas).
                d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))['facil']
                for p in d['perguntas']:
                    alineas = p.get('alineas') or [x for g in p['grupos'] for x in g['alineas']]
                    self.assertGreaterEqual(len(alineas), 5)
                    for x in alineas:
                        self.assertEqual(len(re.findall(r'[.?!](?:\s|$)', re.sub(r'<[^>]+>', '', x))), 1, x)
                        self.assertLessEqual(len(x.split()), 14, x)

    def test_tudo_junto_as_mesmas_palavras(self):
        # O enunciado novo diz «as duas perguntas», «a letra do teu tema» e «as respostas ligam-se»: a grelha, a correção, o aquecimento,
        # o guia, o índice e o mapa usam as mesmas palavras, e as antigas saem de todos.
        for slug in SLUGS:
            for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                rel = f'tarefas/{slug}/{parte}index.html'
                with self.subTest(pagina=rel):
                    texto = visivel(ler(rel), so_main=False, sem_nav=False)
                    for velha in ('úcleo', 'tema escolhido', 'articulad'):
                        self.assertNotIn(velha, texto)
                    self.assertNotRegex(texto, r'(?<!a letra d)o tema no topo')
            enunciado = visivel(ler(f'tarefas/{slug}/index.html'))
            self.assertIn(f'Responde a duas perguntas.', enunciado)
            self.assertIn(f'Escreve a letra do teu tema (A{N}ou{N}B) no topo.', enunciado)
            self.assertIn('As respostas ligam-se (não estão soltas)?', enunciado)
            self.assertIn(f'A letra do meu tema (A{N}ou{N}B) está no topo?', enunciado)
            self.assertIn(f'<meta name="description" content="Aula de tarefa com consulta: aquecimento, duas perguntas e um tema à escolha, em papel, durante 90{N}minutos, com entrega no Teams.">', ler(f'tarefas/{slug}/index.html'))
            for parte in ('grelha/', 'correcao/'):
                p = ler(f'tarefas/{slug}/{parte}index.html')
                self.assertIn('Respostas ligadas, extensão e escrita revista', p)
                self.assertIn('a letra do teu tema está no topo', p)
            grelha = ler(f'tarefas/{slug}/grelha/index.html')
            self.assertEqual(grelha.count('Respostas ligadas, extensão e escrita revista'), 3)
            self.assertIn('<p>Duas perguntas e um tema à escolha (A ou B), à mão, entre 200 e ', grelha)
            self.assertIn('a letra do tema no topo', grelha)
            self.assertIn('<li>Não escrever no topo a letra do teu tema (A ou B).</li>', grelha)
            aquecimento = ler(f'tarefas/{slug}/aquecimento/index.html')
            self.assertEqual(aquecimento.count(f'<b>Perguntas{N}1{N}e{N}2.<\\/b>'), 1)
        self.assertIn('Respondes às duas perguntas, com as citações e as sílabas', ler('tarefas/m3-u1/aquecimento/index.html'))
        self.assertIn('as duas perguntas vêm antes porque são para todos', ler('tarefas/m3-u1/aquecimento/index.html'))
        self.assertIn('a gramática fecha as duas perguntas;', ler('tarefas/m3-u2/aquecimento/index.html'))
        # Na m3-u2 o enunciado chama «tese» à interpretação que se discute, como a grelha, a correção e o aquecimento.
        u2 = ler('tarefas/m3-u2/index.html')
        self.assertIn('<li>Começa pela tua tese: uma interpretação que possa ser discutida.</li>', u2)
        self.assertIn('Tese na primeira frase', ler('tarefas/m3-u2/grelha/index.html'))
        # O guia, o índice e o mapa do M3.
        for rel, frases in ((GUIA, ['<span>Lê as duas perguntas e os temas A e B.</span>']),
                            (INDICE, ['aquecimento em cartões, duas perguntas, tema A ou B, revisão e fotografias no Teams.',
                                      'com consulta: aquecimento, duas perguntas, tema A ou B, revisão e fotografias no Teams.']),
                            (MAPA, ['com aquecimento, duas perguntas, tema A ou B e grelha /20;'])):
            fonte = ler(rel)
            self.assertNotIn('núcleo comum', fonte, rel)
            for frase in frases:
                self.assertIn(frase, fonte, rel)
        self.assertEqual(ler(INDICE).count('com consulta: aquecimento, duas perguntas, tema A ou B, revisão e fotografias no Teams.'), 2)

    # ---------- 13/11/2026: a autoavaliação colada no Teams e o par de trabalho saem do guia ----------

    def test_guia_sem_autoavaliacao_para_o_teams_nem_par_de_trabalho(self):
        # 13/11/2026 (decisão do docente): no guia da tarefa do M3, a «Autoavaliação» que se copiava para o Teams sai (a autoavaliação
        # é só para o aluno e não se entrega) e «pergunta ao teu par de trabalho» sai (não há trabalho de grupo nem de pares).
        guia, base = ler(GUIA), antes(GUIA)
        lido = visivel(guia, so_main=False, sem_nav=False)
        # As frases de antes estavam na base (o main de partida) e já não estão na página, nem no código.
        saem = ['<h2>Autoavaliação</h2>',
                'Em cada parâmetro, toca no nível que achas que tens. O 4 é o melhor. Escreve uma linha a dizer porquê.',
                '<div id="r-auto"></div>',
                'dás-te um nível em cada parâmetro',
                'O docente vê o teu plano, as notas, a lista e a autoavaliação.',
                'l.push("","AUTOAVALIAÇÃO");',
                '$("#r-auto").innerHTML=',
                '(extra sem nota)',
                'placeholder="Porquê, numa linha."',
                'if(t.dataset.auto!=null)',
                'ev.target.closest(".niveis button")',
                '3) pergunta ao teu par de trabalho',
                '<b>Três antes de mim.</b>']
        for frase in saem:
            with self.subTest(sai=frase):
                self.assertEqual(base.count(frase), 1)
                self.assertNotIn(frase, guia)
        # Nenhuma autoavaliação, nenhum nível para tocar e nenhum par, grupo ou equipa em todo o guia (texto e código). Ficam
        # só a regra «Original» (copiar de um colega não conta) e a chave «grupo» dos dados das produções antigas, sempre falsa.
        self.assertNotRegex(guia, r'(?i)auto-?avalia')
        self.assertNotRegex(guia, r'r-auto|data-auto|dataset\.auto|D\.auto|\.niveis button"|class="niveis"|aria-pressed="')
        # O estilo dos níveis fica na folha de estilo, sem uso e igual ao do main: os nove guias da tarefa têm o mesmo estilo, letra a
        # letra (tests/test_tasks_m356.py), e a decisão é só para o M3. Nada na página nem no código o usa.
        estilo = guia[guia.index('<style>'):guia.index('</style>')]
        self.assertEqual(estilo, base[base.index('<style>'):base.index('</style>')])
        self.assertEqual(guia.count('niveis button'), estilo.count('niveis button'))
        self.assertEqual(guia.count('aria-pressed'), estilo.count('aria-pressed'))
        self.assertNotRegex(lido, r'(?i)\bpar(?:es)?\b|\bgrupos?\b|\bequipas?\b|\bduplas?\b|em conjunto')
        self.assertEqual(re.findall(r'(?i)colegas?', guia), ['colega'])
        self.assertIn('Copiar de uma página ou de um colega, ou mandar fazer a uma máquina, não conta como tarefa.', guia)
        self.assertEqual(set(re.findall(r'"grupo":(\w+)', guia)), {'false'})
        self.assertEqual(len(re.findall(r'(?i)\bgrupo', guia)), guia.count('"grupo":false'))
        # O que fica, com a frase certa: a regra com dois passos numerados (1 e 2, sem 3) e o nome a dizer dois.
        self.assertEqual(guia.count('<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; '
                                    '2) vê a rubrica. Só depois levantas o braço.</div>'), 1)
        regra = guia[guia.index('<b>Dois antes de mim.</b>'):]
        regra = regra[:regra.index('</div>')]
        self.assertEqual(re.findall(r'(\d)\)', regra), ['1', '2'])
        self.assertEqual(guia.count('No fim, verificas o trabalho com a lista da rubrica e copias tudo para a tarefa do Teams. '
                                    'O que escreves fica só neste telemóvel.</p>'), 1)
        self.assertEqual(guia.count('Cola na tarefa do Teams, juntamente com o trabalho. O docente vê o teu plano, as notas e a lista.</p>'), 1)
        # O resto do modelo que se copia fica: o plano, as notas e a lista de verificação; a seguir à lista vêm logo os botões.
        self.assertIn('<h2>Verificar antes de entregar</h2>\n<ul class="lista" id="r-verificar"></ul>\n<div class="fila">'
                      '<button class="btn" id="copiar">Copiar para o Teams</button>', guia)
        copiado = guia[guia.index('function texto(){'):guia.index('$("#copiar").onclick')]
        self.assertEqual(re.findall(r'"([A-ZÇÃÕÁÉÍÓÚ ]{5,})"', copiado), ['PLANO', 'NOTAS DE TRABALHO', 'VERIFICAÇÃO'])
        self.assertTrue(copiado.endswith('+p.nome)});return l.join("\\n")}\n'), copiado[-80:])
        self.assertEqual(re.findall(r'<h2[^>]*>([^<]*)</h2>', guia[guia.index('<section id="rota"'):]),
                         ['', 'Os blocos de hoje', 'Verificar antes de entregar'])
        # Cada identificador que o código procura existe na página (nada fica a apontar para o bloco que saiu).
        codigo = guia[guia.index('var M="M3"'):]
        for ident in sorted(set(re.findall(r'\$\("#([\w-]+)"\)', codigo))):
            with self.subTest(identificador=ident):
                self.assertEqual(guia.count(f' id="{ident}"'), 1)
        # O resto da página é o main de partida, letra a letra, salvo as trocas da camada: as quatro de 12/11/2026 (tempos e «as duas
        # perguntas») e as oito de 13/11/2026. Cada troca que tira um pedaço inteiro só tira: o que fica é a base sem esse pedaço.
        edits = MANIFESTO['files'][GUIA]['edits']
        self.assertEqual(len(edits), 12)
        r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{GUIA}'], cwd=ROOT, capture_output=True)
        if r.returncode == 0:
            self.assertEqual(r.stdout.decode('utf-8'), base)
        self.assertEqual(sha_lf(base), MANIFESTO['files'][GUIA]['base_sha256_lf'])
        de_novo = base
        for e in edits:
            self.assertEqual(de_novo.count(e['old']), 1, e['location'])
            de_novo = de_novo.replace(e['old'], e['new'])
        self.assertEqual(de_novo, guia)
        so_tiram = 0
        for e in edits[7:]:
            i = 0
            while i < len(e['new']) and e['old'][i] == e['new'][i]:
                i += 1
            resto = e['new'][i:]
            if resto and e['old'].endswith(resto):
                so_tiram += 1
        self.assertEqual(so_tiram, 5)
        self.assertEqual(len(base) - len(guia), sum(len(e['old']) - len(e['new']) for e in edits))
        # As páginas das duas tarefas dizem o mesmo: a autoavaliação da grelha é só do aluno e não se entrega.
        for slug in SLUGS:
            self.assertIn('A autoavaliação da grelha é só para ti: não se entrega.', ler(f'tarefas/{slug}/index.html'))
            self.assertIn('Esta autoavaliação é só para ti: não se entrega.', ler(f'tarefas/{slug}/grelha/index.html'))
            for parte in ('', 'grelha/', 'correcao/'):
                self.assertNotRegex(visivel(ler(f'tarefas/{slug}/{parte}index.html'), so_main=False, sem_nav=False),
                                    r'(?i)par de trabalho|trabalho de (?:grupo|pares)|em pares|com (?:o|a) (?:teu|tua) colega')

    # ---------- as regras do texto ----------

    def test_regras_do_texto(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                texto = visivel(fonte)
                baixo = texto.lower()
                for palavra in ('professor', 'jogar', 'jogador', 'ficha', 'folha', 'em grupo', 'em pares', 'fernandes'):
                    self.assertNotIn(palavra, baixo, palavra)
                self.assertNotRegex(baixo, r'\bjog(?:o|os|a|am|ar)\b')
                self.assertNotIn('—', texto)
                self.assertNotRegex(texto, r'\bQual (?!d[aeo]s? )')
                self.assertNotRegex(texto, r'\b[Vv]ocê\b')
        for slug in SLUGS:
            fonte = ler(f'tarefas/{slug}/index.html')
            texto = visivel(fonte)
            with self.subTest(enunciado=slug):
                # «·» só no molde comum (o título da janela e a navegação), nunca numa frase nossa.
                self.assertNotIn('·', texto)
                # Títulos de obras em itálico.
                self.assertNotRegex(re.sub(r'<i>Os Lusíadas</i>|alt="[^"]*"|aria-label="[^"]*"', '', fonte[fonte.index('<main'):fonte.index('</main>')]), r'Os Lusíadas')
                self.assertNotRegex(re.sub(r'<i>[^<]*</i>', '', fonte[fonte.index('<main'):]), r'\bKit\b')
                # Referências que não se partem (U+00A0), como nas outras páginas.
                for padrao in (r'\b(?:Texto|Pergunta|pergunta|Tema|tema|Lição|lição|canto|Canto|estância|estâncias|verso|versos) (?:\d|[AB]\b|[IVX]+\b|F\d)',
                               r'\d (?:min|minutos|palavras)\b', r'\b[IVX]+, \d', r'\d (?:a|e|ou) \d', r'\bA ou B\b'):
                    # (o «Tema » que só os leitores de ecrã leem antes da letra de cada tema, no molde comum, fica de fora)
                    self.assertNotRegex(visivel(fonte.replace('<span class="sr-only">Tema </span>', '')), padrao)
                # As falas do aluno em discurso direto ficam entre «» (nenhuma aspa direita nem curva nas nossas frases).
                self.assertNotRegex(texto, r'[“”"]')
        # O molde não é o piloto por aprovar: os comentários dizem que foi aprovado.
        for rel in ('scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py', 'scripts/grelhas_tarefas.py', 'assets/task-textos.css', 'assets/task-reader.js'):
            self.assertNotIn('por aprovar', ler(rel), rel)

    # ---------- o contrato da página (substitui o de tests/test_task_choice.py nestas duas tarefas) ----------

    def test_contrato_da_pagina(self):
        for slug in SLUGS:
            rel = f'tarefas/{slug}/index.html'
            fonte = ler(rel)
            p = Pagina(fonte)
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            with self.subTest(tarefa=slug):
                self.assertIn('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil data-task-opening="Começar" data-task-index="nomes">', fonte)
                self.assertEqual([t for t, _, _ in p.raiz], ['nav', 'header', 'section', 'section', 'section', 'section', 'section'])
                self.assertEqual([i for _, i, _ in p.raiz][2:], ['produzir', 'pergunta-2', 'tema', 'entregar', 'apoios'])
                self.assertEqual(['Começar'] + [c for _, _, c in p.raiz][2:], CARTOES_NOMES)
                self.assertEqual(p.temas, ['A', 'B'])
                self.assertEqual(len(re.findall(r'<h3 id="tema-([AB])"><span><span class="sr-only">Tema </span>\1</span> ', fonte)), 2)
                self.assertEqual(len(p.ids), len(set(p.ids)))
                # O primeiro cartão: o que vais fazer, o que entregas, o quadro, a grelha.
                cabeca = fonte.split('<header>', 1)[1].split('</header>', 1)[0]
                self.assertEqual(re.findall(r'<h2 class="task-part"[^>]*>(.*?)</h2>', cabeca), ['O que vais fazer', 'Relógio do aquecimento', 'O que entregas', 'Tempo e tamanho'])
                self.assertEqual(cabeca.count('<ol class="tf-fazer">'), 1)
                self.assertEqual(len(re.findall(r'<li>', cabeca.split('<ol class="tf-fazer">')[1].split('</ol>')[0])), 5)
                self.assertIn('<p class="tf-p">Fotografias do teu trabalho em papel, na tarefa do Teams.</p>', cabeca)
                self.assertEqual(fonte.count('<a href="grelha/">'), 1)
                self.assertIn('<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>', cabeca)
                # Uma só pergunta opcional, num desdobrável, com três opções, uma certa, explicações diferentes.
                self.assertEqual(p.perguntas, [('1', True)])
                self.assertEqual(len(p.opcoes), 3)
                self.assertEqual(sum(a['data-correct'] == 'true' for a in p.opcoes), 1)
                self.assertEqual(len({a['data-response'] for a in p.opcoes}), 3)
                self.assertEqual(len(re.findall(r'<span class="task-letter">[ABC]<span class="sr-only">:</span></span> ', fonte)), 3)
                # Os recursos: os mesmos do molde de 28/10, mais a folha e o leitor desta versão.
                self.assertLess(fonte.index('assets/relogio.js'), fonte.index('pt-lessons/casca.js'))
                # 13/11/2026: a folha mudou (o cabeçalho dos temas em papel), por isso a versão dos dois recursos passa de facil-6 a facil-7.
                for recurso in ('task-choice.css?v=20261028-escolha-2', 'task-90.js?v=20261027-compact-1', 'task-reader.js?v=20261112-facil-7',
                                'task-textos.css?v=20261112-facil-7', 'info-i.css?v=20261105', 'info-i.js?v=20261105'):
                    self.assertEqual(fonte.count(recurso), 1, recurso)
                for fora in ('task-clock', 'rondas', '10/10/60/10'):
                    self.assertNotIn(fora, fonte)
                # As duas linhas finais, a entrega e a letra do tema.
                for frase in ('<h2 id="finais-titulo">Duas linhas finais</h2>', '<h2>Entrega no Teams</h2>', '<h2 id="entregar-title">Antes de entregar, verifica</h2>'):
                    self.assertEqual(fonte.count(frase), 1, frase)
                # Dossiê do tema B: cada facto com a sua fonte e a ligação, que existe; citações e números na página para onde aponta.
                dossie = re.findall(r'<section class="task-dossier tf-dossie".*?</section>', fonte, re.S)
                self.assertEqual(len(dossie), 1)
                factos = re.findall(r'<li>(.*?)<span class="tf-origem">Fonte: <a href="([^"]+)">(.*?)</a></span></li>', dossie[0])
                self.assertEqual(len(factos), dossie[0].count('<li>'))
                self.assertEqual([(x, h, n) for x, h, n in factos], [(x['facto'], x['href'], x['fonte']) for x in d['dossie']])
                self.assertGreaterEqual(len(factos), 5)
                for facto, href, _ in factos:
                    alvo = plana(str((Path(rel).parent / href / 'index.html').as_posix()).replace('tarefas/' + slug + '/../../', ''))
                    texto = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', facto)))
                    for pedaco in re.findall(r'«([^»]+)»', texto) + re.findall(r'\b\d{3,4}\b', texto):
                        self.assertIn(pedaco, alvo, (href, pedaco))
                # Todas as ligações internas existem; as âncoras apontam para ids da página.
                licoes = [h for h in p.ligacoes if '/m3/licao-' in h]
                self.assertGreaterEqual(len(set(licoes)), 4)
                for href in p.ligacoes:
                    url = urlsplit(href)
                    if url.scheme:
                        self.assertIn((url.scheme, url.netloc), (('https', 'creativecommons.org'), ('https', 'pedrohfernandes-klk.github.io')), href)
                        continue
                    if not url.path:
                        self.assertIn(url.fragment, p.ids, href)
                        continue
                    alvo = (ROOT / rel).parent / unquote(url.path)
                    self.assertTrue(((alvo / 'index.html') if alvo.is_dir() else alvo).is_file(), href)
                self.assertGreaterEqual(len([h for h in p.ligacoes if h.startswith('#texto-')]), 2)
                self.assertIn('#dossie', p.ligacoes)
                # «Rever a matéria»: uma linha por pergunta ou tema; o nome da página e os nomes das secções entre «» são os da lição.
                rever = re.search(r'<ul class="tf-rever-lista">(.*?)</ul>', fonte, re.S).group(1)
                itens = re.findall(r'<li><b>((?:Pergunta|Tema)\xa0[12AB])\.</b> (?:Lição\xa0F\d\d|Pensar devagar), <a href="([^"]+)">(.*?)</a>\.? (.*?)</li>', rever)
                self.assertEqual(len(itens), rever.count('<li>'))
                self.assertGreaterEqual(len(itens), 4)
                self.assertEqual({solto(x[0]) for x in itens} & {'Pergunta 1', 'Pergunta 2'}, {'Pergunta 1', 'Pergunta 2'})
                motor = plana('assets/pt-lessons/jogo.js')
                for _, href, nome, resto in itens:
                    alvo = plana(href.replace('../../', '') + 'index.html')
                    self.assertIn(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', nome))), alvo, href)
                    for secao in re.findall(r'«([^»]+)»', resto):
                        secao = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', secao)))
                        self.assertTrue(secao in alvo or secao in motor, (href, secao))
                # A fotografia do tema B da m3-u1 é a da lição F04 (os mesmos bytes), com o crédito atrás do «i».
                if slug == 'm3-u1':
                    imagem = re.search(r'<figure class="tf-fig"><img src="(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+)" alt="([^"]+)"', fonte)
                    self.assertIn(f'<img src=\\"{imagem.group(1)}\\" alt=\\"{imagem.group(2)}\\"', ler('m3/licao-m3-f04/index.html'))
                    self.assertIn('CC BY-SA 4.0', fonte)
                else:
                    self.assertNotIn('<figure', fonte)
                    # A m3-u2 usa as três chaves novas do molde: grupos de alíneas com as letras seguidas, um apoio e uma orientação comum.
                    self.assertEqual(re.findall(r'<ol class="tf-alineas"(?: start="(\d)")?>', fonte.split('id="pergunta-2"')[1].split('</section>')[0]), ['', '4'])
                    self.assertEqual(fonte.count('<details class="tf-so-tema tf-mais tf-so-ecra"><summary>Ver o quadro das três modalidades, como está na lição\xa0F15</summary>'), 1)
                    self.assertIn(f'<td rowspan="2">orientação: cerca de{N}110 nas duas perguntas</td>', fonte)
                    self.assertEqual(fonte.count('<span class="tt-v tt-esc">'), 16)
        leitor = ler('assets/task-reader.js')
        self.assertIn('page.getAttribute("data-task-opening")||(compact?"Enunciado":"A aula de tarefa")', leitor)
        self.assertIn('node.getAttribute("data-task-card-name")||', leitor)
        self.assertIn('(page.getAttribute("data-task-index")==="nomes"?"":String(i+1)+". ")+item.label', leitor)

    # ---------- as outras onze tarefas não mudam ----------

    def test_as_outras_onze_tarefas_nao_mudam(self):
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(sorted(OUTRAS + SLUGS + NO_MOLDE_M1), sorted(p.stem for p in (ROOT / 'docs/pedagogia/tarefas-escolha').glob('*.json')))
        self.assertEqual(len(OUTRAS), 9)
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in OUTRAS:
            with self.subTest(tarefa=slug):
                self.assertNotIn('facil', json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json')))
                self.assertFalse({'autoavaliacao_so_tua', 'trocas_aluno'} & set(grelhas[slug]))
                pagina = ler(f'tarefas/{slug}/index.html')
                for marca in ('data-task-facil', 'task-textos.css', 'facil-', 'class="tf-', 'class="tt-'):
                    self.assertNotIn(marca, pagina)
                self.assertIn('task-reader.js?v=20261028-escolha-2', pagina)
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertNotIn(f'tarefas/{slug}/{parte}index.html', MANIFESTO['files'])
        # Os três geradores, com os dados da árvore, dão todas as páginas da árvore, byte a byte (as treze tarefas, as grelhas, as
        # correções e os aquecimentos).
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for slug in OUTRAS + SLUGS + NO_MOLDE_M1:
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertIn(f'tarefas/{slug}/{parte}index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())

    # ---------- a camada ----------

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 13/11/2026: por cima desta camada fica a das tarefas do M1 mais fáceis de fazer: a ordem ganha mais uma posição (esta passa
        # a segunda, logo por cima das provas em cartões) e as camadas são 48, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(len(verificar_camadas.LAYERS), 48)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 48)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertIn('não se edita à mão', MANIFESTO['_nota'])
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(len(TROCAS), sum(len(v['edits']) for v in MANIFESTO['files'].values()))
        self.assertEqual(len(MANIFESTO['files']), 16)
        # 13/11/2026: confere-se com a camada do M1, que está por cima, desfeita primeiro.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar',
                            '--desfazer-antes', M1], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 16 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        for t in TROCAS:
            self.assertTrue(t['achado'].startswith('12/11/2026: '), t['local'])
            self.assertEqual(t['ocorrencias'], 2 if t['ficheiro'] == INDICE and 'com consulta' in t['antigo'] else 1)
        # Ida e volta, letra a letra: a árvore é o «after» do manifesto; desfeita a camada, cada ficheiro é a base (o main de partida);
        # voltando a aplicar, é outra vez a árvore.
        for rel, registo in MANIFESTO['files'].items():
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = antes(rel)
                self.assertEqual(sha_lf(base), registo['base_sha256_lf'])
                self.assertNotEqual(base, atual)
                de_novo = base
                for e in registo['edits']:
                    self.assertEqual(de_novo.count(e['old']), e['occurrences'], e['location'])
                    de_novo = de_novo.replace(e['old'], e['new'])
                self.assertEqual(de_novo, atual)
                # A base é o ficheiro do commit de partida, byte a byte (quando o repositório o tem: num clone raso, vale o resumo).
                r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
                if r.returncode == 0:
                    self.assertEqual(r.stdout.decode('utf-8'), base)
                # O desfazer da auditoria dá o mesmo, e não desfaz nada segunda vez.
                self.assertEqual(undo_tarefas_faceis_m3_1112(rel, atual), base)
                self.assertEqual(undo_tarefas_faceis_m3_1112(rel, base), base)
                self.assertEqual(undo_exame_provas_oficial_1112(rel, atual), base)
        # 13/11/2026: com a camada do M1, que fica por cima, partilha só os dados das grelhas.
        self.assertEqual(set(MANIFESTO['files']) & set(json.loads((ROOT / M1).read_text('utf-8'))['files']), {GRELHAS})
        # Esta camada não partilha nenhum ficheiro com a que fica logo abaixo.
        self.assertEqual(set(MANIFESTO['files']) & set(json.loads(ler(PO))['files']), set())

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m3_20261112', ROOT / 'scripts/tarefas_faceis_m3_20261112.py')
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        todas, finais = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(C.FICHEIROS, FICHEIROS)
        self.assertEqual(C.BASE_COMMIT, BASE_COMMIT)
        # As três páginas do módulo mudam só nas trocas escritas à mão.
        # 13/11/2026: eram sete; a decisão do docente de 13/11/2026 (a «Autoavaliação» colada no Teams e o par de trabalho saem do guia)
        # junta oito no guia, e o teste passa a exigir as quinze, com as oito novas todas no guia.
        self.assertEqual(sorted((f, a, b, n) for f, a, b, n, _ in C.EDICOES),
                         sorted((t['ficheiro'], t['antigo'], t['novo'], t['ocorrencias']) for t in TROCAS if t['ficheiro'] in (GUIA, INDICE, MAPA)))
        self.assertEqual(len(C.EDICOES), 15)
        self.assertEqual([f for f, *_ in C.EDICOES[7:]], [GUIA] * 8)
        self.assertEqual(len(C.SAI), 5)
        for f, fica_antes, sai, fica_depois, _ in C.SAI:
            self.assertIn((f, fica_antes + sai + fica_depois, fica_antes + fica_depois, 1), [e[:4] for e in C.EDICOES])

    def test_leitura_historica_dos_enunciados(self):
        # Os contratos históricos leem as tarefas como eram antes do pedido #192 (scripts/tarefas_claras_historico.py). Com esta camada
        # por cima, a leitura dá a base do manifesto do #192, letra a letra, nos enunciados e nos dados da M3-U1 e da M3-U2, a partir
        # da página inteira ou com esta camada já desfeita; e não desfaz nada segunda vez.
        import tarefas_claras_historico as historico
        claras = json.loads(ler('tests/fixtures/tarefas-claras-edits-20261110.json'))['files']
        m6 = json.loads(ler('tests/fixtures/cuidado-m6-edits-20261108.json'))['files']
        nossos = sorted(set(MANIFESTO['files']) & set(claras))
        self.assertEqual(nossos, sorted(DADOS_TAREFAS + ['tarefas/m3-u1/index.html', 'tarefas/m3-u2/index.html']))
        for rel in nossos:
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                antes_192 = historico.desfazer(rel, atual)
                self.assertEqual(sha_lf(antes_192), claras[rel]['base_sha256_lf'])
                self.assertEqual(historico.desfazer(rel, antes(rel)), antes_192)
                self.assertEqual(historico.desfazer(rel, antes_192), antes_192)
                self.assertEqual(sha_lf(antes(rel)), m6[rel]['after_sha256_lf'])
                self.assertEqual(historico.desfazer_faceis(rel, atual), antes(rel))
                self.assertEqual(historico.desfazer_faceis(rel, antes(rel)), antes(rel))
        for rel in MANIFESTO['files']:
            self.assertEqual(historico.desfazer_faceis(rel, ler(rel)), antes(rel), rel)
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer(path, text):'):]
        self.assertLess(corpo.index('desfazer_faceis(rel, text)'), corpo.index('FILES.get(rel)'))
        self.assertLess(corpo.index('desfazer_faceis(rel, text)'), corpo.index('CUIDADO_M9.get(rel)'))
        self.assertIn("_sha_lf(text) == no_cimo['after_sha256_lf']", fonte)
        self.assertIn("assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M3 mais fáceis de fazer não confere: {rel}'", fonte)

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        # A auditoria desfaz primeiro esta camada; o corte da Sala também; as bases das camadas que partilham ficheiros com ela também.
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_tarefas_faceis_m3_1112(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_exame_provas_oficial_1112\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m3_1112\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('tarefas-faceis-m3-edits-20261112.json'), sala.index('exame-provas-oficial-edits-20261112.json'))
        for rel in ('scripts/cuidado_m6_20261108.py', 'scripts/cuidado_m7_20261111.py'):
            self.assertIn('return desfazer_faceis(rel, (ROOT / rel).read_bytes().decode(\'utf-8\'))', ler(rel), rel)
        indices = ler('scripts/cartaz_indices_148_20261106.py')
        corpo = indices[indices.index('def base(rel):'):]
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M3.read_text'), corpo.index('json.loads(CUIDADO_EXAME.read_text'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs', 'tests/browser_creditos_i_pt1.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((tarefasFaceisM3['), texto.index('((cuidadoExame['), rel)
        # Nos fluxos e nos outros testes, cada cadeia de desfazer começa por esta camada, sem nada entre ela e a das provas em cartões.
        cadeias = 0
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            # (13/11/2026: o teste da camada do M1 tem as suas próprias asserções sobre as cadeias)
            if p.name in ('test_tarefas_faceis_m3.py', 'test_tarefas_faceis_m1.py'):
                continue
            texto = '\n'.join(linha for linha in p.read_text('utf-8').split('\n') if not linha.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + PO), plano.count(f'--desfazer-antes {meu} --desfazer-antes {PO}'))
                # 13/11/2026: cada cadeia começa agora pela camada do M1, logo seguida desta, sem nada entre as duas; a exigência é a
                # mesma, com mais um elo à cabeça.
                self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count(f'--desfazer-antes {M1} --desfazer-antes {meu}'))
                self.assertEqual(plano.count('--desfazer-antes {po}'), plano.count('--desfazer-antes {t1} --desfazer-antes {tf} --desfazer-antes {po}'))
                self.assertEqual(plano.count('--desfazer-antes {PO}'), plano.count('--desfazer-antes {T1} --desfazer-antes {TF} --desfazer-antes {PO}'))
                self.assertEqual(plano.count(f"ROOT/'{PO}',"), plano.count(f"(ROOT/'{M1}',ROOT/'{meu}',ROOT/'{PO}',"))
                self.assertEqual(plano.count("ROOT/'{po}',"), plano.count("(ROOT/'{t1}',ROOT/'{tf}',ROOT/'{po}',"))
                # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça (13/11/2026: logo a seguir à do M1).
                if p.suffix == '.yml':
                    self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count(f'--verificar --desfazer-antes {M1} --desfazer-antes {meu}'))
                cadeias += plano.count(f'--desfazer-antes {meu} --desfazer-antes {PO}')
        self.assertGreater(cadeias, 40)
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        # 13/11/2026: no fluxo, esta camada confere-se com a do M1 desfeita primeiro, e as de baixo com as duas.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m3_20261112.json --manifesto {meu} --verificar --desfazer-antes {M1}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/exame_provas_oficial_20261112.json --manifesto {PO} --verificar --desfazer-antes {M1} --desfazer-antes {meu}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m3.py' -v", tarefas)
        self.assertIn('        run: python tests/browser_tarefas_faceis_m3.py\n', tarefas)
        self.assertTrue((ROOT / 'tests/browser_tarefas_faceis_m3.py').is_file())
        # Os fluxos que conferem ou desfazem esta camada arrancam quando ela muda.
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/tarefas_faceis_m3_20261112.*', meu):
                self.assertIn(f"'{caminho}'", texto, nome)
            self.assertRegex(texto.split('\non:')[0], r'\n# 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3, a camada tarefas_faceis_m3_20261112 ')
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        blocos = re.findall(r'^    paths: (\[.*\])$', cartaz, re.M)
        self.assertEqual(len(blocos), 2)
        self.assertEqual(blocos[0], blocos[1])

        # No fluxo das tarefas, tudo o que a camada muda, os geradores, o molde e os seus testes estão nos caminhos do pedido.
        def padrao(glob):
            partes = re.split(r'(\*\*|\*|\[[^\]]+\])', glob)
            return re.compile(''.join('.*' if x == '**' else '[^/]*' if x == '*' else x if x.startswith('[') else re.escape(x)
                                      for x in partes) + '$')
        cabeca = tarefas[tarefas.index('  pull_request:\n    paths:\n'):tarefas.index('\npermissions:')]
        padroes = [padrao(g) for g in re.findall(r"^      - '([^']+)'$", cabeca, re.M)]
        self.assertGreater(len(padroes), 50)
        for rel in FICHEIROS + ['scripts/tarefas_faceis_m3_20261112.py', CAMADA_REL, meu, 'scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py',
                                'scripts/grelhas_tarefas.py', 'scripts/aquecimentos.py', 'scripts/tarefas_claras_historico.py',
                                'assets/task-textos.css', 'assets/task-reader.js', 'tests/test_tarefas_faceis_m3.py',
                                'tests/browser_tarefas_faceis_m3.py']:
            self.assertTrue(any(q.match(rel) for q in padroes), rel)


if __name__ == '__main__':
    unittest.main()
