import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import result_first as m

class TestResultFirst(unittest.TestCase):
    def test_ten_genres_declared(self):
        self.assertEqual(len(m.GENRE_PALETTES),10)
    def test_unknown_genre_blocked(self):
        with self.assertRaises(ValueError):m.check_genre('unknown',True)
    def test_other_genre_real_render_blocked(self):
        with self.assertRaises(ValueError):m.check_genre('food',False)
    def test_ai_work_real_allowed(self):
        m.check_genre('ai_work',False)
    def test_other_genre_synthetic_allowed(self):
        m.check_genre('food',True)
    def test_overlay_safe_and_source_derived(self):
        with tempfile.TemporaryDirectory() as t:
            frame=Image.new('RGB',(1080,1920),'#182635')
            d=ImageDraw.Draw(frame);d.rectangle((108,318,805,1130),fill='white')
            frame.save(Path(t)/'source.png')
            out=Path(t)/'hook.png'
            m.build_overlay(Path(t)/'source.png',out,synthetic=True)
            im=Image.open(out)
            self.assertEqual(im.size,(1080,1920))
            self.assertTrue(im.getbbox()[3]<m.SAFE_TOP)
            self.assertEqual(im.getpixel((300,600))[:3],(255,255,255))
            self.assertEqual(im.getpixel((500,1500))[3],0)
    def test_bad_frame_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'wrong.png';Image.new('RGB',(200,300)).save(f)
            with self.assertRaises(ValueError):
                m.build_overlay(f,Path(t)/'x.png',synthetic=True)
    def test_no_fake_synthetic_preview(self):
        with self.assertRaises(ValueError):
            m.render('unused.mp4','unused2.mp4',synthetic=True)
    def test_crop_within_safe_area(self):
        self.assertTrue(m.PREVIEW_CROP[3]<m.SAFE_TOP)
if __name__=='__main__': unittest.main()
