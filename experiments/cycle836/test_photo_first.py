import unittest
from PIL import Image
from experiments.cycle836.photo_first import WIDTH, HEIGHT, FRAMES, PALETTES, cover, slide

class TestPhotoFirst(unittest.TestCase):
    def setUp(self):
        self.photo = Image.new("RGB", (720, 1000), "#AABBCC")
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES), 10)
    def test_eight_scenes_775_frames(self):
        self.assertEqual(len(FRAMES), 8)
        self.assertEqual(sum(FRAMES), 775)
    def test_cover_preserves_target_aspect(self):
        self.assertEqual(cover(self.photo, (1080, 1500)).size, (1080, 1500))
    def test_full_bleed_slide_dimensions(self):
        self.assertEqual(slide(self.photo, "headline", "sub", 0).size,
                         (WIDTH, HEIGHT))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):
            slide(self.photo, "headline", "sub", 0, "unknown")
    def test_invalid_scene_rejected(self):
        with self.assertRaises(ValueError):
            slide(self.photo, "headline", "sub", 8)

if __name__ == "__main__":
    unittest.main()
