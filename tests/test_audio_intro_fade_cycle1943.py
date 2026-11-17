import unittest
from pathlib import Path
from unittest.mock import patch
from tools.audio_intro_fade import build

class Tests(unittest.TestCase):
    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            build(Path("a.mp4"), Path("b.mp4"), 2.0)

    @patch("tools.audio_intro_fade.subprocess.run")
    def test_video_copy_and_audio_fade(self, run):
        build(Path("a.mp4"), Path("b.mp4"))
        args = run.call_args.args[0]
        self.assertEqual(args[args.index("-c:v") + 1], "copy")
        self.assertIn("afade=t=in:st=0:d=0.18", args)
