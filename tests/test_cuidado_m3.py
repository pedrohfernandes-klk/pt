"""08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M3. Camada literal cuidado_m3_20261108
(scripts/cuidado_m3_20261108.json, gerada por scripts/cuidado_m3_20261108.py; manifesto tests/fixtures/cuidado-m3-edits-20261108.json),
a mais recente, por cima da decisão 152 no M2 (cuidado_m2_20261108).

Este teste confere, no modelo de tests/test_cuidado_m1.py e tests/test_cuidado_m2.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices e o gerador do desenho comum dos índices;
* cada um dos 44 achados confirmados: as 9 tabelas novas (9 achados A), com o cabeçalho (th scope=col), a primeira coluna (th
  scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato, e a coluna do peso
  estreita; a entrada «Polidoro» da F13 (achado 11, A); os 3 casos do mesmo tipo (C), com o texto exato; os 31 achados B, com a
  contagem certa de cada sequência (das mais longas para as mais curtas, como a varredura), sem nenhuma ocorrência que se parta fora
  do que o achado deixa de fora (o «alt», a «frase» de um sublinhar), e a casca das lições, que fica para o molde;
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e que o baralho da F18
  (assets/pt-lessons/m3-f18.js) só serve a lição M3-F18;
* que nenhum dos 9 achados recusados (4, 6, 7, 8, 9, 10, 12, 13 e 21) entrou;
* as regras do texto: as tabelas só usam texto que lá estava (o do trecho e os cabeçalhos); nada de «professor», «jogar», «jogo»,
  «ficha», «folha», «—» ou «·» novos; nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>, chaves JSON
  ou da «frase» de um sublinhar; nas passagens mudadas, nenhuma referência nem número que se parta;
* que as tarefas, os aquecimentos, as grelhas e a correção da M3-U1 e da M3-U2 e o vídeo da F17 saem iguais dos dados e dos
  geradores, e que os painéis do docente seguem os enunciados das lições."""
from html.parser import HTMLParser
from pathlib import Path
import glob
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
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
from tarefas_claras_historico import desfazer as desfazer_enunciados
sys.path.insert(0, str(ROOT / 'tests'))
from auditoria_20261028 import undo_cuidado_m3_0811, undo_cuidado_m2_0811  # noqa: E402
# 08/11/2026: por cima desta camada fica a decisão 152 no M4 (camada cuidado_m4_20261108).
from auditoria_20261028 import undo_cuidado_m4_0811  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m3_20261108.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m3-edits-20261108.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
BASE_COMMIT = '77ad2feab4d15150274a8b12082d8f2a84e80098'
NBSP, WJ = '\xa0', '⁠'
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
A = {0, 1, 2, 3, 5, 11, 17, 18, 19, 20}
B = set(range(22, 53))
C_ = {14, 15, 16}
CONFIRMADOS = A | B | C_
RECUSADOS = {4, 6, 7, 8, 9, 10, 12, 13, 21}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)

PESOS = [['Tarefa da Unidade 1', '30\xa0%'], ['Tarefa da Unidade 2', '30\xa0%'], ['Provas rápidas', '10\xa0%'], ['Prova escrita', '30\xa0%']]
# (página, índice da tabela na página, rótulo no parágrafo antes da tabela, cabeçalho, linhas): o texto de cada célula, como se lê.
TABELAS = [
    # achado 0, cartão 4 («As três modalidades»)
    ('m3/licao-m3-f15/index.html', 0, None, ['Modalidade', 'O que exprime', 'Exemplos'],
     [['Epistémica', 'grau de certeza (valor de certeza ou probabilidade)', '«talvez», «deve estar», «é certo que»'],
      ['Deôntica', 'obrigação ou permissão; o pedido e a ordem também são deônticos', '«tem de», «pode sair»'],
      ['Apreciativa', 'avaliação ou emoção do locutor', '«Infelizmente», «Que belo!»']]),
    # achado 1, cartão 20 («Recorda»)
    ('m3/licao-m3-f05/index.html', 0, None, ['Termo', 'O que é'],
     [['Medida velha', 'os versos curtos da tradição peninsular'], ['Redondilha maior', 'verso de sete sílabas'],
      ['Redondilha menor', 'verso de cinco sílabas'], ['Mote', 'os versos de abertura, que dão o tema'],
      ['Voltas', 'as estrofes que desenvolvem o mote e voltam ao seu último verso'], ['Hipérbole', 'exagero que engrandece']]),
    # achado 2, cartão 20 («Recorda», primeira caixa)
    ('m3/licao-m3-f09/index.html', 0, None, ['Termo', 'O que é'],
     [['Apóstrofe', 'chamar alguém e falar-lhe, mesmo que não possa ouvir'], ['Antítese', 'duas ideias opostas lado a lado'],
      ['Paralelismo', 'a mesma construção repetida em dois versos'], ['Sujeito poético', 'a voz que fala no poema']]),
    # achado 3, cartão 22 («Recorda»)
    ('m3/licao-m3-f13/index.html', 0, None, ['Termo', 'O que é'],
     [['Reflexão do Poeta', 'o narrador para a ação e fala em nome próprio'], ['Interrogação retórica', 'pergunta que não espera resposta'],
      ['Metáfora', 'dá a uma coisa o nome de outra'], ['Anáfora', 'a mesma palavra a abrir versos seguidos']]),
    # achado 5, baralho da F18, cartão 10 («Planos que se articulam»)
    ('assets/pt-lessons/m3-f18.js', 0, None, ['Plano', 'O que faz'],
     [['Viagem', 'acompanha os navegantes'], ['História de Portugal', 'alarga o relato ao passado do povo'],
      ['Mitologia', 'introduz deuses e conflitos divinos'], ['Reflexões do Poeta', 'interrompem a ação para julgar']]),
    # achado 17, página «Ler a fundo» da modalidade, passo 0
    ('m3/gram-modalidade/index.html', 0, None, ['Modalidade', 'O que marca', 'Exemplos'],
     [['epistémica', 'grau de certeza', 'talvez, deve estar, é certo que'], ['deôntica', 'obrigação, permissão, pedido, ordem', 'tem de, pode, dai-me'],
      ['apreciativa', 'avaliação de quem fala', 'infelizmente, que belo!']]),
    # achados 18, 19 e 20: os pesos da avaliação
    ('m3/index.html', 0, 'Pesos na avaliação', ['Componente', 'Peso'], PESOS),
    ('m3/guia-da-tarefa-m3/index.html', 0, 'Avaliação', ['Componente', 'Peso'], PESOS),
    ('m3/mapa-do-modulo-m3/index.html', 0, 'Avaliação', ['Componente', 'Peso'], PESOS),
]
# Onde está cada tabela nas lições: (página, tabela) > (índice do cartão, o que fica por cima da tabela).
LUGARES = {('m3/licao-m3-f15/index.html', 0): (4, '<div class="caixa"><h3>As três modalidades</h3><table class="apoio-tabela"'),
           ('m3/licao-m3-f05/index.html', 0): (20, '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela"'),
           ('m3/licao-m3-f09/index.html', 0): (20, '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela"'),
           ('m3/licao-m3-f13/index.html', 0): (22, '<div class="caixa"><h3>Recorda</h3><table class="apoio-tabela"'),
           ('assets/pt-lessons/m3-f18.js', 0): (10, '<h3>Planos que se articulam</h3><table class="apoio-tabela"')}
# A página onde cada tabela se vê (o baralho da F18 vê-se na lição M3-F18).
PAGINA = {'assets/pt-lessons/m3-f18.js': 'm3/licao-m3-f18/index.html'}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a regra pede U+00A0, ou traço de intervalo sem U+2060,
# ou hífen entre anos. As formas do M3 (canto e estância, «c.», «séc.», «t.», «n.º», «est.», «vv.», «D.», ordinal e nome, número e
# unidade, datas, intervalos «N a M» e «N e M», «artigo 13.º», «soneto XIII», «verso 6»).
PARTE = re.compile(
    r'(?<![\w.])(?:vv?|pp?|séc|c|t|est|D)\. (?=[\dIVXLC]|[A-ZÁÉÍÓÚ][a-záéíóúãõç])'
    r'|n\.º (?=\d)|\b(?:séculos?|[Cc]antos?|estâncias?|versos?|soneto|artigo) (?=[\dIVXLC]+\b)|\d\.[ºª] (?=\w)'
    r'|\b[IVXL]+, (?=\d)|\b(?:Manuel|Sebastião) (?=[IVX]+\b)'
    r'|\d (?=(?:min|minutos|segundos|s|palavras|%)(?![\w]))'
    r'|\b\d+ [ae][ \xa0]\d|\b\d+[ \xa0][ae] \d'
    r'|\b\d{1,2} de (?=janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)'
    r'|(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) de \d'
    r'|\d–(?!⁠)\S|\b1\d{3}-\d{4}\b')


def ler(rel):
    return desfazer_enunciados(rel, (ROOT / rel).read_bytes().decode('utf-8'))


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def gerador():
    spec = importlib.util.spec_from_file_location('cuidado_m3_20261108', ROOT / 'scripts/cuidado_m3_20261108.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


C = gerador()


def cartoes(texto):
    """Os cartões de uma lição (ou do baralho da F18)."""
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0]


def visivel(fragmento):
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragmento.replace('\\"', '"').replace('<\\/', '</').replace('\\n', '\n')))


def palavras(texto):
    return set(re.findall(r'[\wÀ-ÿ]+', visivel(texto).lower()))


def base(rel):
    """A página sem esta camada (desfeita pelo manifesto, com contagem estrita)."""
    return undo_cuidado_m3_0811(rel, ler(rel))


class Tabela(HTMLParser):
    def __init__(self, fonte):
        super().__init__()
        self.tabela, self.legenda, self.linhas, self.atual, self.grupos, self.em_legenda = None, None, [], None, [], False
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'table':
            self.tabela = a
        elif tag == 'caption':
            self.em_legenda, self.legenda = True, ''
        elif tag in ('thead', 'tbody'):
            self.grupos.append((tag, a))
        elif tag == 'tr':
            self.linhas.append({'attrs': a, 'grupo': self.grupos[-1][0], 'celulas': []})
        elif tag in ('th', 'td'):
            self.atual = {'tag': tag, 'attrs': a, 'texto': ''}
            self.linhas[-1]['celulas'].append(self.atual)

    def handle_data(self, data):
        if self.em_legenda:
            self.legenda += data
        elif self.atual is not None:
            self.atual['texto'] += data

    def handle_endtag(self, tag):
        if tag in ('th', 'td'):
            self.atual = None
        elif tag == 'caption':
            self.em_legenda = False


def tabelas_da_pagina(texto, classe='apoio-tabela'):
    out = []
    for m in re.finditer(r'<table class=\\?"' + classe + r'\\?"', texto):
        fim = texto.index('</table>', m.start()) + len('</table>')
        out.append(texto[m.start():fim].replace('\\"', '"'))
    return out


def contextos_proibidos(texto):
    """Os pedaços onde não pode entrar U+00A0 nem U+2060: alt, aria-label, href e title, <title>, as chaves JSON e a «frase» de um
    sublinhar."""
    out = [m.group(2) for m in re.finditer(r'\b(alt|aria-label|href|title)=\\?"((?:(?!\\?").)*)', texto)]
    out += re.findall(r'<title>(.*?)</title>', texto, re.S)
    out += re.findall(r'"((?:[^"\\]|\\.)*)"\s*:', texto)
    for m in re.finditer(r'\{\s*"t":\s*"sublinhar"', texto):
        f = re.compile(r'"frase":\s*"((?:[^"\\]|\\.)*)"').search(texto, m.end())
        if f:
            out.append(f.group(1))
    return out


def ac_aplicadas(rel, texto):
    """O texto com só as trocas A e C desta camada (e a folha das tabelas) aplicadas por cima da base."""
    for t in TROCAS:
        if t['ficheiro'] == rel and '(B)' not in t['achado']:
            texto = texto.replace(t['antigo'], t['novo'])
    return texto


class CuidadoM3(unittest.TestCase):
    def test_nove_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 9)
        for rel, k, legenda, cabecalho, linhas in TABELAS:
            t = Tabela(tabelas_da_pagina(ler(rel))[k])
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(t.tabela.get('class'), 'apoio-tabela')
                self.assertEqual(t.tabela.get('role'), 'table')
                # Sem <caption> (fora das lições a folha comum não lhe dá estilo): o rótulo dos pesos fica no parágrafo antes da tabela.
                self.assertIsNone(t.legenda)
                if legenda:
                    self.assertIn(f'<p>{legenda}:</p>' + tabelas_da_pagina(ler(rel))[k], ler(rel))
                self.assertEqual([g for g, _ in t.grupos], ['thead', 'tbody'])
                self.assertTrue(all(a.get('role') == 'rowgroup' for _, a in t.grupos))
                topo, corpo = t.linhas[0], t.linhas[1:]
                self.assertEqual(topo['grupo'], 'thead')
                self.assertEqual([c['texto'] for c in topo['celulas']], cabecalho)
                for c in topo['celulas']:
                    self.assertEqual((c['tag'], c['attrs'].get('scope'), c['attrs'].get('role')), ('th', 'col', 'columnheader'))
                self.assertEqual([[c['texto'] for c in l['celulas']] for l in corpo], linhas)
                for linha in t.linhas:
                    self.assertEqual(linha['attrs'].get('role'), 'row')
                for linha in corpo:
                    self.assertEqual(linha['grupo'], 'tbody')
                    primeira, resto = linha['celulas'][0], linha['celulas'][1:]
                    self.assertEqual((primeira['tag'], primeira['attrs'].get('scope'), primeira['attrs'].get('role')), ('th', 'row', 'rowheader'))
                    self.assertEqual(len(linha['celulas']), len(cabecalho))
                    self.assertTrue(primeira['texto'].strip())
                    for coluna, c in enumerate(resto, 1):
                        self.assertEqual((c['tag'], c['attrs'].get('role'), c['attrs'].get('data-label')), ('td', 'cell', cabecalho[coluna]))
                        self.assertTrue(c['texto'].strip())
                # A coluna que só leva um número (o peso) é estreita; a primeira fica com o resto. As outras tabelas não têm larguras.
                larguras = [c['attrs'].get('style') for c in topo['celulas']]
                self.assertEqual(larguras, ['width:auto', 'width:5.5rem'] if cabecalho == ['Componente', 'Peso'] else [None] * len(cabecalho))
        # Nenhuma página do M3 (nem as suas tarefas, nem o baralho da F18) tem mais tabelas de apoio do que estas.
        contagem = {}
        for rel, _, _, _, _ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        paginas = (sorted(glob.glob(str(ROOT / 'm3/**/index.html'), recursive=True))
                   + sorted(glob.glob(str(ROOT / 'tarefas/m3-*/**/index.html'), recursive=True)) + [str(ROOT / 'assets/pt-lessons/m3-f18.js')])
        for p in paginas:
            rel = Path(p).relative_to(ROOT).as_posix()
            with self.subTest(pagina=rel):
                self.assertEqual(len(tabelas_da_pagina(ler(rel))), contagem.get(rel, 0))

    def test_tabelas_nos_cartoes_e_nos_sitios_certos(self):
        for (rel, k), (indice, topo) in LUGARES.items():
            cards = cartoes(ler(rel))
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(cards[indice]['t'], 'ler')
                self.assertEqual([i for i, c in enumerate(cards) if 'apoio-tabela' in c.get('html', '')], [indice])
                self.assertIn(topo, cards[indice]['html'])
        # F15: «Marcas: …» fica num parágrafo a seguir à tabela. F18: o parágrafo «Compara I, 19–20…» fica a seguir.
        self.assertIn('</table><p>Marcas: verbos modais, advérbios, adjetivos, modos verbais, tipos de frase.</p>',
                      cartoes(ler('m3/licao-m3-f15/index.html'))[4]['html'])
        self.assertIn('</table><p>Compara I,' + NBSP + '19–' + WJ + '20 com III,' + NBSP + '3–' + WJ + '5.',
                      cartoes(ler('assets/pt-lessons/m3-f18.js'))[10]['html'])
        # F09: a segunda caixa («Como se representa a amada») fica como estava, em prosa.
        self.assertIn('Como se representa a amada', cartoes(ler('m3/licao-m3-f09/index.html'))[20]['html'])
        # «Ler a fundo»: a tabela fica dentro de um div.nota, no passo 0, e o resto do passo fica igual.
        t = ler('m3/gram-modalidade/index.html')
        E = json.JSONDecoder().raw_decode(t[t.index('var E={') + 6:])[0]
        passo = E['passos'][0]['html']
        self.assertEqual(E['passos'][0]['rot'], 'Três frases, três tons')
        self.assertTrue(passo.endswith('<div class="nota"><table class="apoio-tabela" role="table">' + passo.split('<div class="nota"><table class="apoio-tabela" role="table">', 1)[1]))
        self.assertTrue(passo.endswith('</table></div>'))
        self.assertNotIn('<p class="nota">', passo)
        # Os pesos: a tabela vem logo antes do p.avaliacao-tarefas, que fica com o resto do parágrafo e continua a ser um só.
        resto = ('<p class="avaliacao-tarefas">Cada tarefa tem uma grelha /20. Na primeira recuperação, fazes a tarefa da unidade em falta, '
                 'com a mesma grelha /20.</p>')
        for rel in ('m3/index.html', 'm3/guia-da-tarefa-m3/index.html', 'm3/mapa-do-modulo-m3/index.html'):
            texto = ler(rel)
            with self.subTest(pagina=rel):
                self.assertEqual(texto.count('class="avaliacao-tarefas"'), 1)
                self.assertIn('</tbody></table>' + resto, texto)
        self.assertIn('A avaliação é feita pelo docente.<p>Pesos na avaliação:</p><table class="apoio-tabela" role="table"><thead',
                      ler('m3/index.html'))
        self.assertIn('<h1>Tarefas das unidades</h1><p>Avaliação:</p><table class="apoio-tabela" role="table"><thead',
                      ler('m3/guia-da-tarefa-m3/index.html'))
        self.assertIn('<summary>As tarefas do Teams</summary><p>Avaliação:</p><table class="apoio-tabela" role="table"><thead',
                      ler('m3/mapa-do-modulo-m3/index.html'))
        # Só o M3 muda (este pedido é do M3): nos outros módulos, os pesos continuam no parágrafo.
        # 08/11/2026: a decisão 152 no M5 (achado 1) passa também os pesos do M5 a uma tabela (conferida em test_cuidado_m5.py); nos
        # outros módulos, como estava.
        for m in (6, 8, 9):
            self.assertNotIn('apoio-tabela', ler(f'm{m}/index.html'), m)
        self.assertEqual(ler('m5/index.html').count('<table class="apoio-tabela"'), 1)

    def test_folha_das_tabelas_antes_da_aparencia(self):
        com_tabela = sorted({PAGINA.get(r, r) for r, _, _, _, _ in TABELAS})
        self.assertEqual(com_tabela, sorted(C.COM_TABELA))
        for rel in com_tabela:
            cabeca = ler(rel).split('</head>')[0]
            with self.subTest(pagina=rel):
                self.assertEqual(cabeca.count(FOLHA), 1)
                self.assertLess(cabeca.index(FOLHA), cabeca.index('assets/appearance.css'))
        # As outras páginas do M3 não carregam a folha.
        for p in sorted(glob.glob(str(ROOT / 'm3/**/index.html'), recursive=True)) + sorted(glob.glob(str(ROOT / 'tarefas/m3-*/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            if rel not in com_tabela:
                self.assertNotIn('apoios-tabelas.css', ler(rel), rel)
        # A folha é a do M1 e não muda: as regras das lições (.jogo .ler) e as de fora das lições já lá estão.
        css = ler('assets/pt-lessons/apoios-tabelas.css')
        self.assertIn('.jogo .ler .apoio-tabela td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertIn('.apoio-tabela:not(.jogo .ler .apoio-tabela) td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertNotIn('apoios-tabelas.css', {t['ficheiro'] for t in TROCAS})
        # O baralho da F18 só serve a lição M3-F18: nenhuma outra página o carrega.
        quem = sorted(Path(p).relative_to(ROOT).as_posix() for p in glob.glob(str(ROOT / '**/*.html'), recursive=True)
                      if 'm3-f18.js' in Path(p).read_text('utf-8', errors='ignore'))
        self.assertEqual(quem, ['m3/licao-m3-f18/index.html'])

    def test_casos_do_mesmo_tipo_e_a_entrada_da_f13(self):
        # Achado 14: os dois sentidos de «pena» na mesma entrada do vocabulário da F05.
        f05 = ler('m3/licao-m3-f05/index.html')
        self.assertEqual(f05.count('<b>pena</b>, pluma e sofrimento (duplo sentido);'), 1)
        self.assertNotIn('pluma; sofrimento', f05)
        # Achado 15: na F10, a referência sai do primeiro verso e do «cita» e passa ao título do cartão.
        f10 = ler('m3/licao-m3-f10/index.html')
        cards = cartoes(f10)
        self.assertEqual([(cards[i]['rot'], cards[i]['titulo']) for i in (2, 6, 10)],
                         [('O texto, 1 de 3', 'Canto' + NBSP + 'I,' + NBSP + '4'), ('O texto, 2 de 3', 'Canto' + NBSP + 'I,' + NBSP + '5'),
                          ('O texto, 3 de 3', 'Canto' + NBSP + 'X,' + NBSP + '145')])
        for i, verso in ((2, 'E vós, <b class="gt"'), (6, 'Dai-me uma <b class="gt"'), (10, '<b class="gt" data-s="não mais">Nô mais</b>')):
            self.assertIn('<span class="n"></span>' + verso, cards[i]['html'])
        self.assertNotIn(' · ', ''.join(cards[i]['html'] for i in (2, 6, 10)))
        self.assertEqual(cards[3]['cita'], 'E vós, Tágides minhas, pois criado')
        self.assertEqual(cards[11]['cita'], 'Nô mais, Musa, nô mais, que a Lira tenho')
        # O título «Duas invocações, dois tons» continua no «Em paralelo» (cartão 14).
        self.assertEqual(f10.count('Duas invocações, dois tons'), 1)
        self.assertEqual(cards[14]['titulo'], 'Duas invocações, dois tons')
        # As linhas marcáveis ficam iguais (data-l) e o sublinhar do cartão 3 conta as palavras da «frase», que não muda.
        self.assertEqual(re.findall(r'data-l="([\d-]+)"', ''.join(cards[i]['html'] for i in (2, 6, 10))),
                         re.findall(r'data-l="([\d-]+)"', ''.join(cartoes(base('m3/licao-m3-f10/index.html'))[i]['html'] for i in (2, 6, 10))))
        self.assertEqual(cards[3]['frase'], cartoes(base('m3/licao-m3-f10/index.html'))[3]['frase'])
        # Achado 16: na F13, os cartões das estâncias 97, 98 e 99 dizem a estância que mostram.
        f13 = cartoes(ler('m3/licao-m3-f13/index.html'))
        self.assertEqual([(f13[i]['rot'], f13[i]['titulo']) for i in (12, 14, 17)],
                         [('O texto, 3 de 5', 'Canto' + NBSP + 'VIII,' + NBSP + '97'), ('O texto, 4 de 5', 'Canto' + NBSP + 'VIII,' + NBSP + '98'),
                          ('O texto, 5 de 5', 'Canto' + NBSP + 'VIII,' + NBSP + '99')])
        texto = lambda i: re.sub(r'\s+', ' ', visivel(f13[i]['html']))
        self.assertIn('A Polidoro mata o Rei Treício', texto(12))
        self.assertIn('Este rende munidas fortalezas', texto(14))
        self.assertIn('Este interpreta mais que sutilmente', texto(17))
        # Achado 11 (A): a entrada «Polidoro» do vocabulário com os quatro nomes a negrito; o vocabulário continua em linha.
        self.assertIn('<b>Polidoro</b>, <b>Rei Treício</b>, <b>Acriso</b> e <b>Tarpeia</b>, exemplos antigos de crimes por dinheiro;',
                      f13[17]['html'])
        self.assertIn('<p class="gl"><b>Vocabulário:</b>', f13[17]['html'])

    def test_achados_b_com_a_contagem_certa(self):
        self.assertEqual(sorted(x['i'] for x in C.ACHADOS_B), sorted(B))
        vistos = 0
        for x in C.ACHADOS_B:
            rel = x['ficheiro']
            # A conta da varredura: o que muda, mais o que fica de fora, dá as ocorrências do achado.
            fora = x.get('fora', {})
            self.assertEqual(sum(n for _, n in x['pares']) + sum(n for _, n in x.get('nb', [])) + sum(n for n, _ in fora.values()),
                             x['ocorrencias'], x['i'])
            pre, final = ac_aplicadas(rel, base(rel)), ler(rel)
            seqs = [s for s, _ in x['pares']]
            antes, _ = C.ocorrencias(rel, pre, seqs, [])
            depois, ficaram = C.ocorrencias(rel, final, seqs, [])
            for seq, n in x['pares']:
                with self.subTest(achado=x['i'], trecho=seq):
                    # Antes, cada sequência aparece (fora do que fica de fora) exatamente as vezes que o achado conta; depois, nenhuma
                    # se parte, e a forma que não se parte está lá.
                    self.assertEqual(len(antes[seq]), n)
                    self.assertEqual(depois[seq], [])
                    self.assertGreaterEqual(final.count(C.nao_parte(seq)), n)
                    vistos += 1
            # O que fica com o espaço normal está só onde não pode levar U+00A0 (o «alt», o <title>, a «frase» de um sublinhar).
            for seq, s, razao in ficaram:
                self.assertTrue(razao.startswith(('atributo alt', '<title>', 'frase de um sublinhar')), (rel, seq, razao))
        self.assertEqual(vistos, sum(len(x['pares']) for x in C.ACHADOS_B))
        # A casca das lições (migalhas, «Estás em», sigla do rodapé) fica para o molde, como no M1 e no M2: nenhuma lição a muda.
        self.assertEqual(len(C.CASCA_NO_MOLDE), 11)
        for rel in C.CASCA_NO_MOLDE:
            texto = ler(rel)
            n = re.search(r'licao-m3-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                self.assertIn('/pt/1/">1.º ano</a>', texto)
                self.assertIn(f'Estás em: Lição M3-{n}', texto)
                self.assertIn(f'Lição M3-{n}, ', texto)
                self.assertNotIn('M3-' + WJ, texto)
                self.assertNotIn('1.º' + NBSP, texto)
        # As fontes do rodapé mudam, como no M1 (o rodapé da F10 tem o intervalo com a junção).
        self.assertIn('<i>Os Lusíadas</i> (1572), I,' + NBSP + '4–' + WJ + '5 e X,' + NBSP + '145.', ler('m3/licao-m3-f10/index.html'))
        # Nas outras páginas, as migalhas mudam onde o achado da página as inclui (como no M2).
        for rel in ('m3/index.html', 'm3/guia-da-tarefa-m3/index.html', 'm3/mapa-do-modulo-m3/index.html', 'm3/portefolio-do-modulo-m3/index.html',
                    'm3/camoes-alma/index.html', 'm3/camoes-invocacoes/index.html', 'm3/camoes-leonor/index.html', 'm3/camoes-mudanca/index.html',
                    'm3/bicho-da-terra/index.html', 'm3/gram-modalidade/index.html', 'm3/m3-soneto-raciocinio/index.html',
                    'm3/m3-velho-restelo-juri/index.html'):
            self.assertIn('/pt/1/">1.º' + NBSP + 'ano</a>', ler(rel), rel)
        # Os intervalos: traço com junção; o hífen de «c. 1520-1540» passa a traço (na F10 e no crédito do «i» do mapa).
        f18 = ler('assets/pt-lessons/m3-f18.js')
        for intervalo in ('I,' + NBSP + '19–' + WJ + '20', 'II,' + NBSP + '109–' + WJ + '110', 'III,' + NBSP + '3–' + WJ + '5',
                          'III,' + NBSP + '1–' + WJ + '5', 'IV,' + NBSP + '84–' + WJ + '93'):
            self.assertIn(intervalo, f18)
        self.assertIn('"rot":"O texto · I,' + NBSP + '19–' + WJ + '20"', f18)
        self.assertIn('"rot":"Quem conta · III,' + NBSP + '1–' + WJ + '5"', f18)
        self.assertNotRegex(f18, r'\d–(?!' + WJ + r')\d')
        self.assertIn('(c.' + NBSP + '1520–' + WJ + '1540, The Met). Domínio público', ler('m3/licao-m3-f10/index.html'))
        self.assertIn('alt=\\"Prato com esfera armilar e armas de Portugal, porcelana chinesa (c. 1520-1540, The Met)\\"',
                      ler('m3/licao-m3-f10/index.html'))
        mapa = ler('m3/mapa-do-modulo-m3/index.html')
        self.assertIn('<span class="nb">c.' + NBSP + '1520–' + WJ + '1540</span>', mapa)
        self.assertIn('(c.' + NBSP + '1524–' + WJ + '1580)', mapa)
        self.assertEqual(mapa.count('1497–' + WJ + '1499'), 2)
        # Os créditos que outra camada já tinha posto em <span class="nb"> ficam como estavam.
        self.assertIn('<span class="nb">c.' + NBSP + '1577</span>', mapa)
        self.assertIn('<span class="nb">c.' + NBSP + '1560</span>', mapa)
        # «até 25 palavras»: só «25 palavras» se prende.
        self.assertEqual(ler('m3/licao-m3-f11/index.html').count('até 25' + NBSP + 'palavras'), 3)
        self.assertEqual(ler('m3/index.html').count('até 25' + NBSP + 'palavras'), 2)
        # A «frase» do sublinhar do cartão 3 da F10 fica como estava; as dos completar mudam (não se contam palavras).
        self.assertIn('"frase":"Em 25' + NBSP + 'de' + NBSP + 'novembro de [1]', ler('m3/licao-m3-f11/index.html'))

    def test_nenhum_recusado_aplicado(self):
        achados = {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertFalse(RECUSADOS & achados)
        # 4: na F18, os três recortes continuam uma lista (só com os intervalos que não se partem, do achado 33).
        f18 = cartoes(ler('assets/pt-lessons/m3-f18.js'))
        self.assertIn('<h3>Os mesmos momentos, duas ordens</h3><ul><li><b>I,' + NBSP + '19:</b>', f18[3]['html'])
        self.assertNotIn('apoio-tabela', f18[3]['html'])
        # 6 e 7: na F11, o guião de escuta e os tipos de pergunta ficam como estavam (sem tabela).
        self.assertNotIn('apoio-tabela', ler('m3/licao-m3-f11/index.html'))
        # 8: na F02, os seis objetos do Kit continuam uma lista.
        self.assertNotIn('apoio-tabela', ler('m3/licao-m3-f02/index.html'))
        # 9, 10, 12 e 13: os vocabulários em linha (p.gl) da F10, da F02, da F03 e da F05 ficam em linha.
        for rel, k in (('m3/licao-m3-f10/index.html', 10), ('m3/licao-m3-f02/index.html', 12), ('m3/licao-m3-f03/index.html', 7),
                       ('m3/licao-m3-f05/index.html', 7)):
            with self.subTest(vocabulario=rel):
                self.assertIn('<p class="gl"><b>Vocabulário:</b>', cartoes(ler(rel))[k]['html'])
        # 21: o guia não ganha a tabela da rubrica (nem código novo).
        self.assertEqual({t['ficheiro'] for t in TROCAS if t['ficheiro'] == 'm3/guia-da-tarefa-m3/index.html' and '<script' in t['novo']}, set())

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, _, cab, _ in TABELAS for c in cab}
        permitidas = {p for c in cabecalhos for p in palavras(c)}
        # O que entra de propósito (proposta final da conferência), achado a achado: o «e» que fecha a lista dos nomes da F13 (11) e a
        # forma do vocabulário da F05 que o sítio já usa em m3/camoes-perdigao, «pluma e sofrimento (duplo sentido)» (14); os títulos
        # da F10 (15) e da F13 (16) são a referência da estância («Canto I, 4»), que já está na lição. O que sai: na F18 (5), os artigos
        # à cabeça das frases que passam a linhas da tabela («A viagem» > «Viagem», «As reflexões» > «Reflexões»); na F10 (15), a
        # referência que estava no verso e no «cita» (vai para o título) e o título «Duas invocações, dois tons» do cartão 2 (fica no
        # cartão 14).
        entram = {11: {'e'}, 14: {'e', 'duplo', 'sentido'}, 15: {'canto', 'i', 'x', '4', '5', '145'}, 16: {'canto', 'viii', '97', '98', '99'}}
        saem = {5: {'a', 'as'}, 15: {'i', 'x', '4', '5', '145', 'duas', 'invocações', 'dois', 'tons'}}
        css = [t for t in TROCAS if t['novo'].startswith('<link rel="stylesheet"')]
        self.assertEqual(sorted(t['ficheiro'] for t in css), sorted(C.COM_TABELA))
        # «nao_partir» nos dados dos geradores: só a chave, a seguir à unidade (e mais nada).
        chaves = [t for t in TROCAS if '"nao_partir": true' in t['novo']]
        self.assertEqual(len(chaves), 4)
        for t in chaves:
            self.assertRegex(t['novo'], r'^' + re.escape(t['antigo']) + r' +"nao_partir": true,\n$')
        for t in TROCAS:
            if t in css or t in chaves:
                continue
            i = int(re.search(r'achado (\d+)', t['achado']).group(1))
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                antes, depois = visivel(t['antigo']), visivel(t['novo'])
                self.assertEqual(palavras(t['novo']) - palavras(t['antigo']) - permitidas - entram.get(i, set()), set())
                self.assertEqual(palavras(t['antigo']) - palavras(t['novo']) - saem.get(i, set()), set())
                self.assertLessEqual(depois.count('·'), antes.count('·'))
                self.assertEqual(depois.count('—'), antes.count('—'))
                self.assertEqual(len(PROIBIDAS.findall(depois)), len(PROIBIDAS.findall(antes)))
                self.assertTrue(t['achado'].startswith('08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M3'))
        for c in cabecalhos:
            self.assertIsNone(PROIBIDAS.search(c), c)
        # As trocas B só mudam espaços (U+00A0), põem a junção (U+2060) e trocam o hífen de «c. 1520-1540» por traço de intervalo.
        for t in TROCAS:
            if '(B)' in t['achado'] and t not in chaves:
                with self.subTest(local=t['local']):
                    self.assertEqual(t['novo'].replace(NBSP, ' ').replace(WJ, ''), t['antigo'].replace(NBSP, ' ')
                                     if '1520-1540' not in t['antigo'] else t['antigo'].replace(NBSP, ' ').replace('1520-1540', '1520–1540'))
        # Nenhum U+00A0 nem U+2060 novo dentro de alt, aria-label, href, title, <title>, chaves JSON nem da «frase» de um sublinhar.
        for rel in MANIFESTO['files']:
            with self.subTest(contextos=rel):
                conta = lambda texto: sum(p.count(NBSP) + p.count(WJ) for p in contextos_proibidos(texto))
                self.assertEqual(conta(ler(rel)), conta(base(rel)))

    def test_passagens_mudadas_sem_referencias_que_se_partam(self):
        for t in TROCAS:
            if t['novo'].startswith('<link rel="stylesheet"') or 'nao_partir' in t['novo']:
                continue
            texto = visivel(t['novo']) if '<' in t['novo'] else t['novo']
            # Os atributos que ficam de fora (alt) não contam; o resto não pode ter nada que se parta.
            texto = re.sub(r'\balt="[^"]*"', '', t['novo'].replace('\\"', '"'))
            texto = visivel(texto) if '<' in texto else texto
            m = PARTE.search(texto)
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                self.assertIsNone(m, m and texto[max(0, m.start() - 30):m.end() + 30])
        # E o contrário: o detetor apanha as formas que partem, e deixa as inteiras.
        for partido in ('canto I', 'Canto VIII, 96 a 99', 'I, 106', 'estância 106', 'est. 94', 'c. 1577', 'séc. XVI', 't. III', 'n.º 37192',
                        'vv. 3 e 4', 'verso 6', 'D. Manuel I', 'D. Sebastião', '1.º ano', '30 %', '4 min', '90 minutos', '30 segundos',
                        '200 a 240 palavras', '120–150', 'I, 19–20', 'c. 1520-1540', '5 de maio', '25 de novembro de 2019', 'artigo 13.º',
                        'soneto XIII', '1 a 3', '0 a 20'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for inteiro in ('canto' + NBSP + 'I', 'Canto' + NBSP + 'VIII,' + NBSP + '96' + NBSP + 'a' + NBSP + '99', 'I,' + NBSP + '106',
                        'estância' + NBSP + '106', 'est.' + NBSP + '94', 'c.' + NBSP + '1577', 'séc.' + NBSP + 'XVI', 't.' + NBSP + 'III',
                        'n.º' + NBSP + '37192', 'vv.' + NBSP + '3' + NBSP + 'e' + NBSP + '4', 'verso' + NBSP + '6',
                        'D.' + NBSP + 'Manuel' + NBSP + 'I', 'D.' + NBSP + 'Sebastião', '1.º' + NBSP + 'ano', '30' + NBSP + '%',
                        '4' + NBSP + 'min', '90' + NBSP + 'minutos', '30' + NBSP + 'segundos',
                        '200' + NBSP + 'a' + NBSP + '240' + NBSP + 'palavras', '120–' + WJ + '150', 'I,' + NBSP + '19–' + WJ + '20',
                        'c.' + NBSP + '1520–' + WJ + '1540', '5' + NBSP + 'de' + NBSP + 'maio',
                        '25' + NBSP + 'de' + NBSP + 'novembro' + NBSP + 'de' + NBSP + '2019', 'artigo' + NBSP + '13.º',
                        'soneto' + NBSP + 'XIII', '1' + NBSP + 'a' + NBSP + '3', '0' + NBSP + 'a' + NBSP + '20'):
            self.assertIsNone(PARTE.search(inteiro), inteiro)

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 08/11/2026: por cima desta camada fica agora a decisão 152 no M4 (cuidado_m4_20261108, que não mexe em nenhuma página do
        # M3); desfaz-se primeiro, com a mesma exigência, e as contagens são as mesmas.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m3_20261108.json', '--manifesto', MANIFESTO_REL,
                            # 08/11/2026: a decisão 152 no M5 (cuidado_m5_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M5, incluindo o índice, o guia, o mapa e o portefólio do módulo, e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M4; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M6 (cuidado_m6_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M6, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M5; desfaz-se primeiro, com a mesma exigência.
                            # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
                            '--verificar', '--desfazer-antes', 'tests/fixtures/cuidado-m6-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json', '--desfazer-antes', 'tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m4-edits-20261108.json'], cwd=ROOT,
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em {len(MANIFESTO["files"])} ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.',
                      r.stdout)
        self.assertEqual((len(TROCAS), len(MANIFESTO['files'])), (484, 45))
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M3'))
        self.assertIn('cuidado_m2_20261108', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                # 08/11/2026: a página como esta camada a deixou: com a camada de cima (cuidado_m4_20261108) desfeita, com contagem
                # estrita; undo_cuidado_m3_0811 desfaz as duas, a partir da página inteira.
                atual = undo_cuidado_m4_0811(rel, ler(rel))
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = undo_cuidado_m3_0811(rel, ler(rel))
                self.assertEqual(sha_lf(b), registo['base_sha256_lf'])
                # Ida e volta: refazer as trocas sobre a base devolve a página, letra a letra.
                refeito = b
                for e in registo['edits']:
                    self.assertEqual(refeito.count(e['old']), e['occurrences'], (rel, e['location']))
                    refeito = refeito.replace(e['old'], e['new'])
                self.assertEqual(refeito, atual)
                for e in registo['edits']:
                    self.assertEqual(atual.count(e['new']), e['occurrences'], (rel, e['location']))
                    self.assertEqual(atual.replace(e['new'], '\0').count(e['old']), 0, (rel, e['location']))
                # A camada de baixo (a decisão 152 no M2) continua a desfazer-se por baixo desta.
                # 08/11/2026: na página inteira, porque a cadeia de desfazer começa agora pela decisão 152 no M4.
                undo_cuidado_m2_0811(rel, ler(rel))
        # Os 44 achados confirmados estão todos na camada; nenhum recusado.
        achados = {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertEqual(achados, CONFIRMADOS)
        self.assertEqual((len(A), len(B), len(C_)), (10, 31, 3))
        self.assertEqual(sorted({x['i'] for x in C.ACHADOS_AC if x['cat'] == 'A'}), sorted(A))
        self.assertEqual(sorted({x['i'] for x in C.ACHADOS_AC if x['cat'] == 'C'}), sorted(C_))
        # A e C antes de B, em cada ficheiro.
        for rel in m['files']:
            ordem = ['B' if '(B)' in t['achado'] else 'AC' for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual(ordem, sorted(ordem, key=lambda x: x != 'AC'), rel)
        # No topo da cadeia.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 08/11/2026: por cima desta camada fica a decisão 152 no M4 (cuidado_m4_20261108): esta passa a segunda, logo por baixo dela.
        # 08/11/2026: por cima da decisão 152 no M4 fica a decisão 152 no M5 (cuidado_m5_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 08/11/2026: por cima da decisão 152 no M5 fica a decisão 152 no M6 (cuidado_m6_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): logo abaixo da decisão 152 no M6 fica a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192), por cima da decisão 152 no M5; as posições seguintes descem uma.
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('cuidado_m4_20261108', 'cuidado-m4-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('cuidado_m3_20261108', 'cuidado-m3-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cuidado_m2_20261108', 'cuidado-m2-edits-20261108'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m2_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m3_0811(path, text)'), corpo.index('_CUIDADO_M2_0811.get('))
        # 08/11/2026: e esta camada desfaz primeiro a da decisão 152 no M4, que está por cima dela.
        corpo = auditoria[auditoria.index('def undo_cuidado_m3_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m4_0811(path, text)'), corpo.index('_CUIDADO_M3_0811.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m3-edits-20261108.json'), sala.index('cuidado-m2-edits-20261108.json'))
        # 08/11/2026: e, antes desta, a decisão 152 no M4.
        self.assertLess(sala.index('cuidado-m4-edits-20261108.json'), sala.index('cuidado-m3-edits-20261108.json'))
        # 08/11/2026: e, antes da decisão 152 no M4, a do M5.
        self.assertLess(sala.index('cuidado-m5-edits-20261108.json'), sala.index('cuidado-m4-edits-20261108.json'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6, agora a mais recente.
        self.assertLess(sala.index('cuidado-m6-edits-20261108.json'), sala.index('cuidado-m5-edits-20261108.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes da decisão 152 no M2, sem nada pelo meio.
        meu, m2 = MANIFESTO_REL, 'tests/fixtures/cuidado-m2-edits-20261108.json'
        # 08/11/2026: e logo a seguir à decisão 152 no M4, que se desfaz primeiro, logo a seguir a --verificar, sem nada pelo meio.
        m4 = 'tests/fixtures/cuidado-m4-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M4, a do M5, logo a seguir a --verificar.
        m5 = 'tests/fixtures/cuidado-m5-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M5, a do M6 (cuidado_m6_20261108), agora a primeira, logo a seguir a --verificar.
        m6 = 'tests/fixtures/cuidado-m6-edits-20261108.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + m2 not in linha:
                    continue
                linhas += 1
                # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
                # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
                self.assertIn(f'--verificar --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {meu} --desfazer-antes {m2}', linha, wf)
        self.assertEqual(linhas, 16)
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        # 08/11/2026: a decisão 152 no M2 desfaz primeiro a do M4 e depois esta.
        # 08/11/2026: e, antes da do M4, a do M5.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m2_20261108.json --manifesto {m2} --verificar --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} '
                      f'--desfazer-antes {m4} --desfazer-antes {meu}\n', tarefas)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        # 08/11/2026: o cartaz «Ler a cidade» desfaz primeiro a decisão 152 no M4, depois esta e a do M2.
        # 08/11/2026: e, antes da do M4, a do M5.
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto tests/fixtures/cidade-cartaz-edits-20261108.json --verificar '
                      # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
                      # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
                      f'--desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {meu} --desfazer-antes {m2}\n', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e da decisão 152 no M1 conferem as cadeias com frases partidas em várias linhas
            # (e já exigem esta camada à cabeça); ficam de fora pela mesma razão.
            # 08/11/2026: e o teste da decisão 152 no M4, pela mesma razão.
            # 08/11/2026: e o teste da decisão 152 no M5, pela mesma razão.
            # 08/11/2026: e o teste da decisão 152 no M6, pela mesma razão.
            if p.name in ('test_cuidado_m3.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py', 'test_cuidado_m4.py', 'test_cuidado_m5.py',
                          'test_cuidado_m6.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + m2), plano.count(f'--desfazer-antes {meu} --desfazer-antes {m2}'))
        # 08/11/2026: nas rotas, a decisão 152 no M4 vem primeiro, logo antes desta.
        # 08/11/2026: e, antes da do M4, a do M5.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        self.assertIn(f"(ROOT/'{m6}',ROOT/'{m5}',ROOT/'{m4}',ROOT/'{meu}',ROOT/'{m2}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM3['), texto.index('((cuidadoM2['), rel)
            # 08/11/2026: e, antes desta, a decisão 152 no M4.
            self.assertLess(texto.index('((cuidadoM4['), texto.index('((cuidadoM3['), rel)
            # 08/11/2026: e, antes da do M4, a do M5.
            self.assertLess(texto.index('((cuidadoM5['), texto.index('((cuidadoM4['), rel)
            # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (que mexe no índice do M6).
            self.assertLess(texto.index('((cuidadoM6['), texto.index('((cuidadoM5['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM3[rel]'), corpo.index('((cuidadoM2[rel]'))
        # 08/11/2026: e, antes desta, a decisão 152 no M4.
        self.assertLess(corpo.index('((cuidadoM4[rel]'), corpo.index('((cuidadoM3[rel]'))
        # 08/11/2026: e, antes da do M4, a do M5.
        self.assertLess(corpo.index('((cuidadoM5[rel]'), corpo.index('((cuidadoM4[rel]'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6.
        self.assertLess(corpo.index('((cuidadoM6[rel]'), corpo.index('((cuidadoM5[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M3.read_text'), gerador_148.index('CUIDADO_M2.read_text'))
        # 08/11/2026: e, antes desta, a decisão 152 no M4.
        self.assertLess(gerador_148.index('CUIDADO_M4.read_text'), gerador_148.index('CUIDADO_M3.read_text'))
        # 08/11/2026: e, antes da do M4, a do M5.
        self.assertLess(gerador_148.index('CUIDADO_M5.read_text'), gerador_148.index('CUIDADO_M4.read_text'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6.
        self.assertLess(gerador_148.index('CUIDADO_M6.read_text'), gerador_148.index('CUIDADO_M5.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1 e do M2.
        # 08/11/2026: conferem-na com a decisão 152 no M4, a única por cima, desfeita antes.
        # 08/11/2026: e, antes dela, a decisão 152 no M5 (as duas por cima, desfeitas antes, a mais recente primeiro).
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m3_20261108.json --manifesto {meu} --verificar --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} '
                      f'--desfazer-antes {m4}\n', tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m3.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m3.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m3_20261108.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_dos_dados(self):
        # As tarefas, os aquecimentos, as grelhas e a correção da M3-U1 e da M3-U2 mudam também nos dados, que estão nesta camada, e o
        # gerador das grelhas lê «nao_partir»; o vídeo da F17 muda nos dados de scripts/videos_escolhidos_pt.py.
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/')}
        self.assertEqual(dados, {'docs/pedagogia/tarefas-escolha/m3-u1.json', 'docs/pedagogia/tarefas-escolha/m3-u2.json',
                                 'docs/pedagogia/aquecimentos/m3-u1.json', 'docs/pedagogia/aquecimentos/m3-u2.json',
                                 'docs/pedagogia/grelhas-tarefas-20261027.json', 'docs/pedagogia/videos-escolhidos-pt-20261028.json'})
        for slug in ('m3-u1', 'm3-u2'):
            self.assertIs(json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))['nao_partir'], True)
        grelhas = json.loads(ler('docs/pedagogia/grelhas-tarefas-20261027.json'))['tarefas']
        self.assertEqual(sorted(s for s, t in grelhas.items() if t.get('nao_partir')), ['m3-u1', 'm3-u2'])
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for rel in ('tarefas/m3-u1/index.html', 'tarefas/m3-u2/index.html', 'tarefas/m3-u1/aquecimento/index.html',
                        'tarefas/m3-u2/aquecimento/index.html', 'tarefas/m3-u1/grelha/index.html', 'tarefas/m3-u2/grelha/index.html',
                        'tarefas/m3-u1/correcao/index.html', 'tarefas/m3-u2/correcao/index.html'):
                self.assertIn(rel, geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())
        # Os intervalos dos níveis das grelhas do M3 não se partem; nas outras grelhas, como estavam.
        for slug in ('m3-u1', 'm3-u2'):
            g = ler(f'tarefas/{slug}/grelha/index.html')
            self.assertEqual(len(re.findall(r'<dt>1\xa0a\xa0\d<small>', g)), 5, slug)
            self.assertNotRegex(g, r'<dt>1 a \d<small>')
        self.assertRegex(ler('tarefas/m5-u1/grelha/index.html'), r'<dt>1 a \d<small>')
        # O vídeo da F17 confere com os dados.
        r = subprocess.run([sys.executable, 'scripts/videos_escolhidos_pt.py', '--verificar'], cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('de Sá de Miranda (2' + NBSP + 'min)', ler('m3/licao-m3-f17/index.html'))

    def test_paineis_seguem_as_licoes(self):
        # Os painéis do docente das lições do M3 projetam os enunciados dos cartões: onde um mudou, o painel muda igual, na lista e no
        # seletor; e cada enunciado que seguia a lição antes desta camada continua a segui-la.
        paineis = sorted({t['ficheiro'] for t in TROCAS if '/painel-' in t['ficheiro']})
        self.assertEqual(paineis, ['m3/painel-m3-f02/index.html', 'm3/painel-m3-f03/index.html', 'm3/painel-m3-f10/index.html',
                                   'm3/painel-m3-f11/index.html', 'm3/painel-m3-f13/index.html', 'm3/painel-m3-f15/index.html',
                                   'm3/painel-m3-f17/index.html'])
        seguidos = 0
        for p in sorted(glob.glob(str(ROOT / 'm3/painel-m3-f*/index.html'))):
            rel = Path(p).relative_to(ROOT).as_posix()
            licao = rel.replace('/painel-', '/licao-')
            if 'CARTOES=' not in ler(rel):
                continue
            itens, itens_antes = cartoes(ler(rel)), cartoes(base(rel))
            L, L_antes = cartoes(ler(licao)), cartoes(base(licao))
            for item, antes in zip(itens, itens_antes):
                f = next((f for f in C.ENUNCIADOS if f(L_antes[antes['k']]) == antes['p']), None)
                if f is None:
                    continue
                with self.subTest(painel=rel, k=item['k']):
                    self.assertEqual(item['p'], f(L[item['k']]))
                    seguidos += 1
                    # Alguns painéis não põem todos os cartões no seletor; os que lá estão mostram o enunciado (cortado, às vezes).
                    m = re.search(r'<option value="%d">([^<]*)</option>' % item['k'], ler(rel))
                    if not m:
                        continue
                    opcao = m.group(1)
                    self.assertTrue(html.escape(re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\1', item['p']), quote=False).startswith(opcao)
                                    or html.escape(item['p'], quote=False).startswith(opcao))
        self.assertGreater(seguidos, 150)


if __name__ == '__main__':
    unittest.main()
