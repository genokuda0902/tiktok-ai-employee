import importlib.util
import unittest
from pathlib import Path
from PIL import ImageChops

spec=importlib.util.spec_from_file_location('cinematic_cta',Path(__file__).with_name('cinematic_cta.py'))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class CTAQualityTest(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(m.GENRES),10)
        self.assertEqual(len(set(m.GENRES)),10)
        self.assertEqual(set(m.GENRES),set(m.PALETTES))
    def test_fail_closed_unknown_genre(self):
        with self.assertRaises(ValueError):m.make_base('unapproved genre')
    def test_safe_bounds(self):
        self.assertGreaterEqual(171,m.SAFE['left'])
        self.assertLessEqual(909,1080-m.SAFE['right'])
        self.assertGreaterEqual(165,m.SAFE['top'])
        self.assertLessEqual(1635,1920-m.SAFE['bottom'])
    def test_temporal_contract(self):
        self.assertEqual(m.FPS,30)
        self.assertAlmostEqual(m.CTA_END-m.CTA_START,3.0)
    def test_palette_no_untrusted_assets(self):
        self.assertEqual(len(m.PALETTES),10)
        for pair in m.PALETTES.values():
            for color in pair:
                self.assertEqual(len(color),7)
                self.assertTrue(color.startswith('#'))
                self.assertEqual(len(m._rgb(color)),3)
    def test_image_and_animation(self):
        base=m.make_base(m.GENRES[0]);self.assertEqual(base.size,(1080,1920))
        f0=m.frame(base,0.0,m.GENRES[0]);f1=m.frame(base,1.5,m.GENRES[0])
        self.assertEqual(f0.size,(1080,1920))
        self.assertIsNotNone(ImageChops.difference(f0,f1).getbbox())
    def test_time_rejected(self):
        base=m.make_base(m.GENRES[0])
        for t in (-.1,3.1):
            with self.assertRaises(ValueError):m.frame(base,t,m.GENRES[0])
    def test_static_original_art_only(self):
        source=Path(__file__).with_name('cinematic_cta.py').read_text()
        for banned in ('requests.get(', 'urllib.request', 'Image.open(', 'auto_post(', 'upload_to_tiktok('):
            self.assertNotIn(banned,source)

if __name__=='__main__':unittest.main()
