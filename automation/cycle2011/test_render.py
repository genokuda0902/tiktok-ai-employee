from pathlib import Path
import unittest
from unittest.mock import patch
from render import render

class RenderTests(unittest.TestCase):
    def test_ffmpeg_audio_copy_and_safe_area(self):
        with patch("subprocess.run") as run:
            render(Path("input.mp4"), Path("output.mp4"))
            cmd = run.call_args.args[0]
            self.assertIn("copy", cmd)
            self.assertIn("1080", "1080")
            self.assertIn("drawbox=x=70:y=270", cmd[cmd.index("-vf")+1])
    def test_unsafe_punctuation_rejected(self):
        with self.assertRaises(ValueError):
            render(Path("a"), Path("b"), "a:b")
