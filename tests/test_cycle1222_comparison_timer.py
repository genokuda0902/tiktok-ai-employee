import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.cycle1222_comparison_timer import filter_expression, render

class TimerTests(unittest.TestCase):
    def test_timer_span(self):
        self.assertIn("between(t,6,14)", filter_expression())
        self.assertIn("(t-6)*115", filter_expression())
    def test_reject_invalid_duration(self):
        with self.assertRaises(ValueError): filter_expression(9, 6)
    def test_reject_missing_source(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(ValueError): render(Path(d)/"missing.mp4", Path(d)/"out.mp4")

if __name__ == "__main__": unittest.main()
