import unittest
from caption_contract import Caption, validate, publication_gate

class CaptionTests(unittest.TestCase):
    def test_valid_three_scenes(self):
        self.assertTrue(validate([Caption(0,5000,"合計を確認"),Caption(5000,10000,"数式を入力"),Caption(10000,15000,"検算")],15000))
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            validate([Caption(0,6000,"A"),Caption(5000,15000,"B")],15000)
    def test_past_duration_rejected(self):
        with self.assertRaises(ValueError):
            validate([Caption(0,15001,"A")],15000)
    def test_no_narration_never_publishable(self):
        self.assertFalse(publication_gate(japanese_narration_verified=False,speech_sync_verified=False,asset_rights_approved=True,employee_approved=False))

if __name__=="__main__":
    unittest.main()
