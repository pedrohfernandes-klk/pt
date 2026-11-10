"""08/11/2026: cartaz «Ler a cidade» na entrada do Português e nome novo da secção nas páginas publicadas.

Pedido do utilizador: «quero que [Ler a cidade] tenha um banner em português». Camada literal fechada cidade_cartaz_20261108
(scripts/cidade_cartaz_20261108.py constrói scripts/cidade_cartaz_20261108.json; o manifesto é
tests/fixtures/cidade-cartaz-edits-20261108.json). Este teste confere que:

* a camada está aplicada, confere-se sem nada por cima e é reversível letra a letra (com as contagens exatas do manifesto e os
  hashes da base e do depois), e o gerador dá o mesmo JSON;
* fica registada como a camada mais recente (por cima dos créditos atrás de um «i» do pedido pt-1) em scripts/verificar_camadas.py,
  nas cadeias de desfazer de tests/auditoria_20261028.py e de scripts/desligar_sala.py, nas cadeias dos workflows e dos testes e
  nos testes de navegador que montam o «antes» da entrada e dos índices; o workflow dos cartazes confere-a e corre o seu teste de
  navegador;
* o cartaz vem logo a seguir ao do Atlas, com o texto exato e as duas ligações para o Lente; a linha pequena «Português ×
  Cidadania · Ler a cidade: …» saiu;
* 08/11/2026 (revisão): o utilizador achou a primeira versão «visualmente igual ao do Atlas... estranho e mau». O cartaz deixa as
  classes do cartaz do Atlas e a grelha dos 14 números (essas conferências saem) e passa a ter cara própria: a fotografia de Lisboa
  vista do Tejo em 1907 (src, width, height e o alt exatos, os do cartão «Ler a cidade.» da entrada do Lente), a etiqueta, e o
  crédito exato num «i» com a ligação da Biblioteca do Congresso; as regras do cartaz só tocam as classes dele;
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
# 08/11/2026: por cima desta camada fica a decisão 152 no M2 (camada cuidado_m2_20261108).
from auditoria_20261028 import undo_cuidado_m2_0811

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/cidade_cartaz_20261108.json'
MANIFESTO = ROOT / 'tests/fixtures/cidade-cartaz-edits-20261108.json'
MANIFESTO_REL = 'tests/fixtures/cidade-cartaz-edits-20261108.json'
BASE_COMMIT = '4833c23655061e0cc2a366edee1b2b21eaea6237'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/cidade/'
FRASE_ANTIGA = 'A cidade antes da aula: {nmissoes} missões feitas, relê o teu caderno'
FRASE_NOVA = 'Ler a cidade: {nmissoes} missões feitas, relê o teu caderno'
# 08/11/2026 (revisão): o cartaz com fotografia e desenho próprios, letra a letra (sem a folha, que se confere à parte). A fotografia,
# o alt, a etiqueta e o crédito são os do cartão «Ler a cidade.» da entrada do Lente (os da revisão do Lente); o «i» tem o formato
# do da fotografia de Muybridge na entrada do Português (a ligação diz «Library of Congress», com o ponto final).
FOTO = 'img/arquivo/tejo-1907-vela-e-cidade.jpg'
ALT = 'Barco à vela no Tejo; atrás, o cais e a cidade.'
ETIQUETA = 'Lisboa vista do Tejo, 1907'
FONTE = 'https://www.loc.gov/item/2021640928/'
CREDITO = ('Metade de um estereograma de 1907, com direitos de J. J. Killelea &amp; Co. e publicado por H. C. White Co. Domínio '
           f'público. <a href="{FONTE}">Library of Congress</a>.')
I_CREDITO = ('<details class="info-i info-i--linha" name="info-i"><summary aria-label="Créditos da fotografia: Lisboa vista do Tejo">'
             f'<span aria-hidden="true">i</span></summary><p class="info-i-texto">{CREDITO}</p></details>')
CARTAZ = (
    '<section class="cidade-cartaz" aria-labelledby="cidade-cartaz-titulo"><div class="cidade-cartaz-foto"><div '
    f'class="cidade-cartaz-imagem"><img src="{FOTO}" alt="{ALT}" width="1160" height="773" loading="lazy" decoding="async"><span '
    f'class="cidade-cartaz-etiqueta">{ETIQUETA}</span></div>{I_CREDITO}</div><div class="cidade-cartaz-texto"><p '
    'class="portal-kicker">Português × Cidadania</p><h2 id="cidade-cartaz-titulo">Ler a cidade</h2><p>Uma rua pode ser lida como '
    'um texto e discutida como um espaço de todos. São 14 missões, no bairro ou a partir das fotografias.</p><nav '
    'aria-label="Entradas de Ler a cidade"><a href="https://pedrohfernandes-klk.github.io/lente/cidade/">Entrar na cidade <span '
    'aria-hidden="true">→</span></a><a href="https://pedrohfernandes-klk.github.io/lente/cidade/#m01">Ver as missões <span '
    'aria-hidden="true">→</span></a></nav></div></section>')
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
    """08/11/2026 (revisão): o que um leitor encontra numa secção (pela classe): o texto à vista (sem o que é decorativo, com
    aria-hidden, e sem o crédito dentro do «i»), o texto do crédito, as ligações (com o sítio onde estão), as imagens e as classes
    de todos os elementos. Era o parser dos 14 números da primeira versão."""
    VAZIOS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

    def __init__(self, classe):
        super().__init__(convert_charrefs=True)
        self.classe, self.pilha, self.texto, self.credito, self.ligacoes, self.imagens, self.classes = classe, [], [], [], [], [], []
        self.ligacao = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if not self.pilha:
            if tag == 'section' and self.classe in (a.get('class') or '').split():
                self.pilha.append((tag, a))
                self.classes += (a.get('class') or '').split()
            return
        # (cada elemento separa as palavras, como no ecrã: «Cidadania» e «Ler» não se colam)
        self.texto.append(' ')
        self.classes += (a.get('class') or '').split()
        if tag == 'img':
            self.imagens.append(a)
        if tag in self.VAZIOS:
            return
        self.pilha.append((tag, a))
        if tag == 'a':
            self.ligacao = [a.get('href'), '', any(t == 'details' for t, _ in self.pilha)]

    def handle_endtag(self, tag):
        if not self.pilha or tag in self.VAZIOS:
            return
        self.texto.append(' ')
        if tag == 'a' and self.ligacao:
            self.ligacoes.append((self.ligacao[0], re.sub(r'\s+', ' ', self.ligacao[1]).strip(), self.ligacao[2]))
            self.ligacao = None
        self.pilha.pop()

    def handle_data(self, data):
        if not self.pilha:
            return
        if any(t == 'details' for t, _ in self.pilha):
            if not any(t == 'summary' for t, _ in self.pilha):
                self.credito.append(data)
        elif not any(a.get('aria-hidden') == 'true' for _, a in self.pilha):
            self.texto.append(data)
        if self.ligacao and not any(a.get('aria-hidden') == 'true' for _, a in self.pilha):
            self.ligacao[1] += data


class CidadeCartaz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trocas = json.loads(CAMADA.read_text('utf-8'))
        cls.manifesto = json.loads(MANIFESTO.read_text('utf-8'))
        cls.entrada = ler('index.html')

    def test_camada_aplicada_fechada_e_reversivel(self):
        # A camada mais recente confere-se sem nada por cima, com as contagens exatas do manifesto.
        # 08/11/2026: por cima dela fica agora a decisão 152 no M2 (cuidado_m2_20261108, que também mexe nas lições e no índice do
        # M2); desfaz-se primeiro, com a mesma exigência, e as contagens são as mesmas.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', str(CAMADA.relative_to(ROOT)), '--manifesto', MANIFESTO_REL,
                            # 08/11/2026: a decisão 152 no M3 (cuidado_m3_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M3, incluindo o índice, o guia e o mapa do módulo) passa a camada mais recente, por cima da decisão 152 no M2; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M4 (cuidado_m4_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M4, incluindo o índice, o guia, o mapa e o portefólio do módulo) passa a camada mais recente, por cima da decisão 152 no M3; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M5 (cuidado_m5_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M5, incluindo o índice, o guia, o mapa e o portefólio do módulo, e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M4; desfaz-se primeiro, com a mesma exigência.
                            '--verificar', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json', '--desfazer-antes', 'tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m3-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m2-edits-20261108.json'], cwd=ROOT,
                           capture_output=True, text=True, encoding='utf-8')
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
                # 08/11/2026: a página como esta camada a deixou: com a camada de cima (cuidado_m2_20261108) desfeita, com contagem
                # estrita; undo_cidade_cartaz_0811 desfaz as duas, a partir da página inteira.
                # 08/11/2026: undo_cuidado_m2_0811 desfaz agora primeiro a decisão 152 no M3 (cuidado_m3_20261108), que está por cima
                # de todas, com a mesma contagem estrita.
                atual = undo_cuidado_m2_0811(rel, ler(rel))
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = undo_cidade_cartaz_0811(rel, ler(rel))
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
                # 08/11/2026: na página inteira, porque a cadeia de desfazer começa agora pela decisão 152 no M2.
                undo_creditos_i_pt1_0711(rel, ler(rel))

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
        # 08/11/2026: por cima desta camada fica a decisão 152 no M2 (cuidado_m2_20261108): esta passa a segunda, logo por baixo
        # dela, e em cada cadeia desfaz-se logo a seguir a ela, sem nada pelo meio.
        # 08/11/2026: por cima da decisão 152 no M2 fica a decisão 152 no M3 (cuidado_m3_20261108): esta camada passa a terceira.
        # 08/11/2026: por cima da decisão 152 no M3 fica a decisão 152 no M4 (cuidado_m4_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 08/11/2026: por cima da decisão 152 no M4 fica a decisão 152 no M5 (cuidado_m5_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('cuidado_m4_20261108', 'cuidado-m4-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('cuidado_m3_20261108', 'cuidado-m3-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('cuidado_m2_20261108', 'cuidado-m2-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cidade_cartaz_20261108', 'cidade-cartaz-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('creditos_i_pt1_20261107', 'creditos-i-pt1-edits-20261107'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_creditos_i_pt1_0711'):]
        self.assertLess(corpo.index('undo_cidade_cartaz_0811(path, text)'), corpo.index('_CREDITOS_I_PT1_0711.get('))
        # 08/11/2026: e esta camada desfaz primeiro a da decisão 152 no M2, que está por cima dela.
        corpo = auditoria[auditoria.index('def undo_cidade_cartaz_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m2_0811(path, text)'), corpo.index('_CIDADE_CARTAZ_0811.get('))
        # 08/11/2026: e a da decisão 152 no M2 desfaz primeiro a da decisão 152 no M3, que está por cima de todas.
        corpo = auditoria[auditoria.index('def undo_cuidado_m2_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m3_0811(path, text)'), corpo.index('_CUIDADO_M2_0811.get('))
        # 08/11/2026: e a decisão 152 no M3 chama primeiro a decisão 152 no M4, que está por cima.
        corpo = auditoria[auditoria.index('def undo_cuidado_m3_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m4_0811(path, text)'), corpo.index('_CUIDADO_M3_0811.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cidade-cartaz-edits-20261108.json'), sala.index('creditos-i-pt1-edits-20261107.json'))
        self.assertLess(sala.index('cuidado-m2-edits-20261108.json'), sala.index('cidade-cartaz-edits-20261108.json'))
        # 08/11/2026: e, antes da do M2, a decisão 152 no M3.
        self.assertLess(sala.index('cuidado-m3-edits-20261108.json'), sala.index('cuidado-m2-edits-20261108.json'))
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4, a camada mais recente.
        self.assertLess(sala.index('cuidado-m4-edits-20261108.json'), sala.index('cuidado-m3-edits-20261108.json'))
        # 08/11/2026: e, antes da do M4, a decisão 152 no M5, agora a mais recente.
        self.assertLess(sala.index('cuidado-m5-edits-20261108.json'), sala.index('cuidado-m4-edits-20261108.json'))
        # Em cada cadeia dos workflows, esta camada desfaz-se primeiro, logo a seguir a --verificar, e logo antes do pt-1.
        # 08/11/2026: logo a seguir à decisão 152 no M2, que se desfaz primeiro, logo a seguir a --verificar.
        meu, pt1 = MANIFESTO_REL, 'tests/fixtures/creditos-i-pt1-edits-20261107.json'
        m2 = 'tests/fixtures/cuidado-m2-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M2, a decisão 152 no M3 (cuidado_m3_20261108), a primeira, logo a seguir a --verificar.
        m3 = 'tests/fixtures/cuidado-m3-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M3, a decisão 152 no M4 (cuidado_m4_20261108), a primeira, logo a seguir a --verificar.
        m4 = 'tests/fixtures/cuidado-m4-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M4, a decisão 152 no M5 (cuidado_m5_20261108), agora a primeira, logo a seguir a --verificar.
        m5 = 'tests/fixtures/cuidado-m5-edits-20261108.json'
        cadeias = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + pt1 not in linha:
                    continue
                cadeias += 1
                # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
                # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
                self.assertIn(f'--verificar --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {m3} --desfazer-antes {m2} --desfazer-antes {meu} '
                              f'--desfazer-antes {pt1}', linha, wf)
        # As 13 cadeias de antes e a da decisão 152 no M1.
        self.assertEqual(cadeias, 14)
        # O pt-1, que no workflow dos cartazes se conferia sem nada por cima, desfaz primeiro esta camada.
        # 08/11/2026: e, antes desta, a decisão 152 no M2.
        # 08/11/2026: e, antes da do M2, a decisão 152 no M3.
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
        # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
        self.assertIn(f'scripts/creditos_i_pt1_20261107.json --manifesto {pt1} --verificar --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {m3} '
                      f'--desfazer-antes {m2} --desfazer-antes {meu}\n', ler('.github/workflows/cartaz-qa.yml'))
        # Nas cadeias dos testes, esta camada vem logo antes da do pt-1, sem outra pelo meio.
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pt-1 e da decisão 152 no M1 conferem as cadeias com frases (em cadeias de texto partidas em
            # várias linhas), não as correm; ficam de fora pela mesma razão.
            if p.name in ('test_cidade_cartaz.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                # 08/11/2026: e a cadeia começa pela decisão 152 no M2, logo antes desta, sem nada pelo meio.
                # 08/11/2026: e, antes da do M2, a decisão 152 no M3, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes ' + pt1),
                                 # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
                                 # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
                                 plano.count(f'--desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {m3} --desfazer-antes {m2} --desfazer-antes {meu} '
                                             f'--desfazer-antes {pt1}'))
        # 08/11/2026: nas rotas, a decisão 152 no M2 vem primeiro, logo antes desta.
        # 08/11/2026: e, antes dela, a decisão 152 no M3.
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
        # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
        self.assertIn(f"(ROOT/'{m5}',ROOT/'{m4}',ROOT/'{m3}',ROOT/'{m2}',ROOT/'{meu}',ROOT/'{pt1}',", ler('tests/test_task_routes_closure.py'))
        # Os testes de navegador que montam o «antes» da entrada e dos índices desfazem-na primeiro.
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            with self.subTest(teste=rel):
                self.assertLess(texto.index('((cidadeCartaz['), texto.index('((creditosPt1['))
                # 08/11/2026: e, antes desta, a decisão 152 no M2 (que mexe no índice do M2).
                self.assertLess(texto.index('((cuidadoM2['), texto.index('((cidadeCartaz['))
                # 08/11/2026: e, antes da do M2, a decisão 152 no M3 (que mexe no índice do M3).
                self.assertLess(texto.index('((cuidadoM3['), texto.index('((cuidadoM2['))
                # 08/11/2026: e, antes da do M3, a decisão 152 no M4 (que mexe no índice do M4).
                self.assertLess(texto.index('((cuidadoM4['), texto.index('((cuidadoM3['))
                # 08/11/2026: e, antes da do M4, a decisão 152 no M5 (que mexe no índice do M5).
                self.assertLess(texto.index('((cuidadoM5['), texto.index('((cuidadoM4['))
        texto = ler('tests/browser_cartaz_cabecalho.cjs')
        self.assertLess(texto.index("cidadeCartaz.files['index.html']"), texto.index("creditosPt1.files['index.html']"))
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cidadeCartaz[rel]'), corpo.index('manifesto[rel].edits'))
        # 08/11/2026: e, antes desta, a decisão 152 no M2.
        self.assertLess(corpo.index('((cuidadoM2[rel]'), corpo.index('((cidadeCartaz[rel]'))
        # 08/11/2026: e, antes da do M2, a decisão 152 no M3.
        self.assertLess(corpo.index('((cuidadoM3[rel]'), corpo.index('((cuidadoM2[rel]'))
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4.
        self.assertLess(corpo.index('((cuidadoM4[rel]'), corpo.index('((cuidadoM3[rel]'))
        # 08/11/2026: e, antes da do M4, a decisão 152 no M5.
        self.assertLess(corpo.index('((cuidadoM5[rel]'), corpo.index('((cuidadoM4[rel]'))
        gerador = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador.index('CIDADE_CARTAZ.read_text'), gerador.index('CREDITOS_PT1.read_text'))
        # 08/11/2026: e, antes desta, a decisão 152 no M2.
        self.assertLess(gerador.index('CUIDADO_M2.read_text'), gerador.index('CIDADE_CARTAZ.read_text'))
        # 08/11/2026: e, antes da do M2, a decisão 152 no M3.
        self.assertLess(gerador.index('CUIDADO_M3.read_text'), gerador.index('CUIDADO_M2.read_text'))
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4.
        self.assertLess(gerador.index('CUIDADO_M4.read_text'), gerador.index('CUIDADO_M3.read_text'))
        # 08/11/2026: e, antes da do M4, a decisão 152 no M5.
        self.assertLess(gerador.index('CUIDADO_M5.read_text'), gerador.index('CUIDADO_M4.read_text'))
        # O workflow dos cartazes confere-a sem nada por cima e corre o seu teste de navegador; os caminhos levam-na.
        # 08/11/2026: confere-a com a decisão 152 no M2, a única por cima, desfeita antes.
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        # 08/11/2026: e, por cima da do M2, a decisão 152 no M3, desfeita primeiro.
        self.assertIn('      - run: python scripts/aplicar_trocas.py scripts/cidade_cartaz_20261108.json --manifesto '
                      # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
                      # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
                      f'{meu} --verificar --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {m3} --desfazer-antes {m2}\n', cartaz)
        self.assertIn('      - run: node tests/browser_cidade_cartaz.cjs\n', cartaz)
        self.assertLess(cartaz.index('node tests/browser_creditos_i_pt1.cjs'), cartaz.index('node tests/browser_cidade_cartaz.cjs'))
        for caminho in ('scripts/cidade_cartaz_20261108.*', meu, 'tests/*cidade_cartaz*', 'assets/retro-portals.css', 'index.html'):
            self.assertEqual(cartaz.count(f"'{caminho}'"), 2, caminho)
        for wf in ('pt-tarefas-qa.yml', 'pt-exame-laboratorio-qa.yml'):
            texto = ler('.github/workflows/' + wf)
            for caminho in ('scripts/cidade_cartaz_20261108.*', meu, 'tests/test_cidade_cartaz.py'):
                self.assertIn(f"'{caminho}'", texto, wf)

    def test_cartaz_logo_a_seguir_ao_do_atlas_com_o_texto_exato(self):
        # 08/11/2026 (revisão): o cartaz com fotografia e desenho próprios; saem as conferências das classes do cartaz do Atlas e dos
        # 14 números, e entram a fotografia, a etiqueta e o crédito no «i».
        s = self.entrada
        self.assertEqual(s.count(CARTAZ), 1)
        # A folha do cartaz vem logo antes dele e o cartaz logo a seguir ao fim do cartaz do Atlas e antes do portal do Lente.
        m = re.search(r'<span>TL</span></div></section>(<style>[^<]*</style>)' + re.escape(CARTAZ)
                      + re.escape('<nav class="site-portal-wrap" aria-label="Explorar o Lente">'), s)
        self.assertIsNotNone(m, 'Atlas, folha do cartaz, cartaz «Ler a cidade», portal do Lente')
        self.assertEqual(len(re.findall(r'<section class="atlas-poster[ "]', s)), 1)
        self.assertEqual(s.count('<section class="cidade-cartaz"'), 1)
        self.assertEqual(s.count('id="cidade-cartaz-titulo"'), 1)
        self.assertNotIn('cidade-poster', s)
        # As regras da folha só tocam o cartaz (as classes cidade-cartaz*), em todos os temas e larguras.
        folha = m.group(1)[len('<style>'):-len('</style>')]
        regras = re.findall(r'([^{}]+)\{[^{}]*\}', re.sub(r'@media[^{]*\{', '', folha))
        self.assertGreater(len(regras), 10)
        for r in regras:
            for seletor in r.split(','):
                self.assertIn('.cidade-cartaz', seletor, r)
        self.assertNotIn('atlas', folha)
        # O título em Georgia itálico de peso normal; o tema escuro pelo data-theme e, sem ele, pela preferência do sistema.
        self.assertIn('font:italic 400 clamp(2.4rem,5.5vw,4rem)/1 Georgia,', folha)
        self.assertIn(':root[data-theme="dark"] .cidade-cartaz{', folha)
        self.assertIn('(prefers-color-scheme:dark){:root:not([data-theme]) .cidade-cartaz{', folha)
        self.assertIn('@media(forced-colors:active){', folha)
        p = Seccao('cidade-cartaz')
        p.feed(s)
        self.assertEqual(re.sub(r'\s+', ' ', ''.join(p.texto)).strip(),
                         'Lisboa vista do Tejo, 1907 Português × Cidadania Ler a cidade Uma rua pode ser lida como um texto e discutida '
                         'como um espaço de todos. São 14 missões, no bairro ou a partir das fotografias. Entrar na cidade Ver as missões')
        self.assertEqual(p.ligacoes, [(FONTE, 'Library of Congress', True), (LENTE, 'Entrar na cidade', False),
                                      (LENTE + '#m01', 'Ver as missões', False)])
        # Sem nada do cartaz do Atlas: nem as classes, nem a grelha dos números.
        self.assertFalse([c for c in p.classes if 'atlas' in c or 'poster' in c], p.classes)
        self.assertEqual(p.classes[0], 'cidade-cartaz')
        # A fotografia: a do cartão «Ler a cidade.» da entrada do Lente, com o alt e as medidas exatas; o ficheiro está no sítio.
        self.assertEqual(p.imagens, [{'src': FOTO, 'alt': ALT, 'width': '1160', 'height': '773', 'loading': 'lazy', 'decoding': 'async'}])
        jpg = (ROOT / FOTO).read_bytes()
        i = 2
        while jpg[i + 1] not in (0xC0, 0xC2):
            i += 2 + int.from_bytes(jpg[i + 2:i + 4], 'big')
        self.assertEqual((int.from_bytes(jpg[i + 7:i + 9], 'big'), int.from_bytes(jpg[i + 5:i + 7], 'big')), (1160, 773))
        self.assertLessEqual(abs(1160 / 773 / 1.5 - 1), .02)
        # A etiqueta no canto da imagem, dentro da moldura dela, e o crédito inteiro no «i», depois da imagem.
        self.assertIn(f'<span class="cidade-cartaz-etiqueta">{ETIQUETA}</span></div>{I_CREDITO}', s)
        self.assertEqual(re.sub(r'\s+', ' ', ''.join(p.credito)).strip(),
                         'Metade de um estereograma de 1907, com direitos de J. J. Killelea & Co. e publicado por H. C. White Co. '
                         'Domínio público. Library of Congress.')
        self.assertEqual(s.count(I_CREDITO), 1)

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
        # 08/11/2026 (revisão): a secção chama-se agora cidade-cartaz; o texto novo inclui a etiqueta e o crédito do «i».
        p = Seccao('cidade-cartaz')
        p.feed(self.entrada)
        visivel = ''.join(p.texto) + ' ' + ''.join(p.credito)
        self.assertIn('Library of Congress', visivel)
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
