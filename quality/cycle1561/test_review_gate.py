import unittest
from quality.cycle1561.review_gate import assess
class ReviewGateTests(unittest.TestCase):
    def test_silent_demo_rejected(self):
        result=assess(dict(width=720,height=1280,video_decodes=True))
        self.assertFalse(result["publication_approved"])
        self.assertIn("japanese_narration_missing",result["problems"])
    def test_all_evidence_required(self):
        data=dict(width=1080,height=1920,video_decodes=True,japanese_narration_verified=True,speech_caption_sync_verified=True,assets_approved=True,employee_approved=True)
        self.assertTrue(assess(data)["publication_approved"])
if __name__=="__main__":unittest.main()
