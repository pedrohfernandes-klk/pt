from pathlib import Path
import unittest,re
ROOT=Path(__file__).resolve().parents[1]
class SharedEngine(unittest.TestCase):
 def test_all_108_lessons_use_one_versioned_engine(self):
  paths=list(ROOT.glob('m[1-9]/licao-*/index.html'));self.assertEqual(len(paths),108)
  for p in paths:
   s=p.read_text('utf-8')
   self.assertNotIn('window.EPIJogo=(function()',s,str(p))
   self.assertEqual(len(re.findall(r'<script[^>]+src=["\']../../assets/pt-lessons/jogo.js\?v=20261021-ux06["\']',s)),1,str(p))
 def test_all_nine_challenge_pages_use_the_same_engine(self):
  for p in ROOT.glob('m[1-9]/index.html'):
   s=p.read_text('utf-8');self.assertNotIn('window.EPIJogo=(function()',s,str(p))
   self.assertEqual(s.count('../assets/pt-lessons/jogo.js?v=20261021-ux06'),1,str(p))
if __name__=='__main__':unittest.main()
