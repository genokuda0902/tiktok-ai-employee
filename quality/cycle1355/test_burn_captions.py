import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from burn_captions import render
class BurnCaptionTests(unittest.TestCase):
    def test_missing_source_fails_closed(self):
        with TemporaryDirectory() as d:
            p=Path(d);(p/"a.srt").write_text("test")
            with self.assertRaises(FileNotFoundError): render(p/"missing.mp4",p/"a.srt",p/"out.mp4")
    def test_no_speech_claim(self):
        with TemporaryDirectory() as d:
            p=Path(d);(p/"in.mp4").write_bytes(b"synthetic");(p/"a.srt").write_text("test")
            with patch("subprocess.run") as run:
                m=render(p/"in.mp4",p/"a.srt",p/"out.mp4")
                self.assertFalse(m["japanese_narration_verified"])
                self.assertFalse(m["speech_sync_verified"])
                self.assertFalse(m["publication_approved"])
                self.assertIn("subtitles=",str(run.call_args))
if __name__=="__main__": unittest.main()
