"""05/11/2026: decisão 154 do docente, «os exercícios fazem-se sozinho»: todo o exercício, atividade, tarefa ou cartão que o
aluno lê faz-se sozinho, a qualquer hora; nenhuma instrução para o aluno depende de o docente estar presente; quando o único
caminho para acabar precisava de um colega ou da turma, fica um caminho a sós, curto. A decisão 146 mantém-se: o momento
«em turma» pode ficar, como opção de aula, entre parênteses («na aula, …») ou ao lado de uma gravação.

Camada literal autonomia_154_20261105 (scripts/autonomia_154_20261105.json, manifesto
tests/fixtures/autonomia-154-edits-20261105.json), a mais recente, por cima do contexto do Laboratório do exame. As tarefas e
o aquecimento gerados mudam nos dados dos geradores (docs/pedagogia/tarefas-escolha e docs/pedagogia/aquecimentos/m4-u2.json),
que também estão na camada, e regeneram-se sem diferenças.

Este teste confere que nenhuma das passagens mudadas guarda a dependência antiga e que cada texto novo está lá, com a
contagem exata."""
from pathlib import Path
import json
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'scripts/autonomia_154_20261105.json').read_text('utf-8'))
MANIFESTO = ROOT / 'tests/fixtures/autonomia-154-edits-20261105.json'

# O que punha o exercício a depender do docente, de um colega, da turma ou da aula.
DEPENDENCIA_ANTIGA = re.compile(
    r'(?i)docente|professor|colega|turma|\bdupla\b|\bpares\b|braço no ar|outra pessoa|alguém|na aula|em aula|da aula|'
    r'com papéis|\bEscolham\b|apresentação|debate|te fizeram')
# O que não pode ficar no texto novo, fora do momento de aula opcional. «alguém» fica permitido: é qualquer pessoa, a
# qualquer hora (M3-F04, protótipo mostrado a alguém; M7-F34, «Relê ou mostra a alguém»).
# «outra pessoa» só como dependência (não em «como se fosses outra pessoa», que se faz a sós); «interturmas» é o nome do
# torneio, não a turma.
DEPENDENCIA_NOVA = re.compile(
    r'(?i)docente|professor|\bcolegas?\b|\bturmas?\b|\bdupla\b|\bpares\b|braço no ar|(?<!fosses )outra pessoa|na aula|em aula|da aula|'
    r'com papéis|\bEscolham\b|apresentação pelo|5 minutos de apresentação|debate|te fizeram')
# O momento de aula opcional: entre parênteses, ou ao lado de uma gravação.
OPCIONAL = re.compile(r'\([^()]*\)|numa gravação ou na aula|gravada ou na aula')
# Trocas que só acompanham outra (versões dos ficheiros JS e a pergunta do cartão no painel do docente) ou que tornam
# explícito o caminho a sós de uma pergunta que antes só alguém fazia.
ACOMPANHAMENTO = {
    'Versão do tpc-entrada.js, para os navegadores não usarem a cópia antiga',
    'Versões do atlas-editorial.js e do atlas-explorar.js, para os navegadores não usarem a cópia antiga',
    'Versão do atlas-explorar.js, para os navegadores não usarem a cópia antiga',
    'Painel da M8-F09, pergunta do cartão «completar» (seletor e lista): como se escolhem as três imagens',
    'Enunciado: responde a uma pergunta, feita ou prevista',
    'Rubrica «Apresentação», nível de topo: pergunta feita ou prevista',
}
# 05/11/2026: correções da revisão. Trocas em que a dependência antiga não tem uma marca que DEPENDENCIA_ANTIGA apanhe
# (os retornos da M3-F11 que punham a leitura em voz alta como regra, a alternativa «em sala» do Atlas, o rótulo «Rever em
# conjunto» da M4-F28) ou que só tiram a repetição criada por outra troca (o segundo bloco de leitura da M4-U3). O antigo
# tem de trazer a marca implícita (MARCA_IMPLICITA), e o texto novo confere-se como o de todas as outras trocas.
SEM_MARCA_NO_ANTIGO = {
    'Investigação «O poema muda quando ganha voz?», entrada «Escuta»: sem áudio, lês tu a frase de duas maneiras',
    'Retorno das lacunas «O que muda se não houver conferência?» (lição e cópia do painel): a pergunta faz-se por escrito',
    'Arquivo do índice, retorno das lacunas «O que muda se não houver conferência?»: a pergunta faz-se por escrito',
    'Retorno do verdadeiro ou falso sobre a pergunta em público (lição e cópia do painel): sem conferência, por escrito',
    'Retorno de erro do verdadeiro ou falso sobre a pergunta em público: sem conferência, por escrito',
    'M4-F28, rótulo do cartão «Rever em conjunto»: «Rever a produção», porque o cartão se faz a sós',
    'Apoio de comparação «A palavra contra o poder», organização da aula: o segundo bloco passa a «Preparação na página»',
}
MARCA_IMPLICITA = re.compile(r'voz alta|\bem sala\b|em conjunto|Leitura e preparação')
GERADAS = {
    'tarefas/m1-u1/index.html', 'tarefas/m1-u2/index.html', 'tarefas/m3-u1/index.html', 'tarefas/m3-u2/index.html',
    'tarefas/m5-u1/index.html', 'tarefas/m5-u2/index.html', 'tarefas/m6-u1/index.html', 'tarefas/m6-u2/index.html',
    'tarefas/m7-u3/index.html', 'tarefas/m8-u1/index.html', 'tarefas/m8-u2/index.html', 'tarefas/m9-u1/index.html',
    'tarefas/m9-u2/index.html', 'tarefas/m4-u2/aquecimento/index.html',
}


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


class Autonomia154(unittest.TestCase):
    def test_cada_texto_novo_esta_e_o_antigo_saiu(self):
        # 05/11/2026: correções da revisão: 137 trocas e mais 16 (as trocas antigas que a revisão reescreveu contam uma vez).
        self.assertGreaterEqual(len(TROCAS), 153)
        for troca in TROCAS:
            texto = ler(troca['ficheiro'])
            with self.subTest(ficheiro=troca['ficheiro'], local=troca['local']):
                self.assertEqual(texto.count(troca['novo']), troca['ocorrencias'])
                # o antigo não pode aparecer fora de uma ocorrência do novo
                self.assertEqual(texto.replace(troca['novo'], '\0').count(troca['antigo']), 0)

    def test_nenhuma_passagem_mudada_guarda_a_dependencia_antiga(self):
        for troca in TROCAS:
            with self.subTest(ficheiro=troca['ficheiro'], local=troca['local']):
                if troca['local'] in ACOMPANHAMENTO:
                    continue
                # 05/11/2026: correções da revisão: sem marca no antigo, exige-se a marca implícita; o novo confere-se igual.
                if troca['local'] in SEM_MARCA_NO_ANTIGO:
                    self.assertRegex(troca['antigo'], MARCA_IMPLICITA)
                else:
                    self.assertRegex(troca['antigo'], DEPENDENCIA_ANTIGA)
                sem_opcional = OPCIONAL.sub('', troca['novo'])
                self.assertNotRegex(sem_opcional, DEPENDENCIA_NOVA)

    def test_nada_no_texto_novo_depende_do_docente(self):
        for troca in TROCAS:
            with self.subTest(ficheiro=troca['ficheiro'], local=troca['local']):
                self.assertNotRegex(troca['novo'], r'(?i)docente|professor')

    def test_regras_da_casa_no_texto_novo(self):
        for troca in TROCAS:
            novo = re.sub(r'<[^>]+>', ' ', troca['novo'])
            with self.subTest(ficheiro=troca['ficheiro'], local=troca['local']):
                self.assertNotIn('—', novo)
                self.assertNotIn('·', novo)
                self.assertNotRegex(novo, r'(?i)\bjog(ar|o|os|a|as)\b|\bficha|\bfolha')
                self.assertNotRegex(novo, r'\bQual\s+(?!é\b|foi\b|será\b|era\b)[a-zà-ú]')

    def test_casos_conferidos_a_um_a_um(self):
        # Os textos novos de cada achado, lidos nas páginas, e a dependência que saiu.
        casos = [
            ('m4/index.html', 'Lê em voz alta um discurso de 1915, desmonta-o', 'Ouve o docente ler'),
            ('m4/licao-m4-f14/index.html', '90 minutos: ler em voz alta o discurso de 1915', 'ouvir o docente'),
            ('m3/licao-m3-f11/index.html', 'como Mia Couto no vídeo abaixo. Escreve a tua pergunta (na aula, lê-se em voz alta).', 'O docente traz'),
            ('m3/licao-m3-f11/index.html', '«ouves ou lês como se estivesses na conferência»', 'a turma ouve'),
            ('m3/index.html', 'Se não houver conferência, ouves ou lês um texto com [1] e data, e a pergunta faz-se por [2].', 'o docente traz'),
            ('m3/index.html', 'Prepara perguntas justas, com resposta e fonte, para o torneio interturmas (extra sem nota).', 'Prepara com a turma'),
            ('m3/index.html', '"o":["A ninguém","Aos autores de um manual","A alguém"],"c":2', '"Ao docente","Aos autores'),
            ('m3/licao-m3-f04/index.html', 'protótipo mostrado a alguém', 'protótipo mostrado a um colega'),
            ('m5/index.html', '"frase":"A voz da narração do filme é interpretada por [1]."', 'Vês os episódios que o [1] indicar'),
            # 05/11/2026: correção da revisão: «desenvolve a adaptação», e não «desenvolve-o», que se agarrava a «o conflito».
            ('m2/index.html', '(no projeto de turma, desenvolve a adaptação em vídeo)', 'No projeto de turma, desenvolve a adaptação'),
            ('m2/index.html', 'justifica o conflito que conserva (no projeto de turma, desenvolve a adaptação em vídeo).', 'desenvolve-o em vídeo'),
            ('m2/gram-subordinadas/index.html', 'apresenta-a em três frases, no caderno.', 'a alguém da turma'),
            ('m4/licao-m4-f20/index.html', 'Decide em silêncio. Depois abre os lados.', 'braço no ar'),
            ('m1/licao-m1-f04/index.html', 'Decide em silêncio. Depois abre os três lados.', 'braço no ar'),
            ('m1/licao-m1-f08/index.html', 'Ler a fundo, títulos em papel', 'a pares'),
            ('m1/licao-m1-f15/index.html', 'Ler a fundo, resposta em papel', 'em pares'),
            ('m1/licao-m1-f05/index.html', 'praticar, responder em papel', 'em pares'),
            # 05/11/2026: correção da revisão: uma voz para cada personagem; as didascálias fazem-se como o aluno decidir.
            ('m4/licao-m4-f20/index.html', 'Lê em voz alta, com uma voz para Manuel e outra para Madalena. Decide como fazes as duas didascálias: em voz alta, com som ou com um gesto.', 'com papéis'),
            ('m4/licao-m4-f20/index.html', 'Decide como fazes as duas didascálias', 'Madalena e as duas didascálias. Decide como as fazes'),
            # 05/11/2026: correção da revisão: «compara essa leitura», e não «compara-a», que se referia à cena.
            ('tarefas/m4-u2/index.html', 'lê em voz alta uma cena do ato I e compara essa leitura com a tua leitura silenciosa.', 'lida em voz alta na aula'),
            ('tarefas/m4-u2/index.html', 'lê em voz alta uma cena do ato I e compara essa leitura', 'e compara-a com a tua leitura silenciosa'),
            ('tarefas/m4-u2/aquecimento/index.html', 'Se usares a alternativa de leitura, identifica essa opção.', 'leitura em aula'),
            ('tarefas/m4-u3/index.html', '<span>Leitura do enunciado</span>', 'Apresentação pelo docente'),
            # 05/11/2026: correção da revisão: o segundo bloco deixa de repetir a leitura; os tempos ficam 10, 10, 60 e 10.
            ('tarefas/m4-u3/index.html', '<li><b>10 min</b><span>Leitura do enunciado</span></li><li><b>10 min</b><span>Preparação na página</span></li>', 'Leitura e preparação na página'),
            # 05/11/2026: correção da revisão: «compara essa leitura», e não «compara-a», que se referia à cena.
            ('m4/visita-frei-luis-de-sousa-no-teatro/index.html', 'Lê em voz alta uma cena do Ato I e compara essa leitura com a tua leitura silenciosa', 'lida em voz alta na aula'),
            ('m4/visita-frei-luis-de-sousa-no-teatro/index.html', 'Lê em voz alta uma cena do Ato I e compara essa leitura', 'e compara-a com a tua leitura silenciosa'),
            ('m2/visita-farsa-de-ines-pereira-no-teatro/index.html', 'Lê uma cena em voz alta e escreve a apreciação crítica dessa leitura', 'feita na aula'),
            ('m4/recursos/tpc-entrada.js', 'relê, identifica a tensão e o sinal que a sustenta e revê um ponto pouco claro.', 'um colega identifica'),
            ('m4/recursos/tpc-entrada.js', 'Revê a tua produção (na aula, duas da turma, com autorização de quem as fez):', 'Escolham duas produções'),
            # 05/11/2026: correção da revisão: o rótulo deixa de anunciar trabalho em conjunto; o título fica.
            ('m4/recursos/tpc-entrada.js', '"rot":"Rever a produção · 10 min","titulo":"O que já percebemos da peça?"', 'Rever em conjunto'),
            ('tarefas/m1-u1/index.html', '5 minutos para leres o enunciado', 'para o docente apresentar'),
            ('tarefas/m2-u2/index.html', 'O relógio de produção começa depois da leitura.', 'depois da apresentação'),
            ('tarefas/m8-u1/index.html', 'Depois, lês o enunciado e começam os 60 minutos de produção.', 'o docente apresenta'),
            ('tarefas/m7-u3/index.html', 'Depois, lês a tarefa e começam os 60 minutos de produção.', 'o docente apresenta'),
            ('m6/guia-da-tarefa-m6/index.html', 'Lê o núcleo comum e os temas A e B.', 'O docente apresenta'),
            ('m6/guia-da-tarefa-m6/index.html', 'Seguem-se 5 minutos de leitura, 60 de produção', 'apresentação pelo docente'),
            ('m6/guia-da-tarefa-m6/index.html', 'Apresenta em três minutos, numa gravação ou na aula, e entrega os créditos.', 'Apresenta à turma'),
            ('m8/guia-da-tarefa-m8/index.html', 'Seguem-se 5 minutos de leitura, 60 de produção individual', '5 minutos de apresentação'),
            ('m7/guia-da-tarefa-m7/index.html', 'Os cartões do aquecimento e a leitura da tarefa; na tarefa extra', 'pelo docente'),
            ('m9/guia-da-tarefa-m9/index.html', 'Apresentação, gravada ou na aula; créditos.', 'Apresentação à turma'),
            ('m9/guia-da-tarefa-m9/index.html', 'uma crítica registada (de um colega ou tua)', 'crítica de um colega registada'),
            ('tarefas/m7-u2/index.html', 'uma pergunta (a que te fizeram ou uma que prevês) e a tua resposta', 'a pergunta que te fizeram e o que respondeste'),
            # 05/11/2026: correção da revisão: diz-se de onde o aluno, sozinho, tira as imagens.
            ('m8/licao-m8-f09/index.html', 'três imagens tiradas ao acaso (de um livro, de uma revista ou da galeria do telemóvel) e um conto', 'preparado pelo docente'),
            ('m8/licao-m8-f09/index.html', 'galeria do telemóvel) e um conto de 400 a 600 palavras que', 'três imagens tiradas ao acaso e um conto'),
            ('m8/licao-m8-f09/index.html', '"frase":"As três imagens tiram-se [1] e têm de ser [2] à história.","lacunas":[{"o":["ao acaso","por tema","pela ordem"],"c":0}', 'conjunto preparado pelo [1]'),
            ('m8/licao-m8-f09/index.html', 'lês em voz alta, mudas duas coisas', 'a um colega, mudas'),
            ('m8/index.html', '"o":["Mudas duas coisas","Entregas logo","Recomeças do zero"],"c":0', '"A um colega","Ao docente","À turma"'),
            ('m8/index.html', 'um álbum à tua escolha, com provas do texto; indica uma semelhança', 'selecionado pelo docente'),
            ('m8/painel-m8-f09/index.html', 'leitura em voz alta: o processo também conta', 'leitura a um colega'),
            ('m9/index.html', 'escreve o texto de opinião que responde ao outro lado (na aula, debate em turma).', 'participa no debate'),
            ('m1/m1-promessa-do-cronista/index.html', 'Responde-lhe agora em voz alta, numa frase.</p>', 'numa frase, a alguém'),
            ('m6/m6-cesario-noite-inteira/index.html', 'Diz a tua posição em voz alta e justifica-a', 'em voz alta a um colega'),
            ('m8/m8-george-tres-idades/index.html', '"rot":"Outra leitura"', 'Troca a tua leitura com um colega'),
            ('m8/m8-poema-testemunha/index.html', 'Compara a tua escolha com a outra pista', 'com a de um colega'),
            ('obras/memorial/index.html', 'depois lê-o em voz alta, com uma voz para cada um.', 'a duas vozes com um colega'),
            ('obras/mensagem/index.html', 'Lê «Mar Português» em voz alta e escolhe', 'em voz alta a um colega'),
            ('atlas/index.html', 'uma cena de dois minutos.","nasceu"', 'com a tua turma'),
            ('assets/atlas-editorial.js', 'continua-a noutra voz, como se fosses outra pessoa.', 'a um colega e deixa-o continuar'),
            ('assets/atlas-editorial.js', 'Grava uma frase tua; depois regista-a', 'pede a um colega'),
            ('assets/atlas-editorial.js', 'explica a ordem numa frase.', 'explica a ordem a um colega'),
            ('assets/atlas-editorial.js', 'em palco. Experimenta a mesma fala com dois gestos diferentes.', 'Em dupla'),
            ('assets/atlas-explorar.js', 'Ouve-as e descreve o que mudou.', 'Pede a alguém'),
            ('assets/atlas-explorar.js', 'Lê-a pela partitura e grava-te; ajusta um sinal depois de ouvir.', 'Outra pessoa interpreta-a'),
            # 05/11/2026: correção da revisão: o poema não está na página; sem vídeo, o caminho diz o que fazer sem ele, e a
            # participação oral fica entre parênteses, como momento de aula.
            ('m8/licao-m8-f01/index.html', 'Sem vídeo: se tiveres o poema em livro, lê-o em voz alta; se não, escolhe a pista só pela pergunta e volta a ela quando puderes ouvir a leitura. (Na aula, podes participar oralmente ou apenas comparar mentalmente.)', 'pede ao docente'),
            ('m8/licao-m8-f01/index.html', 'quando puderes ouvir a leitura. (Na aula, podes participar', 'Sem vídeo: lê o poema em voz alta.'),
            ('m7/licao-m7-f34/index.html', 'Relê ou mostra a alguém: reconhecem-se os dois planos', 'consegue reconhecer'),
            ('m7/licao-m7-f34/index.html', 'Lê-os em voz alta e confirma que se veem os dois lugares.', 'pergunta-lhe que dois lugares viu'),
            # 05/11/2026: correções da revisão: casos nas mesmas páginas (ou no mesmo caso de outras) que ainda dependiam de
            # alguém, dos colegas, da sala ou do docente.
            ('m1/m1-voz-emprestada/index.html', 'Escolhe a resposta que defendes e justifica-a em voz alta.","opcoes"', 'justifica-a em voz alta a alguém'),
            ('m2/guia-da-tarefa-m2/index.html', 'com consulta, e 5 minutos para leres o enunciado; depois respondes', 'apresentação do enunciado pelo docente'),
            ('m1/guia-da-tarefa-m1/index.html', 'Seguem-se 5 minutos de leitura do enunciado, 60 minutos de produção com consulta', 'apresentação do enunciado pelo docente'),
            ('assets/atlas-explorar.js', 'Sem áudio, lê a mesma frase de duas maneiras e compara as duas leituras.', 'em sala.'),
            ('assets/atlas-explorar.js', 'Na alternativa sem áudio, compara as tuas duas leituras da mesma frase.', 'dita pelos colegas'),
            ('m3/licao-m3-f11/index.html', '"f":"Um texto com **autor** e data; a pergunta faz-se por **escrito** (na aula, lê-se em voz alta)."', 'lidas em voz alta'),
            ('m3/painel-m3-f11/index.html', '"f":"Um texto com **autor** e data; a pergunta faz-se por **escrito** (na aula, lê-se em voz alta)."', 'lidas em voz alta'),
            ('m3/index.html', 'Autor e data tornam a fonte verificável; a pergunta faz-se por escrito (na aula, lê-se em voz alta).', 'leem-se em voz alta na mesma'),
            ('m3/licao-m3-f11/index.html', 'sem conferência, a pergunta faz-se por escrito (na aula, lê-se em voz alta).', 'por escrito e lê-se em voz alta'),
            ('m3/painel-m3-f11/index.html', 'sem conferência, a pergunta faz-se por escrito (na aula, lê-se em voz alta).', 'por escrito e lê-se em voz alta'),
            ('m3/licao-m3-f11/index.html', 'fazes uma pergunta em público (sem conferência, por escrito).', 'lida em voz alta, se não houver conferência'),
            ('m2/guia-da-tarefa-m2/index.html', 'Se faltaste à ida ao teatro, lê uma cena em voz alta e escreve a apreciação crítica dessa leitura, com os mesmos critérios.', 'feita na aula'),
            ('m4/guia-da-tarefa-m4/index.html', 'Se faltaste à ida ao teatro, lê em voz alta uma cena do ato I e escreve a apreciação crítica dessa leitura: compara-a com a tua leitura silenciosa, com os mesmos critérios.', 'lida em voz alta na aula'),
            ('m9/m9-de-quem-e-o-convento/index.html', 'Deixa de fora a decisão que a pergunta te pede, e vais ter de a tomar na mesma.', 'o docente vai pedir-ta'),
        ]
        for rel, novo, antigo in casos:
            texto = ler(rel)
            with self.subTest(ficheiro=rel, novo=novo):
                self.assertIn(novo, texto)
                self.assertNotIn(antigo, texto)

    def test_paginas_geradas_mudam_no_gerador(self):
        # As tarefas e o aquecimento gerados saem iguais, byte a byte, dos dados já corrigidos.
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for rel in sorted(GERADAS):
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())
        mudadas = {t['ficheiro'] for t in TROCAS if t['ficheiro'].startswith('tarefas/')}
        literais = {'tarefas/m2-u1/index.html', 'tarefas/m2-u2/index.html', 'tarefas/m4-u2/index.html',
                    'tarefas/m4-u3/index.html', 'tarefas/m7-u2/index.html'}
        self.assertEqual(mudadas, GERADAS | literais)
        for t in TROCAS:
            if t['ficheiro'] in GERADAS:
                with self.subTest(dados=t['ficheiro']):
                    fonte = [d for d in TROCAS if d['ficheiro'].startswith('docs/pedagogia/') and d['novo'] == t['novo']]
                    self.assertTrue(fonte, 'a troca da página gerada tem de estar também nos dados do gerador')

    def test_camada_mais_recente_e_registada(self):
        # 06/11/2026: o lote 3 do Atlas fica por cima da decisão 154 depois de juntar o main; desfaz-se antes, com a mesma exigência.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/autonomia_154_20261105.json',
                            '--manifesto', str(MANIFESTO), '--verificar',
                            # 06/11/2026: por cima de tudo, o desenho comum dos nove índices (decisão 148); desfaz-se primeiro, com a mesma exigência.
                            '--desfazer-antes', 'tests/fixtures/cartaz-indices-148-edits-20261106.json',
                            # 06/11/2026: por cima de tudo, os créditos atrás de um «i» (decisão 153, pedido pt-2); desfazem-se primeiro.
                            '--desfazer-antes', 'tests/fixtures/creditos-i-edits-20261105.json',
                            '--desfazer-antes', 'tests/fixtures/atlas-lote3-edits-20261105.json'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import verificar_camadas
        finally:
            sys.path.pop(0)
        # 06/11/2026: por cima da decisão 154 fica o lote 3 do Atlas (junção com o main); a decisão 154 passa a segunda, logo por baixo dele,
        # e a cadeia de desfazer chama primeiro o Atlas.
        # 06/11/2026: por cima do lote 3 do Atlas ficam os créditos atrás de um «i» (decisão 153, pedido pt-2, junção com o main): o
        # Atlas passa a segundo, a decisão 154 a terceira, e a cadeia de desfazer chama primeiro os créditos, depois o Atlas.
        # 06/11/2026: por cima dos créditos atrás de um «i» fica o desenho comum dos nove índices (decisão 148): os créditos passam
        # a segundos, o Atlas a terceiro, a decisão 154 a quarta, e a cadeia de desfazer chama primeiro o desenho comum.
        self.assertEqual(verificar_camadas.LAYERS[0], ('cartaz_indices_148_20261106', 'cartaz-indices-148-edits-20261106'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('creditos_i_20261105', 'creditos-i-edits-20261105'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('atlas_lote3_20261105', 'atlas-lote3-edits-20261105'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('autonomia_154_20261105', 'autonomia-154-edits-20261105'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('exame_contexto_20261105', 'exame-contexto-edits-20261105'))
        auditoria = ler('tests/auditoria_20261028.py')
        # 06/11/2026: os créditos desfazem primeiro o desenho comum dos índices (decisão 148).
        corpo = auditoria[auditoria.index('def undo_creditos_i_0511'):]
        self.assertLess(corpo.index('undo_cartaz_148_0611(path, text)'), corpo.index('_CREDITOS_I_0511.get('))
        corpo = auditoria[auditoria.index('def undo_contexto_0511'):]
        self.assertLess(corpo.index('undo_autonomia_0511(path, text)'), corpo.index('_CONTEXTO_0511.get('))
        corpo = auditoria[auditoria.index('def undo_atlas_lote3_0511'):]
        self.assertLess(corpo.index('undo_creditos_i_0511(path, text)'), corpo.index('_ATLAS_LOTE3_0511.get('))
        corpo = auditoria[auditoria.index('def undo_autonomia_0511'):]
        self.assertLess(corpo.index('undo_atlas_lote3_0511(path, text)'), corpo.index('_AUTONOMIA_0511.get('))
        sala = ler('scripts/desligar_sala.py')
        self.assertIn('autonomia-154-edits-20261105.json', sala)
        # 06/11/2026: na Sala desligada, o desenho comum dos índices (decisão 148) desfaz-se antes dos créditos atrás de um «i».
        self.assertLess(sala.index('cartaz-indices-148-edits-20261106.json'), sala.index('creditos-i-edits-20261105.json'))
        self.assertLess(sala.index('creditos-i-edits-20261105.json'), sala.index('atlas-lote3-edits-20261105.json'))
        self.assertLess(sala.index('atlas-lote3-edits-20261105.json'), sala.index('autonomia-154-edits-20261105.json'))


if __name__ == '__main__':
    unittest.main()
