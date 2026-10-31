import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from proof_component import GENRES,W,H,FPS,draw_hook_frame,draw_proof_frame,smoothstep

class ProofComponentTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for genre in GENRES:
   self.assertEqual(draw_hook_frame(.5,genre).size,(W,H))
   self.assertEqual(draw_proof_frame(.5,genre).size,(W,H))
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):draw_hook_frame(.2,"bad")
 def test_hook_changes(self):
  a=draw_hook_frame(.1).crop((600,740,1000,1080))
  b=draw_hook_frame(1.1).crop((600,740,1000,1080))
  self.assertNotEqual(a.tobytes(),b.tobytes())
 def test_proof_changes(self):
  a=draw_proof_frame(.1).crop((580,750,1000,1090))
  b=draw_proof_frame(1.8).crop((580,750,1000,1090))
  self.assertNotEqual(a.tobytes(),b.tobytes())
 def test_safe_region(self):
  a=draw_proof_frame(1.0)
  self.assertEqual(a.getpixel((100,1500)),(7,26,43))
 def test_duration(self):
  self.assertEqual((W,H,FPS),(1080,1920,30))
 def test_clamping(self):
  self.assertEqual(smoothstep(-1),0)
  self.assertEqual(smoothstep(2),1)
  self.assertAlmostEqual(smoothstep(.5),.5)
if __name__=="__main__":unittest.main()
