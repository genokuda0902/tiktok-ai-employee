import unittest
from frame_timing import frame_times, scene_at, cursor_visible

class FrameTimingTests(unittest.TestCase):
    def test_frame_count(self):
        self.assertEqual(len(frame_times(15, 10)), 150)
        self.assertEqual(len(frame_times(15, 5)), 75)
    def test_scene_boundaries(self):
        self.assertEqual(scene_at(3), (1, 0))
        self.assertEqual(scene_at(14.9)[0], 4)
        with self.assertRaises(ValueError):
            scene_at(15)
    def test_cursor_changes(self):
        self.assertNotEqual(cursor_visible(0), cursor_visible(0.2))

if __name__ == "__main__":
    unittest.main()
