"""02/11/2026: F0 acrescenta ajuda e protege a importação, sem alterar os bancos."""
import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from auditoria_20261028 import undo_variedade_f0, undo_cabecalho

ROOT=Path(__file__).resolve().parents[1]


class F0(unittest.TestCase):
    def test_vinte_aquecimentos_mesmos_cartoes_chaves_e_versoes(self):
        data=list((ROOT/'docs/pedagogia/aquecimentos').glob('*.json'))
        self.assertEqual(len(data),20)
        for source in data:
            rel=f'tarefas/{source.stem}/aquecimento/index.html'
            now=(ROOT/rel).read_text('utf-8');before=undo_variedade_f0(rel,now)
            button='<button type="button" class="c-ic" data-c-como aria-label="Como se faz" title="Como se faz" hidden><span class="c-roda">?</span></button>'
            self.assertEqual(now.count(button),1,rel)
            self.assertEqual(now.replace(button,''),before,rel)
            self.assertEqual(re.findall(r'\b(?:chave|versao):[^,}]+',before),re.findall(r'\b(?:chave|versao):[^,}]+',now),rel)

    def test_manifesto_reversivel_e_ambito_exato(self):
        m=json.loads((ROOT/'tests/fixtures/variedade-f0-edits-20261102.json').read_text('utf-8'))
        expected={'index.html'}|{f'tarefas/{p.stem}/aquecimento/index.html' for p in (ROOT/'docs/pedagogia/aquecimentos').glob('*.json')}
        self.assertEqual(set(m['files']),expected)
        self.assertEqual(sum(len(r['edits']) for r in m['files'].values()),24)
        for rel,r in m['files'].items():
            # 03/11/2026: retirar só a ligação visual antes de conferir os mesmos SHA da F0.
            now=undo_cabecalho(rel,(ROOT/rel).read_text('utf-8'))
            self.assertEqual(hashlib.sha256(now.encode()).hexdigest(),r['after_sha256_lf'],rel)
            self.assertEqual(hashlib.sha256(undo_variedade_f0(rel,now).encode()).hexdigest(),r['base_sha256_lf'],rel)

    def test_verificador_confere_a_camada(self):
        # 05/11/2026: a revisão de 5/11 desfaz-se primeiro; as conferências ficam iguais.
        # 05/11/2026: a tabela dos seis movimentos é a camada mais recente; desfaz-se antes da revisão, com a mesma exigência.
        # 05/11/2026: o Laboratório do exame (lição, não «leitura de apoio») é a camada mais recente; desfaz-se antes da tabela dos seis movimentos.
        # 05/11/2026: o contexto de cada sessão do Laboratório do exame (lição e excerto, não «recorte») é a camada mais recente; desfaz-se antes da ligação e das notas do Laboratório do exame.
        # 05/11/2026: o lote 3 do Atlas é a camada mais recente; desfaz-se antes do contexto do Laboratório do exame, com a mesma exigência.
        r=subprocess.run([sys.executable,'scripts/aplicar_trocas.py','scripts/variedade_f0_20261102.json','--manifesto','tests/fixtures/variedade-f0-edits-20261102.json','--verificar','--desfazer-antes','tests/fixtures/atlas-lote3-edits-20261105.json','--desfazer-antes','tests/fixtures/exame-contexto-edits-20261105.json','--desfazer-antes','tests/fixtures/exame-licao-edits-20261105.json','--desfazer-antes','tests/fixtures/tabela-movimentos-edits-20261105.json','--desfazer-antes','tests/fixtures/revisao-edits-20261105.json','--desfazer-antes','tests/fixtures/cartaz-cabecalho-edits-20261103.json'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)


if __name__=='__main__':unittest.main()
