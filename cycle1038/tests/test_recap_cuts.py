import sys,unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from recap_cuts import GENRES,SHOTS,START,END,SAFE_TOP,stage_for_frame,layout,validate
class RecapTest(unittest.TestCase):
 def setUp(self):self.stills=[Image.new('RGB',(1080,1920),'#234567') for _ in SHOTS]
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_3_source_stills(self):self.assertEqual(len(set(s[0] for s in SHOTS)),3)
 def test_timing(self):self.assertEqual([stage_for_frame(i) for i in (609,630,651,672,690)],[0,1,2,3,3])
 def test_protect_subtitle(self):self.assertEqual(layout(610,self.stills).size,(1080,SAFE_TOP))
 def test_ten_palettes(self):
  for genre in GENRES:
   with self.subTest(genre=genre):self.assertEqual(layout(675,self.stills,genre).size,(1080,1280))
 def test_reject_outside(self):
  for n in (608,691):
   with self.assertRaises(ValueError):stage_for_frame(n)
 def test_reject_unknown(self):
  with self.assertRaises(ValueError):layout(610,self.stills,'unknown')
 def test_fail_closed_source(self):
  with self.assertRaises(ValueError):validate('nonexistent.mp4','bad','beauty')
 def test_requires_three(self):
  with self.assertRaises(ValueError):layout(610,self.stills[:2])
if __name__=='__main__':unittest.main()
