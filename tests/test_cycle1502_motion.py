import unittest
from quality.cycle1502_motion import zoompan_filter, publication_preflight

class MotionReviewTests(unittest.TestCase):
    def test_motion_filter(self):
        vf = zoompan_filter()
        self.assertIn("s=720x1280:fps=24", vf)
        self.assertIn("zoompan", vf)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            zoompan_filter(width=0)

    def test_no_speech_is_not_approved(self):
        self.assertFalse(publication_preflight(
            japanese_speech_verified=False, subtitle_sync_verified=True,
            assets_approved=True, employee_approved=True))

    def test_all_gates_required(self):
        self.assertTrue(publication_preflight(
            japanese_speech_verified=True, subtitle_sync_verified=True,
            assets_approved=True, employee_approved=True))

if __name__ == "__main__":
    unittest.main()
