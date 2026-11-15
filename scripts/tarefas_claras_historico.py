"""Reconstitui o texto anterior à revisão dos enunciados para os contratos históricos."""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
FILES = json.loads((ROOT / 'tests/fixtures/tarefas-claras-edits-20261110.json').read_text('utf-8'))['files']
# 11/11/2026: a decisão 152 no M6 (cuidado_m6_20261108) fica por cima desta revisão e repõe, nos enunciados novos, os espaços que
# não quebram que a revisão tinha tirado às tarefas do M1, do M3, do M4 e do M5. Quando o texto recebido é a página como essa
# camada a deixou (o hash «after» do seu manifesto), desfaz-se primeiro essa camada, com contagem estrita; quem já a desfez
# (tests/auditoria_20261028.py) entrega outro texto e nada se desfaz duas vezes.
CUIDADO_M6 = json.loads((ROOT / 'tests/fixtures/cuidado-m6-edits-20261108.json').read_text('utf-8'))['files']
# 12/11/2026: a decisão 152 no M7 (cuidado_m7_20261111) fica por cima das duas e muda as tarefas da M7-U1, da M7-U2 e da M7-U3
# (as páginas e os dados da M7-U3), que a revisão dos enunciados também mudou. Pela mesma regra: quando o texto recebido é a
# página como a camada do M7 a deixou (o hash «after» do seu manifesto), desfaz-se primeiro essa camada, com contagem estrita, e
# só depois a do M6 e a dos enunciados; quem já a desfez entrega outro texto e nada se desfaz duas vezes.
CUIDADO_M7 = json.loads((ROOT / 'tests/fixtures/cuidado-m7-edits-20261111.json').read_text('utf-8'))['files']
# 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112) fica por cima das três e muda as tarefas da M8-U1 e da M8-U2 (as páginas
# e os dados), que a revisão dos enunciados também mudou. Pela mesma regra: quando o texto recebido é a página como a camada do
# M8 a deixou (o hash «after» do seu manifesto), desfaz-se primeiro essa camada, com contagem estrita, e só depois as do M7 e do
# M6 e a dos enunciados; quem já a desfez entrega outro texto e nada se desfaz duas vezes.
CUIDADO_M8 = json.loads((ROOT / 'tests/fixtures/cuidado-m8-edits-20261112.json').read_text('utf-8'))['files']
# 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112) fica por cima das quatro e muda as tarefas da M9-U1 e da M9-U2 (as páginas
# e os dados), que a revisão dos enunciados também mudou. Pela mesma regra: quando o texto recebido é a página como a camada do
# M9 a deixou (o hash «after» do seu manifesto), desfaz-se primeiro essa camada, com contagem estrita, e só depois as do M8, do
# M7 e do M6 e a dos enunciados; quem já a desfez entrega outro texto e nada se desfaz duas vezes.
CUIDADO_M9 = json.loads((ROOT / 'tests/fixtures/cuidado-m9-edits-20261112.json').read_text('utf-8'))['files']
# 12/11/2026: as duas tarefas do M3 «mais fáceis de fazer» (tarefas_faceis_m3_20261112) ficam por cima de todas e mudam os
# enunciados e os dados da M3-U1 e da M3-U2, que a revisão dos enunciados e a decisão 152 no M6 também mudaram. Pela mesma regra:
# quando o texto recebido é a página como essa camada a deixou (o hash «after» do seu manifesto), desfaz-se primeiro essa camada,
# com contagem estrita, e só depois as outras; quem já a desfez entrega outro texto e nada se desfaz duas vezes.
TAREFAS_FACEIS_M3 = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json').read_text('utf-8'))['files']
# 13/11/2026: as duas tarefas do M1 «mais fáceis de fazer» (tarefas_faceis_m1_20261113) ficam por cima de todas, também das do M3, e
# mudam os enunciados e os dados da M1-U1 e da M1-U2 e os dados das grelhas (que a camada do M3 também muda). Pela mesma regra:
# quando o texto recebido é o ficheiro como essa camada o deixou (o hash «after» do seu manifesto), desfaz-se primeiro, com contagem
# estrita, e só depois a do M3 e as outras.
TAREFAS_FACEIS_M1 = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json').read_text('utf-8'))['files']
# 13/11/2026: as duas tarefas do M5 «mais fáceis de fazer» (tarefas_faceis_m5_20261113) ficam por cima de todas, também das do M1 e
# das do M3, e mudam os enunciados e os dados da M5-U1 e da M5-U2, os dados das grelhas (que as camadas do M1 e do M3 também mudam) e
# os dados e o enunciado da M3-U2 (que a camada do M3 também muda). Pela mesma regra: quando o texto recebido é o ficheiro como essa
# camada o deixou (o hash «after» do seu manifesto), desfaz-se primeiro, com contagem estrita, e só depois as do M1, do M3 e as outras.
TAREFAS_FACEIS_M5 = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json').read_text('utf-8'))['files']
# 13/11/2026: as duas tarefas do M6 «mais fáceis de fazer» (tarefas_faceis_m6_20261113) ficam por cima de todas, também das do M5, e
# mudam os enunciados e os dados da M6-U1 e da M6-U2 e os dados das grelhas (que as camadas do M5, do M1 e do M3 também mudam). Pela
# mesma regra: quando o texto recebido é o ficheiro como essa camada o deixou (o hash «after» do seu manifesto), desfaz-se primeiro,
# com contagem estrita, e só depois as do M5, do M1, do M3 e as outras.
TAREFAS_FACEIS_M6 = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json').read_text('utf-8'))['files']
# 13/11/2026: as três tarefas do M7 «mais fáceis de fazer» (tarefas_faceis_m7_20261113) ficam por cima de todas, também das do M6, e
# mudam os enunciados da M7-U1, da M7-U2 e da M7-U3, os dados da M7-U3 e os dados das grelhas (que as camadas do M6, do M5, do M1 e do
# M3 também mudam). Pela mesma regra: desfaz-se primeiro, com contagem estrita, quando o texto é o ficheiro como ela o deixou.
TAREFAS_FACEIS_M7 = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json').read_text('utf-8'))['files']
# 13/11/2026: as duas tarefas do M8 «mais fáceis de fazer» (tarefas_faceis_m8_20261113) ficam por cima de todas, também das do M7, e
# mudam os enunciados e os dados da M8-U1 e da M8-U2 e os dados das grelhas (que as camadas do M7, do M6, do M5, do M1 e do M3 também
# mudam). Pela mesma regra: desfaz-se primeiro, com contagem estrita, quando o texto é o ficheiro como ela o deixou.
TAREFAS_FACEIS_M8 = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m8-edits-20261113.json').read_text('utf-8'))['files']
# 14/11/2026: as duas tarefas do M9 «mais fáceis de fazer» (tarefas_faceis_m9_20261114) ficam por cima de todas, também das do M8, e
# mudam os enunciados e os dados da M9-U1 e da M9-U2 e os dados das grelhas (que as camadas do M8, do M7, do M6, do M5, do M1 e do M3
# também mudam). Pela mesma regra: desfaz-se primeiro, com contagem estrita, quando o texto é o ficheiro como ela o deixou.
TAREFAS_FACEIS_M9 = json.loads((ROOT / 'tests/fixtures/tarefas-faceis-m9-edits-20261114.json').read_text('utf-8'))['files']
# 15/11/2026: a tarefa m4-u2 com «Tema A ou B», «tudo junto» no M4 e o acerto do M8 (tarefa_m4u2_tema_b_20261115) fica por cima de
# todas, também da do M9, e muda os dados das grelhas (que as camadas do M9, do M8, do M7, do M6, do M5, do M1 e do M3 também mudam).
# Pela mesma regra: desfaz-se primeiro, com contagem estrita, quando o texto é o ficheiro como ela o deixou.
TAREFA_M4U2 = json.loads((ROOT / 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json').read_text('utf-8'))['files']
# 15/11/2026: a fila final (fila_final_20261115: assets/exame/app.js, assets/exame/sessoes.json e a lição M3-F05) fica por cima de todas,
# também das duas linhas finais. Pela mesma regra: desfaz-se primeiro, com contagem estrita, quando o texto é o ficheiro como ela o deixou.
FILA_FINAL = json.loads((ROOT / 'tests/fixtures/fila-final-edits-20261115.json').read_text('utf-8'))['files']
# 15/11/2026: a revisão geral antes de publicar (revisao_geral_20261115: o Atlas, a M9-F11 e a M9-F12, as provas em cartões, as lições
# M8-F13, M8-F14, M5-F14 e M5-F15, a tarefa M5-U2 e assets/exame/sessoes.json) fica por cima de todas, também da fila final. Pela mesma
# regra: desfaz-se primeiro, com contagem estrita, quando o texto é o ficheiro como ela o deixou.
REVISAO_GERAL = json.loads((ROOT / 'tests/fixtures/revisao-geral-edits-20261115.json').read_text('utf-8'))['files']
# 15/11/2026: «duas linhas finais» em vez de «síntese integrada» nos índices, nos portefólios, nos mapas e no guia da tarefa do M1, do
# M3, do M5, do M6, do M7 e do M8 (sintese_duas_linhas_20261115) fica por cima de todas, também da tarefa m4-u2. Pela mesma regra:
# desfaz-se primeiro, com contagem estrita, quando o texto é o ficheiro como ela o deixou.
SINTESE_DUAS_LINHAS = json.loads((ROOT / 'tests/fixtures/sintese-duas-linhas-edits-20261115.json').read_text('utf-8'))['files']
def _sha_lf(text):
    return hashlib.sha256(text.replace('\r\n', '\n').encode()).hexdigest()
def desfazer_faceis(path, text):
    """12/11/2026: desfaz só a camada das tarefas do M3 mais fáceis de fazer, em qualquer dos seus 16 ficheiros (também o guia, o
    índice e o mapa do M3, as grelhas, as correções e os aquecimentos, que a revisão dos enunciados não mudou), quando o texto é a
    página como ela a deixou."""
    p = Path(path)
    rel = p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()
    # 15/11/2026: antes de tudo, a revisão geral, por cima de todas, também da fila final (nos seus 24 ficheiros).
    por_cima = REVISAO_GERAL.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'A revisão geral não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 15/11/2026: antes de tudo, a fila final, por cima de todas (nos seus 3 ficheiros).
    por_cima = FILA_FINAL.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'A fila final não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 15/11/2026: antes de tudo, as duas linhas finais em vez da síntese integrada, por cima de todas (em qualquer dos seus 18 ficheiros).
    por_cima = SINTESE_DUAS_LINHAS.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Duas linhas finais em vez de síntese integrada não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 15/11/2026: primeiro a camada da tarefa m4-u2, que está por cima de todas, também da do M9 (em qualquer dos seus 12 ficheiros).
    por_cima = TAREFA_M4U2.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefa m4-u2 com «Tema A ou B» não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 14/11/2026: primeiro a camada do M9, que está por cima de todas, também da do M8 (em qualquer dos seus 15 ficheiros).
    por_cima = TAREFAS_FACEIS_M9.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M9 mais fáceis de fazer não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 13/11/2026: primeiro a camada do M8, que está por cima de todas, também da do M7 (em qualquer dos seus 13 ficheiros).
    por_cima = TAREFAS_FACEIS_M8.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M8 mais fáceis de fazer não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 13/11/2026: primeiro a camada do M7, que está por cima de todas (em qualquer dos seus 13 ficheiros).
    por_cima = TAREFAS_FACEIS_M7.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M7 mais fáceis de fazer não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 13/11/2026: depois a camada do M6, que está por cima das do M5, do M1 e do M3 (em qualquer dos seus 17 ficheiros).
    por_cima = TAREFAS_FACEIS_M6.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M6 mais fáceis de fazer não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 13/11/2026: depois a camada do M5, que está por cima das do M1 e do M3 (em qualquer dos seus 20 ficheiros).
    por_cima = TAREFAS_FACEIS_M5.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M5 mais fáceis de fazer não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    # 13/11/2026: depois a camada do M1, que está por cima da do M3 (em qualquer dos seus 12 ficheiros).
    no_topo = TAREFAS_FACEIS_M1.get(rel)
    if no_topo and _sha_lf(text) == no_topo['after_sha256_lf']:
        for edit in reversed(no_topo['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M1 mais fáceis de fazer não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    no_cimo = TAREFAS_FACEIS_M3.get(rel)
    if no_cimo and _sha_lf(text) == no_cimo['after_sha256_lf']:
        for edit in reversed(no_cimo['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M3 mais fáceis de fazer não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    return text
def desfazer(path, text):
    p = Path(path)
    rel = p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()
    # 12/11/2026: antes de tudo, a camada do topo (as tarefas do M3 mais fáceis de fazer), também nos ficheiros que a revisão dos
    # enunciados não mudou.
    text = desfazer_faceis(rel, text)
    entry = FILES.get(rel)
    if not entry:
        return text
    mais_recente = CUIDADO_M9.get(rel)
    if mais_recente and _sha_lf(text) == mais_recente['after_sha256_lf']:
        for edit in reversed(mais_recente['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Decisão 152 no M9 não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    primeiro = CUIDADO_M8.get(rel)
    if primeiro and _sha_lf(text) == primeiro['after_sha256_lf']:
        for edit in reversed(primeiro['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Decisão 152 no M8 não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    no_topo = CUIDADO_M7.get(rel)
    if no_topo and _sha_lf(text) == no_topo['after_sha256_lf']:
        for edit in reversed(no_topo['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Decisão 152 no M7 não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    por_cima = CUIDADO_M6.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Decisão 152 no M6 não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    if _sha_lf(text) == entry['base_sha256_lf']:
        return text
    for edit in reversed(entry['edits']):
        assert text.count(edit['new']) == edit['occurrences'], f'Enunciado revisto não confere: {rel}'
        text = text.replace(edit['new'], edit['old'])
    return text
