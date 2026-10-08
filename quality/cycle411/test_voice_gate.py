"""Tests for zero-cost narration gate. ffmpeg is required."""
import unittest, tempfile, subprocess
from pathlib import Path
from voice_gate import check

class TestNarrationGate(unittest.TestCase):
    def make(self, root, tone):
        out=Path(root)/("tone.mp4" if tone else "silent.mp4")
        audio="sine=frequency=430:sample_rate=48000" if tone else "anullsrc=r=48000:cl=mono"
        subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-i","color=c=black:s=1080x1920:r=30",
                        "-f","lavfi","-i",audio,"-t","1","-c:v","libx264","-preset","ultrafast",
                        "-c:a","aac","-ar","48000",str(out)],check=True)
        return out
    def test_silence_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"Silent"): check(self.make(d,False))
    def test_tone_not_certified_as_japanese(self):
        with tempfile.TemporaryDirectory() as d:
            result=check(self.make(d,True))
            self.assertEqual(result["japanese_listening"],"HUMAN_REVIEW_REQUIRED")
            self.assertEqual(result["publication"],"NOT_APPROVED")
if __name__=="__main__": unittest.main()
