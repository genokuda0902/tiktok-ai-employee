import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
from prompt_source_demo import (GENRES, POLICY, TOP, BOTTOM, START, COUNT,
                                PROMPT_LINES, source_record, prompt, typed_lines,
                                frame, safe_text, render)


class SourcePromptTests(unittest.TestCase):
    def test_all_ten_genres_have_correct_totals(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            with self.subTest(genre=genre):
                d = source_record(genre)
                self.assertEqual(d['totals'][0], sum(x[1] for x in d['rows']))
                self.assertEqual(d['totals'][1], sum(x[2] for x in d['rows']))
                self.assertEqual(len(d['rows']), 3)

    def test_ai_work_same_data_as_previous_cycle(self):
        d = source_record('ai_work')
        self.assertEqual(d['rows'], (('4月',12,8),('5月',16,9),('6月',18,12)))
        self.assertEqual(d['totals'], (46,29))

    def test_prompt_uses_three_specific_actions(self):
        p = prompt('ai_work')
        self.assertIn('整理', p)
        self.assertIn('合計とグラフ', p)
        self.assertIn('照合', p)

    def test_typing_is_monotone_and_completes(self):
        counts = [sum(map(len, typed_lines(i))) for i in range(COUNT)]
        self.assertEqual(counts, sorted(counts))
        self.assertEqual(typed_lines(COUNT-1), PROMPT_LINES)

    def test_render_all_genres_at_key_frames(self):
        for genre in GENRES:
            for i in (0, 16, 39, 55, 72, COUNT-1):
                with self.subTest(genre=genre, frame=i):
                    self.assertEqual(frame(i, genre).size, (1080, BOTTOM-TOP))

    def test_text_clipping_rejected(self):
        d = ImageDraw.Draw(Image.new('RGB', (10,10)))
        with self.assertRaises(ValueError):
            safe_text(d,(0,0),'長すぎる文字',10,40,'white')

    def test_out_of_range_and_unknown_genre(self):
        for i in (-1, COUNT):
            with self.assertRaises(ValueError):frame(i)
        with self.assertRaises(ValueError):source_record('nonexistent')

    def test_caption_region_is_not_replaced(self):
        self.assertEqual((START,COUNT,TOP,BOTTOM), (251,85,285,1450))
        self.assertLess(BOTTOM,1490)

    def test_no_external_publish_approval(self):
        for k in ('publication_approved','external_upload','automatic_posting','source_rights_reviewed'):
            self.assertFalse(POLICY[k])

    def test_missing_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(FileNotFoundError):
                render(Path(t)/'missing.mp4',Path(t)/'new.mp4',POLICY)

    def test_reject_wrong_source_manifest(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'placeholder.mp4';src.write_bytes(b'not a video')
            with self.assertRaises(ValueError):
                render(src,Path(t)/'out.mp4',POLICY)

    def test_no_brand_impersonation_or_private_data(self):
        import inspect
        from prompt_source_demo import frame as renderer
        code=inspect.getsource(renderer)
        self.assertIn('OFFLINE DEMO',code)
        self.assertIn('ローカル',code)
        self.assertNotIn('顧客氏名',code)


if __name__=='__main__':
    unittest.main()