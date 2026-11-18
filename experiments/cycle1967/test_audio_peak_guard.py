import unittest
from pathlib import Path
from audio_peak_guard import render
class TestPeakGuard(unittest.TestCase):
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError): render('/missing/file.mp4','/tmp/out.mp4')
    def test_filter_config(self):
        self.assertIn('TP=-1.5',Path(__file__).with_name('audio_peak_guard.py').read_text())
if __name__=='__main__': unittest.main()
