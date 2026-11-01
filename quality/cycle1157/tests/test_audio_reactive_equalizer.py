import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from audio_reactive_equalizer import (PALETTES,validate_safe_region,
                                     compute_levels,rgba_frame,eval_fraction)

class AudioReactiveTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
    def test_safe_icon(self):self.assertTrue(validate_safe_region())
    def test_reject_text_overlap(self):
        with self.assertRaises(ValueError):validate_safe_region(x=500)
    def test_reject_outside(self):
        with self.assertRaises(ValueError):validate_safe_region(y=1900)
    def test_seven_bands_and_alpha(self):
        im=rgba_frame([.2]*7)
        self.assertEqual(im.size,(124,74))
        self.assertEqual(im.mode,'RGBA')
        self.assertEqual(im.getpixel((0,0))[3],0)
        self.assertGreater(im.getpixel((8,37))[3],0)
    def test_audio_reactivity(self):
        sr=48000;t=np.arange(sr*2)/sr
        amp=np.concatenate([np.zeros(sr//2),np.ones(sr//2)*.6,
                            np.zeros(sr//2),np.ones(sr//2)*.8])
        a=(amp*np.sin(2*np.pi*420*t)).astype('float32')
        levels,rms=compute_levels(a,60,30,sr)
        self.assertEqual(levels.shape,(60,7))
        self.assertGreater(float(levels[25].mean()),float(levels[5].mean())+.2)
        self.assertGreater(float(levels[55].mean()),float(levels[35].mean())+.2)
        self.assertGreater(float(np.corrcoef(levels.mean(axis=1),rms)[0,1]),.65)
    def test_silent_audio(self):
        levels,rms=compute_levels(np.zeros(48000,dtype='float32'),30)
        self.assertTrue(np.all(levels==0))
        self.assertTrue(np.all(rms==0))
    def test_fraction(self):self.assertEqual(eval_fraction('30/1'),30)

if __name__=='__main__':unittest.main()
