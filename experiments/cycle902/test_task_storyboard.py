import sys
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[0]))
from task_storyboard import (GENRE_TASKS, POLICY, W, H, X, Y, CAPTION_TOP,
                             STAGE_TIMES, STATUS, validate, render)

class TestTaskStoryboard(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_TASKS), 10)
        for genre in GENRE_TASKS:
            for stage in range(3):
                self.assertEqual(len(validate(genre, stage)), 3)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): validate('medical_diagnosis', 0)
    def test_reject_invalid_stages(self):
        for bad in (-1, 3, 10):
            with self.assertRaises(ValueError): validate('ai', bad)
    def test_safe_area(self):
        self.assertLessEqual(Y+H, CAPTION_TOP)
        self.assertLessEqual(X+W, 1080)
    def test_stage_timing(self):
        self.assertEqual(STAGE_TIMES[0][0], 2.9)
        self.assertEqual(STAGE_TIMES[-1][1], 5.80)
        self.assertTrue(all(a[1] == b[0] for a,b in zip(STAGE_TIMES, STAGE_TIMES[1:])))
    def test_release_gate(self):
        self.assertTrue(POLICY['human_approval_required'])
        self.assertFalse(any(POLICY[k] for k in ('paid_service','auto_post','public_media_upload','unapproved_merge')))
        self.assertIn('NOT_APPROVED', STATUS)
    def test_render_full_res_png(self):
        with TemporaryDirectory() as d:
            paths = [render(Path(d)/f'{i}.png', i) for i in range(3)]
            for p in paths:
                with Image.open(p) as im:
                    self.assertEqual(im.size, (W,H))
                    self.assertEqual(im.mode, 'RGBA')
                    self.assertGreater(im.getpixel((W//2,H//2))[3], 200)
            with Image.open(paths[0]) as a, Image.open(paths[1]) as b:
                self.assertNotEqual(a.tobytes(), b.tobytes())
    def test_no_real_personal_data(self):
        for tasks in GENRE_TASKS.values():
            for s in tasks:
                self.assertNotIn('@', s)
                self.assertNotIn('http', s)
                self.assertLessEqual(len(s), 17)

if __name__ == '__main__': unittest.main()
