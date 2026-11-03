import tempfile
import unittest
from pathlib import Path
from audio_edge import build_command

class TestAudioEdge(unittest.TestCase):
    def test_command(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "in.mp4"
            src.touch()
            cmd = build_command(src, Path(td) / "out.mp4", 23.033)
            self.assertIn("-c:v", cmd)
            self.assertIn("copy", cmd)
            self.assertIn("afade=t=out:st=22.783:d=0.25", cmd[cmd.index("-af")+1])
    def test_missing(self):
        with self.assertRaises(ValueError):
            build_command(Path("/nonexistent.mp4"), Path("/tmp/out.mp4"), 23)
    def test_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td)/"in.mp4"
            src.touch()
            with self.assertRaises(ValueError):
                build_command(src, Path(td)/"out.mp4", .1)

if __name__ == "__main__":
    unittest.main()
