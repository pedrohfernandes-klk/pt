"""Vídeos escolhidos (28/10/2026) nas lições do Português: no fim de cartões que já existiam."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import videos_escolhidos_pt as ve  # noqa: E402

DADOS = json.loads(ve.DADOS.read_text('utf-8'))


class VideosEscolhidosPt(unittest.TestCase):
    def test_escrita(self):
        self.assertEqual(ve.verificar(DADOS)[0], [])

    def test_aplicado_e_idempotente(self):
        r = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'videos_escolhidos_pt.py'), '--verificar'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_indices_e_restantes_cartoes_iguais(self):
        # Os painéis apontam para os cartões pela posição: nenhum cartão entra, sai ou muda de lugar,
        # e o cartão escolhido só ganha o bloco do vídeo no fim.
        for pagina, vs in ve.verificar(DADOS)[1].items():
            r = subprocess.run(['git', 'show', 'origin/main:' + pagina], cwd=ROOT, capture_output=True, text=True)
            if r.returncode:
                self.skipTest('sem origin/main local')
            antes = [o for o, _, _ in ve.cartoes(r.stdout)]
            depois = [o for o, _, _ in ve.cartoes((ROOT / pagina).read_text('utf-8'))]
            self.assertEqual(len(antes), len(depois), pagina)
            for a, d in zip(antes, depois):
                if a == d:
                    continue
                self.assertEqual({k: v for k, v in a.items() if k != 'html'}, {k: v for k, v in d.items() if k != 'html'})
                self.assertTrue(d['html'].startswith(a['html']), pagina)
                extra = d['html'][len(a['html']):]
                self.assertTrue(all('data-pv="%s"' % v['id'] in extra for v in vs if ('data-pv="%s"' % v['id']) in d['html']))
            self.assertEqual(sum(a != d for a, d in zip(antes, depois)), len(vs), pagina)

    def test_leitor_carregado_e_so_ao_toque(self):
        for v in DADOS['videos']:
            s = (ROOT / v['pagina']).read_text('utf-8')
            self.assertEqual(s.count('data-pv=\\"%s\\"' % v['id']) + s.count('data-pv="%s"' % v['id']), 1, v['id'])
            self.assertIn('assets/pt-lessons/video-youtube.js', s)
            self.assertFalse(any('<iframe' in o.get('html', '') for o, _, _ in ve.cartoes(s)), v['id'])

    def test_no_maximo_dois_videos_por_licao(self):
        for pagina in ve.verificar(DADOS)[1]:
            itens = [o for o, _, _ in ve.cartoes((ROOT / pagina).read_text('utf-8'))]
            n = sum(o.get('html', '').count('data-yt=') for o in itens)
            self.assertLessEqual(n, 2, pagina)


if __name__ == '__main__':
    unittest.main()
