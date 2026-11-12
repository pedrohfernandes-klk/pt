"""12/11/2026: decisão 152 do docente («cuidado em todas as lições») no Exame e nas páginas transversais.

A camada cuidado_exame_20261112 (scripts/cuidado_exame_20261112.py e .json; manifesto em
tests/fixtures/cuidado-exame-edits-20261112.json) fica por cima da decisão 152 no M9. Confere-se aqui:
- a tabela nova (as fases da sessão, na vista «Programa e fontes» do Exame) e as quatro listas novas das provas em cartões, com as
  palavras todas, pela mesma ordem;
- os achados B: só espaços que não quebram (U+00A0) e junções (U+2060), com as contagens da conferência (nas provas em cartões,
  nunca mais do que a conferência contou) e fora dos sítios que não mudam;
- o texto oficial das provas (o texto e os itens da prova, as grelhas e os tópicos dos critérios), os rótulos dos cartões, as
  citações, o texto de apoio dos aquecimentos e o texto das obras nas sessões, que ficam como estavam, letra a letra;
- as páginas geradas (os 27 aquecimentos e as provas em cartões), que saem iguais dos geradores;
- o que fica de fora (diapositivos, páginas «todos», treinos, a moldura das provas) e a camada: fechada, reversível e no topo.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
import cuidado_exame_20261112 as C  # noqa: E402
import exame_aquecimentos  # noqa: E402
import verificar_camadas  # noqa: E402
from auditoria_20261028 import undo_cuidado_exame_1112, undo_cuidado_m9_1112  # noqa: E402
from provas_casos import provas  # noqa: E402
from test_provas_cartoes import OFICIAL, sem_oficial, segmentos  # noqa: E402

MANIFESTO_REL = 'tests/fixtures/cuidado-exame-edits-20261112.json'
BASE_COMMIT = 'e4b0e4c3fd8d2e970278ce326f0ac417c01d72ea'
N, WJ = '\xa0', '⁠'
APP, SESSOES = 'assets/exame/app.js', 'assets/exame/sessoes.json'
# Os achados confirmados (bordo/cidadania-v3/cuidado-152/exame-confirmados.json): 55, em 139 ficheiros lidos (1 A, 50 B e 4 C).
A, C_ = {0}, {3, 4, 5, 6}
B = set(range(26, 33)) | set(range(34, 77))
# Ficam de fora, por decisão já tomada (como do M1 ao M9): os diapositivos (57) e as páginas «todos» (60, 61 e 62); e a secção das
# provas (28), que sai inteira do molde do gerador e de prova.json e seccao.json, que esta camada não muda.
FORA_DE_AMBITO = {57: 'diapositivos/index.html', 60: '3/todos/index.html', 61: '2/todos/index.html', 62: '1/todos/index.html'}
MOLDURA_DAS_PROVAS = {28: 'exame/provas/index.html'}
RECUSADOS = set(range(1, 3)) | set(range(7, 26)) | {33, 77, 78}
APLICADOS = (A | B | C_) - set(FORA_DE_AMBITO) - set(MOLDURA_DAS_PROVAS)
PROVAS = {66: '2026-1f/grupo-ii', 67: '2026-1f/grupo-iii', 69: '2026-2f/grupo-ii', 70: '2026-2f/grupo-iii', 71: '2026-1f/grupo-i',
          72: '2026-2f/grupo-i'}
# Nas provas em cartões: (ocorrências que mudam, ocorrências que a conferência contou), por achado.
PROVAS_CONTAS = {66: (124, 171), 67: (93, 160), 69: (216, 270), 70: (162, 231), 71: (282, 358), 72: (403, 477)}
NUMEROS = (1753, 65)


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def base(rel):
    """O ficheiro sem esta camada (desfeita pelo manifesto, com contagem estrita)."""
    return undo_cuidado_exame_1112(rel, ler(rel))


def solto(texto):
    return texto.replace(N, ' ').replace(WJ, '')


def palavras(fragmento):
    """As palavras que se leem num fragmento de HTML (também dentro do JavaScript dos cartões), em minúsculas."""
    return re.findall(r'[0-9a-zà-ÿ]+', re.sub(r'<[^>]+>', ' ', solto(fragmento).replace('<\\/', '</').replace('\\"', '"')).lower())


def achados_da_troca(t):
    m = re.search(r'achado ([\d, /]+) \(([ABC])\)', t['achado'])
    return {int(n) for n in re.findall(r'\d+', m.group(1))}, m.group(2)


TROCAS = json.loads(ler('scripts/cuidado_exame_20261112.json'))
MANIFESTO = json.loads(ler(MANIFESTO_REL))


class CuidadoExame(unittest.TestCase):
    def test_tabela_das_fases_da_sessao(self):
        app, antes = ler(APP), base(APP)
        self.assertEqual((antes.count(C.FASES_ANTES), app.count(C.FASES_ANTES)), (1, 0))
        m = re.search(r'<h2>Como cabe em 50\xa0minutos\?</h2>(<table class="apoio-tabela" role="table">.*?</table>)(<p>.*?</p>)', app)
        self.assertIsNotNone(m)
        tabela, frase = m.groups()
        self.assertEqual(app.count('<table class="apoio-tabela"'), 1)
        self.assertEqual(re.findall(r'<th scope="col" role="columnheader">(.*?)</th>', tabela), ['Fase', 'Tempo'])
        linhas = re.findall(r'<tr role="row"><th scope="row" role="rowheader">(.*?)</th><td role="cell" data-label="Tempo">(.*?)</td></tr>', tabela)
        self.assertEqual(linhas, [('Aquecer', '10\xa0min'), ('Ler e planear', '8\xa0min'), ('Escrever', '10–⁠20\xa0min'),
                                  ('Corrigir', '7–⁠17\xa0min'), ('Fechar', '5\xa0min')])
        self.assertEqual(tabela.count('<tr role="row">'), 6)
        self.assertIn('<thead role="rowgroup">', tabela)
        self.assertIn('<tbody role="rowgroup">', tabela)
        self.assertEqual(frase, C.FASES_DEPOIS)
        # A cadeia continua entre plicas no JavaScript: nenhuma plica nem quebra de linha no texto novo.
        self.assertNotRegex(tabela + frase, r"['\n]")
        # As palavras são as mesmas, pela mesma ordem: entram «Fase» e «Tempo» (os cabeçalhos) e sai o «e» antes de «fechar», que
        # a tabela substitui.
        velhas, novas = palavras(C.FASES_ANTES), palavras(tabela + frase)
        self.assertEqual(novas[:2], ['fase', 'tempo'])
        k = velhas.index('fechar')
        self.assertEqual(velhas[k - 1], 'e')
        self.assertEqual(novas[2:], velhas[:k - 1] + velhas[k:])
        # A vista já tinha uma tabela e a folha do Exame dá o estilo às duas; a página não carrega a folha das tabelas de apoio.
        self.assertIn('.coverage th,.coverage td{', ler('assets/exame/exame.css'))
        self.assertNotIn('apoios-tabelas.css', ler('exame/index.html'))
        self.assertNotIn('exame/index.html', MANIFESTO['files'])

    def test_listas_novas_das_provas_em_cartoes(self):
        self.assertEqual(sorted(x['i'] for x in C.PROVAS_C), sorted(C_))
        for x in C.PROVAS_C:
            dados = C.dados_da_prova(x['pagina'])
            for rel, antigo, novo in ((x['pagina'], x['antigo'], x['novo']),
                                      (dados, x['antigo'].replace('<\\/', '</'), x['novo'].replace('<\\/', '</'))):
                with self.subTest(achado=x['i'], ficheiro=rel):
                    atual, antes = ler(rel), base(rel)
                    self.assertEqual((antes.count(antigo), atual.count(antigo), atual.count(novo)), (1, 0, 1))
                    # As palavras ficam todas, pela mesma ordem (só muda a maiúscula de «Tipo A» e «Tipo B» no início da linha).
                    self.assertEqual(palavras(antigo), palavras(novo))
                    # A proposta final já prende os pontos dos rótulos («8 pontos:»); mais nenhum espaço invisível no texto novo.
                    self.assertLessEqual(set(re.findall(r'[^\s>]+\xa0[^\s<]+', novo)), {'8\xa0pontos:', '3\xa0pontos:', '2\xa0pontos:'})
                    self.assertNotIn(WJ, novo)
                    self.assertGreater(novo.count('<li>'), antigo.count('<li>'))
            # É a nossa leitura dos critérios: nenhum pedaço da lista nova está num bloco oficial.
            self.assertEqual(sem_oficial(x['novo'].replace('<\\/', '</').replace('\\"', '"')).strip(),
                             x['novo'].replace('<\\/', '</').replace('\\"', '"').strip())

    def test_achados_b_so_com_espacos_invisiveis_e_contagens_da_conferencia(self):
        por_ficheiro = {}
        for t in TROCAS:
            nums, cat = achados_da_troca(t)
            self.assertLessEqual(nums, APLICADOS, t['local'])
            por_ficheiro.setdefault(t['ficheiro'], []).append((t, cat))
            if cat == 'B':
                # Um achado B só troca espaços por U+00A0 e junta U+2060: o texto fica igual, letra a letra.
                self.assertEqual(solto(t['novo']), t['antigo'], t['local'])
                self.assertNotEqual(t['novo'], t['antigo'])
                self.assertTrue(set(C.edicoes(t['antigo'], t['novo'])), t['local'])
                self.assertLessEqual({tipo for _, tipo in C.edicoes(t['antigo'], t['novo'])}, {'nbsp', 'wj'})
        # Ficheiro a ficheiro: sem as trocas A e C, o ficheiro de agora diz o mesmo que a base, letra a letra.
        for rel, lista in por_ficheiro.items():
            with self.subTest(ficheiro=rel):
                esperado = base(rel)
                for t, cat in lista:
                    if cat != 'B':
                        self.assertEqual(esperado.count(t['antigo']), 1)
                        esperado = esperado.replace(t['antigo'], solto(t['novo']))
                self.assertEqual(solto(ler(rel)), solto(esperado))
        # As contagens: fora das provas em cartões, cada par muda exatamente as ocorrências que a conferência contou (com os
        # ajustes que o script explica); nas provas, as que estão em texto nosso, nunca mais do que a conferência contou.
        contas = {}
        for x in C.ACHADOS_B:
            rel = x['ficheiro']
            C.ATUAL = rel
            antes = base(rel)
            if rel == APP:
                antes = antes.replace(C.FASES_ANTES, C.achados_ac()[0]['novo'])
            em_prova = bool(C.PROVA.match(rel))
            self.assertEqual(em_prova, x['i'] in PROVAS)
            if em_prova:
                for c in C.PROVAS_C:
                    if c['pagina'] == rel:
                        antes = antes.replace(c['antigo'], c['novo'])
                        a = antes.index(c['novo'])
                        C.REGIOES_NOVAS[:] = [(a, a + len(c['novo']))]
            total = 0
            for antigo, novo, n in x['pares']:
                onde = C.ocorrencias(antes, antigo, novo, x['pares'])
                if em_prova:
                    total += len(onde) if len(onde) <= n else 0
                else:
                    self.assertEqual(len(onde), n, (rel, antigo))
                # Depois da camada, nenhuma dessas ocorrências fica por prender.
            C.REGIOES_NOVAS[:] = []
            if em_prova:
                contas[x['i']] = (total, sum(p[2] for p in x['pares']))
                self.assertLessEqual(total, contas[x['i']][1])
        C.ATUAL = None
        self.assertEqual(contas, PROVAS_CONTAS)
        # Os pares «por analogia» (referências de exame que o M5 não tinha: Prova, Grupo, item, linha, verso, nível, pontos…)
        # entram, como a conferência os confirmou; ficam marcados no script, para poderem sair em bloco.
        self.assertTrue(all(set(v) <= {p[0] for x in C.ACHADOS_B if x['i'] == i for p in x['pares']} for i, v in C.ANALOGIA.items()))
        self.assertIn(26, C.ANALOGIA)

    def test_sitios_que_nao_mudam(self):
        for rel in MANIFESTO['files']:
            atual, antes = ler(rel), base(rel)
            with self.subTest(ficheiro=rel):
                # Atributos que não se veem, o <title> e os desenhos: iguais à base.
                for padrao in (r'(?:alt|aria-label|title|href|src|content|data-titulo)=\\?"[^"]*"', r'<title>.*?</title>', r'<svg.*?</svg>'):
                    self.assertEqual(re.findall(padrao, atual, re.S), re.findall(padrao, antes, re.S), padrao)
                # O texto de apoio dos aquecimentos (as obras e o resumo que as acompanha).
                apoio = r'<p class=\\"pr\\".*?<\\?/p>'
                self.assertEqual(re.findall(apoio, atual, re.S), re.findall(apoio, antes, re.S))
        # Nas sessões do Exame: o texto das obras (a chave «text») fica como estava, e as perguntas antigas (warmup) também, salvo
        # as quatro opções da pergunta da s19 copiada da M9-F01, que mudam nas duas cópias.
        atual, antes = json.loads(ler(SESSOES)), json.loads(base(SESSOES))

        def textos(x, chave=None):
            if isinstance(x, dict):
                for k, v in x.items():
                    yield from textos(v, k)
            elif isinstance(x, list):
                for v in x:
                    yield from textos(v, chave)
            elif chave == 'text':
                yield x
        self.assertEqual(list(textos(atual)), list(textos(antes)))
        self.assertTrue(list(textos(atual)))
        mudadas = []
        for s, s0 in zip(atual['sessions'], antes['sessions']):
            if s['warmup'] != s0['warmup']:
                mudadas.append(s['id'])
                self.assertEqual(solto(json.dumps(s['warmup'], ensure_ascii=False)), solto(json.dumps(s0['warmup'], ensure_ascii=False)))
                q, q0 = s['warmup'][0], s0['warmup'][0]
                self.assertEqual([k for k in q if q[k] != q0[k]], ['options'])
                self.assertEqual(q['options'], s['correction']['check']['options'])
                self.assertEqual(sum(a != b for a, b in zip(q['options'], q0['options'])), 4)
        self.assertEqual(mudadas, ['s19'])
        # As chaves dos filtros («10.º ano»…) têm de ser iguais nas sessões e no app.js: ficam como estavam.
        self.assertEqual({s['group'] for s in atual['sessions']}, {s['group'] for s in antes['sessions']})
        self.assertFalse(any(N in s['group'] or N in s['id'] or N in s['source']['url'] for s in atual['sessions']))

    def test_texto_oficial_das_provas_como_estava(self):
        por_pasta = {P.pasta: P for P in provas()}
        vistos = 0
        for i, onde in PROVAS.items():
            rel = f'scripts/provas/dados/{onde}.json'
            P = por_pasta[onde.split('/')[0]]
            atual, antes = json.loads(ler(rel)), json.loads(base(rel))
            self.assertEqual({k: v for k, v in atual.items() if k != 'cartoes'}, {k: v for k, v in antes.items() if k != 'cartoes'})
            self.assertEqual(len(atual['cartoes']), len(antes['cartoes']))
            for k, (c, c0) in enumerate(zip(atual['cartoes'], antes['cartoes'])):
                with self.subTest(prova=onde, cartao=k):
                    self.assertEqual(set(c), set(c0))
                    # Os rótulos (pelos quais os testes e o motor reconhecem os itens oficiais), os campos dos exercícios e as
                    # ligações: iguais.
                    for campo in ('t', 'rot', 'g', 'l', 'ver', 'frase', 'palavras', 'passos', 'linhas', 'cita', 'trecho', 'certas', 'c', 'v'):
                        self.assertEqual(c.get(campo), c0.get(campo), campo)
                    # Um item oficial fica como está, inteiro, salvo o retorno, que é nosso.
                    if OFICIAL.search(c.get('rot', '')):
                        for campo in ('p', 'o', 'pares', 'lacunas'):
                            self.assertEqual(c.get(campo), c0.get(campo), campo)
                    cadeia, cadeia0 = json.dumps(c, ensure_ascii=False), json.dumps(c0, ensure_ascii=False)
                    # As citações entre «» ficam como estavam.
                    self.assertEqual(re.findall(r'«[^«»]*»', cadeia), re.findall(r'«[^«»]*»', cadeia0))
                    if c['t'] != 'ler':
                        continue
                    h, h0 = c['html'], c0['html']
                    # Os blocos que reproduzem a prova ou os critérios (os de tests/test_provas_cartoes.py): iguais, letra a letra.
                    for padrao in (r'<div class="v prova-l[^"]*">.*?</div>', r'<p class="gl">.*?</p>', r'<p class="papel-q">.*?</p>',
                                   r'<table class="(?:empilha grelha|cl)">.*?</table>', r'<ul class="(?:prova-lista|papel-l)">.*?</ul>',
                                   r'<ol class="prova-obs">.*?</ol>'):
                        self.assertEqual(re.findall(padrao, h, re.S), re.findall(padrao, h0, re.S), padrao)
                    if c.get('rot') == 'A prova':
                        self.assertEqual(re.sub(r'<p class="fonte">.*?</p>', '', h, flags=re.S), re.sub(r'<p class="fonte">.*?</p>', '', h0, flags=re.S))
                    # Nenhum pedaço com um espaço preso está, letra a letra, na transcrição da prova ou dos critérios.
                    for pedaco in segmentos(h):
                        for parte in re.split(r'[«»]', pedaco):
                            if N in parte or WJ in parte:
                                vistos += 1
                                self.assertFalse(P.oficial(solto(parte)), parte)
        self.assertGreater(vistos, 100)
        # As transcrições conferidas, a secção das provas e a configuração do gerador não estão na camada.
        for rel in MANIFESTO['files']:
            self.assertNotRegex(rel, r'tests/fixtures/prova-|prova\.json$|seccao\.json$|scripts/provas/gerar\.py|^exame/provas/index\.html$')

    def test_paginas_geradas_saem_iguais_da_origem(self):
        bancos = sorted((ROOT / 'docs/pedagogia/exame-aquecimentos').glob('s*.json'))
        self.assertEqual(len(bancos), 27)
        na_camada = 0
        for p in bancos:
            pagina = f'exame/aquecimentos/{p.stem}/index.html'
            with self.subTest(sessao=p.stem):
                self.assertEqual(ler(pagina), exame_aquecimentos.pagina(json.loads(p.read_text('utf-8'))))
                # A página e o banco entram juntos na camada, ou nenhum dos dois.
                self.assertEqual(pagina in MANIFESTO['files'], p.relative_to(ROOT).as_posix() in MANIFESTO['files'])
                na_camada += pagina in MANIFESTO['files']
        self.assertEqual(na_camada, 14)
        r = subprocess.run([sys.executable, 'scripts/exame_aquecimentos.py', '--check'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = subprocess.run([sys.executable, 'scripts/provas/gerar.py', '--verificar'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Tudo igual ao que está na árvore.', r.stdout)
        for onde in PROVAS.values():
            self.assertIn(f'exame/provas/{onde}/index.html', MANIFESTO['files'])
            self.assertIn(f'scripts/provas/dados/{onde}.json', MANIFESTO['files'])

    def test_fora_de_ambito_e_recusados(self):
        self.assertEqual((len(A), len(B), len(C_), len(A | B | C_)), (1, 50, 4, 55))
        self.assertFalse((A | B | C_) & RECUSADOS)
        self.assertEqual(len(RECUSADOS), 24)
        achados = set()
        for t in TROCAS:
            achados |= achados_da_troca(t)[0]
        self.assertEqual(achados, APLICADOS)
        self.assertEqual(len(APLICADOS), 50)
        self.assertEqual({x['i'] for x in C.ACHADOS_B} | {x['i'] for x in C.achados_ac()}, APLICADOS)
        # Diapositivos, provas rápidas, questionários e páginas «todos» não mudam (como do M1 ao M9); os treinos do Exame ficam
        # fora desta camada; a secção das provas e a moldura que o gerador escreve também.
        for rel in list(FORA_DE_AMBITO.values()) + list(MOLDURA_DAS_PROVAS.values()):
            self.assertNotIn(rel, MANIFESTO['files'])
            self.assertTrue((ROOT / rel).is_file(), rel)
        for rel in MANIFESTO['files']:
            self.assertNotRegex(rel, r'^diapositivos/|/todos/|^exame/treinos/|quest|prova-rapida|^revisao-m147/|^m\d/|^tarefas/')
        ambito = r'^(?:exame/(?:laboratorio/index\.html|aquecimentos/s\d\d/index\.html|provas/2026-[12]f/grupo-i{1,3}/index\.html)|' \
                 r'docs/pedagogia/exame-aquecimentos/s\d\d\.json|scripts/provas/dados/2026-[12]f/grupo-i{1,3}\.json|' \
                 r'assets/exame/(?:app|laboratorio|dossier)\.js|assets/exame/sessoes\.json|obras/(?:[a-z0-9-]+/)?index\.html|' \
                 r'[123]/index\.html|mapa/index\.html|index\.html)$'
        for rel in MANIFESTO['files']:
            self.assertRegex(rel, ambito)
        # O único texto novo que se vê são os dois cabeçalhos da tabela; nada de palavras proibidas no que a camada escreve.
        for t in TROCAS:
            self.assertNotRegex(t['local'] + t['achado'], r'—|\bprofessor|\bjog[oa]')

    def test_camada_fechada_reversivel_e_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_exame_20261112.json', '--manifesto', MANIFESTO_REL,
                            '--verificar'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), NUMEROS)
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('12/11/2026: decisão 152 do docente («cuidado em todas as lições»), Exame e páginas transversais'))
        self.assertIn('cuidado_exame_20261112', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        m9 = json.loads(ler('tests/fixtures/cuidado-m9-edits-20261112.json'))['files']
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_exame_1112(rel, atual)
                self.assertEqual(sha_lf(b), registo['base_sha256_lf'])
                # Ida e volta: refazer as trocas sobre a base devolve o ficheiro, letra a letra.
                refeito = b
                for e in registo['edits']:
                    self.assertEqual(refeito.count(e['old']), e['occurrences'], (rel, e['location']))
                    refeito = refeito.replace(e['old'], e['new'])
                self.assertEqual(refeito, atual)
                for e in registo['edits']:
                    self.assertEqual(atual.count(e['new']), e['occurrences'], (rel, e['location']))
                    self.assertEqual(atual.replace(e['new'], '\0').count(e['old']), 0, (rel, e['location']))
                # A camada de baixo (a decisão 152 no M9) continua a desfazer-se por baixo desta; só partilham as sessões do Exame.
                if rel in m9:
                    self.assertEqual(rel, SESSOES)
                    self.assertEqual(sha_lf(b), m9[rel]['after_sha256_lf'])
                    self.assertEqual(sha_lf(undo_cuidado_m9_1112(rel, atual)), m9[rel]['base_sha256_lf'])
                else:
                    self.assertEqual(undo_cuidado_m9_1112(rel, atual), b)
        self.assertIn(SESSOES, m['files'])
        # No topo das camadas, por cima da decisão 152 no M9, e registada onde as outras estão.
        self.assertEqual(verificar_camadas.LAYERS[0], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('cuidado_m9_20261112', 'cuidado-m9-edits-20261112'))
        self.assertEqual(len(verificar_camadas.LAYERS), 44)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 44)
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-exame-edits-20261112.json'), sala.index('cuidado-m9-edits-20261112.json'))
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_cuidado_exame_1112(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_cuidado_m9_1112\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_cuidado_exame_1112\(path, text\)\n')
        for script in ('cartaz_indices_148_20261106', 'indices_acertos_20261107', 'creditos_i_pt1_20261107'):
            s = ler(f'scripts/{script}.py')
            self.assertLess(s.index("json.loads(CUIDADO_EXAME.read_text"), s.index("json.loads(CUIDADO_M9.read_text"), script)
        # Nos fluxos e nos outros testes, a cadeia de desfazer começa por esta camada, sem nada entre ela e a do M9.
        ex, m9_rel = MANIFESTO_REL, 'tests/fixtures/cuidado-m9-edits-20261112.json'
        cadeias = 0
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name == 'test_cuidado_exame.py':
                continue
            texto = '\n'.join(linha for linha in p.read_text('utf-8').split('\n') if not linha.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + m9_rel), plano.count(f'--desfazer-antes {ex} --desfazer-antes {m9_rel}'))
                self.assertEqual(plano.count('--desfazer-antes {m9}'), plano.count('--desfazer-antes {ex} --desfazer-antes {m9}'))
                cadeias += plano.count(f'--desfazer-antes {ex} --desfazer-antes {m9_rel}') + plano.count('--desfazer-antes {ex} --desfazer-antes {m9}')
        self.assertGreater(cadeias, 80)
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_exame_20261112.json --manifesto {ex} --verificar\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m9_20261112.json --manifesto {m9_rel} --verificar --desfazer-antes {ex}\n', tarefas)
        apoios = ler('.github/workflows/pt-apoios-qa.yml')
        self.assertIn("run: python -m unittest discover -s tests -p 'test_cuidado_exame.py' -v", apoios)
        self.assertIn('run: python tests/browser_cuidado_exame.py', apoios)
        self.assertLess(apoios.index('run: python tests/browser_cuidado_m9.py'), apoios.index('run: python tests/browser_cuidado_exame.py'))

    def test_gerador_da_o_mesmo_json(self):
        todas, _, n = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(n, len(MANIFESTO['files']))


if __name__ == '__main__':
    unittest.main()
