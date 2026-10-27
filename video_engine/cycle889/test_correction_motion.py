import unittest
from pathlib import Path
from PIL import Image
from correction_motion import (Correction,EXAMPLE,GENRES,TITLES,START,END,TOP,BOTTOM,
                               POLICY,draw_frame,safe_geometry,stage,validate_manifest,sha256)

class CorrectionTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10);self.assertEqual(set(GENRES),set(TITLES))
    def test_arithmetic(self):self.assertEqual(EXAMPLE.totals(),(45,46))
    def test_other_values(self):self.assertEqual(Correction('travel_food','交通費',(100,200,300),1,150).totals(),(550,600))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):Correction('unknown','費用',(1,2),0,0).totals()
    def test_invalid_value(self):
        with self.assertRaises(ValueError):Correction('ai_productivity','テスト',(1,-2),0,0).totals()
    def test_no_difference(self):
        with self.assertRaises(ValueError):Correction('ai_productivity','テスト',(1,2),0,1).totals()
    def test_invalid_index(self):
        with self.assertRaises(ValueError):Correction('ai_productivity','テスト',(1,2),2,1).totals()
    def test_pii_rejection(self):
        with self.assertRaises(ValueError):Correction('career','080-1234-5678',(1,2),0,0).totals()
    def test_stage_bounds(self):self.assertEqual([stage(i) for i in (0,27,28,57,58,87)],[0,0,1,1,2,2])
    def test_stage_out_of_range(self):
        with self.assertRaises(ValueError):stage(88)
    def test_safe_region(self):self.assertTrue(safe_geometry());self.assertLess(BOTTOM,1438)
    def test_frame_geometry(self):self.assertEqual(draw_frame(0).size,(1080,BOTTOM-TOP))
    def test_distinct_frames(self):
        a,b,c=[draw_frame(i).tobytes() for i in (3,42,80)]
        self.assertNotEqual(a,b);self.assertNotEqual(b,c)
    def test_policy_hash(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'private source')
            m=dict(POLICY,source_sha256=sha256(p));self.assertTrue(validate_manifest(m,p))
            m['source_sha256']='0'*64
            with self.assertRaises(ValueError):validate_manifest(m,p)
    def test_policy_release_guard(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'data')
            m=dict(POLICY,source_sha256=sha256(p),publication_approved=True)
            with self.assertRaises(ValueError):validate_manifest(m,p)

if __name__=='__main__':unittest.main()
