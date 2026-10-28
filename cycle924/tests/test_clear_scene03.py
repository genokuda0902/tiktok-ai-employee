import unittest
from pathlib import Path
from PIL import Image
from clear_scene03 import (
    GENRES, START, END, NFRAMES, CAPTION_START, EDIT_BOTTOM,
    STATUS, beat, validate, draw_scene,
)

class TestClearScene03(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES), 10)
    def test_unique_titles(self): self.assertEqual(len({v[0] for v in GENRES.values()}), 10)
    def test_no_private_data(self):
        for v in GENRES.values():
            self.assertNotIn('奥田', str(v))
            self.assertNotIn('ミカ', str(v))
    def test_missing_values_not_filled(self):
        for v in GENRES.values(): self.assertEqual(v[5][1:], ('—','—'))
    def test_three_beats(self):
        self.assertEqual([beat(START),beat(START+29),beat(START+58),beat(END-1)], [0,1,2,2])
    def test_bounds(self):
        for i in [START-1, END]:
            with self.assertRaises(ValueError): beat(i)
    def test_validate_review_only(self): validate('ai_work',Path('x_REVIEW_ONLY.mp4'))
    def test_reject_unsupported(self):
        with self.assertRaises(ValueError): validate('unsupported',Path('x_REVIEW_ONLY.mp4'))
    def test_reject_public_name(self):
        with self.assertRaises(ValueError): validate('ai_work',Path('public.mp4'))
    def test_reject_wrong_frames(self):
        with self.assertRaises(ValueError): validate('ai_work',Path('x_REVIEW_ONLY.mp4'),100)
    def test_edit_region_above_caption(self): self.assertLess(EDIT_BOTTOM,CAPTION_START)
    def test_status_fail_closed(self): self.assertIn('PUBLICATION_NOT_APPROVED',STATUS)
    def test_caption_band_pixel_exact_preencode(self):
        im=Image.new('RGB',(1080,1920),(42,81,116))
        for index in [START,START+35,END-1]:
            out=draw_scene(im,index,'ai_work')
            self.assertEqual(out.crop((0,CAPTION_START,1080,1920)).tobytes(),im.crop((0,CAPTION_START,1080,1920)).tobytes())
    def test_scene_outside_unchanged(self):
        im=Image.new('RGB',(1080,1920),(42,81,116))
        self.assertIs(draw_scene(im,START-1),im)
    def test_visible_change(self):
        im=Image.new('RGB',(1080,1920),(42,81,116))
        out=draw_scene(im,START,'ai_work')
        self.assertNotEqual(out.getpixel((400,500)),im.getpixel((400,500)))

if __name__=='__main__': unittest.main()
