import unittest
from src.review_gate_cycle1359 import review_status

class ReviewGateTest(unittest.TestCase):
    def test_video_only_fails(self):
        x=review_status([{"codec_type":"video"}], True, True, True, True)
        self.assertFalse(x["posting_allowed"])
        self.assertFalse(x["checks"]["japanese_narration"])
    def test_audio_without_narration_verification_fails(self):
        x=review_status([{"codec_type":"video"},{"codec_type":"audio"}], False, True, True, True)
        self.assertFalse(x["posting_allowed"])
    def test_all_verified(self):
        x=review_status([{"codec_type":"video"},{"codec_type":"audio"}], True, True, True, True)
        self.assertTrue(x["posting_allowed"])
if __name__=="__main__": unittest.main()
