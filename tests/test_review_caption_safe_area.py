import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.review_caption_safe_area import render

class CaptionReviewTests(unittest.TestCase):
    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); font=root/"font.ttc"; font.touch()
            with self.assertRaises(FileNotFoundError):
                render(root/"missing.mp4",root/"out.mp4",font)
    def test_overwrite_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); src=root/"source.mp4"; src.touch(); font=root/"font.ttc"; font.touch()
            with self.assertRaises(ValueError):
                render(src,src,font)
    def test_ffmpeg_uses_audio_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); src=root/"source.mp4"; src.touch(); font=root/"font.ttc"; font.touch()
            with patch("subprocess.run") as run:
                render(src,root/"out.mp4",font)
                args=run.call_args.args[0]
                self.assertEqual(args[args.index("-c:a")+1],"copy")
                self.assertIn("字幕の位置を確認",args[args.index("-vf")+1])
if __name__=="__main__": unittest.main()
