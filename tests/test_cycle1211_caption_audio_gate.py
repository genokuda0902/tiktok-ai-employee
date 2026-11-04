import unittest
from quality.cycle1211_caption_audio_gate import validate_timing


class CaptionTimingTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_timing([{"start": 0, "end": 2, "text": "こんにちは"}], 3), [])

    def test_overlap(self):
        c = [{"start": 0, "end": 2, "text": "一"}, {"start": 1, "end": 3, "text": "二"}]
        self.assertIn("1:overlap_or_unsorted", validate_timing(c, 4))

    def test_missing(self):
        self.assertIn("missing_captions", validate_timing([], 4))

    def test_out_of_bounds(self):
        self.assertIn("0:out_of_bounds", validate_timing([{"start": 0, "end": 5, "text": "文字"}], 4))

    def test_too_short(self):
        self.assertIn("0:too_short", validate_timing([{"start": 0, "end": 0.2, "text": "文字"}], 4))

    def test_too_long_text(self):
        self.assertIn("0:too_many_characters", validate_timing([{"start": 0, "end": 3, "text": "あ" * 25}], 4))


if __name__ == "__main__":
    unittest.main()
