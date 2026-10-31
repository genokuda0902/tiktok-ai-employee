import unittest
from quality.cycle1070.format_reveal import (
    W, H, FPS, PANEL_TOP, PANEL_H, SCENE_START_FRAME, SCENE_END_FRAME,
    FORMATS, PALETTES, MASK, visible_chars, overlay_frame, check_layout)

class FormatRevealTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(FORMATS), 10)
        self.assertEqual(set(FORMATS), set(PALETTES))
    def test_layout(self):
        self.assertTrue(check_layout())
    def test_source_resolution(self):
        self.assertEqual((W,H,FPS),(1080,1920,30))
    def test_scene_frame_count(self):
        self.assertEqual(SCENE_END_FRAME-SCENE_START_FRAME,86)
    def test_preserves_caption_area(self):
        self.assertLess(PANEL_TOP+PANEL_H, 1460)
    def test_mask_is_bounded(self):
        self.assertGreaterEqual(MASK[0], 0)
        self.assertLessEqual(MASK[2], W)
        self.assertLessEqual(MASK[3], PANEL_H)
    def test_no_overlay_before_reveal(self):
        for i in (0, 25, 56):
            self.assertIsNone(overlay_frame(i).getbbox())
    def test_last_frame_shows_full_string(self):
        for g,t in FORMATS.items():
            self.assertEqual(visible_chars(85,t),len(t))
            self.assertIsNotNone(overlay_frame(85,g).getbbox())
    def test_monotonic_typing(self):
        t=FORMATS['ai_work']
        self.assertEqual(visible_chars(56,t),0)
        self.assertTrue(all(visible_chars(i,t)<=visible_chars(i+1,t) for i in range(85)))
    def test_full_text_hold(self):
        t=FORMATS["ai_work"]
        self.assertEqual(visible_chars(75,t),len(t))
        self.assertEqual(visible_chars(85,t),len(t))
    def test_genre_visual_difference(self):
        self.assertNotEqual(overlay_frame(85,'finance').tobytes(), overlay_frame(85,'ai_work').tobytes())
    def test_invalid_genre(self):
        with self.assertRaises(ValueError): overlay_frame(80,'invalid')
    def test_invalid_frame(self):
        for f in (-1,86):
            with self.assertRaises(ValueError): overlay_frame(f)

if __name__=='__main__':unittest.main()
