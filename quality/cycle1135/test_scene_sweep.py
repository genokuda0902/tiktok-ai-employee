import unittest, tempfile, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_sweep import PALETTES,CUTS,make_sweep,overlay_expr
class SceneSweepTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(PALETTES),10)
  with tempfile.TemporaryDirectory() as d:
   for name,color in PALETTES.items():
    path=Path(d)/(name+'.png');im=make_sweep(path,color)
    self.assertTrue(path.is_file());self.assertEqual(im.size,(600,64))
    self.assertEqual(im.getpixel((0,0))[3],0)
    self.assertGreater(im.getpixel((300,32))[3],50)
 def test_cuts(self):
  self.assertEqual(CUTS,[2.8,5.6,8.4,11.2,14.,16.8,19.6])
 def test_overlay_windows(self):
  e=overlay_expr();self.assertEqual(e.count('between(t,'),7);self.assertIn('NAN',e)
if __name__=='__main__':unittest.main()
