import unittest
from pathlib import Path
from unittest.mock import patch
from stabilize_caption import render

class TestCaption(unittest.TestCase):
    def test_invalid_top(self):
        with self.assertRaises(ValueError):
            render(Path("a"), Path("b"), Path("/tmp/out"), 1920)

    @patch("stabilize_caption.subprocess.run")
    def test_audio_copied(self, run):
        render(Path("a"), Path("b"), Path("/tmp/out"))
        args = run.call_args.args[0]
        self.assertIn("copy", args)
        self.assertIn("0:a:0", args)

if __name__ == "__main__":
    unittest.main()
