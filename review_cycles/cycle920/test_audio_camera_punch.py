import unittest
from audio_camera_punch import (GENRES, SCENE_BOUNDS, TOP_H, STATUS,
    choose_punches, zoom_expression, make_filter)

class CameraPunchTests(unittest.TestCase):
    def setUp(self):
        self.rms = [.04 + .03*((i%13)/13) for i in range(240)]
    def test_ten_genres(self): self.assertEqual(len(set(GENRES)),10)
    def test_fail_closed_status(self): self.assertIn('NOT_APPROVED',STATUS)
    def test_caption_region_preserved(self): self.assertLess(TOP_H,1490)
    def test_scene_count(self): self.assertEqual(len(SCENE_BOUNDS)-1,8)
    def test_punch_count(self): self.assertEqual(len(choose_punches(self.rms)),8)
    def test_each_punch_in_scene(self):
        for p in choose_punches(self.rms):
            lo,hi=SCENE_BOUNDS[p['scene']-1:p['scene']+1]
            self.assertTrue(lo<=p['start']<p['peak']<p['end']<hi)
    def test_silence_no_punch(self): self.assertEqual(choose_punches([0]*240),[])
    def test_ffmpeg_expression(self):
        e=zoom_expression(choose_punches(self.rms))
        self.assertIn('between(on,',e)
        self.assertIn('0.055',e)
    def test_ffmpeg_filter(self):
        f=make_filter(choose_punches(self.rms))
        self.assertIn('overlay=0:0',f)
        self.assertIn('crop=1080:1380',f)
    def test_audio_only_peak(self):
        p=choose_punches(self.rms)
        self.assertTrue(all(x['audio_rms']>.012 for x in p))

if __name__=='__main__': unittest.main()
