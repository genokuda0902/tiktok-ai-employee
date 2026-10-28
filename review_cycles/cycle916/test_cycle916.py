"""Offline tests: no network or private MP4 required."""
import ast, unittest
from pathlib import Path
from source_diff import GENRES, W,H,FRAMES,START_FRAME,OVERLAY_Y,CAPTION_Y,STATUS,validate,stage,ease,render
class TestCycle916(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_distinct_genres(self):self.assertEqual(len(set(GENRES)),10)
 def test_review_only(self):self.assertIn('PUBLICATION_NOT_APPROVED',STATUS)
 def test_safe_area(self):self.assertLess(OVERLAY_Y+H,CAPTION_Y)
 def test_scene_bounds(self):self.assertEqual((START_FRAME,FRAMES),(435,75))
 def test_three_stages(self):self.assertEqual([stage(i) for i in (0,24,25,49,50,74)],[0,0,1,1,2,2])
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):stage(75)
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):validate('unknown')
 def test_ease(self):self.assertEqual((ease(0),ease(1)),(0,1))
 def test_original_data_label(self):self.assertIn('架空データ',Path(__file__).with_name('source_diff.py').read_text())
 def test_render_size(self):self.assertEqual(render(0).size,(W,H))
 def test_render_last(self):self.assertEqual(render(74,'pets').size,(W,H))
 def test_no_network_or_upload(self):
  tree=ast.parse(Path(__file__).with_name('source_diff.py').read_text()); imports=set()
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):imports.update(n.name.split('.')[0] for n in node.names)
   if isinstance(node,ast.ImportFrom):imports.add((node.module or '').split('.')[0])
  self.assertFalse(imports & {'requests','urllib','httpx','boto3','selenium'})
 def test_no_media_in_source(self):self.assertFalse([p for p in Path(__file__).parent.rglob('*') if p.suffix.lower() in {'.mp4','.png','.jpg','.wav','.aac'}])
if __name__=='__main__':unittest.main()
