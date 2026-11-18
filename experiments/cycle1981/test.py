import unittest
from pathlib import Path
from process import render

class Tests(unittest.TestCase):
    def test_filter_scope(self):
        s = Path(__file__).with_name('process.py').read_text()
        self.assertIn('crop=1080:1248:0:0', s)
        self.assertIn("'-c:a','copy'", s)
    def test_faststart(self):
        self.assertIn("'+faststart'", Path(__file__).with_name('process.py').read_text())

if __name__ == '__main__':
    unittest.main()
