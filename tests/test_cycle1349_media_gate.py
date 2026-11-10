import unittest
from src.cycle1349_media_gate import assess


class MediaGateTests(unittest.TestCase):
    def setUp(self):
        self.good = {"streams": [{"codec_type": "video", "width": 1080, "height": 1920},
                                 {"codec_type": "audio", "codec_name": "aac"}]}

    def test_silent_rejected(self):
        self.assertIn("audio_missing", assess({"streams": self.good["streams"][:1]})["issues"])

    def test_electronic_tone_not_narration(self):
        self.assertIn("japanese_narration_unverified", assess(self.good)["issues"])

    def test_unsynced_rejected(self):
        self.assertIn("speech_caption_sync_unverified", assess(self.good, narration_verified=True)["issues"])

    def test_rights_rejected(self):
        self.assertIn("asset_rights_unapproved", assess(self.good, True, True)["issues"])

    def test_approved_only_when_all_proven(self):
        self.assertTrue(assess(self.good, True, True, True)["approved_for_publication"])

if __name__ == "__main__":
    unittest.main()
