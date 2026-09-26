import unittest

from video_engine.semantic_keyword_emphasis import KeywordBeat, build_drawtext_filters, validate_beats


class SemanticKeywordEmphasisTests(unittest.TestCase):
    def test_valid_non_overlapping_beats(self):
        beats = [KeywordBeat("時短", 1.8, 3.8), KeywordBeat("自動化", 3.8, 6.0)]
        self.assertEqual(2, len(validate_beats(beats, 12.7)))

    def test_rejects_overlap(self):
        with self.assertRaises(ValueError):
            validate_beats([KeywordBeat("A", 1, 3), KeywordBeat("B", 2, 4)], 10)

    def test_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            validate_beats([KeywordBeat("結果", 9, 11)], 10)

    def test_filter_keeps_safe_zone_and_timing(self):
        value = build_drawtext_filters([KeywordBeat("保存", 10.4, 12.5)], 12.7, "/font.ttc")
        self.assertIn("y=1320", value)
        self.assertIn("between(t,10.400,12.500)", value)
        self.assertIn("text='保存'", value)


if __name__ == "__main__":
    unittest.main()
