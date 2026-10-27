"""Dependency-free CI tests for cycle909; full Pillow render/MP4 QA run locally."""
import ast
from pathlib import Path
import unittest
SRC=Path(__file__).with_name("input_output_bridge.py")
TEXT=SRC.read_text(encoding="utf-8")
TREE=ast.parse(TEXT)
VALUES={}
for n in TREE.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
  try: VALUES[n.targets[0].id]=ast.literal_eval(n.value)
  except (ValueError,TypeError): pass

class TestCycle909Policy(unittest.TestCase):
 def test_source_compiles(self): compile(TEXT,str(SRC),"exec")
 def test_ten_genres(self):
  self.assertEqual(len(VALUES["PALETTES"]),10)
  self.assertIn("ai_work",VALUES["PALETTES"])
 def test_87_frames(self):
  self.assertEqual(VALUES["FRAMES"],87)
  self.assertEqual(VALUES["FPS"],30)
 def test_native_panel(self): self.assertIn("W,H=952,1195",TEXT)
 def test_fiction_label(self):
  self.assertIn("架空",VALUES["DISCLAIMER"])
  self.assertIn("架空の例",TEXT)
 def test_approval_gate(self):
  self.assertIn("承認後に手動投稿",TEXT)
  self.assertIn("必ず確認",TEXT)
 def test_no_external_service(self):
  for bad in ("requests.post","urllib.request","api.tiktok.com","upload_video","publish_video","subprocess.run("):
   self.assertNotIn(bad,TEXT)
 def test_expected_steps(self):
  self.assertEqual(VALUES["LABELS"],("目的","条件","形式"))
  self.assertEqual(len(VALUES["INPUTS"]),len(VALUES["OUTPUTS"]))
 def test_render_api(self):
  funcs={n.name for n in TREE.body if isinstance(n,ast.FunctionDef)}
  self.assertIn("render_frame",funcs)
  self.assertIn("ease",funcs)

if __name__=="__main__": unittest.main()
