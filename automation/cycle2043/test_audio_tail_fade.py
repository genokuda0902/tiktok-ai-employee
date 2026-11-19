import unittest
from audio_tail_fade import render
class TestFade(unittest.TestCase):
    def test_invalid_input(self):
        with self.assertRaises(ValueError): render('missing.mp4','out.mp4',999)
