import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import unittest
import numpy as np
from scene_focus import SCENES,GENRE_COLORS,SAFE_Y,validate,color_bgr,envelope,apply_focus
class TestFocus(unittest.TestCase):
 def test_safe_scene_layout(self):self.assertTrue(validate(SCENES))
 def test_all_genres(self):self.assertEqual(len(GENRE_COLORS),10);[self.assertEqual(len(color_bgr(g)),3) for g in GENRE_COLORS]
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):color_bgr('not-a-genre')
 def test_fade_no_flash(self):
  self.assertEqual(envelope(0),0);self.assertEqual(envelope(100),0)
  self.assertGreater(envelope(10),0.5)
 def test_outside_region_untouched(self):
  f=np.full((1920,1080,3),30,dtype=np.uint8)
  apply_focus(f,[150,400,600,900],(255,100,0),1)
  self.assertTrue((f[1300:,:,:]==30).all())
  self.assertTrue((f[:200,:,:]==30).all())
  self.assertGreater(int(f[400,150,0]),30)
 def test_invalid_scene_in_safe_zone(self):
  with self.assertRaises(AssertionError):validate([{'start':1,'end':2,'rect':[80,400,900,1350]}])
 def test_scene_order(self):
  with self.assertRaises(AssertionError):validate(list(reversed(SCENES)))
if __name__=='__main__':unittest.main()
