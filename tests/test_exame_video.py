"""The optional video session must work without a teacher or a video player."""
from pathlib import Path
import json, re, unittest

ROOT = Path(__file__).resolve().parents[1]

class ExamVideo(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf8'))
        self.session = next(s for s in self.data['sessions'] if s['id'] == 's27')

    def test_duration_comprehension_and_writing(self):
        s = self.session
        self.assertEqual(s['durationMinutes'], 45)
        self.assertEqual(5+8+s['writing']['minutes']+(27-s['writing']['minutes'])+5, 45)
        self.assertEqual(s['writing']['minutes'], 15)
        self.assertEqual(len(s['video']['questions']), 4)
        all_questions = s['warmup']+s['video']['questions']+[s['correction']['check']]
        self.assertEqual(len({q['id'] for q in all_questions}), len(all_questions))
        for q in all_questions:
            self.assertIn(q['answer'], range(len(q['options'])))
            self.assertEqual(len(set(q['options'])), len(q['options']))
            self.assertTrue(q['feedback'])

    def test_clips_use_verified_windows_without_promotional_tail(self):
        v = self.session['video']
        self.assertEqual(v['author'], 'Academia X')
        self.assertEqual(v['duration'], '48:52')
        self.assertEqual([(c['start'],c['end']) for c in v['clips']], [(1638,1703),(1744,1812)])
        for clip in v['clips']:
            self.assertRegex(clip['id'], r'^[A-Za-z0-9_-]{11}$')
            self.assertLess(clip['end'], 30*60+12+1)
        self.assertLess(sum(c['end']-c['start'] for c in v['clips']), 3*60)

    def test_independent_text_route_and_correction(self):
        s = self.session
        self.assertGreater(len(s['video']['fallback'].split()), 40)
        self.assertIn('individualmente', s['video']['intro'])
        self.assertIs(s['video']['embeddable'], False)
        self.assertIn('não permite', s['video']['playbackNote'])
        self.assertIn('Inês', s['source']['excerpt'])
        self.assertIn('Rui', s['source']['excerpt'])
        self.assertIn('Inês', s['correction']['model'])
        self.assertIn('Rui', s['correction']['model'])
        self.assertNotRegex(json.dumps(s,ensure_ascii=False), r'(?i)em salas|formem grupos|o professor dará')

    def test_player_is_loaded_only_on_request_and_keeps_accessible_fallback(self):
        js = (ROOT/'assets/exame/app.js').read_text('utf8')
        self.assertIn('data-video-slot', js)
        self.assertIn("document.createElement('iframe')", js)
        self.assertIn('www.youtube-nocookie.com/embed/', js)
        self.assertIn('f.title=c.label', js)
        self.assertIn('f.allowFullscreen=true', js)
        self.assertNotIn('autoplay=1', js)
        self.assertIn('session.video.questions', js)
        self.assertIn('video-fallback', js)
        self.assertIn('v.embeddable===false', js)
        self.assertIn('Abrir este trecho no YouTube', js)
        self.assertIn('Controla o ritmo ou acompanha a projeção', js)
        css = (ROOT/'assets/exame/exame.css').read_text('utf8')
        self.assertIn('aspect-ratio:16/9',css)

if __name__ == '__main__': unittest.main()
