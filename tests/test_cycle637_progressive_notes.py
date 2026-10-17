"""Tests for cycle637 progressive disclosure schedule."""
import importlib.util
import pathlib
import unittest

MODULE = pathlib.Path(__file__).resolve().parents[1] / "quality" / "cycle637" / "progressive_notes.py"
spec = importlib.util.spec_from_file_location("cycle637_notes", MODULE)
notes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notes)

class ProgressiveNoteTests(unittest.TestCase):
    def test_scene_count_and_bounds(self):
        self.assertTrue(notes.validate_schedule())
        self.assertEqual(len(notes.BOUNDS) - 1, 8)
        self.assertEqual(notes.BOUNDS[-1], 468)

    def test_early_hidden_late_visible_for_every_scene(self):
        for start in notes.BOUNDS[:-1]:
            self.assertEqual(notes.alpha_level_for_frame(start + 6), 0)
            self.assertEqual(notes.alpha_level_for_frame(start + 32), 10)

    def test_alpha_is_bounded(self):
        for frame in range(468):
            self.assertTrue(0 <= notes.alpha_level_for_frame(frame) <= 10)

    def test_scene_transition(self):
        self.assertEqual(notes.scene_for_frame(notes.BOUNDS[1]), 1)
        self.assertEqual(notes.scene_for_frame(notes.BOUNDS[7]), 7)

    def test_invalid_frames(self):
        for frame in (-1, 468, 1.5, None):
            with self.assertRaises(ValueError):
                notes.scene_for_frame(frame)

if __name__ == "__main__":
    unittest.main()
