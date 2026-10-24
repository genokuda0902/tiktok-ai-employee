import unittest
from PIL import ImageChops
from priority_reveal import (ACCENTS,DEFAULT_LABELS,START,FRAMES,X,Y,CW,CH,W,H,
                             validate,stage,smooth,draw)

class TestPriorityReveal(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(ACCENTS),10)
        for g in ACCENTS:
            self.assertTrue(validate(g,DEFAULT_LABELS,1,True))
            self.assertEqual(draw(0,g).size,(CW,CH))
    def test_fictional_optin(self):
        with self.assertRaises(ValueError):validate('sales_business',DEFAULT_LABELS,1,False)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate('bad',DEFAULT_LABELS,1,True)
    def test_labels(self):
        for labels in [('A',),('A','B',''),('A','B','too-long-label'),('A\nX','B','C')]:
            with self.assertRaises(ValueError):validate('sales_business',labels,1,True)
    def test_selection(self):
        for selected in (-1,3):
            with self.assertRaises(ValueError):validate('sales_business',DEFAULT_LABELS,selected,True)
    def test_caption_safe(self):
        self.assertEqual((START,FRAMES),(270,90))
        self.assertGreaterEqual(X,100);self.assertLessEqual(X+CW,W-100)
        self.assertGreaterEqual(Y,620);self.assertLessEqual(Y+CH,1360)
    def test_phases(self):
        self.assertEqual([stage(x) for x in (0,26,27,56,57,89)],[0,0,1,1,2,2])
    def test_invalid_frames(self):
        for i in (-1,90):
            with self.assertRaises(ValueError):stage(i)
    def test_smooth(self):
        self.assertEqual(smooth(-2),0);self.assertEqual(smooth(2),1)
    def test_animation(self):
        self.assertIsNotNone(ImageChops.difference(draw(5).convert('RGB'),draw(42).convert('RGB')).getbbox())
        self.assertIsNotNone(ImageChops.difference(draw(42).convert('RGB'),draw(75).convert('RGB')).getbbox())
    def test_opaque_card(self):
        for i in (0,27,57,89):self.assertEqual(draw(i).getpixel((350,320))[3],255)
    def test_no_publication(self):
        import inspect,priority_reveal
        s=inspect.getsource(priority_reveal.render)
        self.assertIn("'publication_approved':False",s)
        self.assertIn("'auto_post':False",s)

if __name__=='__main__':unittest.main()
