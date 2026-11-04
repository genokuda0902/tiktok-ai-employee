import tempfile
import unittest
from pathlib import Path
from tools.cycle1202_loudness_gate import normalize

class TestLoudnessGate(unittest.TestCase):
    def test_reject_out_of_range(self):
        with self.assertRaises(ValueError):
            normalize(Path("missing.mp4"), Path("out.mp4"), -30)

    def test_reject_same_file(self):
        with self.assertRaises(ValueError):
            normalize(Path("same.mp4"), Path("same.mp4"))

    def test_reject_missing_input(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                normalize(Path(d)/"missing.mp4", Path(d)/"out.mp4")

if __name__ == "__main__":
    unittest.main()
