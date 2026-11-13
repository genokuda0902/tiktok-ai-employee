import unittest
from caption_timing import scene_srt,srt_timestamp
class TestTiming(unittest.TestCase):
 def test_end(self):
  s=scene_srt(["最初","次"],6)
  self.assertIn("00:00:03,000 --> 00:00:06,000",s)
 def test_negative(self):
  with self.assertRaises(ValueError): srt_timestamp(-1)
 def test_blank(self):
  with self.assertRaises(ValueError): scene_srt([""],3)
if __name__=="__main__": unittest.main()
