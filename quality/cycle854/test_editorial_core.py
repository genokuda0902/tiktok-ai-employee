"""Standard-library CI tests for 10-genre native slide rules."""
import unittest
from editorial_core import (
    GENRES, WIDTH, HEIGHT, FPS, FRAMES, PHOTO_MAX_SCALE,
    SAFE_LEFT, SAFE_RIGHT, foreground_scale, validate_beats,
    contrast_ratio, scene_count, slide_dimensions, safe_width,
)

class EditorialCoreTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_palette_pairs(self):
        for dark,accent in GENRES.values():
            self.assertTrue(dark.startswith("#") and accent.startswith("#"))
    def test_native_dimensions(self): self.assertEqual(slide_dimensions(),(1080,1920))
    def test_scene_count(self): self.assertEqual(scene_count(),8)
    def test_frame_count(self): self.assertEqual(FRAMES,691)
    def test_frame_rate(self): self.assertEqual(FPS,30)
    def test_safe_width(self): self.assertEqual(safe_width(),838)
    def test_photo_scale_cap(self): self.assertEqual(foreground_scale(200,200),PHOTO_MAX_SCALE)
    def test_large_photo_downscale(self): self.assertLess(foreground_scale(1800,1500),1)
    def test_invalid_size(self):
        with self.assertRaises(ValueError): foreground_scale(0,200)
    def test_valid_beats(self):
        beats=[{"start":i*0.9,"end":i*0.9+0.7,"text":"字幕"} for i in range(24)]
        self.assertTrue(validate_beats(beats))
    def test_wrong_beats(self):
        with self.assertRaises(ValueError):validate_beats([])
    def test_overlapping_beats(self):
        beats=[{"start":i*0.9,"end":i*0.9+0.7} for i in range(24)]
        beats[1]["start"]=0.2
        with self.assertRaises(ValueError):validate_beats(beats)
    def test_white_dark_contrast(self):self.assertGreater(contrast_ratio((255,255,255),(8,15,27)),7)

if __name__=="__main__":unittest.main()
