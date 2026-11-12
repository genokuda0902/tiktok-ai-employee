import unittest
from numeric_proof import NumericProof

class NumericProofTest(unittest.TestCase):
    def test_matching_total(self):
        result = NumericProof((2500, 3200, 4100, 2600), 12400).verify()
        self.assertTrue(result["arithmetic_ok"])
        self.assertFalse(result["publication_allowed"])

    def test_incorrect_total(self):
        self.assertFalse(NumericProof((2500, 3200), 12400).verify()["arithmetic_ok"])

    def test_all_gates_required(self):
        self.assertTrue(NumericProof((1, 2), 3, True, True, True).verify()["publication_allowed"])
        self.assertFalse(NumericProof((1, 2), 3, True, False, True).verify()["publication_allowed"])

if __name__ == "__main__":
    unittest.main()
