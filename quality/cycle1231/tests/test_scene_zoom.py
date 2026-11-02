import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_zoom import zoom_expression,chapter_frames,filtergraph,GENRES,ZOOM_MAX,X,Y,PW,PH
class TestSceneZoom(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(GENRES),10)
 def test_bounds(self):self.assertEqual(chapter_frames([{'start_time':'0'},{'start_time':'1.1'}],60),[0,33,60])
 def test_dedupe(self):self.assertEqual(chapter_frames([{'start_time':'0'},{'start_time':'0'}],60),[0,60])
 def test_empty(self):self.assertEqual(chapter_frames([],60),[0,60])
 def test_expression(self):
  s=zoom_expression([0,33,60]);self.assertIn('lt(on,33)',s);self.assertIn('lt(on,60)',s)
 def test_zoom_limit(self):
  for z in [0.99,1.051]:
   with self.assertRaises(ValueError):zoom_expression([0,60],z)
 def test_bad_bounds(self):
  for x in [[1,60],[0,60,40],[0,0,60]]:
   with self.assertRaises(ValueError):zoom_expression(x)
 def test_filter_preserves_frame_count(self):self.assertIn('d=1',filtergraph([0,60]))
 def test_filter_preserves_safe_area(self):
  f=filtergraph([0,60]);self.assertIn(f'crop={PW}:{PH}:{X}:{Y}',f);self.assertIn(f'overlay={X}:{Y}',f)
 def test_panel_geometry(self):self.assertLessEqual(X+PW,1080);self.assertLessEqual(Y+PH,1150)
 def test_zoom_default(self):self.assertLessEqual(ZOOM_MAX,1.02)
if __name__=='__main__':unittest.main()
