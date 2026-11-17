import unittest
from audio_gate import inspect
class AudioGateTests(unittest.TestCase):
    def test_missing_file_fails(self):
        self.assertFalse(inspect("/nonexistent.mp4")["pass"])
    def test_missing_file_reason(self):
        self.assertEqual(inspect("/nonexistent.mp4")["reason"],"probe_failed")
if __name__=="__main__":unittest.main()
