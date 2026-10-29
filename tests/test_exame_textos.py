"""Textos das sessões do exame (27/10/2026): compostos como no exame e presos às lições de onde vêm.

Cada verso ou parágrafo traz a referência à linha da lição (cartão e data-l). Se uma lição mudar,
este teste falha antes de o exame mostrar um texto diferente do que o aluno estudou."""
from pathlib import Path
from html.parser import HTMLParser
import html, json, re, sys, unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards


class Units(HTMLParser):
    """Linhas (span.ln) e parágrafos (p.pr) de um cartão, com a marcação dos dados: {termo|glosa} e _itálico_."""
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.units, self.cur, self.depth, self.gloss, self.skip = {}, None, [], None, 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = a.get('class', '').split()
        if self.cur is not None:
            if tag == 'span' and 'n' in cls: self.skip += 1; self.depth.append('skip'); return
            if tag == 'b' and 'gt' in cls: self.gloss = [a.get('data-s', ''), '']; self.depth.append('gt'); return
            if tag in ('i', 'em'):
                if self.gloss: self.gloss[1] += '_'
                else: self.cur['text'] += '_'
                self.depth.append('i'); return
            self.depth.append(tag); return
        if (tag == 'span' and 'ln' in cls) or (tag == 'p' and 'pr' in cls):
            self.cur = {'l': a.get('data-l', ''), 'text': ''}; self.depth = ['unit']

    def handle_endtag(self, tag):
        if self.cur is None: return
        kind = self.depth.pop() if self.depth else None
        if kind == 'skip': self.skip -= 1
        elif kind == 'gt': term = self.gloss; self.cur['text'] += '{' + term[1] + '|' + term[0] + '}'; self.gloss = None
        elif kind == 'i':
            if self.gloss: self.gloss[1] += '_'
            else: self.cur['text'] += '_'
        if not self.depth:
            self.units[self.cur['l']] = re.sub(r'\s+', ' ', self.cur['text']).strip(); self.cur = None

    def handle_data(self, data):
        if self.cur is None or self.skip: return
        if self.gloss is not None: self.gloss[1] += data
        else: self.cur['text'] += data


def words(text):
    text = re.sub(r'\{([^|{}]+)\|[^{}]+\}', r'\1', text).replace('_', ' ')
    return re.findall(r'[a-zà-öø-ÿ0-9]+', html.unescape(re.sub(r'<[^>]+>', ' ', text)).lower())


class ExamTexts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sessions = json.loads((ROOT / 'assets/exame/sessoes.json').read_text('utf-8'))['sessions']
        cls.cache = {}

    def card(self, url, index):
        key = (url, index)
        if key not in self.cache:
            self.cache[key] = lesson_cards(ROOT / url.removeprefix('/pt/') / 'index.html')[index]['html']
        return self.cache[key]

    def passages(self):
        for s in self.sessions:
            for p in s['source'].get('passages', []):
                yield s, p

    def test_fifteen_literary_sessions_have_composed_texts_and_no_flat_excerpt(self):
        with_texts = [s['id'] for s in self.sessions if s['source'].get('passages')]
        self.assertEqual(with_texts, ['s01', 's02', 's04', 's05', 's06', 's07', 's08', 's09', 's10', 's11', 's12', 's13', 's14', 's15', 's16'])
        for s in self.sessions:
            if s['source'].get('passages'):
                self.assertNotIn('excerpt', s['source'], s['id'])

    def test_shape_markup_and_labels(self):
        for s, p in self.passages():
            with self.subTest(session=s['id'], head=p['head']):
                self.assertIn(p['form'], ('verso', 'prosa', 'cena'))
                self.assertTrue(p['head'] and p['credit'])
                many = len(s['source']['passages']) > 1
                self.assertEqual('label' in p, many)
                lines = [l for st in p['stanzas'] for l in st] if p['form'] == 'verso' else [q['text'] for q in p['paragraphs']]
                self.assertTrue(lines)
                for text in lines + [p['head'], p['credit'], p.get('note', '')]:
                    self.assertEqual(text.count('{'), text.count('}'), text)
                    self.assertEqual(text.count('_') % 2, 0, text)
                    self.assertNotRegex(text, r'\w ,|\s{2}', text)  # nada do texto achatado antigo
                for text in (p['head'], p['credit'], p.get('note', '')):
                    self.assertNotRegex(text, r'\b[Ff](icha|olha)s?\b|—| · ', text)
                if p['form'] == 'verso':
                    self.assertTrue(all(isinstance(st, list) and st for st in p['stanzas']))

    def test_every_line_matches_its_lesson(self):
        checked = 0
        for s, p in self.passages():
            lines = [l for st in p['stanzas'] for l in st if l != '[…]'] if p['form'] == 'verso' else [q['text'] for q in p['paragraphs']]
            self.assertEqual(len(lines), len(p['refs']), (s['id'], p['head']))
            for text, ref in zip(lines, p['refs']):
                with self.subTest(session=s['id'], ref=ref):
                    source = self.card(ref['url'], ref['card'])
                    if ref.get('quote'):
                        self.assertIn(' '.join(words(text)), ' '.join(words(source)))
                    else:
                        unit = Units(source).units[ref['l']]
                        if p['form'] != 'verso':  # na prosa, a lição numera cada parágrafo ([1] ou B)
                            unit = re.sub(r'^(?:\[\d+\]|[A-Z])\s+', '', unit)
                        self.assertEqual(text, unit)
                    checked += 1
        self.assertGreaterEqual(checked, 160)

    def test_renderer_and_export_know_the_composed_form(self):
        app = (ROOT / 'assets/exame/app.js').read_text('utf-8')
        for token in ('function passage(p)', 'class="estrofe"', 'class="notas"', 'class="pass-credito"', 'fala-quem', 'pass-omissao'):
            self.assertIn(token, app)
        dossier = (ROOT / 'assets/exame/dossier.js').read_text('utf-8')
        self.assertIn("'Leitura':readingText(source)", dossier)


if __name__ == '__main__':
    unittest.main()
