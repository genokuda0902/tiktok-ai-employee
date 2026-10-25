import unittest
import tempfile
from pathlib import Path
import numpy as np
from subtitle_flash_guard import (GENRES,POLICY,bright_count,repair_frame,
    should_repair,validate_manifest,sha256)

ROI=(10,10,90,50)

def frame(text=True,background=15):
    f=np.full((100,100,3),background,np.uint8)
    if text:f[20:35,20:80]=230
    return f

class FlashGuardTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_single_flash_repaired(self):
        p=frame();c=frame(False);n=frame()
        out,changed=repair_frame(p,c,n,ROI)
        self.assertTrue(changed)
        self.assertTrue(np.array_equal(out[10:50,10:90],p[10:50,10:90]))
    def test_no_change_for_legible(self):
        p=frame();out,changed=repair_frame(p,p,p,ROI)
        self.assertFalse(changed);self.assertTrue(np.array_equal(out,p))
    def test_persistent_dropout_not_repaired(self):
        p=frame();z=frame(False)
        self.assertFalse(should_repair(p,z,z,ROI))
    def test_scene_change_guard(self):
        p=frame(background=10);n=frame(background=150)
        self.assertFalse(should_repair(p,frame(False),n,ROI))
    def test_outside_caption_identical(self):
        p=frame();z=frame(False);out,_=repair_frame(p,z,p,ROI)
        self.assertTrue(np.array_equal(out[:10],z[:10]))
        self.assertTrue(np.array_equal(out[50:],z[50:]))
    def test_invalid_roi(self):
        with self.assertRaises(ValueError):bright_count(frame(),(0,0,110,30))
    def test_policy_fail_closed(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'s.mp4';src.write_bytes(b'fictional')
            dest=Path(t)/'o.mp4'
            m={**POLICY,'source_sha256':sha256(src)}
            for g in GENRES:validate_manifest(m,g,src,dest)
            for key in POLICY:
                bad=m.copy();bad.pop(key)
                with self.assertRaises(ValueError):validate_manifest(bad,'ai_work',src,dest)
            with self.assertRaises(ValueError):validate_manifest(m,'unknown',src,dest)
            with self.assertRaises(ValueError):validate_manifest(m,'ai_work',src,src)
    def test_sha_mismatch(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'s';src.write_bytes(b'x')
            with self.assertRaises(ValueError):validate_manifest({**POLICY,'source_sha256':'0'*64},'ai_work',src,Path(t)/'out')

if __name__=='__main__':unittest.main()
