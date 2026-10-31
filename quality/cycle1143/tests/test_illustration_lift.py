import importlib.util
import pathlib
import tempfile
import unittest
from PIL import Image

MOD = pathlib.Path(__file__).resolve().parents[1]/'code'/'illustration_lift.py'
spec = importlib.util.spec_from_file_location('lift', MOD)
lift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lift)

class LiftTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(lift.PRESETS), 10)
        self.assertEqual(len(set(lift.PRESETS)),10)
    def test_all_presets_bounded(self):
        for p in lift.PRESETS.values():
            self.assertTrue(1 <= p['gamma'] <= 1.2)
            self.assertTrue(1 <= p['contrast'] <= 1.08)
            self.assertTrue(1 <= p['saturation'] <= 1.15)
            self.assertTrue(0 <= p['brightness'] <= .03)
    def test_top_protected(self):
        self.assertEqual(lift.alpha_at(200),0)
    def test_bottom_subtitles_protected(self):
        self.assertEqual(lift.alpha_at(1400),0)
    def test_center_active(self):
        self.assertEqual(lift.alpha_at(800),255)
    def test_edge_feather(self):
        self.assertEqual(lift.alpha_at(lift.Y_TOP),0)
        self.assertTrue(0 < lift.alpha_at(lift.Y_TOP+20) < 255)
        self.assertEqual(lift.alpha_at(lift.Y_BOTTOM-1),0)
    def test_invalid_bounds(self):
        with self.assertRaises(ValueError): lift.alpha_at(20,10,15,10)
    def test_mask_pixels(self):
        with tempfile.TemporaryDirectory() as t:
            p=lift.make_mask(pathlib.Path(t)/'mask.png',width=8)
            im=Image.open(p)
            self.assertEqual(im.size,(8,lift.Y_BOTTOM-lift.Y_TOP))
            self.assertEqual(im.getpixel((4,0)),0)
            self.assertEqual(im.getpixel((4,200)),255)
            self.assertEqual(im.getpixel((4,im.height-1)),0)
    def test_graph_contains_overlay(self):
        s=lift.filter_graph()
        self.assertIn('alphamerge',s)
        self.assertIn('format=yuv420p',s)
    def test_validation_rejects_nonvertical(self):
        with self.assertRaises(ValueError):
            lift.validate_source({'width':1920,'height':1080,'fps':'30/1',
                                  'audio_codec':'aac','sample_rate':48000})
    def test_validation_accepts_correct(self):
        lift.validate_source({'width':1080,'height':1920,'fps':'30/1',
                              'audio_codec':'aac','sample_rate':48000})

if __name__=='__main__': unittest.main()
