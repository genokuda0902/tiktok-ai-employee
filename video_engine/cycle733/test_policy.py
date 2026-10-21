import unittest
from cta_policy import PALETTES, GENRE_COPY, validate_genre

class TestCTA(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES), 10)
        self.assertEqual(set(PALETTES), set(GENRE_COPY))
    def test_unknown_rejected(self):
        with self.assertRaises(ValueError):
            validate_genre('unknown')

if __name__ == '__main__':
    unittest.main()
