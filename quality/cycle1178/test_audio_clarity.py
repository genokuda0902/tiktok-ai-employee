import tempfile
import unittest
from pathlib import Path
from quality.cycle1178.audio_clarity import FILTER, build

class AudioClarityTest(unittest.TestCase):
    def test_safe_filter(self):
        self.assertIn("highpass=f=80", FILTER)
        self.assertIn("TP=-1.5", FILTER)
    def test_missing_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                build(Path(d)/"missing.mp4", Path(d)/"out.mp4")
    def test_source_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"in.mp4";p.write_bytes(b"x")
            with self.assertRaises(ValueError):
                build(p,p)
if __name__=="__main__": unittest.main()
