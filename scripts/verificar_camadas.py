# 03/11/2026: cabeçalho sobre F0 publicada, mantendo reversão e asserções.
#!/usr/bin/env python3
"""01/11/2026: verifica todas as camadas literais, da mais recente para a mais antiga."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
LAYERS=[
 # 13/11/2026: as três tarefas do M7 «mais fáceis de fazer» e «tudo junto» no M7 (os enunciados da m7-u1, da m7-u2 e da m7-u3, a
 # grelha, a correção e os aquecimentos, os seus dados, e o guia e o portefólio do M7), camada mais recente, por cima das tarefas do
 # M6 mais fáceis de fazer (que passa a ser a segunda), com a qual partilha os dados das grelhas.
 ('tarefas_faceis_m7_20261113','tarefas-faceis-m7-edits-20261113'),
 # 13/11/2026: as duas tarefas do M6 «mais fáceis de fazer» e «tudo junto» no M6 (os enunciados, as grelhas, as correções e os
 # aquecimentos da m6-u1 e da m6-u2, os seus dados, e o guia, o índice, o mapa e o portefólio do M6), camada mais recente, por cima
 # das tarefas do M5 mais fáceis de fazer (que passa a ser a segunda), com a qual partilha os dados das grelhas.
 ('tarefas_faceis_m6_20261113','tarefas-faceis-m6-edits-20261113'),
 # 13/11/2026: as duas tarefas do M5 «mais fáceis de fazer» e «tudo junto» no M5 (os enunciados, as grelhas, as correções e os
 # aquecimentos da m5-u1 e da m5-u2, os seus dados, e o guia, o índice, o mapa e o portefólio do M5), com dois acertos do M3 (o
 # portefólio do M3 e o tema B da m3-u2), camada mais recente, por cima das tarefas do M1 mais fáceis de fazer (que passa a ser a
 # segunda), com a qual partilha os dados das grelhas.
 ('tarefas_faceis_m5_20261113','tarefas-faceis-m5-edits-20261113'),
 # 13/11/2026: as duas tarefas do M1 «mais fáceis de fazer» e «tudo junto» no M1 (os enunciados, as grelhas e as correções da m1-u1
 # e da m1-u2, os seus dados, e o guia, o índice e o portefólio do M1), camada mais recente, por cima das tarefas do M3 mais fáceis de fazer (que
 # passa a ser a segunda), com a qual partilha os dados das grelhas.
 ('tarefas_faceis_m1_20261113','tarefas-faceis-m1-edits-20261113'),
 # 12/11/2026: as duas tarefas do M3 «mais fáceis de fazer» e «tudo junto» no M3 (os enunciados, as grelhas, as correções e os
 # aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3), camada mais recente, por cima das provas em
 # cartões com os documentos oficiais (que passa a ser a segunda), com a qual não partilha nenhum ficheiro.
 ('tarefas_faceis_m3_20261112','tarefas-faceis-m3-edits-20261112'),
 # 12/11/2026: as provas em cartões com os documentos oficiais (a secção exame/provas/, as seis lições das provas de 2026 e os seus
 # dados: ligações para eduqa.pt, autoria, frases só com o que as duas provas mostram e referências que não se partem), camada mais
 # recente, por cima da ligação «Treinos» na página principal do Exame (que passa a ser a segunda) e da decisão 152 no Exame.
 ('exame_provas_oficial_20261112','exame-provas-oficial-edits-20261112'),
 # 12/11/2026: a ligação «Treinos» na navegação da página principal do Exame (exame/index.html), camada mais recente, por cima da
 # decisão 152 no Exame e nas páginas transversais (que passa a ser a segunda).
 ('exame_ligacao_treinos_20261112','exame-ligacao-treinos-edits-20261112'),
 # 12/11/2026: decisão 152 (cuidado em todas as lições), Exame e páginas transversais (as sessões, o laboratório, as provas em
 # cartões e os aquecimentos do Exame, as obras, as páginas dos anos, o mapa e a entrada): uma tabela onde havia itens paralelos e
 # referências e números que não se partem, camada mais recente, por cima da decisão 152 no M9.
 ('cuidado_exame_20261112','cuidado-exame-edits-20261112'),
 # 12/11/2026: decisão 152 (cuidado em todas as lições), módulo M9: tabelas onde há itens paralelos e referências e números que
 # não se partem, por cima da decisão 152 no M8 (a mais recente passou a ser a do Exame e das páginas transversais, acima).
 ('cuidado_m9_20261112','cuidado-m9-edits-20261112'),
 # 12/11/2026: decisão 152 (cuidado em todas as lições), módulo M8: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima da decisão 152 no M7.
 ('cuidado_m8_20261112','cuidado-m8-edits-20261112'),
 # 11/11/2026: decisão 152 (cuidado em todas as lições), módulo M7: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima da decisão 152 no M6.
 ('cuidado_m7_20261111','cuidado-m7-edits-20261111'),
 # 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M6: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima da decisão 152 no M5.
 ('cuidado_m6_20261108','cuidado-m6-edits-20261108'),
 # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): a revisão dos enunciados das tarefas (#192) fica logo abaixo da decisão 152
 # no M6, que foi refeita sobre ela e continua a camada mais recente.
 ('tarefas_claras_20261110','tarefas-claras-edits-20261110'),
 # 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M5: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima da decisão 152 no M4.
 ('cuidado_m5_20261108','cuidado-m5-edits-20261108'),
 # 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M4: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima da decisão 152 no M3.
 ('cuidado_m4_20261108','cuidado-m4-edits-20261108'),
 # 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M3: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima da decisão 152 no M2.
 ('cuidado_m3_20261108','cuidado-m3-edits-20261108'),
 # 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M2: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção.
 ('cuidado_m2_20261108','cuidado-m2-edits-20261108'),
 # 08/11/2026: cartaz «Ler a cidade» na entrada do Português e nome novo da secção nas páginas publicadas (pedido do
 # utilizador: «quero que [Ler a cidade] tenha um banner em português»), camada mais recente, por cima dos créditos atrás de um
 # «i» do pedido pt-1.
 ('cidade_cartaz_20261108','cidade-cartaz-edits-20261108'),
 # 07/11/2026: decisões 153, 176 e 177, créditos atrás de um «i» na entrada, nos nove índices e no Atlas (pedido pt-1), camada
 # mais recente, por cima da decisão 152 no M1.
 ('creditos_i_pt1_20261107','creditos-i-pt1-edits-20261107'),
 # 06/11/2026: decisão 152 (cuidado em todas as lições), módulo M1: tabelas onde há itens paralelos e referências e números que
 # não se partem, camada mais recente, por cima dos créditos atrás de um «i». 07/11/2026 (fusão do main 29441e6b): por cima dos acertos da decisão 173.
 ('cuidado_m1_20261106','cuidado-m1-edits-20261106'),
 # 07/11/2026: três acertos dos índices deixados pela decisão 173 (acesso do docente repetido no M3, M5 e M6; «·» no M8 e M9; menu dos materiais sem JavaScript), camada mais recente, por cima do desenho comum dos índices.
 ('indices_acertos_20261107','indices-acertos-edits-20261107'),
 # 06/11/2026: decisão 148, o desenho do índice do M4 nos nove índices do Português, camada mais recente, por cima dos créditos atrás de um «i» (07/11/2026: por baixo dos acertos da decisão 173).
 ('cartaz_indices_148_20261106','cartaz-indices-148-edits-20261106'),
 # 05/11/2026: decisão 153, créditos das imagens atrás de um «i» (pedido pt-2), por cima do lote 3 do Atlas e da decisão 154 (06/11/2026: depois de juntar o main; 06/11/2026: por baixo do desenho comum dos índices, decisão 148).
 ('creditos_i_20261105','creditos-i-edits-20261105'),
 # 05/11/2026: Atlas Lusófono, lote 3 (66 figuras, «Imprensa e pensamento», localização aproximada, fotografias e vídeos), por cima da decisão 154 (06/11/2026: correções da revisão do lote 3 na mesma camada, e a camada passa por cima da decisão 154 depois de juntar o main).
 ('atlas_lote3_20261105','atlas-lote3-edits-20261105'),
 # 05/11/2026: decisão 154 (os exercícios fazem-se sozinho): nada no texto do aluno depende do docente nem só de um colega ou da turma, por cima do contexto do Laboratório do exame.
 ('autonomia_154_20261105','autonomia-154-edits-20261105'),
 # 05/11/2026: Laboratório do exame: o texto de contexto de cada sessão fala da lição e do excerto, por cima da ligação e das notas.
 ('exame_contexto_20261105','exame-contexto-edits-20261105'),
 # 05/11/2026: Laboratório do exame: a ligação e as notas falam da lição, por cima da tabela.
 ('exame_licao_20261105','exame-licao-edits-20261105'),
 # 05/11/2026: tabela dos seis movimentos (M7-F10) e intervalos de versos, por cima da revisão.
 ('tabela_movimentos_20261105','tabela-movimentos-edits-20261105'),
 # 05/11/2026: revisão de 5/11, por cima do cabeçalho.
 ('revisao_20261105','revisao-edits-20261105'),
 # 02/11/2026: créditos de IA depois do lote 2 publicado.
 # 03/11/2026: abertura visual acima dos creditos publicados.
 ('cartaz_cabecalho_20261103','cartaz-cabecalho-edits-20261103'),
 # 03/11/2026: piloto M4 acima de F0 publicado, ambos reversíveis.
 ('cartaz_m4_piloto_20261102','cartaz-m4-piloto-edits-20261102'),
 # 03/11/2026: F0 acima dos créditos publicados, antes do lote 2.
 ('variedade_f0_20261102','variedade-f0-edits-20261102'),
 ('creditos_grafismos_ia_20261102','creditos-grafismos-ia-edits-20261102'),
 # 02/11/2026: lote 2 reaplicado por cima do main publicado.
 ('conteudos_lote2_20261101','conteudos-lote2-edits-20261101'),
 # 02/11/2026: decisão 139, a calçada «mar largo» na entrada (camada mais recente).
 # 02/11/2026: varredura de formatação (pt #152), refeita em trocas mínimas sobre o main (camada mais recente).
 ('varredura_formatacao_20261101','varredura-formatacao-edits-20261101'),
 # 02/11/2026: decisão 139, a calçada «mar largo» na entrada.
 ('calcada_mar_20261102','calcada-mar-edits-20261102'),
 # 02/11/2026: pedido do docente, não há tarefas de grupo.
 ('tarefas_individuais_20261102','tarefas-individuais-edits-20261102'),
 ('cartaz_indices_20261101','cartaz-indices-edits-20261101'),
 ('licoes_m16_20261101','licoes-m16-edits-20261101'),
 ('licoes_m89_20261101','licoes-m89-edits-20261101'),
 # 02/11/2026: o fundo da entrada (pt #159 e #160), que entrou no main sem camada.
 ('fundos_20261102','fundos-edits-20261102'),
 ('tarefas_m89_20261101','tarefas-m89-edits-20261101'),
 ('tarefas_m356_20261031','tarefas-m356-edits-20261031'),
 ('lingua_pessoa_m7_20261030','lingua-pessoa-m7-edits-20261030'),
 ('opcoes_denunciadoras_20261030','opcoes-denunciadoras-edits-20261030'),
 ('texto_justificado_20261030','texto-justificado-edits-20261030'),
 ('aquecimentos_m2_20261030','aquecimentos-m2-edits-20261030'),
 ('aquecimentos_m4_20261030','aquecimentos-m4-edits-20261030'),
 ('aquecimentos_m1_20261030','aquecimentos-m1-edits-20261030'),
 ('aquecimentos_m7_20261029','aquecimentos-m7-edits-20261029'),
 ('auditoria_m4_m7_20261028','auditoria-m4-m7-edits-20261028'),
]


def main():
    failures=[]
    for i,(layer,manifest) in enumerate(LAYERS):
        command=[sys.executable,'scripts/aplicar_trocas.py','scripts/'+layer+'.json',
                 '--manifesto','tests/fixtures/'+manifest+'.json','--verificar']
        for _,newer in LAYERS[:i]:
            command+=['--desfazer-antes','tests/fixtures/'+newer+'.json']
        if layer=='auditoria_m4_m7_20261028':
            # Contrato histórico: M7-U3 foi regenerada; o predecessor e o sucessor
            # continuam integralmente verificados pelos testes task_source_contract.
            command+=['--fora','tarefas/m7-u3/index.html']
        result=subprocess.run(command,cwd=ROOT)
        print(layer, 'PASS' if result.returncode==0 else 'FAIL', flush=True)
        if result.returncode:failures.append(layer)
    print(f'{len(LAYERS)-len(failures)}/{len(LAYERS)} camadas conferidas',flush=True)
    return bool(failures)


if __name__=='__main__':sys.exit(main())
