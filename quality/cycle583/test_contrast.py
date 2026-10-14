import unittest
from contrast import ContrastSpec, DEFAULT, GENRES, frame, SIZE

class ContrastTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for name in GENRES:
            self.assertTrue(ContrastSpec(name, '課題', '手順', '証拠', '結果', True).validate())

    def test_requires_evidence(self):
        with self.assertRaises(ValueError):
            ContrastSpec('sales', '課題', '手順', '証拠', '結果').validate()

    def test_render(self):
        self.assertEqual(frame(DEFAULT, 0).size, SIZE)
        self.assertEqual(frame(DEFAULT, 59).size, SIZE)

    def test_numeric_proof(self):
        self.assertEqual(sum([120, 150, 200, 250]), int(DEFAULT.result))

if __name__ == '__main__':
    unittest.main()
