import importlib.util
import unittest
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'src' / 'prompt_focus_scene.py'
spec = importlib.util.spec_from_file_location('prompt_scene', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class TestPromptFocusScene(unittest.TestCase):
    def test_data_and_layout(self):
        self.assertTrue(m.validate())
        self.assertEqual(sum(m.VALUES), 650000)
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRE_COLORS), 10)
        for genre in m.GENRE_COLORS:
            with self.subTest(genre=genre):
                self.assertEqual(m.frame_at(50, genre).size, (540, 960))
    def test_subtitle_zone_untouched(self):
        for idx in (0, 49, 98):
            im = m.frame_at(idx)
            self.assertEqual(im.getpixel((250, 610))[3], 0)
            self.assertEqual(im.getpixel((250, 800))[3], 0)
    def test_prompt_reveal(self):
        self.assertEqual(m.shown_lines(0), [''])
        self.assertEqual(m.shown_lines(1), list(m.PROMPT_LINES))
        for t in (0.0, 0.2, 0.5, 0.8, 1.0):
            self.assertTrue('\n'.join(m.shown_lines(t)) in '\n'.join(m.PROMPT_LINES))
    def test_visual_motion(self):
        self.assertNotEqual(m.frame_at(5).tobytes(), m.frame_at(70).tobytes())
    def test_reject_invalid_genre(self):
        with self.assertRaises(ValueError): m.frame_at(10, 'not-a-genre')
    def test_reject_invalid_index(self):
        with self.assertRaises(ValueError): m.frame_at(m.FRAMES)
    def test_no_false_ai_claim(self):
        self.assertIn('実際のAI操作映像ではありません', p.read_text(encoding='utf-8'))
    def test_render_preserves_full_duration(self):
        self.assertEqual(m.FRAMES, 99)
        self.assertAlmostEqual(m.END-m.START, 3.3)
if __name__ == '__main__': unittest.main()
