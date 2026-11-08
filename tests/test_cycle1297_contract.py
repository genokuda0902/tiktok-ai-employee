import unittest
from quality.cycle1297_video_contract import publication_ready

class ContractTests(unittest.TestCase):
    def test_silent_review_rejected(self):
        self.assertFalse(publication_ready({"width":1080,"height":1920,"has_audio":False}, timed_captions_verified=True, rights_approved=True, employee_approved=True))
    def test_missing_approval_rejected(self):
        self.assertFalse(publication_ready({"width":1080,"height":1920,"has_audio":True}, timed_captions_verified=True, rights_approved=True))
    def test_all_checks_pass(self):
        self.assertTrue(publication_ready({"width":1080,"height":1920,"has_audio":True}, timed_captions_verified=True, rights_approved=True, employee_approved=True))
if __name__ == "__main__": unittest.main()
