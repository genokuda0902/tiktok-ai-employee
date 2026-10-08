"""Cycle407 QA contract tests. Run with python -m unittest discover -s tests -p 'test_cycle407_quality.py'."""
import unittest
from tools.quality.cycle407_quality_gate import GENRES,CAPTION_BOX,SAFE_BOTTOM_START

class TestCycle407(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_safezone(self): self.assertLess(CAPTION_BOX[3],SAFE_BOTTOM_START)
    def test_caption_dimensions(self): self.assertGreater(CAPTION_BOX[2]-CAPTION_BOX[0],700)
    def test_speech_fail_closed(self):
        from tools.quality.cycle407_quality_gate import inspect_mp4
        import inspect
        self.assertIn("japanese_narration_verified",inspect.getsource(inspect_mp4))
        self.assertIn("False",inspect.getsource(inspect_mp4))

if __name__=="__main__": unittest.main()
