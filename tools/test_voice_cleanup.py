import unittest
from voice_cleanup import build_command

class TestVoiceCleanup(unittest.TestCase):
    def test_preserves_video(self):
        c = build_command("a.mp4", "b.mp4")
        self.assertEqual(c[c.index("-c:v")+1], "copy")
    def test_highpass(self):
        self.assertIn("highpass=f=75", build_command("a.mp4","b.mp4"))
    def test_rejects_same_path(self):
        with self.assertRaises(ValueError):
            build_command("a.mp4", "a.mp4")
