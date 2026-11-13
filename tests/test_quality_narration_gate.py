import unittest
from src.quality_narration_gate import VideoEvidence, publication_gate

class TestNarrationGate(unittest.TestCase):
    def base(self, **overrides):
        args = dict(width=1080,height=1920,video_decodes=True,
                    audio_stream_present=True,japanese_narration_verified=True,
                    speech_caption_sync_verified=True,assets_approved=True,
                    human_quality_approved=True)
        args.update(overrides)
        return VideoEvidence(**args)
    def test_silent_audio_not_narration(self):
        ok, reasons = publication_gate(self.base(japanese_narration_verified=False))
        self.assertFalse(ok)
        self.assertIn("narration", reasons)
    def test_no_human_approval(self):
        self.assertFalse(publication_gate(self.base(human_quality_approved=False))[0])
    def test_missing_sync(self):
        self.assertIn("caption_sync", publication_gate(self.base(speech_caption_sync_verified=False))[1])
    def test_all_verified(self):
        self.assertEqual(publication_gate(self.base()), (True, []))

if __name__ == "__main__":
    unittest.main()
