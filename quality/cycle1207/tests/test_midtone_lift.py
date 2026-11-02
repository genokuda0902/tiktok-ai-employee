import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'midtone_lift.py'
s=importlib.util.spec_from_file_location('mid',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class MidtoneTest(unittest.TestCase):
 def test_profiles(self):self.assertEqual(len(m.GENRE_PROFILES),10)
 def test_profile_bounds(self):
  for v in m.GENRE_PROFILES.values():self.assertTrue(7<=v<=14)
 def test_valid_roi(self):self.assertEqual(m.validate_roi(m.ROI),m.ROI)
 def test_subtitle_overlap(self):
  with self.assertRaises(ValueError):m.validate_roi((64,500,952,1000))
 def test_edge_overlap(self):
  with self.assertRaises(ValueError):m.validate_roi((0,500,952,816))
 def test_odd_roi(self):
  with self.assertRaises(ValueError):m.validate_roi((65,500,952,816))
 def test_reject_high_lift(self):
  with self.assertRaises(ValueError):m.build_filter(lift=25)
 def test_reject_low_lift(self):
  with self.assertRaises(ValueError):m.build_filter(lift=3)
 def test_filter_preserves_other_regions(self):
  f=m.build_filter();self.assertIn('crop=952:816:64:500',f);self.assertIn('overlay=64:500',f)
 def test_filter_luma_only(self):self.assertIn('lutyuv=y=',m.build_filter())
 def test_filter_peak(self):self.assertIn('val+12*',m.build_filter())
 def test_reject_source_missing_stream(self):
  with self.assertRaises(ValueError):m.validate_source({'streams':[]})
if __name__=='__main__':unittest.main()
