import unittest
from narration_evidence import check

class NarrationEvidenceTests(unittest.TestCase):
    def test_missing_evidence_rejected(self):
        self.assertFalse(check({})["passed"])
    def test_audio_track_alone_not_enough(self):
        self.assertFalse(check({"audio_stream_present":True,"posting_allowed":False})["passed"])
    def test_review_only_never_postable(self):
        m=dict(narration_language="ja",narration_verified=True,caption_sync_verified=True,
               asset_rights_approved=True,human_quality_approved=True,posting_allowed=False)
        self.assertTrue(check(m)["passed"])
        self.assertFalse(check(m)["posting_allowed"])
    def test_unapproved_rejected(self):
        m=dict(narration_language="ja",narration_verified=True,caption_sync_verified=True,
               asset_rights_approved=False,human_quality_approved=False,posting_allowed=False)
        self.assertFalse(check(m)["passed"])
if __name__=="__main__": unittest.main()
