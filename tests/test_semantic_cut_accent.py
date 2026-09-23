import unittest

from video_engine.semantic_cut_accent import (
    AUTO_POST_ALLOWED,
    HUMAN_APPROVAL_REQUIRED,
    CutAccentPolicy,
    eq_filter,
    ffmpeg_enable_expression,
)


class SemanticCutAccentTests(unittest.TestCase):
    def test_expression_is_deterministic_and_deduplicated(self):
        self.assertEqual(
            ffmpeg_enable_expression([4, 2, 2]),
            "between(t,2.000,2.100)+between(t,4.000,4.100)",
        )

    def test_rejects_non_vertical_output(self):
        with self.assertRaises(ValueError):
            CutAccentPolicy(width=720, height=1280).validate()

    def test_rejects_overbright_flash(self):
        with self.assertRaises(ValueError):
            CutAccentPolicy(brightness=0.08).validate()

    def test_filter_and_safety_contract(self):
        self.assertIn("eq=brightness=0.035", eq_filter([2.0]))
        self.assertTrue(HUMAN_APPROVAL_REQUIRED)
        self.assertFalse(AUTO_POST_ALLOWED)


if __name__ == "__main__":
    unittest.main()
