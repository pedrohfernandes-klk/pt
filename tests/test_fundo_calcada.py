"""02/11/2026: decisão 125 (docente). Fundo animado a traço «A calçada e o mar» na entrada do Português.

02/11/2026: decisão 139 (docente: «maiores e mais bem feitos; a calçada tem de parecer realmente calçada»). O desenho a traço
sai; entra, por baixo do nome, a faixa da calçada «mar largo» (assets/calcada-mar.svg, gerada por scripts/gerar_calcada_mar.py),
com o mesmo motor comum e o mesmo botão. A camada literal é scripts/calcada_mar_20261102.json.

O desenho é decorativo (aria-hidden), está parado por omissão (sem JavaScript, com movimento reduzido e na projeção) e
não sai na impressão. As animações só existem dentro do bloco de movimento e fora da projeção.
"""
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text('utf-8')
CSS = (ROOT / 'assets/fundo-calcada.css').read_text('utf-8')
# 02/11/2026: decisão 137. O script próprio saiu: o movimento é do motor comum (assets/fundos.js e assets/fundos.css).
JS = (ROOT / 'assets/fundos.js').read_text('utf-8')
MOTOR_CSS = (ROOT / 'assets/fundos.css').read_text('utf-8')


class FundoCalcada(unittest.TestCase):
    def test_decorativo_dentro_do_cabecalho(self):
        # 02/11/2026: decisão 137. O cabeçalho leva a marca do motor comum (data-fundo e o ciclo, agora de 40 s).
        # 02/11/2026: decisão 139. A faixa da calçada fica no cabeçalho, depois do texto, decorativa (aria-hidden), uma só vez;
        # o desenho a traço (fiadas em SVG, pedras soltas e a folha da entrada) sai por inteiro, com os seus ids.
        self.assertIn('<header class="p-cab" data-fundo="cf" data-fundo-ciclo="40"><p class="p-etiqueta', HTML)
        self.assertIn('Experimentar outras vozes.</p><div class="cf-mar" aria-hidden="true"><div class="cf-pedras"></div></div></header>', HTML)
        self.assertEqual(HTML.count('class="cf-mar"'), 1)
        self.assertEqual(HTML.count('data-fundo="cf"'), 1)
        self.assertNotIn('cf-anda', HTML, 'o movimento só se liga pelo script')
        for antigo in ('cf-fundo', 'cf-papel', 'cf-fi', 'cf-cena', 'cf-soltas', 'id="cf-'):
            self.assertNotIn(antigo, HTML)
        for ident in ('u0', 'u1', 'u2', 'd0', 'd1', 'd2'):
            self.assertNotIn(f'id="{ident}"', HTML)

    def test_calcada_gerada_e_conferida(self):
        # 02/11/2026: decisão 139. O ficheiro corresponde ao gerador (semente fixa), é um SVG simples, sem scripts nem
        # ligações para fora, e o ladrilho (960 × 440) é o que o CSS repete e faz andar: um ciclo anda exatamente um ladrilho.
        r = subprocess.run([sys.executable, 'scripts/gerar_calcada_mar.py', '--verificar'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        svg = (ROOT / 'assets/calcada-mar.svg').read_text('utf-8')
        self.assertTrue(svg.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 440"'))
        for proibido in ('<script', 'href=', 'url(', '<image', 'on'):
            if proibido == 'on':
                self.assertNotRegex(svg, r'\son\w+=')
            else:
                self.assertNotIn(proibido, svg)
        self.assertLess(len(svg.encode()), 120_000)
        self.assertIn('--cf-tw:calc(var(--cf-h) * 960 / 440)', CSS)
        self.assertIn('background:url(calcada-mar.svg) repeat-x 0 0/var(--cf-tw) 100%', CSS)
        self.assertIn('@keyframes cf-mar{from{transform:translateX(0)}to{transform:translateX(calc(-1 * var(--cf-tw)))}}', CSS)

    def test_credito_e_texto_inalterados(self):
        # 02/11/2026: decisão 137. O crédito leva o botão «Parar o desenho», escondido sem script (WCAG 2.2.2).
        # 02/11/2026: nova instrução editorial do docente, crédito explícito de IA sem atribuição manual.
        # 07/11/2026: decisões 153, 176 e 177 (pedido pt-1). O crédito passa para o «i»; continua a exigir o texto completo, letra a
        # letra, agora dentro de details.info-i, e o botão de parar fora dela, na .fundo-acoes (sempre à vista), com o texto novo
        # «Parar a animação» (decisão 177) e escondido sem script (WCAG 2.2.2).
        self.assertIn('<div class="fundo-acoes cf-credito"><button type="button" class="fundo-botao" data-fundo-botao="cf" hidden>Parar a animação'
                      '</button><details class="info-i info-i--linha" name="info-i"><summary aria-label="Créditos do desenho"><span '
                      'aria-hidden="true">i</span></summary><p class="info-i-texto">Grafismo gerado com recurso a IA, EPI, 2026, a partir do '
                      'padrão de ondas da calçada portuguesa (o «mar largo» do Rossio, Lisboa).</p></details></div>', HTML)
        self.assertNotIn('<p class="cf-credito">', HTML)
        self.assertNotIn('Parar o desenho', HTML)
        inicio = HTML.index('<div class="fundo-acoes cf-credito">')
        credito = HTML[inicio:HTML.index('</div>', inicio)]
        self.assertLess(credito.index('</button>'), credito.index('<details'), 'o botão fica fora do «i»')
        self.assertNotIn('pedra a pedra', credito)
        self.assertNotIn('Desenho nosso', credito)
        self.assertIn('Grafismo gerado com recurso a IA, EPI, 2026:', (ROOT/'assets/calcada-mar.svg').read_text('utf-8'))
        self.assertNotIn('a traço', credito)
        self.assertIn('<h1 aria-label="Português">', HTML)
        # 02/11/2026: decisão 139. O texto da entrada não muda; a faixa vem logo depois dele.
        self.assertIn('<p class="pt-entry-lead">Ler com atenção. Relacionar ideias. Experimentar outras vozes.</p><div class="cf-mar"', HTML)
        self.assertIn('assets/fundo-calcada.css?v=', HTML)
        self.assertIn('assets/fundos.css?v=', HTML)
        self.assertIn('<script defer src="assets/fundos.js?v=', HTML)
        self.assertNotIn('fundo-calcada.js', HTML)

    def test_animacoes_so_no_bloco_de_movimento(self):
        bloco = CSS.index('@media(prefers-reduced-motion:no-preference){')
        fim = CSS.index('\n}', bloco)
        usos = list(re.finditer(r'animation(?:-name)?:\s*([\w-]+)', CSS))
        # 02/11/2026: decisão 139. Uma só animação (as ondas a correr), e só dentro do bloco de movimento.
        self.assertEqual([u.group(1) for u in usos], ['cf-mar'])
        for uso in usos:
            self.assertTrue(bloco < uso.start() < fim, f'animação fora do bloco de movimento: {uso.group(0)}')
            linha = CSS[CSS.rindex('\n', 0, uso.start()):uso.start()]
            self.assertIn('html:not(.em-projecao)', linha)
        # 02/11/2026: decisão 137. A pausa fora do ecrã e com o separador escondido é a do motor comum.
        self.assertIn('[data-fundo].fundo-pausa *{animation-play-state:paused!important}', MOTOR_CSS)
        # 02/11/2026: decisão 139. Na impressão, a faixa não sai.
        self.assertRegex(CSS, r'@media print\{\.raiz \.cf-mar\{display:none\}\}')

    def test_script_respeita_projecao_e_movimento_reduzido(self):
        self.assertIn("matchMedia('(prefers-reduced-motion: no-preference)')", JS)
        # 07/11/2026: decisão 177. O motor comum escreve «Parar a animação» e, parado, «Retomar a animação» (era «Parar o desenho»
        # e «Pôr o desenho a andar»), igual no Lente.
        self.assertIn("botao.textContent = anda() ? 'Parar a animação' : 'Retomar a animação';", JS)
        self.assertNotIn('Parar o desenho\'', JS)
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
