import hashlib
import tempfile
import unittest
from pathlib import Path
from kinetic_wipe import (GENRES, CUTS, POLICY, CAPTION_TOP,
                          validate, validate_manifest, filtergraph, make_mask)

class KineticWipeTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for g in GENRES:
            with self.subTest(genre=g): self.assertTrue(validate(g))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): validate('unknown')
    def test_unique_ordered_cuts(self):
        for cuts in ((89, 89), (170, 89), ()):
            with self.subTest(cuts=cuts), self.assertRaises(ValueError): validate(GENRES[0], cuts=cuts)
    def test_overlapping_cuts(self):
        with self.assertRaises(ValueError): validate(GENRES[0], cuts=(89, 96))
    def test_outside_duration(self):
        with self.assertRaises(ValueError): validate(GENRES[0], cuts=(1, 89))
    def test_wipe_duration_limits(self):
        for half in (1, 2, 10, 20):
            with self.subTest(half=half), self.assertRaises(ValueError): validate(GENRES[0], half=half)
    def test_caption_safe_geometry(self):
        with self.assertRaises(ValueError): validate(GENRES[0], caption_top=1900)
        with self.assertRaises(ValueError): validate(GENRES[0], canvas=(0, 1920))
    def test_mask_height_and_alpha(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'mask.png'; w = make_mask(p)
            im = Image.open(p)
            self.assertEqual(im.size, (w, CAPTION_TOP))
            self.assertEqual(im.mode, 'RGBA')
            self.assertEqual(im.getpixel((0, 0))[3], 248)
    def test_filtergraph_7_distinct_wipes(self):
        graph, pad = filtergraph()
        self.assertEqual(graph.count('overlay='), len(CUTS))
        self.assertEqual(pad, '[v7]')
        for c in CUTS: self.assertIn(f'(n-{c-4})', graph)
    def test_manifest_review_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'source.mp4'; p.write_bytes(b'synthetic test only')
            good = dict(POLICY, synthetic_ui=True, source_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            self.assertTrue(validate_manifest(good, p))
            for k in POLICY:
                bad = dict(good); bad[k] = not POLICY[k]
                with self.subTest(key=k), self.assertRaises(ValueError): validate_manifest(bad, p)
            bad = dict(good, source_sha256='0'*64)
            with self.assertRaises(ValueError): validate_manifest(bad, p)
            bad = dict(good, synthetic_ui=False)
            with self.assertRaises(ValueError): validate_manifest(bad, p)

if __name__ == '__main__': unittest.main()
