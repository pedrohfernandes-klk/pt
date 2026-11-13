"""11/11/2026: os três treinos da preparação de exame (exame/treinos/): páginas iguais ao gerador, textos oficiais iguais às
transcrições, ligações aos documentos em eduqa.pt, regras de língua no texto nosso e convenções das páginas do exame.
12/11/2026: quatro treinos, com o da sessão 17 (poesia contemporânea): as mesmas conferências, mais as citações curtas dos
poemas com direitos de autor, letra a letra com as lições do M8 de onde vêm.
12/11/2026: cinco treinos, com o da sessão 18 (conto): as mesmas conferências, mais o recorte de «George», letra a letra
com a lição M8-F16 de onde vem.
13/11/2026: oito treinos, com os das sessões 22 (coesão e modalidade), 25 (apreciação crítica) e 23 (exposição): as mesmas
conferências, mais as linhas da prova e as citações do Dicionário Terminológico do treino 6, o crédito e os direitos da imagem
do treino 7, os dois sonetos do treino 8, verso a verso, e a regra de que os limites de 200 a 350 palavras só se dizem do Grupo III."""
import json
from pathlib import Path
import re
import sys
import unittest
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import exame_treinos as G
from exame_treinos_dados import base as B, interpretacao as T1, gramatica as T2, escrita as T3, poesia_contemporanea as T4, conto as T5, indice as T0
# 13/11/2026: mais os módulos dos treinos das sessões 22, 25 e 23
from exame_treinos_dados import coesao as T6, apreciacao_critica as T7, exposicao as T8

# 12/11/2026: mais uma página, a do treino da sessão 17
# 12/11/2026: e mais outra, a do treino da sessão 18
PAGINAS = ['exame/treinos/index.html', 'exame/treinos/interpretacao/index.html', 'exame/treinos/gramatica/index.html', 'exame/treinos/escrita/index.html',
           'exame/treinos/poesia-contemporanea/index.html', 'exame/treinos/conto/index.html',
           # 13/11/2026: mais três páginas, as dos treinos das sessões 22, 25 e 23, por esta ordem
           'exame/treinos/coesao/index.html', 'exame/treinos/apreciacao-critica/index.html', 'exame/treinos/exposicao/index.html']
# 13/11/2026: a imagem da prova (Grupo III da 1.ª fase) vê-se no enunciado em eduqa.pt, na página 13; a gravura do treino 7 tem a fonte no sítio do museu
EDUQA_P13 = 'https://eduqa.pt/wp-content/uploads/2026/06/portugues_prova_639_v2_enunciado.pdf#page=13'
MET = 'https://www.metmuseum.org/art/collection/search/353966'
EDUQA = {
    'https://eduqa.pt/wp-content/uploads/2026/06/portugues_prova_639_v2_enunciado.pdf',
    'https://eduqa.pt/wp-content/uploads/2026/07/portugues_prova_639_cc.pdf',
    'https://eduqa.pt/wp-content/uploads/2026/07/EX-Port639-F2-2026-V2_net.pdf',
    'https://eduqa.pt/wp-content/uploads/2026/07/EX-Port639-F2-2026-CC-VD_net.pdf',
}


def simples(s):
    """Texto sem marcas da transcrição (_itálico_, **negrito**, [^n]) e com os espaços normalizados."""
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'(?<![\w/])_(.+?)_(?![\w/])', r'\1', s)
    s = re.sub(r'\[\^(\d+)\]', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def cadeias(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from cadeias(v)
    elif isinstance(o, list):
        for v in o:
            yield from cadeias(v)


def dados(html):
    m = re.search(r'<script type="application/json" id="treino-dados">(.*?)</script>', html, re.S)
    return json.loads(m.group(1)) if m else None


def texto(html):
    """Todo o texto que a página pode mostrar: o HTML estático e o que vem nos dados dos passos."""
    d = dados(html)
    fora = re.sub(r'<script\b.*?</script>', ' ', html, flags=re.S)
    tudo = fora + ' ' + ' '.join(cadeias(d) if d else [])
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', tudo)))


class TreinosExame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f1 = json.loads((ROOT / 'tests/fixtures/prova-639-2026-1f-v2.json').read_text('utf-8'))
        cls.f2 = json.loads((ROOT / 'tests/fixtures/prova-639-2026-2f-v2.json').read_text('utf-8'))
        cls.html = {p: (ROOT / p).read_text('utf-8') for p in PAGINAS}
        cls.texto = {p: texto(h) for p, h in cls.html.items()}

    def presentes(self, pagina, oficiais):
        t = self.texto[pagina]
        for s in oficiais:
            with self.subTest(pagina=pagina, oficial=s[:60]):
                self.assertIn(simples(s), t)

    def test_paginas_iguais_ao_gerador(self):
        geradas = G.paginas()
        self.assertEqual(PAGINAS, list(geradas))
        for p in PAGINAS:
            with self.subTest(pagina=p):
                self.assertEqual(self.html[p], geradas[p])
        self.assertEqual(0, G.main(['--check']))
        # 12/11/2026: só existem estas seis páginas em exame/treinos/ (a entrada e os cinco treinos), pela ordem de base.TREINOS
        # 13/11/2026: agora nove (a entrada e os oito treinos); a exigência é a mesma
        self.assertEqual(9, len(PAGINAS))
        self.assertEqual(PAGINAS[1:], ['exame/treinos/%s/index.html' % t for t, _ in B.TREINOS])
        self.assertEqual(sorted(PAGINAS), sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'exame/treinos').rglob('*') if p.is_file()))

    def test_interpretacao_item_oficial_igual_a_transcricao(self):
        pb = self.f1['grupos'][0]['partes'][1]
        it = pb['itens'][1]
        self.assertEqual(('I.5', 13), (it['numero'], it['cotacao']))
        cr = it['criterios']
        oficiais = list(it['enunciado']) + [pb['instrucao'], pb['textos'][0]['fonte'], cr['instrucao']]
        oficiais += [v['t'] for e in pb['textos'][0]['estrofes'] for v in e] + [n['texto'] for n in pb['notas']]
        for t in cr['topicos']:
            oficiais += [t['rotulo']] + list(t['pontos'])
        ced, cl = cr['parametros']
        oficiais += list(cadeias([n['descritores'] for n in ced['niveis']])) + [ced['nota_de_rodape'], cl['texto'], cl['nota_de_rodape']]
        self.presentes(PAGINAS[1], oficiais)
        h = self.html[PAGINAS[1]]
        # os níveis e as pontuações do parâmetro C-ED, pela ordem dos critérios
        for n in ced['niveis']:
            self.assertIn('<td class="c">%s</td>' % n['nivel'], h)
            self.assertIn('<td class="c">%s</td></tr>' % n['pontuacao'], h)
        self.assertIn('Item 5 (13 pontos', h)
        # o poema de treino é o do banco do aquecimento da sessão 14, verso a verso
        banco = json.loads((ROOT / 'docs/pedagogia/exame-aquecimentos/s14.json').read_text('utf-8'))
        versos = [unescape(v) for v in re.findall(r'<span class="ln" data-l="[^"]+">(.*?)</span>', banco['cartoes'][1]['html'])]
        self.assertEqual(12, len(versos))
        apoio = re.search(r'<div data-apoio="poema" hidden>(.*?)</div>', h, re.S).group(1)
        self.assertEqual(versos, [unescape(v) for v in re.findall(r'<li(?: class="e")?><span class="n">\d+</span><span>(.*?)</span></li>', apoio)])

    def test_gramatica_itens_oficiais_iguais_a_transcricao(self):
        p = PAGINAS[2]
        chaves = {}
        for fase, f in (('1f', self.f1), ('2f', self.f2)):
            g = f['grupos'][1]
            it = g['itens'][6]
            self.assertEqual(('II.7', 13), (it['numero'], it['cotacao']))
            self.presentes(p, list(it['enunciado']) + ['(%s) %s' % (o['letra'], simples(o['texto'])) for o in it['opcoes']])
            chaves[fase] = it['chave_versao_2']
            self.assertEqual(['7.', 13], [g['chaves_criterios_quadro']['linhas'][6][0], g['chaves_criterios_quadro']['linhas'][6][3]])
            self.assertEqual('(%s)' % it['chave_versao_2'], g['chaves_criterios_quadro']['linhas'][6][2])
        self.assertEqual({'1f': 'D', '2f': 'A'}, chaves)
        # as linhas das provas mostradas ao lado dos passos são as da transcrição, com o número da prova
        linhas = {fase: {l['n']: simples(l['t']) for l in f['grupos'][1]['textos'][0]['linhas']} for fase, f in (('1f', self.f1), ('2f', self.f2))}
        vistos = 0
        for bloco in re.findall(r'<ol class="prosa">(.*?)</ol>', self.html[p], re.S):
            for n, t in re.findall(r'<li><span class="n">(\d+)</span><span>(.*?)</span></li>', bloco):
                limpo = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', t))).strip()
                with self.subTest(linha=n, texto=limpo[:40]):
                    self.assertIn(limpo, (linhas['1f'].get(int(n)), linhas['2f'].get(int(n))))
                vistos += 1
        self.assertGreaterEqual(vistos, 10)
        # as citações do Dicionário Terminológico conferem com as entradas guardadas
        dt = json.loads((ROOT / 'tests/fixtures/dicionario-terminologico-20261111.json').read_text('utf-8'))['entradas']
        for cit, i in ((T2.DT_AG, 'n297'), (T2.DT_MOD, 'n301'), (T2.DT_OBL, 'n296'), (T2.DT_SUJ, 'n285'), (T2.DT_POS, 'n285')):
            entrada = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', dt[i]['definition'] + ' ' + (dt[i].get('notes') or ''))))
            entrada = entrada.replace(' ,', ',').replace(' .', '.').replace('( ', '(')
            self.assertIn(cit.strip('«»'), entrada)
            self.assertIn(cit, self.texto[p])

    def test_escrita_item_e_grelha_iguais_a_transcricao(self):
        p = PAGINAS[3]
        it = self.f2['grupos'][2]['itens'][0]
        cr = it['criterios']
        self.assertEqual((44, 30, 14), (it['cotacao'], cr['ETD']['pontos'], cr['CL']['pontos']))
        self.assertEqual({'min_palavras': 200, 'max_palavras': 350, 'minimo_para_classificar': 80}, it['extensao'])
        oficiais = list(it['enunciado']) + list(it['enunciado_lista']) + [cr['CL']['texto']]
        for par in cr['ETD']['parametros']:
            self.assertEqual(10, par['pontos'])
            oficiais += list(cadeias([n['descritores'] for n in par['niveis']]))
        self.presentes(p, oficiais)
        # a tabela de correção linguística (14 pontos) é a das duas fases, célula a célula
        t = self.f2['criterios']['tabelas_CL']['CL_14']
        self.assertEqual(t, self.f1['criterios']['tabelas_CL']['CL_14'])
        d = dados(self.html[p])
        tabela = next(s for s in cadeias(d) if '<table class="cl">' in s)
        corpo = re.search(r'<table class="cl">.*?<tbody>(.*?)</tbody>', tabela, re.S).group(1)
        for linha in re.findall(r'<tr>(.*?)</tr>', corpo, re.S):
            b = re.search(r'<th class="c" scope="row">(\d+)</th>', linha).group(1)
            celulas = re.findall(r'<td class="c(?: vazia)?">(.*?)</td>', linha)
            esperado = [str(t['erros_B'][b].get('A%d' % a, '')) for a in range(len(celulas))]
            self.assertEqual(esperado, celulas, b)
        self.assertEqual(len(t['erros_B']), len(re.findall(r'<tr>', corpo)))
        # as regras gerais citadas estão nos critérios gerais das duas fases
        g1, g2 = (json.dumps(f['criterios']['gerais'], ensure_ascii=False) for f in (self.f1, self.f2))
        for regra in (T3.R_DESC, T3.R_80, T3.R_CONTA, T3.R_ZERO, T3.R_MAI, T3.R_UMA, T3.R_ALT):
            self.assertIn(regra.strip('«»'), g1)
            self.assertIn(regra.strip('«»'), g2)
            self.assertIn(regra, self.texto[p])
        # nada calcula descontos nem níveis: só as regras, à vista
        self.assertNotRegex(self.texto[p], r'Dentro dos limites|Onde situas o teu texto')

    def test_poesia_item_oficial_igual_a_transcricao(self):
        # 12/11/2026: treino da sessão 17, ligado ao item 2 do Grupo I da 2.ª fase (dois poemas, um eixo, transcrições)
        p = PAGINAS[4]
        h = self.html[p]
        pa = self.f2['grupos'][0]['partes'][0]
        it = pa['itens'][1]
        self.assertEqual(('I.2', 13, 'Explique', True), (it['numero'], it['cotacao'], it['verbo_instrucional'], it['obrigatorio']))
        cr = it['criterios']
        oficiais = list(it['enunciado']) + [pa['instrucao'], cr['instrucao'], self.f2['grupos'][0]['nota_dos_criterios']] + [t['fonte'] for t in pa['textos']]
        for t in cr['topicos']:
            oficiais += [t['rotulo']] + list(t['pontos'])
        ced, cl = cr['parametros']
        oficiais += list(cadeias([n['descritores'] for n in ced['niveis']])) + [ced['nota_de_rodape'], cl['texto'], cl['nota_de_rodape']]
        # o item de 2026 com o verbo «Compare» (1.ª fase, item 2) vem citado inteiro, e é o único do Grupo I com esse verbo
        it1 = self.f1['grupos'][0]['partes'][0]['itens'][1]
        self.assertEqual(('I.2', 13, 'Compare'), (it1['numero'], it1['cotacao'], it1['verbo_instrucional']))
        oficiais += list(it1['enunciado'])
        self.presentes(p, oficiais)
        com = [(f, i['numero']) for f, d in (('1f', self.f1), ('2f', self.f2)) for pt in d['grupos'][0]['partes'] for i in pt['itens'] if re.search(r'\bCompar', ' '.join(i['enunciado']))]
        self.assertEqual([('1f', 'I.2')], com)
        for n in ced['niveis']:
            self.assertIn('<td class="c">%s</td>' % n['nivel'], h)
            self.assertIn('<td class="c">%s</td></tr>' % n['pontuacao'], h)
        self.assertIn('Item 2 (13 pontos', h)
        # as citações oficiais usadas nos passos estão nos critérios, tal e qual
        self.assertTrue(it1['criterios']['topicos'][0]['pontos'][0].startswith(T4.T_AMBOS))
        n3 = [n for n in ced['niveis'] if n['nivel'] == 3][0]
        self.assertEqual(6, n3['pontuacao'])
        self.assertIn(T4.D_UM, list(cadeias(n3['descritores'])))
        for n in ced['niveis']:
            if n['nivel'] > 3:
                self.assertNotIn(T4.D_UM, list(cadeias(n['descritores'])))
        g1, g2 = (json.dumps(f['criterios']['gerais'], ensure_ascii=False) for f in (self.f1, self.f2))
        for regra in (T4.REGRA_P2.strip('«»'), T4.R_INTRO, T4.R_CONECT, T4.R_CITAR):
            self.assertIn(regra, g1)
            self.assertIn(regra, g2)
            self.assertIn(regra, self.texto[p])
        # os dois poemas da prova não se repetem na página: só aparecem os versos que os critérios transcrevem; o resto lê-se nas provas em cartões
        crit = simples(json.dumps(cr, ensure_ascii=False))
        fora = [simples(v['t']) for t in pa['textos'] for e in t['estrofes'] for v in e if simples(v['t']) not in crit]
        self.assertGreaterEqual(len(fora), 15)
        for v in fora:
            with self.subTest(verso=v):
                self.assertNotIn(v, self.texto[p])
        self.assertIn('<a href="../../provas/2026-2f/grupo-i/">provas em cartões (2.ª fase, Grupo I)</a>', h)
        self.assertIn(fora[0], (ROOT / 'exame/provas/2026-2f/grupo-i/index.html').read_text('utf-8'))

    def test_poesia_citacoes_curtas_conferidas_com_as_licoes(self):
        # 12/11/2026: os dois poemas do treino têm direitos de autor; a página só mostra as duas citações que as lições do M8 já publicam
        p = PAGINAS[4]
        h = self.html[p]
        origem = {T4.C_SENA: 'm8/licao-m8-f03/index.html', T4.C_EUG: 'm8/licao-m8-f04/index.html'}
        self.assertEqual({'Apenas como elas. / Mas brilha.': 'm8/licao-m8-f03/index.html', 'São como um cristal, / as palavras.': 'm8/licao-m8-f04/index.html'}, origem)
        for cit, licao in origem.items():
            with self.subTest(citacao=cit):
                # letra a letra, no ficheiro publicado da lição (sem passar pelo leitor de cartões do gerador)
                self.assertIn('«%s»' % cit, (ROOT / licao).read_text('utf-8'))
                self.assertIn('«%s»' % cit, self.texto[p])
        apoio = re.search(r'<div data-apoio="cit" hidden>(.*?)</div>', h, re.S).group(1)
        self.assertEqual(['«%s»' % T4.C_SENA, '«%s»' % T4.C_EUG], [unescape(c) for c in re.findall(r'<p class="cit">(.*?)</p>', apoio)])
        # as palavras em que se toca no passo 2 são as das citações, pela ordem
        d = dados(h)
        tocar = [b for ps in d['passos'] for b in ps['blocos'] if b['t'] == 'tocar']
        self.assertEqual([T4.C_SENA, T4.C_EUG], [' '.join(t['x'] for t in b['tokens']) for b in tocar])
        # tudo o que o texto nosso põe entre «» é bocado de uma das duas citações, citação oficial conferida ou título/palavra da lista
        T4.cita_ok(T4.NOSSO)
        for mau in ('«Um verso que nenhuma lição publica»', 'como em «Carta a meus filhos»', '«brilha apenas»'):
            with self.subTest(recusa=mau):
                with self.assertRaises(AssertionError):
                    T4.cita_ok(mau)
        vistos = 0
        for c in re.findall(r'«([^«»]+)»', re.sub(r'<[^>]+>', '', T4.NOSSO)):
            if c in T4.ENTRE_ASPAS or c in T4.OFICIAIS:
                continue
            with self.subTest(entre_aspas=c):
                self.assertTrue(any(c.rstrip('.,') in cit for cit in origem), c)
            vistos += 1
        self.assertGreaterEqual(vistos, 20)
        # nenhum título nem palavra da lista é verso: nenhuma entrada da lista tem barra de verso
        self.assertEqual([], [x for x in T4.ENTRE_ASPAS if ' / ' in x])
        # remete para o manual (sem página, que as lições não dão) e para as lições, com ligação
        ta = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', apoio)))
        self.assertIn('Abre o manual', ta)
        self.assertIn('<i>Novo Sentidos 12</i> (ASA, 2023)', apoio)
        self.assertNotRegex(ta, r'(?i)manual[^.]*\bp(p|ág)?\. ?\d')
        self.assertIn('direitos de autor', ta)
        for f in ('f03', 'f04'):
            self.assertIn('<a href="../../../m8/licao-m8-%s/">' % f, apoio)
            self.assertIn('<i>Novo Sentidos 12</i>, ASA, 2023', (ROOT / ('m8/licao-m8-%s/index.html' % f)).read_text('utf-8'))
        self.assertIn('<a href="../../../m8/licao-m8-f05/">', json.dumps(d, ensure_ascii=False).replace('\\"', '"'))
        # o texto de apoio está em todos os passos
        self.assertEqual({'cit'}, {ps['apoio'] for ps in d['passos']})
        self.assertEqual(6, len(d['passos']))

    def test_conto_item_oficial_igual_a_transcricao(self):
        # 12/11/2026: treino da sessão 18, ligado ao item 4 do Grupo I da 2.ª fase (inferir traços de uma personagem, com elementos textuais)
        p = PAGINAS[5]
        h = self.html[p]
        pb = self.f2['grupos'][0]['partes'][1]
        it = pb['itens'][0]
        self.assertEqual(('I.4', 13, 'Infira', True), (it['numero'], it['cotacao'], it['verbo_instrucional'], it['obrigatorio']))
        tx = pb['textos'][0]
        self.assertEqual('texto dramático (excerto)', tx['genero'])
        cr = it['criterios']
        oficiais = list(it['enunciado']) + [pb['instrucao'], tx['fonte'], cr['instrucao'], self.f2['grupos'][0]['nota_dos_criterios']]
        oficiais += [l['t'] for l in tx['linhas']] + [n['texto'] for n in pb['notas']]
        self.assertEqual(5, len(cr['topicos']))
        for t in cr['topicos']:
            oficiais += list(t['pontos'])
        ced, cl = cr['parametros']
        oficiais += list(cadeias([n['descritores'] for n in ced['niveis']])) + [ced['nota_de_rodape'], cl['texto'], cl['nota_de_rodape']]
        # o primeiro item de 2026 sobre texto narrativo (1.ª fase, item 1) vem citado inteiro
        pa1 = self.f1['grupos'][0]['partes'][0]
        it1 = pa1['itens'][0]
        self.assertEqual(('I.1', 13, 'Explicite'), (it1['numero'], it1['cotacao'], it1['verbo_instrucional']))
        oficiais += list(it1['enunciado'])
        self.presentes(p, oficiais)
        # o excerto da prova, linha a linha, com o número da prova
        dobra = re.search(r'<details class="dobra">(.*?)</details>', h, re.S).group(1)
        linhas = re.findall(r'<li><span class="n">(\d+)</span><span>(.*?)</span></li>', re.search(r'<ol class="prosa">(.*?)</ol>', dobra, re.S).group(1))
        self.assertEqual([(str(l['n']), simples(l['t'])) for l in tx['linhas']],
                         [(n, re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', t))).strip()) for n, t in linhas])
        self.assertEqual(36, len(linhas))
        for n in ced['niveis']:
            self.assertIn('<td class="c">%s</td>' % n['nivel'], h)
            self.assertIn('<td class="c">%s</td></tr>' % n['pontuacao'], h)
        self.assertIn('Item 4 (13 pontos', h)
        # o que a página afirma sobre 2026: «Infira» só neste item do Grupo I; os textos narrativos são os dois excertos da Parte A da 1.ª fase,
        # com os verbos «Explicite» e «Compare» nos dois itens de resposta restrita
        inf = [(f, i['numero']) for f, d in (('1f', self.f1), ('2f', self.f2)) for pt in d['grupos'][0]['partes'] for i in pt['itens'] if re.search(r'\bInfir', ' '.join(i['enunciado']))]
        self.assertEqual([('2f', 'I.4')], inf)
        narr = [(f, pt['id']) for f, d in (('1f', self.f1), ('2f', self.f2)) for pt in d['grupos'][0]['partes'] if any(re.search(r'romance|conto|narrativ', t['genero']) for t in pt.get('textos', []))]
        self.assertEqual([('1f', 'A')], narr)
        self.assertEqual([('Explicite', 'construção: resposta restrita'), ('Compare', 'construção: resposta restrita')], [(i['verbo_instrucional'], i['tipo']) for i in pa1['itens'][:2]])
        self.assertTrue(pa1['itens'][2]['tipo'].startswith('seleção'))
        self.assertRegex(self.texto[p], r'No Grupo I das duas fases, o verbo «Infira» só aparece no item 4 da 2\.ª fase\. Nenhum item de 2026 manda inferir a partir de um conto\.')
        # as citações oficiais usadas nos passos estão nos critérios, tal e qual
        n5 = [n for n in ced['niveis'] if n['nivel'] == 5][0]
        n3 = [n for n in ced['niveis'] if n['nivel'] == 3][0]
        self.assertEqual((10, 6), (n5['pontuacao'], n3['pontuacao']))
        self.assertEqual(T5.D_DOIS, n5['descritores'][0][0])
        self.assertIn(T5.D_UM, list(cadeias(n3['descritores'])))
        for n in ced['niveis']:
            if n['nivel'] > 3:
                self.assertNotIn(T5.D_UM, list(cadeias(n['descritores'])))
        self.assertTrue(cr['topicos'][2]['pontos'][0].startswith(T5.T_RAC + ' («'))
        self.assertIn(T5.I_DOIS, simples(cr['instrucao']))
        for s in (T5.D_DOIS, T5.D_UM, T5.T_RAC, T5.I_DOIS):
            self.assertIn('«%s»' % s, self.texto[p])
        g1, g2 = (json.dumps(f['criterios']['gerais'], ensure_ascii=False) for f in (self.f1, self.f2))
        for regra in (T5.REGRA_P2.strip('«»'), T5.R_INTRO, T5.R_CONECT, T5.R_CITAR):
            self.assertIn(regra, g1)
            self.assertIn(regra, g2)
            self.assertIn(regra, self.texto[p])

    def test_conto_recorte_conferido_com_a_licao(self):
        # 12/11/2026: «George» tem direitos de autor; a página só mostra o recorte de duas frases que a lição M8-F16 já publica
        p = PAGINAS[5]
        h = self.html[p]
        recorte = 'À sua frente uma senhora de idade, primeiro esboçada, finalmente completa, olha-a atentamente. De idade não, George detesta eufemismos, mesmo só pensados, uma mulher velha.'
        self.assertEqual(recorte, T5.RECORTE)
        self.assertEqual([recorte], list(T5.CITACOES))
        # letra a letra, no ficheiro publicado da lição (sem passar pelo leitor de cartões do gerador)
        licao = (ROOT / 'm8/licao-m8-f16/index.html').read_text('utf-8')
        self.assertEqual(1, licao.count('«%s»' % recorte))
        self.assertIn('<blockquote class=\\"prosa\\">«%s»<\\/blockquote>' % recorte, licao)
        self.assertIn('«%s»' % recorte, self.texto[p])
        apoio = re.search(r'<div data-apoio="cit" hidden>(.*?)</div>', h, re.S).group(1)
        self.assertEqual(['«%s»' % recorte], [unescape(c) for c in re.findall(r'<p class="cit">(.*?)</p>', apoio)])
        # as palavras em que se toca no passo 2 são as do recorte (as duas frases, e depois só a segunda), pela ordem
        d = dados(h)
        tocar = [b for ps in d['passos'] for b in ps['blocos'] if b['t'] == 'tocar']
        self.assertEqual([recorte, recorte.split('. ')[1]], [' '.join(t['x'] for t in b['tokens']) for b in tocar])
        self.assertEqual(['não,', 'pensados,'], [b['tokens'][b['nucleos'][0][0]]['x'] for b in tocar])
        # tudo o que o texto nosso põe entre «» é bocado do recorte, citação oficial conferida ou título/palavra da lista
        T5.cita_ok(T5.NOSSO)
        for mau in ('«Uma frase que nenhuma lição publica»', 'como diz Georgina: «Sou eu»', '«uma velha senhora»', '«George detesta a velhice»'):
            with self.subTest(recusa=mau):
                with self.assertRaises(AssertionError):
                    T5.cita_ok(mau)
        vistos = 0
        for c in re.findall(r'«([^«»]+)»', re.sub(r'<[^>]+>', '', T5.NOSSO)):
            if c in T5.ENTRE_ASPAS or c in T5.OFICIAIS:
                continue
            with self.subTest(entre_aspas=c):
                self.assertIn(c.rstrip('.,'), recorte)
            vistos += 1
        self.assertGreaterEqual(vistos, 20)
        # nenhuma entrada da lista é frase do conto: são títulos, verbos dos enunciados e nomes de partes da página, todos curtos
        self.assertEqual([], [x for x in T5.ENTRE_ASPAS if len(x.split()) > 8 or x.endswith('.')])
        # o que a Resposta A (a insuficiente) inventa não vem entre aspas
        self.assertEqual(['George detesta eufemismos'], re.findall(r'«([^«»]+)»', T5.RESP_A))
        # dá a referência que a lição dá, remete para o manual (sem página, que as lições não dão) e para as lições, com ligação
        ta = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', apoio)))
        self.assertIn('Maria Judite de Carvalho, «George», em Seta Despedida, Mem Martins, Europa-América, 1995.', ta)
        self.assertIn('Maria Judite de Carvalho, «George», em <i>Seta Despedida<\\/i>, Mem Martins, Europa-América, 1995.', licao)
        self.assertIn('Abre o manual', ta)
        self.assertIn('<i>Novo Sentidos 12</i> (ASA, 2023)', apoio)
        self.assertNotRegex(ta, r'(?i)manual[^.]*\bp(p|ág)?\. ?\d')
        self.assertIn('direitos de autor', ta)
        self.assertEqual(['../../../m8/licao-m8-f16/', '../../../m8/licao-m8-f08/'], re.findall(r'<a href="([^"]+)"', apoio))
        self.assertIn('<i>Novo Sentidos 12</i>, ASA, 2023', (ROOT / 'm8/licao-m8-f08/index.html').read_text('utf-8'))
        self.assertIn('<a href="../../../m8/m8-george-tres-idades/">', json.dumps(d, ensure_ascii=False).replace('\\"', '"'))
        self.assertIn('"titulo":"Passagem, leitura, limite"', (ROOT / 'm8/m8-george-tres-idades/index.html').read_text('utf-8'))
        # a página não diz quem é a mulher do recorte, porque as lições não o dizem
        self.assertNotRegex(self.texto[p], r'(?i)a mulher (velha )?é Georgina|Georgina é a mulher|é a própria George')
        # o texto de apoio está em todos os passos
        self.assertEqual({'cit'}, {ps['apoio'] for ps in d['passos']})
        self.assertEqual(7, len(d['passos']))

    # ---------- 13/11/2026: treinos das sessões 22, 25 e 23 ----------
    def test_coesao_itens_oficiais_iguais_a_transcricao(self):
        # 13/11/2026: treino da sessão 22, ligado aos itens 5 e 6 do Grupo II da 2.ª fase (coesão gramatical referencial; modalidade)
        p = PAGINAS[6]
        h = self.html[p]
        g = self.f2['grupos'][1]
        for n, chave, linha in ((5, 'D', ['5.', '(C)', '(D)', 13]), (6, 'C', ['6.', '(A)', '(C)', 13])):
            it = g['itens'][n - 1]
            self.assertEqual(('II.%d' % n, 13, False, chave), (it['numero'], it['cotacao'], it['obrigatorio'], it['chave_versao_2']))
            self.assertEqual(linha, g['chaves_criterios_quadro']['linhas'][n - 1])
            self.presentes(p, list(it['enunciado']) + ['(%s) %s' % (o['letra'], simples(o['texto'])) for o in it['opcoes']])
            # os dois itens são opcionais (contam os três melhores de cinco) e a página di-lo, com a frase da prova
            self.assertIn('II.%d' % n, self.f2['cotacoes']['opcionais']['itens'])
        self.assertIn('«%s»' % self.f2['cotacoes']['opcionais']['texto'], self.texto[p])
        self.assertEqual(self.f1['cotacoes']['opcionais']['texto'], self.f2['cotacoes']['opcionais']['texto'])
        self.assertGreaterEqual(self.texto[p].count('é um dos cinco itens de que contam os três melhores'), 3)
        self.assertNotIn('conta sempre', self.texto[p])
        d = dados(h)
        # as chaves oficiais, com a página dos critérios; a do item 5 só aparece depois de guardada a resposta (passo 6)
        self.assertIn('Chave oficial: Versão 2, (C); 13 pontos (critérios da 2.ª fase, p. 13', self.texto[p])
        comp = [ps for ps in d['passos'] if ps['id'] == 'comparar'][0]
        self.assertEqual('p6-resposta', comp['precisa'])
        self.assertIn('<b>Chave do item 5:</b> Versão 1, (C); Versão 2, <b>(D)</b>. Pontuação: 13.', json.dumps(comp, ensure_ascii=False))
        antes = json.dumps([ps for ps in d['passos'] if ps['id'] in ('pedido', 'localizar', 'distinguir', 'situar', 'responder')], ensure_ascii=False)
        self.assertNotRegex(antes, r'Versão 2, <b>\(D\)|opção \(D\)|\(D\) é a opção certa')
        it6 = [b for ps in d['passos'] for b in ps['blocos'] if b.get('id') == 'p6-item6'][0]
        self.assertEqual(('oficial', 2), (it6['etq'], it6['c']))
        self.assertEqual([simples(o['texto']) for o in g['itens'][5]['opcoes']], [unescape(re.sub(r'<[^>]+>', '', o['t'])) for o in it6['o']])
        # as linhas da prova mostradas ao lado dos passos são as da transcrição, com o número da prova; a linha 24 não entra
        linhas = {l['n']: simples(l['t']) for l in g['textos'][0]['linhas']}
        vistos = set()
        for bloco in re.findall(r'<ol class="prosa">(.*?)</ol>', h, re.S):
            for n, t in re.findall(r'<li><span class="n">(\d+)</span><span>(.*?)</span></li>', bloco):
                limpo = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', t))).strip()
                with self.subTest(linha=n):
                    self.assertEqual(linhas[int(n)], limpo)
                vistos.add(int(n))
        self.assertEqual(set(T6.MOSTRADAS), vistos)
        self.assertEqual(23, len(vistos))
        self.assertNotIn(24, vistos)
        self.assertNotIn('—', self.texto[p])
        self.assertEqual(4, h.count(': ver o PDF da prova]'))
        # os realces são as doze expressões do item 5 (uma parte-se em duas linhas) e as expressões das perguntas de treino
        ap = {k: re.search(r'<div data-apoio="%s" hidden>(.*?)</div>' % k, h, re.S).group(1) for k in ('of', 'tr', 'mod')}
        marcas = [unescape(re.sub(r'<[^>]+>', '', m)) for m in re.findall(r'<mark>(.*?)</mark>', ap['of'])]
        self.assertEqual(13, len(marcas))
        todas = ' '.join(o['texto'] for o in g['itens'][4]['opcoes'])
        for m in marcas:
            if m not in ('os', 'segundos'):
                self.assertIn('«%s»' % m, simples(todas))
        self.assertEqual(['a', 'esta questão', 'na qual', 'na atualidade'], re.findall(r'<mark>(.*?)</mark>', ap['tr']))
        self.assertEqual(['podemos fazer', 'para que', 'pois', 'tem de estar', 'pode implicar'], re.findall(r'<mark>(.*?)</mark>', ap['mod']))
        # as palavras em que se toca são as das linhas da prova, pela ordem
        junto = ' '.join(linhas[n] for n in range(11, 16))
        tocar = [b for ps in d['passos'] for b in ps['blocos'] if b['t'] == 'tocar']
        self.assertEqual(['p6-qual', 'p6-a', 'p6-modo'], [b['id'] for b in tocar])
        for b in tocar:
            self.assertIn(unescape(re.sub(r'<[^>]+>', '', ' '.join(t['x'] for t in b['tokens']))), junto)
        self.assertEqual(['vida', 'visão', 'acabe'], [b['tokens'][b['nucleos'][0][0]]['x'] for b in tocar])
        # as citações do Dicionário Terminológico conferem com as entradas guardadas a 13/11/2026 e estão na página
        dt = json.loads((ROOT / 'tests/fixtures/dicionario-terminologico-20261113.json').read_text('utf-8'))['entradas']
        self.assertEqual(['n390', 'n402', 'n420', 'n462', 'n463'], sorted(dt))
        self.assertEqual(9, len(T6.DT_CITA))
        for cit, i in T6.DT_CITA:
            entrada = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', dt[i]['definition'] + ' ' + (dt[i].get('examples') or '') + ' ' + (dt[i].get('notes') or ''))))
            entrada = entrada.replace(' ,', ',').replace(' .', '.').replace('( ', '(').replace(' )', ')')
            with self.subTest(citacao=cit[:40]):
                self.assertIn(cit.strip('«»'), entrada)
                self.assertIn(cit, self.texto[p])
        self.assertGreaterEqual(h.count('consultado a 13/11/2026; grafia do original'), 5)
        # as citações dos critérios estão nos critérios gerais das duas fases e no parâmetro C do Grupo III (p. 15), tal e qual
        g1, g2 = (json.dumps(f['criterios']['gerais'], ensure_ascii=False) for f in (self.f1, self.f2))
        for regra in (T6.R_DICO, T6.R_CONECT, T6.R_COES):
            self.assertIn(regra, g1)
            self.assertIn(regra, g2)
            self.assertIn('«%s»' % regra, self.texto[p])
        self.assertIn('sem recurso obrigatório a conectores interfrásicos', T6.R_CONECT)
        for f in (self.f1, self.f2):
            c4 = f['grupos'][2]['itens'][0]['criterios']['ETD']['parametros'][2]['niveis'][0]['descritores'][0]
            self.assertEqual([T6.C_LIGAR + ';', T6.C_RETOMAR + ';', T6.C_SITUAR + '.'], c4[3:6])
        for c in (T6.C_LIGAR, T6.C_RETOMAR, T6.C_SITUAR):
            self.assertIn('«%s»' % c, self.texto[p])
        self.assertIn('mecanismos de articulação interfrásica', T6.C_LIGAR)
        # as frases de treino vêm do aquecimento da sessão 22; tudo o que explica as chaves vem dito como leitura nossa
        banco = (ROOT / 'docs/pedagogia/exame-aquecimentos/s22.json').read_text('utf-8')
        for fr in (T6.F_INES, T6.F_TALVEZ):
            self.assertIn('_%s_' % fr, banco)
            self.assertIn(fr, self.texto[p])
        self.assertGreaterEqual(self.texto[p].count('leitura nossa'), 5)
        # nada sobre limites de palavras nem sobre conectores obrigatórios; sete passos; a página liga às provas em cartões
        self.assertNotRegex(self.texto[p], r'200 a 350|duzentas|\d+ a \d+ palavras|80.120')
        self.assertEqual(7, len(d['passos']))
        self.assertEqual({'of', 'tr', 'mod'}, {ps['apoio'] for ps in d['passos']})
        for href in ('../../provas/2026-1f/grupo-ii/', '../../provas/2026-2f/grupo-ii/'):
            self.assertIn('<a href="%s">' % href, json.dumps(d, ensure_ascii=False).replace('\\"', '"'))

    def test_apreciacao_item_e_grelha_iguais_a_transcricao(self):
        # 13/11/2026: treino da sessão 25, ligado ao Grupo III da 1.ª fase (apreciação crítica de uma imagem)
        p = PAGINAS[7]
        h = self.html[p]
        it = self.f1['grupos'][2]['itens'][0]
        cr = it['criterios']
        self.assertEqual((44, 30, 14, True), (it['cotacao'], cr['ETD']['pontos'], cr['CL']['pontos'], it['obrigatorio']))
        self.assertEqual({'min_palavras': 200, 'max_palavras': 350, 'minimo_para_classificar': 80}, it['extensao'])
        oficiais = list(it['enunciado']) + list(it['enunciado_lista']) + [cr['CL']['texto'], it['imagem']['fonte']]
        for o in it['observacoes']:
            oficiais += [o] if isinstance(o, str) else [o['texto']] + list(o['lista'])
        for par in cr['ETD']['parametros']:
            self.assertEqual(10, par['pontos'])
            self.assertEqual([(4, 10), (3, 8), (2, 5), (1, 3)], [(n['nivel'], n['pontuacao']) for n in par['niveis']])
            oficiais += list(cadeias([n['descritores'] for n in par['niveis']]))
        oficiais.append(cr['ETD']['parametros'][0]['nota'])
        self.presentes(p, oficiais)
        # o pedido de treino é o enunciado da prova com duas mudanças ditas: a imagem e o tratamento por «tu»; a lista é a da prova, letra a letra
        self.assertEqual(simples(it['enunciado'][0]).replace('faça', 'faz').replace('do cartoon, da autoria de Javad Takjoo', 'da gravura, da autoria de Giovanni Battista Piranesi'),
                         unescape(re.sub(r'<[^>]+>', '', T7.PEDIDO_1)))
        self.assertIn('O que mudou em relação ao item oficial: a imagem', self.texto[p])
        d = dados(h)
        # a tabela de correção linguística (14 pontos) é a das duas fases, célula a célula
        t = self.f1['criterios']['tabelas_CL']['CL_14']
        self.assertEqual(t, self.f2['criterios']['tabelas_CL']['CL_14'])
        tabela = next(s for s in cadeias(d) if '<table class="cl">' in s)
        corpo = re.search(r'<table class="cl">.*?<tbody>(.*?)</tbody>', tabela, re.S).group(1)
        for linha in re.findall(r'<tr>(.*?)</tr>', corpo, re.S):
            b = re.search(r'<th class="c" scope="row">(\d+)</th>', linha).group(1)
            celulas = re.findall(r'<td class="c(?: vazia)?">(.*?)</td>', linha)
            self.assertEqual([str(t['erros_B'][b].get('A%d' % a, '')) for a in range(len(celulas))], celulas, b)
        self.assertEqual(len(t['erros_B']), len(re.findall(r'<tr>', corpo)))
        # as regras gerais citadas estão nos critérios gerais das duas fases
        g1, g2 = (json.dumps(f['criterios']['gerais'], ensure_ascii=False) for f in (self.f1, self.f2))
        for regra in (T7.R_DESC, T7.R_80, T7.R_CONTA, T7.R_ZERO, T7.R_MAI, T7.R_UMA, T7.R_ALT):
            self.assertIn(regra.strip('«»'), g1)
            self.assertIn(regra.strip('«»'), g2)
            self.assertIn(regra, self.texto[p])
        # os descritores citados nos passos são os do parâmetro A (p. 14), com a pontuação certa
        pa = cr['ETD']['parametros'][0]
        self.assertTrue(pa['niveis'][1]['descritores'][0][0].endswith(T7.D_DOIS) and pa['niveis'][1]['pontuacao'] == 8)
        self.assertTrue(pa['niveis'][2]['descritores'][0][0].endswith(T7.D_UM) and pa['niveis'][2]['pontuacao'] == 5)
        for s in (T7.D_DOIS, T7.D_UM, T7.A_DESC, T7.A_COM, T7.A_CONC, T7.B_ASP, T7.B_REG, T7.C_PARTES):
            self.assertIn(s, self.texto[p])
        self.assertIn('três aspetos relevantes', it['enunciado_lista'][1])
        self.assertIn('três aspetos distintos', pa['niveis'][0]['descritores'][0][2])
        self.assertIn('o enunciado diz «três aspetos relevantes» (p. 13); o parâmetro A diz «três aspetos distintos» (p. 14)', self.texto[p])
        # as palavras em que se toca são as do segundo ponto da lista do enunciado, pela ordem
        tocar = [b for ps in d['passos'] for b in ps['blocos'] if b['t'] == 'tocar']
        self.assertEqual([it['enunciado_lista'][1]], [' '.join(t['x'] for t in b['tokens']) for b in tocar])
        self.assertEqual('três', tocar[0]['tokens'][tocar[0]['nucleos'][0][0]]['x'])
        # nada calcula descontos nem níveis; a marcação é aspeto a aspeto (3 + 4 + 5), com os aspetos do nível 4, letra a letra
        self.assertNotRegex(self.texto[p], r'Dentro dos limites|Onde situas o teu texto')
        grelhas = [b for ps in d['passos'] for b in ps['blocos'] if b['t'] == 'grelha']
        self.assertEqual([3, 4, 5], [len(b['aspetos']) for b in grelhas])
        for b, par in zip(grelhas, cr['ETD']['parametros']):
            esperados = [simples(x).rstrip(';.') for x in par['niveis'][0]['descritores'][0][1:]]
            self.assertEqual(esperados, [unescape(re.sub(r'<[^>]+>', '', a)) for a in b['aspetos']][-len(esperados):])
            self.assertEqual(['Está no meu texto', 'Está, com falhas', 'Não está'], b['opcoes'])
        # o exemplo comentado fica dentro dos limites do item
        self.assertTrue(200 <= T7.N_MODELO <= 350)
        self.assertEqual(T7.N_MODELO, sum(len(a.split()) for a, _ in T7.MODELO))
        self.assertIn('com %d palavras' % T7.N_MODELO, self.texto[p])
        # a reserva e as duas características vêm da sessão 25, não do item: a página di-lo; nenhuma pergunta nem aspeto da grelha pede reserva
        self.assertIn('O item não a pede; quem a propõe é a sessão 25 (orientação nossa).', self.texto[p])
        self.assertIn('analisa duas características', unescape((ROOT / 'assets/exame/sessoes.json').read_text('utf-8')))
        for b in [b for ps in d['passos'] for b in ps['blocos'] if b['t'] in ('escolha', 'tocar', 'grelha')]:
            self.assertNotRegex(json.dumps([b.get('p'), b.get('o'), b.get('aspetos')], ensure_ascii=False), r'(?i)reserva')
        self.assertEqual(6, len(d['passos']))
        self.assertEqual({'img'}, {ps['apoio'] for ps in d['passos']})
        self.assertIn('<a href="../../provas/2026-1f/grupo-iii/">', json.dumps(d, ensure_ascii=False).replace('\\"', '"'))

    def test_apreciacao_imagem_com_credito_e_sem_a_imagem_da_prova(self):
        # 13/11/2026: a imagem da prova (cartoon de Javad Takjoo) tem direitos e não se reproduz; o treino usa uma gravura em domínio público
        # que o repositório já publica, com o crédito do registo das imagens das lições
        p = PAGINAS[7]
        h = self.html[p]
        self.assertEqual(['../../../img/fontes/licoes-20261101/piranesi.jpg'], re.findall(r'<img[^>]* src="([^"]+)"', h))
        self.assertEqual(1, h.count('<img '))
        self.assertTrue((ROOT / 'img/fontes/licoes-20261101/piranesi.jpg').is_file())
        self.assertNotRegex(h, r'(?i)takjoo\.(jpg|jpeg|png|webp|gif|svg)|<svg|<picture|<canvas|background-image')
        self.assertEqual([], [f.name for f in (ROOT / 'exame/treinos/apreciacao-critica').iterdir() if f.name != 'index.html'])
        self.assertEqual([], [f for f in (ROOT / 'img').rglob('*') if 'takjoo' in f.name.lower()])
        prova = json.loads((ROOT / 'scripts/provas/dados/2026-1f/prova.json').read_text('utf-8'))
        self.assertIn('"reproduzir": false', json.dumps(prova, ensure_ascii=False))
        # a fonte da imagem da prova vem como a prova a indica, em texto simples (sem ligação para fora de eduqa.pt)
        self.assertIn('https://takjoo.com (consultado em 23/02/2026).', self.texto[p])
        self.assertNotIn('href="https://takjoo.com', h)
        self.assertGreaterEqual(self.texto[p].count('tem direitos de autor'), 3)
        # o crédito é o do registo (scripts/imagens_licoes_20261101.py), campo a campo, e o texto alternativo é o da lição M9-F14
        registo = (ROOT / 'scripts/imagens_licoes_20261101.py').read_text('utf-8')
        self.assertIn('"""Documentos visuais inspecionados em 01/11/2026, com direitos verificados."""', registo)
        img = T7.IMG
        for campo, valor in (('autor', 'Giovanni Battista Piranesi'), ('obra', 'Vista interior da Basílica de São Pedro, da série Vedute di Roma'), ('data', 'Cerca de 1748'),
                             ('instituicao', 'The Metropolitan Museum of Art, inventário 1972.620.1. Oferta de Mrs. Otto F. Langmann, 1972.'), ('licenca', 'Domínio público'),
                             ('fonte', MET), ('direitos', MET)):
            with self.subTest(campo=campo):
                self.assertEqual(valor, img[campo])
                self.assertIn("%s='%s'" % (campo, valor), registo)
        apoio = re.search(r'<div data-apoio="img" hidden>(.*)</div><div class="apoio-cab">|<div data-apoio="img" hidden>(.*?)</div></div></aside>', h, re.S)
        apoio = next(x for x in apoio.groups() if x)
        ta = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', apoio)))
        for valor in ('Giovanni Battista Piranesi', 'Vista interior da Basílica de São Pedro, da série Vedute di Roma', 'Cerca de 1748',
                      'The Metropolitan Museum of Art, inventário 1972.620.1. Oferta de Mrs. Otto F. Langmann, 1972.', 'Domínio público', 'Redimensionada, sem recorte.'):
            self.assertIn(valor, ta)
        self.assertIn('<i>Vedute di Roma</i>', apoio)
        self.assertIn('<a href="%s" target="_blank" rel="noopener">' % MET, apoio)
        self.assertIn(' alt="%s"' % img['alt'], apoio)
        self.assertIn(' width="800" height="551"', apoio)
        licao = (ROOT / 'm9/licao-m9-f14/index.html').read_text('utf-8')
        self.assertIn('piranesi.jpg', licao)
        self.assertIn(img['alt'], unescape(licao))
        self.assertIn('<a href="../../../m9/licao-m9-f14/">', apoio)
        # a imagem não é de IA nem vem de fora: o estilo só lhe dá tamanho, e o ficheiro é o que a lição já usa
        css = (ROOT / 'assets/exame/treino.css').read_text('utf-8')
        self.assertIn('.apoio-img img{', css)
        # o pedido de treino fica junto da imagem, em todos os passos
        self.assertIn('faz a apreciação crítica da gravura, da autoria de Giovanni Battista Piranesi.', ta)

    def test_exposicao_item_oficial_igual_a_transcricao(self):
        # 13/11/2026: treino da sessão 23, ligado ao item 7 do Grupo I da 2.ª fase (breve exposição sobre a lírica de Camões)
        p = PAGINAS[8]
        h = self.html[p]
        pc = self.f2['grupos'][0]['partes'][2]
        it = pc['itens'][0]
        self.assertEqual(('I.7', 13, True, 'construção: resposta restrita (breve exposição)'), (it['numero'], it['cotacao'], it['obrigatorio'], it['tipo']))
        self.assertIn(['I.7', 13], self.f2['cotacoes']['obrigatorios']['itens'])
        cr = it['criterios']
        oficiais = list(it['enunciado']) + list(it['enunciado_lista']) + [cr['instrucao'], cr['introducao_topicos']]
        self.assertEqual(7, len(cr['topicos']))
        for t in cr['topicos']:
            oficiais += list(t['pontos'])
        c, ed, cl = cr['parametros']
        self.assertEqual([('C', 8), ('ED', 3), ('CL', 2)], [(x['sigla'], x['pontos']) for x in (c, ed, cl)])
        oficiais += list(cadeias([n['descritores'] for n in c['niveis'] + ed['niveis']])) + [ed['nota_de_rodape'], cl['texto'], cl['nota_de_rodape']]
        self.presentes(p, oficiais)
        d = dados(h)
        todo = json.dumps(d, ensure_ascii=False)
        for par in (c, ed):
            for n in par['niveis']:
                self.assertIn('<td class=\\"c\\">%s</td>' % n['nivel'], todo)
                self.assertIn('<td class=\\"c\\">%s</td></tr>' % n['pontuacao'], todo)
        # a tabela de correção linguística (2 pontos), célula a célula
        t = self.f2['criterios']['tabelas_CL']['CL_2']
        self.assertEqual(t, self.f1['criterios']['tabelas_CL']['CL_2'])
        tabela = next(s for s in cadeias(d) if '<table class="cl">' in s)
        corpo = re.search(r'<table class="cl">.*?<tbody>(.*?)</tbody>', tabela, re.S).group(1)
        for linha in re.findall(r'<tr>(.*?)</tr>', corpo, re.S):
            b = re.search(r'<th class="c" scope="row">(\d+)</th>', linha).group(1)
            celulas = re.findall(r'<td class="c(?: vazia)?">(.*?)</td>', linha)
            self.assertEqual([str(t['erros_B'][b].get('A%d' % a, '')) for a in range(len(celulas))], celulas, b)
        self.assertEqual(len(t['erros_B']), len(re.findall(r'<tr>', corpo)))
        # as citações oficiais usadas nos passos estão nos critérios, tal e qual, com o nível e a pontuação que a página lhes dá
        self.assertEqual([[T8.D_C4]], c['niveis'][0]['descritores'])
        self.assertEqual((4, 8), (c['niveis'][0]['nivel'], c['niveis'][0]['pontuacao']))
        self.assertEqual(([T8.D_C2B], 2, 4), (c['niveis'][2]['descritores'][1], c['niveis'][2]['nivel'], c['niveis'][2]['pontuacao']))
        self.assertEqual((T8.D_ED3, 3, 3), (ed['niveis'][0]['descritores'][0][0], ed['niveis'][0]['nivel'], ed['niveis'][0]['pontuacao']))
        self.assertEqual((T8.D_ED2, 2, 2), (ed['niveis'][1]['descritores'][0][0], ed['niveis'][1]['nivel'], ed['niveis'][1]['pontuacao']))
        self.assertIn(T8.ED_PARTES, T8.D_ED3)
        self.assertIn(T8.ED_COES, T8.D_ED3)
        self.assertIn(T8.ED_DESEQ, T8.D_ED2)
        self.assertEqual(T8.I_DOIS, simples(cr['instrucao']))
        self.assertTrue(cr['topicos'][0]['pontos'][0].startswith(T8.T_AMOR + ' (') and '«%s»' % T8.T_AMOR_V in cr['topicos'][0]['pontos'][0])
        self.assertEqual(T8.T_MORTE + ' («%s»);' % T8.T_MORTE_V, cr['topicos'][1]['pontos'][0])
        for s in (T8.D_C4, T8.D_C2B, T8.D_ED3, T8.ED_PARTES, T8.ED_DESEQ, T8.T_AMOR, T8.T_MORTE, T8.T_AMOR_V, T8.T_MORTE_V):
            self.assertIn('«%s»' % s, self.texto[p])
        g1, g2 = (json.dumps(f['criterios']['gerais'], ensure_ascii=False) for f in (self.f1, self.f2))
        for regra in (T8.REGRA_P2, T8.R_INTRO, T8.R_PARAG, T8.R_CONECT, T8.R_CITAR, T8.R_DESC.strip('«»')):
            self.assertIn(regra, g1)
            self.assertIn(regra, g2)
            self.assertIn('«%s»' % regra, self.texto[p])
        self.assertIn('sem recurso obrigatório a conectores interfrásicos', T8.R_CONECT)
        self.assertTrue(T8.R_INTRO.startswith('exceto quando tal é expressamente requerido no item'))
        # o item pede introdução e conclusão (p. 5): a página só as dá como pedidas aqui, pelo item
        self.assertEqual(('uma introdução ao tema;', 'uma conclusão adequada ao desenvolvimento do tema.'), (it['enunciado_lista'][0], it['enunciado_lista'][2]))
        self.assertIn('Neste item, a introdução e a conclusão são pedidas pelo enunciado.', self.texto[p])
        # a mesma breve exposição na 1.ª fase: mesma cotação, mesma divisão, mesmos níveis de estruturação; o enunciado da 1.ª fase não se reproduz
        it1 = self.f1['grupos'][0]['partes'][2]['itens'][0]
        self.assertEqual(('I.7', 13, it['tipo']), (it1['numero'], it1['cotacao'], it1['tipo']))
        self.assertEqual([('C', 8), ('ED', 3), ('CL', 2)], [(x['sigla'], x['pontos']) for x in it1['criterios']['parametros']])
        self.assertEqual(ed['niveis'], it1['criterios']['parametros'][1]['niveis'])
        self.assertEqual((it['enunciado_lista'][0], it['enunciado_lista'][2]), (it1['enunciado_lista'][0], it1['enunciado_lista'][2]))
        self.assertNotIn(simples(it1['enunciado'][0]), self.texto[p])
        # autoavaliação só por marcação aspeto a aspeto (4 + 5), sem níveis nem contas
        grelhas = [b for ps in d['passos'] for b in ps['blocos'] if b['t'] == 'grelha']
        self.assertEqual([4, 5], [len(b['aspetos']) for b in grelhas])
        for b in grelhas:
            self.assertEqual(['Está no meu texto', 'Está, com falhas', 'Não está'], b['opcoes'])
        self.assertEqual(['uma introdução ao tema', 'um desenvolvimento', 'uma conclusão adequada ao desenvolvimento do tema'], grelhas[1]['aspetos'][:3])
        self.assertNotRegex(self.texto[p], r'Dentro dos limites|Onde situas o teu texto|Em que nível')
        self.assertNotRegex(json.dumps([b['aspetos'] for b in grelhas], ensure_ascii=False), r'(?i)um poema (diferente )?para cada|dois poemas')
        self.assertIn('não exige um poema diferente para cada reflexão', grelhas[0]['intro'])
        self.assertEqual(8, len(d['passos']))
        self.assertEqual({'item', 'poemas'}, {ps['apoio'] for ps in d['passos']})
        self.assertEqual(['comparar', 'rever'], [ps['id'] for ps in d['passos'] if ps.get('precisa') == 'p8-resposta'])

    def test_exposicao_sonetos_conferidos_com_as_paginas_do_m3(self):
        # 13/11/2026: os dois sonetos do treino 8 estão em domínio público e vêm, verso a verso, de páginas já publicadas
        p = PAGINAS[8]
        h = self.html[p]
        banco = json.loads((ROOT / 'docs/pedagogia/exame-aquecimentos/s04.json').read_text('utf-8'))
        alma = [unescape(v) for v in re.findall(r'<span class="ln" data-l="0-\d+">(.*?)</span>', banco['cartoes'][1]['html'])]
        m3 = (ROOT / 'm3/m3-soneto-raciocinio/index.html').read_text('utf-8')
        bloco = [m for m in re.findall(r'<blockquote class=\\"cit\\">(.*?)</blockquote>', m3, re.S) if 'Amor é fogo' in m][0]
        amor = [unescape(v) for v in re.findall(r'<p>(.*?)</p>', bloco)]
        self.assertEqual((14, 14), (len(alma), len(amor)))
        self.assertEqual((alma, amor), (T8.ALMA, T8.AMOR))
        apoio = re.search(r'<div data-apoio="poemas" hidden>(.*?)</div>', h, re.S).group(1)
        poemas = re.findall(r'<ol class="poema">(.*?)</ol>', apoio, re.S)
        self.assertEqual(2, len(poemas))
        for esperado, ol in zip((alma, amor), poemas):
            versos = re.findall(r'<li(?: class="e")?><span class="n">(\d+)</span><span>(.*?)</span></li>', ol)
            self.assertEqual([(str(i + 1), v) for i, v in enumerate(esperado)], [(n, unescape(v)) for n, v in versos])
            self.assertEqual(3, ol.count('<li class="e">'))
        licao = (ROOT / 'm3/licao-m3-f09/index.html').read_text('utf-8').replace('\xa0', ' ')
        for v in ('Repousa lá no céu eternamente,', 'E viva eu cá na terra sempre triste.'):
            self.assertIn(v, licao)
        self.assertIn('a antítese separa-os: «lá no céu», «cá na terra».', licao)
        # as fontes são as das páginas de origem, e a página diz que os sonetos estão em domínio público e não saíram impressos na prova
        ta = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', apoio)))
        self.assertIn('Luís de Camões, Rhythmas (1595), soneto XIII (grafia modernizada).', ta)
        self.assertIn('Obras Completas, tomo II (transcrição do Project Gutenberg n.º 31509); aqui moderniza-se a grafia.', ta)
        self.assertIn(T8.FONTE_AMOR, m3.replace('\xa0', ' '))
        self.assertIn('Os dois sonetos estão em domínio público.', ta)
        self.assertEqual(['../../../m3/licao-m3-f09/', '../../../m3/m3-soneto-raciocinio/'], re.findall(r'<a href="([^"]+)"', apoio))
        self.assertFalse(self.f2['grupos'][0]['partes'][2].get('textos'))
        # as palavras em que se toca são os versos, pela ordem; cada busca tem uma só resposta
        d = dados(h)
        tocar = [b for ps in d['passos'] for b in ps['blocos'] if b['t'] == 'tocar']
        self.assertEqual([alma[:4], amor], [[unescape(t['x']) for t in b['tokens']] for b in tocar])
        self.assertEqual([[[2, 3]], [[11]]], [b['nucleos'] for b in tocar])
        self.assertEqual([i for i, v in enumerate(alma[:4]) if re.search(r'\b(lá|cá)\b', v)], [2, 3])
        self.assertEqual([i for i, v in enumerate(amor) if not v.startswith(('Amor é', 'É '))], [11, 12, 13])
        # tudo o que o texto nosso põe entre «» é verso dos dois sonetos, citação oficial conferida ou título/palavra da lista
        T8.cita_ok(T8.NOSSO)
        for mau in ('«Um verso que nenhuma página publica»', '«Amor é um fogo que arde sem se ver»', '«cá na terra sempre tão triste»', 'como em «Mudam-se os tempos, mudam-se as vontades»'):
            with self.subTest(recusa=mau):
                with self.assertRaises(AssertionError):
                    T8.cita_ok(mau)
        versos = ' / '.join(alma) + ' // ' + ' / '.join(amor)
        vistos = 0
        for c in re.findall(r'«([^«»]+)»', re.sub(r'<[^>]+>', '', T8.NOSSO)):
            if c in T8.ENTRE_ASPAS or c in T8.OFICIAIS:
                continue
            with self.subTest(entre_aspas=c):
                self.assertTrue(c in versos or c.rstrip('.,') in versos, c)
            vistos += 1
        self.assertGreaterEqual(vistos, 20)
        self.assertEqual([], [x for x in T8.ENTRE_ASPAS if ' / ' in x or len(x.split()) > 8])
        # a vírgula que os critérios põem no verso 2 não está no texto da página, e a página di-lo
        self.assertIn('É ferida que dói e não se sente;', amor)
        self.assertNotIn(T8.T_AMOR_V, versos)
        self.assertIn('com vírgula; nesta página, o verso 2 vem sem ela', self.texto[p])

    def test_limites_de_palavras_so_no_grupo_iii(self):
        # 13/11/2026: os limites de 200 a 350 palavras só existem no Grupo III (enunciados, pp. 13 e 8; critérios, p. 3): nenhuma página os dá a outro item
        for f in (self.f1, self.f2):
            self.assertEqual((200, 350), (f['grupos'][2]['itens'][0]['extensao']['min_palavras'], f['grupos'][2]['itens'][0]['extensao']['max_palavras']))
            for g in f['grupos'][:2]:
                for it in [i for pt in g.get('partes', []) for i in pt['itens']] + g.get('itens', []):
                    self.assertNotIn('extensao', it)
                    self.assertNotRegex(' '.join(it['enunciado']), r'(?i)duzentas|trezentas|\d+ palavras')
        limite = r'200 a 350|200.{1,3}350|duzentas'
        # os treinos que não são do Grupo III não falam destes limites
        for i in (1, 2, 4, 5, 6):
            with self.subTest(pagina=PAGINAS[i]):
                self.assertNotRegex(self.texto[PAGINAS[i]], limite)
        # os dois treinos do Grupo III dizem-nos do seu item, com o grupo no cabeçalho
        for i, fase in ((3, '2.ª fase'), (7, '1.ª fase')):
            self.assertRegex(self.texto[PAGINAS[i]], limite)
            self.assertIn('Prova 639, 2026, %s, Grupo III (resposta extensa, 44 pontos)' % fase, self.texto[PAGINAS[i]])
        # na entrada, só os cartões desses dois treinos
        for cartao in re.findall(r'<article class="cartao-p">(.*?)</article>', self.html[PAGINAS[0]], re.S):
            pasta = re.search(r'href="([^"/]+)/"', cartao).group(1)
            with self.subTest(cartao=pasta):
                if pasta in ('escrita', 'apreciacao-critica'):
                    self.assertRegex(cartao, r'200 a 350 palavras')
                    self.assertIn('Grupo III', cartao)
                else:
                    self.assertNotRegex(cartao, limite)
        fora = re.sub(r'<article class="cartao-p">.*?</article>', '', self.html[PAGINAS[0]], flags=re.S)
        self.assertNotRegex(fora, limite)
        # no treino da exposição (item 7 do Grupo I, sem limite), cada frase com estes números diz que são do Grupo III ou da sessão 23;
        # as duas únicas exceções são distratores, e a pista e a explicação da pergunta desfazem-nos
        cadeias8 = list(cadeias(T8.TREINO)) + [T8.CAB]
        frases = [f for s in cadeias8 for f in re.split(r'(?<=[.!?])\s+|</p>|</dd>', s) if re.search(limite, f)]
        self.assertEqual(6, len(frases))
        distratores = ['De 200 a 350 palavras; por cada palavra a mais ou a menos, desconta-se um ponto.',
                       'A Exposição B: não chega às duzentas palavras que uma resposta escrita tem de ter.']
        for f in frases:
            with self.subTest(frase=f[:60]):
                if f in distratores:
                    continue
                self.assertRegex(f, r'Grupo III|sessão 23')
        esc = {b['id']: b for ps in T8.TREINO['passos'] for b in ps['blocos'] if b['t'] == 'escolha'}
        self.assertEqual((distratores[0], 1), (esc['p8-regras']['o'][0]['t'], esc['p8-regras']['c']))
        self.assertIn('são do item de resposta extensa, o Grupo III (enunciado, p. 8; critérios, p. 3)', esc['p8-regras']['f'])
        self.assertEqual((distratores[1], 1), (esc['p8-distinguir']['o'][3]['t'], esc['p8-distinguir']['c']))
        self.assertIn('O enunciado só diz «breve».', esc['p8-regras']['f'])
        self.assertNotRegex(' '.join(self.f2['grupos'][0]['partes'][2]['itens'][0]['enunciado']), r'\d')
        self.assertIn('é uma meta de treino da sessão (orientação nossa)', T8.CAB)
        self.assertIn('A caixa conta as palavras só para saberes o tamanho do que escreveste.', self.texto[PAGINAS[8]])
        # e a página não diz quantas palavras deve ter a exposição: o número do exemplo vem dito como não sendo meta
        self.assertIn('O número de palavras também não é uma meta: o item só diz «breve».', self.texto[PAGINAS[8]])

    def test_achados_da_revisao_de_12_11(self):
        # 12/11/2026: teste novo, com o que a revisão independente dos treinos 4 e 5 apanhou
        # a opção adequada não se reconhece pelo tamanho: nunca passa de 1,4 vezes a mais longa das outras
        # 13/11/2026: a regra passa a cobrir os oito treinos
        for T in (T1, T2, T3, T4, T5, T6, T7, T8):
            for ps in T.TREINO['passos']:
                for b in ps['blocos']:
                    if b['t'] != 'escolha':
                        continue
                    tam = [len(o['t']) for o in b['o']]
                    outras = max(t for i, t in enumerate(tam) if i != b['c'])
                    with self.subTest(pergunta=b['id']):
                        self.assertLessEqual(tam[b['c']] / outras, 1.4, tam)
        # no passo 3 do conto, as quatro afirmações têm a mesma forma: nenhuma traz a justificação depois de dois pontos
        sep = [b for ps in T5.TREINO['passos'] for b in ps['blocos'] if b.get('id') == 'p5-separar'][0]
        self.assertEqual(4, len(sep['o']))
        for o in sep['o']:
            self.assertNotIn(':', o['t'])
            self.assertRegex(o['t'], r'^George [^;()«»]+\.$')
        # nenhuma pista da primeira busca do conto entrega as palavras que a segunda busca pede
        rec, pen = [b for ps in T5.TREINO['passos'] for b in ps['blocos'] if b.get('id') in ('p5-recusa', 'p5-pensados')]
        self.assertEqual(('p5-recusa', 'p5-pensados'), (rec['id'], pen['id']))
        pistas1 = ' '.join(x['x'] for x in rec['pistas']) + rec['falta'] + rec['pista2']
        self.assertNotRegex(pistas1, r'pensad|pergunta seguinte|[Gg]uarda')
        # 13/11/2026: também nos treinos 6, 7 e 8
        for T in (T1, T2, T3, T4, T5, T6, T7, T8):
            self.assertNotIn('pergunta seguinte', json.dumps(T.TREINO, ensure_ascii=False))
        # a página da poesia não afirma por conta própria que a citação é o último verso de «Uma pequenina luz»
        self.assertNotRegex(T4.NOSSO, r'(?i)\bfech(o|a)\b')
        self.assertIn('Vem no fim do poema, segundo a <a href="../../../m8/licao-m8-f03/">', T4.APOIO)
        # o número do verso ou da linha é hábito nosso, e as duas páginas dizem-no
        for T in (T4, T5):
            self.assertNotRegex(json.dumps(T.TREINO, ensure_ascii=False), r'na prova, ou a partir do manual|copiada do manual, com o número|copia-o do manual')
        self.assertIn('Se copiei do manual, juntei o número do verso (hábito nosso, não é exigência dos critérios).', self.texto['exame/treinos/poesia-contemporanea/index.html'] + json.dumps(T4.TREINO, ensure_ascii=False))
        self.assertIn('Juntá-lo é um hábito nosso', json.dumps(T4.TREINO, ensure_ascii=False))
        self.assertIn('Juntá-lo é um hábito nosso', json.dumps(T5.TREINO, ensure_ascii=False))
        # o descritor «um dos sujeitos poéticos» vem depois da ponte que diz que a Resposta A cumpria a estrutura do item oficial
        t4 = json.dumps(T4.TREINO, ensure_ascii=False)
        self.assertLess(t4.index('lá, uma resposta como a A cumpria a estrutura pedida'), t4.index(T4.D_UM))
        # o conto: os itens 1 e 2 da 1.ª fase são os de excerto narrativo dado na prova (o item 7 é resposta restrita sem excerto)
        h5 = self.html['exame/treinos/conto/index.html']
        self.assertEqual(2, h5.count('os itens de resposta restrita sobre um excerto narrativo dado na prova são os itens 1 e 2 da 1.ª fase'))
        self.assertNotIn('itens de resposta restrita sobre texto narrativo', h5)
        # e uma inferência não é uma palavra nova para o que o recorte já escreve
        t5 = json.dumps(T5.TREINO, ensure_ascii=False)
        self.assertNotRegex(t5, r'com uma palavra que o recorte não usa|que não copiei do recorte')
        self.assertIn('Trocar uma palavra por um sinónimo não chegava.', t5)

    def test_ligacoes_oficiais_em_eduqa(self):
        self.assertEqual(EDUQA, set(B.URL.values()))
        for p in PAGINAS[1:]:
            fora = set(re.findall(r'href="(https?://[^"]+)"', self.html[p]))
            with self.subTest(pagina=p):
                self.assertTrue(fora)
                # 13/11/2026: o treino 7 tem mais duas ligações externas, e só essas: a página 13 do enunciado da 1.ª fase (a imagem da prova)
                # e a página da gravura no sítio do museu (crédito da imagem); nas outras páginas a exigência fica como estava
                # e passam a contar também as ligações que vêm nos dados dos passos (com as aspas escapadas), que a expressão de cima não apanha
                todas = set(re.findall(r'href=\\?"(https?://[^"\\]+)', self.html[p]))
                self.assertLessEqual(fora, todas)
                if p.endswith('apreciacao-critica/index.html'):
                    self.assertEqual({B.URL['e1'], B.URL['c1'], EDUQA_P13, MET}, fora)
                    self.assertEqual(fora, todas)
                else:
                    self.assertLessEqual(fora, EDUQA)
                    self.assertLessEqual(todas, EDUQA)
                for a in re.findall(r'<a href=\\?"https?://[^>]+>', self.html[p]):
                    self.assertRegex(a, r'target=\\?"_blank\\?" rel=\\?"noopener\\?"')
                for a in re.findall(r'<a href="https?://[^"]+"[^>]*>', self.html[p]):
                    self.assertIn('target="_blank" rel="noopener"', a)
        self.assertLessEqual({B.URL['e1'], B.URL['c1']}, set(re.findall(r'href="([^"]+)"', self.html[PAGINAS[1]])))
        self.assertEqual(EDUQA, set(re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[2]])))
        self.assertLessEqual({B.URL['e2'], B.URL['c2']}, set(re.findall(r'href="([^"]+)"', self.html[PAGINAS[3]])))
        # 12/11/2026: o treino da sessão 17 liga aos documentos das duas fases
        self.assertEqual(EDUQA, set(re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[4]])))
        # 12/11/2026: o treino da sessão 18 também (item oficial da 2.ª fase; itens sobre texto narrativo da 1.ª)
        self.assertEqual(EDUQA, set(re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[5]])))
        # 13/11/2026: o treino 6 liga aos documentos das duas fases; o treino 8 também (item da 2.ª fase e o mesmo item na 1.ª)
        self.assertEqual(EDUQA, set(re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[6]])))
        self.assertEqual({B.URL['e2'], B.URL['c2']}, set(re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[8]])))
        self.assertEqual(EDUQA, set(re.findall(r'href=\\?"(https?://[^"\\]+)', self.html[PAGINAS[8]])))
        # a imagem da prova não está no repositório nem na página: só a ligação à página 13 do enunciado, em eduqa.pt
        self.assertGreaterEqual(self.html[PAGINAS[7]].count('href="%s"' % EDUQA_P13), 3)
        self.assertEqual(EDUQA_P13, B.URL['e1'] + '#page=13')
        self.assertEqual([], re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[0]]))

    def test_regras_de_lingua_no_texto_nosso(self):
        # o gerador recusa escrever páginas com estas formas no texto nosso (fora das citações oficiais e literárias)
        for mau in ('o professor', 'vamos jogar', 'um jogo', 'a ficha', 'a folha', 'isto — aquilo', 'um · dois', 'Qual resposta fica', 'faz sozinho',
                    'no Dicionário Terminológico'):
            with self.subTest(forma=mau):
                with self.assertRaises(SystemExit):
                    B.lint('teste', mau)
        self.assertEqual([], B.lint('teste', 'Que resposta fica aquém? Qual das duas? No <i>Dicionário Terminológico</i>, com o docente.'))
        # 12/11/2026: mais o texto nosso do treino da sessão 17
        # 12/11/2026: e o do treino da sessão 18
        nossos = {'indice': T0.CORPO, 'interpretacao': T1.NOSSO, 'gramatica': T2.NOSSO, 'escrita': T3.NOSSO, 'poesia-contemporanea': T4.NOSSO, 'conto': T5.NOSSO,
                  # 13/11/2026: e o dos treinos das sessões 22, 25 e 23
                  'coesao': T6.NOSSO, 'apreciacao-critica': T7.NOSSO, 'exposicao': T8.NOSSO}
        self.assertEqual(len(PAGINAS), len(nossos))
        for nome, nosso in nossos.items():
            with self.subTest(treino=nome):
                self.assertGreater(len(nosso), 3000)
                self.assertEqual([], B.lint(nome, re.sub(re.escape(B.md(T1.IT['enunciado'][0])), '', nosso)))
                self.assertNotRegex(nosso, r'(?i)\bvocês?\b|\bconvosco\b|\bo vosso\b')
        # nas páginas inteiras: nada da prévia, o docente sem nome, e as palavras proibidas só em citação oficial
        for p in PAGINAS:
            with self.subTest(pagina=p):
                self.assertNotRegex(self.html[p], r'(?i)pr[ée]via|pilot|antes-e-depois|noindex')
                self.assertNotRegex(self.texto[p], r'(?i)professor|\bjog(o|ar|os)\b|\bfichas?\b')
                self.assertNotIn('·', self.texto[p])
        self.assertNotIn('—', self.texto[PAGINAS[0]])

    def test_convencoes_das_paginas_do_exame(self):
        versao = B.V_TREINO
        for i, p in enumerate(PAGINAS):
            h = self.html[p]
            raiz = '../../' if i == 0 else '../../../'
            exame = '../' if i == 0 else '../../'
            with self.subTest(pagina=p):
                self.assertTrue(h.startswith('<!doctype html>\n<html lang="pt-PT" data-appearance-site="pt"><head><meta charset="utf-8">'))
                self.assertEqual(1, len(re.findall(r'<title>[^<]+ \| Português</title>', h)))
                self.assertRegex(h, r'<meta name="description" content="[^"]{60,200}">')
                self.assertEqual(1, len(re.findall(r'<h1[ >]', h)))
                # nada embutido: o estilo e o motor vêm de assets/exame/, com versão
                self.assertNotRegex(h, r'<style|\sstyle=|\son[a-z]+=')
                self.assertEqual([], [s for s in re.findall(r'<script\b[^>]*>', h) if 'src=' not in s and 'type="application/json"' not in s])
                self.assertIn('<link rel="stylesheet" href="%sassets/exame/treino.css?v=%s">' % (raiz, versao), h)
                self.assertIn('<script defer src="%sassets/exame/treino.js?v=%s"></script>' % (raiz, versao), h)
                self.assertLess(h.index('assets/appearance.css'), h.index('assets/exame/treino.css'))
                for ref in re.findall(r'(?:href|src)="([^"#]+)"', h):
                    if ref.startswith('http'):
                        continue
                    alvo = (ROOT / p).parent / ref.split('?')[0]
                    self.assertTrue(alvo.is_file() or (alvo / 'index.html').is_file(), ref)
                    if re.search(r'\.(css|js)(\?|$)', ref):
                        self.assertRegex(ref, r'\?v=[\w.-]+$')
                    self.assertFalse(ref.startswith('/'), ref)
                    self.assertNotIn('index.html', ref)
                for fonte in ('fraunces-latin-normal.woff2', 'ibm-plex-sans-latin-normal.woff2'):
                    self.assertIn('<link rel="preload" href="%sassets/exame/fontes/%s" as="font" type="font/woff2" crossorigin>' % (raiz, fonte), h)
                # cabeçalho e navegação das páginas do exame, de volta à entrada
                self.assertIn('<a class="skip" href="#conteudo">', h)
                self.assertIn('<nav class="migalhas" aria-label="Onde estás"><ol><li><a href="%s">Português</a></li><li><a href="%s">Preparação de exame</a></li>' % (raiz, exame), h)
                self.assertIn('<a class="wordmark" href="%s">Português<span>.</span><small>Preparação de exame</small></a>' % exame, h)
                self.assertIn('<a href="%s">Sessões</a><a href="%slaboratorio/">Laboratório de respostas</a><a href="%sprovas/">Provas em cartões</a>' % (exame, exame, exame), h)
                # créditos e licenças dos tipos de letra
                self.assertIn('%sassets/exame/fontes/Fraunces-OFL.txt' % raiz, h)
                self.assertIn('%sassets/exame/fontes/IBM-Plex-Sans-OFL.txt' % raiz, h)
        # cada treino liga à sua sessão e ao aquecimento dessa sessão, que continuam onde estavam
        sessoes = {s['id']: s for s in json.loads((ROOT / 'assets/exame/sessoes.json').read_text('utf-8'))['sessions']}
        # 12/11/2026: mais a sessão 17; o zip não pode deixar nenhum treino de fora
        # 12/11/2026: e a sessão 18
        # 13/11/2026: e as sessões 22, 25 e 23, por esta ordem; oito treinos
        self.assertEqual(8, len(PAGINAS[1:]))
        for p, sid in zip(PAGINAS[1:], ('s14', 's21', 's24', 's17', 's18', 's22', 's25', 's23')):
            h = self.html[p]
            self.assertIn('<a href="../../#%s">sessão %s («%s»)</a>' % (sid, sid[1:], sessoes[sid]['title']), h)
            self.assertIn('<a href="../../aquecimentos/%s/">aquecimento</a>' % sid, h)
            self.assertIn('<a href="../#%s">sessão %s («%s»)</a>' % (sid, sid[1:], sessoes[sid]['title']), self.html[PAGINAS[0]])
            self.assertNotRegex(self.texto[p], r'(?i)\brefaz|\brefeit')
        self.assertNotRegex(self.texto[PAGINAS[0]], r'(?i)\brefaz|\brefeit|substitu')

    def test_entrada_dos_treinos_ligada_a_partir_do_exame(self):
        # exame/index.html está registado em camadas literais e não se muda aqui: os treinos ligam-se a partir das provas em
        # cartões e do laboratório, que têm a navegação da preparação no cabeçalho
        # 12/11/2026: a ligação na página principal do Exame entrou depois, pela camada literal exame_ligacao_treinos_20261112
        # (conferida em tests/test_exame_ligacao_treinos.py); as asserções daqui ficam como estavam
        for p in ('exame/provas/index.html', 'exame/laboratorio/index.html'):
            with self.subTest(pagina=p):
                h = (ROOT / p).read_text('utf-8')
                cab = re.search(r'<header class="site-head[^"]*">.*?</header>', h, re.S).group(0)
                self.assertEqual(1, cab.count('<a href="../treinos/">Treinos</a>'))
        self.assertTrue((ROOT / 'exame/treinos/index.html').is_file())

    def test_estilo_e_motor(self):
        css = (ROOT / 'assets/exame/treino.css').read_text('utf-8')
        js = (ROOT / 'assets/exame/treino.js').read_text('utf-8')
        # os tipos de letra vêm de assets/exame/fontes/ e nada vem de fora
        self.assertEqual(['fontes/fraunces-latin-normal.woff2', 'fontes/fraunces-latin-italic.woff2', 'fontes/ibm-plex-sans-latin-normal.woff2'],
                         re.findall(r'url\("([^"]+)"\)', css))
        for f in re.findall(r'url\("([^"]+)"\)', css):
            self.assertTrue((ROOT / 'assets/exame' / f).is_file(), f)
        self.assertNotRegex(css + js, r'https?://|data:font|base64')
        # tema claro e escuro: pela escolha do sítio (data-theme) e, sem ela, pelo sistema
        self.assertIn(':root[data-theme="dark"] body.treino{', css)
        self.assertIn('@media (prefers-color-scheme:dark){:root:not([data-theme]) body.treino{', css)
        self.assertNotRegex(css + js, r'(?i)pilot|pr[ée]via')
        self.assertIn("var PREFIXO='exame-treino:'", js)
        self.assertNotRegex(js, r'\beval\(|document\.write|fetch\(|XMLHttpRequest|sendBeacon')


if __name__ == '__main__':
    unittest.main()
