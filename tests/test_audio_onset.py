import unittest
from tools.audio_onset import smooth_onset
class TestOnset(unittest.TestCase):
    def test_invalid_duration(self):
        for n in [-1,0,.51]:
            with self.assertRaises(ValueError): smooth_onset("missing.mp4","out.mp4",n)
    def test_missing_input(self):
        with self.assertRaises(FileNotFoundError): smooth_onset("missing.mp4","out.mp4")
