import unittest
from focus_motion import CUES, FocusCue, validate_cues, ffmpeg_focus_filter

class FocusMotionTest(unittest.TestCase):
    def test_all_cues_valid(self):
        self.assertTrue(validate_cues(CUES))
    def test_reject_out_of_frame(self):
        with self.assertRaisesRegex(ValueError, 'out of frame'):
            validate_cues([FocusCue(0,0,1,(1075,500,50,100))])
    def test_reject_overlap(self):
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            validate_cues([FocusCue(0,0,1,(0,0,50,50)), FocusCue(0,.5,1.5,(0,0,50,50))])
    def test_reject_bad_scene(self):
        with self.assertRaisesRegex(ValueError, 'scene index'):
            validate_cues([FocusCue(8,0,1,(0,0,50,50))])
    def test_reject_bad_time(self):
        with self.assertRaisesRegex(ValueError, 'timing'):
            validate_cues([FocusCue(0,1,3,(0,0,50,50))])
    def test_filter_contains_scene_cues(self):
        self.assertEqual(ffmpeg_focus_filter(0,CUES),'')
        self.assertEqual(ffmpeg_focus_filter(2,CUES).count('drawbox='),4)
    def test_invalid_color(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported'):
            validate_cues([FocusCue(0,0,1,(0,0,50,50),'0x000000')])
if __name__=='__main__':
    unittest.main()
