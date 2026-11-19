import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render
class TestSyntheticRenderer(unittest.TestCase):
 def test_duration(self): self.assertEqual(render.DUR,12)
 def test_dimensions(self): self.assertEqual((render.W,render.H,render.FPS),(720,1280,24))
 def test_scene_count(self): self.assertEqual(len(render.STEPS),4)
 def test_original_synthetic_data(self): self.assertIn("10,000",render.STEPS[-1][0])
 def test_frame_changes(self): self.assertNotEqual(render.frame(1).tobytes(),render.frame(10).tobytes())
if __name__=="__main__":unittest.main()
