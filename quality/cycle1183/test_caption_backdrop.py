import unittest
from quality.cycle1183.caption_backdrop import command

class BackdropTest(unittest.TestCase):
    def test_overlay_and_audio_copy(self):
        cmd = command("in.mp4", "out.mp4")
        self.assertIn("-c:a", cmd)
        self.assertEqual(cmd[cmd.index("-c:a") + 1], "copy")
        self.assertIn("drawbox=", cmd[cmd.index("-vf") + 1])
    def test_reject_invalid_alpha(self):
        with self.assertRaises(ValueError):
            command("a.mp4", "b.mp4", 0.9)
    def test_reject_overwrite(self):
        with self.assertRaises(ValueError):
            command("same.mp4", "same.mp4")
if __name__ == "__main__":
    unittest.main()
