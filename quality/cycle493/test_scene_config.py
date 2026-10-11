import importlib.util, pathlib, unittest
P=pathlib.Path(__file__).resolve().parent/'scene_config.py'
s=importlib.util.spec_from_file_location('cycle493_config',P)
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
class Cycle493ContractTests(unittest.TestCase):
 def test_genres(self): self.assertEqual(len(c.GENRES),10)
 def test_vertical(self): self.assertEqual(c.RESOLUTION,(1080,1920))
 def test_scene_count(self): self.assertEqual(len(c.SCENES),6)
 def test_caption_segments(self): self.assertEqual(sum(len(x['clauses']) for x in c.SCENES),12)
 def test_safezone(self): self.assertLessEqual(c.SAFE_TEXT_BOX[2],875)
 def test_gate_rejects_proxy(self):
  q={'voice_native_japanese_verified':False,'full_decode':'PASS','resolution':[1080,1920],
     'human_review':'APPROVED','rights':'ORIGINAL_PROCEDURAL','publication':'MANUAL_POST_APPROVED'}
  self.assertFalse(c.release_gate(q))
 def test_gate_rejects_no_approval(self):
  q={'voice_native_japanese_verified':True,'full_decode':'PASS','resolution':[1080,1920],
     'human_review':'PENDING','rights':'ORIGINAL_PROCEDURAL','publication':'NOT_APPROVED'}
  self.assertFalse(c.release_gate(q))
 def test_gate_requires_all(self):
  q={'voice_native_japanese_verified':True,'full_decode':'PASS','resolution':[1080,1920],
     'human_review':'APPROVED','rights':'ORIGINAL_PROCEDURAL','publication':'MANUAL_POST_APPROVED'}
  self.assertTrue(c.release_gate(q))
if __name__=='__main__':unittest.main()
