import unittest
from hotspot_config import GENRES, VIDEO, APPROVAL

class TestConfig(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES), 10)
    def test_dimensions(self):
        self.assertEqual((VIDEO['width'], VIDEO['height']), (1080, 1920))
    def test_approval(self):
        self.assertFalse(APPROVAL['auto_publish'])
