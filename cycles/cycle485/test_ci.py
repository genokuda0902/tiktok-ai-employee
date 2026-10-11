import unittest
from ci_build import TEXTS, render

class TestCycle485(unittest.TestCase):
    def test_scene_count(self):
        self.assertEqual(len(TEXTS), 6)

    def test_resolution(self):
        self.assertEqual(render(0, 0).size, (1080, 1920))

    def test_visual_change(self):
        self.assertNotEqual(render(0, 0).tobytes(), render(0, 3).tobytes())

if __name__ == '__main__':
    unittest.main()
