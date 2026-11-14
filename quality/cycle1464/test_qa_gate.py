import unittest
from qa_gate import publishable
class TestGate(unittest.TestCase):
    def test_silent_rejected(self):
        self.assertFalse(publishable({"assets_approved": True}))
    def test_unapproved_rejected(self):
        self.assertFalse(publishable({"narration_language":"ja","speech_aligned_captions":True,"assets_approved":True}))
    def test_all_approved(self):
        self.assertTrue(publishable({"narration_language":"ja","speech_aligned_captions":True,"assets_approved":True,"employee_approved":True,"publication_approved":True}))
if __name__ == "__main__": unittest.main()
