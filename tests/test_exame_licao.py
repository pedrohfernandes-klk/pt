"""05/11/2026: pedido do docente sobre o Laboratório do exame: «isto n é uma leitura, é uma lição, e são duas coisas
diferentes». Cada sessão aponta para uma lição do módulo; a ligação, as notas e as fases dizem «lição» e «texto»,
nunca «leitura de apoio» nem «recorte de leitura»."""
from pathlib import Path
import json, re, unittest

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'assets/exame/app.js').read_text('utf-8')
DADOS = json.loads((ROOT / 'assets/exame/sessoes.json').read_text('utf-8'))


class ExameLicao(unittest.TestCase):
    def test_a_ligacao_diz_licao(self):
        self.assertIn("link({label:'Abrir a lição ↗',url:s.source.url})", APP)
        self.assertNotIn('leitura de apoio', APP)
        self.assertIn('<summary>Consultar o texto</summary>', APP)

    def test_notas_sem_leitura_de_apoio(self):
        for s in DADOS['sessions']:
            nota = s['source'].get('note', '')
            with self.subTest(sessao=s['id']):
                self.assertNotRegex(nota, r'(?i)leitura de apoio|recorte de leitura')
                if not s['source'].get('original'):
                    # A ligação de cada sessão é uma lição do Português.
                    self.assertRegex(s['source']['url'], r'^/pt/m\d/licao-m\d-f\d+/$')

    def test_a_versao_do_app_mudou(self):
        html = (ROOT / 'exame/index.html').read_text('utf-8')
        self.assertIn('../assets/exame/app.js?v=20261105-licao-1', html)


if __name__ == '__main__':
    unittest.main()
