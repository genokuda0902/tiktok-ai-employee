import unittest
from render import focus_filter

class FocusTest(unittest.TestCase):
    def test_time_bounds(self):
        self.assertIn("between(t,3,6)",focus_filter())
    def test_japanese_guide(self):
        self.assertIn("ここに注目",focus_filter())
    def test_no_false_speech_claim(self):
        self.assertNotIn("narration_verified",focus_filter())

if __name__=='__main__':
    unittest.main()
