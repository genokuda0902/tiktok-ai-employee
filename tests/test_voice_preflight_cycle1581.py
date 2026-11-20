import unittest
from quality.voice_preflight import posting_allowed

class VoiceGateTests(unittest.TestCase):
    def test_silent_fails(self):
        self.assertFalse(posting_allowed({"video": True, "audio": False, "duration": 12}, True, True, True, True))
    def test_audio_not_enough(self):
        self.assertFalse(posting_allowed({"video": True, "audio": True, "duration": 12}, False, True, True, True))
    def test_all_approvals_required(self):
        self.assertTrue(posting_allowed({"video": True, "audio": True, "duration": 12}, True, True, True, True))
if __name__ == "__main__": unittest.main()
