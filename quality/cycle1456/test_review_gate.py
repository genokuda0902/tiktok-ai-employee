import unittest
from review_gate import assess
class TestReviewGate(unittest.TestCase):
    def test_tone_is_not_narration(self):
        video=dict(width=1080,height=1920,duration=14,video_codec="h264",audio_codec="aac",japanese_narration=False,burned_captions=True)
        result=assess(video,True,True)
        self.assertFalse(result["publication_approved"])
        self.assertIn("no_japanese_narration",result["reasons"])
    def test_approval_required(self):
        video=dict(width=1080,height=1920,duration=14,video_codec="h264",audio_codec="aac",japanese_narration=True,burned_captions=True)
        self.assertFalse(assess(video)["publication_approved"])
    def test_approved_metadata(self):
        video=dict(width=1080,height=1920,duration=14,video_codec="h264",audio_codec="aac",japanese_narration=True,burned_captions=True)
        self.assertTrue(assess(video,True,True)["publication_approved"])
if __name__=="__main__": unittest.main()
