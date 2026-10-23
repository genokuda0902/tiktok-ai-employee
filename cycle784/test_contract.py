import unittest
from contract import GENRES, SAFE_TOP, SAFE_BOTTOM, PUBLICATION_APPROVED

class ContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
    def test_safe_area(self):
        self.assertEqual((SAFE_TOP, SAFE_BOTTOM), (192, 1536))
    def test_review_only(self):
        self.assertFalse(PUBLICATION_APPROVED)

if __name__ == '__main__':
    unittest.main()
