import unittest
from audio_onset import render

class TestAudioOnset(unittest.TestCase):
    def test_invalid_duration(self):
        with self.assertRaises(ValueError): render("missing.mp4","out.mp4",0)
        with self.assertRaises(ValueError): render("missing.mp4","out.mp4",1)
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError): render("missing.mp4","out.mp4")
