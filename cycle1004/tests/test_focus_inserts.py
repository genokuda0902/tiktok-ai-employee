import importlib.util
import pathlib
import unittest
import numpy as np

HERE = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('focus_inserts', HERE/'source'/'focus_inserts.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class FocusTests(unittest.TestCase):
    def test_all_ten_genres_declared(self):
        self.assertEqual(len(m.GENRES), 10)
    def test_non_ai_genres_fail_closed(self):
        for g in m.GENRES[1:]:
            with self.assertRaises(ValueError): m.validate(g, m.AI_WORK_INSERTS)
    def test_release_denied(self):
        with self.assertRaises(ValueError): m.validate('ai_work', m.AI_WORK_INSERTS, approved=True)
    def test_valid_review_windows(self):
        m.validate('ai_work', m.AI_WORK_INSERTS)
    def test_overlap_denied(self):
        w=list(m.AI_WORK_INSERTS);w[1]=(4.5,5.5,.5,.5,'overlap')
        with self.assertRaises(ValueError):m.validate('ai_work',w)
    def test_unsafe_focus_denied(self):
        w=list(m.AI_WORK_INSERTS);w[0]=(3.7,4.5,.01,.5,'bad')
        with self.assertRaises(ValueError):m.validate('ai_work',w)
    def test_no_ghosting_ramp(self):
        a,b,*_=m.AI_WORK_INSERTS[0]
        self.assertEqual(m.focus_strength(a,a,b),0)
        self.assertEqual(m.focus_strength(b,a,b),0)
        self.assertEqual(m.focus_strength((a+b)/2,a,b),1)
    def test_safe_region_exact(self):
        f=np.random.default_rng(1).integers(0,255,(1920,1080,3),dtype=np.uint8)
        original=f.copy();m.focus_roi(f,1,.5,.5)
        self.assertTrue(np.array_equal(f[:520],original[:520]))
        self.assertTrue(np.array_equal(f[1330:],original[1330:]))
        self.assertTrue(np.array_equal(f[:,0:70],original[:,0:70]))
        self.assertTrue(np.array_equal(f[:,1010:],original[:,1010:]))
        self.assertFalse(np.array_equal(f[600:1200,100:900],original[600:1200,100:900]))

if __name__=='__main__':unittest.main()
