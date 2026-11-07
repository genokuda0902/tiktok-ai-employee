import unittest
from review_gate import Review, publication_allowed

class GateTests(unittest.TestCase):
    def test_missing_voice_blocks(self):
        r = Review(1080,1920,12,True,False,True,True,True)
        self.assertFalse(publication_allowed(r))
    def test_missing_rights_blocks(self):
        r = Review(1080,1920,12,True,True,True,False,True)
        self.assertFalse(publication_allowed(r))
    def test_all_approved(self):
        r = Review(1080,1920,12,True,True,True,True,True)
        self.assertTrue(publication_allowed(r))
if __name__ == "__main__":
    unittest.main()
