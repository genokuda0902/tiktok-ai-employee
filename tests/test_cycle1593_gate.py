import unittest
from quality.cycle1593.qa_gate import evaluate, REQUIRED
class TestGate(unittest.TestCase):
    def test_missing_narration_blocks(self):
        self.assertIn("japanese_narration_verified", evaluate({"video_decodes": True})["missing"])
    def test_all_requirements_pass(self):
        self.assertTrue(evaluate({k: True for k in REQUIRED})["publication_approved"])
    def test_false_approval_blocks(self):
        self.assertFalse(evaluate({"employee_approved": False})["publication_approved"])
if __name__ == "__main__": unittest.main()
