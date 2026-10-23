import unittest
from caption_contract import GENRES, validate

class CaptionTests(unittest.TestCase):
    def test_ten_genres(self):
        for genre in GENRES:
            self.assertTrue(validate(genre))

if __name__ == '__main__':
    unittest.main()
