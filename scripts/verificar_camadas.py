#!/usr/bin/env python3
"""01/11/2026: verifica todas as camadas literais, da mais recente para a mais antiga."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
LAYERS=[
 ('licoes_m16_20261101','licoes-m16-edits-20261101'),
 ('licoes_m89_20261101','licoes-m89-edits-20261101'),
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
