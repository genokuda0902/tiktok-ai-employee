import unittest
from tools.audio_loudness import normalize

class TestNormalize(unittest.TestCase):
    def test_invalid_low(self):
        with self.assertRaises(ValueError):
            normalize("a.mp4", "b.mp4", -30)
    def test_invalid_high(self):
        with self.assertRaises(ValueError):
            normalize("a.mp4", "b.mp4", -5)
