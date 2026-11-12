"""08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M2. Camada literal cuidado_m2_20261108
(scripts/cuidado_m2_20261108.json, gerada por scripts/cuidado_m2_20261108.py; manifesto tests/fixtures/cuidado-m2-edits-20261108.json),
a mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção (cidade_cartaz_20261108).

Este teste confere, no modelo de tests/test_cuidado_m1.py:
* que a camada está aplicada, fechada e reversível letra a letra (o manifesto, as contagens, os hashes e a ida e volta), que o
  gerador dá o mesmo JSON e que fica no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos, os testes
  da cadeia, os testes de navegador que montam o «antes» dos índices e o gerador do desenho comum dos índices;
* cada um dos 29 achados confirmados: as 6 tabelas novas (5 achados A), com o cabeçalho (th scope=col), a primeira coluna (th
  scope=row), as células (td com data-label do cabeçalho da sua coluna), os role e cada célula com o texto exato; os 4 casos do
  mesmo tipo (C), com o texto exato; os 20 achados B, com a contagem certa de cada trecho (e o que o achado deixa de fora); a casca
  das lições (achado 16), que fica para o molde, como no M1;
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência;
* que nenhum dos 7 achados recusados (4, 5, 6, 7, 9, 10 e 13) entrou;
* as regras do texto: as tabelas e listas só usam texto que lá estava (o do trecho e os cabeçalhos); nada de «professor», «jogar»,
  «jogo», «ficha», «folha», «—» ou «·» novos; nas passagens mudadas, nenhuma referência nem número que se parta;
* que os aquecimentos da M2-U1 e da M2-U2 e as lições geradas F14 e F15 saem iguais dos dados e dos geradores."""
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
from auditoria_20261028 import undo_cuidado_m2_0811, undo_cidade_cartaz_0811  # noqa: E402
# 08/11/2026: por cima desta camada fica a decisão 152 no M3 (camada cuidado_m3_20261108).
from auditoria_20261028 import undo_cuidado_m3_0811  # noqa: E402

CAMADA = ROOT / 'scripts/cuidado_m2_20261108.json'
MANIFESTO_REL = 'tests/fixtures/cuidado-m2-edits-20261108.json'
TROCAS = json.loads(CAMADA.read_text('utf-8'))
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
BASE_COMMIT = '17966724925640704eb568644a90f87f1ece2917'
NBSP, WJ = '\xa0', '⁠'
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'
CONFIRMADOS = {0, 1, 2, 3, 8, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35}
RECUSADOS = {4, 5, 6, 7, 9, 10, 13}
PROIBIDAS = re.compile(r'\b(jogar|jogos?|fichas?|folhas?|professor\w*)\b', re.IGNORECASE)

# (página, índice da tabela na página, cabeçalho, linhas): o texto de cada célula, como se lê.
TABELAS = [
    # achado 0, cartão 23 (caixa «Recorda: cinco recursos»)
    ('m2/licao-m2-f02/index.html', 0, ['Recurso', 'O que faz', 'Exemplo'],
     [['Comparação', 'aproxima duas coisas com «como»', '«Licença, como a bugia»'],
      ['Metáfora', 'dá a uma coisa o nome de outra, sem «como»', '«cativa / Em poder de desfiados»'],
      ['Enumeração', 'acumula termos numa lista', '«Rico, honrado, conhecido», diz Lianor Vaz'],
      ['Antítese', 'põe frente a frente dois opostos', '«sam aguçosa / E vós dais-vos de vagar»'],
      ['Interrogação retórica', 'pergunta que não espera resposta', '«Ou cuidas que é dia santo?»']]),
    # achado 8, cartão 28 (caixa «Recorda»)
    ('m2/licao-m2-f06/index.html', 0, ['Recurso', 'O que é'],
     [['Anáfora', 'a mesma palavra a abrir versos seguidos.'], ['Antítese', 'duas ideias opostas lado a lado.'],
      ['Provérbio', 'frase feita que guarda um saber comum.'],
      ['Duplo sentido', 'a frase diz uma coisa a quem está em cena e outra ao público.']]),
    # achado 1, cartão 7 (caixas «Coordenadas» e «Subordinadas»)
    ('m2/licao-m2-f07/index.html', 0, ['Tipo', 'Conectores'],
     [['copulativas', 'e, nem'], ['adversativas', 'mas; também porém, contudo, todavia, que são advérbios de ligação'],
      ['disjuntivas', 'ou'], ['conclusivas', 'logo; também portanto e por isso, advérbios de ligação'], ['explicativas', 'pois, que']]),
    ('m2/licao-m2-f07/index.html', 1, ['Tipo', 'Conector'],
     [['causais', 'porque'], ['temporais', 'quando'], ['condicionais', 'se'], ['finais', 'para que'], ['concessivas', 'embora'],
      ['consecutivas', 'tão… que'], ['comparativas', 'como']]),
    # achado 2, cartão 2 (caixa «Roteiro da apresentação oral»)
    ('m2/licao-m2-f09/index.html', 0, ['Passo', 'Conteúdo', 'Tempo'],
     [['1', 'O provérbio e o par asno/cavalo que escolheste', 'meio minuto'],
      ['2', 'O mapa: em que se transformou cada momento da farsa, e uma escolha de que te orgulhas', 'dois minutos'],
      ['3', 'Uma dificuldade e como a resolveste', 'um minuto'],
      ['4', 'A tua resposta à pergunta do módulo: o que é que escolheste mudar na tua recontagem, e porquê?', 'um minuto']]),
    # achado 3, item 6 da página «Pensar devagar» A máquina de rir (o monólogo não tem exemplo no texto: célula vazia)
    ('m2/m2-maquina-de-rir/index.html', 0, ['Peça', 'O que faz', 'Exemplo'],
     [['A personagem-tipo', 'cada figura é um tipo social e entra vestida do que é',
       'o lavrador rico e simples, o fidalgo pobre que se gaba, a alcoviteira que vende, o falso religioso'],
      ['A rubrica', 'texto secundário, manda o gesto', '«Assentou-se com as costas pera elas»'],
      ['O aparte', 'a fala que só a sala ouve', '«Ó Jesu! que João das bestas!»'],
      ['O monólogo', 'a fala de quem está só em cena', ''],
      ['O duplo sentido', 'a palavra que uma personagem ouve de uma maneira e a sala de outra', '«mor gado» e «morgado»']]),
]
# A única célula vazia (e sem data-label): o exemplo do monólogo.
VAZIAS = {('m2/m2-maquina-de-rir/index.html', 0, 3, 2)}
# Onde está cada tabela: (página, tabela) > (índice do cartão ou item, título que fica por cima da tabela).
LUGARES = {('m2/licao-m2-f02/index.html', 0): (23, '<h3>Recorda: cinco recursos</h3><table class="apoio-tabela"'),
           ('m2/licao-m2-f06/index.html', 0): (28, '<h3>Recorda</h3><table class="apoio-tabela"'),
           ('m2/licao-m2-f07/index.html', 0): (7, '<h3>Coordenadas</h3><p><b>Coordenadas</b> (as orações ligam-se sem que nenhuma '
                                                  'esteja dentro da outra):</p><table class="apoio-tabela"'),
           ('m2/licao-m2-f07/index.html', 1): (7, '<b>adverbiais</b>:</p><table class="apoio-tabela"'),
           ('m2/licao-m2-f09/index.html', 0): (2, '<h3>Roteiro da apresentação oral</h3><p><b>Cinco minutos, quatro passos.</b></p>'
                                                  '<table class="apoio-tabela"'),
           ('m2/m2-maquina-de-rir/index.html', 0): (6, '<p>As peças têm nome nas lições.</p><table class="apoio-tabela"')}

# Uma referência ou um número que se parte entre linhas: espaço normal onde a regra pede U+00A0, ou traço de intervalo e hífen de
# sigla sem U+2060. As formas do M1 e as do M2 (nome e numeral romano, «s», «por cento», intervalos «N a M» e «N e M», «M2-F01»).
PARTE = re.compile(
    r'(?<![\w.])(?:vv?|pp?|caps?|[Cc]ap|séc|c|vol|D|S)\. (?=[\dIVXLC]|[A-ZÁÉÍÓÚ][a-záéíóúãõç])'
    r'|n\.º (?=\d)|séculos? (?=[IVXLC]+\b)|\d\.[ºª] (?=\w)'
    r'|\b(?:João|Maria|Manuel|Pedro|Dinis|Afonso|Sebastião) (?=[IVX]+\b)'
    r'|\d (?=(?:min|minutos|segundos|s|palavras|%|por cento)(?![\w]))'
    r'|\b\d+ [ae][ \xa0]\d|\b\d+[ \xa0][ae] \d'
    r'|\b\d{1,2} de (?=janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)'
    r'|(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) de \d'
    r'|\d–(?!⁠)\S|\bM\d-(?!⁠)F\d')


def ler(rel):
    return desfazer_enunciados(rel, (ROOT / rel).read_bytes().decode('utf-8'))


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def gerador():
    spec = importlib.util.spec_from_file_location('cuidado_m2_20261108', ROOT / 'scripts/cuidado_m2_20261108.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


C = gerador()


def cartoes(texto):
    """Os cartões de uma lição (CARTOES) ou os itens da página «Pensar devagar» (itens:[…])."""
    marca = 'CARTOES=' if 'CARTOES=' in texto else 'itens:'
    return json.JSONDecoder().raw_decode(texto.split(marca, 1)[1].lstrip())[0]


def visivel(fragmento):
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragmento.replace('\\"', '"').replace('<\\/', '</').replace('\\n', '\n')))


def palavras(texto):
    return set(re.findall(r'[\wÀ-ÿ]+', visivel(texto).lower()))


class Tabela(HTMLParser):
    def __init__(self, fonte):
        super().__init__()
        self.tabela, self.linhas, self.atual, self.grupos = None, [], None, []
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'table':
            self.tabela = a
        elif tag in ('thead', 'tbody'):
            self.grupos.append((tag, a))
        elif tag == 'tr':
            self.linhas.append({'attrs': a, 'grupo': self.grupos[-1][0], 'celulas': []})
        elif tag in ('th', 'td'):
            self.atual = {'tag': tag, 'attrs': a, 'texto': ''}
            self.linhas[-1]['celulas'].append(self.atual)

    def handle_data(self, data):
        if self.atual is not None:
            self.atual['texto'] += data

    def handle_endtag(self, tag):
        if tag in ('th', 'td'):
            self.atual = None


def tabelas_da_pagina(texto, classe='apoio-tabela'):
    out = []
    for m in re.finditer(r'<table class=\\?"' + classe + r'\\?"', texto):
        fim = texto.index('</table>', m.start()) + len('</table>')
        out.append(texto[m.start():fim].replace('\\"', '"'))
    return out


class CuidadoM2(unittest.TestCase):
    def test_seis_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 6)
        for rel, k, cabecalho, linhas in TABELAS:
            t = Tabela(tabelas_da_pagina(ler(rel))[k])
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(t.tabela.get('class'), 'apoio-tabela')
                self.assertEqual(t.tabela.get('role'), 'table')
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
                for n, linha in enumerate(corpo):
                    self.assertEqual(linha['grupo'], 'tbody')
                    primeira, resto = linha['celulas'][0], linha['celulas'][1:]
                    self.assertEqual((primeira['tag'], primeira['attrs'].get('scope'), primeira['attrs'].get('role')),
                                     ('th', 'row', 'rowheader'))
                    self.assertEqual(len(linha['celulas']), len(cabecalho))
                    for coluna, c in enumerate(resto, 1):
                        if (rel, k, n, coluna) in VAZIAS:
                            # A célula vazia não leva rótulo: no telemóvel, «Exemplo:» sem nada a seguir não serve.
                            self.assertEqual((c['tag'], c['attrs'].get('role'), c['attrs'].get('data-label'), c['texto']),
                                             ('td', 'cell', None, ''))
                            continue
                        self.assertEqual((c['tag'], c['attrs'].get('role'), c['attrs'].get('data-label')), ('td', 'cell', cabecalho[coluna]))
                        self.assertTrue(c['texto'].strip())
                    self.assertTrue(primeira['texto'].strip())
        # Nenhuma página do M2 (nem as suas tarefas) tem mais tabelas de apoio do que estas.
        contagem = {}
        for rel, _, _, _ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        for p in sorted(glob.glob(str(ROOT / 'm2/**/index.html'), recursive=True)) + sorted(glob.glob(str(ROOT / 'tarefas/m2-*/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            with self.subTest(pagina=rel):
                self.assertEqual(len(tabelas_da_pagina(ler(rel))), contagem.get(rel, 0))

    def test_tabelas_nos_cartoes_certos(self):
        for (rel, k), (indice, titulo) in LUGARES.items():
            cards = cartoes(ler(rel))
            with self.subTest(pagina=rel, tabela=k):
                self.assertEqual(cards[indice]['t'], 'ler')
                self.assertIn('apoio-tabela', cards[indice]['html'])
                self.assertEqual([i for i, c in enumerate(cards) if 'apoio-tabela' in c.get('html', '')], [indice])
                # O título (h3) e a caixa ficam; a tabela entra no lugar do parágrafo.
                self.assertIn(titulo, cards[indice]['html'])
                self.assertFalse(cards[indice].get('escuro'))
        self.assertEqual(cartoes(ler('m2/m2-maquina-de-rir/index.html'))[6]['titulo'], 'As peças da máquina')
        # O fecho do roteiro e da máquina continua num parágrafo a seguir à tabela.
        self.assertIn('</table><p>Sobra meio minuto para uma pergunta da turma.</p>', cartoes(ler('m2/licao-m2-f09/index.html'))[2]['html'])
        self.assertIn('</table><p>Lê a fala de Pêro com estas peças na cabeça.</p>', cartoes(ler('m2/m2-maquina-de-rir/index.html'))[6]['html'])
        # Na F09, a tabela «Encomenda por curso» (table.quadro.empilha) fica como estava.
        self.assertIn('Encomenda por curso', cartoes(ler('m2/licao-m2-f09/index.html'))[2]['html'])

    def test_folha_das_tabelas_antes_da_aparencia(self):
        com_tabela = sorted({r for r, _, _, _ in TABELAS})
        self.assertEqual(com_tabela, sorted(C.COM_TABELA))
        for rel in com_tabela:
            cabeca = ler(rel).split('</head>')[0]
            with self.subTest(pagina=rel):
                self.assertEqual(cabeca.count(FOLHA), 1)
                self.assertLess(cabeca.index(FOLHA), cabeca.index('assets/appearance.css'))
        # As outras páginas do M2 não carregam a folha.
        for p in sorted(glob.glob(str(ROOT / 'm2/**/index.html'), recursive=True)):
            rel = Path(p).relative_to(ROOT).as_posix()
            if rel not in com_tabela:
                self.assertNotIn('apoios-tabelas.css', ler(rel), rel)
        # A folha é a do M1 (as tabelas das lições usam as regras de .jogo .ler, que já lá estão).
        css = ler('assets/pt-lessons/apoios-tabelas.css')
        self.assertIn('.jogo .ler .apoio-tabela td[data-label]::before{content:attr(data-label) ": "', css)
        self.assertIn('.jogo .ler .apoio-tabela thead{position:absolute', css)

    def test_casos_do_mesmo_tipo(self):
        # Achado 11: na F06, o termo «Señores, por caridad» inteiro a negrito (e a glosa do verso certa); a entrada sem negrito passa
        # a ter o termo a negrito. Os outros vocabulários ficam (não há <dl> nos vocabulários do M2).
        f06 = ler('m2/licao-m2-f06/index.html')
        self.assertIn('<b class=\\"gt\\" data-s=\\"senhores, por caridade\\">Señores, por caridad</b></span>', f06)
        self.assertIn('<b>Señores, por caridad</b>, senhores, por caridade;', f06)
        self.assertIn('; <b>haced que el tiempo pasado no se cuente por perdido</b>, fazei', f06)
        self.assertNotIn('por caridad, senhores, por caridade', f06)
        for p in sorted(glob.glob(str(ROOT / 'm2/licao-m2-f*/index.html'))):
            self.assertNotIn('<dl>', Path(p).read_text('utf-8'), p)
        # Achado 12: a lista dos ficheiros do portefólio, com cabeçalho, as 15 linhas de hoje, todos os nomes em <code> e inteiros.
        port = ler('m2/portefolio-do-modulo-m2/index.html')
        self.assertEqual(port.count(C.LISTA_DEPOIS), 1)
        self.assertNotIn('<th style="width:36%">', port)
        t = Tabela(tabelas_da_pagina(port, 'lista-ficheiros')[0])
        self.assertEqual([c['texto'] for c in t.linhas[0]['celulas']], ['Nome do ficheiro', 'O que é'])
        self.assertEqual([c['attrs'].get('scope') for c in t.linhas[0]['celulas']], ['col', 'col'])
        nomes = [l['celulas'][0]['texto'] for l in t.linhas[1:]]
        self.assertEqual(nomes, [html.unescape(n) for n, _, _ in C.FICHEIROS])
        self.assertEqual(len(nomes), 15)
        for l in t.linhas[1:]:
            self.assertEqual([c['attrs'].get('data-th') for c in l['celulas']], ['Nome do ficheiro', 'O que é'])
        lista = tabelas_da_pagina(port, 'lista-ficheiros')[0]
        self.assertEqual(lista.count('<code>'), 15)
        self.assertFalse(any(ch in lista for ch in (WJ, '‑', NBSP)))
        estilo = port.split('</head>')[0]
        self.assertEqual(estilo.count(C.CSS_LISTA), 1)
        self.assertIn('.lista-ficheiros code{white-space:nowrap}', estilo)
        self.assertLess(estilo.index('.lista-ficheiros code'), estilo.index('</style>'))
        # Achado 14: os exemplos A, B e C da F14 em lista, sem o valor de cada um (que daria a resposta do cartão seguinte).
        f14 = cartoes(ler('m2/licao-m2-f14/index.html'))
        self.assertIn('<p>Exemplos criados para esta lição.</p><ul><li><b>A:</b> Guardei a casinha de madeira da maqueta.</li><li><b>B:</b> '
                      'A nossa casinha acolheu toda a família.</li><li><b>C:</b> É só uma casinha, não merece atenção.</li></ul>', f14[12]['html'])
        self.assertEqual(f14[13]['t'], 'emparelhar')
        # Achado 15: os versos da F07 com a marcação das outras lições do M2, sem itálico; os […], as notas e as fontes ficam.
        f07 = cartoes(ler('m2/licao-m2-f07/index.html'))
        versos = [l for c, linhas in C.VERSOS_F07 for l in linhas]
        self.assertEqual(len(C.VERSOS_F07), 9)
        self.assertEqual(len(versos), 64)
        achados = []
        for i in (2, 3, 4):
            h = f07[i]['html']
            self.assertNotIn('<p><i>', h)
            self.assertNotIn('data-l=', h)
            self.assertEqual(h.count('<p>[…]</p>'), 1)
            self.assertEqual(h.count('<p class="nota">'), 1)
            self.assertEqual(h.count('<p class="fonte">'), 1)
            achados += re.findall(r'<span class="ln"><span class="n"></span>(.*?)</span>', h)
            for bloco in re.findall(r'<p class="v">(.*?)</p>', h, re.S):
                self.assertEqual(bloco.count('<span class="ln">'), bloco.count('\n') + 1)
        self.assertEqual(achados, versos)
        self.assertIn('<p class="v"><span class="ln"><span class="n"></span>Rubrica: Assentou-se com as costas pera elas, e diz:</span></p>',
                      f07[2]['html'])

    def test_achados_b_com_a_contagem_certa(self):
        self.assertEqual(sorted(x['i'] for x in C.ACHADOS_B), list(range(16, 36)))
        vistos = 0
        for x in C.ACHADOS_B:
            if not x['ficheiro']:
                continue
            texto = ler(x['ficheiro'])
            fora = C.EXCLUIR.get(x['i'], {})
            for antigo, novo, n in x['pares']:
                with self.subTest(achado=x['i'], trecho=antigo):
                    # Cada trecho aparece com o espaço que não quebra exatamente as vezes que o achado conta.
                    self.assertEqual(texto.count(novo), n)
                    # E já não aparece com o espaço normal, salvo o que o achado deixa de fora.
                    self.assertEqual(texto.count(antigo), sum(texto.count(c) for c in fora.get(antigo, [])))
                    vistos += 1
        self.assertEqual(vistos, 88)
        # O que fica de fora: a «frase» do sublinhar do lead (as palavras contam-se por espaços, com «certas» [6, 7, 8, 9]) e os «alt».
        for rel in ('m2/licao-m2-f10/index.html', 'm2/index.html'):
            self.assertEqual(ler(rel).count(C.FRASE_LEAD), 1, rel)
        for rel in ('m2/licao-m2-f07/index.html', 'm2/licao-m2-f09/index.html'):
            self.assertEqual(ler(rel).count(C.ALT_D_JOAO), 1, rel)
        self.assertIn('alt="D. João III (Anthonis Mor, 1552)"', ler('m2/mapa-do-modulo-m2/index.html'))
        self.assertIn('rei D. João, o terceiro do nome', ler('m2/licao-m2-f01/index.html'))
        # Achado 16: a casca das lições (migalhas, «Estás em», rodapé) fica para o molde, como no M1: nenhuma lição a muda.
        for rel in C.CASCA_NO_MOLDE[16]:
            texto = ler(rel)
            n = re.search(r'licao-m2-(f\d+)', rel).group(1).upper()
            with self.subTest(casca=rel):
                self.assertIn('/pt/1/">1.º ano</a>', texto)
                self.assertIn(f'Estás em: Lição M2-{n}', texto)
                self.assertIn(f'Lição M2-{n}, ', texto)
                self.assertNotIn('M2-' + WJ, texto)
                self.assertNotIn('1.º' + NBSP, texto)
        # Nas outras páginas, as migalhas mudam onde o achado da página as inclui (como no índice e no guia do M1).
        for rel in ('m2/index.html', 'm2/guia-da-tarefa-m2/index.html', 'm2/mapa-do-modulo-m2/index.html',
                    'm2/portefolio-do-modulo-m2/index.html', 'm2/m2-maquina-de-rir/index.html', 'm2/m2-ines-escolhe-duas-vezes/index.html'):
            self.assertIn('/pt/1/">1.º' + NBSP + 'ano</a>', ler(rel), rel)
        # «M2-F01» com a junção só no mapa (as quatro ligações da galeria «Para ver»).
        self.assertEqual(ler('m2/mapa-do-modulo-m2/index.html').count('Lição M2-' + WJ + 'F01</a>'), 4)
        # No índice, os pesos ficam no parágrafo (o achado 4 foi recusado), com o espaço que não quebra.
        self.assertIn('<p class="avaliacao-tarefas">Pesos na avaliação: tarefa da Unidade 1, 30\xa0%; tarefa da Unidade 2, 30\xa0%; '
                      'provas rápidas, 10\xa0%; prova escrita, 30\xa0%. Cada tarefa tem uma grelha /20.</p>', ler('m2/index.html'))

    def test_nenhum_recusado_aplicado(self):
        self.assertFalse(RECUSADOS & {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])})
        indice, mapa = ler('m2/index.html'), ler('m2/mapa-do-modulo-m2/index.html')
        # 4 e 5: sem tabela dos pesos no índice nem no mapa.
        self.assertNotIn('apoio-tabela', indice)
        self.assertNotIn('<table', mapa.split('<p class="aval">', 1)[1].split('</p>', 1)[0])
        self.assertIn('<p class="aval"><b>Como se avalia:</b> duas tarefas de unidade no Teams (30\xa0% cada), provas rápidas (10\xa0%, média '
                      'das três; conta a primeira tentativa) e uma prova escrita de 45\xa0minutos (30\xa0%).', mapa)
        # 6 e 7: o «Em paralelo» da F06 e da F11 fica no componente de sempre.
        self.assertIn('<h3>O asno</h3><ul><li>No provérbio: o que leva, sem derrubar.</li>', ler('m2/licao-m2-f06/index.html'))
        self.assertIn('<h3>Pêro Marques</h3><ul><li>Tipo: o lavrador rico e simples.</li>', ler('m2/licao-m2-f11/index.html'))
        self.assertNotIn('apoio-tabela', ler('m2/licao-m2-f11/index.html'))
        # 9 e 10: o parágrafo dos tempos da aula de tarefa fica um parágrafo (só com os espaços que não quebram dos achados 30 e 31).
        for slug in ('m2-u1', 'm2-u2'):
            tarefa = ler(f'tarefas/{slug}/index.html')
            self.assertIn('<p>No início da aula de tarefa: 10\xa0minutos de cartões com consulta, 5\xa0minutos para leres o enunciado, '
                          '60\xa0minutos de produção e 15\xa0minutos de revisão e entrega. Total: 90\xa0minutos. O relógio de produção '
                          'começa depois da leitura.</p>', tarefa)
            self.assertNotIn('<table', tarefa)
        # 13: a regra «Três antes de mim» do guia fica como estava.
        self.assertIn('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; '
                      '3) pergunta ao teu par de trabalho. Só depois levantas o braço.</div>', ler('m2/guia-da-tarefa-m2/index.html'))

    def test_nada_inventado_e_regras_do_texto(self):
        cabecalhos = {c for _, _, cab, _ in TABELAS for c in cab} | {'Nome do ficheiro', 'O que é'}
        permitidas = {p for c in cabecalhos for p in palavras(c)}
        # O que sai de propósito (proposta final da conferência): na máquina de rir, o «como» que ligava o duplo sentido ao exemplo,
        # que passa à coluna Exemplo.
        saem = {'m2/m2-maquina-de-rir/index.html': {'como'}}
        # As regras da lista dos ficheiros, no <style> do portefólio: só CSS, a seguir à regra de <code>, sem texto à vista.
        css = [t for t in TROCAS if t['novo'] == C.CSS_ANCORA + C.CSS_LISTA]
        self.assertEqual([(t['ficheiro'], t['antigo']) for t in css], [('m2/portefolio-do-modulo-m2/index.html', C.CSS_ANCORA)])
        for t in TROCAS:
            if t in css:
                continue
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                antes, depois = visivel(t['antigo']), visivel(t['novo'])
                # Só o texto que lá estava (o do trecho), mais os cabeçalhos das colunas.
                self.assertEqual(palavras(t['novo']) - palavras(t['antigo']) - permitidas, set())
                # E nada se perde: as palavras do trecho estão todas no texto novo.
                self.assertEqual(palavras(t['antigo']) - palavras(t['novo']) - saem.get(t['ficheiro'], set()), set())
                # Nenhum «·», «—» nem palavra proibida nova.
                self.assertEqual(depois.count('·'), antes.count('·'))
                self.assertEqual(depois.count('—'), antes.count('—'))
                self.assertEqual(len(PROIBIDAS.findall(depois)), len(PROIBIDAS.findall(antes)))
                self.assertTrue(t['achado'].startswith('08/11/2026: decisão 152 (cuidado em todas as lições), varredura do M2'))
        for c in cabecalhos:
            self.assertIsNone(PROIBIDAS.search(c), c)
        # As trocas B só mudam espaços (U+00A0) e põem a junção (U+2060): o texto, sem eles, é o mesmo.
        for t in TROCAS:
            if '(B)' in t['achado']:
                self.assertEqual(t['novo'].replace(NBSP, ' ').replace(WJ, ''), t['antigo'], t['local'])

    def test_passagens_mudadas_sem_referencias_que_se_partam(self):
        for t in TROCAS:
            if t['ficheiro'].startswith('docs/'):
                texto = t['novo']
            else:
                texto = visivel(t['novo']) if '<' in t['novo'] else t['novo']
            m = PARTE.search(texto)
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                self.assertIsNone(m, m and texto[max(0, m.start() - 30):m.end() + 30])
        # E o contrário: o detetor apanha as formas que partem, e deixa as inteiras.
        for partido in ('D. João III', 'João III', 'D. Maria II', '(4 min)', '90 minutos', '30 segundos', '(30 s)', '25 %', '25 por cento',
                        '180 a 240 palavras', '180\xa0a 240', '200 e 260 palavras', '50 a 80', '3 de março', '17 de janeiro de 2023',
                        '1.º ano', '180–240', 'c. 1465–c. 1536', 'Lição M2-F01'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for inteiro in ('D.\xa0João\xa0III', 'D.\xa0Maria\xa0II', '(4\xa0min)', '90\xa0minutos', '30\xa0segundos', '(30\xa0s)', '25\xa0%',
                        '25\xa0por cento', '180\xa0a\xa0240\xa0palavras', '200\xa0e\xa0260\xa0palavras', '50\xa0a\xa080',
                        '3\xa0de\xa0março', '17\xa0de\xa0janeiro\xa0de\xa02023', '1.º\xa0ano', '180–⁠240', 'c.\xa01465–⁠c.\xa01536',
                        'Lição M2-⁠F01'):
            self.assertIsNone(PARTE.search(inteiro), inteiro)

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 08/11/2026: por cima desta camada fica agora a decisão 152 no M3 (cuidado_m3_20261108, que não mexe em nenhuma página do
        # M2); desfaz-se primeiro, com a mesma exigência, e as contagens são as mesmas.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m2_20261108.json', '--manifesto', MANIFESTO_REL,
                            # 08/11/2026: a decisão 152 no M4 (cuidado_m4_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M4, incluindo o índice, o guia, o mapa e o portefólio do módulo) passa a camada mais recente, por cima da decisão 152 no M3; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M5 (cuidado_m5_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M5, incluindo o índice, o guia, o mapa e o portefólio do módulo, e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M4; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M6 (cuidado_m6_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M6, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M5; desfaz-se primeiro, com a mesma exigência.
                            # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
                            # 11/11/2026: a decisão 152 no M7 (cuidado_m7_20261111: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M7, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo», «Olhar» e «Pensar devagar», e nas tarefas, nos aquecimentos e na grelha das suas unidades) passa a camada mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M9, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», as atividades e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
                            # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            '--verificar', '--desfazer-antes', 'tests/fixtures/exame-provas-oficial-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-exame-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m9-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m8-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m7-edits-20261111.json', '--desfazer-antes', 'tests/fixtures/cuidado-m6-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json', '--desfazer-antes', 'tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m3-edits-20261108.json'], cwd=ROOT,
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('122 trocas em 24 ficheiros: 122 aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('08/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M2'))
        self.assertIn('cidade_cartaz_20261108', m['_nota'])
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
        for rel, registo in m['files'].items():
            with self.subTest(pagina=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                # 08/11/2026: a página como esta camada a deixou: com a camada de cima (cuidado_m3_20261108) desfeita, com contagem
                # estrita; undo_cuidado_m2_0811 desfaz as duas, a partir da página inteira.
                atual = undo_cuidado_m3_0811(rel, ler(rel))
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = undo_cuidado_m2_0811(rel, ler(rel))
                self.assertEqual(sha_lf(base), registo['base_sha256_lf'])
                # Ida e volta: refazer as trocas sobre a base devolve a página, letra a letra.
                refeito = base
                for e in registo['edits']:
                    self.assertEqual(refeito.count(e['old']), e['occurrences'], (rel, e['location']))
                    refeito = refeito.replace(e['old'], e['new'])
                self.assertEqual(refeito, atual)
                for e in registo['edits']:
                    self.assertEqual(atual.count(e['new']), e['occurrences'], (rel, e['location']))
                    self.assertEqual(atual.replace(e['new'], '\0').count(e['old']), 0, (rel, e['location']))
                # A camada de baixo (o cartaz «Ler a cidade») continua a desfazer-se por baixo desta.
                # 08/11/2026: na página inteira, porque a cadeia de desfazer começa agora pela decisão 152 no M3.
                undo_cidade_cartaz_0811(rel, ler(rel))
        # Os 29 achados confirmados: todos na camada, salvo a casca das lições (16), que fica para o molde; nenhum recusado.
        achados = {int(n) for t in TROCAS for n in re.findall(r'\d+', t['achado'].split('achado ', 1)[1].split(' (')[0])}
        self.assertEqual(achados, CONFIRMADOS - {16})
        self.assertEqual(len(CONFIRMADOS), 29)
        cats = {}
        for x in C.ACHADOS_AC:
            cats[x['i']] = x['cat']
        self.assertEqual(sorted(i for i, c in cats.items() if c == 'A'), [0, 1, 2, 3, 8])
        self.assertEqual(sorted(i for i, c in cats.items() if c == 'C'), [11, 12, 14, 15])
        self.assertEqual(len(C.ACHADOS_B), 20)
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
        # 08/11/2026: por cima desta camada fica a decisão 152 no M3 (cuidado_m3_20261108): esta passa a segunda, logo por baixo dela.
        # 08/11/2026: por cima da decisão 152 no M3 fica a decisão 152 no M4 (cuidado_m4_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 08/11/2026: por cima da decisão 152 no M4 fica a decisão 152 no M5 (cuidado_m5_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 08/11/2026: por cima da decisão 152 no M5 fica a decisão 152 no M6 (cuidado_m6_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 11/11/2026: por cima da decisão 152 no M6 fica a decisão 152 no M7 (cuidado_m7_20261111): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M7 fica a decisão 152 no M8 (cuidado_m8_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M8 fica a decisão 152 no M9 (cuidado_m9_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M9 fica a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no Exame e nas páginas transversais fica a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da ligação «Treinos» na página principal do Exame ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('cuidado_m9_20261112', 'cuidado-m9-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('cuidado_m8_20261112', 'cuidado-m8-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cuidado_m7_20261111', 'cuidado-m7-edits-20261111'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): logo abaixo da decisão 152 no M6 fica a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192), por cima da decisão 152 no M5; as posições seguintes descem uma.
        self.assertEqual(verificar_camadas.LAYERS[7], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[8], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[9], ('cuidado_m4_20261108', 'cuidado-m4-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[10], ('cuidado_m3_20261108', 'cuidado-m3-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[11], ('cuidado_m2_20261108', 'cuidado-m2-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[12], ('cidade_cartaz_20261108', 'cidade-cartaz-edits-20261108'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cidade_cartaz_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m2_0811(path, text)'), corpo.index('_CIDADE_CARTAZ_0811.get('))
        # 08/11/2026: e esta camada desfaz primeiro a da decisão 152 no M3, que está por cima dela.
        corpo = auditoria[auditoria.index('def undo_cuidado_m2_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m3_0811(path, text)'), corpo.index('_CUIDADO_M2_0811.get('))
        # 08/11/2026: e a decisão 152 no M3 chama primeiro a decisão 152 no M4, que está por cima.
        corpo = auditoria[auditoria.index('def undo_cuidado_m3_0811'):]
        self.assertLess(corpo.index('undo_cuidado_m4_0811(path, text)'), corpo.index('_CUIDADO_M3_0811.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m2-edits-20261108.json'), sala.index('cidade-cartaz-edits-20261108.json'))
        # 08/11/2026: e, antes desta, a decisão 152 no M3.
        self.assertLess(sala.index('cuidado-m3-edits-20261108.json'), sala.index('cuidado-m2-edits-20261108.json'))
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4, a camada mais recente.
        self.assertLess(sala.index('cuidado-m4-edits-20261108.json'), sala.index('cuidado-m3-edits-20261108.json'))
        # 08/11/2026: e, antes da do M4, a decisão 152 no M5, agora a mais recente.
        self.assertLess(sala.index('cuidado-m5-edits-20261108.json'), sala.index('cuidado-m4-edits-20261108.json'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6, agora a mais recente.
        self.assertLess(sala.index('cuidado-m6-edits-20261108.json'), sala.index('cuidado-m5-edits-20261108.json'))
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7, agora a mais recente.
        self.assertLess(sala.index('cuidado-m7-edits-20261111.json'), sala.index('cuidado-m6-edits-20261108.json'))
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8, agora a mais recente.
        self.assertLess(sala.index('cuidado-m8-edits-20261112.json'), sala.index('cuidado-m7-edits-20261111.json'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9, agora a mais recente.
        self.assertLess(sala.index('cuidado-m9-edits-20261112.json'), sala.index('cuidado-m8-edits-20261112.json'))
        # Em cada cadeia dos fluxos e dos testes, esta camada desfaz-se logo antes do cartaz «Ler a cidade», sem nada pelo meio.
        # 08/11/2026: e logo a seguir à decisão 152 no M3, que se desfaz primeiro, logo a seguir a --verificar, sem nada pelo meio.
        meu, cidade = MANIFESTO_REL, 'tests/fixtures/cidade-cartaz-edits-20261108.json'
        m3 = 'tests/fixtures/cuidado-m3-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M3, a decisão 152 no M4 (cuidado_m4_20261108), a primeira, logo a seguir a --verificar.
        m4 = 'tests/fixtures/cuidado-m4-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M4, a do M5 (cuidado_m5_20261108), agora a primeira, logo a seguir a --verificar.
        m5 = 'tests/fixtures/cuidado-m5-edits-20261108.json'
        # 08/11/2026: e, antes da decisão 152 no M5, a do M6 (cuidado_m6_20261108), agora a primeira, logo a seguir a --verificar.
        m6 = 'tests/fixtures/cuidado-m6-edits-20261108.json'
        # 11/11/2026: e, antes da decisão 152 no M6, a do M7 (cuidado_m7_20261111), agora a primeira, logo a seguir a --verificar.
        m7 = 'tests/fixtures/cuidado-m7-edits-20261111.json'
        # 12/11/2026: e, antes da decisão 152 no M7, a do M8 (cuidado_m8_20261112), agora a primeira, logo a seguir a --verificar.
        m8 = 'tests/fixtures/cuidado-m8-edits-20261112.json'
        # 12/11/2026: e, antes da decisão 152 no M8, a do M9 (cuidado_m9_20261112), agora a primeira, logo a seguir a --verificar.
        m9 = 'tests/fixtures/cuidado-m9-edits-20261112.json'
        # 12/11/2026: e, por cima da do M9, a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112).
        ex = 'tests/fixtures/cuidado-exame-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (a ligação «Treinos» na página principal do Exame).
        lt = 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json'
        # 12/11/2026: o manifesto da camada que fica por cima dela (as provas em cartões com os documentos oficiais).
        po = 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
        linhas = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes ' + cidade not in linha:
                    continue
                linhas += 1
                # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
                # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
                # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
                # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
                # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                self.assertIn(f'--verificar --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {m3} --desfazer-antes {meu} --desfazer-antes {cidade}', linha, wf)
        self.assertEqual(linhas, 15)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        # 08/11/2026: o cartaz «Ler a cidade» desfaz primeiro a decisão 152 no M3 e depois esta.
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
        # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'scripts/cidade_cartaz_20261108.json --manifesto {cidade} --verificar --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {m3} '
                      f'--desfazer-antes {meu}\n', cartaz)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, os testes do pedido pt-1 e da decisão 152 no M1 conferem as cadeias com frases partidas em várias linhas.
            if p.name in ('test_cuidado_m2.py', 'test_creditos_i_pt1.py', 'test_cuidado_m1.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto).replace("',ROOT/'", ' ')
            # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): entre a decisão 152 no M6 e a do M5 fica a revisão dos enunciados das tarefas
            # (tarefas_claras_20261110), nas cadeias onde o #192 a pôs; nas que o #192 não mudou (test_cartaz_m4_piloto.py e test_variedade_f0.py),
            # a do M5 continua logo a seguir à do M6. A contagem lê as duas formas como uma só; nada mais cabe entre as duas.
            plano = plano.replace('--desfazer-antes ' + m6 + ' --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json ', '--desfazer-antes ' + m6 + ' ')
            with self.subTest(teste=p.name):
                # 08/11/2026: e a decisão 152 no M3 logo antes desta, sem nada pelo meio.
                self.assertEqual(plano.count('--desfazer-antes ' + cidade),
                                 # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
                                 # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
                                 # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
                                 # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
                                 # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
                                 # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
                                 # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                                 # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                                 # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                                 plano.count(f'--desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes {m5} --desfazer-antes {m4} --desfazer-antes {m3} --desfazer-antes {meu} --desfazer-antes {cidade}'))
        # 08/11/2026: nas rotas, a decisão 152 no M3 vem primeiro, logo antes desta.
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
        # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f"(ROOT/'{po}',ROOT/'{lt}',ROOT/'{ex}',ROOT/'{m9}',ROOT/'{m8}',ROOT/'{m7}',ROOT/'{m6}',ROOT/'{m5}',ROOT/'{m4}',ROOT/'{m3}',ROOT/'{meu}',ROOT/'{cidade}',", ler('tests/test_task_routes_closure.py'))
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((cuidadoM2['), texto.index('((cidadeCartaz['), rel)
            # 08/11/2026: e, antes desta, a decisão 152 no M3.
            self.assertLess(texto.index('((cuidadoM3['), texto.index('((cuidadoM2['), rel)
            # 08/11/2026: e, antes da do M3, a decisão 152 no M4 (que mexe no índice do M4).
            self.assertLess(texto.index('((cuidadoM4['), texto.index('((cuidadoM3['), rel)
            # 08/11/2026: e, antes da do M4, a decisão 152 no M5 (que mexe no índice do M5).
            self.assertLess(texto.index('((cuidadoM5['), texto.index('((cuidadoM4['), rel)
            # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (que mexe no índice do M6).
            self.assertLess(texto.index('((cuidadoM6['), texto.index('((cuidadoM5['), rel)
        texto = ler('tests/browser_creditos_i_pt1.cjs')
        corpo = texto[texto.index('function antes(rel)'):]
        self.assertLess(corpo.index('((cuidadoM2[rel]'), corpo.index('((cidadeCartaz[rel]'))
        # 08/11/2026: e, antes desta, a decisão 152 no M3.
        self.assertLess(corpo.index('((cuidadoM3[rel]'), corpo.index('((cuidadoM2[rel]'))
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4.
        self.assertLess(corpo.index('((cuidadoM4[rel]'), corpo.index('((cuidadoM3[rel]'))
        # 08/11/2026: e, antes da do M4, a decisão 152 no M5.
        self.assertLess(corpo.index('((cuidadoM5[rel]'), corpo.index('((cuidadoM4[rel]'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6.
        self.assertLess(corpo.index('((cuidadoM6[rel]'), corpo.index('((cuidadoM5[rel]'))
        gerador_148 = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador_148.index('CUIDADO_M2.read_text'), gerador_148.index('CIDADE_CARTAZ.read_text'))
        # 08/11/2026: e, antes desta, a decisão 152 no M3.
        self.assertLess(gerador_148.index('CUIDADO_M3.read_text'), gerador_148.index('CUIDADO_M2.read_text'))
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4.
        self.assertLess(gerador_148.index('CUIDADO_M4.read_text'), gerador_148.index('CUIDADO_M3.read_text'))
        # 08/11/2026: e, antes da do M4, a decisão 152 no M5.
        self.assertLess(gerador_148.index('CUIDADO_M5.read_text'), gerador_148.index('CUIDADO_M4.read_text'))
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6.
        self.assertLess(gerador_148.index('CUIDADO_M6.read_text'), gerador_148.index('CUIDADO_M5.read_text'))
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7.
        self.assertLess(gerador_148.index('CUIDADO_M7.read_text'), gerador_148.index('CUIDADO_M6.read_text'))
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8.
        self.assertLess(gerador_148.index('CUIDADO_M8.read_text'), gerador_148.index('CUIDADO_M7.read_text'))
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9.
        self.assertLess(gerador_148.index('CUIDADO_M9.read_text'), gerador_148.index('CUIDADO_M8.read_text'))
        # Os fluxos conferem a camada sem nada por cima e correm os testes deste pedido, onde estão os do M1.
        # 08/11/2026: conferem-na com a decisão 152 no M3, a única por cima, desfeita antes.
        tarefas, apoios = ler('.github/workflows/pt-tarefas-qa.yml'), ler('.github/workflows/pt-apoios-qa.yml')
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4, sem nada pelo meio.
        # 08/11/2026: e, antes da do M4, a do M5, sem nada pelo meio.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192) fica entre a decisão 152 no M6, que continua a mais recente e se desfaz primeiro, e a decisão 152 no M5.
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_m2_20261108.json --manifesto {meu} --verificar --desfazer-antes {po} --desfazer-antes {lt} --desfazer-antes {ex} --desfazer-antes {m9} --desfazer-antes {m8} --desfazer-antes {m7} --desfazer-antes {m6} --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json --desfazer-antes {m5} --desfazer-antes {m4} '
                      f'--desfazer-antes {m3}\n', tarefas)
        for wf in (tarefas, apoios):
            self.assertIn("python -m unittest discover -s tests -p 'test_cuidado_m2.py' -v", wf)
        self.assertIn('python tests/browser_cuidado_m2.py', apoios)
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/cuidado_m2_20261108.*', MANIFESTO_REL):
                self.assertIn(f"'{caminho}'", texto, nome)

    def test_gerador_da_o_mesmo_json(self):
        self.assertEqual(C.construir()[0], TROCAS)

    def test_paginas_geradas_saem_iguais_dos_dados(self):
        # Os aquecimentos da M2-U1 e da M2-U2 (scripts/aquecimentos.py) mudam também nos dados, que estão nesta camada.
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/')}
        self.assertEqual(dados, {'docs/pedagogia/aquecimentos/m2-u1.json', 'docs/pedagogia/aquecimentos/m2-u2.json'})
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, 'scripts/aquecimentos.py', '--saida', tmp], cwd=ROOT, capture_output=True, text=True,
                               encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for rel in ('tarefas/m2-u1/aquecimento/index.html', 'tarefas/m2-u2/aquecimento/index.html'):
                self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes(), rel)
        # As lições F14 e F15 são geradas (scripts/gerar_licoes_20261101.py, com os textos em scripts/licoes_m1_m6_20261101.py): os
        # dados levam a mesma mudança, e a página sai igual.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from licoes_20261101 import LESSONS
            from gerar_licoes_20261101 import render, sequences
        finally:
            sys.path.pop(0)
        unidades = sequences()
        for ident in ('m2-f14', 'm2-f15'):
            item = next(x for x in LESSONS if x['id'] == ident)
            self.assertEqual(ler(f'm2/licao-{ident}/index.html'), render(item, unidades), ident)
        self.assertIn('17\xa0de\xa0janeiro\xa0de\xa02023', json.dumps(next(x for x in LESSONS if x['id'] == 'm2-f15')['cards'], ensure_ascii=False))


if __name__ == '__main__':
    unittest.main()
