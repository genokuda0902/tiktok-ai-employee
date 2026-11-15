import unittest
from unittest.mock import patch
from improve import render

class TestCommand(unittest.TestCase):
    @patch("subprocess.run")
    def test_luma_only_sharpen_and_audio_copy(self, run):
        render("input.mp4","output.mp4")
        args=run.call_args.args[0]
        self.assertIn("unsharp=5:5:0.32:5:5:0.0",args)
        self.assertEqual(args[args.index("-c:a")+1],"copy")
        self.assertEqual(args[-1],"output.mp4")

if __name__=="__main__": unittest.main()
