import unittest
from review_gate import assess

class ReviewGateTest(unittest.TestCase):
    def test_silent_video_rejected(self):
        self.assertFalse(assess({"streams":[{"codec_type":"video","width":720,"height":1280}]})["posting_allowed"])

    def test_audio_stream_alone_not_narration(self):
        m={"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}
        self.assertFalse(assess(m)["checks"]["japanese_narration_verified"])

    def test_all_approval_conditions_required(self):
        m={"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}
        self.assertFalse(assess(m,japanese_narration_verified=True,captions_synchronized_verified=True,assets_approved=True)["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
