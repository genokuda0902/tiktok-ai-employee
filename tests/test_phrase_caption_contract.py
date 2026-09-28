import unittest

from video_engine.phrase_caption_contract import PhraseCaption, ass_safe_margin_v, validate_caption, validate_sequence


class PhraseCaptionContractTests(unittest.TestCase):
    def test_accepts_short_two_line_caption(self):
        validate_caption(PhraseCaption(0.0, 1.2, "毎日の集計\\NAIなら一瞬"))

    def test_rejects_more_than_two_lines(self):
        with self.assertRaises(ValueError):
            validate_caption(PhraseCaption(0.0, 1.0, "a\\Nb\\Nc"))

    def test_rejects_overlap(self):
        with self.assertRaises(ValueError):
            validate_sequence([PhraseCaption(0, 1, "A"), PhraseCaption(0.9, 2, "B")], 3)

    def test_rejects_caption_past_video_end(self):
        with self.assertRaises(ValueError):
            validate_sequence([PhraseCaption(0, 3.1, "A")], 3)

    def test_safe_margin_is_twelve_percent(self):
        self.assertEqual(ass_safe_margin_v(1920), 230)


if __name__ == "__main__":
    unittest.main()
