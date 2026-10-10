import unittest, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import render_ci as r
class Cycle455Tests(unittest.TestCase):
 def test_duration(self):self.assertAlmostEqual(sum(r.DUR),20.0,places=4)
 def test_caption_alignment(self):self.assertEqual(len(r.CAP),len(r.DUR))
 def test_japanese_voice_script(self):
  self.assertEqual(len(r.LINES),8)
  self.assertTrue(all(any('ぁ'<=c<='ん' or '一'<=c<='龥' for c in s) for s in r.LINES))
 def test_formula_math(self):
  self.assertEqual(sum(r.VALUES),17)
  self.assertEqual(sum([3,4,4,1,5,2]),19)
 def test_ten_genres(self):self.assertEqual(len(set(r.GENRES)),10)
 def test_scene_draw(self):
  p=ROOT/'test_scene.png';r.draw_slide(2,p)
  from PIL import Image
  with Image.open(p) as im:self.assertEqual(im.size,(1080,1920))
  p.unlink()
if __name__=='__main__':unittest.main()
