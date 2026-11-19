import unittest
from pathlib import Path
from unittest.mock import patch
from src.review_finish import finish_review

class TestFinish(unittest.TestCase):
    def test_reject_fps(self):
        with self.assertRaises(ValueError):
            finish_review(Path("missing"), Path("out.mp4"), 60)
    def test_reject_missing_source(self):
        with self.assertRaises(ValueError):
            finish_review(Path("missing"), Path("out.mp4"))
