import unittest
from unittest.mock import patch
from progress_overlay import add_progress
class TestProgress(unittest.TestCase):
    def test_rejects_zero_duration(self):
        with self.assertRaises(ValueError): add_progress("a","b",0)
    @patch("progress_overlay.subprocess.run")
    def test_preserves_audio(self, run):
        add_progress("a","b",23)
        self.assertIn("copy",run.call_args.args[0])
