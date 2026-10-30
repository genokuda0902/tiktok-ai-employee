import importlib.util
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'tools/quality/cycle1011_silence_safe_trim.py'
spec=importlib.util.spec_from_file_location('cycle1011',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class SafeTrimTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(set(m.GENRE_IDS)),10)
    def test_keep_speech_and_pause(self):
        cuts=m.plan_cuts([(1.0,1.5)],[],5)
        self.assertEqual(len(cuts),1)
        a,b=cuts[0];self.assertGreaterEqual(a-1,0.12);self.assertGreaterEqual(1.5-b,0.12)
        self.assertGreaterEqual(1.5-1-(b-a),0.30-1e-4)
    def test_short_pause_not_cut(self):self.assertFalse(m.plan_cuts([(1,1.35)],[],5))
    def test_chapter_guard(self):
        self.assertFalse(m.plan_cuts([(1.0,1.5)],[{'start_time':'1.25'}],5))
    def test_protect_opening_and_end(self):
        self.assertFalse(m.plan_cuts([(0.1,0.6),(4.5,4.95)],[],5))
    def test_mapping(self):
        c=[(1.0,1.1),(2.0,2.1)]
        self.assertAlmostEqual(m.map_time(2.5,c),2.3)
        self.assertAlmostEqual(m.map_time(1.05,c),1.0)
    def test_keep_segments(self):
        self.assertEqual(m.keep_segments(3,[(1,1.1),(2,2.1)]),[(0,1),(1.1,2),(2.1,3)])
    def test_srt_timing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.srt';b=Path(d)/'b.srt'
            a.write_text('1\n00:00:02,000 --> 00:00:03,000\n日本語\n')
            m.retime_srt(a,b,[(1,1.1)])
            self.assertIn('00:00:01,900 --> 00:00:02,900',b.read_text())
    def test_empty_cuts_not_claimed(self):self.assertEqual(m.plan_cuts([],[],5),[])

if __name__=='__main__':unittest.main()
