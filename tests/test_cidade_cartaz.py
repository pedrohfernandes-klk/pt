"""2026-11-08: cartaz «Ler a cidade» na entrada do Português e nome novo da secção nas páginas publicadas.

Pedido do utilizador: «quero que [Ler a cidade] tenha um banner em português». Camada literal fechada cidade_cartaz_20261108
(scripts/cidade_cartaz_20261108.py constrói scripts/cidade_cartaz_20261108.json; o manifesto é
tests/fixtures/cidade-cartaz-edits-20261108.json). Este teste confere que:

* a camada está aplicada, confere-se sem nada por cima e é reversível letra a letra (com as contagens exatas do manifesto e os
  hashes da base e do depois), e o gerador dá o mesmo JSON;
* fica registada como a camada mais recente (por cima dos créditos atrás de um «i» do pedido pt-1) em scripts/verificar_camadas.py,
  nas cadeias de desfazer de tests/auditoria_20261028.py e de scripts/desligar_sala.py, nas cadeias dos workflows e dos testes e
  nos testes de navegador que montam o «antes» da entrada e dos índices; o workflow dos cartazes confere-a e corre o seu teste de
  navegador;
* o cartaz vem logo a seguir ao do Atlas, com as classes dele, o texto exato, as duas ligações para o Lente e os 14 números das
  missões pela ordem; a linha pequena «Português × Cidadania · Ler a cidade: …» saiu;
* não sobra nenhuma ocorrência do nome antigo («A cidade antes da aula», em qualquer caixa) nas páginas publicadas (HTML e JS),
  fora da página do endereço antigo (bairro/index.html), que fica como estava; a frase da sugestão «continua» diz o nome novo;
* o texto novo segue as regras da casa: nenhum «·» novo dentro de frases, nenhum travessão «—», e nada de «jogar», «jogo»,
  «ficha», «folha» ou «professor».
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import glob
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import unittest

from auditoria_20261028 import undo_cidade_cartaz_0811, undo_creditos_i_pt1_0711

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/cidade_cartaz_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cidade-cartaz-edits-20261108.json'
MANIFESTO_REL = 'tests/fixtures/cidade-cartaz-edits-20261108.json'
BASE_COMMIT = '4833c23655061e0cc2a366edee1b2b21eaea6237'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/cidade/'
NUMEROS = ['01', '02', '03', '04', '05', '06', '08', '10', '11', '12', '15', '16', '17', '18']
FRASE_ANTIGA = 'A cidade antes da aula: {nmissoes} missões feitas, relê o teu caderno'
FRASE_NOVA = 'Ler a cidade: {nmissoes} missões feitas, relê o teu caderno'
ESTILO = ('<style>.atlas-poster-art.cidade-poster-art{grid-template-columns:repeat(4,minmax(0,1fr));font-size:1.15rem}'
          '@media(max-width:760px){.atlas-poster-art.cidade-poster-art{grid-template-columns:repeat(3,minmax(0,1fr));font-size:.9rem}'
          '.cidade-poster-art span{min-height:36px;padding:4px}}@media(max-width:520px){.atlas-poster-art.cidade-poster-art{'
          'grid-template-columns:repeat(7,minmax(0,1fr));font-size:.85rem}}</style>')
CARTAZ = (
    '<section class="atlas-poster cidade-poster" aria-labelledby="cidade-poster-title"><div class="atlas-poster-copy"><p '
    'class="portal-kicker">Português × Cidadania</p><h2 id="cidade-poster-title">Ler a<br>cidade<span aria-hidden="true">↗</span>'
    '</h2><p>Uma rua pode ser lida como um texto e discutida como um espaço de todos. São 14 missões, no bairro ou a partir das '
    'fotografias.</p><nav aria-label="Entradas de Ler a cidade"><a href="https://pedrohfernandes-klk.github.io/lente/cidade/">'
    'Entrar na cidade <span aria-hidden="true">→</span></a><a href="https://pedrohfernandes-klk.github.io/lente/cidade/#m01">Ver '
    'as missões <span aria-hidden="true">→</span></a></nav></div><div class="atlas-poster-art cidade-poster-art" '
    'aria-hidden="true"><span>01</span><span>02</span><span>03</span><span>04</span><span>05</span><span>06</span><span>08</span>'
    '<span>10</span><span>11</span><span>12</span><span>15</span><span>16</span><span>17</span><span>18</span></div></section>')
LINHA = ('<p class="sp-credit"><strong>Português × Cidadania</strong> · <a href="https://pedrohfernandes-klk.github.io/lente/cidade/">'
         'Ler a cidade: observar, criar e discutir o espaço comum →</a></p>')
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)
FORA = 'bairro/index.html'
BAIRRO_SHA256 = '5cd4233fdb5d4f95701363c3bc15fba839479cf285f5ca6eeda4390bfd2cbccb'


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def publicadas():
    """As páginas publicadas: HTML e JS (fora das pastas do repositório que não se publicam como páginas)."""
    fora = {'.git', 'node_modules', 'scripts', 'tests', 'docs'}
    for pasta, subpastas, ficheiros in os.walk(ROOT):
        subpastas[:] = sorted(n for n in subpastas if not (Path(pasta) == ROOT and n in fora) and n not in ('.git', 'node_modules'))
        for nome in sorted(ficheiros):
            if nome.endswith(('.html', '.js')):
                yield (Path(pasta) / nome).relative_to(ROOT).as_posix()


class Seccao(HTMLParser):
    """O texto e as ligações de um elemento (pelo id ou pela classe), com o texto escondido aos leitores de ecrã à parte."""

    def __init__(self, classe):
        super().__init__(convert_charrefs=True)
        self.classe, self.dentro, self.pilha, self.texto, self.ligacoes, self.numeros, self.na_arte = classe, 0, [], [], [], [], 0
        self.ligacao = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.dentro:
            # (cada elemento separa as palavras, como no ecrã: «Cidadania» e «Ler» não se colam)
            self.texto.append(' ')
            self.dentro += 1
            self.pilha.append((tag, a))
            if 'cidade-poster-art' in (a.get('class') or '').split():
                self.na_arte = self.dentro
            if tag == 'a':
                self.ligacao = [a.get('href'), '']
            if tag == 'br':
                self.dentro -= 1
                self.pilha.pop()
                self.texto.append(' ')
        elif tag == 'section' and self.classe in (a.get('class') or '').split():
            self.dentro = 1
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        if not self.dentro:
            return
        self.texto.append(' ')
        if tag == 'a' and self.ligacao:
            self.ligacoes.append((self.ligacao[0], re.sub(r'\s+', ' ', self.ligacao[1]).strip()))
            self.ligacao = None
        if self.na_arte == self.dentro:
            self.na_arte = 0
        self.dentro -= 1
        self.pilha.pop()

    def handle_data(self, data):
        if not self.dentro:
            return
        escondido = any(a.get('aria-hidden') == 'true' for _, a in self.pilha)
        if self.na_arte and self.pilha[-1][0] == 'span':
            self.numeros.append(data)
        if not escondido:
            self.texto.append(data)
            if self.ligacao:
                self.ligacao[1] += data


class CidadeCartaz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trocas = json.loads(CAMADA.read_text('utf-8'))
        cls.manifesto = json.loads(MANIFESTO.read_text('utf-8'))
        cls.entrada = ler('index.html')

    def test_camada_aplicada_fechada_e_reversivel(self):
        # A camada mais recente confere-se sem nada por cima, com as contagens exatas do manifesto.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', str(CAMADA.relative_to(ROOT)), '--manifesto', MANIFESTO_REL,
                            '--verificar'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('246 trocas em 242 ficheiros: 246 aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        m = self.manifesto
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('08/11/2026: pedido do utilizador'))
        self.assertIn('creditos_i_pt1_20261107', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in self.trocas})
        self.assertNotIn(FORA, m['files'])
        for t in self.trocas:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
            self.assertTrue(t['achado'].startswith('08/11/2026: pedido do utilizador, «quero que [Ler a cidade] tenha um banner'))
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = undo_cidade_cartaz_0811(rel, atual)
                self.assertEqual(sha_lf(base), registo['base_sha256_lf'])
                # Ida e volta: refazer as trocas sobre a base devolve a página, letra a letra.
                refeito = base
                for e in registo['edits']:
                    self.assertEqual(refeito.count(e['old']), e['occurrences'], (rel, e['location']))
                    self.assertEqual(refeito.count(e['new']), 0, (rel, e['location']))
                    refeito = refeito.replace(e['old'], e['new'])
                self.assertEqual(refeito, atual)
                for e in registo['edits']:
                    self.assertEqual(atual.count(e['new']), e['occurrences'], (rel, e['location']))
                    self.assertEqual(atual.replace(e['new'], '\0').count(e['old']), 0, (rel, e['location']))
                # A camada de baixo (os créditos do pedido pt-1) continua a desfazer-se por baixo desta.
                undo_creditos_i_pt1_0711(rel, atual)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('cidade_cartaz', ROOT / 'scripts/cidade_cartaz_20261108.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        self.assertEqual(modulo.construir(), self.trocas)

    def test_contagens_por_familia(self):
        familias = Counter(t['local'].split(',')[0] for t in self.trocas)
        self.assertEqual(familias, Counter({'C1': 2, 'C2': 238, 'C3': 6}))
        self.assertTrue(all(t['ocorrencias'] == 1 for t in self.trocas))
        self.assertEqual(Counter(t['ficheiro'] for t in self.trocas if t['local'].startswith('C3')),
                         Counter({'m2/gram-subordinadas/index.html': 3, '1/todos/index.html': 1, '2/todos/index.html': 1,
                                  '3/todos/index.html': 1}))
        self.assertEqual([t['local'].split(',')[0] for t in self.trocas if t['ficheiro'] == 'index.html'], ['C1', 'C1', 'C2'])

    def test_registada_como_a_camada_mais_recente(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        self.assertEqual(verificar_camadas.LAYERS[0], ('cidade_cartaz_20261108', 'cidade-cartaz-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('creditos_i_pt1_20261107', 'creditos-i-pt1-edits-20261107'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_creditos_i_pt1_0711'):]
        self.assertLess(corpo.index('undo_cidade_cartaz_0811(path, text)'), corpo.index('_CREDITOS_I_PT1_0711.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cidade-cartaz-edits-20261108.json'), sala.index('creditos-i-pt1-edits-20261107.json'))
        # Em cada cadeia dos workflows, esta camada desfaz-se primeiro, logo a seguir a --verificar, e logo antes do pt-1.
        meu, pt1 = MANIFESTO_REL, 'tests/fixtures/creditos-i-pt1-edits-20261107.json'
        cadeias = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + pt1 not in linha:
                    continue
                cadeias += 1
                self.assertIn(f'--verificar --desfazer-antes {meu} --desfazer-antes {pt1}', linha, wf)
        # As 13 cadeias de antes e a da decisão 152 no M1.
        self.assertEqual(cadeias, 14)
        # O pt-1, que no workflow dos cartazes se conferia sem nada por cima, desfaz primeiro esta camada.
        self.assertIn(f'scripts/creditos_i_pt1_20261107.json --manifesto {pt1} --verificar --desfazer-antes {meu}\n',
                      ler('.github/workflows/cartaz-qa.yml'))
        # Nas cadeias dos testes, esta camada vem logo antes da do pt-1, sem outra pelo meio.
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pt-1 e da decisão 152 no M1 conferem as cadeias com frases (em cadeias de texto partidas em
            # várias linhas), não as correm; ficam de fora pela mesma razão.
            if p.name in ('test_cidade_cartaz.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + pt1), plano.count(f'--desfazer-antes {meu} --desfazer-antes {pt1}'))
        self.assertIn(f"(ROOT/'{meu}',ROOT/'{pt1}',", ler('tests/test_task_routes_closure.py'))
        # Os testes de navegador que montam o «antes» da entrada e dos índices desfazem-na primeiro.
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            with self.subTest(teste=rel):
                self.assertLess(texto.index('((cidadeCartaz['), texto.index('((creditosPt1['))
        texto = ler('tests/browser_cartaz_cabecalho.cjs')
        self.assertLess(texto.index("cidadeCartaz.files['index.html']"), texto.index("creditosPt1.files['index.html']"))
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cidadeCartaz[rel]'), corpo.index('manifesto[rel].edits'))
        gerador = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador.index('CIDADE_CARTAZ.read_text'), gerador.index('CREDITOS_PT1.read_text'))
        # O workflow dos cartazes confere-a sem nada por cima e corre o seu teste de navegador; os caminhos levam-na.
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn('      - run: python scripts/aplicar_trocas.py scripts/cidade_cartaz_20261108.json --manifesto '
                      f'{meu} --verificar\n', cartaz)
        self.assertIn('      - run: node tests/browser_cidade_cartaz.cjs\n', cartaz)
        self.assertLess(cartaz.index('node tests/browser_creditos_i_pt1.cjs'), cartaz.index('node tests/browser_cidade_cartaz.cjs'))
        for caminho in ('scripts/cidade_cartaz_20261108.*', meu, 'tests/*cidade_cartaz*', 'assets/retro-portals.css', 'index.html'):
            self.assertEqual(cartaz.count(f"'{caminho}'"), 2, caminho)
        for wf in ('pt-tarefas-qa.yml', 'pt-exame-laboratorio-qa.yml'):
            texto = ler('.github/workflows/' + wf)
            for caminho in ('scripts/cidade_cartaz_20261108.*', meu, 'tests/test_cidade_cartaz.py'):
                self.assertIn(f"'{caminho}'", texto, wf)

    def test_cartaz_logo_a_seguir_ao_do_atlas_com_o_texto_exato(self):
        s = self.entrada
        self.assertEqual(s.count(CARTAZ), 1)
        self.assertEqual(s.count(ESTILO + CARTAZ), 1)
        # Logo a seguir ao fim do cartaz do Atlas e logo antes do portal do Lente.
        self.assertEqual(s.count('<span>TL</span></div></section>' + ESTILO + CARTAZ
                                 + '<nav class="site-portal-wrap" aria-label="Explorar o Lente">'), 1)
        self.assertEqual(len(re.findall(r'<section class="atlas-poster[ "]', s)), 2)
        self.assertEqual(s.count('id="cidade-poster-title"'), 1)
        # As regras próprias só tocam a grelha dos números do cartaz novo.
        regras = re.findall(r'([^{}]+)\{[^{}]*\}', re.sub(r'@media\([^)]*\)\{', '', ESTILO[len('<style>'):-len('</style>')]))
        self.assertTrue(regras)
        self.assertTrue(all('cidade-poster-art' in r for r in regras), regras)
        p = Seccao('cidade-poster')
        p.feed(s)
        texto = re.sub(r'\s+', ' ', ''.join(p.texto)).strip()
        self.assertEqual(texto, 'Português × Cidadania Ler a cidade Uma rua pode ser lida como um texto e discutida como um espaço de '
                                'todos. São 14 missões, no bairro ou a partir das fotografias. Entrar na cidade Ver as missões')
        self.assertEqual(p.ligacoes, [(LENTE, 'Entrar na cidade'), (LENTE + '#m01', 'Ver as missões')])
        self.assertEqual(p.numeros, NUMEROS)
        self.assertEqual(len(p.numeros), 14)
        self.assertEqual(sorted(p.numeros, key=int), NUMEROS)

    def test_a_linha_pequena_saiu(self):
        self.assertNotIn(LINHA, self.entrada)
        self.assertEqual(self.entrada.count('class="sp-credit"'), 0)
        self.assertEqual(self.entrada.count('Ler a cidade: observar, criar e discutir o espaço comum'), 0)
        # Saiu só a linha: o «i» da fotografia e o fim do portal ficam encostados, como antes dela.
        self.assertIn(LINHA, undo_cidade_cartaz_0811('index.html', self.entrada))
        self.assertEqual(self.entrada.count('Library of Congress</a>.</p></details></nav>'), 1)
        # Para a secção, a entrada liga agora pelo cartaz (duas ligações) e pelas sugestões; a ligação da linha era a única.
        self.assertEqual(undo_cidade_cartaz_0811('index.html', self.entrada).count(f'href="{LENTE}"'), 1)
        self.assertEqual(self.entrada.count(f'href="{LENTE}"'), 1)
        self.assertEqual(self.entrada.count(f'href="{LENTE}#m01"'), 1)

    def test_nome_antigo_nenhures_nas_paginas_publicadas(self):
        restos = []
        for rel in publicadas():
            if rel == FORA:
                continue
            if 'cidade antes da aula' in ler(rel).lower():
                restos.append(rel)
        self.assertEqual(restos, [])
        # Nos JS servidos (assets/**/*.js), também não.
        self.assertTrue(any(r.startswith('assets/') for r in publicadas()))
        # A página do endereço antigo fica como estava: redireciona para o Lente e explica a mudança de nome.
        bairro = ler(FORA)
        self.assertIn('A cidade antes da aula passou para o Lente', bairro)
        # (o hash da página no commit da base, 4833c236; sem depender do histórico do git, que os fluxos não trazem todos)
        self.assertEqual(hashlib.sha256((ROOT / FORA).read_bytes()).hexdigest(), BAIRRO_SHA256)

    def test_frase_da_sugestao_com_o_nome_novo(self):
        com_frase = [t['ficheiro'] for t in self.trocas if t['local'].startswith('C2')]
        self.assertEqual(len(com_frase), 238)
        self.assertIn('index.html', com_frase)
        for rel in com_frase:
            with self.subTest(pagina=rel):
                s = ler(rel)
                self.assertEqual(s.count(FRASE_NOVA), 1)
                self.assertEqual(s.count(FRASE_ANTIGA), 0)
                self.assertEqual(s.count('"completo":[{"frase":"' + FRASE_NOVA + '"}]'), 1)
        for rel in publicadas():
            if rel != FORA:
                with self.subTest(pagina=rel):
                    self.assertNotIn('A cidade antes da aula:', ler(rel))
        # As outras formas: o título, a marca e o rótulo do cartão de sugestão antigo e a ligação das listas «todos».
        s = ler('m2/gram-subordinadas/index.html')
        for forma in ('{"titulo":"Ler a cidade","texto":"Um mapa do bairro', '"A EPI · Ler a cidade"', '"Atlas Lusófono":"Ler a cidade")'):
            self.assertEqual(s.count(forma), 1, forma)
        for ano in (1, 2, 3):
            self.assertEqual(ler(f'{ano}/todos/index.html').count(f'<a href="{LENTE}">Ler a cidade<small>percurso extra'), 1, ano)

    def test_regras_do_texto_novo(self):
        p = Seccao('cidade-poster')
        p.feed(self.entrada)
        visivel = ''.join(p.texto)
        # No cartaz, nenhum «·» (o pré-título usa «×», como «Português × Cidadania» de antes).
        self.assertNotIn('·', visivel)
        for t in self.trocas:
            with self.subTest(local=t['local'], ficheiro=t['ficheiro']):
                # Nenhum «·» novo (a marca do cartão antigo, «A EPI · …», já o tinha) e nenhum travessão.
                self.assertLessEqual(t['novo'].count('·'), t['antigo'].count('·'))
                self.assertNotIn('—', t['novo'])
                novas = set(m.lower() for m in PROIBIDAS.findall(t['novo'])) - set(m.lower() for m in PROIBIDAS.findall(t['antigo']))
                self.assertEqual(novas, set())
        self.assertIsNone(PROIBIDAS.search(visivel))
        self.assertNotIn('—', visivel)
        for frase in (FRASE_NOVA, 'Uma rua pode ser lida como um texto e discutida como um espaço de todos.',
                      'São 14 missões, no bairro ou a partir das fotografias.'):
            self.assertNotIn('·', frase)
            self.assertIsNone(PROIBIDAS.search(frase))


if __name__ == '__main__':
    unittest.main()
