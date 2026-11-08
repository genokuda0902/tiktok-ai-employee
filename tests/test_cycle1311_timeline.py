import unittest
from quality.cycle1311_timeline import Scene, validate_timeline

class TimelineTest(unittest.TestCase):
    def test_review_only_without_audio_or_approval(self):
        self.assertEqual(validate_timeline([Scene(0, 3, "導入"), Scene(3, 6, "結果")], 6),
                         ["human_unapproved", "narration_unverified", "rights_unapproved"])
    def test_gap_rejected(self):
        self.assertIn("gap_or_overlap", validate_timeline([Scene(0, 2, "A"), Scene(3, 5, "B")], 5))
    def test_approved_contiguous_timeline(self):
        self.assertEqual(validate_timeline([Scene(0, 2, "A"), Scene(2, 4, "B")], 4, True, True, True), [])

if __name__ == "__main__":
    unittest.main()
