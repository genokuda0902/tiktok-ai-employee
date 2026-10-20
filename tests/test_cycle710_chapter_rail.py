"""Unit tests for cycle710 chapter progress overlays (no network required)."""
import math
import unittest
from src.quality.cycle710_chapter_rail import (
    make_overlay, frame_scene, PALETTES, FRAME_COUNT, SCENE_COUNT,
    RAIL_X, RAIL_Y, RAIL_W, RAIL_H
)

class ChapterRailTest(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(PALETTES), 10)
        for name in PALETTES:
            self.assertEqual(make_overlay(40, name).size, (RAIL_W, RAIL_H))

    def test_chapters(self):
        for chapter in range(SCENE_COUNT):
            frame = math.ceil(chapter * FRAME_COUNT / SCENE_COUNT)
            self.assertEqual(frame_scene(frame)[0], chapter)

    def test_dynamic(self):
        self.assertNotEqual(make_overlay(10).tobytes(), make_overlay(100).tobytes())

    def test_safe_area(self):
        self.assertLess(RAIL_Y + RAIL_H, 350)
        self.assertLess(RAIL_X + RAIL_W, 900)

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            make_overlay(1, 'unknown')
        with self.assertRaises(ValueError):
            frame_scene(FRAME_COUNT)

if __name__ == '__main__':
    unittest.main()
