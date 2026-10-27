"""Offline tests for review-only native Japanese verification panel."""
import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from review_panel import (CAPTION_Y, CHECKS, GENRES, PANEL_X, PANEL_Y,
                          PANEL_W, PANEL_H, POLICY, REVIEW_STATUS, validate,
                          render_panel, render_all)
from PIL import Image

class ReviewPanelTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)
        for genre in GENRES:
            for focus in range(3):
                validate(genre, focus)

    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):
            validate('unknown', 0)

    def test_invalid_focus_rejected(self):
        for focus in (-1, 3, 99):
            with self.assertRaises(ValueError):
                validate('ai', focus)

    def test_caption_and_frame_safe(self):
        self.assertLess(PANEL_Y+PANEL_H, CAPTION_Y)
        self.assertLessEqual(PANEL_X+PANEL_W, 1080)

    def test_fail_closed_policy(self):
        self.assertTrue(POLICY['human_approval_required'])
        self.assertFalse(POLICY['automatic_posting'])
        self.assertFalse(POLICY['public_upload'])
        self.assertFalse(POLICY['paid_service'])
        self.assertFalse(POLICY['merge_without_approval'])
        self.assertIn('NOT_APPROVED', REVIEW_STATUS)

    def test_three_distinct_checks(self):
        self.assertEqual(len(CHECKS), 3)
        self.assertEqual(len(set(x.title for x in CHECKS)), 3)

    def test_render_rgba_native_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = render_panel(Path(tmp) / 'panel.png', 0)
            with Image.open(path) as im:
                self.assertEqual(im.size, (PANEL_W, PANEL_H))
                self.assertEqual(im.mode, 'RGBA')
                self.assertEqual(im.getpixel((0,0))[3], 0)

    def test_focus_changes_pixels(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = render_all(Path(tmp))
            self.assertEqual(len(paths), 3)
            ims = [Image.open(p).convert('RGB') for p in paths]
            self.assertNotEqual(ims[0].tobytes(), ims[1].tobytes())
            self.assertNotEqual(ims[1].tobytes(), ims[2].tobytes())

    def test_render_ten_genres_same_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            for genre in GENRES:
                with Image.open(render_panel(Path(tmp)/f'{genre}.png', 1, genre)) as im:
                    self.assertEqual(im.size, (PANEL_W, PANEL_H))

    def test_reject_too_long_content(self):
        from review_panel import Check
        with self.assertRaises(ValueError):
            validate('ai', 0, (Check('x'*13,'ok'),)*3)

    def test_no_external_dependencies_in_policy(self):
        self.assertNotIn('network', POLICY)
        self.assertNotIn('api_key', POLICY)

if __name__ == '__main__':
    unittest.main()
