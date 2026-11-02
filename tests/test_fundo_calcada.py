"""02/11/2026: decisão 125 (docente). Fundo animado a traço «A calçada e o mar» na entrada do Português.

O desenho é decorativo (aria-hidden), está parado por omissão (sem JavaScript, com movimento reduzido e na projeção) e
não sai na impressão. As animações só existem dentro do bloco de movimento e fora da projeção.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text('utf-8')
CSS = (ROOT / 'assets/fundo-calcada.css').read_text('utf-8')
# 02/11/2026: decisão 137. O script próprio saiu: o movimento é do motor comum (assets/fundos.js e assets/fundos.css).
JS = (ROOT / 'assets/fundos.js').read_text('utf-8')
MOTOR_CSS = (ROOT / 'assets/fundos.css').read_text('utf-8')


class FundoCalcada(unittest.TestCase):
    def test_decorativo_dentro_do_cabecalho(self):
        # 02/11/2026: decisão 137. O cabeçalho leva a marca do motor comum (data-fundo e o ciclo de 16 s).
        self.assertIn('<header class="p-cab" data-fundo="cf" data-fundo-ciclo="16"><div class="cf-fundo" aria-hidden="true">', HTML)
        self.assertIn('<div class="cf-papel" aria-hidden="true"></div>', HTML)
        self.assertEqual(HTML.count('class="cf-fi"'), 7)
        self.assertNotIn('cf-anda', HTML, 'o movimento só se liga pelo script')
        # os nomes do desenho têm prefixo próprio: nenhum id do protótipo fica solto na página
        for ident in ('u0', 'u1', 'u2', 'd0', 'd1', 'd2'):
            self.assertNotIn(f'id="{ident}"', HTML)
            self.assertIn(f'id="cf-{ident}"', HTML)

    def test_credito_e_texto_inalterados(self):
        # 02/11/2026: decisão 137. O crédito leva o botão «Parar o desenho», escondido sem script (WCAG 2.2.2).
        self.assertIn('<p class="cf-credito">Desenho nosso, a traço, EPI, 2026, a partir do padrão de ondas da calçada portuguesa '
                      '(o «mar largo» do Rossio, Lisboa). <button type="button" class="fundo-botao" data-fundo-botao="cf" hidden>Parar o desenho</button></p>', HTML)
        self.assertIn('<h1 aria-label="Português">', HTML)
        self.assertIn('<p class="pt-entry-lead">Ler com atenção. Relacionar ideias. Experimentar outras vozes.</p></header>', HTML)
        self.assertIn('assets/fundo-calcada.css?v=', HTML)
        self.assertIn('assets/fundos.css?v=', HTML)
        self.assertIn('<script defer src="assets/fundos.js?v=', HTML)
        self.assertNotIn('fundo-calcada.js', HTML)

    def test_animacoes_so_no_bloco_de_movimento(self):
        bloco = CSS.index('@media(prefers-reduced-motion:no-preference){')
        fim = CSS.index('\n}', bloco)
        usos = list(re.finditer(r'animation(?:-name)?:\s*([\w-]+)', CSS))
        self.assertGreaterEqual(len(usos), 2)
        for uso in usos:
            self.assertTrue(bloco < uso.start() < fim, f'animação fora do bloco de movimento: {uso.group(0)}')
            linha = CSS[CSS.rindex('\n', 0, uso.start()):uso.start()]
            self.assertIn('html:not(.em-projecao)', linha)
        # 02/11/2026: decisão 137. A pausa fora do ecrã e com o separador escondido é a do motor comum.
        self.assertIn('[data-fundo].fundo-pausa *{animation-play-state:paused!important}', MOTOR_CSS)
        self.assertRegex(CSS, r'@media print\{[^@]*\.raiz \.cf-fundo,\.raiz \.cf-papel\{display:none\}\}')

    def test_script_respeita_projecao_e_movimento_reduzido(self):
        self.assertIn("matchMedia('(prefers-reduced-motion: no-preference)')", JS)
        # 02/11/2026: decisão 137. As mesmas condições, escritas no motor comum, que liga <prefixo>-anda (aqui cf-anda), pausa com o
        # separador escondido, pára ao fim de dois ciclos e desliga-se se a moldura de projeção marcar a página depois de carregar.
        self.assertIn('window.self !== window.top', JS)
        self.assertIn('projetar=1', JS)
        self.assertIn("classList.add(p + '-anda')", JS)
        self.assertIn('IntersectionObserver', JS)
        self.assertIn('visibilitychange', JS)
        self.assertIn('setTimeout(parar, 2 * ciclo)', JS)
        self.assertIn('epi-projection', JS)
        self.assertIn('MutationObserver', JS)
        self.assertNotRegex(JS, r'localStorage|sessionStorage')


if __name__ == '__main__':
    unittest.main()
