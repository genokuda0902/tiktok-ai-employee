import unittest
from src.cycle716_tts_guard import gate_audio, offline_japanese_tts

class JapaneseAudioGateTests(unittest.TestCase):
    def test_fail_closed_no_voice(self):
        self.assertFalse(gate_audio(False, True, True))
    def test_fail_closed_no_transcript(self):
        self.assertFalse(gate_audio(True, False, True))
    def test_fail_closed_no_rights(self):
        self.assertFalse(gate_audio(True, True, False))
    def test_gate_all_verified(self):
        self.assertTrue(gate_audio(True, True, True))
    def test_probe_list(self):
        self.assertIsInstance(offline_japanese_tts(), list)

if __name__ == "__main__":
    unittest.main()
