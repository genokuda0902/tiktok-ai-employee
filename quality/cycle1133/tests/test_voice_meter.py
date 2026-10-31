import unittest,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from voice_meter import *
class TestMeter(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
 def test_all_genres_render(self):
  for g in PALETTES:self.assertEqual(meter_frame(.7,g,10).size,SIZE)
 def test_transparent_outside(self):self.assertEqual(meter_frame(.4).getpixel((0,0))[3],0)
 def test_opaque_inside(self):self.assertGreater(meter_frame(.4).getpixel((50,50))[3],0)
 def test_silence(self):self.assertEqual(energy_level(0),0)
 def test_monotonic(self):self.assertLess(energy_level(.003),energy_level(.02))
 def test_saturation(self):self.assertEqual(energy_level(.4),1)
 def test_reject_negative(self):
  with self.assertRaises(ValueError):energy_level(-1)
 def test_reject_nan(self):
  with self.assertRaises(ValueError):energy_level(float('nan'))
 def test_reject_genre(self):
  with self.assertRaises(ValueError):meter_frame(.5,'invalid')
 def test_reject_level(self):
  with self.assertRaises(ValueError):meter_frame(2)
 def test_visual_changes(self):self.assertNotEqual(meter_frame(0).tobytes(),meter_frame(.8).tobytes())
if __name__=='__main__':unittest.main()
