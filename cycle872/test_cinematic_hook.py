import unittest
from PIL import Image, ImageChops
from cinematic_hook import (
    GENRES, POLICY, MONTHS, W, START, COUNT, TOP, BOTTOM, fit,
    make_frame, validate, ease,
)

class CinematicHookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.photo = Image.new('RGB', (941, 1672), '#497388')

    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)

    def test_genre_render(self):
        for genre in GENRES:
            with self.subTest(genre=genre):
                self.assertEqual(make_frame(self.photo, 0, genre).size, (W, BOTTOM - TOP))

    def test_dynamic_scene(self):
        a = make_frame(self.photo, 0)
        b = make_frame(self.photo, 70)
        self.assertIsNotNone(ImageChops.difference(a, b).getbbox())

    def test_early_hook_present(self):
        self.assertEqual(make_frame(self.photo, 0).mode, 'RGB')

    def test_three_data_rows_and_totals(self):
        self.assertEqual(sum(row[1] for row in MONTHS), 46)
        self.assertEqual(sum(row[2] for row in MONTHS), 29)

    def test_safe_region(self):
        self.assertEqual((START, COUNT, TOP, BOTTOM), (0, 89, 132, 1490))

    def test_review_policy_fail_closed(self):
        self.assertTrue(POLICY['review_only'])
        for key in ('publication_approved', 'automatic_posting', 'external_upload', 'source_rights_reviewed'):
            self.assertFalse(POLICY[key])

    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): validate('unknown', self.photo, 0)

    def test_small_photo_rejected(self):
        with self.assertRaises(ValueError): validate('ai_work', Image.new('RGB', (640, 1136)), 0)

    def test_out_of_range_rejected(self):
        with self.assertRaises(ValueError): validate('ai_work', self.photo, COUNT)

    def test_clipping_rejected(self):
        with self.assertRaises(ValueError): fit('とても長いタイトル' * 20, 100, 84)

    def test_ease_bounds(self):
        self.assertEqual(ease(-1), 0)
        self.assertEqual(ease(2), 1)

if __name__ == '__main__':
    unittest.main()
