import unittest
from cycle866_motion_core import (PALETTES, VIDEO_SIZE, VIDEO_FPS, OLD_CAPTURE_FPS,
    NEW_CAPTURE_FPS, ACTIONS, expected_frames, smoothstep, interpolate,
    pointer_at, validate_genre, report_stats, progress_monotonic)

class MotionTests(unittest.TestCase):
    def setUp(self):
        self.targets=[(200+i*50,100+i*60) for i in range(len(ACTIONS))]
    def test_10_genres(self): self.assertEqual(len(PALETTES),10)
    def test_all_genres(self):
        for genre in PALETTES:self.assertTrue(validate_genre(genre).startswith('#'))
    def test_reject_unknown(self):
        with self.assertRaises(ValueError):validate_genre('unknown')
    def test_resolution(self):self.assertEqual(VIDEO_SIZE,(1080,1920))
    def test_video_fps(self):self.assertEqual(VIDEO_FPS,30)
    def test_3x_capture(self):self.assertEqual(NEW_CAPTURE_FPS,3*OLD_CAPTURE_FPS)
    def test_132_frames(self):self.assertEqual(expected_frames(),132)
    def test_invalid_fps(self):
        with self.assertRaises(ValueError):expected_frames(7)
    def test_smoothstep_edges(self):self.assertEqual((smoothstep(0),smoothstep(1)),(0,1))
    def test_smoothstep_clamp(self):self.assertEqual((smoothstep(-1),smoothstep(2)),(0,1))
    def test_smoothstep_mid(self):self.assertAlmostEqual(smoothstep(.5),.5)
    def test_interpolation_mid(self):self.assertEqual(interpolate((0,0),(100,200),.5),(50,100))
    def test_pointer_initial(self):self.assertEqual(pointer_at(0,self.targets),(60,80))
    def test_pointer_arrival(self):
        for (t,_,_),target in zip(ACTIONS,self.targets):
            self.assertEqual(pointer_at(t-.01,self.targets),target)
    def test_pointer_final(self):self.assertEqual(pointer_at(8.7,self.targets),self.targets[-1])
    def test_pointer_moves(self):self.assertNotEqual(pointer_at(.1,self.targets),pointer_at(.3,self.targets))
    def test_bad_targets(self):
        with self.assertRaises(ValueError):pointer_at(.5,[])
    def test_report(self):self.assertEqual(report_stats(3),{'done':3,'total':4,'pending':1,'percent':75})
    def test_report_bad(self):
        with self.assertRaises(ValueError):report_stats(5)
    def test_monotonic(self):self.assertTrue(progress_monotonic([{'percent':0},{'percent':25},{'percent':75}]))
    def test_nonmonotonic(self):self.assertFalse(progress_monotonic([{'percent':50},{'percent':25}]))
if __name__=='__main__':unittest.main()
