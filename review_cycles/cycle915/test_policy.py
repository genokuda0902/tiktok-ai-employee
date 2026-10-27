"""Offline CI: syntax, 10-genre config, safety gates; no private media needed."""
import ast
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'evidence_review.py'
CODE=SRC.read_text(encoding='utf-8')
TREE=ast.parse(CODE)

def literal_assignment(name):
 for node in TREE.body:
  if isinstance(node,ast.Assign):
   if any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
    return ast.literal_eval(node.value)
 raise AssertionError(f'missing {name}')

class TestCycle915(unittest.TestCase):
 def test_parses(self):self.assertIsInstance(TREE,ast.Module)
 def test_ten_genres(self):self.assertEqual(len(literal_assignment('GENRES')),10)
 def test_ai_work(self):self.assertIn('ai_work',literal_assignment('GENRES'))
 def test_pets(self):self.assertIn('pets',literal_assignment('GENRES'))
 def test_87_frames(self):self.assertIn('30,87,300,348',CODE)
 def test_safe_bottom(self):self.assertIn('Y0+H==1460',CODE)
 def test_original_fictional(self):self.assertIn('架空の画面',CODE)
 def test_progressive_three_stage(self):self.assertIn('stage=min(2,frame//29)',CODE)
 def test_no_network_import(self):
  imports=[]
  for n in ast.walk(TREE):
   if isinstance(n,ast.Import):imports.extend(x.name.split('.')[0] for x in n.names)
   if isinstance(n,ast.ImportFrom):imports.append((n.module or '').split('.')[0])
  self.assertFalse(set(imports)&{'requests','httpx','boto3','urllib','selenium'})
 def test_no_posting_function(self):
  names={n.name for n in ast.walk(TREE) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
  self.assertFalse(names&{'post_video','publish','upload_video','auto_post'})
 def test_no_media_committed(self):
  self.assertFalse([p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in {'.mp4','.wav','.aac','.png','.jpg','.jpeg'}])
 def test_no_secrets(self):
  self.assertNotIn('GITHUB_TOKEN',CODE)
  self.assertNotIn('TIKTOK_ACCESS_TOKEN',CODE)

if __name__=='__main__':unittest.main()
