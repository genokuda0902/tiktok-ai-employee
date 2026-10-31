import importlib.util, pathlib, unittest
import numpy as np
p=pathlib.Path(__file__).resolve().parents[1]/'source'/'loop_bridge.py'
spec=importlib.util.spec_from_file_location('loop_bridge',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class LoopBridgeTests(unittest.TestCase):
    def test_10_genres_unique(self): self.assertEqual(len(set(m.GENRES)),10)
    def test_duration_and_range(self):
        self.assertEqual(m.START_FRAME,673)
        self.assertEqual(m.BRIDGE_FRAMES,18)
        self.assertEqual(m.FRAMES,691)
    def test_start_fully_transparent(self): self.assertEqual(int(m.radial_mask(0,30,40).max()),0)
    def test_end_fully_opaque(self): self.assertEqual(int(m.radial_mask(17,30,40).min()),255)
    def test_mask_monotonic(self):
        previous=m.radial_mask(0,60,90)
        for i in range(1,18):
            current=m.radial_mask(i,60,90)
            self.assertTrue(np.all(current>=previous))
            previous=current
    def test_mask_range(self):
        for i in range(18):
            mask=m.radial_mask(i,80,120)
            self.assertEqual(mask.shape,(120,80))
            self.assertEqual(mask.dtype,np.uint8)
    def test_mask_opaque_center_by_middle(self):
        mask=m.radial_mask(12,80,120)
        self.assertGreater(mask[60,40],mask[0,0])
    def test_bad_index(self):
        for n in (-1,18):
            with self.assertRaises(ValueError):m.radial_mask(n,20,30)
    def test_fail_closed_missing_review(self):
        with self.assertRaisesRegex(ValueError,'review-only'):
            m.validate_source('missing.mp4',m.SOURCE_SHA,'ai_work',False)
    def test_fail_closed_unknown_genre(self):
        with self.assertRaisesRegex(ValueError,'unknown genre'):
            m.validate_source('missing.mp4',m.SOURCE_SHA,'other',True)
    def test_fail_closed_unapproved_genre(self):
        with self.assertRaisesRegex(ValueError,'no approved'):
            m.validate_source('missing.mp4',m.SOURCE_SHA,'beauty',True)
    def test_fail_closed_source_sha(self):
        with self.assertRaisesRegex(ValueError,'mismatch'):
            m.validate_source('missing.mp4','incorrect','ai_work',True)
if __name__=='__main__':unittest.main()
