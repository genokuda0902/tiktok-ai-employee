import copy
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from repeated_task_ui import *

ROWS = [{'label':'4月','a':12,'b':8},{'label':'5月','a':16,'b':9},{'label':'6月','a':18,'b':12}]

class Cycle892Tests(unittest.TestCase):
    def test_three_rows(self): self.assertTrue(validate_rows(ROWS))
    def test_missing_rows_rejected(self):
        with self.assertRaises(ValueError): validate_rows(ROWS[:2])
    def test_extra_key_rejected(self):
        x=copy.deepcopy(ROWS);x[0]['email']='x'
        with self.assertRaises(ValueError): validate_rows(x)
    def test_url_rejected(self):
        x=copy.deepcopy(ROWS);x[0]['label']='https://a'
        with self.assertRaises(ValueError): validate_rows(x)
    def test_private_like_number_rejected(self):
        x=copy.deepcopy(ROWS);x[0]['label']='12345678'
        with self.assertRaises(ValueError): validate_rows(x)
    def test_negative_rejected(self):
        x=copy.deepcopy(ROWS);x[1]['a']=-1
        with self.assertRaises(ValueError): validate_rows(x)
    def test_float_rejected(self):
        x=copy.deepcopy(ROWS);x[1]['b']=2.5
        with self.assertRaises(ValueError): validate_rows(x)
    def test_boolean_rejected(self):
        x=copy.deepcopy(ROWS);x[0]['a']=True
        with self.assertRaises(ValueError): validate_rows(x)
    def test_large_number_rejected(self):
        x=copy.deepcopy(ROWS);x[0]['a']=1000
        with self.assertRaises(ValueError): validate_rows(x)
    def test_genres_count(self): self.assertEqual(len(set(GENRES)),10)
    def test_stage_boundaries(self):
        self.assertEqual([stage_at(i) for i in (0,26,27,53,54,80)],[0,0,1,1,2,2])
    def test_invalid_stage_rejected(self):
        with self.assertRaises(ValueError): stage_at(81)
    def test_negative_stage_rejected(self):
        with self.assertRaises(ValueError): stage_at(-1)
    def test_patch_dimensions(self): self.assertEqual(draw_patch(30,ROWS).size,(940,530))
    def test_subtitle_protection(self): self.assertLess(PATCH_Y+PATCH_H,1280)
    def _dummy_manifest(self):
        td=tempfile.TemporaryDirectory()
        p=Path(td.name)/'synthetic_source.bin'
        p.write_bytes(b'CI synthetic source; not user media')
        m=dict(REVIEW_POLICY,genre='ai_productivity',source_sha256=sha256(p),rows=ROWS)
        return td,p,m
    def test_manifest_pinned(self):
        td,p,m=self._dummy_manifest()
        try: self.assertTrue(validate_manifest(m,p))
        finally: td.cleanup()
    def test_manifest_rights_fail_closed(self):
        td,p,m=self._dummy_manifest()
        try:
            m['publication_approved']=True
            with self.assertRaises(ValueError): validate_manifest(m,p)
        finally: td.cleanup()
    def test_manifest_bad_genre(self):
        td,p,m=self._dummy_manifest()
        try:
            m['genre']='unapproved'
            with self.assertRaises(ValueError): validate_manifest(m,p)
        finally: td.cleanup()
    def test_alpha_has_content(self):
        self.assertGreater(draw_patch(45,ROWS).getpixel((100,100))[3],200)

if __name__=='__main__': unittest.main()
