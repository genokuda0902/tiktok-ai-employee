import unittest
from quality_cycle1304 import review
class GateTest(unittest.TestCase):
    def test_silent_review_rejected(self):
        result=review(dict(width=1080,height=1920,video_decodes=True,assets_rights_approved=True,privacy_checked=True))
        self.assertFalse(result["approved"])
        self.assertIn("narration",result["failures"])
    def test_only_verified_media_approved(self):
        result=review(dict(width=1080,height=1920,video_decodes=True,japanese_narration_verified=True,captions_speech_aligned=True,assets_rights_approved=True,privacy_checked=True,employee_approved=True))
        self.assertTrue(result["approved"])
if __name__=="__main__":unittest.main()
