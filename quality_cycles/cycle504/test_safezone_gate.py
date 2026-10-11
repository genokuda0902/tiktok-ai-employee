"""Run: python -m unittest quality_cycles.cycle504.test_safezone_gate"""
import unittest
from quality_cycles.cycle504.safezone_gate import (
    GENRES, TextBox, text_fits_safe_zone, verify_text_boxes,
    publication_approved,
)

class QualityGateTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)

    def test_inside(self):
        self.assertTrue(text_fits_safe_zone(TextBox(125, 270, 760, 1240)))

    def test_left_overflow(self):
        self.assertFalse(text_fits_safe_zone(TextBox(100, 270, 760, 1240)))

    def test_right_rail(self):
        self.assertFalse(text_fits_safe_zone(TextBox(125, 270, 820, 1240)))

    def test_bottom_overlay(self):
        self.assertFalse(text_fits_safe_zone(TextBox(125, 270, 760, 1420)))

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            verify_text_boxes([])

    def test_invalid_rejected(self):
        with self.assertRaises(ValueError):
            verify_text_boxes([TextBox(100, 270, 760, 1240)])

    def test_sfx_only_never_approved(self):
        qa = {
            "full_decode": "PASS", "resolution": [1080, 1920],
            "native_japanese_voice": "NOT_GENERATED",
            "voice_caption_sync": "NOT_VERIFIED",
            "human_review": "PENDING",
            "publication": "NOT_APPROVED",
        }
        self.assertFalse(publication_approved(qa))

    def test_approved_requires_all(self):
        qa = {
            "full_decode": "PASS", "resolution": [1080, 1920],
            "native_japanese_voice": "HUMAN_VERIFIED",
            "voice_caption_sync": "PASS",
            "human_review": "APPROVED",
            "publication": "MANUAL_POST_APPROVED",
        }
        self.assertTrue(publication_approved(qa))
        qa["voice_caption_sync"] = "NOT_VERIFIED"
        self.assertFalse(publication_approved(qa))

if __name__ == "__main__":
    unittest.main()
