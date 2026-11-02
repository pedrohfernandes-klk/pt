"""01/11/2026: contratos do lote 2, sem alterar tipos, seleção ou progresso."""
from pathlib import Path
from collections import Counter
import json,re,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from opcoes_equilibradas import medir
from auditoria_20261028 import undo_conteudos_lote2
LOG=json.loads((ROOT/'docs/qa/conteudos-lote2-cartoes-20261101.json').read_text('utf-8'))

def cards(text):
    m=re.search(r'\bCARTOES\s*=\s*',text)
    return json.JSONDecoder().raw_decode(text,m.end())[0]

class Lote2(unittest.TestCase):
    def test_tipos_selecao_e_ordem_conservados(self):
        for rel in sorted({x['ficheiro'] for x in LOG}):
            current=(ROOT/rel).read_text('utf-8')
            before=cards(undo_conteudos_lote2(rel,current));after=cards(current)
            self.assertEqual(len(before),len(after),rel)
            for i,(a,b) in enumerate(zip(before,after)):
                for key in ('t','mais','g','l','variar','aula'):
                    self.assertEqual(a.get(key),b.get(key),(rel,i,key))
    def test_limite_de_seis_e_registo_exato(self):
        counts=Counter(x['licao'] for x in LOG)
        self.assertTrue(all(n<=6 for n in counts.values()),counts)
        self.assertEqual(len(LOG),len({(x['licao'],x['cartao']) for x in LOG}))
        for x in LOG:
            self.assertEqual(cards((ROOT/x['ficheiro']).read_text('utf-8'))[x['cartao']-1],x['depois'])
            self.assertNotEqual(x['antes'],x['depois'])
    def test_opcoes_e_retornos_dos_cartoes_tocados(self):
        for x in LOG:
            c=x['depois']
            groups=[(c['o'],c['c'])] if c['t'] in ('escolha','rever') else [(l['o'],l['c']) for l in c.get('lacunas',[])]
            for options,correct in groups:
                with self.subTest(licao=x['licao'],cartao=x['cartao']):
                    self.assertFalse(medir(options,correct)['amplitude_acima'])
                    self.assertFalse(medir(options,correct)['certa_25_porcento'])
            if c['t']=='escolha':
                self.assertEqual(len(c['fe']),len(c['o']))
                for i,f in enumerate(c['fe']):
                    if i!=c['c']:
                        self.assertTrue(f)
                        self.assertRegex(f,r'Relê|relê|Volta|volta|Compara|compara|Procura|procura')
    def test_provas_nao_alteram_dados_dos_percursos(self):
        for m in range(1,10):
            rel=f'm{m}/index.html';current=(ROOT/rel).read_text('utf-8')
            if 'id="prova-esperada-lote2"' not in current:continue
            before=undo_conteudos_lote2(rel,current)
            pattern=r'<script id="epi-unidades-pedagogicas">(.*?)</script>'
            self.assertEqual(re.search(pattern,before,re.S)[1],re.search(pattern,current,re.S)[1])
            self.assertEqual(re.findall(r'\bid="([^"]+)"',before),[v for v in re.findall(r'\bid="([^"]+)"',current) if v!='prova-esperada-lote2'])
            self.assertEqual(re.findall(r'\bhref="([^"]+)"',before),re.findall(r'\bhref="([^"]+)"',current))
            units=json.loads(re.search(pattern,current,re.S)[1])
            self.assertEqual(current.count('<p class="prova-esperada">'),len(units))
            self.assertIn('content:"Prova da unidade"',current)

if __name__=='__main__':unittest.main()
