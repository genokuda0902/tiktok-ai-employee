import unittest
from caption_safe_zone import caption_rect, validate_caption_rect, publication_gate

class CaptionSafeZoneTests(unittest.TestCase):
    def test_vertical_geometry(self):
        self.assertTrue(validate_caption_rect(caption_rect(1080, 1920),1080,1920))
    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            caption_rect(0, 1920)
    def test_fail_closed_without_verified_speech(self):
        self.assertFalse(publication_gate(captions_synchronized=True,rights_approved=True,employee_approved=True))
    def test_all_approvals_required(self):
        self.assertTrue(publication_gate(japanese_speech_verified=True,captions_synchronized=True,rights_approved=True,employee_approved=True))

if __name__ == "__main__":
    unittest.main()
