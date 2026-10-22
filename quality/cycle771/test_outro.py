import unittest
from PIL import Image
from outro_contract import GENRES, SAFE, START_FRAME, END_FRAME, validate, VOICE, CAPTION
from outro_frames import frame

class TestOutros(unittest.TestCase):
    def setUp(self):
        self.c=dict(genre="AI・仕事効率化",supported_genres=list(GENRES),
            quality_approved=False,status="HUMAN_REVIEW",
            post_policy="employee_manual_after_approval",
            media_rights="unverified_review_only",
            narration_cue=VOICE,onscreen_cta=CAPTION,claim="synthetic_arithmetic_only")
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES.values())),10)
    def test_frame_count(self):
        self.assertEqual((START_FRAME,END_FRAME),(729,819))
    def test_safe_area(self):
        self.assertLessEqual(SAFE[2],960)
        self.assertLessEqual(SAFE[3],1600)
    def test_review_gate(self):
        self.assertTrue(validate(self.c))
        for key,bad in [("quality_approved",True),("status","PUBLISHED"),
                        ("post_policy","auto"),("media_rights","approved"),
                        ("claim","guaranteed_10x")]:
            c=dict(self.c);c[key]=bad
            with self.subTest(key=key),self.assertRaises(ValueError):validate(c)
    def test_all_genre_frames(self):
        hero=Image.new("RGB",(1080,1920),"#123456")
        for genre in GENRES:
            with self.subTest(genre=genre):
                self.assertEqual(frame(hero,44,genre).size,(1080,1920))
if __name__=="__main__":unittest.main()
