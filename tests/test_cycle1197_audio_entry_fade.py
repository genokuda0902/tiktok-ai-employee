import unittest
from pathlib import Path
from tools.cycle1197_audio_entry_fade import build_command

class FadeTest(unittest.TestCase):
    def test_audio_fade_and_video_copy(self):
        command = build_command(Path("in.mp4"), Path("out.mp4"))
        self.assertIn("afade=t=in:st=0:d=0.18", command)
        self.assertEqual(command[command.index("-c:v")+1], "copy")
    def test_no_overwrite(self):
        with self.assertRaises(ValueError):
            build_command(Path("same.mp4"), Path("same.mp4"))
    def test_duration_limit(self):
        for value in (0, -1, 0.51):
            with self.assertRaises(ValueError):
                build_command(Path("a.mp4"), Path("b.mp4"), value)

if __name__ == "__main__":
    unittest.main()
