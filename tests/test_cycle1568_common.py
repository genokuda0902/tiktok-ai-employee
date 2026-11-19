import unittest
from quality.cycle1568_common import Scene, validate, progress_frame, publication_gate

class TestReview(unittest.TestCase):
    def test_scene_duration(self):
        self.assertEqual(validate([Scene("冒頭", "説明"), Scene("結果", "解説")]), 6)
    def test_invalid_scene(self):
        with self.assertRaises(ValueError):
            validate([Scene("", "説明")])
    def test_progress_clamp(self):
        self.assertEqual(progress_frame(20, 12), 900)
        self.assertEqual(progress_frame(-1, 12), 0)
    def test_fail_closed(self):
        self.assertFalse(publication_gate())
        self.assertTrue(publication_gate(True, True, True, True))

if __name__ == "__main__":
    unittest.main()
