import unittest
from scene_contract import GENRES,SCENES,VALUES,validate,publication_gate
class ContractTest(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for g in GENRES:self.assertTrue(validate(g))
 def test_contiguous_timeline(self):
  self.assertEqual(SCENES[-1][1],600)
  self.assertEqual(sum(b-a for a,b,_,_ in SCENES),600)
 def test_numbers(self):
  self.assertEqual(sum(VALUES),720)
  with self.assertRaises(ValueError):validate(values=(120,150,200,240))
 def test_asset_rights_fail_closed(self):
  with self.assertRaises(PermissionError):validate(asset_manifest=[{'source':'unknown'}])
 def test_publication_gate(self):
  self.assertEqual(publication_gate(),'PUBLICATION_NOT_APPROVED')
  self.assertEqual(publication_gate(True,True,True,True,False),'PUBLICATION_NOT_APPROVED')
 def test_timeline_gap(self):
  bad=list(SCENES);bad[1]=(61,120,'test','problem')
  with self.assertRaises(ValueError):validate(scenes=bad)
 def test_caption_length(self):
  bad=list(SCENES);bad[1]=(60,120,'長'*21,'problem')
  with self.assertRaises(ValueError):validate(scenes=bad)
 def test_caption_dwell(self):
  bad=list(SCENES);bad[1]=(60,75,'short','problem')
  with self.assertRaises(ValueError):validate(scenes=bad)
if __name__=='__main__':unittest.main()
