import unittest
from kinetic_hook import (draw_frame, validate, GENRE_ACCENTS, STAGES,
                          CARD_W, CARD_H, CARD_X, CARD_Y, W, H,
                          HOOK_FRAMES, AUTO_POST, PUBLICATION_APPROVED)

class KineticHookTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS),10)
        for genre in GENRE_ACCENTS: self.assertTrue(validate(genre).startswith('#'))
    def test_original_japanese_three_stages(self):
        self.assertEqual(STAGES,('目的','原因','行動'))
    def test_all_frames_opaque(self):
        for i in (0,20,21,41,42,63,89):
            im=draw_frame(i)
            self.assertEqual(im.mode,'RGB')
            self.assertEqual(im.size,(CARD_W,CARD_H))
    def test_stage_animation_actually_changes_pixels(self):
        frames=[draw_frame(i) for i in (0,22,43)]
        # Activation of each stage changes a pixel in its circle.
        self.assertNotEqual(frames[0].getpixel((425,216)),frames[1].getpixel((425,216)))
        self.assertNotEqual(frames[1].getpixel((695,216)),frames[2].getpixel((695,216)))
    def test_progress_animation(self):
        self.assertNotEqual(draw_frame(0).getpixel((420,456)),draw_frame(60).getpixel((420,456)))
    def test_frame_validation(self):
        for i in (-1,HOOK_FRAMES):
            with self.assertRaises(ValueError):draw_frame(i)
        with self.assertRaises(ValueError):validate('private')
    def test_safe_area_preserves_caption_zone(self):
        self.assertGreaterEqual(CARD_X,100)
        self.assertLessEqual(CARD_X+CARD_W,W-100)
        self.assertLessEqual(CARD_Y+CARD_H,1510)
    def test_review_only(self):
        self.assertFalse(AUTO_POST)
        self.assertFalse(PUBLICATION_APPROVED)

if __name__=='__main__': unittest.main()