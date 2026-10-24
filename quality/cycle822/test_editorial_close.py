import unittest
from editorial_close import (GENRES, CLOSE_FRAMES, SAFE, W, H, CLOSE_TITLE, CLOSE_CTA,
                             validate_close_copy, synthetic_photo, prepared_photo,
                             close_frame, text_alpha)

class TestEditorialClose(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.photo=prepared_photo(synthetic_photo())

    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES: self.assertTrue(validate_close_copy(g))

    def test_all_genres_render(self):
        for g in GENRES:
            self.assertEqual(close_frame(70,self.photo,g).size,(W,H))

    def test_invalid_genre(self):
        with self.assertRaises(ValueError):validate_close_copy('fake')

    def test_blank_copy(self):
        with self.assertRaises(ValueError):validate_close_copy('sales_business',cta='')

    def test_no_fake_results(self):
        with self.assertRaises(ValueError):
            validate_close_copy('sales_business',title=('8件','20件'))

    def test_safe_area(self):
        self.assertEqual(SAFE,(90,120,990,1620))
        self.assertTrue(all(CLOSE_TITLE));self.assertTrue(CLOSE_CTA)

    def test_frame_bounds(self):
        for n in (-1,CLOSE_FRAMES):
            with self.assertRaises(ValueError):close_frame(n,self.photo)

    def test_motion_and_reveal(self):
        a=close_frame(0,self.photo).resize((108,192))
        b=close_frame(89,self.photo).resize((108,192))
        self.assertNotEqual(a.tobytes(),b.tobytes())
        self.assertEqual(text_alpha(0,39),0)
        self.assertEqual(text_alpha(89,39),255)

if __name__=='__main__':unittest.main()
