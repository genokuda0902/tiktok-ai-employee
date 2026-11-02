import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from slide_detail import GENRES,DEFAULT_ROI,validate_roi,ffmpeg_filter
class TestDetail(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_roi(self): self.assertEqual(validate_roi(DEFAULT_ROI),DEFAULT_ROI)
    def test_outside(self):
        with self.assertRaises(ValueError): validate_roi((100,1800,100,200))
    def test_subtitle_guard(self):
        with self.assertRaises(ValueError): validate_roi((64,900,952,600))
    def test_odd_coords(self):
        with self.assertRaises(ValueError): validate_roi((63,480,952,720))
    def test_too_high_amount(self):
        with self.assertRaises(ValueError): ffmpeg_filter(DEFAULT_ROI,1.1)
    def test_negative_amount(self):
        with self.assertRaises(ValueError): ffmpeg_filter(DEFAULT_ROI,-.1)
    def test_filter(self):
        s=ffmpeg_filter();self.assertIn('unsharp=5:5:0.60:5:5:0',s)
    def test_caption_protected(self): self.assertLessEqual(DEFAULT_ROI[1]+DEFAULT_ROI[3],1280)
    def test_genre_names(self): self.assertEqual(len(set(GENRES)),len(GENRES))
if __name__=='__main__': unittest.main()
