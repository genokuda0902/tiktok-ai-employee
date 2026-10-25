import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import cv2
import numpy as np
from real_calc_correction import (
    GENRES, POLICY, PALETTES, PANEL, stage, panel_image,
    composite, validate, sha256
)

class TestRealCalcCorrection(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(PALETTES), 10)
    def test_fail_closed_policy(self):
        self.assertTrue(POLICY['review_only'])
        self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['automatic_posting'])
        self.assertFalse(POLICY['external_upload'])
        self.assertFalse(POLICY['source_rights_reviewed'])
        self.assertFalse(POLICY['contains_personal_data'])
    def test_stages(self):
        self.assertEqual(stage(0, 85), 0)
        self.assertEqual(stage(29, 85), 0)
        self.assertEqual(stage(30, 85), 1)
        self.assertEqual(stage(56, 85), 1)
        self.assertEqual(stage(57, 85), 2)
        self.assertEqual(stage(84, 85), 2)
    def test_out_of_bounds(self):
        for k in (-1, 85):
            with self.assertRaises(ValueError): stage(k, 85)
    def test_panel_dimensions(self):
        f = np.zeros((900, 1440, 3), np.uint8)
        for genre in GENRES:
            self.assertEqual(panel_image(f, 5, 85, genre).shape, (758, 908, 3))
    def test_caption_and_heading_protection(self):
        f = np.full((1920, 1080, 3), 77, np.uint8)
        c = np.full((900, 1440, 3), 199, np.uint8)
        o = composite(f, c, 5, 85, 'ai_work')
        self.assertTrue(np.array_equal(o[:476], f[:476]))
        self.assertTrue(np.array_equal(o[1234:], f[1234:]))
        self.assertTrue(np.array_equal(o[:, :86], f[:, :86]))
        self.assertTrue(np.array_equal(o[:, 994:], f[:, 994:]))
        self.assertFalse(np.array_equal(o[476:1234, 86:994], f[476:1234, 86:994]))
    def test_invalid_source_rejected(self):
        with self.assertRaises(FileNotFoundError):
            validate('/not/here', '/not/here', '/tmp/out', {}, 'ai_work', (1, 2))
    def test_invalid_genre_rejected(self):
        with self.assertRaises(ValueError):
            validate('/not/here', '/not/here', '/tmp/out', {}, 'unknown', (1, 2))
    def test_crop_requires_genuine_screen_size(self):
        with self.assertRaises(ValueError):
            panel_image(np.zeros((100, 100, 3), np.uint8), 1, 85, 'ai_work')
    def test_hash_determinism(self):
        with TemporaryDirectory() as d:
            p = Path(d) / 'test'; p.write_bytes(b'fictional')
            self.assertEqual(sha256(p), sha256(p))

if __name__ == '__main__': unittest.main()