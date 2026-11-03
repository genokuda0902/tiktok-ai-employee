import unittest
from tools.cycle1190_loudness import command

class LoudnessTests(unittest.TestCase):
    def test_video_stream_is_copied(self):
        cmd = command("in.mp4", "out.mp4")
        self.assertEqual(cmd[cmd.index("-c:v") + 1], "copy")
    def test_target_and_peak(self):
        cmd = command("in.mp4", "out.mp4")
        filt = cmd[cmd.index("-af") + 1]
        self.assertIn("I=-16", filt)
        self.assertIn("TP=-1.5", filt)
    def test_refuse_overwrite_input(self):
        with self.assertRaises(ValueError):
            command("in.mp4", "./in.mp4")

if __name__ == "__main__":
    unittest.main()
