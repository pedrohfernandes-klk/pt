"""02/11/2026: contratos do piloto visual M4, sem relaxar o conteúdo publicado."""
import hashlib,json,re,subprocess,sys,unittest
from html.parser import HTMLParser
from pathlib import Path
from auditoria_20261028 import undo_m4_piloto
# 05/11/2026: para desfazer, antes do piloto, só a camada da decisão 154, que muda o m4/index.html por cima dele.
from auditoria_20261028 import undo_autonomia_0511
# 06/11/2026: decisão 148, o desenho comum dos nove índices fica por cima do piloto; estes contratos são os da camada do piloto.
from auditoria_20261028 import undo_cartaz_148_0611
ROOT=Path(__file__).resolve().parents[1]
class Inventory(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.scripts=[];self.in_script=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag=='script':self.in_script=True;self.scripts.append([a,''])
 def handle_endtag(self,tag):
  if tag=='script':self.in_script=False
 def handle_data(self,text):
  if self.in_script:self.scripts[-1][1]+=text
class M4Piloto(unittest.TestCase):
 def setUp(self):
  # 05/11/2026: a decisão 154 muda o passo 16 do percurso do M4, dentro de um bloco do piloto; desfaz-se só essa camada
  # antes do piloto, com contagem estrita, e as conferências continuam a olhar para a página publicada.
  # 06/11/2026: decisão 148. O desenho comum dos nove índices (camada cartaz_indices_148_20261106) muda o m4/index.html por cima
  # do piloto; o «depois» destes contratos é a página com essa camada desfeita (contagem estrita), e o «antes» continua a ser a
  # página sem o piloto. O desenho comum confere-se em tests/test_cartaz_indices_148.py, nos nove índices.
  current=(ROOT/'m4/index.html').read_text('utf-8')
  self.after=undo_cartaz_148_0611('m4/index.html',current);self.before=undo_m4_piloto('m4/index.html',undo_autonomia_0511('m4/index.html',current))
 def test_conserva_ids_ligacoes_scripts_e_dados(self):
  a,b=Inventory(self.before),Inventory(self.after)
  self.assertEqual(sorted(a.ids),sorted(b.ids));self.assertEqual(sorted(a.links),sorted(b.links))
  self.assertEqual(a.scripts,[x for x in b.scripts if 'cartaz-m4-piloto.js' not in x[0].get('src','')])
  self.assertEqual(re.findall(r'<p class="prova-esperada">(.*?)</p>',self.before),re.findall(r'<p class="prova-esperada">(.*?)</p>',self.after))
 def test_reversao_exata_e_idempotencia(self):
  manifest=json.loads((ROOT/'tests/fixtures/cartaz-m4-piloto-edits-20261102.json').read_text('utf-8'))
  self.assertEqual(list(manifest['files']),['m4/index.html'])
  self.assertEqual(hashlib.sha256(self.before.encode()).hexdigest(),manifest['files']['m4/index.html']['base_sha256_lf'])
  # 05/11/2026: a decisão 154 (camada autonomia_154_20261105) é a camada mais recente e muda o m4/index.html; as camadas
  # por cima do piloto desfazem-se antes, da mais recente para a mais antiga, como em scripts/verificar_camadas.py, com a
  # mesma exigência.
  # 06/11/2026: o desenho comum dos nove índices (decisão 148) muda o m4/index.html por cima de tudo; desfaz-se primeiro, com a
  # mesma exigência.
  # 07/11/2026: os três acertos dos índices deixados pela decisão 173 são a camada mais recente, por cima do desenho comum dos nove índices; desfazem-se primeiro, com a mesma exigência.
  # 07/11/2026: os créditos atrás de um «i» do pedido pt-1 (camada creditos_i_pt1_20261107) passam a camada mais recente e mudam o m4/index.html (a imagem documental); desfazem-se primeiro, com a mesma exigência.
  # 08/11/2026: o cartaz «Ler a cidade» na entrada e o nome novo da secção nas páginas publicadas (cidade_cartaz_20261108) passam a camada mais recente, por cima dos créditos atrás de um «i» do pedido pt-1 (e mudam páginas desta cadeia: a entrada, os índices e a frase da sugestão «continua»); desfazem-se primeiro, com a mesma exigência.
  # 08/11/2026: a decisão 152 no M2 (cuidado_m2_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M2, incluindo o índice do módulo) passa a camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção; desfaz-se primeiro, com a mesma exigência.
  # 08/11/2026: a decisão 152 no M3 (cuidado_m3_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M3, incluindo o índice, o guia e o mapa do módulo) passa a camada mais recente, por cima da decisão 152 no M2; desfaz-se primeiro, com a mesma exigência.
  # 08/11/2026: a decisão 152 no M4 (cuidado_m4_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M4, incluindo o índice, o guia, o mapa e o portefólio do módulo) passa a camada mais recente, por cima da decisão 152 no M3; desfaz-se primeiro, com a mesma exigência.
  # 08/11/2026: a decisão 152 no M5 (cuidado_m5_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M5, incluindo o índice, o guia, o mapa e o portefólio do módulo, e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M4; desfaz-se primeiro, com a mesma exigência.
  # 08/11/2026: a decisão 152 no M6 (cuidado_m6_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M6, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M5; desfaz-se primeiro, com a mesma exigência.
  # 11/11/2026: a decisão 152 no M7 (cuidado_m7_20261111: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M7, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo», «Olhar» e «Pensar devagar», e nas tarefas, nos aquecimentos e na grelha das suas unidades) passa a camada mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com a mesma exigência.
  # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
  # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M9, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», as atividades e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com a mesma exigência.
  # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
  run=subprocess.run([sys.executable,'scripts/aplicar_trocas.py','scripts/cartaz_m4_piloto_20261102.json','--manifesto','tests/fixtures/cartaz-m4-piloto-edits-20261102.json','--verificar','--desfazer-antes','tests/fixtures/cuidado-exame-edits-20261112.json','--desfazer-antes','tests/fixtures/cuidado-m9-edits-20261112.json','--desfazer-antes','tests/fixtures/cuidado-m8-edits-20261112.json','--desfazer-antes','tests/fixtures/cuidado-m7-edits-20261111.json','--desfazer-antes','tests/fixtures/cuidado-m6-edits-20261108.json','--desfazer-antes','tests/fixtures/cuidado-m5-edits-20261108.json', '--desfazer-antes','tests/fixtures/cuidado-m4-edits-20261108.json', '--desfazer-antes','tests/fixtures/cuidado-m3-edits-20261108.json', '--desfazer-antes','tests/fixtures/cuidado-m2-edits-20261108.json', '--desfazer-antes','tests/fixtures/cidade-cartaz-edits-20261108.json', '--desfazer-antes','tests/fixtures/creditos-i-pt1-edits-20261107.json','--desfazer-antes','tests/fixtures/indices-acertos-edits-20261107.json','--desfazer-antes','tests/fixtures/cartaz-indices-148-edits-20261106.json','--desfazer-antes','tests/fixtures/autonomia-154-edits-20261105.json','--desfazer-antes','tests/fixtures/exame-contexto-edits-20261105.json','--desfazer-antes','tests/fixtures/exame-licao-edits-20261105.json','--desfazer-antes','tests/fixtures/tabela-movimentos-edits-20261105.json','--desfazer-antes','tests/fixtures/revisao-edits-20261105.json','--desfazer-antes','tests/fixtures/cartaz-cabecalho-edits-20261103.json'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
  self.assertEqual(run.returncode,0,run.stdout+run.stderr)
 def test_adesao_exclusiva_e_sem_novo_motor(self):
  for n in range(1,10):
   # 06/11/2026: decisão 148. A exclusividade é a da camada do piloto: lê-se cada índice com o desenho comum desfeito.
   text=undo_cartaz_148_0611(f'm{n}/index.html',(ROOT/f'm{n}/index.html').read_text('utf-8'))
   self.assertEqual('data-m4-piloto=' in text,n==4)
   self.assertEqual('cartaz-m4-piloto.css' in text,n==4)
  js=(ROOT/'assets/cartaz-m4-piloto.js').read_text('utf-8')
  self.assertNotRegex(js,r'(?:localStorage|sessionStorage)|MutationObserver|innerHTML')
  self.assertNotIn('!important',(ROOT/'assets/cartaz-m4-piloto.css').read_text('utf-8'))
 def test_titulos_e_controlo_comum_com_destino_explicito(self):
  self.assertEqual(len(re.findall(r'<h2 class="cz-fold-t" id="unidade-pedagogica-[123]">',self.after)),3)
  self.assertEqual(self.after.count('data-appearance-control=""'),1)
  self.assertEqual(self.after.count('class="teacher-access"'),1)
  self.assertNotIn('style="position:fixed;left:12px;bottom:64px',self.after)
if __name__=='__main__':unittest.main()
