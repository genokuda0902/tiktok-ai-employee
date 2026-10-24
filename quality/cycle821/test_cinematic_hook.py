import unittest
from cinematic_hook import GENRES, FRAMES, SAFE, W, H, HEADLINE, make_frame, synthetic_photo, text_alpha, validate_genre

class TestCinematicHook(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            self.assertTrue(validate_genre(genre))
            self.assertEqual(make_frame(42,synthetic_photo(),genre).size,(W,H))

    def test_reject_invalid_genre(self):
        with self.assertRaises(ValueError): validate_genre('unsupported')

    def test_frame_bounds(self):
        for n in (-1,FRAMES):
            with self.assertRaises(ValueError): make_frame(n,synthetic_photo())

    def test_safe_text_and_review_banner(self):
        self.assertLess(SAFE[0],SAFE[2]);self.assertLess(SAFE[1],SAFE[3])
        self.assertTrue(all(isinstance(x,str) and x for x in HEADLINE))
        self.assertGreaterEqual(text_alpha(89,40),250)

    def test_motion_changes_frames(self):
        photo=synthetic_photo()
        a=make_frame(0,photo).resize((90,160))
        b=make_frame(89,photo).resize((90,160))
        self.assertNotEqual(a.tobytes(),b.tobytes())

    def test_safe_area_not_blank(self):
        im=make_frame(89,synthetic_photo())
        self.assertGreater(len(im.getcolors(maxcolors=1000000) or []),100)

if __name__=='__main__':unittest.main()
