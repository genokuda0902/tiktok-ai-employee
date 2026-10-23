import unittest
from motion_contract import (WIDTH, HEIGHT, FPS, SCENE_FRAMES, ART_RECT,
    SUBTITLE_SAFE_RECT, GENRES, progress_at, attention_target, validate_contract)

class TestGuidedMotion(unittest.TestCase):
    def test_video_contract(self):
        self.assertEqual((WIDTH,HEIGHT,FPS),(1080,1920,30))
        self.assertEqual(sum(SCENE_FRAMES),429)
        self.assertTrue(validate_contract())
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_safe_subtitle_area(self):
        self.assertLessEqual(ART_RECT[1]+ART_RECT[3],SUBTITLE_SAFE_RECT[1])
    def test_motion_changes_with_time(self):
        self.assertNotEqual(attention_target(3,0.1),attention_target(3,0.9))
        self.assertNotEqual(attention_target(5,0.1),attention_target(5,0.9))
    def test_targets_are_inside_art(self):
        for scene in (3,5):
            for p in (0.01,0.35,0.67,0.99):
                x,y,r=attention_target(scene,p)
                self.assertTrue(r<=x<ART_RECT[2]-r)
                self.assertTrue(r<=y<ART_RECT[3]-r)
    def test_other_scenes_no_forced_target(self):
        for scene in (0,1,2,4,6,7):
            self.assertIsNone(attention_target(scene,0.5))
    def test_progress_bounds(self):
        self.assertLess(progress_at(0,47),progress_at(46,47))
        with self.assertRaises(ValueError):progress_at(47,47)
        with self.assertRaises(ValueError):attention_target(3,1.1)

if __name__=='__main__':unittest.main()
