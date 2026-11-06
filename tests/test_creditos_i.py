"""05/11/2026: decisões 153 e 162. Créditos atrás de um botão «i» (plano-creditos-i-20261105.md, secção 3.3).

O docente: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir». Confere, sem navegador:

* a peça comum (assets/info-i.css e assets/info-i.js) é igual, byte a byte, à registada em tests/fixtures/info-i-sha256.json,
  que é o mesmo ficheiro no Português e no Lente: mudar a peça num sítio obriga a mudá-la no outro;
* cada «i» (details.info-i), nas páginas e no HTML dos cartões (as cadeias JSON dos scripts e dos ficheiros de dados), tem a
  estrutura da peça: name="info-i"; primeiro filho um summary com aria-label começado por «Créditos» ou «Fonte» e só
  <span aria-hidden="true">i</span>; um só .info-i-texto não vazio (um p; um div só quando leva a ficha de um documento
  visual, que é uma tabela); fora de a, button, label, figcaption e [aria-hidden="true"]; a variante «canto» dentro de um
  .com-i; e a página carrega assets/info-i.css e assets/info-i.js;
* nenhum crédito longo fica à vista fora de um «i» (marcas de crédito em figure, figcaption, nas classes de crédito conhecidas e
  nos parágrafos colados a uma imagem), salvo o que está na lista fechada tests/fixtures/creditos-a-vista-20261105.json, com
  página, classe, contagem exata e razão. As famílias que esperam pedido entram com a contagem de hoje, que só pode descer:
  cada pedido põe a sua a zero e tira-a da lista. Um crédito longo novo, fora do «i», faz falhar o teste;
* cada fundo animado ([data-fundo]) tem exatamente um botão «Parar o desenho» ([data-fundo-botao]) com hidden no HTML, fora de
  qualquer «i» (decisão 153: o botão fica sempre à vista; WCAG 2.2.2).
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PECA = ('assets/info-i.css', 'assets/info-i.js')
SHA = ROOT / 'tests/fixtures/info-i-sha256.json'
LISTA = ROOT / 'tests/fixtures/creditos-a-vista-20261105.json'
# Fora de âmbito (secção 4 do plano): as páginas de demonstração; os testes e a documentação não são páginas do sítio.
FORA = ('.git/', 'node_modules/', 'tests/', 'docs/', 'demonstracoes/', 'como/', 'scripts/', 'tools/')
MARCAS = ('Domínio público', 'CC BY', 'CC0', 'Wikimedia Commons', 'commons.wikimedia.org', 'Grafismo gerado com recurso a IA',
          'Fotografia de', 'Fotografia:', 'Library of Congress', 'Biblioteca do Congresso', 'Metropolitan', 'Arquivo da EPI',
          'Open Access', 'sem restrições conhecidas')
CLASSES_CREDITO = {'credito', 'cz-credit', 'fr-cred', 'fa-cred', 'rosto-c', 'yt-cred', 'sp-credit', 'cf-credito', 'lf-credito',
                   'jc-credito', 'ld-credito', 'mr-cred', 'cred', 'tabela'}
VAZIOS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
# 05/11/2026: pedido pt-2, fatia 2. Os créditos de P11 a P13 tal como estavam à vista, letra a letra (o itálico do motor, _…_,
# mostrava-se sem os traços): o «i» tem de os ter inteiros.
# 06/11/2026: revisão do pedido pt-2. «H. C. White Co.» com espaços inseparáveis (decisão 152): as mesmas letras, sem partir.
P11_CREDITO = ('Duas fotografias sobrepostas: um jardim de Lisboa em 1907 e o Tejo diante da Praça do Comércio, cerca de 1910 '
               '(H.\u00a0C.\u00a0White\u00a0Co. e National Photo Company; Biblioteca do Congresso dos EUA, sem restrições conhecidas).')
P12_CREDITOS = {
    'm1/licao-m1-f19/index.html': ['Ilha de San Simón, ria de Vigo (Iago Pillado, 2024). CC BY-SA 4.0.',
                                   'Pergaminho Vindel, com «Ondas do mar de Vigo». Domínio público.'],
    'm4/licao-m4-f01/index.html': ['Garcia Fernandes (pormenor)', 'Retrato, séc. XVIII (pormenor)'],
    'm4/licao-m4-f02/index.html': ['Garcia Fernandes (pormenor)', 'Retrato, séc. XVIII (pormenor)'],
    'm4/licao-m4-f11/index.html': ['Retrato, séc. XVIII (pormenor)', 'José Malhoa, 1881'],
}
_P13_PEIXE = ('peixe-voador-1889.jpg', 'Cromolitografia: Allen & Ginter, _Peixe-voador_ (série _Fish from American Waters_), '
              '1889, The Met. Domínio público.')
_P13_BOCCIONI = ('boccioni-cidade-que-sobe-1910.jpg', 'Pintura: Umberto Boccioni, _A cidade que sobe_, 1910, MoMA. Domínio público.')
_P13_FREI = ('frei-luis-personagens-1844.jpg', 'Imagem: _Frei Luiz de Sousa_, primeira edição, 1844. Domínio público.')
P13_CREDITOS = {'m4/licao-m4-f01/index.html': _P13_PEIXE, 'm4/painel-m4-f01/index.html': _P13_PEIXE,
                'm4/licao-m4-f04/index.html': _P13_BOCCIONI, 'm4/painel-m4-f04/index.html': _P13_BOCCIONI,
                'm4/licao-m4-f11/index.html': _P13_FREI, 'm4/painel-m4-f11/index.html': _P13_FREI}
# 05/11/2026: pedido pt-2, fatia 3. Os créditos dos «Pensar devagar» (P14) tal como estavam no span.fr-cred, letra a letra (o
# texto, com a ligação «commons.wikimedia.org»); no «i», só a primeira letra sobe a maiúscula, porque o crédito o abre sozinho.
P14_CREDITOS = {
    'm1/m1-promessa-do-cronista': 'Crónicas de Jean Froissart (iluminura). Domínio público. commons.wikimedia.org',
    'm1/m1-voz-emprestada': 'Domínio público. commons.wikimedia.org',
    'm2/m2-ines-escolhe-duas-vezes': 'impressão de João Álvares, 1562 (reprodução de Victorcouto). Domínio público. '
                                     'commons.wikimedia.org',
    'm2/m2-maquina-de-rir': 'CC0. commons.wikimedia.org',
    'm3/m3-soneto-raciocinio': 'página impressa de 1595. Domínio público. commons.wikimedia.org',
    'm3/m3-velho-restelo-juri': 'Luís de Camões. Academia Brasileira de Letras, via Wikimedia Commons. Domínio público. '
                                'commons.wikimedia.org',
    'm4/m4-frei-luis-quem-sabia': 'Almeida Garrett (edição de 1844, BNP). Domínio público. commons.wikimedia.org',
    'm4/m4-sermao-tribunal': 'Domínio público. commons.wikimedia.org',
    'm5/m5-o-pais-ou-eles': 'Domínio público. commons.wikimedia.org',
    'm5/m5-quem-podia-ter-feito-diferente': 'Lucas de Almeida Marrão (BNP). Domínio público. commons.wikimedia.org',
    'm6/m6-antero-viagem-ao-nada': 'Domínio público. commons.wikimedia.org',
    'm6/m6-cesario-noite-inteira': 'José Artur Leitão Bárcia (Arquivo Municipal de Lisboa). Domínio público. '
                                   'commons.wikimedia.org',
    'm7/m7-fingidor-maquina': 'autor não identificado (fotografia de 1929). Domínio público. commons.wikimedia.org',
    'm7/m7-quatro-vozes-um-problema': 'revista Orpheu. Domínio público. commons.wikimedia.org',
    'm8/m8-poema-testemunha': 'Domínio público. commons.wikimedia.org',
    # 06/11/2026: revisão do pedido pt-2. O autor que a CC BY-SA 3.0 exige, confirmado no Commons (File:Mafra_May_2013-2.jpg).
    'm9/m9-de-quem-e-o-convento': 'Fotografia de Alvesgaspar, 2013. CC BY-SA 3.0. commons.wikimedia.org',
    'm9/m9-ver-e-nao-ver': 'Bartolomeu de Gusmão (fac-símile). Domínio público. commons.wikimedia.org',
}
# 06/11/2026: confirmação final do pedido pt-2. Os títulos de obras em itálico nos créditos da P14 que os têm (nenhuma palavra
# muda: as letras continuam as de P14_CREDITOS); nos outros créditos da P14 não há itálico.
P14_ITALICOS = {'m1/m1-promessa-do-cronista': ['Crónicas'], 'm7/m7-quatro-vozes-um-problema': ['Orpheu']}
# 06/11/2026: confirmação final do pedido pt-2. Títulos de obras que ficavam em redondo nos créditos alterados (P7, P14 e P16): em
# cada «i» das lições M1 e M4 (P7), dos «Pensar devagar» (P14) e das galerias «Para ver» (P16), e em cada legenda à vista das
# galerias, cada ocorrência vive dentro de um <i>.
TITULOS_ITALICO = ('Painéis de São Vicente', 'Crónicas', 'Santo António a pregar aos peixes', 'Cícero denuncia Catilina no Senado',
                   'In Memoriam', 'Cancioneiro da Biblioteca Nacional', 'Orpheu')
# Os quatro «Olhar» (P15): o campo credito, com os pontos médios passados a pontos finais (nenhuma palavra sai), e o creditoUrl,
# que passa a viver no «i» (ligado a «Wikimedia Commons»).
P15_OLHAR = {
    'm1/olhar-ajuda/index.html': ('_Cancioneiro da Ajuda_, fólio 21r. Domínio público. Wikimedia Commons.',
                                  'https://commons.wikimedia.org/w/index.php?curid=168669'),
    'm1/olhar-andeiro/index.html': ('José de Sousa Azevedo, _Morte do Conde Andeiro_ (c.\u00a01860), Museu Nacional de Soares dos '
                                    'Reis, Porto. Domínio público. Wikimedia Commons.',
                                    'https://commons.wikimedia.org/w/index.php?curid=1539861'),
    'm4/olhar-lupi/index.html': ('Miguel Ângelo Lupi, _D. João de Portugal_ (1863). Domínio público. Wikimedia Commons.',
                                 'https://commons.wikimedia.org/w/index.php?curid=39076717'),
    'm7/olhar-pessoa/index.html': ('Fernando Pessoa, fotografia de 1914. Domínio público. Wikimedia Commons.',
                                   'https://commons.wikimedia.org/w/index.php?curid=56775462'),
}
# 06/11/2026: revisão do pedido pt-2. As legendas à vista da P16 que não são o começo do crédito, e o começo exato do crédito de
# cada uma: «retrato imaginado» diz o que se vê; os dois retratos de Antero de Quental distinguem-se pelo autor e pela data; a
# página do Cancioneiro da Biblioteca Nacional deixa de ficar truncada.
P16_A_VISTA = {
    'Fernão Lopes (retrato imaginado).': 'Fernão Lopes (retrato imaginado, Pollini).',
    'Antero de Quental (fotografia, c. 1887).': 'Antero de Quental (fotografia, c. 1887, publicada em In Memoriam, 1896).',
    'Antero de Quental (Columbano Bordalo Pinheiro, 1889).': 'Antero de Quental (Columbano Bordalo Pinheiro, 1889, MNAC).',
    'Uma página do Cancioneiro da Biblioteca Nacional.': 'Cancioneiro da Biblioteca Nacional, página (cópia do século XVI).',
}
# As galerias «Para ver» dos nove mapas (P16, mais Pessoa, da P10): figuras e ligações «Lição Mx-Fyy» por mapa.
P16_GALERIAS = {1: (11, 11), 2: (4, 4), 3: (8, 8), 4: (12, 10), 5: (7, 7), 6: (7, 7), 7: (19, 19), 8: (4, 4), 9: (7, 7)}
LICENCA = re.compile(r'(Domínio público(?: \(The Met, Open Access\))?|CC0|CC BY(?:-SA)? \d\.\d)\.')


class No:
    __slots__ = ('tag', 'attrs', 'filhos', 'pai')

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

    def texto(self, parar=lambda n: False):
        partes = []
        for f in self.filhos:
            if isinstance(f, str):
                partes.append(f)
            elif f.tag not in ('script', 'style', 'template') and not parar(f):
                partes.append(f.texto(parar))
        return ''.join(partes)

    def antepassados(self):
        n = self.pai
        while n is not None:
            yield n
            n = n.pai


class Arvore(HTMLParser):
    """Uma árvore mínima (só a biblioteca padrão): elementos, atributos e texto; os fechos em falta fecham-se sozinhos."""

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


def paginas():
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT).as_posix()
        if not rel.startswith(FORA):
            yield rel, p.read_text('utf-8', errors='replace')


def dados():
    """Ficheiros de dados com o HTML dos cartões (fora das páginas): os .js das lições e os .json do sítio."""
    for p in sorted(list(ROOT.rglob('*.js')) + list(ROOT.rglob('*.json'))):
        rel = p.relative_to(ROOT).as_posix()
        if not rel.startswith(FORA):
            yield rel, p.read_text('utf-8', errors='replace')


def cadeias(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from cadeias(v)
    elif isinstance(valor, list):
        for v in valor:
            yield from cadeias(v)


INICIO_JSON = re.compile(r'(?:[=(:,\[]|^)\s*([\[{])', re.M)


def html_em_json(codigo):
    """O HTML que vive dentro de dados JSON num script (CARTOES=[…], var U=…): cada cadeia com etiquetas."""
    decoder, i, out = json.JSONDecoder(), 0, []
    for m in INICIO_JSON.finditer(codigo):
        k = m.start(1)
        if k < i:
            continue
        try:
            valor, fim = decoder.raw_decode(codigo, k)
        except ValueError:
            continue
        i = fim
        out += [c for c in cadeias(valor) if '<' in c and re.search(r'<[a-z][^>]*>', c)]
    return out


def explicacoes(codigo):
    """05/11/2026: os textos das explicações (campos f e fe) nos dados JSON de um script: cartões e material dos painéis."""
    decoder, i = json.JSONDecoder(), 0
    for m in INICIO_JSON.finditer(codigo):
        k = m.start(1)
        if k < i:
            continue
        try:
            valor, fim = decoder.raw_decode(codigo, k)
        except ValueError:
            continue
        i = fim
        pilha = [valor]
        while pilha:
            v = pilha.pop()
            if isinstance(v, dict):
                for chave, w in v.items():
                    if chave in ('f', 'fe'):
                        yield from cadeias(w)
                    else:
                        pilha.append(w)
            elif isinstance(v, list):
                pilha.extend(v)


def fragmentos(rel, texto):
    """A árvore da página e as árvores do HTML dentro dos dados JSON dos seus scripts (ou do ficheiro de dados)."""
    if rel.endswith('.html'):
        arvore = Arvore(texto).raiz
        yield arvore
        for s in arvore.descendentes():
            if s.tag == 'script' and not s.attrs.get('src'):
                for h in html_em_json(s.texto()):
                    yield Arvore(h).raiz
    elif rel.endswith('.json'):
        try:
            valor = json.loads(texto)
        except ValueError:
            return
        for c in cadeias(valor):
            if '<' in c and re.search(r'<[a-z][^>]*>', c):
                yield Arvore(c).raiz
    else:
        for h in html_em_json(texto):
            yield Arvore(h).raiz


def e_i(no):
    return isinstance(no, No) and no.tag == 'details' and 'info-i' in no.classes()


def tem_imagem_so(no):
    """Um elemento que é só uma imagem (img, ou uma ligação ou moldura com uma só imagem e sem texto)."""
    if no.tag in ('img', 'picture'):
        return True
    imgs = [d for d in no.descendentes() if d.tag == 'img']
    return len(imgs) == 1 and not no.texto().strip()


def e_credito(no):
    if no.tag in ('figure', 'figcaption') or (no.classes() & CLASSES_CREDITO):
        return True
    if no.tag == 'p' and no.pai is not None:
        irmaos = no.pai.elementos()
        k = irmaos.index(no)
        return k > 0 and tem_imagem_so(irmaos[k - 1])
    return False


def titulos_em_redondo(no):
    """06/11/2026: os títulos de TITULOS_ITALICO que aparecem no texto de um nó (sem o summary do «i») fora de um <i>."""
    texto = no.texto(lambda n: n.tag == 'summary')
    italicos = [n.texto() for n in no.descendentes() if n.tag == 'i']
    return [t for t in TITULOS_ITALICO if texto.count(t) != sum(i.count(t) for i in italicos)]


def creditos_a_vista(raiz):
    """Cada elemento de crédito cujo texto próprio (sem os «i» e sem os elementos de crédito dentro dele) tem uma marca."""
    out = []
    for no in raiz.descendentes():
        if not e_credito(no) or any(e_i(a) for a in no.antepassados()):
            continue
        texto = no.texto(lambda n: e_i(n) or e_credito(n))
        if any(m in texto for m in MARCAS):
            out.append(no.tag + ''.join('.' + c for c in sorted(no.classes())))
    return out


def contagem_atual():
    contagem = Counter()
    for rel, texto in list(paginas()) + list(dados()):
        for raiz in fragmentos(rel, texto):
            for classe in creditos_a_vista(raiz):
                contagem[(rel, classe)] += 1
    return contagem


class CreditosI(unittest.TestCase):
    def test_peca_igual_nos_dois_sitios(self):
        registo = json.loads(SHA.read_text('utf-8'))
        for rel in PECA:
            with self.subTest(ficheiro=rel):
                self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), registo['sha256'][rel])
        self.assertEqual(sorted(registo['sha256']), sorted(PECA))

    def test_estrutura_de_cada_i(self):
        total = 0
        for rel, texto in list(paginas()) + [('tests/fixtures/info-i.html', (ROOT / 'tests/fixtures/info-i.html').read_text('utf-8'))]:
            arvore = None
            for raiz in fragmentos(rel, texto):
                arvore = arvore or raiz
                for d in (n for n in raiz.descendentes() if e_i(n)):
                    total += 1
                    with self.subTest(pagina=rel, i=total):
                        self.assertEqual(d.attrs.get('name'), 'info-i')
                        filhos = d.elementos()
                        self.assertTrue(filhos and filhos[0].tag == 'summary', 'o primeiro filho é o summary')
                        s = filhos[0]
                        self.assertRegex(s.attrs.get('aria-label', ''), r'^(Créditos|Fonte)\b')
                        self.assertEqual([(e.tag, e.attrs.get('aria-hidden')) for e in s.elementos()], [('span', 'true')])
                        self.assertEqual(s.texto().strip(), 'i')
                        self.assertEqual(s.elementos()[0].elementos(), [])
                        textos = [e for e in filhos[1:] if 'info-i-texto' in e.classes()]
                        self.assertEqual(len(textos), 1, 'um só .info-i-texto')
                        self.assertEqual(len(filhos), 2, 'só o summary e o crédito')
                        t = textos[0]
                        self.assertIn(t.tag, ('p', 'div'))
                        if t.tag == 'div':
                            self.assertTrue(any(e.tag == 'table' for e in t.descendentes()), 'div só com a ficha (tabela)')
                        self.assertTrue(t.texto().strip())
                        for a in d.antepassados():
                            self.assertNotIn(a.tag, ('a', 'button', 'label', 'figcaption'))
                            self.assertNotEqual(a.attrs.get('aria-hidden'), 'true')
                        if 'info-i--linha' not in d.classes():
                            self.assertIn('com-i', d.pai.classes(), 'a variante «canto» vive num .com-i')
                        # A ordem: imagem, «i», legenda. Nada de crédito longo dentro do summary.
                        irmaos = d.pai.elementos()
                        depois = irmaos[irmaos.index(d) + 1:]
                        self.assertFalse(any(e.tag in ('img', 'picture') for e in depois), 'o «i» vem depois da imagem')
                        self.assertTrue(re.search(r'href="[^"]*assets/info-i\.css(\?[^"]*)?"', texto), 'carrega info-i.css')
                        self.assertTrue(re.search(r'src="[^"]*assets/info-i\.js(\?[^"]*)?"', texto), 'carrega info-i.js')
        # 05/11/2026: pedido pt-2, fatia 1: 47 «i» nas lições M1 e M4 (P7), 6 nos documentos visuais (P9) e 7 na página de ensaio.
        # 05/11/2026: fatia 2: mais 3 de Pessoa (P10), 1 da dupla exposição (P11), 8 retratos (P12) e 6 imagens do campo ver (P13).
        # 05/11/2026: fatia 3: mais 17 «Pensar devagar» (P14) e 78 figuras das galerias (P16); os quatro «Olhar» (P15) montam o «i»
        # no motor e conferem-se à parte.
        self.assertGreaterEqual(total, 47 + 6 + 7 + 3 + 1 + 8 + 6 + 17 + 78)

    def test_nenhum_credito_longo_a_vista(self):
        lista = json.loads(LISTA.read_text('utf-8'))
        esperado = {}
        for e in lista['creditos']:
            chave = (e['pagina'], e['classe'])
            self.assertNotIn(chave, esperado, f'entrada repetida: {chave}')
            self.assertTrue(e['razao'].strip(), chave)
            self.assertGreater(e['contagem'], 0, f'{chave}: uma família a zero sai da lista')
            esperado[chave] = e['contagem']
        atual = contagem_atual()
        novos = {k: v for k, v in atual.items() if k not in esperado}
        self.assertEqual(novos, {}, 'créditos longos à vista fora de um «i» e fora da lista fechada')
        diferentes = {k: (esperado[k], atual.get(k, 0)) for k in esperado if atual.get(k, 0) != esperado[k]}
        self.assertEqual(diferentes, {}, '(esperado, atual): a lista tem a contagem exata; uma família feita sai da lista')

    def test_o_teste_reconhece_um_credito_a_vista(self):
        raiz = Arvore('<figure><div class="moldura com-i"><img alt="x"><details class="info-i" name="info-i"><summary '
                      'aria-label="Créditos da imagem"><span aria-hidden="true">i</span></summary><p class="info-i-texto">'
                      'Domínio público.</p></details></div><figcaption>A legenda.</figcaption></figure>'
                      '<figure><img alt="y"><figcaption>Autor, 1900. Domínio público.</figcaption></figure>'
                      '<a href="#"><img alt="z"></a><p>Fotografia de alguém.</p>').raiz
        self.assertEqual(creditos_a_vista(raiz), ['figcaption', 'p'])
        self.assertEqual(html_em_json('var K="x",CARTOES=[{"html":"<figcaption>CC BY 4.0</figcaption>"}];'),
                         ['<figcaption>CC BY 4.0</figcaption>'])

    # 05/11/2026: pedido pt-2, fatia 2. O que o varrimento não vê por inteiro: a instrução da dupla exposição que fica à vista
    # (P11), os retratos do «Em paralelo» letra a letra (P12) e o crédito que vivia no fim da explicação, um texto sem etiquetas
    # (P13). Cada crédito passa inteiro para o «i»: nada se encurta.
    def test_p11_a_instrucao_da_dupla_exposicao_fica_a_vista(self):
        texto = (ROOT / 'm7/licao-m7-f34/index.html').read_text('utf-8')
        figuras = [n for raiz in fragmentos('m7/licao-m7-f34/index.html', texto) for n in raiz.descendentes()
                   if n.tag == 'figure' and 'dupla' in n.classes()]
        self.assertEqual(len(figuras), 1)
        fig = figuras[0]
        legenda = [n for n in fig.elementos() if n.tag == 'figcaption'][0]
        self.assertEqual(legenda.texto().split('os dois planos')[-1], 'Toca num pedaço do verso: acende-se o seu plano.')
        self.assertEqual(len([n for n in legenda.descendentes() if n.tag == 'input']), 5, 'os botões dos versos ficam')
        ii = [n for n in fig.descendentes() if e_i(n)]
        self.assertEqual(len(ii), 1)
        self.assertEqual(ii[0].pai.elementos()[0].attrs.get('role'), 'img', 'o «i» fica fora do div com role="img"')
        self.assertEqual(ii[0].texto(lambda n: n.tag == 'summary'), P11_CREDITO)

    def test_p12_retratos_do_em_paralelo_com_i(self):
        for rel, creditos in P12_CREDITOS.items():
            texto = (ROOT / rel).read_text('utf-8')
            with self.subTest(pagina=rel):
                self.assertNotIn('rosto-c', texto)
                vistos = []
                for raiz in fragmentos(rel, texto):
                    for img in (n for n in raiz.descendentes() if n.tag == 'img' and 'rosto' in n.classes()):
                        irmaos = img.pai.elementos()
                        d = irmaos[irmaos.index(img) + 1]
                        self.assertTrue(e_i(d) and 'info-i--linha' in d.classes(), 'o «i» («linha») logo depois do retrato')
                        self.assertRegex(d.elementos()[0].attrs.get('aria-label', ''), r'^Créditos da imagem: \S')
                        vistos.append(re.sub(r'\s', ' ', d.texto(lambda n: n.tag == 'summary')))
                        if 'CC BY' in vistos[-1]:
                            self.assertTrue(any(a.tag == 'a' and a.attrs.get('rel') == 'license' and 'creativecommons.org' in
                                                a.attrs.get('href', '') for a in d.descendentes()), 'a ligação da licença')
                self.assertEqual(vistos, creditos)

    def test_p13_o_credito_sai_da_explicacao_para_o_i_da_imagem(self):
        for rel, (imagem, credito) in P13_CREDITOS.items():
            texto = (ROOT / rel).read_text('utf-8')
            with self.subTest(pagina=rel):
                vers = [json.loads('"' + m.group(1) + '"') for m in re.finditer(r'"ver":"((?:[^"\\]|\\.)*)"', texto)
                        if imagem in m.group(1)]
                self.assertEqual(len(vers), 1)
                ii = [n for n in Arvore(vers[0]).raiz.descendentes() if e_i(n)]
                self.assertEqual(len(ii), 1)
                # Nas lições, a imagem ocupa a largura do cartão («canto»); nos painéis, tem menos de 240 px numa das larguras
                # medidas («linha»).
                self.assertEqual('info-i--linha' in ii[0].classes(), '/painel-' in rel)
                self.assertIn('com-i', ii[0].pai.classes())
                self.assertEqual([e.tag for e in ii[0].pai.elementos()], ['img', 'details'])
                self.assertEqual(ii[0].texto(lambda n: n.tag == 'summary'), credito.replace('_', ''))
        # Em nenhuma página fica um crédito no texto de uma explicação (campos f e fe dos cartões e do material dos painéis).
        vistas = 0
        for rel, texto in paginas():
            for s in (n for n in Arvore(texto).raiz.descendentes() if n.tag == 'script' and not n.attrs.get('src')):
                for valor in explicacoes(s.texto()):
                    vistas += 1
                    self.assertFalse(any(k in valor for k in MARCAS), (rel, valor[-90:]))
        self.assertGreater(vistas, 1000)

    # 05/11/2026: pedido pt-2, fatia 3. P14: o crédito do fr-cred passa inteiro para o «i» da moldura; a legenda (fr-leg) fica à
    # vista, sozinha no figcaption. P15: o motor dos «Olhar» monta o «i» e liga-o ao creditoUrl. P16: nas galerias «Para ver», cada
    # figura tem o «i» entre a imagem e a legenda, com o crédito inteiro (a identificação e a licença), e a legenda guarda o que se
    # vê e a ligação «Lição Mx-Fyy».
    def test_p14_pensar_devagar_com_i(self):
        # Todas as páginas com uma figura fig-rev com legenda (o m8-george-tres-idades só tem as regras de estilo).
        vistas = sorted(p.relative_to(ROOT).parent.as_posix() for p in ROOT.glob('m[1-9]/m[1-9]-*/index.html')
                        if 'class=\\"fr-leg\\"' in p.read_text('utf-8'))
        self.assertEqual(vistas, sorted(P14_CREDITOS))
        for pasta, credito in P14_CREDITOS.items():
            rel = pasta + '/index.html'
            texto = (ROOT / rel).read_text('utf-8')
            with self.subTest(pagina=rel):
                self.assertNotIn('fr-cred\\"', texto)
                figuras = [n for raiz in fragmentos(rel, texto) for n in raiz.descendentes()
                           if n.tag == 'figure' and 'fig-rev' in n.classes()]
                self.assertEqual(len(figuras), 1)
                moldura, legenda = figuras[0].elementos()
                self.assertEqual((moldura.tag, sorted(moldura.classes())), ('div', ['com-i', 'fr-moldura']))
                self.assertEqual([e.tag for e in moldura.elementos()], ['img', 'details'])
                ii = moldura.elementos()[1]
                self.assertTrue(e_i(ii) and 'info-i--linha' not in ii.classes(), 'o «i» («canto») na moldura')
                self.assertEqual(ii.elementos()[0].attrs.get('aria-label'), 'Créditos da imagem')
                self.assertEqual(ii.texto(lambda n: n.tag == 'summary'), credito[:1].upper() + credito[1:])
                # 06/11/2026: confirmação final do pedido pt-2. E o itálico dos títulos, exatamente onde o há.
                self.assertEqual([n.texto() for n in ii.descendentes() if n.tag == 'i'], P14_ITALICOS.get(pasta, []))
                if 'CC BY' in credito:
                    self.assertTrue(any(a.tag == 'a' and a.attrs.get('rel') == 'license' for a in ii.descendentes()))
                self.assertEqual(legenda.tag, 'figcaption')
                self.assertEqual([sorted(e.classes()) for e in legenda.elementos()], [['fr-leg']], 'só a legenda fica à vista')
                self.assertTrue(legenda.texto().strip())
                self.assertFalse(any(m in legenda.texto() for m in MARCAS))

    def test_p15_olhar_com_i_e_ligacao(self):
        for rel, (credito, url) in P15_OLHAR.items():
            texto = (ROOT / rel).read_text('utf-8')
            with self.subTest(pagina=rel):
                self.assertNotIn('class="credito"', texto)
                self.assertEqual(texto.count(f'"credito":"{json.loads(chr(34) + credito + chr(34))}","creditoUrl":"{url}"'), 1)
                self.assertNotIn('·', json.loads('"' + credito + '"'))
                motor = re.search(r'function imagem\(\)\{return E\.imagemData\?(.*?)\}', texto).group(1)
                self.assertIn('<div class="com-i olhar-com-i"><img class="img"', motor)
                variante = ' info-i--linha' if rel == 'm7/olhar-pessoa/index.html' else ''
                self.assertIn(f'<details class="info-i{variante}" name="info-i"><summary aria-label="Créditos da imagem"><span '
                              f'aria-hidden="true">i</span></summary><p class="info-i-texto">\'+creditoI()+\'</p></details></div>',
                              motor)
                self.assertRegex(texto, r'function creditoI\(\)\{var c=it\(E\.credito\),u=E\.creditoUrl')
                self.assertIn('#palco .olhar-com-i{width:fit-content;max-width:100%;margin:0 auto}', texto)

    def test_p16_galerias_para_ver_com_i(self):
        for n, (figuras_esperadas, licoes_esperadas) in P16_GALERIAS.items():
            rel = f'm{n}/mapa-do-modulo-m{n}/index.html'
            texto = (ROOT / rel).read_text('utf-8')
            with self.subTest(pagina=rel):
                galeria = [d for d in Arvore(texto).raiz.descendentes() if d.tag == 'div' and 'galeria' in d.classes()]
                self.assertEqual(len(galeria), 1)
                figuras = [f for f in galeria[0].elementos() if f.tag == 'figure']
                self.assertEqual(len(figuras), figuras_esperadas)
                nomes, licoes = [], 0
                for f in figuras:
                    img, ii, legenda = f.elementos()
                    self.assertEqual((img.tag, legenda.tag), ('img', 'figcaption'), 'a ordem: imagem, «i», legenda')
                    self.assertTrue(e_i(ii) and 'info-i--linha' in ii.classes(), 'o «i» («linha») entre a imagem e a legenda')
                    nome = ii.elementos()[0].attrs.get('aria-label', '')
                    self.assertRegex(nome, r'^Créditos da imagem: \S')
                    nomes.append(nome)
                    credito = re.sub(r'\s', ' ', ii.texto(lambda x: x.tag == 'summary'))
                    links = [a for a in legenda.elementos() if a.tag == 'a']
                    licoes += len(links)
                    self.assertTrue(all(re.fullmatch(r'Lição M\d-F\d+', a.texto()) for a in links), 'na legenda, só «Lição Mx-Fyy»')
                    visivel = re.sub(r'\s', ' ', legenda.texto(lambda x: x.tag == 'a')).strip()
                    self.assertFalse(any(m in visivel for m in MARCAS) or LICENCA.search(visivel), (rel, visivel))
                    if 'PessoaChapeu' in str([a.attrs for a in ii.descendentes()]):
                        continue  # Pessoa, cerca de 1914 (P10): os seis campos, conferidos em test_varredura_formatacao.
                    # O crédito começa pela identificação que fica à vista (sem o parêntese final) e acaba na licença (e na Fonte).
                    # 06/11/2026: revisão do pedido pt-2. Salvo as quatro legendas da lista fechada P16_A_VISTA, cada uma com o começo
                    # exato do seu crédito (o que diz o que se vê e distingue duas imagens fica à vista; o crédito fica inteiro).
                    self.assertTrue(credito.startswith(P16_A_VISTA.get(visivel, visivel[:-1])), (rel, visivel, credito))
                    self.assertRegex(credito, r'^[^()]*(\([^()]*\)[^()]*)*' + LICENCA.pattern + r'( Fonte: [^.]+\.)?$')
                    # 06/11/2026: confirmação final do pedido pt-2. Os títulos de obras em itálico, à vista e no «i»; o nome do «i»
                    # continua sem etiquetas.
                    self.assertEqual(titulos_em_redondo(legenda) + titulos_em_redondo(ii), [], (rel, visivel))
                    self.assertNotRegex(nome, r'[<>]')
                    if 'CC BY' in credito:
                        self.assertTrue(any(a.tag == 'a' and a.attrs.get('rel') == 'license' and 'creativecommons.org/licenses/'
                                            in a.attrs.get('href', '') for a in ii.descendentes()), 'a ligação da licença')
                self.assertEqual(len(set(nomes)), len(nomes), 'cada «i» da galeria tem o seu nome')
                self.assertEqual(licoes, licoes_esperadas)

    # 06/11/2026: confirmação final do pedido pt-2. Os títulos de obras em itálico no «i» das lições M1 e M4 (P7, e com elas a P12
    # e a P13) e dos «Pensar devagar» (P14): «<i>Cancioneiro da Biblioteca Nacional</i>, cópia do século XVI.» em M1-F01, como em
    # M1-F04; «<i>Crónicas</i> de Jean Froissart» e «Revista <i>Orpheu</i>». As galerias «Para ver» (P16) conferem-se em
    # test_p16_galerias_para_ver_com_i.
    def test_titulos_de_obras_em_italico_no_i(self):
        vistos = set()
        for rel, texto in paginas():
            if not re.fullmatch(r'm[14]/licao-m[14]-f\d+/index\.html|m[1-9]/m[1-9]-[^/]+/index\.html', rel):
                continue
            for raiz in fragmentos(rel, texto):
                for d in (n for n in raiz.descendentes() if e_i(n)):
                    with self.subTest(pagina=rel):
                        self.assertEqual(titulos_em_redondo(d), [])
                    vistos.update(t for t in TITULOS_ITALICO if t in d.texto(lambda n: n.tag == 'summary'))
        # O teste vê todos os títulos da lista, salvo «In Memoriam», que só está na galeria do mapa M6.
        self.assertEqual(vistos, set(TITULOS_ITALICO) - {'In Memoriam'})
        texto = (ROOT / 'm1/licao-m1-f01/index.html').read_text('utf-8')
        self.assertEqual(texto.count('<i>Cancioneiro da Biblioteca Nacional</i>, cópia do século XVI. Domínio público.'), 1)

    def test_parar_o_desenho_fora_do_i(self):
        vistos = 0
        for rel, texto in paginas():
            arvore = Arvore(texto).raiz
            nos = list(arvore.descendentes())
            for f in (n for n in nos if 'data-fundo' in n.attrs):
                vistos += 1
                with self.subTest(pagina=rel, fundo=f.attrs['data-fundo']):
                    botoes = [n for n in nos if n.attrs.get('data-fundo-botao') == f.attrs['data-fundo']]
                    self.assertEqual(len(botoes), 1)
                    b = botoes[0]
                    self.assertIn('hidden', b.attrs, 'sem JavaScript, o desenho fica parado e o botão escondido')
                    self.assertFalse(any(e_i(a) for a in b.antepassados()), '«Parar o desenho» fica fora do «i»')
        self.assertGreaterEqual(vistos, 1)


if __name__ == '__main__':
    unittest.main()
