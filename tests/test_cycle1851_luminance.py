import unittest
from unittest.mock import patch
from tools.cycle1851_luminance import enhance
class TestEnhance(unittest.TestCase):
    def test_filter(self):
        with patch("subprocess.run") as run:
            enhance("input.mp4","output.mp4")
            self.assertIn("eq=gamma=1.1:contrast=1.015",run.call_args.args[0])
    def test_bounds(self):
        with self.assertRaises(ValueError):
            enhance("input.mp4","output.mp4",1.3)
