import copy
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from quality.cycle1090 import topic_continuity_cta as c

MANIFEST = json.loads((Path(__file__).parent / 'synthetic_manifest.json').read_text())

class ContinuityTests(unittest.TestCase):
    def test_all_ten_genres(self):
        for genre in c.PALETTES:
            m = dict(MANIFEST, genre=genre)
            self.assertTrue(c.check_manifest(m))
            im = c.render_frame(60, m, Image.new('RGB', (934, 512), 'teal'))
            self.assertEqual(im.size, (1080, 1490))
            self.assertEqual(im.getpixel((0, 0))[3], 255)

    def test_manifest_is_review_only(self):
        for key, value in [('synthetic', False), ('review_only', False),
                           ('rights_status', 'approved'), ('contains_private_data', True)]:
            with self.subTest(key=key):
                m = dict(MANIFEST, **{key: value})
                with self.assertRaises(ValueError): c.check_manifest(m)

    def test_missing_fields_fail_closed(self):
        m = dict(MANIFEST)
        del m['preview_crop']
        with self.assertRaises(ValueError): c.check_manifest(m)

    def test_preview_must_be_from_prior_scene(self):
        with self.assertRaises(ValueError): c.check_manifest(dict(MANIFEST, preview_time=20.3))
        with self.assertRaises(ValueError): c.check_manifest(dict(MANIFEST, preview_crop=[0, 0, 1080, 1800]))

    def test_step_and_copy_validation(self):
        for change in [{'steps': ['one']}, {'headline': ''}, {'genre': 'invalid'}]:
            with self.assertRaises(ValueError): c.check_manifest(dict(MANIFEST, **change))

    def test_frame_range(self):
        preview = Image.new('RGB', (934, 512), 'white')
        for i in [-1, c.END - c.START]:
            with self.assertRaises(ValueError): c.render_frame(i, MANIFEST, preview)

    def test_sha_pin(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'clip.txt'
            p.write_bytes(b'private review test')
            c.check_source(p, c.sha256(p))
            with self.assertRaises(ValueError): c.check_source(p, '0' * 64)

    def test_preview_is_synthetic_input_only(self):
        self.assertEqual(MANIFEST['rights_status'], 'unverified')
        self.assertFalse(MANIFEST['contains_private_data'])
        self.assertTrue(MANIFEST['review_only'])

if __name__ == '__main__': unittest.main()
