"""Run with python -m unittest discover -s quality_cycles/cycle542 -p 'test_*.py'."""
import unittest
from parallax_contract import GENRES, FPS, SCENE_FRAMES, DIRECTIONS, ease_cos, subject_offset, ffmpeg_motion
class ContractTests(unittest.TestCase):
    def test_ten_unique_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)
    def test_exact_timing(self):
        self.assertEqual(sum(SCENE_FRAMES), 375)
        self.assertEqual(FPS, 30)
    def test_six_directions(self):
        self.assertEqual(len(set(DIRECTIONS)), 6)
    def test_ease_clamped(self):
        self.assertEqual(ease_cos(-1), 0)
        self.assertAlmostEqual(ease_cos(.5), .5)
        self.assertEqual(ease_cos(2), 1)
    def test_start_centered(self):
        for scene in range(2, 8):
            self.assertEqual(subject_offset(scene, 0), (-22, -38))
    def test_end_motion(self):
        for scene in range(2, 8):
            self.assertNotEqual(subject_offset(scene, 1), (-22, -38))
    def test_invalid_scene(self):
        with self.assertRaises(ValueError):
            ffmpeg_motion(1)
    def test_time_expression(self):
        for scene in range(2, 8):
            self.assertIn("cos(PI*t/", ffmpeg_motion(scene)[0])
if __name__ == "__main__":
    unittest.main()
