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

# 01/11/2026: retira apenas o itálico; conserva espaços, negrito e números das lacunas.
def sem_italico(s):
    return re.sub(r'(?<!\w)_(.+?)_(?!\w)',r'\1',s)


def enunciado(c):
    p=c.get('p') or c.get('frase') or ''
    p=re.sub(r'\*\*(.+?)\*\*',r'\1',re.sub(r'(?<!\w)_(.+?)_(?!\w)',r'\1',p))
    return re.sub(r'\[\d\]','…',p)

# 02/11/2026: o enunciado que o painel projeta conserva o itálico do cartão (_…_); só saem o negrito e os números das
# lacunas. Assim, um título em itálico na lição fica em itálico no painel, e nunca só metade (M9-F07, k=13).
def enunciado_italico(c):
    p=c.get('p') or c.get('frase') or ''
    p=re.sub(r'\*\*(.+?)\*\*',r'\1',p)
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
            # 01/11/2026: o cartão ganha itálico; a equivalência textual e a ordem mantêm-se.
            # 02/11/2026: compara com o itálico mantido (enunciado_italico), em vez de o tirar dos dois lados.
            self.assertEqual(P,[{'k':i,'t':c['t'],'p':enunciado_italico(c)} for i,c in enumerate(L) if c['t']!='ler'],pasta)
            ops=re.findall(r'<option value="\d+">(.*?)</option>',re.search(r'<select data-r-k>(.*?)</select>',texto,re.S).group(1))
            self.assertEqual([html.unescape(o) for o in ops],[c['p'] for c in esperado],pasta)
            # 01/11/2026: sem marcadores visíveis no seletor; o painel converte os do cartão em itálico.
            self.assertFalse(any('_' in o or '**' in o for o in ops),pasta)

    def test_italico_do_painel_igual_ao_da_licao(self):
        # 02/11/2026: em todos os painéis, cada enunciado com itálico é o do cartão da lição, itálico incluído.
        n=0
        for p,texto,P,licao in paineis():
            L=banco(licao.read_text('utf-8'))
            for c in P:
                if '_' in c['p']:
                    with self.subTest(painel=p.parent.name,k=c['k']):
                        self.assertEqual(c['p'],enunciado_italico(L[c['k']]))
                    n+=1
        self.assertGreater(n,0)

if __name__=='__main__':unittest.main()
