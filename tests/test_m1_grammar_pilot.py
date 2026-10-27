"""Literal authorization, card/progress continuity and actual formative quiz behavior."""
from pathlib import Path
import hashlib
import json
import re
import unittest

from test_m1_unit_tasks import TaskPage

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/fixtures/m1-grammar-pilot-edits-20261027.json'


def restore(source, edits):
    for edit in reversed(edits):
        if source.count(edit['new']) != edit['occurrences']:
            raise AssertionError('Literal edit missing or duplicated: ' + edit['location'])
        source = source.replace(edit['new'], edit['old'])
    return source


def cards(source):
    start = re.search(r'\bCARTOES\s*=\s*', source).end()
    return json.JSONDecoder().raw_decode(source[start:])[0]


def legacy(source):
    for match in re.finditer(r'\bvar E\s*=\s*', source):
        try:
            data = json.JSONDecoder().raw_decode(source[match.end():])[0]
        except ValueError:
            continue
        if isinstance(data, dict) and 'passos' in data:
            return data
    raise AssertionError('Legacy E.passos not found')


class M1GrammarPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text('utf-8'))

    def sources(self):
        for path, info in self.manifest['files'].items():
            after = (ROOT / path).read_text('utf-8')
            yield path, info, restore(after, info['edits']), after

    def test_exact_authorized_edits_restore_frozen_files_and_heads(self):
        expected = {'m1/licao-m1-f05/index.html', 'm1/gram-fonologia/index.html',
                    'tarefas/m1-u1/index.html', 'tarefas/m1-u2/index.html'}
        self.assertEqual(set(self.manifest['files']), expected)
        for path, info, before, after in self.sources():
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256(before.encode()).hexdigest(), info['before_sha256'])
                self.assertEqual(hashlib.sha256(after.encode()).hexdigest(), info['after_sha256'])
                self.assertEqual(before.split('</head>')[0], after.split('</head>')[0])
                forward = before
                for edit in info['edits']:
                    self.assertEqual(forward.count(edit['old']), edit['occurrences'])
                    forward = forward.replace(edit['old'], edit['new'])
                self.assertEqual(forward, after)

    def test_manifest_rejects_missing_or_duplicated_authorized_text(self):
        path, info, _, after = next(self.sources())
        edit = info['edits'][-1]
        with self.assertRaises(AssertionError):
            restore(after.replace(edit['new'], '', 1), info['edits'])
        with self.assertRaises(AssertionError):
            restore(after + edit['new'], info['edits'])

    def test_all_card_types_order_metadata_and_progress_keys_are_preserved(self):
        for path, _, before, after in self.sources():
            if path.startswith('tarefas/'):
                continue
            old = cards(before) if 'licao-' in path else legacy(before)['passos']
            new = cards(after) if 'licao-' in path else legacy(after)['passos']
            self.assertEqual(len(old), len(new))
            for previous, current in zip(old, new):
                for key in ('t', 'tipo', 'rot', 'g', 'conceito', 'mais', 'id', 'indice', 'nivel', 'c'):
                    self.assertEqual(previous.get(key), current.get(key), (path, key))
            for pattern in (r'\b(?:K|CH|ID)\s*=\s*"[^"]+"', r'versao:\s*"[^"]+"'):
                self.assertEqual(re.findall(pattern, before), re.findall(pattern, after))
            if 'gram-fonologia/' in path:
                previous, current = legacy(before), legacy(after)
                for key in set(previous) - {'passos'}:
                    self.assertEqual(previous[key], current[key], key)

    def test_schema_attempt_and_transfer_select_sounds_not_complete_etymologies(self):
        for path, _, _, source in self.sources():
            text = '\n'.join(c.get('html', '') for c in cards(source)) if 'licao-' in path else source
            for phrase in ('Sons e letras', 'PEP', 'ASA', 'humile', 'humilde', 'amare',
                           'scribere', 'alevantada', 'não representam necessariamente todas as etapas históricas'):
                self.assertIn(phrase, text, path)
            self.assertIn('minedu.gov.cv', text)
            self.assertIn('estudoautonomo.dge.mec.pt', text)
        lesson = cards((ROOT / 'm1/licao-m1-f05/index.html').read_text('utf-8'))
        self.assertIn('Tenta com apoio', lesson[5]['html'])
        self.assertIn('Experimenta outro caso', lesson[5]['html'])
        self.assertNotIn('Se fosse erro, cada um errava à sua maneira', lesson[20]['html'])
        self.assertNotIn('sempre da mesma maneira.', lesson[21]['html'])
        self.assertIn('só a vogal inserida', legacy((ROOT / 'm1/gram-fonologia/index.html').read_text('utf-8'))['passos'][3]['itens'][3][0])

    def test_four_mc_literary_transfer_and_time_are_preserved(self):
        for unit in (1, 2):
            text = (ROOT / f'tarefas/m1-u{unit}/index.html').read_text('utf-8')
            parsed = TaskPage(text)
            self.assertEqual(parsed.errors, [])
            self.assertEqual(len(parsed.questions), 4)
            for q in parsed.questions:
                self.assertEqual(len(q['options']), 3)
                self.assertEqual(sum(o['data-correct'] == 'true' for o in q['options']), 1)
            clock = re.search(r'<ol class="task-clock".*?</ol>', text, re.S)[0]
            self.assertEqual(re.findall(r'<b>(\d+) min</b>', clock), ['10', '10', '60', '10'])
            self.assertIn('nas mesmas folhas', text)
            self.assertIn('duas linhas', text)
        u1 = (ROOT / 'tarefas/m1-u1/index.html').read_text('utf-8')
        self.assertIn('confronto <i>mare</i>', u1)
        self.assertIn('Chega já', u1)
        self.assertIn('liga-a a uma passagem de A e a uma de C', u1)
        self.assertIn('até dois destes minutos', u1)
        u2 = (ROOT / 'tarefas/m1-u2/index.html').read_text('utf-8')
        self.assertIn('três destes quinze minutos', u2)
        self.assertIn('restantes doze minutos', u2)
        self.assertIn('Não és obrigado a usar esta fala', u2)
        self.assertIn('não alteres as palavras de uma fala documentada', u2)
        self.assertIn('fora da contagem da crónica', u2)


if __name__ == '__main__':
    unittest.main()
