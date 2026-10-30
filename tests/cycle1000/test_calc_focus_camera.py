import unittest
import numpy as np
from calc_focus_camera import GENRES,ROI,KEYFRAMES,camera_at,focus_frame,render

class TestCamera(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_no_motion_outside_scene(self):
        self.assertEqual(camera_at(5.8),(1.,.5,.5))
        self.assertEqual(camera_at(8.9),(1.,.5,.5))
    def test_zoom_two_focus_beats(self):
        self.assertAlmostEqual(camera_at(7.0)[0],1.16)
        self.assertLess(camera_at(7.0)[2],camera_at(7.9)[2])
    def test_no_jump_at_keyframes(self):
        for k in KEYFRAMES[1:-1]:
            before=camera_at(k[0]-.001);after=camera_at(k[0]+.001)
            self.assertLess(max(abs(x-y) for x,y in zip(before,after)),.003)
    def test_preserve_subtitles_and_header(self):
        f=np.zeros((1920,1080,3),np.uint8)
        y,x=np.indices((720,1000));f[335:1055,40:1040,0]=(x%255).astype('uint8')
        g=focus_frame(f,7.3)
        self.assertTrue(np.array_equal(f[:335],g[:335]))
        self.assertTrue(np.array_equal(f[1490:1840],g[1490:1840]))
        self.assertGreater(np.mean(np.abs(f[500:900].astype('int16')-g[500:900].astype('int16'))),2)
    def test_identity_outside_active_window(self):
        f=np.ones((1920,1080,3),np.uint8)
        self.assertIs(f,focus_frame(f,1.))
    def test_bad_roi_rejected(self):
        with self.assertRaises(ValueError):focus_frame(np.zeros((200,200,3),np.uint8),7.3)
    def test_review_only_required(self):
        with self.assertRaises(ValueError):render('none','out','report','ai_work',False)
    def test_genre_allowlist(self):
        with self.assertRaises(ValueError):render('none','out','report','unknown',True)
if __name__=='__main__':unittest.main()
