import hashlib
import tempfile
import unittest
from pathlib import Path
from row_focus import (GENRES,DEMO_STEPS,Focus,POLICY,validate,validate_manifest,
                       frame_overlay,create_overlays)

class FocusTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            with self.subTest(genre=genre):self.assertTrue(validate(genre))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate('bad')
    def test_duplicate_steps(self):
        with self.assertRaises(ValueError):validate(GENRES[0],steps=(Focus(18,(50,50,200,200)),Focus(18,(50,50,200,200))))
    def test_too_close_steps(self):
        with self.assertRaises(ValueError):validate(GENRES[0],steps=(Focus(18,(50,50,200,200)),Focus(24,(50,50,200,200))))
    def test_outside_timeline(self):
        with self.assertRaises(ValueError):validate(GENRES[0],steps=(Focus(689,(50,50,200,200)),))
    def test_caption_collision(self):
        with self.assertRaises(ValueError):validate(GENRES[0],steps=(Focus(20,(50,1400,500,1480)),))
    def test_off_canvas(self):
        with self.assertRaises(ValueError):validate(GENRES[0],steps=(Focus(20,(-3,50,500,200)),))
    def test_before_start_transparent(self):
        im=frame_overlay(0)
        self.assertIsNone(im.getbbox())
    def test_focus_active_and_caption_clear(self):
        for n in (18,22,36,42,54,60,78,83):
            im=frame_overlay(n)
            self.assertIsNotNone(im.getbbox())
            self.assertIsNone(im.crop((0,1438,1080,1920)).getbbox())
    def test_distinct_focus_positions(self):
        images=[frame_overlay(s.frame+5) for s in DEMO_STEPS]
        for a,b in zip(images,images[1:]):self.assertNotEqual(a.getbbox(),b.getbbox())
    def test_overlays_count(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(create_overlays(d,count=3,canvas=(1080,1920)),3)
            self.assertEqual(len(list(Path(d).glob('*.png'))),3)
    def test_manifest_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'source.mp4';src.write_bytes(b'synthetic-only')
            good=dict(POLICY,synthetic_ui=True,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest())
            self.assertTrue(validate_manifest(good,src))
            for key in POLICY:
                bad=dict(good);bad[key]=not good[key]
                with self.subTest(key=key),self.assertRaises(ValueError):validate_manifest(bad,src)
            with self.assertRaises(ValueError):validate_manifest(dict(good,source_sha256='0'*64),src)
            with self.assertRaises(ValueError):validate_manifest(dict(good,synthetic_ui=False),src)

if __name__=='__main__':unittest.main()
