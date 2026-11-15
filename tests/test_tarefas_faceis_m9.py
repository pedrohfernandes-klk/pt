"""14/11/2026: as duas tarefas do M9 (m9-u1 e m9-u2) «mais fáceis de fazer», «tudo junto» no M9 e dois acertos (o guia da tarefa do
M2 e o índice do M7), na camada tarefas_faceis_m9_20261114.

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201) e levado ao M1, ao M5, ao M6, ao M7 e ao
M8. Esta camada leva-o ao M9, e este ficheiro exige das duas tarefas do M9 o que tests/test_tarefas_faceis_m8.py exige das do M8:

* a tarefa pede o mesmo: os títulos, os nomes e as letras dos temas, os números de palavras, cada pedido do enunciado de antes (com as
  mesmas palavras), a pergunta das duas linhas finais e a pergunta opcional, e os critérios, níveis, exemplos e pontos das grelhas,
  iguais aos de antes da camada (a base do manifesto, o main 85c4b504);
* DIREITOS DE AUTOR (decisão do docente para todo o M9): <i>Memorial do Convento</i> ainda tem direitos (José Saramago morre em 2010:
  confere-se no mapa do módulo M9, porque nenhuma lição do M9 dá o ano) e não se copia. Cada passagem tem um bloco «Onde está o
  texto» só com as citações curtas que as lições do M9 já publicam, conferidas letra a letra no cartão da lição de origem, e a linha de
  fonte, que diz onde ler a passagem como a lição o diz («na edição da turma», «no livro»), nunca «no manual» (nenhuma lição do M9 o
  diz), sem número de página; os excertos longos das lições F01, F02 e F05 não se copiam; nada vem de fora das lições; não há imagens;
* os exemplos usam outro caso (os casos inventados dos aquecimentos, com as frases dos aquecimentos, letra a letra), sem palavras dos
  textos da tarefa, sem dar feita nenhuma alínea, sem a resposta certa da pergunta opcional e sem nenhuma resposta do aquecimento;
* as decisões do docente, em todos os sítios: tempos 10/10/55/15 (quadro, relógios, guia); «com consulta» dito uma vez, no primeiro
  cartão; as passagens citadas ou copiadas não contam para as palavras (a mesma frase no enunciado, na grelha e no guia); a
  autoavaliação da grelha não se entrega; o aquecimento com uma só ligação; no máximo 10 perguntas de sim ou não; as mesmas palavras
  no enunciado, na grelha, na correção, no guia, no índice e no mapa;
* o guia, o portefólio, o índice e o mapa do M9, o guia do M2 e o índice do M7 são os do main de partida, letra a letra, salvo as
  trocas da camada, conferidas uma a uma;
* as regras do texto; o contrato da página; as outras tarefas, grelhas, correções e aquecimentos iguais ao main, byte a byte;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base, gerador que dá o mesmo JSON, registada na
  auditoria, em scripts/desligar_sala.py, na leitura histórica e nas cadeias e caminhos dos fluxos.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em
tests/browser_tarefas_faceis_m9.py."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import html
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'scripts'))
from auditoria_20261028 import (undo_tarefas_faceis_m9_1114, undo_tarefas_faceis_m8_1113, undo_tarefas_faceis_m7_1113,  # noqa: E402
                                undo_tarefas_faceis_m3_1112)
import verificar_camadas  # noqa: E402

CAMADA_REL = 'scripts/tarefas_faceis_m9_20261114.json'
MANIFESTO_REL = 'tests/fixtures/tarefas-faceis-m9-edits-20261114.json'
M8F = 'tests/fixtures/tarefas-faceis-m8-edits-20261113.json'
M7F = 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'
M3F = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
BASE_COMMIT = '85c4b50420a00513d252a9da09e4901a4c3f4a49'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
TROCAS = json.loads((ROOT / CAMADA_REL).read_text('utf-8'))
SLUGS = ('m9-u1', 'm9-u2')
N = '\xa0'
DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
ENUNCIADOS = [f'tarefas/{s}/index.html' for s in SLUGS]
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'correcao/')]
AQUECIMENTOS = [f'tarefas/{s}/aquecimento/index.html' for s in SLUGS]
DADOS_AQUECIMENTOS = [f'docs/pedagogia/aquecimentos/{s}.json' for s in SLUGS]
GUIA, INDICE, MAPA = 'm9/guia-da-tarefa-m9/index.html', 'm9/index.html', 'm9/mapa-do-modulo-m9/index.html'
PORTEFOLIO = 'm9/portefolio-do-modulo-m9/index.html'
GUIA_M2, INDICE_M7 = 'm2/guia-da-tarefa-m2/index.html', 'm7/index.html'
FICHEIROS = DADOS_TAREFAS + [GRELHAS] + PAGINAS + [GUIA, PORTEFOLIO, INDICE, MAPA, GUIA_M2, INDICE_M7]
L = {k: f'm9/licao-m9-f{k}/index.html' for k in ('01', '02', '03', '05', '10', '11', '12', '13', '14', '15', '16')}
OUTRAS = ('m1-u1', 'm1-u2', 'm3-u1', 'm3-u2', 'm5-u1', 'm5-u2', 'm6-u1', 'm6-u2', 'm7-u3', 'm8-u1', 'm8-u2')
FORA_DAS_LICOES = {'https://estudoemcasaapoia.dge.mec.pt/recurso/memorial-do-convento-de-jose-saramago-representatividade-de-sociedade-da-epoca-rei-e-rainha'}
CARTOES_NOMES = ['Começar', 'Tema A ou B', 'O teu plano', 'O teu texto', 'Fechar e entregar', 'Rever a matéria']
NAO_CONTAM = 'Não contam para as palavras: as passagens citadas ou copiadas, o plano e as duas linhas finais.'
CONSULTA = 'Trabalhas à mão. O aquecimento e a tarefa são com consulta: podes usar as lições do site, o caderno e o dicionário.'
ANTES_DA_AULA = f'Antes da aula, lê os capítulos{N}I{N}e{N}V de <i>Memorial do Convento</i>, na edição da turma.'
MR = '<i>Memorial do Convento</i>'
# O que cada enunciado de antes pedia, com as suas palavras: cada pedaço está no enunciado de antes e continua no de agora.
PEDIDOS = {
    'm9-u1': ['No capítulo I, como transforma a descrição da miniatura da basílica de São Pedro a imagem do rei?',
              'os gestos do rei da forma como o narrador os conta', 'No capítulo V, como transforma o narrador a imagem do auto de fé?',
              'o olhar da assistência da crítica construída pela narração', 'a tua opinião inicial', 'dois pormenores do episódio',
              'onde se encontram', 'um procedimento de escrita', 'uma dificuldade da tua leitura', 'xplica o efeito', 'com exemplos',
              'dentificá-lo não chega', 'como muda a tua leitura do episódio quando distingues o que acontece da maneira como é contado?',
              'Localiza o pormenor decisivo.', 'Fotografa o plano, o texto e as duas linhas finais.', 'O rei e a miniatura',
              'A cerimónia e o olhar', 'O diretor elogia a calma entre buzinas.', 'Que alteração conserva o procedimento crítico do caso?',
              'apreciação crítica'],
    'm9-u2': ['Como devem aparecer as vidas dos construtores na apresentação pública de um monumento?', 'uma decisão',
              'a nomeação dos trabalhadores com o episódio de Francisco Marques',
              'Como devem aparecer o cuidado e a arte na apresentação pública de uma invenção?',
              'o papel de Blimunda com a intervenção de Scarlatti', 'a decisão concreta que propões',
              'duas situações de Memorial do Convento que a apoiem', 'onde se encontram', 'uma objeção',
              'uma diferença entre a época do romance e o presente', 'ustifica a decisão', 'esponde à objeção',
              'xplica até onde a comparação entre as épocas funciona',
              'que diferença entre a época do romance e o presente te levou a ajustar a decisão?',
              'Indica a passagem do romance que manténs como apoio.', 'Fotografa o plano, o texto e as duas linhas finais.',
              'Apresentar um monumento', 'Apresentar uma invenção', 'Juntar o ano numa linha da legenda.',
              'Que resposta enfrenta essa objeção?', 'texto de opinião', 'uma campanha, um cartaz ou outro produto'],
}
ALINEAS = {
    'm9-u1': [['Escreve a tua opinião inicial sobre o episódio.', 'Regista dois pormenores do episódio.',
               'Indica onde se encontram: a página da tua edição e o início de cada passagem.', 'Escolhe um procedimento de escrita.',
               'Anota uma dificuldade da tua leitura.'],
              ['Apresenta a tua apreciação: o que pensas do episódio, e porquê.', 'Desenvolve a apreciação com os dois pormenores do teu plano.',
               'Explica o efeito do procedimento de escrita com exemplos.', 'Indica a edição que usaste: a editora e o ano.',
               'Escreve o total de palavras no fim.']],
    'm9-u2': [['Escreve a decisão concreta que propões.', f'Indica duas situações de {MR} que a apoiem.',
               'Indica onde se encontram: a página da tua edição e o início de cada passagem.', 'Anota uma objeção à tua decisão.',
               'Anota uma diferença entre a época do romance e o presente.'],
              ['Apresenta a tua decisão.', 'Justifica a decisão com as duas situações do romance.', 'Apresenta a objeção do teu plano.',
               'Responde à objeção.', 'Explica até onde a comparação entre as épocas funciona.',
               'Indica a edição que usaste: a editora e o ano.', 'Escreve o total de palavras no fim.']],
}
PASSOS = {'m9-u1': [['Aprecia o episódio.', 'Distingue os gestos do rei da forma como o narrador os conta.'],
                    ['Aprecia o episódio.', 'Distingue o olhar da assistência da crítica construída pela narração.']],
          'm9-u2': [['Propõe uma decisão.', 'Relaciona a nomeação dos trabalhadores com o episódio de Francisco Marques.'],
                    ['Propõe uma decisão.', 'Relaciona o papel de Blimunda com a intervenção de Scarlatti.']]}
# Os blocos «Onde está o texto», pela ordem da página: (id, título, [(intro, linha, lição, cartão)], linha de fonte inteira,
# [(lição, cartão, frase que a lição tem, letra a letra)] que confirmam o que a linha de fonte e as frases dizem).
ONDE = {
    'm9-u1': [
        ('texto-1', f'{MR}, capítulo{N}I: a miniatura da basílica', [],
         f'José Saramago, {MR}, capítulo{N}I. Lê o episódio na edição da turma, como diz a lição{N}F14 (cartão «Lê de perto»).',
         [('14', 4, 'Lê o episódio na edição da turma'), ('14', 4, 'Este resumo não é uma citação do romance.'),
          ('14', 4, f'Resumo didático do capítulo{N}I')]),
        ('texto-2', f'{MR}, capítulo{N}V: o primeiro auto de fé', [(f'Palavras que a lição{N}F15 cita:', '«a descansada leitura das sentenças»', '15', 4)],
         f'José Saramago, {MR}, capítulo{N}V. Lê o capítulo na edição da turma, como diz a lição{N}F15 (cartão «Lê de perto»).',
         [('15', 4, 'Lê o capítulo na edição da turma.'), ('15', 4, f'José Saramago, {MR}, capítulo{N}V.')]),
    ],
    'm9-u2': [
        ('texto-1', f'{MR}: os nomes dos trabalhadores',
         [(f'Palavras que a lição{N}F05 cita:', '«já não podemos falar-lhes das vidas, por tantas serem, ao menos deixemos os nomes escritos»', '05', 16)],
         f'José Saramago, {MR} (1982), a viagem da pedra para Mafra. Lê a passagem no livro, na edição da turma. A lição{N}F05 tem um excerto: cartão «O texto, 1 de 3».',
         [('05', 5, 'José Saramago, _Memorial do Convento_ (1982), a viagem da pedra para Mafra (excerto).'), ('05', 8, 'Com o livro aberto: a pedra e os nomes'),
          ('05', 8, 'o narrador diz os nomes deles, um a um')]),
        ('texto-2', f'{MR}, capítulo{N}XIX: o episódio de Francisco Marques',
         [(f'Palavras que a lição{N}F16 cita:', '«está a fazer bem o trabalho»', '16', 4),
          (f'Palavras que a lição{N}F05 cita:', '«aquela mulher ali é que é a viúva, não sabemos que nome tem, nem adiantaria nada à história ir lá perguntar-lhe»', '05', 24)],
         f'José Saramago, {MR}, capítulo{N}XIX. A lição{N}F16 diz onde ler a passagem: cartão «Lê de perto» (o excerto da Porto Editora ou a edição da turma).',
         [('16', 4, 'Se o acesso não estiver disponível, lê a passagem na edição da turma.'), ('16', 4, 'Lê o excerto na fonte editorial</a>'),
          ('16', 4, 'A passagem apresenta o trabalho de Francisco Marques'), ('05', 24, f'(capítulo{N}XIX)'),
          ('13', 9, f'No capítulo{N}XIX, regressa ao transporte da grande pedra, à morte de Francisco Marques')]),
        ('texto-3', f'{MR}: o papel de Blimunda',
         [(f'Palavras do voo que a lição{N}F02 cita:', '«por obra também dos olhos de Blimunda»', '02', 22)],
         f'José Saramago, {MR}. As passagens leem-se no livro, como diz a lição{N}F11 (cartão «Para levar»). A lição{N}F02 tem um excerto do voo e um do reencontro: cartões «O texto».',
         [('11', 13, 'As passagens literárias leem-se no livro'), ('11', 5, f'No voo da passarola, capítulo{N}XVI'),
          ('11', 2, f'no capítulo{N}XXV, a procura de Baltasar'), ('02', 5, 'O voo da passarola'), ('02', 6, 'O reencontro (último capítulo)')]),
        ('texto-4', f'{MR}: a intervenção de Scarlatti', [],
         f'José Saramago, {MR}. A lição{N}F12 diz como a procurar no livro: cartão «O que Scarlatti acrescenta».',
         [('12', 2, 'No livro, localiza as passagens em que Scarlatti toca e se relaciona com os protagonistas.'), ('12', 13, 'As passagens literárias leem-se no livro')]),
    ],
}
# De onde vem o caso dos exemplos: os dados do aquecimento da mesma tarefa, letra a letra (fora as marcas de itálico _…_).
EXEMPLOS_DO_AQUECIMENTO = {
    'm9-u1': ['Caso inventado: o diretor inaugura a biblioteca, corta uma fita e elogia o silêncio. Atrás dele, uma máquina de obras impede '
              'que se ouça o discurso. O narrador descreve ambos os sons.'],
    'm9-u2': ['Caso inventado: numa exposição escolar, as legendas só dão os títulos das fotografias. A turma discute se deve acrescentar as '
              'datas. Algumas imagens mostram o mesmo lugar em anos diferentes.'],
}
TROCAS_COMUNS = [
    ['com núcleo de planificação e síntese de duas linhas fora da contagem.', 'com plano e duas linhas finais. ' + NAO_CONTAM],
    ['extensão, identificação, núcleo ou síntese', 'extensão, identificação, plano ou duas linhas finais'],
    ['a identificação do tema, o núcleo e a síntese', 'a identificação do tema, o plano e as duas linhas finais'],
    ['separo dele o núcleo e as duas linhas finais', 'separo dele o plano e as duas linhas finais'],
    ['falta a contagem e o tema', 'falta a contagem e a letra do tema'],
    ['Não identificar a edição consultada.', 'Não indicar a edição que usaste (a editora e o ano).']]
TROCAS_GRELHA = {'m9-u1': TROCAS_COMUNS,
                 'm9-u2': TROCAS_COMUNS + [['Repetir a tese como se fosse uma resposta.', 'Repetir a decisão como se fosse uma resposta.']]}
AUTO_HTML = '<h2>Autoavaliação</h2>\n<p class="pequeno">Em cada parâmetro, toca no nível que achas que tens. O 4 é o melhor. Escreve uma linha a dizer porquê.</p>\n<div id="r-auto"></div>\n'
AUTO_INPUT = ('if(t.dataset.k){d().campos[t.dataset.k]=t.value;guardar()}if(t.dataset.auto!=null){var a=d().auto;a[t.dataset.auto]=a[t.dataset.auto]||{};a[t.dataset.auto].j=t.value;guardar()}});',
              'if(t.dataset.k){d().campos[t.dataset.k]=t.value;guardar()}});', 1)
AUTO_CLIQUE = ('''document.addEventListener("click",function(ev){var b=ev.target.closest(".niveis button");if(!b||!atual)return;var p=b.parentNode.dataset.p;b.parentNode.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-pressed","false")});b.setAttribute("aria-pressed","true");var a=d().auto;a[p]=a[p]||{};a[p].n=Number(b.dataset.n);guardar()});\n''', '', 1)
AUTO_COPIA = ('''")+p.nome)});l.push("","AUTOAVALIAÇÃO");\n  atual.rubrica.forEach(function(p,i){var a=D.auto[i]||{};l.push(p.nome+": nível "+(a.n||"-")+(a.j?" · "+a.j:""))});return l.join("\\n")}''',
              '''")+p.nome)});return l.join("\\n")}''', 1)
AUTO_VE = ('O docente vê o teu plano, as notas, a lista e a autoavaliação.</p>', 'O docente vê o teu plano, as notas e a lista.</p>', 1)
# As trocas das páginas do módulo e dos dois acertos: (antes, depois, vezes). Aplicadas à base, dão a página da árvore, letra a letra.
TROCAS_MODULO = {
    GUIA: [
        (f'Seguem-se 5{N}minutos de leitura, 60 de produção individual em papel e 15 de revisão e entrega no Teams. O núcleo integra a planificação; não é uma resposta pronta.</p>',
         f'Seguem-se 10{N}minutos de leitura, 55 de produção individual em papel e 15 de revisão e entrega no Teams. O plano prepara o texto; não é uma resposta pronta. {NAO_CONTAM}</p>', 1),
        ('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica;</li><li>pergunta ao teu par de trabalho.</li></ol>',
         '<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica.</li></ol>', 1),
        (f'<b>Ler o enunciado, 5{N}min</b><span>Lê o núcleo comum e os temas A e B.</span>',
         f'<b>Ler o enunciado, 10{N}min</b><span>Lê os temas A e B, o que o plano leva e o que o texto leva.</span>', 1),
        (f'<b>Produzir, 60{N}min</b>', f'<b>Produzir, 55{N}min</b>', 1),
        ('[5, "Ler o enunciado", "Lê o núcleo comum e os temas A e B."], [60, "Produzir",',
         '[10, "Ler o enunciado", "Lê os temas A e B, o que o plano leva e o que o texto leva."], [55, "Produzir",', 1),
        (AUTO_HTML, '', 1), AUTO_VE,
        ('''  $("#r-auto").innerHTML=atual.rubrica.map(function(p,i){var a=D.auto[i]||{};return '<p style="margin:10px 0 4px"><b>'+esc(p.nome)+'</b> <span class="pequeno">(extra sem nota)</span></p><div class="niveis" data-p="'+i+'">'+[4,3,2,1].map(function(n){return '<button aria-pressed="'+(a.n===n?"true":"false")+'" data-n="'+n+'">'+n+'</button>'}).join("")+'</div><textarea data-auto="'+i+'" placeholder="Porquê, numa linha." style="min-height:56px">'+esc(a.j||"")+'</textarea>'}).join("");\n''', '', 1),
        AUTO_INPUT, AUTO_CLIQUE, AUTO_COPIA,
    ],
    INDICE: [
        ('aquecimento em cartões, planificação, tema A ou B, revisão e fotografias no Teams.', 'aquecimento em cartões, tema A ou B, plano, texto, revisão e fotografias no Teams.', 1),
        ('com consulta: aquecimento, planificação, tema A ou B, revisão e fotografias no Teams.', 'com consulta: aquecimento, tema A ou B, plano, texto, revisão e fotografias no Teams.', 2),
        # 15/11/2026 (revisão): «tudo junto» também no índice: «duas linhas finais» em vez de «síntese», como no mapa.
        ('A síntese integra a produção.', 'As duas linhas finais fazem parte da entrega.', 1),
        ('Cada unidade termina na sua aula de tarefa, com a síntese integrada.', 'Cada unidade termina na sua aula de tarefa, e as duas linhas finais fazem parte da entrega.', 1),
    ],
    MAPA: [('A síntese faz parte da entrega e não cria outro registo de conclusão.', 'As duas linhas finais fazem parte da entrega e não criam outro registo de conclusão.', 1)],
    PORTEFOLIO: [
        (': tema A ou B, núcleo, texto, duas linhas e autoavaliação /20.', ': tema A ou B, plano, texto e duas linhas finais.', 2),
        ('autonomia, responsabilidade, trabalho de equipa, pensamento crítico', 'autonomia, responsabilidade, pensamento crítico', 1),
        # 15/11/2026 (revisão): «tudo junto» também no portefólio: «duas linhas finais» em vez de «síntese», como no mapa.
        ('A tarefa da unidade inclui as duas linhas de síntese;', 'A tarefa da unidade inclui as duas linhas finais;', 1),
        ('Retomas formativas da leitura, sem síntese adicional obrigatória. A síntese integra a tarefa da unidade.',
         'Retomas formativas da leitura, sem outro registo obrigatório. As duas linhas finais fazem parte da tarefa da unidade.', 2),
    ],
    # 14/11/2026: acerto do M2, só nas frases do guia: sai a «Autoavaliação» que se copiava para o Teams (com o código e o texto
    # copiado que lhe pertencem) e o par de trabalho; «Dois antes de mim», com dois passos, como nos guias do M3 ao M9.
    GUIA_M2: [
        ('<div class="regra"><b>Três antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica; 3) pergunta ao teu par de trabalho. Só depois levantas o braço.</div>',
         '<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica. Só depois levantas o braço.</div>', 1),
        ('Se encravares, regra dos três antes de mim.', 'Se encravares, regra dos dois antes de mim.', 2),
        ('Lista da rubrica, regra do original, autoavaliação, duas linhas e fotografias no Teams.', 'Lista da rubrica, regra do original, duas linhas e fotografias no Teams.', 2),
        (AUTO_HTML, '', 1), AUTO_VE,
        ('''  $("#r-auto").innerHTML=atual.rubrica.map(function(p,i){var a=D.auto[i]||{};return '<p style="margin:10px 0 4px"><b>'+esc(p.nome)+'</b> <span class="pequeno">('+p.pontos[0]+' pontos no nível 4)</span></p><div class="niveis" data-p="'+i+'">'+[4,3,2,1].map(function(n){return '<button aria-pressed="'+(a.n===n?"true":"false")+'" data-n="'+n+'">'+n+'</button>'}).join("")+'</div><textarea data-auto="'+i+'" placeholder="Porquê, numa linha." style="min-height:56px">'+esc(a.j||"")+'</textarea>'}).join("");\n''', '', 1),
        AUTO_INPUT, AUTO_CLIQUE, AUTO_COPIA,
    ],
    # 14/11/2026: acerto do M7: «opinião» em vez de «tese» (a m7-u3 diz «opinião» em todo o lado).
    INDICE_M7: [('No fim, defendes uma tese com um verso de <em>Mensagem</em>', 'No fim, defendes uma opinião com um verso de <em>Mensagem</em>', 1)],
}
# As lições que o cartão «Rever a matéria» manda reler: (para, lição, título da lição, secções, frase da secção que a linha resume).
REVER = {
    'm9-u1': [(f'Tema{N}A', '14', 'Um rei em miniatura', ['Lê de perto', 'Para entender'], 'Comparar sem igualar'),
              (f'Tema{N}B', '15', 'A festa vista do outro lado', ['Lê de perto', 'Para entender'], 'Dois planos em confronto'),
              ('O teu plano', '11', 'O cuidado também é ação', ['Lê e confronta'], 'escolhe uma ação concreta de Blimunda e descreve o seu efeito e o seu limite'),
              ('O teu texto', '03', 'A voz que conta', ['O essencial'], 'um narrador que comenta')],
    'm9-u2': [(f'Texto{N}1', '05', 'Os que carregaram a pedra', ['Para entender'], 'a pedra e os nomes'),
              (f'Texto{N}2', '16', 'O instante dentro da duração', ['Lê de perto'], 'A passagem apresenta o trabalho de Francisco Marques e o acidente mortal que o interrompe.'),
              (f'Texto{N}3', '11', 'O cuidado também é ação', ['Lê e confronta'], 'descreve o seu efeito e o seu limite'),
              (f'Texto{N}4', '12', 'Quando a música entra no projeto', ['Lê e confronta'], 'O que Scarlatti acrescenta'),
              ('O teu plano', '13', 'Da pista à interpretação', ['Lê e confronta'], 'o que a passagem mostra; o que proponho que isso significa'),
              ('O teu texto', '10', 'De quem é uma obra?', ['Para entender'], 'Refutação')],
}


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def antes(rel):
    """O ficheiro como estava por baixo desta camada (desfeita pelo manifesto, com contagem estrita): o main de partida."""
    texto = ler(rel)
    for e in reversed(MANIFESTO['files'].get(rel, {}).get('edits', [])):
        assert texto.count(e['new']) == e['occurrences'], (rel, e['location'])
        texto = texto.replace(e['new'], e['old'])
    return texto


def do_main(rel):
    """O ficheiro no commit de partida (os fluxos que correm este teste descarregam o histórico: fetch-depth: 0)."""
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    assert r.returncode == 0, f'{rel}: falta o commit de partida {BASE_COMMIT[:8]} (o fluxo tem de fazer checkout com fetch-depth: 0)'
    return r.stdout.decode('utf-8')


def visivel(fonte, so_main=True, sem_nav=True):
    """O texto que se lê numa página: sem scripts, estilos nem etiquetas, com os espaços normais juntos (U+00A0 fica)."""
    if so_main and '<main' in fonte:
        fonte = fonte[fonte.index('<main'):fonte.index('</main>')]
    fonte = re.sub(r'<(script|style)\b.*?</\1>', ' ', fonte, flags=re.S)
    if sem_nav:
        fonte = re.sub(r'<nav\b.*?</nav>', ' ', fonte, flags=re.S)
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fonte))).strip()


def solto(texto):
    return texto.replace(N, ' ')


def sem_marcas(texto):
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', texto)))


def cartoes(k):
    """Os cartões de uma lição do M9 (CARTOES=[…] no ficheiro da lição ou, nas F11, F12 e F13, em m9/recursos/fNN.js)."""
    fonte = ler(L[k])
    if 'CARTOES=[' not in fonte:
        fonte = ler(f'm9/recursos/f{k}.js')
    return json.JSONDecoder().raw_decode(fonte[fonte.index('CARTOES=[') + 8:])[0]


def no_cartao(k, i):
    """Tudo o que o cartão i (contado de 1) da lição k escreve, como está no ficheiro (o html e os campos das perguntas)."""
    c = cartoes(k)[i - 1]
    return c.get('html', '') + json.dumps({a: b for a, b in c.items() if a != 'html'}, ensure_ascii=False)


def blocos_onde(f):
    return [o for t in f['temas'] for o in t['material'].get('onde', [])] + f.get('temas_material', {}).get('onde', [])


def respostas_do_aquecimento(aq):
    """As respostas que o aquecimento dá (sem as marcas _…_, em minúsculas): a opção certa de cada escolha, as palavras certas e a
    frase preenchida de cada cartão de completar, a frase revista de cada cartão de rever, cada passo de ordenar (sem o verbo de ordem
    do princípio), cada par de emparelhar e as palavras certas de cada cartão de sublinhar."""
    tira = lambda s: solto(re.sub(r'_([^_]+)_', r'\1', s)).strip().rstrip('.').lower()
    out = []
    for c in aq['cartoes']:
        if c['t'] == 'escolha':
            out.append(tira(c['o'][c['c']]))
        elif c['t'] == 'completar':
            frase = c['frase']
            for i, l in enumerate(c['lacunas'], 1):
                out.append(tira(l['o'][l['c']]))
                frase = frase.replace(f'[{i}]', l['o'][l['c']])
            out.append(tira(frase))
        elif c['t'] == 'rever':
            out.append(tira(c['o'][c['c']]))
            out.append(tira(c['frase'].replace(c['trecho'], c['o'][c['c']])))
        elif c['t'] == 'ordenar':
            out += [tira(x.split(' ', 1)[1]) for x in c['passos']]
        elif c['t'] == 'emparelhar':
            out += [tira(b) for a, b in c['pares']]
        elif c['t'] == 'sublinhar':
            palavras = c['frase'].split()
            out += [tira(palavras[i]) for i in c.get('certas', []) if i < len(palavras) and len(tira(palavras[i])) > 3]
        # 15/11/2026 (revisão): também as respostas dos cartões de verdadeiro ou falso (a afirmação, quando é verdadeira) e as
        # explicações de todos os cartões (os campos f e fe), frase a frase: o exemplo não pode dizer o que o aquecimento explica.
        if c['t'] == 'vf' and c.get('v'):
            out.append(tira(c['p']))
        explicacoes = [c.get('f')] + (c['fe'] if isinstance(c.get('fe'), list) else [c.get('fe')])
        for e in explicacoes:
            if e:
                out += [tira(x) for x in re.split(r'(?<=[.;:!?])\s+', e) if len(tira(x).split()) >= 3]
    return [x for x in out if x]


# 15/11/2026 (revisão): as ideias que o aquecimento de cada tarefa já ensina, ditas por outras palavras (raízes). Nenhuma pode
# aparecer no texto dos exemplos (o caso, que é o mesmo, fica de fora). Na m9-u1: a solenidade ou a pompa que se perde, o ruído
# por cima da fala (abafar, ouvir, barulho, calma), o contraste e a ironia, o que o diretor pensa ou quer, e a fita e a presença
# do diretor, que o aquecimento diz que não servem de indício. Na m9-u2: as datas e os anos nas legendas, a linha curta, o texto
# a mais e o público de fora.
IDEIAS_DO_AQUECIMENTO = {
    'm9-u1': r'solen|pompa|cerimón|por cima|abaf|contrast|contrap|ironi|exalt|contest|corrobor|\bcalm|\bouv|\bouç|barulh|ruíd|'
             r'\belogi|silênci|\bpensa|pensament|\bquer\b|intenç|\bsabia|\bfita\b|presen[çt]|buzin|enfraquec|diminu',
    'm9-u2': r'\bdatas?\b|\banos?\b|legenda|\blinhas?\b|texto a mais|mais texto|públic|visitant|municipal|enfeit|histór',
}


class Pagina(HTMLParser):
    """A estrutura de uma página de tarefa: os filhos de <main>, os temas, as perguntas com opções, os ids e as ligações."""

    def __init__(self, fonte):
        super().__init__()
        self.pilha, self.raiz, self.ids, self.ligacoes, self.temas, self.perguntas, self.opcoes = [], [], [], [], [], [], []
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.pilha and self.pilha[-1][0] == 'main':
            self.raiz.append((tag, a.get('id'), a.get('data-task-card-name')))
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a':
            self.ligacoes.append(a.get('href', ''))
        if 'data-task-theme' in a:
            self.temas.append(a['data-task-theme'])
        if 'data-task-question' in a:
            self.perguntas.append((a['data-task-question'], any(x[0] == 'details' for x in self.pilha)))
        if tag == 'button' and 'data-response' in a:
            self.opcoes.append(a)
        if tag not in ('meta', 'link', 'br', 'img', 'input'):
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        if any(x[0] == tag for x in self.pilha):
            self.pilha = self.pilha[:max(i for i, x in enumerate(self.pilha) if x[0] == tag)]


class TarefasFaceisM9(unittest.TestCase):
    maxDiff = None

    # ---------- a tarefa pede o mesmo ----------

    def test_a_tarefa_pede_o_mesmo(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            d, a = json.loads(ler(rel)), json.loads(antes(rel))
            f = d['facil']
            palavras = {'m9-u1': '200 a 240', 'm9-u2': '220 a 260'}[slug]
            with self.subTest(tarefa=slug):
                # As chaves de antes ficam todas, iguais: a camada só acrescenta «facil», no fim. A base é o main de partida.
                self.assertNotIn('facil', a)
                self.assertEqual({k: v for k, v in d.items() if k != 'facil'}, a)
                self.assertEqual(list(d)[-1], 'facil')
                self.assertEqual(antes(rel), do_main(rel))
                pagina, velha = ler(enunciado), do_main(enunciado)
                self.assertEqual(re.search(r'<h1>(.*?)</h1>', velha).group(1), re.search(r'<h1>(.*?)</h1>', pagina).group(1))
                self.assertEqual(re.search(r'<title>(.*?)</title>', velha).group(1), re.search(r'<title>(.*?)</title>', pagina).group(1))
                self.assertEqual([(t['letra'], t['nome']) for t in f['temas']], [(t['letra'], t['nome']) for t in a['temas']])
                self.assertEqual(re.findall(r'data-task-theme="([AB])"', pagina), ['A', 'B'])
                # Os números de palavras, como no «lead» de antes, no quadro, junto do tema e do texto e na verificação.
                self.assertIn(f'<strong>{palavras} palavras</strong>', solto(a['lead']))
                self.assertEqual([solto(x[2]) for x in f['quadro']['linhas']], ['', '', palavras, '', palavras])
                self.assertIn(f'{palavras} palavras.', solto(f['temas_nota']))
                self.assertEqual(solto(f['depois'][1]['meta']), f'{palavras} palavras, sobre o tema A ou o tema B.')
                self.assertIn(f'Tenho {palavras} palavras, com o total no fim, e revi a escrita?', [solto(x) for x in f['verificar']])
                lido = solto(visivel(pagina))
                self.assertEqual(len(re.findall(r'\b\d+ a \d+\b', lido)), lido.count(palavras))
                # Cada pedido do enunciado de antes, com as mesmas palavras, na página de antes e na de agora.
                self.assertGreaterEqual(len(PEDIDOS[slug]), 20)
                for pedaco in PEDIDOS[slug]:
                    self.assertIn(pedaco, solto(visivel(velha)), pedaco)
                    self.assertIn(pedaco, lido, pedaco)
                # As alíneas do plano e do texto: os pedidos de antes, um por alínea; os passos de cada tema são as ordens do tema.
                self.assertEqual([p['nome'] for p in f['depois']], ['O teu plano', 'O teu texto'])
                self.assertEqual([[solto(x) for x in p['alineas']] for p in f['depois']], [[solto(x) for x in y] for y in ALINEAS[slug]])
                self.assertEqual([t['passos'] for t in f['temas']], PASSOS[slug])
                for t, de_antes in zip(f['temas'], a['temas']):
                    for x in [t['intro']] + t['passos']:
                        self.assertIn(solto(x).rstrip('.?').split(' ', 1)[1], solto(de_antes['texto']), x)
                for p in f['depois']:
                    for x in p['alineas']:
                        self.assertEqual(len(re.findall(r'[.?!](?: |$)', x)), 1, x)
                        self.assertNotIn(';', x)
                # A pergunta das duas linhas finais é a de antes.
                pergunta = re.search(r'contagem do texto: (.*?\?)', a['fecho']).group(1)
                self.assertEqual(f['finais']['passos'], ['Responde: ' + pergunta, a['fecho'].split('? ')[1]])
                # A entrega é a de antes, em passos; a letra do tema escreve-se no topo, logo ao escolher.
                self.assertIn('Fotografa o plano, o texto e as duas linhas finais.', a['clareza']['entrega'])
                self.assertEqual(f['entrega'][0], 'Fotografa o plano, o texto e as duas linhas finais.')
                self.assertEqual(len(f['entrega']), 3)
                self.assertEqual(solto(f['temas_topo']), 'Escreve a letra do teu tema (A ou B) no topo.')
                self.assertIn('o plano, o texto e as duas linhas finais', f['entregas']['intro'])
                # A pergunta opcional é a de antes (a página lê-a da chave antiga).
                self.assertNotIn('opcional', f)
                self.assertEqual(d['opcional'], a['opcional'])
                self.assertIn(html.escape(d['opcional']['pergunta'], quote=False), pagina)
                for o in d['opcional']['opcoes']:
                    self.assertIn(f'data-response="{o["resposta"]}"', pagina)
                # O dossiê antigo fica nos dados, igual, e já não aparece na página; as ligações para fora continuam nas lições.
                self.assertEqual(d['dossie'], a['dossie'])
                self.assertNotIn('class="task-dossier', pagina)
                self.assertNotIn('tf-origem', pagina)
                licoes = ''.join(ler(x) for x in L.values()) + ler('m9/recursos/f11.js') + ler('m9/recursos/f12.js')
                for facto in d['dossie']:
                    if facto['href'].startswith('http'):
                        self.assertNotIn(facto['href'], pagina)
                        # A ligação da DGE (m9-u1) não está em nenhuma lição do M9: fica só nos dados (pergunta ao docente).
                        self.assertEqual(facto['href'].split('#')[0] in licoes, facto['href'] not in FORA_DAS_LICOES, facto['href'])
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        a1, a2 = (json.loads(antes(rel)) for rel in DADOS_TAREFAS)
        # m9-u1: as condições do dossiê de antes são agora a ordem de ler antes da aula, as alíneas e as linhas de ajuda.
        self.assertIn('Lê o capítulo completo antes da aula e marca dois pormenores', a1['dossie'][1]['facto'])
        self.assertIn('não o confundas com o episódio final', a1['dossie'][2]['facto'])
        self.assertIn('É o primeiro auto de fé do romance: não o confundas com o do último capítulo.', u1['temas'][1]['antes'])
        self.assertIn('regista a editora, o ano e as páginas efetivamente usados', a1['dossie'][0]['facto'])
        self.assertTrue(u1['modo'].startswith(ANTES_DA_AULA))
        self.assertIn(f'lê antes da aula os capítulos{N}I e{N}V de <i>Memorial do Convento</i>', ler(GUIA))
        # m9-u2: as condições do dossiê de antes são agora alíneas e linhas de ajuda.
        self.assertIn('Consulta apenas o texto literário, não o questionário desse recurso.', a2['dossie'][1]['facto'])
        self.assertIn('lê só o texto do romance, não o questionário.', blocos_onde(u2)[1]['frases'][0])
        self.assertIn('localiza no livro duas situações, uma relativa a Blimunda e outra a Scarlatti', a2['dossie'][2]['facto'])
        self.assertIn('As duas situações do teu plano são uma de Blimunda e outra de Scarlatti.', u2['temas'][1]['antes'])
        self.assertIn('A decisão pode ser uma escolha de conteúdo ou de apresentação; não construas uma campanha, um cartaz ou outro produto.', a2['dossie'][3]['facto'])
        self.assertEqual(u2['depois'][0]['ajudas'][:2], ['A decisão pode ser uma escolha de conteúdo ou de apresentação.',
                                                         'Não construas uma campanha, um cartaz ou outro produto: a entrega é só o texto.'])
        self.assertIn('Identifica autor, título, editora, ano e páginas', a2['dossie'][0]['facto'])
        # As palavras da grelha ficam e levam a ponte: «juízo crítico», «indícios».
        self.assertEqual(u1['grelha_nota'], 'A autoavaliação da grelha é só para ti: não se entrega. Na grelha, a tua apreciação chama-se '
                                            '«juízo crítico» e os pormenores chamam-se «indícios».')
        self.assertEqual(u2['grelha_nota'], 'A autoavaliação da grelha é só para ti: não se entrega. Na grelha, as situações do romance '
                                            'também se chamam «indícios».')
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        self.assertEqual(grelhas['m9-u1']['criterios'][0]['nome'], 'Juízo crítico pertinente e desenvolvido')
        self.assertEqual(grelhas['m9-u1']['criterios'][1]['nome'], 'Leitura rigorosa de dois indícios')
        self.assertEqual(grelhas['m9-u2']['criterios'][1]['nome'], 'Utilização rigorosa de duas situações do romance')
        # A objeção define-se com as palavras da lição F10 («a razão de quem discorda»).
        self.assertIn('Uma objeção é a razão de quem discorda de ti.', u2['depois'][1]['ajudas'][0])
        self.assertIn('a razão de quem discorda', no_cartao('10', 5))

    def test_criterios_da_grelha_iguais(self):
        agora, base = json.loads(ler(GRELHAS))['tarefas'], json.loads(antes(GRELHAS))['tarefas']
        self.assertEqual(antes(GRELHAS), do_main(GRELHAS))
        self.assertEqual(list(agora), list(base))
        novas = {'autoavaliacao_so_tua', 'correcao_estreita', 'trocas_aluno'}
        for slug, t in agora.items():
            with self.subTest(grelha=slug):
                self.assertEqual(set(t) - set(base[slug]), novas if slug in SLUGS else set())
                self.assertEqual({k: v for k, v in t.items() if k not in novas} if slug in SLUGS else t, base[slug])
                self.assertEqual(sum(c['max'] for c in t['criterios']), 20)
        self.assertEqual([c['max'] for c in agora['m9-u1']['criterios']], [4, 5, 5, 3, 3])
        self.assertEqual([c['max'] for c in agora['m9-u2']['criterios']], [3, 5, 5, 4, 3])
        for slug in SLUGS:
            t = agora[slug]
            self.assertIs(t['autoavaliacao_so_tua'], True)
            self.assertIs(t['correcao_estreita'], True)
            self.assertEqual(t['trocas_aluno'], TROCAS_GRELHA[slug])
            fonte = json.dumps({k: v for k, v in t.items() if k != 'trocas_aluno'}, ensure_ascii=False)
            for a, _ in t['trocas_aluno']:
                self.assertIn(a, fonte)
            for parte in ('grelha/', 'correcao/'):
                lida = solto(visivel(ler(f'tarefas/{slug}/{parte}index.html'), so_main=False, sem_nav=False))
                self.assertNotRegex(lida, r'(?i)\bnúcleo\b|\bsíntese\b|edição consultada|\btese\b|fora da contagem')
                for c in t['criterios']:
                    self.assertIn(c['nome'], lida)
            grelha = solto(visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False, sem_nav=False))
            esperado = json.dumps(base[slug], ensure_ascii=False)
            for a, b in t['trocas_aluno']:
                esperado = esperado.replace(json.dumps(a, ensure_ascii=False)[1:-1], json.dumps(b, ensure_ascii=False)[1:-1])
            esperado = json.loads(esperado)
            for c in esperado['criterios']:
                for desc, ex in c['niveis'].values():
                    self.assertIn(desc, grelha)
                    self.assertIn(ex, grelha)
                for x in c['custa']:
                    self.assertIn(x, grelha)
            self.assertIn(esperado['produto'], grelha)
            self.assertEqual(grelha.count(NAO_CONTAM), 1)
        for outra in OUTRAS:
            self.assertEqual(ler(f'tarefas/{outra}/grelha/index.html'), do_main(f'tarefas/{outra}/grelha/index.html'), outra)
            self.assertEqual(ler(f'tarefas/{outra}/correcao/index.html'), do_main(f'tarefas/{outra}/correcao/index.html'), outra)

    # ---------- o romance tem direitos de autor: não se copia ----------

    def test_textos_com_direitos_so_as_citacoes_das_licoes_letra_a_letra(self):
        # José Saramago morre em 2010 (o mapa do módulo M9; nenhuma lição do M9 dá o ano): o romance ainda tem direitos.
        self.assertIn('José Saramago (Azinhaga, 1922–Lanzarote, 2010)', ler(MAPA))
        self.assertGreater(2010, 1955)
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            f = json.loads(ler(rel))['facil']
            pagina = ler(enunciado)
            principal = pagina[pagina.index('<main'):pagina.index('</main>')]
            blocos = blocos_onde(f)
            self.assertEqual([o['id'] for o in blocos], [x[0] for x in ONDE[slug]])
            # Nenhum texto copiado: nem versos, nem prosa, nem imagens, nem ligações para fora.
            self.assertEqual(f['textos'], [])
            for fora in ('class="tt-versos"', 'class="tt-prosa"', 'class="tt-texto', 'tt-estrofe', '<img', '<figure', 'data:image', 'href="http',
                         'portoeditora', 'josesaramago.org', 'dge.mec.pt', 'run.unl.pt'):
                self.assertNotIn(fora, principal, fora)
            self.assertEqual(principal.count('<section class="tt-onde"'), len(blocos))
            self.assertEqual(principal.count('<blockquote class="tt-cit">'), sum(len(x[2]) for x in ONDE[slug]))
            citadas = []
            for o, (ident, titulo, cits, fonte, confere) in zip(blocos, ONDE[slug]):
                with self.subTest(tarefa=slug, texto=ident):
                    self.assertEqual(o['titulo'], f'<span class="tt-num">Texto{N}{ident[-1]}</span> {titulo}')
                    # As citações são as que as lições publicam, letra a letra, no cartão indicado; são curtas (no máximo 25
                    # palavras), uma linha cada; nenhuma vem do cartão «O texto» (os excertos longos ficam nas lições).
                    self.assertEqual([(c['intro'], c['linhas']) for c in o['citacoes']], [(i, [l]) for i, l, _, _ in cits])
                    for intro, linha, k, i in cits:
                        self.assertIn(linha, no_cartao(k, i), (k, i, linha))
                        self.assertFalse((cartoes(k)[i - 1].get('rot') or '').startswith('O texto'), (k, i))
                        self.assertLessEqual(len(linha.strip('«»').split()), 25)
                        self.assertTrue(linha.startswith('«') and linha.endswith('»'), linha)
                        self.assertEqual(intro.split(f'lição{N}F')[1][:2], k)
                        citadas.append(linha)
                    # A linha de fonte inteira, letra a letra; o que diz confere-se na lição. Nunca «manual», nunca página.
                    self.assertEqual(o['fonte'], fonte)
                    for k, i, frase in confere:
                        self.assertIn(frase, no_cartao(k, i), (k, i, frase))
                    for rot in re.findall(r'cartão «([^»]+)»', o['fonte']):
                        k = re.findall(r'lição' + N + r'F(\d\d)', o['fonte'])
                        self.assertTrue(any(rot in [c.get('rot') for c in cartoes(x)] + [c.get('titulo') for c in cartoes(x)]
                                            or solto(rot) in [c.get('rot') for c in cartoes(x)] for x in k), rot)
                    self.assertNotIn('manual', o['fonte'])
                    self.assertNotRegex(solto(sem_marcas(o['fonte'])), r'(?i)\bpp?\. ?\d|\bpágina \d|\bpág')
                    for k, i, _ in confere:
                        self.assertIn(f'm9/licao-m9-f{k}/index.html' if k not in ('11', '12', '13') else f'm9/recursos/f{k}.js', o['origem'])
                    bloco = re.search(r'<section class="tt-onde" id="' + ident + r'".*?</section>', pagina, re.S).group(0)
                    self.assertIn(f'<h3 id="{ident}-titulo">{o["titulo"]}</h3>', bloco)
                    for c in o['citacoes']:
                        self.assertIn(f'<p class="tf-p tt-cit-intro">{c["intro"]}</p><blockquote class="tt-cit">{html.escape(c["linhas"][0], quote=False)}</blockquote>', bloco)
                    self.assertIn(f'<p class="tt-fonte">{o["fonte"]}</p>', bloco)
                    self.assertEqual(pagina.count(f'id="{ident}"'), 1)
                    # Fora do bloco, nenhuma citação aparece na página.
                    resto = pagina.replace(bloco, '')
                    for c in o['citacoes']:
                        self.assertNotIn(c['linhas'][0].strip('«»'), resto)
            # Os excertos longos das lições (F01, F02 e F05, cartões «O texto») não estão na página: nenhum pedaço de oito palavras.
            lido = solto(visivel(pagina))
            for k in ('01', '02', '05'):
                for c in cartoes(k):
                    if (c.get('rot') or '').startswith('O texto'):
                        palavras = solto(sem_marcas(c['html'])).split()
                        self.assertGreater(len(palavras), 60)
                        for j in range(0, len(palavras) - 8):
                            pedaco = ' '.join(palavras[j:j + 8])
                            if not any(pedaco in solto(x) for x in citadas):
                                self.assertNotIn(pedaco, lido, (k, pedaco))
            self.assertNotRegex(lido, r'\bmanual\b')
            self.assertNotRegex(lido, r'(?i)\bpp?\. ?\d|\bpágina \d')
            self.assertIn('direitos de autor', lido)
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        # Os blocos ficam no desdobrável de cada tema (fechado no ecrã, aberto em papel); a razão diz-se uma vez, no tema.
        self.assertEqual([[o['id'] for o in t['material']['onde']] for t in u1['temas']], [['texto-1'], ['texto-2']])
        self.assertEqual([[o['id'] for o in t['material']['onde']] for t in u2['temas']], [['texto-1', 'texto-2'], ['texto-3', 'texto-4']])
        for f, ancora in ((u1, 'onde ler o episódio'), (u2, 'onde ler as passagens')):
            self.assertNotIn('temas_material', f)
            for t, k in zip(f['temas'], (1, 2 if f is u1 else 3)):
                self.assertEqual(t['antes'][0], 'O romance tem direitos de autor. Por isso não está copiado nesta página. '
                                 f'Vê <a href="#texto-{k}">{ancora}</a>, por baixo dos passos.')
        # O que a página diz das lições que não citam: a F14 dá só um resumo; nenhuma lição do M9 cita a passagem de Scarlatti.
        self.assertEqual(blocos_onde(u1)[0]['frases'], [f'As lições não citam esta passagem: a lição{N}F14 resume o episódio, sem o citar.'])
        self.assertEqual(blocos_onde(u2)[3]['frases'], ['As lições não citam esta passagem.'])
        todas = ''.join(json.dumps(cartoes(k), ensure_ascii=False) for k in L)
        self.assertEqual(set(re.findall(r'«[^»]*Scarlatti[^»]*»', todas)), {'«O que Scarlatti acrescenta»'})  # (o título do cartão)
        self.assertEqual(blocos_onde(u2)[2]['frases'], [f'A lição{N}F11 aponta duas passagens: o voo da passarola, no capítulo{N}XVI, e a procura de Baltasar, no capítulo{N}XXV.'])
        # Nenhuma lição do M9 diz que o romance está no manual.
        self.assertNotIn('manual', ' '.join(solto(sem_marcas(json.dumps(cartoes(k), ensure_ascii=False))) for k in L if k != '14').lower().replace('manuais/', ''))
        # O molde não ganhou chaves: as do M8 chegam (citações curtas e blocos «onde» no material de cada tema).
        self.assertEqual(ler('scripts/tarefa_facil.py'), do_main('scripts/tarefa_facil.py'))
        self.assertEqual(ler('assets/task-textos.css'), do_main('assets/task-textos.css'))

    def test_exemplos_com_outro_caso(self):
        for slug, rel, enunciado, dados_aq in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS, DADOS_AQUECIMENTOS):
            d = json.loads(ler(rel))
            f = d['facil']
            pagina = ler(enunciado)
            aq = json.loads(ler(dados_aq))
            with self.subTest(tarefa=slug):
                self.assertEqual([len(p['exemplos']) for p in f['depois']], [1, 1])
                apoios = re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>Ver um exemplo com outro caso</summary>.*?</details>', pagina, re.S)
                self.assertEqual(len(apoios), 2)
                self.assertEqual(pagina.count('<aside class="tf-exemplo">'), 2)
                self.assertEqual(pagina.count('tf-so-ecra'), 3)
                juntos = solto(sem_marcas(' '.join(apoios)))
                # Nenhuma palavra reservada do aquecimento, nenhuma citação, nenhum nome do romance.
                cits = [c for x in ONDE[slug] for _, c, _, _ in x[2]]
                for fora in aq['reservadas'] + cits + ['Saramago', 'Memorial', 'rei', 'Blimunda', 'Baltasar', 'Scarlatti', 'Francisco', 'convento',
                                                       'pedra', 'auto de fé', 'sentenças', 'miniatura', 'passarola', 'manual']:
                    self.assertNotRegex(juntos, r'\b' + re.escape(fora.strip('«»')) + r'\b', fora)
                fonte_aq = solto(re.sub(r'_([^_]+)_', r'\1', json.dumps(aq, ensure_ascii=False)))
                for frase in EXEMPLOS_DO_AQUECIMENTO[slug]:
                    self.assertIn(frase, fonte_aq, frase)
                for x in f['depois']:
                    ex = x['exemplos'][0]
                    self.assertIn('outro caso', ex['titulo'])
                    self.assertEqual(ex['contexto'], EXEMPLOS_DO_AQUECIMENTO[slug][0])
                    rotulos = [solto(p['al']) for p in ex['paragrafos']]
                    for r in rotulos:
                        self.assertRegex(r, r'^Alíneas? [a-g]\)(?: e [a-g]\))?:$')
                    letras = set(re.findall(r'([a-g])\)', ' '.join(rotulos)))
                    self.assertTrue(letras <= set('abcdefg'[:len(x['alineas'])]))
                    # As letras dos exemplos são alíneas que existem (o caso é outro: nenhuma alínea da tarefa fica feita).
                    self.assertLessEqual(len(letras), len(x['alineas']))
                # Nenhuma resposta do aquecimento está nos exemplos (fora o caso, que é o mesmo), nem uma frase do aquecimento.
                juntos_min = juntos.lower().replace(EXEMPLOS_DO_AQUECIMENTO[slug][0].lower(), '')
                respostas = respostas_do_aquecimento(aq)
                # 15/11/2026 (revisão): com os cartões de verdadeiro ou falso e as explicações, a lista cresce (era 12).
                self.assertGreaterEqual(len(respostas), 30)
                for r in respostas:
                    self.assertNotRegex(juntos_min, r'\b' + re.escape(r) + r'\b', (slug, r))
                for x in f['depois']:
                    for par in x['exemplos'][0]['paragrafos']:
                        self.assertNotIn(solto(par['t']).rstrip('.').lower(), fonte_aq.lower(), par['t'])
                        # 15/11/2026 (revisão): nem as ideias do aquecimento por outras palavras.
                        self.assertNotRegex(solto(par['t']).lower(), IDEIAS_DO_AQUECIMENTO[slug], par['t'])
                certa = [o['texto'] for o in d['opcional']['opcoes'] if o['certa']]
                self.assertEqual(len(certa), 1)
                self.assertNotIn(certa[0].rstrip('.'), juntos)
                self.assertNotIn(certa[0].rstrip('.').split(' ', 2)[-1].lower(), juntos_min)
        u1, u2 = (json.loads(ler(rel))['facil'] for rel in DADOS_TAREFAS)
        # m9-u2: a decisão do exemplo não é a do aquecimento (as datas nas legendas): são as fotografias lado a lado.
        self.assertNotRegex(' '.join(p['t'] for x in u2['depois'] for p in x['exemplos'][0]['paragrafos']).lower(), r'\bdatas?\b|\bano\b|legenda')
        self.assertEqual(u2['depois'][0]['exemplos'][0]['paragrafos'][0]['t'], 'Pôr lado a lado as fotografias do mesmo lugar, da mais antiga para a mais recente.')
        # m9-u1: o exemplo não diz «ironia» nem «contraste» (a etiqueta que o aquecimento só aceita depois de explicar a relação).
        self.assertNotRegex(' '.join(p['t'] for x in u1['depois'] for p in x['exemplos'][0]['paragrafos']).lower(), r'ironia|contrast|contrap|abaf|exalt|contest')
        for slug in SLUGS:
            self.assertIn('Os exemplos são inventados e usam outros casos. Não são respostas à tarefa.', json.loads(ler(GRELHAS))['tarefas'][slug]['nota'])

    # ---------- as decisões do docente ----------

    def test_tempos_10_10_55_15_em_todos_os_sitios(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            d = json.loads(ler(rel))
            f, pagina = d['facil'], ler(enunciado)
            with self.subTest(tarefa=slug):
                quadro = pagina[pagina.index('<table class="tf-quadro">'):pagina.index('</table>')]
                tempos = [int(x) for x in re.findall(r'<th scope="row">(\d+)' + N + 'min</th>', quadro)]
                self.assertEqual(tempos, [10, 10, 55, 15, 90])
                self.assertEqual(sum(tempos[:4]), 90)
                self.assertEqual(d['aquecer']['minutos'], 10)
                self.assertEqual(f['producao_minutos'], 55)
                self.assertEqual(pagina.count('data-max="10" data-passo="1" data-rotulo="Aquecimento"'), 1)
                self.assertEqual(pagina.count('data-max="55" data-passo="5" data-rotulo="Produção em papel"'), 1)
                self.assertEqual(pagina.count('data-relogio'), 2)
                self.assertEqual(f['kicker'], f'Tarefa individual, 90{N}minutos')
                self.assertEqual(f['fazer'][0], f'Faz o aquecimento (10{N}minutos).')
        for rel in PAGINAS + AQUECIMENTOS + [GUIA, MAPA, PORTEFOLIO]:
            lido = solto(visivel(ler(rel), so_main=False, sem_nav=False))
            self.assertNotRegex(lido, r'(?<![\d,])\b(?:5|60) min(?:utos)?\b|\b[Ss]essenta minutos|\b[Cc]inco minutos de leitura', rel)
        chips = re.findall(r'<a class="cz-row" href="\.\./tarefas/m9-u\d/(aquecimento/)?">.*?<span class="chip">([^<]*)</span>', ler(INDICE), re.S)
        self.assertEqual(chips, [('aquecimento/', f'10{N}min'), ('', f'90{N}min')] * 2)
        guia = ler(GUIA)
        self.assertIn(f'fazes os cartões durante 10{N}minutos. Seguem-se 10{N}minutos de leitura, 55 de produção individual em papel e 15 de revisão e entrega no Teams.', guia)
        blocos = json.JSONDecoder().raw_decode(guia.split('BLOCOS=', 1)[1])[0]
        self.assertEqual([b[0] for b in blocos], [10, 10, 55, 15])
        self.assertEqual(re.findall(r'<b>([^<,]+), (\d+)' + N + r'min</b><span>([^<]*)</span>', guia), [(b[1], str(b[0]), b[2]) for b in blocos])
        self.assertIn('<span class="relogio" id="relogio">10:00</span>', guia)
        for rel in DADOS_AQUECIMENTOS:
            self.assertIn('Dez minutos com consulta, sem nota.', ler(rel))
        # Os tempos do M2 não mudam (o acerto do M2 é só nas frases do guia).
        self.assertEqual(json.JSONDecoder().raw_decode(ler(GUIA_M2).split('BLOCOS=', 1)[1])[0][0::1][0][0], 15)
        self.assertEqual([b[0] for b in json.JSONDecoder().raw_decode(ler(GUIA_M2).split('BLOCOS=', 1)[1])[0]],
                         [b[0] for b in json.JSONDecoder().raw_decode(do_main(GUIA_M2).split('BLOCOS=', 1)[1])[0]])

    def test_consulta_contagem_autoavaliacao_e_aquecimento(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            f, pagina = json.loads(ler(rel))['facil'], ler(enunciado)
            lido = solto(visivel(pagina))
            with self.subTest(tarefa=slug):
                self.assertEqual(f['modo'], (ANTES_DA_AULA + ' ' if slug == 'm9-u1' else '') + CONSULTA)
                self.assertEqual(lido.count('com consulta'), 1)
                self.assertEqual(len(re.findall(r'\bconsultas?\b', lido.lower())), 1)
                cabeca = pagina[pagina.index('<header>'):pagina.index('</header>')]
                self.assertIn(f'<p class="tf-p">{f["modo"]}</p>', cabeca)
                if slug == 'm9-u1':
                    self.assertEqual(lido.count(solto(visivel(ANTES_DA_AULA))), 1)
                    self.assertNotIn('<details', cabeca)
                else:
                    self.assertNotIn('antes da aula', lido)
                self.assertEqual(f['quadro']['notas'][1], NAO_CONTAM)
                self.assertEqual(lido.count(NAO_CONTAM), 1)
                self.assertEqual(solto(visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False)).count(NAO_CONTAM), 1)
                self.assertEqual(f['depois'][0]['meta'], 'Não conta para as palavras.')
                self.assertEqual(f['finais']['texto'], 'Ficam fora da contagem.')
                self.assertTrue(f['grelha_nota'].startswith('A autoavaliação da grelha é só para ti: não se entrega.'))
                self.assertEqual(lido.count('A autoavaliação da grelha é só para ti: não se entrega.'), 1)
                self.assertNotIn('autoavaliação', ' '.join(f['entrega'] + f['verificar'] + [f['entregas']['intro']]))
                grelha, correcao = ler(f'tarefas/{slug}/grelha/index.html'), ler(f'tarefas/{slug}/correcao/index.html')
                self.assertEqual(grelha.count('Esta autoavaliação é só para ti: não se entrega.'), 1)
                self.assertNotIn('Entrega esta autoavaliação', grelha)
                self.assertNotIn('<th class="n">Aluno</th>', correcao)
                self.assertIn('<th class="n">Docente</th>', correcao)
                self.assertIn('<th class="n">Aluno</th>', do_main(f'tarefas/{slug}/correcao/index.html'))
                self.assertEqual(pagina.count('href="aquecimento/"'), 1)
                self.assertIn(f'<ol class="tf-fazer"><li>Faz o aquecimento (10{N}minutos).<span class="task-aquecer tf-abrir"><a href="aquecimento/">Abrir o aquecimento em cartões</a></span></li>', cabeca)
                self.assertNotIn('Antes de começar: aquecer', lido)
                # A verificação: no máximo dez perguntas de sim ou não, na primeira pessoa.
                self.assertLessEqual(len(f['verificar']), 10)
                self.assertEqual(len(f['verificar']), {'m9-u1': 9, 'm9-u2': 10}[slug])
                for x in f['verificar']:
                    self.assertTrue(x.endswith('?'), x)
                    self.assertEqual(x.count('?'), 1, x)
                    self.assertRegex(solto(x), r'\b(?:meu|minha|Tenho|Expliquei|Escolhi|Indiquei|Escrevi|Anotei|Fiz|Relacionei|Apresentei|penso)\b', x)
                self.assertEqual(pagina.count('<label><input type="checkbox">'), len(f['verificar']))
                ordem = [cabeca.index(x) for x in ('O que vais fazer</h2>', 'O que entregas</h2>', 'Tempo e tamanho</h2>', '<p class="task-grelha">')]
                self.assertEqual(ordem, sorted(ordem))
        self.assertEqual(solto(ler(GUIA)).count(NAO_CONTAM), 1)

    def test_tudo_junto_as_mesmas_palavras(self):
        for rel in PAGINAS + [GUIA]:
            lido = solto(visivel(ler(rel), so_main=False, sem_nav=False))
            with self.subTest(pagina=rel):
                self.assertNotRegex(lido, r'(?i)\bnúcleo\b|\bsíntese\b|\bplanificação\b|opção escolhida|edição consultada|\bexemplar\b')
                self.assertNotRegex(lido, r'(?i)para todos\b|\bsó um\b|Relembrar|Fecha o trabalho')
        for slug in SLUGS:
            lido = solto(visivel(ler(f'tarefas/{slug}/index.html')))
            for palavra in ('plano', 'duas linhas finais', 'a letra do teu tema', 'a edição que usaste'):
                self.assertIn(palavra, lido, palavra)
            self.assertNotRegex(lido, r'(?i)\btese\b|\bopção\b')
            for parte in ('grelha/', 'correcao/'):
                self.assertIn('o plano e as duas linhas finais', solto(visivel(ler(f'tarefas/{slug}/{parte}index.html'), so_main=False)), parte)
        grelha_u1 = solto(visivel(ler('tarefas/m9-u1/grelha/index.html'), so_main=False))
        grelha_u2 = solto(visivel(ler('tarefas/m9-u2/grelha/index.html'), so_main=False))
        for g in (grelha_u1, grelha_u2):
            self.assertIn('Não indicar a edição que usaste (a editora e o ano).', g)
            self.assertIn('falta a contagem e a letra do tema', g)
        self.assertIn('Repetir a decisão como se fosse uma resposta.', grelha_u2)
        # As palavras da grelha que o enunciado usa: «efeito», «procedimento», «objeção», «decisão», «diferença entre épocas».
        for palavra in ('efeito', 'procedimento', 'juízo crítico', 'indícios'):
            self.assertIn(palavra, solto(visivel(ler(ENUNCIADOS[0]))))
        for palavra in ('objeção', 'decisão', 'situações do romance', 'indícios'):
            self.assertIn(palavra, solto(visivel(ler(ENUNCIADOS[1]))))
        indice = solto(visivel(ler(INDICE), so_main=False, sem_nav=False))
        self.assertEqual(indice.count('tema A ou B, plano, texto, revisão e fotografias no Teams.'), 3)
        self.assertNotIn('planificação', indice)
        mapa = solto(visivel(ler(MAPA), so_main=False, sem_nav=False))
        self.assertIn('As duas linhas finais fazem parte da entrega e não criam outro registo de conclusão.', mapa)
        self.assertNotIn('A síntese faz parte', mapa)
        portefolio = solto(visivel(ler(PORTEFOLIO), so_main=False, sem_nav=False))
        self.assertEqual(portefolio.count('tema A ou B, plano, texto e duas linhas finais.'), 2)
        self.assertNotRegex(portefolio, r'(?i)\bnúcleo\b')
        # 15/11/2026 (revisão): o módulo não fica a meio caminho: nem o índice, nem o mapa, nem o portefólio dizem «síntese»
        # (no texto visível nem na fonte); as duas linhas finais aparecem nos três.
        for rel, lido in ((INDICE, indice), (MAPA, mapa), (PORTEFOLIO, portefolio)):
            self.assertNotRegex(lido, r'(?i)síntese', rel)
            self.assertNotRegex(ler(rel), r'(?i)síntese', rel)
            self.assertIn('duas linhas finais', lido, rel)
        self.assertEqual(indice.count('As duas linhas finais fazem parte da entrega.'), 1)
        self.assertEqual(portefolio.count('As duas linhas finais fazem parte da tarefa da unidade.'), 2)
        for rel in AQUECIMENTOS + DADOS_AQUECIMENTOS:
            self.assertEqual(ler(rel), do_main(rel), rel)
            self.assertNotRegex(ler(rel), r'(?i)\bnúcleo\b|\bsíntese\b')

    def test_guia_portefolio_indice_mapa_e_acertos_so_mudam_nas_trocas_da_camada(self):
        for rel, trocas in TROCAS_MODULO.items():
            with self.subTest(pagina=rel):
                esperado = do_main(rel)
                self.assertEqual(esperado, antes(rel))
                for a, b, n in trocas:
                    self.assertEqual(esperado.count(a), n, a[:60])
                    esperado = esperado.replace(a, b)
                self.assertEqual(esperado, ler(rel))
        # Nos guias do M9 e do M2 saem a «Autoavaliação» que se copiava para o Teams e o par de trabalho; nada entra no lugar.
        for rel, regra in ((GUIA, '<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica.</li></ol>Só depois levantas o braço.</div>'),
                           (GUIA_M2, '<div class="regra"><b>Dois antes de mim.</b> Antes de chamares o docente: 1) relê o enunciado; 2) vê a rubrica. Só depois levantas o braço.</div>')):
            guia = ler(rel)
            lido = solto(visivel(guia, so_main=False, sem_nav=False))
            self.assertNotRegex(lido, r'(?i)autoavaliação|par de trabalho|Três antes de mim|três antes de mim')
            for fora in ('AUTOAVALIAÇÃO', 'r-auto', 'dataset.auto', 'closest(".niveis button")', 'três antes de mim'):
                self.assertNotIn(fora, guia, (rel, fora))
            self.assertEqual(guia.count(regra), 1)
            self.assertIn('"VERIFICAÇÃO"];', guia)
            self.assertIn('O docente vê o teu plano, as notas e a lista.', guia)
            self.assertEqual(guia.count('regra dos dois antes de mim'), 2 if rel == GUIA_M2 else 0)
        self.assertEqual(len(TROCAS_MODULO[GUIA]), 11)
        self.assertEqual(len(TROCAS_MODULO[GUIA_M2]), 9)
        # As tarefas e os tempos do M2 não mudam.
        for slug in ('m2-u1', 'm2-u2'):
            for p in (ROOT / 'tarefas').glob(f'{slug}*/**/index.html'):
                self.assertEqual(p.read_bytes().decode('utf-8'), do_main(p.relative_to(ROOT).as_posix()))
        portefolio = solto(visivel(ler(PORTEFOLIO), so_main=False, sem_nav=False))
        self.assertNotRegex(portefolio, r'(?i)autoavaliação|trabalho de equipa|em equipa|em grupo|em pares')
        self.assertIn('É a base da avaliação qualitativa do módulo (40 %): autonomia, responsabilidade, pensamento crítico, entre outros.', portefolio)
        # O acerto do M7: «opinião», como a m7-u3 diz em todo o lado; nenhuma «tese» no índice do M7.
        indice_m7 = solto(visivel(ler(INDICE_M7), so_main=False, sem_nav=False))
        self.assertIn('No fim, defendes uma opinião com um verso de Mensagem explicado no contexto', indice_m7)
        self.assertNotRegex(indice_m7, r'\btese\b')
        # A m7-u3 chama-lhe «opinião»; só a ponte para as lições diz «tese».
        m7u3 = solto(visivel(ler('tarefas/m7-u3/index.html')))
        self.assertEqual(re.findall(r'[^.]*\btese\b[^.]*\.', m7u3), [' Nas lições, a opinião que defendes chama-se «tese».'])

    # ---------- as regras do texto ----------

    def test_regras_do_texto(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                texto = visivel(ler(rel))
                baixo = texto.lower()
                for palavra in ('professor', 'jogar', 'jogador', 'ficha', 'folha', 'em grupo', 'em pares', 'colega', 'fernandes'):
                    self.assertNotIn(palavra, baixo, palavra)
                self.assertNotRegex(baixo, r'\bjog(?:o|os|a|am|ar)\b')
                self.assertNotIn('—', texto)
                self.assertNotRegex(texto, r'\bQual (?!d[aeo]s? )')
                self.assertNotRegex(texto, r'\b[Vv]ocê\b')
        for slug in SLUGS:
            fonte = ler(f'tarefas/{slug}/index.html')
            texto = visivel(fonte)
            principal = fonte[fonte.index('<main'):fonte.index('</main>')]
            with self.subTest(enunciado=slug):
                self.assertNotIn('·', texto)
                self.assertNotRegex(texto, r'[—–]')
                # O título do romance sempre em itálico.
                sem_italicos = re.sub(r'<i>[^<]*</i>|alt="[^"]*"|aria-label="[^"]*"', '', principal)
                self.assertNotIn('Memorial do Convento', sem_italicos)
                self.assertGreaterEqual(principal.count(MR), 4)
                for padrao in (r'\b(?:Texto|Textos|Pergunta|pergunta|Tema|Temas|tema|Lição|lição|capítulo|capítulos|Alínea|Alíneas|alínea) (?:\d|[AB]\b|[IVX]+\b|F\d|[a-h]\))',
                               r'\d (?:min|minutos|palavras)\b', r'(?:\d|\]|\)|\b[IVX]+) (?:a|e|ou) (?:\d|\[|[a-h]\)|[IVX]+\b)', r'\bA (?:ou|e) B\b'):
                    self.assertNotRegex(visivel(fonte.replace('<span class="sr-only">Tema </span>', '')), padrao)
                self.assertNotRegex(texto, r'[“”"]')
                self.assertNotRegex(texto.lower(), r'\bsozinh[oa]\b|\bo aluno\b|\ba aluna\b|\bpar de\b|\bem equipa\b')
                # A fala do aluno em discurso direto vai entre «».
                if slug == 'm9-u2':
                    self.assertIn('«Há quem diga que…»', texto)
        for rel in ('scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py', 'scripts/grelhas_tarefas.py', 'scripts/tarefas_faceis_m9_20261114.py'):
            self.assertNotIn('por aprovar', ler(rel), rel)

    # ---------- o contrato da página ----------

    def test_contrato_da_pagina(self):
        for slug, rel, enunciado in zip(SLUGS, DADOS_TAREFAS, ENUNCIADOS):
            d = json.loads(ler(rel))
            f, fonte = d['facil'], ler(enunciado)
            p = Pagina(fonte)
            with self.subTest(tarefa=slug):
                self.assertEqual(fonte.count('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil '
                                             'data-task-opening="Começar" data-task-index="nomes">'), 1)
                self.assertEqual([x[0] for x in p.raiz], ['nav', 'header', 'section', 'section', 'section', 'section', 'section'])
                self.assertEqual(['Começar'] + [x[2] for x in p.raiz if x[0] == 'section'], CARTOES_NOMES)
                self.assertEqual([x[1] for x in p.raiz if x[0] == 'section'], ['tema', 'o-teu-plano', 'o-teu-texto', 'entregar', 'apoios'])
                self.assertEqual(len(p.ids), len(set(p.ids)), [x for x in p.ids if p.ids.count(x) > 1])
                self.assertEqual(p.temas, ['A', 'B'])
                self.assertEqual(p.perguntas, [('1', True)])
                self.assertEqual(len(p.opcoes), 3)
                self.assertEqual([o['data-correct'] for o in p.opcoes].count('true'), 1)
                self.assertEqual(fonte.count('<details data-task-optional-preparation><summary>Experimentar uma pergunta</summary>'), 1)
                tema = fonte[fonte.index('<section class="task-section tf-tema"'):fonte.index('<section class="task-section tf-pergunta" id="o-teu-plano"')]
                self.assertLess(tema.index('data-rotulo="Produção em papel"'), tema.index('<div class="task-themes">'))
                self.assertIn(f'data-chave="pt-relogio:tarefas/{slug}:producao"', tema)
                principal = fonte[fonte.index('<main'):fonte.index('</main>')]
                for href in re.findall(r'<a href="([^"]+)"', principal):
                    if href.startswith('#'):
                        self.assertIn(href[1:], p.ids, href)
                    else:
                        self.assertFalse(href.startswith('http'), href)
                        alvo = (ROOT / 'tarefas' / slug / href.split('#')[0]).resolve()
                        self.assertTrue((alvo / 'index.html').is_file() if not alvo.suffix else alvo.is_file(), href)
                self.assertEqual(len(re.findall(r'<a href="#texto-\d">', principal)), 2)
                self.assertEqual(f['folha_versao'], '20261113-facil-12')
                self.assertEqual(fonte.count('assets/task-textos.css?v=20261113-facil-12"'), 1)
                self.assertEqual(fonte.count('task-textos.css'), 1)
                self.assertIn('assets/task-reader.js?v=20261112-facil-7"', fonte)
                self.assertEqual(fonte.count('<details'), 5)
                self.assertEqual(fonte.count('<details class="tf-so-tema">'), 2)
                self.assertEqual(fonte.count('<button type="button" data-task-print hidden>Imprimir o enunciado</button>'), 1)
                self.assertEqual(fonte.count('<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>'), 1)
                # «Rever a matéria»: cada lição existe, tem o título dito e as secções que se mandam reler; o que a linha resume está lá.
                self.assertEqual([x['para'] for x in f['rever']], [x[0] for x in REVER[slug]])
                for x, (para, k, titulo, seccoes, frase) in zip(f['rever'], REVER[slug]):
                    self.assertTrue(x['texto'].startswith(f'Lição{N}F{k}, <a href="../../m9/licao-m9-f{k}/">{titulo}</a>'), x['texto'])
                    arr = cartoes(k)
                    self.assertEqual(html.unescape(arr[0]['titulo']), titulo, k)
                    rotulos = [c.get('rot') for c in arr if c['t'] == 'ler']
                    for s in seccoes:
                        self.assertIn(f'«{s}»', x['texto'])
                        self.assertIn(s, rotulos, (k, s))
                    seccao = ''.join(c.get('html', '') + c.get('titulo', '') for c in arr if c.get('rot') in seccoes)
                    self.assertIn(frase, seccao, (k, frase))
                    # 15/11/2026 (revisão): nenhuma pontuação dupla depois de um título que acaba em «?» («obra?. Relê»).
                    self.assertNotRegex(x['texto'], r'[?!]</a>\s*[.,:;]|[?!][.,:;]', x['texto'])
                self.assertNotRegex(solto(visivel(fonte)), r'[?!]\s*[.,:;]')
        # 15/11/2026 (revisão): na m9-u2, a linha «O teu texto» diz as palavras do enunciado («objeção», «resposta») e liga-as às
        # da lição F10, que estão, letra a letra, no seu «Para entender».
        u2 = json.loads(ler(DADOS_TAREFAS[1]))['facil']
        linha = [x['texto'] for x in u2['rever'] if x['para'] == 'O teu texto'][0]
        self.assertTrue(linha.endswith('Relê «Para entender»: a objeção (na lição, «contra-argumento») e a resposta (na lição, «refutação»).'), linha)
        entender = ''.join(c.get('html', '') for c in cartoes('10') if c.get('rot') == 'Para entender')
        for termo in ('Contra-argumento', 'Refutação', 'a razão de quem discorda', 'a resposta a essa razão'):
            self.assertIn(termo, entender, termo)
        enunciado_u2 = solto(visivel(ler(ENUNCIADOS[1])))
        for termo in ('Uma objeção é a razão de quem discorda de ti.', 'Responde à objeção.'):
            self.assertIn(termo, enunciado_u2, termo)
        for slug in OUTRAS:
            self.assertEqual(ler(f'tarefas/{slug}/index.html'), do_main(f'tarefas/{slug}/index.html'))

    # ---------- as outras tarefas não mudam ----------

    def test_as_outras_tarefas_nao_mudam(self):
        r = subprocess.run(['git', 'ls-tree', '-r', '--name-only', BASE_COMMIT, 'tarefas', 'docs/pedagogia/tarefas-escolha', 'docs/pedagogia/aquecimentos',
                            'docs/pedagogia/tarefas-individuais', GRELHAS], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        nomes = r.stdout.split()
        self.assertGreater(len(nomes), 100)
        na_arvore = sorted(p.relative_to(ROOT).as_posix() for pasta in ('tarefas', 'docs/pedagogia/tarefas-escolha', 'docs/pedagogia/aquecimentos',
                                                                      'docs/pedagogia/tarefas-individuais') for p in (ROOT / pasta).rglob('*') if p.is_file())
        self.assertEqual(sorted(n for n in nomes if n != GRELHAS), na_arvore)
        iguais = 0
        for rel in nomes:
            if rel in FICHEIROS:
                continue
            with self.subTest(igual_ao_main=rel):
                self.assertEqual((ROOT / rel).read_bytes(), subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True).stdout)
                iguais += 1
        # Nestas pastas, a camada muda nove ficheiros; todos os outros são os do main, byte a byte (as outras onze tarefas de escolha,
        # as duas individuais do M7, as suas grelhas, correções e aquecimentos, e os aquecimentos do M9).
        self.assertEqual(iguais, len(nomes) - 9)
        self.assertEqual(sorted(f for f in FICHEIROS if f in nomes), sorted(DADOS_TAREFAS + [GRELHAS] + PAGINAS))
        for slug in OUTRAS + SLUGS:
            self.assertIn('facil', json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json')), slug)
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/tarefas_individuais_faceis.py', '--saida', tmp], ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            self.assertGreaterEqual(len(geradas), 13 + 26 + 2 + 20)
            for slug in OUTRAS + SLUGS:
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertIn(f'tarefas/{slug}/{parte}index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())

    # ---------- a camada ----------

    def test_camada_fechada_reversivel_e_no_topo(self):
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m9_20261114', 'tarefas-faceis-m9-edits-20261114'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m8_20261113', 'tarefas-faceis-m8-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(len(verificar_camadas.LAYERS), 53)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 53)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertIn('não se edita à mão', MANIFESTO['_nota'])
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(len(FICHEIROS), 15)
        self.assertEqual(len(set(FICHEIROS)), 15)
        self.assertEqual(len(TROCAS), sum(len(v['edits']) for v in MANIFESTO['files'].values()))
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 15 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        for t in TROCAS:
            self.assertTrue(t['achado'].startswith('14/11/2026: '), t['local'])
            self.assertEqual(t['ocorrencias'], 1)
            self.assertNotIn('—', t['local'])
        for rel, registo in MANIFESTO['files'].items():
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = antes(rel)
                self.assertEqual(sha_lf(base), registo['base_sha256_lf'])
                self.assertNotEqual(base, atual)
                de_novo = base
                for e in registo['edits']:
                    self.assertEqual(de_novo.count(e['old']), e['occurrences'], e['location'])
                    de_novo = de_novo.replace(e['old'], e['new'])
                self.assertEqual(de_novo, atual)
                self.assertEqual(do_main(rel), base)
                self.assertEqual(undo_tarefas_faceis_m9_1114(rel, atual), base)
                self.assertEqual(undo_tarefas_faceis_m9_1114(rel, base), base)
        # Com as camadas das tarefas do M8, do M7 e do M3, que ficam por baixo, partilha os dados das grelhas (e, com a do M7, o índice do
        # M7). O desfazer da auditoria tira primeiro esta e depois as outras, até à grelha sem nenhuma das chaves novas.
        m8, m7, m3 = (json.loads(ler(x))['files'] for x in (M8F, M7F, M3F))
        self.assertEqual(set(MANIFESTO['files']) & set(m8), {GRELHAS})
        self.assertEqual(set(MANIFESTO['files']) & set(m7), {GRELHAS, INDICE_M7})
        self.assertEqual(sha_lf(antes(GRELHAS)), m8[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(antes(INDICE_M7)), m7[INDICE_M7]['after_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m8_1113(GRELHAS, ler(GRELHAS))), m8[GRELHAS]['base_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m7_1113(INDICE_M7, ler(INDICE_M7))), m7[INDICE_M7]['base_sha256_lf'])
        sem_todas = undo_tarefas_faceis_m3_1112(GRELHAS, ler(GRELHAS))
        self.assertEqual(sha_lf(sem_todas), m3[GRELHAS]['base_sha256_lf'])
        for chave in ('autoavaliacao_so_tua', 'trocas_aluno'):
            self.assertNotIn(chave, sem_todas)
        # Confere-se também cada camada de baixo com esta desfeita primeiro.
        for camada, manifesto in (('tarefas_faceis_m8_20261113', M8F), ('tarefas_faceis_m7_20261113', M7F)):
            cadeia = ['--desfazer-antes', MANIFESTO_REL] + (['--desfazer-antes', M8F] if manifesto == M7F else [])
            r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', f'scripts/{camada}.json', '--manifesto', manifesto, '--verificar'] + cadeia,
                               cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m9_20261114', ROOT / 'scripts/tarefas_faceis_m9_20261114.py')
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        todas, finais = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', ler(CAMADA_REL))
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(sorted(C.FICHEIROS), sorted(FICHEIROS))
        self.assertEqual(C.BASE_COMMIT, BASE_COMMIT)
        for rel, (a, b) in finais.items():
            self.assertEqual(a, antes(rel), rel)
            self.assertEqual(b, ler(rel), rel)
        for nome in ('tarefas_faceis_m8_20261113', 'tarefas_faceis_m7_20261113', 'tarefas_faceis_m6_20261113', 'tarefas_faceis_m5_20261113',
                     'tarefas_faceis_m1_20261113', 'tarefas_faceis_m3_20261112', 'cuidado_m9_20261112'):
            spec = importlib.util.spec_from_file_location(nome, ROOT / f'scripts/{nome}.py')
            outra = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(outra)
            self.assertEqual(outra.construir()[0], json.loads(ler(f'scripts/{nome}.json')), nome)
        partilhados = set(MANIFESTO['files']) & set(json.loads(ler('tests/fixtures/cuidado-m9-edits-20261112.json'))['files'])
        self.assertTrue({GUIA, INDICE, MAPA, PORTEFOLIO} <= partilhados, partilhados)

    def test_leitura_historica_dos_enunciados(self):
        import tarefas_claras_historico as historico
        claras = json.loads(ler('tests/fixtures/tarefas-claras-edits-20261110.json'))['files']
        nossos = sorted(set(MANIFESTO['files']) & set(claras))
        self.assertEqual(nossos, sorted(DADOS_TAREFAS + ENUNCIADOS))
        for rel in nossos:
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                antes_192 = historico.desfazer(rel, atual)
                self.assertEqual(sha_lf(antes_192), claras[rel]['base_sha256_lf'])
                self.assertEqual(historico.desfazer(rel, antes(rel)), antes_192)
                self.assertEqual(historico.desfazer(rel, antes_192), antes_192)
        m3 = json.loads(ler(M3F))['files']
        m7 = json.loads(ler(M7F))['files']
        for rel in MANIFESTO['files']:
            with self.subTest(faceis=rel):
                sem = historico.desfazer_faceis(rel, ler(rel))
                esperado = {GRELHAS: m3[GRELHAS]['base_sha256_lf'], INDICE_M7: m7[INDICE_M7]['base_sha256_lf']}.get(rel, MANIFESTO['files'][rel]['base_sha256_lf'])
                self.assertEqual(sha_lf(sem), esperado)
                self.assertEqual(historico.desfazer_faceis(rel, sem), sem)
                if rel not in (GRELHAS, INDICE_M7):
                    self.assertEqual(sem, antes(rel))
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer_faceis(path, text):'):fonte.index('def desfazer(path, text):')]
        self.assertLess(corpo.index('TAREFAS_FACEIS_M9.get(rel)'), corpo.index('TAREFAS_FACEIS_M8.get(rel)'))
        self.assertIn("assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M9 mais fáceis de fazer não confere: {rel}'", corpo)

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_tarefas_faceis_m9_1114(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m8_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m9_1114\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('tarefas-faceis-m9-edits-20261114.json'), sala.index('tarefas-faceis-m8-edits-20261113.json'))
        self.assertIn("raise ManifestoDesatualizado(f'{rel}: tarefas do M9 mais fáceis de fazer não confere')", sala)
        self.assertIn("return desfazer_faceis(rel, (ROOT / rel).read_bytes().decode('utf-8'))", ler('scripts/cuidado_m9_20261112.py'))
        indices = ler('scripts/cartaz_indices_148_20261106.py')
        corpo = indices[indices.index('def base(rel):'):]
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M9.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M8.read_text'))
        for rel in ('scripts/tarefas_faceis_m3_20261112.py', 'scripts/tarefas_faceis_m1_20261113.py', 'scripts/tarefas_faceis_m5_20261113.py',
                    'scripts/tarefas_faceis_m6_20261113.py', 'scripts/tarefas_faceis_m7_20261113.py', 'scripts/tarefas_faceis_m8_20261113.py'):
            fonte = ler(rel)
            leitura = fonte[fonte.index('def ler(rel):'):fonte.index('def base(rel):')]
            self.assertIn("m9 = ROOT / 'tests/fixtures/tarefas-faceis-m9-edits-20261114.json'", leitura, rel)
            if 'm8 = ROOT' in leitura:
                self.assertLess(leitura.index('m9 = ROOT'), leitura.index('m8 = ROOT'), rel)
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs', 'tests/browser_creditos_i_pt1.cjs'):
            texto = ler(rel)
            self.assertEqual(texto.count('for(const e of [...((tarefasFaceisM9['), 1, rel)
            self.assertLess(texto.index('((tarefasFaceisM9['), texto.index('((tarefasFaceisM8['), rel)
        # Em todos os fluxos e testes: onde a camada do M8 se desfaz, a do M9 desfaz-se logo antes, sem nada pelo meio, e é a primeira.
        fluxos = sorted((ROOT / '.github/workflows').glob('*.yml'))
        com_cadeia = 0
        for p in fluxos:
            fluxo = p.read_text('utf-8')
            self.assertEqual(fluxo.count(f'--desfazer-antes {M8F}'), fluxo.count(f'--desfazer-antes {meu} --desfazer-antes {M8F}'), p.name)
            self.assertEqual(fluxo.count(f'--desfazer-antes {meu}'), fluxo.count(f'--verificar --desfazer-antes {meu}'), p.name)
            self.assertEqual(fluxo.count("'scripts/tarefas_faceis_m8_20261113.*'"), fluxo.count("'scripts/tarefas_faceis_m9_20261114.*'"), p.name)
            self.assertEqual(fluxo.count(f"'{M8F}'"), fluxo.count(f"'{meu}'"), p.name)
            self.assertEqual(fluxo.count("- 'tests/test_tarefas_faceis_m8.py'"), fluxo.count("- 'tests/test_tarefas_faceis_m9.py'"), p.name)
            self.assertEqual(fluxo.count("- 'tests/browser_tarefas_faceis_m8.py'"), fluxo.count("- 'tests/browser_tarefas_faceis_m9.py'"), p.name)
            com_cadeia += bool(fluxo.count(f'--desfazer-antes {meu}'))
        self.assertEqual(com_cadeia, 7)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name in ('test_tarefas_faceis_m9.py',):
                continue
            texto = p.read_text('utf-8')
            with self.subTest(teste=p.name):
                self.assertEqual(texto.count(f"'--desfazer-antes', '{M8F}'"), texto.count(f"'--desfazer-antes', '{meu}', '--desfazer-antes', '{M8F}'"))
                self.assertEqual(texto.count(f'--desfazer-antes {M8F}'), texto.count(f'--desfazer-antes {meu} --desfazer-antes {M8F}'))
                for velho, novo in (('t8f', 't9f'), ('T8F', 'T9F'), ('M8F', 'M9F')):
                    self.assertEqual(texto.count('--desfazer-antes {%s}' % velho), texto.count('--desfazer-antes {%s} --desfazer-antes {%s}' % (novo, velho)))
                    self.assertEqual(texto.count("ROOT/'{%s}'," % velho), texto.count("ROOT/'{%s}',ROOT/'{%s}'," % (novo, velho)))
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m8_20261113.json --manifesto {M8F} --verificar --desfazer-antes {meu}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py {CAMADA_REL} --manifesto {meu} --verificar\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m9.py' -v\n", tarefas)
        self.assertIn('      - name: Tarefas do M9 mais fáceis de fazer\n        run: python tests/browser_tarefas_faceis_m9.py\n', tarefas)
        self.assertLess(tarefas.index("-p 'test_tarefas_faceis_m8.py'"), tarefas.index("-p 'test_tarefas_faceis_m9.py'"))
        for caminho in ("'m9/**'", "'m2/guia-da-tarefa-m2/**'", "'m7/index.html'", "'tarefas/**'", "'scripts/tarefa_facil.py'",
                        "'docs/pedagogia/tarefas-escolha/**'", "'docs/pedagogia/grelhas-tarefas-20261027.json'"):
            self.assertIn(f'      - {caminho}\n', tarefas, caminho)
        self.assertEqual(tarefas.count('timeout-minutes: 40'), 1)
        self.assertEqual(re.findall(r'timeout-minutes: \d+', tarefas), re.findall(r'timeout-minutes: \d+', do_main('.github/workflows/pt-tarefas-qa.yml')))
        # Este teste lê o main de partida (git show): os trabalhos que o correm descarregam o histórico (fetch-depth: 0).
        trabalho = tarefas[tarefas.index('  lessons:'):]
        self.assertLess(trabalho.index('fetch-depth: 0'), trabalho.index('actions/setup-python'))
        correm = [p.name for p in fluxos if "-p 'test_tarefas_faceis_m9.py'" in p.read_text('utf-8') or re.search(r'unittest discover -s tests(?: -v)?\s*$', p.read_text('utf-8'), re.M)]
        self.assertEqual(correm, ['pt-tarefas-qa.yml'])


if __name__ == '__main__':
    unittest.main()
