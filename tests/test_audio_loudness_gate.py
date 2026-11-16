import unittest
from tools.audio_loudness_gate import validate

class TestAudioGate(unittest.TestCase):
    def test_pass(self):
        self.assertTrue(validate(-15.99, -2.27))
    def test_peak_fail(self):
        self.assertFalse(validate(-16, -0.5))
    def test_loudness_fail(self):
        self.assertFalse(validate(-20, -3))

if __name__ == "__main__":
    unittest.main()
