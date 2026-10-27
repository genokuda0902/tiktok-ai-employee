"""Offline policy and 10-genre source checks. Stdlib only for free GitHub CI."""
import ast
from pathlib import Path
import unittest
SRC=Path(__file__).with_name('paper_report.py')
ROOT=Path(__file__).parent
TREE=ast.parse(SRC.read_text(encoding='utf-8'))
CODE=SRC.read_text(encoding='utf-8')

def literal_assignment(name):
 for node in TREE.body:
  if isinstance(node,ast.Assign):
   if any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
    return ast.literal_eval(node.value)
 raise AssertionError(f'no literal {name}')

class TestCycle914(unittest.TestCase):
 def test_source_parses(self):self.assertIsInstance(TREE,ast.Module)
 def test_ten_genres(self):self.assertEqual(len(literal_assignment('GENRES')),10)
 def test_genre_names(self):
  self.assertIn('ai_work',literal_assignment('GENRES'))
  self.assertIn('cooking',literal_assignment('GENRES'))
 def test_scene_geometry(self):
  values=None
  for node in TREE.body:
   if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Tuple):
    if any(isinstance(x,ast.Name) and x.id=='FRAMES' for x in node.targets[0].elts):
     values=ast.literal_eval(node.value)
  self.assertEqual(values,(1080,1160,30,87,300))
 def test_review_label(self):self.assertIn('架空の見本',CODE)
 def test_no_external_image(self):self.assertIn('np.random.default_rng(914)',CODE)
 def test_no_network_import(self):
  modules=[]
  for n in ast.walk(TREE):
   if isinstance(n,ast.Import):modules.extend(x.name for x in n.names)
   if isinstance(n,ast.ImportFrom):modules.append(n.module or '')
  self.assertFalse(set(modules)&{'requests','httpx','boto3','urllib','selenium'})
 def test_no_posting_function(self):
  names={n.name for n in ast.walk(TREE) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
  self.assertFalse(names&{'post_video','publish','upload_video','auto_post'})
 def test_only_text_source(self):
  media={'.mp4','.png','.jpg','.jpeg','.wav','.aac','.xlsx'}
  self.assertFalse([p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in media])
 def test_animation_is_progressive(self):self.assertIn('frame-i*25',CODE)
 def test_safe_boundary(self):self.assertIn('Y0+H==1460',CODE)
if __name__=='__main__':unittest.main()
