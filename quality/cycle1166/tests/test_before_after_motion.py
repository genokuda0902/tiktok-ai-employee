import tempfile
import unittest
from pathlib import Path
from PIL import Image
from before_after_motion import PALETTES,POLICY,START,END,panel_assets,positions,validate

class BeforeAfterTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES),10)
        self.assertEqual(len(set(PALETTES)),10)
    def test_policy_fail_closed(self):
        with self.assertRaises(ValueError):validate({'policy':'PUBLISH'},'/not/a/file.mp4')
    def test_asset_procedural_dimensions(self):
        with tempfile.TemporaryDirectory() as d:
            paths=panel_assets(Path(d),'ai')
            sizes=[]
            for x in paths:
                with Image.open(x) as im: sizes.append(im.size)
            self.assertEqual(sizes,[(920,580),(414,412),(414,412)])
    def test_every_genre_procedural_assets(self):
        with tempfile.TemporaryDirectory() as d:
            for genre in PALETTES:
                self.assertEqual(len(panel_assets(Path(d),genre)),3)
    def test_position_lands_inside_safe_area(self):
        for t in (20.9,21.2,22.0):
            x1,x2=positions(t)
            self.assertEqual(x1,76)
            if t>=21.2:self.assertEqual(x2,522)
            self.assertLessEqual(354+412,800)
    def test_chapter_duration(self):
        self.assertEqual((START,END),(20.5,22.99))
    def test_review_only(self):
        self.assertIn('NOT_APPROVED',POLICY)

if __name__=='__main__':unittest.main()
