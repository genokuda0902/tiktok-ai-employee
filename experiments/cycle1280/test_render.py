import unittest
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("render",Path(__file__).with_name("render.py"))
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class ReviewContract(unittest.TestCase):
 def test_dimensions(self): self.assertEqual((mod.W,mod.H),(1080,1920))
 def test_duration(self): self.assertEqual(sum(s[2] for s in mod.SCENES),12)
 def test_scene_count(self): self.assertEqual(len(mod.SCENES),4)
 def test_no_external_asset_paths(self): self.assertTrue(all(isinstance(s[0],str) for s in mod.SCENES))
if __name__=="__main__":unittest.main()
