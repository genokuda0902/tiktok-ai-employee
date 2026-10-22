"""Offline regression tests: no paid service or network required."""
import json, unittest
from pathlib import Path
import numpy as np
from motion_path import MotionSpec,apply_motion,genre_spec,W,H

ROOT=Path(__file__).resolve().parent

class MotionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=np.zeros((H,W,3),np.uint8)
        cls.base[675:1090]=15

    def test_shape_and_type(self):
        got=apply_motion(self.base,140)
        self.assertEqual(got.shape,self.base.shape)
        self.assertEqual(got.dtype,np.uint8)

    def test_no_change_outside_scene(self):
        for idx in [0,120,177,400]:
            self.assertTrue(np.array_equal(apply_motion(self.base,idx),self.base))

    def test_preserve_subtitles(self):
        for idx in [122,140,154,170]:
            self.assertTrue(np.array_equal(apply_motion(self.base,idx)[1280:],self.base[1280:]))

    def test_preserve_title_area(self):
        self.assertTrue(np.array_equal(apply_motion(self.base,160)[:675],self.base[:675]))

    def test_visible_travel(self):
        self.assertGreater(np.abs(apply_motion(self.base,135).astype(int)-self.base.astype(int)).sum(),1000)

    def test_visible_screen_activation(self):
        self.assertGreater(np.abs(apply_motion(self.base,160).astype(int)-self.base.astype(int)).sum(),1000)

    def test_invalid_size_rejected(self):
        with self.assertRaises(ValueError):apply_motion(np.zeros((100,100,3),np.uint8),130)

    def test_ten_genre_config(self):
        genres=json.loads((ROOT/'config/genres.json').read_text(encoding='utf-8'))['genres']
        self.assertEqual(len(genres),10)
        self.assertEqual(len({g['name'] for g in genres}),10)
        for genre in genres:
            spec=genre_spec(genre['accent'])
            got=apply_motion(self.base,155,spec)
            self.assertEqual(got.shape,self.base.shape)
            self.assertTrue(np.array_equal(got[1280:],self.base[1280:]))

    def test_no_external_assets(self):
        import motion_path
        self.assertFalse(any(x in Path(motion_path.__file__).read_text() for x in ['http://','https://','requests.get']))

if __name__=='__main__':unittest.main()
