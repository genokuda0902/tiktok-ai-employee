import unittest

class TestVideoDimensions(unittest.TestCase):
    def test_vertical_ratio(self):
        self.assertEqual(1080 * 16, 1920 * 9)
    def test_fps(self):
        self.assertEqual(30 * 20, 600)

if __name__ == '__main__':
    unittest.main()
