import unittest
from review_caption_gate import Caption, validate_captions, publication_allowed

class CaptionTests(unittest.TestCase):
    def test_contiguous(self):
        self.assertTrue(validate_captions([Caption(0, 2, "最初"), Caption(2, 4, "次")], 4))
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            validate_captions([Caption(0, 2, "最初"), Caption(3, 4, "次")], 4)
    def test_missing_voice_rejected(self):
        self.assertFalse(publication_allowed(speech_sync_verified=True, rights_approved=True, employee_approved=True))
    def test_all_evidence_required(self):
        self.assertTrue(publication_allowed(japanese_speech_verified=True, speech_sync_verified=True, rights_approved=True, employee_approved=True))

if __name__ == "__main__":
    unittest.main()
