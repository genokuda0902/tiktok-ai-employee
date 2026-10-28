import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from safe_motion import SCENE_EDGES,MOTION_SCENES,PROFILES,ROI,eased_pulse,motion_params,make_mask,process_frame

class MotionTests(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(PROFILES),10)
 def test_nonnegative_amplitudes(self): self.assertTrue(all(0<a<=.024 for a in PROFILES.values()))
 def test_scene_edges(self): self.assertEqual(len(SCENE_EDGES),9)
 def test_scene_order(self): self.assertTrue(all(a<b for a,b in zip(SCENE_EDGES,SCENE_EDGES[1:])))
 def test_only_four_motion_scenes(self): self.assertEqual(MOTION_SCENES,(0,2,6,7))
 def test_safe_roi_header(self): self.assertGreaterEqual(ROI[1],350)
 def test_safe_roi_captions(self): self.assertLessEqual(ROI[1]+ROI[3],1200)
 def test_roi_inside_frame(self): self.assertLessEqual(ROI[0]+ROI[2],1080)
 def test_pulse_endpoints(self):
  self.assertAlmostEqual(eased_pulse(0),0)
  self.assertAlmostEqual(eased_pulse(1),0)
 def test_pulse_midpoint(self): self.assertAlmostEqual(eased_pulse(.5),1)
 def test_bad_progress(self):
  with self.assertRaises(ValueError): eased_pulse(-.1)
 def test_bad_genre(self):
  with self.assertRaises(ValueError): motion_params(1,'unknown')
 def test_no_motion_scene(self): self.assertEqual(motion_params(4,'ai_productivity'),(1,0,0))
 def test_motion_scene(self): self.assertGreater(motion_params(1.45,'ai_productivity')[0],1.02)
 def test_mask_edges(self):
  m=make_mask(900,840)
  self.assertEqual(m.shape,(840,900,1))
  self.assertEqual(float(m[0,0,0]),0)
  self.assertEqual(float(m[420,450,0]),1)
 def test_preserves_header_caption_and_footer_pixels(self):
  import numpy as np
  frame=np.random.default_rng(42).integers(0,256,size=(1920,1080,3),dtype=np.uint8)
  original=frame.copy()
  process_frame(frame,1.45,'ai_productivity')
  self.assertTrue(np.array_equal(frame[:350],original[:350]))
  self.assertTrue(np.array_equal(frame[1190:],original[1190:]))
  self.assertFalse(np.array_equal(frame[500:1000,200:800],original[500:1000,200:800]))

if __name__=='__main__': unittest.main()
