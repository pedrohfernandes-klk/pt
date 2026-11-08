"""07/11/2026: decisões 153, 176 e 177 (pedido pt-1 do plano plano-creditos-i-20261105.md, famílias P1 a P4).

O docente, na 153: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir»; na 177: «"parar desenho" soa
muito mal. "parar animação", ou assim, é melhor». Confere, sem navegador, a camada creditos_i_pt1_20261107
(scripts/creditos_i_pt1_20261107.json, gerada por scripts/creditos_i_pt1_20261107.py; manifesto
tests/fixtures/creditos-i-pt1-edits-20261107.json):

* a camada é fechada e reversível: 25 trocas literais em 11 páginas, cada uma com a contagem exata; desfeita, dá a página de
  baixo letra a letra, e refeita, a de agora; o gerador dá o mesmo JSON;
* fica registada como a camada mais recente (por cima da decisão 152 no M1) em scripts/verificar_camadas.py, nas cadeias de
  desfazer de tests/auditoria_20261028.py e de scripts/desligar_sala.py, nas cadeias dos workflows e dos testes e nos testes de
  navegador que montam o «antes» dos índices;
* nada do conteúdo se perde: as ligações e as imagens são as mesmas (só entram a folha e o script da peça comum, a ligação da
  licença CC BY-SA 2.0 do M8 e a versão nova do motor dos fundos), e as palavras também (só muda o texto do botão, decisão 177,
  e entram o «i» de cada summary e o «© OpenStreetMap» curto do mapa, decisão 162);
* cada crédito passa inteiro para dentro do «i», com a estrutura da peça comum, e o botão do fundo fica fora dele.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import glob
import importlib.util
import json
import re
import subprocess
import sys
import unittest

from auditoria_20261028 import undo_creditos_i_pt1_0711, undo_cuidado_m1_0611

ROOT = Path(__file__).resolve().parents[1]
CAMADA = ROOT / 'scripts/creditos_i_pt1_20261107.json'
MANIFESTO = ROOT / 'tests/fixtures/creditos-i-pt1-edits-20261107.json'
INDICES = [f'm{n}/index.html' for n in range(1, 10)]
PAGINAS = sorted(['index.html', 'atlas/index.html'] + INDICES)
PECA = ('info-i.css?v=20261105', 'info-i.js?v=20261105')
# Os créditos de antes, letra a letra (o texto, sem etiquetas), e o que o «i» tem agora. Só mudam os «·» (passam a pontos finais)
# e a maiúscula que fica a abrir a frase, no portal do Lente.
CREDITOS_INDICES = {
    'm1/index.html': 'Cancioneiro da Biblioteca Nacional, página (cópia do século XVI). Domínio público.',
    'm2/index.html': 'Copilaçam de todalas obras de Gil Vicente (Lisboa, 1562), frontispício. Domínio público.',
    'm3/index.html': 'Fonte: Academia Brasileira de Letras, via Wikimedia Commons ↗. Domínio público.',
    'm4/index.html': 'Sermão de Santo António aos Peixes, em Sermoens (Lisboa, 1682). Domínio público.',
    'm5/index.html': 'Fonte: Wikimedia Commons ↗. Domínio público.',
    'm6/index.html': '«O Sentimento dum Ocidental» em O Livro de Cesário Verde (1887), primeira página. Domínio público.',
    'm7/index.html': 'Revista Orpheu, n.º 2 (1915), capa. Domínio público.',
    'm8/index.html': 'Rua do Alecrim, Lisboa (fotografia de Roger Wollstadt, 1968). CC BY-SA 2.0.',
    'm9/index.html': 'A Passarola de Bartolomeu de Gusmão, desenho do século XVIII (fac-símile, BNP). Domínio público.',
}
TITULOS = {'m1/index.html': ['Cancioneiro da Biblioteca Nacional'], 'm2/index.html': ['Copilaçam de todalas obras de Gil Vicente'],
           'm4/index.html': ['Sermão de Santo António aos Peixes', 'Sermoens'], 'm6/index.html': ['O Livro de Cesário Verde'],
           'm7/index.html': ['Orpheu']}
P1_CREDITO = ('Grafismo gerado com recurso a IA, EPI, 2026, a partir do padrão de ondas da calçada portuguesa (o «mar largo» do '
              'Rossio, Lisboa).')
P3_ANTES = 'Estudo do movimento · domínio público · Library of Congress'
P3_AGORA = 'Estudo do movimento. Domínio público. Library of Congress.'
P4_CREDITO = ('Mapa: Natural Earth (domínio público), projeção Equal Earth; pontos de passagem: © contribuidores do '
              'OpenStreetMap')
VAZIOS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


class No:
    def __init__(self, tag, attrs, pai):
        self.tag, self.attrs, self.filhos, self.pai = tag, attrs, [], pai

    def classes(self):
        return set((self.attrs.get('class') or '').split())

    def elementos(self):
        return [f for f in self.filhos if isinstance(f, No)]

    def descendentes(self):
        for f in self.elementos():
            yield f
            yield from f.descendentes()

    def antepassados(self):
        n = self.pai
        while n is not None:
            yield n
            n = n.pai

    def texto(self, parar=lambda n: False):
        return ''.join(f if isinstance(f, str) else ('' if f.tag in ('script', 'style') or parar(f) else f.texto(parar))
                       for f in self.filhos)

    def html_interior(self):
        """O HTML de dentro (etiquetas e texto), para conferir ligações e itálicos."""
        partes = []
        for f in self.filhos:
            if isinstance(f, str):
                partes.append(f)
            else:
                attrs = ''.join(f' {k}="{v}"' for k, v in f.attrs.items())
                partes.append(f'<{f.tag}{attrs}>' + ('' if f.tag in VAZIOS else f.html_interior() + f'</{f.tag}>'))
        return ''.join(partes)


class Arvore(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.raiz = No('#raiz', {}, None)
        self.atual = self.raiz
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        no = No(tag, {k: (v if v is not None else '') for k, v in attrs}, self.atual)
        self.atual.filhos.append(no)
        if tag not in VAZIOS:
            self.atual = no

    def handle_startendtag(self, tag, attrs):
        self.atual.filhos.append(No(tag, {k: (v if v is not None else '') for k, v in attrs}, self.atual))

    def handle_endtag(self, tag):
        n = self.atual
        while n is not None and n.tag != tag:
            n = n.pai
        if n is not None and n.pai is not None:
            self.atual = n.pai

    def handle_data(self, data):
        self.atual.filhos.append(data)


def norm(s):
    return re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()


def texto_espacado(no):
    """O texto de um nó com um espaço em cada fronteira de elemento (o «i» do summary não se cola à palavra seguinte)."""
    return ''.join(f if isinstance(f, str) else ('' if f.tag in ('script', 'style') else ' ' + texto_espacado(f) + ' ')
                   for f in no.filhos)


def palavras(raiz):
    """As palavras do texto da página (sem scripts nem estilos), em minúsculas e sem pontuação, para contar o que muda."""
    return Counter(re.findall(r'[\w©↗]+', norm(texto_espacado(raiz)).lower()))


def inventario(html):
    raiz = Arvore(html).raiz
    nos = list(raiz.descendentes())
    return {'raiz': raiz, 'hrefs': Counter(n.attrs['href'] for n in nos if 'href' in n.attrs),
            'srcs': Counter(n.attrs['src'] for n in nos if 'src' in n.attrs),
            'imgs': [(n.attrs.get('src'), n.attrs.get('alt')) for n in nos if n.tag == 'img'],
            'ii': [n for n in nos if n.tag == 'details' and 'info-i' in n.classes()]}


class CreditosIPt1(unittest.TestCase):
    def test_camada_mais_recente_fechada_e_reversivel(self):
        # A camada mais recente confere-se sem nada por cima, com as contagens exatas do manifesto.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', str(CAMADA.relative_to(ROOT)), '--manifesto',
                            str(MANIFESTO.relative_to(ROOT)), '--verificar'], cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('25 trocas em 11 ficheiros: 25 aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        manifesto = json.loads(MANIFESTO.read_text('utf-8'))
        self.assertEqual(sorted(manifesto['files']), PAGINAS)
        trocas = json.loads(CAMADA.read_text('utf-8'))
        self.assertEqual(Counter(t['ficheiro'] for t in trocas),
                         Counter({'index.html': 3, 'atlas/index.html': 4, **{rel: 2 for rel in INDICES}}))
        self.assertTrue(all(t['ocorrencias'] == 1 for t in trocas))
        self.assertTrue(all(t['achado'].startswith('07/11/2026: decisões 153, 176 e 177') for t in trocas))
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                atual = ler(rel)
                base = undo_creditos_i_pt1_0711(rel, atual)
                refeito = base
                for e in manifesto['files'][rel]['edits']:
                    self.assertEqual(refeito.count(e['old']), 1, (rel, e['location']))
                    self.assertEqual(refeito.count(e['new']), 0, (rel, e['location']))
                    refeito = refeito.replace(e['old'], e['new'])
                self.assertEqual(refeito, atual, rel)
                # A camada de baixo (a decisão 152 no M1) continua a desfazer-se por cima desta base.
                undo_cuidado_m1_0611(rel, atual)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('creditos_i_pt1', ROOT / 'scripts/creditos_i_pt1_20261107.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        self.assertEqual(modulo.construir(), json.loads(CAMADA.read_text('utf-8')))

    def test_registada_como_a_camada_mais_recente(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        self.assertEqual(verificar_camadas.LAYERS[0], ('creditos_i_pt1_20261107', 'creditos-i-pt1-edits-20261107'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('cuidado_m1_20261106', 'cuidado-m1-edits-20261106'))
        auditoria = ler('tests/auditoria_20261028.py')
        corpo = auditoria[auditoria.index('def undo_cuidado_m1_0611'):]
        self.assertLess(corpo.index('undo_creditos_i_pt1_0711(path, text)'), corpo.index('_CUIDADO_M1_0611.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('creditos-i-pt1-edits-20261107.json'), sala.index('cuidado-m1-edits-20261106.json'))
        # Em cada cadeia dos workflows, esta camada desfaz-se primeiro, logo a seguir a --verificar.
        cadeias = 0
        for wf in sorted(glob.glob(str(ROOT / '.github/workflows/*.yml'))):
            for linha in Path(wf).read_text('utf-8').splitlines():
                if linha.lstrip().startswith('#') or '--desfazer-antes tests/fixtures/cuidado-m1-edits-20261106.json' not in linha:
                    continue
                cadeias += 1
                self.assertIn('--verificar --desfazer-antes tests/fixtures/creditos-i-pt1-edits-20261107.json --desfazer-antes '
                              'tests/fixtures/cuidado-m1-edits-20261106.json', linha, wf)
        self.assertEqual(cadeias, 13)
        # A decisão 152 no M1, que se conferia sem nada por cima, desfaz primeiro esta camada.
        self.assertIn('scripts/cuidado_m1_20261106.json --manifesto tests/fixtures/cuidado-m1-edits-20261106.json --verificar '
                      '--desfazer-antes tests/fixtures/creditos-i-pt1-edits-20261107.json', ler('.github/workflows/pt-tarefas-qa.yml'))
        # Nas cadeias dos testes, esta camada vem logo antes da decisão 152 no M1, sem outra pelo meio.
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            # Como este, o teste da decisão 152 no M1 confere as cadeias com frases (a cadeia inteira numa cadeia de texto), não as corre.
            if p.name in ('test_creditos_i_pt1.py', 'test_cuidado_m1.py'):
                continue
            texto = '\n'.join(l for l in p.read_text('utf-8').split('\n') if not l.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            plano = plano.replace("',ROOT/'", ' ')
            with self.subTest(teste=p.name):
                self.assertEqual(plano.count('--desfazer-antes tests/fixtures/cuidado-m1-edits-20261106.json'),
                                 plano.count('--desfazer-antes tests/fixtures/creditos-i-pt1-edits-20261107.json --desfazer-antes '
                                             'tests/fixtures/cuidado-m1-edits-20261106.json'))
        self.assertIn("(ROOT/'tests/fixtures/creditos-i-pt1-edits-20261107.json',ROOT/'tests/fixtures/cuidado-m1-edits-20261106.json',",
                      ler('tests/test_task_routes_closure.py'))
        # Os testes de navegador que montam o «antes» dos índices desfazem-na primeiro.
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs'):
            texto = ler(rel)
            with self.subTest(teste=rel):
                self.assertLess(texto.index('((creditosPt1['), texto.index('((cuidado['))
        # O gerador do desenho comum dos índices também (calcula a sua base desfazendo as camadas de cima).
        gerador = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(gerador.index('CREDITOS_PT1.read_text'), gerador.index('CUIDADO.read_text'))
        # O workflow dos testes de navegador dos índices corre o teste de navegador desta camada e confere-a sem nada por cima.
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn('node tests/browser_creditos_i_pt1.cjs', cartaz)
        self.assertIn('python scripts/aplicar_trocas.py scripts/creditos_i_pt1_20261107.json --manifesto '
                      'tests/fixtures/creditos-i-pt1-edits-20261107.json --verificar', cartaz)
        for caminho in ('scripts/creditos_i_pt1_20261107.*', 'tests/fixtures/creditos-i-pt1-edits-20261107.json',
                        'tests/*creditos_i_pt1*', 'atlas/index.html', 'assets/fundos.js', 'assets/info-i.*'):
            self.assertIn(f"'{caminho}'", cartaz)

    def test_nada_do_conteudo_se_perde(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                atual = ler(rel)
                antes, depois = inventario(undo_creditos_i_pt1_0711(rel, atual)), inventario(atual)
                # As imagens são as mesmas, pela mesma ordem, com o mesmo alt.
                self.assertEqual(antes['imgs'], depois['imgs'])
                # As ligações também; só entram a peça comum, a licença do M8 e a versão nova do motor dos fundos.
                prefixo = '' if rel == 'index.html' else '../'
                entram = Counter({prefixo + 'assets/' + PECA[0]: 1})
                if rel == 'm8/index.html':
                    entram['https://creativecommons.org/licenses/by-sa/2.0/deed.pt'] = 1
                self.assertEqual(depois['hrefs'] - antes['hrefs'], entram)
                self.assertEqual(antes['hrefs'] - depois['hrefs'], Counter())
                entram_src = Counter({prefixo + 'assets/' + PECA[1]: 1})
                sai_src = Counter()
                if rel == 'index.html':
                    entram_src['assets/fundos.js?v=20261107'] = 1
                    sai_src['assets/fundos.js?v=20261102-1'] = 1
                self.assertEqual(depois['srcs'] - antes['srcs'], entram_src)
                self.assertEqual(antes['srcs'] - depois['srcs'], sai_src)
                # As palavras: nenhuma se perde, salvo as do botão (decisão 177); entram o «i» de cada summary e, no mapa, o
                # «© OpenStreetMap» curto (decisão 162).
                perdidas = palavras(antes['raiz']) - palavras(depois['raiz'])
                ganhas = palavras(depois['raiz']) - palavras(antes['raiz'])
                if rel == 'index.html':
                    self.assertEqual(perdidas, Counter({'o': 1, 'desenho': 1}))
                    self.assertEqual(ganhas, Counter({'i': 2, 'a': 1, 'animação': 1}))
                elif rel == 'atlas/index.html':
                    self.assertEqual(perdidas, Counter())
                    self.assertEqual(ganhas, Counter({'i': 1, '©': 1, 'openstreetmap': 1}))
                else:
                    self.assertEqual(perdidas, Counter())
                    self.assertEqual(ganhas, Counter({'i': 1}))
                # Um «i» por crédito que passou para trás dele.
                self.assertEqual(len(antes['ii']), 0)
                self.assertEqual(len(depois['ii']), 2 if rel == 'index.html' else 1)

    def test_cada_credito_inteiro_no_i(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                s = ler(rel)
                inv = inventario(s)
                for d in inv['ii']:
                    s_ = d.elementos()[0]
                    self.assertEqual((d.attrs.get('name'), s_.tag), ('info-i', 'summary'))
                    self.assertEqual(s_.html_interior(), '<span aria-hidden="true">i</span>')
                    self.assertTrue(all(a.tag not in ('a', 'button', 'label', 'figcaption') for a in d.antepassados()))
                    self.assertNotIn('·', d.texto(), 'nunca «·» dentro de frases')
                    if 'info-i--linha' not in d.classes():
                        self.assertIn('com-i', d.pai.classes(), 'a variante «canto» vive na moldura da imagem')
                for nome in PECA:
                    self.assertEqual(s.count(nome), 1, nome)
        # P1: o crédito do fundo no «i» («linha»); o botão fora dele, na .fundo-acoes, com o texto novo e escondido sem JavaScript.
        inv = inventario(ler('index.html'))
        calcada, portal = inv['ii']
        self.assertEqual(calcada.classes(), {'info-i', 'info-i--linha'})
        self.assertEqual(calcada.elementos()[0].attrs['aria-label'], 'Créditos do desenho')
        self.assertEqual(norm(calcada.elementos()[1].texto()), P1_CREDITO)
        acoes = calcada.pai
        self.assertEqual(acoes.classes(), {'fundo-acoes', 'cf-credito'})
        botao = acoes.elementos()[0]
        self.assertEqual((botao.tag, botao.attrs.get('data-fundo-botao'), 'hidden' in botao.attrs, botao.texto()),
                         ('button', 'cf', True, 'Parar a animação'))
        self.assertFalse(any(a is calcada for a in botao.antepassados()))
        # P3: o crédito da fotografia no «i» («linha»), a seguir à ligação do portal; o rótulo e a ligação cruzada ficam à vista.
        self.assertEqual(portal.classes(), {'info-i', 'info-i--linha', 'sp-i'})
        self.assertEqual(portal.elementos()[0].attrs['aria-label'], 'Créditos da fotografia')
        self.assertEqual(norm(portal.elementos()[1].texto()), P3_AGORA)
        self.assertEqual(re.sub(r'[^\w ]', '', P3_ANTES.lower()).split(), re.sub(r'[^\w ]', '', P3_AGORA.lower()).split())
        self.assertIn('<a href="https://www.loc.gov/item/2005684184/">Library of Congress</a>', portal.elementos()[1].html_interior())
        irmaos = portal.pai.elementos()
        self.assertEqual(irmaos[irmaos.index(portal) - 1].attrs.get('class'), 'site-portal portal-lente')
        self.assertEqual(irmaos[irmaos.index(portal) + 1].attrs.get('class'), 'sp-credit')
        self.assertIn('<span class="sp-image-label">Eadweard Muybridge · 1878</span>', ler('index.html'))
        self.assertEqual(ler('index.html').count('class="sp-credit"'), 1)
        # P2: a imagem documental de cada índice; o crédito inteiro no «i» no canto da imagem, o figcaption sai.
        for rel, credito in CREDITOS_INDICES.items():
            with self.subTest(indice=rel):
                s = ler(rel)
                (d,) = inventario(s)['ii']
                self.assertEqual(d.elementos()[0].attrs['aria-label'], 'Créditos da imagem')
                self.assertEqual(norm(d.elementos()[1].texto()), credito)
                moldura = d.pai
                self.assertEqual(moldura.tag, 'div')
                self.assertTrue({'doc-i', 'com-i'} <= moldura.classes())
                self.assertEqual(moldura.pai.attrs.get('class'), 'doc')
                self.assertEqual([e.tag for e in moldura.pai.elementos()], ['div'], 'o figcaption sai')
                self.assertNotIn('figcaption', s[s.index('<figure class="doc">'):s.index('</figure>', s.index('<figure class="doc">'))])
                primeiro = moldura.elementos()[0]
                if rel in ('m3/index.html', 'm5/index.html'):
                    # A imagem dentro de uma ligação: o «i» fica fora dela, ao lado, na mesma moldura.
                    self.assertEqual((primeiro.tag, primeiro.elementos()[0].tag), ('a', 'img'))
                    self.assertIn('<a href="https://commons.wikimedia.org/wiki/File:', d.elementos()[1].html_interior())
                else:
                    self.assertEqual(primeiro.tag, 'img')
                self.assertEqual(sorted(i.texto() for i in d.descendentes() if i.tag == 'em'), sorted(TITULOS.get(rel, [])))
                # A largura da imagem com a altura fixa de 200 px, para o «i» ficar no canto dela quando o crédito abre por baixo.
                largura = re.search(r'width="(\d+)"', s[s.index('<figure class="doc">'):]).group(1)
                altura = re.search(r'height="(\d+)"', s[s.index('<figure class="doc">'):]).group(1)
                self.assertIn('>figure.doc>.doc-i{--doc-w:%.2fpx}' % (200 * int(largura) / int(altura)), s)
        licenca = [a for a in inventario(ler('m8/index.html'))['ii'][0].descendentes() if a.tag == 'a']
        self.assertEqual([(a.attrs.get('rel'), a.attrs.get('href'), a.texto()) for a in licenca],
                         [('license', 'https://creativecommons.org/licenses/by-sa/2.0/deed.pt', 'CC BY-SA 2.0')])
        self.assertIn('n.º 2', ler('m7/index.html'))
        # P4: o crédito do mapa no «i» no canto do mapa; à vista, o «© OpenStreetMap» curto; o p.credito sai.
        s = ler('atlas/index.html')
        (d,) = inventario(s)['ii']
        self.assertEqual(d.elementos()[0].attrs['aria-label'], 'Créditos do mapa')
        self.assertEqual(norm(d.elementos()[1].texto()), P4_CREDITO)
        self.assertEqual(d.pai.classes(), {'mapa-quadro', 'com-i'})
        self.assertIn('</svg><p class="mapa-osm">© OpenStreetMap</p><details class="info-i"', s)
        self.assertNotIn('class="credito"', s)

    def test_motor_dos_fundos_com_o_botao_novo(self):
        # Decisão 177: «Parar a animação» e, parado, «Retomar a animação», no motor comum (igual no Lente) e na entrada.
        js = ler('assets/fundos.js')
        self.assertIn("botao.textContent = anda() ? 'Parar a animação' : 'Retomar a animação';", js)
        self.assertIn('07/11/2026: decisão 177, era «Parar o desenho».', js)
        self.assertNotIn('Pôr o desenho a andar', js)
        s = ler('index.html')
        self.assertEqual(s.count('<script defer src="assets/fundos.js?v=20261107"></script>'), 1)
        self.assertNotIn('fundos.js?v=20261102-1', s)
        # Nenhuma outra página carrega o motor com a versão antiga.
        for p in ROOT.rglob('*.html'):
            rel = p.relative_to(ROOT).as_posix()
            if rel.startswith(('tests/', 'docs/', 'node_modules/', '.git/')):
                continue
            with self.subTest(pagina=rel):
                self.assertNotIn('fundos.js?v=20261102', p.read_text('utf-8', errors='replace'))


if __name__ == '__main__':
    unittest.main()
