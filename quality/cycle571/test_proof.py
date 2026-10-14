import unittest
from proof import DEMO, chart_bars, GENRES

class ProofTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(DEMO.check(), 720)

    def test_fourth_bar(self):
        self.assertEqual(chart_bars(DEMO)[3][1], 250)

    def test_genres(self):
        self.assertEqual(len(GENRES), 10)

if __name__ == '__main__':
    unittest.main()
