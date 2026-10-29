import unittest
from formula_focus import GENRES, SAFE_Y, ORIGIN, SIZE, beat, overlay_frame, validate_genre

class FocusTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_unknown_fails(self):
        with self.assertRaises(ValueError): validate_genre('other')
    def test_unreviewed_genres_fail_closed(self):
        for g in GENRES[1:]:
            with self.assertRaises(ValueError): validate_genre(g)
    def test_synthetic_only_bypass(self):
        for g in GENRES: validate_genre(g,True)
    def test_caption_safe(self):
        self.assertLess(ORIGIN[1]+SIZE[1],110)
        self.assertLess(ORIGIN[1]+SIZE[1],SAFE_Y)
    def test_frame_boundaries(self):
        self.assertEqual(beat(0,87),0)
        self.assertEqual(beat(43,87),1)
        self.assertEqual(beat(86,87),1)
        for i in [-1,87]:
            with self.assertRaises(ValueError): beat(i,87)
    def test_overlay_rgba(self):
        self.assertEqual(overlay_frame(20,87).mode,'RGBA')
        self.assertEqual(overlay_frame(20,87).size,SIZE)
    def test_two_proofs_animate(self):
        self.assertNotEqual(overlay_frame(10,87).tobytes(),overlay_frame(80,87).tobytes())
    def test_only_second_half_has_right_panel(self):
        self.assertNotEqual(overlay_frame(10,87).tobytes(), overlay_frame(70,87).tobytes())
    def test_non_overlay_pixels_transparent(self):
        for i in [0,30,70,86]:
            self.assertEqual(overlay_frame(i,87).getpixel((858,76))[3],0)

if __name__=='__main__': unittest.main()
