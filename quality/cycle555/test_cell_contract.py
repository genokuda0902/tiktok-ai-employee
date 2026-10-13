import unittest
from cell_contract import FORMULA, check

class CellContractTests(unittest.TestCase):
    def test_formula(self):
        self.assertEqual(FORMULA, "=SUM(B2:B5)")
    def test_sum(self):
        cells = check([120,150,200,250])
        self.assertEqual(cells["B5"], 250)
        self.assertEqual(cells["B6"], 720)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            check([1,-1,2,3])

if __name__ == "__main__":
    unittest.main()
