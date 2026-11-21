import unittest
from quality.cycle1612_review import review
class ReviewTests(unittest.TestCase):
    def test_missing_evidence_fails(self):
        self.assertFalse(review({})["publication_approved"])
    def test_no_voice_fails(self):
        m=dict(width=720,height=1280,fps=24,japanese_speech_verified=False,captions_speech_aligned=True,assets_approved=True,privacy_checked=True,employee_approved=True)
        self.assertIn("japanese_speech",review(m)["failures"])
    def test_full_evidence(self):
        m=dict(width=720,height=1280,fps=24,japanese_speech_verified=True,captions_speech_aligned=True,assets_approved=True,privacy_checked=True,employee_approved=True)
        self.assertTrue(review(m)["publication_approved"])
if __name__=="__main__":unittest.main()
