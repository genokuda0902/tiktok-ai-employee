import hashlib
import tempfile
import unittest
from pathlib import Path
from cycle842.before_after import (GENRE_PALETTES,REQUIRED,SCENE_FRAMES,REGION,
    START_FRAME,FRAME_COUNT,ease,panel_frame,validate_manifest,sha256)

class Cycle842Tests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRE_PALETTES),10)
    def test_unique_palette(self): self.assertEqual(len(set(GENRE_PALETTES.values())),10)
    def test_frame_range(self): self.assertEqual((START_FRAME,FRAME_COUNT,sum(SCENE_FRAMES)),(588,103,691))
    def test_region_protects_header_caption(self):
        x,y,w,h=REGION
        self.assertGreaterEqual(x,40)
        self.assertGreaterEqual(y,360)
        self.assertLessEqual(y+h,1150)
        self.assertLessEqual(x+w,1080)
    def test_ease_clamp(self): self.assertEqual((ease(-1),ease(0),ease(1),ease(2)),(0,0,1,1))
    def test_panel_distinct(self):
        a=panel_frame(0); b=panel_frame(55)
        self.assertEqual(a.size,(960,760))
        self.assertNotEqual(hashlib.md5(a.tobytes()).hexdigest(),hashlib.md5(b.tobytes()).hexdigest())
    def test_panel_ten_genres(self):
        for g in GENRE_PALETTES: self.assertEqual(panel_frame(25,g).size,(960,760))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): panel_frame(0,'unknown')
    def test_reject_missing_manifest(self):
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'in';s.write_bytes(b'source');o=Path(t)/'out'
            with self.assertRaises(ValueError): validate_manifest({},'ai_work',s,o)
    def test_reject_unapproved_media(self):
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'in';s.write_bytes(b'source');o=Path(t)/'out'
            m={**REQUIRED,'source_sha256':sha256(s)};m['contains_confidential_media']=True
            with self.assertRaises(ValueError): validate_manifest(m,'ai_work',s,o)
    def test_reject_changed_sha(self):
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'in';s.write_bytes(b'source');o=Path(t)/'out'
            m={**REQUIRED,'source_sha256':'0'*64}
            with self.assertRaises(ValueError): validate_manifest(m,'ai_work',s,o)
    def test_allow_review_only_pinned_fictional(self):
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'in';s.write_bytes(b'source');o=Path(t)/'out'
            m={**REQUIRED,'source_sha256':sha256(s)}
            self.assertIsNone(validate_manifest(m,'ai_work',s,o))
    def test_reject_same_path(self):
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'in';s.write_bytes(b'source')
            m={**REQUIRED,'source_sha256':sha256(s)}
            with self.assertRaises(ValueError): validate_manifest(m,'ai_work',s,s)

if __name__=='__main__':unittest.main()
