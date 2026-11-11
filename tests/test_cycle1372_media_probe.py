import unittest
from quality.cycle1372_media_probe import assert_review_only
class ReviewGateTests(unittest.TestCase):
    def test_blocks_unverified_audio(self):
        self.assertTrue(assert_review_only({"posting_allowed":False,"human_approval_required":True,"narration_verified":False}))
    def test_rejects_publishing(self):
        with self.assertRaises(AssertionError):
            assert_review_only({"posting_allowed":True,"human_approval_required":True,"narration_verified":False})
if __name__=="__main__":unittest.main()
