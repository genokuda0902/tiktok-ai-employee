import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from cycle1829_audio_fade import process

class TestFade(unittest.TestCase):
    @patch("cycle1829_audio_fade.subprocess.run")
    @patch("cycle1829_audio_fade.duration",return_value=22.87)
    def test_audio_only_fade(self,duration,run):
        process("a.mp4","b.mp4",.45)
        args=run.call_args.args[0]
        self.assertIn("copy",args)
        self.assertIn("afade=t=out:st=22.420:d=0.450",args)

    @patch("cycle1829_audio_fade.duration",return_value=.2)
    def test_short_video(self,duration):
        with self.assertRaises(ValueError): process("a.mp4","b.mp4")

if __name__=="__main__": unittest.main()
