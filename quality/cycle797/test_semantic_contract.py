import unittest
from semantic_contract import (GENRES, SCENES, SCENE_FRAMES, ART_RECT,
                               SUBTITLE_SAFE_RECT, scene_index, validate)

class TestSemanticAlignment(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
    def test_429_frames(self):
        self.assertEqual(sum(SCENE_FRAMES), 429)
    def test_scene_boundaries(self):
        self.assertEqual(scene_index(0), 0)
        self.assertEqual(scene_index(57), 1)
        self.assertEqual(scene_index(429 - 1), 7)
        with self.assertRaises(ValueError): scene_index(429)
    def test_narration_matches_art(self):
        self.assertIn("画面", SCENES[2][0])
        self.assertIn("display", SCENES[2][2])
        self.assertIn("三つ", SCENES[3][1])
        self.assertIn("power", SCENES[3][2])
        self.assertIn("process", SCENES[5][2])
        self.assertIn("Python", SCENES[6][2])
        self.assertIn("save", SCENES[7][2])
    def test_art_never_overlaps_subtitles(self):
        self.assertLessEqual(ART_RECT[1] + ART_RECT[3], SUBTITLE_SAFE_RECT[1])
    def test_contract(self):
        self.assertTrue(validate())

if __name__ == "__main__": unittest.main()
