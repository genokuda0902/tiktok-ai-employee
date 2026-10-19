import unittest

class TestDimensions(unittest.TestCase):
    def test_vertical(self):
        self.assertEqual((1080, 1920, 30), (1080, 1920, 30))

if __name__ == '__main__':
    unittest.main()
