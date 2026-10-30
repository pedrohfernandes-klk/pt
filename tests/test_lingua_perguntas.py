import json,pathlib,re,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
# 30/10/2026: pedido do docente («Qual citação identifica…» é muito mau em português; o problema é transversal). Mesmo
# teste do Lente (lente #76). Em português europeu, a pergunta que escolhe entre opções diz «Qual das citações…», «Qual
# destas notas…», «Qual é a frase que…» ou «Que frase…»; nunca «Qual citação…». Vale também para a interrogativa indireta
# («diz que homem casa»). «Qual» como pronome («Qual preferes?», «Qual é…», «Qual depende de qual?») e os textos
# literários citados ficam livres: a lista só tem nomes que aparecem em enunciados.
NOMES=r'''frases? citaç(?:ão|ões) afirmaç(?:ão|ões) perguntas? image(?:m|ns) vers(?:ão|ões) recortes? critérios?
conclus(?:ão|ões) formulaç(?:ão|ões) reformulaç(?:ão|ões) propostas? utilizaç(?:ão|ões) raz(?:ão|ões) créditos? obras?
detalhes? pormenor(?:es)? decis(?:ão|ões) opç(?:ão|ões) respostas? palavras? versos? estrofes? linhas? comparaç(?:ão|ões)
interpretaç(?:ão|ões) revis(?:ão|ões) sínteses? justificaç(?:ão|ões) desenvolvimentos? notas? registos? aç(?:ão|ões)
alteraç(?:ão|ões) inícios? par(?:es)? trios? procedimentos? promessas? exemplos? textos? parágrafos? títulos? legendas?
cenas? persona(?:gem|gens) argumentos? recursos? sentidos? efeitos? ideias? teses? provas? fontes? planos?
acontecimentos? hipóteses? nomes? leituras? testemunh(?:a|as|o|os) homem homens meninas? casas?'''.split()
QUAL_NOME=re.compile(r'(?<![A-Za-zÀ-ÿ])(?:Qual|Quais|qual|quais)\s+(?:'+'|'.join(NOMES)+r')(?![A-Za-zÀ-ÿ])')
# 30/10/2026: o aluno trata-se por «tu» e a turma por «vocês»: nada de imperativos de «você» a abrir uma instrução.
# «Toque de quê?» (M1-F08) é o nome «toque», não o imperativo, e fica de fora.
IMPERATIVO_VOCE=re.compile(r'(?:<li>|<p>|<dd>|"\s*:\s*")\s*(?:Clique|Toque(?! de quê)|Arraste|Compare|Escreva|Leia|Observe|Repare|Responda|Escolha|Assinale|Sublinhe|Justifique|Explique|Indique)\s')
FORA=('tests','scripts','docs','node_modules','.git','.github','_interno')
# As instruções oficiais das provas do IAVE (cartões «item» e enunciados transcritos) usam «Leia», «Explique»: são
# citação da prova e não se mudam. Ficam fora do teste dos imperativos, não do de «Qual + nome».
PROVAS=('exame/provas/',)
TROCAS=ROOT/'scripts/lingua_pessoa_m7_20261030.json'
def paginas():
 for p in sorted(ROOT.rglob('*')):
  if p.suffix in ('.html','.js','.json') and not set(p.relative_to(ROOT).parts)&set(FORA):yield p
class LinguaDasPerguntas(unittest.TestCase):
 def test_padroes(self):
  for bom in ('Qual das citações identifica a testemunha?','Que critério deve decidir?','Qual preferes?','Qual é a frase que…','Qual depende de qual?','diz que homem casa'):
   self.assertIsNone(QUAL_NOME.search(bom),bom)
  for mau in ('Qual citação identifica a testemunha?','decide qual razão é mais forte','Quais frases mostram','Qual par cumpre?','diz qual homem casa'):
   self.assertIsNotNone(QUAL_NOME.search(mau),mau)
  self.assertIsNotNone(IMPERATIVO_VOCE.search('<li>Compare duas apresentações'))
  self.assertIsNone(IMPERATIVO_VOCE.search('<li>Comparem duas apresentações'))
  self.assertIsNone(IMPERATIVO_VOCE.search('"p":"Toque de quê?"'))
 def test_sem_qual_mais_nome(self):
  falhas=[]
  for p in paginas():
   s=p.read_text('utf-8',errors='replace')
   for m in QUAL_NOME.finditer(s):falhas.append(p.relative_to(ROOT).as_posix()+': …'+s[max(0,m.start()-30):m.end()+40].replace('\n',' ')+'…')
  self.assertEqual(falhas,[],'\n'.join(falhas))
 def test_sem_imperativo_de_voce(self):
  falhas=[]
  for p in paginas():
   rel=p.relative_to(ROOT).as_posix()
   if rel.startswith(PROVAS):continue
   s=p.read_text('utf-8',errors='replace')
   for m in IMPERATIVO_VOCE.finditer(s):falhas.append(rel+': …'+s[m.start():m.end()+60].replace('\n',' ')+'…')
  self.assertEqual(falhas,[],'\n'.join(falhas))
 def test_trocas_registadas(self):
  # 30/10/2026: as trocas de «Qual + nome» estão na camada literal scripts/lingua_pessoa_m7_20261030.json (manifesto
  # tests/fixtures/lingua-pessoa-m7-edits-20261030.json); cada «novo» está no sítio o número de vezes registado e nenhum
  # «antigo» voltou. As provas em cartões mudam pelos dados (scripts/provas/dados/2026-*/grupo-iii.json).
  trocas=[t for t in json.loads(TROCAS.read_text('utf-8')) if t['achado'].startswith('«Qual + nome»')]
  self.assertGreaterEqual(len(trocas),40)
  for t in trocas:
   s=(ROOT/t['ficheiro']).read_text('utf-8')
   self.assertEqual(s.count(t['novo']),t['ocorrencias'],t['ficheiro']+': '+t['novo'])
   self.assertNotIn(t['antigo'],s,t['ficheiro'])
  for prova in ('2026-1f','2026-2f'):
   dados=(ROOT/f'scripts/provas/dados/{prova}/grupo-iii.json').read_text('utf-8')
   self.assertIn('Qual das conclusões é «adequada',dados);self.assertNotIn('Qual conclusão',dados)
if __name__=='__main__':unittest.main()
