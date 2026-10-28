import sys, unittest
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from depth_focus import CANVAS, FRAME_COUNT, GENRES, process_frame, focus_strength

class DepthFocusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.im = Image.new('RGB', CANVAS, (32, 64, 90))
        d = ImageDraw.Draw(cls.im)
        for x in range(0,1080,18):
            d.line((x,270,x,1250),fill=(210,180,120),width=5)
        d.rectangle((145,390,795,1080),fill=(245,244,234))
        for y in range(450,1050,60):
            d.line((160,y,750,y),fill=(20,20,20),width=5)
    def test_all_genres_supported(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            with self.subTest(genre=genre):
                self.assertEqual(process_frame(self.im,20,genre).size,CANVAS)
    def test_invalid_genre_fails_closed(self):
        with self.assertRaises(ValueError):process_frame(self.im,20,'unsafe')
    def test_dimensions_fail_closed(self):
        with self.assertRaises(ValueError):process_frame(Image.new('RGB',(10,10)),20)
    def test_index_bounds(self):
        with self.assertRaises(ValueError):focus_strength(-1)
        with self.assertRaises(ValueError):focus_strength(FRAME_COUNT)
    def test_first_frame_unchanged(self):
        self.assertIsNone(ImageChops.difference(self.im,process_frame(self.im,0)).getbbox())
    def test_unchanged_header_and_caption_band(self):
        out=process_frame(self.im,30)
        for region in [(0,0,1080,270),(0,1250,1080,1920)]:
            self.assertIsNone(ImageChops.difference(self.im.crop(region),out.crop(region)).getbbox())
    def test_japanese_page_inner_area_unchanged(self):
        out=process_frame(self.im,30)
        self.assertIsNone(ImageChops.difference(self.im.crop((180,425,730,1000)),out.crop((180,425,730,1000))).getbbox())
    def test_scene_badges_and_footnote_protected(self):
        out=process_frame(self.im,30)
        for region in [(0,270,1080,330),(100,1030,780,1120)]:
            self.assertIsNone(ImageChops.difference(self.im.crop(region),out.crop(region)).getbbox())
    def test_background_changes(self):
        out=process_frame(self.im,30)
        self.assertIsNotNone(ImageChops.difference(self.im.crop((0,350,75,1150)),out.crop((0,350,75,1150))).getbbox())
    def test_strength_ramps_and_holds(self):
        self.assertEqual(focus_strength(0),0)
        self.assertGreater(focus_strength(10),focus_strength(5))
        self.assertEqual(focus_strength(20),1)
        self.assertEqual(focus_strength(86),1)
if __name__=='__main__':unittest.main()
