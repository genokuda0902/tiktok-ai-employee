import unittest
from storyboard_cycle1433 import Beat, validate, publication_allowed
class TestStory(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate([Beat("problem",0,5,"課題"),Beat("demo",5,10,"実演"),Beat("verification",10,15,"検算")]))
    def test_gap_rejected(self):
        self.assertFalse(validate([Beat("problem",0,5,"課題"),Beat("demo",6,10,"実演"),Beat("verification",10,15,"検算")]))
    def test_missing_voice_rejected(self):
        self.assertFalse(publication_allowed(speech_sync_verified=True,asset_rights_approved=True,employee_approved=True,media_decode_verified=True))
if __name__=="__main__": unittest.main()
