"""Cycle1019 safety and reusable-genre tests."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_focus import PALETTES,SIZE,BEFORE,AFTER,validate,overlay,timings,filtergraph

class FocusTests(unittest.TestCase):
    def test_ten_unique_genres(self):
        self.assertEqual(len(PALETTES),10)
        self.assertEqual(len(set(PALETTES)),10)
    def test_all_color_codes(self):
        for pair in PALETTES.values():
            for color in pair:
                self.assertEqual(len(color),7)
                bytes.fromhex(color[1:])
    def test_safe_rectangles(self):
        validate(BEFORE);validate(AFTER)
        self.assertLess(AFTER[3],int(SIZE[1]*.68))
    def test_reject_caption_overlap(self):
        with self.assertRaises(ValueError):
            validate((0,1300,800,1600))
    def test_timing_order(self):
        b,a,fade=timings()
        self.assertLess(b[1],a[0])
        self.assertGreater(fade,0)
    def test_short_scene_rejected(self):
        with self.assertRaises(ValueError):timings(0,.5)
    def test_filter_keeps_source_video(self):
        f=filtergraph()
        self.assertIn('[0:v][1f]overlay',f)
        self.assertIn('format=yuv420p[v]',f)
    def test_transparency_protects_captions(self):
        with TemporaryDirectory() as d:
            path=Path(d)/'overlay.png'
            overlay(path,AFTER,'#20D8D3')
            im=Image.open(path)
            self.assertEqual(im.size,SIZE)
            self.assertEqual(im.getpixel((100,1450))[3],0)
            self.assertGreater(im.getpixel((73,1000))[3],100)
    def test_fades_both_layers(self):
        self.assertEqual(filtergraph().count('alpha=1'),4)

if __name__=='__main__':unittest.main()
