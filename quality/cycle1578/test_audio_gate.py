import unittest
from audio_gate import audio_gate

class AudioGateTest(unittest.TestCase):
    def test_silent_video_rejected(self):
        self.assertFalse(audio_gate({"streams": [{"codec_type": "video"}]}, True, True, True, True))
    def test_unverified_speech_rejected(self):
        self.assertFalse(audio_gate({"streams": [{"codec_type": "audio"}]}, False, True, True, True))
    def test_unsynced_captions_rejected(self):
        self.assertFalse(audio_gate({"streams": [{"codec_type": "audio"}]}, True, False, True, True))
    def test_unapproved_assets_rejected(self):
        self.assertFalse(audio_gate({"streams": [{"codec_type": "audio"}]}, True, True, False, True))
    def test_employee_approval_required(self):
        self.assertFalse(audio_gate({"streams": [{"codec_type": "audio"}]}, True, True, True, False))
    def test_all_evidence_present(self):
        self.assertTrue(audio_gate({"streams": [{"codec_type": "audio"}]}, True, True, True, True))

if __name__ == "__main__":
    unittest.main()
