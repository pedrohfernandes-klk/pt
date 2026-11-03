"""02/11/2026: F0, preservação de progresso no Chromium, sem páginas publicadas novas."""
import json
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class Acrescentos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.route('http://acrescentos.test/**', lambda route: route.fulfill(body='<html><body></body></html>', content_type='text/html'))
        self.page.goto('http://acrescentos.test/')
        self.page.add_script_tag(path=str(ROOT/'assets/pt-lessons/acrescentos.js'))

    def tearDown(self):
        self.context.close()

    def run_js(self, js):
        return self.page.evaluate(js)

    def test_sem_progresso_marca_sem_criar_estado(self):
        self.assertEqual(self.run_js("EPIAcrescentos.aplicar(localStorage,'licao-m4-f01','l1',[2,5]).estado"), 'marcado')
        self.assertIsNone(self.run_js("localStorage.getItem('licao-m4-f01')"))
        self.assertEqual(self.run_js("JSON.parse(localStorage.getItem('licao-m4-f01-acrescentos'))"), ['l1'])

    def test_primeira_tentativa_e_recarregamento_nao_remapeiam_indices_novos(self):
        self.run_js("EPIAcrescentos.aplicar(localStorage,'K','l1',[2]);localStorage.setItem('K',JSON.stringify({versao:'v',tentativas:1,exposicoes:{2:1,3:2},ult:'2,3'}))")
        before = self.run_js("localStorage.getItem('K')")
        self.page.reload()
        self.page.add_script_tag(path=str(ROOT/'assets/pt-lessons/acrescentos.js'))
        self.run_js("EPIAcrescentos.aplicar(localStorage,'K','l1',[2])")
        self.assertEqual(self.run_js("localStorage.getItem('K')"), before)

    def test_dois_lotes_idempotencia_versao_e_campos_intactos(self):
        original = {'versao':'m4-f01-v3','lida':True,'melhor':7,'totalMelhor':9,'tentativas':4,'xp':125,'mais':{'feito':True},'banco':'preservado','exposicoes':{'0':4,'2':3,'8':2},'ult':'0,2,8'}
        self.run_js("localStorage.setItem('K'," + json.dumps(json.dumps(original)) + ")")
        self.run_js("EPIAcrescentos.aplicar(localStorage,'K','l1',[2,5]);EPIAcrescentos.aplicar(localStorage,'K','l2',[1])")
        final = self.run_js("JSON.parse(localStorage.getItem('K'))")
        self.assertEqual(final['exposicoes'], {'0':4,'4':3,'11':2})
        self.assertEqual(final['ult'], '0,11,4')  # O motor ordena texto, não números.
        for k in original.keys() - {'exposicoes','ult'}:
            self.assertEqual(final[k], original[k], k)
        self.run_js("EPIAcrescentos.aplicar(localStorage,'K','l1',[2,5]);EPIAcrescentos.aplicar(localStorage,'K','l2',[1])")
        self.assertEqual(self.run_js("JSON.parse(localStorage.getItem('K'))"), final)

    def test_migracoes_m2_correm_antes_do_acrescento(self):
        # 02/11/2026: no banco F06, o antigo 9 está na posição 15; com a inserção em 1, fica em 16.
        for lesson, old, expected in [('06',9,16),('07',3,7)]:
            with self.subTest(lesson=lesson):
                key=f'licao-m2-f{lesson}'
                self.run_js(f"localStorage.setItem('{key}',JSON.stringify({{tentativas:1,lida:true,melhor:6,exposicoes:{{'{old}':3}},ult:'{old}'}}))")
                migration=ROOT/f'assets/pt-lessons/m2-f{lesson}-bank-migration.js'
                self.page.add_script_tag(path=str(migration))
                self.run_js(f"EPIAcrescentos.aplicar(localStorage,'{key}','novo',[1])")
                state=self.run_js(f"JSON.parse(localStorage.getItem('{key}'))")
                self.assertEqual(state['exposicoes'], {str(expected):3})
                self.assertEqual(state['ult'], str(expected))
                self.assertTrue(state['lida'])
                self.assertEqual(state['melhor'],6)
                self.assertEqual(state['banco'],f'm2-f{lesson}-20261021')

    def test_importacao_antiga_retira_so_indices_incompativeis(self):
        got=self.run_js("EPIAcrescentos.protegerImportacao({lida:true,melhor:8,tentativas:3,exposicoes:{1:2},ult:'1'},'[\"l1\"]',null)")
        self.assertEqual(got, {'lida':True,'melhor':8,'tentativas':3})
        same=self.run_js("EPIAcrescentos.protegerImportacao({exposicoes:{1:2},ult:'1'},'[\"l1\"]','[\"l1\"]')")
        self.assertEqual(same, {'exposicoes':{'1':2},'ult':'1'})

    def test_projecao_nao_le_nem_escreve(self):
        self.assertEqual(self.run_js("EPIAcrescentos.aplicar({getItem(){throw Error('leu')},setItem(){throw Error('escreveu')}},'K','l1',[1],true).estado"), 'projecao')
        self.assertEqual(self.run_js('localStorage.length'),0)

    def test_registo_invalido_nao_e_apagado(self):
        self.run_js("localStorage.setItem('K','invalido')")
        self.assertEqual(self.run_js("EPIAcrescentos.aplicar(localStorage,'K','l1',[1]).estado"), 'indisponivel')
        self.assertEqual(self.run_js("localStorage.getItem('K')"), 'invalido')
        self.assertIsNone(self.run_js("localStorage.getItem('K-acrescentos')"))

    def test_falha_na_escrita_reverte_marca(self):
        self.assertEqual(self.run_js("""() => {
          const m = new Map([['K',JSON.stringify({tentativas:1,ult:'2'})]]);
          const s = {getItem:k=>m.has(k)?m.get(k):null,removeItem:k=>m.delete(k),setItem(k,v){if(k==='K')throw Error('quota');m.set(k,v)}};
          const r = EPIAcrescentos.aplicar(s,'K','l1',[1]);
          return [r.estado,m.get('K'),m.has('K-acrescentos')];
        }"""), ['indisponivel','{"tentativas":1,"ult":"2"}',False])


if __name__ == '__main__':
    unittest.main()
