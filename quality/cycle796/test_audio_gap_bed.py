import json
import math
import tempfile
import unittest
from pathlib import Path
from audio_gap_bed import GENRES, clamp, smoothstep, gap_envelope, make_original_bed, render

class AudioGapBedTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertIn('AI・仕事効率化',GENRES)
        self.assertIn('商品比較・暮らし',GENRES)
    def test_gain_envelope_away_from_gap(self):
        self.assertEqual(gap_envelope(0,[[2,3]]),0)
    def test_gain_envelope_inside_gap(self):
        self.assertGreater(gap_envelope(2.5,[[2,3]]),.95)
    def test_gain_envelope_soft_edge(self):
        self.assertEqual(gap_envelope(2.001,[[2,3]]),0)
        self.assertEqual(gap_envelope(2.999,[[2,3]]),0)
    def test_smoothstep_bounded(self):
        self.assertEqual(smoothstep(-5),0)
        self.assertEqual(smoothstep(5),1)
    def test_make_bed_has_exact_samples(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bed.wav'
            m=make_original_bed(path,1.0,[[.2,.8]],sample_rate=8000)
            self.assertEqual(m['samples'],8000)
            self.assertGreater(path.stat().st_size,16000)
    def test_no_excess_gain(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_original_bed(Path(tmp)/'bed.wav',1,[],gap_gain=.5)
    def test_refuse_publishing(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'config.json'
            p.write_text(json.dumps({'genre':GENRES[0],'genres':GENRES,'mode':'publish',
                'rights_reviewed':False,'employee_approved':False,'publication_approved':True}),encoding='utf8')
            with self.assertRaisesRegex(ValueError,'REVIEW ONLY'):
                render(p,'nonexistent.mp4',Path(tmp)/'out_REVIEW_ONLY.mp4',Path(tmp)/'qa.json',Path(tmp)/'bed.wav')
    def test_refuse_wrong_genre_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'config.json'
            p.write_text(json.dumps({'genre':'random','genres':['random']}),encoding='utf8')
            with self.assertRaisesRegex(ValueError,'genre'):
                render(p,'nonexistent.mp4',Path(tmp)/'out_REVIEW_ONLY.mp4',Path(tmp)/'qa.json',Path(tmp)/'bed.wav')
    def test_clamp(self):
        self.assertEqual(clamp(3),1)
        self.assertEqual(clamp(-1),0)

if __name__=='__main__':unittest.main()
