import unittest
from scene_config import (
    GENRE_PALETTES, SCENES, FRAME_COUNTS, CAPTION_COUNT,
    WIDTH, HEIGHT, FPS, PUBLICATION_APPROVED
)
class TestSceneConfig(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_PALETTES), 10)
        for palette in GENRE_PALETTES.values():
            self.assertEqual(len(palette), 3)
            self.assertTrue(all(v.startswith("#") and len(v) == 7 for v in palette))
    def test_8_scenes(self):
        self.assertEqual(len(SCENES), 8)
        self.assertEqual(len(FRAME_COUNTS), 8)
    def test_led_visual_fix(self):
        self.assertIn("LED", SCENES[4][0])
        self.assertNotEqual(SCENES[3], SCENES[4])
    def test_video_spec(self):
        self.assertEqual((WIDTH, HEIGHT, FPS), (1080, 1920, 30))
        self.assertEqual(sum(FRAME_COUNTS), 429)
        self.assertEqual(CAPTION_COUNT, 16)
    def test_manual_post_only(self):
        self.assertFalse(PUBLICATION_APPROVED)
if __name__ == "__main__":
    unittest.main()
