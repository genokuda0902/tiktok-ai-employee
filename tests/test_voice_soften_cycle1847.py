import unittest
from quality.voice_soften import process

class TestVoiceSoftening(unittest.TestCase):
    def test_reject_positive_gain(self):
        with self.assertRaises(ValueError): process("a","b",1)
    def test_reject_excessive_cut(self):
        with self.assertRaises(ValueError): process("a","b",-8)

if __name__ == "__main__":
    unittest.main()
