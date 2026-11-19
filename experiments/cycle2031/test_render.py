import unittest
from unittest.mock import patch
from render import render

class TestRender(unittest.TestCase):
    def test_reject_invalid_duration(self):
        with self.assertRaises(ValueError):
            render("in.mp4", "out.mp4", 1.5)

    @patch("render.subprocess.run")
    def test_audio_copy(self, run):
        render("in.mp4", "out.mp4")
        args = run.call_args.args[0]
        self.assertEqual(args[args.index("-c:a") + 1], "copy")
        self.assertIn("fade=t=in:st=0:d=0.35", args)
