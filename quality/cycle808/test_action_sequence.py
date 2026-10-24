import unittest
from action_sequence import (GENRES,ACCENTS,STEPS,START_FRAME,SCENE_FRAMES,
                             TOTAL_FRAMES,W,H,validate,action_frame,ease)

class ActionSequenceTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(set(GENRES),set(ACCENTS))
    def test_3_actions(self):validate('sales_business',STEPS)
    def test_unsupported_genre(self):
        with self.assertRaises(ValueError):validate('unknown',STEPS)
    def test_wrong_count(self):
        with self.assertRaises(ValueError):validate('sales_business',STEPS[:2])
    def test_reject_long_values(self):
        with self.assertRaises(ValueError):validate('sales_business',(('誰が','X'*100),)+STEPS[1:])
    def test_reject_multiline(self):
        with self.assertRaises(ValueError):validate('sales_business',(('誰が','悪い\n表示'),)+STEPS[1:])
    def test_reject_frame(self):
        with self.assertRaises(ValueError):action_frame(SCENE_FRAMES)
    def test_smooth_motion(self):
        self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
        self.assertLess(ease(.3),ease(.7))
    def test_image_geometry(self):self.assertEqual(action_frame(0).size,(W,H))
    def test_visible_animation(self):
        self.assertNotEqual(action_frame(10).tobytes(),action_frame(83).tobytes())
    def test_overlay_only_middle_safe_region(self):
        for idx in (0,45,93):
            bbox=action_frame(idx).getchannel('A').getbbox()
            self.assertIsNotNone(bbox)
            self.assertGreaterEqual(bbox[0],120)
            self.assertLessEqual(bbox[2],960)
            self.assertGreaterEqual(bbox[1],730)
            self.assertLessEqual(bbox[3],1320)
    def test_reveal_sequence(self):
        a=action_frame(25).crop((160,1110,915,1220)).getchannel('A')
        b=action_frame(80).crop((160,1110,915,1220)).getchannel('A')
        self.assertNotEqual(a.tobytes(),b.tobytes())
    def test_all_genres_render(self):
        for g in GENRES:self.assertEqual(action_frame(91,g).size,(W,H))
    def test_timeline_bounds(self):
        self.assertEqual((START_FRAME,SCENE_FRAMES,TOTAL_FRAMES),(445,94,718))
        self.assertLess(START_FRAME+SCENE_FRAMES,TOTAL_FRAMES)

if __name__=='__main__':unittest.main()
