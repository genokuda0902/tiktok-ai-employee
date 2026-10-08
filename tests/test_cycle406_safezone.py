import unittest
from tools.quality.cycle406_safezone_gate import GENRES, CAPTION_BOX, SAFE_BOTTOM_START, check_caption_box

class TestSafeZone(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(set(GENRES)), 10)
    def test_caption_geometry(self):
        self.assertTrue(check_caption_box())
        self.assertLess(CAPTION_BOX[3], SAFE_BOTTOM_START)

if __name__ == '__main__':
    unittest.main()
