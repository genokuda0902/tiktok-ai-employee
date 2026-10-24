import unittest
from localize import GENRE_ACCENTS, GENRE_LABELS, SCENE_TITLES, check_config, overlay_image, overlay_framerate

class LocalizationTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS), 10)
        self.assertEqual(set(GENRE_ACCENTS), set(GENRE_LABELS))
    def test_eight_scenes(self):
        self.assertEqual(len(SCENE_TITLES), 8)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): check_config('unknown')
    def test_reject_bad_index(self):
        with self.assertRaises(ValueError): overlay_image(8, 'sales_business')
    def test_all_genres_render(self):
        for genre in GENRE_ACCENTS:
            im = overlay_image(0, genre)
            self.assertEqual(im.size, (1080, 1920))
            self.assertEqual(im.getpixel((150, 175))[3], 255)
            self.assertEqual(im.getpixel((150, 1620))[3], 255)
            self.assertEqual(im.getpixel((15, 15))[3], 0)
    def test_scene_titles_render(self):
        for i in range(8):
            im = overlay_image(i, 'sales_business')
            self.assertEqual(im.getpixel((540, 335))[3], 255)
    def test_variable_length(self):
        self.assertEqual(overlay_framerate(718), '240/718')
        self.assertEqual(overlay_framerate(775), '240/775')
        with self.assertRaises(ValueError): overlay_framerate(7)
    def test_japanese_titles(self):
        for s in SCENE_TITLES:
            self.assertTrue(any(ord(c) > 127 for c in s))

if __name__ == '__main__': unittest.main()
