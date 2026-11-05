import unittest
from pathlib import Path
from render_timed_story import render

class TimedStoryTests(unittest.TestCase):
    def test_missing_input_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            render(Path("/nonexistent/never.mp4"),Path("/tmp/never.mp4"))
    def test_review_label_in_source(self):
        self.assertIn("REVIEW ONLY",Path(__file__).with_name("render_timed_story.py").read_text())
if __name__=="__main__": unittest.main()
