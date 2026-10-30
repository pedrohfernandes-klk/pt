"""Tarefas com aquecimento e tema à escolha (28/10/2026, piloto no M2; decisão do docente de 27/10).

Contrato: aquecimento em papel com duas máquinas do exame (verbo, objeto e condição; prova ou distração),
núcleo comum (leitura e gramática) e dois temas, A sobre a língua da obra e B sobre a obra e o seu
público ou a sua atualidade, com dossiê de factos com fonte. Relógio do aluno no aquecimento e na produção."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import html, json, re, subprocess, sys, tempfile, unittest
ROOT = Path(__file__).resolve().parents[1]
# 28/10/2026 (decisão do docente, PR #122): as duas aulas de tarefa do M1 passam ao formato do piloto do M2,
# geradas por scripts/tarefas_escolha.py a partir de docs/pedagogia/tarefas-escolha/<slug>.json.
# 29/10/2026 (decisão do docente): a tarefa da unidade 3 do M7 («Louco, sim: argumentar com os movimentos de Mensagem»)
# entra no formato com escolha, gerada por scripts/tarefas_escolha.py; o aquecimento é em cartões (CARTOES_NO_AQUECER).
CHOICE = ['m1-u1', 'm1-u2', 'm2-u1', 'm2-u2', 'm7-u3']
# 29/10/2026: na M7-U3 os cartões substituem as máquinas em papel, para caber nos 90 minutos: o cartão «Aquecer» liga à
# página tarefas/m7-u3/aquecimento/ e não há pergunta «aquecer». As citações do baralho conferem-se em
# tests/test_task_aquecimentos.py, contra as lições indicadas nos dados do aquecimento.
# 30/10/2026: aquecimento em cartões (decisão do docente)
CARTOES_NO_AQUECER = {'m1-u1', 'm1-u2', 'm7-u3'}
# Lições onde estão as passagens do aquecimento, por módulo (a lista do M2 fica como estava).
# 28/10/2026: no M1, as cantigas de D. Dinis e Guilhade (F04, F19) e o grito do cap. XII (F06).
WARM_LESSONS = {'m2': ('licao-m2-f02', 'licao-m2-f06', 'licao-m2-f07', 'licao-m2-f11'),
                'm1': ('licao-m1-f04', 'licao-m1-f06', 'licao-m1-f19'),
                # 29/10/2026: no M7, as lições da unidade 3 (o aquecimento em papel não tem passagens; fica para o caso).
                'm7': ('licao-m7-f07', 'licao-m7-f08', 'licao-m7-f09', 'licao-m7-f11')}


def flat(path):
    """Texto de uma página do sítio, sem marcas nem entidades, com os espaços juntos."""
    source = Path(path).read_text('utf-8')
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', source)))


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
                cartoes = slug in CARTOES_NO_AQUECER
                self.assertEqual(p.machines, [] if cartoes else ['1', '2'])
                self.assertEqual(p.themes, ['A', 'B'])
                self.assertEqual(len(re.findall(r'<li>', source.split('id="produzir"')[1].split('task-themes')[0])), 2)
                # 29/10/2026: com o aquecimento em cartões, o cartão «Aquecer» e o enunciado ligam à página dos cartões.
                aquecer = (('Aquecer em cartões', 'data-task-warm="cartoes"', '<p class="task-aquecer"><a href="aquecimento/">') if cartoes
                           else ('Descobre o que te pedem', 'Prova ou distração?', 'Verbos', 'Objeto', 'Condição'))
                for token in aquecer + ('Núcleo comum', 'Escolhe um tema',
                              'Dossiê do tema B', 'Tarefa individual', '90 min', 'consulta', 'Teams', 'duas linhas', 'tema que escolheste (A ou B)'):
                    self.assertIn(token, source)
                if cartoes:
                    self.assertEqual(source.count('<p class="task-aquecer"><a href="aquecimento/">'), 2)
                    self.assertTrue((ROOT / 'tarefas' / slug / 'aquecimento' / 'index.html').is_file())
                for token in ('task-clock', 'em grupo', 'rondas', '10/10/60/10', 'ficha', 'folha', '—', 'professor'):
                    self.assertNotIn(token, source)
                self.assertEqual(p.criteria, 3)
                self.assertLessEqual(len(' '.join(p.text['header'] + p.text['criteria']).split()), 300)
                # Uma pergunta de aquecimento e uma opcional; três opções, uma certa, explicações diferentes.
                # 29/10/2026: com o aquecimento em cartões, só a opcional.
                self.assertEqual(p.questions, [('1', True)] if cartoes else [('aquecer', False), ('1', True)])
                for q in (('1',) if cartoes else ('aquecer', '1')):
                    opts = [a for k, a in p.options if k == q]
                    self.assertEqual(len(opts), 3)
                    self.assertEqual(sum(a['data-correct'] == 'true' for a in opts), 1)
                    self.assertEqual(len({a['data-response'] for a in opts}), 3)
                # Relógio do aluno: aquecimento até 15 min, produção até 60 min.
                # 29/10/2026: com o aquecimento em cartões, até 10 min (os 90 minutos da aula: 10, 5, 60 e 10).
                self.assertIn(f'data-relogio data-max="{10 if cartoes else 15}" data-passo="1" data-rotulo="Aquecimento" data-chave="pt-relogio:tarefas/{slug}:aquecimento"', source)
                self.assertIn(f'data-relogio data-max="60" data-passo="5" data-rotulo="Produção em papel" data-chave="pt-relogio:tarefas/{slug}:producao"', source)
                self.assertLess(source.index('assets/relogio.js'), source.index('pt-lessons/casca.js'))
                # 28/10/2026 (revisão do PR #122): task-choice.css muda (impressão do aquecimento, letras no nome
                # acessível) e a versão passa a -2 nas quatro páginas.
                for asset in ('task-choice.css?v=20261028-escolha-2', 'task-reader.js?v=20261028-escolha-2', 'task-90.js?v=20261027-compact-1'):
                    self.assertIn(asset, source)
                # 28/10/2026 (revisão do PR #122): as letras das opções e dos temas ficam no nome acessível, porque as
                # instruções mandam escrevê-las no papel («Escreve a letra», «o tema que escolheste (A ou B)»).
                self.assertNotIn('aria-hidden="true">A</span>', source)
                self.assertEqual(len(re.findall(r'<span class="task-letter">[ABC]<span class="sr-only">:</span></span> ', source)), 3 if cartoes else 6)
                self.assertEqual(len(re.findall(r'<h3 id="tema-([AB])"><span><span class="sr-only">Tema </span>\1</span> ', source)), 2)
                self.assertIn('incluindo a síntese (as duas linhas finais)', source)

    def test_dossier_facts_carry_sources_and_links_exist(self):
        for slug in CHOICE:
            path = ROOT / 'tarefas' / slug / 'index.html'; source = path.read_text('utf-8'); p = Page(source)
            with self.subTest(task=slug):
                facts = re.findall(r'<section class="task-dossier".*?</section>', source, re.S)[0]
                self.assertGreaterEqual(facts.count('<li>'), 3)
                self.assertEqual(facts.count('<li>'), facts.count('class="task-fonte"'))
                lessons = [h for h in p.links if '/' + slug.split('-')[0] + '/licao-' in h]
                self.assertGreaterEqual(len(lessons), 4)
                for href in p.links:
                    url = urlsplit(href)
                    if url.scheme: continue
                    target = (path.parent / unquote(url.path)).resolve() if url.path else path
                    if target.is_dir(): target = target / 'index.html'
                    self.assertTrue(target.is_file(), href)

    def test_quotes_used_in_the_warmup_exist_in_the_lessons(self):
        for slug in CHOICE:
            module = slug.split('-')[0]
            lessons = ' '.join((ROOT / module / f / 'index.html').read_text('utf-8') for f in WARM_LESSONS[module])
            flat = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|\\n', ' ', lessons))
            source = (ROOT / 'tarefas' / slug / 'index.html').read_text('utf-8')
            warm = source.split('id="aquecer"')[1].split('</section>')[0]
            choices = ' '.join(re.findall(r'</span> (.*?)</button>', warm))
            for quote in re.findall(r'«([^»]+)»', choices):
                for verse in [v.strip() for v in quote.replace('&#x27;', "'").split(' / ')]:
                    with self.subTest(task=slug, verso=verse):
                        self.assertIn(re.sub(r'\s+', ' ', verse), flat)

    def test_dossier_quotes_and_numbers_are_in_the_lesson_they_point_to(self):
        # 28/10/2026: cada facto do dossiê está escrito na lição para onde aponta. Confere-se cada citação
        # entre «» e cada número (anos, quantidades) no texto da página ligada pela fonte do facto.
        for slug in CHOICE:
            path = ROOT / 'tarefas' / slug / 'index.html'; source = path.read_text('utf-8')
            dossier = re.findall(r'<section class="task-dossier".*?</section>', source, re.S)[0]
            facts = re.findall(r'<li>(.*?) <a class="task-fonte" href="([^"]+)"', dossier)
            self.assertEqual(len(facts), dossier.count('<li>'))
            for fact, href in facts:
                target = flat((path.parent / href / 'index.html').resolve())
                text = html.unescape(re.sub(r'<[^>]+>', '', fact))
                for piece in re.findall(r'«([^»]+)»', text) + re.findall(r'\b\d{3,4}\b', text):
                    with self.subTest(task=slug, fonte=href, facto=piece):
                        self.assertIn(piece, target)

    def test_support_names_are_the_names_in_the_linked_lessons(self):
        # 28/10/2026: «Relembrar» remete pelos nomes das secções e dos conceitos, entre «», tal como estão na
        # lição ligada (aspas interiores “ ” = « »). «Para ir mais longe» é o botão do motor das lições.
        engine = flat(ROOT / 'assets/pt-lessons/jogo.js')
        for slug in CHOICE:
            path = ROOT / 'tarefas' / slug / 'index.html'; source = path.read_text('utf-8')
            support = re.search(r'id="apoios".*?<ul>(.*?)</ul>', source, re.S)[1]
            items = re.findall(r'<li><a href="([^"]+)">(.*?)</a></li>', support)
            self.assertGreaterEqual(len(items), 3)
            for href, text in items:
                target = flat((path.parent / href / 'index.html').resolve())
                for name in re.findall(r'«([^»]+)»', text):
                    name = html.unescape(re.sub(r'<[^>]+>', '', name)).replace('“', '«').replace('”', '»')
                    with self.subTest(task=slug, licao=href, nome=name):
                        self.assertTrue(name in target or name in engine, name)

    def test_generated_pages_come_from_public_data_only(self):
        # 28/10/2026: as tarefas do M1 são geradas por scripts/tarefas_escolha.py; os dados guardam só o que a
        # página publica (sem grelha nem chave da correção) e o gerador é idempotente.
        data = sorted((ROOT / 'docs/pedagogia/tarefas-escolha').glob('*.json'))
        # 29/10/2026 (decisão do docente): junta-se a M7-U3, gerada pelo mesmo script.
        self.assertEqual([p.stem for p in data], ['m1-u1', 'm1-u2', 'm7-u3'])
        for p in data:
            d = json.loads(p.read_text('utf-8'))
            self.assertFalse({'grelha', 'provas', 'notas_docente', 'chave'} & set(d), p.name)
            self.assertIn(d['slug'], CHOICE)
        # 28/10/2026 (revisão do PR #122): gera numa pasta temporária (--saida) e compara byte a byte, sem
        # reescrever a árvore de quem corre os testes.
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, '-B', 'scripts/tarefas_escolha.py', '--saida', tmp], cwd=ROOT, check=True, capture_output=True)
            for p in data:
                slug = p.stem
                self.assertEqual((Path(tmp) / 'tarefas' / slug / 'index.html').read_bytes(),
                                 (ROOT / 'tarefas' / slug / 'index.html').read_bytes(), slug)

    def test_reader_puts_the_warmup_first(self):
        reader = (ROOT / 'assets/task-reader.js').read_text('utf-8')
        self.assertIn('node.id==="aquecer"?"Aquecer"', reader)
        self.assertIn('cards.unshift(cards.splice(warm,1)[0])', reader)
        self.assertNotIn('localStorage', reader)


if __name__ == '__main__':
    unittest.main()
