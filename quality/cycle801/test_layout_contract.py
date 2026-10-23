import unittest
from layout_contract import (
    WIDTH, HEIGHT, FPS, SCENES, PALETTE, CAPTION_BAND,
    IMAGE_CARD, HEADLINES, scene_index, validate_cues, validate_layout
)

class LayoutContractTest(unittest.TestCase):
    def test_vertical_video(self):
        self.assertEqual((WIDTH, HEIGHT, FPS), (1080, 1920, 30))
    def test_ten_genres(self):
        self.assertEqual(len(PALETTE), 10)
        self.assertEqual(len(set(PALETTE.values())), 10)
    def test_safe_caption_band(self):
        self.assertTrue(validate_layout())
        self.assertLess(IMAGE_CARD[3], CAPTION_BAND[1])
    def test_eight_scenes(self):
        self.assertEqual(len(HEADLINES), SCENES)
        self.assertEqual(scene_index(0), 0)
        self.assertEqual(scene_index(428), 7)
    def test_scene_out_of_range(self):
        with self.assertRaises(ValueError):
            scene_index(429)
    def test_caption_valid(self):
        self.assertTrue(validate_cues([
            {"start": 0, "end": 12, "text": "この基板", "accent": "基板"},
            {"start": 12, "end": 30, "text": "実はパソコン", "accent": "パソコン"},
        ], 429))
    def test_caption_bad_timing(self):
        with self.assertRaises(ValueError):
            validate_cues([{"start": 5, "end": 430, "text": "a", "accent": "a"}], 429)
    def test_caption_missing_emphasis(self):
        with self.assertRaises(ValueError):
            validate_cues([{"start": 0, "end": 10, "text": "abc", "accent": "xyz"}], 429)

if __name__ == "__main__":
    unittest.main()
