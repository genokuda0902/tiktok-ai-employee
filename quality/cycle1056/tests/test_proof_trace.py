import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from proof_trace import *
class TestProofTrace(unittest.TestCase):
 def test_math_provenance(self):self.assertEqual(totals(),(46,29))
 def test_ten_genres(self):
  self.assertEqual(set(GENRES),set(PALETTES))
  for g in GENRES:self.assertEqual(render_frame(40,g).size,(1080,1270))
 def test_stage_boundaries(self):self.assertEqual([stage(i) for i in (0,22,23,51,52,85)],[0,0,1,1,2,2])
 def test_motion(self):self.assertNotEqual(render_frame(5).tobytes(),render_frame(70).tobytes())
 def test_unknown_genre_fails_closed(self):
  with self.assertRaises(ValueError):render_frame(1,'unsafe')
 def test_invalid_frame_fails(self):
  with self.assertRaises(ValueError):render_frame(86)
 def test_recreated_ui_only(self):
  self.assertEqual(render_frame(0).mode,'RGB')
  self.assertEqual(len(A),3)
if __name__=='__main__':unittest.main()
