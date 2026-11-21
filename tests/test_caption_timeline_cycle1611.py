import unittest
from src.caption_timeline import Caption, validate_captions

class CaptionTimelineTests(unittest.TestCase):
    def test_timed_cards_are_not_speech_aligned(self):
        result = validate_captions([Caption(0, 3, "集計"), Caption(3, 6, "条件")], 6)
        self.assertFalse(result["speech_aligned"])
        self.assertFalse(result["publication_approved"])

    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            validate_captions([Caption(0, 4, "A"), Caption(3, 6, "B")], 6)

    def test_false_speech_claim_rejected(self):
        with self.assertRaises(ValueError):
            validate_captions([Caption(0, 3, "A")], 3, speech_aligned=True)

if __name__ == "__main__":
    unittest.main()
