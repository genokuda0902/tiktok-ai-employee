"""No third-party packages or private media required by CI."""
import ast
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parent
SRC=(ROOT/'source_diff.py').read_text(encoding='utf-8')
TREE=ast.parse(SRC)
class TestOffline(unittest.TestCase):
 def test_valid_syntax(self):self.assertIsInstance(TREE,ast.Module)
 def test_ten_genres(self):self.assertEqual(SRC.count("':("),10)
 def test_review_gate(self):self.assertIn('PUBLICATION_NOT_APPROVED',SRC)
 def test_75_frames(self):self.assertIn('30, 75, 435, 300',SRC)
 def test_caption_protection(self):self.assertIn('OVERLAY_Y+H>=CAPTION_Y',SRC)
 def test_fictional_label(self):self.assertIn('架空データ',SRC)
 def test_three_stages(self):self.assertIn('frame//25',SRC)
 def test_no_network(self):
  imports=set()
  for n in ast.walk(TREE):
   if isinstance(n,ast.Import):imports.update(x.name.split('.')[0] for x in n.names)
   if isinstance(n,ast.ImportFrom):imports.add((n.module or '').split('.')[0])
  self.assertFalse(imports & {'requests','httpx','urllib','boto3'})
 def test_no_posting(self):
  names={n.name for n in ast.walk(TREE) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
  self.assertFalse(names & {'publish','post_video','upload_video','auto_post'})
 def test_no_media(self):self.assertFalse([p for p in ROOT.rglob('*') if p.suffix.lower() in {'.mp4','.png','.jpg','.wav','.aac'}])
if __name__=='__main__':unittest.main()
