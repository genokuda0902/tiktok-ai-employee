"""Offline CI tests; synthetic audio and frames only, no proprietary assets."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from motion_filter import GENRES, STATUS, VIDEO_FILTER, render, probe, audio_digest

class Cycle813Tests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_no_auto_publication(self):
        self.assertIn("PUBLICATION_NOT_APPROVED",STATUS)
    def test_motion_is_time_varying(self):
        self.assertIn("sin(n/42)",VIDEO_FILTER)
        self.assertIn("cos(n/55)",VIDEO_FILTER)
    def test_native_1080p_output(self):
        self.assertIn("crop=1080:1920",VIDEO_FILTER)
    def test_audio_copy_and_full_decode(self):
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            self.skipTest("ffmpeg/ffprobe unavailable")
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/"source.mp4"; dst=Path(d)/"result.mp4"
            subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
                "testsrc2=size=1080x1920:rate=30:duration=1",
                "-f","lavfi","-i","sine=frequency=440:sample_rate=48000:duration=1",
                "-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",
                "-c:a","aac","-shortest",str(src)],check=True)
            result=render(src,dst)
            self.assertTrue(dst.exists())
            self.assertEqual(result["resolution"],[1080,1920])
            self.assertTrue(result["audio_unchanged"])
            self.assertEqual(audio_digest(src),audio_digest(dst))
            self.assertEqual(int(next(s for s in probe(dst)["streams"] if s["codec_type"]=="video")["nb_frames"]),30)

if __name__=="__main__":
    unittest.main()
