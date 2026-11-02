import importlib.util
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('content_detail',ROOT/'code'/'content_detail.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestContentDetail(unittest.TestCase):
    def test_genre_count(self): self.assertEqual(len(m.GENRE_PROFILES),10)
    def test_genre_strength_range(self):
        for s in m.GENRE_PROFILES.values(): self.assertTrue(0.15<=s<=0.45)
    def test_roi_valid(self): self.assertEqual(m.validate_roi(m.DEFAULT_ROI),m.DEFAULT_ROI)
    def test_roi_excludes_subtitles(self):
        for r in [(72,390,936,1120),(72,1320,936,400),(10,390,936,860),(72,390,1000,860)]:
            with self.assertRaises(ValueError):m.validate_roi(r)
    def test_odd_roi_rejected(self):
        with self.assertRaises(ValueError):m.validate_roi((73,390,936,860))
    def test_filter_has_safe_overlay(self):
        f=m.build_filter(m.DEFAULT_ROI,0.3)
        self.assertIn('cas=strength=0.300',f)
        self.assertIn('overlay=72:390',f)
    def test_strength_bounds(self):
        for s in [-1,0.5]:
            with self.assertRaises(ValueError):m.build_filter(m.DEFAULT_ROI,s)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):m.render('fake','fake','unknown')
    def test_validate_video(self):
        info={'streams':[{'codec_type':'video','width':1080,'height':1920,'r_frame_rate':'30/1','nb_frames':'675'},
                         {'codec_type':'audio','codec_name':'aac'}], 'format':{'duration':'22.5'}}
        self.assertEqual(m.validate_source(info),675)
    def test_reject_nonportrait(self):
        info={'streams':[{'codec_type':'video','width':1920,'height':1080,'r_frame_rate':'30/1'},
                         {'codec_type':'audio','codec_name':'aac'}], 'format':{'duration':'22.5'}}
        with self.assertRaises(ValueError):m.validate_source(info)

if __name__=='__main__':unittest.main()
