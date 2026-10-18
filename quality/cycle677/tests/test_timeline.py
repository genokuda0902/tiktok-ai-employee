import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from voice_timeline_gate import validate

class TimelineTest(unittest.TestCase):
    def test_missing(self):
        with self.assertRaises(ValueError):
            validate([])
    def test_valid(self):
        self.assertTrue(validate([{'start':0,'end':2,'text':'日本語'}]))
