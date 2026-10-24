"""Cycle825 shared visual component / CI regression tests (offline)."""
import importlib.util
import pathlib
import unittest
from PIL import Image, ImageChops

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rail',HERE/'action_rail.py')
rail=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rail)

class TestSharedRail(unittest.TestCase):
    def test_ten_genre_palettes(self):
        self.assertEqual(len(rail.PALETTES),10)
    def test_eight_distinct_actions(self):
        self.assertEqual(len(rail.ACTIONS),8)
        self.assertEqual(len(set(rail.ACTIONS)),8)
    def test_rail_draws_progress_and_action(self):
        im=Image.new('RGB',(1080,1920),'#FFFFFF')
        a=rail.apply_action_rail(im,0)
        b=rail.apply_action_rail(im,7)
        self.assertEqual(a.size,(1080,1920))
        self.assertIsNotNone(ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox())
        self.assertEqual(a.getpixel((0,1900))[:3],(13,36,52))
    def test_invalid_genre_and_scene_fail_closed(self):
        with self.assertRaises(ValueError):
            rail.apply_action_rail(Image.new('RGB',(1080,1920)),8)
        with self.assertRaises(ValueError):
            rail.apply_action_rail(Image.new('RGB',(1080,1920)),0,'unknown')
    def test_no_upload_code(self):
        source=(HERE/'action_rail.py').read_text()
        self.assertNotIn('requests.post(',source)
        self.assertNotIn('tiktok.com/upload',source)

if __name__=='__main__':
    unittest.main()
