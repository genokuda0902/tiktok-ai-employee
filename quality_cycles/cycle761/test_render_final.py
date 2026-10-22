import importlib.util
import pathlib
import unittest

PATH = pathlib.Path(__file__).with_name('render_final.py')
spec = importlib.util.spec_from_file_location('cycle761_render', PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class RenderTests(unittest.TestCase):
    def test_invalid_order(self):
        with self.assertRaises(ValueError):
            mod.render('unused.mp4', 'a.png', 'b.png', 'out.mp4', 3, 2, 4)

    def test_invalid_start(self):
        with self.assertRaises(ValueError):
            mod.render('unused.mp4', 'a.png', 'b.png', 'out.mp4', -1, 2, 4)

    def test_entry_point_exists(self):
        self.assertTrue(callable(mod.render))

if __name__ == '__main__':
    unittest.main()
