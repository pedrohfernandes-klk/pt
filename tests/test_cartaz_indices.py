# 02/11/2026: crédito de IA acima do lote 2; mesmas asserções.
# 02/11/2026: desfaz o lote 2 antes da base publicada; mesmas asserções.
"""01/11/2026: índices Cartaz, preservação e camada literal reversível."""
import json,re,subprocess,sys,unittest
from pathlib import Path
from auditoria_20261028 import undo_cartaz_indices, undo_tarefas_individuais
ROOT=Path(__file__).resolve().parents[1]

class IndicesCartaz(unittest.TestCase):
 def test_ligacoes_ancoras_ordem_e_dados_do_motor(self):
  for n in range(1,10):
   rel=f'm{n}/index.html';after=(ROOT/rel).read_text('utf8');before=undo_cartaz_indices(rel,after)
   # 02/11/2026: a camada das tarefas individuais (por cima desta) muda o texto de cartões da retoma; compara-se a página sem ela.
   after=undo_tarefas_individuais(rel,after)
   with self.subTest(module=n):
    # 01/11/2026: só a política de carregamento da fonte muda, sem trocar o recurso.
    self.assertEqual(re.findall(r'\bhref="([^"]*)"',before.replace('display=swap','display=optional')),[x for x in re.findall(r'\bhref="([^"]*)"',after) if 'cartaz-indices.css' not in x])
    ids=lambda s:re.findall(r'\bid="([^"]*)"',s)
    self.assertEqual(ids(before),[x for x in ids(after) if x!='cz-index-route'])
    data=lambda s:json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
    self.assertEqual(data(before),data(after))
    self.assertEqual(re.findall(r'localStorage\.[\s\S]{0,150}',before),re.findall(r'localStorage\.[\s\S]{0,150}',after))
    self.assertEqual(re.findall(r'<img\b[^>]*>',before),re.findall(r'<img\b[^>]*>',after))
 def test_m4_conserva_as_tres_provas_do_149(self):
  # 02/11/2026: comparar as três provas com o histórico aprovado, agora aplicado no lote 2.
  from test_pendentes_camada_149_20261101 import APROVADAS_CAMADA_149_20261101
  proofs=lambda s:re.findall(r'<p class="prova-esperada">(.*?)</p>',s)
  expected=[proofs(e['novo'])[0] for e in APROVADAS_CAMADA_149_20261101 if e['local'].startswith('M4 unidade')]
  self.assertEqual(proofs((ROOT/'m4/index.html').read_text('utf8')),expected)
  self.assertEqual(len(expected),3)
 def test_uma_prova_e_uma_dobra_aberta_por_unidade(self):
  for n in range(1,10):
   s=(ROOT/f'm{n}/index.html').read_text('utf8');units=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
   self.assertEqual(s.count('<p class="prova-esperada">'),len(units))
   self.assertEqual(len(re.findall(r'<details class="cz-fold"[^>]*\bopen>',s)),len(units))
   # 02/11/2026: decisão 134 (docente). Sem a caixa «A seguir»: um só botão de continuar, simples, sem título nem linha de estado.
   self.assertEqual(s.count('<div class="module-entry"><a class="cz-button primary" data-module-next'),1)
   self.assertEqual(s.count('class="module-entry cz-next"'),0);self.assertNotIn('<h2>A seguir</h2>',s);self.assertNotIn('cz-index-status',s)
   # 01/11/2026: a banda fechada identifica a unidade, além do seu número.
   names=re.findall(r'<span class="cz-fold-t">(.*?)</span>',s)
   self.assertEqual(len(names),len(units))
   self.assertTrue(all(re.sub('<[^>]+>','',name).strip() for name in names))
 def test_adaptador_nao_grava_progresso_e_reutiliza_o_motor(self):
  s=(ROOT/'assets/cartaz-indices.js').read_text('utf8')
  self.assertNotRegex(s,r'(?:localStorage|sessionStorage)\.(?:setItem|removeItem|clear)')
  self.assertIn('EPIUnitTaskRoute.lessonDone(step)',s)
  self.assertIn('previous.get(step.id)===false&&done',s)
  self.assertNotIn('setAttribute("href"',s)
 def test_camada_aplicada_e_reversivel(self):
  # 02/11/2026: desfaz antes a camada das tarefas individuais, a mais recente.
  r=subprocess.run([sys.executable,'scripts/aplicar_trocas.py','scripts/cartaz_indices_20261101.json','--manifesto','tests/fixtures/cartaz-indices-edits-20261101.json','--verificar','--desfazer-antes', 'tests/fixtures/creditos-grafismos-ia-edits-20261102.json', '--desfazer-antes', 'tests/fixtures/conteudos-lote2-edits-20261101.json', '--desfazer-antes', 'tests/fixtures/varredura-formatacao-edits-20261101.json', '--desfazer-antes', 'tests/fixtures/calcada-mar-edits-20261102.json','--desfazer-antes','tests/fixtures/tarefas-individuais-edits-20261102.json'],cwd=ROOT,capture_output=True,text=True,encoding='utf8')
  self.assertEqual(r.returncode,0,r.stdout+r.stderr)
 def test_so_nove_paginas_migram_sobre_a_base_integrada(self):
  # 01/11/2026: o manifesto delimita a camada, sem depender de commits após squash.
  files=json.loads((ROOT/'tests/fixtures/cartaz-indices-edits-20261101.json').read_text('utf8'))['files']
  self.assertEqual(sorted(files),[f'm{n}/index.html' for n in range(1,10)])
 def test_rota_do_adaptador_coincide_com_motor(self):
  # 01/11/2026: uma lição nova no motor tem de entrar também no adaptador.
  for n in range(1,10):
   s=(ROOT/f'm{n}/index.html').read_text('utf8')
   units=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
   route=json.loads(re.search(r'<script type="application/json" id="cz-index-route">(.*?)</script>',s,re.S)[1])
   expected=[{'n':u['n'],'passos':[{k:p[k] for k in ('id','licao','exs') if k in p} for p in u['passos']]} for u in units]
   self.assertEqual(route,expected,n)
 def test_o_carrossel_antigo_nao_apaga_o_ambito_novo(self):
  for n in range(1,10):
   s=(ROOT/f'm{n}/index.html').read_text('utf8')
   self.assertIn("[data-cartaz]:not([data-cartaz='2']):not([data-cz-feito])",s)
if __name__=='__main__':unittest.main()
