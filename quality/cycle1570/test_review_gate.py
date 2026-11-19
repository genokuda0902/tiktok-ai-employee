import unittest
from quality.cycle1570.review_gate import review_gate
class ReviewGateTest(unittest.TestCase):
    def test_rejects_silent_review_video(self):
        result=review_gate({"width":720,"height":1280})
        self.assertFalse(result["approved"])
        self.assertIn("japanese_speech_unverified",result["reasons"])
    def test_requires_all_evidence(self):
        result=review_gate({"width":1080,"height":1920,"japanese_speech_verified":True,"captions_synced_verified":True,"assets_approved":True,"employee_approved":True})
        self.assertTrue(result["approved"])
if __name__=="__main__": unittest.main()
