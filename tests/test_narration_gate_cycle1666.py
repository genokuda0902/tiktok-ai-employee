import unittest
from src.narration_gate import NarrationEvidence, publication_allowed

class GateTest(unittest.TestCase):
    def test_sfx_is_not_narration(self):
        e=NarrationEvidence(True,False,"",False,True,True)
        self.assertFalse(publication_allowed(e))
    def test_missing_approval_rejected(self):
        e=NarrationEvidence(True,True,"日本語の発話",True,True,False)
        self.assertFalse(publication_allowed(e))
    def test_complete_evidence(self):
        e=NarrationEvidence(True,True,"日本語の発話",True,True,True)
        self.assertTrue(publication_allowed(e))

if __name__=="__main__":
    unittest.main()
