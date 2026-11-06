import unittest
from qa.cycle1270_audio_gate import review

class ReviewGateTest(unittest.TestCase):
    def test_silent_video_fails(self):
        meta={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertFalse(review(meta,narration_verified=True,captions_synced=True,assets_approved=True,human_approved=True)["publication_approved"])
    def test_audio_stream_alone_fails(self):
        meta={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
        self.assertFalse(review(meta)["publication_approved"])
    def test_all_verified_pass(self):
        meta={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertTrue(review(meta,narration_verified=True,captions_synced=True,assets_approved=True,human_approved=True)["publication_approved"])

if __name__ == "__main__": unittest.main()
