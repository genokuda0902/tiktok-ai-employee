import unittest
from unittest.mock import patch
from cycle1877_gamma_readability import improve

class TestGamma(unittest.TestCase):
    @patch("subprocess.run")
    def test_audio_copy_and_gamma(self, run):
        improve("in.mp4","out.mp4")
        cmd=run.call_args.args[0]
        self.assertIn("eq=gamma=1.09:brightness=0.008:saturation=1.02",cmd)
        self.assertEqual(cmd[cmd.index("-c:a")+1],"copy")
        self.assertTrue(run.call_args.kwargs["check"])
