import importlib.util
import unittest
from pathlib import Path

FILE=Path(__file__).resolve().parents[1]/'code'/'shadow_lift.py'
spec=importlib.util.spec_from_file_location('shadow_lift',FILE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ShadowLiftTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(mod.GENRES),10)
        self.assertEqual(len(set(mod.GENRES)),10)
    def test_graph_for_each_genre(self):
        for genre in mod.GENRES:
            with self.subTest(genre=genre):
                g=mod.filtergraph(genre)
                self.assertIn('crop=1080:1240:0:150',g)
                self.assertIn('overlay=0:150',g)
                self.assertIn('0.85/0.85 1/1',g)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):
            mod.filtergraph('unknown')
    def test_header_and_caption_safe_zone(self):
        top,height=150,1240
        self.assertGreaterEqual(top,130)
        self.assertLess(top+height,1450)
    def test_conservative_lift(self):
        for p in mod.PRESETS.values():
            self.assertTrue(0.15<p['shadow']<0.30)
            self.assertTrue(0.50<p['midtone']<0.60)

if __name__=='__main__':
    unittest.main()
