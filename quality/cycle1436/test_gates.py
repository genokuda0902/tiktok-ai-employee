import unittest
from gates import evaluate
BASE = dict(public_safe_synthetic=True,narration_verified=False,subtitle_speech_synced=False,employee_approved=False,decode_pass=True,width=1080,height=1920)
class GateTests(unittest.TestCase):
    def test_review_only(self):
        self.assertFalse(evaluate(BASE)["posting_allowed"])
    def test_missing_rights(self):
        self.assertIn("source_rights",evaluate({**BASE,"public_safe_synthetic":False})["blockers"])
    def test_low_resolution(self):
        self.assertIn("resolution",evaluate({**BASE,"width":512,"height":910})["blockers"])
    def test_all_gates(self):
        ok={**BASE,"narration_verified":True,"subtitle_speech_synced":True,"employee_approved":True}
        self.assertTrue(evaluate(ok)["posting_allowed"])
if __name__ == "__main__": unittest.main()
