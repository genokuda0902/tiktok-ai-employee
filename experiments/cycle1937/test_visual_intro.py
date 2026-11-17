import unittest
from visual_intro import build_command

class FadeTests(unittest.TestCase):
    def test_audio_copy_and_filter(self):
        c = build_command("in.mp4", "out.mp4")
        self.assertIn("fade=t=in:st=0:d=0.320", c)
        self.assertEqual(c[c.index("-c:a")+1], "copy")
    def test_reject_same_path(self):
        with self.assertRaises(ValueError): build_command("a.mp4", "a.mp4")
    def test_reject_bad_duration(self):
        with self.assertRaises(ValueError): build_command("a.mp4", "b.mp4", 2)

if __name__ == "__main__": unittest.main()
