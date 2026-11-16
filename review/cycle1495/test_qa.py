import unittest
from pathlib import Path
from qa import assess

class GateTests(unittest.TestCase):
    def test_missing_audio_cannot_pass(self):
        p = Path(__file__).parent / "cycle1495_REVIEW_ONLY.mp4"
        if not p.exists():
            self.skipTest("Review MP4 not in repository; run local renderer first")
        result = assess(p, True, True, True, True)
        self.assertFalse(result["publication_approved"])
        self.assertFalse(result["checks"]["japanese_narration_verified"])

    def test_no_approval(self):
        p = Path(__file__).parent / "cycle1495_REVIEW_ONLY.mp4"
        if not p.exists():
            self.skipTest("Review MP4 not in repository; run local renderer first")
        self.assertFalse(assess(p)["publication_approved"])

if __name__ == "__main__":
    unittest.main()
