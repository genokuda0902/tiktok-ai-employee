import unittest
from caption_overlay import BOX, CANVAS, SAFE_BOTTOM, LINES, validate
class Quality(unittest.TestCase):
    def test_layout(self):
        validate()
        self.assertLessEqual(BOX[1]+BOX[3], CANVAS[1]-SAFE_BOTTOM)
    def test_eight_scenes(self):
        self.assertEqual(len(LINES), 8)
if __name__ == "__main__":
    unittest.main()
