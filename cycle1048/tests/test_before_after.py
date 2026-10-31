import sys
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from before_after import GENRES,ACCENTS,START,END,SAFE_Y,frame,validate,crop_evidence

class ReviewOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.still=Image.new('RGB',(1080,1920),'#335577')
        cls.crop=crop_evidence(cls.still)

    def test_ten_genres_are_distinct(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(ACCENTS.values())),10)

    def test_10_genres_can_draw_without_private_assets(self):
        for genre in GENRES:
            im=frame(20,genre,self.crop,self.crop,self.crop)
            self.assertEqual(im.size,(1080,SAFE_Y))

    def test_frame_bounds_fail_closed(self):
        for n in (-1,END-START):
            with self.assertRaises(ValueError): frame(n,'ai_work',self.crop,self.crop,self.crop)

    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): frame(1,'invalid',self.crop,self.crop,self.crop)

    def test_right_panel_reveals_over_time(self):
        a=frame(0,'ai_work',self.crop,self.crop,self.crop)
        b=frame(36,'ai_work',self.crop,self.crop,self.crop)
        self.assertNotEqual(a.getpixel((800,650)),b.getpixel((800,650)))

    def test_protected_subtitle_is_outside_overlay(self):
        self.assertLess(SAFE_Y,1490)
        self.assertEqual(START,609)
        self.assertEqual(END,673)

    def test_no_publication_without_review_flag(self):
        with self.assertRaises(ValueError): validate('missing.mp4','x','ai_work',False)

    def test_no_other_genre_without_rights(self):
        with self.assertRaises(ValueError): validate('missing.mp4','x','beauty',True)

    def test_wrong_source_hash_fails_closed(self):
        with self.assertRaises(ValueError): validate('missing.mp4','x','ai_work',True)

if __name__=='__main__': unittest.main()
