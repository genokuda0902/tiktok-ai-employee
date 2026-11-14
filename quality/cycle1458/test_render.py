import unittest
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('render',Path(__file__).with_name('render.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestRenderer(unittest.TestCase):
    def test_three_scenes(self): self.assertEqual(len(m.SCENES),3)
    def test_safe_no_private_assets(self): self.assertTrue(all(len(x)==2 for x in m.SCENES))
    def test_no_false_voice_claim(self): self.assertIn('No Japanese speech',Path(m.__file__).read_text())
if __name__=='__main__': unittest.main()
