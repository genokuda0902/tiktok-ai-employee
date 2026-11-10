import unittest
from pathlib import Path
from quality.cycle1345_render import render

class ReviewRenderTests(unittest.TestCase):
    def test_output_exists(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)/"review.mp4"
            render(output)
            self.assertGreater(output.stat().st_size, 1000)
