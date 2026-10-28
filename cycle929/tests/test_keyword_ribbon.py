import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from keyword_ribbon import (FRAMES, SCENES, GENRE_COLORS, POLICY, RIBBON_SIZE,
                            RIBBON_XY, scene_for_frame, alpha_for_frame, ribbon)

class KeywordRibbonTests(unittest.TestCase):
    def test_10_genres(self):
        self.assertEqual(len(GENRE_COLORS), 10)
        self.assertEqual(len(set(GENRE_COLORS.values())), 10)
    def test_all_scenes_cover_video_without_gaps(self):
        self.assertEqual(SCENES[0][0], 0)
        self.assertEqual(SCENES[-1][1], FRAMES)
        self.assertTrue(all(a[1] == b[0] for a,b in zip(SCENES,SCENES[1:])))
    def test_scene_boundaries(self):
        self.assertEqual(scene_for_frame(86)[0], 1)
        self.assertEqual(scene_for_frame(87)[0], 2)
        self.assertEqual(scene_for_frame(690)[0], 8)
    def test_out_of_range_rejected(self):
        for frame in (-1, FRAMES):
            with self.assertRaises(ValueError): scene_for_frame(frame)
    def test_fade_at_boundaries(self):
        self.assertEqual(alpha_for_frame(0), 0)
        self.assertEqual(alpha_for_frame(86), 0)
        self.assertEqual(alpha_for_frame(20), 1)
    def test_ribbon_is_transparent_at_boundary(self):
        self.assertEqual(ribbon(0).getbbox(), None)
    def test_ribbon_visible_mid_scene(self):
        self.assertIsNotNone(ribbon(40).getbbox())
    def test_ribbon_changes_per_scene(self):
        self.assertNotEqual(ribbon(40).tobytes(), ribbon(140).tobytes())
    def test_10_genre_render(self):
        for genre in GENRE_COLORS:
            with self.subTest(genre=genre):
                self.assertEqual(ribbon(40, genre).size, RIBBON_SIZE)
    def test_invalid_genre_rejected(self):
        with self.assertRaises(ValueError): ribbon(40, 'unknown')
    def test_subtitle_and_header_safe_regions(self):
        x,y=RIBBON_XY; w,h=RIBBON_SIZE
        self.assertGreaterEqual(x, 600)
        self.assertGreaterEqual(y, 255)
        self.assertLessEqual(y+h, 390)
        self.assertLessEqual(x+w, 1080)
    def test_review_only_policy(self):
        self.assertIn('PUBLICATION_NOT_APPROVED', POLICY)

if __name__ == '__main__': unittest.main()
