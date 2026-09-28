import unittest

from video_engine.compact_caption_layout import CompactCaptionLayout, validate_phrase


class CompactCaptionLayoutTest(unittest.TestCase):
    def test_default_layout_is_valid(self):
        CompactCaptionLayout().validate()

    def test_rejects_wrong_resolution(self):
        with self.assertRaises(ValueError):
            CompactCaptionLayout(canvas_width=720, canvas_height=1280).validate()

    def test_rejects_oversized_card(self):
        with self.assertRaises(ValueError):
            CompactCaptionLayout(card_height=300).validate()

    def test_rejects_long_phrase(self):
        with self.assertRaises(ValueError):
            validate_phrase("あ" * 19)

    def test_accepts_short_japanese_phrase(self):
        self.assertEqual(validate_phrase("まず現状を確認"), "まず現状を確認")


if __name__ == "__main__":
    unittest.main()
