import unittest
from pathlib import Path

class Tests(unittest.TestCase):
    def test_filter(self):
        source=Path("tools/audio_presence_cycle1905.py").read_text()
        self.assertIn("g=1.5",source)
        self.assertIn("'copy'",source)

if __name__=="__main__": unittest.main()
