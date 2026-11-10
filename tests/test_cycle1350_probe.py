import unittest
from quality.cycle1350_probe import probe
class TestProbe(unittest.TestCase):
 def test_missing_file(self):
  with self.assertRaises(FileNotFoundError): probe("/not/a/real/video.mp4")
