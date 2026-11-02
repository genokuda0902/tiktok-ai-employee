import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('chapter_progress', Path(__file__).resolve().parents[1] / 'code' / 'chapter_progress.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class ProgressTests(unittest.TestCase):
    def test_genre_count(self): self.assertEqual(len(mod.GENRE_ACCENTS), 10)
    def test_default_eight_scenes(self): self.assertEqual(len(mod.DEFAULT_SCENE_STARTS), 8)
    def test_geometry_safe_area(self):
        for n in range(4, 17):
            segments = mod.segment_geometry(n)
            self.assertEqual(len(segments), n)
            self.assertTrue(all(128 <= y <= 175 and x+w <= 930 for x,y,w,h in segments))
    def test_intro_has_no_active_rail(self):
        graph = mod.filter_graph((10, 20, 30, 40), 50)
        self.assertIn('between(n\\,10\\,19)', graph)
        self.assertNotIn('between(n\\,0', graph)
    def test_completed_step_latches(self):
        graph = mod.filter_graph((10, 20, 30, 40), 50)
        self.assertIn('gte(n\\,20)', graph)
    def test_last_scene_includes_final_frame(self):
        self.assertIn('between(n\\,40\\,49)', mod.filter_graph((10,20,30,40),50))
    def test_invalid_scene_order(self):
        with self.assertRaises(ValueError): mod.validate_scene_starts((10,30,20,40), 50)
    def test_scene_outside(self):
        with self.assertRaises(ValueError): mod.validate_scene_starts((10,20,30,50), 50)
    def test_unsupported_genre_accent(self):
        with self.assertRaises(ValueError): mod.filter_graph((10,20,30,40),50,'ffffff')
    def test_safe_area_reject(self):
        with self.assertRaises(ValueError): mod.segment_geometry(8,y=200)

if __name__ == '__main__': unittest.main()
