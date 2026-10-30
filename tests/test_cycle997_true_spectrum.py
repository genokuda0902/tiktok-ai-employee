import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'/'quality'))
from cycle997_true_spectrum import BANDS_HZ,COLORS,METER,spectral_envelopes,meter_frame

class TestSpectrum(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(COLORS),10)
        for color in COLORS.values(): self.assertEqual(len(color),3)
    def test_eight_bands(self): self.assertEqual(len(BANDS_HZ),8)
    def test_bands_ascending(self):
        self.assertTrue(all(BANDS_HZ[i][1]<=BANDS_HZ[i+1][0] for i in range(7)))
    def test_meters_shape(self): self.assertEqual(meter_frame(np.zeros(8)).size,METER[2:])
    def test_meter_rejects_bad_input(self):
        with self.assertRaises(ValueError):meter_frame(np.ones(7))
        with self.assertRaises(ValueError):meter_frame(np.array([float('nan')]*8))
    def test_silence_is_silent(self):
        out=spectral_envelopes(np.zeros(16000,dtype=np.float32))
        self.assertEqual(out.shape,(30,8));self.assertEqual(float(out.max()),0.)
    def test_signal_frequency_discrimination(self):
        t=np.arange(16000,dtype=np.float32)/16000
        out=spectral_envelopes(.25*np.sin(2*np.pi*430*t).astype(np.float32))
        self.assertGreater(float(out[:,2].mean()),float(out[:,7].mean())+.3)
    def test_attack_release_capped(self):
        t=np.arange(16000,dtype=np.float32)/16000
        s=np.zeros(16000,dtype=np.float32)
        s[5000:10000]=.4*np.sin(2*np.pi*700*t[5000:10000])
        out=spectral_envelopes(s)
        dif=np.diff(out,axis=0)
        self.assertLessEqual(float(dif.max()),.171)
        self.assertGreaterEqual(float(dif.min()),-.096)
    def test_deterministic(self):
        t=np.arange(8000,dtype=np.float32)/16000
        s=.2*np.sin(2*np.pi*1000*t)
        self.assertTrue(np.array_equal(spectral_envelopes(s),spectral_envelopes(s)))
    def test_not_arbitrary_sine(self):
        t=np.arange(16000,dtype=np.float32)/16000
        low=spectral_envelopes(.2*np.sin(2*np.pi*150*t))
        high=spectral_envelopes(.2*np.sin(2*np.pi*3000*t))
        self.assertGreater(float(low[:,0].mean()),float(low[:,6].mean())+.2)
        self.assertGreater(float(high[:,6].mean()),float(high[:,0].mean())+.2)
if __name__=='__main__':unittest.main()
