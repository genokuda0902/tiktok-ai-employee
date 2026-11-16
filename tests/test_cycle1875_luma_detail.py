import unittest
from tools.cycle1875_luma_detail import command

class TestLumaDetail(unittest.TestCase):
    def test_audio_is_preserved(self):
        self.assertIn("copy",command("a.mp4","b.mp4"))
    def test_strength_limit(self):
        with self.assertRaises(ValueError): command("a","b",2)
