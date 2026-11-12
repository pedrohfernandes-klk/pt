"""05/11/2026: pedido do docente sobre o Laboratório do exame: «isto n é uma leitura, é uma lição, e são duas coisas
diferentes». Cada sessão aponta para uma lição do módulo; a ligação, as notas e as fases dizem «lição» e «texto»,
nunca «leitura de apoio» nem «recorte de leitura».

05/11/2026: camada exame_contexto_20261105, por cima: o texto de contexto de cada sessão (o parágrafo que app.js mostra
por cima do texto) também fala da lição e do excerto, nunca de uma «leitura de apoio» nem de um «recorte»."""
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
        # 05/11/2026: a camada do contexto (exame_contexto_20261105) muda sessoes.json; a versão do app.js, que também
        # refresca sessoes.json, passa a licao-2, e a licao-1 já não pode aparecer.
        self.assertIn('../assets/exame/app.js?v=20261105-licao-2', html)
        self.assertNotIn('app.js?v=20261105-licao-1', html)

    # 05/11/2026: o contexto de cada sessão (camada exame_contexto_20261105). Nenhum «context» nem «note» de
    # sessoes.json fala de «leitura de apoio» (nem no plural) ou de «recorte»; as 16 frases novas estão lá.
    def test_contexto_e_notas_sem_leitura_de_apoio_nem_recorte(self):
        for s in DADOS['sessions']:
            for campo in ('context', 'note'):
                with self.subTest(sessao=s['id'], campo=campo):
                    self.assertNotRegex(s['source'].get(campo, ''), r'(?i)leituras? de apoio|recort')

    def test_as_16_frases_novas_do_contexto(self):
        frase = ('Abre a lição, lê o excerto indicado e identifica duas marcas relevantes antes de responder. '
                 'O texto completo está na lição; esta sessão organiza o treino a partir dele.')
        com_frase = [s['id'] for s in DADOS['sessions'] if s['source'].get('context') == frase]
        self.assertEqual(len(com_frase), 16, com_frase)
        self.assertEqual((ROOT / 'assets/exame/sessoes.json').read_text('utf-8').count(frase), 16)
        for s in DADOS['sessions']:
            if s['id'] in com_frase:
                with self.subTest(sessao=s['id']):
                    # A frase manda abrir a lição: a ligação da sessão é uma lição do Português.
                    self.assertRegex(s['source']['url'], r'^/pt/m\d/licao-m\d-f\d+/$')
        contexto = {s['id']: s['source'].get('context', '') for s in DADOS['sessions']}
        # 12/11/2026: decisão 152 no Exame (camada cuidado_exame_20261112, achado 73): «D. Dinis» não se parte (U+00A0); a frase é a
        # mesma, letra a letra, com esse espaço preso, e a forma com o espaço normal já não pode aparecer.
        self.assertIn('O excerto de D.\xa0Dinis serve a pergunta sobre «vos».', contexto['s01'])
        self.assertNotIn('O excerto de D. Dinis', contexto['s01'])
        self.assertIn('nas duas lições de apoio.', contexto['s03'])
        self.assertTrue(contexto['s11'].startswith('O excerto apresenta «Noite Fechada».'), contexto['s11'])


if __name__ == '__main__':
    unittest.main()
