import importlib.util
from pathlib import Path
import unittest

CODE = Path(__file__).resolve().parents[1] / 'code' / 'clean_headers.py'
spec = importlib.util.spec_from_file_location('clean_headers', CODE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestCleanHeaders(unittest.TestCase):
    def test_10_genres(self):
        self.assertEqual(len(module.GENRE_ACCENTS), 10)
        self.assertEqual(len(set(module.GENRE_ACCENTS.values())), 10)
    def test_7_new_chapters(self):
        self.assertEqual(len(module.DEFAULT_SCENES), 7)
        self.assertEqual(module.DEFAULT_SCENES[0][0], 2.633)
        self.assertEqual(module.DEFAULT_SCENES[-1][1], 22.5)
    def test_valid_scenes(self):
        self.assertEqual(len(module.validate_scenes(module.DEFAULT_SCENES)), 7)
    def test_refuse_non_vertical(self):
        with self.assertRaises(ValueError): module.validate_scenes(module.DEFAULT_SCENES, 720, 1280)
    def test_refuse_overlap(self):
        with self.assertRaises(ValueError): module.validate_scenes([(1,3,'one'),(2,4,'two')])
    def test_refuse_long_title(self):
        with self.assertRaises(ValueError): module.validate_scenes([(1,2,'あ'*25)])
    def test_refuse_unknown_genre(self):
        with self.assertRaises(ValueError): module.filtergraph('unknown', fontfile=__file__)
    def test_refuse_missing_font(self):
        with self.assertRaises(FileNotFoundError): module.filtergraph(fontfile='/tmp/not-a-real-font-1031.ttf')
    def test_safe_header(self):
        x,y,w,h=module.HEADER_RECT
        self.assertLess(y+h, module.CAPTION_MIN_Y)
        self.assertLess(x+w, 1080)
    def test_graph_contains_7_titles(self):
        g=module.filtergraph(fontfile=__file__)
        for _,_,title in module.DEFAULT_SCENES:
            self.assertIn(title,g)
        self.assertIn('format=yuv420p',g)
    def test_preserves_first_scene(self):
        g=module.filtergraph(fontfile=__file__)
        self.assertNotIn('between(t,0.000,',g)

if __name__ == '__main__': unittest.main()
