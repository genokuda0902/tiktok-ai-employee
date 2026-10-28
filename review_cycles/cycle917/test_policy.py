"""Offline stdlib policy and static QA; GitHub Actions needs no paid dependencies."""
import ast, pathlib, unittest
ROOT=pathlib.Path(__file__).parent
CODE=(ROOT/'template_story.py').read_text(encoding='utf8')
class OfflinePolicy(unittest.TestCase):
 def test_source_parses(self):ast.parse(CODE)
 def test_ten_genres(self):
  tree=ast.parse(CODE);assign=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GENRES' for t in n.targets));self.assertEqual(len(ast.literal_eval(assign.value)),10)
 def test_safe_geometry(self):
  self.assertIn('Y0+H < SAFE_CAPTION_Y',CODE)
  self.assertIn('START+FRAMES<=691',CODE)
 def test_review_only(self):self.assertIn('PUBLICATION_NOT_APPROVED',CODE)
 def test_no_external_calls(self):
  for word in ('requests','urllib','http.client','subprocess','os.system','tiktok.upload','post_video'):
   self.assertNotIn(word,CODE)
 def test_no_private_media(self):
  for p in ROOT.rglob('*'):
   if p.is_file():self.assertNotIn(p.suffix.lower(),('.mp4','.mov','.mp3','.aac','.wav','.jpg','.jpeg','.png','.webp'))
 def test_not_autopost(self):self.assertNotIn('publish(',CODE)
 def test_frame_budget(self):self.assertIn('FRAMES,START,Y0=1080,1260,30,78,510,150',CODE)
if __name__=='__main__':unittest.main()
