import unittest
from quality.cycle651.review_gate import GENRES

class ReviewTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES), 10)

if __name__ == '__main__':
    unittest.main()
