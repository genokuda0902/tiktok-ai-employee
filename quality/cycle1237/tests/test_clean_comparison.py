import importlib.util
import unittest
from pathlib import Path
from PIL import Image
spec=importlib.util.spec_from_file_location('mod',Path(__file__).resolve().parents[1]/'clean_comparison.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class ComparisonTests(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(mod.PALETTES),10)
 def test_all_palettes(self):
  for key in mod.PALETTES: self.assertEqual(mod.render_panel(key).size,(1080,1920))
 def test_bad_genre(self):
  with self.assertRaises(ValueError): mod.render_panel('unsupported')
 def test_long_text(self):
  with self.assertRaises(ValueError): mod.render_panel(before='長い'*20)
 def test_empty_text(self):
  with self.assertRaises(ValueError): mod.render_panel(after='')
 def test_roi_avoids_subtitles(self): self.assertLess(mod.ROI[1]+mod.ROI[3],1300)
 def test_roi_avoids_heading(self): self.assertGreater(mod.ROI[1],400)
 def test_outside_roi_transparent(self):
  a=mod.render_panel();self.assertEqual(a.getpixel((100,1400))[3],0)
 def test_inside_roi_opaque(self):
  a=mod.render_panel();self.assertEqual(a.getpixel((100,600))[3],255)
 def test_distinct_card_colors(self):
  a=mod.render_panel();self.assertNotEqual(a.getpixel((100,650)),a.getpixel((100,900)))
 def test_scene_validation(self):
  ch=[{'start_time':'13.733','end_time':'16.633'}];mod.validate_scene(13.733,16.633,ch)
 def test_reject_wrong_scene(self):
  with self.assertRaises(ValueError): mod.validate_scene(12,15,[{'start_time':'13.733','end_time':'16.633'}])
 def test_reject_too_long(self):
  with self.assertRaises(ValueError): mod.validate_scene(0,10,[{'start_time':'0','end_time':'10'}])
if __name__=='__main__':unittest.main()
