import importlib.util
import unittest
from pathlib import Path

p=Path(__file__).resolve().parents[1]/'ui_focus_lens.py'
spec=importlib.util.spec_from_file_location('lens',p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class FocusTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.PALETTES),10)
        for k in m.PALETTES:
            self.assertIn('[v]',m.graph(k))
    def test_cues_nonoverlap(self):
        for i,(start,end,roi) in enumerate(m.CUES):
            self.assertLess(start,end)
            self.assertLess(roi[1]+roi[3],m.CAPTION_SAFE_Y)
            if i:self.assertLessEqual(m.CUES[i-1][1],start)
    def test_lens_outside_caption(self):
        self.assertLess(m.ZOOM_Y+m.ZOOM_H,m.CAPTION_SAFE_Y)
    def test_actual_video_crop_only(self):
        g=m.graph('ai')
        self.assertEqual(g.count('crop='),3)
        self.assertEqual(g.count('overlay='),3)
        self.assertNotIn('drawtext',g)
    def test_reject_bad_genre(self):
        with self.assertRaises(KeyError):m.graph('unknown')
    def test_fail_closed(self):
        class Dummy:
            pass
        with self.assertRaises(ValueError):m.validate({},'/nonexistent')

if __name__=='__main__':unittest.main()
