"""01/11/2026: discurso direto criado, já presente antes da troca de aspas.

Lista fechada: nenhuma citação literária entra aqui. As falas continuam a ser
conferidas palavra por palavra e só são aceites em casos declarados inventados.
"""
import re

FALAS = {
    ('m1-u2', 4): {'Abre a porta.'},
    ('m2-u2', 5): {'Pés sem botas, serra sem fim.'},
    ('m2-u2', 7): {'Sou pontual!', 'Trago o guião', 'inútil', 'Costumo faltar sem avisar.'},
    ('m2-u2', 10): {'Está queimado por baixo', 'Está queimado por baixo.'},
}


def fala_criada(slug, numero, cartao, fala):
    return (fala in FALAS.get((slug, numero), set())
            and bool(re.search(r'\binventad[oa]s?\b', cartao.get('p', ''), re.I)))
