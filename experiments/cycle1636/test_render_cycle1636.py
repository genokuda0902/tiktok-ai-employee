import unittest
from pathlib import Path
from render_cycle1636 import W,H,FPS,DURATION,SCENES,frame
class RendererTests(unittest.TestCase):
    def test_dimensions(self):
        self.assertEqual(frame(0).size,(1080,1920))
    def test_scene_boundaries(self):
        self.assertEqual(len(SCENES),5)
        self.assertEqual(DURATION,18)
        self.assertEqual(FPS,24)
    def test_frames_change(self):
        self.assertNotEqual(frame(0).tobytes(),frame(2).tobytes())
    def test_no_unapproved_audio_claim(self):
        source=Path(__file__).with_name("render_cycle1636.py").read_text()
        self.assertIn('"-an"',source)
if __name__=="__main__":unittest.main()
