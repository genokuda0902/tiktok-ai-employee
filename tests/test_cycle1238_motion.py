import unittest
from src.quality.cycle1238_motion import punch_in

class MotionTests(unittest.TestCase):
    def test_rejects_invalid_zoom(self):
        with self.assertRaises(ValueError): punch_in("missing.mp4","out.mp4",zoom=1.2)
    def test_rejects_invalid_interval(self):
        with self.assertRaises(ValueError): punch_in("missing.mp4","out.mp4",start=15,end=7)
    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError): punch_in("/missing/video.mp4","out.mp4")

if __name__ == "__main__": unittest.main()
