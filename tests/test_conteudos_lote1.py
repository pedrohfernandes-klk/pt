"""01/11/2026: contratos do lote aprovado, incluindo o núcleo realmente apresentado."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards, validate_cards
from opcoes_equilibradas import medir
from aplicar_trocas import sha_lf

PATHS = {k: ROOT / f'{k[:2].lower()}/licao-{k.lower()}/index.html'
         for k in ('M1-F20','M4-F01','M4-F28','M6-F01','M7-F34','M8-F12','M9-F13')}
# Cartões de leitura com uma produção explícita. Cada lugar conta uma vez.
PRODUCOES = {'M1-F20': [1,4,7,10,12,16], 'M4-F01': [1,6,7,9,13,17,18],
             'M4-F28': [1,2,4,7,10,12,14,15], 'M6-F01': [],
             'M7-F34': [32], 'M8-F12': [11,22], 'M9-F13': [5,23]}


class Conteudos(unittest.TestCase):
    def test_ligacoes_chaves_lugares_e_reversibilidade(self):
        manifest = json.loads((ROOT/'tests/fixtures/conteudos-lote1-edits-20261101.json').read_text('utf-8'))
        for rel, item in manifest['files'].items():
            with self.subTest(path=rel):
                after = (ROOT/rel).read_text('utf-8')
                self.assertEqual(sha_lf(after), item['after_sha256_lf'])
                before = after
                for e in reversed(item['edits']):
                    self.assertEqual(before.count(e['new']), e['occurrences'])
                    before = before.replace(e['new'], e['old'])
                self.assertEqual(sha_lf(before), item['base_sha256_lf'])
                # A camada nunca introduz uma escrita em localStorage.
                self.assertEqual(re.findall(r'localStorage\.[a-zA-Z]+\([^;]+',after),
                                 re.findall(r'localStorage\.[a-zA-Z]+\([^;]+',before))
                self.assertEqual(re.findall(r'\b(?:var )?K\s*=\s*"[^"]+"',after),
                                 re.findall(r'\b(?:var )?K\s*=\s*"[^"]+"',before))

    def test_nucleo_variedade_e_producao(self):
        for k,p in PATHS.items():
            cards=lesson_cards(p)
            with self.subTest(lesson=k):
                self.assertEqual(validate_cards(cards),[])
                self.assertFalse(any(c.get('mais') for c in cards))
                auto=[c for c in cards if c['t']!='ler']
                self.assertGreaterEqual(len(auto)+len(PRODUCOES[k]),14)
                self.assertGreaterEqual(len({c['t'] for c in auto}),5)
                for n in PRODUCOES[k]:
                    self.assertEqual(cards[n-1]['t'],'ler')
                    self.assertTrue(cards[n-1].get('html'))
                for a,b,c in zip(cards,cards[1:],cards[2:]):
                    self.assertFalse(a['t']==b['t']==c['t'])
                source=p.read_text('utf-8')
                if k=='M4-F28':source=(ROOT/'m4/recursos/tpc-entrada.js').read_text('utf-8')
                if k=='M9-F13':source=(ROOT/'m9/recursos/f13.js').read_text('utf-8')
                config=source.split('EPIJogo.montar(',1)[1]
                self.assertIn('aula:true',config)
                self.assertIn('variar:false',config)

    def test_opcoes_reescritas_e_retorno_delimitado(self):
        edits=json.loads((ROOT/'scripts/conteudos_lote1_20261101.json').read_text('utf-8'))
        for e in edits:
            try:c=json.loads(e['novo'])
            except ValueError:continue
            if not isinstance(c,dict) or 't' not in c:continue
            groups=[c] if c['t']=='escolha' else c.get('lacunas',[])
            for g in groups:
                with self.subTest(card=e['local']):
                    result=medir(g['o'],g['c'])
                    self.assertFalse(result['amplitude_acima'])
                    self.assertFalse(result['certa_25_porcento'])
            if c['t']!='ler':
                self.assertTrue(c.get('f'))
                if c['t']=='escolha':
                    self.assertEqual(len(c['fe']),len(c['o']))
                    self.assertTrue(all(v for i,v in enumerate(c['fe']) if i!=c['c']))

    def test_piloto_mantem_duas_producoes_e_arco(self):
        cards=lesson_cards(PATHS['M9-F13'])
        self.assertEqual(len(cards),23)
        self.assertIn('liberdade completa',cards[1]['html'])
        self.assertIn('contraexemplo',cards[22]['html'])
        self.assertEqual(cards[20]['t'],'escolha')
        self.assertEqual(len(cards[20]['o']),3)
        self.assertEqual([cards[i-1]['t'] for i in (5,23)],['ler','ler'])
        m7=lesson_cards(PATHS['M7-F34'])
        self.assertTrue(all(not m7[n-1].get('mais') for n in (9,31,32)))

    def test_medicao_publica_sem_solucao_nem_armazenamento(self):
        h=(ROOT/'m9/painel-m9-f13/index.html').read_text('utf-8')
        self.assertEqual(h.count('<strong>Caso criado.</strong>'),3)
        for text in ('Antes:','Depois:','Uma semana depois:','Hipótese','Apoio','Limite','Revisão','Totais da turma'):
            self.assertIn(text,h)
        self.assertNotIn('localStorage',h)
        self.assertNotIn('Resposta esperada',h)


if __name__=='__main__':unittest.main()
