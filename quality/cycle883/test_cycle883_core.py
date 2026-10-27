import unittest
from dataclasses import replace
from cycle883_core import *
class TestCore(unittest.TestCase):
 def test_ten_genres(self):
  for genre in GENRES:self.assertTrue(validate(genre))
 def test_22_states(self):self.assertEqual(len(timeline()),22)
 def test_691_frames(self):self.assertEqual(sum(c.end-c.start for c in timeline()),691)
 def test_exactly_eight_scenes(self):self.assertEqual({c.scene for c in timeline()},set(range(1,9)))
 def test_source_screenshot_count(self):self.assertEqual(sum(c.scene in SCREENSHOTS for c in timeline()),13)
 def test_zoom_minimum(self):
  for scene in SCREENSHOTS:self.assertGreaterEqual(zoom_factor(scene),1.5)
 def test_safe_caption_zone(self):self.assertLess(CAPTION_BAND[1],1800)
 def test_missing_state(self):
  with self.assertRaises(ValueError):validate(clips=timeline()[:-1])
 def test_frame_gap(self):
  clips=list(timeline());clips[1]=replace(clips[1],start=clips[1].start+1)
  with self.assertRaises(ValueError):validate(clips=clips)
 def test_bad_genre(self):
  with self.assertRaises(ValueError):validate('random')
 def test_safe_source(self):self.assertTrue(safe_source('locally authored HTML / offline Chromium screenshots'))
 def test_external_network_blocked(self):
  with self.assertRaises(ValueError):safe_source('locally authored HTML / offline Chromium screenshots',external_network=True)
 def test_personal_data_blocked(self):
  with self.assertRaises(ValueError):safe_source('locally authored HTML / offline Chromium screenshots',personal_data=True)
 def test_unknown_source_blocked(self):
  with self.assertRaises(ValueError):safe_source('some external website')
if __name__=='__main__':unittest.main()
