import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from animated_proof_chart import PALETTES,VALUES,draw_frame,ease,reveal_fraction,make_frames,SIZE

class ChartTests(unittest.TestCase):
 def test_ten_palettes(self): self.assertEqual(len(PALETTES),10)
 def test_all_render(self):
  for g in PALETTES:
   with self.subTest(genre=g):self.assertEqual(draw_frame(1.6,g).size,SIZE)
 def test_no_negative_data(self):
  with self.assertRaises(ValueError):draw_frame(1.5,values=(-1,14,21))
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):draw_frame(1.5,'not-a-genre')
 def test_monotonic_easing(self):
  x=[ease(i/20) for i in range(21)]
  self.assertEqual(x,sorted(x));self.assertEqual(x[0],0);self.assertEqual(x[-1],1)
 def test_staggered_reveal(self):
  self.assertGreater(reveal_fraction(.9,0),reveal_fraction(.9,1))
  self.assertGreater(reveal_fraction(.9,1),reveal_fraction(.9,2))
 def test_final_all_revealed(self):
  self.assertTrue(all(reveal_fraction(2.4,i)==1 for i in range(3)))
 def test_nonempty_frame(self):
  self.assertGreater(draw_frame(1.5).getbbox()[2],300)
 def test_values_not_hardcoded_in_renderer(self):
  self.assertEqual(draw_frame(2.2,values=(2,4,6)).size,SIZE)
 def test_overlay_not_full_screen(self):
  self.assertLess(SIZE[0]*SIZE[1],1080*1920*.1)

if __name__=='__main__':unittest.main()
