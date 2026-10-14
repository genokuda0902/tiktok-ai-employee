import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from build_cycle573 import draw_frame,CFG,smooth,W,H,N
class TestCycle573(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(CFG['genres']),10)
 def test_each_genre_renders(self):
  for g in CFG['genres']:
   with self.subTest(genre=g):self.assertEqual(draw_frame(1,g).size,(W,980))
 def test_three_stages_distinct(self):
  imgs=[draw_frame(n).tobytes() for n in (5,30,55)]
  self.assertEqual(len(set(imgs)),3)
 def test_bounds(self):
  for n in (-1,N):
   with self.assertRaises(ValueError):draw_frame(n)
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):draw_frame(1,'unknown')
 def test_easing(self):
  self.assertEqual(smooth(-2),0);self.assertEqual(smooth(2),1)
  self.assertAlmostEqual(smooth(.5),.5)
if __name__=='__main__':unittest.main(verbosity=2)
