#!/usr/bin/env python3
"""15/11/2026: a fila final do pedido: o exame diz que o alvo das sessões é meta da sessão e não limite do exame, a síntese e a
exposição ficam ditas como treino, a referência de 2026 diz que a de 2027 ainda não está disponível, e a lição M3-F05 conta os versos
do poema (de 5 em 5) sem contar os rótulos «Mote» e «Voltas». O «Item N da prova» não muda (ver abaixo).

Ficheiros (3):
- assets/exame/app.js: a linha de alvo da sessão («Meta da sessão: …. Não é um limite do exame.»), a versão para imprimir («Meta da
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

Nenhum destes três ficheiros sai de um gerador nem de dados que o reescrevam: assets/exame/sessoes.json e app.js são os ficheiros
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

ACHADO_APP = ('15/11/2026: fila final: o alvo de cada sessão do Exame é a meta da sessão e não um limite do exame; a Informação-Prova '
              'de 2026 é a referência e a de 2027 ainda não está disponível.')
ACHADO_SESSOES = ('15/11/2026: fila final: a síntese de 80 a 100 palavras e a exposição de 200 a 350 palavras são metas de treino da '
                  'sessão, não regras nem itens do exame (nenhuma das provas de 2026 tem item de síntese; o item I.7 não tem limite '
                  'de palavras e pede uma só obra).')
ACHADO_F05 = ('15/11/2026: fila final: os versos de «Descalça vai para a fonte» contam-se de 5 em 5 sem contar os rótulos «Mote» e '
              '«Voltas» (3 versos de mote e 2 voltas de 7, 10 versos); os números 5 e 10 estavam duas linhas fora do sítio.')

TROCAS = [
    (APP, 'Alvo da sessão («Meta da sessão», não limite do exame)',
     "minutos · '+e(session.writing.target)+'</p>",
     "minutos. Meta da sessão: '+e(session.writing.target)+'. Não é um limite do exame.</p>", ACHADO_APP),
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
FICHEIROS = [APP, SESSOES, F05]


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
