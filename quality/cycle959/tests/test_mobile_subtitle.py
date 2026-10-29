import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mobile_subtitle as m

class MobileSubtitleTests(unittest.TestCase):
    def test_ten_genre_presets(self):
        self.assertEqual(len(m.GENRE_ACCENTS), 10)
        for genre in m.GENRE_ACCENTS:
            im, meta = m.panel_for_scene(0, genre)
            self.assertEqual(im.size, (1080, 270))
            self.assertGreaterEqual(min(meta['font_sizes_px']), 50)
    def test_eight_distinct_scenes(self):
        self.assertEqual(len(m.SCENES), 8)
        self.assertEqual(len({''.join(t for ln in s for t, _ in ln) for s in m.SCENES}), 8)
    def test_exact_frame_coverage(self):
        self.assertEqual(m.CUTS[0], 0)
        self.assertEqual(m.CUTS[-1], 691)
        self.assertEqual([m.scene_at_frame(x) for x in [0,86,87,173,174,608,609,690]], [0,0,1,1,2,6,7,7])
    def test_all_frames_have_scene(self):
        self.assertEqual([sum(m.scene_at_frame(f)==i for f in range(m.FRAMES)) for i in range(8)], [87]*7+[82])
    def test_text_safe_width_all_genres(self):
        for genre in m.GENRE_ACCENTS:
            for i in range(8):
                im, meta = m.panel_for_scene(i, genre)
                self.assertEqual(im.getpixel((500, 90))[3], 255)
                self.assertTrue(all(70 <= x0 and x1 <= 1010 for x0, _, x1, _ in meta['text_bounds']))
                self.assertGreaterEqual(min(meta['font_sizes_px']), 50)
    def test_invalid_genre_and_scene(self):
        with self.assertRaises(ValueError): m.panel_for_scene(0,'unknown')
        with self.assertRaises(ValueError): m.panel_for_scene(8)
        with self.assertRaises(ValueError): m.scene_at_frame(691)
    def test_reject_unreviewed_source_before_render(self):
        with self.assertRaises(PermissionError):
            m.render(Path(__file__), Path('/tmp/should_not_exist.mp4'))
    def test_existing_text_not_rewritten(self):
        self.assertIn('最初の一歩が大事。', ''.join(t for ln in m.SCENES[0] for t,_ in ln))
        self.assertIn('毎日の習慣にしよう。', ''.join(t for ln in m.SCENES[7] for t,_ in ln))

if __name__ == '__main__': unittest.main()
