import sys, unittest
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from audio_meter import envelope,make_overlays,GENRE_COLORS,METER_W,METER_H

class MeterTests(unittest.TestCase):
 def test_genres(self): self.assertEqual(len(GENRE_COLORS),10)
 def test_silence(self):
  v=envelope(np.zeros(48000,dtype=np.float32),30)
  self.assertTrue(np.all(v==0))
 def test_voice_dynamic(self):
  t=np.arange(48000)/48000
  signal=np.zeros(48000,dtype=np.float32)
  signal[16000:32000]=0.5*np.sin(2*np.pi*220*t[16000:32000])
  v=envelope(signal,30)
  self.assertGreater(v[14].mean(),v[2].mean()+0.4)
  self.assertLess(v[28].mean(),v[14].mean())
 def test_bounds(self):
  v=envelope(np.ones(1600*5,dtype=np.float32),5)
  self.assertTrue(np.all(v>=0) and np.all(v<=1))
 def test_padding(self):
  self.assertEqual(envelope(np.zeros(100,dtype=np.float32),2).shape,(2,7))
 def test_invalid(self):
  with self.assertRaises(ValueError): envelope(np.zeros(10),0)
 def test_png(self):
  from tempfile import TemporaryDirectory
  with TemporaryDirectory() as p:
   make_overlays(np.array([[0]*7,[1]*7],dtype=float),Path(p),'#4DE3D2')
   with Image.open(Path(p)/'0000.png') as a:
    self.assertEqual(a.size,(METER_W,METER_H))
    self.assertEqual(a.mode,'RGBA')
   self.assertTrue((Path(p)/'0001.png').exists())
 def test_all_genre_colors(self):
  from tempfile import TemporaryDirectory
  for genre,c in GENRE_COLORS.items():
   with TemporaryDirectory() as p:
    make_overlays(np.zeros((1,7)),Path(p),c)
    self.assertTrue((Path(p)/'0000.png').exists(),genre)

if __name__=='__main__':unittest.main()
