"""Dependency-free CI checks. Actual private video is NOT uploaded to CI."""
from pathlib import Path
import ast,unittest
SOURCE=Path(__file__).with_name('hook_comparison.py')
class Policy(unittest.TestCase):
 def test_source_compiles(self):compile(SOURCE.read_text(),str(SOURCE),'exec')
 def test_ten_genres(self):
  tree=ast.parse(SOURCE.read_text())
  assign=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PALETTES' for t in n.targets))
  self.assertEqual(len(ast.literal_eval(assign.value)),10)
 def test_frames(self):
  s=SOURCE.read_text();self.assertIn('FRAMES=87',s);self.assertIn('WIDTH=952',s);self.assertIn('HEIGHT=1015',s)
 def test_disclaimer(self):self.assertIn('実績ではなく説明用イメージ',SOURCE.read_text())
 def test_human_review(self):self.assertIn('人による確認が必要',SOURCE.read_text())
 def test_no_network(self):
  s=SOURCE.read_text()
  for t in ('requests','urllib.request','httpx','socket','openai','subprocess'):self.assertNotIn('import '+t,s)
 def test_no_posting(self):
  s=SOURCE.read_text()
  for t in ('upload_video','publish_video','post_to_tiktok','auto_merge'):self.assertNotIn(t,s)
 def test_fail_closed_genre(self):self.assertIn("if genre not in PALETTES:raise ValueError",SOURCE.read_text())
 def test_fail_closed_frame(self):self.assertIn("if frame<0 or frame>=FRAMES:raise ValueError",SOURCE.read_text())
 def test_no_real_claim(self):self.assertNotIn('成果保証',SOURCE.read_text())
if __name__=='__main__':unittest.main()
