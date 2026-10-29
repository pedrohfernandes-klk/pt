"""Painéis de aula (27/10/2026): cada pergunta-relâmpago do painel abre um exercício da lição.

O recetor da lição ignora índices que apontam para um cartão de leitura (`x.t==="ler"`); em quatro
painéis, onze opções tinham deixado de abrir depois de a lição ganhar cartões novos. Todos os painéis:
índice dentro do banco e nunca uma leitura; seletor igual à lista do painel. Nos quatro corrigidos por
conteúdo (M2-F02, M2-F07, M3-F10, M9-F10): a lista é a dos exercícios atuais, com tipo e enunciado
iguais aos do cartão.
"""
from pathlib import Path
import html,json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
CORRIGIDOS=['m2/painel-m2-f02','m2/painel-m2-f07','m3/painel-m3-f10','m9/painel-m9-f10']

def banco(texto):
    m=re.search(r'CARTOES\s*=\s*(\[)',texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0] if m else None

def enunciado(c):
    p=c.get('p') or c.get('frase') or ''
    p=re.sub(r'\*\*(.+?)\*\*',r'\1',re.sub(r'(?<!\w)_(.+?)_(?!\w)',r'\1',p))
    return re.sub(r'\[\d\]','…',p)

def paineis():
    for p in sorted(ROOT.glob('m*/painel-m*-f*/index.html')):
        texto=p.read_text('utf-8');P=banco(texto)
        if P is None:continue
        licao=p.parents[1]/p.parent.name.replace('painel-','licao-')/'index.html'
        yield p,texto,P,licao

class Paineis(unittest.TestCase):
    def test_nenhuma_pergunta_aponta_para_uma_leitura(self):
        n=0
        for p,texto,P,licao in paineis():
            L=banco(licao.read_text('utf-8'))
            sel=re.search(r'<select data-r-k>(.*?)</select>',texto,re.S)
            self.assertIsNotNone(sel,p)
            self.assertEqual([int(v) for v in re.findall(r'<option value="(\d+)">',sel.group(1))],[c['k'] for c in P],p)
            for c in P:
                with self.subTest(painel=p.parent.name,k=c['k']):
                    self.assertTrue(0<=c['k']<len(L))
                    self.assertNotEqual(L[c['k']]['t'],'ler')
                n+=1
        self.assertGreater(n,1000)

    def test_quatro_paineis_corrigidos_por_conteudo(self):
        for pasta in CORRIGIDOS:
            texto=(ROOT/pasta/'index.html').read_text('utf-8');P=banco(texto)
            L=banco((ROOT/pasta.replace('painel-','licao-')/'index.html').read_text('utf-8'))
            esperado=[{'k':i,'t':c['t'],'p':enunciado(c)} for i,c in enumerate(L) if c['t']!='ler']
            self.assertEqual(P,esperado,pasta)
            ops=re.findall(r'<option value="\d+">(.*?)</option>',re.search(r'<select data-r-k>(.*?)</select>',texto,re.S).group(1))
            self.assertEqual([html.unescape(o) for o in ops],[c['p'] for c in esperado],pasta)
            self.assertFalse(any('_' in c['p'] or '**' in c['p'] for c in P),pasta)

if __name__=='__main__':unittest.main()
