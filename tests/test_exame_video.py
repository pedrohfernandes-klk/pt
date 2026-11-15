"""The optional video session must work without a teacher or a video player.

15/11/2026: revisão geral (camada revisao_geral_20261115; decisão do utilizador: só vídeos oficiais): a sessão 27 perde a masterclass da
«Academia X» (canal privado, que não permitia a reprodução noutros sites), com os dois trechos e as perguntas s27-video1 a s27-video4, e
fica com a alternativa em texto, que já fazia a sessão sem sair da página: o antigo video.fallback, palavra por palavra, abre o contexto
do texto. Este teste passa a conferir que nenhuma sessão tem vídeo, que a s27 se faz só com o texto (o mesmo tempo, a mesma escrita e a
mesma correção) e que o motor continua a tratar o vídeo como opcional (o caminho do leitor fica no app.js, só a pedido).
"""
from pathlib import Path
import json, re, unittest

ROOT = Path(__file__).resolve().parents[1]

class ExamVideo(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'assets/exame/sessoes.json').read_text('utf8'))
        self.session = next(s for s in self.data['sessions'] if s['id'] == 's27')

    def test_duration_comprehension_and_writing(self):
        s = self.session
        # 01/11/2026: dez minutos de aquecimento, preservando leitura e escrita.
        self.assertEqual(s['durationMinutes'], 50)
        self.assertEqual(10+8+s['writing']['minutes']+(27-s['writing']['minutes'])+5, 50)
        self.assertEqual(s['writing']['minutes'], 15)
        # 15/11/2026: sem o vídeo, a fase 2 é a de todas as sessões («Ler»), com os mesmos 8 minutos; as perguntas são as do
        # aquecimento e a da correção.
        self.assertNotIn('video', s)
        all_questions = s['warmup']+[s['correction']['check']]
        self.assertEqual(len(all_questions), 4)
        self.assertEqual(len({q['id'] for q in all_questions}), len(all_questions))
        for q in all_questions:
            self.assertIn(q['answer'], range(len(q['options'])))
            self.assertEqual(len(set(q['options'])), len(q['options']))
            self.assertTrue(q['feedback'])

    def test_no_session_keeps_a_video_from_a_private_channel(self):
        # 15/11/2026: substitui a conferência das janelas dos trechos (27:18 a 28:23 e 29:04 a 30:12 da masterclass), que saíram com ela.
        self.assertFalse([s['id'] for s in self.data['sessions'] if 'video' in s])
        texto = (ROOT/'assets/exame/sessoes.json').read_text('utf8')
        for velho in ('Academia X', 'Xzst0nmqtFE', 'Masterclass', 'youtube.com', 's27-video'):
            self.assertNotIn(velho, texto)
        self.assertNotIn('vídeo', self.session['tags'])
        self.assertNotIn('compreensão oral', self.session['tags'])

    def test_independent_text_route_and_correction(self):
        s = self.session
        # 15/11/2026: a alternativa em texto (mais de 40 palavras) abre o contexto, antes dos dois casos; é a única rota da sessão.
        contexto = s['source']['context']
        self.assertTrue(contexto.startswith('Uma explicação pode ser seguida de exercícios sobre o conteúdo revisto'))
        self.assertTrue(contexto.endswith('Lê os dois casos. O que permite verificar a aprendizagem de cada aluno?'))
        self.assertGreater(len(contexto.split()), 40 + 12)
        self.assertIn('«Programa e fontes»', s['source']['note'])
        self.assertIn('Inês', s['source']['excerpt'])
        self.assertIn('Rui', s['source']['excerpt'])
        self.assertIn('Inês', s['correction']['model'])
        self.assertIn('Rui', s['correction']['model'])
        self.assertNotRegex(json.dumps(s,ensure_ascii=False), r'(?i)em salas|formem grupos|o professor dará|trechos')

    def test_player_is_loaded_only_on_request_and_keeps_accessible_fallback(self):
        # 15/11/2026: o motor fica igual: o vídeo é opcional (as sessões sem «video» seguem a fase «Ler») e o leitor, se uma sessão
        # voltar a ter um vídeo oficial, só se carrega a pedido.
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
        self.assertIn('if(phase===1&&session.video)return videoLesson();', js)
        # 27/10/2026 (pedido do docente): o relógio da fase passa a ser o relógio do aluno (assets/relogio.js).
        self.assertIn('EPIRelogio.criar(host,{max:duration(session,phase)/60', js)
        css = (ROOT/'assets/exame/exame.css').read_text('utf8')
        self.assertIn('aspect-ratio:16/9',css)

if __name__ == '__main__': unittest.main()
