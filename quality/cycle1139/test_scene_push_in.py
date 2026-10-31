import unittest
from scene_push_in import GENRES, MAX_ZOOM, zoom_value, zoom_expression
CUTS=[0,94,168,247,330,412,499,575,675]
class TestChapterPushIn(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_cuts(self):
        self.assertEqual(len(CUTS)-1,8)
        self.assertEqual(CUTS[-1],675)
    def test_reset(self):
        for a in CUTS[:-1]: self.assertAlmostEqual(zoom_value(a,CUTS),1)
    def test_bounds(self):
        for i in range(675):
            self.assertGreaterEqual(zoom_value(i,CUTS),1)
            self.assertLessEqual(zoom_value(i,CUTS),MAX_ZOOM+1e-10)
    def test_monotonic(self):
        for a,b in zip(CUTS,CUTS[1:]):
            self.assertLess(zoom_value(a,CUTS),zoom_value(b-1,CUTS))
    def test_expression(self):
        e=zoom_expression(CUTS)
        for a,b in zip(CUTS,CUTS[1:]):
            self.assertIn(f'between(on,{a},{b-1})',e)
    def test_unsafe_zoom(self):
        for z in [0.98,1.041,1.2]:
            with self.assertRaises(ValueError): zoom_expression(CUTS,z)
    def test_bad_cuts(self):
        for c in [[0,10,10,20],[2,10,20],[0,20,10]]:
            with self.assertRaises(ValueError): zoom_expression(c)
if __name__=='__main__': unittest.main()
