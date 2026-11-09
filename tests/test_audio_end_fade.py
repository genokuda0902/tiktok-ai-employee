import unittest
from pathlib import Path
from tools.audio_end_fade import render
class FadeTest(unittest.TestCase):
    def test_rejects_too_long_fade(self):
        import unittest.mock as mock
        with mock.patch("tools.audio_end_fade.duration",return_value=0.2):
            with self.assertRaises(AssertionError):
                render(Path("input.mp4"),Path("output.mp4"),fade=0.55)
