import unittest
from goal_ui_demo import W,H,FPS,TOTAL_FRAMES,START_FRAME,SCENE_FRAMES,SCENARIOS,validate,frame,ease

class GoalUIDemoTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(SCENARIOS),10)
    def test_every_genre_valid(self):
        for g in SCENARIOS:validate(g)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):validate('unknown')
    def test_geometry(self):self.assertEqual(frame(20).size,(W,H))
    def test_frame_bounds(self):
        for i in (-1,SCENE_FRAMES):
            with self.assertRaises(ValueError):frame(i)
    def test_scene_timing(self):
        self.assertEqual((START_FRAME,SCENE_FRAMES,TOTAL_FRAMES,FPS),(90,89,718,30))
        self.assertLess(START_FRAME+SCENE_FRAMES,TOTAL_FRAMES+1)
    def test_motion_changes(self):
        self.assertNotEqual(frame(12).tobytes(),frame(78).tobytes())
    def test_save_confirmation_changes(self):
        a=frame(45).crop((180,1070,900,1165))
        b=frame(75).crop((180,1070,900,1165))
        self.assertNotEqual(a.tobytes(),b.tobytes())
    def test_caption_safe_region(self):
        for i in (1,30,70,88):
            bbox=frame(i).getchannel('A').getbbox()
            self.assertGreaterEqual(bbox[0],100)
            self.assertLessEqual(bbox[2],980)
            self.assertGreaterEqual(bbox[1],780)
            self.assertLessEqual(bbox[3],1290)
    def test_transparency_outside_card(self):
        f=frame(65)
        self.assertEqual(f.getpixel((500,1350))[3],0)
        self.assertEqual(f.getpixel((500,550))[3],0)
    def test_all_genres_render(self):
        for g in SCENARIOS:self.assertEqual(frame(75,g).size,(W,H))
    def test_easing(self):
        self.assertEqual(ease(-1),0)
        self.assertEqual(ease(2),1)
        self.assertLess(ease(.2),ease(.8))

if __name__=='__main__':unittest.main()
