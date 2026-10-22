import unittest
from quality_cycles.cycle763.src.genre_geometry import GENRES, validate_genre, safe_caption

class TestQuality(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            self.assertTrue(validate_genre(genre))

    def test_unknown(self):
        with self.assertRaises(ValueError):
            validate_genre("unknown")

    def test_caption(self):
        self.assertTrue(safe_caption(92,1455,904,1605))
        self.assertFalse(safe_caption(92,1455,1000,1605))

if __name__ == "__main__":
    unittest.main()
