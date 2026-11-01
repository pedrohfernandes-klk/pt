"""01/11/2026: contratos das novas lições, decisões 63 e 65."""
from collections import Counter
from itertools import groupby
from pathlib import Path
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from licoes_20261101 import LESSONS
from gerar_licoes_20261101 import render, sequences
from audit_cards import lesson_cards, validate_cards
from opcoes_equilibradas import avaliar


class NewLessons(unittest.TestCase):
    def test_generated_pages_match_reviewed_sources(self):
        units = sequences()
        for item in LESSONS:
            path = ROOT / item['id'].split('-')[0] / ('licao-' + item['id']) / 'index.html'
            with self.subTest(lesson=item['id']):
                self.assertEqual(path.read_text('utf-8'), render(item, units))
                self.assertEqual(lesson_cards(path), item['cards'])
                self.assertEqual(validate_cards(item['cards']), [])

    def test_fourteen_activities_five_nonwriting_types_and_feedback(self):
        for item in LESSONS:
            cards = [c for c in item['cards'] if c['t'] != 'ler']
            with self.subTest(lesson=item['id']):
                self.assertGreaterEqual(len(cards), 14)
                self.assertGreaterEqual(len({c['t'] for c in cards} - {'escrever', 'escrita'}), 5)
                self.assertLessEqual(sum(c['t'] in {'escrever','escrita'} for c in cards), 2)
                self.assertTrue(all(len(list(g)) <= 2 for _,g in groupby(c['t'] for c in cards)))
                self.assertTrue(all(len(c['f'].split()) >= 15 for c in cards))
                self.assertEqual(item['cards'][0]['rot'], 'Abre')
                self.assertEqual(item['cards'][-1]['rot'], 'Para levar')
                self.assertTrue(any(c.get('rot') == 'O essencial' for c in item['cards']))

    def test_balanced_choices_including_gaps(self):
        for item in LESSONS:
            questions = [dict(opcoes=q['o'], certa=q['c'], onde=str(i))
                         for i,c in enumerate(item['cards'])
                         for q in ([c] if c['t']=='escolha' else c.get('lacunas',[]))]
            with self.subTest(lesson=item['id']):
                self.assertEqual(avaliar(questions)['erros'], [])

    def test_language_and_explicit_provenance(self):
        for item in LESSONS:
            text = json.dumps(item['cards'], ensure_ascii=False)
            with self.subTest(lesson=item['id']):
                self.assertNotRegex(text, r'(?i)\b(?:professor|jogar|jogo|ficha|folha)\b')
                self.assertNotIn('—', text)
                self.assertNotIn('·', text)
                self.assertNotRegex(text, r'Qual (?:frase|palavra|citação|razão|texto)\b')
                self.assertIn('https://', text)

    def test_embedded_routes_match_the_visible_curriculum(self):
        # 01/11/2026: as aulas de tarefa leem também o contrato JSON de cada índice.
        plan=json.loads((ROOT/'docs/pedagogia/percursos-unidades-20261020.json').read_text('utf-8'))
        for module in {int(x['id'][1]) for x in LESSONS}:
            text=(ROOT/f'm{module}/index.html').read_text('utf-8')
            raw=re.search(r'<script[^>]+id="epi-unidades-pedagogicas"[^>]*>(.*?)</script>', text, re.S).group(1)
            embedded=json.loads(raw)
            for actual,expected in zip(embedded,plan[module-1]['units']):
                self.assertEqual(actual['lessons'],expected['lessons'])
                self.assertEqual(actual['steps'],expected['steps'])

    def test_attempt_arc_retrieval_and_proof(self):
        # 01/11/2026: conta a sequência efetiva e a produção oral, não só o banco automático.
        for item in LESSONS:
            self.assertEqual(item['tentativa'],dict(automaticas=14,producao_oral=1,escrita_livre=0,selecionadas=0,variantes_p2=0))
            self.assertTrue(item['cards'][1]['p'].startswith('Antes de reler.'))
            self.assertIn(item['question'],item['cards'][0]['html'])
            self.assertIn(item['question'],item['cards'][-1]['html'])
            self.assertIn('outra que a limite',item['cards'][-1]['html'])
            self.assertTrue(any('<details class="apoio">' in c.get('html','') for c in item['cards']))
            # 01/11/2026: a releitura é delimitada por alternativa, sem exigir a frase-molde retirada.
            for card in item['cards']:
                self.assertNotIn('confronta a pista com a tua resposta',card.get('f',''))
                if card['t']=='escolha':
                    self.assertEqual(len(card['fe']),len(card['o']))
                    self.assertEqual(len(set(card['fe'])),len(card['o']))
                    for i,feedback in enumerate(card['fe']):
                        self.assertGreaterEqual(len(feedback.split()),15)
                        if i!=card['c']:
                            self.assertRegex(feedback,r'Relê|Repara|Regressa|Confronta|Retoma|Volta|Confere|Compara|Mantém')
            values=[c['v'] for c in item['cards'] if c['t']=='vf']
            self.assertIn(True,values)
            self.assertIn(False,values)
        self.assertEqual(len({tuple(c['t'] for c in item['cards']) for item in LESSONS}),len(LESSONS))
        values=[c['v'] for item in LESSONS for c in item['cards'] if c['t']=='vf']
        self.assertLessEqual(abs(sum(values)-len(values)/2),2)

    def test_george_quote_and_credit(self):
        item = next(x for x in LESSONS if x['id']=='m8-f16')
        quote = re.search(r'<blockquote[^>]*>«(.*?)»</blockquote>', next(c['html'] for c in item['cards'] if 'Europa-América, 1995' in c.get('html',''))).group(1)
        self.assertEqual(len(quote.split()), 25)
        self.assertEqual(quote, 'À sua frente uma senhora de idade, primeiro esboçada, finalmente completa, olha-a atentamente. De idade não, George detesta eufemismos, mesmo só pensados, uma mulher velha.')
        self.assertIn('Europa-América, 1995', next(c['html'] for c in item['cards'] if 'Europa-América, 1995' in c.get('html','')))
        self.assertIn('não indica a página da edição', next(c['html'] for c in item['cards'] if 'Europa-América, 1995' in c.get('html','')))

    def test_protected_poems_quote_at_most_four_lines(self):
        for id in ('m8-f13','m8-f14'):
            item=next(x for x in LESSONS if x['id']==id)
            quotes=[q for c in item['cards'] for q in re.findall(r'<blockquote>(.*?)</blockquote>',c.get('html',''))]
            self.assertEqual(len(quotes),1)
            self.assertLessEqual(quotes[0].count('<br>')+1,4)


if __name__ == '__main__':
    unittest.main()
