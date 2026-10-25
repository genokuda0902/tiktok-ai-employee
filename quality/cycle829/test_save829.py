import importlib.util,unittest
from pathlib import Path
from PIL import ImageChops
spec=importlib.util.spec_from_file_location('save829',Path(__file__).with_name('save829.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestSave829(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        for g in m.GENRES:self.assertTrue(m.validate(g))
    def test_palette_complete(self):self.assertEqual(set(m.GENRES),set(m.PALETTES))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):m.validate('unknown')
    def test_reject_scene_shift(self):
        with self.assertRaises(ValueError):m.validate(start=18)
    def test_safe_caption_region(self):self.assertLess(m.Y+m.H,1200)
    def test_three_distinct_phases(self):
        frames=[m.frame(p) for p in (.12,.5,.94)]
        self.assertTrue(all(f.size==(952,648) for f in frames))
        self.assertTrue(all(ImageChops.difference(a,b).getbbox() is not None for a,b in zip(frames,frames[1:])))
    def test_ten_genre_render_samples(self):
        for g in m.GENRES:self.assertEqual(m.frame(.55,g).size,(952,648))
    def test_non_publication_text(self):
        self.assertIn('架空',m.NOTICE)
        self.assertNotIn('一瞬で', ''.join(m.PHASES))
    def test_progress_clamp(self):self.assertEqual(m.frame(-1).size,m.frame(2).size)
if __name__=='__main__':unittest.main()
