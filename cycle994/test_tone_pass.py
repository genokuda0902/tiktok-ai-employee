import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('tone_pass', Path(__file__).with_name('tone_pass.py'))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TonePassTests(unittest.TestCase):
    def test_ten_genres_conservative(self):
        self.assertEqual(len(mod.GENRE_GAMMA), 10)
        for g in mod.GENRE_GAMMA.values():
            self.assertTrue(1.0 <= g <= 1.25)

    def test_publication_gate(self):
        m = {'streams': [{'codec_type':'video','width':1080,'height':1920},
                         {'codec_type':'audio','sample_rate':'48000'}]}
        with self.assertRaises(ValueError): mod.validate(m,'ai_work',False)
        with self.assertRaises(ValueError): mod.validate(m,'unknown',True)
        self.assertTrue(mod.validate(m,'ai_work',True))

    def test_portrait_and_narration_required(self):
        for streams in ([{'codec_type':'video','width':720,'height':1280},
                         {'codec_type':'audio','sample_rate':'48000'}],
                        [{'codec_type':'video','width':1080,'height':1920}]):
            with self.assertRaises(ValueError): mod.validate({'streams':streams},'ai_work',True)

    def test_mask_protects_edges(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t)/'mask.png'
            mod.mask_image(path, 100, 80, 10)
            from PIL import Image
            with Image.open(path) as m:
                self.assertEqual(m.getpixel((0, 40)),0)
                self.assertEqual(m.getpixel((50, 0)),0)
                self.assertEqual(m.getpixel((50, 40)),255)
                self.assertGreater(m.getpixel((5, 40)),0)

    def test_roi_excludes_captions(self):
        x,y,w,h=mod.ROI
        self.assertGreaterEqual(y,200)
        self.assertLess(y+h,1450)
        self.assertLessEqual(x+w,1080)
        self.assertIn('alphamerge',mod.filtergraph(1.18))
        with self.assertRaises(ValueError): mod.filtergraph(1.5)

if __name__ == '__main__': unittest.main()
