import unittest
from pathlib import Path
from unittest.mock import patch
from subtitle_guard import render

class TestSubtitleGuard(unittest.TestCase):
    def test_invalid_zone(self):
        with self.assertRaises(ValueError): render(Path("a"),Path("b"),start_y=1900,height=100)
    def test_invalid_opacity(self):
        with self.assertRaises(ValueError): render(Path("a"),Path("b"),opacity=.9)
    @patch("subtitle_guard.subprocess.run")
    def test_audio_copy(self, mock):
        render(Path("a"),Path("b"))
        self.assertIn("copy",mock.call_args.args[0])
