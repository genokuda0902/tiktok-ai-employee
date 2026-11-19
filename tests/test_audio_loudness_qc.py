import unittest
from audio_loudness_qc import duration
class AudioTests(unittest.TestCase):
    def test_duration_probe(self):
        self.assertTrue(callable(duration))
    def test_reject_invalid_input(self):
        with self.assertRaises(Exception): duration("missing.mp4")
if __name__=="__main__": unittest.main()
