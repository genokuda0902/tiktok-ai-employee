import unittest
from color_balance import filtergraph

class TestColorBalance(unittest.TestCase):
    def test_default(self):
        self.assertEqual(filtergraph(), "eq=saturation=0.880")
    def test_invalid(self):
        for value in [0.4, 1.1]:
            with self.assertRaises(ValueError):
                filtergraph(value)

if __name__ == "__main__":
    unittest.main()
