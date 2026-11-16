import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from render import render

class RenderTests(unittest.TestCase):
    def test_missing_inputs_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            with self.assertRaises(FileNotFoundError):
                render(p/"missing.mp4", p/"missing.srt", p/"out.mp4")

    def test_source_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/"source.mp4").write_bytes(b"synthetic")
            (p/"captions.srt").write_text("test")
            with self.assertRaises(ValueError):
                render(p/"source.mp4", p/"captions.srt", p/"source.mp4")

    def test_command_burns_subtitles_and_never_claims_voice(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/"source.mp4").write_bytes(b"synthetic")
            (p/"captions.srt").write_text("test")
            with patch("subprocess.run") as run:
                render(p/"source.mp4", p/"captions.srt", p/"out.mp4")
                cmd = run.call_args.args[0]
                self.assertIn("subtitles=", " ".join(cmd))
                self.assertIn("-an", cmd)
                self.assertNotIn("upload", cmd)
if __name__ == "__main__":
    unittest.main()
