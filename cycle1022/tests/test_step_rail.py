import importlib.util
from pathlib import Path
import tempfile
import unittest

SRC=Path(__file__).resolve().parents[1]/'source'/'step_rail_audio_audit.py'
spec=importlib.util.spec_from_file_location('rail',SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class RailTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
    def test_valid_srt(self):
        cues=m.parse_srt(SRC.parents[1]/'fixtures'/'captions.srt')
        self.assertEqual(len(cues),8)
        self.assertAlmostEqual(cues[-1]['end'],23.033)
    def test_reject_overlapping_cues(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.srt';p.write_text('1\n00:00:00,000 --> 00:00:01,000\na\n\n2\n00:00:00,900 --> 00:00:02,000\nb\n')
            with self.assertRaises(ValueError):m.parse_srt(p)
    def test_reject_empty_cue(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.srt';p.write_text('1\n00:00:00,000 --> 00:00:01,000\n\n')
            with self.assertRaises(ValueError):m.parse_srt(p)
    def test_rail_has_eight_distinct_beats(self):
        s=m.rail_filter(m.parse_srt(SRC.parents[1]/'fixtures'/'captions.srt'),'ai_work')
        self.assertEqual(s.count('color=white@0.85'),8)
        self.assertIn('gte(t,20.300)',s)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):m.rail_filter([{'start':0,'end':1}], 'unknown')
    def test_requires_review_gate(self):
        with self.assertRaises(ValueError):m.render('a','b','c','d','ai_work',False)

if __name__=='__main__':unittest.main()
