import sys,unittest
from pathlib import Path
import cv2
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from scene_clarity import SIZE,GENRE_PROFILES,CONTENT_BOUNDS,SCENE_START,SCENE_END,feather_mask,strength_at,render_frame

class ClarityTests(unittest.TestCase):
    def setUp(self):
        self.frame=np.zeros((SIZE[1],SIZE[0],3),dtype=np.uint8)
        self.frame[:,:,:]=(14,26,40)
        self.frame[390:1060,115:805]=(220,228,232)
        for y in range(460,990,40):
            cv2.putText(self.frame,'01  TEST',(170,y),cv2.FONT_HERSHEY_SIMPLEX,1,(30,40,50),2,cv2.LINE_AA)
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_PROFILES),10)
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError):
            strength_at(7.5,'other')
    def test_no_changes_before_scene(self):
        self.assertTrue(np.array_equal(self.frame,render_frame(self.frame,2.0)))
    def test_no_changes_after_scene(self):
        self.assertTrue(np.array_equal(self.frame,render_frame(self.frame,13.0)))
    def test_ramp_and_bounded_strength(self):
        self.assertEqual(strength_at(SCENE_START),0)
        self.assertGreater(strength_at(6.5),strength_at(6.0))
        self.assertLessEqual(strength_at(7.5),0.48)
    def test_safe_areas_pixel_preserved(self):
        out=render_frame(self.frame,7.5)
        x0,y0,x1,y1=CONTENT_BOUNDS
        self.assertTrue(np.array_equal(out[:y0],self.frame[:y0]))
        self.assertTrue(np.array_equal(out[y1:],self.frame[y1:]))
        self.assertTrue(np.array_equal(out[:,:x0],self.frame[:,:x0]))
        self.assertTrue(np.array_equal(out[:,x1:],self.frame[:,x1:]))
    def test_real_detail_change(self):
        out=render_frame(self.frame,7.5)
        self.assertGreater(np.count_nonzero(out!=self.frame),500)
    def test_roi_edges_preserved(self):
        out=render_frame(self.frame,7.5)
        x0,y0,x1,y1=CONTENT_BOUNDS
        self.assertTrue(np.array_equal(out[y0],self.frame[y0]))
        self.assertTrue(np.array_equal(out[y1-1],self.frame[y1-1]))
    def test_mask_range(self):
        a=feather_mask(100,80)
        self.assertEqual(a.shape,(80,100,1))
        self.assertEqual(float(a[0,50,0]),0)
        self.assertGreater(float(a[40,50,0]),0)
    def test_all_genres_render(self):
        for genre in GENRE_PROFILES:
            self.assertEqual(render_frame(self.frame,7.5,genre).shape,self.frame.shape)
    def test_invalid_resolution(self):
        with self.assertRaises(ValueError):
            render_frame(np.zeros((200,100,3),dtype=np.uint8),7.5)

if __name__=='__main__':
    unittest.main()
