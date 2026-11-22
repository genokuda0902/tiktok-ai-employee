import unittest
from quality.cycle1644.storyboard_gate import Review, issues, publishable

class TestReview(unittest.TestCase):
    def test_rejects_silent_review(self):
        r=Review(5,20,1080,1920,False,False,False,False)
        self.assertIn("japanese_narration",issues(r))
        self.assertFalse(publishable(r))
    def test_rejects_unapproved_even_with_audio(self):
        r=Review(5,20,1080,1920,True,True,False,False)
        self.assertFalse(publishable(r))
    def test_all_checks_required(self):
        r=Review(5,20,1080,1920,True,True,True,True)
        self.assertTrue(publishable(r))

if __name__ == "__main__":
    unittest.main()
