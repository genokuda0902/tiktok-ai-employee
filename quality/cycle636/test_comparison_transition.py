import unittest
from PIL import Image
from comparison_transition import geometry, reveal_fraction, draw_transition

class WipeTests(unittest.TestCase):
    def test_monotonic(self):
        a=[geometry(i/30) for i in range(31)]
        self.assertEqual(a[0]['visible_after_pixels'],0)
        self.assertEqual(a[-1]['visible_after_pixels'],410)
        self.assertTrue(all(x['divider']>=y['divider'] for x,y in zip(a,a[1:])))
    def test_safe_stage(self):
        x0,y0,x1,y1=geometry(.5)['box']
        self.assertTrue(0<=x0<x1<=540 and 206<=y0<y1<=718)
    def test_no_flash(self):
        self.assertTrue(all(0<=reveal_fraction(i/30)<=1 for i in range(31)))
    def test_invalid_labels(self):
        with self.assertRaises(ValueError):
            draw_transition(Image.new('RGB',(540,960)),.5,{'before':('a',),'after':('b',)})
    def test_pixels_change(self):
        a=Image.new('RGB',(540,960));b=Image.new('RGB',(540,960))
        draw_transition(a,0);draw_transition(b,1)
        self.assertNotEqual(a.tobytes(),b.tobytes())

if __name__=='__main__':unittest.main()
