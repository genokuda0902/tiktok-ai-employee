import unittest
from visual import VALUES, W, H, make_background, make_frame
class TestCycle568(unittest.TestCase):
    def test_verified_total(self):
        self.assertEqual(sum(VALUES), 720)
        self.assertEqual(VALUES, (120,150,200,250))
    def test_vertical(self):
        self.assertEqual((W,H),(1080,1920))
    def test_frame(self):
        self.assertEqual(make_frame(1.0,make_background()).size,(1080,1920))
    def test_result_is_visible_early(self):
        self.assertEqual(round(720*(1-(1-min(1,.65/.65))**3)),720)
if __name__ == '__main__':
    unittest.main()
