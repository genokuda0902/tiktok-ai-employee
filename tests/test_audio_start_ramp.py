import unittest
from pathlib import Path
from tools.audio_start_ramp import render

class TestRamp(unittest.TestCase):
    def test_invalid_duration(self):
        for duration in (0, 0.8):
            with self.assertRaises(ValueError):
                render(Path("x"), Path("y"), duration)
