from pathlib import Path
import unittest
from unittest.mock import patch
from render import render

class TestRender(unittest.TestCase):
    @patch("subprocess.run")
    def test_video_adjustment_and_audio_copy(self, run):
        render(Path("in.mp4"),Path("out.mp4"))
        args=run.call_args.args[0]
        self.assertIn("eq=contrast=1.025:saturation=1.02:brightness=0",args)
        self.assertEqual(args[args.index("-c:a")+1],"copy")
        self.assertEqual(args[args.index("-pix_fmt")+1],"yuv420p")
        self.assertTrue(run.call_args.kwargs["check"])
if __name__=="__main__":
    unittest.main()
