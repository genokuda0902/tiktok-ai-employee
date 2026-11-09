import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.cycle1334_burn_captions import burn

class TestBurnCaptions(unittest.TestCase):
    def test_missing_input_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            with self.assertRaises(FileNotFoundError):
                burn(root/"missing.mp4",root/"missing.srt",root/"out.mp4")
    def test_in_place_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"in.mp4").write_bytes(b"x")
            (root/"in.srt").write_text("1",encoding="utf-8")
            with self.assertRaises(ValueError):
                burn(root/"in.mp4",root/"in.srt",root/"in.mp4")
    def test_ffmpeg_keeps_optional_audio(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"in.mp4").write_bytes(b"x")
            (root/"in.srt").write_text("1",encoding="utf-8")
            with patch("tools.cycle1334_burn_captions.subprocess.run") as run:
                burn(root/"in.mp4",root/"in.srt",root/"out.mp4")
                args=run.call_args.args[0]
                self.assertIn("0:a?",args)
                self.assertIn("+faststart",args)
if __name__=="__main__": unittest.main()
