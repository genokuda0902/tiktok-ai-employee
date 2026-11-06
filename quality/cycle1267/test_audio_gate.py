import unittest
from audio_gate import publication_gate

class GateTest(unittest.TestCase):
    def test_silent_video_rejected(self):
        self.assertIn("missing_audio", publication_gate([{"codec_type": "video"}]))

    def test_audio_track_not_enough(self):
        self.assertIn("japanese_voice_unverified", publication_gate([{"codec_type": "video"}, {"codec_type": "audio"}]))

    def test_all_gates_required(self):
        self.assertEqual([], publication_gate([{"codec_type": "video"}, {"codec_type": "audio"}], japanese_voice_verified=True, captions_synced=True, assets_approved=True, human_approved=True))

if __name__ == "__main__":
    unittest.main()
