import unittest
from src.quality.audio_silence_gate import parse_silence, inspect
class SilenceTests(unittest.TestCase):
    def test_interval(self):
        log = '[silencedetect] silence_start: 1.2\n[silencedetect] silence_end: 2.1 | silence_duration: 0.9'
        self.assertEqual(parse_silence(log), [(1.2,2.1,0.9)])
    def test_empty(self):
        self.assertEqual(parse_silence('no silence'), [])
    def test_missing(self):
        with self.assertRaises(FileNotFoundError): inspect('/missing/none.mp4')
if __name__ == '__main__': unittest.main()
