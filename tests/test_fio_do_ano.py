"""02/11/2026: âmbito e conservação do piloto do fio do ano."""
from pathlib import Path
import json,re,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from auditoria_20261028 import undo_fio_do_ano
FILES={'1/index.html','m1/index.html','m2/index.html','m3/index.html'}

class FioDoAno(unittest.TestCase):
    def test_piloto_so_nas_quatro_paginas_autorizadas(self):
        edits=json.loads((ROOT/'scripts/fio_do_ano_20261101.json').read_text('utf-8'))
        self.assertEqual({e['ficheiro'] for e in edits},FILES)
        self.assertEqual(len(edits),8)
        for e in edits:
            self.assertEqual(e['ocorrencias'],1)
            self.assertNotRegex(e['novo'],r'<script|\bon\w+\s*=|localStorage|sessionStorage')
        for rel in ['2/index.html','3/index.html']+[f'm{n}/index.html' for n in range(4,10)]:
            self.assertNotIn('class="fio-ano',(ROOT/rel).read_text('utf-8'))

    def test_ligacoes_ancoras_scripts_e_progresso_intactos(self):
        for rel in sorted(FILES):
            with self.subTest(page=rel):
                after=(ROOT/rel).read_text('utf-8');before=undo_fio_do_ano(rel,after)
                for pattern in (r'<script\b.*?</script>',r'\bid="[^"]*"',r'\bhref="[^"]*"',r'<title>.*?</title>',r'<meta\b[^>]*>',r'\bdata-(?:u|unidade|passo|task-lesson|module-next)[^>]*'):
                    self.assertEqual(re.findall(pattern,before,re.S),re.findall(pattern,after,re.S),pattern)
                if rel.startswith('m'):
                    self.assertLess(after.index('data-module-next'),after.index('class="fio-ano-modulo"'))
                    self.assertEqual(after.count('class="fio-ano-modulo"'),1)
                    self.assertEqual(re.findall(r'<p class="prova-esperada">.*?</p>',before,re.S),re.findall(r'<p class="prova-esperada">.*?</p>',after,re.S))

    def test_rubrica_unica_sem_respostas_nem_classificacao(self):
        page=(ROOT/'1/index.html').read_text('utf-8')
        fio=re.search(r'<section class="fio-ano".*?</section>',page,re.S)[0]
        self.assertEqual(re.findall(r'<dt>(.*?)</dt>',fio),['Afirmação delimitada','Indício pertinente','Ligação explicada','Limite reconhecido'])
        self.assertEqual(fio.count('<details>'),1)
        self.assertIn('<summary>Quatro perguntas para rever</summary>',fio)
        self.assertNotRegex(fio,r'\b(?:jogo|jogar|ficha|folha|professor)\b|[—·]|/20|\d+\s*%')
        for rel in FILES-{'1/index.html'}:
            self.assertNotIn('<dt>Afirmação delimitada</dt>',(ROOT/rel).read_text('utf-8'))

if __name__=='__main__':unittest.main()
