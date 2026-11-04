import unittest
from tools.cycle1216_summary_card import filtergraph

class SummaryCardTests(unittest.TestCase):
    def test_contains_three_steps(self):
        value = filtergraph()
        for text in ("目的を明確に", "条件を具体的に", "結果を確認"):
            self.assertIn(text, value)
    def test_time_window(self):
        self.assertIn("between(t,17,22)", filtergraph())
    def test_invalid_interval(self):
        with self.assertRaises(ValueError):
            filtergraph(start=22,end=17)

if __name__ == "__main__":
    unittest.main()
