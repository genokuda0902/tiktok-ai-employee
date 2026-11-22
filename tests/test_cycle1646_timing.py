import unittest
from quality.cycle1646_timing import Scene, validate_scenes
class TimingTests(unittest.TestCase):
    def test_timeline(self):
        x=validate_scenes([Scene(3,'A','字幕A'),Scene(4,'B','字幕B')]); self.assertEqual(x['timeline'][1]['start'],3);self.assertEqual(x['duration'],7)
    def test_fail_closed(self):
        self.assertFalse(validate_scenes([Scene(2,'A','字幕')])['posting_allowed'])
    def test_invalid(self):
        with self.assertRaises(ValueError):validate_scenes([Scene(0,'A','字幕')])
if __name__=='__main__':unittest.main()
