#!/usr/bin/env python3
"""01/11/2026: verifica todas as camadas literais, da mais recente para a mais antiga."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
LAYERS=[
 # 02/11/2026: piloto visual do M4, reversível sobre o main publicado.
 ('cartaz_m4_piloto_20261102','cartaz-m4-piloto-edits-20261102'),
 # 02/11/2026: créditos de IA depois do lote 2 publicado.
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
