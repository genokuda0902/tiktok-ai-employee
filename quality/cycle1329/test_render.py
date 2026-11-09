import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from quality.cycle1329.render import render

class RenderSmokeTest(unittest.TestCase):
    def test_review_mp4_decodes_and_has_faststart(self):
        with TemporaryDirectory() as tmp:
            output = render(Path(tmp) / "review.mp4")
            self.assertTrue(output.is_file())
            data = output.read_bytes()
            self.assertLess(data.find(b"moov"), data.find(b"mdat"))
            subprocess.run(["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"], check=True)
            info = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(output)], text=True).strip()
            self.assertEqual(info, "720,1280")

if __name__ == "__main__":
    unittest.main()
