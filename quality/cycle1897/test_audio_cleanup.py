import unittest
from audio_cleanup import cleanup

class CleanupTests(unittest.TestCase):
    def test_inverted_band(self):
        with self.assertRaises(ValueError): cleanup("x","y",15000,100)
    def test_low_cutoff(self):
        with self.assertRaises(ValueError): cleanup("x","y",10,14500)
    def test_high_cutoff(self):
        with self.assertRaises(ValueError): cleanup("x","y",75,25000)
