"""03/11/2026: calçada sem repetição vertical e com três ondas independentes."""
from pathlib import Path
import subprocess
import sys
import unittest
import re
ROOT=Path(__file__).resolve().parents[1]
class CalcadaContinua(unittest.TestCase):
    def test_gerador(self):
        result=subprocess.run([sys.executable,'scripts/gerar_calcada_continua.py','--verificar'],cwd=ROOT,capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        for name in ['calcada-clara.svg']+[f'calcada-onda-{i}.svg' for i in range(1,4)]:
            text=(ROOT/'assets'/name).read_text('utf-8')
            self.assertIn('viewBox="0 0 960 440"',text)
            self.assertNotRegex(text,r'<script|<image|href=|\son\w+=')
    def test_camadas_e_movimento(self):
        css=(ROOT/'assets/calcada-continua.css').read_text('utf-8')
        self.assertEqual(len(re.findall(r'@keyframes cf-respira-',css)),3)
        self.assertNotIn('translateX',css)
        self.assertNotRegex(css,r'background-repeat:\s*repeat\s*[;}]')
        self.assertIn('prefers-reduced-motion:no-preference',css)
        self.assertIn('animation-play-state:paused',css)
        self.assertNotIn('!important',css)
    def test_ambito_isolado(self):
        # 03/11/2026: prova de preservação exata dos HTML, motores, páginas e peças em revisão.
        result=subprocess.run(['git','diff','--exit-code','8a38a69d554dca94e7018b14e7fef581286f5896','--','*.html','assets/fundos.js','assets/fundos.css','assets/appearance.js','assets/pt-lessons/','assets/task-*','assets/cartaz-components.*'],cwd=ROOT,capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
if __name__=='__main__':unittest.main()
