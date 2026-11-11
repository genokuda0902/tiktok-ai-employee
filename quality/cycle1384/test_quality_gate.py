import unittest
from quality_gate import publication_allowed, review_report
class QualityGateTests(unittest.TestCase):
    def test_missing_is_blocked(self):
        self.assertFalse(publication_allowed({}))
    def test_audio_stream_is_not_narration(self):
        self.assertFalse(publication_allowed({"audio_stream_present": True}))
    def test_all_verified(self):
        keys=("asset_rights_approved","privacy_approved","employee_approved",
              "japanese_narration_verified","captions_synced_verified",
              "visual_review_approved","recipient_file_verified")
        self.assertTrue(publication_allowed({k:True for k in keys}))
    def test_missing_report(self):
        self.assertIn("japanese_narration_verified",review_report({})["missing"])
if __name__=="__main__": unittest.main()
