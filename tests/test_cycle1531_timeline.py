import unittest
from quality.cycle1531_timeline import Segment, validate_timeline

class TimelineTest(unittest.TestCase):
    def test_review_video_stays_blocked(self):
        result = validate_timeline([Segment(0, 3, "入力"), Segment(3, 6, "結果")], 6)
        self.assertFalse(result["posting_allowed"])
        self.assertIn("Japanese narration unverified", result["errors"])

    def test_overlap_rejected(self):
        result = validate_timeline([Segment(0, 4, "A"), Segment(3, 6, "B")], 6,
                                   narration_verified=True, rights_approved=True, human_approved=True)
        self.assertFalse(result["posting_allowed"])

    def test_valid_approved_timeline(self):
        result = validate_timeline([Segment(0, 3, "A"), Segment(3, 6, "B")], 6,
                                   narration_verified=True, rights_approved=True, human_approved=True)
        self.assertTrue(result["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
