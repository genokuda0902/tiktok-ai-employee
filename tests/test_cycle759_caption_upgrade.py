"""Cycle759 captions: fail-closed asset handling, timeline and ten-genre coverage."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'src' / 'cycle759_caption_upgrade.py'
spec = importlib.util.spec_from_file_location('cycle759_caption_upgrade', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

SRT = '''1
00:00:00,000 --> 00:00:03,200
Hello

2
00:00:03,200 --> 00:00:06,500
Hello

3
00:00:06,500 --> 00:00:09,800
Hello

4
00:00:09,800 --> 00:00:12,800
Hello

5
00:00:12,800 --> 00:00:16,433
Hello

6
00:00:16,433 --> 00:00:20,133
Hello

7
00:00:20,133 --> 00:00:24,300
Hello

8
00:00:24,300 --> 00:00:27,300
Hello
'''

class CaptionQualityTest(unittest.TestCase):
    def setUp(self):
        self.cues = module.parse_srt(SRT)

    def test_eight_contiguous_cues(self):
        self.assertEqual(len(self.cues), 8)
        self.assertEqual(self.cues[0][0], 0)
        self.assertEqual(self.cues[-1][1], 27300)

    def test_all_ten_genres_render(self):
        self.assertEqual(len(module.GENRE_ACCENTS), 10)
        for genre in module.GENRE_ACCENTS:
            with self.subTest(genre=genre):
                ass = module.make_ass(self.cues, genre)
                self.assertEqual(ass.count('Dialogue:'), 8)
                self.assertIn(module.GENRE_ACCENTS[genre], ass)
                self.assertIn(r'\fad(120,100)', ass)
                self.assertIn(r'\N', ass)

    def test_larger_font_and_right_bottom_safety(self):
        module.validate_layout()
        self.assertIn('Noto Sans CJK JP,68', module.make_ass(self.cues))
        self.assertLessEqual(module.CAPTION_Y, 1680)
        self.assertLessEqual(module.CAPTION_X, 530)

    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError):
            module.make_ass(self.cues, 'not_a_genre')

    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            module.parse_srt(SRT.replace('00:00:03,200 --> 00:00:06,500',
                                         '00:00:03,300 --> 00:00:06,500'))

    def test_injection_and_overlong_rejected(self):
        old = module.CAPTION_LINES
        try:
            module.CAPTION_LINES = (('x{', 'ok', 'x'),) + old[1:]
            with self.assertRaises(ValueError):
                module.validate_layout()
            module.CAPTION_LINES = (('あ' * 11, 'ok', 'あ'),) + old[1:]
            with self.assertRaises(ValueError):
                module.validate_layout()
        finally:
            module.CAPTION_LINES = old

    def test_sha_gate_rejects_bad_media(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src, srt, out = root/'fake.mp4', root/'cue.srt', root/'out.mp4'
            src.write_bytes(b'not a real video')
            srt.write_text(SRT)
            with self.assertRaises(ValueError):
                module.render(src, srt, out, '0' * 64)
            self.assertFalse(out.exists())

    def test_known_values_and_summaries(self):
        all_text = ''.join(a+b for a,b,_ in module.CAPTION_LINES)
        self.assertIn('65万円', all_text)
        self.assertIn('最後は人が確認', all_text)
        self.assertIn('架空', all_text)

if __name__ == '__main__':
    unittest.main()
