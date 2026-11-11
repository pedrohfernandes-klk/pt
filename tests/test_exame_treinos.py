"""11/11/2026: os três treinos da preparação de exame (exame/treinos/): páginas iguais ao gerador, textos oficiais iguais às
transcrições, ligações aos documentos em eduqa.pt, regras de língua no texto nosso e convenções das páginas do exame."""
import json
from pathlib import Path
import re
import sys
import unittest
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import exame_treinos as G
from exame_treinos_dados import base as B, interpretacao as T1, gramatica as T2, escrita as T3, indice as T0

PAGINAS = ['exame/treinos/index.html', 'exame/treinos/interpretacao/index.html', 'exame/treinos/gramatica/index.html', 'exame/treinos/escrita/index.html']
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
        # só existem estas quatro páginas em exame/treinos/
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

    def test_ligacoes_oficiais_em_eduqa(self):
        self.assertEqual(EDUQA, set(B.URL.values()))
        for p in PAGINAS[1:]:
            fora = set(re.findall(r'href="(https?://[^"]+)"', self.html[p]))
            with self.subTest(pagina=p):
                self.assertTrue(fora)
                self.assertLessEqual(fora, EDUQA)
                for a in re.findall(r'<a href="https?://[^"]+"[^>]*>', self.html[p]):
                    self.assertIn('target="_blank" rel="noopener"', a)
        self.assertLessEqual({B.URL['e1'], B.URL['c1']}, set(re.findall(r'href="([^"]+)"', self.html[PAGINAS[1]])))
        self.assertEqual(EDUQA, set(re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[2]])))
        self.assertLessEqual({B.URL['e2'], B.URL['c2']}, set(re.findall(r'href="([^"]+)"', self.html[PAGINAS[3]])))
        self.assertEqual([], re.findall(r'href="(https?://[^"]+)"', self.html[PAGINAS[0]]))

    def test_regras_de_lingua_no_texto_nosso(self):
        # o gerador recusa escrever páginas com estas formas no texto nosso (fora das citações oficiais e literárias)
        for mau in ('o professor', 'vamos jogar', 'um jogo', 'a ficha', 'a folha', 'isto — aquilo', 'um · dois', 'Qual resposta fica', 'faz sozinho',
                    'no Dicionário Terminológico'):
            with self.subTest(forma=mau):
                with self.assertRaises(SystemExit):
                    B.lint('teste', mau)
        self.assertEqual([], B.lint('teste', 'Que resposta fica aquém? Qual das duas? No <i>Dicionário Terminológico</i>, com o docente.'))
        nossos = {'indice': T0.CORPO, 'interpretacao': T1.NOSSO, 'gramatica': T2.NOSSO, 'escrita': T3.NOSSO}
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
        for p, sid in zip(PAGINAS[1:], ('s14', 's21', 's24')):
            h = self.html[p]
            self.assertIn('<a href="../../#%s">sessão %s («%s»)</a>' % (sid, sid[1:], sessoes[sid]['title']), h)
            self.assertIn('<a href="../../aquecimentos/%s/">aquecimento</a>' % sid, h)
            self.assertIn('<a href="../#%s">sessão %s («%s»)</a>' % (sid, sid[1:], sessoes[sid]['title']), self.html[PAGINAS[0]])
            self.assertNotRegex(self.texto[p], r'(?i)\brefaz|\brefeit')
        self.assertNotRegex(self.texto[PAGINAS[0]], r'(?i)\brefaz|\brefeit|substitu')

    def test_entrada_dos_treinos_ligada_a_partir_do_exame(self):
        # exame/index.html está registado em camadas literais e não se muda aqui: os treinos ligam-se a partir das provas em
        # cartões e do laboratório, que têm a navegação da preparação no cabeçalho
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
