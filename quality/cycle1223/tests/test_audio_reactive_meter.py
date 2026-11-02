import sys
import unittest
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from audio_reactive_meter import GENRE_COLORS, METER, envelope, validate_meter, draw_meter

class MeterTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_COLORS), 10)
        for genre in GENRE_COLORS:
            self.assertEqual(draw_meter(np.ones(7), genre).size, (150,100))
    def test_reject_genre(self):
        with self.assertRaises(ValueError): draw_meter(np.zeros(7), 'unapproved')
    def test_guard_geometry(self):
        validate_meter()
        with self.assertRaises(ValueError): validate_meter(rect=(200,1457,150,100))
        with self.assertRaises(ValueError): validate_meter(rect=(704,1590,150,100))
    def test_silent_meter(self):
        levels, voice = envelope(np.zeros(16000,dtype=np.float32),30)
        self.assertTrue(np.all(levels == 0))
        self.assertTrue(np.all(voice == 0))
    def test_loud_voice_raises_bars(self):
        sr=16000
        x=np.concatenate([np.zeros(sr//2),.4*np.sin(2*np.pi*220*np.arange(sr//2)/sr)]).astype(np.float32)
        levels,voice=envelope(x,30)
        self.assertGreater(levels[24].mean(), levels[3].mean()+.35)
        self.assertGreater(voice[24],voice[3]+.5)
    def test_attack_release_finite(self):
        x=np.zeros(16000,dtype=np.float32)
        x[3200:9600]=.2*np.sin(2*np.pi*440*np.arange(6400)/16000)
        levels,_=envelope(x,30)
        self.assertTrue(np.isfinite(levels).all())
        self.assertTrue(((levels>=0)&(levels<=1)).all())
        self.assertGreater(levels[10].mean(),levels[1].mean())
    def test_alpha_and_palette(self):
        im=draw_meter(np.linspace(0,1,7),'ai')
        self.assertEqual(im.mode,'RGBA')
        self.assertEqual(im.getpixel((0,0))[3],0)
        self.assertGreater(im.getpixel((60,40))[3],0)
    def test_invalid_frame_count(self):
        with self.assertRaises(ValueError): envelope(np.zeros(100),0)

if __name__ == '__main__': unittest.main()
