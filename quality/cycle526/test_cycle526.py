import unittest
from quality.cycle526.motion_cadence import DEMO, GENRES, FocusScene, draw_frame, stage_at, validate

BASE = {"genre":"ai_work","rights":"synthetic_local_review_only","privacy_checked":True,"publication":"NOT_APPROVED","human_review":"HUMAN_REVIEW","auto_post":False,"scene_cut_seconds":4.0}

class SceneBoundaryTest(unittest.TestCase):
    def test_genres(self):
        for genre in GENRES:
            validate({**BASE,"genre":genre}, DEMO)
    def test_cut_rejection(self):
        with self.assertRaises(ValueError):
            validate(BASE, FocusScene(2.5, 4.1, DEMO.boxes))
    def test_stages(self):
        self.assertEqual([stage_at(t, DEMO)[0] for t in (2.6,3.1,3.6,3.9)], [0,1,2,3])
    def test_safe_caption_area(self):
        for t in (2.6,3.1,3.6,3.9):
            self.assertEqual(draw_frame(DEMO,t).getpixel((200,650))[3],0)

if __name__ == "__main__":
    unittest.main()
