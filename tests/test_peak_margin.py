import unittest
from pathlib import Path
from unittest.mock import patch
from tools.peak_margin import render

class TestPeakMargin(unittest.TestCase):
    def test_invalid_margin(self):
        with self.assertRaises(ValueError): render(Path("in.mp4"),Path("out.mp4"),0)
    @patch("subprocess.run")
    def test_audio_only_reencode(self, run):
        render(Path("in.mp4"),Path("out.mp4"))
        cmd=run.call_args.args[0]
        self.assertEqual(cmd[cmd.index("-c:v")+1],"copy")
        self.assertIn("volume=-1.5dB",cmd)
