import unittest
from quality.cycle1429.storyboard import Beat, validate

class StoryboardTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate([Beat("hook",0,5,"問題"),Beat("demonstration",5,10,"実演"),Beat("verification",10,15,"検証")]))
    def test_missing_verification(self):
        with self.assertRaises(ValueError):
            validate([Beat("hook",0,5,"問題"),Beat("demonstration",5,10,"実演")])
    def test_gap(self):
        with self.assertRaises(ValueError):
            validate([Beat("hook",0,5,"問題"),Beat("demonstration",6,10,"実演"),Beat("verification",10,15,"検証")])

if __name__ == "__main__":
    unittest.main()
