import unittest
import tempfile
from pathlib import Path
from PIL import Image
from hook_evidence import GENRES,PALETTES,POLICY,WINDOW,PANEL,stage_index,animate,panel_beat,validate,sha256

class HookTests(unittest.TestCase):
    def setUp(self):
        self.desk=Image.new('RGB',(908,758),(32,45,63))
        self.evidence=Image.new('RGB',(908,758),(195,210,218))
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_palette_per_genre(self):self.assertEqual(set(GENRES),set(PALETTES))
    def test_safe_panel(self):self.assertEqual(PANEL,(86,476,994,1234))
    def test_three_beats(self):self.assertEqual([stage_index(i,90) for i in (0,29,30,59,60,89)],[0,0,1,1,2,2])
    def test_bad_frame(self):
        with self.assertRaises(ValueError):stage_index(90,90)
    def test_bad_duration(self):
        with self.assertRaises(ValueError):stage_index(0,8)
    def test_panel_dimensions(self):
        for i in range(3):self.assertEqual(panel_beat(self.desk,self.evidence,i,'ai_work').size,(908,758))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):panel_beat(self.desk,self.evidence,0,'unknown')
    def test_bad_panel(self):
        with self.assertRaises(ValueError):panel_beat(Image.new('RGB',(1,1)),self.evidence,0,'ai_work')
    def test_animation_no_blank(self):
        p=[panel_beat(self.desk,self.evidence,i,'ai_work') for i in range(3)]
        for f in (0,29,30,31,60,61,89):self.assertEqual(animate(p,f,90).size,(908,758))
    def test_review_only_policy(self):
        self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['external_upload']);self.assertFalse(POLICY['automatic_posting'])
    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError):validate('/missing.mp4','/tmp/out.mp4',{},'ai_work',WINDOW,20,195)
    def test_sha_pinned_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'test')
            with self.assertRaises(ValueError):validate(p,Path(d)/'out',{},'ai_work',WINDOW,0,0)
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'test')
            with self.assertRaises(ValueError):validate(p,p,{**POLICY,'source_sha256':sha256(p)},'ai_work',WINDOW,0,0)

if __name__=='__main__':unittest.main()