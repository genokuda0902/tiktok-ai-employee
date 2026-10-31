import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from original_sfx import sfx_wave,make_overlay,GENRE_INTENSITY,BOUNDARIES,SAMPLE_RATE

class TestSFX(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRE_INTENSITY),10)
        for genre in GENRE_INTENSITY:
            a,e=make_overlay(SAMPLE_RATE*23,genre=genre)
            self.assertEqual(a.shape,(SAMPLE_RATE*23,2))
            self.assertEqual(len(e),7)
            self.assertTrue(np.isfinite(a).all())
            self.assertLess(np.max(np.abs(a)),0.09)
    def test_original_deterministic(self):
        self.assertTrue(np.array_equal(sfx_wave(seed=3),sfx_wave(seed=3)))
        self.assertFalse(np.array_equal(sfx_wave(seed=3),sfx_wave(seed=4)))
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError):
            make_overlay(SAMPLE_RATE*2,boundaries=(0.9,),genre='invalid')
    def test_boundary_alignment(self):
        _,events=make_overlay(SAMPLE_RATE*23)
        for e,b in zip(events,BOUNDARIES):
            self.assertLess(e['start_s'],b)
            self.assertGreater(e['end_s'],b)
    def test_20_3_boundary_quieter(self):
        _,events=make_overlay(SAMPLE_RATE*23)
        self.assertLess(events[-1]['intensity'],events[-2]['intensity']/2)
    def test_no_click_at_sfx_edges(self):
        a=sfx_wave()
        self.assertLess(np.max(np.abs(a[0])),1e-6)
        self.assertLess(np.max(np.abs(a[-1])),1e-6)
    def test_untouched_pcm_exact_outside_sfx(self):
        a,_=make_overlay(SAMPLE_RATE*23)
        original=np.random.default_rng(42).uniform(-0.1,0.1,a.shape).astype(np.float32)
        mixed=original+a
        mask=np.all(a==0,axis=1)
        self.assertTrue(np.array_equal(original[mask],mixed[mask]))
    def test_reject_invalid_scene_timing(self):
        with self.assertRaises(ValueError):make_overlay(SAMPLE_RATE*2,boundaries=(2.9,))
        with self.assertRaises(ValueError):make_overlay(SAMPLE_RATE*2,boundaries=(1.4,0.9))
    def test_short_synthetic_media(self):
        a,e=make_overlay(SAMPLE_RATE*2,boundaries=(0.9,1.4))
        self.assertEqual(len(e),2)
        self.assertGreater(np.max(np.abs(a)),0)

if __name__=='__main__':unittest.main()
