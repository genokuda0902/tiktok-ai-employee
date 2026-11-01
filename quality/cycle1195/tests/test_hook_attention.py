import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from hook_attention import HookGeometry,GENRE_COLORS,draw_frame,ease,validate

class HookAttentionTest(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRE_COLORS),10)
    def test_genre_validation(self):
        for genre in GENRE_COLORS:self.assertTrue(validate(HookGeometry(),genre))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate(HookGeometry(),'invalid')
    def test_unsafe_underline(self):
        with self.assertRaises(ValueError):validate(HookGeometry(underline=(74,1155,605)),'ai')
    def test_unsafe_focus(self):
        with self.assertRaises(ValueError):validate(HookGeometry(focal=(468,1130)),'ai')
    def test_duration_limit(self):
        with self.assertRaises(ValueError):validate(HookGeometry(frame_count=50),'ai')
    def test_ease_bounds(self):
        self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
    def test_transparent_start(self):
        self.assertIsNone(draw_frame(0).getbbox())
    def test_effect_is_visible(self):
        self.assertIsNotNone(draw_frame(25).getbbox())
    def test_subtitle_area_untouched(self):
        self.assertIsNone(draw_frame(25).crop((0,1150,1080,1920)).getbbox())
    def test_after_effect_fades(self):
        self.assertGreater(draw_frame(24).getchannel('A').getextrema()[1],draw_frame(41).getchannel('A').getextrema()[1])
    def test_no_frame_overflow(self):
        with self.assertRaises(ValueError):draw_frame(42)

if __name__=='__main__':unittest.main()
