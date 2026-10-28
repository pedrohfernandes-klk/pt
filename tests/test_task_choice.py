"""Tarefas com aquecimento e tema à escolha (28/10/2026, piloto no M2; decisão do docente de 27/10).

Contrato: aquecimento em papel com duas máquinas do exame (verbo, objeto e condição; prova ou distração),
núcleo comum (leitura e gramática) e dois temas, A sobre a língua da obra e B sobre a obra e o seu
público ou a sua atualidade, com dossiê de factos com fonte. Relógio do aluno no aquecimento e na produção."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, unittest
ROOT = Path(__file__).resolve().parents[1]
CHOICE = ['m2-u1', 'm2-u2']


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.stack, self.root, self.ids, self.links = [], [], [], []
        self.machines, self.themes, self.questions, self.options, self.criteria = [], [], [], [], 0
        self.text = {'header': [], 'criteria': [], 'dossier': []}
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.stack and self.stack[-1][0] == 'main': self.root.append((tag, a.get('id')))
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a': self.links.append(a.get('href', ''))
        if 'data-task-machine' in a: self.machines.append(a['data-task-machine'])
        if 'data-task-theme' in a: self.themes.append(a['data-task-theme'])
        if 'data-task-question' in a: self.questions.append((a['data-task-question'], any(x[0] == 'details' for x in self.stack)))
        if tag == 'button' and 'data-response' in a: self.options.append((self.questions[-1][0], a))
        if tag == 'li' and any('task-criteria' in x[1].get('class', '') for x in self.stack): self.criteria += 1
        if tag not in ('meta', 'link', 'br', 'img', 'input'): self.stack.append((tag, a))

    def handle_endtag(self, tag):
        if any(x[0] == tag for x in self.stack):
            i = max(i for i, x in enumerate(self.stack) if x[0] == tag); self.stack = self.stack[:i]

    def handle_data(self, data):
        if any(x[0] == 'header' for x in self.stack): self.text['header'].append(data)
        if any('task-criteria' in x[1].get('class', '') for x in self.stack): self.text['criteria'].append(data)
        if any('task-dossier' in x[1].get('class', '') for x in self.stack): self.text['dossier'].append(data)


class ChoiceTasks(unittest.TestCase):
    def test_warmup_core_and_two_themes(self):
        for slug in CHOICE:
            source = (ROOT / 'tarefas' / slug / 'index.html').read_text('utf-8'); p = Page(source)
            with self.subTest(task=slug):
                self.assertIn('data-task-compact data-task-choice', source)
                self.assertEqual([t for t, _ in p.root], ['nav', 'section', 'header', 'section', 'section'])
                self.assertEqual([i for _, i in p.root][1:], ['aquecer', None, 'apoios', 'entregar'])
                self.assertEqual(p.machines, ['1', '2'])
                self.assertEqual(p.themes, ['A', 'B'])
                self.assertEqual(len(re.findall(r'<li>', source.split('id="produzir"')[1].split('task-themes')[0])), 2)
                for token in ('Descobre o que te pedem', 'Prova ou distração?', 'Verbos', 'Objeto', 'Condição', 'Núcleo comum', 'Escolhe um tema',
                              'Dossiê do tema B', 'Tarefa individual', '90 min', 'consulta', 'Teams', 'duas linhas', 'tema que escolheste (A ou B)'):
                    self.assertIn(token, source)
                for token in ('task-clock', 'em grupo', 'rondas', '10/10/60/10', 'ficha', 'folha', '—', 'professor'):
                    self.assertNotIn(token, source)
                self.assertEqual(p.criteria, 3)
                self.assertLessEqual(len(' '.join(p.text['header'] + p.text['criteria']).split()), 300)
                # Uma pergunta de aquecimento e uma opcional; três opções, uma certa, explicações diferentes.
                self.assertEqual(p.questions, [('aquecer', False), ('1', True)])
                for q in ('aquecer', '1'):
                    opts = [a for k, a in p.options if k == q]
                    self.assertEqual(len(opts), 3)
                    self.assertEqual(sum(a['data-correct'] == 'true' for a in opts), 1)
                    self.assertEqual(len({a['data-response'] for a in opts}), 3)
                # Relógio do aluno: aquecimento até 15 min, produção até 60 min.
                self.assertIn(f'data-relogio data-max="15" data-passo="1" data-rotulo="Aquecimento" data-chave="pt-relogio:tarefas/{slug}:aquecimento"', source)
                self.assertIn(f'data-relogio data-max="60" data-passo="5" data-rotulo="Produção em papel" data-chave="pt-relogio:tarefas/{slug}:producao"', source)
                self.assertLess(source.index('assets/relogio.js'), source.index('pt-lessons/casca.js'))
                for asset in ('task-choice.css?v=20261028-escolha-1', 'task-reader.js?v=20261028-escolha-1', 'task-90.js?v=20261027-compact-1'):
                    self.assertIn(asset, source)

    def test_dossier_facts_carry_sources_and_links_exist(self):
        for slug in CHOICE:
            path = ROOT / 'tarefas' / slug / 'index.html'; source = path.read_text('utf-8'); p = Page(source)
            with self.subTest(task=slug):
                facts = re.findall(r'<section class="task-dossier".*?</section>', source, re.S)[0]
                self.assertGreaterEqual(facts.count('<li>'), 3)
                self.assertEqual(facts.count('<li>'), facts.count('class="task-fonte"'))
                lessons = [h for h in p.links if '/m2/licao-' in h]
                self.assertGreaterEqual(len(lessons), 4)
                for href in p.links:
                    url = urlsplit(href)
                    if url.scheme: continue
                    target = (path.parent / unquote(url.path)).resolve() if url.path else path
                    if target.is_dir(): target = target / 'index.html'
                    self.assertTrue(target.is_file(), href)

    def test_quotes_used_in_the_warmup_exist_in_the_lessons(self):
        lessons = ' '.join((ROOT / 'm2' / f / 'index.html').read_text('utf-8') for f in ('licao-m2-f02', 'licao-m2-f06', 'licao-m2-f07', 'licao-m2-f11'))
        flat = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|\\n', ' ', lessons))
        for slug in CHOICE:
            source = (ROOT / 'tarefas' / slug / 'index.html').read_text('utf-8')
            warm = source.split('id="aquecer"')[1].split('</section>')[0]
            choices = ' '.join(re.findall(r'</span> (.*?)</button>', warm))
            for quote in re.findall(r'«([^»]+)»', choices):
                for verse in [v.strip() for v in quote.replace('&#x27;', "'").split(' / ')]:
                    with self.subTest(task=slug, verso=verse):
                        self.assertIn(re.sub(r'\s+', ' ', verse), flat)

    def test_reader_puts_the_warmup_first(self):
        reader = (ROOT / 'assets/task-reader.js').read_text('utf-8')
        self.assertIn('node.id==="aquecer"?"Aquecer"', reader)
        self.assertIn('cards.unshift(cards.splice(warm,1)[0])', reader)
        self.assertNotIn('localStorage', reader)


if __name__ == '__main__':
    unittest.main()
