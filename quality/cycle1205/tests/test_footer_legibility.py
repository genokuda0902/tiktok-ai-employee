import importlib.util
from pathlib import Path
import unittest

mod_path = Path(__file__).resolve().parents[1] / 'footer_legibility.py'
spec = importlib.util.spec_from_file_location('footer_legibility', mod_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FooterTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(module.GENRE_PROFILES), 10)
    def test_default_roi(self):
        self.assertEqual(module.validate_roi(module.ROI), module.ROI)
    def test_roi_rejects_subtitle_overlap(self):
        with self.assertRaises(ValueError):
            module.validate_roi((64, 1400, 952, 144))
    def test_roi_rejects_right_ui(self):
        with self.assertRaises(ValueError):
            module.validate_roi((64, 1730, 1020, 144))
    def test_roi_rejects_odd(self):
        with self.assertRaises(ValueError):
            module.validate_roi((65, 1730, 952, 144))
    def test_filter_copies_base(self):
        f = module.build_filter()
        self.assertIn('split=2', f)
        self.assertIn('overlay=', f)
    def test_bright_pixels_only(self):
        f = module.build_filter()
        self.assertIn('gte(val,58)', f)
        self.assertIn('min(235,val*1.250)', f)
    def test_profile_bounds(self):
        for t, g in module.GENRE_PROFILES.values():
            module.build_filter(module.ROI, t, g)
    def test_reject_gain(self):
        with self.assertRaises(ValueError):
            module.build_filter(module.ROI, 58, 1.8)
    def test_reject_source_shape(self):
        with self.assertRaises(ValueError):
            module.validate_source({'streams': [
                {'codec_type':'video','codec_name':'h264','width':720,
                 'height':1280,'r_frame_rate':'30/1'},
                {'codec_type':'audio','codec_name':'aac'}]})

if __name__ == '__main__':
    unittest.main()
