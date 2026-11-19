import unittest
from pathlib import Path
from recover_video import verify

class TestRecovery(unittest.TestCase):
    def test_black_video_is_rejected(self):
        # A synthetic all-black fixture generated locally by FFmpeg.
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/"black.mp4"
            subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
                "color=black:s=108x192:r=5:d=1","-c:v","libx264",str(f)],check=True)
            with self.assertRaises(ValueError): verify(f)

if __name__=="__main__":
    unittest.main()
