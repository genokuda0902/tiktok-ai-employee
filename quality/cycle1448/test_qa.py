import unittest
from quality.cycle1448.qa import check_video

class QATest(unittest.TestCase):
    def setUp(self):
        self.meta={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
    def test_review_is_blocked_without_audio(self):
        r=check_video(self.meta,captions_burned=True,rights_approved=True,employee_approved=True)
        self.assertFalse(r["publication_approved"])
        self.assertIn("japanese_narration_unverified",r["issues"])
    def test_no_rights_is_blocked(self):
        self.meta["streams"].append({"codec_type":"audio"})
        self.assertFalse(check_video(self.meta,captions_burned=True,japanese_voice_verified=True,employee_approved=True)["publication_approved"])
    def test_approved_case(self):
        self.meta["streams"].append({"codec_type":"audio"})
        self.assertTrue(check_video(self.meta,captions_burned=True,japanese_voice_verified=True,rights_approved=True,employee_approved=True)["publication_approved"])
if __name__=="__main__": unittest.main()
