import unittest
from edge_fade import fade_filter

class Tests(unittest.TestCase):
    def test_filter(self):
        self.assertIn("st=22.718", fade_filter(22.938))
    def test_invalid_duration(self):
        with self.assertRaises(ValueError): fade_filter(0.2)
    def test_invalid_fade(self):
        with self.assertRaises(ValueError): fade_filter(10, 1)

if __name__ == "__main__":
    unittest.main()
