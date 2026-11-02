import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_audio_cues import cue_wave,make_mix,validate_starts,GENRE_TONES,SR

class CueTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRE_TONES),10)
    def test_cue_zero_endpoints(self):
        c=cue_wave(660)
        self.assertLess(abs(float(c[0])),1e-6)
        self.assertLess(abs(float(c[-1])),1e-6)
        self.assertLessEqual(np.max(abs(c)),1.)
    def test_sorted_scene_boundaries(self):
        with self.assertRaises(ValueError):validate_starts((5,3),100)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):make_mix(np.zeros(SR,dtype=np.float32),30,(0,15),'unknown')
    def test_invalid_peak(self):
        with self.assertRaises(ValueError):make_mix(np.zeros(SR,dtype=np.float32),30,(0,15),peak=.3)
    def test_cue_timing_and_outside_unchanged(self):
        voice=np.zeros(SR*3,dtype=np.float32)
        y,original,events=make_mix(voice,90,(0,30,60))
        self.assertEqual(len(events),2)
        self.assertEqual(len(y),SR*3)
        self.assertEqual(float(np.max(abs(y[:SR]))),0.)
        self.assertEqual(float(np.max(abs(y[int(1.2*SR):int(1.9*SR)]))),0.)
        self.assertGreater(np.max(abs(y[SR:SR+6000])),.02)
        self.assertTrue(np.array_equal(original,voice))
    def test_ducking_with_speech(self):
        voice=np.ones(SR*3,dtype=np.float32)*.2
        a,_,events=make_mix(voice,90,(0,30))
        self.assertTrue(events[0]['ducked'])
        self.assertAlmostEqual(events[0]['cue_peak'],.016)
        self.assertLess(float(np.max(abs(a))),.25)
    def test_no_clipping(self):
        with self.assertRaises(ValueError):make_mix(np.ones(SR*3,dtype=np.float32)*.93,90,(0,30))
    def test_voice_padding(self):
        voice=np.ones(SR,dtype=np.float32)*.01
        y,original,_=make_mix(voice,90,(0,30))
        self.assertEqual(len(y),SR*3)
        self.assertTrue(np.all(original[SR:]==0))
    def test_invalid_scene_count(self):
        with self.assertRaises(ValueError):validate_starts((0,),100)

if __name__=='__main__':unittest.main()
