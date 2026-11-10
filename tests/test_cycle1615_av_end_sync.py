import unittest
from pathlib import Path
from unittest.mock import patch
from tools.cycle1615_av_end_sync import render

class FadeTests(unittest.TestCase):
    def test_fade_and_copy(self):
        with patch("subprocess.run") as run:
            render(Path("in.mp4"), Path("out.mp4"), 25.507)
            args = run.call_args.args[0]
            self.assertIn("afade=t=out:st=25.007:d=0.500", args)
            self.assertEqual(args[args.index("-c:v")+1], "copy")
            self.assertIn("+faststart", args)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            render(Path("a"), Path("b"), 2, 3)
