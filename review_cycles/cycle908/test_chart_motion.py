import unittest
from chart_motion import GENRES, validate, ease, chart_heights, axis_max, frame, publication_gate, PANEL_Y, PANEL_H, CAPTION_TOP

class ChartMotionTests(unittest.TestCase):
 def setUp(self):
  self.data={'genre':'ai_work','synthetic':True,'publication_approved':False,'employee_approved':False,'asset_rights_approved':False,'independent_asr_verified':False,'automatic_posting':False,'source_sha256':'a'*64,'values':{'A':[12,16,18],'B':[8,9,12]}}
 def test_all_genres(self):
  for genre in GENRES:
   d={**self.data,'genre':genre};self.assertTrue(validate(d))
 def test_bad_genre(self):
  d={**self.data,'genre':'invalid'}
  with self.assertRaises(ValueError):validate(d)
 def test_no_unverified_numbers(self):
  d={**self.data,'synthetic':False}
  with self.assertRaises(ValueError):validate(d)
 def test_no_publish(self):
  for key in ('publication_approved','employee_approved','asset_rights_approved','independent_asr_verified','automatic_posting'):
   d={**self.data,key:True}
   with self.assertRaises(ValueError):validate(d)
 def test_numbers(self):
  for values in ({'A':[1,2,-1],'B':[1,2,3]},{'A':[1,2,3],'B':[1,2,'x']},{'A':[1,2,3]}, {'A':[1,2,3,4],'B':[1,2,3]}):
   d={**self.data,'values':values}
   with self.assertRaises(ValueError):validate(d)
 def test_ease(self):
  self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1);self.assertAlmostEqual(ease(.5),.5)
 def test_chart_height_monotonic(self):
  h0=chart_heights(self.data['values'],0);h1=chart_heights(self.data['values'],1)
  self.assertTrue(all(x==0 for v in h0.values() for x in v))
  self.assertEqual(h1['A'][-1],284);self.assertEqual(h1['B'][0],126)
  self.assertEqual(axis_max(self.data['values']),20)
  self.assertEqual(axis_max({'A':[30,45,55],'B':[20,20,20]}),60)
 def test_caption_safe(self):self.assertLess(PANEL_Y+PANEL_H,CAPTION_TOP)
 def test_no_posting(self):
  with self.assertRaises(PermissionError):publication_gate({})
 def test_frames(self):
  try: import PIL
  except ImportError: self.skipTest("Pillow not installed on CI")
  self.assertEqual(frame(self.data,0).size,(900,990))
  self.assertEqual(frame(self.data,80).size,(900,990))
 def test_out_of_range(self):
  with self.assertRaises(ValueError):frame(self.data,81)
if __name__=='__main__':unittest.main()
