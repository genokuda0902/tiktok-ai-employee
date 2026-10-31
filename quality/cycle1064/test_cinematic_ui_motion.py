import unittest
from PIL import Image
from quality.cycle1064.cinematic_ui_motion import (
    COUNT, W, H, PALETTES, phase, motion, render_frame, smoothstep,
)

class MotionTests(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual([phase(x) for x in (0, 27, 28, 55, 56, 81)], [0, 0, 1, 1, 2, 2])
        for bad in (-1, 82):
            with self.assertRaises(ValueError): phase(bad)
    def test_motion_is_smooth_and_bounded(self):
        values = [motion(i)[0] for i in range(COUNT)]
        self.assertEqual(values[0], 1)
        self.assertAlmostEqual(values[-1], 1.085)
        self.assertTrue(all(a <= b for a,b in zip(values, values[1:])))
    def test_easing(self):
        self.assertEqual(smoothstep(-2), 0)
        self.assertEqual(smoothstep(2), 1)
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES), 10)
        blank = Image.new('RGB', (1600, 900), 'white')
        for genre in PALETTES:
            self.assertEqual(render_frame(0, blank, genre).size, (W, H))
    def test_reject_unknown(self):
        with self.assertRaises(ValueError):
            render_frame(0, Image.new('RGB',(1600,900)), 'fake')
    def test_reject_wrong_screenshot_size(self):
        with self.assertRaises(ValueError):
            render_frame(0, Image.new('RGB',(900,1600)))
    def test_distinct_animation_frames(self):
        blank = Image.new('RGB',(1600,900), 'white')
        a = render_frame(0, blank)
        b = render_frame(81, blank)
        self.assertNotEqual(a.tobytes(), b.tobytes())

if __name__ == '__main__': unittest.main()
