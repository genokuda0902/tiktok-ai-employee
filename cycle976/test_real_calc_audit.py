import sys,unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from real_calc_audit import GENRES,SCENE_FRAMES,SAFE_BOTTOM,check_genre,make_frame
class TestRealCalcAudit(unittest.TestCase):
 def setUp(self):self.proof=Image.new('RGB',(1158,1638),'white')
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_unknown_rejected(self):
  with self.assertRaises(ValueError):check_genre('unknown',True)
 def test_unreviewed_real_rejected(self):
  for g in GENRES[1:]:
   with self.subTest(g=g):
    with self.assertRaises(ValueError):check_genre(g,False)
 def test_synthetic_accepted(self):
  for g in GENRES:check_genre(g,True)
 def test_frame_count(self):self.assertEqual(SCENE_FRAMES,87)
 def test_safe_height(self):
  for f in [0,22,23,58,59,86]:
   im=make_frame(self.proof,f)
   self.assertEqual(im.size,(1080,SAFE_BOTTOM))
 def test_three_distinct_stages(self):
  ims=[make_frame(self.proof,i).tobytes() for i in [12,40,73]]
  self.assertEqual(len(set(ims)),3)
 def test_reject_frame_outside_scene(self):
  with self.assertRaises(ValueError):make_frame(self.proof,87)
 def test_arithmetic(self):
  self.assertEqual(sum([12,16,18]),46);self.assertEqual(sum([8,9,12]),29)
if __name__=='__main__':unittest.main()
