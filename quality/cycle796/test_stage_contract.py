import unittest
from stage_contract import (
    GENRE_THEMES, SCENE_FRAMES, ART_RECT, SUBTITLE_SAFE_RECT,
    WIDTH, HEIGHT, FPS, scene_index, validate_contract,
)

class StageContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_THEMES), 10)
        self.assertEqual(len(set(GENRE_THEMES)), 10)
        self.assertTrue(all(len(color) == 7 for color in GENRE_THEMES.values()))

    def test_eight_scenes_exact_429_frames(self):
        self.assertEqual(len(SCENE_FRAMES), 8)
        self.assertEqual(sum(SCENE_FRAMES), 429)
        self.assertEqual(scene_index(0), 0)
        self.assertEqual(scene_index(56), 0)
        self.assertEqual(scene_index(57), 1)
        self.assertEqual(scene_index(428), 7)

    def test_bad_frame_rejected(self):
        with self.assertRaises(ValueError):
            scene_index(-1)
        with self.assertRaises(ValueError):
            scene_index(429)

    def test_safe_artwork_subtitle_non_overlap(self):
        x, y, w, h = ART_RECT
        sx, sy, sw, sh = SUBTITLE_SAFE_RECT
        self.assertLessEqual(y+h, sy)
        self.assertLessEqual(x+w, WIDTH)
        self.assertLessEqual(sx+sw, WIDTH)
        self.assertLessEqual(sy+sh, HEIGHT)

    def test_contract(self):
        self.assertTrue(validate_contract())
        self.assertEqual(FPS, 30)

if __name__ == "__main__":
    unittest.main()
