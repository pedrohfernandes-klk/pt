"""15/11/2026: acabamento visual (Gestalt e movimento curto) em assets/appearance.css.

Confere que todo o movimento novo vive em prefers-reduced-motion: no-preference, que @media print não ganha animações
e que há regras de focus-visible.
"""
import re
import unittest
from pathlib import Path

CSS = (Path(__file__).resolve().parents[1] / 'assets/appearance.css').read_text('utf-8')
INI = CSS.index('/* 15/11/2026: acabamento visual')
FIM = CSS.index('/* 30/10/2026: texto corrido justificado')
BLOCO = CSS[INI:FIM]


def corpo(css, inicio):
    """Texto entre as chaves do bloco @ que começa em inicio."""
    i = css.index('{', inicio)
    n = 0
    for j in range(i, len(css)):
        n += css[j] == '{'
        n -= css[j] == '}'
        if n == 0:
            return css[i + 1:j]
    raise AssertionError('chaves por fechar')


def sem_blocos(css, cabecalho):
    out, pos = '', 0
    for m in re.finditer(re.escape(cabecalho), css):
        if m.start() < pos:
            continue
        out += css[pos:m.start()]
        i = css.index('{', m.start())
        corpo_ = corpo(css, m.start())
        pos = i + len(corpo_) + 2
    return out + css[pos:]


class AcabamentoVisual(unittest.TestCase):
    def test_movimento_so_com_no_preference(self):
        mov = re.compile(r'\b(transition|animation|@keyframes)\b|transform\s*:|translate\s*:')
        resto = sem_blocos(BLOCO, '@media screen and (prefers-reduced-motion:no-preference)')
        resto = sem_blocos(resto, '@media print')
        resto = re.sub(r'/\*.*?\*/', '', resto, flags=re.S)
        self.assertIsNone(mov.search(resto), mov.search(resto) and resto[mov.search(resto).start():][:80])
        self.assertIn('prefers-reduced-motion:no-preference', BLOCO)

    def test_duracoes_curtas(self):
        for v in re.findall(r'\.(\d+)s ease-out', BLOCO):
            self.assertTrue(150 <= int(v.ljust(3, '0')) <= 250, v)

    def test_print_sem_animacoes(self):
        i = BLOCO.index('@media print')
        imp = corpo(BLOCO, i)
        self.assertIn('animation:none', imp)
        self.assertNotRegex(imp, r'animation:\s*(?!none)\w')
        self.assertNotIn('@keyframes', imp)
        for m in re.finditer(r'@media\s+print', CSS):
            self.assertNotRegex(corpo(CSS, m.start()), r'animation:\s*(?!none)[a-z-]+\s+[\d.]+m?s')

    def test_focus_visible(self):
        self.assertRegex(BLOCO, r'focus-visible\{outline:3px solid')

    def test_sem_movimento_reduzido(self):
        self.assertNotIn('prefers-reduced-motion:reduce', BLOCO)

    def test_dobras_sempre_abertas_nunca_ficam_transparentes(self):
        # 15/11/2026: revisão geral antes de publicar: as dobras que o ecrã mostra sempre abertas sem o atributo open (.cz-fold dos
        # índices, .info-i, .tf-so-tema) não podem ganhar opacity:0 no ::details-content.
        linhas = [l for l in BLOCO.splitlines() if '::details-content{opacity:0' in l]
        self.assertTrue(linhas)
        for l in linhas:
            for c in ('.cz-fold', '.info-i', '.tf-so-tema'):
                self.assertIn(c, l)


if __name__ == '__main__':
    unittest.main()
