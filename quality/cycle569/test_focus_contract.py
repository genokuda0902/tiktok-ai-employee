import unittest
from focus_contract import CUES, validate

class CueTests(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(CUES), 4)
    def test_valid(self):
        self.assertTrue(validate())
