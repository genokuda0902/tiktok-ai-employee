import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from cycle775_chart_contract import GENRES, SALES, animated_amounts

class ContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
    def test_sum(self):
        self.assertEqual(sum(SALES.values()), 650000)
    def test_reveal(self):
        self.assertEqual(animated_amounts(1), (120000, 150000, 200000, 180000))

if __name__ == '__main__':
    unittest.main()
