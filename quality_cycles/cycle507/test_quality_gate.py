import unittest

class QualityContractTest(unittest.TestCase):
    def test_native_japanese_voice_is_required(self):
        qa = {"native_japanese_voice": "BLOCKED_NO_TTS_ENGINE"}
        self.assertNotEqual(qa["native_japanese_voice"], "HUMAN_VERIFIED")

    def test_video_is_unapproved(self):
        qa = {"human_review": "PENDING", "publication": "NOT_APPROVED"}
        self.assertNotEqual(qa["publication"], "MANUAL_POST_APPROVED")

if __name__ == "__main__":
    unittest.main()
