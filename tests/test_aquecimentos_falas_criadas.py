"""01/11/2026: conferir as falas criadas sem as confundir com citações da obra."""
import json
from pathlib import Path
import re
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from aquecimentos_falas_criadas import FALAS, fala_criada
from aquecimentos import texto_visivel, validar


class FalasCriadas(unittest.TestCase):
    def test_lista_literal_presente_identificada_e_sem_excecoes_obsoletas(self):
        for (slug,n),falas in FALAS.items():
            d=json.loads((ROOT/f'docs/pedagogia/aquecimentos/{slug}.json').read_text('utf-8'))
            card=d['cartoes'][n-1]
            quotes=set(re.findall('«([^»]+)»',texto_visivel(card)))
            self.assertEqual(quotes,falas,(slug,n))
            for quote in quotes:
                self.assertTrue(fala_criada(slug,n,card,quote))
                self.assertFalse(fala_criada(slug,n,card,quote+' diferente'))
                self.assertFalse(fala_criada(slug,n,dict(card,p='Citação da obra'),quote))
            changed=json.loads(json.dumps(d))
            changed['cartoes'][n-1]['p']+=' Citação sem fonte: «Esta passagem foi fabricada e não pertence à obra.»'
            self.assertTrue(any('não está letra a letra' in e for e in validar(ROOT,changed)))


if __name__=='__main__':unittest.main()
