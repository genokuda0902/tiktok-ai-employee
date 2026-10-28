"""Dependency-free CI policy tests; no MP4 or private image uploaded to GitHub."""
import ast, pathlib, unittest
ROOT=pathlib.Path(__file__).parent
SOURCE=(ROOT/'emotional_before_after.py').read_text(encoding='utf-8')
class PolicyTests(unittest.TestCase):
 def test_syntax(self):ast.parse(SOURCE)
 def test_10_genres(self):
  tree=ast.parse(SOURCE)
  v=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GENRES' for t in n.targets))
  self.assertEqual(len(ast.literal_eval(v)),10)
 def test_safe_area(self):self.assertIn('Y0+H < SAFE_CAPTION_Y',SOURCE)
 def test_frame_budget(self):self.assertIn('START+FRAMES==691',SOURCE)
 def test_review_only(self):self.assertIn('PUBLICATION_NOT_APPROVED',SOURCE)
 def test_no_network_or_autopost(self):
  for s in ('requests','urllib','http.client','tiktok.upload','post_video','publish(','os.system'):
   self.assertNotIn(s,SOURCE)
 def test_no_media_committed(self):
  for p in ROOT.rglob('*'):
   if p.is_file():self.assertNotIn(p.suffix.lower(),('.mp4','.mov','.mp3','.aac','.wav','.jpg','.jpeg','.png','.webp'))
if __name__=='__main__':unittest.main()
