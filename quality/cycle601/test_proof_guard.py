import unittest
from proof_guard import require_first_frame_evidence

class TestEvidence(unittest.TestCase):
    def test_complete_chart(self):
        result = require_first_frame_evidence('AI・仕事効率化', [120, 150, 200, 250], '=SUM(B2:B5)', 4, 720)
        self.assertTrue(result['first_frame_proof'])
    def test_blank_chart_fails(self):
        with self.assertRaises(ValueError):
            require_first_frame_evidence('AI・仕事効率化', [120, 150, 200, 250], '=SUM(B2:B5)', 0, 720)

if __name__ == '__main__':
    unittest.main()
