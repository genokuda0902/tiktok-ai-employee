import unittest
from temporal_cleanup import FILTER
class TestFilter(unittest.TestCase):
    def test_caption_protection(self):
        self.assertIn("crop=iw:1380:0:0", FILTER)
        self.assertIn("overlay=0:0", FILTER)
    def test_denoise(self):
        self.assertIn("hqdn3d=", FILTER)
if __name__=="__main__": unittest.main()
