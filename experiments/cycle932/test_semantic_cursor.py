import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from semantic_cursor import SIZE, GENRE_COLORS, SCENE_DURATION, STEPS, cursor_state, render_frame

class CursorTest(unittest.TestCase):
    def test_ten_distinct_genres(self):
        self.assertEqual(len(GENRE_COLORS),10)
        self.assertEqual(len(set(GENRE_COLORS.values())),10)
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError): render_frame(.8,'unknown')
    def test_safe_canvas(self):
        for genre in GENRE_COLORS:
            self.assertEqual(render_frame(1.53,genre).size,SIZE)
    def test_not_in_opening_hook(self):
        self.assertIsNone(cursor_state(0.0))
    def test_no_overlay_after_scene(self):
        self.assertIsNone(cursor_state(SCENE_DURATION))
    def test_three_distinct_clicks(self):
        for _,_,y,click in STEPS:
            self.assertAlmostEqual(cursor_state(click)[1],y,delta=1)
            self.assertGreater(cursor_state(click)[2],0.9)
    def test_overlay_is_transparent_outside_ui(self):
        frame=render_frame(1.53)
        for point in ((0,0),(540,1450),(540,1800),(60,600)):
            self.assertEqual(frame.getpixel(point)[3],0)
    def test_alpha_at_cursor(self):
        self.assertGreater(render_frame(1.53).getpixel((708,762))[3],0)

if __name__=='__main__': unittest.main()
