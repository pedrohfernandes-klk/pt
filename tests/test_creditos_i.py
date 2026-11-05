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
        self.assertGreaterEqual(total, 47 + 6 + 7)

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
