import tempfile
import unittest
from pathlib import Path
from tools.review_caption_track import make_srt, timestamp


class CaptionTests(unittest.TestCase):
    def test_time(self):
        self.assertEqual(timestamp(3.125), "00:00:03,125")

    def test_four_scenes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "captions.srt"
            make_srt([(0, 3, "開始"), (3, 6, "入力"), (6, 9, "計算"), (9, 12, "結果")], path)
            data = path.read_text(encoding="utf-8")
            self.assertIn("00:00:09,000 --> 00:00:12,000", data)
            self.assertEqual(data.count("-->"), 4)

    def test_overlap_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_srt([(0, 3, "A"), (2, 4, "B")], Path(tmp) / "bad.srt")

    def test_empty_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_srt([], Path(tmp) / "bad.srt")


if __name__ == "__main__":
    unittest.main()
