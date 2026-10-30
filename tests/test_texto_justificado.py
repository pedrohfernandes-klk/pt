"""30/10/2026: texto corrido justificado, com hifenização em português europeu (decisão do docente).

A regra vive num só bloco no fim de assets/appearance.css, o ficheiro de estilo comum a todas as páginas (mais uma linha em
cada um dos dois ficheiros de estilo dos painéis de notas, assets/pt-lessons/notes.css e m9/recursos/notas.css, quatro painéis cada,
que usam <main> sem classe). Este teste confere, sem navegador:

* que cada família de páginas carrega a regra: liga assets/appearance.css (uma vez, para um ficheiro que existe),
  tem <html lang="pt-PT"> e o bloco traz o seletor do texto corrido dessa família;
* que a regra só mexe no alinhamento e na hifenização (nem letra, nem tamanho, nem cores, nem espaçamento das linhas)
  e volta à esquerda abaixo de 22.5em (360 px; era 20em até à revisão de 30/10/2026);
* que nenhum seletor justificado aponta para versos, opções, botões, listas, tabelas, legendas, créditos ou para as
  áreas reservadas (o índice das provas e a prosa das provas em cartões);
* que a camada literal de 30/10 (classes «prosa» e «verso») só acrescenta classes, que nenhum excerto em prosa
  citado em blockquote nos cartões fica por marcar e que nenhum parágrafo feito sobretudo de verso citado fica por
  marcar como verso;
* que, nos exercícios de telemóvel, as caixas com botões de escolha (versos com lacuna, casos, itens a classificar)
  ficam fora da regra.
Revisão de 30/10/2026 (achados confirmados da revisão adversarial): também confere que os parágrafos de lista com rótulo
e verso citado sem « / » estão marcados como verso, que os excertos em prosa em blockquote sem <p> (também nos dados em
.js) estão marcados como prosa, que nenhum parágrafo com um botão ou um campo e nenhuma especificação de entrega das
guias se justifica, e que o texto da obra em p.pr com <br>, as cenas do Pensar devagar e o retorno da opção escolhida
entram. A camada pode também acrescentar o atributo lang a um trecho noutra língua.
O teste de navegador é tests/browser_texto_justificado.py.
"""
from pathlib import Path
import json
import re
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'assets/appearance.css').read_text('utf-8')
MARCA = '/* 30/10/2026: texto corrido justificado'
NOTAS = ROOT / 'm9/recursos/notas.css'
NOTES = ROOT / 'assets/pt-lessons/notes.css'
MANIFESTO = ROOT / 'tests/fixtures/texto-justificado-edits-20261030.json'


def bloco():
    assert CSS.count(MARCA) == 1, 'o bloco do texto justificado tem de existir uma vez em assets/appearance.css'
    return CSS[CSS.index(MARCA):]


def sem_comentarios(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def regras(css):
    """Pares (seletores, declarações) das regras de primeiro nível e dentro de @media/@supports."""
    css = sem_comentarios(css)
    out = []
    for m in re.finditer(r'([^{}@]+)\{([^{}]*)\}', css):
        sel = m.group(1).strip()
        if sel.startswith(':root'):
            continue
        out.append((sel, m.group(2).strip()))
    return out


def dividir(seletores):
    """Divide uma lista de seletores pelas vírgulas de primeiro nível (fora de parênteses)."""
    partes, nivel, atual = [], 0, ''
    for c in seletores:
        if c == '(':
            nivel += 1
        elif c == ')':
            nivel -= 1
        if c == ',' and nivel == 0:
            partes.append(atual.strip())
            atual = ''
        else:
            atual += c
    if atual.strip():
        partes.append(atual.strip())
    return partes


def justificados():
    out = []
    for sel, decl in regras(bloco()):
        if 'text-align:var(--epi-texto-corrido)' in decl:
            out.extend(dividir(sel))
    return out


def paginas():
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT).as_posix()
        if any(x in ('.git', 'tests', '_qa', 'node_modules') for x in p.relative_to(ROOT).parts):
            continue
        texto = p.read_text('utf-8')
        if 'http-equiv="refresh"' in texto and '<main' not in texto:
            continue  # redirecionamento, sem conteúdo
        yield rel, p, texto


# (família, caminho, marca no HTML que confirma a família, seletores do bloco que servem o seu texto corrido)
FAMILIAS = [
    ('lições em cartões', r'^m\d/licao-m\d-f\d+/index\.html$', 'casca',
     ['.jogo .ler p:not([class]):not(:has(br))', '.casca-folha .c-expl:not(:has(>br))', '.jogo .ler blockquote.prosa>p']),
    ('aquecimentos', r'^tarefas/m\d-u\d/aquecimento/index\.html$', 'casca', ['.jogo .ler p:not([class]):not(:has(br))']),
    ('provas em cartões (área reservada: herdam a regra dos cartões)', r'^exame/provas/[^/]+/grupo-[ivx]+/index\.html$',
     'casca', ['.jogo .ler p:not([class]):not(:has(br))']),
    ('Pensar devagar', r'^m\d/m\d-[^/]+/index\.html$', 'Pensar devagar', ['.jogo .ler blockquote.prosa>p']),
    ('exercícios de telemóvel', r'^(c|m\d)/[^/]+/index\.html$', 'id="palco"',
     ['#palco .caixa:not(:has(>.chips)) p:not([class]):not(:has(br))', '#palco .caixa p.prosa']),
    ('índices dos módulos', r'^m\d/index\.html$', 'pt-module', ['.pt-module details.regra>div', '.pt-module p.regras', '.pt-module main>p.pequeno']),
    ('mapas do módulo', r'^m\d/mapa-do-modulo-m\d/index\.html$', 'class="sec', ['details.sec>p:not([class])', 'main>header.topo>p[class="lead"]']),
    ('guias da tarefa (escolha e rota)', r'^m\d/guia-da-tarefa-m\d/index\.html$', 'id="escolha"', ['#escolha>p:not([class])', '#rota>div.regra']),
    ('guias da tarefa (arquivo das produções)', r'^m\d/guia-da-tarefa-m\d/index\.html$', 'id="arquivo-producoes"',
     # 30/10/2026 (revisão): sem as especificações de entrega de cada tarefa (section.tarefa-c), cujos nomes de ficheiro
     # compridos não partem e abriam buracos de 10 a 12 em
     ['#arquivo-producoes>p:not([class])', '#arquivo-producoes :not(section.tarefa-c)>p:not([class])',
      'main:has(>details#arquivo-producoes)>p:not([class])']),
    ('portefólios do módulo', r'^m\d/portefolio-do-modulo-m\d/index\.html$', 'class="regra"',
     ['main>div.regra', 'main:is(:has(>section#rota),:has(>div.regra))>:is(section:not([id]),aside:not([class]))>p:not([class])']),
    ('visitas', r'^m\d/visita-[^/]+/index\.html$', 'class="cx"', ['section[id] .cx>p:not([class])']),
    ('provas rápidas', r'^m\d/prova-[a-c]/index\.html$', 'id="entrada"', ['section#entrada>.aviso', '.q .exp']),
    ('questionários', r'^m\d/questionarios/index\.html$', 'id="indice"', ['section#indice>.aviso']),
    ('guiões de aula', r'^m\d/aulas/aula-\d+/index\.html$', 'class="dois"', ['.dois .caixa p:not([class])', 'ol.disc p.r']),
    ('tarefas', r'^tarefas/[^/]+/index\.html$', 'task-page', ['.task-page section>p:not([class])']),
    ('grelhas', r'^tarefas/[^/]+/grelha/index\.html$', 'class="grelha', ['main.grelha>header>p:not([class])']),
    ('obras', r'^obras/[^/]+/index\.html$', 'class="ob', ['main.ob>p:not([class])']),
    ('portais dos anos', r'^[123]/index\.html$', 'p-lead', ['.p-cab .p-lead']),
    ('entrada', r'^index\.html$', 'pt-entry-lead', ['.pt-entry-lead']),
    ('atlas', r'^atlas/index\.html$', 'atlas-investigar', ['.atlas-investigar>p:not([class])']),
    ('exame (sessões)', r'^exame/index\.html$', 'app.js', ['.pass-prosa .par', '.model']),
    ('laboratório do exame', r'^exame/laboratorio/index\.html$', 'laboratorio', ['#laboratorio .of-rosto>.of-entrada']),
]

# Nenhum seletor justificado pode atravessar versos nem as áreas reservadas (o índice das provas e a prosa das provas em
# cartões), e nenhum pode ter por sujeito opções, botões, listas, tabelas, legendas, créditos, formulários, títulos,
# perguntas ou o retorno curto. O que vem dentro de :not() e de :has() é condição, não sujeito.
PROIBIDO_EM_TODO = re.compile(r'\.(v|vl|ln|estrofe|verso|dupla-v|verso-q|frase-toda|prova-l)(?![\w-])|blockquote\.cit(?!\.prosa)|#provas|\.pv-')
PROIBIDO_SUJEITO = re.compile(r'(^|[(,])(li|td|th|dd|dt|tr|table|button|label|figcaption|summary|h[1-6]|input|textarea|select)(?![\w-])'
                              r'|\.(op|cc-op|fe|resp-proj|fonte|fonte-x|rodape|gl|cita|q|perg|papel-q|c-veredito)(?![\w-])')


def sem_condicoes(seletor):
    """Tira :not(...) e :has(...), com parênteses encaixados."""
    out, i = '', 0
    while i < len(seletor):
        m = re.match(r':(not|has)\(', seletor[i:])
        if m:
            nivel, j = 1, i + len(m.group(0))
            while nivel:
                nivel += {'(': 1, ')': -1}.get(seletor[j], 0)
                j += 1
            i = j
            continue
        out += seletor[i]
        i += 1
    return out


def sujeito(seletor):
    """O último composto do seletor (depois do último combinador fora de parênteses)."""
    limpo, nivel, inicio = sem_condicoes(seletor), 0, 0
    for k, c in enumerate(limpo):
        nivel += {'(': 1, ')': -1}.get(c, 0)
        if nivel == 0 and c in ' >+~':
            inicio = k + 1
    return limpo[inicio:]


DECLARACOES = {'text-align', 'text-align-last', 'hyphens', '-webkit-hyphens', 'hyphenate-limit-chars',
               '-webkit-hyphenate-limit-before', '-webkit-hyphenate-limit-after', 'word-spacing', 'overflow-wrap'}


class TextoJustificado(unittest.TestCase):
    def test_bloco_comum_com_hifenizacao_e_volta_a_esquerda_em_ecras_estreitos(self):
        b = sem_comentarios(bloco())
        self.assertIn(':root{--epi-texto-corrido:start}', b)
        # 30/10/2026: o limiar sobe de 20em para 22.5em (360 px), achado A4 da revisão adversarial: a 320 px, com hifenização
        # simulada, um quarto dos parágrafos de três ou mais linhas tinha um espaço de 0,9 em ou mais (a 360 px, 8 %).
        self.assertIn('@media screen and (min-width:22.5em),print{:root{--epi-texto-corrido:justify}}', b)
        corpo = [d for s, d in regras(bloco()) if 'text-align:var(--epi-texto-corrido)' in d]
        self.assertEqual(len(corpo), 2, 'uma regra geral e uma dentro de @supports selector(:has())')
        for d in corpo:
            for parte in ('text-align-last:auto', '-webkit-hyphens:auto', 'hyphens:auto', 'hyphenate-limit-chars:6 3 3',
                          'word-spacing:normal', 'overflow-wrap:break-word'):
                self.assertIn(parte, d)
        self.assertIn('@supports selector(p:has(br)){', b)

    def test_so_alinhamento_e_hifenizacao(self):
        for sel, decl in regras(bloco()):
            for propriedade in re.findall(r'(-?[a-z-]+)\s*:', decl):
                with self.subTest(seletor=sel[:60], propriedade=propriedade):
                    self.assertIn(propriedade, DECLARACOES)
        for css in (NOTAS, NOTES):
            notas = sem_comentarios(css.read_text('utf-8'))
            regra = notas[notas.index('@supports'):]
            for propriedade in re.findall(r'\{?(-?[a-z-]+)\s*:', regra.split('{', 2)[2]):
                with self.subTest(css=css.name, propriedade=propriedade):
                    self.assertIn(propriedade, DECLARACOES)

    def test_nenhum_seletor_justifica_versos_listas_botoes_ou_areas_reservadas(self):
        lista = justificados()
        self.assertGreater(len(lista), 50)
        for s in lista:
            with self.subTest(seletor=s):
                self.assertIsNone(PROIBIDO_EM_TODO.search(sem_condicoes(s)), s)
                self.assertIsNone(PROIBIDO_SUJEITO.search(sujeito(s)), s)
        # o próprio teste reconhece o que proíbe
        self.assertIsNotNone(PROIBIDO_EM_TODO.search(sem_condicoes('.jogo .ler .v .ln')))
        self.assertIsNotNone(PROIBIDO_SUJEITO.search(sujeito('.task-page li')))
        self.assertIsNone(PROIBIDO_SUJEITO.search(sujeito('main:has(>div.regra)>h2+p:not([class])')))
        # os parágrafos com <br> (versos ou linhas soltas) e os marcados como verso ficam fora; nos exercícios de telemóvel,
        # as caixas com botões de escolha (versos com lacuna, casos, itens a classificar) também
        for s in lista:
            if s.startswith('#palco .caixa') and not s.endswith('p.prosa'):
                self.assertIn(':not(:has(>.chips))', s)
            if s.startswith(('.jogo .ler p:not([class])', '#palco .caixa', 'main.pg>p')) and not s.endswith('p.prosa'):
                self.assertIn(':not(:has(br))', s)
            if 'p.cx' in s:
                self.assertIn(':not(.verso)', s)

    def test_cada_familia_carrega_a_regra(self):
        lista = set(justificados())
        todas = list(paginas())
        for familia, caminho, marca, seletores in FAMILIAS:
            with self.subTest(familia=familia):
                membros = [(rel, p, t) for rel, p, t in todas if re.match(caminho, rel) and marca in t]
                self.assertTrue(membros, f'nenhuma página da família {familia}')
                for s in seletores:
                    self.assertTrue(any(x.startswith(s) for x in lista), f'{familia}: o bloco não traz {s}')
                for rel, p, texto in membros:
                    self.assertRegex(texto, r'<html lang="pt-PT"', rel)
                    refs = re.findall(r'href="([^"]*assets/appearance\.css[^"]*)"', texto)
                    self.assertEqual(len(refs), 1, rel)
                    self.assertEqual((p.parent / refs[0].split('?')[0]).resolve(), (ROOT / 'assets/appearance.css').resolve(), rel)

    def test_todas_as_paginas_em_portugues_europeu(self):
        for rel, _, texto in paginas():
            with self.subTest(pagina=rel):
                self.assertRegex(texto, r'<html lang="pt-PT"')

    def test_paineis_de_notas_com_o_seu_css(self):
        # 30/10/2026: os oito painéis de notas usam <main> sem classe (ou main.pg) e um de dois ficheiros de estilo próprios; cada um
        # traz uma regra curta com a mesma declaração e o mesmo valor por omissão (à esquerda, se appearance.css faltar).
        for css, nome, seletor in ((NOTAS, 'recursos/notas.css', 'main>h1~p:not(:has(a)),main>details p:not([class]){'),
                                     (NOTES, 'pt-lessons/notes.css', 'main>h1~p:not([class]):not(:has(a)),main li>details>p:not([class]){')):
            with self.subTest(css=nome):
                texto = css.read_text('utf-8')
                self.assertIn('@supports selector(p:has(a)){' + seletor + 'text-align:var(--epi-texto-corrido,start);', texto)
                usam = [rel for rel, _, t in paginas() if nome in t]
                self.assertEqual(len(usam), 4, usam)
                for rel, _, t in paginas():
                    if nome in t:
                        self.assertLess(t.index(nome), t.index('assets/appearance.css'), rel)

    def test_camada_literal_so_acrescenta_classes(self):
        # 30/10/2026 (revisão): além das classes «prosa» e «verso», a camada pode acrescentar o atributo lang a um elemento
        # que já existe (trechos noutra língua); nunca muda texto.
        manifesto = json.loads(MANIFESTO.read_text('utf-8'))
        self.assertTrue(manifesto['files'])
        for rel, registo in manifesto['files'].items():
            texto = (ROOT / rel).read_text('utf-8')
            for edit in registo['edits']:
                with self.subTest(pagina=rel, local=edit['location']):
                    self.assertEqual(texto.count(edit['new']), edit['occurrences'])
                    novo = re.sub(r' lang=\\?"[a-z]{2}(?:-[A-Z]{2})?\\?"', '', edit['new'], count=1)
                    for classe in (' prosa', ' verso'):
                        novo = novo.replace(classe + '\\"', '\\"', 1).replace(classe + '"', '"', 1)
                    for so in (' class=\\"prosa\\"', ' class="prosa"', ' class=\\"verso\\"', ' class="verso"'):
                        novo = novo.replace(so, '', 1)
                    self.assertEqual(novo, edit['old'])

    def test_excertos_em_prosa_marcados_nos_cartoes(self):
        # 30/10/2026: um blockquote nos dados dos cartões com um parágrafo de 100 ou mais caracteres é prosa e leva a
        # classe «prosa»; as estrofes (um verso por parágrafo) ficam sem ela e à esquerda.
        for rel, _, texto in paginas():
            if 'class="jogo' not in texto and 'jogo-alvo' not in texto:
                continue
            dados = texto.replace('\\"', '"').replace('\\/', '/')
            for m in re.finditer(r'<blockquote([^>]*)>(.*?)</blockquote>', dados, re.S):
                ps = [re.sub(r'<[^>]+>', '', p) for p in re.findall(r'<p[^>]*>(.*?)</p>', m.group(2), re.S)]
                if ps and max(len(p) for p in ps) >= 100:
                    with self.subTest(pagina=rel, inicio=ps[0][:40]):
                        self.assertIn('prosa', m.group(1))

    def test_excertos_em_prosa_sem_paragrafos_marcados(self):
        # 30/10/2026 (revisão): um blockquote sem <p> e sem <br> nos dados dos cartões (também nos que vêm de um ficheiro .js
        # de recursos, como m4/recursos/tpc-entrada.js) com 100 ou mais caracteres é texto da obra em prosa e leva a classe
        # «prosa», que o justifica; um verso solto citado assim (m8/licao-m8-f10, assets/pt-lessons/m3-f18.js) fica sem ela.
        fontes = [(rel, t) for rel, _, t in paginas() if 'class="jogo' in t or 'jogo-alvo' in t or 'EPIJogo' in t]
        fontes += [(p.relative_to(ROOT).as_posix(), p.read_text('utf-8'))
                   for p in sorted(ROOT.glob('m*/recursos/*.js')) + sorted(ROOT.glob('assets/pt-lessons/m*-f*.js'))]
        vistos = 0
        for rel, texto in fontes:
            dados = texto.replace('\\"', '"').replace('\\/', '/')
            for m in re.finditer(r'<blockquote([^>]*)>((?:(?!</blockquote>).)*)</blockquote>', dados, re.S):
                if '<p' in m.group(2) or '<br' in m.group(2):
                    continue
                txt = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                if len(txt) >= 100:
                    vistos += 1
                    with self.subTest(ficheiro=rel, inicio=txt[:40]):
                        self.assertIn('prosa', m.group(1))
        self.assertGreaterEqual(vistos, 2)
        self.assertTrue(any(s.startswith('.jogo .ler blockquote.prosa:not(:has(p))') for s in justificados()))

    def test_verso_citado_marcado_nos_cartoes_e_exercicios(self):
        # 30/10/2026: um parágrafo justificável (sem <br>, sem classe ou com uma classe de prosa) em que o verso citado
        # («… / …») é pelo menos 60% do texto é verso, com rótulo, atribuição ou glosa curta, e leva a classe «verso».
        # Abaixo disso é uma frase que cita versos e justifica-se como o resto do texto.
        prosa = {'', 'pr', 'abre', 'abre-gancho', 'ex-antes', 'ex-depois', 'nota-ed', 'nota', 'nota-pensa', 'fecho-o', 'liga',
                 'cx', 'cc-def', 'cc-nao', 'pequeno'}
        vistos = 0
        for rel, _, texto in paginas():
            if not re.search(r'CARTOES=|EPIJogo|id="palco"', texto):
                continue
            dados = texto.replace('\\"', '"').replace('\\/', '/')
            for m in re.finditer(r'<p(?: class="([^"]*)")?>((?:(?!</p>).)*?)</p>', dados, re.S):
                classes = (m.group(1) or '').split()
                if '<br' in m.group(2) or not set(classes) - {'verso'} <= prosa:
                    continue
                txt = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                if ' / ' not in txt:
                    continue
                citado = sum(len(q) for q in re.findall(r'«(?:[^«»]|«[^«»]*»)*»', txt) if ' / ' in q)
                if citado >= 0.6 * len(txt):
                    vistos += 1
                    with self.subTest(pagina=rel, inicio=txt[:50]):
                        self.assertIn('verso', classes)
        self.assertGreaterEqual(vistos, 20)

    def test_rotulo_com_verso_citado_marcado(self):
        # 30/10/2026 (revisão): os versos citados sem « / » também contam. Um parágrafo de lista com rótulo («A.», ou a letra e um travessão)
        # seguido de uma citação e, quando muito, de uma atribuição ou glosa curta (60 caracteres) é verso se a citação for
        # um verso que o sítio mostra noutro lado em verso (num parágrafo com <br>, numa linha .ln ou .vl, ou numa estrofe
        # citada em blockquote), ou se outro parágrafo da mesma lista o for (os versos de uma lista vêm do mesmo sítio).
        # Uma citação em prosa numa lista de versos fica de fora pelo texto (PROSA_EM_LISTA).
        PROSA_EM_LISTA = {'Acorrei ao Mestre, que o matam!'}
        prosa = {'', 'pr', 'abre', 'abre-gancho', 'ex-antes', 'ex-depois', 'nota-ed', 'nota', 'nota-pensa', 'fecho-o', 'liga',
                 'cx', 'cc-def', 'cc-nao', 'pequeno'}

        def norm(x):
            x = unicodedata.normalize('NFC', re.sub(r'<[^>]+>', '', x)).lower()
            return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', x)).strip()

        todas = [(rel, t.replace('\\"', '"').replace('\\/', '/')) for rel, _, t in paginas()]
        versos = set()
        for _, dados in todas:
            for m in re.finditer(r'<p(?: class="([^"]*)")?[^>]*>((?:(?!</p>).)*?)</p>', dados, re.S):
                if '<br' in m.group(2) and not {'prosa', 'pr'} & set((m.group(1) or '').split()):
                    versos.update(norm(x) for x in re.split(r'<br\s*/?>', m.group(2)))
            for m in re.finditer(r'class="(?:ln|vl)[^"]*"[^>]*>((?:(?!</span>|</div>).)*)', dados, re.S):
                versos.add(norm(m.group(1)))
            for m in re.finditer(r'<blockquote(?: class="([^"]*)")?>(.*?)</blockquote>', dados, re.S):
                if 'prosa' not in (m.group(1) or ''):
                    for par in re.findall(r'<p[^>]*>(.*?)</p>', m.group(2), re.S):
                        versos.update(norm(x) for x in re.split(r'<br\s*/?>', par) if len(x) <= 90)
        versos = {v for v in versos if len(v) >= 12}
        rotulo = re.compile(r'^[A-Z]{1,4}[.)]?\s*(?:—\s*)?«((?:[^«»]|«[^«»]*»)*)»(.*)$', re.S)
        vistos = 0
        for rel, dados in todas:
            if not re.search(r'CARTOES=|EPIJogo|id="palco"', dados):
                continue
            corrida, fim = [], -1
            corridas = []
            for m in re.finditer(r'<p(?: class="([^"]*)")?>((?:(?!</p>).)*?)</p>', dados, re.S):
                if corrida and dados[fim:m.start()].strip():
                    corridas.append(corrida)
                    corrida = []
                corrida.append(m)
                fim = m.end()
            corridas.append(corrida)
            for corrida in corridas:
                itens = []
                for m in corrida:
                    classes = (m.group(1) or '').split()
                    if '<br' in m.group(2) or not set(classes) - {'verso'} <= prosa:
                        continue
                    txt = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                    r = rotulo.match(txt)
                    if not r or len(r.group(2).strip()) > 60 or r.group(1) in PROSA_EM_LISTA:
                        continue
                    itens.append((classes, txt, any(norm(x) in versos for x in r.group(1).split(' / '))))
                if any(e for _, _, e in itens):
                    for classes, txt, _ in itens:
                        vistos += 1
                        with self.subTest(pagina=rel, inicio=txt[:50]):
                            self.assertIn('verso', classes)
        self.assertGreaterEqual(vistos, 15)

    def test_controlos_e_nomes_de_ficheiro_fora_do_texto_justificado(self):
        # 30/10/2026 (revisão): um parágrafo com um botão ou um campo no meio do texto não é texto corrido (o botão não parte
        # e a linha de cima abria um buraco: «Podes imprimir… [Imprimir o mapa atualizado]» nos nove mapas); as
        # especificações de entrega das guias (section.tarefa-c, com nomes de ficheiro compridos) também ficam à esquerda.
        sem_controlo = ':not(:has(button,input,select,textarea))'
        lista = justificados()
        for s in lista:
            with self.subTest(seletor=s):
                if s.startswith(('details.sec>p:not', 'main.pg>p', '#escolha', 'section[id] .cx>p')):
                    self.assertIn(sem_controlo, s)
                if s.startswith('#arquivo-producoes ') and ':is(' not in s:
                    self.assertIn(':not(section.tarefa-c)>p', s)
        for mapa in sorted(ROOT.glob('m*/mapa-do-modulo-m*/index.html')):
            with self.subTest(mapa=mapa.parent.name):
                self.assertRegex(mapa.read_text('utf-8'), r'<p>Podes imprimir[^<]*<button')

    def test_revisao_texto_da_obra_cenas_e_retorno(self):
        # 30/10/2026 (revisão): as falas de teatro em p.pr com <br> (M4-F08) e as cenas do Pensar devagar entram; o retorno da
        # opção escolhida (.fe, mediana de 105 caracteres, três a quatro linhas no telemóvel) acompanha a explicação.
        lista = justificados()
        self.assertIn('.jogo .ler p.pr:not(.verso)', lista)
        self.assertTrue(any(s.startswith('.jogo p.cid-cena') for s in lista))
        excecao = [sel for sel, decl in regras(bloco()) if 'text-align:start' in decl]
        self.assertEqual(len(excecao), 1)
        self.assertNotIn('.fe', excecao[0])
        self.assertIn('.resp-proj', excecao[0])


if __name__ == '__main__':
    unittest.main()
