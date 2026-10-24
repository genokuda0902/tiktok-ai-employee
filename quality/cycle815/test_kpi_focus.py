import unittest
from PIL import ImageChops
from kpi_focus import (ACCENTS,DEFAULT_ROWS,START,FRAMES,X,Y,CW,CH,W,H,check,phase,smooth,draw)

class TestKpiFocus(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(ACCENTS),10)
        for genre in ACCENTS:
            self.assertTrue(check(genre,DEFAULT_ROWS,True))
            self.assertEqual(draw(0,genre).size,(CW,CH))
    def test_data_gate(self):
        with self.assertRaises(ValueError): check('sales_business',DEFAULT_ROWS,False)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): check('unknown',DEFAULT_ROWS,True)
    def test_invalid_metrics(self):
        for rows in [(('X',10,0),)*3,(('X',110,90),)*3,(('X',-1,10),)*3]:
            with self.assertRaises(ValueError): check('sales_business',rows,True)
    def test_oversized_label(self):
        with self.assertRaises(ValueError): check('sales_business',(('長い文字列をたくさん書く',10,20),)*3,True)
    def test_safe_area(self):
        self.assertEqual((START,FRAMES),(180,90))
        self.assertGreaterEqual(X,100)
        self.assertLessEqual(X+CW,W-100)
        self.assertGreaterEqual(Y,620)
        self.assertLessEqual(Y+CH,1320)
    def test_three_beats(self):
        self.assertEqual([phase(i) for i in (0,29,30,59,60,89)],[0,0,1,1,2,2])
    def test_outside_rejected(self):
        for i in (-1,90):
            with self.assertRaises(ValueError): phase(i)
    def test_smooth_bounds(self):
        self.assertEqual(smooth(-1),0)
        self.assertEqual(smooth(2),1)
    def test_visual_animation(self):
        self.assertIsNotNone(ImageChops.difference(draw(0).convert('RGB'),draw(20).convert('RGB')).getbbox())
        self.assertIsNotNone(ImageChops.difference(draw(30).convert('RGB'),draw(55).convert('RGB')).getbbox())
    def test_opacity_no_ghosting(self):
        for i in (0,30,60,89):
            self.assertEqual(draw(i).getpixel((400,300))[3],255)
    def test_fictional_label_and_nonposting(self):
        import inspect,kpi_focus
        s=inspect.getsource(kpi_focus.render)
        self.assertIn("'publication_approved':False",s)
        self.assertIn("'auto_post':False",s)

if __name__=='__main__':unittest.main()
