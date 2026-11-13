"""06/11/2026: decisão 152 do docente («cuidado em todas as lições»), módulo M1. Camada literal cuidado_m1_20261106
(scripts/cuidado_m1_20261106.json, gerada por scripts/cuidado_m1_20261106.py; manifesto tests/fixtures/cuidado-m1-edits-20261106.json),
a mais recente, por cima dos créditos atrás de um «i» (creditos_i_20261105).

Este teste confere:
* cada uma das 12 tabelas novas (onde havia itens paralelos), com o cabeçalho (th scope=col), a primeira coluna (th scope=row),
  as células (td com data-label do cabeçalho da sua coluna), os role, e cada célula com o texto exato;
* que cada página com tabela nova carrega a folha das tabelas de apoio antes da camada de aparência, e que a folha tem as regras
  do cartão escuro e das páginas fora das lições;
* que, nos ficheiros dos achados B, nenhum trecho fica com espaço que parte (salvo o que o achado deixa de fora: a casca do mapa
  e do portefólio), e que nas passagens mudadas (as tabelas novas e as trocas B) não há referência nem número que se parta;
* que as tabelas e as listas só usam texto que lá estava (o do cartão, ou o cabeçalho), salvo a reformulação mínima registada;
* as duas listas da grelha da M1-U1 e as três hipóteses da M1-F02;
* que as tarefas, o aquecimento, as grelhas e as correções do M1 se regeneram sem diferenças a partir dos dados;
* que a camada está no topo da cadeia: verificar_camadas, auditoria_20261028, desligar_sala, os fluxos e os testes da cadeia."""
from html.parser import HTMLParser
from pathlib import Path
import html
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
from auditoria_20261028 import undo_cuidado_m1_0611  # noqa: E402
# 07/11/2026: por cima desta camada ficam os créditos atrás de um «i» do pedido pt-1 (camada creditos_i_pt1_20261107).
from auditoria_20261028 import undo_creditos_i_pt1_0711  # noqa: E402

TROCAS = json.loads((ROOT / 'scripts/cuidado_m1_20261106.json').read_text('utf-8'))
MANIFESTO = json.loads((ROOT / 'tests/fixtures/cuidado-m1-edits-20261106.json').read_text('utf-8'))
NBSP, WJ = '\xa0', '\u2060'
FOLHA = 'assets/pt-lessons/apoios-tabelas.css?v=20261106.1'

TABELAS = [
    # achado 0, cartão 5
    ('m1/licao-m1-f05/index.html', 0, ['Onde', 'Entra (PEP)', 'Desaparece (ASA)'],
     [['início', 'prótese (scribere > escrever: vogal inicial)', 'aférese (alevantada > levantada: vogal inicial)'], ['meio', 'epêntese (humile > humilde: [d])', 'síncope (malu > mau: [l])'], ['fim', 'paragoge (ante > antes: consoante final)', 'apócope (amare > amar: vogal final)']]),
    # achado 1, E.passos[0]
    ('m1/gram-fonologia/index.html', 0, ['Onde', 'Entra (PEP)', 'Desaparece (ASA)'],
     [['início', 'prótese (scribere > escrever: vogal inicial)', 'aférese (alevantada > levantada: vogal inicial)'], ['interior', 'epêntese (humile > humilde: [d])', 'síncope (malu > mau: [l])'], ['fim', 'paragoge (ante > antes: consoante final)', 'apócope (amare > amar: vogal final)']]),
    # achado 2, cartão 18
    ('m1/licao-m1-f08/index.html', 0, ['Título', 'Sublinhado', 'Sem o grupo', 'Complemento'],
     [['1. «Acaba a venda do trigo em Lisboa»', '«do trigo»', '«a venda»… de quê?', '«Venda» é nome: complemento do nome.'], ['2. «Pobres incapazes de comprar trigo»', '«de comprar trigo»', '«incapazes»… de quê?', 'É adjetivo: complemento do adjetivo.'], ['3. «A cidade cercada carece de trigo»', '«de trigo»', '«carece»… de quê?', 'É verbo, e «carece-lhe» não se diz (diz-se «carece dele»): complemento oblíquo.']]),
    # achado 3, cartão 19, escuro
    ('m1/licao-m1-f08/index.html', 1, ['Quem pede', 'Complemento', 'Exemplo'],
     [['um nome', 'do nome', '«a guarda dos muros»'], ['um adjetivo', 'do adjetivo', '«amigas da natureza»'], ['um verbo, se o grupo tem preposição e não troca por «lhe»', 'oblíquo', '«chegar a ele»']]),
    # achado 4, cartão 14
    ('m1/licao-m1-f11/index.html', 0, ['Valor', 'O que faz', 'Conjunções'],
     [['copulativa', 'soma', 'e, nem'], ['adversativa', 'contraria o que se esperava', 'mas'], ['explicativa', 'justifica o que se disse ou mandou', 'pois, que'], ['conclusiva', 'tira a consequência', 'portanto, logo, por isso']]),
    # achado 8, cartão 19, escuro
    ('m1/licao-m1-f15/index.html', 0, ['Conjunção', 'Relação', 'Valor'],
     [['«e»', 'soma', 'copulativa (e, nem)'], ['«mas»', 'contraria o que se esperava', 'adversativa (mas)'], ['«pois»', 'justifica', 'explicativa (pois, que)'], ['«portanto»', 'tira a consequência', 'conclusiva (portanto, logo, por isso)']]),
    # achado 9, cartão 16, escuro
    ('m1/licao-m1-f20/index.html', 0, ['Etiqueta', 'O que é'],
     [['explícito', 'o que se aponta nas palavras'], ['inferência', 'o que se conclui de pistas'], ['interpretação', 'um sentido com provas'], ['opinião', 'um juízo de valor']]),
    # achado 13, cartão 1
    ('m1/licao-m1-f10/index.html', 0, ['Figura', 'Fontes'],
     [['Álvaro Pais ou o pajem, a 6\xa0de\xa0dezembro de\xa01383', 'Fernão Lopes, cap.\xa0XII'], ['Nuno Álvares Pereira em Aljubarrota', 'Wikipédia, «Batalha de Aljubarrota»'], ['uma pessoa do cerco de 1384', 'Fernão Lopes, caps.\xa0CXVI e\xa0CXLVIII; Wikipédia, «Cerco de Lisboa (1384)»'], ['Inês de Castro', 'Wikipédia, «Inês de Castro»'], ['alguém da área do teu curso, um fotógrafo, um músico, um realizador', 'Wikipédia e uma entrevista publicada']]),
    # achado 16, «Como se cumpre uma unidade»
    ('m1/index.html', 0, ['Componente', 'Peso'],
     [['tarefa da Unidade 1', '30\xa0%'], ['tarefa da Unidade 2', '30\xa0%'], ['provas rápidas', '10\xa0%'], ['prova escrita', '30\xa0%']]),
    # achado 17, «Aquecer em cartões»
    ('tarefas/m1-u1/index.html', 0, ['Momento', 'Tempo'],
     [['cartões com consulta', '10\xa0minutos'], ['lês o enunciado', '5\xa0minutos'], ['produção', '60\xa0minutos'], ['revisão e entrega', '15\xa0minutos'], ['Total', '90\xa0minutos']]),
    # achado 18, «Aquecer em cartões»
    ('tarefas/m1-u2/index.html', 0, ['Momento', 'Tempo'],
     [['cartões com consulta', '10\xa0minutos'], ['lês o enunciado', '5\xa0minutos'], ['produção', '60\xa0minutos'], ['revisão e entrega', '15\xa0minutos'], ['Total', '90\xa0minutos']]),
    # achado 19, «Aulas de tarefa das unidades»
    ('m1/guia-da-tarefa-m1/index.html', 0, ['Momento', 'Tempo'],
     [['aquecimento em cartões, no telemóvel e com consulta', '10\xa0minutos'], ['leitura do enunciado', '5\xa0minutos'], ['produção com consulta', '60\xa0minutos'], ['revisão e entrega', '15\xa0minutos']]),
]


# Texto que não estava no trecho e que a tabela pode trazer: os cabeçalhos das colunas e a reformulação mínima registada nas
# tarefas («para leres» > «lês», como o achado aceitou «para o docente apresentar» > «o docente apresenta»).
CABECALHOS = {c for _, _, cab, _ in TABELAS for c in cab}
REFORMULADO = {'tarefas/m1-u1/index.html': {'lês'}, 'tarefas/m1-u2/index.html': {'lês'}}
# Valores de coluna que vêm do mesmo cartão (as frases da aula), como o achado diz.
DO_CARTAO = {'m1/licao-m1-f08/index.html', 'm1/licao-m1-f15/index.html'}

# Uma referência ou um número que se parte entre linhas (espaço normal onde a regra pede U+00A0, ou traço de intervalo sem U+2060).
PARTE = re.compile(
    r'(?<![\w.])(?:vv?|pp?|caps?|[Cc]ap|séc|c|vol|D|S)\. (?=[\dIVXLC]|[A-ZÁÉÍÓÚ][a-záéíóúãõç])'
    r'|n\.º (?=\d)|séculos? (?=[IVXLC]+\b)|\d\.[ºª] (?=\w)'
    r'|\d (?=(?:min|minutos|segundos|palavras|%)(?![\w]))'
    r'|\b\d{1,2} de (?=janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)'
    r'|(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) de \d'
    r'|\d–(?!\u2060)\S|João I\b')


def ler(rel):
    return desfazer_enunciados(rel, (ROOT / rel).read_bytes().decode('utf-8'))


def cartoes(texto):
    return json.JSONDecoder().raw_decode(texto.split('CARTOES=', 1)[1].lstrip())[0]


def visivel(fragmento):
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragmento.replace('\\"', '"')))


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


def tabelas_da_pagina(texto):
    out = []
    for m in re.finditer(r'<table class=\\?"apoio-tabela\\?"', texto):
        fim = texto.index('</table>', m.start()) + len('</table>')
        out.append(texto[m.start():fim].replace('\\"', '"'))
    return out


class CuidadoM1(unittest.TestCase):
    def test_doze_tabelas_com_cabecalhos_linhas_e_celulas(self):
        self.assertEqual(len(TABELAS), 12)
        for rel, k, cabecalho, linhas in TABELAS:
            fonte = tabelas_da_pagina(ler(rel))[k]
            t = Tabela(fonte)
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
                for linha in corpo:
                    self.assertEqual(linha['grupo'], 'tbody')
                    primeira, resto = linha['celulas'][0], linha['celulas'][1:]
                    self.assertEqual((primeira['tag'], primeira['attrs'].get('scope'), primeira['attrs'].get('role')),
                                     ('th', 'row', 'rowheader'))
                    self.assertEqual(len(linha['celulas']), len(cabecalho))
                    for coluna, c in enumerate(resto, 1):
                        self.assertEqual((c['tag'], c['attrs'].get('role'), c['attrs'].get('data-label')),
                                         ('td', 'cell', cabecalho[coluna]))
                    self.assertTrue(all(c['texto'].strip() for c in linha['celulas']))
        # Nenhuma página do M1 tem mais tabelas de apoio do que estas.
        contagem = {}
        for rel, _, _, _ in TABELAS:
            contagem[rel] = contagem.get(rel, 0) + 1
        for rel, n in contagem.items():
            self.assertEqual(len(tabelas_da_pagina(ler(rel))), n, rel)

    def test_tabelas_nos_cartoes_certos(self):
        # Nas lições, cada tabela está no cartão do achado; as três do «Para levar» estão no cartão escuro.
        lugares = {('m1/licao-m1-f05/index.html', 0): (5, False), ('m1/licao-m1-f08/index.html', 0): (18, False),
                   ('m1/licao-m1-f08/index.html', 1): (19, True), ('m1/licao-m1-f11/index.html', 0): (14, False),
                   ('m1/licao-m1-f15/index.html', 0): (19, True), ('m1/licao-m1-f20/index.html', 0): (16, True),
                   ('m1/licao-m1-f10/index.html', 0): (1, False)}
        for (rel, k), (indice, escuro) in lugares.items():
            cards = cartoes(ler(rel))
            com_tabela = [i for i, c in enumerate(cards) if 'apoio-tabela' in c.get('html', '')]
            with self.subTest(pagina=rel, tabela=k):
                self.assertIn(indice, com_tabela)
                self.assertEqual(bool(cards[indice].get('escuro')), escuro)
                self.assertEqual(cards[indice]['t'], 'ler')
        # Na página «Ler a fundo», a tabela está no primeiro passo, dentro do «Consultar o esquema PEP/ASA e experimentar».
        texto = ler('m1/gram-fonologia/index.html')
        E = json.JSONDecoder().raw_decode('{' + texto.split('var E={', 1)[1])[0]
        primeiro = json.dumps(E['passos'][0], ensure_ascii=False)
        self.assertIn('apoio-tabela', primeiro)
        self.assertNotIn('apoio-tabela', json.dumps(E['passos'][1:], ensure_ascii=False))

    def test_folha_das_tabelas_antes_da_aparencia(self):
        for rel in sorted({r for r, _, _, _ in TABELAS}):
            cabeca = ler(rel).split('</head>')[0]
            with self.subTest(pagina=rel):
                self.assertEqual(cabeca.count(FOLHA), 1)
                self.assertLess(cabeca.index(FOLHA), cabeca.index('assets/appearance.css'))
        css = ler('assets/pt-lessons/apoios-tabelas.css')
        # O cartão escuro: o cabeçalho é uma linha da cor do texto e os rótulos do telemóvel herdam essa cor.
        self.assertIn('.jogo .cartao.escuro .ler .apoio-tabela thead th{background:transparent;color:inherit;border-bottom:2px solid currentColor}', css)
        self.assertIn('.jogo .cartao.escuro .ler .apoio-tabela td[data-label]::before{color:inherit}', css)
        # Fora das lições: só as tabelas que não estão numa lição, com cabeçalho legível e sem maiúsculas forçadas.
        self.assertIn('.apoio-tabela:not(.jogo .ler .apoio-tabela){width:100%;table-layout:fixed', css)
        self.assertIn('.apoio-tabela:not(.jogo .ler .apoio-tabela) tbody th{font:inherit;font-weight:700;text-transform:none', css)
        self.assertNotIn('!important', css)
        self.assertNotIn('display:none', css)
        # As lições do M7 com tabela ficam como estavam.
        self.assertIn('apoios-tabelas.css?v=20261105.1', ler('m7/licao-m7-f10/index.html'))
        self.assertIn('apoios-tabelas.css?v=20261027.1', ler('m7/licao-m7-f15/index.html'))

    def test_nada_inventado_nas_tabelas_e_listas(self):
        for t in TROCAS:
            if '<table' not in t['novo'] and '<ul>' not in t['novo']:
                continue
            rel = t['ficheiro']
            with self.subTest(ficheiro=rel, local=t['local']):
                fonte = palavras(t['antigo'])
                if rel in DO_CARTAO:
                    base = undo_cuidado_m1_0611(rel, ler(rel))
                    cartao = next(c['html'] for c in cartoes(base) if json.dumps(c.get('html', ''), ensure_ascii=False)[1:-1].count(t['antigo']))
                    fonte |= palavras(cartao)
                permitido = fonte | {p for c in CABECALHOS for p in palavras(c)} | REFORMULADO.get(rel, set())
                self.assertEqual(palavras(t['novo']) - permitido, set())

    def test_listas_da_grelha_e_hipoteses(self):
        f02 = next(c['html'] for c in cartoes(ler('m1/licao-m1-f02/index.html')) if 'Mais de uma hipótese' in c.get('html', ''))
        self.assertIn('<ul><li>O perigo é real.</li><li>É a espera que exagera.</li><li>Morrer «fremosa» acusa quem não veio.</li></ul>'
                      '<p>Mais de uma hipótese tem apoio no texto.</p>', f02)
        grelha = ler('tarefas/m1-u1/grelha/index.html')
        self.assertIn('(mais um ponto). </p><p><b>Tema A</b>:</p><ul><li>paralelismo;</li><li>refrão que repete a promessa;</li>'
                      '<li>o teu verso que desmente a promessa;</li><li>um verso de Codax citado;</li><li>uma diferença entre a tua '
                      'espera e a da cantiga de Codax.</li></ul><p>Explicação: o que imitaste de Codax.</p><p><b>Tema B</b>:</p><ul>'
                      '<li>imagem em duas frases;</li><li>dois factos do dossiê (contam como dois);</li><li>um verso escolhido;</li>'
                      '<li>o que o cartaz não pode prometer.</li></ul><p>Explicação: porque escolheste esse verso.</p><p class="ex">', grelha)
        # Na versão de correção, o mesmo texto fica corrido dentro do <small> (não há listas dentro de <small>).
        correcao = ler('tarefas/m1-u1/correcao/index.html')
        self.assertIn('(mais um ponto). Tema A: paralelismo; refrão que repete a promessa;', correcao)
        self.assertNotIn('<ul><li>paralelismo', correcao)

    def test_nenhum_trecho_b_fica_a_partir(self):
        # Em cada ficheiro dos achados B (páginas e dados dos geradores), nenhum trecho do achado fica com espaço normal ou sem a
        # junção depois do traço, salvo o que o achado deixa de fora (a casca do mapa e do portefólio).
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import cuidado_m1_20261106 as C
        finally:
            sys.path.pop(0)
        fora = {('m1/mapa-do-modulo-m1/index.html', '1.º ano'): 1, ('m1/portefolio-do-modulo-m1/index.html', '1.º ano'): 1}
        vistos = 0
        for x in C.ACHADOS_B:
            texto = ler(x['ficheiro'])
            for antigo, novo in x['pares']:
                with self.subTest(ficheiro=x['ficheiro'], trecho=antigo):
                    self.assertEqual(texto.count(antigo), fora.get((x['ficheiro'], antigo), 0))
                    vistos += 1
        self.assertGreaterEqual(vistos, 200)
        # A casca que fica: as migalhas do mapa e do portefólio («1.º ano» com espaço normal); no índice e no guia, os achados
        # incluem as migalhas, e aí mudou.
        for rel in ('m1/mapa-do-modulo-m1/index.html', 'm1/portefolio-do-modulo-m1/index.html'):
            self.assertIn('/pt/1/">1.º ano</a>', ler(rel))
        for rel in ('m1/index.html', 'm1/guia-da-tarefa-m1/index.html'):
            self.assertIn('/pt/1/">1.º' + NBSP + 'ano</a>', ler(rel))
        # «Lição M1-Fxx» não mudou (nenhum achado o pede).
        for rel in sorted({x['ficheiro'] for x in C.ACHADOS_B}):
            self.assertNotIn('M1-' + WJ, ler(rel))

    def test_passagens_mudadas_sem_referencias_que_se_partam(self):
        # Cada passagem nova (as tabelas, as listas e as janelas das trocas B, nas páginas e nos dados), no texto que se lê.
        for t in TROCAS:
            texto = visivel(t['novo']) if '<' in t['novo'] else t['novo']
            m = PARTE.search(texto)
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                self.assertIsNone(m, m and texto[max(0, m.start() - 30):m.end() + 30])
        # E o contrário: o detetor apanha as formas que partem.
        for partido in ('cap. XII', 'v. 14', 'séc. XIII', 'século XV', '1.º ano', '30 %', '90 minutos', '6 de dezembro',
                        'dezembro de 1383', '1279–1325', 'D. Dinis', 'João I', 'n.º 1308', 'p. 244', 'c. 1860', 'vol. I', '200 a 240 palavras'):
            self.assertIsNotNone(PARTE.search(partido), partido)
        for inteiro in ('cap.\xa0XII', 'v.\xa014', 'séc.\xa0XIII', 'século\xa0XV', '1.º\xa0ano', '30\xa0%', '90\xa0minutos',
                        '6\xa0de\xa0dezembro', 'de\xa01383', '1279–\u20601325', 'D.\xa0Dinis', 'João\xa0I'):
            self.assertIsNone(PARTE.search(inteiro), inteiro)

    def test_camada_confere_e_esta_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cuidado_m1_20261106.json',
                            '--manifesto', 'tests/fixtures/cuidado-m1-edits-20261106.json', '--verificar',
                            # 07/11/2026: por cima desta camada ficam os créditos atrás de um «i» do pedido pt-1 (creditos_i_pt1_20261107,
                            # que também mexe no índice do M1); desfazem-se primeiro, com a mesma exigência.
                            # 08/11/2026: e, por cima deles, o cartaz «Ler a cidade» e o nome novo da secção (cidade_cartaz_20261108, que
                            # também mexe no índice e nas lições do M1: a frase da sugestão «continua»); desfaz-se antes, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M2 (cuidado_m2_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M2, incluindo o índice do módulo) passa a camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção; desfaz-se primeiro, com a mesma exigência.
                            # 08/11/2026: a decisão 152 no M3 (cuidado_m3_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M3, incluindo o índice, o guia e o mapa do módulo) passa a camada mais recente, por cima da decisão 152 no M2; desfaz-se primeiro, com a mesma exigência.
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
                            # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json', '--desfazer-antes', 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-provas-oficial-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-exame-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m9-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m8-edits-20261112.json', '--desfazer-antes', 'tests/fixtures/cuidado-m7-edits-20261111.json', '--desfazer-antes', 'tests/fixtures/cuidado-m6-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/tarefas-claras-edits-20261110.json', '--desfazer-antes', 'tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m3-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cuidado-m2-edits-20261108.json', '--desfazer-antes', 'tests/fixtures/cidade-cartaz-edits-20261108.json',
                            '--desfazer-antes', 'tests/fixtures/creditos-i-pt1-edits-20261107.json'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('manifesto em dia', r.stdout)
        for t in TROCAS:
            # 07/11/2026: cada troca confere-se na página com a camada do pedido pt-1 desfeita (a camada por cima desta).
            # 08/11/2026: a mesma função desfaz antes o cartaz «Ler a cidade» e o nome novo da secção, que estão por cima do pt-1.
            texto = undo_creditos_i_pt1_0711(t['ficheiro'], ler(t['ficheiro']))
            with self.subTest(ficheiro=t['ficheiro'], local=t['local']):
                self.assertEqual(texto.count(t['novo']), t['ocorrencias'])
                self.assertEqual(texto.replace(t['novo'], '\0').count(t['antigo']), 0)
                self.assertTrue(t['achado'].startswith('06/11/2026: decisão 152'))
        self.assertEqual(set(MANIFESTO['files']), {t['ficheiro'] for t in TROCAS})
        # Os 48 achados confirmados: 12 tabelas, 2 casos do mesmo tipo e 34 achados B, todos na camada.
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import cuidado_m1_20261106 as C
            import verificar_camadas
        finally:
            sys.path.pop(0)
        self.assertEqual(sorted(x['cat'] for x in C.ACHADOS_AC).count('A'), 12)
        self.assertEqual(sorted(x['cat'] for x in C.ACHADOS_AC).count('C'), 2)
        self.assertEqual(len(C.ACHADOS_B), 34)
        achados = {int(n) for t in TROCAS for n in re.findall(r'achado ([\d, /]+) \(', t['achado'])[0].replace('/', ',').split(',')}
        self.assertEqual(achados, {x['i'] for x in C.ACHADOS_AC} | {x['i'] for x in C.ACHADOS_B})
        # No topo da cadeia.
        # 07/11/2026: logo por baixo do topo, que passa a ser dos créditos atrás de um «i» do pedido pt-1 (creditos_i_pt1_20261107);
        # a ordem ganha uma posição.
        # 08/11/2026: por cima do pt-1 fica o cartaz «Ler a cidade» e o nome novo da secção (cidade_cartaz_20261108); a ordem ganha
        # mais uma posição e esta camada passa a terceira.
        # 08/11/2026: por cima do cartaz «Ler a cidade» fica a decisão 152 no M2 (cuidado_m2_20261108); a ordem ganha mais uma
        # posição e esta camada passa a quarta.
        # 08/11/2026: por cima da decisão 152 no M2 fica a decisão 152 no M3 (cuidado_m3_20261108); a ordem ganha mais uma posição e esta camada passa a quinta.
        # 08/11/2026: por cima da decisão 152 no M3 fica a decisão 152 no M4 (cuidado_m4_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 08/11/2026: por cima da decisão 152 no M4 fica a decisão 152 no M5 (cuidado_m5_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 08/11/2026: por cima da decisão 152 no M5 fica a decisão 152 no M6 (cuidado_m6_20261108): a ordem ganha mais uma posição, com a mesma exigência.
        # 11/11/2026: por cima da decisão 152 no M6 fica a decisão 152 no M7 (cuidado_m7_20261111): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M7 fica a decisão 152 no M8 (cuidado_m8_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M8 fica a decisão 152 no M9 (cuidado_m9_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no M9 fica a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da decisão 152 no Exame e nas páginas transversais fica a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima da ligação «Treinos» na página principal do Exame ficam as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 12/11/2026: por cima das provas em cartões com os documentos oficiais ficam as duas tarefas do M3 mais fáceis de fazer (tarefas_faceis_m3_20261112): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M3 mais fáceis de fazer ficam as duas tarefas do M1 mais fáceis de fazer (tarefas_faceis_m1_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        # 13/11/2026: por cima das tarefas do M1 mais fáceis de fazer ficam as duas tarefas do M5 mais fáceis de fazer (tarefas_faceis_m5_20261113): a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[6], ('cuidado_m9_20261112', 'cuidado-m9-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[7], ('cuidado_m8_20261112', 'cuidado-m8-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[8], ('cuidado_m7_20261111', 'cuidado-m7-edits-20261111'))
        self.assertEqual(verificar_camadas.LAYERS[9], ('cuidado_m6_20261108', 'cuidado-m6-edits-20261108'))
        # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): logo abaixo da decisão 152 no M6 fica a revisão dos enunciados das tarefas (tarefas_claras_20261110, #192), por cima da decisão 152 no M5; as posições seguintes descem uma.
        self.assertEqual(verificar_camadas.LAYERS[10], ('tarefas_claras_20261110', 'tarefas-claras-edits-20261110'))
        self.assertEqual(verificar_camadas.LAYERS[11], ('cuidado_m5_20261108', 'cuidado-m5-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[12], ('cuidado_m4_20261108', 'cuidado-m4-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[13], ('cuidado_m3_20261108', 'cuidado-m3-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[14], ('cuidado_m2_20261108', 'cuidado-m2-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[15], ('cidade_cartaz_20261108', 'cidade-cartaz-edits-20261108'))
        self.assertEqual(verificar_camadas.LAYERS[16], ('creditos_i_pt1_20261107', 'creditos-i-pt1-edits-20261107'))
        self.assertEqual(verificar_camadas.LAYERS[17], ('cuidado_m1_20261106', 'cuidado-m1-edits-20261106'))
        # 07/11/2026 (fusão do main 29441e6b no pedido #182): esta camada fica por cima dos acertos da decisão 173, que ficam por cima do desenho comum dos índices
        # (decisão 148), por cima dos créditos atrás de um «i».
        # 08/11/2026: com a decisão 152 no M4 por cima de todas, cada uma destas desce uma posição.
        self.assertEqual(verificar_camadas.LAYERS[18], ('indices_acertos_20261107', 'indices-acertos-edits-20261107'))
        self.assertEqual(verificar_camadas.LAYERS[19], ('cartaz_indices_148_20261106', 'cartaz-indices-148-edits-20261106'))
        self.assertEqual(verificar_camadas.LAYERS[20], ('creditos_i_20261105', 'creditos-i-edits-20261105'))
        auditoria = ler('tests/auditoria_20261028.py')
        # 07/11/2026 (fusão do main 29441e6b no pedido #182): quem chama primeiro esta camada é a função dos acertos (os créditos chamam o desenho comum, que chama os acertos).
        corpo = auditoria[auditoria.index('def undo_acertos_0711'):]
        self.assertLess(corpo.index('undo_cuidado_m1_0611(path, text)'), corpo.index('_ACERTOS_0711.get('))
        # 07/11/2026: e esta camada desfaz primeiro a do pedido pt-1, que está por cima dela.
        corpo = auditoria[auditoria.index('def undo_cuidado_m1_0611'):]
        self.assertLess(corpo.index('undo_creditos_i_pt1_0711(path, text)'), corpo.index('_CUIDADO_M1_0611.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('cuidado-m1-edits-20261106.json'), sala.index('creditos-i-edits-20261105.json'))
        self.assertLess(sala.index('cuidado-m1-edits-20261106.json'), sala.index('indices-acertos-edits-20261107.json'))
        # 07/11/2026: na Sala desligada, a camada do pedido pt-1 desfaz-se antes desta.
        self.assertLess(sala.index('creditos-i-pt1-edits-20261107.json'), sala.index('cuidado-m1-edits-20261106.json'))
        # 08/11/2026: e, antes dela, o cartaz «Ler a cidade» e o nome novo da secção, a camada mais recente.
        self.assertLess(sala.index('cidade-cartaz-edits-20261108.json'), sala.index('creditos-i-pt1-edits-20261107.json'))
        # 08/11/2026: e, antes do cartaz, a decisão 152 no M2, a camada mais recente.
        self.assertLess(sala.index('cuidado-m2-edits-20261108.json'), sala.index('cidade-cartaz-edits-20261108.json'))
        # 08/11/2026: e, antes da do M2, a decisão 152 no M3, a camada mais recente.
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
        # Onde a camada dos créditos se desfaz antes de conferir outra (fluxos e testes da cadeia), esta desfaz-se primeiro.
        # 07/11/2026 (fusão do main 29441e6b no pedido #182): a regra é a mesma (onde se desfazem os créditos, esta camada desfaz-se
        # primeiro), mas entre esta e os créditos ficam agora os acertos da decisão 173 e o desenho comum dos índices (decisão 148),
        # por esta ordem: a cadeia inteira tem de aparecer, sem nada pelo meio.
        creditos = '--desfazer-antes tests/fixtures/creditos-i-edits-20261105.json'
        # 07/11/2026: a cadeia inteira passa a começar pelos créditos atrás de um «i» do pedido pt-1 (a camada mais recente, por cima
        # desta), com a mesma exigência: nada pelo meio.
        # 08/11/2026: e começa agora pelo cartaz «Ler a cidade» e pelo nome novo da secção (cidade_cartaz_20261108), por cima do pt-1,
        # com a mesma exigência: nada pelo meio.
        # 08/11/2026: e começa agora pela decisão 152 no M2 (cuidado_m2_20261108), por cima do cartaz, com a mesma exigência: nada pelo meio.
        # 08/11/2026: e começa agora pela decisão 152 no M3 (cuidado_m3_20261108), por cima da do M2, com a mesma exigência: nada pelo meio.
        # 08/11/2026: e começa agora pela decisão 152 no M4 (cuidado_m4_20261108), por cima da do M3, com a mesma exigência: nada pelo meio.
        # 08/11/2026: e começa agora pela decisão 152 no M5 (cuidado_m5_20261108), por cima da do M4, com a mesma exigência: nada pelo meio.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026: e, antes da do M6, a decisão 152 no M7 (cuidado_m7_20261111), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M7, a decisão 152 no M8 (cuidado_m8_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        cadeia = ('--desfazer-antes tests/fixtures/tarefas-faceis-m5-edits-20261113.json --desfazer-antes tests/fixtures/tarefas-faceis-m1-edits-20261113.json --desfazer-antes tests/fixtures/tarefas-faceis-m3-edits-20261112.json --desfazer-antes tests/fixtures/exame-provas-oficial-edits-20261112.json --desfazer-antes tests/fixtures/exame-ligacao-treinos-edits-20261112.json --desfazer-antes tests/fixtures/cuidado-exame-edits-20261112.json --desfazer-antes tests/fixtures/cuidado-m9-edits-20261112.json --desfazer-antes tests/fixtures/cuidado-m8-edits-20261112.json --desfazer-antes tests/fixtures/cuidado-m7-edits-20261111.json --desfazer-antes tests/fixtures/cuidado-m6-edits-20261108.json --desfazer-antes tests/fixtures/cuidado-m5-edits-20261108.json '
                  '--desfazer-antes tests/fixtures/cuidado-m4-edits-20261108.json '
                  '--desfazer-antes tests/fixtures/cuidado-m3-edits-20261108.json '
                  '--desfazer-antes tests/fixtures/cuidado-m2-edits-20261108.json '
                  '--desfazer-antes tests/fixtures/cidade-cartaz-edits-20261108.json '
                  '--desfazer-antes tests/fixtures/creditos-i-pt1-edits-20261107.json '
                  '--desfazer-antes tests/fixtures/cuidado-m1-edits-20261106.json --desfazer-antes tests/fixtures/indices-acertos-edits-20261107.json '
                  '--desfazer-antes tests/fixtures/cartaz-indices-148-edits-20261106.json ' + creditos)
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name == 'test_cuidado_m1.py':
                continue
            # 07/11/2026 (fusão do main 29441e6b no pedido #182): como este, os testes das camadas do desenho comum e dos acertos
            # conferem as cadeias com frases (if '…' in linha, assertIn), não as correm; ficam de fora pela mesma razão.
            if p.name in ('test_cartaz_indices_148.py', 'test_indices_acertos_20261107.py'):
                continue
            # Sem as linhas de comentário, e com as listas de argumentos («'a', 'b'») juntas numa linha de comando.
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): entre a decisão 152 no M6 e a do M5 fica a revisão dos enunciados das tarefas
            # (tarefas_claras_20261110), nas cadeias onde o #192 a pôs; nas que o #192 não mudou (test_cartaz_m4_piloto.py e test_variedade_f0.py),
            # a do M5 continua logo a seguir à do M6. A contagem lê as duas formas como uma só; nada mais cabe entre as duas.
            plano = plano.replace('--desfazer-antes tests/fixtures/cuidado-m6-edits-20261108.json' + ' --desfazer-antes tests/fixtures/tarefas-claras-edits-20261110.json ', '--desfazer-antes tests/fixtures/cuidado-m6-edits-20261108.json' + ' ')
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano.count(creditos), plano.count(cadeia))
        rotas = ler('tests/test_task_routes_closure.py')
        # 07/11/2026 (fusão do main 29441e6b no pedido #182): na cadeia das rotas, esta camada vem logo antes dos acertos da decisão 173.
        # 07/11/2026: e, antes dela, a do pedido pt-1, a primeira da cadeia.
        # 08/11/2026: e, antes de todas, a do cartaz «Ler a cidade» e do nome novo da secção.
        # 08/11/2026: e, antes de todas, a da decisão 152 no M2.
        # 08/11/2026: e, antes de todas, a da decisão 152 no M3 (cuidado_m3_20261108), por cima da do M2.
        # 08/11/2026: e, antes da do M3, a decisão 152 no M4 (cuidado_m4_20261108), a camada mais recente, sem nada pelo meio.
        # 08/11/2026: e, antes da do M4, a decisão 152 no M5 (cuidado_m5_20261108), agora a mais recente, sem nada pelo meio.
        # 08/11/2026: e, antes da do M5, a decisão 152 no M6 (cuidado_m6_20261108), agora a mais recente, sem nada pelo meio.
        # 11/11/2026: a decisão 152 no M7 (cuidado_m7_20261111: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M7, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo», «Olhar» e «Pensar devagar», e nas tarefas, nos aquecimentos e na grelha das suas unidades) passa a camada mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: e, antes da do M8, a decisão 152 no M9 (cuidado_m9_20261112), agora a mais recente, sem nada pelo meio.
        # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
        # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn("(ROOT/'tests/fixtures/tarefas-faceis-m5-edits-20261113.json',ROOT/'tests/fixtures/tarefas-faceis-m1-edits-20261113.json',ROOT/'tests/fixtures/tarefas-faceis-m3-edits-20261112.json',ROOT/'tests/fixtures/exame-provas-oficial-edits-20261112.json',ROOT/'tests/fixtures/exame-ligacao-treinos-edits-20261112.json',ROOT/'tests/fixtures/cuidado-exame-edits-20261112.json',ROOT/'tests/fixtures/cuidado-m9-edits-20261112.json',ROOT/'tests/fixtures/cuidado-m8-edits-20261112.json',ROOT/'tests/fixtures/cuidado-m7-edits-20261111.json',ROOT/'tests/fixtures/cuidado-m6-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m5-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m4-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m3-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m2-edits-20261108.json',ROOT/'tests/fixtures/cidade-cartaz-edits-20261108.json',"
                      "ROOT/'tests/fixtures/creditos-i-pt1-edits-20261107.json',"
                      "ROOT/'tests/fixtures/cuidado-m1-edits-20261106.json',ROOT/'tests/fixtures/indices-acertos-edits-20261107.json',", rotas)

    def test_paginas_geradas_saem_iguais_dos_dados(self):
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            self.assertIn('tarefas/m1-u1/index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())
        # As páginas geradas que a camada muda têm a troca também nos dados do gerador (ou no gerador: a folha e «nao_partir»).
        dados = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('docs/pedagogia/')}
        self.assertEqual(dados, {'docs/pedagogia/tarefas-escolha/m1-u1.json', 'docs/pedagogia/tarefas-escolha/m1-u2.json',
                                 'docs/pedagogia/aquecimentos/m1-u1.json', 'docs/pedagogia/grelhas-tarefas-20261027.json'})
        for slug in ('m1-u1', 'm1-u2'):
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            self.assertIs(d['nao_partir'], True)
            self.assertEqual(d['aquecer']['tabela']['colunas'], ['Momento', 'Tempo'])
        outras = [p for p in (ROOT / 'docs/pedagogia/tarefas-escolha').glob('*.json') if not p.name.startswith('m1-')]
        self.assertTrue(outras)
        for p in outras:
            d = json.loads(p.read_text('utf-8'))
            # 08/11/2026: decisão 152 no M3 (camada cuidado_m3_20261108): as tarefas da M3-U1 e da M3-U2 também levam «nao_partir»
            # (os números do molde com espaço que não quebra), mas não a tabela dos tempos; as outras ficam como estavam.
            # 08/11/2026: decisão 152 no M5 (camada cuidado_m5_20261108): as tarefas da M5-U1 e da M5-U2 levam «nao_partir» e a tabela
            # dos tempos (como as do M1, com as mesmas colunas); as outras ficam como estavam.
            # 08/11/2026: decisão 152 no M6 (camada cuidado_m6_20261108): as tarefas da M6-U1 e da M6-U2 também levam «nao_partir» (e
            # «nao_partir_grelha», conferida em test_cuidado_m6.py), mas não a tabela dos tempos (a conferência recusou-a).
            # 11/11/2026: decisão 152 no M7 (camada cuidado_m7_20261111): a tarefa da M7-U3 também leva «nao_partir» (os números do
            # molde com espaço que não quebra), sem a tabela dos tempos; as outras ficam como estavam.
            # 12/11/2026: decisão 152 no M8 (camada cuidado_m8_20261112): as tarefas da M8-U1 e da M8-U2 também levam «nao_partir» (os
            # números do molde com espaço que não quebra), sem a tabela dos tempos; as outras ficam como estavam.
            # 12/11/2026: decisão 152 no M9 (camada cuidado_m9_20261112): as tarefas da M9-U1 e da M9-U2 também levam «nao_partir» (os
            # números do molde com espaço que não quebra), sem a tabela dos tempos; as outras ficam como estavam.
            if p.name in ('m3-u1.json', 'm3-u2.json', 'm5-u1.json', 'm5-u2.json', 'm6-u1.json', 'm6-u2.json', 'm7-u3.json', 'm8-u1.json',
                          'm8-u2.json', 'm9-u1.json', 'm9-u2.json'):
                self.assertIs(d['nao_partir'], True, p.name)
            else:
                self.assertNotIn('nao_partir', d, p.name)
            if p.name in ('m5-u1.json', 'm5-u2.json'):
                self.assertEqual(d['aquecer']['tabela']['colunas'], ['Momento', 'Tempo'], p.name)
            else:
                self.assertNotIn('tabela', d['aquecer'], p.name)


if __name__ == '__main__':
    unittest.main()
