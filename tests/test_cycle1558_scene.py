import unittest
from src.cycle1558_scene import VALUES, STEPS, scene_state

class SceneStateTest(unittest.TestCase):
    def test_timeline(self):
        self.assertEqual([scene_state(t)["index"] for t in (0, 3, 6, 9)], [0, 1, 2, 3])
    def test_highlight_and_result(self):
        self.assertEqual(scene_state(6)["highlight"], "source_range")
        self.assertEqual(scene_state(9)["result"], 10000)
        self.assertEqual(sum(VALUES), 10000)
    def test_fail_closed(self):
        self.assertFalse(scene_state(9)["narration_verified"])
        self.assertFalse(scene_state(9)["publication_approved"])
    def test_bounds(self):
        for t in (-1, 12):
            with self.assertRaises(ValueError): scene_state(t)

if __name__ == "__main__":
    unittest.main()
