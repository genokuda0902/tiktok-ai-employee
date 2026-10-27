import unittest
import numpy as np
from audio_reactive_header import (
    TEN_GENRES,HeaderGeometry,audio_bands,bar_heights,draw_bars,cue_energy,FPS
)
class AudioReactiveTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(TEN_GENRES),10)
        self.assertEqual(len(set(TEN_GENRES)),10)
    def test_header_safe(self):self.assertTrue(HeaderGeometry().safe())
    def test_header_rejects_subtitle(self):self.assertFalse(HeaderGeometry(y=1300).safe())
    def test_header_rejects_right_ui(self):self.assertFalse(HeaderGeometry(x=930).safe())
    def test_bands_shape(self):
        sr=16000;t=np.arange(sr)/sr
        self.assertEqual(audio_bands(np.sin(2*np.pi*500*t),sr,FPS).shape,(FPS,7))
    def test_deterministic(self):
        sr=16000;v=np.sin(2*np.pi*220*np.arange(sr//2)/sr)
        self.assertTrue(np.array_equal(audio_bands(v,sr,15),audio_bands(v,sr,15)))
    def test_silence(self):
        self.assertEqual(float(audio_bands(np.zeros(16000),16000,FPS).max()),0)
    def test_min_bar(self):
        self.assertEqual(bar_heights(np.zeros((1,7))).tolist(),[[4]*7])
    def test_max_bar(self):
        self.assertTrue(np.all(bar_heights(np.ones((1,7)))<=43))
    def test_image_shape(self):self.assertEqual(draw_bars([4]*7).shape,(54,180,3))
    def test_silent_cue(self):
        self.assertEqual(cue_energy(np.zeros(16000),16000,[(.1,.5)]),[0.0])
    def test_invalid_audio(self):
        with self.assertRaises(ValueError):audio_bands(np.array([np.nan]),16000,1)
    def test_invalid_cue(self):
        with self.assertRaises(ValueError):cue_energy(np.zeros(16000),16000,[(2,1)])
if __name__=='__main__':unittest.main()
