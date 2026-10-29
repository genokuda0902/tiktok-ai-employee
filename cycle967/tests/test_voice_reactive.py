import importlib.util, pathlib, unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('voice_reactive',ROOT/'code'/'voice_reactive.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class VoiceReactiveTests(unittest.TestCase):
    def test_ten_genre_palettes(self):
        self.assertEqual(len(m.GENRE_COLORS),10)
        self.assertEqual(len(set(m.GENRE_COLORS)),10)
    def test_unreviewed_genre_fails_closed(self):
        with self.assertRaises(PermissionError):m.check_media({'streams':[]},'finance')
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):m.check_media({'streams':[]},'unknown')
    def test_zero_audio_fails_closed(self):
        with self.assertRaises(ValueError):m.analyze_audio(np.zeros(0,dtype=np.float32),90)
    def test_audio_drives_levels(self):
        sr=m.SR;t=np.arange(sr*3)/sr
        amp=np.where(t<1,.015,np.where(t<2,.3,.09))
        audio=(amp*np.sin(2*np.pi*350*t)).astype(np.float32)
        lev,rms=m.analyze_audio(audio,90)
        self.assertEqual(lev.shape,(90,8))
        self.assertGreater(float(rms[45]),float(rms[15])*8)
        self.assertGreater(float(lev[45].mean()),float(lev[15].mean()))
    def test_meter_dimensions_and_alpha(self):
        im=m.draw_meter(np.ones(8),m.GENRE_COLORS['ai_work'])
        self.assertEqual(im.size,(150,41))
        self.assertEqual(im.getpixel((0,0))[3],0)
        self.assertGreater(im.getpixel((10,15))[3],0)
    def test_safe_header_only(self):
        x0,y0,x1,y1=m.METER_BOX
        self.assertTrue(550<=x0<x1<=720 and 60<=y0<y1<=115)
        self.assertLess(y1,1490)
    def test_audio_samples_nonfinite_rejected(self):
        with self.assertRaises(ValueError):m.analyze_audio(np.array([np.nan],dtype=np.float32),2)

if __name__=='__main__':unittest.main()
