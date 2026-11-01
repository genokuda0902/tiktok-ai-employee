import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('content_parallax',str(Path(__file__).resolve().parents[1]/'code/content_parallax.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ContentParallaxTests(unittest.TestCase):
 def test_genres(self):
  self.assertEqual(len(m.GENRE_CONFIG),10)
  self.assertEqual(len(set(m.GENRE_CONFIG)),10)
 def test_mask_edge_and_center(self):
  with tempfile.TemporaryDirectory() as td:
   a=m.make_mask(Path(td)/'a.png')
   self.assertEqual(a.shape,(735,820))
   self.assertEqual(int(a[0,0]),0)
   self.assertEqual(int(a[-1,-1]),0)
   self.assertEqual(int(a[367,410]),255)
   self.assertTrue((a>=0).all() and (a<=255).all())
 def test_bad_roi_rejected(self):
  for roi in [(0,0,500,500),(0,1200,500,500),(900,500,300,300),(60,400,820,800)]:
   with self.assertRaises(ValueError):m.validate_roi(roi)
 def test_graph_keeps_base_and_audio_unmodified(self):
  f=m.filter_graph(m.DEFAULT_ROI,675)
  self.assertIn('split=2[base][src]',f)
  self.assertIn('overlay=60:430',f)
  self.assertIn('on/674',f)
  self.assertNotIn('subtitles',f)
 def test_zoom_limits(self):
  for z in (0.99,1.05):
   with self.assertRaises(ValueError):m.filter_graph(m.DEFAULT_ROI,675,z)
 def test_default_protected_regions(self):
  x,y,w,h=m.DEFAULT_ROI
  self.assertGreaterEqual(y,400)
  self.assertLessEqual(y+h,1180)
  self.assertLessEqual(x+w,930)
 def test_bad_genre(self):
  with self.assertRaises(ValueError):m.render('bad.mp4','badout.mp4','unknown')

if __name__=='__main__': unittest.main()
