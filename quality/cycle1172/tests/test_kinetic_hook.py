import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'kinetic_hook.py'
s=importlib.util.spec_from_file_location('kinetic_hook',P)
k=importlib.util.module_from_spec(s);s.loader.exec_module(k)

class HookTests(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(k.GENRES),10)
 def test_caption_protected(self):
  self.assertTrue(all(y+h<k.CAPTION_TOP-100 for x,y,w,h in k.CARDS))
 def test_three_distinct_reveals(self):
  self.assertEqual(len(k.STARTS),3)
  self.assertTrue(all(a<b for a,b in zip(k.STARTS,k.STARTS[1:])))
  self.assertLess(k.END,1.5)
 def test_filter_contains_each_label(self):
  g=k.filtergraph({'genre':'ai','hook_labels':['集計','確認','報告']})
  for word in ('集計','確認','報告'):self.assertIn(word,g)
  self.assertIn('between(t,0.18,1.43)',g)
 def test_reject_unknown_genre(self):
  with self.assertRaises(ValueError): k.validate({'genre':'illegal'},'/nonexistent')
 def test_fail_closed_policy(self):
  with self.assertRaises(ValueError): k.validate({},'/nonexistent')
 def test_all_palettes(self):
  for genre in k.GENRES:
   self.assertIn('drawtext',k.filtergraph({'genre':genre,'hook_labels':['集計','確認','報告']}))
 def test_font(self):self.assertTrue(Path(k.FONT).is_file())

if __name__=='__main__': unittest.main()
