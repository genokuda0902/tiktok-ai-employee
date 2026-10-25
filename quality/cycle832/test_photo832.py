"""cycle832: image prominence and caption-safe layout regression tests (10 genres)."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image
source=Path(__file__).resolve().parents[1]/'cycle831'/'scene831.py'
spec=importlib.util.spec_from_file_location('scene831_for832',source)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class PhotoFirst832(unittest.TestCase):
    def test_image_occupies_nearly_half_the_frame(self):
        x0,y0,x1,y1=m.PHOTO_BOX
        self.assertGreaterEqual((x1-x0)*(y1-y0)/(m.W*m.H),0.47)
        self.assertGreater(y1,1300)
    def test_caption_and_photo_do_not_overlap(self):
        self.assertLessEqual(m.PHOTO_BOX[3]+25,m.CAPTION_SAFE_TOP)
        self.assertLess(m.CAPTION_SAFE_TOP,1650)
    def test_right_side_is_photo_not_step_sidebar(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'photo.png'
            m.slide(0,Image.new('RGB',(600,900),(230,25,30)),path,'ai_work')
            with Image.open(path) as im:
                r,g,b=im.getpixel((905,800))
                self.assertGreater(r,160)
                self.assertLess(g,90)
                self.assertLess(b,90)
    def test_ten_genres_same_safe_geometry(self):
        with tempfile.TemporaryDirectory() as td:
            for genre in m.COLORS:
                path=Path(td)/(genre+'.png')
                m.slide(0,Image.new('RGB',(500,800),(230,25,30)),path,genre)
                with Image.open(path) as im:
                    self.assertEqual(im.size,(1080,1920))
                    self.assertGreater(im.getpixel((905,800))[0],160)
    def test_invalid_scene_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                m.slide(8,Image.new('RGB',(400,600)),Path(td)/'x.png')
if __name__=='__main__':unittest.main()
