import unittest
from cinematic_review import (GENRE_COLORS,FRAME_COUNT,START_FRAME,WIDTH,HEIGHT,
                              check_genre,render_frame)

class CinematicTests(unittest.TestCase):
    def test_genre_contract(self):
        self.assertEqual(len(GENRE_COLORS),10)
        for genre in GENRE_COLORS:
            self.assertTrue(check_genre(genre).startswith('#'))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):check_genre('unknown')
    def test_exact_scene_timing(self):
        self.assertEqual(START_FRAME,540)
        self.assertEqual(FRAME_COUNT,90)
    def test_frame_bounds(self):
        for bad in (-1,90,1000):
            with self.assertRaises(ValueError):render_frame(bad)
    def test_all_genres_render(self):
        for genre in GENRE_COLORS:
            im=render_frame(65,genre)
            self.assertEqual(im.size,(WIDTH,HEIGHT))
            self.assertEqual(im.mode,'RGB')
    def test_animation_changes_visual(self):
        a=render_frame(3)
        b=render_frame(60)
        self.assertNotEqual(a.tobytes(),b.tobytes())
    def test_deterministic(self):
        a=render_frame(20)
        b=render_frame(20)
        self.assertEqual(a.tobytes(),b.tobytes())
    def test_no_personal_data_or_external_assets(self):
        import inspect,cinematic_review
        source=inspect.getsource(cinematic_review)
        self.assertNotIn('http://',source)
        self.assertNotIn('https://',source)
        self.assertNotIn('requests.get',source)
    def test_scene_is_in_safe_middle_region(self):
        from cinematic_review import X,Y
        self.assertGreaterEqual(X,110)
        self.assertGreaterEqual(Y,700)
        self.assertLessEqual(X+WIDTH,960)
        self.assertLessEqual(Y+HEIGHT,1350)

if __name__=='__main__':unittest.main()
