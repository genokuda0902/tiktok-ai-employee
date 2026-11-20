import unittest
from quality.cycle1584_audio_truth_gate import review

class TestGate(unittest.TestCase):
    def test_tone_is_not_speech(self):
        streams = {"streams": [{"codec_type": "video", "width": 540, "height": 960},
                               {"codec_type": "audio", "codec_name": "aac"}]}
        result = review({"japanese_speech_verified": False, "caption_sync_verified": True,
                         "assets_approved": True, "employee_approved": True}, streams)
        self.assertFalse(result["publication_approved"])
        self.assertTrue(result["has_audio_stream"])
        self.assertIn("japanese_speech_unverified", result["reasons"])

    def test_all_approvals_required(self):
        data = {"streams": [{"codec_type": "video"}, {"codec_type": "audio"}]}
        self.assertFalse(review({"japanese_speech_verified": True}, data)["publication_approved"])

    def test_missing_video_fails(self):
        self.assertIn("missing_video", review({}, {"streams": []})["reasons"])

if __name__ == "__main__":
    unittest.main()
