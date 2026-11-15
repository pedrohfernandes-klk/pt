#!/usr/bin/env python3
"""15/11/2026: a fila final do pedido: o exame diz que o alvo das sessões é meta da sessão e não limite do exame, a síntese e a
exposição ficam ditas como treino, a referência de 2026 diz que a de 2027 ainda não está disponível, e a lição M3-F05 conta os versos
do poema (de 5 em 5) sem contar os rótulos «Mote» e «Voltas». O «Item N da prova» não muda (ver abaixo). Acrescenta o resto da decisão do docente de 15/11/2026,
«síntese integrada» → «duas linhas finais» (ver o fim desta nota).

Ficheiros (3 do Exame e da M3-F05, mais os 14 da decisão «duas linhas finais», no fim desta nota):
- assets/exame/app.js: a linha de alvo da sessão («Meta da sessão: ….», sem a frase «Não é um limite do exame.», que é falsa nas sessões 24 e 25, cujo alvo de 200 a 350 palavras é o limite do Grupo III; nas sessões 20 e 23 a ressalva está no prompt), a versão para imprimir («Meta da
  sessão: …») e a página «Programa e fontes» («A Informação-Prova de 2027 ainda não está disponível.»; os dados, com
  referenceYear 2026, já diziam a verdade e não mudam);
- assets/exame/sessoes.json: o critério da sessão 20 («Cheguei à meta de treino de 80 a 100 palavras.» em vez de «Respeitei as 80 a
  100 palavras.»), o prompt da sessão 20 («Isto é um treino de síntese, não um item do exame.») e o da sessão 23 («A extensão é a meta
  desta sessão, não uma regra do exame: no exame, a breve exposição do item I.7 não tem limite de palavras e pede uma só obra.»; as
  expressões «texto expositivo de 200 a 350 palavras» e «em duas obras estudadas» ficam, porque scripts/exame_treinos_dados/exposicao.py
  as confere por assert);
- m3/licao-m3-f05/index.html: a numeração dos versos de «Descalça vai para a fonte»: os números 5 e 10 estavam duas linhas fora do
  sítio (o 5 no rótulo «Voltas», o 10 no oitavo verso). O verso 5 é «O testo nas mãos de prata»; o 10, o último, «Vai formosa, e
  não segura»; o oitavo, «Traz a vasquinha de cote», fica sem número.

Fica de fora (e porquê):
- Os 20 rótulos «Item N da prova»: prender o espaço (U+00A0) parte o motor (assets/exame/provas-licao.js, scripts/provas/opcoes.py) e os
  testes, que os reconhecem com espaço normal de propósito.
- «Onipotente»/«Omnipotente» (Os Lusíadas, VIII, 99): o repositório não prova a grafia nem a edição; as duas famílias de páginas
  discordam entre si e ficam como estão até haver edição que as sustente.
- As perguntas de Teresa na lição M5-F08: o repositório só tem o original de Camilo da terceira pergunta, e não se inventa o das outras
  duas.
- O exame/provas/, o scripts/provas/dados/, os aquecimentos do exame e os textos das sessões 24 e 25 (já verdadeiros).

Duas linhas finais (15/11/2026, decisão do docente), o que a camada sintese_duas_linhas_20261115 deixou por fazer, com as mesmas frases:
- o M2: o índice, o portefólio, o mapa e o guia da tarefa (16 trocas, iguais às do M1);
- m1/todos e m7/todos («com consulta e duas linhas finais»), m1/licao-m1-f11 («As duas linhas finais ficam na Tarefa da Unidade 2.»);
- os planos m1/aulas/aula-06 e aula-14 e m4/aulas/aula-08, aula-15 e aula-18 («O fecho e as duas linhas finais fazem parte da aula de
  tarefa.»);
- o portefólio do M4 («já fotografadas; não escreves outras») e o do M8 («sem outra escrita obrigatória», nas duas retomas).
Ficam as perguntas de escolha das lições, «síntese oral ou no caderno» e a chave «synthesis». O portefólio do M8 e o do M4 partilham
ficheiro com sintese_duas_linhas_20261115 e com tarefa_m4u2_tema_b_20261115: estas desfazem esta camada primeiro.

Nenhum destes ficheiros sai de um gerador nem de dados que o reescrevam: assets/exame/sessoes.json e app.js são os ficheiros
editados pelas camadas do Exame, e a lição M3-F05 é página escrita. A camada é literal e fica no topo.

Constrói scripts/fila_final_20261115.json, a camada literal, que se aplica com scripts/aplicar_trocas.py; o manifesto fica em
tests/fixtures/fila-final-edits-20261115.json:

  python3 scripts/fila_final_20261115.py
  python3 scripts/aplicar_trocas.py scripts/fila_final_20261115.json \\
      --manifesto tests/fixtures/fila-final-edits-20261115.json \\
      --base-commit 4f4135bf679176c6c8e4abda543837632aad7325 --nota "…"

Fica no topo da pilha (scripts/verificar_camadas.py, LAYERS[0]), por cima de «duas linhas finais» (sintese_duas_linhas_20261115), com a
qual não partilha ficheiros. Partilha ficheiros com camadas mais antigas (as do Exame, as do cuidado do M3, do M6 e do M9, as lições
do M1 ao M6 e a cidade do cartaz): todas a desfazem primeiro.

Sem argumentos, o script confere que as trocas dão da base (a árvore com esta camada desfeita pelo manifesto, se o houver) o estado
da árvore, e escreve o JSON. Pode voltar a correr depois de a camada estar aplicada e dá o mesmo JSON.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/fila_final_20261115.json'
MANIFESTO = ROOT / 'tests/fixtures/fila-final-edits-20261115.json'

APP = 'assets/exame/app.js'
SESSOES = 'assets/exame/sessoes.json'
F05 = 'm3/licao-m3-f05/index.html'

ACHADO_APP = ('15/11/2026: fila final: o alvo de cada sessão do Exame é a meta da sessão (a ressalva de que não é limite do exame só vale nas sessões 20 e 23 e está nos seus prompts); a Informação-Prova '
              'de 2026 é a referência e a de 2027 ainda não está disponível.')
ACHADO_SESSOES = ('15/11/2026: fila final: a síntese de 80 a 100 palavras e a exposição de 200 a 350 palavras são metas de treino da '
                  'sessão, não regras nem itens do exame (nenhuma das provas de 2026 tem item de síntese; o item I.7 não tem limite '
                  'de palavras e pede uma só obra).')
ACHADO_F05 = ('15/11/2026: fila final: os versos de «Descalça vai para a fonte» contam-se de 5 em 5 sem contar os rótulos «Mote» e '
              '«Voltas» (3 versos de mote e 2 voltas de 7, 10 versos); os números 5 e 10 estavam duas linhas fora do sítio.')

TROCAS = [
    (APP, 'Alvo da sessão («Meta da sessão: ….»)',
     "minutos · '+e(session.writing.target)+'</p>",
     "minutos. Meta da sessão: '+e(session.writing.target)+'.</p>", ACHADO_APP),
    (APP, 'Alvo da sessão na versão para imprimir («Meta da sessão»)',
     "<p>'+e(s.writing.target)+'</p>",
     "<p>Meta da sessão: '+e(s.writing.target)+'.</p>", ACHADO_APP),
    (APP, 'Programa e fontes: a Informação-Prova de 2027 ainda não está disponível',
     'indicadas pela DGE.',
     'indicadas pela DGE. A Informação-Prova de 2027 ainda não está disponível.', ACHADO_APP),
    (SESSOES, 'Sessão 20, critério da síntese: meta de treino',
     'Respeitei as 80',
     'Cheguei à meta de treino de 80', ACHADO_SESSOES),
    (SESSOES, 'Sessão 20, prompt: a síntese é um treino',
     'Não acrescentes opiniões nem exemplos teus.',
     'Não acrescentes opiniões nem exemplos teus. Isto é um treino de síntese, não um item do exame.', ACHADO_SESSOES),
    (SESSOES, 'Sessão 23, prompt: a extensão é meta da sessão, não regra do exame',
     'Define um eixo, explica-o e apoia-o em exemplos pertinentes.',
     'Define um eixo, explica-o e apoia-o em exemplos pertinentes. A extensão é a meta desta sessão, não uma regra do exame: no exame, '
     'a breve exposição do item I.7 não tem limite de palavras e pede uma só obra.', ACHADO_SESSOES),
    (F05, 'M3-F05, «Descalça vai para a fonte»: o 5 sai do rótulo «Voltas»',
     'data-l=\\"0-5\\"><span class=\\"n\\">5</span>Voltas</span>',
     'data-l=\\"0-5\\"><span class=\\"n\\"></span>Voltas</span>', ACHADO_F05),
    (F05, 'M3-F05, «Descalça vai para a fonte»: o 5 está no quinto verso, «O testo nas mãos de prata»',
     'data-l=\\"0-7\\"><span class=\\"n\\"></span>O <b',
     'data-l=\\"0-7\\"><span class=\\"n\\">5</span>O <b', ACHADO_F05),
    (F05, 'M3-F05, «Descalça vai para a fonte»: o 10 sai do oitavo verso, «Traz a vasquinha de cote»',
     'data-l=\\"0-10\\"><span class=\\"n\\">10</span>Traz a',
     'data-l=\\"0-10\\"><span class=\\"n\\"></span>Traz a', ACHADO_F05),
    (F05, 'M3-F05, «Descalça vai para a fonte»: o 10 está no décimo e último verso, «Vai formosa, e não segura»',
     'data-l=\\"0-12\\"><span class=\\"n\\"></span>Vai formosa, e não segura.</span>',
     'data-l=\\"0-12\\"><span class=\\"n\\">10</span>Vai formosa, e não segura.</span>', ACHADO_F05),
]
# 15/11/2026: o resto da decisão do docente «síntese integrada» → «duas linhas finais» (a camada sintese_duas_linhas_20261115 fez o M1, o
# M3, o M5, o M6, o M7 e o M8; o M2 e as peças soltas ficaram por fazer). As frases seguem as dessa camada.
ACHADO_SINTESE = ('15/11/2026: Decisão do docente: «síntese integrada» e «síntese simples integrada» passam a «duas linhas finais», como no '
                  'M1; o mesmo vocabulário nas peças soltas (todos, lição M1-F11, planos das aulas de tarefa e portefólios do M4 e do M8). '
                  'Só a peça da aula de tarefa: as perguntas de escolha das lições, «síntese oral ou no caderno» e a chave «synthesis» ficam.')
M2I, M2P, M2M, M2G = ('m2/index.html', 'm2/portefolio-do-modulo-m2/index.html', 'm2/mapa-do-modulo-m2/index.html',
                      'm2/guia-da-tarefa-m2/index.html')
M4P, M8P = 'm4/portefolio-do-modulo-m4/index.html', 'm8/portefolio-do-modulo-m8/index.html'
_FECHO_V = 'O fecho e a síntese integram a aula de tarefa.'
_FECHO_N = 'O fecho e as duas linhas finais fazem parte da aula de tarefa.'
_POR_PERGUNTA = ('Síntese de duas linhas no papel da aula de tarefa, fotografada com o trabalho. Recupera essa entrega, sem fazer outra '
                 'síntese.</td></tr><tr><td data-th="Nome do ficheiro"><code>M2_U{n}_o-que-aprendi</code></td><td data-th="O que é">'
                 'Recupera a síntese ')
_POR_PERGUNTA_N = ('As duas linhas finais, no papel da aula de tarefa, fotografadas com o trabalho. Recupera essa entrega, sem escrever '
                   'outras.</td></tr><tr><td data-th="Nome do ficheiro"><code>M2_U{n}_o-que-aprendi</code></td><td data-th="O que é">'
                   'Recupera as duas linhas finais ')
TROCAS += [
    (M2I, 'Índice do M2: «produção em papel, duas linhas finais e fotografias no»',
     ' produção em papel, uma síntese simples integrada e fotografias no', ' produção em papel, duas linhas finais e fotografias no',
     ACHADO_SINTESE),
    (M2I, 'Índice do M2: «as duas linhas finais.»', ' a síntese integrada.</span></nav>', ' as duas linhas finais.</span></nav>',
     ACHADO_SINTESE),
    (M2I, 'Índice do M2: «Tarefa da Unidade 1: aula de 90 minutos com consulta, trabalho em papel, duas linhas finais»',
     'Duas escolhas, que liberdade?</span><span class="f">Aula de 90\u00a0minutos com consulta: aquecimento em cartões no início, '
     'trabalho em papel, síntese integrada e fotografias',
     'Duas escolhas, que liberdade?</span><span class="f">Aula de 90\u00a0minutos com consulta: aquecimento em cartões no início, '
     'trabalho em papel, duas linhas finais e fotografias', ACHADO_SINTESE),
    (M2I, 'Índice do M2: «Tarefa da Unidade 2: aula de 90 minutos com consulta, trabalho em papel, duas linhas finais»',
     'Dois anúncios de casamento</span><span class="f">Aula de 90\u00a0minutos com consulta: aquecimento em cartões no início, '
     'trabalho em papel, síntese integrada e fotografias',
     'Dois anúncios de casamento</span><span class="f">Aula de 90\u00a0minutos com consulta: aquecimento em cartões no início, '
     'trabalho em papel, duas linhas finais e fotografias', ACHADO_SINTESE),
    (M2P, 'Portefólio do módulo M2: «que integra as duas linhas finais;»', 'que integra a síntese; as retomas',
     'que integra as duas linhas finais; as retomas', ACHADO_SINTESE),
    (M2P, 'Portefólio do módulo M2: «as duas linhas finais já entregues»', 'trabalhos e as sínteses já entregues',
     'trabalhos e as duas linhas finais já entregues', ACHADO_SINTESE),
    (M2P, 'Portefólio do módulo M2: «As duas linhas finais, no papel da aula de tarefa» (U1)',
     'liberdade? ' + _POR_PERGUNTA.format(n=1), 'liberdade? ' + _POR_PERGUNTA_N.format(n=1), ACHADO_SINTESE),
    (M2P, 'Portefólio do módulo M2: «As duas linhas finais, no papel da aula de tarefa» (U2)',
     'representação? ' + _POR_PERGUNTA.format(n=2), 'representação? ' + _POR_PERGUNTA_N.format(n=2), ACHADO_SINTESE),
    (M2M, 'Mapa do módulo M2: «que integra as duas linhas finais;»', 'que integra a síntese; as retomas',
     'que integra as duas linhas finais; as retomas', ACHADO_SINTESE),
    (M2M, 'Mapa do módulo M2: «Aula de tarefa · 90 min · duas linhas finais» (unidade 1)',
     '#tarefa-unidade-1">Aula de tarefa · 90\u00a0min · síntese integrada<', '#tarefa-unidade-1">Aula de tarefa · 90\u00a0min · duas linhas finais<',
     ACHADO_SINTESE),
    (M2M, 'Mapa do módulo M2: «Aula de tarefa · 90 min · duas linhas finais» (unidade 2)',
     '#tarefa-unidade-2">Aula de tarefa · 90\u00a0min · síntese integrada<', '#tarefa-unidade-2">Aula de tarefa · 90\u00a0min · duas linhas finais<',
     ACHADO_SINTESE),
    (M2M, 'Mapa do módulo M2: «As duas linhas finais ficam no papel do trabalho»',
     ' A síntese tem duas linhas, no papel do trabalho: uma aprendizagem e uma escolha do trabalho que a mostra. Entrega-a ',
     ' As duas linhas finais ficam no papel do trabalho: uma aprendizagem e uma escolha do trabalho que a mostra. Entrega-as ',
     ACHADO_SINTESE),
    (M2G, 'Guia da tarefa do M2: «com duas linhas finais;»', 'de 90\u00a0minutos, com síntese integrada; as retomas',
     'de 90\u00a0minutos, com duas linhas finais; as retomas', ACHADO_SINTESE),
    (M2G, 'Guia da tarefa do M2: «escreves duas linhas finais»', 'fazes uma síntese simples no trabalho',
     'escreves duas linhas finais no trabalho', ACHADO_SINTESE),
]
for _rel in ('m1/todos/index.html', 'm7/todos/index.html'):
    TROCAS.append((_rel, f'Todos do M{_rel[1]}: «com consulta e duas linhas finais»', 'com consulta e síntese simples integrada.',
                   'com consulta e duas linhas finais.', ACHADO_SINTESE))
TROCAS += [
    ('m1/licao-m1-f11/index.html', 'M1-F11: «As duas linhas finais ficam na Tarefa da Unidade 2.»',
     'A síntese integra a Tarefa da Unidade 2.', 'As duas linhas finais ficam na Tarefa da Unidade 2.', ACHADO_SINTESE),
]
for _rel in ('m1/aulas/aula-06', 'm1/aulas/aula-14', 'm4/aulas/aula-08', 'm4/aulas/aula-15', 'm4/aulas/aula-18'):
    TROCAS.append((f'{_rel}/index.html', f'Plano da aula {_rel[-2:]} do M{_rel[1]}: «O fecho e as duas linhas finais fazem parte da aula de tarefa.»',
                   _FECHO_V, _FECHO_N, ACHADO_SINTESE))
TROCAS += [
    (M4P, 'Portefólio do módulo M4: «já fotografadas; não escreves outras»', 'já fotografada; não escreves outra.',
     'já fotografadas; não escreves outras.', ACHADO_SINTESE),
    (M8P, 'Portefólio do módulo M8: «sem outra escrita obrigatória» (U1)',
     'U1_<wbr>retoma</code></td><td>Retomas formativas da leitura, sem síntese adicional obrigatória',
     'U1_<wbr>retoma</code></td><td>Retomas formativas da leitura, sem outra escrita obrigatória', ACHADO_SINTESE),
    (M8P, 'Portefólio do módulo M8: «sem outra escrita obrigatória» (U2)',
     'U2_<wbr>retoma</code></td><td>Retomas formativas da leitura, sem síntese adicional obrigatória',
     'U2_<wbr>retoma</code></td><td>Retomas formativas da leitura, sem outra escrita obrigatória', ACHADO_SINTESE),
]
ACHADO_REVISAO = ('15/11/2026: fila final: revisão geral antes de publicar: «sozinho» marca o género de quem lê e sai do texto dirigido ao aluno; '
                  'a última «síntese» da lição M1-F11 passa a «duas linhas finais», como no resto da lição; no portefólio do M8, '
                  '«sem linhas a mais obrigatórias» lia-se mal e passa a «sem outra escrita obrigatória».')
TROCAS += [
    ('m1/aulas/aula-06/index.html', 'Plano da aula 06 do M1, «Para casa»: «refazer o exercício no telemóvel, sem ajuda», sem marca de género',
     'refazer o exercício sozinho, no telemóvel, ao teu ritmo', 'refazer o exercício no telemóvel, sem ajuda, ao teu ritmo', ACHADO_REVISAO),
    ('m4/aulas/aula-15/index.html', 'Plano da aula 15 do M4, «Para casa»: «refazer o exercício no telemóvel, sem ajuda», sem marca de género',
     'refazer o exercício sozinho, no telemóvel, ao teu ritmo', 'refazer o exercício no telemóvel, sem ajuda, ao teu ritmo', ACHADO_REVISAO),
    ('m1/licao-m1-f11/index.html', 'M1-F11, retorno de um cartão: «Serve às duas linhas finais da unidade 2»',
     'Serve à síntese da unidade 2, não a este plano.', 'Serve às duas linhas finais da unidade 2, não a este plano.', ACHADO_REVISAO),
]
FICHEIROS = [APP, SESSOES, F05]
for _t in TROCAS:
    if _t[0] not in FICHEIROS:
        FICHEIROS.append(_t[0])


def trocas():
    return [{'ficheiro': f, 'local': l, 'antigo': a, 'novo': n, 'ocorrencias': 1, 'achado': ach} for f, l, a, n, ach in TROCAS]


def base(rel):
    """O ficheiro sem esta camada (desfeita pelo manifesto, se o houver e a camada estiver aplicada)."""
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    if MANIFESTO.is_file():
        edits = json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])
        if edits and all(texto.count(e['new']) == e['occurrences'] for e in edits):
            for e in reversed(edits):
                texto = texto.replace(e['new'], e['old'])
    return texto


def main():
    todas = trocas()
    for rel in FICHEIROS:
        lista = [(i, t) for i, t in enumerate(todas, 1) if t['ficheiro'] == rel]
        try:
            processar(rel, lista, base(rel))
        except TrocaFalhou as erro:
            raise SystemExit(f'{rel}: as trocas não conferem: {erro}')
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {len(FICHEIROS)} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
