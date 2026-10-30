import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'code'))
sys.path.insert(0, str(ROOT/'tools'/'quality'))
from cycle1007_accessible_review import (
    Cue, CHAPTERS, GENRES, CUT_FRAMES, TEXTS, default_cues, ffmetadata,
    srt_text, stamp, validate_cues, mux)

class AccessibleReviewTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_eight_scenes(self):
        self.assertEqual(len(default_cues()),8)
        self.assertEqual(len(CHAPTERS),8)
        self.assertEqual(len(TEXTS),8)
        self.assertEqual(CUT_FRAMES[-1],691)
    def test_cue_validation(self):
        validate_cues(default_cues(),23.033333)
    def test_no_overlap(self):
        cues=(Cue(0,.8,'あ','a'),Cue(.7,1.2,'い','b'))
        with self.assertRaises(ValueError): validate_cues(cues,2)
    def test_duration_reject(self):
        with self.assertRaises(ValueError): validate_cues((Cue(.1,2.1,'あ','a'),),2)
    def test_blank_reject(self):
        with self.assertRaises(ValueError): validate_cues((Cue(.1,.9,'','a'),),2)
    def test_time_format(self):
        self.assertEqual(stamp(1.234),'00:00:01,234')
        self.assertEqual(stamp(61.001),'00:01:01,001')
    def test_srt_japanese(self):
        srt=srt_text(default_cues())
        self.assertEqual(srt.count(' --> '),8)
        self.assertIn('テンプレート',srt)
        self.assertIn('00:00:00,100',srt)
    def test_chapter_metadata(self):
        txt=ffmetadata(default_cues(),23.033333)
        self.assertEqual(txt.count('[CHAPTER]'),8)
        self.assertIn('TIMEBASE=1/1000',txt)
        self.assertIn('END=23033',txt)
    def test_no_custom_cues_production(self):
        with self.assertRaises(FileNotFoundError): mux(Path('/nonexistent.mp4'),Path('/tmp/none.mp4'))
    def test_fail_closed_unknown_genre(self):
        with self.assertRaises(ValueError): mux(Path('/nonexistent.mp4'),Path('/tmp/none.mp4'),genre='unknown')
    def test_fail_closed_other_genre(self):
        with self.assertRaises(ValueError): mux(Path('/nonexistent.mp4'),Path('/tmp/none.mp4'),genre='travel')

if __name__=='__main__': unittest.main()
