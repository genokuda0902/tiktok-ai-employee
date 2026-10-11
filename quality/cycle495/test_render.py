import unittest
from render_cycle495 import DATA, SCENES, SIZE, FPS

class RenderQualityTests(unittest.TestCase):
    def test_vertical(self):
        self.assertEqual(SIZE, (1080, 1920))
    def test_fps(self):
        self.assertEqual(FPS, 30)
    def test_duration(self):
        self.assertEqual(sum(s[3] for s in SCENES), 20)
    def test_scene_count(self):
        self.assertEqual(len(SCENES), 8)
    def test_example_data(self):
        self.assertEqual(sum(DATA), 720)

if __name__ == '__main__':
    unittest.main()
