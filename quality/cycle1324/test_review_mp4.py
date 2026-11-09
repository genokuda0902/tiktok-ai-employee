import unittest
from review_mp4 import gate

class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.ok = dict(decode_ok=True, width=1080, height=1920, audio_present=True)
    def test_audio_missing_fails(self):
        self.assertFalse(gate({**self.ok, "audio_present": False}))
    def test_low_resolution_fails(self):
        self.assertFalse(gate({**self.ok, "height": 1280, "width": 720}))
    def test_decode_failure_fails(self):
        self.assertFalse(gate({**self.ok, "decode_ok": False}))
    def test_valid_metadata_passes(self):
        self.assertTrue(gate(self.ok))

if __name__ == "__main__":
    unittest.main()
