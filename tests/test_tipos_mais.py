"""02/11/2026: contratos de F2; os limites são exercitados, não normalizados."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from tipos_regras import validar,textos_de,verificar_recursos,ENTROU
CARDS=json.loads((ROOT/'tests/fixtures/tipos-mais-ensaio.json').read_text('utf8'))

class TiposMais(unittest.TestCase):
 def c(self,t):return copy.deepcopy(next(c for c in CARDS if c['t']==t))
 def test_seis_formatos_sem_mutacao(self):
  for c in CARDS:
   before=copy.deepcopy(c)
   for ctx in ('licao','nucleo','projecao','aquecimento'):self.assertEqual(validar(c,ctx),[],(c['t'],ctx))
   self.assertEqual(c,before)
 def test_chaves_de_ajuda_e_identificadores(self):
  import subprocess
  code="const vm=require('vm'),fs=require('fs');const s={window:{},Map,WeakMap};vm.runInNewContext(fs.readFileSync('assets/pt-lessons/tipos-mais.js','utf8'),s);console.log(JSON.stringify(Object.fromEntries(Object.entries(s.window.EPITipos).map(([t,d])=>[t,d.como]))));"
  r=subprocess.run(['node','-e',code],cwd=ROOT,capture_output=True,text=True,encoding='utf8')
  self.assertEqual(r.returncode,0,r.stderr)
  self.assertEqual(json.loads(r.stdout),dict(lacunas='completar-texto',varias='escolher-certas',montar='montar-frase',intruso='intruso',razao='escolher-com-razao',corrigir='corrigir-erro'))
  c=self.c('lacunas');c['id']='temporario';self.assertTrue(validar(c))
 def test_lacunas_retornos_dependem_do_espaco(self):
  c=self.c('lacunas');del c['fe_bloco']['embora']['2'];self.assertTrue(validar(c))
  c['fe_bloco']['embora']['*']='Relê a oposição.';self.assertEqual(validar(c),[])
  c['texto']=c['texto'].replace('[2]','[1]');self.assertTrue(validar(c))
 def test_lacunas_limite_contexto_e_aceites(self):
  c=self.c('lacunas');c['texto']=' '.join(['palavra']*41)+' [1] [2]'
  self.assertEqual(validar(c),[]);self.assertTrue(validar(c,'aquecimento'))
  c['aceita']={'1':['fantasma']};self.assertTrue(validar(c))
 def test_varias_exige_subconjunto_e_retornos(self):
  for cs in ([0],[0,1,2,3],[0,0],[True,2],[0,9]):
   c=self.c('varias');c['certas']=cs;self.assertTrue(validar(c),cs)
  c=self.c('varias');c['fe'][1]='';self.assertTrue(validar(c))
 def test_montar_maiusculas_fim_e_ordens(self):
  c=self.c('montar');c['blocos'][2]='Vi';self.assertTrue(validar(c))
  c['blocos'][2]='vi';del c['fim'];self.assertTrue(validar(c))
  c=self.c('montar');c['aceita']=[[0,1,1,3]];self.assertTrue(validar(c))
  c=self.c('montar');c['aceita']=[[[3,0,1,2],'Ontem, não o vi.']];self.assertEqual(validar(c),[])
 def test_intruso_sem_criterio_na_pergunta(self):
  c=self.c('intruso');c['p']='Que elemento pede complemento?';self.assertTrue(validar(c))
 def test_imagens_exigem_licenca_e_credito(self):
  c=self.c('intruso');c['itens']=[{'img':'a.svg','alt':'Descrição visível','autor':'Autor','obra':'Obra','data':'1900','origem':'https://museu.example/obra','licenca':'CC BY-SA 4.0'} for _ in range(4)]
  self.assertEqual(validar(c),[])
  for k in ('autor','obra','data','origem','licenca','alt'):
   bad=copy.deepcopy(c);del bad['itens'][0][k];self.assertTrue(validar(bad),k)
  c['itens'][0]['licenca']='CC BY-NC 4.0';self.assertTrue(validar(c))
 def test_razao_nao_repete_leitura(self):
  c=self.c('razao');c['razoes'][0]='O texto diz que escolheu.';self.assertTrue(validar(c))
 def test_corrigir_indices_e_armadilhas(self):
  for index in (-1,100,True):
   c=self.c('corrigir');c['erros'][0]['em']=index;self.assertTrue(validar(c))
  c=self.c('corrigir');c['armadilhas']['0']='Não é uma armadilha.';self.assertTrue(validar(c))
  c=self.c('corrigir');c['erros'][0]['o'][1]='Á';self.assertTrue(validar(c))
 def test_dados_malformados_nao_passam_nem_lancam(self):
  for c in CARDS:
   for key in c:
    if key in ('p','id','f','t'):continue
    for value in (None,False,42):
     bad=copy.deepcopy(c);bad[key]=value
     if key=='diz_quantas' and value is False:
      self.assertEqual(validar(bad),[])
     else:self.assertTrue(validar(bad),(c['t'],key,value))
 def test_extracao_inclui_erros_modelos_e_variantes(self):
  c=self.c('lacunas');c['p2']='Variante a ler';c['fe_bloco']['embora']['2']='Sentinela única'
  self.assertIn('Sentinela única',textos_de(c));self.assertIn('Variante a ler',textos_de(c))
  c=self.c('corrigir');self.assertIn('houvesse',textos_de(c));self.assertIn(c['erros'][0]['fe'],textos_de(c))
  self.assertNotIn(c['id'],textos_de(c))
 def test_recurso_em_falta_versao_e_ordem(self):
  html='<link href="tipos-mais.css?v=20261102-f2"><script src="tipos-mais.js?v=20261102-f2"></script><script>EPIJogo.montar({})</script>'
  self.assertEqual(verificar_recursos(html,CARDS),[])
  self.assertTrue(verificar_recursos(html.replace('tipos-mais.js','outro.js'),CARDS))
  self.assertTrue(verificar_recursos(html.replace('20261102-f2','20251001'),CARDS))
  self.assertTrue(verificar_recursos('<script>EPIJogo.montar({})</script>'+html,CARDS))
  self.assertEqual(verificar_recursos('',[{'t':'escolha'}]),[])

class Consumidores(unittest.TestCase):
 def test_medicao_continua_executavel_pela_linha_de_comandos(self):
  # 03/11/2026: importar o módulo não exercita a descrição usada por argparse.
  import subprocess
  r=subprocess.run([sys.executable,str(ROOT/'scripts/medir_opcoes.py'),'--help'],capture_output=True,text=True,encoding='utf8')
  self.assertEqual(r.returncode,0,r.stderr)
  self.assertIn('--regra',r.stdout)
 def test_papel_sem_solucoes_e_sem_mutacao(self):
  from tipos_regras import material_publico,material_html
  forbidden={'certas','certos','espacos','erros','armadilhas','fe','fe_item','fe_razao','fe_ordem','fe_bloco','aceita'}
  for c in CARDS:
   before=copy.deepcopy(c);m=material_publico(c,'ensaio')
   self.assertFalse(set(m)&forbidden,c['t']);self.assertEqual(c,before)
   self.assertNotIn(c['f'],material_html(c,'ensaio'))
   if c['t']=='montar':self.assertNotEqual(m['banco'],c['blocos'])
  c=copy.deepcopy(CARDS[0]);c['texto']='<script>alert(1)</script> [1] [2]'
  self.assertNotIn('<script>',material_html(c));self.assertIn('&lt;script&gt;',material_html(c))
 def test_audit_valida_ids_e_contexto(self):
  from audit_cards import validate_cards
  self.assertEqual(validate_cards(CARDS),[])
  self.assertTrue(validate_cards(CARDS+[CARDS[0]]))
  c=copy.deepcopy(CARDS[0]);c['texto']=' '.join(['palavra']*41)+' [1] [2]'
  self.assertEqual(validate_cards([c]),[]);self.assertTrue(validate_cards([c],'aquecimento'))
 def test_as_duas_medicoes_incluem_todos_os_conjuntos(self):
  from tipos_regras import campos_opcoes
  from medir_opcoes import itens
  from opcoes_equilibradas import perguntas_adicionais
  for c in CARDS:
   sets=campos_opcoes(c)
   self.assertEqual(len(list(itens(c))),len(sets),c['t'])
   self.assertEqual(len(perguntas_adicionais(c)),sum(len(g['certas']) for g in sets if len(g['certas'])<len(g['opcoes'])))
 def test_gerador_carrega_pecas_antes_do_motor_so_quando_usadas(self):
  from aquecimentos import pagina
  d=json.loads((ROOT/'docs/pedagogia/aquecimentos/m1-u1.json').read_text('utf8'))
  self.assertNotIn('tipos-mais.js',pagina(ROOT,d))
  d['cartoes']=copy.deepcopy(CARDS)
  html=pagina(ROOT,d)
  self.assertLess(html.index('tipos-mais.js'),html.index('pt-lessons/jogo.js'))
  self.assertEqual(verificar_recursos(html,d['cartoes']),[])
 def test_sala_historica_igual_e_material_novo_sem_gabarito(self):
  import desligar_sala as D
  self.assertEqual(D.painel_js('{}'),D.PAINEL_MATERIAL_JS)
  for c in CARDS:
   m=D.material_de('ensaio',0,c,'ensaio')
   self.assertEqual(m['f'],c['f']);self.assertNotIn(c['f'],m['adicional_html'])
   self.assertIn('m.adicional_html',D.painel_js(json.dumps({'0':m})))
 def test_extracao_expoe_lingua_tambem_nos_retornos(self):
  from test_lingua_perguntas import QUAL_NOME
  from aquecimentos import PROIBIDAS
  import re
  for c in CARDS:
   for s in textos_de(c):
    self.assertIsNone(QUAL_NOME.search(s),s)
    self.assertFalse(any(re.search(p,s,re.I) for p in PROIBIDAS),s)
  c=copy.deepcopy(CARDS[0]);c['fe_bloco']['embora']['1']='Qual frase explica o jogo?'
  self.assertTrue(any(QUAL_NOME.search(s) for s in textos_de(c)))
  self.assertTrue(any(re.search(r'\bjogo\b',s) for s in textos_de(c)))

if __name__=='__main__':unittest.main()
