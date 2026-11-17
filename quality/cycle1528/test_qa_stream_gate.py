import unittest
from qa_stream_gate import gate

class TestGate(unittest.TestCase):
    def test_no_audio(self):
        self.assertFalse(gate({"has_audio_stream": False, "narration_verified": True, "caption_sync_verified": True, "rights_approved": True, "employee_approved": True}))
    def test_audio_not_narration(self):
        self.assertFalse(gate({"has_audio_stream": True, "narration_verified": False, "caption_sync_verified": True, "rights_approved": True, "employee_approved": True}))
    def test_missing_approval(self):
        self.assertFalse(gate({"has_audio_stream": True, "narration_verified": True, "caption_sync_verified": True, "rights_approved": True}))
    def test_all_gates(self):
        self.assertTrue(gate({"has_audio_stream": True, "narration_verified": True, "caption_sync_verified": True, "rights_approved": True, "employee_approved": True}))

if __name__ == "__main__":
    unittest.main()
