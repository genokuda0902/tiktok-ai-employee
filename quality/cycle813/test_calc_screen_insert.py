import unittest
from PIL import Image, ImageChops
from calc_screen_insert import (GENRE_ACCENTS,START,DURATION,CARD_X,CARD_Y,CARD_W,CARD_H,
    AUTO_POST,PUBLICATION_APPROVED,validate,source_index,draw_card)

class TestRealCalcInsert(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS),10)
        for name in GENRE_ACCENTS: self.assertTrue(validate(name,20,12,True))
    def test_reject_private_or_unsanitized(self):
        with self.assertRaises(ValueError): validate('sales_business',20,12,False)
    def test_reject_invalid_genre(self):
        with self.assertRaises(ValueError): validate('unknown',20,12,True)
    def test_reject_invalid_numbers(self):
        for x,y in [(-1,0),(20,21),(1000,1)]:
            with self.assertRaises(ValueError): validate('sales_business',x,y,True)
    def test_safe_area_and_exact_three_seconds(self):
        self.assertEqual((START,DURATION),(90,90))
        self.assertGreaterEqual(CARD_X,100)
        self.assertLessEqual(CARD_X+CARD_W,980)
        self.assertLessEqual(CARD_Y+CARD_H,1320)
    def test_sampling_monotonic(self):
        seq=[source_index(i,162) for i in range(DURATION)]
        self.assertEqual(len(seq),90)
        self.assertTrue(all(a<=b for a,b in zip(seq,seq[1:])))
        self.assertGreater(seq[0],0)
        self.assertLess(seq[-1],162)
    def test_capture_too_short_fails(self):
        with self.assertRaises(ValueError): source_index(1,60)
    def test_card_opaque_and_japanese(self):
        im=Image.new('RGB',(800,292),'white')
        for i in (0,30,80):
            card=draw_card(i,im,'sales_business',20,12)
            self.assertEqual(card.size,(CARD_W,CARD_H))
            self.assertEqual(card.mode,'RGB')
    def test_animation_progress_changes(self):
        im=Image.new('RGB',(800,292),'white')
        a=draw_card(0,im,'sales_business',20,12)
        b=draw_card(80,im,'sales_business',20,12)
        self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
    def test_synthetic_mark_is_different(self):
        im=Image.new('RGB',(800,292),'white')
        self.assertIsNotNone(ImageChops.difference(
            draw_card(50,im,'sales_business',20,12,False),
            draw_card(50,im,'sales_business',20,12,True)).getbbox())
    def test_no_publication_or_autopost(self):
        self.assertIs(AUTO_POST,False)
        self.assertIs(PUBLICATION_APPROVED,False)

if __name__=='__main__': unittest.main()
