import unittest
from unittest.mock import patch
from tools.cycle1869_normalize_audio import normalize

class TestNormalize(unittest.TestCase):
    def test_reject_invalid_target(self):
        with self.assertRaises(ValueError):
            normalize("in.mp4","out.mp4",-4)

    @patch("tools.cycle1869_normalize_audio.subprocess.run")
    def test_command(self, run):
        normalize("in.mp4","out.mp4")
        cmd=run.call_args.args[0]
        self.assertIn("copy",cmd)
        self.assertIn("loudnorm=I=-16:TP=-1.5:LRA=11",cmd)
        self.assertTrue(run.call_args.kwargs["check"])
