import unittest
from review_gate import review_gate
class TestReviewGate(unittest.TestCase):
    def test_silent_video_fails(self):
        p={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertIn("japanese_narration_unverified",review_gate(p)["issues"])
    def test_unapproved_fails(self):
        p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertFalse(review_gate(p,narration_verified=True,captions_synced=True)["approved_for_manual_post"])
    def test_all_gates_pass(self):
        p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertTrue(review_gate(p,narration_verified=True,captions_synced=True,assets_approved=True,employee_approved=True)["approved_for_manual_post"])
if __name__=="__main__": unittest.main()
