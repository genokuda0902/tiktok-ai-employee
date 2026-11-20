import unittest
from quality.audio_proof import AudioProof, publication_allowed

class AudioProofTest(unittest.TestCase):
    def test_tone_with_audio_stream_rejected(self):
        self.assertFalse(publication_allowed(AudioProof(True, "", False, False, True, True)))

    def test_missing_caption_alignment_rejected(self):
        self.assertFalse(publication_allowed(AudioProof(True, "日本語の原稿", True, False, True, True)))

    def test_no_employee_approval_rejected(self):
        self.assertFalse(publication_allowed(AudioProof(True, "日本語の原稿", True, True, True, False)))

    def test_all_evidence_required(self):
        self.assertTrue(publication_allowed(AudioProof(True, "日本語の原稿", True, True, True, True)))

if __name__ == "__main__":
    unittest.main()
