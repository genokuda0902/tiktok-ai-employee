import unittest
from pathlib import Path
from unittest.mock import patch
from faststart import package

class FaststartTests(unittest.TestCase):
    def test_missing_input_raises(self):
        with patch("faststart.subprocess.run", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                package(Path("missing.mp4"), Path("output.mp4"))
    def test_atom_order_validation(self):
        with patch("faststart.subprocess.run"):
            with patch("pathlib.Path.read_bytes", return_value=b"ftyp-moov-mdat"):
                self.assertEqual(package(Path("input.mp4"),Path("output.mp4")),Path("output.mp4"))
    def test_invalid_atom_order_rejected(self):
        with patch("faststart.subprocess.run"):
            with patch("pathlib.Path.read_bytes", return_value=b"ftyp-mdat-moov"):
                with self.assertRaises(ValueError):
                    package(Path("input.mp4"),Path("output.mp4"))
if __name__ == "__main__": unittest.main()
