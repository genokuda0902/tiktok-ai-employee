import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from spectral_voice_meter import (GENRE_PRESETS,BANDS,extract_features,
                                  meter_heights,draw_meter,correlation,original_bar_heights)
import numpy as np

class SpectralVoiceMeterTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRE_PRESETS),10)
    def test_eight_bands(self): self.assertEqual(len(BANDS),8)
    def test_silence(self):
        rms,e=extract_features(np.zeros(16000),30)
        self.assertTrue(np.all(meter_heights(rms,e)==7))
    def test_sine_low_vs_high(self):
        t=np.arange(16000)/16000
        _,lo=extract_features((.3*np.sin(2*np.pi*300*t)).astype('float32'),30)
        _,hi=extract_features((.3*np.sin(2*np.pi*3200*t)).astype('float32'),30)
        self.assertGreater(lo[:,1].mean(),lo[:,6].mean()*10)
        self.assertGreater(hi[:,6].mean(),hi[:,1].mean()*10)
    def test_10_genre_bounds(self):
        a=np.random.default_rng(7).normal(0,.1,16000).astype('float32')
        rms,e=extract_features(a,30)
        for g in GENRE_PRESETS:
            h=meter_heights(rms,e,g)
            self.assertEqual(h.shape,(30,8))
            self.assertGreaterEqual(h.min(),7)
            self.assertLessEqual(h.max(),33)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):meter_heights(np.ones(3),np.ones((3,8)),'unknown')
    def test_invalid_bands(self):
        with self.assertRaises(ValueError):meter_heights(np.ones(3),np.ones((3,7)))
    def test_render_outside_roi(self):
        f=np.zeros((1920,1080,3),dtype='uint8')
        draw_meter(f,[7,11,15,19,23,27,31,33])
        self.assertEqual(int(f[1500,500].sum()),0)
        self.assertEqual(int(f[80,400].sum()),0)
        self.assertGreater(int(f[103,575].sum()),0)
    def test_detect_teal(self):
        f=np.zeros((1920,1080,3),dtype='uint8')
        self.assertEqual(sum(original_bar_heights(f)),0)
        draw_meter(f,[33]*8)
        self.assertGreater(sum(original_bar_heights(f)),100)
    def test_corr(self):
        self.assertAlmostEqual(correlation([1,2,3],[2,4,6]),1.)
        self.assertEqual(correlation([0,0,0],[1,2,3]),0.)
    def test_no_network_or_posting(self):
        src=(Path(__file__).resolve().parents[1]/'src'/'spectral_voice_meter.py').read_text()
        self.assertNotIn('requests.',src)
        self.assertNotIn('tiktok.com',src)
        self.assertNotIn('upload_video',src)

if __name__=='__main__':unittest.main()
