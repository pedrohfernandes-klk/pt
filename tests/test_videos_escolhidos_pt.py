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
        # 28/10/2026: compara com o baralho registado nos dados (cartoes, indice) e já não com origin/main,
        # que passa a ter os vídeos depois da fusão.
        for v in DADOS['videos']:
            itens = [o for o, _, _ in ve.cartoes((ROOT / v['pagina']).read_text('utf-8'))]
            self.assertEqual(len(itens), v['cartoes'], v['id'])
            com = [i for i, o in enumerate(itens) if ('data-pv="%s"' % v['id']) in o.get('html', '')]
            self.assertEqual(com, [v['indice']], v['id'])
            html = itens[v['indice']]['html']
            self.assertTrue(html.endswith('</div>') and html.rfind('<div class="yt" data-pv="%s"' % v['id']) > 0, v['id'])
            (campo, valor), = v['cartao'].items()
            self.assertEqual(itens[v['indice']].get(campo), valor, v['id'])

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
