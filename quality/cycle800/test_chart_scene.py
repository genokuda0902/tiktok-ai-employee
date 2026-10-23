import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from chart_scene import *
C=json.loads((Path(__file__).parent/'config.json').read_text())
class ChartTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(set(C['genres'])),10)
 def test_valid(self):self.assertTrue(validate(C))
 def test_total(self):self.assertEqual(sum(C['chart']['values']),650000)
 def test_sum_reject(self):
  x=copy.deepcopy(C);x['chart']['total']+=1
  with self.assertRaises(ValueError):validate(x)
 def test_approval_fail_closed(self):
  for k in ('rights_reviewed','employee_approved','publication_approved'):
   x=copy.deepcopy(C);x[k]=True
   with self.assertRaises(ValueError):validate(x)
 def test_publish_reject(self):
  x=copy.deepcopy(C);x['mode']='publish'
  with self.assertRaises(ValueError):validate(x)
 def test_negative_reject(self):
  x=copy.deepcopy(C);x['chart']['values'][0]=-1
  with self.assertRaises(ValueError):validate(x)
 def test_float_reject(self):
  x=copy.deepcopy(C);x['chart']['values'][0]=12.0
  with self.assertRaises(ValueError):validate(x)
 def test_label_mismatch_reject(self):
  x=copy.deepcopy(C);x['chart']['labels'].pop()
  with self.assertRaises(ValueError):validate(x)
 def test_two_to_eight_bars(self):
  x=copy.deepcopy(C);x['chart']['labels']=['A'];x['chart']['values']=[1];x['chart']['total']=1
  with self.assertRaises(ValueError):validate(x)
 def test_frame_geometry(self):self.assertEqual(draw_frame(95,C).size,(1080,1920))
 def test_animation_changes(self):self.assertNotEqual(draw_frame(0,C).tobytes(),draw_frame(80,C).tobytes())
 def test_frame_out_of_bounds(self):
  with self.assertRaises(ValueError):draw_frame(96,C)
 def test_safe_area(self):
  for x0,y0,x1,y1 in safe_boxes().values():self.assertTrue(80<=x0<x1<=1000 and 230<=y0<y1<=1690)
 def test_easing(self):self.assertEqual(easing(-1),0);self.assertEqual(easing(2),1)
if __name__=='__main__':unittest.main()
