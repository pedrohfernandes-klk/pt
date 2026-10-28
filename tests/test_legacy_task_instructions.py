"""Legacy closure UX changes are narrow, reversible and independent of literature."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import unittest
from test_task_routes_closure import original_lesson_text

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'tests/fixtures/task-instruction-edits-20261026.json'


class Text(HTMLParser):
    def __init__(self,source):
        super().__init__();self.skip=0;self.parts=[];self.feed(source)
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']:self.skip+=1
    def handle_endtag(self,tag):
        if tag in ['script','style']:self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)


class LegacyTaskInstructions(unittest.TestCase):
    def test_exact_manifest_reverses_only_nine_ux_strings(self):
        manifest=json.loads(MANIFEST.read_text('utf-8'))
        self.assertEqual(set(manifest['files']),{
            'm1/licao-m1-f11/index.html','m4/licao-m4-f10/index.html','m4/licao-m4-f11/index.html'})
        self.assertEqual(sum(len(item['edits']) for item in manifest['files'].values()),9)
        original=json.loads((ROOT/'tests/fixtures/task-route-lesson-content-before.json').read_text('utf-8'))
        for path,item in manifest['files'].items():
            with self.subTest(path=path):
                frozen=next(module['files'][path] for module in original.values() if path in module['files'])
                self.assertEqual(item['base_sha256_lf'],frozen)
                self.assertEqual(hashlib.sha256(original_lesson_text(path).encode()).hexdigest(),frozen)
                current=(ROOT/path).read_text('utf-8')
                for edit in item['edits']:
                    self.assertEqual(current.count(edit['new']),edit['occurrences'])
                    self.assertNotIn(edit['old'],current)

    def test_short_opening_promises_no_independent_checkpoint(self):
        endings={
            'm1/licao-m1-f11/index.html':'Preparação para a Tarefa da Unidade 2.',
            'm4/licao-m4-f10/index.html':'Preparação para a Tarefa da Unidade 1.',
            'm4/licao-m4-f11/index.html':'Preparação para a Tarefa da Unidade 3: Discurso no abrigo.'}
        for path,ending in endings.items():
            source=(ROOT/path).read_text('utf-8')
            start=re.search(r'"aula":\{"linha":"([^"]+)"',source)[1]
            self.assertTrue(start.endswith(ending))
            self.assertLess(len(start),180)
            for retired in ['desafio','Teams','fotograf','síntese']:
                self.assertNotIn(retired,start)

    def test_maps_and_portfolios_have_no_extra_closure_gate(self):
        # 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 passa ao mesmo modelo, com duas aulas de tarefa.
        for module in ['m1','m2','m4','m7']:
            for slug in [f'mapa-do-modulo-{module}',f'portefolio-do-modulo-{module}']:
                source=(ROOT/module/slug/'index.html').read_text('utf-8')
                text=' '.join(' '.join(Text(source).parts).split())
                with self.subTest(module=module,slug=slug):
                    self.assertNotIn('Cada unidade termina com um desafio',text)
                    self.assertNotIn('Desafio e síntese no fim da unidade',text)
                    self.assertNotIn('desafios de unidade',text)
                    self.assertNotIn('copiado da página do percurso',text)
                    self.assertNotIn('Copias o cartão do percurso',text)
                    self.assertNotIn('Síntese oral ou no caderno, com duas passagens',text)
                    self.assertIn('aula de tarefa',text)
                    if slug.startswith('portefolio'):
                        self.assertIn('Registo anterior, facultativo.',text)
                        self.assertIn('mantêm-se os parâmetros e as ponderações',text)

    def test_teacher_guides_reuse_preparation_not_a_second_delivery(self):
        files=['m1/aulas/aula-06/index.html','m1/aulas/aula-14/index.html',
               'm4/aulas/aula-08/index.html','m4/aulas/aula-15/index.html','m4/aulas/aula-18/index.html']
        for file in files:
            source=(ROOT/file).read_text('utf-8')
            with self.subTest(file=file):
                for retired in ['<small>Desafio da unidade','<small>Síntese da unidade',
                                'registar a síntese','marcar a síntese','Quem não passar repete em casa',
                                'o desafio e a síntese','sem telemóvel']:
                    self.assertNotIn(retired,source)
                self.assertIn('Preparação que se recupera',source)
                self.assertIn('sem nova entrega obrigatória',source)
                self.assertIn('O fecho e a síntese integram a aula de tarefa.',source)
                self.assertIn('class="disc"',source)
                self.assertIn('Critérios',source)

    def test_teacher_questions_and_rubrics_are_frozen(self):
        manifest=json.loads(MANIFEST.read_text('utf-8'))
        for file,expected in manifest['teacher_content'].items():
            source=(ROOT/file).read_text('utf-8')
            values={
                'questions':re.findall(r'<p class="p">.*?</p>',source,re.S),
                'rubrics':re.findall(r'<p class="rot" style="margin-top:6px">Critérios</p><ul>.*?</ul>',source,re.S)}
            for kind,texts in values.items():
                self.assertEqual(hashlib.sha256(json.dumps(texts,ensure_ascii=False).encode()).hexdigest(),expected[kind],(file,kind))


if __name__=='__main__':unittest.main()
