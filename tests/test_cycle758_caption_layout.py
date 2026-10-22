"""Cycle758 layout tests. Run: python -m unittest discover -s tests."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'video_engine' / 'quality'))
from cycle758_layout import GENRES, CAPTIONS, parse_srt, make_ass, ass_time

TIMES = ['00:00:00,000','00:00:03,200','00:00:06,500',
         '00:00:09,800','00:00:12,800','00:00:16,433',
         '00:00:20,133','00:00:24,300','00:00:27,300']
SRT = '\n\n'.join(
    f'{i+1}\n{TIMES[i]} --> {TIMES[i+1]}\n架空'
    for i in range(8))

class TestCaptionLayout(unittest.TestCase):
    def test_eight_contiguous_cues(self):
        self.assertEqual(len(parse_srt(SRT)), 8)
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
    def test_genre_rendering(self):
        for name in GENRES:
            self.assertEqual(make_ass(parse_srt(SRT), name).count('Dialogue:'), 8)
    def test_short_captions(self):
        self.assertTrue(all(len(x) <= 20 for x in CAPTIONS))
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            parse_srt(SRT.replace('00:00:03,200 -->', '00:00:03,300 -->'))
    def test_bad_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            parse_srt(SRT.replace('00:00:00,000', 'bad'))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):
            make_ass(parse_srt(SRT), 'unknown')
    def test_rounding(self):
        self.assertEqual(ass_time(16433), '0:00:16.43')

if __name__ == '__main__':
    unittest.main()
