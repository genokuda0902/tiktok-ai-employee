import importlib.util
import pathlib
import unittest

SCRIPT=pathlib.Path(__file__).resolve().parents[1]/'tools'/'quality'/'cycle995_audio_reactive_voice.py'
spec=importlib.util.spec_from_file_location('voice',SCRIPT)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class TestVoiceMeter(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.COLORS),10)
        for key,color in m.COLORS.items():
            self.assertEqual(m.meter_frame(.5,5,color).size,(145,40))
    def test_zero_energy(self):
        self.assertEqual(m.smooth_levels([0.]*30),[0.]*30)
    def test_energy_increase(self):
        levels=m.smooth_levels([0.]*15+[.1]*15)
        self.assertGreater(levels[-1],levels[15]); self.assertLessEqual(max(levels),1)
    def test_slow_decay(self):
        levels=m.smooth_levels([.2]*15+[0.]*15)
        self.assertGreater(levels[15],levels[29])
    def test_invalid(self):
        with self.assertRaises(ValueError): m.smooth_levels([])
        with self.assertRaises(ValueError): m.meter_frame(1.2,0)
    def test_roi_is_safe(self):
        x,y,w,h=m.METER
        self.assertTrue(x>=470 and x+w<=730 and y>=55 and y+h<=120)
    def test_bars_change_visually(self):
        self.assertNotEqual(m.meter_frame(0,10).tobytes(),m.meter_frame(.9,10).tobytes())

if __name__=='__main__': unittest.main()
