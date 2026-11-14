import unittest
from unittest.mock import patch
from tools.video_quality.end_fade import apply

class EndFadeTests(unittest.TestCase):
    @patch("tools.video_quality.end_fade.subprocess.run")
    @patch("tools.video_quality.end_fade.subprocess.check_output",return_value="22.848")
    def test_filter_and_audio_copy(self, probe, run):
        apply("in.mp4","out.mp4")
        args=run.call_args.args[0]
        self.assertIn("fade=t=out:st=22.498:d=0.35",args)
        self.assertEqual(args[args.index("-c:a")+1],"copy")
