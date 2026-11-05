import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.review_audio_qa import render_review

class ReviewAudioQATests(unittest.TestCase):
    def test_missing_input_fails_closed(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                render_review(Path(d)/"missing.mp4", Path(d)/"out.mp4")

if __name__ == "__main__":
    unittest.main()
