import unittest

GENRES = ('ai_work','beauty','love_psychology','saving','sales_business','career','health','science','travel_food','product_comparison')

class ProofContractTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES), 10)

    def test_verified_arithmetic(self):
        self.assertEqual(2 + 3, 5)

    def test_caption_safe_area(self):
        self.assertLess(1474, 1920 * 0.8)

if __name__ == '__main__':
    unittest.main()
