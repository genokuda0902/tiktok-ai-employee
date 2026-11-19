import unittest
from video_end_fade import fade_filter
class FadeTests(unittest.TestCase):
 def test_timing(self): self.assertEqual(fade_filter(22.75), "fade=t=out:st=22.150:d=0.600")
 def test_invalid(self):
  with self.assertRaises(ValueError): fade_filter(0.5)
if __name__=="__main__": unittest.main()
