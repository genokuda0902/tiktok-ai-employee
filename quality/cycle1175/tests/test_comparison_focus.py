import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from comparison_focus import GENRES,PALETTES,DEFAULT_CARDS,validate,render_glow,filter_graph
class FocusTest(unittest.TestCase):
 def test_genres(self): self.assertEqual(len(GENRES),10);self.assertEqual(set(GENRES),set(PALETTES))
 def test_valid(self): validate(1080,1920)
 def test_bad_size(self):
  with self.assertRaises(ValueError): validate(720,1280)
 def test_unknown_genre(self):
  with self.assertRaises(ValueError): validate(1080,1920,genre='unknown')
 def test_caption_protected(self):
  for c in DEFAULT_CARDS.values(): self.assertLess(c[3],1320)
 def test_reject_caption_overlap(self):
  with self.assertRaises(ValueError): validate(1080,1920,{'before':(0,1400,100,1600),'after':DEFAULT_CARDS['after']})
 def test_glow_nonzero(self):
  im=render_glow((1080,1920),DEFAULT_CARDS['before'],'#e87caa')
  self.assertGreater(im.getpixel((90,551))[3],0)
 def test_glow_text_interior_transparent(self):
  im=render_glow((1080,1920),DEFAULT_CARDS['before'],'#e87caa')
  self.assertEqual(im.getpixel((300,640))[3],0)
 def test_glow_subtitle_transparent(self):
  im=render_glow((1080,1920),DEFAULT_CARDS['after'],'#51d9d1')
  self.assertEqual(im.getpixel((300,1500))[3],0)
 def test_filter(self):
  f=filter_graph(1,2,2.2,3.5)
  self.assertIn('overlay=0:0',f);self.assertIn('fade=t=out',f)
 def test_overlap_rejected(self):
  with self.assertRaises(ValueError): filter_graph(1,2,1.5,3)
 def test_short_window_rejected(self):
  with self.assertRaises(ValueError): filter_graph(1,1.1,2,3)
if __name__=='__main__': unittest.main()
