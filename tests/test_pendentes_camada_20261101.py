"""01/11/2026: trocas do pt #143 à espera da primeira camada nova depois do #144 e do #145.

O #143 mudava texto em páginas congeladas (M2: a apreciação crítica sem o peso de 25 %; M9: o exercício longo
m9-ver-e-nao-ver com o título «Quem vê mais?», para deixar de repetir o da lição M9-F02) acrescentando trocas à camada
scripts/lingua_pessoa_m7_20261030.json. As revisões de 01/11/2026 mostraram que essa camada já não podia receber trocas:
as páginas congeladas só mudam por uma camada nova de trocas literais, e a camada mais recente está ocupada pelo #144
(tarefas_m356) e pelo #145 (tarefas_m89) enquanto estiverem abertos. Havia também choques concretos: o #145 (e o #148 e o
#150, que o contêm) reescreve as linhas de m9/index.html e de m9/mapa-do-modulo-m9/index.html com «Ver e não ver» no
antigo e no novo, e a camada licoes_m16 do #150 tem no antigo a linha de m2/index.html com «(tarefa de 25 por cento)».

Por isso as trocas saíram da camada (que volta a ser a do main, com o manifesto
tests/fixtures/lingua-pessoa-m7-edits-20261030.json, e scripts/aplicar_trocas.py --verificar confere-a) e ficam aqui,
com o antigo e o novo letra a letra, para entrarem juntas na primeira camada nova depois do #144 e do #145. Saem todas as
do M9 (e não só as duas que chocam), para que o percurso, o mapa e a página do exercício não mostrem títulos diferentes;
e saem as do M2, pela mesma regra. Juntam-se três achados da revisão de língua do #143 fora do diff (mapa do M2 e M2-F09,
na lição e no painel), também em páginas congeladas.

O teste confere que cada troca ainda se aplica à árvore (o antigo está lá as vezes registadas e o novo ainda não), que
cada novo fica único depois de aplicado e que desfazer devolve o texto de partida. Quando a camada nova as aplicar, o teste
falha e pede que se tirem daqui: a lista só diminui.
"""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
CAMADA_LINGUA = ROOT / 'scripts/lingua_pessoa_m7_20261030.json'

# 01/11/2026: trocas do título «Quem vê mais?» (m9-ver-e-nao-ver, m9/index.html, m9/mapa-do-modulo-m9 e
# m9-de-quem-e-o-convento), do M2 sem o peso de 25 % e dos três achados da revisão de língua, à espera da camada a seguir
# ao #144 e ao #145. Mesmo formato de scripts/aplicar_trocas.py; aplicam-se pela ordem da lista, ficheiro a ficheiro.
PENDENTES_CAMADA_20261101 = (
    {
        'ficheiro': 'm2/index.html',
        'local': 'Percurso do M2, linha da lição M2-F08',
        'antigo': 'escreve a apreciação crítica (tarefa de 25 por cento).',
        'novo': 'escreve a apreciação crítica.',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10: a apreciação crítica deixou de ser tarefa de 25 % (a unidade 2 leva a «Dois anúncios de casamento»).',
    },
    {
        'ficheiro': 'm2/licao-m2-f08/index.html',
        'local': 'M2-F08, cartão do juízo',
        'antigo': 'cortas o que repete e assinas (vale 25 %).',
        'novo': 'cortas o que se repete e assinas.',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10: sem o peso de 25 %.',
    },
    {
        'ficheiro': 'm2/licao-m2-f08/index.html',
        'local': 'M2-F08, pistas',
        'antigo': 'cortas o que repete, assinas: vale 25 por cento.',
        'novo': 'cortas o que se repete e, no fim, assinas.',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10: sem o peso de 25 %.',
    },
    {
        'ficheiro': 'm9/m9-ver-e-nao-ver/index.html',
        'local': 'Exercício longo do M9, título',
        'antigo': '<title>Ver e não ver · Português · Módulo 9</title>',
        'novo': '<title>Quem vê mais? · Português · Módulo 9</title>',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10: o exercício longo tinha o mesmo título da M9-F02; passa a «Quem vê mais?», a pergunta com que abre.',
    },
    {
        'ficheiro': 'm9/m9-ver-e-nao-ver/index.html',
        'local': 'Exercício longo do M9, h1',
        'antigo': '<h1 class="c-sr">Ver e não ver',
        'novo': '<h1 class="c-sr">Quem vê mais?',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10.',
    },
    {
        'ficheiro': 'm9/m9-ver-e-nao-ver/index.html',
        'local': 'Exercício longo do M9, migalhas',
        'antigo': 'Estás em: Ver e não ver',
        'novo': 'Estás em: Quem vê mais?',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10.',
    },
    {
        'ficheiro': 'm9/m9-ver-e-nao-ver/index.html',
        'local': 'Exercício longo do M9, título do baralho',
        'antigo': 'titulo:"Ver e não ver",itens',
        'novo': 'titulo:"Quem vê mais?",itens',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10.',
    },
    {
        'ficheiro': 'm9/m9-ver-e-nao-ver/index.html',
        'local': 'Exercício longo do M9, cartão «Abre»',
        'antigo': '"rot":"Abre","titulo":"Ver e não ver"',
        'novo': '"rot":"Abre","titulo":"Quem vê mais?"',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10.',
    },
    {
        'ficheiro': 'm9/index.html',
        'local': 'Percurso do M9, linha do exercício longo',
        'antigo': '<span class="t">Ver e não ver</span><span class="s">Pensar devagar:',
        'novo': '<span class="t">Quem vê mais?</span><span class="s">Pensar devagar:',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10.',
    },
    {
        'ficheiro': 'm9/mapa-do-modulo-m9/index.html',
        'local': 'Mapa do M9, ligação ao exercício longo',
        'antigo': '<a href="../m9-ver-e-nao-ver/">Ver e não ver</a>',
        'novo': '<a href="../m9-ver-e-nao-ver/">Quem vê mais?</a>',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10.',
    },
    {
        'ficheiro': 'm9/m9-de-quem-e-o-convento/index.html',
        'local': 'Outro exercício longo do M9, ligação',
        'antigo': 'm9-ver-e-nao-ver/\\">Ver e não ver</a>',
        'novo': 'm9-ver-e-nao-ver/\\">Quem vê mais?</a>',
        'ocorrencias': 1,
        'achado': 'Achado do GPT 1 (plano de 31/10/2026, parte 3), corrigido por decisão do docente de 31/10.',
    },
    {
        'ficheiro': 'm2/mapa-do-modulo-m2/index.html',
        'local': 'Mapa do M2, «As tarefas do Teams» e «Como se avalia»',
        'antigo': '<details class="sec" id="tarefas"><summary>As tarefas do Teams</summary><div class="tarefa"><span class="tn">1</span><div><b>Apreciação crítica da Farsa de Inês Pereira no teatro</b><span class="peso">25 %, individual</span><span class="crit">Descrição e juízo; Provas; Língua e género; Respostas das unidades (percurso)</span></div></div><div class="tarefa"><span class="tn">2</span><div><b>Recontagem contemporânea da farsa em vídeo</b><span class="peso">25 %, em grupo</span><span class="crit">Fidelidade e escolha; A cena assinada; Produção e apresentação</span></div></div><div class="tarefa"><span class="tn">3</span><div><b>Dois anúncios de casamento</b><span class="peso">25 %, em grupo de 2 ou 3</span><span class="crit">Marcas da farsa; Registo e contraste; Limite, áudio e grupo</span></div></div><p class="aval"><b>Como se avalia:</b> três tarefas no Teams (25 % cada), provas rápidas (10 %, média das três; conta a primeira tentativa) e uma prova escrita de 45 minutos (15 %). <b>Em papel:</b> a Revisão 1, a Revisão 2 e a prova escrita; tudo o resto está aqui e no Teams.</p></details>',
        'novo': '<details class="sec" id="tarefas"><summary>As tarefas do Teams</summary><p><a href="../../tarefas/m2-u1/">Unidade 1: Duas escolhas, que liberdade?</a>, individual, 90 minutos, 30 %.</p><p><a href="../../tarefas/m2-u2/">Unidade 2: Dois anúncios de casamento</a>, individual, 90 minutos, 30 %.</p><p class="aval"><b>Como se avalia:</b> tarefa da Unidade 1, 30 %; tarefa da Unidade 2, 30 %; provas rápidas, 10 %; prova escrita, 30 %. Cada tarefa tem uma grelha /20. Na primeira recuperação, fazes a tarefa da unidade em falta, com a mesma grelha /20. <b>Em papel:</b> a Revisão 1, a Revisão 2 e a prova escrita; tudo o resto está aqui e no Teams.</p></details>',
        'ocorrencias': 1,
        'achado': 'Revisão de língua do pt #143 (01/11/2026), fora do diff: o mapa ainda dá a apreciação crítica como tarefa de 25 % e «três tarefas no Teams (25 % cada) … prova escrita de 45 minutos (15 %)»; a decisão 20 dá 30 + 30 + 10 + 30, com as duas tarefas de unidade.',
    },
    {
        'ficheiro': 'm2/licao-m2-f09/index.html',
        'local': 'M2-F09, retorno do completar do vídeo',
        'antigo': 'apresentação oral: segunda tarefa de avaliação, 25 por cento.',
        'novo': 'apresentação oral: um extra sem nota.',
        'ocorrencias': 1,
        'achado': 'Revisão de língua do pt #143 (01/11/2026), fora do diff: «segunda tarefa de avaliação, 25 por cento»: a recontagem em vídeo já não é tarefa avaliada.',
    },
    {
        'ficheiro': 'm2/painel-m2-f09/index.html',
        'local': 'Painel da M2-F09, material do completar do vídeo',
        'antigo': 'apresentação oral: segunda tarefa de avaliação, 25 por cento.',
        'novo': 'apresentação oral: um extra sem nota.',
        'ocorrencias': 1,
        'achado': 'Revisão de língua do pt #143 (01/11/2026), fora do diff: a mesma frase da M2-F09, copiada no material do painel.',
    },
)
# 01/11/2026: a lista só pode diminuir; este número desce quando a camada nova aplicar as trocas.
MAXIMO_PENDENTES = 14


class TrocasPendentes(unittest.TestCase):
    def test_formato(self):
        # 01/11/2026: as mesmas chaves de scripts/aplicar_trocas.py, com o novo diferente do antigo e sem travessão.
        for t in PENDENTES_CAMADA_20261101:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'}, t.get('local'))
            self.assertTrue(t['novo'] and t['novo'] != t['antigo'], t['local'])
            self.assertGreaterEqual(t['ocorrencias'], 1, t['local'])
            self.assertNotIn('\u2014', t['novo'], t['local'])
            self.assertTrue((ROOT / t['ficheiro']).is_file(), t['ficheiro'])

    def test_a_lista_so_diminui(self):
        # 01/11/2026: nada entra nesta lista depois de hoje; o que precisar da camada vai para uma lista nova e datada.
        self.assertLessEqual(len(PENDENTES_CAMADA_20261101), MAXIMO_PENDENTES)

    def test_ainda_se_aplicam(self):
        # 01/11/2026: cada antigo ainda está na árvore as vezes registadas, cada novo ainda não; aplicadas pela ordem, cada
        # novo fica único (ocorrencias vezes) e desfazê-las, da última para a primeira, devolve o texto de partida.
        por_ficheiro = {}
        for t in PENDENTES_CAMADA_20261101:
            por_ficheiro.setdefault(t['ficheiro'], []).append(t)
        for ficheiro, trocas in por_ficheiro.items():
            base = (ROOT / ficheiro).read_text('utf-8')
            texto = base
            for t in trocas:
                if texto.count(t['novo']) == t['ocorrencias'] and t['antigo'] not in texto:
                    self.fail(f"{ficheiro}: {t['local']} já está aplicada; tira-a de PENDENTES_CAMADA_20261101")
                self.assertEqual(texto.count(t['antigo']), t['ocorrencias'], f"{ficheiro}: {t['local']} (antigo)")
                self.assertEqual(texto.count(t['novo']), 0, f"{ficheiro}: {t['local']} (o novo já existe)")
                texto = texto.replace(t['antigo'], t['novo'])
                self.assertEqual(texto.count(t['novo']), t['ocorrencias'], f"{ficheiro}: {t['local']} (novo único)")
            for t in reversed(trocas):
                texto = texto.replace(t['novo'], t['antigo'])
            self.assertEqual(texto, base, ficheiro)

    def test_fora_da_camada_da_lingua(self):
        # 01/11/2026: nenhuma destas trocas fica na camada lingua_pessoa_m7, que está como no main.
        camada = json.loads(CAMADA_LINGUA.read_text('utf-8'))
        pares = {(t['ficheiro'], t['antigo']) for t in camada} | {(t['ficheiro'], t['novo']) for t in camada}
        for t in PENDENTES_CAMADA_20261101:
            self.assertNotIn((t['ficheiro'], t['antigo']), pares, t['local'])
            self.assertNotIn((t['ficheiro'], t['novo']), pares, t['local'])


if __name__ == '__main__':
    unittest.main()
