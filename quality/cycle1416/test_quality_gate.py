import unittest
from quality_gate import evaluate

class QualityGateTest(unittest.TestCase):
    def test_missing_voice_blocks(self):
        self.assertFalse(evaluate(True, False, False, True, False, True)['publication_approved'])
    def test_missing_approval_blocks(self):
        self.assertFalse(evaluate(True, True, True, True, False, True)['publication_approved'])
    def test_all_requirements_pass(self):
        self.assertTrue(evaluate(True, True, True, True, True, True)['publication_approved'])

if __name__ == '__main__': unittest.main()
