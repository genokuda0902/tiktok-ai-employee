import unittest,importlib.util
from pathlib import Path
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('r818',ROOT/'render818_ci.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class TestCycle818(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(r.load_base().GENRE_ACCENTS),10)
 def test_eight_scenes(self):self.assertEqual(len(r.load_base().PHRASES),8)
 def test_cta(self):self.assertIn('fad(280,0)',(ROOT/'render818_ci.py').read_text())
 def test_no_posting(self):
  for p in ROOT.glob('*.py'):
   if p.name.startswith('test_'):continue
   for forbidden in ['requests.post(', 'tiktok.upload(']:
    self.assertNotIn(forbidden,p.read_text())
if __name__=='__main__':unittest.main()
