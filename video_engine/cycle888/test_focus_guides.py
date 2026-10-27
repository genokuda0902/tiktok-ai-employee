import tempfile,unittest
from pathlib import Path
from focus_guides import FOCUSES,GENRES,Focus,corners,timestamp,validate,write_ass

class FocusGuideTests(unittest.TestCase):
    def test_ten_unique_genres(self):self.assertEqual(len(set(GENRES)),10)
    def test_timing_valid(self):self.assertTrue(validate())
    def test_eight_events(self):self.assertEqual(len(FOCUSES),8)
    def test_caption_safe(self):self.assertLess(max(f.y+f.h for f in FOCUSES),1250)
    def test_header_safe(self):self.assertGreater(min(f.y for f in FOCUSES),300)
    def test_corner_eight_segments(self):self.assertEqual(corners(FOCUSES[0]).count('m '),8)
    def test_timestamp(self):self.assertEqual(timestamp(9.65),'0:00:09.65')
    def test_no_overlap(self):
        with self.assertRaises(ValueError):
            validate((Focus(.1,1,100,400,300,200,'a'),Focus(.8,2,100,400,300,200,'b')))
    def test_no_bottom_subtitle_overlay(self):
        with self.assertRaises(ValueError):validate((Focus(.1,1,100,1300,300,100,'bad'),))
    def test_no_header_overlay(self):
        with self.assertRaises(ValueError):validate((Focus(.1,1,100,100,300,100,'bad'),))
    def test_no_unknown_color(self):
        with self.assertRaises(ValueError):validate((Focus(.1,1,100,400,300,200,'bad','red'),))
    def test_no_end_beyond_duration(self):
        with self.assertRaises(ValueError):validate((Focus(22,25,100,400,300,200,'bad'),))
    def test_ass_contains_eight_events(self):
        with tempfile.TemporaryDirectory() as d:
            s=write_ass(Path(d)/'focus.ass').read_text()
            self.assertEqual(s.count('Dialogue:'),8)
            self.assertIn('\\fad(',s)
            self.assertIn('PlayResY: 1920',s)
    def test_no_posting_apis(self):
        import inspect,focus_guides
        s=inspect.getsource(focus_guides)
        self.assertNotIn('requests.post(',s)
        self.assertNotIn('tiktok.upload(',s)

if __name__=='__main__':unittest.main()
