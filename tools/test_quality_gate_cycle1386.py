import unittest
from quality_gate_cycle1386 import evaluate

class GateTest(unittest.TestCase):
    def setUp(self):
        self.good = dict(source="synthetic", narration_verified=True,
                         subtitle_sync_verified=True, posting_allowed=False,
                         manual_approval_required=True)
    def test_missing_fields_block(self):
        self.assertFalse(evaluate({})[0])
    def test_no_audio_blocks(self):
        self.good["narration_verified"] = False
        self.assertFalse(evaluate(self.good)[0])
    def test_no_subtitle_sync_blocks(self):
        self.good["subtitle_sync_verified"] = False
        self.assertFalse(evaluate(self.good)[0])
    def test_no_auto_posting(self):
        self.good["posting_allowed"] = True
        self.assertFalse(evaluate(self.good)[0])
    def test_complete_checks_still_require_human(self):
        self.assertTrue(evaluate(self.good)[0])

if __name__ == "__main__":
    unittest.main()
