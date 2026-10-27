"""Offline stdlib-only CI gate; finished private MP4 is checked locally, not on CI."""
import ast
from pathlib import Path
import unittest

SRC=Path(__file__).with_name('evidence_wipe.py')
TEXT=SRC.read_text(encoding='utf-8')
TREE=ast.parse(TEXT)
VALUES={}
for node in TREE.body:
 if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
  try: VALUES[node.targets[0].id]=ast.literal_eval(node.value)
  except (ValueError,TypeError):pass
 if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Tuple):
  try:
   for target,value in zip(node.targets[0].elts,ast.literal_eval(node.value)):VALUES[target.id]=value
  except (ValueError,TypeError,AttributeError):pass

class PolicyTests(unittest.TestCase):
 def test_source_compiles(self):compile(TEXT,str(SRC),'exec')
 def test_ten_genres(self):self.assertEqual(len(VALUES['PALETTES']),10)
 def test_genre_labels(self):self.assertEqual(set(VALUES['PALETTES']),set(VALUES['GENRE_LABELS']))
 def test_duration(self):self.assertEqual(VALUES['END_FRAME']-VALUES['START_FRAME'],103)
 def test_end_frame(self):self.assertEqual(VALUES['END_FRAME'],691)
 def test_caption_safe_area(self):self.assertLess(VALUES['OVERLAY_Y']+VALUES['H'],VALUES['SUBTITLE_Y'])
 def test_publication_block(self):self.assertEqual(VALUES['POLICY'],'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED')
 def test_audio_copy(self):self.assertIn("'-c:a','copy'",TEXT)
 def test_source_sha_guard(self):self.assertIn('sha256(source)!=expected_sha',TEXT)
 def test_review_suffix(self):self.assertIn("REVIEW_ONLY.mp4",TEXT)
 def test_no_auto_post(self):self.assertNotIn('tiktok.upload',TEXT)
 def test_no_external_http(self):self.assertNotIn('requests.get',TEXT)
if __name__=='__main__':unittest.main()
