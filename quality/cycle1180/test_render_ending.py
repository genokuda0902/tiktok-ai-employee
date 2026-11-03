import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from render_ending import render

class EndingTests(unittest.TestCase):
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            render(Path("/nonexistent/source.mp4"), Path("/tmp/out.mp4"))
    def test_invalid_duration(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "source.mp4"
            source.touch()
            with self.assertRaises(ValueError):
                render(source, Path(td) / "out.mp4", fade_seconds=2.0)
    def test_audio_is_copied_and_review_only(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "source.mp4"
            source.touch()
            with patch("subprocess.run") as run:
                render(source, Path(td) / "out.mp4")
            cmd = run.call_args.args[0]
            self.assertEqual(cmd[cmd.index("-c:a")+1], "copy")
            self.assertIn("fade=t=out", " ".join(cmd))
            self.assertNotIn("upload", " ".join(cmd))

if __name__ == "__main__":
    unittest.main()
