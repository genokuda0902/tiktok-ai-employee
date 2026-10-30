import importlib.util
from pathlib import Path
import tempfile
import unittest

PATH=Path(__file__).resolve().parents[1]/'tools/quality/cycle993_safe_microzoom.py'
spec=importlib.util.spec_from_file_location('safe_microzoom',PATH)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SafeMicrozoomTest(unittest.TestCase):
    def test_ten_genre_profiles(self):
        self.assertEqual(len(mod.GENRE_ZOOM),10)
        for name,v in mod.GENRE_ZOOM.items():
            with self.subTest(name=name): self.assertTrue(0 < v <= .04)
    def test_scene_seams_and_midpoints(self):
        for scene in range(7):
            self.assertAlmostEqual(mod.eased_zoom(scene*87),1.0,places=8)
            self.assertAlmostEqual(mod.eased_zoom(scene*87+86),1.0,places=8)
            self.assertGreater(mod.eased_zoom(scene*87+43),1.017)
    def test_mask_edges_are_zero_center_opaque(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'mask.png'
            mod.feather_mask(path,90,85,feather=8)
            from PIL import Image
            with Image.open(path) as m:
                self.assertEqual(m.getpixel((0,40)),0)
                self.assertEqual(m.getpixel((45,0)),0)
                self.assertEqual(m.getpixel((45,40)),255)
    def test_graph_keeps_subtitle_outside_roi(self):
        graph=mod.filter_graph(90,300,900,850,87,.018)
        self.assertIn('crop=900:850:90:300',graph)
        self.assertIn('overlay=90:300',graph)
        self.assertIn('mod(on,87)',graph)
        self.assertNotIn('scale=1080:1920',graph)
    def test_invalid_settings(self):
        for kwargs in ({'scene_frames':2},{'strength':.08}):
            with self.assertRaises(ValueError): mod.eased_zoom(10,**kwargs)
        with self.assertRaises(ValueError): mod.feather_mask(Path('unused'),10,10,6)

if __name__=='__main__': unittest.main()
