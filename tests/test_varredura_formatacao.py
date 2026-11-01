"""01/11/2026: âmbito, reversibilidade e integridade da revisão editorial."""
from pathlib import Path
import hashlib
import json
import re
import unittest
from auditoria_20261028 import undo_varredura

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT/'docs/qa/varredura-formatacao-20261101.json').read_text('utf-8'))
MANIFEST = json.loads((ROOT/'tests/fixtures/varredura-formatacao-edits-20261101.json').read_text('utf-8'))


class Varredura(unittest.TestCase):
    def test_todos_os_pontos_tem_destino(self):
        rows = LEDGER['achados']
        self.assertEqual(len(rows), 361)
        self.assertEqual(len({r['id'] for r in rows}), 361)
        self.assertEqual(sum(r['estado']=='adiado' for r in rows), 109)
        self.assertEqual(sum(r['estado']=='conforme' for r in rows), 13)
        self.assertEqual(sum(r['estado']=='corrigido' for r in rows), 239)

    def test_nao_toca_nos_ficheiros_editoriais_em_revisao(self):
        protected = {f for p in LEDGER['pedidos'] for f in p['ficheiros']}
        self.assertEqual(set(MANIFEST['files']) & protected, set())
        for r in LEDGER['achados']:
            expected = [p['numero'] for p in LEDGER['pedidos'] if r['file'] in p['ficheiros']]
            self.assertEqual(r['depois'], expected, r['id'])

    def test_camada_reversivel_e_cabecalhos_intactos(self):
        for rel, record in MANIFEST['files'].items():
            with self.subTest(file=rel):
                current = (ROOT/rel).read_text('utf-8')
                original = undo_varredura(rel, current)
                self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), record['base_sha256_lf'])
                self.assertEqual(hashlib.sha256(current.encode()).hexdigest(), record['after_sha256_lf'])
                for edit in record['edits']:
                    self.assertEqual(current.count(edit['new']), 1)
                if rel.endswith('.html'):
                    self.assertEqual(re.search(r'<head>.*?</head>', original, re.S)[0],
                                     re.search(r'<head>.*?</head>', current, re.S)[0])
                    self.assertIn('<html lang="pt-PT"', current)

    def test_lugar_familia_e_poema_nao_passam_a_titulos_de_livro(self):
        for rel in MANIFEST['files']:
            if not rel.endswith('.html'):
                continue
            s=(ROOT/rel).read_text('utf-8')
            self.assertNotIn('Largo <i>Amor de Perdição', s)
            self.assertNotIn('<i>Os Maias</i> «vieram habitar»', s)
            self.assertNotIn('<i>O Sentimento dum Ocidental</i>', s)

    def test_creditos_declaram_as_lacunas_da_fonte(self):
        for slug in ('licao-m7-f01', 'licao-m7-f05', 'mapa-do-modulo-m7'):
            s=(ROOT/f'm7/{slug}/index.html').read_text('utf-8').replace('\\"', '"')
            self.assertIn('Fotógrafo não identificado.', s)
            self.assertIn('Instituição depositária do original não indicada.', s)
            self.assertIn('File:PessoaChapeu.jpg', s)
            for field in ('Autor', 'Obra', 'Data', 'Instituição', 'Licença'):
                self.assertIn(f'<th scope="row">{field}</th>', s)


if __name__ == '__main__':
    unittest.main()
