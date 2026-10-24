import unittest
from PIL import Image, ImageChops
from calc_screen_insert import (GENRE_ACCENTS,START,DURATION,CARD_X,CARD_Y,CARD_W,CARD_H,
    AUTO_POST,PUBLICATION_APPROVED,validate,source_index,draw_card,focus_box,smoothstep)

class TestFocusDemo(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS),10)
        for name in GENRE_ACCENTS: self.assertTrue(validate(name,20,12,True))
    def test_no_private_data_flag(self):
        with self.assertRaises(ValueError): validate('sales_business',20,12,False)
    def test_invalid_genre_or_metrics(self):
        for args in [('unknown',20,12,True),('sales_business',10,12,True),('sales_business',-1,0,True)]:
            with self.assertRaises(ValueError): validate(*args)
    def test_segment_and_safe_region(self):
        self.assertEqual((START,DURATION),(90,90))
        self.assertGreaterEqual(CARD_X,100)
        self.assertLessEqual(CARD_X+CARD_W,980)
        self.assertLessEqual(CARD_Y+CARD_H,1320)
    def test_source_index_monotonic(self):
        seq=[source_index(i,162) for i in range(DURATION)]
        self.assertTrue(all(a<=b for a,b in zip(seq,seq[1:])))
        self.assertEqual(seq[-1],seq[-12])
    def test_short_capture_rejected(self):
        with self.assertRaises(ValueError): source_index(1,60)
    def test_focus_crop_inside_source_all_frames(self):
        for dims in [(1280,800),(1920,1080)]:
            for i in range(DURATION):
                x1,y1,x2,y2=focus_box(i,*dims)
                self.assertTrue(0<=x1<x2<=dims[0] and 0<=y1<y2<=dims[1])
    def test_focus_progressively_zooms_and_pans(self):
        a=focus_box(0);b=focus_box(40);c=focus_box(89)
        self.assertGreater(a[2]-a[0],b[2]-b[0])
        self.assertGreater(c[0],b[0])
    def test_smoothstep_clamped(self):
        self.assertEqual(smoothstep(-2),0)
        self.assertEqual(smoothstep(2),1)
        self.assertAlmostEqual(smoothstep(.5),.5)
    def test_small_capture_rejected(self):
        with self.assertRaises(ValueError): focus_box(30,800,400)
    def test_card_opaque_and_changes(self):
        im=Image.new('RGB',(1280,800),'white')
        a=draw_card(0,im,'sales_business',20,12)
        b=draw_card(88,im,'sales_business',20,12)
        self.assertEqual(a.size,(CARD_W,CARD_H))
        self.assertEqual(a.mode,'RGB')
        self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
    def test_synthetic_marked(self):
        im=Image.new('RGB',(1280,800),'white')
        self.assertIsNotNone(ImageChops.difference(
            draw_card(55,im,'sales_business',20,12,False),
            draw_card(55,im,'sales_business',20,12,True)).getbbox())
    def test_no_posting(self):
        self.assertIs(AUTO_POST,False)
        self.assertIs(PUBLICATION_APPROVED,False)

if __name__=='__main__': unittest.main()
