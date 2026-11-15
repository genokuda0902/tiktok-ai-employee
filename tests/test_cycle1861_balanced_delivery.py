import unittest
from tools.cycle1861_balanced_delivery import encode

class TestEncode(unittest.TestCase):
    def test_rejects_invalid_crf(self):
        for crf in (-1, 52):
            with self.assertRaises(ValueError):
                encode(None, None, crf)
