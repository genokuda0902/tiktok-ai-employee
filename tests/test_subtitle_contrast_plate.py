import unittest
from tools.subtitle_contrast_plate import render
class TestSubtitleContrastPlate(unittest.TestCase):
    def test_callable(self):
        self.assertTrue(callable(render))
    def test_invalid_source_raises(self):
        with self.assertRaises(Exception):
            render("/nonexistent/input.mp4","/tmp/should-not-exist.mp4")
if __name__=="__main__": unittest.main()
