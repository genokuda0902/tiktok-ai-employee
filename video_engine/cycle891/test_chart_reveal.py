import unittest,tempfile,hashlib
from pathlib import Path
from chart_reveal import *

class ChartTests(unittest.TestCase):
    def test_genres(self):self.assertEqual(len(GENRES),10)
    def test_geometry(self):self.assertTrue(safe_geometry())
    def test_data(self):self.assertTrue(validate_data(PERIODS,SERIES_A,SERIES_B))
    def test_reject_negative(self):
        with self.assertRaises(ValueError):validate_data(PERIODS,(-1,2,3),SERIES_B)
    def test_reject_float(self):
        with self.assertRaises(ValueError):validate_data(PERIODS,(1.5,2,3),SERIES_B)
    def test_reject_pii(self):
        with self.assertRaises(ValueError):validate_data(('test@example.com','5月','6月'),SERIES_A,SERIES_B)
    def test_reject_wrong_periods(self):
        with self.assertRaises(ValueError):validate_data(('4月','5月'),SERIES_A,SERIES_B)
    def test_initial_zero(self):self.assertEqual(displayed_totals(0),(0,0))
    def test_final_totals(self):self.assertEqual(displayed_totals(80),(46,29))
    def test_monotonic(self):
        values=[displayed_totals(i) for i in range(81)]
        self.assertTrue(all(x<=y and a<=b for (x,a),(y,b) in zip(values,values[1:])))
    def test_reject_outside(self):
        with self.assertRaises(ValueError):revealed(81)
    def test_midway(self):self.assertGreater(displayed_totals(40)[0],12)
    def test_patch(self):self.assertEqual(draw_patch(60).size,(PATCH_W,PATCH_H))
    def test_patch_changes(self):self.assertNotEqual(draw_patch(0).tobytes(),draw_patch(80).tobytes())
    def test_source_hash(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source';p.write_bytes(b'fixture')
            self.assertEqual(sha256(p),hashlib.sha256(b'fixture').hexdigest())
    def test_policy(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source';p.write_bytes(b'fixture')
            m=dict(POLICY,source_sha256=sha256(p))
            self.assertTrue(validate_manifest(m,p))
            m['publication_approved']=True
            with self.assertRaises(ValueError):validate_manifest(m,p)
    def test_hash_gate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source';p.write_bytes(b'fixture')
            with self.assertRaises(ValueError):validate_manifest(dict(POLICY,source_sha256='bad'),p)

if __name__=='__main__':unittest.main()
