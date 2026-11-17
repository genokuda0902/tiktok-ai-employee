import unittest
from caption_integrity import validate_captions, publication_gate

class CaptionTests(unittest.TestCase):
    def test_contiguous(self):
        self.assertTrue(validate_captions([(0, 3, "入力"), (3, 8, "確認")], 8))
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            validate_captions([(0, 3, "入力"), (4, 8, "確認")], 8)
    def test_silent_video_rejected(self):
        self.assertFalse(publication_gate({"captions_present": True, "audio_stream_present": True}))
    def test_approved(self):
        self.assertTrue(publication_gate(dict(narration_verified=True, caption_sync_verified=True, asset_rights_approved=True, human_approved=True)))

if __name__ == "__main__":
    unittest.main()
