import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).with_name("chapter_ticks.py")
spec = importlib.util.spec_from_file_location("chapter_ticks", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestChapterTicks(unittest.TestCase):
    def test_positions(self):
        f = module.chapter_filter()
        self.assertIn("x=270:", f)
        self.assertIn("x=540:", f)
        self.assertIn("x=810:", f)
        self.assertEqual(f.count("drawbox="), 3)
    def test_other_genre_geometry(self):
        self.assertEqual(module.chapter_filter(1000, 2).count("drawbox="), 1)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            module.chapter_filter(chapters=1)

if __name__ == "__main__":
    unittest.main()
