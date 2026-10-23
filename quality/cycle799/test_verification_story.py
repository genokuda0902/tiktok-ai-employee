import copy,json,sys,unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from verification_story import W,H,FPS,FRAMES,START_FRAME,END_FRAME,validate,make_frame,safe_boxes,ease
C=json.loads((Path(__file__).parent/'config.json').read_text())
class Tests(unittest.TestCase):
 def test_10_unique_genres(self):self.assertEqual(len(set(C['genres'])),10)
 def test_valid_sum(self):self.assertTrue(validate(C));self.assertEqual(sum(C['values']),650000)
 def test_wrong_sum_rejected(self):
  c=copy.deepcopy(C);c['total']=1
  with self.assertRaises(ValueError):validate(c)
 def test_negative_value_rejected(self):
  c=copy.deepcopy(C);c['values'][0]=-1
  with self.assertRaises(ValueError):validate(c)
 def test_float_value_rejected(self):
  c=copy.deepcopy(C);c['values'][0]=120000.0
  with self.assertRaises(ValueError):validate(c)
 def test_rights_fail_closed(self):
  for k in ('rights_reviewed','employee_approved','publication_approved'):
   c=copy.deepcopy(C);c[k]=True
   with self.assertRaises(ValueError):validate(c)
 def test_publish_mode_rejected(self):
  c=copy.deepcopy(C);c['mode']='publish'
  with self.assertRaises(ValueError):validate(c)
 def test_formula_must_match_rows(self):
  c=copy.deepcopy(C);c['formula']='=SUM(B2:B4)'
  with self.assertRaises(ValueError):validate(c)
 def test_geometry_safe(self):
  for rect in safe_boxes().values():
   x0,y0,x1,y1=rect
   self.assertGreaterEqual(x0,80);self.assertLessEqual(x1,1000)
   self.assertGreaterEqual(y0,230);self.assertLessEqual(y1,1660)
 def test_exact_96_frames(self):self.assertEqual(FRAMES,96);self.assertEqual(END_FRAME-START_FRAME,FRAMES);self.assertEqual(FPS,30)
 def test_frame_dimensions(self):self.assertEqual(make_frame(50,C).size,(W,H))
 def test_frame_changes(self):
  bg=Image.new('RGB',(W,H),'#061322')
  self.assertNotEqual(make_frame(15,C,bg).tobytes(),make_frame(90,C,bg).tobytes())
 def test_frame_bounds(self):
  with self.assertRaises(ValueError):make_frame(96,C)
 def test_easing(self):self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
if __name__=='__main__':unittest.main()
