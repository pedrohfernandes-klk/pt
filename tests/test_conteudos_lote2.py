"""01/11/2026: contratos do lote 2, sem alterar tipos, seleção ou progresso."""
from pathlib import Path
from collections import Counter
import json,re,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from opcoes_equilibradas import medir
from auditoria_20261028 import undo_conteudos_lote2, undo_m4_piloto
# 05/11/2026: a revisão de 5/11 está por cima do lote 2.
from auditoria_20261028 import undo_revisao_0511
# 05/11/2026: a decisão 154 está por cima do piloto M4 (passo 16 do percurso do M4); desfaz-se só essa camada.
from auditoria_20261028 import undo_autonomia_0511
# 06/11/2026: a decisão 152 no M1 (tabelas e espaços que não quebram) está por cima do lote 2; desfaz-se antes, com contagem estrita.
from auditoria_20261028 import undo_cuidado_m1_0611
LOG=json.loads((ROOT/'docs/qa/conteudos-lote2-cartoes-20261101.json').read_text('utf-8'))

def cards(text):
    m=re.search(r'\bCARTOES\s*=\s*',text)
    return json.JSONDecoder().raw_decode(text,m.end())[0]

class Lote2(unittest.TestCase):
    def test_tipos_selecao_e_ordem_conservados(self):
        for rel in sorted({x['ficheiro'] for x in LOG}):
            current=(ROOT/rel).read_text('utf-8')
            # 06/11/2026: o «depois» compara-se sem a decisão 152 no M1 (só espaços que não quebram e tabelas), desfeita com contagem
            # estrita; o «antes» já a desfaz na cadeia (undo_conteudos_lote2 chama-a primeiro).
            before=cards(undo_conteudos_lote2(rel,current));after=cards(undo_cuidado_m1_0611(rel,current))
            self.assertEqual(len(before),len(after),rel)
            for i,(a,b) in enumerate(zip(before,after)):
                for key in ('t','mais','g','l','variar','aula'):
                    # 02/11/2026: mudanças explícitas já confirmadas no #149, verificadas pelo valor exato.
                    approved={('m4/licao-m4-f01/index.html',10,'mais'):(True,None),
                              ('m7/licao-m7-f34/index.html',8,'g'):(2,'dupla-exposicao'),
                              ('m8/licao-m8-f12/index.html',16,'t'):('vf','escolha')}
                    if (rel,i,key) in approved:
                        self.assertEqual((a.get(key),b.get(key)),approved[rel,i,key])
                    else:
                        self.assertEqual(a.get(key),b.get(key),(rel,i,key))
    def test_limite_de_seis_e_registo_exato(self):
        counts=Counter(x['licao'] for x in LOG)
        self.assertTrue(all(n<=6 for n in counts.values()),counts)
        self.assertEqual(len(LOG),len({(x['licao'],x['cartao']) for x in LOG}))
        for x in LOG:
            # 05/11/2026: o cartão do lote 2 confere-se por baixo da revisão de 5/11 (desfeita com contagem estrita).
            self.assertEqual(cards(undo_revisao_0511(x['ficheiro'],(ROOT/x['ficheiro']).read_text('utf-8')))[x['cartao']-1],x['depois'])
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
            # 02/11/2026: verificar os nove índices, incluindo as provas já publicadas pelo Cartaz.
            before=undo_conteudos_lote2(rel,current)
            # 02/11/2026: comparar o lote de conteúdo antes da camada visual posterior.
            # 05/11/2026: a decisão 154 muda o passo 16 do percurso do M4, dentro de um bloco do piloto; desfaz-se só essa
            # camada antes do piloto, com contagem estrita, e as conferências continuam a olhar para a página publicada.
            current=undo_m4_piloto(rel,undo_autonomia_0511(rel,current))
            # 02/11/2026: M4/M7 já publicam o tipo JSON antes do id; verificar o mesmo conteúdo integral.
            pattern=r'<script (?:type="application/json" )?id="epi-unidades-pedagogicas">(.*?)</script>'
            self.assertEqual(re.search(pattern,before,re.S)[1],re.search(pattern,current,re.S)[1])
            # 02/11/2026: o identificador novo limita a correção dos alvos táteis ao M2.
            self.assertEqual(current.count('id="alvos-lote2"'),1 if m==2 else 0)
            self.assertEqual(re.findall(r'\bid="([^"]+)"',before),[v for v in re.findall(r'\bid="([^"]+)"',current) if v not in ('prova-esperada-lote2','alvos-lote2')])
            self.assertEqual(re.findall(r'\bhref="([^"]+)"',before),re.findall(r'\bhref="([^"]+)"',current))
            units=json.loads(re.search(pattern,current,re.S)[1])
            self.assertEqual(current.count('<p class="prova-esperada">'),len(units))
            self.assertIn('cartaz-indices.css',current)
            self.assertRegex((ROOT/'assets/cartaz-indices.css').read_text('utf-8'),r'\.prova-esperada\{[^}]*font:1rem/1\.55 Georgia,serif')

if __name__=='__main__':unittest.main()
